from wpilib.command.instantcommand import InstantCommand

import robot
from custom.config import Config
from networktables import NetworkTables

class SetUseEncodersCommand(InstantCommand):

    def __init__(self, encodersEnabled):
        super().__init__('Set Use Encoders')

        self.requires(robot.drivetrain)
        self.encodersEnabled = encodersEnabled


    def initialize(self):
        robot.drivetrain.setUseEncoders(self.encodersEnabled)
        if not self.encodersEnabled:
            maxSpeed = Config('DriveTrain/maxSpeed')
            if not maxSpeed:
                dt = NetworkTables.getTable('DriveTrain')
                dt.putValue('maxSpeed', 1)

            robot.drivetrain.setSpeedLimit(maxSpeed)
