
'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUILoOperations.MenuAppProSelectUILoOperations import MenuAppProSelectUILoOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.MenuAppProSelectUIHybridOperations import MenuAppProSelectUIHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowUIXSOperations import MenuAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.MenuAppWorkflowUISOperations import MenuAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.MenuAppWorkflowUIMOperations import MenuAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.MenuAppWorkflowUILOperations import MenuAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MenuAppWorkflowUIXLOperations import MenuAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflow2UIXSOperations import MenuAppWorkflow2UIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.MenuAppWorkflow2UISOperations import MenuAppWorkflow2UISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.MenuAppWorkflow2UIMOperations import MenuAppWorkflow2UIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.MenuAppWorkflow2UILOperations import MenuAppWorkflow2UILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MenuAppWorkflow2UIXLOperations import MenuAppWorkflow2UIXLOperations

class spice_menu_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        
    def homeMenuUI(self):
        if self.uitype == "ProSelect":
            print ("UI Theme: " + self.uitheme)
            if self.uitheme == "loTheme":
                return MenuAppProSelectUILoOperations(self)
            elif self.uitheme == "hybridTheme":
                return MenuAppProSelectUIHybridOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)   
        if self.uitype == "Workflow":
            print ("UI Size: " + self.uisize)
            if self.uisize == "XS":
                return MenuAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return MenuAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return MenuAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return MenuAppWorkflowUILOperations(self)  
            elif self.uisize == "XL":
                return MenuAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)     
        if self.uitype == "Workflow2":
            print ("UI Size: " + self.uisize)
            if self.uisize == "XS":
                return MenuAppWorkflow2UIXSOperations(self)
            elif self.uisize == "S":
                return MenuAppWorkflow2UISOperations(self)
            elif self.uisize == "M":
                return MenuAppWorkflow2UIMOperations(self)
            elif self.uisize == "L":
                return MenuAppWorkflow2UILOperations(self)  
            elif self.uisize == "XL":
                return MenuAppWorkflow2UIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)     
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)



