from wpilib.command.subsystem import Subsystem

from controller.logitechdualshock import LogitechDualShock
from controller import logicalaxes

from custom.config import Config

from commands.drivecommand import DriveCommand

class OI(Subsystem):
    '''Handles joystick (operator input) interaction with the commands.'''

    def __init__(self):
        '''
        Declare all controllers, assign axes to logical axes, and trigger
        commands on various button events. Available event types are:
         - whenPressed
         - whileHeld: cancelled when the button is released
         - whenReleased
         - toggleWhenPressed: start on first press, cancel on next
         - cancelWhenPressed: good for commands started with a different button
        '''

        super().__init__('OI')
        self.mainController = LogitechDualShock(0)

        logicalaxes.driveX = self.mainController.LeftX
        logicalaxes.driveY = self.mainController.LeftY
        logicalaxes.driveRotate = self.mainController.RightX

        self.mainController.X.toggleWhenPressed(DriveCommand(Config('DriveTrain/preciseMaxSpeed')))

        self.backupController = LogitechDualShock(1)
