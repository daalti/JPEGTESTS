'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.JobAppProSelectUICommonOperations import JobAppProSelectUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowUICommonOperations import JobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.JobAppWorkflowUIXSOperations import JobAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.JobAppWorkflowUISOperations import JobAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.JobAppWorkflowUIXLOperations import JobAppWorkflowUIXLOperations

class spice_job_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._job_options_ui_operations = None

    @property
    def job_ui(self):
        """Return Job navigation methods."""
        if self.uitype == "ProSelect":
            if self._job_options_ui_operations == None:
                self._job_options_ui_operations = JobAppProSelectUICommonOperations(self)
            return self._job_options_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._job_options_ui_operations == None:
                    self._job_options_ui_operations = JobAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                if self._job_options_ui_operations == None:
                    self._job_options_ui_operations = JobAppWorkflowUISOperations(self)
            elif self.uisize == "XL":
                if self._job_options_ui_operations == None:
                    self._job_options_ui_operations = JobAppWorkflowUIXLOperations(self)
            else:
                if self._job_options_ui_operations == None:
                    self._job_options_ui_operations = JobAppWorkflowUICommonOperations(self)
            return self._job_options_ui_operations
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
