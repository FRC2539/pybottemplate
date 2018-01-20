from wpilib.command.commandgroup import CommandGroup
import commandbased.flowcontrol as fc

from .setuseencoderscommand import SetUseEncodersCommand
from .moveycommand import MoveYCommand
from .calculatemaxspeedcommand import CalculateMaxSpeedCommand
from ..drivetrain.setspeedcommand import SetSpeedCommand
from wpilib.command.waitcommand import WaitCommand

from custom.config import Config

class ConfigurePIDCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Configure PID')

        setMaxSpeed = CalculateMaxSpeedCommand()

        self.addSequential(SetUseEncodersCommand(False))
        self.addSequential(MoveYCommand(1))
        self.addSequential(WaitCommand(2))
        self.addSequential(setMaxSpeed)
        self.addSequential(MoveYCommand(0))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(-1))
        self.addSequential(WaitCommand(2))
        self.addSequential(setMaxSpeed)
        self.addSequential(SetUseEncodersCommand(True))
        self.addSequential(SetSpeedCommand(Config('DriveTrain/normalSpeed')))
        self.addSequential(MoveYCommand(1))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(0))
        self.addSequential(WaitCommand(2))
        self.addSequential(SetSpeedCommand(Config('DriveTrain/preciseSpeed')))
        self.addSequential(MoveYCommand(1))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(0))
