from wpilib.command import Command

import subsystems

class MonitorCommand(Command):
    '''Runs continually while the robot is enabled.'''

    def __init__(self):
        super().__init__('MonitorCommand')

        '''
        Required because this is the default command for the monitor subsystem.
        '''
        self.requires(subsystems.monitor)

        self.setInterruptible(False)
        self.setRunWhenDisabled(True)


    def execute(self):
        '''Implement watchers here.'''

        pass
