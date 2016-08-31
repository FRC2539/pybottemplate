from wpilib.command.commandgroup import CommandGroup

class DefaultAutonomousCommandGroup(CommandGroup):
    '''A generic standby, the trusty do-nothing automomous mode.'''

    def __init__(self):
        super().__init__('DefaultAutonomous')
