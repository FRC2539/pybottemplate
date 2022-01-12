from commands2 import CommandBase
from subsystems.swervedrive import SwerveDrive
from custom import driverhud
from custom.config import MissingConfigError
import robot


class MoveCommand(CommandBase):
    def __init__(self, distance, angle=0, tolerance=5, slow=False, name=None):
        """
        Takes a distance in inches and stores it for later. We allow overriding
        name so that other autonomous driving commands can extend this class.
        """

        if name is None:
            name = "Move %f inches" % distance

        super().__init__()

        if isinstance(robot.drivetain, SwerveDrive):

            self.distance = -distance
            self.angle = angle
            self.tol = tolerance  # Angle tolerance in degrees.
            self.isSlow = slow

            self.moveSet = False
            self.addRequirements(robot.drivetrain)

    def swerveInitialize(self):
        if self.isSlow:
            robot.drivetrain.setCruiseVelocity(True)

        robot.drivetrain.setModuleProfiles(1, turn=False)

        self.count = 0
        self.startPos = robot.drivetrain.getPositions()

        robot.drivetrain.setUniformModuleAngle(self.angle)

    def execute(self):

        self.count = 0
        if self.count != 4 and not self.moveSet:
            print(robot.drivetrain.getModuleAngles())
            for currentAngle in robot.drivetrain.getModuleAngles():
                if (
                    abs(currentAngle - self.angle) < self.tol
                    or abs(currentAngle - self.angle - 360) < self.tol
                ):
                    self.count += 1
                else:
                    continue

        if self.count == 4:  # All angles aligned.
            robot.drivetrain.setPositions(
                [self.distance, self.distance, self.distance, self.distance]
            )

            self.moveSet = True

        robot.drivetrain.setUniformModuleAngle(self.angle)

    def isFinished(self):
        count = 0
        for position, start in zip(robot.drivetrain.getPositions(), self.startPos):
            if abs(position - (start + self.distance)) < 4:
                count += 1
            else:
                return False

        if count == 4:
            return True

    def end(self, interrupted):
        print("WHAT")
        robot.drivetrain.stop()
        robot.drivetrain.setCruiseVelocity()
        robot.drivetrain.setModuleProfiles(0, turn=False)
        self.moveSet = False
