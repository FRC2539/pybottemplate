from commandbased import Command
from wpilib.preferences import Preferences
from wpilib.cantalon import CANTalon

import subsystems
from controller import logicalaxes

class MoveAutonomousCommand(Command):
    def __init__(self):
        super().__init__('MoveAutonomousCommand')
        self.moveDistance = 100
        self.requires(subsystems.drivetrain)
    
    def initialize(self):
        self.targetPositions = subsystems.drivetrain.getPositions()
        for position in self.targetPositions:
            position += self.moveDistance
        subsystems.drivetrain.setPositions(self.targetPositions)
    
    def isFinished(self):
        return subsystems.drivetrain.atPosition()
    
    def end(self):
        subsystems.drivetrain.stop()
        
