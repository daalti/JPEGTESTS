'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.FaxDiagnosticProSelectUIOperations import FaxDiagnosticProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.FaxDiagnosticWorkflowUIXSOperations import FaxDiagnosticWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.FaxDiagnosticWorkflowUISOperations import FaxDiagnosticWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.FaxDiagnosticWorkflowUIMOperations import FaxDiagnosticWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.FaxDiagnosticWorkflowUILOperations import FaxDiagnosticWorkflowUILOperations

class spice_service_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size


    @property
    def serviceFaxDiagnostic(self):
        if self.uitype == "ProSelect":
            return FaxDiagnosticProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return FaxDiagnosticWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return FaxDiagnosticWorkflowUISOperations(self)
            elif self.uisize == "M":
                return FaxDiagnosticWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return FaxDiagnosticWorkflowUILOperations(self)  
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)      
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
