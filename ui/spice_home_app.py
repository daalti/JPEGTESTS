'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.HomeAppProselectUIOperations import HomeAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.HomeAppWorkflowUIXSOperations import HomeAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.HomeAppWorkflowUISOperations import HomeAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.HomeAppWorkflowUIMOperations import HomeAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.HomeAppWorkflowUILOperations import HomeAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.HomeAppWorkflowUIXLOperations import HomeAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.HomeAppWorkflow2UIXSOperations import HomeAppWorkflow2UIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.HomeAppWorkflow2UISOperations import HomeAppWorkflow2UISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.HomeAppWorkflow2UIMOperations import HomeAppWorkflow2UIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.HomeAppWorkflow2UILOperations import HomeAppWorkflow2UILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.HomeAppWorkflow2UIXLOperations import HomeAppWorkflow2UIXLOperations

class spice_home_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size

    @property
    def home(self):
        if self.uitype == "ProSelect":
            return HomeAppProSelectUIOperations(self)
        if self.uitype == "Workflow2":
            logging.info("UI - Experience: Workflow2")
            if self.uisize == "XS":
                return HomeAppWorkflow2UIXSOperations(self)
            elif self.uisize == "S":
                return HomeAppWorkflow2UISOperations(self)
            elif self.uisize == "M":
                return HomeAppWorkflow2UIMOperations(self)
            elif self.uisize == "L":
                return HomeAppWorkflow2UILOperations(self)
            elif self.uisize == "XL":
                return HomeAppWorkflow2UIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        if self.uitype == "Workflow":
            logging.info("UI - Experience: Workflow")
            if self.uisize == "XS":
                return HomeAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return HomeAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return HomeAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return HomeAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return HomeAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)