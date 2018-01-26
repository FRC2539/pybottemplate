from commands.drivetrain.movecommand import MoveCommand
from networktables import NetworkTables

import subsystems
from custom.config import Config

class CalculateErrorCommand(MoveCommand):

    errors = []

    def __init__(self, direction=1):
        super().__init__(30 * direction, 'Calculate Error')

        self.requires(subsystems.drivetrain)
        Config('DriveTrain/ticksPerInch', 350)
        self.table = NetworkTables.getTable('DriveTrain/Speed')


    def isFinished(self):
        if not self.isTimedOut():
            return False

        speeds = subsystems.drivetrain.getSpeeds()
        for speed in speeds:
            if abs(speed) > 0.01:
                return False

        return True


    def end(self):
        self.errors.append(subsystems.drivetrain.averageError())

        self.table.putValue('P', sum(self.errors) / len(self.errors))
