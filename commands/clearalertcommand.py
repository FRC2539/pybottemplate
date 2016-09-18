from wpilib.smartdashboard import SmartDashboard

from commandbased import TimedCommand

class ClearAlertCommand(TimedCommand):
    '''Remove the alert message after a set number of seconds.'''

    def __init__(self):
        super().__init__('ClearAlert', 4)


    def end(self):
        SmartDashboard.putString('Alerts', '')
