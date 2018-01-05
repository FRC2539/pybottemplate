from wpilib.command import InstantCommand

from custom import driverhud

class AlertCommand(InstantCommand):

    def __init__(self, msg, type='Alerts'):
        '''Show an alert on the dashboard'''
        super().__init__('Alert: %s' % msg)

        self.setRunWhenDisabled(True)

        self.msg = msg
        self.type = type


    def initialize(self):
        driverhud.showAlert(self.msg, self.type)


    def setMessage(self, msg):
        self.msg = msg
