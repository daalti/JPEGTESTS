from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromNetworkAppWorkflowUICommonOperations import PrintFromNetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromNetworkAppWorkflowObjectIds import PrintFromNetworkAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

import logging
import sys

class PrintFromNetworkAppWorkflowUIXLOperations(PrintFromNetworkAppWorkflowUICommonOperations):
    def __init__(self, spice):
        """
        PrintFromNetworkAppUIOperations class to initialize print from network options operations.
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
        print_app = self.spice.wait_for(PrintFromNetworkAppWorkflowObjectIds.print_app + " MouseArea")
        print_app.mouse_click()
        logging.info("At Print App")

    def goto_print_from_network(self):
        """
        Purpose: navigate to Print from Network under Print app.
        Ui Flow: Home_Print -> Print from Network app(ERROR_MESSAGE/ADDRESSBOOK_STATE/NO_NETWORK_FOLDER_CONFIGURED)
        @return:
        """
        self.spice.wait_for(PrintFromNetworkAppWorkflowObjectIds.icon_print_from_network + " MouseArea")
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromNetwork 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        current_button = self.spice.query_item(PrintFromNetworkAppWorkflowObjectIds.icon_print_from_network + " MouseArea")
        current_button.mouse_click()

    def goto_sort_filter_search_options_menu(self):
        """
        Go to sort filter search options menu.
        """
        self.spice.wait_for(PrintFromNetworkAppWorkflowObjectIds.print_network_app_view)
    