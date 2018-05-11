from wpilib.command.instantcommand import InstantCommand

import robot

class ZeroGyroCommand(InstantCommand):

    def __init__(self):
        super().__init__('Zero Gyro')

        self.requires(robot.drivetrain)


    def initialize(self):
        robot.drivetrain.resetGyro()
