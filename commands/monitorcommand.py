from wpilib.command import Command

import robot


class MonitorCommand(Command):
    """Runs continually while the robot is powered on."""

    def __init__(self):
        super().__init__("MonitorCommand")

        """
        Required because this is the default command for the monitor subsystem.
        """
        self.requires(robot.monitor)

        self.setInterruptible(False)
        self.setRunWhenDisabled(True)

    def execute(self):
        """Implement watchers here."""
        pass
