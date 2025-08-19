
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.TraysAppWorkflowUICommonOperations import TraysAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations


class TraysAppWorkflowUISOperations(TraysAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = self._spice.basic_common_operations

    
