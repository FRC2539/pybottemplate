
from wpilib.command import Command

import subsystems

class RunIntoWallCommand(Command):
    '''Drives the robot at a steady speed until it crashes into something.'''

    def __init__(self, timelimit=None):
        super().__init__('Run Into Wall', timelimit)

        self.requires(subsystems.drivetrain)


    def initialize(self):
        subsystems.drivetrain.setProfile(0)
        subsystems.drivetrain.move(0, 1, 0)


    def isFinished(self):
        if self.isTimedOut():
            return True

        return abs(subsystems.drivetrain.getAcceleration()) > 1


    def end(self):
        subsystems.drivetrain.stop()
