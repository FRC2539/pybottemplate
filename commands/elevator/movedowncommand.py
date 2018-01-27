from wpilib.command.instantcommand import InstantCommand

import subsystems

class MoveDownCommand(InstantCommand):

    def __init__(self):
        super().__init__('Move Down')

        self.requires(subsystems.elevator)


    def initialize(self):
        pass
