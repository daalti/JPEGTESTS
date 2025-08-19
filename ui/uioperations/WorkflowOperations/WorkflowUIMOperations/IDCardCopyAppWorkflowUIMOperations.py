
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowObjectIds import IDCardCopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations

class IDCardCopyAppWorkflowUIMOperations(IDCardCopyAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        self.maxtimeout = 120
        self.IDCardCopyAppWorkflowObjectIds = IDCardCopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

    def goto_menu_idcopy(self, spice):
        """
        navigate screen: home_menu -> menu -> copy -> id card copy
        @return:
        """
        self.homemenu.goto_menu(spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        copy_app = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_menu_copy + " MouseArea")
        copy_app.mouse_click()
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only few options
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code

        #self.workflow_common_operations.scroll_position(IDCardCopyAppWorkflowObjectIds.view_menu_copy_screen, IDCardCopyAppWorkflowObjectIds.button_menu_idCopy , IDCardCopyAppWorkflowObjectIds.scrollBar_menucopyFolderLanding , IDCardCopyAppWorkflowObjectIds.copyFolderPage_column_name , IDCardCopyAppWorkflowObjectIds.copyFolderPage_Content_Item)
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_menu_idCopy + " MouseArea")
        current_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.button_menu_idCopy + " MouseArea")
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        logging.info("At ID Card Copy Landing Screen")

    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from IDCopy screen.
        UI Flow is IDCopy->Options
        '''
		# Wait for Options screen
        currentScreen = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen + " " + IDCardCopyAppWorkflowObjectIds.button_idCopyMoreOptions)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)
        logging.info("UI: At Options in IDCopy")
