from networktables import NetworkTables
from ntcore.constants import NT_PERSISTENT


class Config:
    '''
    Config values are stored on the roboRIO and updated using NetworkTables.
    By default the stored value is None, so make sure you set a value before
    running code that uses it.
    '''

    _values = {}

    def __init__(self, key, default=None):
        '''The key is the name that will be used in NetworkTables.'''

        if '/' not in key:
            key = '/Config/%s' % key

        if not key.startswith('/'):
            key = '/%s' % key

        self.key = key
        if key in Config._values:
            return

        value = NetworkTables._api.getEntryValue(self.key)

        if not value and default is None:
            Config._values[self.key] = None
        else:
            Config._values[self.key] = NetworkTables.getGlobalAutoUpdateValue(
                self.key,
                value.value if value else default,
                False
            )

            '''Make entry persistent so it is saved to the roboRIO.'''
            flags = NetworkTables._api.getEntryFlags(self.key) | NT_PERSISTENT
            NetworkTables._api.setEntryFlags(self.key, flags)


    def getValue(self):
        if Config._values[self.key] is None:
            value = NetworkTables._api.getEntryValue(self.key)
            if not value:
                return None

            Config._values[self.key] = NetworkTables.getGlobalAutoUpdateValue(
                self.key,
                value.value,
                False
            )

            flags = NetworkTables._api.getEntryFlags(self.key) | NT_PERSISTENT
            NetworkTables._api.setEntryFlags(self.key, flags)

            return value.value

        else:
            return Config._values[self.key].get()


    '''
    We overload the "magic methods" for different primitive types that we would
    like to store in Config.
    '''
    def __bool__(self):
        return bool(self.getValue())


    def __float__(self):
        try:
            return float(self.getValue())
        except TypeError:
            return 0.0


    def __int__(self):
        try:
            return int(self.getValue())
        except TypeError:
            return 0


    def __str__(self):
        '''If we're requesting a string for a number, show its key.'''

        try:
            float(self.getValue())
            return self.key
        except TypeError:
            return str(self.getValue())
