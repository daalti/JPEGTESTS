import logging
from time import sleep, time
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowUICommonOperations import NetworkFolderAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class NetworkFolderAppWorkflowUILOperations(NetworkFolderAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUILOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    def goto_scan_to_network_folder_screen(self,abId, recordId):
        '''
        Navigates to Scan then Network Folder screen starting from Home screen.
        UI Flow is Scan->Network Folder(Scan to Network Folder landing view)
        '''
        sleep(5)
        self.workflow_common_operations.scroll_position(NetworkFolderAppWorkflowObjectIds.view_scan_screen, NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan , NetworkFolderAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , NetworkFolderAppWorkflowObjectIds.scanFolderPage_column_name , NetworkFolderAppWorkflowObjectIds.scanFolderPage_Content_Item)
        network_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        network_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        logging.info("UI: At Scan to network folder screen")

    def goto_folder_quickset_view(self, timeout = 20):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click view all quickset button
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # self.workflow_common_operations.scroll_to_position_vertical(scroll_option, CopyAppWorkflowObjectIds.qs_scroll_horizontal_bar)
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return
        while timeout > 0:
            try:
                scrollbar = self.spice.query_item(NetworkFolderAppWorkflowObjectIds.scrollbar_quicksets_list_horizontal)
                scrollbarSize = scrollbar["size"]
                scrollbar["position"] = 1 - scrollbarSize
                view_all_btn = self.spice.query_item(NetworkFolderAppWorkflowObjectIds.button_view_all)
                view_all_btn.mouse_click()
                self.spice.query_item(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_grid_view)
                logging.info("In View All")
                return
            except:
                timeout = timeout - 0.25
                sleep(0.25)

    def select_folder_quickset_by_quickset_name_from_list(self, quickset_name):
        '''
        This is helper method to select folder quickset in View All screen.
        UI flow Select quickset
        Args: quickset_name: str, quickset name
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_grid_view)
        quickset_name_button = self.spice.query_item(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_grid_view + f" #{quickset_name}" + " MouseArea")
        self.workflow_common_operations.click_button_on_middle(quickset_name_button)
        landing_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def wait_for_scan_status_complete(self, net, message: str = "Complete", timeout: int = 60):
        """
        Purpose: Wait for the given toast message to appear in screen and complete if given toast appears
        Args: message: Scanning, Sending, Complete... : str
        """
        if message == "Starting":
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
        elif message == "Scanning":
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
        elif message == 'Sending':
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSending')
        elif message == 'Complete':
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessfulMessage')

        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen)
        start_time = time()
        while time()-start_time < timeout:
           try:
               self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen)
               status = self.spice.query_item(NetworkFolderAppWorkflowObjectIds.text_toastInfoText)["text"]
               logging.info("Current Toast message is : %s" % status)
               self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen)
           except:
               logging.info("Still finding corresponding status.")
           if option in status:
               break
        if option not in status:
           raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    def select_folder_contact_from_summarize_settings(self, abId=None, recordId=None, contact_name=None):
        button_select_folder = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        button_select_folder.mouse_click()
        button_addressbook_ntwrk_fldr = self.spice.wait_for(
           NetworkFolderAppWorkflowObjectIds.button_address_book)
        button_addressbook_ntwrk_fldr.mouse_click()
        button_radio_addressbook = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        button_radio_addressbook.mouse_click()
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)
        if contact_name is not None:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact.replace("folder_1", contact_name)
            button_radio_select_folder = self.spice.wait_for(button_radio_select_folder_locator)
        else:
            button_radio_select_folder = self.spice.wait_for(
                NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact)

        button_radio_select_folder.mouse_click()

        button_select = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_contact_select)
        button_select.mouse_click()

    def goto_local_address_from_scan_folder_landing_view(self, cdm, job):
        '''
        Go to local contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        folder_contact_select_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        self.spice.wait_until(lambda: folder_contact_select_btn["visible"] == True)
        self.spice.validate_button(folder_contact_select_btn)
        folder_contact_select_btn.mouse_click()

        button_addressbook_ntwrk_fldr = self.spice.wait_for(
           NetworkFolderAppWorkflowObjectIds.button_address_book)
        button_addressbook_ntwrk_fldr.mouse_click()

        button_addressbook_custom = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        button_addressbook_custom.mouse_click()
        logging.info("UIL: Inside Contacts Screen")
    
    def verify_options_combobox_with_values(self, net, option_id, value_id, expected_text):
        """
        Verify the values of a combobox.
        """
        # Define the options list and the specific option value to verify
        options_list = f"#{option_id}ComboBoxpopupList"
        option_value = f"#{option_id}ComboBoxpopupList #ComboBoxOptions{value_id}"

        # Scroll to the specified option value in the combobox        
        self.workflow_common_operations.goto_item(option_value, options_list, scrollbar_objectname=NetworkFolderAppWorkflowObjectIds.combobox_scroll_bar)
                
        # Get the text of the specified value in the combobox
        value_text = self.spice.wait_for(f"{option_value} #contentItem")["text"]
        
        # Get the expected translation for the value
        expected_translation = LocalizationHelper.get_string_translation(net, expected_text)
        
        # Assert that the actual value matches the expected translation
        assert value_text == expected_translation, f"Expected {expected_translation} but got {value_text}"
        
    def select_quickset_and_verify_ldap_signin_error(self):
        '''
        This is helper method to verify LDAP sign in error
        UI flow Sign in -> LDAP sign in error
        '''
        self.spice.quickset_ui.select_quickset_from_app_landing_view("networkFolder2", quickset_type= "folder")
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ldap_signin_error)
        ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ldap_signin_error_ok)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)