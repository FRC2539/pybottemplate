from wpilib.command import Command
from custom.config import Config
import subsystems

class MoveCommand(Command):

    def __init__(self, distance, name=None):
        '''
        Takes a distance in inches and stores it for later. We allow overriding
        name so that other autonomous driving commands can extend this class.
        '''

        if name is None:
            name = 'Move %f inches' % distance

        super().__init__(name, 0.2)

        self.distance = distance
        self.requires(subsystems.drivetrain)


    def initialize(self):
        self.onTarget = 0
        offset = self.distance * Config('DriveTrain/ticksPerInch')
        targetPositions = []
        sign = 1
        for position in subsystems.drivetrain.getPositions():
            targetPositions.append(position + offset * sign)
            sign *= -1

        subsystems.drivetrain.setPositions(targetPositions)


    def isFinished(self):
        if self.isTimedOut() and subsystems.drivetrain.atPosition():
            self.onTarget += 1
        else:
            self.onTarget = 0

        return self.onTarget > 5
