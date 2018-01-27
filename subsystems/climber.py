from .debuggablesubsystem import DebuggableSubsystem
from ctre import ControlMode, NeutralMode, WPI_TalonSRX
from wpilib.digitalinput import DigitalInput

import ports

class Climber(DebuggableSubsystem):
    '''
    A subsystem designed to climb a rope.
    '''

    def __init__(self):
        super().__init__('Climber')

        self.motor = WPI_TalonSRX(ports.climber.motorID)
        self.motor.enableBrakeMode(True)
        self.motor.setSafetyEnabled(False)
        self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)


    def start(self):
        self.motor.set(ControlMode.PercentOutput, 1)


    def stop(self):
        self.motor.set(0)


    def atTop(self):
        return False
