from wpilib.command.instantcommand import InstantCommand

import subsystems

class MoveYCommand(InstantCommand):

    def __init__(self, y):
        super().__init__('Move Y')

        self.requires(subsystems.drivetrain)
        self.y = y


    def initialize(self):
        subsystems.drivetrain.move(0, self.y, 0)
