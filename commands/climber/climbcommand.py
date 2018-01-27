from wpilib.command import Command
from networktables import NetworkTables

import subsystems
from custom import driverhud

class ClimbCommand(Command):
    '''
    Start spinning the winch.
    '''

    def __init__(self):
        super().__init__('Climb')

        self.requires(subsystems.climber)


    def initialize(self):
        if not subsystems.climber.atTop():
            subsystems.climber.start()
        else:
            driverhud.showAlert('Already at top')


    def isFinished(self):
        return subsystems.climber.atTop()


    def end(self):
        subsystems.climber.stop()
