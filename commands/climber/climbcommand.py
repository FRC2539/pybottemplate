from wpilib.command import Command

import subsystems

class ClimbCommand(Command):
    '''
    Start spinning the winch.
    '''

    def __init__(self):
        super().__init__('Climb')

        self.requires(subsystems.climber)


    def initialize(self):
        subsystems.climber.startWinch()


    def end(self):
        subsystems.climber.stopWinch()
