from commandbased import Command
from wpilib.preferences import Preferences

import subsystems
from controller import logicalaxes

logicalaxes.registerAxis('pivot')

class PivotCommand(Command):
    # Initialize the named command.
    def __init__(self, pivotSpeed):
        super().__init__('PivotCommand %s' % (pivotSpeed))
        
        self.requires(subsystems.shooter)
        self.pivotSpeed = pivotSpeed
    
    def execute(self):
        if(abs(logicalaxes.pivot.get()) == 1):
            print(logicalaxes.pivot.get())
            subsystems.shooter.pivot(logicalaxes.pivot.get() * self.pivotSpeed)
        else:
            subsystems.shooter.holdAt(subsystems.shooter.getHeight())
