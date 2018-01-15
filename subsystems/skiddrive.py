from .basedrive import BaseDrive
from ctre._impl import ControlMode
from wpilib.robotdrive import RobotDrive
import ports

class SkidDrive(BaseDrive):
    '''A drive base where all wheels on each side move together.'''


    def _configureMotors(self):

        '''Only the front motors are active in a skid system.'''
        self.activeMotors = self.motors[0:2]

        '''Make the back motors follow the front.'''
        if len(self.motors) == 4:
            self.motors[2].set(ControlMode.Follower, ports.drivetrain.frontLeftMotorID)
            self.motors[3].set(ControlMode.Follower, ports.drivetrain.frontRightMotorID)

        '''Invert the left side.'''
        self.motors[RobotDrive.MotorType.kFrontLeft].setInverted(True)


    def _calculateSpeeds(self, x, y, rotate):
        return [y + rotate, -y + rotate]
