from  wpilib import digitalInput.py     
from wpilib.cantalon import CANTalon

class Shooter():
    ballDetector = digitalInput(0)
    leftPivorMotor = CANTalon(9)
    rightPivotMotor = CANTalon(8)
    indexWheel = CANTalon(10)
    shooterWheel = CANTalon(11)
    
    rightPivotMotor.setControlMode(CANTalon.ControlMode.Position);
    
    # P = .003, I = 0, D = 0
    rightPivotMotor.setPID(.003, 0, 0);
    rightPivotMotor.configMaxOutputVoltage(4);
    rightPivotMotor.SetInverted(true);
    
    leftPivotMotor.setControlMode(CANTalon.ControlMode.Follower)
    leftPivotMotor.set(8)
    leftPivotMotor.reverseSensor(True)
    
    def pivot(bool direction) {
            
            
	
