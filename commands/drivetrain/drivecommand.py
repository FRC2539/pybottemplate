from wpilib.command import Command

import subsystems
from controller import logicalaxes

logicalaxes.registerAxis('driveX')
logicalaxes.registerAxis('driveY')
logicalaxes.registerAxis('driveRotate')

class DriveCommand(Command):
    def __init__(self, speedLimit):
        super().__init__('DriveCommand %s' % speedLimit)

        self.requires(subsystems.drivetrain)
        self.speedLimit = speedLimit


    def initialize(self):
        subsystems.drivetrain.stop()
        subsystems.drivetrain.setProfile(0)
        try:
            subsystems.drivetrain.setSpeedLimit(self.speedLimit)
        except ZeroDivisionError:
            print('Could not set speed to %f' % self.speedLimit)


    def execute(self):
        subsystems.drivetrain.move(
            logicalaxes.driveX.get(),
            logicalaxes.driveY.get(),
            logicalaxes.driveRotate.get()
        )
