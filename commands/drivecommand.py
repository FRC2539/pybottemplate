from commandbased import Command
from wpilib.preferences import Preferences

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
        try:
            speedLimit = int(self.speedLimit)
        except ValueError:
            speedLimit = Preferences.getInstance().getInt(self.speedLimit, 1)

        subsystems.drivetrain.setSpeedLimit(speedLimit)

    def execute(self):
        subsystems.drivetrain.move(
            logicalaxes.driveX.get(),
            logicalaxes.driveY.get(),
            logicalaxes.driveRotate.get()
        )
