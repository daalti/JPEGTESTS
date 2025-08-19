
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations

class HomeAppWorkflow2UIXSOperations(HomeAppWorkflow2UICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        self.maxtimeout = 120
        self.workflow_common_operations = Workflow2UICommonOperations(self.spice)