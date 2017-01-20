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
        subsystems.drivetrain.setSpeedLimit(self.speedLimit)
        subsystems.drivetrain.setUseEncoders(False)


    def execute(self):
        subsystems.drivetrain.move(
            logicalaxes.driveX.get(),
            logicalaxes.driveY.get(),
            logicalaxes.driveRotate.get()
        )


    def end(self):
        subsystems.drivetrain.setUseEncoders()
