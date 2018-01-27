from wpilib.command.subsystem import Subsystem
from ctre import WPI_TalonSRX, ControlMode
import ports
from custom.config import Config

class Elevator(Subsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Elevator')

        self.motor = WPI_TalonSRX(ports.elevator.motorID)
        self.motor.setSafetyEnabled(False)

        self.floors = [
            Config("Elevator/ground"),
            Config("Elevator/exchange"),
            Config("Elevator/portal"),
            Config("Elevator/switch"),
            Config("Elevator/scale"),
            Config("Elevator/hang")
        ]


    def initDefaultCommand(self):
        from commands.elevator.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())

    def up(self):
        self.motor.set(ControlMode.PercentOutput, 1)

    def down(self):
        self.motor.set(ControlMode.PercentOutput, -1)

    def stop(self):
        self.motor.set(ControlMode.PercentOutput, 0)
