from wpimath.kinematics import (
    SwerveDrive4Odometry,
    SwerveDrive4Kinematics,
    SwerveModuleState,
)
from wpimath.geometry import Translation2d, Rotation2d, Pose2d

from .cougarsystem import *
from .basedrive import BaseDrive
from .swervemodule import SwerveModule

import ports
import constants

import math


class SwerveDrive(BaseDrive):
    def __init__(self, name):
        super().__init__(name)

        """
        "Rollers? Where we're going, we don't need 'rollers'." - Ben Bistline, 2021
        
        The constructor for the class. When returning lists, it should follow like:
        [front left, front right, back left, back right]
        """

        if not constants.drivetrain.swerveStyle:
            self.move = self.tankMove
            self._calculateSpeeds = self.tankCalculateSpeeds

        self.isFieldOriented = True

        self.speedLimit = (
            constants.drivetrain.speedLimit
        )  # Override the basedrive without editing the file.

        self.modules = [
            SwerveModule(  # Front left module.
                ports.drivetrain.frontLeftDriveID,
                ports.drivetrain.frontLeftTurnID,
                ports.drivetrain.frontLeftCANCoder,
                self.speedLimit,
                -255.761719,
            ),
            SwerveModule(  # Front right module.
                ports.drivetrain.frontRightDriveID,
                ports.drivetrain.frontRightTurnID,
                ports.drivetrain.frontRightCANCoder,
                self.speedLimit,
                -273.8672,
                invertedDrive=constants.drivetrain.swerveStyle,  # Invert for some reason?
            ),
            SwerveModule(  # Back left module.
                ports.drivetrain.backLeftDriveID,
                ports.drivetrain.backLeftTurnID,
                ports.drivetrain.backLeftCANCoder,
                self.speedLimit,
                -41.484375,
            ),
            SwerveModule(  # Back right module.
                ports.drivetrain.backRightDriveID,
                ports.drivetrain.backRightTurnID,
                ports.drivetrain.backRightCANCoder,
                self.speedLimit,
                -129.726563,
                invertedDrive=constants.drivetrain.swerveStyle,  # Invert for some reason. Ezra's going nuts lol.
            ),
        ]

        self.swerveKinematics = (
            SwerveDrive4Kinematics(  # X and Y components of center offsets.
                Translation2d(0.427799754, 0.427799754),  # Front left module
                Translation2d(0.427799754, -0.427799754),  # Front right module
                Translation2d(-0.427799754, 0.427799754),  # Back left module
                Translation2d(-0.427799754, -0.427799754),  # Back right module
            )
        )

        self.swerveOdometry = SwerveDrive4Odometry(
            self.swerveKinematics,
            self.navX.getRotation2d(),
            Pose2d(0, 0, Rotation2d(0)),
        )

        self.resetOdometry()
        self.resetGyro()
        self.PosX = 0
        self.PosY = 0
        self.LastPositions = self.getPositions()

    def periodic(self):
        """
        Loops whenever there is robot code. I recommend
        feeding networktable values here.
        """

        self.feed()  # Update the desired

        self.updateOdometry()

        Angles = self.getModuleAngles()
        Distance = []
        Positions = self.getPositions()
        for pos, lPos in zip(Positions, self.LastPositions):
            Distance.append(pos - lPos)
        VectorX = 0
        VectorY = 0
        for angle, distance in zip(Angles, Distance):
            VectorX += math.cos(math.radians(angle - 180)) * distance
            VectorY += math.sin(math.radians(angle - 180)) * distance
        VectorX = VectorX / 4
        VectorY = VectorY / 4
        PolarR = math.sqrt(VectorX ** 2 + VectorY ** 2)
        PolarTheta = math.degrees(math.atan2(VectorY, VectorX))

        PolarTheta -= self.getAngle()
        VectorX = math.cos(math.radians(PolarTheta + 90)) * PolarR
        VectorY = math.sin(math.radians(PolarTheta + 90)) * PolarR

        self.PosX += VectorX
        self.PosY += VectorY
        self.LastPositions = self.getPositions()

    def GenerateRobotVector(self):
        Angles = self.getModuleAngles()
        Speeds = self.getSpeeds()
        VectorX = 0
        VectorY = 0
        for angle, speed in zip(Angles, Speeds):
            VectorX += math.cos(math.radians(angle - 180)) * speed
            VectorY += math.sin(math.radians(angle - 180)) * speed
        VectorX = VectorX / 4
        VectorY = VectorY / 4
        return VectorX, VectorY

    def waitForRoll(self):
        """
        Forces the robot to wait until
        it's not tipping.
        """
        while abs(self.navX.getRoll()) > 5:
            pass

    def updateOdometry(self):
        """
        Updates the WPILib odometry object
        using the gyro and the module states.
        """

        states = self.getModuleStates()

        self.swerveOdometry.update(
            self.navX.getRotation2d(),
            states[0],  # 0
            states[1],  # 1
            states[2],  # 2
            states[3],  # 3
        )

    def resetOdometry(self, pose=Pose2d(0, 0, Rotation2d(0))):
        """
        Resets the odometry to a given position, typically the one used when starting a trajectory.
        """
        self.swerveOdometry.resetPosition(pose, self.navX.getRotation2d())

    def getSwervePose(self):
        """
        Get the odometry's idea of the position
        """
        return self.swerveOdometry.getPose()

    def getChassisSpeeds(self):
        """
        Returns the robots velocity and heading, using
        module states, in the form of a ChassisSpeeds object.
        """

        return self.swerveKinematics.toChassisSpeeds(self.getModuleStates())

    def getChassisSpeedsData(self):
        """
        Basically the same thing as getChassisSpeeds, but this one
        extracts the data and returns the useful stuff in a list, which
        looks like this: [vx_fps, vy_fps, omega_dps].
        """

        speeds = self.swerveKinematics.toChassisSpeeds(self.getModuleStates())

        return [speeds.vy_fps, -speeds.vx_fps, speeds.omega_dps]

    def _configureMotors(self):
        """
        Configures the motors. Shouldn't need this.
        """

        self.activeMotors = self.motors[
            0:2
        ]  # Don't actually need these, this just keeps basedrive happy.

    def _calculateSpeeds(self, x, y, rotate):
        """
        Gonna take this nice and slow. Declaring variables to be simple,
        should try to walk through while coding.
        """

        """
        'self.getAngle()' is the robot's heading, 
        multiply it by pi over 180 to convert to radians.
        """

        theta = self.getAngleTo(0) * (
            math.pi / 180
        )  # Gets the offset to zero, -180 to 180.

        if (
            self.isFieldOriented
        ):  # Are we field-centric, as opposed to robot-centric. A tank drive is robot-centric, for example.

            temp = y * math.cos(theta) + x * math.sin(
                theta
            )  # just the new y value being temporarily stored.
            x = -y * math.sin(theta) + x * math.cos(theta)
            y = temp

        """
        The bottom part is the most confusing part, but it basically uses ratios and vectors with the
        pythagorean theorem to calculate the velocities.
        """
        A = x - rotate * (self.wheelBase / self.r)  # Use variables to simplify it.
        B = x + rotate * (self.wheelBase / self.r)
        C = y - rotate * (self.trackWidth / self.r)
        D = y + rotate * (self.trackWidth / self.r)

        ws1 = math.sqrt(B ** 2 + D ** 2)  # Front left speed
        ws2 = math.sqrt(B ** 2 + C ** 2)  # Front right speed
        ws3 = math.sqrt(A ** 2 + D ** 2)  # Back left speed
        ws4 = math.sqrt(A ** 2 + C ** 2)  # Back right speed

        wa1 = math.atan2(B, D) * 180 / math.pi  # Front left angle
        wa2 = math.atan2(B, C) * 180 / math.pi  # Front right angle
        wa3 = math.atan2(A, D) * 180 / math.pi  # Back left angle
        wa4 = math.atan2(A, C) * 180 / math.pi  # Back right angle

        speeds = [ws2, ws1, ws4, ws3]  # It is in order (FL, FR, BL, BR).
        angles = [wa2, wa1, wa4, wa3]  # It is in order (FL, FR, BL, BR).

        newSpeeds = speeds  # Do NOT delete! This IS used!
        newAngles = angles

        maxSpeed = max(speeds)  # Find the largest speed.
        minSpeed = min(speeds)  # Find the smallest speed.

        if (
            maxSpeed > 1
        ):  # Normalize speeds if greater than 1, but keep then consistent with each other.
            speeds[:] = [
                speed / maxSpeed for speed in speeds
            ]  # We can do this by dividing ALL by the largest value.

        if (
            minSpeed < -1
        ):  # Normalize speeds if less than -1, but keep then consitent with each other.
            speeds[:] = [
                speed / minSpeed * -1 for speed in speeds
            ]  # We can do this by dividing ALL by the smallest value. The negative maintains the signs.

        magnitude = math.sqrt(
            (x ** 2) + (y ** 2)
        )  # Pythagorean theorem, vector of joystick.
        if magnitude > 1:
            magnitude = 1

        speeds[:] = [
            speed * magnitude for speed in speeds
        ]  # Ensures that the speeds of the motors are relevant to the joystick input.
        return newSpeeds, angles  # Return the calculated speed and angles.

    def move(self, x, y, rotate):
        """
        Turns coordinate arguments into motor outputs.
        Short-circuits the rather expensive movement calculations if the
        coordinates have not changed.
        """
        if [x, y, rotate] == [0, 0, 0]:
            self.stop()
            return

        """Prevent drift caused by small input values"""
        x = math.copysign(max(abs(x) - self.deadband, 0), x)
        y = math.copysign(max(abs(y) - self.deadband, 0), y)
        rotate = math.copysign(max(abs(rotate) - (self.deadband + 0.05), 0), rotate)

        speeds, angles = self._calculateSpeeds(x, y, rotate)

        if (
            x == 0 and y == 0 and rotate != 0
        ):  # The robot won't apply power if it's just rotate (fsr?!)
            for module, angle in zip(
                self.modules, angles
            ):  # You're going to need encoders, so only focus here.
                module.setWheelAngle(angle)
                module.setWheelSpeed(abs(rotate))

        else:
            for module, speed, angle in zip(
                self.modules, speeds, angles
            ):  # You're going to need encoders, so only focus here.
                module.setWheelAngle(angle)
                module.setWheelSpeed(abs(math.sqrt(speed ** 2 + rotate ** 2)))

    def tankMove(self, y, rotate):
        if [y, rotate] == self.lastInputs:
            return

        self.lastInputs = [y, rotate]

        """Prevent drift caused by small input values"""
        if self.useEncoders:
            y = math.copysign(max(abs(y) - self.deadband, 0), y)
            rotate = math.copysign(max(abs(rotate) - self.deadband, 0), rotate)

        speeds = self.tankCalculateSpeeds(y, rotate)

        for module, speed in zip(self.modules, speeds):
            module.setWheelAngle(0)
            module.setWheelSpeed(speed)

    def tankCalculateSpeeds(self, y, rotate):
        return [y + rotate, -y + rotate, y + rotate, -y + rotate]  # FL, FR, BL, BR

    def stop(self):
        """
        Stops the modules.
        """
        for module in self.modules:
            module.stopModule()

    def longStop(self):
        """
        Returns true when all wheel speeds
        are zero.
        """
        self.stop()
        while self.getSpeeds().count(0) < 3:
            pass

    def resetEncoders(self, anArgumentAsWell=0):
        """
        Resets all drive encoders to 0 by default.
        """
        for module in self.modules:
            module.resetDriveEncoders(anArgumentAsWell)

    def setProfile(self, profile):
        """
        Sets the profile for both drive and turn motors.
        """
        for module in self.modules:
            module.setModuleProfile(profile)

    def setModuleProfiles(self, id_=0, drive=True, turn=True):
        """
        Sets the PID profiles for each of the modules.
        This one accepts an optional turn and drive.
        """
        for module in self.modules:
            module.setModuleProfile(id_, drive, turn)

    def updateCANCoders(self, positions: list):
        """
        Sets the position of the CANCoders. Be careful using
        this method!
        """
        for module, position in zip(self.modules, positions):
            module.updateCANCoder(position)

    def setSpeedLimit(self, speed):
        """
        Sets the speed limit of the drive motor in
        inches per second.
        """
        self.speedLimit = speed

        for module in self.modules:
            module.speedLimit = speed

    def setFieldOriented(self, fieldCentric=True):
        """
        Changes the orientation of the robot. It should almost always be
        field centric on a swerve robot.
        """
        self.isFieldOriented = fieldCentric

    def getModuleStates(self):
        """
        Returns a list of SwerveModuleState objects.
        Usefulf for chassis speeds and odometry.
        """

        states = []
        for module in self.modules:
            s = module.getWheelSpeed() / 39.3701  # In Meters Per Second
            a = Rotation2d(math.radians(module.getWheelAngle() - 180))
            states.append(SwerveModuleState(s, a))

        return states

    def setModuleStates(self, moduleStates):
        """
        Set the states of the modules. Used by trajectory stuff.
        """
        for module, state in zip(self.modules, moduleStates):
            module.setState(state)

    def getSpeeds(self, inIPS=True):  # Defaults to giving in inches per second.
        """
        Returns the speeds of the wheel.
        """
        return [module.getWheelSpeed(inIPS) for module in self.modules]

    def setSpeeds(self, speeds: list):  # Set a speed in inches per second.
        """
        Sets the speeds of the wheels in inches per second.
        It takes a list. Please use setUniformModuleSpeed if
        you want to set the same speed amongst all the modules.
        """
        for module, speed in zip(self.modules, speeds):
            module.setWheelSpeed(speed)

    def setUniformModuleSpeed(self, speed: float):  # Set a speed in inches per second.
        """
        Sets a uniform speed to eall the drive motors in inches per
        second. This takes a float because all modules use
        the same speed. Use the setSpeeds method if you want to pass
        a list of different speeds.
        """
        for module in self.modules:
            module.setWheelSpeed(speed)

    def getPercents(self):
        """
        Returns the percent outputs of each drive motor.
        """
        return [module.getWheelPercent() for module in self.modules]

    def setPercents(self, speeds: list):
        """
        Sets the percent speed of each module's drive motor.
        """
        for module, speed in zip(self.modules, speeds):
            module.setWheelPercent(speed)

    def setUniformModulePercent(self, speed: float):
        """
        Sets a uniform percent to the drive motor
        of each module.
        """
        for module in self.modules:
            module.setWheelPercent(speed)

    def getModuleAngles(self):
        """
        Returns the CANCoder's absolute reading.
        Note, this does take into account the magnet
        offset which we set at the beginning.
        I think, 180 is forward, 0 is backwards. It
        returns between 0 and 360.
        """

        # Add module in front, not to be confused with gyro! Returns degrees.
        return [module.getWheelAngle() % 360 for module in self.modules]

    def setModuleAngles(self, angles: list):  # Set a list of different angles.
        """
        Set the angle of the wheel using the turn motor.
        This method takes a list of angles, 0-360 degrees.
        """

        for module, angle in zip(self.modules, angles):
            module.setWheelAngle(angle)

    def setUniformModuleAngle(self, angle: int):
        """
        Set the angle of the wheel using the turn motor.
        This method takes a universal angle to set to all
        modules. The angle should be 0-360 degrees.
        """
        for module in self.modules:
            module.setWheelAngle(angle)

    def getPositions(self, inInches=True):  # Defaults to giving in inches.
        """
        Returns the module position in inches (by default).
        """
        return [module.getModulePosition(inInches) for module in self.modules]

    def setPositions(self, positions: list):
        """
        Sets the position of the modules. It will go forward this many inches.
        I recommend using the setUniformModulePosition however.
        Remember, provide these in inches. It will go forward/back x many inches.
        """
        for module, position in zip(self.modules, positions):
            module.setModulePosition(position)

    def setUniformModulePosition(self, distance):
        """
        Sets a uniform distance for the drive motor to travel. Note,
        you should give the distance in inches. The modules will move this
        much in the direction they are facing.
        """
        for module in self.modules:
            module.setModulePosition(distance)

    def getQuadraticBezierPosition(self, p: list, t):
        """
        Returns the position in the quadratic Bezier curve, given
        the control points and the percentage through the
        curve. See https://math.stackexchange.com/questions/1360891/find-quadratic-bezier-curve-equation-based-on-its-control-points.
        """

        # Returns (x, y) @ % = t
        return (
            ((1 - t) ** 2 * p[0][0] + 2 * t * (1 - t) * p[1][0] + t ** 2 * p[2][0]),
            ((1 - t) ** 2 * p[0][1] + 2 * t * (1 - t) * p[1][1] + t ** 2 * p[2][1]),
        )

    def getCubicBezierPosition(self, p: list, t: float):
        """
        Returns the position in the cubic Bezier curve, given
        the control points and the percentage through the
        curve. NOTE: Doesn't seem to be working. Please use
        getHigherBezierPositionInstead instead.
        """

        # Returns (x, y) @ % = t
        return (
            (
                (1 - t) ** 3 * p[0][0]
                + 3 * (1 - t) ** 2 * p[1][0]
                + 3 * (1 - t) ** 2 * p[2][0]
                + t ** 3 * p[3][0]
            ),
            (
                (1 - t) ** 3 * p[0][1]
                + 3 * (1 - t) ** 2 * p[1][1]
                + 3 * (1 - t) ** 2 * p[2][1]
                + t ** 3 * p[3][1]
            ),
        )

    def getHigherBezierPosition(self, p: list, t: float):
        """
        Ok this math is going to kill the robot lol. Look here:
        https://en.wikipedia.org/wiki/B%C3%A9zier_curve#General_definition
        for the math behind what I'm about to write. Tested, it
        works! Look at test. Test can be found here:
        https://www.researchgate.net/figure/Quintic-trigonometric-Bezier-curve-with-a-b_fig2_318599090
        """

        # The for loop will act as our summation.
        # Start at one, end at our given number.
        xSum = 0
        ySum = 0

        # Don't subtrct one here so we can iterate through each point.
        for i in range(len(p)):
            x = p[i][0]
            y = p[i][1]

            # Binomial coefficient stuff here ('n' is the 'w'):
            # https://math.stackexchange.com/questions/1713706/what-does-2-values-vertically-arranged-in-parenthesis-in-an-equation-mean
            # Remember, 'n' is NOT number of points; instead, it's the degree. This means an 'n' of five has six points.
            n = len(p) - 1
            binomialCoefficient = math.factorial(n) / (
                math.factorial(i) * math.factorial(n - i)
            )

            xSum += binomialCoefficient * (1 - t) ** (n - i) * t ** i * x
            ySum += binomialCoefficient * (1 - t) ** (n - i) * t ** i * y

        return (xSum, ySum)

    def getQuadraticBezierSlope(self, p: list, t):
        """
        Returns the slope of the current position along
        a quadratic bezier curve, defined by three given control points.
        """

        # Define the given points.
        x0 = p[0][0]
        y0 = p[0][1]
        x1 = p[1][0]
        y1 = p[1][1]
        x2 = p[2][0]
        y2 = p[2][1]

        # 'a' is the x, 'b' is the y
        a0 = x0 - (x0 - x1) * t
        b0 = y0 - (y0 - y1) * t

        a1 = x1 - (x1 - x2) * t
        b1 = y1 - (y1 - y2) * t

        # Return the slope as (y, x) of the two points we just calculated.
        return ((b1 - b0), (a1 - a0))

    def getCubicBezierSlope(self, p: list, t):
        """
        Returns the slope of the current position along
        a cubic bezier curve, defined by four given control points.
        """

        # Define the given points.
        x0 = p[0][0]
        y0 = p[0][1]
        x1 = p[1][0]
        y1 = p[1][1]
        x2 = p[2][0]
        y2 = p[2][1]
        x3 = p[3][0]
        y3 = p[3][1]

        # 'a' is the x, 'b' is the y
        a0 = x0 - (x0 - x1) * t
        b0 = y0 - (y0 - y1) * t

        a1 = x1 - (x1 - x2) * t
        b1 = y1 - (y1 - y2) * t

        a2 = x2 - (x2 - x3) * t
        b2 = y2 - (y2 - y3) * t

        c0 = a0 - (a0 - a1) * t
        d0 = b0 - (b0 - b1) * t

        c1 = a1 - (a1 - a2) * t
        d1 = b1 - (b1 - b2) * t

        # Return the slope calculated using the previous points
        return ((d1 - d0), (c1 - c0))

    def getHigherBezierSlope(self, p: list, t):
        """
        The derivative of the equation for the points.
        Note, it will be in terms of t. To make it in terms of dx/dy, we
        have to do division; more info here:
        https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/Bezier/bezier-der.html
        (lol this page is from my college!)
        """

        dxDt = 0
        dyDt = 0

        # The for loop will act as our summation again.
        for i in range(len(p) - 1):
            x = p[i][0]
            y = p[i][1]

            nextX = p[i + 1][0]
            nextY = p[i + 1][1]

            # View the position method for binomial coefficient info.
            n = len(p) - 2
            binomialCoefficient = math.factorial(n) / (
                math.factorial(i) * math.factorial(n - i)
            )

            # (n + 1) restores 'n's original value, the length of p.
            qX = (n + 1) * (nextX - x)
            qY = (n + 1) * (nextY - y)

            dxDt += binomialCoefficient * (1 - t) ** (n - i) * t ** i * qX
            dyDt += binomialCoefficient * (1 - t) ** (n - i) * t ** i * qY

        # According to parametric differentiation, we can do the following, and get dyDx.
        return (dyDt, dxDt)

    def getQuadraticBezierLength(self, p: list):
        """
        Returns the length of a Quadratic Bezier
        curve given via control points. Source:
        https://gist.github.com/tunght13488/6744e77c242cc7a94859.
        """

        # Divide the points into invidual lists of x's and y's.
        xs, ys = map(list, zip(*p))

        # Are all of the x's the same?
        if len(xs) == xs.count(xs[0]):
            length = 0
            initial = 0
            for y in list(enumerate(ys)):
                length += abs(y[1] - initial)
                initial = ys[y[0]]

            return length

        # Are all of the y's the same?
        elif len(ys) == ys.count(ys[0]):
            length = 0
            initial = 0
            for x in list(enumerate(xs)):
                length += abs(x[1] - initial)
                initial = xs[x[0]]

            return length

        positions = self.createPositionObjects(p)

        if len(positions) != 3:
            raise Exception("Bruh this is a quadratic. Three points!")

        pointOne, pointTwo, pointThree = positions[0], positions[1], positions[2]

        aX = pointOne.x - 2 * pointTwo.x + pointThree.x
        aY = pointOne.y - 2 * pointTwo.y + pointThree.y

        bX = 2 * pointTwo.x - 2 * pointOne.x
        bY = 2 * pointOne.y - 2 * pointTwo.y

        A = 4 * (aX ** 2 + aY ** 2)
        B = 4 * (aX * bX + aY * bY)
        C = bX ** 2 + bY ** 2

        SABC = 2 * math.sqrt(A + B + C)
        A2 = math.sqrt(A)
        A32 = 2 * A * A2
        C2 = 2 * math.sqrt(C)
        BA = B / A2

        return (
            A32 * SABC
            + A2 * B * (SABC - C2)
            + (4 * C * A - B * B) * math.log((2 * A2 + BA + SABC) / (BA + C2))
        ) / (4 * A32)

    def getHigherBezierLength(self, p: list, iterations: int = 1000):
        """
        Ok. So with cubic bezier, their is no closed-integral
        definition for the cubic Bezier length. I've done lot's
        of research, and it appears as there is an approximation.
        We can approximate it by adding individual line segments together.
        "iterations" will track how many divisions we make, and thus
        the precision. Read up here https://www.lemoda.net/maths/bezier-length/index.html.
        1000 iterations is pretty good for our purposes.
        """

        # Establish the total length variable and previous position.
        length = 0
        previousX = 0
        previousY = 0

        # Iterate through each step, taking the length of each sum with Pythagorean Theorem.
        for i in range(iterations + 1):
            t = i / iterations

            # "positions" is (x,y).
            positions = self.getHigherBezierPosition(p, t)

            if i > 0:
                xDiff = positions[0] - previousX
                yDiff = positions[1] - previousY
                length += math.sqrt(xDiff ** 2 + yDiff ** 2)

            previousX = positions[0]
            previousY = positions[1]

        # Return the sum of the segments.
        return length

    def createPositionObjects(self, points: list):
        """
        Creates Position objects using a given list
        of Xs and Ys. Returns that new list.
        """
        return [Position(coord[0], coord[1]) for coord in points]

    # Cougar Course Below.

    def injectBetweenTwoPoints(self, startPoint: list, endPoint: list, spacing=1):
        """
        Used in CougarCourse. Adds additional points.
        """

        reverseNessesary = False
        print(startPoint)
        print("e " + str(endPoint))

        if startPoint[1] < endPoint[1]:
            x1, y1 = startPoint[0], startPoint[1]
            x2, y2 = endPoint[0], endPoint[1]
        elif startPoint[1] > endPoint[1]:
            x2, y2 = startPoint[0], startPoint[1]
            x1, y1 = endPoint[0], endPoint[1]
            reverseNessesary = True
        else:
            raise Exception("Start and end point cannot be the same!")

        pointsInBetween = [[x1, y1]]

        totalDistance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Calculate spacing.
        numOfPoints = math.ceil(totalDistance / spacing)
        spacing = totalDistance / numOfPoints

        # Angle diff.
        theta = math.atan((y2 - y1) / (x2 - x1))

        for segment in range(numOfPoints):
            newX = math.sin(theta) * spacing + x1
            newY = math.cos(theta) * spacing + y1

            pointsInBetween.append([newX, newY])

            x1 = newX  # Override for next loop.
            y1 = newY  # Override for next loop.

        if reverseNessesary:
            pointsInBetween.reverse()

        return pointsInBetween

    def injectPoints(self, points: list, spacing=1):
        """
        Inject points between a series of points. Used in the CougarCourse.
        """
        final = []
        for point in points:
            startPoint = [point[0], point[1]]
            endPoint = [point[2], point[3]]

            pointsToInsert = self.injectBetweenTwoPoints(startPoint, endPoint, spacing)

            for point in pointsToInsert:
                final.append(point)

        return final

    def smoothPoints(
        self, path: list, weightData=0.75, weightSmooth=0.25, tolerance=0.001
    ):
        """
        Curves a lot of points. Used in
        CougarCourse.
        """
        newPath = path.copy()

        change = tolerance
        while change >= tolerance:  # You touch this, you die.
            change = 0
            i = 1
            while i < len(path) - 1:

                j = 0
                while j < len(path[i]):
                    aux = newPath[i][j]
                    newPath[i][j] += weightData * (
                        path[i][j] - newPath[i][j]
                    ) + weightSmooth * (
                        newPath[i - 1][j] + newPath[i + 1][j] - (2 * newPath[i][j])
                    )
                    change += abs(aux - newPath[i][j])

                    j += 1

                i += 1

        return newPath

    def assertDistanceAlongCurve(self, points: list):
        """
        Adds the distance travelled to the points by using
        the distance formula. Used in CougarCourse.
        """
        points[0].append(0)
        i = 1
        while i < len(points):
            points[i].append(
                points[i - 1][2]
                + math.sqrt(
                    (points[i][0] - points[i - 1][0]) ** 2
                    + (points[i][1] - points[i - 1][1]) ** 2
                )
            )
            i += 1

        return points

    def setCruiseVelocity(self, slow=False):
        """
        Changes the motion magic's max cruise velocity.
        Used in CougarCourse.
        """
        for module in self.modules:
            module.setDriveCruiseVelocity(slow)


class Position:
    """
    No, not that garbage by Ariane Grande. Stores
    An X and Y value for convenience.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
