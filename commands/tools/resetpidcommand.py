from wpilib.command.instantcommand import InstantCommand

import subsystems

class ResetPIDCommand(InstantCommand):

    def __init__(self):
        super().__init__('Reset PID values')

        self.requires(subsystems.drivetrain)


    def initialize(self):
        subsystems.drivetrain.resetPID()
