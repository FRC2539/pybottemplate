from wpilib.command.instantcommand import InstantCommand

import subsystems

class CalculateMaxSpeedCommand(InstantCommand):

    def __init__(self):
        super().__init__('Calculate Max Speed')

        self.requires(subsystems.drivetrain)


    def initialize(self):
        pass
