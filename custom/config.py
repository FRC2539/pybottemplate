from networktables import NetworkTables

class Config:
    '''
    Config values are stored on the roboRIO and updated using NetworkTables.
    By default the stored value is None, so make sure you set a value before
    running code that uses it.
    '''

    _values = {}
    _nt = None
    _sep = NetworkTables.PATH_SEPARATOR

    def __init__(self, key, default=None):
        '''The key is the name that will be used in NetworkTables.'''

        if self._sep not in key:
            key = 'Config%s%s' % (self._sep, key)

        if key.startswith(self._sep):
            key = key[1:]

        self.key = key
        if key in Config._values:
            return

        if Config._nt is None:
            Config._nt = NetworkTables.getGlobalTable()

        try:
            value = Config._nt.getValue(self.key, None)
        except KeyError:
            value = None

        if value is None and default is None:
            Config._values[self.key] = None
        else:
            Config._values[self.key] = Config._nt.getAutoUpdateValue(
                self.key,
                value if value is not None else default,
                False
            )

            '''Make entry persistent so it is saved to the roboRIO.'''
            Config._nt.setPersistent(self.key)


    def getValue(self):
        if Config._values[self.key] is None:
            try:
                value = Config._nt.getValue(self.key)
            except KeyError:
                return None

            Config._values[self.key] = Config._nt.getAutoUpdateValue(
                self.key,
                value,
                False
            )
            Config._nt.setPersistent(self.key)

            return value

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


    '''
    Treat config values like normal numbers, if possible.
    '''
    def __lt__(self, other):
        return self.getValue() < other

    def __le__(self, other):
        return self.getValue() <= other

    def __eq__(self, other):
        return self.getValue() == other

    def __ge__(self, other):
        return self.getValue() >= other

    def __gt__(self, other):
        return self.getValue() > other

    def __add__(self, other):
        return self.getValue() + other

    def __sub__(self, other):
        return self.getValue() - other

    def __rsub__(self, other):
        return other - self.getValue()

    def __mul__(self, other):
        return self.getValue() * other

    def __truediv__(self, other):
        return self.getValue() / other

    def __rtruediv__(self, other):
        return other / self.getValue()

    def __mod__(self, other):
        return self.getValue() % other

    def __rmod__(self, other):
        return other % self.getValue()

    def __neg__(self):
        return -1 * self.getValue()

    def __abs__(self):
        return abs(self.getValue())

    __pos__ = getValue
    __radd__ = __add__
    __rmul__ = __mul__
