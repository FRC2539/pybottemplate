from wpilib.preferences import Preferences
import ast
from networktables import NetworkTable
from threading import Thread

class Config:
    '''
    Config values are stored on the roboRIO and updated using NetworkTables.
    By default the stored value is None, so make sure you set a value before
    running code that uses it.
    '''

    store = None
    keys = []
    tables = {}

    def __init__(self, key):
        '''The key is the name that will be used in NetworkTables.'''

        try:
            self.table, self.key = key.split('/', 1)
        except ValueError:
            self.table = 'Config'
            self.key = key

        if (self.table, self.key) in Config.keys:
            return

        Config.keys.append((self.table, self.key))

        if self.table not in Config.tables:
            Config.tables[self.table] = NetworkTable.getTable(self.table)

        '''
        If _loadPreferences has already been run, we need to add our new key to
        the store dictionary, and potentially add a new listener for the table.
        '''
        if Config.store is not None:
            value = ast.literal_eval(
                Config.tables[self.table].getString(self.key, 'None')
            )

            if self.table not in Config.store:
                Config.store[self.table] = { self.key: value }
                Config.tables[self.table].name  = self.table
                Config.tables[self.table].addTableListener(Config._valueChanged)

            if self.key not in Config.store[self.table]:
                Config.store[self.table][self.key] = value


    @staticmethod
    def _loadPreferences():
        '''
        If the config has not been read from disk yet, read it, parse it, and
        populate the store with all known values.
        '''

        if Config.store is not None:
            return

        preferences = Preferences.getInstance()

        Config.store = ast.literal_eval(preferences.get('config', '{}'))

        '''
        Loop through all registered keys and make sure we have slots for them in
        the store.
        '''
        for table, key in Config.keys:
            if table not in Config.store:
                Config.store[table] = {}

            if key not in Config.store[table]:
                Config.store[table][key] = None

        '''
        Check in NetworkTables to see if any values have already been
        registered. If they have, update the store accordingly and save the new
        values back to disk. If a value is not already in NetworkTables, set it
        there.
        '''
        changes = False
        for table, keys in Config.store.items():
            if table not in Config.tables:
                Config.tables[table] = NetworkTable.getTable(table)

            for key, value in keys.items():
                currentValue = ast.literal_eval(
                    Config.tables[table].getString(key, 'None')
                )
                if currentValue is not None and currentValue != value:
                    changes = True
                    keys[key] = currentValue

                if currentValue is None and value is not None:
                    Config.tables[table].putString(key, repr(value))

        if changes:
            Config.save()

        '''Add listeners to all tables, so we can update values on changes.'''
        for name, table in Config.tables.items():
            table.addTableListener(Config._valueChanged)

            '''
            There is no easy way to get the name back from a table object, so we
            add it to the object directly.
            '''
            table.name = name


    @staticmethod
    def _valueChanged(table, key, value, isNew):
        '''Respond to updates made to our values via NetworkTables.'''

        try:
            if key in Config.store[table.name]:
                Config.store[table.name][key] = ast.literal_eval(str(value))
        except SyntaxError:
            Config.store[table.name][key] = None

        '''
        Save config in a sepearate thread so we don't hang up NetworkTable's
        event loop.
        '''
        Thread(target=Config.save).start()


    @staticmethod
    def save():
        '''Store changes to the roboRIO's internal hard drive.'''

        preferences = Preferences.getInstance()
        preferences['config'] = repr(Config.store)
        preferences.save()


    '''
    We overload the "magic methods" for different primitive types that we would
    like to store in Config.
    '''
    def __bool__(self):
        Config._loadPreferences()
        return bool(Config.store[self.table][self.key])


    def __float__(self):
        Config._loadPreferences()
        try:
            return float(Config.store[self.table][self.key])
        except TypeError:
            return 0


    def __int__(self):
        Config._loadPreferences()
        try:
            return int(Config.store[self.table][self.key])
        except TypeError:
            return 0


    def __str__(self):
        Config._loadPreferences()
        return str(Config.store[self.table][self.key])
