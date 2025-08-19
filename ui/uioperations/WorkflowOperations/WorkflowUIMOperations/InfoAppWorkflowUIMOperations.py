import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.InfoAppWorkflowUICommonOperations import InfoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations

class InfoAppWorkflowUIMOperations(InfoAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
