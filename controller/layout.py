from .logitechdualshock import LogitechDualShock
from . import logicalaxes

from custom.config import Config

from commands.drivetrain.drivecommand import DriveCommand
from commands.resetcommand import ResetCommand
from commands.tools.configurepidcommandgroup import ConfigurePIDCommandGroup
from commands.intake.intakecommand import IntakeCommand
from commands.intake.outtakecommand import OuttakeCommand
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

    mainController.X.toggleWhenPressed(DriveCommand(Config('DriveTrain/preciseSpeed')))
    mainController.Back.whenPressed(ResetCommand())
    mainController.B.toggleWhenPressed(IntakeCommand())
    mainController.Y.toggleWhenPressed(OuttakeCommand())
    #mainController.Y.whenPressed(ConfigurePIDCommandGroup())


    backupController = LogitechDualShock(1)
