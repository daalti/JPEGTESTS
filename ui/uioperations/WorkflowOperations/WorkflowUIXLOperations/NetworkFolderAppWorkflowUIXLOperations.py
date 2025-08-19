from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowUICommonOperations import NetworkFolderAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
import time
import logging
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class NetworkFolderAppWorkflowUIXLOperations(NetworkFolderAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUILOperations(self.spice)

    def is_landing_expanded(self, spice):
        """
        Return if copy landing sceen is expanded, only preview visible in main panel and detail panel with settings is not shown
        """
        landing_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        return landing_view["isSecondaryCollapsed"]

    def are_quicksets_visible(self, spice):
        """
        Return if quicksets are visible in scan to network app screen
        """
        are_quicksets_visible = False

        if not self.is_landing_expanded(spice):
            qs_list = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.quickset_selection_view)
            self.spice.wait_until(lambda: qs_list["visible"], timeout = 10.0)
            are_quicksets_visible = qs_list["visible"]

        return are_quicksets_visible
    
    def save_to_network_folder_back_to_back(self, iteration):
        if iteration == 0:
            self.save_to_network_folder()
        self.spice.scan_settings.wait_for_preview_n(1)
        self.send_to_network_folder(ScanAppWorkflowObjectIds.send_button)

    def press_save_to_network_folder(self, scan_more_pages: bool = False, wait_time=5, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        time.sleep(7)
        self.save_to_network_folder()
        if(wait_for_preview):
            self.spice.scan_settings.wait_for_preview_n(1)
        self.send_to_network_folder(button)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()

    def select_folder_contact_from_summarize_settings(self, abId=None, recordId=None, contact_name=None):
        interactive_summary = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_to_network_folder_landing_page_deatil_panel)
        self.spice.wait_until(lambda: interactive_summary["visible"])
        interactive_summary_scroll_bar = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scrollbar_scan_to_network_folder_landing_page)
        self.spice.wait_until(lambda: interactive_summary_scroll_bar["visible"])
        folder_destination_row = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder)
        self.spice.wait_until(lambda: folder_destination_row["visible"])
        button_select_folder = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        self.spice.validate_button(button_select_folder)
        button_select_folder.mouse_click()

        button_addressbook_ntwrk_fldr = self.spice.wait_for(
           NetworkFolderAppWorkflowObjectIds.button_address_book)
        button_addressbook_ntwrk_fldr.mouse_click()

        # Wait for the address book selection dialog to appear
        time.sleep(5)
        button_radio_addressbook = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        button_radio_addressbook.mouse_click()
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder, timeout=9.0)
        if contact_name is not None:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact.replace("folder_1", contact_name)
            button_radio_select_folder = self.spice.wait_for(button_radio_select_folder_locator)
        else:
            button_radio_select_folder = self.spice.wait_for(
                NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact)

        button_radio_select_folder.mouse_click()

        button_select = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_contact_select)
        self.spice.validate_button(button_select)
        button_select.mouse_click()

    def goto_local_address_from_scan_folder_landing_view(self, cdm, job):
        '''
        Go to local contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        folder_contact_select_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select, timeout=9.0)
        self.spice.validate_button(folder_contact_select_btn)
        folder_contact_select_btn.mouse_click()

        button_addressbook_ntwrk_fldr = self.spice.wait_for(
           NetworkFolderAppWorkflowObjectIds.button_address_book)
        button_addressbook_ntwrk_fldr.mouse_click()

        button_addressbook_custom = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        button_addressbook_custom.mouse_click()
        logging.info("Inside Contacts Screen")

    def back_to_folder_landing_view_from_select_addressbook_view(self, cdm, job):
        """
        Back to Scan folder landing screen from select addressbook screen through close button.
        """
        close_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.view_address_book} {NetworkFolderAppWorkflowObjectIds.button_back_close}")
        close_button.mouse_click()

        back_button_from_ntwrk_fldr = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.view_folder_select_ntwrk_fldr} {NetworkFolderAppWorkflowObjectIds.button_back}")
        back_button_from_ntwrk_fldr.mouse_click()

    def save_to_network_folder(self, scan_more_pages: bool = False, wait_time=2, click_send=False):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_start,  timeout=20.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(5)
        logging.info("After press save to network folder")
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()
        if click_send:
            self.spice.scan_settings.wait_for_preview_n(1)
            self.click_send_button()

    def click_send_button(self):
        """
        Clicks the send button in the Network Folder app workflow.
        """
        send_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        self.wait_and_validate_property_value(send_button, "visible", True, 25, delay = 0.01)
        self.wait_and_validate_property_value(send_button, "enabled", True, 25, delay = 0.01)
        self.wait_and_validate_property_value(send_button, "constrained", False, 10, delay = 0.01)
        send_button.mouse_click()

    def wait_and_validate_property_value(self, object, property, state, timeout = 10, delay = 0.25):
        self.workflow_common_operations.wait_until_property_value( object, property, state, timeout, delay = delay)
        assert object[property] == state            

    def send_to_network_folder(self, button=ScanAppWorkflowObjectIds.send_button):
        '''
        UI should be at Scan Network Folder landing view.
        Starts send to Network Folder.
        '''
        scan_send_button = self.spice.wait_for(button)
        self.spice.wait_until(lambda: scan_send_button["enabled"], 10)
        self.spice.wait_until(lambda: scan_send_button["visible"], 10)
        self.wait_and_validate_property_value(scan_send_button, "constrained", False, 10, delay = 0.01)
        scan_send_button.mouse_click()
        
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