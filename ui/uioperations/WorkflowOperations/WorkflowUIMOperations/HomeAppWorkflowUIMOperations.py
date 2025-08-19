
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations

class HomeAppWorkflowUIMOperations(HomeAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120