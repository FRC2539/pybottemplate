from wpilib.command.instantcommand import InstantCommand
from networktables import NetworkTables

from custom.config import Config

class AlterConfigCommand(InstantCommand):
    '''Changes the value stored in Config.'''

    def __init__(self, key, func):
        super().__init__('Alter %s' % key)
        self.setRunWhenDisabled(True)

        self.config = Config(key)
        self.func = func


    def initialize(self):
        NetworkTables.getGlobalTable().putValue(
            self.config.key,
            self.func(self.config)
        )
