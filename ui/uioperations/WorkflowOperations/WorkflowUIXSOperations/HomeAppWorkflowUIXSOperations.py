
import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations

class HomeAppWorkflowUIXSOperations(HomeAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.workflow_common_operations = self._spice.basic_common_operations
        self._spice = spice

    def is_back_button_visible(self):
        is_back_button_work = self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")
        if is_back_button_work == '1':
            return True
        else:
            return False
