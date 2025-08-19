'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''


import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import ProSelectHybridKeyboardOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.KeyboardWorkflowUIXSOperations import KeyboardWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.KeyboardWorkflowUISOperations import KeyboardWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.KeyboardWorkflowUIMOperations import KeyboardWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.KeyboardWorkflowUILOperations import KeyboardWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.KeyboardWorkflowUIXLOperations import KeyboardWorkflowUIXLOperations


class spice_keyboard_app(object):
    uitype = None
    uisize = None
    

    def __init__(self, experience, size):

        uitype = experience
        uisize = size

    @property    
    def keyBoard(self):
        if self.uitype == "ProSelect":
            if self.uitheme == "hybridTheme":
                return ProSelectHybridKeyboardOperations(self)
            else:
                return ProSelectKeyboardOperations(self)

        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return KeyboardWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return KeyboardWorkflowUISOperations(self)
            elif self.uisize == "M":
                return KeyboardWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return KeyboardWorkflowUILOperations(self)  
            elif self.uisize == "XL":
                return KeyboardWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)      
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)    
