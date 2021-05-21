from __future__ import print_function

import builtins as __builtin__

import pprint

import inspect

from commands2 import SubsystemBase

from ctre import Orchestra

from networktables import NetworkTables

ALLOWPRINTS = True

printsDisabled = []

"""
This is a 'middle man' class. Subsystems should inherit from this class.
print control does indeed work, please use it. The network table crap kinda
doesn't work yet though. 

TODO: 
- Network table and subsystem integration. 
"""


def print(*args, **kwargs):
    if not inspect.stack()[1].filename in printsDisabled:
        return __builtin__.print(*args, **kwargs)


def disablePrints():
    caller = inspect.stack()[1].filename

    printsDisabled.append(str(caller))


def enablePrints():
    caller = inspect.stack()[1].filename

    try:
        printsDisabled.remove(str(caller))
    except (ValueError):
        pass


class CougarSystem(SubsystemBase):
    """
    A middle-man class between subsystems
    and the base subsystem. Please inherit
    from this class when writing a subsystem.
    Features easy networktable access and print
    control!
    """

    intialized = False

    orchestra = Orchestra()
    
    messageSystemTable = NetworkTables.getTable("MessagingSystem")
    messages = []
    messageSystemTable.putStringArray('messages', messages)

    def __init__(self, subsystemName="Unknown Subsystem"):

        super().__init__()

        self.tableName = subsystemName
        self.table = NetworkTables.getTable(self.tableName)

        self.updateThese = {}

        # Need to re-write the nt system.

        if not CougarSystem.intialized:
            self.intializeNTServer()
            CougarSystem.intialized = True

    def intializeNTServer(self):
        """
        Do not call this please. Only call once in the first CougarSystem init.
        """
        NetworkTables.initialize(server="roborio-2539-frc.local")

    def put(self, valueName, value):
        """
        Assigns a value to a networktable value
        with the corresponding key given!
        """
        try:
            self.table.putValue(valueName, value)

        except:  # Must be a list or tuple.

            try:
                if type(value[0]) is bool:
                    self.table.putBooleanArray(valueName, value)

                if type(value[0]) is str:
                    self.table.putStringArray(valueName, value)

                else:
                    self.table.putNumberArray(valueName, value)

            except (TypeError):
                raise Exception(
                    "Unrecognizable Data Type . . . \nShould be a: boolean, int, float, string, list of bools, \nlist of strings, list of numbers."
                )

    def get(self, valueName):
        """
        Get the value of the key with the
        given name.
        """
        return self.table.getValue(valueName, None)  # Returns None if it doesn't exist.

    def hasChanged(self, valueName, compareTo):
        """
        Has this networktable value changed?
        Returns true if the value you give does
        not equal the current value of the networktable.
        """
        if compareTo is None:
            return True
        return not self.table.getValue(valueName, None) == compareTo

    def delete(self, valueName):
        """
        Deletes the networktable key and value
        with the given value.
        """
        self.table.delete(valueName)

    def constantlyUpdate(self, valueName, call):
        """
        Constantly updates this networktable value so you
        don't have to! This is nice for something like a shooter'sRPM.
        The callable should take nothing (or use a lambda),
        and return the desired, updated value. For example, if
        you wanted RPM: "self.motor.getRPM", or
        something of the liking.
        """

        if not callable(call):
            raise Exception(
                "Please pass a callable! " + str(call) + ", is not callable!"
            )

        if not self.table.containsKey(valueName):
            self.put(valueName, call())

        self.updateThese[valueName] = call
        
    def sendMessage(self, message: str):
        """
        Sends a message to the driver station
        via networktables.
        """
        if len(CougarSystem.messages) > 99:
            CougarSystem.messages.pop(0)
            
        CougarSystem.messages.append(self.tableName + ': ' + message)

    @staticmethod
    def sendGeneralMessage(self, message: str):
        """
        Used in MessageCommand. Do not use for subsystems! Instead,
        use sendMessage(). 
        """
        if len(CougarSystem.messages) > 99:
            CougarSystem.messages.pop(0)
            
        CougarSystem.messages.append('Robot: ' + message)
        
    def feed(self):
        """
        Called in periodic. This does all the updating stuff needed!
        Do not call this yourself (unless it's in the periodic of
        course).
        """
        for key, value in self.updateThese.items():
            self.put(key, value())

    def addOrchestraInstrument(self, motor):
        """
        Add a falcon 500 to the robot's orchestra!
        """
        CougarSystem.orchestra.addInstrument(motor)

    def loadSong(self, fileName):
        """
        Prepares music file to play.
        """
        CougarSystem.orchestra.loadMusic("/home/lvuser/py/" + fileName)

    def playSong(self):
        """
        Play the loaded song.
        """
        CougarSystem.orchestra.play()

    def stopSong(self):
        """
        Stop the loaded song.
        """
        CougarSystem.orchestra.stop()

    def periodic(self):
        """
        Please remember to call self.feed if you override this!
        """
        self.feed()
