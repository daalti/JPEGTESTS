'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.TraysAppProSelectUIOperations import TraysAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.TraysAppWorkflowUIXSOperations import TraysAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.TraysAppWorkflowUISOperations import TraysAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.TraysAppWorkflowUIMOperations import TraysAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.TraysAppWorkflowUILOperations import TraysAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.TraysAppWorkflowUIXLOperations import TraysAppWorkflowUIXLOperations


class spice_trays_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        
    @property
    def traysapp(self):
        if self.uitype == "ProSelect":
            return TraysAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return TraysAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return TraysAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return TraysAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return TraysAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return TraysAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)