from commandbased import Command

import subsystems

class ShooterCommand(Command):
    # Initialize the named command.
    def __init__(self, shootingSpeed):
        super().__init__('ShootingCommand %s' % (shootingSpeed))
        
        self.requires(subsystems.shooter)
        self.shootingSpeed = shootingSpeed
    
    def initialize(self):
        subsystems.shooter.setShooterSpeed(self.shootingSpeed)
        subsystems.shooter.setShooterIsDone(False)
    
    def isFinished(self):
        return subsystems.shooter.isShooterDone()
        
