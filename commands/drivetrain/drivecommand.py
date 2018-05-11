from wpilib.command import Command

import robot
from controller import logicalaxes
from custom.config import Config, MissingConfigError
import math

logicalaxes.registerAxis('driveX')
logicalaxes.registerAxis('driveY')
logicalaxes.registerAxis('driveRotate')

class DriveCommand(Command):
    def __init__(self, speedLimit):
        super().__init__('DriveCommand %s' % speedLimit)

        self.requires(robot.drivetrain)
        self.speedLimit = speedLimit


    def initialize(self):
        robot.drivetrain.stop()
        robot.drivetrain.setProfile(0)
        try:
            robot.drivetrain.setSpeedLimit(self.speedLimit)
        except (ValueError, MissingConfigError):
            print('Could not set speed to %s' % self.speedLimit)
            robot.drivetrain.enableSimpleDriving()

        self.lastY = None
        self.slowed = False


    def execute(self):
        # Avoid quick changes in direction
        y = logicalaxes.driveY.get()
        if self.lastY is None:
            self.lastY = y
        else:
            cooldown = 0.05
            self.lastY -= math.copysign(cooldown, self.lastY)

            # If the sign has changed, don't move
            if self.lastY * y < 0:
                y = 0

            if abs(y) > abs(self.lastY):
                self.lastY = y

        tilt = robot.drivetrain.getTilt()
        correction = tilt / 20
        if abs(correction) < 0.2:
            correction = 0

        robot.drivetrain.move(
            logicalaxes.driveX.get(),
            y - correction,
            logicalaxes.driveRotate.get()
        )
