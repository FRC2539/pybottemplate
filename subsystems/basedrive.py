from .cougarsystem import *

import math

from networktables import NetworkTables
from ctre import ControlMode, NeutralMode, WPI_TalonFX, FeedbackDevice
from navx import AHRS

from custom.config import Config
import ports
import constants


class BaseDrive(CougarSystem):
    """
    A general case drive train system. It abstracts away shared functionality of
    the various drive types that we can employ. Anything that can be done
    without knowing what type of drive system we have should be implemented here.
    """

    def __init__(self, name):
        super().__init__(name)

        """
        Create all motors, disable the watchdog, and turn off neutral braking
        since the PID loops will provide braking.
        """
        try:
            self.motors = [
                WPI_TalonFX(ports.drivetrain.frontLeftMotorID),
                WPI_TalonFX(ports.drivetrain.frontRightMotorID),
                WPI_TalonFX(ports.drivetrain.backLeftMotorID),
                WPI_TalonFX(ports.drivetrain.backRightMotorID),
            ]

        except AttributeError:
            self.motors = [
                WPI_TalonFX(ports.drivetrain.leftMotorID),
                WPI_TalonFX(ports.drivetrain.rightMotorID),
            ]

        for motor in self.motors:
            motor.setNeutralMode(NeutralMode.Brake)
            motor.setSafetyEnabled(False)
            motor.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor, 0, 0)

        """
        Subclasses should configure motors correctly and populate activeMotors.
        """
        self.activeMotors = []
        self._configureMotors()

        """Initialize the navX MXP"""
        self.navX = AHRS.create_spi()
        self.resetGyro()
        self.flatAngle = constants.drivetrain.flatAngle

        """A record of the last arguments to move()"""
        self.lastInputs = None

        self.speedLimit = self.get("Normal Speed", 45)
        self.deadband = self.get("Deadband", 0.05)

        self.wheelBase = (
            constants.drivetrain.wheelBase
        )  # These are distances across the robot; horizontal, vertical, diagonal.

        self.trackWidth = constants.drivetrain.trackWidth
        self.r = math.sqrt(self.wheelBase ** 2 + self.trackWidth ** 2)

        self.wheelDiameter = (
            constants.drivetrain.wheelDiameter
        )  # The diamter, in inches, of our driving wheels.
        self.circ = (
            self.wheelDiameter * math.pi
        )  # The circumference of our driving wheel.

        self.driveMotorGearRatio = (
            constants.drivetrain.driveMotorGearRatio
        )  # 6.86 motor rotations per wheel rotation (on y-axis).
        self.turnMotorGearRatio = (
            constants.drivetrain.turnMotorGearRatio
        )  # 12.8 motor rotations per wheel rotation (on x-axis).

        # Tell the robot to use encoders.
        self.useEncoders = True

    def initDefaultCommand(self):
        """
        By default, unless another command is running that requires this
        subsystem, we will drive via joystick using the max speed stored in
        Config.
        """
        from commands.drivetrain.drivecommand import DriveCommand

        self.setDefaultCommand(DriveCommand())

    def move(self, x, y, rotate):
        """Turns coordinate arguments into motor outputs."""

        """
        Short-circuits the rather expensive movement calculations if the
        coordinates have not changed.
        """
        if [x, y, rotate] == self.lastInputs:
            return

        self.lastInputs = [x, y, rotate]

        """Prevent drift caused by small input values"""
        if self.useEncoders:
            x = math.copysign(max(abs(x) - self.deadband, 0), x)
            y = math.copysign(max(abs(y) - self.deadband, 0), y)
            rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        speeds = self._calculateSpeeds(x, y, rotate)

        """Prevent speeds > 1"""
        maxSpeed = 0
        for speed in speeds:
            maxSpeed = max(abs(speed), maxSpeed)

        if maxSpeed > 1:
            speeds = [x / maxSpeed for x in speeds]

        """Use speeds to feed motor output."""
        for motor, speed in zip(self.activeMotors, speeds):
            motor.set(ControlMode.Velocity, speed * self.speedLimit)

    def setPositions(self, positions):
        """
        Have the motors move to the given positions. There should be one
        position per active motor. Extra positions will be ignored.
        """

        if not self.useEncoders:
            raise RuntimeError("Cannot set position. Encoders are disabled.")

        for motor in self.motors:
            motor.set(
                TalonFXControlMode.MotionMagic,
                self.getModulePosition(False) + self.inchesToTicks(distance),
            )

    def averageError(self):
        """Find the average distance between setpoint and current position."""
        error = 0
        for motor in self.activeMotors:
            error += abs(
                motor.getClosedLoopTarget(0) - motor.getSelectedSensorPosition(0)
            )

        return error / len(self.activeMotors)

    def atPosition(self, tolerance=10):
        """
        Check setpoint error to see if it is below the given tolerance.
        """
        return self.averageError() <= tolerance

    def stop(self):
        """Disable all motors until set() is called again."""
        for motor in self.activeMotors:
            motor.stopMotor()

        self.lastInputs = None

    def setProfile(self, profile):
        """Select which PID profile to use."""
        for motor in self.activeMotors:
            motor.selectProfileSlot(profile, 0)

    def resetPID(self):
        """Set all PID values to 0 for profiles 0 and 1."""
        for motor in self.activeMotors:
            motor.configClosedLoopRamp(0, 0)

            # Drive PIDs here.
            motor.config_kP(0, 0, 0)
            motor.config_kI(0, 0, 0)
            motor.config_kD(0, 0, 0)
            motor.config_kF(0, 0, 0)
            motor.config_IntegralZone(0, 0, 0)

            # Position control PIDs here.
            motor.config_kP(1, 0, 0)
            motor.config_kI(1, 0, 0)
            motor.config_kD(1, 0, 0)
            motor.config_kF(1, 0, 0)
            motor.config_IntegralZone(1, 0, 0)

    def resetGyro(self):
        """Force the navX to consider the current angle to be zero degrees."""

        self.setGyroAngle(0)

    def setGyroAngle(self, angle):
        """Tweak the gyro reading."""

        self.navX.reset()
        self.navX.setAngleAdjustment(angle)

    def getAngle(self):
        """Current gyro reading"""

        return self.navX.getAngle() % 360

    def getAngleTo(self, targetAngle):
        """
        Returns the anglular distance from the given target. Values will be
        between -180 and 180, inclusive.
        """
        degrees = targetAngle - self.getAngle()
        while degrees > 180:
            degrees -= 360
        while degrees < -180:
            degrees += 360

        return degrees

    def inchesToTicks(self, inches):
        """
        Convert inches to the robot's understandable 'tick' unit.
        """
        wheelRotations = (
            inches / self.circ
        )  # Find the number of wheel rotations by dividing the distance into the circumference.
        motorRotations = (
            wheelRotations * self.gearRatio
        )  # Find out how many motor rotations this number is.
        return motorRotations * 2048  # 2048 ticks in one Falcon rotation.

    def ticksToInches(self, ticks):
        """
        Convert 'ticks', robot units, to the imperial unit, inches.
        """
        motorRotations = ticks / 2048
        wheelRotations = motorRotations / self.gearRatio
        return (
            wheelRotations * self.circ
        )  # Basically just worked backwards from the sister method above.

    def inchesPerSecondToTicksPerTenth(self, inchesPerSecond):
        """
        Convert a common velocity to falcon-interprettable
        """
        return self.inchesToDriveTicks(inchesPerSecond / 10)

    def ticksPerTenthToInchesPerSecond(self, ticksPerTenth):
        """
        Convert a robot velocity to a legible one.
        """
        return self.driveTicksToInches(ticksPerTenth * 10)

    def resetTilt(self):
        self.flatAngle = self.navX.getPitch()

    def getTilt(self):
        return self.navX.getPitch() - self.flatAngle

    def getAcceleration(self):
        """Reads acceleration from NavX MXP."""
        return self.navX.getWorldLinearAccelY()

    def getSpeeds(self, inInchesPerSecond=True):
        """Returns the speed of each active motors."""
        if inInchesPerSecond:
            return [
                self.ticksPerTenthToInchesPerSecond(motor.getSelectedSensorVelocity())
                for motor in self.activeMotors
            ]

        # Returns ticks per 0.1 seconds (100 mS).
        return [motor.getSelectedSensorVelocity() for motor in self.activeMotors]

    def getPositions(self, inInches=True):
        """Returns the position of each active motor."""
        if inInchesPerSecond:
            return [
                self.ticksToInches(self.getSelectedSensorPosition(0))
                for x in self.activeMotors
            ]
        return [x.getSelectedSensorPosition(0) for x in self.activeMotors]

    def setUseEncoders(self, useEncoders=True):
        """
        Turns on and off encoders. As a side effect, if encoders are enabled,
        the motors will be set to speed mode. Disabling encoders should not be
        done lightly, as many commands rely on encoder information.
        """
        self.useEncoders = useEncoders

    def setSpeedLimit(self, speed):
        """
        Updates the max speed of the drive and changes to the appropriate
        mode depending on if encoders are enabled.
        """

        self.speedLimit = speed

    def _configureMotors(self):
        """
        Make any necessary changes to the motors and populate self.activeMotors.
        """

        raise NotImplementedError()

    def _calculateSpeeds(self, x, y, rotate):
        """Return a speed for each active motor."""

        raise NotImplementedError()
