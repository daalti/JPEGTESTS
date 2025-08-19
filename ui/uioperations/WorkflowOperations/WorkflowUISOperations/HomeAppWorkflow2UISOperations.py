
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class HomeAppWorkflow2UISOperations(HomeAppWorkflow2UICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        self.maxtimeout = 120
        super().__init__(spice)

    def goto_home_supplies(self):
        self.spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.supplies_app_button)
        assert self.spice.wait_for(HomeAppWorkflowObjectIds.view_supplies)
        print("At Supplies App")