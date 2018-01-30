from wpilib.command import Command

import subsystems

class ElevateCommand(Command):

    def __init__(self):
        super().__init__('Elevate')

        self.requires(subsystems.elevator)


    def initialize(self):
        pass


    def execute(self):
        pass


    def end(self):
        pass
