

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.FaxAppProSelectUIOperations import FaxAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.FaxAppWorkflowUIXSOperations import FaxAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.FaxAppWorkflowUISOperations import FaxAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.FaxAppWorkflowUIMOperations import FaxAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.FaxAppWorkflowUILOperations import FaxAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.FaxAppWorkflowUIXLOperations import FaxAppWorkflowUIXLOperations

class spice_fax_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size

    def fax_ui(self):
        if self.uitype == "ProSelect":
            return FaxAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return FaxAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return FaxAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return FaxAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return FaxAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return FaxAppWorkflowUIXLOperations(self)    
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)