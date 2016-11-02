from commandbased import Command

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
        subsystems.shooter.pivot(logicalaxes.pivot.get() * self.pivotSpeed)
