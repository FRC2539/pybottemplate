from wpilib.command.instantcommand import InstantCommand

import robot

class MoveYCommand(InstantCommand):

    def __init__(self, y):
        super().__init__('Move Y')

        self.requires(robot.drivetrain)
        self.y = y


    def initialize(self):
        robot.drivetrain.move(0, self.y, 0)
