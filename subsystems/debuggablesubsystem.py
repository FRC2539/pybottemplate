from wpilib.command import Subsystem
from wpilib import LiveWindow

class DebuggableSubsystem(Subsystem):
    '''
    Simplifies sending sensor and actuator data to the SmartDashboard. This
    should be used as the base class for any subsystem that has motors or
    sensors.
    '''

    def debugSensor(self, label, sensor):
        sensor.setName(self.getName(), label)


    def debugMotor(self, label, motor):
        motor.setName(self.getName(), label)
