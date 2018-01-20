from wpilib.command.instantcommand import InstantCommand

import subsystems

class SetUseEncodersCommand(InstantCommand):

    def __init__(self):
        super().__init__('Set Use Encoders')

        self.requires(subsystems.drivetrain)


    def initialize(self):
        pass
