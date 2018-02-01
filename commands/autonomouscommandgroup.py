from wpilib.command import CommandGroup
import commandbased.flowcontrol as fc
from custom.config import Config


class AutonomousCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Autonomous')
