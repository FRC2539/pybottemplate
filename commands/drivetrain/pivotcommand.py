from .movecommand import MoveCommand

import subsystems
from custom.config import Config

import math


class PivotCommand(MoveCommand):
    '''Allows autonomous turning using the drive base encoders.'''

    def __init__(self, degrees, name=None):
        if name is None:
            name = 'Pivot %f degrees' % degrees

        super().__init__(degrees, name)


    def initialize(self):
        '''Calculates new positions by offseting the current ones.'''

        offset = self._calculateDisplacement()
        targetPositions = []
        for i, position in enumerate(subsystems.drivetrain.getPositions()):
            if self.distance > 0:
                if i % 2 == 0:
                    targetPositions.append(position + offset)
                else:
                    targetPositions.append(position)
            else:
                if i % 2 == 1:
                    targetPositions.append(position + offset)
                else:
                    targetPositions.append(position)

        subsystems.drivetrain.setPositions(targetPositions)

    def _calculateDisplacement(self):
        '''
        In order to avoid having a separate ticksPerDegree, we calculate it
        based on the width of the robot base.
        '''

        inchesPerDegree = math.pi * Config('DriveTrain/width') / 360
        totalDistanceInInches = self.distance * inchesPerDegree

        return totalDistanceInInches * Config('DriveTrain/ticksPerInch') * 2
