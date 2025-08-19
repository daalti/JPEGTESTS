
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations


class KeyboardWorkflowUISOperations(WorkflowKeyboardUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.faxoperations = FaxAppWorkflowUICommonOperations(self._spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuApp_Workflow_UI_Common_Operations = spice.menu_operations
        
        
       