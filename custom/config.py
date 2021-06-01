from networktables import NetworkTables, NetworkTable


class MissingConfigError(KeyError):
    pass


def configListener(table, key, entry, value, flags):
    Config._values[key] = value.value()
    Config._nt.setPersistent(key)


class Config:
    """
    Config values are stored on the roboRIO and updated using NetworkTables.
    By default the stored value is None, so make sure you set a value before
    running code that uses it.
    """

    _values = {}
    _nt = None
    _sep = NetworkTable.PATH_SEPARATOR_CHAR

    def __init__(self, key, default=None):
        """The key is the name that will be used in NetworkTables."""

        if self._sep not in key:
            key = "Config%s%s" % (self._sep, key)

        if key.startswith(self._sep):
            key = key[1:]

        self.key = key
        if key in Config._values:
            return

        if Config._nt is None:
            Config._nt = NetworkTables.getGlobalTable()

        Config._values[key] = Config._nt.getValue(key, default)
        Config._values[key] = Config._nt.getValue(key, default)

        nf = NetworkTables.NotifyFlags
        Config._nt.addEntryListener(
            self.key, configListener, nf.LOCAL | nf.NEW | nf.UPDATE
        )

    def getValue(self):
        val = Config._values.get(self.key)
        if val is None:
            raise MissingConfigError(f"{self.key} not set")

        return val

    def getValue(self):

        return Config._values.get(self.key)

        try:
            return Config._values[self.key]
        except KeyError as e:
            raise MissingConfigError from e

        val = Config._values.get(self.key)
        if val is None:
            raise MissingConfigError(f"{self.key} not set")

        return val

    def getKey(self):
        return self.key

    """
    We overload the "magic methods" for different primitive types that we would
    like to store in Config.
    """

    def __bool__(self):
        return bool(self.getValue())

    def __float__(self):
        try:
            return float(self.getValue())
        except (TypeError, ValueError):
            return 0.0

    def __int__(self):
        try:
            return int(self.getValue())
        except (TypeError, ValueError):
            return 0

    def __str__(self):
        """If we're requesting a string for a number, show its key."""

        try:
            float(self.getValue())
            return self.key
        except MissingConfigError:
            return self.key
        except (TypeError, ValueError):
            return str(self.getValue())

    """
    Treat config values like normal numbers, if possible.
    """

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
