class ControllerAxis:
    '''Represents an axis of a joystick.'''

    def __init__(self, controller, id, isInverted):
        '''
        An axis is considered inverted if pushing up gives a negative result.
        In that case, we multiply its value by -1 before returning it.
        '''
        self.controller = controller
        self.id = id
        self.isInverted = isInverted

    def get(self):
        value = self.controller.getRawAxis(self.id)
        if self.isInverted:
            value *= -1

        return value
