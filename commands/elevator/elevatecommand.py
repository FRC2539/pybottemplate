from wpilib.command import Command

import subsystems

class ElevateCommand(Command):

    def __init__(self):
        super().__init__('Elevate')

        self.requires(subsystems.elevator)


    def initialize(self):
        subsystems.elevator.up()


    def end(self):
        subsystems.elevator.stop()
