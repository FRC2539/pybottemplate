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

        # targetInfo = NetworkTable::GetTable("cameraTarget");

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
        if pivotDirection == 0:
                self.rightPivotMotor.set(20000)
        elif pivotDirection == 1:
                self.rightPivotMotor.set(-20000)

            
    def atKnownPosition(self):
        if not self.settingsLoaded:
            preferences = Preferences.getInstance()
            if (preferences.containsKey("shooterPosition")):
                    self.rightPivotMotor.setPosition(preferences.getInt("shooterPosition"))
                    self.settingsLoaded = True
            
