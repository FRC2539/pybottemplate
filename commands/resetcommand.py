from wpilib.command import InstantCommand

import robot

class ResetCommand(InstantCommand):
    '''
    Disable any running commands for all subsystems, except Monitor. This should
    be used to stop any motion and return the commands to a safe state. In
    general just requiring a subsystem will stop its current command. Additional
    resetting can be handled in the initialize method.
    '''

    def __init__(self):
        super().__init__('Reset')

        '''Require all subsystems to reset.'''
        self.requires(robot.drivetrain)
