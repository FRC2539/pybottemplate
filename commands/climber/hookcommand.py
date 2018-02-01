from wpilib.command import Command

import subsystems

class HookCommand(Command):
    '''
    Start spinning the winch.
    '''

    def __init__(self):
        super().__init__('Hook')

        self.requires(subsystems.climber)

    def initialize(self):
        subsystems.climber.hookDown()


    def end(self):
        subsystems.climber.stopHook()
