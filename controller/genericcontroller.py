from wpilib import Joystick
from wpilib.buttons import JoystickButton

from .controlleraxis import ControllerAxis
from .povbutton import POVButton

class GenericController(Joystick):
    '''The base class for all controllers.'''

    namedButtons = {}
    namedAxes = {}
    invertedAxes = []

    def __init__(self, port):
        '''
        Creates attributes of this class for every button and axis defined in
        its dictionaries. Subclasses need only fill in those dictionaries
        correctly.
        '''

        super().__init__(port)

        for name, id  in self.namedButtons.items():
            if id >= 20:
                '''
                By convention, the DPad buttons are 20 through 23 and can be
                converted to POV angles by the formula below.
                '''
                
                angle = (id - 20) * 90
                self.__dict__[name] = POVButton(self, angle)
            else:
                self.__dict__[name] = JoystickButton(self, id)

        for name, id in self.namedAxes.items():
            isInverted = name in self.invertedAxes
            self.__dict__[name] = ControllerAxis(self, id, isInverted)
