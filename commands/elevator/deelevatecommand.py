from wpilib.command import Command

import subsystems

class DeelevateCommand(Command):

    def __init__(self):
        super().__init__('Deelevate')

        self.requires(subsystems.elevator)


    def initialize(self):
        pass


    def execute(self):
        pass


    def end(self):
        pass
