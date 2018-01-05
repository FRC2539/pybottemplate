from wpilib.command import CommandGroup
import commandbased.flowcontrol as fc


class AutonomousCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Autonomous')
