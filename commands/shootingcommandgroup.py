from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand
from .shootercommand import ShooterCommand
from .indexcommand import IndexCommand


class ShootingCommandGroup(CommandGroup):
    # Initialize the named command.
    def __init__(self):
        super().__init__('ShootingCommandGroup')
        self.addParallel(ShooterCommand(10000))
        self.addSequential(WaitCommand(3))
        self.addSequential(IndexCommand(10000))
