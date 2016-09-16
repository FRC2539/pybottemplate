from  wpilib import digitalInput
from wpilib.cantalon import CANTalon

class Shooter(Subsystem):
    def __init__(self, name):
        super().__init__(name)
    ballDetector = digitalInput(0)
    leftPivorMotor = CANTalon(9)
    rightPivotMotor = CANTalon(8)
    indexWheel = CANTalon(10)
    shooterWheel = CANTalon(11)
    settingsLoaded = False
    
    indexWheel.setControlMode(CANTalon.ControlMode.PercentVbus)
    # Set brake mode to coast.
    indexWheel.enableBrakeMode(False)
    indexWheel.setInverted(True)
    
    rightPivotMotor.setControlMode(CANTalon.ControlMode.Position)
    
    # P = .003, I = 0, D = 0
    rightPivotMotor.setPID(.003, 0, 0)
    rightPivotMotor.configMaxOutputVoltage(4)
    rightPivotMotor.SetInverted(true)
    
    leftPivotMotor.setControlMode(CANTalon.ControlMode.Follower)
    leftPivotMotor.set(8)
    leftPivotMotor.reverseSensor(True)
    
    def pivot(bool direction):
        print(1)
            
            
	
