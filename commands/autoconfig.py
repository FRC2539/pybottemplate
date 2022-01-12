from commands2 import SequentialCommandGroup

from commands.autonomouscommandgroup import AutonomousCommandGroup

from custom import driverhud

from networktables import NetworkTables

excludedMethods = [
    "interrupted"
]  # Methods that aren't from the parents but aren't autos. If you want to exclude a program because it might not work, add it here.

table = NetworkTables.getTable("Autonomous")
autoVars = [var.lower() for var in dir(AutonomousCommandGroup)]

definedAutos = []
for auto in autoVars:
    if (
        auto[0] != "_"  # Make sure it's not one of Python's methods.
        and auto
        not in [
            var.lower() for var in dir(SequentialCommandGroup)
        ]  # Make sure it's not from the parent.
        and auto
        not in excludedMethods  # Other methods to exclude that are in the Auto command group.
    ):
        definedAutos.append(auto)


def init():
    table.putStringArray("autos", [a.lower() for a in definedAutos])
    try:
        val = definedAutos[0]
        for auto in definedAutos:
            if auto[-1] == "0":
                val = auto
        table.putString("selectedAuto", val)
    except (IndexError):
        table.putString("selectedAuto", "NO AUTO FOUND")


def getAutoProgram():
    """
    Returns the first defined auto if none are selected.
    """
    try:
        return table.getString(
            "selectedAuto", (definedAutos[0]).lower()
        )  # Should never call the default here since default is populated above.
    except (IndexError):
        raise Exception("You don't have any autos defined!")
