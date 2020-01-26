from wpilib.command import CommandGroup
import commandbased.flowcontrol as fc

import robot

from .drivetrain.resettiltcommand import ResetTiltCommand

class StartUpCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Start Up')
        self.setRunWhenDisabled(True)

        self.addParallel(ResetTiltCommand())
