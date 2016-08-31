from wpilib.command.subsystem import Subsystem

from commands.monitorcommand import MonitorCommand

class Monitor(Subsystem):
    '''Exists to observe system state via its default command.'''

    def __init__(self):
        super().__init__('Monitor')


    def initDefaultCommand(self):
        self.setDefaultCommand(MonitorCommand())

