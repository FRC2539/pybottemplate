from wpilib.command import CommandGroup
from wpilib.driverstation import DriverStation
import commandbased.flowcontrol as fc
from custom.config import Config

from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.pivotcommand import PivotCommand
from commands.drivetrain.runintowallcommand import RunIntoWallCommand
from commands.drivetrain.setspeedcommand import SetSpeedCommand
from commands.network.alertcommand import AlertCommand

class AutonomousCommandGroup(CommandGroup):

    def __init__(self):
        super().__init__('Autonomous')

        ds = DriverStation.getInstance()

        def getSwitch():
            if Config('Autonomous/switch') == "always":
                return True
            if Config('Autonomous/switch') == "never":
                return False
            msg = ds.getGameSpecificMessage()[0]
            location = Config('Autonomous/robotLocation')
            return msg == location

        def getScale():
            if Config('Autonomous/scale') == "always":
                return True
            if Config('Autonomous/scale') == "never":
                return False
            msg = ds.getGameSpecificMessage()[1]
            location = Config('Autonomous/robotLocation')
            return msg == location

        @fc.IF(lambda: Config('Autonomous/robotLocation') == 'L')
        def fromLeft(self):
            @fc.IF(getSwitch)
            def cubeOnSwitch(self):
                self.addSequential(MoveCommand(20))
                self.addSequential(PivotCommand(-90))
                self.addSequential(MoveCommand(10))
                self.addSequential(PivotCommand(90))
                self.addSequential(MoveCommand(10))
                self.addSequential(PivotCommand(90))
                self.addSequential(MoveCommand(5))
                self.addSequential(SetSpeedCommand(1500))
                self.addSequential(AlertCommand('We scored!', 'Info'))
                #self.addSequential(MoveCommand(20))
                #self.addSequential(PivotCommand(60))
                #self.addSequential(MoveCommand(30))
                #self.addSequential(PivotCommand(-60))
                #self.addSequential(SetSpeedCommand(1500))
                #self.addSequential(MoveCommand(32))
                #self.addSequential(AlertCommand('We scored!', 'Info'))

            @fc.ELIF(getScale)
            def cubeOnScale(self):
                pass

            @fc.ELSE
            def crossBaseline(self):
                self.addSequential(MoveCommand(100))

        @fc.ELIF(lambda: Config('Autonomous/robotLocation') == 'R')
        def fromRight(self):
            @fc.IF(getSwitch)
            def cubeOnSwitch(self):
                self.addSequential(MoveCommand(48))


                '''
                self.addSequential(MoveCommand(20))
                self.addSequential(PivotCommand(90))
                self.addSequential(MoveCommand(10))
                self.addSequential(PivotCommand(-90))
                self.addSequential(MoveCommand(10))
                self.addSequential(PivotCommand(-90))
                self.addSequential(MoveCommand(5))
                self.addSequential(SetSpeedCommand(1500))
                self.addSequential(AlertCommand('We scored!', 'Info'))
                '''

                #self.addSequential(MoveCommand(20))
                #self.addSequential(PivotCommand(-60))
                #self.addSequential(MoveCommand(30))
                #self.addSequential(PivotCommand(60))
                #self.addSequential(SetSpeedCommand(1500))
                #self.addSequential(MoveCommand(32))
                #self.addSequential(AlertCommand('We scored!', 'Info'))

            @fc.ELIF(getScale)
            def cubeOnScale(self):
                pass

            @fc.ELSE
            def crossBaseline(self):
                self.addSequential(MoveCommand(100))

        @fc.ELSE
        def middle(self):
            @fc.IF(lambda: Config('Autonomous/switch') == 'always')
            def scoreSwitch(self):
                @fc.IF(lambda: ds.getGameSpecificMessage()[0])
                def fromLeft(self):
                    self.addSequential(MoveCommand(15))
                    self.addSequential(PivotCommand(-90))
                    self.addSequential(MoveCommand(21))
                    self.addSequential(PivotCommand(90))
                    self.addSequential(MoveCommand(32))

                @fc.ELSE
                def fromRight(self):
                    self.addSequential(MoveCommand(15))
                    self.addSequential(PivotCommand(90))
                    self.addSequential(MoveCommand(11))
                    self.addSequential(PivotCommand(-90))
                    self.addSequential(MoveCommand(32))

            @fc.ELIF(lambda: Config('Autonomous/scale') == 'always')
            def scoreScale(self):
                @fc.IF(lambda: ds.getGameSpecificMessage()[1])
                def fromLeft(self):
                    pass

                @fc.ELSE
                def fromRight(self):
                    pass

            @fc.ELSE
            def crossBaselineCenter(self):
                @fc.IF(lambda: ds.getGameSpecificMessage()[0] == 'L')
                def crossRight(self):
                    self.addSequential(MoveCommand(20))
                    self.addSequential(PivotCommand(45))
                    self.addSequential(MoveCommand(60))
                    self.addSequential(PivotCommand(-45))
                    self.addSequential(MoveCommand(20))

                @fc.ELSE
                def crossLeft(self):
                    self.addSequential(MoveCommand(20))
                    self.addSequential(PivotCommand(-45))
                    self.addSequential(MoveCommand(60))
                    self.addSequential(PivotCommand(45))
                    self.addSequential(MoveCommand(20))
