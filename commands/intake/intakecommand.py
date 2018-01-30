from wpilib.command.command import Command

import subsystems

class IntakeCommand(Command):

    def __init__(self):
        super().__init__('Intake')

        self.requires(subsystems.intake)


    def initialize(self):
        subsystems.intake.intake()


    def isFinished(self):
        return subsystems.intake.isCubeInIntake()
