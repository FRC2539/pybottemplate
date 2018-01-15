from wpilib.command.command import Command
from wpilib.joystick import Joystick


class ControllerDebugCommand(Command):

    def __init__(self, port=0):
        super().__init__('Get Controller Values')

        self.setRunWhenDisabled(True)
        self.joystick = Joystick(port)


    def execute(self):
        for i in range(0, 6):
            value = self.joystick.getRawAxis(i)
            if (abs(value) >= 0.5):
                print('Axis %d: %f' % (i, value))

        for i in range(1, 15):
            if self.joystick.getRawButtonPressed(i):
                print('Button %d Pressed' % i)
