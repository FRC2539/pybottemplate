from ctre import (
    CANCoderConfiguration,
    AbsoluteSensorRange,
    SensorInitializationStrategy,
)


class Constants:
    """
    Dummy class for robot constants.
    """

    pass


"""
Use this class to declare variables that may have to be 
adjusted a lot. This makes it more global and easier to find. 
Please note that this is not the ports.py. That should host 
IDs for the CANbus, sensors, PWM, and the liking. 
"""

drivetrain = Constants()
shooter = Constants()

# Drive Velocity Control
drivetrain.dPk = 0.0085
drivetrain.dIk = 0
drivetrain.dDk = 0
drivetrain.dFFk = 0.25  # 1?
drivetrain.dIZk = 0

# Drive Position Control
drivetrain.sdPk = 0.45  # 0.1
drivetrain.sdIk = 0
drivetrain.sdDk = 0
drivetrain.sdFFk = 0.1
drivetrain.sdIZk = 0

# Turn Position Control
drivetrain.tPk = 22.5
drivetrain.tIk = 0
drivetrain.tDk = 0.01
drivetrain.tFFk = 0
drivetrain.tIZk = 0

# Turn Secondary Position Control
drivetrain.stPk = 8.5
drivetrain.stIk = 0
drivetrain.stDk = 0
drivetrain.stFFk = 0
drivetrain.stIZk = 0

# The angle of the gyro.
drivetrain.flatAngle = 0

# Gear ratios on the drivetrain.
drivetrain.driveMotorGearRatio = 6.86
drivetrain.turnMotorGearRatio = 12.8

# Motion magic velocities and accelerations
drivetrain.driveMotionAcceleration = 13500
drivetrain.driveMotionCruiseVelocity = 18500
drivetrain.slowDriveMotionCruiseVelocity = 11000

drivetrain.turnMotionAcceleration = 1000
drivetrain.turnMotionCruiseVelocity = 800

# Trajectory constraints.
drivetrain.maxMetersPerSecond = 1  # Velocity for trajectory
drivetrain.maxMetersPerSecondSquared = 0.1  # Accel for trajectory

# Diameter of the wheel in inches.
drivetrain.wheelDiameter = 4

# Distance between adjacent wheels.
drivetrain.wheelBase = 23.5
drivetrain.trackWidth = 23.5

# Center of the robot to the center of a wheel in inches.
drivetrain.robotRadius = 16.84251

drivetrain.speedLimit = (
    30.0  # in inches per second (if you have feet per second, multiply by 12!)
)

drivetrain.encoderConfig = CANCoderConfiguration()
drivetrain.encoderConfig.absoluteSensorRange = AbsoluteSensorRange.Unsigned_0_to_360
drivetrain.encoderConfig.initializationStrategy = (
    SensorInitializationStrategy.BootToAbsolutePosition
)
drivetrain.encoderConfig.sensorDirection = False

drivetrain.mostRecentPath = []  # Updated in record auto.

drivetrain.preBuild = {1: ".barrelracing.json"}

# Constants for the shooter below.

shooter.kP = 1
shooter.kI = 0
shooter.kD = 0.01
shooter.kF = 0.0495
shooter.IZone = 0
