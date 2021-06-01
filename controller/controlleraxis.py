class ControllerAxis:
    """Represents an axis of a joystick."""

    def __init__(self, controller, id, isInverted):
        """
        An axis is considered inverted if pushing up gives a negative result.
        In that case, we multiply its value by -1 before returning it.
        """

        if isInverted:
            self.get = lambda: -1 * controller.getRawAxis(id)
        else:
            self.get = lambda: controller.getRawAxis(id)
