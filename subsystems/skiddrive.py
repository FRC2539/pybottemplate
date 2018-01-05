from .basedrive import BaseDrive
from ctre import CANTalon
from wpilib.robotdrive import RobotDrive
import ports

class SkidDrive(BaseDrive):
    '''A drive base where all wheels on each side move together.'''


    def _configureMotors(self):

        '''Only the front motors are active in a skid system.'''
        self.activeMotors = self.motors[0:2]

        '''Make the back motors follow the front.'''
        if len(self.motors) == 4:
            self.motors[2].setControlMode(CANTalon.ControlMode.Follower)
            self.motors[2].set(ports.drivetrain.frontLeftMotorID)
            self.motors[3].setControlMode(CANTalon.ControlMode.Follower)
            self.motors[3].set(ports.drivetrain.frontRightMotorID)

        '''Invert the left side.'''
        self.motors[RobotDrive.MotorType.kFrontLeft].reverseSensor(True)


    def _calculateSpeeds(self, x, y, rotate):
        return [y + rotate, -y + rotate]

