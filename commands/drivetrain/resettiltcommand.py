from commands2 import InstantCommand

import robot


class ResetTiltCommand(InstantCommand):
    def __init__(self):
        super().__init__()

        self.addRequirements(robot.drivetrain)

    def initialize(self):
        robot.drivetrain.resetTilt()
