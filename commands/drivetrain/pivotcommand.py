from .turncommand import TurnCommand

import robot
from custom.config import Config

import math


class PivotCommand(TurnCommand):
    """Allows autonomous turning using the drive base encoders."""

    def __init__(self, degrees, reverse=False, name=None):
        if name is None:
            name = "Pivot %f degrees" % degrees

        super().__init__(degrees, name)

        # 0 = Left Side, 1 = Right Side
        self.pivotSide = 0
        if degrees < 0:
            self.pivotSide = 1

        if reverse:
            self.pivotSide = abs(self.pivotSide - 1)

    def initialize(self):
        """Calculates new positions by offsetting the current ones."""

        offset = self._calculateDisplacement() * 2
        targetPositions = []
        for i, position in enumerate(robot.drivetrain.getPositions()):
            side = i % 2
            if self.pivotSide == side:
                position += offset

            targetPositions.append(position)

        robot.drivetrain.setPositions(targetPositions)
