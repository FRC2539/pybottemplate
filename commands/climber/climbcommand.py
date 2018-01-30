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
        subsystems.climber.start()


    def end(self):
        subsystems.climber.stop()
