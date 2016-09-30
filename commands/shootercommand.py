from commandbased import Command

import subsystems

from controller import logicalaxes

logicalaxes.registerAxis('pivot')

class ShooterCommand(Command):
    # Initialize the named command.
    def __init__(self):
        super().__init__('ShooterCommand')
        
        self.requires(subsystems.shooter)
    
    
    
    def execute(self):
        subsystems.shooter.pivot(
            logicalaxes.pivot.get()
        )
