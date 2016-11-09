from  wpilib.digitalinput import DigitalInput
from wpilib.cantalon import CANTalon
from networktables import NetworkTable
from wpilib.preferences import Preferences
from .debuggablesubsystem import DebuggableSubsystem
from commands.pivotcommand import PivotCommand


class Shooter(DebuggableSubsystem):
    def __init__(self):
        super().__init__('shooter')
        self.ballDetector = DigitalInput(0)
        self.leftPivotMotor = CANTalon(9)
        self.rightPivotMotor = CANTalon(8)
        self.indexWheel = CANTalon(10)
        self.shooterWheel = CANTalon(11)
        self.settingsLoaded = False
        self.pivotSpeed = 10000
        self.shootingSpeed = 10000
        self.shooterIsDone = True
        
        self.indexWheel.setControlMode(CANTalon.ControlMode.PercentVbus)
        # Set brake mode to coast.
        self.indexWheel.enableBrakeMode(False)
        self.indexWheel.setInverted(True)
        
        self.shooterWheel.setControlMode(CANTalon.ControlMode.Speed);
        # Set brake mode to coast.
        self.shooterWheel.enableBrakeMode(False)
        self.shooterWheel.setPID(0, .01, 0)
        self.shooterWheel.setInverted(True)
        
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.Position)
        
        self.rightPivotMotor.setPID(.003, 0, 0)
        self.rightPivotMotor.configMaxOutputVoltage(4)
        self.rightPivotMotor.setInverted(True)
        
        self.leftPivotMotor.setControlMode(CANTalon.ControlMode.Follower)
        self.leftPivotMotor.set(8)
        self.leftPivotMotor.reverseSensor(True)

        targetInfo = NetworkTable.getTable("cameraTarget");

        self.debugMotor("left pivot motor", self.leftPivotMotor)
        self.debugMotor("right pivot motor", self.rightPivotMotor)
        self.debugMotor("index wheel", self.indexWheel)
        self.debugMotor("shooter wheel", self.shooterWheel)

        self.debugSensor("ball detector", self.ballDetector)
        
    
    def initDefaultCommand(self):
        self.setDefaultCommand(PivotCommand(self.pivotSpeed))
        
    def pivot(self, speed):
        self.rightPivotMotor.clearIaccum()
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.Speed)
        self.rightPivotMotor.setPID(0, .001, 0)
        self.rightPivotMotor.set(speed)
        
    
    def holdAt(self, position):
        if self.atKnownPosition() == False:
            return
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.Position)
        # pivotHoldPID = 0.003, 0, 0
        self.rightPivotMotor.setPID(0.003, 0, 0)
        self.rightPivotMotor.set(position)

    def setIndexerSpeed(self, speed):
        self.indexWheel.set(speed)
    
    def setShooterSpeed(self, speed):
        self.shooterWheel.setControlMode(CANTalon.ControlMode.Speed)
        self.shooterWheel.set(speed)


    def isShooterDone(self):
        return self.shooterIsDone
    

    def setShooterIsDone(self, done):
        self.shooterIsDone = done
        
    def stopShooter(self):
        self.manualShooter(0)
        
    def manualPivot(self, power):
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.rightPivotMotor.set(power)
    
    def manualShooter(self, power):
        self.shooterWheel.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.shooterWheel.set(power)
    
    def readyToFire(self):
        #firing speed = 5000
        if self.shooterWheel.getSetpoint() != 5000:
            return False
        return abs(self.shooterWheel.getClosedLoopError()) < 100
    
    def getHeight(self):
        self.rightPivotMotor.getPosition()
        
    def atTopLimit(self):
        self.rightPivotMotor.isRevLimitSwitchClosed()
        
    def atBottomLimit(self):
        self.rightPivotMotor.isFwdLimitSwitchClosed()
            
    def hasBall(self):
        return self.ballDetector.get()
    
    """def getTarget(self):
        Target target
        if self.targetInfo.getBoolean("hasTarget", False) == False:
            return target
        target.found = true
        target.position = self.targetInfo->getNumber("centerX", 0)
        target.distance = self.targetInfo.getNumber("distance", 0)
        return target
        """
        
        
