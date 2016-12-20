from commandbased import Command
from custom.config import Config
import subsystems

class MoveAutonomousCommand(Command):
    def __init__(self, distance):
        super().__init__('MoveAutonomousCommand', 0.2)
        self.moveDistance = distance * float(Config("DriveTrain/ticksPerInch"))
        self.requires(subsystems.drivetrain)
    
    def initialize(self):
        targetPositions = []
        sign = 1
        for position in subsystems.drivetrain.getPositions():
            targetPositions.append(position + self.moveDistance * sign)
            sign *= -1

        subsystems.drivetrain.setPositions(targetPositions)
    
    def isFinished(self):
        return self.isTimedOut() and subsystems.drivetrain.atPosition()
    
    def end(self):
        subsystems.drivetrain.stop()
        
