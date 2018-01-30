from custom.config import Config

defaults = {
    'DriveTrain/maxSpeed': 950,
    'DriveTrain/normalSpeed': 600,
    'DriveTrain/preciseSpeed': 150,
    'DriveTrain/ticksPerInch': 750,
    'Autonomous/robotLocation': 'C',
    'Autonomous/switch': 'easy',
    'Autonomous/scale': 'easy'
}

def fakeConfig(self):
    global defaults

    if self.key in defaults:
        return defaults[self.key]

    return self._getValue()

Config._getValue = Config.getValue
Config.getValue = fakeConfig
Config.__pos__ = fakeConfig

from wpilib.driverstation import DriverStation
DriverStation.getGameSpecificMessage = lambda x=0: 'LRL'
