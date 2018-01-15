from .debuggablesubsystem import DebuggableSubsystem

import math

from networktables import NetworkTables
from ctre import ControlMode, NeutralMode, WPI_TalonSRX
from robotpy_ext.common_drivers.navx.ahrs import AHRS

from custom.config import Config
import ports


class BaseDrive(DebuggableSubsystem):
    '''
    A general case drive train system. It abstracts away shared functionality of
    the various drive types that we can employ. Anything that can be done
    without knowing what type of drive system we have should be implemented here.
    '''

    def __init__(self, name):
        super().__init__(name)

        '''
        Create all motors, disable the watchdog, and turn off neutral braking
        since the PID loops will provide braking.
        '''
        try:
            self.motors = [
                WPI_TalonSRX(ports.drivetrain.frontLeftMotorID),
                WPI_TalonSRX(ports.drivetrain.frontRightMotorID),
                WPI_TalonSRX(ports.drivetrain.backLeftMotorID),
                WPI_TalonSRX(ports.drivetrain.backRightMotorID),
            ]

        except AttributeError:
            self.motors = [
                WPI_TalonSRX(ports.drivetrain.leftMotorID),
                WPI_TalonSRX(ports.drivetrain.rightMotorID),
            ]

        for motor in self.motors:
            motor.setNeutralMode(NeutralMode.Coast)
            motor.setSafetyEnabled(False)

        '''
        Subclasses should configure motors correctly and populate activeMotors.
        '''
        self.activeMotors = []
        self._configureMotors()

        '''Initialize the navX MXP'''
        self.navX = AHRS.create_spi()
        self.resetGyro()

        '''A record of the last arguments to move()'''
        self.lastInputs = None

        self.setUseEncoders()
        self.maxSpeed = Config('DriveTrain/maxSpeed')
        self.speedLimit = Config('DriveTrain/normalSpeed')
        self.deadband = Config('DriveTrain/deadband', 0.05)

        '''Allow changing CAN Talon settings from dashboard'''
        self._publishPID('Speed', 0)
        self._publishPID('Position', 1)


        '''Add items that can be debugged in Test mode.'''
        self.debugSensor('navX', self.navX)

        self.debugMotor('Front Left Motor', self.motors[0])
        self.debugMotor('Front Right Motor', self.motors[1])

        try:
            self.debugMotor('Back Left Motor', self.motors[2])
            self.debugMotor('Back Right Motor', self.motors[3])
        except IndexError:
            pass


    def initDefaultCommand(self):
        '''
        By default, unless another command is running that requires this
        subsystem, we will drive via joystick using the max speed stored in
        Config.
        '''
        from commands.drivetrain.drivecommand import DriveCommand

        self.setDefaultCommand(DriveCommand(self.speedLimit))


    def move(self, x, y, rotate):
        '''Turns coordinate arguments into motor outputs.'''

        '''
        Short-circuits the rather expensive movement calculations if the
        coordinates have not changed.
        '''
        if [x, y, rotate] == self.lastInputs:
            return

        self.lastInputs = [x, y, rotate]

        '''Prevent drift caused by small input values'''
        if self.useEncoders:
            x = math.copysign(max(abs(x) - self.deadband, 0), x)
            y = math.copysign(max(abs(y) - self.deadband, 0), y)
            rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        speeds = self._calculateSpeeds(x, y, rotate)

        '''Prevent speeds > 1'''
        maxSpeed = 0
        for speed in speeds:
            maxSpeed = max(abs(speed), maxSpeed)

        if maxSpeed > 1:
            speeds = [x / maxSpeed for x in speeds]

        '''Use speeds to feed motor output.'''
        if self.useEncoders:
            if not any(speeds):
                '''
                When we are trying to stop, clearing the I accumulator can
                reduce overshooting, thereby shortening the time required to
                come to a stop.
                '''
                for motor in self.activeMotors:
                    motor.setIntegralAccumulator(0, 0, 0)

            for motor, speed in zip(self.activeMotors, speeds):
                motor.set(ControlMode.Velocity, speed * self.speedLimit)

        else:
            for motor, speed in zip(self.activeMotors, speeds):
                motor.set(ControlMode.PercentOutput, speed * self.maxPercentVBus)


    def setPositions(self, positions):
        '''
        Have the motors move to the given positions. There should be one
        position per active motor. Extra positions will be ignored.
        '''

        if not self.useEncoders:
            raise RuntimeError('Cannot set position. Encoders are disabled.')

        for motor, position in zip(self.activeMotors, positions):
            motor.configMotionCruiseVelocity(self.speedLimit)
            motor.configMotionAcceleration(self.speedLimit)
            motor.set(ControlMode.MotionMagic, position)


    def atPosition(self, tolerance=10):
        '''
        Check setpoint error to see if it is below the given tolerance.
        '''
        error = 0
        for motor in self.activeMotors:
            error += abs(motor.getSetpoint() - motor.getSelectedSensorPosition())

        error /= len(self.activeMotors)

        return error <= tolerance


    def stop(self):
        '''Disable all motors until set() is called again.'''
        for motor in self.activeMotors:
            motor.stopMotor()


    def resetGyro(self):
        '''Force the navX to consider the current angle to be zero degrees.'''

        self.navX.reset()
        self.gyroOffset = 0


    def setGyroAngle(self, angle):
        '''Tweak the gyro reading.'''

        heading = self.naxX.getYaw()
        self.gyroOffset = angle - heading


    def getAngle(self):
        '''Current gyro reading'''

        return (self.navX.getYaw() + self.gyroOffset) % 360


    def getAcceleration(self):
        '''Reads acceleration from NavX MXP.'''
        return self.navX.getWorldLinearAccelY()


    def getSpeeds(self):
        '''Returns the speed of each active motors.'''

        if not self.useEncoders:
            raise RuntimeError('Cannot read speed. Encoders are disabled.')

        return [x.getSelectedSensorVelocity() for x in self.activeMotors]


    def getPositions(self):
        '''Returns the position of each active motor.'''

        if not self.useEncoders:
            raise RuntimeError('Cannot read position. Encoders are disabled.')

        return [x.getSelectedSensorPosition() for x in self.activeMotors]


    def setUseEncoders(self, useEncoders=True):
        '''
        Turns on and off encoders. As a side effect, if encoders are enabled,
        the motors will be set to speed mode. Disabling encoders should not be
        done lightly, as many commands rely on encoder information.
        '''
        self.useEncoders = useEncoders


    def setSpeedLimit(self, speed):
        '''
        Updates the max speed of the drive and changes to the appropriate
        mode depending on if encoders are enabled.
        '''

        if speed < 0:
            raise ValueError('DriveTrain speed cannot be less than 0')

        self.speedLimit = speed
        if speed > self.maxSpeed:
            self.maxSpeed = speed

        '''If we can't use encoders, attempt to approximate that speed.'''
        self.maxPercentVBus = speed / self.maxSpeed


    def _publishPID(self, table, profile):
        '''
        Read the PID value from the first active CAN Talon and publish it to the
        passed NetworkTable.
        '''

        table = NetworkTables.getTable('DriveTrain/%s' % table)

        talon = self.activeMotors[0]

        #talon.selectProfileSlot(profile, 0)
        #table.putNumber('P', talon.getP())
        #table.putNumber('I', talon.getI())
        #table.putNumber('D', talon.getD())
        #table.putNumber('F', talon.getF())
        #table.putNumber('IZone', talon.getIZone())
        #table.putNumber('RampRate', talon.getCloseLoopRampRate())

        table.addTableListener(self._PIDListener(profile))


    def _PIDListener(self, profile):
        '''Provides as easy way to make sure we update the right profile.'''

        def updatePID(table, key, value, isNew):
            '''
            Loops over all active motors and updates the appropriate setting. To
            avoid using a very long if structure inside the loop, we use getattr
            to access the methods of the motor by name.
            '''

            funcs = {
                'P': 'config_kP',
                'I': 'config_kI',
                'D': 'config_kD',
                'F': 'config_kF',
                'IZone': 'setIZone',
                'RampRate': 'setCloseLoopRampRate'
            }

            for motor in self.activeMotors:
                motor.setProfileSlot(profile)
                getattr(motor, funcs[key])(value)

        return updatePID


    def _configureMotors(self):
        '''
        Make any necessary changes to the motors and populate self.activeMotors.
        '''

        raise NotImplementedError()


    def _calculateSpeeds(self, x, y, rotate):
        '''Return a speed for each active motor.'''

        raise NotImplementedError()
