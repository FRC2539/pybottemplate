from wpilib.command.instantcommand import InstantCommand

import robot

class ResetTiltCommand(InstantCommand):

    def __init__(self):
        super().__init__('Set Tilt to 0')

        self.requires(robot.drivetrain)
        self.setRunWhenDisabled(True)


    def initialize(self):
        robot.drivetrain.resetTilt()
