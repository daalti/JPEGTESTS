
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class HomeAppWorkflowUISOperations(HomeAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def goto_home_supplies(self):
        self._spice.goto_homescreen()
        self._scroll_to_position_horizontal(0.4)
        menuApp = self._spice.wait_for(HomeAppWorkflowObjectIds.supplies_app_button)
        menuApp.mouse_click()
        time.sleep(3)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_supplies)
        print("At Supplies App")