from ctre import (
    WPI_TalonFX,
    CANCoder,
    NeutralMode,
    TalonFXControlMode,
    FeedbackDevice,
    AbsoluteSensorRange,
    RemoteSensorSource,
    SensorTerm,
    SensorInitializationStrategy,
)

import math

import constants


class SwerveModule:
    def __init__(
        self,
        driveMotorID,
        turnMotorID,
        canCoderID,
        speedLimit,
        offset,
        invertedDrive=False,
    ):  # Get the ports of the devices for a module.

        """
        The class constructor.

        TODO:
        - Organize method definitions into logical order.
        - Get the position of the motor on startup with CANCoder,
          then, convert that to IntegratedSensor ticks, and
          set that as the integrated sensor's current
          position. At that point, we should be able to use
          the TalonFX and its integrated sensor to
          control the position.
        - NOTE Reverse rear encoders?
        """

        self.driveMotor = WPI_TalonFX(driveMotorID)  # Declare and setup drive motor.

        self.driveMotor.setNeutralMode(NeutralMode.Brake)
        self.driveMotor.setSafetyEnabled(False)
        self.driveMotor.setInverted(invertedDrive)
        self.driveMotor.configSelectedFeedbackSensor(
            FeedbackDevice.IntegratedSensor, 0, 0
        )

        self.driveMotor.setSelectedSensorPosition(0)

        self.driveMotor.configMotionCruiseVelocity(
            constants.drivetrain.driveMotionCruiseVelocity, 0
        )
        self.driveMotor.configMotionAcceleration(
            constants.drivetrain.driveMotionAcceleration, 0
        )

        self.dPk = constants.drivetrain.dPk  # P gain for the drive.
        self.dIk = constants.drivetrain.dIk  # I gain for the drive
        self.dDk = constants.drivetrain.dDk  # D gain for the drive
        self.dFk = constants.drivetrain.dFFk  # Feedforward gain for the drive
        self.dIZk = constants.drivetrain.dIZk  # Integral Zone for the drive

        self.sdPk = constants.drivetrain.sdPk  # P gain for the drive.
        self.sdIk = constants.drivetrain.sdIk  # I gain for the drive
        self.sdDk = constants.drivetrain.sdDk  # D gain for the drive
        self.sdFk = constants.drivetrain.sdFFk  # Feedforward gain for the drive
        self.sdIZk = constants.drivetrain.sdIZk  # Integral Zone for the drive

        self.cancoder = CANCoder(canCoderID)  # Declare and setup the remote encoder.
        self.cancoder.configAllSettings(constants.drivetrain.encoderConfig)
        # self.cancoder.setPositionToAbsolute()

        if offset is not None:
            self.cancoder.configMagnetOffset(offset)

        self.turnMotor = WPI_TalonFX(turnMotorID)  # Declare and setup turn motor.

        self.turnMotor.setNeutralMode(NeutralMode.Brake)
        self.turnMotor.setSafetyEnabled(False)

        self.turnMotor.configAllowableClosedloopError(0, 0, 0)  # No errors allowed!

        self.turnMotor.configMotionCruiseVelocity(
            constants.drivetrain.turnMotionCruiseVelocity, 0
        )
        self.turnMotor.configMotionAcceleration(
            constants.drivetrain.turnMotionAcceleration, 0
        )

        self.turnMotor.configRemoteFeedbackFilter(self.cancoder, 0, 0)
        self.turnMotor.configSelectedFeedbackCoefficient(360 / 4096, 0, 0)

        self.turnMotor.configSelectedFeedbackSensor(
            FeedbackDevice.RemoteSensor0, 0, 0
        )  # Set the feedback sensor as remote.

        self.tPk = constants.drivetrain.tPk  # P gain for the turn.
        self.tIk = constants.drivetrain.tIk  # I gain for the turn.
        self.tDk = constants.drivetrain.tDk  # D gain for the turn.
        self.tFk = constants.drivetrain.tFFk  # Feedforward gain for the turn.
        self.tIZk = constants.drivetrain.tIZk  # Integral Zone for the turn.

        self.stPk = constants.drivetrain.stPk  # Secondary P gain for the turn.
        self.stIk = constants.drivetrain.stIk  # Secondary I gain for the turn.
        self.stDk = constants.drivetrain.stDk  # Seconday D gain for the turn.
        self.stFk = (
            constants.drivetrain.stFFk
        )  # Secondary Feedforward gain for the turn.
        self.stIZk = constants.drivetrain.stIZk  # Secondary Integral Zone for the turn.

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

        self.speedLimit = speedLimit  # Pass the speed limit at instantiation so we can drive more easily. In inches per second.

        self.setPID()  # Sets the PID slots to values from the constants file.
        self.setModuleProfile(0)  # Sets the PID profile for the module to follow.

    def setState(self, state):
        """
        Set the "state" of the module. Used in the trajectory stuff.
        """

        self.setWheelAngle(
            (state.angle).degrees()
        )  # Sets the angle using the Rotation2d object of the module state.

        self.speedLimit = (
            state.speed_fps * 12
        )  # Multiply by twelve to make it inches per second.

        self.setWheelSpeed(1)  # Sets to the max velocity, which is set above.

    def updateCANCoder(self, val):
        """
        Updates the value of the CANCoder. This is how we "zero" the entire swerve.
        """
        # self.cancoder.configMagnetOffset(val)
        # print(
        # "just reconfigured (hopefully zero) "
        # + str(self.cancoder.getPosition())
        # )
        pass

    def getWheelAngle(self):
        """
        Get wheel angle relative to the robot.
        """
        return self.cancoder.getPosition()  # Returns absolute position of CANCoder.

    def setWheelAngle(self, angle):
        """
        This will set the angle of the wheel, relative to the robot.
        0 degrees is facing forward. Angles should be given -180 - 180.
        #"""
        # angle += 180

        # angle = (angle + 180) % 360  # Takes the opposite so right isn't left.

        currentAngle = self.getWheelAngle()
        self.addcounter = 0  # Counts how many times we exceed 360.
        self.minuscounter = 0  # Counts how many times we go below 0.
        self.loop = True
        self.change = self.addcounter - self.minuscounter
        angle += 360 * self.change
        while self.loop:
            self.tempangle = angle + 360
            self.tempangle2 = angle - 360
            if abs(currentAngle - self.tempangle) < abs(currentAngle - angle):
                angle = self.tempangle
                self.addcounter += 1
            elif abs(currentAngle - self.tempangle2) < abs(currentAngle - angle):
                angle = self.tempangle2
                self.minuscounter += 1
            else:
                self.loop = False

        self.turnMotor.set(
            TalonFXControlMode.MotionMagic, angle
        )  # self.turnMotor.getSelectedSensorPosition(0) + diff)

    def getWheelSpeed(self, inIPS=True):
        """
        Get the drive speed of this specific module.
        """
        if inIPS:
            return self.ticksPerTenthToInchesPerSecond(
                self.driveMotor.getSelectedSensorVelocity()
            )
        # Returns ticks per 0.1 seconds (100 mS).

        return self.driveMotor.getSelectedSensorVelocity()

    def setWheelSpeed(self, speed):
        """
        This will set the speed of the drive motor to a set velocity. 'speed' is given as a
        percent, which is multiplied by 'self.speedLimit', a max speed in inches per second.
        """
        self.driveMotor.set(
            TalonFXControlMode.Velocity,
            self.inchesPerSecondToTicksPerTenth(
                speed * self.speedLimit
            ),  # Set half of the normal speed temporarily.
        )

    def getWheelPercent(self):
        """
        Returns the drive motor's output in a percent form.
        """
        return self.driveMotor.getMotorOutputPercent()

    def setWheelPercent(self, speed):
        """
        Does just what it sounds like.
        """
        self.driveMotor.set(TalonFXControlMode.PercentOutput, speed)

    def getModulePosition(self, inInches=True):
        """
        Returns the position of the module in ticks or inches. Do it here since we
        will be doing it here when we set it anyway. Doing so should also simplify the
        move command :).
        """
        if inInches:
            return self.driveTicksToInches(
                self.driveMotor.getSelectedSensorPosition()
            )  # Returns the distance in inches.

        return (
            self.driveMotor.getSelectedSensorPosition()
        )  # Returns the distance in ticks.

    def setModulePosition(self, distance):
        """
        I highly advise against setting different distances for each module!
        Provide the distance in inches.
        """
        self.driveMotor.set(
            TalonFXControlMode.MotionMagic,
            self.getModulePosition(False) + self.inchesToDriveTicks(distance),
        )

    def resetDriveEncoders(self, anArgument=0):
        """
        Resets the drive encoders to 0 by default.
        """
        self.driveMotor.setSelectedSensorPosition(anArgument, 1, 0)

    def stopModule(self):
        """
        Stop the motors within the module.
        """
        self.turnMotor.stopMotor()
        self.driveMotor.stopMotor()

    def inchesToDriveTicks(self, inches):
        """
        Convert inches to the robot's understandable 'tick' unit.
        """
        wheelRotations = (
            inches / self.circ
        )  # Find the number of wheel rotations by dividing the distance into the circumference.
        motorRotations = (
            wheelRotations * self.driveMotorGearRatio
        )  # Find out how many motor rotations this number is.
        return motorRotations * 2048  # 2048 ticks in one Falcon rotation.

    def driveTicksToInches(self, ticks):
        """
        Convert 'ticks', robot units, to the imperial unit, inches.
        """
        motorRotations = ticks / 2048
        wheelRotations = motorRotations / self.driveMotorGearRatio
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

    def degreesToTurnTicks(self, degrees):
        """
        Convert the degrees read by something like a joystick or CANCoder to a
        Falcon-settable value (ticks). This is for the turn motor!
        """
        return ((degrees % 360) / 360) * (2048 * self.turnMotorGearRatio)
        # Take a position, makes it a percent, and then multiplies it by the
        # total number of ticks (motor units) in one full wheel rotation.

    def setModuleProfile(self, profile, drive=True, turn=True):
        """
        Which PID profile to use.
        """
        if turn:
            self.turnMotor.selectProfileSlot(profile, 0)
        if drive:
            self.driveMotor.selectProfileSlot(profile, 0)

    def setDriveCruiseVelocity(self, slow):
        """
        Sets the motion magic cruise control max speed for the drive motor
        """

        if slow:
            self.driveMotor.configMotionCruiseVelocity(
                constants.drivetrain.slowDriveMotionCruiseVelocity, 0
            )
        else:
            self.driveMotor.configMotionCruiseVelocity(
                constants.drivetrain.driveMotionCruiseVelocity, 0
            )

    def inchesToMeters(self, num):
        """
        Converts translational units, from inches to meters.
        """
        return num * 0.0254

    def metersToInches(self, num):
        """
        Convers translational units, from meters to inches.
        """
        return num * 39.3701

    def setPID(self):
        """
        Set the PID constants for the module.
        """
        self.driveMotor.config_kP(0, self.dPk, 0)
        self.driveMotor.config_kI(0, self.dIk, 0)
        self.driveMotor.config_kD(0, self.dDk, 0)
        self.driveMotor.config_kF(0, self.dFk, 0)
        self.driveMotor.config_IntegralZone(0, self.dIZk, 0)

        self.driveMotor.config_kP(1, self.sdPk, 0)
        self.driveMotor.config_kI(1, self.sdIk, 0)
        self.driveMotor.config_kD(1, self.sdDk, 0)
        self.driveMotor.config_kF(1, self.sdFk, 0)
        self.driveMotor.config_IntegralZone(1, self.sdIZk, 0)

        self.turnMotor.config_kP(0, self.tPk, 0)
        self.turnMotor.config_kI(0, self.tIk, 0)
        self.turnMotor.config_kD(0, self.tDk, 0)
        self.turnMotor.config_kF(0, self.tFk, 0)
        self.turnMotor.config_IntegralZone(0, self.tIZk, 0)

        self.turnMotor.config_kP(1, self.stPk, 0)
        self.turnMotor.config_kI(1, self.stIk, 0)
        self.turnMotor.config_kD(1, self.stDk, 0)
        self.turnMotor.config_kF(1, self.stFk, 0)
        self.turnMotor.config_IntegralZone(1, self.stIZk, 0)
