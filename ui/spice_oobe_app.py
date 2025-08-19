'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.OOBEAppProSelectUIOperations import OOBEAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.OOBEAppWorkflowUIXSOperations import OOBEAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.OOBEAppWorkflowUISOperations import OOBEAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.OOBEAppWorkflowUIMOperations import OOBEAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.OOBEAppWorkflowUILOperations import OOBEAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.OOBEAppWorkflowUIXLOperations import OOBEAppWorkflowUIXLOperations


class spice_oobe_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size


    @property
    def oobeapp(self):
        if self.uitype == "ProSelect":
            return OOBEAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return OOBEAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return OOBEAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return OOBEAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return OOBEAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return OOBEAppWorkflowUIXLOperations(self)  
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)  
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
