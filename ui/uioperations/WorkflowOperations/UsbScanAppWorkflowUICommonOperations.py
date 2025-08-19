import logging
import datetime
from time import sleep, time
from dunetuf.ui.uioperations.BaseOperations.IUsbScanAppUIOperations import IUsbScanAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowObjectIds import UsbScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from typing import Dict
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.configuration import Configuration


class UsbScanAppWorkflowUICommonOperations(IUsbScanAppUIOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    def goto_scan_to_usb_screen(self):
        """
        Navigates to Scan then USB Drive screen starting from Main menu
        UI Flow is Main menu->Scan->USB Drive->(Scan to USB landing view)
        """
        self.scan_operations.goto_scan_app()
        sleep(5)
        self.workflow_common_operations.scroll_position(UsbScanAppWorkflowObjectIds.view_scan_screen, UsbScanAppWorkflowObjectIds.button_scan_usb , UsbScanAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , UsbScanAppWorkflowObjectIds.scanFolderPage_column_name , UsbScanAppWorkflowObjectIds.scanFolderPage_Content_Item)
        button_usb = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb + " MouseArea")
        self.spice.wait_until(lambda: button_usb["visible"] == True)
        button_usb.mouse_click()
        logging.info("Inside scan to usb")
        sleep(3)
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        logging.info("At Scan to usb App")


    def goto_scan_to_usb(self):
        """
        Navigates to Scan then USB Drive screen starting from Main menu
        UI Flow is Main menu->Scan->USB Drive
        """
        self.scan_operations.goto_scan_app()
        sleep(5)
        self.workflow_common_operations.scroll_position(UsbScanAppWorkflowObjectIds.view_scan_screen, UsbScanAppWorkflowObjectIds.button_scan_usb , UsbScanAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , UsbScanAppWorkflowObjectIds.scanFolderPage_column_name , UsbScanAppWorkflowObjectIds.scanFolderPage_Content_Item)
        button_usb = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb + " MouseArea")
        self.spice.wait_until(lambda: button_usb["visible"] == True)
        # Wait for usb drive screen
        button_usb.mouse_click()

    def goto_scan_to_usb_via_usb_drive_app(self):
        """
        Navigates to USB Drive then Scan screen from Home screen.
        UI Flow is Main menu->USB Drive->Scan->(Scan to USB landing view)
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.4)
        usb_drive_app = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_drive_app + " MouseArea")
        usb_drive_app.mouse_click()
        sleep(3)
        # Wait for usb drive screen
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb)
        current_button = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_scan_usb)
        current_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def goto_usb_scan_location_folders_without_scroll(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to scan location screen.
        UI Flow is Scan Location->(Scan folder list)
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        current_button = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.row_object_usb_insert} {UsbScanAppWorkflowObjectIds.button_scan_usb_home_edit}")
        current_button.mouse_click()
        # Wait for Options screen
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)

    def goto_usb_scan_location_folders(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to scan location screen.
        UI Flow is Scan Location->(Scan folder list)
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.workflow_common_operations.goto_item([UsbScanAppWorkflowObjectIds.row_object_usb_insert, UsbScanAppWorkflowObjectIds.button_scan_usb_home_edit], UsbScanAppWorkflowObjectIds.screen_id, scrollbar_objectname=UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        # current_button = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_scan_usb_home_edit)
        # current_button.mouse_click()
        # Wait for Options screen
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)

    def goto_create_folder_via_all_option(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to Create folder screen via all option.
        """
        self.goto_options_list_from_scan_to_usb()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.all_option_view)

        self.workflow_common_operations.goto_item([UsbScanAppWorkflowObjectIds.row_object_usb_insert, UsbScanAppWorkflowObjectIds.button_scan_usb_home_edit], UsbScanAppWorkflowObjectIds.all_option_view, scrollbar_objectname=UsbScanAppWorkflowObjectIds.scrollbar_all_option)
        self.goto_create_folder_screen()
        
    def goto_create_folder_via_landing_page(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to Create folder screen via landing page.
        """
        self.check_main_button()
        edit_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.edit_button)
        edit_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)
        self.goto_create_folder_screen()
        
    def check_main_button(self):
        send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.spice.validate_button(send_button)

    def goto_scan_location_folders_via_usb(self):
        """
        Navigates to scan location settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Scan Location->(Scan folder list)
        """
        self.goto_scan_to_usb_screen()
        sleep(5)
        self.goto_usb_scan_location_folders()

    def goto_options_list_from_scan_to_usb(self):
        """
        UI should be in Scan to USB screen.
        Navigates to Options screen starting from USB Scan screen.
        UI Flow is Scan to USB->Options->(Options list)
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_options)
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_options)
        current_button.mouse_click()
        # Wait for Options screen
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def goto_options_list_via_usb(self):
        """
        Navigates to Options screen starting from Home screen.
        UI Flow is Home->USB Drive->Scan->Options->(Options list)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_options_list_from_scan_to_usb()

    def goto_lighter_darker_settings_via_usb(self):
        """
        Navigates to Lighter/Darker in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Lighter/Darker->(Lighter/Darker slide)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_lighter_darker_settings()

    def goto_contrast_settings_via_usb(self):
        """
        Navigates to Contrast in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Contrast->(Contrast slide)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_contrast_settings()

    def goto_orientation_settings_via_usb(self):
        """
        Navigates to Orientation in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Orientation->(Orientation settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_orientation_settings()

    def goto_original_size_settings_via_usb(self):
        """
        Navigates to Original Size in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Original Size->(Original Size settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_original_size_settings()

    def goto_color_format_settings_via_usb(self):
        """
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Color Format->(Color format settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_color_settings()

    def goto_filesize_settings_via_usb(self):
        """
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->filesize->(filesize settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_filesize_settings()

    def goto_resolution_settings_via_usb(self):
        """
        Navigates to Resolution in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Resolution->(Resolution settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_resolution_settings()

    def goto_long_original_settings_via_usb(self):
        """
        Navigates to Long original in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Long original->(Long original Toggle)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_long_original_settings()

    def goto_edge_to_edge_settings_via_usb(self):
        """
        Navigates to Edge-to-Edge in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Edge-to-Edge->(Edge-to-Edge Toggle)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_edge_to_edge_settings()

    def goto_background_color_removal_via_usb(self):
        """
        Navigates to Background color removal in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Background color removal->(Background color removal Toggle)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_background_color_removal_settings()

    def goto_background_noise_removal_via_usb(self):
        """
        Navigates to Background noise removal in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Background noise removal->(Background noise removal Toggle)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_background_noise_removal_settings()

    def goto_filetype_settings_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->File Type->(File Type settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_filetype_settings()

    def goto_sides_settings_via_usb(self):
        """
        Navigates to Sides in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Sides-> (Sides settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_sides_settings()

    def back_to_scan_to_usb_options_list_from_resolution_setting_screen(self):
        """
        UI should be in resolution setting view
        Navigates back from resolution setting screen to scan settings view
        """
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_resolution_layout + " " + ScanAppWorkflowObjectIds.back_button)
        close_button.mouse_click()
    
    def back_to_scan_to_usb_options_list_from_original_size_setting_screen_with_close_button(self):
        """
        UI should be in original size setting view
        Navigates back from original size setting screen to scan settings view
        """
        logging.info("Click Close button")
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_layout + " " + ScanAppWorkflowObjectIds.back_button)
        self.spice.validate_button(close_button)
        close_button.mouse_click()
        scan_option_view = self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.spice.wait_until(lambda:scan_option_view["visible"])

    def back_to_scan_to_usb_from_options_list(self):
        """
        UI should be in Options list.
        Navigates back from Options screen to USB landing view.
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.menu_list_scan_settings)
        # self.workflow_common_operations.back_button_press(ScanAppWorkflowObjectIds.menu_list_scan_settings,
        #                                                   UsbScanAppWorkflowObjectIds.view_scan_usb_landing,
        #                                                   index = 2, timeout_val = 60)
        # assert self.spice.query_item("#BackButton", 3)["visible"] == True
        # self.spice.query_item("#BackButton", 3).mouse_click()
        button_close = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close, timeout=30.0)
        self.spice.wait_until(lambda: button_close["visible"] == True, timeout=30.0)
        self.spice.wait_until(lambda: button_close["enabled"] == True, timeout=30.0)
        button_close.mouse_click()
        view_scan_usb_landing = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.spice.wait_until(lambda:view_scan_usb_landing["visible"])

    def back_to_home_from_scan_to_usb(self):
        """
        UI should be in Scan to USB screen
        Navigates back from Scan to USB screen to Scan
        """
        home_screen = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_home)
        home_screen.mouse_click()
        logging.info("At Home Screen")

    def goto_create_folder_screen(self):
        """
        UI should be at Scan folder list.
        Navigates to Create folder screen.
        """
        usb_create_folder_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_create_folder)
        usb_create_folder_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.create_folder_screen_view)

    def back_to_usb_landing_view_from_create_folder_screen(self):
        """
        UI should be at Create folder screen.
        Navigates back from Create folder screen to USB landing view.
        """
        cancel_folder = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add_cancel, timeout=25)
        self.spice.wait_until(lambda: cancel_folder["enabled"] == True)
        cancel_folder.mouse_click()
        sleep(2)
        button_cancel = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb_landing_cancel)
        button_cancel.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def set_usb_folder_location(self, folder: str = None):
        """
        UI should be at Scan folder list.
        Sets folder location
        """
        usb_save_here_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_save_here_button)
        usb_save_here_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def add_page_pop_up_add_more(self):
        scan_add_page_more_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page)
        assert scan_add_page_more_button
        scan_add_page_more_button.mouse_click()

    def add_page_pop_up_finish(self):
        scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
        self.spice.wait_until(lambda: scan_add_page_done_button["visible"] == True, timeout=100.0)
        scan_add_page_done_button.mouse_click()
        
    def add_page_pop_up_cancel(self):
        scan_add_page_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbedduplex_cancel)
        assert scan_add_page_cancel_button
        scan_add_page_cancel_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_no)
        scan_add_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        assert scan_add_page_cancel_page_yes_button
        scan_add_page_cancel_page_yes_button.mouse_click()

    def save_to_usb(self, scan_more_pages: bool = False, dial_value=0, wait_time=5, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True):
        """
        UI should be at Scan USB landing view.
        Starts save to USB drive and verifies job is successful.
        :param scan_more_pages: scan number of pages
        :return:
        """
        # Add sleep time since it takes a while for Send button to be clickable after selecting created quickset.
        sleep(2)
        usb_send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.spice.wait_until(lambda: usb_send_button["visible"] == True)
        self.spice.wait_until(lambda: usb_send_button["enabled"] == True)
        usb_send_button.mouse_click()
        sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()
        
        scan_resource = common_instance.scan_resource()
        job_concurrency_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrency_supported == "false" and scan_resource == "MDF" and scan_more_pages == False:
            self.spice.scan_settings.mdf_addpage_window_alert_click_option()

    def wait_for_save_to_usb_landing_view(self):
        """
        UI should be at Scan USB landing view.
        :return:
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def wait_for_save_to_quickset_app_landing_view(self):
        """
        UI should be at Quickset landing view.
        :return:
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_quickset_app_landing)

    def press_save_to_usb(self, scan_more_pages: bool = False, wait_time=5):
        """
        UI should be at Scan USB landing view.
        Starts save to USB drive.
        :param scan_more_pages: scan number of pages
        :param wait_time: time for sleep
        :return:
        """
        usb_send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.wait_and_validate_property_value(usb_send_button, "visible", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(usb_send_button, "enabled", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(usb_send_button, "constrained", False, 10, delay = 0.01)
        logging.debug("after button_usb_send in press_save_to_usb")
        usb_send_button.mouse_click()
        sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def press_save_to_usb_enterprise(self, scan_more_pages: bool = False, wait_time=5):
        """
        UI should be at Scan USB landing view.
        Starts save to USB drive.
        :param scan_more_pages: scan number of pages
        :param wait_time: time for sleep
        :return:
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        usb_send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.spice.validate_button(usb_send_button)
        logging.debug("after button_usb_send in press_save_to_usb")
        usb_send_button.mouse_click()
        sleep(wait_time)
        if scan_more_pages == True:    
            time.sleep(2)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_add_page_prompt_view)
            add_page_prompt_media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)
            scroll_bar_step_value = 0
            media_size_id_radio_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.add_page_content_id} " + add_page_prompt_media_sizes_list[0])
            self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True)
            assert media_size_id_radio_button
            media_size_id_radio_button.mouse_click()

            self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, ScanAppWorkflowObjectIds.add_page_prompt_scroll_bar)
            self.add_page_pop_up_finish()

    def cancel_scan_to_usb(self):
        """
         UI should be at scan progress view.
        Cancel the scan to usb job.
        :return:
        """
        #self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_scan_progress, timeout=9.0)
        usb_scan_cancel_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_scan_progress_cancel)
        usb_scan_cancel_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)


    def start_scan_job_usb(self):
        """
        UI flow is from Home screen.
        Starts save to USB drive and verifies job is successful.
        :return:
        """
        self.goto_scan_to_usb_screen()
        self.save_to_usb()

    def start_scan_cancel_job_usb(self):
        """
        Start save to USB drive and cancel job.
        UI flow is from Home screen.
        :return:
        """
        self.goto_scan_to_usb_screen()
        current_button = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_usb_send + " SpiceText")
        current_button.mouse_click()
        sleep(2)
        current_button = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_usb_scan_progress_cancel + " SpiceText")
        current_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def save_to_usb_with_settings(self, scan_options, scan_more_pages: bool = False):
        """
        Start save to USB drive with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        scan_options = {
            'filetype': 'pdf',]
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'tiffcompression':'postTiff6'
            'orientation': 'portrait',
            'lighter_Darker': 1,
            'contrast': 1
        }
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_options_list_from_scan_to_usb()
        sleep(5)

        settings = {
            'filetype': scan_options.get('filetype', None),
            'resolution': scan_options.get('resolution', None),
            'filesize': scan_options.get('filesize', None),
            'sides': scan_options.get('sides', None),
            'color': scan_options.get('color', None),
            'size': scan_options.get('size', None),
            'tiffcompression': scan_options.get('tiffcompression', None),
            'orientation': scan_options.get('orientation', None),
            'lighter_darker': scan_options.get('lighter_darker', None),
            'contrast': scan_options.get('contrast', None)
        }

        if settings['filetype'] != None:
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if settings['resolution'] != None:
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if settings['filesize'] != None:
            self.scan_operations.goto_filesize_settings()
            self.scan_operations.set_scan_setting('filesize', settings['filesize'])
        if settings['sides'] != None:
            self.scan_operations.goto_sides_settings()
            self.scan_operations.set_scan_setting('sides', settings['sides'])
        if settings['color'] != None:
            self.scan_operations.goto_color_settings()
            self.scan_operations.set_scan_setting('color', settings['color'])
        if settings['size'] != None:
            self.scan_operations.goto_original_size_settings()
            self.scan_operations.set_scan_setting('size', settings['size'])
        if settings['tiffcompression'] != None:
            if settings['color'] == 'color':
                self.scan_operations.goto_tiff_compression_color_settings()
                self.scan_operations.set_scan_setting('tiffcompression_color', settings['tiffcompression'])
            elif settings['color'] == 'blackonly' or settings['color'] == 'grayscale':
                self.scan_operations.goto_tiff_compression_mono_settings()
                self.scan_operations.set_scan_setting('tiffcompression_mono', settings['tiffcompression'])
            else:
                assert False, "Setting not existing"
        if settings['orientation'] != None:
            self.scan_operations.goto_orientation_settings()
            self.scan_operations.set_scan_setting('orientation', settings['orientation'])
        if settings['lighter_darker'] != None:
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker=settings['lighter_darker'])
        if settings['contrast'] != None:
            self.scan_operations.goto_contrast_settings()
            self.scan_operations.set_scan_settings_contrast(contrast=settings['contrast'])
        self.back_to_scan_to_usb_from_options_list()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        usb_save_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        usb_save_button.mouse_click()
        sleep(5)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def goto_usb_app_landing_view_from_scan_folder(self, net):
        """
        Verify no USB device is connected by checking for no device screen
        :param net:
        :return:
        """
        self.workflow_common_operations.scroll_position(UsbScanAppWorkflowObjectIds.view_scan_screen, UsbScanAppWorkflowObjectIds.button_scan_usb , UsbScanAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , UsbScanAppWorkflowObjectIds.scanFolderPage_column_name , UsbScanAppWorkflowObjectIds.scanFolderPage_Content_Item)
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb )
        current_button = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_scan_usb + " MouseArea")
        current_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.verify_no_front_usb_device_constriant()

    def verify_no_front_usb_device_constriant(self):
        """
        UI should be at no USB device connected screen.
        Verify no front USB device connected screen
        :return:
        """
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.wait_and_validate_property_value(current_button, "visible", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(current_button, "enabled", True, 10, delay = 0.01)
        self.wait_and_validate_property_value(current_button, "constrained", True, 10, delay = 0.01)
        current_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_no_front_device)

    def press_cancel_at_no_usb_device_screen(self):
        """
        UI should be at no USB device connected screen.
        Press Cancel button in the No front USB device screen
        :return:
        """
        # self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_no_front_device, timeout=9.0)
        sleep(3)
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb_no_front_device_cancel)
        current_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def verify_scan_to_usb_landing_view(self):
        """
        This keyword verifies screen is in scan to usb landing view
        :return:
        """
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def verify_scan_to_usb_success(self):
        """
        This keyword verifies screen is in scan to usb success view
        :return:
        """
        progress_view = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_scan_save_success)
        assert progress_view, 'Scan progress not shown'
        self.spice.wait_until(lambda: progress_view["visible"] == False, timeout=100.0)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_scan_save_success)
        logging.info("Inside Scan to USB Successful Screen")
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def verify_filename_string(self, filename):
        """
        This method compares the filename string with the expected string

        Args:
            UI should be in file settings landing view
            filename: expected filename string
        """
        ui_filename_string = self.spice.query_item(UsbScanAppWorkflowObjectIds.button_usb_scan_filename)["displayText"]
        logging.info("Filename = " + ui_filename_string)
        assert ui_filename_string == filename, "Filename mismatch"

    def verify_backgroundcolorremoval_value(self, value):
        """
        This method compares the background color removal value with the expected value

        Args:
            UI should be in file settings landing view
            value: expected value bool
        """
        ui_backgroung_removal_value = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal)["checked"]
        assert ui_backgroung_removal_value == value, "background color removal mismatch"

    def verify_filename_read_only_enabled_screen_displayed(self, net):
        """
        This method is to check the filename read-only enabled
        :return:
        """
        self.workflow_common_operations.goto_item([UsbScanAppWorkflowObjectIds.row_object_filename, UsbScanAppWorkflowObjectIds.button_usb_scan_filename],
                                                  UsbScanAppWorkflowObjectIds.screen_id, select_option=False, scrollbar_objectname=UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        input_box = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.button_usb_scan_filename} {UsbScanAppWorkflowObjectIds.scan_usb_file_name_input}")
        input_box.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_view)
        logging.info("UI: Read-Only Enabled screen display")
        display_message = self.spice.query_item(f"{UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_view} #contentItem")["text"]
        expected_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cReadOnly')
        assert display_message == expected_message, "Filename read-only enabled message is not shown"

    def verify_usb_unsupported_device_error_screen(self, net):
        """
        Verify usb unsupported device error screen displayed and check message.
        :param net
        """
        unsupported_device_error_view = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_unsupported_device_error)
        self.spice.wait_until(lambda:unsupported_device_error_view["visible"])

        self.workflow_common_operations.verify_string(net, "cUSBDeviceConnected",f"{UsbScanAppWorkflowObjectIds.view_usb_unsupported_device_error} {UsbScanAppWorkflowObjectIds.text_title}")
        self.workflow_common_operations.verify_string(net, "cDeviceConnected",f"{UsbScanAppWorkflowObjectIds.view_usb_unsupported_device_error} {UsbScanAppWorkflowObjectIds.text_column_of_detail}")
        self.workflow_common_operations.verify_string(net, "cDisconnectDevice",f"{UsbScanAppWorkflowObjectIds.view_usb_unsupported_device_error} {UsbScanAppWorkflowObjectIds.text_column_of_detail} {UsbScanAppWorkflowObjectIds.contentItem}")
        logging.info("Verify usb unsupported device successfully")

    def press_ok_button_at_usb_unsupported_device_error_screen(self):
        """
        Click OK at usb unsupported device error screen.
        """
        ok_button = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.view_usb_unsupported_device_error} {UsbScanAppWorkflowObjectIds.button_ok}")
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        :return:
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_view)
        logging.info("Click ok button to exit Read-Only Enabled display screen")
        ok_button = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_view} {UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_ok_button}")
        ok_button.mouse_click()

    def select_folder(self, foldername):
        """
        This method used to select the folder name
        :param foldername: foldername
        :return:
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)
        folder_select = self.spice.wait_for("#" + foldername)
        folder_select.mouse_click()
        sleep(2)
        usb_save_here_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_save_here_button)
        usb_save_here_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing) 

    def back_to_scan_to_usb_from_usb_landing_view(self):
        """
        UI should be in Scan to USB landing view.
        Navigates back from USB landing view to Scan to USB screen.
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)
        scan_usb_landing_cancel_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_scan_usb_landing_cancel)
        scan_usb_landing_cancel_button.mouse_click()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def goto_usb_file_settings(self):
        """
        UI should be in Scan to USB landing view.
        Navigates to File settings screen.
        UI Flow is USB Drive->File Name->(File Details settings view)
        :return:
        """
        #N/A
        # current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_scan)
        # current_button.mouse_click()
        # assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_scan_details)
        # logging.info("UI: At File details screen in USB Settings")

    def goto_usb_file_name_setting(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to filename setting screen.
        UI Flow is (File Details settings view)->Filename->(Alphanumeric Keyboard)
        :return:
        """
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_options)
        current_button.mouse_click()
        sleep(2)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_filename, ScanAppWorkflowObjectIds.text_file_name_field_scan_option],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        sleep(2)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_common_keyboard, timeout=12.0)["visible"], "Input keyboard is not shown"
        logging.info("UI: At Scan Filename settings screen")

    def input_folder_name_in_create_folder_screen(self, folder_name, error=False):
        '''
        UI should be at alphanumeric keyboard view.
        Sets foldername
        Args:
            filename: scan to usb foldername
        '''
        logging.info("wait for Create folder screen")
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.create_folder_screen_view)
        display_name_textbox = self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input)
        display_name_textbox.mouse_click()
        display_name_textbox.__setitem__('displayText', folder_name)
        sleep(1)
        keyword_ok = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_keyboard_ok)
        sleep(1)
        keyword_ok.mouse_click()
        if(error):
            assert self.spice.query_item(UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input)["error"] == True
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add_cancel).mouse_click()
        else:
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add).mouse_click()

    def input_folder_name_multiple_times(self, folder_name, error=False):
        '''
        UI should be at alphanumeric keyboard view.
        Sets foldername and opens keyboard five times 
        Args:
            filename: scan to usb foldername
        '''
        logging.info("wait for Create folder screen")
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.create_folder_screen_view)
        display_name_textbox = self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input)
        display_name_textbox.mouse_click()
        display_name_textbox.__setitem__('displayText', folder_name)
        keyword_ok = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

        # Iterate to open the text field and click "OK" multiple times
        for i in range(4):  # 4 times to make a total of 5 including the first time
            logging.info(f"Iteration {i + 1}: Open text field and click OK")
            display_name_textbox.mouse_click()
            keyword_ok = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()

        if(error):
            assert self.spice.query_item(UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input)["error"] == True
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add_cancel).mouse_click()
        else:
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add).mouse_click()

    def input_folder_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Sets empty foldername
        '''
        logging.info("wait for Create folder screen")
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.create_folder_screen_view)
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_folder_add).mouse_click()

    def verify_text_field_error_message(self, net):
        '''
        Verify text field error message.
        :param net
        '''
        self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input} {UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input_error_massage}")
        self.workflow_common_operations.verify_string(net, "cCannotContainSpecialCharacter",f"{UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input} {UsbScanAppWorkflowObjectIds.scan_usb_folder_name_input_error_massage}", isSpiceText=True)
        logging.info("Verify text field error message")

    def verify_paper_jam_message(self):
        '''
        Verify paper jam message.
        '''
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.paper_jam_window, timeout=30.0)
        hide_button = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.hide_button}")
        hide_button.mouse_click()

    def verify_constrained_message(self, net, message):
        '''
        Verify constrained message.
        :param net, message
        '''
        sleep(2)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_constraint_message, timeout=30.0)
        self.workflow_common_operations.verify_string(net, message, f"{UsbScanAppWorkflowObjectIds.view_constraint_message} {UsbScanAppWorkflowObjectIds.constrain_description_view}")
        ok_button = self.spice.wait_for(f"{UsbScanAppWorkflowObjectIds.ok_button_message}")
        ok_button.mouse_click()
        logging.info("Verify constrained message")

    def set_usb_file_name_setting(self, filename: str, screen = "folder_landing_screen"):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to usb filename
            screen:option_screen/folder_landing_screen
        '''
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_common_keyboard)
        if screen == "option_screen":
            display_name_textbox = self.spice.query_item(ScanAppWorkflowObjectIds.menu_list_scan_settings + " " + UsbScanAppWorkflowObjectIds.button_usb_scan_filename)
        else:
            display_name_textbox = self.spice.query_item(UsbScanAppWorkflowObjectIds.view_scan_usb_landing + " " + UsbScanAppWorkflowObjectIds.button_usb_scan_filename)
        display_name_textbox.__setitem__('displayText', filename)
        sleep(2)
        keyword_ok = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        logging.info("UI: At Scan Filename settings screen")

    def set_usb_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_common_keyboard)
        sleep(3)
        clear_text = self.spice.wait_for(UsbScanAppWorkflowObjectIds.clear_text_filename)
        clear_text.mouse_click()
        sleep(2)
        keyword_ok = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_filename_empty_message(self, net):
        '''
        UI should be at usb constraint message screen.
        Function will verify the filename empty message.
        '''
        message = self.spice.query_item(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_file_name_read_only_ok_button)
        send_button.mouse_click()

    def goto_usb_file_format_setting(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to fil format setting screen.
        UI Flow is (File Details settings view)->FileType->(Scan File Type Settings screen)
        :return:
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_file_type, ScanAppWorkflowObjectIds.combobox_scan_file_type],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
        logging.info("UI: At File Type settings screen")

    def goto_file_settings_via_usb(self):
        """
        Navigates to File settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)
        :return:
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_usb_file_settings()

    def goto_file_name_setting_via_usb(self):
        """
        UI should be in Scan to USB File settings screen starting from Home screen..
        Navigates to filename setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Filename->(Alphanumeric Keyboard)
        """
        self.goto_file_settings_via_usb()
        sleep(2)
        self.goto_usb_file_name_setting()

    def goto_file_format_setting_via_usb(self):
        """
        UI should be in Scan to USB File settings screen starting from Home screen.
        Navigates to fil format setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->FileType->(Scan File Type Settings screen)
        """
        self.goto_file_settings_via_usb()
        sleep(2)
        self.goto_usb_file_format_setting()

    def back_to_scan_to_usb_from_file_settings(self):
        """
        UI should be in file settings screen - Home->Scan->USB Drive->File Name->(File Details settings view)
        Navigates back to USB landing view.
        """
        # self.workflow_common_operations.back_button_press(ScanAppWorkflowObjectIds.menu_list_scan_settings,
        #                                                   UsbScanAppWorkflowObjectIds.view_scan_usb_landing, index=2)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        sleep(5)

    def set_scan_to_usb_fileformat(self, filetype: str):
        """
        UI should be on File format settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
        filetype_id = ScanAppWorkflowObjectIds.filetype_dict[filetype.lower()][1]
        self.workflow_common_operations.goto_item(filetype_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen,
                                                  ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
    
    def verify_selected_quickset_name(self, net, stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check UsbQuicksetSelected Button
        '''
        text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, stringId)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing  + " MouseArea")
        text = text.split(" ")
        text = "_".join(text)
        assert self.spice.wait_for(f"#{text}")["checked"]
    
    def is_quickset_existing(self):
        '''
        This is helper method to verify is quickset existing
        '''
        try:
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.default_quickset_button, 5)
            return True
        except:
            logging.info("No usb quicksets in usb screen")
            return False
    
    def goto_usb_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # self.workflow_common_operations.scroll_to_position_vertical(scroll_option, CopyAppWorkflowObjectIds.qs_scroll_horizontal_bar)
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return
        
        view_all_btn = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_all_locator)
        view_all_btn.mouse_click()

        self.spice.wait_for(UsbScanAppWorkflowObjectIds.defaults_and_quick_sets_view)
    
    def select_usb_quickset(self, quickset_name):
        '''
        This is helper method to select usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        quickset_item = self.spice.wait_for(UsbScanAppWorkflowObjectIds.defaults_and_quick_sets_view + " " + quickset_name)
        quickset_item.mouse_click()
        #self.spice.common_operations.goto_item(quickset_name, CopyAppWorkflowObjectIds.defaults_and_quick_sets_view, select_option=True)
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
    
    def save_as_default_usb_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        usb_quickset_save_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.save_as_default_button)
        usb_quickset_save_button.mouse_click()
        sleep(3)
        try:
            (self.spice.query_item(MenuAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_creds(True, "admin", "12345678")
            sleep(3)
        finally:
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_menu_save_options)
            if (self.spice.query_item(UsbScanAppWorkflowObjectIds.usb_quickset_as_defaults_option)["visible"] == True):
                current_option = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_quickset_as_defaults_option)
                current_option.mouse_click()
            current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.ok_under_save_option_veiw)
            current_button.mouse_click()
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.save_as_default_alert_view)
            sleep(2)
            save_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.save_as_default_alert_save_button)
            self.spice.wait_until(lambda: save_button["visible"])
            self.spice.wait_until(lambda: save_button["enabled"])
            save_button.mouse_click()
            sleep(2)
            view_scan_usb_landing = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing, timeout=20.0)
            self.spice.wait_until(lambda:view_scan_usb_landing["visible"])

    def save_to_usb_quickset_default(self, cdm, scan_options:Dict):
        '''
        Start save to USB drive with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        scan_options = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'orientation': 'portrait',
            'lighter_darker': 1
        }
        '''
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_options_list_from_scan_to_usb()
        sleep(5)

        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanUsb"        
        ticket_default_response = cdm.get_raw(uri)
        assert ticket_default_response.status_code < 300
        ticket_default_body = ticket_default_response.json()

        filesize_dict = {
        "lowest": "lowest",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "highest": "highest"
        }

        settings = {
            'filetype': scan_options.get('filetype', None),
            'resolution': scan_options.get('resolution', None),
            'filesize': scan_options.get('filesize', None),
            'sides': scan_options.get('sides', None),
            'color': scan_options.get('color', None),
            'size': scan_options.get('size', None),
            'tiffcompression': scan_options.get('tiffcompression', None),
            'orientation': scan_options.get('orientation', None),
            'lighter_darker': scan_options.get('lighter_darker', None)
        }

        if (settings['filetype'] != None) and (scan_options["filetype"] != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["fileType"]):
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if (settings['resolution'] != None) and (scan_options["resolution"] != ticket_default_body["src"]["scan"]["resolution"].lower()):
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if (settings['filesize'] != None) and (filesize_dict.get(scan_options["filesize"]) != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["filesize"]):
            self.scan_operations.goto_filesize_settings()
            self.scan_operations.set_scan_setting('filesize', settings['filesize'])
        if (settings['sides'] != None) and (scan_options["sides"] != ticket_default_body["src"]["scan"]["plexMode"]):
            self.scan_operations.goto_sides_settings()
            self.scan_operations.set_scan_setting('sides', settings['sides'])
        if (settings['color'] != None) and (scan_options["color"] != ticket_default_body["src"]["scan"]["colorMode"]):
            self.scan_operations.goto_color_settings()
            self.scan_operations.set_scan_setting('color', settings['color'])
        if (settings['size'] != None) and (scan_options["size"] != ticket_default_body["src"]["scan"]["mediaSize"]):
            self.scan_operations.goto_original_size_settings()
            self.scan_operations.set_scan_setting('size', settings['size'])
        if (settings['orientation'] != None) and (scan_options["orientation"] != ticket_default_body["src"]["scan"]["contentOrientation"]):
            self.scan_operations.goto_orientation_settings()
            self.scan_operations.set_scan_setting('orientation', settings['orientation'])
        if (settings['lighter_darker'] != None) and (scan_options["lighter_darker"] != ticket_default_body["pipelineOptions"]["imageModifications"]["exposure"]): #
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker = settings['lighter_darker'])
        if settings['tiffcompression'] != None:
            if settings['color'] == 'color':
                self.scan_operations.goto_tiff_compression_color_settings()
                self.scan_operations.set_scan_setting('tiffcompression_color', settings['tiffcompression'])
            elif settings['color'] == 'blackonly' or settings['color'] == 'grayscale':
                self.scan_operations.goto_tiff_compression_mono_settings()
                self.scan_operations.set_scan_setting('tiffcompression_mono', settings['tiffcompression'])
            else:
                assert False, "Setting not existing"

        self.back_to_scan_to_usb_from_options_list()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.save_as_default_usb_ticket()

    def goto_content_type_settings_via_usb(self):
        """
        Navigates to Content type in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Content Type->(Content Type settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(5)
        self.scan_operations.goto_content_type_settings()

    def goto_original_paper_type_settings_via_usb(self):
        """
        Navigates to Content type in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Original Paper Type->(Original Paper Type settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(5)
        self.scan_operations.goto_original_paper_type_settings()
    def wait_for_scan_job_corresponding_status_displayed(self, net, status: str, timeout=30):
        """
        Wait until corresponding status displayed in FP UI.
        :param status: Starting/Scanning/Sending/Complete
        :param time_out: int
        """
        # It's difficult to get Scanning and Sending status as toast is too fast.
        job_concurrent_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrent_supported == 'true':
            if status == "Starting":
                option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
            elif status == "Scanning":
                option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
            elif status == 'Sending':
                option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSending')
            elif status == 'Complete':
                option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessfulMessage')
            elif status == 'preparingToSend':
                option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cProgressJobQueue')
            start_time = time()
            while time()-start_time < timeout:
                try:
                    toast_msg = self.spice.query_item(UsbScanAppWorkflowObjectIds.view_scan_job_toastwindow+" SpiceText")["text"]
                    logging.info(f"Status:<{toast_msg}> found in FP UI")
                    if option in toast_msg:
                       break
                except:
                    logging.info("Still finding corresponding status.")
            
            if option not in toast_msg:
                raise TimeoutError("Required Toast message does not appear within %s " % timeout)    
        else:
            if status == 'Complete':
                self.spice.wait_for(ScanAppWorkflowObjectIds.scan_complete_wizard_screen, timeout)
            else:
                raise ValueError('Please make sure that the added message is included in the method')

    def goto_usb_file_name_setting_interactive_summary(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to filename setting screen.
        UI Flow is (File Details settings view)->Filename->(Alphanumeric Keyboard)
        :return:
        """
        self.workflow_common_operations.goto_item([UsbScanAppWorkflowObjectIds.row_object_filename, UsbScanAppWorkflowObjectIds.button_usb_scan_filename], UsbScanAppWorkflowObjectIds.screen_id, scrollbar_objectname=UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        sleep(2)
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_common_keyboard)
        logging.info("UI: At Scan Filename settings screen")      

    def goto_usb_file_name_setting_interactive_summary_via_usb(self):
        """
        UI should be in Scan to USB File settings screen starting from Home screen..
        Navigates to filename setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Filename->(Alphanumeric Keyboard)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_usb_file_name_setting_interactive_summary() 

    def goto_sides_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is Sides-> (Sides Settings screen).
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_sides, ScanAppWorkflowObjectIds.combobox_scan_sides],UsbScanAppWorkflowObjectIds.screen_id, scrollbar_objectname=UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen)
        logging.info("UI: At Sides settings screen") 

    def goto_sides_settings_interactive_summary_via_usb(self):
        """
        UI should be in Scan to USB Sides Settings screen..
        Navigates to Sides setting screen.
        UI Flow is Home->Scan->USB Drive->Sides->(Sides Settings screen)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_sides_settings_interactive_summary()
        
    def goto_filetype_settings_interactive_summary_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Type->(File Type settings screen)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_filetype_settings_interactive_summary()

    def goto_filetype_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is file type-> (file type Settings screen).
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)
        self.workflow_common_operations.scroll_to_position_vertical(0.4, UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        sleep(2)
        file_type = self.spice.wait_for(ScanAppWorkflowObjectIds.combobox_scan_file_type)
        file_type.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
        logging.info("UI: At filetype settings screen") 

    def goto_usb_resolution_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is resolution-> (resolution Settings screen).
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)
        self.workflow_common_operations.scroll_to_position_vertical(0.4, UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        sleep(2)
        resolution_combobox = self.spice.wait_for(ScanAppWorkflowObjectIds.combobox_scan_resolution)
        resolution_combobox.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen)
        logging.info("UI: At resolution settings screen") 
         
    def goto_resolution_settings_interactive_summary_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->resolution->(resolution settings screen)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_usb_resolution_settings_interactive_summary()

    def goto_usb_color_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is color-> (color Settings screen).
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)

        self.workflow_common_operations.scroll_to_position_vertical(0.6, UsbScanAppWorkflowObjectIds.scrollbar_usb_landing_page)
        sleep(2)

        color_mode = self.spice.wait_for(ScanAppWorkflowObjectIds.combobox_scan_color)
        color_mode.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_color_screen)
        logging.info("UI: At color settings screen") 

    def goto_color_settings_interactive_summary_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->color->(color settings screen)
        """
        self.goto_scan_to_usb_screen()
        sleep(2)
        self.goto_usb_color_settings_interactive_summary()

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.spice.scan_settings.click_expand_button()
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)["isPreviewButtonVisible"] == False

    def click_back_button_in_header(self):
        """
        UI should be in resolution setting view
        Navigates back from resolution setting screen to scan settings view
        """
        #self.workflow_common_operations.back_button_press(UsbScanAppWorkflowObjectIds.view_usb_folder,
        #                                               UsbScanAppWorkflowObjectIds.view_scan_usb_landing, index=2)

        if (self.spice.query_item(UsbScanAppWorkflowObjectIds.button_back)["visible"] == True):
            # TODO verify the code once the back button is in position
            logging.info("Back button is visible")
            back_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_back)
            back_button.mouse_click()
        else:
            logging.info("Back button is not visible")

    def verify_multiple_usb_partition(self, count):
        """
        This is a helper message to verify there are 2 partitioned USBs present
        UI Flow is Home->Scan->USB Drive->Select->Back->(Verify 2 Partitions)
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_usb_folder)
        assert self.spice.query_item(UsbScanAppWorkflowObjectIds.view_usb_folder)["deviceListCount"] == count

    def select_partition(self, name: str):
        """
        This method used to select the partition with name
        :param name: name of partition
        :return:
        """
        sleep(1)
        partition_select = self.spice.wait_for("#" + name, timeout=15.0)
        partition_select.mouse_click()
        
    def scrollto_usbfolder_in_folder_selection(self, folder_name:str):
        """
        UI should be on Usb Folder selection screen.
        UI Flow is Home > Scan > Scan to Usb > Edit
        """
        logging.info("scrolling to folder: %s", folder_name)
        sleep(3)
        logging.info(f"Try to scroll <{folder_name}> into view of screen")
        screen_id = f"{UsbScanAppWorkflowObjectIds.view_usb_folder} {UsbScanAppWorkflowObjectIds.folder_list_screen_view}"
        current_screen = self.spice.wait_for(screen_id)
        at_y_end = False
        is_visible = False
        while(is_visible is False and at_y_end is False):
            try:
                is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, folder_name)
                while (is_visible is False and at_y_end is False):
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, 20)
                    is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, folder_name)
                    at_y_end = current_screen["atYEnd"]
            except Exception as err:
                logging.info(f"exception msg {err}")
                if str(err).find("Query selection returned no items") != -1:
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, 20)
                    at_y_end = current_screen["atYEnd"]
                else:
                    raise Exception(err)
        logging.info(f"The item <{folder_name}> is in screen view <{screen_id}> now: <{is_visible}>")

        return is_visible
    
    def validate_folder_visibility_in_usb_folder_selection(self, folder_name):
        """
        Validates if a folder is visible within the USB folder selection screen.
        :param folder_name: The name of the folder to validate.
        :return: True if the folder is visible, False otherwise.
        """
        header_y = self.spice.wait_for(UsbScanAppWorkflowObjectIds.scan_usb_selected_Directory)["y"]
        footer_y = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_select_folder_footer)["y"]
 
        try:
            item_widget = self.spice.query_item(folder_name)
            item_y, item_height = item_widget["y"], item_widget["height"]
            return header_y < item_y and item_y + item_height < footer_y
        except Exception:
            logging.info(f"Folder <{folder_name}> is not visible.")
            return False

    def scroll_to_bottom(self, usb_select_folder_layout, folder_name):
        """
        Incrementally scroll to the bottom of the page to find the folder.
        :param usb_select_folder_layout: The layout of the USB folder selection screen.
        :param folder_name: The name of the folder to find.
        :return: True if the folder is found while scrolling, False otherwise.
        """
        pos = 0.02
        logging.info(f"pos: <{pos}>")
        while not usb_select_folder_layout["atYEnd"]:
            self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_select_folder_scroll_bar).__setitem__("position", str(pos))
            if self.validate_folder_visibility_in_usb_folder_selection(folder_name):
                logging.info(f"Folder <{folder_name}> found while scrolling to the bottom.")
                return True
            pos += 0.02
        return False

    def goto_options_list_from_scan_to_usb_screen(self):
        '''
        UI should be in Scan to scan to usb screen.
        Navigates to Options screen starting from scant to usb screen.
        UI Flow is Scan to usb ->Options->(Options list)
        '''
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_options)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        # Wait for Options screen
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.menu_list_scan_settings)

    
    def wait_and_validate_property_value(self, object, property, state, timeout = 5, delay = 0.25):
        self.workflow_common_operations.wait_until_property_value(object, property, state, timeout, delay = delay)
        assert object[property] == state

    def validate_screen_buttons( self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible, click = False, delayClick = 0, constrained_message = ""):
        button_ids = [
            UsbScanAppWorkflowObjectIds.button_usb_send,
            UsbScanAppWorkflowObjectIds.button_usb_start,
            UsbScanAppWorkflowObjectIds.button_usb_stop_scan
        ]

        button = None
        for button_id in button_ids:
            if buttonObjectId == button_id:
                try:
                    button = self.spice.wait_for(button_id, 60)
                    logging.info("Found button with ID %s", button_id)
                    self.wait_and_validate_property_value(button, "visible", True, 30, delay = 0.01)
                    self.wait_and_validate_property_value(button, "enabled", True, 30, delay = 0.01)
                    self.wait_and_validate_property_value(button, "constrained", isButtonConstrained, 30, delay = 0.01)
                    if click:
                        sleep(delayClick)
                        center_x = button["width"] / 2
                        center_y = button["height"] / 2
                        button.mouse_click(center_x, center_y)
                    break
                except:
                    logging.info("Button with ID %s not found", button_id)
                    continue

        if button is None:
            logging.error("Button with ID %s not found", buttonObjectId)
            raise ValueError(f"Button with ID {buttonObjectId} not found")

        # In case that button is constrained, and was clicked, and constrained message was passed by parameter, check message
        if isButtonConstrained and click and constrained_message != "":
            self.verify_constrained_message(net, constrained_message)

        #Get Eject
        ejectButton = self.spice.wait_for( UsbScanAppWorkflowObjectIds.eject_button,10)

        #Validate eject
        self.wait_and_validate_property_value(ejectButton, "visible", isEjectButtonVisible, delay = 0.01)

    def check_stop_scan_button(self):
        button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_stop_scan, timeout = 10)
        logging.info(f"Button visible: {button['visible']}")
        self.wait_and_validate_property_value(button, "visible", True, timeout = 10, delay = 0.01)

    def wait_stateMachine_state(self, state, timeout = 10 ):
        sendLanding = self.spice.wait_for( UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        self.spice.wait_until( lambda: sendLanding["state"] == state , timeout )

    def wait_mainButton_type(self, state, timeout = 10 ):
        sendLanding = self.spice.wait_for( UsbScanAppWorkflowObjectIds.view_scan_usb_landing , 5 )
        self.spice.wait_until( lambda: sendLanding["mainButtonType"] == state , timeout )  

    def get_scan_usb_app(self):
        logging.info("Waiting for scan usb app")
        scan_usb_app = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan_menu_app)
        return scan_usb_app
        
    def get_scan_usb_app_clickable(self):
        logging.info("Waiting for scan usb app")
        scan_usb_app_clickable = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_usb_clickable)
        return scan_usb_app_clickable
    
    def click_usb_disconnect_ok_button(self):
        """
        Click OK button on USB device is disconnected screen.
        @param:
        @return:
        """
        logging.info("Press the OK button")
        ok_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_disconnect_ok_button)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def check_usb_disconnected_error_message(self, net):
        '''
        Check usb disconnected error message
        '''
        self.spice.wait_for("#errorMessage",timeout=60)
        expected_str = LocalizationHelper.get_string_translation(net, "cUSBDisconnectedText")
        actual_str = self.spice.wait_for("#errorMessage #alertDetailDescription #contentItem")["text"]
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"
        ok_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_disconnect_ok_button)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def verify_usb_destination(self, path_text):
        '''
        Verify the destination path
        '''
        destinationConfigured = self.spice.wait_for(UsbScanAppWorkflowObjectIds.destination_name, timeout=20)
        self.spice.wait_until(lambda: destinationConfigured["text"] == path_text)

    def verify_adf_loaded_warning_modal_dialog(self):
        '''
        Ui Should be Send App
        if preview in progress ADF warning modal dialog will be shown
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.adf_warning_modal_dialog)

    def dismiss_usb_disconnected_screen(self):
        """
        To dismiss usb disconnected screen
        """
        ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.ok_button_on_disconnected_screen)
        self.spice.wait_until(lambda: ok_button["visible"])
        sleep(1)
        ok_button.mouse_click()


    def perform_scan_usb_job_from_home_scanapp(self, cdm, udw, net, job,scan_emulation= None, option_payload=None, pages=1, pdf_encryption_code=None, save_options_in_landing_view:bool=False, time_out=90):
        """
        1. Navigation to Home -> Scan app -> Scan to USB landing view
        2. Go to usb options, change options if need to change options. Back to usb landing view.
        3. Send usb job
        4. Validation scan job ticket scan common settings list options if options changed.
        5. Check scan usb job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param option_payload: scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                'content_type': 'mixed', # value from key of scan_content_type_option_dict
                'file_type': 'pdf', # value from key of scan_file_type_option_dict
                'pdf_encryption': True, # True/False
                "high_compression": False, # True/False
                'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
                'file_size': 'medium', # value from key of scan_file_size_option_dict
                'original_sides': '1-sided'', # value from key of scan_sides_option_dict
                'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
                'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
                'orientation': 'portrait', # value from key of scan_orientation_option_dict
                'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
                'lighter&darker': 1   # int [1-9]
            }
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param save_options_in_landing_view: click save button to save update options
        @param time_out: timeout to wait for job finish
        """
        self.workflow_common_operations.goto_scan_app()
        self.spice.scan_settings.goto_usb_from_scanapp_at_home_screen()

        self.perform_scan_usb_job(cdm, udw, net, job,scan_emulation, option_payload, pages, pdf_encryption_code, save_options_in_landing_view, time_out)
    

    def perform_scan_usb_job_from_menu_scanapp(self, cdm, udw, net, job,scan_emulation=None, option_payload=None, pages=1, pdf_encryption_code=None, save_options_in_landing_view:bool=False, time_out=90):
        """
        1. Navigation to Home -> Menu -> Scan app -> Scan to USB landing view
        2. Go to usb options, change options if need to change options. Back to usb landing view.
        3. Send usb job
        4. Validation scan job ticket scan common settings list options if options changed.
        5. Check scan usb job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param option_payload: scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                'content_type': 'mixed', # value from key of scan_content_type_option_dict
                'file_type': 'pdf', # value from key of scan_file_type_option_dict
                'pdf_encryption': True, # True/False
                "high_compression": False, # True/False
                'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
                'file_size': 'medium', # value from key of scan_file_size_option_dict
                'original_sides': '1-sided'', # value from key of scan_sides_option_dict
                'original_sides_auto': 'true', # value from key of scan_sides_auto_option_dict
                'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
                'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
                'orientation': 'portrait', # value from key of scan_orientation_option_dict
                'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
                'lighter&darker': 1   # int [1-9]
            }
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param save_options_in_landing_view: click save button to save update options
        @param time_out: timeout to wait for job finish
        """
        self.goto_scan_to_usb_screen() 

        self.perform_scan_usb_job(cdm, udw, net, job,scan_emulation, option_payload, pages, pdf_encryption_code, save_options_in_landing_view, time_out)
    
    def perform_scan_usb_job_from_menu_scanapp_enterprise(self, cdm, udw, net, job,scan_emulation=None, option_payload=None, pages=1, pdf_encryption_code=None, save_options_in_landing_view:bool=False, time_out=90):
        """
        1. Navigation to Home -> Menu -> Scan app -> Scan to USB landing view
        2. Go to usb options, change options if need to change options. Back to usb landing view.
        3. Send usb job
        4. Validation scan job ticket scan common settings list options if options changed.
        5. Check scan usb job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param option_payload: scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                'content_type': 'mixed', # value from key of scan_content_type_option_dict
                'file_type': 'pdf', # value from key of scan_file_type_option_dict
                'pdf_encryption': True, # True/False
                "high_compression": False, # True/False
                'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
                'file_size': 'medium', # value from key of scan_file_size_option_dict
                'original_sides': '1-sided'', # value from key of scan_sides_option_dict
                'original_sides_auto': 'true', # value from key of scan_sides_auto_option_dict
                'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
                'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
                'orientation': 'portrait', # value from key of scan_orientation_option_dict
                'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
                'lighter&darker': 1   # int [1-9]
            }
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param save_options_in_landing_view: click save button to save update options
        @param time_out: timeout to wait for job finish
        """
        self.goto_scan_to_usb_screen()

        self.perform_scan_usb_job_enterprise(cdm, udw, net, job,scan_emulation, option_payload, pages, pdf_encryption_code, save_options_in_landing_view, time_out)

    def perform_scan_usb_job(self, cdm, udw, net, job,scan_emulation, option_payload=None, pages=1, pdf_encryption_code=None, save_options_in_landing_view:bool=False, time_out=90):
        """
        1. Go to usb options, change options if need to change options. Back to usb landing view.
        2. Send usb job
        3. Validation scan job ticket scan common settings list options if options changed.
        4. Check scan usb job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param option_payload: scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                'content_type': 'mixed', # value from key of scan_content_type_option_dict
                'file_type': 'pdf', # value from key of scan_file_type_option_dict
                'pdf_encryption': True, # True/False
                "high_compression": False, # True/False
                'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
                'file_size': 'medium', # value from key of scan_file_size_option_dict
                'original_sides': '1-sided'', # value from key of scan_sides_option_dict
                'original_sides_auto': 'true', # value from key of scan_sides_auto_option_dict
                'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
                'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
                'orientation': 'portrait', # value from key of scan_orientation_option_dict
                'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
                'lighter&darker': 1   # int [1-9]
            }
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param save_options_in_landing_view: click save button to save update options
        @param time_out: timeout to wait for job finish
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

        if option_payload != None:
            self.goto_options_list_from_scan_to_usb()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)

            self.back_to_scan_to_usb_from_options_list()
        
        if save_options_in_landing_view:
            self.save_as_default_usb_ticket()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)
        
        scan_resource = None
        if scan_emulation != None:
            scan_resource = self.get_scan_resource_used(udw, scan_emulation)
        self.press_save_to_usb(wait_time=0)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()
            self.verify_scan_to_usb_landing_view()

        job_ticket = job.get_job_details("scanUsb")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]          
        if option_payload != None:
            logging.info("validation scan usb job ticket common settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, option_payload, scan_type="scanUsb")

        logging.info(f"scan_resource: {scan_resource}")
        adf_loaded = False
        if pages == 1 and scan_resource == "ADF" and scan_emulation != None:
            scan_emulation.media.load_media("ADF")
            adf_loaded = True
        self.wait_for_scan_usb_job_to_complete(cdm, udw, net, job,scan_emulation, file_type, pages, time_out, adf_loaded=adf_loaded)

    def perform_scan_usb_job_enterprise(self, cdm, udw, net, job,scan_emulation, option_payload=None, pages=1, pdf_encryption_code=None, save_options_in_landing_view:bool=False, time_out=90):
        """
        1. Go to usb options, change options if need to change options. Back to usb landing view.
        2. Send usb job
        3. Validation scan job ticket scan common settings list options if options changed.
        4. Check scan usb job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param option_payload: scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                'content_type': 'mixed', # value from key of scan_content_type_option_dict
                'file_type': 'pdf', # value from key of scan_file_type_option_dict
                'pdf_encryption': True, # True/False
                "high_compression": False, # True/False
                'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
                'file_size': 'medium', # value from key of scan_file_size_option_dict
                'original_sides': '1-sided'', # value from key of scan_sides_option_dict
                'original_sides_auto': 'true', # value from key of scan_sides_auto_option_dict
                'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
                'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
                'orientation': 'portrait', # value from key of scan_orientation_option_dict
                'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
                'lighter&darker': 1   # int [1-9]
            }
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param save_options_in_landing_view: click save button to save update options
        @param time_out: timeout to wait for job finish
        """
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

        if option_payload != None:
            self.goto_options_list_from_scan_to_usb()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)

            self.back_to_scan_to_usb_from_options_list()
        
        if save_options_in_landing_view:
            self.save_as_default_usb_ticket()
        
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)
        sleep(2)
        if(pages > 1):
            self.goto_options_list_from_scan_to_usb()
            self.scan_operations.select_add_more_pages_combo()
            self.back_to_scan_to_usb_from_options_list()

        self.press_save_to_usb_enterprise(wait_time=0)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()
            self.verify_scan_to_usb_landing_view()

        job_ticket = job.get_job_details("scanUsb")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if option_payload != None:
            logging.info("validation scan usb job ticket common settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, option_payload, scan_type="scanUsb")
        
        self.wait_for_scan_usb_job_to_complete_enterprise(cdm, udw, net, job,scan_emulation, file_type, pages, time_out)

    def get_scan_resource_used(self, udw, scan_emulation):
        """
        Return current scan resouse is under used
        """
        list_input_devices = udw.mainApp.ScanMedia.listInputDevices().lower()
        logging.info(f"list_input_devices: {list_input_devices}")
        logging.info(f"scan_emulation.media.is_media_loaded('ADF'): {scan_emulation.media.is_media_loaded('ADF')}")
        if "adf" in list_input_devices:
            logging.info("The device support ADF")
            if scan_emulation.media.is_media_loaded('ADF')== True or scan_emulation.media.is_media_loaded('ADF') == 'Success':
                logging.info("The scan resource from ADF")
                return "ADF"
            else:
                logging.info("The scan resource from glass")
                return "Glass"
        elif "mdf" in list_input_devices:
            logging.info("The scan resource from MDF")
            return "MDF"

        elif "glass" in list_input_devices:
            logging.info("The scan resource from glass")
            return "Glass"
        else:
            logging.info(f"The scan resource is from <{list_input_devices}>")
            raise Exception("Please add corresponding scan resource into if condition")
             
    def wait_for_scan_usb_job_to_complete(self, cdm, udw, net, job,scan_emulation, file_type, pages=1, time_out=90, adf_loaded=False):
        """
        wait for scan usb job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        if scan_emulation == None:            
            scan_resource = common_instance.scan_resource()
        else:
            scan_resource= self.get_scan_resource_used(udw, scan_emulation)
        
        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages(type = "usb")


        if not adf_loaded:
            if scan_resource == "Glass": 
                try:
                    for _ in range(pages-1):
                        scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                        self.spice.validate_button(scan_add_page_button)
                        scan_add_page_button.mouse_click()
                        sleep(2)

                    scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                    logging.info("#finish button found")
                    self.spice.validate_button(scan_add_page_done_button)
                    scan_add_page_done_button.mouse_click()
                except TimeoutError:
                    logging.info("flatbed Add page is not available")
            elif scan_resource == "MDF":
                if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"] and file_type in ["tiff", "pdf", "pdfa"]:
                    # todo: need to add multiple page scene when bug DUNE-147017 fixed.
                    self.spice.scan_settings.mdf_addpage_window_alert_click_option()
                elif configuration.productname == "jupiter" :
                    for _ in range(pages-1):
                        udw.mainApp.ScanMedia.loadMedia("MDF")
                        sleep(2)

                    self.validate_screen_buttons(net, False, UsbScanAppWorkflowObjectIds.button_usb_send, True)
                    self.press_save_to_usb()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "scanUsb", "status": "success"}], time_out = 300)
        # wait for status dismiss
        sleep(7)

    def wait_for_scan_usb_job_to_complete_enterprise(self, cdm, udw, net, job,scan_emulation, file_type, pages=1, time_out=90):
        """
        wait for scan usb job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        if scan_emulation == None:            
            scan_resource = common_instance.scan_resource()
        else:
            scan_resource= self.get_scan_resource_used(udw, scan_emulation)
        
        self.scan_operations.flatbed_scan_more_pages_enterprise(cdm, pages)

        # wait for status dismiss
        sleep(7)

    def perform_scan_usb_job_and_check_file_name(self, job, file_name, file_type, prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='', prefix_username='admin', suffix_username='admin', time_out=90):
        """
        1. Navigation to Home -> Menu -> Scan app -> Scan to USB landing view
        2. Send usb job
        3. Get preview file name from job details, and check file name
        4. Wait for job complete
        @param job
        @param file_name:  file_name from settings
        @param file_type:  file_type from settings, value from key of scan_file_type_option_dict
        @param prefix_type:  prefix_type from settings, value from key of scan_file_name_prefix_option_dict
        @param suffix_type:  suffix_type from settings, value from key of scan_file_name_suffix_option_dict
        @param custom_prefix_string: custom_prefix_string comes from Settings, only custom has Settings
        @param custom_suffix_string:  custom_suffix_string comes from Settings, only custom has Settings
        @param prefix_username: prefix_username select username from settings
        @param suffix_username: suffix_username select username from settings
        @param time_out: timeout to wait for job finish 
        """
        self.goto_scan_to_usb_screen()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

        self.press_save_to_usb(wait_time=0)

        job_ticket = job.get_job_details("scanUsb")
        file_name_preview_from_job = job_ticket['pipelineOptions']['sendFileAttributes']['fileNamePreview']
        logging.info(f'preview file name from job details is: {file_name_preview_from_job}')
        self.spice.quickset_ui.validate_scan_file_name(file_name_preview_from_job, file_name, file_type, prefix_type, suffix_type, custom_prefix_string, custom_suffix_string, prefix_username, suffix_username)
        
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "scanUsb", "status": "success"}], time_out)
        # wait for status dismiss
        sleep(7)

    def check_eject_button_visible(self, visible: bool, timeout = 10.0):
        '''
        Check eject button is visible or not
        '''
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button)
        self.spice.wait_until(lambda: button["visible"] == visible, timeout)

    def click_eject_button(self):
        '''
        Click eject button
        '''
        eject_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button)
        eject_btn.mouse_click()

    def goto_blank_page_suppression_settings_via_usb(self):
        """
        Navigates to blank_page_suppression in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Blank Page Suppression->(Blank Page Suppression settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_blank_settings()

    def start_send_from_secondary_panel(self, button_object_id = None, scan_more_pages: bool = False, wait_time=2):
        '''
        Ui Should be in secondary panel
        Click on send button starts send
        '''
        current_button = self.spice.wait_for(button_object_id)
        self.spice.wait_until(lambda: current_button["visible"] == True)
        self.spice.wait_until(lambda: current_button["enabled"] == True)
        current_button.mouse_click()
        sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def check_original_side_constrained(self, net, side_mode:str, constrained_message: str = ""):
        self.scan_operations.goto_sides_settings()
        to_select_item = ScanAppWorkflowObjectIds.sides_dict[side_mode][1]
        current_button = self.spice.wait_for(to_select_item, timeout=30)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        self.verify_constrained_message(net,constrained_message )
        self.workflow_common_operations.back_or_close_button_press(f"{ScanAppWorkflowObjectIds.view_scan_settings_sides_combobox_view} {ScanAppWorkflowObjectIds.back_button}", ScanAppWorkflowObjectIds.menu_list_scan_settings)
        assert self.spice.wait_for(UsbScanAppWorkflowObjectIds.menu_list_scan_settings, timeout = 9.0)        

    def goto_usb_job_notification_setting(self):
        '''
        UI should be in Scan to USB job notification screen.
        Navigates to job notification setting screen.
        UI Flow is app landing view -> settings -> job notification setting
        '''
        current_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_options, timeout=9.0)
        current_button.mouse_click()
        sleep(2)
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.scan_job_notification_setting,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        sleep(2)
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_job_notification_setting_view)
        logging.info("UI: At Scan job notification settings screen")

    def verify_job_notification_setting(self, job_notification_setting: str, checked: bool = True):
        '''
        Verify job notification setting
        @param job_notification_setting: job notification setting
        @param checked: expected checked state
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_job_notification_setting_view)
        option = self.spice.query_item(job_notification_setting)
        assert option["visible"] == True, f"Option {job_notification_setting} is not visible"
        assert option["checked"] == checked, f"Option {job_notification_setting} checked state is not {checked}"

    def verify_job_notification_include_thumbnail_setting(self, net, checked: bool = True, constrained: bool = False):
        '''
        Verify job notification option include thumbnail
        @param checked: expected checked state
        @param constrained: expected constrained state
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_job_notification_setting_view)
        self.workflow_common_operations.scroll_to_position_vertical(1, ScanAppWorkflowObjectIds.scan_job_notification_setting_view_scroll_bar)
        include_thumbnail = self.spice.query_item(ScanAppWorkflowObjectIds.include_thumbnail_check_option_control_model)
        assert include_thumbnail["visible"] == True, f"Option {ScanAppWorkflowObjectIds.include_thumbnail_check_option_control_model} is not visible"
        assert include_thumbnail["constrained"] == constrained, f"Option {ScanAppWorkflowObjectIds.include_thumbnail_check_option_control_model} constrained state is not {constrained}"
        if not include_thumbnail["checked"] or constrained:
            logging.info(f"Option {ScanAppWorkflowObjectIds.include_thumbnail_check_option_control_model} constrained state is {constrained}")
            include_thumbnail.mouse_click()
        if constrained:
            self.verify_constrained_message(net, "cNotificationOtherNotify")
        else:
            logging.info(f"Waiting for include thumbnail option to be checked: {checked}")
            self.wait_and_validate_property_value(include_thumbnail, "checked", checked, 10)
            assert include_thumbnail["checked"] == checked, f"Option {ScanAppWorkflowObjectIds.include_thumbnail_check_option_control_model} checked state is not {checked}"
            logging.info(f"Include thumbnail option checked state is {checked}")

    def verify_job_notification_settings(self, net, donotnotify: bool, notifyafterjobfinishes: bool, notifyonlywhenjobfail: bool):
        '''
        Verify job notification settings and include thumbnail constraint behavior
        @param donotnotify: expected state of do not notify option
        @param notifyafterjobfinishes: expected state of notify after job finishes option
        @param notifyonlywhenjobfail: expected state of notify only when job fails option
        @param include_thumbnail_checked: expected checked state of include thumbnail option
        '''
        # Verify job notification options
        self.verify_job_notification_setting(ScanAppWorkflowObjectIds.do_not_notify_option_control_model, donotnotify)
        self.verify_job_notification_setting(ScanAppWorkflowObjectIds.notify_after_job_finishes_option_control_model, notifyafterjobfinishes)
        self.verify_job_notification_setting(ScanAppWorkflowObjectIds.notify_only_when_job_fail_option_control_model, notifyonlywhenjobfail)

        # Determine if include thumbnail should be constrained
        constrained = donotnotify

        # Verify include thumbnail option
        self.verify_job_notification_include_thumbnail_setting(
            net,
            checked=not constrained,
            constrained=constrained
        )

    def change_job_notification_setting(self, job_notification_setting: str):
        '''
        Change job notification setting
        @param job_notification_setting: job notification setting
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_job_notification_setting_view)                       
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.scan_job_notification_setting_view_scroll_bar)
        option = self.spice.query_item(job_notification_setting)
        assert option["visible"] == True, f"Option {job_notification_setting} is not visible"
        assert option["checked"] == False, f"Option {job_notification_setting} checked state is not False"
        logging.info(f"Clicking on {job_notification_setting}")
        option.mouse_click()

    def click_job_notification_done_buttom(self):
        '''
        Click on done button in job notification setting screen
        '''
        done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_job_notification_done_button)
        done_button.mouse_click() 
    
    def get_page_items(self, page: int, total_items: int = 120, items_per_page: int = 30, folders_prefix_name: str =""):
        """Helper function to calculate first and last items for a given page"""
        # Calculate the indices in reverse order
        end_idx = total_items - ((page - 1) * items_per_page)
        start_idx = max(end_idx - items_per_page + 1, 1)
        
        # Swap start and end to get descending order
        folder_start = f"{folders_prefix_name}{end_idx:03d}"
        folder_end = f"{folders_prefix_name}{start_idx:03d}" 
        # logging.info(f"Page numbers: {page}, first {folder_start} last {folder_end}")
        return (folder_start, folder_end)
            
    def pagination_navigation_with_folder_order(self, folders_prefix_name: str, total_folders: int, max_items_per_page: int):
        """
        Test case to verify pagination navigation and folder visibility with folder order consideration.

        This function navigates through the USB folder selection screen, verifying folder visibility on 
        different pages (second page, last page, previous page, and first page). It dynamically calculates 
        folder IDs and ensures that folders are visible on the expected pages.

        :param folders_prefix_name: Prefix name for the folder IDs.
        :param total_folders: Total number of folders available.
        """
        logging.info("Starting pagination navigation test with folder order consideration.")

        # Wait for the USB folder layout and page indicator to load
        usb_select_folder_layout = self.spice.wait_for(UsbScanAppWorkflowObjectIds.usb_select_folder_layout)
        page_indicator = self.spice.wait_for(UsbScanAppWorkflowObjectIds.page_indicator)
        num_of_pages = page_indicator["count"]

        # Helper function to verify folder visibility
        def verify_folder_visibility(page: int, page_description: str):
            first, last = self.get_page_items(page, total_folders, max_items_per_page, folders_prefix_name)
            first_item = self.spice.wait_for(f"#{first}")
            last_item = self.spice.wait_for(f"#{last}")
            assert first_item["visible"], f"First item is not visible on {page_description}"
            assert last_item["visible"], f"Last item is not visible on {page_description}"

        # Check if the number of pages is correct
        # Step 1: Navigate to the second page and verify folder visibility
        logging.info("Navigating to the second page and verifying folder visibility.")
        self.scroll_to_bottom(usb_select_folder_layout, None)
        next_page_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_next_page)
        next_page_button.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.folder_list_screen_view)

        if not usb_select_folder_layout["atYEnd"]:
            self.scroll_to_bottom(usb_select_folder_layout, None)
        verify_folder_visibility(2, "second page")

        # Step 2: Navigate to the last page and verify folder visibility
        logging.info("Navigating to the last page and verifying folder visibility.")
        last_page_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.page_indicator_mouse_area + str(num_of_pages - 1))
        last_page_button.mouse_click()

        if not usb_select_folder_layout["atYEnd"]:
            self.scroll_to_bottom(usb_select_folder_layout, None)
        verify_folder_visibility(4, "last page")

        # Step 3: Navigate to the previous page and verify folder visibility
        logging.info("Navigating to the previous page and verifying folder visibility.")
        previous_page_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_previous_page)
        previous_page_button.mouse_click()

        if not usb_select_folder_layout["atYEnd"]:
            self.scroll_to_bottom(usb_select_folder_layout, None)

        verify_folder_visibility(3, "previous page")

        # Step 4: Navigate back to the first page and verify folder visibility
        logging.info("Navigating back to the first page and verifying folder visibility.")
        first_page_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.frist_page_indicator_mouse_area)
        first_page_button.mouse_click()

        if not usb_select_folder_layout["atYEnd"]:
            self.scroll_to_bottom(usb_select_folder_layout, None)
        verify_folder_visibility(1, "first page")

        logging.info("Pagination navigation test with folder order consideration completed successfully.")

    def save_to_usb_click_on_done_button(self):
        '''     
        UI should be in save to usb screen
        Clicks on done button
        '''
        usb_send_button = self.spice.wait_for(UsbScanAppWorkflowObjectIds.button_usb_send)
        self.spice.validate_button(usb_send_button)
        usb_send_button.mouse_click()
        
    def verify_quickset_switchable_after_main_button_enabled(self, net):
        """
        Verify quickset switchable after main button enabled
        """
        # Validate the screen buttons and ensure the main button is enabled
        self.validate_screen_buttons(net, False, UsbScanAppWorkflowObjectIds.button_usb_start, True)
        
        # Initialize the label with the default quickset name
        label = 'cMixedContent'
        
        # Verify that the selected quickset name matches the initialized label
        self.verify_selected_quickset_name(net, label)
        
        # Loop through 20 iterations to switch between two quicksets
        for i in range(20):
            if i % 2 == 0:
                # Select the "Grayscale_Lines" quickset for even iterations
                self.spice.quickset_ui.select_quickset_from_app_landing_view("Grayscale_Lines", quickset_type="usb")
                label = 'cGrayscale_Lines'
            else:
                # Select the "Mixed_Content" quickset for odd iterations
                self.spice.quickset_ui.select_quickset_from_app_landing_view("Mixed_Content", quickset_type="usb")
                label = 'cMixedContent'

        # Verify that the final selected quickset name matches the last updated label
        self.verify_selected_quickset_name(net, label)

