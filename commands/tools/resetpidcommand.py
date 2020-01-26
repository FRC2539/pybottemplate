from wpilib.command import InstantCommand

import robot

class ResetPIDCommand(InstantCommand):

    def __init__(self):
        super().__init__('Reset PID values')

        self.requires(robot.drivetrain)


    def initialize(self):
        robot.drivetrain.resetPID()
