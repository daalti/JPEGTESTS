import logging 
import time
import sys


from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WiFiAppWorkflowUICommonOperations import WifiAppWorkflowUICommonOperations

class WifiAppWorkflowUISOperations(WifiAppWorkflowUICommonOperations):
    
    def __init__(self,spice):
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.home_menu_workflow_ui_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.network_menu_workflow_ui_operations= NetworkAppWorkflowUICommonOperations(self._spice)