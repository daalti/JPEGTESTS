
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class HomeAppWorkflow2UILOperations(HomeAppWorkflow2UICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        self.maxtimeout = 120
        super().__init__(spice)

    def goto_home_copy(self):
        self.spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)
        assert self.spice.wait_for(HomeAppWorkflowObjectIds.view_copyScreen)
        print("At Copy App")

    def click_copy_app(self) -> bool:
        """
        Click the Copy app from the home page on a Workflow 2 L UI device

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' was perfomred, False otherwise
        
        Raises:
            None
        """
        copy_app_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.button_copyApp + " MouseArea")
        return self.workflow_common_operations.click(copy_app_button)
