from wpilib.command import Command

import subsystems

class UnhookCommand(Command):
    '''
    Start spinning the winch.
    '''

    def __init__(self):
        super().__init__('Unhook')

        self.requires(subsystems.climber)


    def initialize(self):
        subsystems.climber.hookUp()


    def end(self):
        subsystems.climber.stopHook()
