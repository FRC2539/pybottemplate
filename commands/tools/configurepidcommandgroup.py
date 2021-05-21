from commands2 import SequentialCommandGroup, WaitCommand, PrintCommand

from .setuseencoderscommand import SetUseEncodersCommand
from .moveycommand import MoveYCommand
from .resetpidcommand import ResetPIDCommand
from .calculatemaxspeedcommand import CalculateMaxSpeedCommand
from .calculateerrorcommand import CalculateErrorCommand
from commands.drivetrain.setspeedcommand import SetSpeedCommand

from custom.config import Config


class ConfigurePIDCommandGroup(SequentialCommandGroup):
    def __init__(self):

        output = """
Your F and P values have been configured. However, P is probably too small.
Use MoveCommand to drive the robot a set distance. (If you have not already done
so, calculate and set Encoder Ticks per Inch.) Keep doubling the P value until
the robot noticeably oscillates during its movement. To correct this
oscillation, set a D value of 10 times P.

Run the MoveCommand again and note the error. Set your I Zone value to twice the
error. Then set an I value of 0.001. Run the MoveCommand and increase I until
the average error is less than 10.

For details see the Motion Magic Closed-Loop Walkthrough section of the Talon
SRX Software Reference Manual.
        """

        super().__init__()

        # self.addCommands(
        #     AlertCommand("Do not disable the robot!"),
        #     WaitCommand(1),
        #     AlertCommand("Enable netconsole for details", "Info"),
        #     WaitCommand(2),
        #     PrintCommand("Zeroing PID Values"),
        #     ResetPIDCommand(),
        #     PrintCommand("Calculating Max Speed"),
        #     SetUseEncodersCommand(False),
        #     MoveYCommand(1),
        #     WaitCommand(2),
        #     CalculateMaxSpeedCommand(),
        #     MoveYCommand(0),
        #     WaitCommand(2),
        #     MoveYCommand(-1),
        #     WaitCommand(2),
        #     CalculateMaxSpeedCommand(),
        #     PrintCommand("Testing PID driving"),
        #     SetUseEncodersCommand(True),
        #     SetSpeedCommand(Config("DriveTrain/normalSpeed")),
        #     MoveYCommand(1),
        #     WaitCommand(2),
        #     MoveYCommand(0),
        #     WaitCommand(2),
        #     SetSpeedCommand(Config("DriveTrain/preciseSpeed")),
        #     MoveYCommand(-1),
        #     WaitCommand(2),
        #     MoveYCommand(0),
        #     WaitCommand(2),
        #     PrintCommand("Generating starting P value"),
        #     CalculateErrorCommand(1),
        #     CalculateErrorCommand(-1),
        #     PrintCommand(output.strip()),
        #     AlertCommand("You may now disable the robot", "Info"),
        # )
