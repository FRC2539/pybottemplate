import commandbased.flowcontrol as fc


class AutonomousCommandGroup(fc.CommandFlow):

    def __init__(self):
        super().__init__('Autonomous')

        # Add commands here with self.addSequential() and self.addParallel()
