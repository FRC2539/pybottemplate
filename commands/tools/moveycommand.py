from wpilib.command.instantcommand import InstantCommand

import subsystems

class MoveYCommand(InstantCommand):

    def __init__(self):
        super().__init__('Move Y')

        self.requires(subsystems.drivetrain)


    def initialize(self):
        pass
