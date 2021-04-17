from commands2 import SequentialCommandGroup


class AutonomousCommandGroup(SequentialCommandGroup):

    def __init__(self):
        super().__init__('Autonomous')
