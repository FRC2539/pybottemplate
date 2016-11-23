from commandbased import Command

import subsystems

class IntakeCommand(Command):
    # Initialize the named command.
    def __init__(self, intakeSpeed):
        super().__init__('IntakeCommand %s' % (intakeSpeed))
        
        self.requires(subsystems.shooter)
        self.intakeSpeed = intakeSpeed
    
    def initialize(self):
        subsystems.shooter.setShooterSpeed(-self.intakeSpeed)
    
    def end(self):
        subsystems.shooter.stopShooter()
