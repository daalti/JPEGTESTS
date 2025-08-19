from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromMyhomeAppWorkflowUICommonOperations import PrintFromMyhomeAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromMyhomeAppWorkflowObjectIds import PrintFromMyhomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowObjectIds

import logging
import sys

class PrintFromMyhomeAppWorkflowUIXLOperations(PrintFromMyhomeAppWorkflowUICommonOperations):
    def __init__(self, spice):
        """
        PrintFromMyhomeAppUIOperations class to initialize print from Myhome options operations.
        @param spice:
        """
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.dial_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage + " MouseArea")
        print_app = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_app + " MouseArea")
        print_app.mouse_click()
        logging.info("At Print App")

    def goto_print_from_myhome(self):
        """
        Purpose: navigate to Print from Myhome under Print app.
        Ui Flow: Home_Print -> Print from Myhome app(ERROR_MESSAGE/LDAP_NOT_CONFIGURED/CONNECTING_TO_NETWORK)
        @return:
        """
        assert self.spice.wait_for(HomeAppWorkflowObjectIds.view_print,timeout=20)
        assert self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome,timeout=20)
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome + " MouseArea")
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromMyhome 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        current_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome + " MouseArea")
        current_button.mouse_click()

    def goto_sort_filter_search_options_menu(self):
        """
        Go to sort filter search options menu.
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_app_view)
    