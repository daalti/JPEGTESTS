'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.StorageJobAppProSelectUIOperations import StorageJobAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.StorageJobAppWorkflowUICommonOperations import StorageJobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.StorageJobAppWorkflowUIXSOperations import StorageJobAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.StorageJobAppWorkflowUISOperations import StorageJobAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.StorageJobAppWorkflowUIMOperations import StorageJobAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.StorageJobAppWorkflowUILOperations import StorageJobAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.StorageJobAppWorkflowUIXLOperations import StorageJobAppWorkflowUIXLOperations

class spice_job_storage_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._storejob_options_ui_operations = None

    @property
    def storejob(self):
        """Return Stored Job navigation methods."""

        if self.uitype == "ProSelect":
            if self._storejob_options_ui_operations == None:
                self._storejob_options_ui_operations = StorageJobAppProSelectUIOperations(self)
            return self._storejob_options_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._storejob_options_ui_operations == None:
                    self._storejob_options_ui_operations = StorageJobAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                if self._storejob_options_ui_operations == None:
                    self._storejob_options_ui_operations = StorageJobAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                if self._storejob_options_ui_operations == None:
                    self._storejob_options_ui_operations = StorageJobAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                if self._storejob_options_ui_operations == None:
                    self._storejob_options_ui_operations = StorageJobAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                if self._storejob_options_ui_operations == None:
                    self._storejob_options_ui_operations = StorageJobAppWorkflowUIXLOperations(self)
            else: 
                raise NotImplementedError('Unimplemented method workflow UI %s' % sys._getframe().f_code.co_name)
            return self._storejob_options_ui_operations
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
