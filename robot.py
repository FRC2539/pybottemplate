#!/usr/bin/env python3

from wpilib import IterativeRobot
from wpilib.command import Scheduler
from wpilib import driverstation
from wpilib import LiveWindow
from wpilib import run

from custom import driverhud
import subsystems


class KryptonBot(IterativeRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        self.scheduler = Scheduler.getInstance()

        subsystems.init()
        driverhud.init()

        self.autonomousPeriodic = self.commandPeriodic
        self.teleopPeriodic = self.commandPeriodic
        self.disabledPeriodic = self.commandPeriodic


    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''

        # Schedule the autonomous command
        driverhud.getAutonomousProgram().start()


    def commandPeriodic(self):
        '''
        Run the scheduler regularly. If an error occurs during a competition,
        prevent it from crashing the program.
        '''

        try:
            self.scheduler.run()
        except Exception as error:
            if not driverstation.getInstance().isFMSAttached():
                raise

            driverhud.showAlert('Error: %s' % error)

            '''Just to be safe, stop all running commands.'''
            self.scheduler.removeAll()


    def testPeriodic(self):
        '''
        Test mode will not run normal commands, but motors can be controlled
        and sensors viewed with the SmartDashboard.
        '''

        LiveWindow.run()


if __name__ == '__main__':
    run(KryptonBot)
