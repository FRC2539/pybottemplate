#!/usr/bin/env python3

from commandbased import CommandBasedRobot
from wpilib._impl.main import run

from custom import driverhud
import subsystems


class KryptonBot(CommandBasedRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        subsystems.init()
        driverhud.init()


    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''

        # Schedule the autonomous command
        driverhud.getAutonomousProgram().start()


    def handleCrash(self, error):
        super().handleCrash()
        driverhud.showAlert('Fatal Error: %s' % error)


if __name__ == '__main__':
    run(KryptonBot)
