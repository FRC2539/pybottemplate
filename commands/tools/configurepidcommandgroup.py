from wpilib.command import CommandGroup, WaitCommand, PrintCommand
import commandbased.flowcontrol as fc

from .setuseencoderscommand import SetUseEncodersCommand
from .moveycommand import MoveYCommand
from .resetpidcommand import ResetPIDCommand
from .calculatemaxspeedcommand import CalculateMaxSpeedCommand
from .calculateerrorcommand import CalculateErrorCommand
from commands.drivetrain.setspeedcommand import SetSpeedCommand
from commands.network.alertcommand import AlertCommand

from custom.config import Config

class ConfigurePIDCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Configure PID')

        output = '''
Your F and P values have been configured. However, P is probably too small.
Use MoveCommand to drive the robot a set distance. (If you have not already done
so, calculate and set Encoder Tickes per Inch.) Keep doubling the P value until
the robot noticeably oscillates during its movement. To correct this
oscillation, set a D value of 10 times P.

Run the MoveCommand again and note the error. Set your I Zone value to twice the
error. Then set an I value of 0.001. Run the MoveCommand and increase I until
the average error is less than 10.

For details see the Motion Magic Closed-Loop Walkthrough section of the Talon
SRX Software Reference Manual.
        '''

        self.addSequential(AlertCommand('Do not disable the robot!'))
        self.addSequential(WaitCommand(1))
        self.addSequential(
            AlertCommand('Enable netconsole for details', 'Info')
        )
        self.addSequential(WaitCommand(2))
        self.addSequential(PrintCommand('Zeroing PID Values'))
        self.addSequential(ResetPIDCommand())
        self.addSequential(PrintCommand('Calculating Max Speed'))
        self.addSequential(SetUseEncodersCommand(False))
        self.addSequential(MoveYCommand(1))
        self.addSequential(WaitCommand(2))
        self.addSequential(CalculateMaxSpeedCommand())
        self.addSequential(MoveYCommand(0))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(-1))
        self.addSequential(WaitCommand(2))
        self.addSequential(CalculateMaxSpeedCommand())
        self.addSequential(PrintCommand('Testing PID driving'))
        self.addSequential(SetUseEncodersCommand(True))
        self.addSequential(SetSpeedCommand(Config('DriveTrain/normalSpeed')))
        self.addSequential(MoveYCommand(1))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(0))
        self.addSequential(WaitCommand(2))
        self.addSequential(SetSpeedCommand(Config('DriveTrain/preciseSpeed')))
        self.addSequential(MoveYCommand(-1))
        self.addSequential(WaitCommand(2))
        self.addSequential(MoveYCommand(0))
        self.addSequential(WaitCommand(2))
        self.addSequential(PrintCommand('Generating starting P value'))
        self.addSequential(CalculateErrorCommand(1))
        self.addSequential(CalculateErrorCommand(-1))
        self.addSequential(PrintCommand(output.strip()))
        self.addSequential(
            AlertCommand('You may now disable the robot', 'Info')
        )
