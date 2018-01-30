from wpilib.command.subsystem import Subsystem
from ctre import WPI_TalonSRX, ControlMode
import ports
from custom.config import Config
import threading

class Elevator(Subsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Elevator')

        self.motor = WPI_TalonSRX(ports.elevator.motorID)
        self.motor.setSafetyEnabled(False)

        self.floors = [
            Config('Elevator/ground'),
            Config('Elevator/exchange'),
            Config('Elevator/portal'),
            Config('Elevator/switch'),
            Config('Elevator/scale'),
            Config('Elevator/hang')
        ]

        self.level = 0
        self.mutex = threading.RLock()


    def initDefaultCommand(self):
        from commands.elevator.defaultcommand import DefaultCommand

        self.setDefaultCommand(DefaultCommand())


    def set(self, speed):
        self.motor.set(ControlMode.PercentOutput, speed)


    def up(self):
        self.set(1)


    def down(self):
        self.set(-1)


    def stop(self):
        self.set(0)


    def goTo(self, position):
        self.motor.set(ControlMode.MotionMagic, int(position))


    def changeLevel(self, amount=1):
        with self.mutex:
            self.level += amount
            if self.level < 0:
                self.level = 0

            if self.level >= len(self.floors):
                self.level = len(self.floors) - 1

        self.goTo(self.floors[self.level])


    def setLevel(self, floor):
        key = 'Elevator/%s' % floor

        with self.mutex:
            for level, floor in enumerate(self.floors):
                if (str(floor) == key):
                    self.level = level
                    break

        self.goTo(self.floors[self.level])
