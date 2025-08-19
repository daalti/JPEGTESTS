import logging 
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflow2UICommonOperations import SignInAppWorkflow2UIOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations


class NetworkAppWorkflowUISOperations(NetworkAppWorkflowUICommonOperations):

    def __init__(self,spice):
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self._spice)
        if (spice.uitype == "Workflow"):
            self.sign_in_app_operations = SignInAppWorkflowUIOperations(self._spice)
        if (spice.uitype == "Workflow2"):
            self.sign_in_app_operations = SignInAppWorkflow2UIOperations(self._spice)
