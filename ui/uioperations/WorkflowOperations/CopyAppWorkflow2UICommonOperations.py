import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.BaseOperations.ICopyAppUIOperations import ICopyAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

class CopyAppWorkflow2UICommonOperations(ICopyAppUIOperations):

    def __init__(self, spice):
        self.CopyAppWorkflowObjectIds = CopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.maxtimeout = 120
        self.spice = spice

    def goto_copy(self):
        self.spice.home.goto_home_copy()
        copy_landing_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        assert copy_landing_view, "Not at CopyApp Landing view screen."
        logging.info("At Copy Landing Screen")