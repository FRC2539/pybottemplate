from wpilib.command.instantcommand import InstantCommand

import robot

class SetSpeedCommand(InstantCommand):
    '''Changes the max speed of the drive subsystem.'''

    def __init__(self, speed):
        super().__init__('Set Speed To %s' % speed)
        self.speed = speed


    def initialize(self):
        robot.drivetrain.setSpeedLimit(self.speed)
