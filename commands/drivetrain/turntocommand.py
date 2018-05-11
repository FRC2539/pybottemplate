from .turncommand import TurnCommand

import robot

class TurnToCommand(TurnCommand):
    '''Turn to a specified angle using the gyroscope.'''

    def __init__(self, targetDegrees):
        super().__init__(
            targetDegrees,
            'Turn to %f degrees' % targetDegrees
        )

        self.targetDegrees = targetDegrees


    def initialize(self):
        self.distance = robot.drivetrain.getAngleTo(self.targetDegrees)

        super().initialize()
