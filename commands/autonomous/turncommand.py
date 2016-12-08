from commandbased import Command

import subsystems
from custom.config import Config

import math


class TurnCommand(Command):
    '''Allows autonomous turning using the drive base encoders.'''

    def __init__(self, degrees):
        super().__init__('Turn %d degrees' % degrees)

        self.degrees = degrees

        self.requires(subsystems.drivetrain)


    def initialize(self):
        '''Calculates new positions by offseting the current ones.'''

        newPositions = []
        displacement = self._calculateDisplacement()
        for position in subsystems.drivetrain.getPositions():
            newPositions.append(position + displacement)

        subsystems.drivetrain.setPositions(newPositions)


    def isFinished(self):
        return subsystems.drivetrain.atPosition()


    def _calculateDisplacement(self):
        '''
        In order to avoid having a separate ticksPerDegree, we calculate it
        based on the width of the robot base.
        '''

        inchesPerDegree = math.pi * Config('DriveTrain/width') / 360
        totalDistanceInInches = self.degrees * inchesPerDegree

        return totalDistanceInInches * Config('DriveTrain/ticksPerInch')
