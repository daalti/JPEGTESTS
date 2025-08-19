
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations


class CopyAppWorkflowUIXSOperations(CopyAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = WorkflowUICommonXSOperations(self.spice)
        self.id_card_copy = IDCardCopyAppWorkflowUICommonOperations(self.spice)
        self.homemenu = spice.menu_operations

    def select_copy_quickset(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        if quickset_name == CopyAppWorkflowObjectIds.default_quickset_button:
            # for workflow, default quickset will not displayed in quickset list view, have to select it on copy home screen
            self.spice.query_item(CopyAppWorkflowObjectIds.close_button_under_quick_sets_view).mouse_click()
            time.sleep(2)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
            default_quickset_item = self.spice.query_item(quickset_name)
            default_quickset_item.mouse_click()
            assert self.spice.query_item(quickset_name)["checked"]
            return

        logging.info("Select quickset by quickset name")
        quickset_item = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.defaults_and_quick_sets_view} {quickset_name}")
        quickset_item.mouse_click()
        
        time.sleep(2)
        current_screen = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.view_copyScreen} {quickset_name}")
        self.spice.wait_until(lambda:current_screen["checked"])

    def select_copy_quickset_landing(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select Copy landing view-> click on quickset
        '''
        logging.info("Select quickset by quickset name")
        quickset_item = self.spice.wait_for(quickset_name)
        quickset_item.mouse_click()
        time.sleep(2)
        assert self.spice.query_item(quickset_name)["checked"]
    
    def goto_copy_quickset_view(self):
        '''
        This is helper method to goto copy quickset view list
        On Copy home -> click "View All" button 
        '''

        if not self.is_quickset_existing():
            return 

        view_all_btn = self.spice.wait_for(CopyAppWorkflowObjectIds.view_all_locator)

        self.workflow_common_operations.scroll_to_rightmost_on_quickset_landing_view(CopyAppWorkflowObjectIds.quickset_selection_view, CopyAppWorkflowObjectIds.qs_scroll_horizontal_bar)

        view_all_btn.mouse_click()

        self.spice.wait_for(CopyAppWorkflowObjectIds.defaults_and_quick_sets_view, timeout=9)
        logging.info("Wait for item displayed completely")
        time.sleep(4)


    def is_quickset_existing(self):
        '''
        This is helper method to verify is quickset existing
        '''
        try:
            # Need to wait for the copyLandingScreen to update if delete quickset with cdm
            time.sleep(2)
            self.spice.wait_for(CopyAppWorkflowObjectIds.default_quickset_button, 5)
            return True
        except:
            logging.info("No copy quicksets in copy screen")
            return False

    def goto_copy_from_copyapp_at_home_screen(self,scroll=True):
        """
        Purpose: Navigates to Copy app screen by clicking copy icon on Home screen
        Ui Flow: Any screen -> Home screen -> Copy app
        :param scroll: Boolean, indicates whether we want to scroll right to find 
                       the Copy app before clicking
        :param spice : Takes 0 arguments
        :return: None
        """
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0)
        time.sleep(1)
        if scroll:
            self.spice.scroll_home_right(0.1)
        time.sleep(1)
        # First enter the copyFolder on the home screen -- id: '#copy'
        logging.info("Entering Copy folder from Home screen")
        copy_icon = self.spice.wait_for(CopyAppWorkflowObjectIds.copyFolder_home_screen + " MouseArea")
        copy_icon.mouse_click()
        # Then open the copy app itself
        logging.info("Launching Copy App")
        copy_icon = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyApp + " MouseArea")
        copy_icon.mouse_click()
        copy_home = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        self.spice.wait_until(lambda: copy_home["visible"] == True)
        logging.info("At Copy Landing Screen")

    def go_back_to_setting_from_paper_selection(self):
        assert self.spice.query_item(CopyAppWorkflowObjectIds.view_copySettings_paperSelection)
        self.workflow_common_operations.click_back_button()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def back_to_landing_view(self):
        close_button = self.spice.wait_for(CopyAppWorkflowObjectIds.close_button,timeout = 30)
        close_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen,timeout = 20)
    
    def verify_item_unavailable(self,objname):
        item_found = False
        try:
            self.spice.query_item(objname)
        except Exception as e:
            if str(e) == "Query selection returned no items":
                item_found = True
                pass
        self.workflow_common_operations.click_back_button()
        self.back_to_landing_view()
        assert item_found, ("item with object name "+objname+" is found, while expected to be unavailable")
    
    def back_to_scan_option_from_original_size_list(self):
        self.workflow_common_operations.click_back_button()

        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)