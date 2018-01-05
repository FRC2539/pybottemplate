from wpilib.command.instantcommand import InstantCommand

import subsystems

class SetSpeedCommand(InstantCommand):
    '''Changes the max speed of the drive subsystem.'''

    def __init__(self, speed):
        super().__init__('Set Speed To %d' % speed)
        self.speed = speed


    def initialize(self):
        subsystems.drivetrain.setSpeedLimit(self.speed)
