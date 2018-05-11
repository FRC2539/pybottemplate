
from wpilib.command import Command

import robot

class RunIntoWallCommand(Command):
    '''Drives the robot at a steady speed until it crashes into something.'''

    def __init__(self, timelimit=None):
        super().__init__('Run Into Wall', timelimit)

        self.requires(robot.drivetrain)


    def initialize(self):
        robot.drivetrain.setProfile(0)
        robot.drivetrain.move(0, 1, 0)


    def isFinished(self):
        if self.isTimedOut():
            return True

        return abs(robot.drivetrain.getAcceleration()) > 1


    def end(self):
        robot.drivetrain.stop()
