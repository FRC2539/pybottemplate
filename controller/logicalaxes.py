"""
A store for axes that are used by commands, without dictating which controller
axis the command reads. A command should call the registerAxis method with a
name. An attribute with that name will then be added to this module. By default
the axis is not attached to a controller and always reads zero. To send actual
controller axis values to the command, assign it to the logical axis in OI.
"""

from .unassignedaxis import UnassignedAxis


def registerAxis(name):

    """
    This gives us access to this module's global variables so we can add new
    attributes to the module.
    """
    vars = globals()

    if not name in vars:
        vars[name] = UnassignedAxis()
