from commandbased import TimedCommand

import subsystems

class IndexCommand(TimedCommand):
    # Initialize the named command.
    def __init__(self, indexSpeed):
        super().__init__('ShootingCommand %s' % (indexSpeed), 1)
        
        self.requires(subsystems.shooter)
        self.indexSpeed = indexSpeed
    
    def initialize(self):
        subsystems.shooter.setIndexerSpeed(self.indexSpeed)
    
    def end(self):
        subsystems.shooter.setIndexerSpeed(0)
        subsystems.shooter.setShooterSpeed(0)
        subsystems.shooter.setShooterIsDone(True)
