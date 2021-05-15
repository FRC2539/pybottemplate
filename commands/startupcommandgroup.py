from commands2 import ParallelCommandGroup

import robot

from .drivetrain.resettiltcommand import ResetTiltCommand

class StartUpCommandGroup(ParallelCommandGroup):

    def __init__(self):
        super().__init__()

        robot.drivetrain.initDefaultCommand()

        self.addCommands(ResetTiltCommand())

    def runsWhenDisabled(self):
        return True
