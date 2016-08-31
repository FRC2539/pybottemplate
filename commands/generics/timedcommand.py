from .defaultcommand import DefaultCommand

class TimedCommand(DefaultCommand):
    '''A command that runs for a set period of time.'''

    def __init__(self, name, timeoutInSeconds):
        super().__init__(name, timeoutInSeconds)

    def isFinished(self):
        return self.isTimedOut()
