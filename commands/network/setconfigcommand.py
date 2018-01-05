from wpilib.command.instantcommand import InstantCommand
from networktables import NetworkTables

from custom.config import Config

class SetConfigCommand(InstantCommand):
    '''Stores a given value in Config.'''

    def __init__(self, key, value):
        super().__init__('Set %s to %s' % (key, value))
        self.setRunWhenDisabled(True)

        self.config = Config(key)
        self.value = value


    def initialize(self):
        NetworkTables.getGlobalTable().putValue(self.config.key, self.value)
