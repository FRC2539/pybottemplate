from wpilib.command import Command

import subsystems

class RunIntoWallCommand(Command):
    '''Drives the robot at a steady speed until it crashes into something.'''

    def __init__(self, speedLimit, timelimit=None):
        super().__init__('Run Into Wall', timelimit)

        self.requires(subsystems.drivetrain)
        self.speedLimit = speedLimit


    def initialize(self):
        subsystems.drivetrain.setUseEncoders(False)

        subsystems.drivetrain.setSpeedLimit(self.speedLimit)
        subsystems.drivetrain.move(0, 1, 0)


    def isFinished(self):
        return abs(subsystems.drivetrain.getAcceleration()) > 0.5


    def end(self):
        subsystems.drivetrain.stop()
