#!/usr/bin/env python3

from commands2 import TimedCommandRobot
from wpilib._impl.main import run
from wpilib import RobotBase

from commands import autoconfig
from custom import driverhud
import controller.layout
import subsystems
import shutil, sys

from subsystems.cougarsystem import CougarSystem

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain

class KryptonBot(TimedCommandRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        if RobotBase.isSimulation():
            import mockdata

        self.subsystems()

        from commands.startupcommandgroup import StartUpCommandGroup
        StartUpCommandGroup().schedule()

        driverhud.init()
        autoconfig.init()
        controller.layout.init()

        self.selectedAuto = autoconfig.getAutoProgram()
        
    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        auton = driverhud.getAutonomousProgram()
        auton.start()
        driverhud.showInfo("Starting %s" % auton)


    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert('Fatal Error: %s' % error)


    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules['robot']
        for key, var in vars.items():
            try:
                if issubclass(var, CougarSystem) and var is not CougarSystem:
                    try:
                        setattr(module, key, var())
                    except TypeError as e:
                        raise ValueError(f'Could not instantiate {key}') from e
            except TypeError:
                pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        shutil.rmtree('opkg_cache', ignore_errors=True)
        shutil.rmtree('pip_cache', ignore_errors=True)

    run(KryptonBot)
