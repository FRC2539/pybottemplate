from  wpilib.digitalinput import DigitalInput
from wpilib.cantalon import CANTalon
from wpilib.cameraserver import CameraServer
from wpilib.preferences import Preferences
from debuggablesubsystem import DebuggableSubsystem

class Shooter(DebuggableSubsystem):
    def __init__(self, name):
        super().__init__(name)
        self.ballDetector = DigitalInput(0)
        self.leftPivotMotor = CANTalon(9)
        self.rightPivotMotor = CANTalon(8)
        self.indexWheel = CANTalon(10)
        self.shooterWheel = CANTalon(11)
        self.settingsLoaded = False
        
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
        
        cam = CameraServer.getInstance()
        cam.startAutomaticCapture()

        # targetInfo = NetworkTable.getTable("cameraTarget");

        self.debugMotor("left pivot motor", self.leftPivotMotor)
        self.debugMotor("right pivot motor", self.rightPivotMotor)
        self.debugMotor("index wheel", self.indexWheel)
        self.debugMotor("shooter wheel", self.shooterWheel)

        self.debugSensor("ball detector", self.ballDetector)
        
    
    def pivot(self, direction):
        pivotDirection = direction
        if not self.atKnownPosition():
            return
        self.rightPivotMotor.clearIaccum()
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.Speed)
        self.rightPivotMotor.setPID(0, .001, 0)

        # 0 = up. 1 = down
        #20000 refers to pivot speed.
        if pivotDirection < 0:
            self.rightPivotMotor.set(20000)
        elif pivotDirection > 0:
            self.rightPivotMotor.set(-20000)
        else:
            self.rightPivotMotor.set(0)
    
    def holdAt(self, position):
        if self.atKnownPosition() == False:
            return
        self.rightPivotMotor.setControlMode(CANTalon.ControlMode.Position)
        # pivotHoldPID = 0.003, 0, 0
        self.rightPivotMotor.setPID(0.003, 0, 0)
        self.rightPivotMotor.set(position)

    def setIndexerSpeed(self, speed):
        self.indexWheel.set(speed)
        
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
    
    def setEncoderPosition(self, position):
        self.rightPivotMotor.setPosition(position)
        preferences = Preferences.getInstance()
        
    def storeEncoderPosition(self):
        if self.atKnownPosition():
            self.setEncoderPosition(self.getHeight())
            
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
        
        
    
    def atKnownPosition(self):
        if not self.settingsLoaded:
            preferences = Preferences.getInstance()
            if (preferences.containsKey("shooterPosition")):
                    self.rightPivotMotor.setPosition(preferences.getInt("shooterPosition"))
                    self.settingsLoaded = True
            
