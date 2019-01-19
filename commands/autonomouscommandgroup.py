from wpilib.command import CommandGroup
import commandbased.flowcontrol as fc
from custom.config import Config

from commands.network.alertcommand import AlertCommand


class AutonomousCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Autonomous')

        AlertCommand(Config('cameraInfo/cargoX'), 'Info')
