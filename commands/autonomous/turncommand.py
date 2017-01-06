from .movecommand import MoveCommand

import subsystems
from custom.config import Config

import math


class TurnCommand(MoveCommand):
    '''Allows autonomous turning using the drive base encoders.'''

    def __init__(self, degrees):
        super().__init__(degrees, 'Turn %f degrees' % degrees)


    def initialize(self):
        '''Calculates new positions by offseting the current ones.'''

        newPositions = []
        displacement = self._calculateDisplacement()
        for position in subsystems.drivetrain.getPositions():
            newPositions.append(position + displacement)

        subsystems.drivetrain.setPositions(newPositions)


    def _calculateDisplacement(self):
        '''
        In order to avoid having a separate ticksPerDegree, we calculate it
        based on the width of the robot base.
        '''

        inchesPerDegree = math.pi * Config('DriveTrain/width') / 360
        totalDistanceInInches = self.distance * inchesPerDegree

        return totalDistanceInInches * Config('DriveTrain/ticksPerInch')
