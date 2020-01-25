from wpilib.buttons import Button

class POVButton(Button):
    '''
    Turns DPad readings into button presses, so they can be used like any other
    button.
    '''

    def __init__(self, controller, angle):
        '''
        Pressing up on the DPad returns 0, up/right returns 45, right return 90
        and so on. So, we can tell if a button is pressed if the reading is
        within 45 degrees of the passed angle.
        '''

        self.validAngles = [angle, angle - 45, angle + 45]
        self.validAngles = [x % 360 for x in self.validAngles]

        self.controller = controller


    def get(self):
        '''Whether the button is pressed or not.'''
        
        return self.controller.getPOV() in self.validAngles
