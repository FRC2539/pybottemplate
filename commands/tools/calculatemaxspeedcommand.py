from wpilib.command.instantcommand import InstantCommand
from networktables import NetworkTables
import math

import subsystems

class CalculateMaxSpeedCommand(InstantCommand):

    def __init__(self):
        super().__init__('Calculate Max Speed')

        self.requires(subsystems.drivetrain)
        self.measuredSpeeds = []

        self.table = NetworkTables.getTable('DriveTrain')


    def initialize(self):
        for speed in subsystems.drivetrain.getSpeeds():
            self.measuredSpeeds.append(abs(speed))

        # Select the smallest max speed
        maxSpeed = min(self.measuredSpeeds)

        self.table.putValue('maxSpeed', math.floor(maxSpeed))
        self.table.putValue('normalSpeed', round(maxSpeed * 0.7))
        self.table.putValue('preciseSpeed', round(maxSpeed * 0.3))

        self.table.putValue('Speed/F', 1023 / maxSpeed)
