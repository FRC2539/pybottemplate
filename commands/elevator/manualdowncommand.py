from wpilib.command.command import Command

import subsystems

class ManualDownCommand(Command):

    def __init__(self):
        super().__init__('Manual Down')

        self.requires(subsystems.elevator)


    def initialize(self):
        pass


    def execute(self):
        pass


    def end(self):
        pass
