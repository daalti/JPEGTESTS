import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowUICommonOperations import ToolsAppWorkflowUICommonOperations




class ToolsAppWorkflowUIMOperations(ToolsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice