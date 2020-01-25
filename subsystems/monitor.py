from wpilib.command import Subsystem


class Monitor(Subsystem):
    '''Exists to observe system state via its default command.'''

    def __init__(self):
        super().__init__('Monitor')


    def initDefaultCommand(self):
        from commands.monitorcommand import MonitorCommand

        self.setDefaultCommand(MonitorCommand())

