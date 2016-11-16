'''
This is the place where we store port numbers for all subsystems. It is based on
the RobotMap concept from WPILib. Each subsystem should have its own ports list.
Values other than port numbers should be stored in Preferences.
'''

class PortsList:
    '''Dummy class used to store variables on an object.'''
    pass

drivetrain = PortsList()
shooter = PortsList()

'''CAN IDs for motors'''
drivetrain.frontLeftMotorID = 1
drivetrain.frontRightMotorID = 3
drivetrain.backLeftMotorID = 2
drivetrain.backRightMotorID = 4

shooter.rightPivotMotorID = 8
shooter.leftPivotMotorID = 9
shooter.indexWheelID = 10
shooter.shooterWheelID = 11
