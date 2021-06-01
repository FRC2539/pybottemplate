#!/usr/bin/env python3

from commands2 import TimedCommandRobot
from wpilib._impl.main import run
from wpilib import RobotBase, DriverStation

from custom import driverhud
import controller.layout
import subsystems
import shutil, sys, os, inspect

from commands2 import SubsystemBase, CommandScheduler

from commands import autoconfig
from commands.autonomouscommandgroup import AutonomousCommandGroup

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain
from subsystems.cougarsystem import CougarSystem

import math


class KryptonBot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""

        if RobotBase.isSimulation():
            import mockdata

        DriverStation.getInstance().silenceJoystickConnectionWarning(True)  # Amen!

        self.subsystems()

        controller.layout.init()
        autoconfig.init()
        driverhud.init()

        self.selectedAuto = autoconfig.getAutoProgram()
        self.auto = AutonomousCommandGroup()

        from commands.startupcommandgroup import StartUpCommandGroup

        StartUpCommandGroup().schedule()

        from commands.drivetrain.drivecommand import DriveCommand

    def autonomousInit(self):
        """This function is called each time autonomous mode starts."""

        from commands.autonomouscommandgroup import AutonomousCommandGroup

        from commands2 import InstantCommand

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        self.auto.schedule()

        driverhud.showInfo("Starting %s" % self.auton)

    def disabledInit(self):
        try:
            self.auton.disable()  # TODO: Fix this.
        except (AttributeError):
            pass

    def disabledPeriodic(self):
        if autoconfig.getAutoProgram() != self.selectedAuto:
            self.selectedAuto = autoconfig.getAutoProgram()
            self.auto = AutonomousCommandGroup()
            # Recreate the auto and its counterparts if the selection changes.

    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert("Fatal Error: %s" % error)

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules["robot"]
        for key, var in vars.items():
            try:
                if issubclass(var, CougarSystem) and var is not CougarSystem:
                    try:
                        setattr(module, key, var())
                    except TypeError as e:
                        print("failed " + str(key))
                        raise ValueError(f"Could not instantiate {key}") from e
            except TypeError:
                pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        shutil.rmtree("opkg_cache", ignore_errors=True)
        shutil.rmtree("pip_cache", ignore_errors=True)

    run(KryptonBot)
