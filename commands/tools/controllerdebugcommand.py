from wpilib.command.command import Command
from wpilib.joystick import Joystick


class ControllerDebugCommand(Command):

    def __init__(self, port=0):
        super().__init__('Get Controller Values')

        self.setRunWhenDisabled(True)
        self.joystick = Joystick(port)

        self.numOfAxes = self.joystick.ds.joystickAxes[port].count
        self.numOfButtons = self.joystick.ds.joystickButtons[port].count


    def execute(self):
        for i in range(0, self.numOfAxes):
            value = self.joystick.getRawAxis(i)
            if (abs(value) >= 0.5):
                print('Axis %d: %f' % (i, value))

        for i in range(1, self.numOfButtons):
            if self.joystick.getRawButtonPressed(i):
                print('Button %d Pressed' % i)
