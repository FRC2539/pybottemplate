from commands.drivetrain.movecommand import MoveCommand
from networktables import NetworkTables

import robot
from custom.config import Config

class CalculateErrorCommand(MoveCommand):

    errors = []

    def __init__(self, direction=1):
        super().__init__(30 * direction, 'Calculate Error')

        self.requires(robot.drivetrain)
        Config('DriveTrain/ticksPerInch', 350)
        self.table = NetworkTables.getTable('DriveTrain/Speed')


    def initialize(self):
        self.table.putValue('P', 0)
        super().initialize()


    def isFinished(self):
        if not self.isTimedOut():
            return False

        speeds = robot.drivetrain.getSpeeds()
        for speed in speeds:
            if abs(speed) > 0.01:
                self.onTarget = 0
                return False

        self.onTarget += 1

        return self.onTarget > 5


    def end(self):
        self.errors.append(robot.drivetrain.averageError())

        avgError = sum(self.errors) / len(self.errors)
        self.table.putValue('P', 415 / avgError)
