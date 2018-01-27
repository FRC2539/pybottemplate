from wpilib.command.instantcommand import InstantCommand

import subsystems

class MoveUpCommand(InstantCommand):

    def __init__(self):
        super().__init__('Move Up')

        self.requires(subsystems.elevator)


    def initialize(self):
        pass
