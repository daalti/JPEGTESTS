
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class HomeAppWorkflowUILOperations(HomeAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def goto_home_copy(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_copyScreen)
        print("At Copy App")