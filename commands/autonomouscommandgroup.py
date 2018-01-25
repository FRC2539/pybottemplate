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
            msg = ds.getGameSpecificMessage()[0]
            location = Config('Autonomous/robotLocation')
            return msg == location

        def getScale():
            msg = ds.getGameSpecificMessage()[1]
            location = Config('Autonomous/robotLocation')
            return msg == location


        @fc.IF(lambda: Config('Autonomous/robotLocation') == 'L')
        def fromLeft(self):
            @fc.IF(getSwitch)
            def cubeOnSwitch(self):
                self.addSequential(MoveCommand(20))
                self.addSequential(PivotCommand(45))
                self.addSequential(MoveCommand(30))
                self.addSequential(PivotCommand(-45))
                self.addSequential(SetSpeedCommand(1500))
                self.addSequential(RunIntoWallCommand())
                self.addSequential(AlertCommand('We scored!', 'Info'))

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
                self.addSequential(SetSpeedCommand(1500))
                self.addSequential(RunIntoWallCommand())
                self.addSequential(AlertCommand('We scored!', 'Info'))

            @fc.ELIF(getScale)
            def cubeOnScale(self):
                pass

            @fc.ELSE
            def crossBaseline(self):
                self.addSequential(MoveCommand(100))

        @fc.ELSE
        def other(self):
            @fc.IF(lambda: Config('Autonomous/switch') == 'always')
            def scoreSwitch(self):
                pass

            @fc.ELIF(lambda: Config('Autonomous/scale') == 'always')
            def scoreScale(self):
                pass

            @fc.ELSE
            def crossBaseline(self):
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
