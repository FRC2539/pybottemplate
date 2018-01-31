from .logitechdualshock import LogitechDualShock
from . import logicalaxes

from custom.config import Config

from commands.drivetrain.drivecommand import DriveCommand
from commands.resetcommand import ResetCommand
from commands.intake.intakecommand import IntakeCommand
from commands.intake.outtakecommand import OuttakeCommand

from commands.elevator.elevatecommand import ElevateCommand
from commands.elevator.deelevatecommand import DeelevateCommand
from commands.climber.climbcommand import ClimbCommand
from commands.climber.hookcommand import HookCommand
from commands.climber.unhookcommand import UnhookCommand


def init():
    '''
    Declare all controllers, assign axes to logical axes, and trigger
    commands on various button events. Available event types are:
        - whenPressed
        - whileHeld: cancelled when the button is released
        - whenReleased
        - toggleWhenPressed: start on first press, cancel on next
        - cancelWhenPressed: good for commands started with a different button
    '''

    mainController = LogitechDualShock(0)

    logicalaxes.driveX = mainController.LeftX
    logicalaxes.driveY = mainController.LeftY
    logicalaxes.driveRotate = mainController.RightX

    mainController.Back.whenPressed(ResetCommand())

    mainController.X.toggleWhenPressed(DriveCommand(Config('DriveTrain/preciseSpeed')))
    mainController.A.toggleWhenPressed(IntakeCommand())
    mainController.B.toggleWhenPressed(OuttakeCommand())
    mainController.Y.whileHeld(ClimbCommand())

    mainController.LeftTrigger.whileHeld(DeelevateCommand())
    mainController.LeftBumper.whileHeld(ElevateCommand())
    mainController.RightTrigger.whileHeld(HookCommand())
    mainController.RightBumper.whileHeld(UnhookCommand())

    backupController = LogitechDualShock(1)

    backupController.Back.whenPressed(ResetCommand())

    backupController.X.toggleWhenPressed(DriveCommand(Config('DriveTrain/preciseSpeed')))
    backupController.A.toggleWhenPressed(IntakeCommand())
    backupController.B.toggleWhenPressed(OuttakeCommand())
    backupController.Y.whileHeld(ClimbCommand())

    backupController.LeftTrigger.whileHeld(DeelevateCommand())
    backupController.LeftBumper.whileHeld(ElevateCommand())
    backupController.RightTrigger.whileHeld(HookCommand())
    backupController.RightBumper.whileHeld(UnhookCommand())
