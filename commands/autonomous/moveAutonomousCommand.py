from commandbased import Command
from wpilib.preferences import Preferences
from wpilib.cantalon import CANTalon

import subsystems
from controller import logicalaxes

class MoveAutonomousCommand(Command):
    def __init__(self):
        super().__init__('MoveAutonomousCommand')
        self.targetPosition = 0
        self.requires(subsystems.drivetrain)
    
    def initialize(self):
        self.targetPosition = subsystems.drivetrain.getPosition + subsystems.drivetrain.ticksPerRotation
        subsystems.drivetrain._setMode(CANTalon.ControlMode.Position)
        subsystems.drivetrain.moveForRotations(1)
    
    def isFinished(self):
        if abs(subsystems.drivetrain.getPosition - self.targetPosition) < 10:
            return True
    
    def end(self):
        subsystems.drivetrain._setMode(CANTalon.ControlMode.Speed)
        
