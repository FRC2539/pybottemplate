'''
All subsystems should be imported here and instantiated inside the init method.
If you want your subsystem to be accessible to commands, you must add a variable
for it in the global scope.
'''

from .drivetrain import DriveTrain
from .monitor import Monitor
from .oi import OI

drivetrain = None
monitor = None

def init():
    '''
    Creates all subsystems. You must run this before any commands are
    instantiated. Do not run it more than once.
    '''
    global drivetrain, monitor

    if drivetrain is not None:
        raise RuntimeError('Subsystems have already been initialized')

    drivetrain = DriveTrain()
    monitor = Monitor()

    '''
    Since OI instantiates command as part of its construction, and those
    commands need access to the subsystems, OI must be instantiated last.
    '''
    OI()
