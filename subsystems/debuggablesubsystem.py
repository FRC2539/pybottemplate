from wpilib.command.subsystem import Subsystem
from wpilib.livewindow import LiveWindow

class DebuggableSubsystem(Subsystem):
    '''
    Simplifies sending sensor and actuator data to the SmartDashboard. This
    should be used as the base class for any subsystem that has motors or
    sensors.
    '''

    def debugSensor(self, label, sensor):
        LiveWindow.addSensor(self.getName(), label, sensor)


    def debugMotor(self, label, motor):
        LiveWindow.addActuator(self.getName(), label, motor)
