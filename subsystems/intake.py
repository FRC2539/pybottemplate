from wpilib.command.subsystem import Subsystem
from ctre import WPI_TalonSRX, ControlMode
import ports
from wpilib.digitalinput import DigitalInput

class Intake(Subsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Intake')
        self.leftMotor = WPI_TalonSRX(ports.intake.leftMotorID)
        self.leftMotor.setSafetyEnabled(False)
        self.rightMotor = WPI_TalonSRX(ports.intake.rightMotorID)
        self.rightMotor.setSafetyEnabled(False)
        self.rightMotor.setInverted(True)
        self.lightSensor = DigitalInput(ports.intake.lightSensorID)

    def initDefaultCommand(self):
        from commands.intake.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())

    def intake(self):
        self.leftMotor.set(ControlMode.PercentOutput, 1)
        self.rightMotor.set(ControlMode.PercentOutput, 1)

    def outtake(self):
        self.leftMotor.set(ControlMode.PercentOutput, -1)
        self.rightMotor.set(ControlMode.PercentOutput, -1)

    def stopTake(self):
        self.leftMotor.set(ControlMode.PercentOutput, 0)
        self.rightMotor.set(ControlMode.PercentOutput, 0)

    def isCubeInIntake(self):
        return self.lightSensor.get()
