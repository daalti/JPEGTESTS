
import logging
import sys
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.QuicksetsAppWorkflowUILOperations import QuicksetsAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.QuicksetsAppWorkflowUIMOperations import QuicksetsAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.QuicksetsAppWorkflowUISOperations import QuicksetsAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.QuicksetsAppWorkflowUIXLOperations import QuicksetsAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.QuicksetsAppWorkflowUIXSOperations import QuicksetsAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.ProSelectOperations.QuicksetsAppProSelectUIOperations import QuicksetsAppProSelectUIOperations

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

class spice_quickset_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size

    @property
    def quickset_ui(self):
        if self.uitype == "ProSelect":
            return QuicksetsAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return QuicksetsAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return QuicksetsAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return QuicksetsAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return QuicksetsAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return QuicksetsAppWorkflowUIXLOperations(self)    
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)