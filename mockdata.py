from custom.config import Config

defaults = {
    'DriveTrain/maxSpeed': 950,
    'DriveTrain/normalSpeed': 600,
    'DriveTrain/preciseSpeed': 150,
    'DriveTrain/ticksPerInch': 750,
    'DriveTrain/width': 29.5
}

def fakeConfig(self):
    global defaults

    if self.key in defaults:
        return defaults[self.key]

    return self._getValue()

Config._getValue = Config.getValue
Config.getValue = fakeConfig
Config.__pos__ = fakeConfig
