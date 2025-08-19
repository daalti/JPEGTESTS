import logging, time
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.send.common.common import Common as ScanCommon


class ScanAppWorkflowUIMOperations(ScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def goto_scan_app(self):
        """
        Purpose: Navigates to Scan app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Scan app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.home_operations.goto_home_scan_folder()
        logging.info("At Scan App")

    def goto_folder_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Network Folder.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan + " MouseArea")
        self.workflow_common_operations.click_button_on_middle(folder_button)
        logging.info("At scan to folder screen")

    def goto_email_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Email.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        email_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan + " MouseArea")
        self.spice.validate_button(email_button)
        self.workflow_common_operations.click_button_on_middle(email_button)
        logging.info("At scan to email screen")

    def click_preview_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_panel)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_preview, timeout =9.0)

        current_button = self.spice.query_item("#previewButtonLargeScreen")
        self.workflow_common_operations.click_button_on_middle(current_button)

    def start_send_from_preview_panel(self, button_object_id = None, scan_more_pages: bool = False, wait_time=2, type="usb"):
        '''
        Ui Should be in previewpanel
        Click on send button starts send
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout =9.0)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout =9.0)
        current_button = self.spice.wait_for(button_object_id)
        current_button.mouse_click()
        time.sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, type):
            self.flatbed_scan_more_pages()

    def cancel_send_from_preview_panel(self):
        """
        UI should be at scan progress view.
        Cancel the scan job.
        :return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_cancel).mouse_click()

    def goto_sharepoint_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At Scan to SharePoint screen")

    def goto_sharepoint_from_scanapp_at_menu(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        #self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At Scan to SharePoint screen")

    def has_lock_icon(self):
        lock_icon_ids = []
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan_menu_app + " #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_network_folder + " #statusIconRect SpiceLottieImageView")

        for index, lock_icon_id in enumerate(lock_icon_ids):
            try:
                #self.workflow_common_operations.scroll_to_position_vertical(0.1 * (index + 1), ScanAppWorkflowObjectIds.scroll_bar_scan_app_home)
                lock_icon = self.spice.wait_for(lock_icon_id)
            except:
                logging.info("Failed to find lock icon")
                return False
            self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return True

    def goto_usb_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to USB.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan +" MouseArea")
        button.mouse_click()
        logging.info("At Scan to USB screen")
