from commands2 import InstantCommand

import robot
from custom.config import Config
from networktables import NetworkTables


class SetUseEncodersCommand(InstantCommand):
    def __init__(self, encodersEnabled):
        super().__init__()

        self.addRequirements(robot.drivetrain)
        self.encodersEnabled = encodersEnabled

    def initialize(self):
        robot.drivetrain.setUseEncoders(self.encodersEnabled)
        if not self.encodersEnabled:
            maxSpeed = Config("DriveTrain/maxSpeed")
            if not maxSpeed:
                dt = NetworkTables.getTable("DriveTrain")
                dt.putValue("maxSpeed", 1)

            robot.drivetrain.setSpeedLimit(maxSpeed)
