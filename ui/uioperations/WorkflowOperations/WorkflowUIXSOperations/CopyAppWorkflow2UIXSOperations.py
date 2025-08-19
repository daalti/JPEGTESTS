import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.CopyAppWorkflowUIXSOperations import CopyAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflow2UICommonOperations import CopyAppWorkflow2UICommonOperations

class CopyAppWorkflow2UIXSOperations(CopyAppWorkflow2UICommonOperations, CopyAppWorkflowUIXSOperations):

    def __init__(self, spice):
        self.CopyAppWorkflowObjectIds = CopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.maxtimeout = 120
        self.spice = spice