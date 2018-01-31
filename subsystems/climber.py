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

        self.hook = WPI_TalonSRX(ports.climber.hookMotorID)
        self.hook.setNeutralMode(NeutralMode.Brake)
        self.hook.setSafetyEnabled(False)

        self.winch = WPI_TalonSRX(ports.climber.winchMotorID)
        self.winch.setNeutralMode(NeutralMode.Brake)
        self.winch.setSafetyEnabled(False)

    def startWinch(self):
        self.winch.set(ControlMode.PercentOutput, 1)

    def stopWinch(self):
        self.winch.set(ControlMode.PercentOutput, 0)


    def hookUp(self):
        self.hook.set(ControlMode.PercentOutput, 1)

    def hookDown(self):
        self.hook.set(ControlMode.PercentOutput, -1)

    def stopHook(self):
        self.hook.set(ControlMode.PercentOutput, 0)
