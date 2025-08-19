import logging

from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowUICommonOperations import UsbScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowObjectIds import UsbScanAppWorkflowObjectIds
from time import sleep
from dunetuf.send.common.common import Common as ScanCommon

class UsbScanAppWorkflowUIXLOperations(UsbScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice=spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)


    def save_to_usb(self, scan_more_pages: bool = False, dial_value=0, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True):
        """
        UI should be at Scan USB landing view.
        Starts save to USB drive and verifies job is successful.
        :param scan_more_pages: scan number of pages
        :return:
        """
        # Add sleep time since it takes a while for Send button to be clickable after selecting created quickset.
        usb_start_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_start)
        self.spice.wait_until(lambda: usb_start_button["visible"] == True, timeout=30.0)
        self.spice.wait_until(lambda: usb_start_button["enabled"] == True, timeout=30.0)
        usb_start_button.mouse_click()
        
        if wait_for_preview:
            self.spice.scan_settings.wait_for_preview_n(1)
            
        usb_send_button = self.spice.wait_for(button, timeout=30.0)
        self.spice.wait_until(lambda: usb_send_button["visible"] == True, timeout=30.0)
        self.spice.wait_until(lambda: usb_send_button["enabled"] == True, timeout=30.0)
        usb_send_button.mouse_click()
        
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def back_to_scan_to_usb_options_list_from_resolution_setting_screen(self):
        """
        UI should be in resolution setting view
        Navigates back from resolution setting screen to scan settings view
        """
        # close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_resolution_layout + " " + ScanAppWorkflowObjectIds.back_button)
        # close_button.mouse_click()
    
    def save_to_usb_click_on_done_button(self):
        '''
        UI should be in save to usb screen
        Clicks on done button
        '''
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        usb_send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.spice.validate_button(usb_send_button)
        usb_send_button.mouse_click()
        sleep(5)

    def press_save_to_usb(self, scan_more_pages: bool = False, wait_time=5):

        """
        UI should be at Scan USB landing view.
        Starts save to USB drive and verifies job is successful.
        :param scan_more_pages: scan number of pages
        :return:
        """
        # Add sleep time since it takes a while for Send button to be clickable after selecting created quickset.
        sleep(2)
        usb_save_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_start)
        usb_save_button.mouse_click()
        sleep(5)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def goto_filetype_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary XL screen.
        UI Flow is file type-> (file type Settings XL screen).
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing,  timeout=9.0)
        file_type = self.spice.query_item(ScanAppWorkflowObjectIds.combobox_scan_file_type)
        file_type.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen, timeout=9.0)
        logging.info("UI: At filetype settings XL screen")

    def verify_no_front_usb_device_constriant(self):
        """
        UI should be at no USB device connected screen.
        Verify no front USB device connected screen
        :return:
        """
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_start)
        self.wait_and_validate_property_value(current_button, "visible", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(current_button, "enabled", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(current_button, "constrained", True, 10, delay = 0.01)
        current_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_no_front_device)

    def wait_and_validate_property_value(self, object, property, state, timeout = 5, delay = 0.25):
        self.workflow_common_operations.wait_until_property_value(object, property, state, timeout, delay = delay)
        assert object[property] == state   
        
    def check_main_button(self):
        start_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_start, 10)
        self.spice.validate_button(start_button)
