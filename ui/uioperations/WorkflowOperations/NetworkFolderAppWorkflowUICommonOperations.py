import logging
import sys
import time as t
from time import sleep
from enum import Enum
from typing import Dict
from dunetuf.addressBook.addressBook import *
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from dunetuf.ui.uioperations.BaseOperations.INetworkFolderAppUIOperations import INetworkFolderAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.send.common.defaultjoboptions.defaultjoboptionsutils import DefaultJobOptionsUtils, JobType
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.configuration import Configuration


class NetworkFolderAppWorkflowUICommonOperations(INetworkFolderAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

        # Scan to Network Folder flow operations
        # Navigation from Home screen

    def goto_scan_to_network_folder_screen(self,abId, recordId):
        '''
        Navigates to Scan then Network Folder screen starting from Home screen.
        UI Flow is Scan->Network Folder(Scan to Network Folder landing view)
        '''
        ##This is put as part of test so commented out in helper method.
        #self.scan_operations.goto_scan_app()
        sleep(5)
        self.workflow_common_operations.scroll_position(NetworkFolderAppWorkflowObjectIds.view_scan_screen, NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan , NetworkFolderAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , NetworkFolderAppWorkflowObjectIds.scanFolderPage_column_name , NetworkFolderAppWorkflowObjectIds.scanFolderPage_Content_Item)
        network_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        self.spice.wait_until(lambda: network_button["visible"]==True)
        network_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing,timeout=20.0)
        logging.info("UI: At Scan to network folder screen")

    def check_scan_folder_button(self):
        """
        Purpose: check if scan to folder under Scan app is visible or not.
        @return: visible
        """
        try:
            self.spice.wait_for(
                NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan)
            visible = True
        except:
            visible = False

        logging.info(
            "[check_scan_folder_button] visible={}".format(visible))
        return visible

    def goto_network_folder_scan_details(self, abId, recordId):
        '''
        Navigates to Scan Details screen starting from Home screen.
        UI Flow is Network Folder->Scan To->(Scan Details settings view)
        '''
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        current_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        logging.info("UI: At Scan details screen in Network folder Settings")

    def goto_network_folder_file_name_setting(self):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen.
        Navigates to file name setting screen.
        UI Flow is (Scan Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_options)
        current_button.mouse_click()
        sleep(2)
        self.workflow_common_operations.goto_item([NetworkFolderAppWorkflowObjectIds.row_object_filename, NetworkFolderAppWorkflowObjectIds.button_usb_scan_filename],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_common_keyboard)
        logging.info("UI: At Scan Filename settings screen")

    def goto_network_folder_filetype_setting(self, abId, recordId):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen.
        Navigates to file format setting screen.
        UI Flow is (Scan Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.goto_network_folder_scan_details(abId, recordId)
        self.scan_operations.goto_filetype_settings()
        logging.info("UI: At Scan File Format settings screen")

    def goto_file_name_setting_via_network_folder(self,abId, recordId):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen starting from Home screen.
        Navigates to filename setting screen.
        UI Flow is Home->Scan->Network Folder->File Name->(Scan Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        self.goto_network_folder_scan_details(abId, recordId)
        self.goto_network_folder_file_name_setting()

    def goto_filetype_setting_via_network_folder(self,abId, recordId):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen starting from Home screen.
        Navigates to file format setting screen.
        UI Flow is Home->Scan->Network Folder->File Type->(Scan Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.goto_network_folder_scan_details(abId, recordId)
        self.scan_operations.goto_filetype_settings()

    def back_to_scan_to_network_folder_from_file_settings(self):
        '''
        UI should be in scan details settings screen - Home->Scan->Network Folder->Options->Settings screen
        Navigates back to Network Folder landing view.
        '''
        sleep(2)
        # self.workflow_common_operations.back_button_press(NetworkFolderAppWorkflowObjectIds.menu_list_scan_settings,
        #                                               NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing, index=4, timeout_val=60)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        self.spice.validate_button(close_button)
        close_button.mouse_click()
        sleep(5)
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        # Navigation in Options

    def goto_options_list_from_scan_to_network_folder_screen(self):
        '''
        UI should be in Scan to Network Folder screen.
        Navigates to Options screen starting from Network Folder Scan screen.
        UI Flow is Scan to Network Folder->Options->(Options list)
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_options)
        self.spice.wait_until(lambda: current_button["visible"]==True)
        self.spice.wait_until(lambda: current_button["enabled"]==True)
        sleep(5)
        current_button.mouse_click()
        # Wait for Options screen
        options_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.menu_list_scan_settings)
        self.spice.wait_until(lambda: options_view["visible"] == True)
        assert options_view, 'Settings not shown'
        logging.info("UI: At Options in Scan Network Folder Settings")

    def goto_options_list_via_network_folder(self, abId, recordId):
        '''
        Navigates to Options screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->(Options list)
        '''
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.goto_options_list_from_scan_to_network_folder_screen()

    def goto_lighter_darker_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Lighter/Darker in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Lighter/Darker->(Lighter/Darker slide)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_lighter_darker_settings()

    def goto_contrast_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Contrast in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Contrast->(Contrast slide)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_contrast_settings()

    def goto_long_original_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Long original in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Long original->(Long original toggle :True/False)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_long_original_settings()

    def goto_edge_to_edge_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Edge-to-Edge in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Edge-to-Edge->(Edge-to-Edge toggle :True/False)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_edge_to_edge_settings()

    def goto_background_color_removal_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Background color removal in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Background color removal->(Background color removal toggle :True/False)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_background_color_removal_settings()

    def goto_background_noise_removal_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Background noise removal in Network Folder Options starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Background noise removal->(Background noise removal toggle :True/False)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_background_noise_removal_settings()

    def goto_orientation_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Orientation in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Orientation->(Orientation settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_orientation_settings()

    def goto_original_size_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Original Size in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Original Size->(Original Size settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_original_size_settings()

    def goto_color_format_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Color Format in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Color Format->(Color format settings screen)
        '''
        self.goto_options_list_via_network_folder( abId, recordId)
        self.scan_operations.goto_color_settings()

    def goto_filesize_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Color Format in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->FileSize->(FileSize settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_filesize_settings()

    def goto_resolution_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Resolution in Network Folder Settings screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Resolution->(Resolution settings screen)
        '''
       # self.goto_options_list_via_network_folder(abId, recordId)
        sleep(2)
        self.scan_operations.goto_resolution_settings()

    def goto_filetype_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to File Type in Network Folder Settings screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->File Type->(File Type settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_filetype_settings()

    def goto_sides_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Sides in Network Folder Settings screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Sides-> (Sides settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_sides_settings()

    def back_to_scan_to_network_folder_from_options_list(self, layer: int = 4):
        '''
        UI should be in Options list.
        Navigates back from Options screen to Network Folder landing view.
        '''
        # self.dial_common_operations.back_button_press(self.scan_operations.SCAN_SETTINGS_VIEW, self.view_scan_network_folder_landing)
        # self.workflow_common_operations.back_button_press(ScanAppWorkflowObjectIds.menu_list_scan_settings,
        #                                               NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing,layer)
        # sleep(2)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        self.spice.wait_until(lambda: close_button["visible"] == True, timeout=30.0)
        self.spice.wait_until(lambda: close_button["enabled"] == True, timeout=30.0)
        sleep(5)
        close_button.mouse_click()
        view_scan_folder_landing = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.spice.wait_until(lambda:view_scan_folder_landing["visible"])
        sleep(1)
        logging.info("UI: At Scan to network folder landing screen")

    def back_to_scan_app_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder landing screen
        UI flow is Scan Folder landing view -> Scan app landing screen
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        back_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing_back_button)
        self.spice.validate_button(back_button)
        back_button.mouse_click()

    def back_to_home_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder screen
        UI flow is scan home -> main ui
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        homeButton = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_home)
        sleep(2)
        homeButton.mouse_click()
        sleep(2)
        # make sure that you are in the home screen
        logging.info("At Home Screen")

    # Scan to network folder functional operations
    # Not modified this methode due to TODO for enter text method
    def set_network_folder_file_name_setting(self, filename: str, screen = "folder_landing_screen"):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to network folder filename
            screen:option_screen/folder_landing_screen
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_common_keyboard)
        if screen == "option_screen":
            display_name_textbox = self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings + " " + NetworkFolderAppWorkflowObjectIds.button_usb_scan_filename)
        else:
            display_name_textbox = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing + " " + NetworkFolderAppWorkflowObjectIds.button_usb_scan_filename)

        display_name_textbox.__setitem__('displayText', filename)
        sleep(2)
        keyword_ok = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        logging.info("UI: At Scan Filename settings screen")

    def set_scan_to_network_folder_filetype(self, filetype: str):
        '''
        UI should be on File type settings screen.
        Args:
            filetype: The filetype to set
            example: filetype options are: jpeg,pdf,pdfa,tiff.
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
        filetype_id = ScanAppWorkflowObjectIds.filetype_dict[filetype][1]
        self.workflow_common_operations.goto_item(filetype_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def wait_for_scan_network_landing_view(self):
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        logging.info("Inside Scan to folder Successful Screen")

    def save_to_network_folder_back_to_back(self, iteration):
        self.press_save_to_network_folder()
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        scan_resource = common_instance.scan_resource()
        job_concurrency_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrency_supported == "false" and scan_resource == "MDF":
            self.spice.scan_settings.mdf_addpage_window_alert_click_option()

    def press_save_to_network_folder(self, scan_more_pages: bool = False, wait_time=2, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True):
        # this function need change
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        sleep(7)
        # self.workflow_common_operations.goto_item(NetworkFolderAppWorkflowObjectIds.button_network_folder_send, NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        # sleep(2)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(wait_time)
        logging.info("After press save to network folder")
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()

    def add_page_pop_up_add_more(self):
        scan_add_page_add_more_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page)
        assert scan_add_page_add_more_button
        scan_add_page_add_more_button.mouse_click()

    def add_page_pop_up_finish(self):
        add_page_done_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_scan_network_folder_add_page_finish)
        add_page_done_button.mouse_click()

    def add_page_pop_up_cancel(self):
        scan_add_page_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbedduplex_cancel)
        assert scan_add_page_cancel_button
        scan_add_page_cancel_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_no)
        scan_add_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        assert scan_add_page_cancel_page_yes_button
        scan_add_page_cancel_page_yes_button.mouse_click()

    def cancel_scan_to_network_folder(self):
        '''
        UI should be at scan progress view.
        Cancel the scan to network folder job.
        '''
        scan_cancel_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_scan_progress_cancel)
        self.spice.wait_until(lambda: scan_cancel_button["enabled"] == True)
        self.spice.wait_until(lambda: scan_cancel_button["visible"] == True)
        scan_cancel_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def start_scan_job_network_folder(self, abId, recordId):
        '''
        UI flow is from Home screen.
        Starts save to Network Folder and verifies job is successful.
        '''
        self.scan_operations.goto_scan_app()
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.save_to_network_folder_and_verify()

    def start_scan_job_network_folder_with_settings(self,abId, recordId, scan_options:Dict,
                                                    scan_more_pages: bool = False):
        #imp need revisit
        '''
        Start save to Network Folder with scan settings and verify job is success
        UI flow is from network folder landing view.
        '''
        self.goto_options_list_from_scan_to_network_folder_screen()
        sleep(2)
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
            'contrast': scan_options.get('contrast', None),
            'sharpness': scan_options.get('sharpness', None),
            'backgroundCleanup': scan_options.get('backgroundCleanup', None)

        }

        if settings['filetype'] != None:
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if settings['resolution'] != None:
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_settings_resolution(settings['resolution'])
        if settings['filesize'] != None:
            self.scan_operations.goto_filesize_settings()
            self.scan_operations.set_scan_settings_filesize(settings['FileSize'])
        if settings['sides'] != None:
            self.scan_operations.goto_sides_settings()
            self.scan_operations.set_scan_settings_sides(settings['sides'])
        if settings['color'] != None:
            self.scan_operations.goto_color_settings()
            self.scan_operations.set_scan_settings_color(settings['color'])
        if settings['size'] != None:
            self.scan_operations.goto_original_size_settings()
            self.scan_operations.set_scan_settings_original_size(settings['size'])
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
            self.scan_operations.set_scan_settings_orientation(orientation=settings['orientation'])
        if settings['lighter_darker'] != None:
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker=settings['lighter_darker'])
        if settings['contrast'] != None:
            self.scan_operations.goto_contrast_settings()
            self.scan_operations.set_scan_settings_contrast(contrast=settings['contrast'])
        if settings['sharpness'] != None:
            self.scan_operations.goto_sharpness_settings()
            self.scan_operations.set_scan_settings_sharpness(sharpness=settings['sharpness'])
        if settings['backgroundCleanup'] != None:
            self.scan_operations.goto_backgroundcleanup_settings()
            self.scan_operations.set_scan_settings_backgroundcleanup(backgroundCleanup=settings['backgroundCleanup'])
        self.back_to_scan_to_network_folder_from_options_list()
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        current_button.mouse_click()
        sleep(5)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()

    def verify_scan_network_folder_setup(self):
        '''
        Verify no network folder is connected by checking for setup screen
        UI flow is from Home screen and reaches not setup view.
        '''
        self.scan_operations.goto_scan_app()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan)
        # self.workflow_common_operations.goto_item(NetworkFolderAppWorkflowObjectIds.scan_network_folder, NetworkFolderAppWorkflowObjectIds.scan_network_folder)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        current_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_folder_not_setup)

    def verify_scan_network_folder_setup_validation(self):
        '''
        UI should be at Scan Network Folder not setup view.
        Verify network folder setup using browser by checking for setup screen
        '''
        self.verify_scan_network_folder_setup()

        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_folder_not_setup)
        ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ok_setup_button)
        ok_button.mouse_click()
        sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_app)
        # self.workflow_common_operations.goto_item(NetworkFolderAppWorkflowObjectIds.button_scan_network_folder_setup_using_browser, "#ButtonListLayout")
        # self.workflow_common_operations.goto_item(NetworkFolderAppWorkflowObjectIds.button_scan_network_folder_setup_using_browser_ok, "#ButtonListLayout")
        # assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_not_setup, timeout=9.0)


    def back_button_press_scan(self, udw, screen_id, layer: int = 0, timeout_val: int = 60):
        '''
        Press back button in specific screen.
        '''

        if (self.spice.wait_for("#BackButton")["visible"] == True):
            # TODO verify the code once the back button is in position
            back_button = self.spice.wait_for("#BackButton")
            back_button.mouse_click()
        else:
            logging.info("Back button is not visible")

    def start_scan_cancel_job_network_folder(self, abId, recordId):
        '''
        Start save to Network Folder and cancel job.
        UI flow is from Home screen.
        '''
        self.scan_operations.goto_scan_app()
        self.goto_scan_to_network_folder_screen(abId, recordId)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send + " SpiceText")
        current_button.mouse_click()
        sleep(2)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_scan_progress_cancel)
        current_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def back_to_addressbook_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder screen
        Navigates back from Scan to Network Folder screen to Address Book
        '''
        self.workflow_common_operations.back_button_press(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing,
                                                      NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder_contact)

    def goto_scan_to_network_folder_option(self):
        '''
        Navigates to Scan then Network Folder screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder
        '''
        self.scan_operations.goto_scan_app()
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)


    def goto_landing_view_via_selecting_quickset(self, quickset):
        '''
        Navigates to Landingk screen starting from Quickset screen.
        UI Flow is QuicksetAddressBook -> Folder Landing View
        '''
        assert self.spice.wait_for(quickset)
        current_button = self.spice.wait_for(quickset)
        current_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def verify_selected_quickset_name(self, net, stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check FolderQuicksetSelected Button
        '''
        text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, stringId)
        text = text.split(" ")
        text = "_".join(text)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        assert self.spice.wait_for(f"#{text}")["checked"]

    def save_as_default_folder_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        # Add sleep time since it takes a while for Save button to be clickable after back from options screen.
        sleep(2)
        save_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_save)
        self.spice.validate_button(save_button)
        save_button.mouse_click()
        sleep(3)
        try:
            (self.spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_creds(True, "admin", "12345678")
            sleep(3)
        finally:
            self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_save_option_view)
            if (self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_save_as_default)["visible"] == True):
                save_as_default_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_save_as_default)
                self.spice.validate_button(save_as_default_button)
                save_as_default_button.mouse_click()
            ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ok_under_save_option_veiw)
            self.spice.validate_button(ok_button)
            ok_button.mouse_click()
            self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.save_as_default_alert_view)
            current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.save_as_default_alert_save_button)
            self.spice.validate_button(current_button)
            current_button.mouse_click()
            sleep(3)
            network_folder_landing_view =  self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
            self.spice.wait_until(lambda: network_folder_landing_view["visible"]==True)

    def is_quickset_existing(self):
        '''
        This is helper method to verify is quickset existing
        '''
        try:
            self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.default_quickset_button, 5)
            return True
        except:
            logging.info("No folder quicksets")
            return False

    def goto_folder_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click view all quickset button
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # self.workflow_common_operations.scroll_to_position_vertical(scroll_option, CopyAppWorkflowObjectIds.qs_scroll_horizontal_bar)
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return

        view_all_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_view_all)
        view_all_btn.mouse_click()

        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_list_view)

    def back_to_network_folder_from_quickset_view(self):
        '''
        UI should be in quickset list view.
        Navigates back from quickset list view to Network Folder landing view.
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_list_view)
        close_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.close_quickset_list_button)
        close_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def select_folder_quickset(self, quickset_name):
        '''
        This is helper method to select folder quickset in App Home screen.
        UI flow Select quickset
        Args: quickset_name: quickset name id, not str
        '''
        quickset_item = self.spice.wait_for(f"#{quickset_name}")
        self.spice.validate_button(quickset_item)
        quickset_item.mouse_click()
        logging.info(f"UI: Selected quickset {quickset_name}")
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        logging.info("UI: At Scan to network folder landing screen after selecting quickset")
        
    def select_quickset_and_verify_ldap_signin_error(self):
        '''
        This is helper method to verify LDAP sign in error
        UI flow Sign in -> LDAP sign in error
        '''
        self.spice.network_folder.select_folder_quickset(quickset_name = "networkFolder2")
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ldap_signin_error)
        ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ldap_signin_error_ok)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    # Quick set not done
    def save_to_folder_quickset_default(self, cdm, abId, recordId, scan_options:Dict):
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
        sleep(2)
        self.scan_operations.goto_scan_app()
        self.goto_options_list_via_network_folder(abId, recordId)

        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanNetworkFolder"
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
            'orientation': scan_options.get('orientation', None),
            'blankPageSuppression': scan_options.get('blankPageSuppression', None),
            'lighter_darker': scan_options.get('lighter_darker', None)
        }
        if (settings['filetype'] != None) and (
                scan_options["filetype"] != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["fileType"]):
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if (settings['resolution'] != None) and (
                scan_options["resolution"] != ticket_default_body["src"]["scan"]["resolution"].lower()):
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if (settings['filesize'] != None) and (
                filesize_dict.get(scan_options["filesize"]) != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["qualityAndFileSize"]):
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
        if (settings['orientation'] != None) and (
                scan_options["orientation"] != ticket_default_body["src"]["scan"]["contentOrientation"]):
            self.scan_operations.goto_orientation_settings()
            self.scan_operations.set_scan_setting('orientation', settings['orientation'])
        if (settings['blankPageSuppression'] != None) and (scan_options["blankPageSuppression"] != ticket_default_body["pipelineOptions"]["imageModifications"]["blankPageSuppressionEnabled"]):
            self.scan_operations.goto_blank_settings()
            self.scan_operations.set_scan_setting('blankPageSuppression', settings['blankPageSuppression'])
        if (settings['lighter_darker'] != None) and (
                scan_options["lighter_darker"] != ticket_default_body["pipelineOptions"]["imageModifications"][
            "exposure"]):  #
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker=settings['lighter_darker'])
        self.back_to_scan_to_network_folder_from_options_list()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.save_as_default_folder_ticket()

    def enter_quickset_pin(self, pin):
        '''
        This is helper method to enter quickset pin
        UI flow Select quickset->enter pin
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.quicksets_pin_view)
        sleep(1)
        custom_element = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.enter_pin_frame} {NetworkFolderAppWorkflowObjectIds.enter_pin_input} {NetworkFolderAppWorkflowObjectIds.scan_folder_inputtextbox}")
        self.spice.wait_until(lambda: custom_element["visible"]==True)
        custom_element.mouse_click()
        sleep(4)
        custom_element["text"] = pin
        sleep(2)

        try:
            ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
            sleep(2)
            ok_button.mouse_click()
            sleep(2)
        except  TimeoutError:
            logging.info('keypad is not displayed')

        sleep(1)
        logging.info("click the confirm button")
        button_confirm = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_pin_confirm)
        button_confirm.mouse_click()

    def select_pin_protected_quickset(self, quickset_name):
        '''
        This is helper method to select pin quickset
        UI flow Select pin protected quickset
        Args: quickset_name: quickset name id, not str
        '''
        pin_protected_quickset = self.spice.wait_for(quickset_name)
        self.spice.wait_until(lambda: pin_protected_quickset["visible"]==True)
        self.spice.wait_until(lambda: pin_protected_quickset["enabled"]==True)
        pin_protected_quickset.mouse_click()
        # Wait for Enter PIN screen
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.quicksets_pin_view)

    def select_folder_quickset_from_menu_quicksets(self, quickset_name):
        '''
        This is helper method to select quickset
        Args: quickset_name: quickset name id, not str
        '''
        folder_quickset = self.spice.wait_for(quickset_name)
        folder_quickset.mouse_click()

    def verify_invalid_pin_dialog_box(self, net):
        '''
        This is helper method to verify invalid pin dialog box
        UI flow Select INVALID PIN
        '''
        excepted_error_pin_message = LocalizationHelper.get_string_translation(net, string_id='cAccessCodeIncorrect')
        logging.info(f"Excepted error pin message is {excepted_error_pin_message}")
        pin_error = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.error_pin_message, timeout=30)
        assert pin_error
        sleep(2)
        actual_error_pin_message = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.enter_pin_frame + ' ' + NetworkFolderAppWorkflowObjectIds.error_pin_message, timeout=60)['text']
        logging.info(f"Actual error pin message is {actual_error_pin_message}")
        assert excepted_error_pin_message == actual_error_pin_message, 'The error message mismatch'

    def select_folder_pin_quickset_from_landing(self, quickset_name):
        '''
        This is helper method to select folder pin quickset
        UI flow Select QuicksetList view-> click on pin quickset
        UI flow Select View All view-> click on pin quickset
        Args: quickset_name: quickset name id, not str
        '''
        self.workflow_common_operations.scroll_to_position_vertical(0.5, NetworkFolderAppWorkflowObjectIds.scrollbar_quicksets_list_horizontal)
        view_all_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_view_all)
        view_all_button.mouse_click()
        quickset_name_button = self.spice.wait_for(quickset_name)
        quickset_name_button.mouse_click()

    # Quick set not done
    def set_folder_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_common_keyboard)
        sleep(3)
        clear_text = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.clear_text_filename)
        clear_text.mouse_click()
        sleep(2)
        keyword_ok = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)


    def verify_filename_empty_message(self, net):
        '''
        UI should be at folder constraint message screen.
        Function will verify the filename empty message.
        '''
        message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        send_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_ok_button)
        send_button.mouse_click()

    def verify_folderpath_empty_message(self, net):
        '''
        UI should be at folder constraint message screen.
        Function will verify the folder path empty message.
        '''
        message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description} #contentItem", timeout = 9.0)["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        send_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_ok_button)
        send_button.mouse_click()

    def select_folder_quickset_by_quickset_name_from_list(self, quickset_name):
        '''
        This is helper method to select folder quickset in View All screen.
        UI flow Select quickset
        Args: quickset_name: str, quickset name
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_quickset_list_view)
        quickset_name_button = self.spice.wait_for(f"#{quickset_name}")
        quickset_name_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def send_scan_job_from_menu_scan(self):
        # make sure in menu scan network folder screen
        # Add sleep time since it takes a while for Send button to be clickable after selecting created quickset.
        sleep(2)
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        current_button.mouse_click()

    def check_spec_scan_to_folder_application(self, net, folder_path=None, folder_name=None):
        #todo: need to update when DUNE-73456 is fixed.
        # self.spice.common_operations.verify_string(net, "cFolderAppHeading", "#folderLandingView #TitleText")
        # logging.info("check the folder path about scan to path")
        # actual_str = self.spice.common_operations.get_actual_str("#FolderScanToFileNamebutton")
        # assert folder_path in actual_str, "Error Folder Path"
        # logging.info("check the str about folder name")
        # self.spice.common_operations.verify_string(net, "cDefaultsAndQuickSets", "#FolderQuickSetSelected #NameText")
        # actual_folder_name_str = self.spice.common_operations.get_actual_str("#FolderQuickSetSelectedButton")
        # assert actual_folder_name_str == folder_name
        pass

    def verify_constrained_message(self, net, message):
        '''
        Verify constrained message.
        :param net, message
        '''
        sleep(2)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_constraint_message, timeout=30.0)
        self.workflow_common_operations.verify_string(net, message, f"{NetworkFolderAppWorkflowObjectIds.view_constraint_message} {NetworkFolderAppWorkflowObjectIds.constrain_description_view}")
        ok_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.ok_button_message}")
        ok_button.mouse_click()
        logging.info("Verify constrained message")

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
        elif message == 'preparingToSend':
            option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cProgressJobQueue')

        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout = 25.0)
        start_time = time()
        while time()-start_time < timeout:
           try:
               self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
               status = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.text_toastInfoText, timeout=20.0)["text"]
               logging.info("Current Toast message is : %s" % status)
               self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
           except:
               logging.info("Still finding corresponding status.")
           if option in status:
               break
        if option not in status:
           raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    def check_loading_screen(self, net):
        # excepted_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        # loading_view = self.spice.wait_for("#processingscreen SpiceText", 20)
        # assert excepted_str == loading_view["text"], "Failed to find loading screen"
        logging.info("No loading screen")

    def check_screen_scan_to_folder_pin_code_prompt(self):
        pin_keyboard_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.quicksets_pin_view, 20)
        assert pin_keyboard_view, "Failed to find pin keyboard screen"
        logging.info("pin keyboard screen is shown")

    def check_scan_to_folder_delete_quickset_successfully(self, folder_name):
        try:
            folder_quickset_option =self.spice.wait_for(f"#{folder_name}")
            assert not folder_quickset_option, f"Fail to delete quickset <{folder_name}>"
        except:
            logging.info(f"Success to delete quickset <{folder_name}>")

        #need to click ok button in menu->quickset screen when no quickset created
        try:
            logging.info("Click ok button to dismiss current screen, then next step can go back to Home screen")
            ok_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.ok_button_menu_quickset_no_quickset)
            ok_button.mouse_click()
        except:
            # no need to do anything
            pass

    def select_folder_contact_from_summarize_settings(self, abId=None, recordId=None, contact_name=None):

        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder)
        addressbookButton_icon = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)['icon']

        addressbook_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        addressbook_button.mouse_click()

        if(not addressbookButton_icon):
            contact_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_folder_addressbook_select)
            contact_button.mouse_click()

        button_select_folder = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        button_select_folder.mouse_click()

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

    def select_folder_contact_from_select_network_folder(self, abId=None, recordId=None, contact_name=None):
        button_select_addressbook = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_folder_addressbook_select)
        button_select_addressbook.mouse_click()

        button_radio_addressbook = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        #Sleep added to fix the clik in the addresbook icon, broken by a flickering seen in this window in 2-DuneHeadHead execution since Kernel update to 6.1. DUNE-225823
        sleep(1)
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

    def goto_send_to_network_from_admin_app(self):
        self.scan_operations.goto_scan_app()

        # Click Scan to Folder Button
        button_scan_to_network = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        self.spice.wait_until(lambda: button_scan_to_network["visible"]==True)
        button_scan_to_network.mouse_click()

    def select_folder_contact(self, abId, recordId, contact_name=None):
        # ob = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        # ob.mouse_click()
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.goto_options_list_from_scan_to_network_folder_screen()
        self.select_folder_contact_from_option_screen(contact_name)

    def select_folder_contact_from_option_screen(self, contact_name=None):
        """
        select folder contact from option screen, UI should in Scan To Folder options screen.
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder,
                                                   NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        addressbookButton = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)['icon']

        if(not addressbookButton):
            contact_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_folder_addressbook_select)
            contact_button.mouse_click()

        button_radio_addressbook = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_radio_select_folder)
        button_radio_addressbook.mouse_click()
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)
        if contact_name:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact.replace("folder_1", contact_name)
            row_select_folder = NetworkFolderAppWorkflowObjectIds.row_select_folder_with_contact.replace("folder_1", contact_name)
        else:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact
            row_select_folder = NetworkFolderAppWorkflowObjectIds.row_select_folder_with_contact

        sleep(3)
        self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, row_select_folder, scroll_height=86)
        button_radio_select_folder = self.spice.wait_for(button_radio_select_folder_locator)
        button_radio_select_folder.mouse_click()
        button_select = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_contact_select)
        button_select.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        sleep(3)

    def select_folder_contact_from_landing_view(self, contact_name=None):
        self.wait_for_scan_network_landing_view()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder)

        addressbook_button_obj = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        addressbookButton_icon = addressbook_button_obj['icon']

        logging.info(f"addressbookButton_icon value: {addressbookButton_icon}")

        addressbook_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select, timeout=25.0)
        sleep(2)
        self.spice.validate_button(addressbook_button)
        addressbook_button.mouse_click()

        if(not addressbookButton_icon):
            logging.info("addressbookButton_icon is not present initially")
            contact_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_folder_addressbook_select, timeout=25.0)
            self.spice.validate_button(contact_button)
            contact_button.mouse_click()


        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_address_book, timeout=45.0)
        button_radio_addressbook = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_radio_select_folder)
        self.workflow_common_operations.click_button_on_middle(button_radio_addressbook)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)
        if contact_name:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact.replace("folder_1", contact_name)
            row_select_folder = NetworkFolderAppWorkflowObjectIds.row_select_folder_with_contact.replace("folder_1", contact_name)
        else:
            button_radio_select_folder_locator = NetworkFolderAppWorkflowObjectIds.button_radio_select_folder_with_contact
            row_select_folder = NetworkFolderAppWorkflowObjectIds.row_select_folder_with_contact

        self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, row_select_folder, scroll_height=86)
        button_radio_select_folder = self.spice.wait_for(button_radio_select_folder_locator)
        button_radio_select_folder.mouse_click()
        button_select = self.spice.wait_for(
            NetworkFolderAppWorkflowObjectIds.button_contact_select)
        button_select.mouse_click()

    def check_folder_destination_path_text(self, path_text, timeout=150, wait_time=2):
        """
        check scan to folder destination path text in landing view
        """
        scan_networkfolder_landing = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.spice.wait_until(lambda: scan_networkfolder_landing["visible"]==True)
        destinationConfigured = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.destination_name, timeout=20.0)
        self.spice.wait_until(lambda: destinationConfigured["visible"]==True)

        # Wait until the text matches the expected path_text or timeout occurs
        end_time = t.time() + timeout
        while t.time() < end_time:
            logging.info(f"Current destination text: {destinationConfigured['text']}")
            if destinationConfigured["text"] == path_text:
                break
            t.sleep(wait_time)
            destinationConfigured = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.destination_name, timeout=20)

        logging.info(f"Final destination text: {destinationConfigured['text']}")
        assert destinationConfigured["text"] == path_text

    def check_folder_destination_path_text_is_set(self, net):
        """
        check scan to folder destination path text in landing view is there
        """
        timeout = 150 
        wait_time = 2
        scan_networkfolder_landing = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.spice.wait_until(lambda: scan_networkfolder_landing["visible"])
        destination_configured = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.destination_name, timeout=20.0)
        self.spice.wait_until(lambda: destination_configured["visible"])
        default_destination_path = LocalizationHelper.get_string_translation(net, "cSelectNetworkFolder")
        # Wait until the text matches the expected path_text or timeout occurs
        end_time = t.time() + timeout
        while t.time() < end_time:
            logging.info(f"Current destination text: {destination_configured['text']}")
            if destination_configured["text"] != "" and destination_configured["text"] != default_destination_path:
                break
            t.sleep(wait_time)
            destination_configured = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.destination_name, timeout=20)

        logging.info(f"Final destination text: {destination_configured['text']}")
        assert destination_configured["text"] != "" and destination_configured["text"] != default_destination_path


    def goto_local_address_from_scan_folder_landing_view(self, cdm, job):
        '''
        Go to local contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        folder_select_view = False
        responsedict = cdm.get_raw(cdm.DEFAULT_FOLDER_DESTINATION_CONFIG_ENDPOINT)
        if responsedict.status_code == 404:
           folder_select_view = False
        else:
           folder_select_view = True

        folder_contact_select_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        self.spice.validate_button(folder_contact_select_btn)
        folder_contact_select_btn.mouse_click()
        if folder_select_view == True and job.job_concurrency_supported =="true":
            button_addressbook_ntwrk_fldr = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_address_book)
            button_addressbook_ntwrk_fldr.mouse_click()

        button_addressbook_custom = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_radio_select_address_book)
        button_addressbook_custom.mouse_click()
        logging.info("Inside Contacts Screen")

    def goto_custom_address_from_scan_folder_landing_view(self, custom_address_name):
        '''
        Go to custom contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder)
        addressbookButton_icon = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)['icon']

        addressbook_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        addressbook_button.mouse_click()

        if(not addressbookButton_icon):
            contact_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_folder_addressbook_select)
            contact_button.mouse_click()

        button_addressbook_custom = self.spice.wait_for(f"#addressbook_{custom_address_name}")
        button_addressbook_custom.mouse_click()
        logging.info("Inside Contacts Screen")

    def goto_ldap_address_from_scan_to_email_landing_view(self):
        '''
        Go to ldap addressbook for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book -> LDAP
        '''
        folder_contact_select_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        self.spice.validate_button(folder_contact_select_btn)
        folder_contact_select_btn.mouse_click()

        address_book_screen = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_address_book)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)

        button_addressbook_ldap = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_addressbook_ldap)
        self.spice.wait_until(lambda: button_addressbook_ldap["visible"]==True)
        button_addressbook_ldap.mouse_click()

        ldap_address_book_screen = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)
        self.spice.validate_button(ldap_address_book_screen)
        logging.info("Inside LDAP Contacts Screen")

    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list:
        @return: contacts_name_list the contacts list should be sorted
        """
        # Wait all contacts load completed
        sleep(2)
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)

        contact_name_to_y_list = []

        for contacts_name in expect_contacts_list:
            contact = f"#radioButton_{contacts_name}Model"
            item_object_name = f"#radioButton_{contacts_name}Row"
            self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, item_object_name, scroll_height=86)
            self.spice.wait_for(item_object_name)

            y_coordinate = self.spice.wait_for(contact)["y"]
            contact_name_to_y_list.append({
                "contacts_name": contacts_name,
                "y_coordinate": y_coordinate
            })
            logging.info(f"(get_sorted_contacts_name_list) -found without scroll:{contacts_name}, {y_coordinate}")

        logging.info("(get_sorted_contacts_name_list) sorted list by y coordinate")
        contact_name_to_y_list.sort(key = lambda item: item["y_coordinate"])
        logging.info("(get_sorted_contacts_name_list) get contacts name list sorted by y coordinate")
        contacts_name_list = [i["contacts_name"] for i in contact_name_to_y_list]
        logging.info(f"(get_sorted_contacts_name_list) contacts name list after sorted by y coordinate is <{contacts_name_list}>")
        return contacts_name_list

    def select_folder_contacts_from_contacts_view(self, contact_name):
        '''
        select folder contacts from contacts view
        UI Flow is in contacts view (already select address book)
        Args: contact_name
        '''
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_addressbook_select_folder)

        contacts_locator = f"#radioButton_{contact_name}Model"
        select_radio_folder_contact = self.spice.wait_for(contacts_locator)
        select_radio_folder_contact.mouse_click()

        select_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_contact_select)
        select_button.mouse_click()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

    def select_folder_contact_from_custom_addressbook(self, abId,recordId, custom_address_name, contact_name):
        '''
        select folder contacts from custom addressbook view
        UI Flow should be in Scan app screen -> Scan to Network Folder -> click folderContactSelectButton -> select custom address book-> select contact.
        Args:
        '''
        self.goto_scan_to_network_folder_screen(abId,recordId)
        self.goto_custom_address_from_scan_folder_landing_view(custom_address_name)
        self.select_folder_contacts_from_contacts_view(contact_name)

    def goto_search_model_view(self):
        '''
        Go to search model view for search contact
        UI Flow is ldap contacts view, click to Search Button -> search model view
        '''
        logging.info("Click Search button")
        search_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_search_header_right)
        self.spice.validate_button(search_btn)
        search_btn.mouse_click()
        logging.info("Goto search model view")
        search_model_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_search_model_screen)
        self.spice.wait_until(lambda: search_model_view["visible"]==True)

    def input_search_contact_name(self, search_str):
        """
        Purpose: Enter search string.
        UI Flow is search model view, click Type here text field -> keyboard-> enter search string
        Args: search string which is provided on the test case
        """
        logging.info("Click Type here text field")
        contact_name_input_field = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.textbox_contact_name_to_field_text)
        contact_name_input_field.mouse_click()
        contact_name_input_field.__setitem__('displayText', search_str)
        key_ok  = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
        key_ok.mouse_click()

    def click_search_button_in_search_model_view(self):
        """
        Purpose: search input search string.
        UI Flow is search model view, click search button for search string
        """
        logging.info("Click Search button")
        search_btn = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_search_body_row)
        self.spice.validate_button(search_btn)
        search_btn.mouse_click()

    def check_spec_no_entries_found(self, net):
        '''
        Check spec no entries found when search no contacts
        '''
        logging.info("Check spec no entries found when search no contacts")
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_contact_integration_view)
        actual_text = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.text_view_empty_record)["text"]
        expected_text = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNoEntriesFound")
        assert actual_text == expected_text, "Failed to check spec no entries found when search no contacts"

    def back_to_select_addressbook_view_from_contacts_select_screen(self):
        """
        Back to Select Address Book screen from select contacts screen through back button.
        """
        back_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.view_contact_integration_view} {NetworkFolderAppWorkflowObjectIds.button_back}")
        back_button.mouse_click()

    def back_to_folder_landing_view_from_select_addressbook_view(self, cdm, job):
        """
        Back to Scan folder landing screen from select addressbook screen through close button.
        """
        folder_select_view = False
        responsedict = cdm.get_raw(cdm.DEFAULT_FOLDER_DESTINATION_CONFIG_ENDPOINT)
        if responsedict.status_code == 404:
           folder_select_view = False
        else:
           folder_select_view = True

        close_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.view_address_book} {NetworkFolderAppWorkflowObjectIds.button_back_close}")
        close_button.mouse_click()

        if folder_select_view == True and job.job_concurrency_supported =="true":
            back_button_from_ntwrk_fldr = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.view_folder_select_ntwrk_fldr} {NetworkFolderAppWorkflowObjectIds.button_back}")
            back_button_from_ntwrk_fldr.mouse_click()

    def wait_stateMachine_state(self, state, timeout = 10 ):
        folderLanding = self.spice.wait_for( NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing , 5 )
        self.spice.wait_until( lambda: folderLanding["state"] == state , timeout )

    def wait_mainButton_type(self, state, timeout = 10 ):
        folderLanding = self.spice.wait_for( NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing , 5 )
        self.spice.wait_until( lambda: folderLanding["mainButtonType"] == state , timeout )

    def validate_button_control(self):
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_control)

    def wait_and_validate_property_value(self, object, property, state, timeout = 10, delay = 0.25):
        self.workflow_common_operations.wait_until_property_value( object, property, state, timeout, delay = delay)
        assert object[property] == state

    def validate_screen_buttons( self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible):
        button_ids = [
            NetworkFolderAppWorkflowObjectIds.button_network_folder_send,
            NetworkFolderAppWorkflowObjectIds.button_network_folder_start,
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
                    break
                except:
                    logging.info("Button with ID %s not found", button_id)
                    continue

        if button is None:
            logging.error("Button with ID %s not found", buttonObjectId)
            raise ValueError(f"Button with ID {buttonObjectId} not found")
        #Get Eject
        ejectButton = self.spice.wait_for( NetworkFolderAppWorkflowObjectIds.eject_button,10)

        #Validate eject
        self.wait_and_validate_property_value(ejectButton, "visible", state =isEjectButtonVisible, delay = 0.01)

    @staticmethod
    def check_eject_button_operation(spice):
        eject_button =spice.wait_for(NetworkFolderAppWorkflowObjectIds.eject_button)
        eject_button.mouse_click()
        WorkflowUICommonOperations.wait_until_object_not_visible(spice, eject_button)

    def goto_content_type_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Color Format in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Content Type->(Content Type settings screen)
        '''
        self.goto_options_list_via_network_folder( abId, recordId)
        sleep(5)
        self.scan_operations.goto_content_type_settings()

    def verify_filename_read_only_enabled_screen_displayed(self, net):
        """
        This method is to check the filename read-only enabled
        :return:
        """
        current_screen = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_view)
        self.spice.wait_until(lambda:current_screen["visible"])
        logging.info("UI: Read-Only Enabled screen display")
        display_message = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_view} {NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_content_item}")["text"]
        expected_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cReadOnly')
        assert display_message == expected_message, "Filename read-only enabled message is not shown"

    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        :return:
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_view)
        logging.info("Click ok button to exit Read-Only Enabled display screen")
        ok_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_view} {NetworkFolderAppWorkflowObjectIds.scan_folder_file_name_read_only_ok_button}")
        ok_button.mouse_click()

    def goto_folder_file_name_setting_from_landing_view(self):
        """
        UI Flow is Scan to folder->Filename-> file name Keyboard
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.workflow_common_operations.scroll_to_position_vertical(0.3, NetworkFolderAppWorkflowObjectIds.scrollbar_scan_to_network_folder_landing_page)
        file_name_textbox = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_usb_scan_filename)
        file_name_textbox.mouse_click()

    def goto_select_network_folder_from_all_options(self):
        '''
        UI Flow is Scan to folder->Select->select network folder
        '''
        self.goto_options_list_from_scan_to_network_folder_screen()
        self.workflow_common_operations.goto_item([NetworkFolderAppWorkflowObjectIds.row_object_select_network_folder,
                                                   NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)

    def goto_select_network_folder(self):
        '''
        UI Flow is Scan to folder->Select->select network folder
        '''
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        select_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select, timeout=80.0)
        self.spice.wait_until(lambda: select_button["visible"]==True, timeout = 100.0)
        assert select_button["visible"] == True, "Select button is not visible"
        sleep(5)
        select_button.mouse_click()

    def select_network_folder_navigation(self, job, folder_path = "doc", save : bool = True):
        '''
        UI Flow is Scan to folder->Select->select network folder
        Args:
            folder_path: subfolder of network folder
            save: Whether or not to press the Save here button. If true, press the Save here button and exit the view.
        '''
        select_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_select_path, timeout = 60.0)
        self.spice.wait_until(lambda: select_button["visible"]==True, timeout = 60.0)
        select_button.mouse_click()

        logging.info("Go to Select Network Folder sub folder view")
        subfolder = self.spice.wait_for(f"#{folder_path}", timeout = 120.0)
        self.spice.wait_until(lambda: subfolder["visible"]==True, timeout = 60.0)
        subfolder.mouse_click()
        sleep(5)
        if(save):
            header = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_header_title, timeout=60)
            self.spice.wait_until(lambda: header['text'] == folder_path, 20)
            save_button = self.spice.wait_for("#savehereButton")
            self.spice.wait_until(lambda: save_button["visible"] == True)
            self.spice.wait_until(lambda: save_button["enabled"] == True)
            save_button.mouse_click()

    def set_folder_path(self, folder_path, save = False):
        """
        This method input the credential information of network folder
        Args:
            UI should be in network folder landing view
            folder_path: network folder path of network folder.
            save: Whether or not to press the Save button. If true, press the Save button and exit the view.
        """
        inputField = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_enter_path)
        inputField["displayText"] = folder_path

        if(save):
            save_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_path_save_button)
            save_button.mouse_click()

    def wait_for_landing_page(self, timeout = 20.0):
        sleep(5)
        landing_page = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing, timeout=timeout)
        self.spice.wait_until(lambda: landing_page['visible'] == True, timeout=timeout)

    def save_folder_path(self):
        save_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_path_save_button)
        self.spice.validate_button(save_button)
        save_button.mouse_click()

    def intput_credential_info(self, cred : dict, save: bool= False):
        """
        This method input the credential information of network folder
        Args:
            UI should be in network folder landing view
            cred: credential information of network folder. dictionary type, it contain domainName, userName and password
            save: Whether or not to press the Save button. If true, press the Save button and exit the credential view.
        """
        if(cred["domainName"]):
            inputField = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.input_domain_text_field)
            self.spice.validate_button(inputField)
            inputField.mouse_click()
            inputField["displayText"] = cred["domainName"]
            key_ok  = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
            self.spice.validate_button(key_ok)
            key_ok.mouse_click()
        landing_page = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        if(cred["userName"]):
            inputField = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.input_user_text_field)
            inputField.mouse_click()
            inputField["displayText"] = cred["userName"]
            key_ok  = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
            key_ok.mouse_click()

        if(cred["password"]):
            inputField = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.input_password_text_field)
            inputField.mouse_click()
            inputField["displayText"] = cred["password"]
            key_ok  = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_keyboard_ok)
            key_ok.mouse_click()

        if(save):
            save_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_path_credential_save_button)
            save_button.mouse_click()

    def press_cancel_button_credential_view(self):
        '''
        UI should be at Scan Network Folder input credential view.
        Cancel input credential info.
        '''
        cancel_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_path_credential_cancel_button)
        cancel_button.mouse_click()

    def press_cancel_button_select_network_folder_view(self):
        '''
        UI should be at Scan Network Folder Select network folder view.
        Cancel folder select.
        '''
        cancel_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_select_path_cancel_button)
        cancel_button.mouse_click()

    def wait_for_job_finish(self, job, net, message: str = "complete"):
        '''
        UI should be at Scan Network Folder input credential view.
        Click Done send to network folder .
        '''
        if job.job_concurrency_supported == "true":
            self.spice.scan_settings.wait_for_scan_status_toast(net, message)
        else:
            current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
            sleep(7)
            current_button.mouse_click()


    def verify_folder_dest_string(self, folder_path):
        """
        This method compares the folder destination string of network folder quickset with the expected string
        Args:
            UI should be in network folder landing view
            folder_path: expected folder destination string
        """
        # wait till verify access complete
        sleep(3)
        ui_folder_dest = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.destination_name, timeout=20.0)
        self.spice.wait_until(lambda: ui_folder_dest["visible"] == True)
        ui_folder_dest_string = ui_folder_dest["text"]
        logging.info("Filename = " + ui_folder_dest_string)
        assert ui_folder_dest_string == folder_path, "Filename mismatch"

    def verify_accessing_error_msg(self, timeout = 60, confirm: bool = True):
        """
        This method verify the accessing error message
        Args:
            UI should be in network folder landing view
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.credential_access_error, timeout)

        if(confirm):
            self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.credential_access_error_ok).mouse_click()

    def verify_folder_path_empty_message(self, timeout = 60, confirm: bool = True):
        """
        This method verify the empty constraint message
        Args:
            UI should be in network folder landing view
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_path_empty_constaint, timeout)

        if(confirm):
            self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.folder_path_empty_constaint_ok).mouse_click()

    def verify_filename_string(self, filename):
        """
        This method compares the filename string of network folder quickset with the expected string
        Args:
            UI should be in network folder landing view
            filename: expected filename string
        """
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing, timeout = 16.0)
        ui_filename_string = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_usb_scan_filename)["displayText"]
        logging.info("Filename = " + ui_filename_string)
        assert ui_filename_string == filename, "Filename mismatch"


    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.spice.scan_settings.click_expand_button()
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)["isPreviewButtonVisible"] == False

    def wait_and_click_on_middle(self, locator: str) -> None:
        """
        Waits for object in clickable state (visible and enabled) and
        it clicks on the middle of the object
        """
        # Validate for object if not exist
        object = self.spice.wait_for(locator)

        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True)
        self.spice.wait_until(lambda: object["visible"] == True)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)

    def check_folder_set_up_software_screen_shows(self):
        """
        Help method to check set up software screen shows, there is no folder contacts/quicksets
        """
        self.scan_operations.goto_scan_app()
        # Click Scan to Folder Button
        self.workflow_common_operations.scroll_position(NetworkFolderAppWorkflowObjectIds.view_scan_screen, NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan , NetworkFolderAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , NetworkFolderAppWorkflowObjectIds.scanFolderPage_column_name , NetworkFolderAppWorkflowObjectIds.scanFolderPage_Content_Item)
        button_scan_to_network = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_network_folder_home_scan + " MouseArea")
        button_scan_to_network.mouse_click()

        set_up_browser_view = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_folder_not_setup)
        self.spice.wait_until(lambda:set_up_browser_view["visible"])

    def perform_scan_folder_job_with_created_contact_and_check_file_name(self, job, contact_name, file_name, file_type, prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='', prefix_username='admin', suffix_username='admin', time_out=90):
        """
        1. Home screen -> Menu -> Scan -> Scan to Network Folder
        2. Select network folder from Local address book contact.
        3. Send email job
        4. Get preview file name from job details, and check file name
        5. Wait for job complete
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
        self.spice.scan_settings.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_menu()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.select_folder_contact_from_summarize_settings(contact_name=contact_name)

        self.press_save_to_network_folder(wait_time=0)

        job_ticket = job.get_job_details("scanNetworkFolder")
        file_name_preview_from_job = job_ticket['pipelineOptions']['sendFileAttributes']['fileNamePreview']
        logging.info(f'preview file name from job details is: {file_name_preview_from_job}')
        self.spice.quickset_ui.validate_scan_file_name(file_name_preview_from_job, file_name, file_type, prefix_type, suffix_type, custom_prefix_string, custom_suffix_string, prefix_username, suffix_username)

        job.check_job_log_by_status_and_type_cdm([{"type": "scanNetworkFolder", "status": "success"}])
        # wait for status dismiss
        sleep(7)

    def perform_scan_folder_job_with_addressbook_contacts_from_menu_scanapp(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=90):
        """
        1. Navigation to Menu -> Scan app -> Scan to Network Folder landing view
        2. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        3. Go to folder options, change options if need to change options. Back to folder landing view.
        4. Send folder job
        5. Validation scan job ticket to list options, scan common settings if changed.
        6. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        self.spice.scan_settings.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_menu()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.perform_scan_folder_job_with_addressbook_contacts(cdm, udw, net, job, contact_name, select_contacts_from, option_payload, address_book_type, custom_book_name, pages, pdf_encryption_code, time_out)


    def perform_scan_folder_job_with_addressbook_contacts_from_home_scanapp(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=120):
        """
        1. Navigation to Home -> Scan app -> Scan to Network Folder landing view
        2. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        3. Go to folder options, change options if need to change options. Back to folder landing view.
        4. Send folder job
        5. Validation scan job ticket to list options, scan common settings if changed.
        6. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        self.spice.common_operations.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_home_screen()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.perform_scan_folder_job_with_addressbook_contacts(cdm, udw, net, job, contact_name, select_contacts_from, option_payload, address_book_type, custom_book_name, pages, pdf_encryption_code, time_out)

    def perform_scan_folder_job_with_addressbook_contacts_from_home_scanapp_enterprise(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=120):
        """
        1. Navigation to Home -> Scan app -> Scan to Network Folder landing view
        2. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        3. Go to folder options, change options if need to change options. Back to folder landing view.
        4. Send folder job
        5. Validation scan job ticket to list options, scan common settings if changed.
        6. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        self.spice.common_operations.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_home_screen()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.perform_scan_folder_job_with_addressbook_contacts_enterprise(cdm, udw, net, job, contact_name, select_contacts_from, option_payload, address_book_type, custom_book_name, pages, pdf_encryption_code, time_out)

    def perform_scan_folder_job_with_addressbook_contacts(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=120):
        """
        1. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        2. Go to folder options, change options if need to change options. Back to folder landing view.
        3. Send folder job
        4. Validation scan job ticket to list options, scan common settings if changed.
        5. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        if select_contacts_from == "landing_view":
            logging.info("In folder landing view, Select Network Folder Path -> Folder Contacts")
            if address_book_type == "Local":
                self.select_folder_contact_from_summarize_settings(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        elif select_contacts_from == "options":
            logging.info("Go to folder option, Select Network Folder Path -> Folder Contacts")
            self.goto_options_list_from_scan_to_network_folder_screen()
            if address_book_type == "Local":
                logging.info("Select Address Book (Local), Click on the folder contact, back to landing view")
                self.select_folder_contact_from_option_screen(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        else:
            assert False, f"select contacts from type <{select_contacts_from}> not existing"

        if option_payload != None:
            self.goto_options_list_from_scan_to_network_folder_screen()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)
            self.back_to_scan_to_network_folder_from_options_list()
            
        if configuration.productname == "jupiter":
            self.wait_and_click_on_middle(NetworkFolderAppWorkflowObjectIds.button_network_folder_start)
        else:
            self.wait_and_click_on_middle(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()

        job_ticket = job.get_job_details("scanNetworkFolder")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if option_payload != None:
            logging.info("validation scan folder job ticket common settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, option_payload, scan_type="scanNetworkFolder")

        self.wait_for_scan_folder_job_to_complete(cdm, udw, net,job, file_type, pages, time_out)

    def perform_scan_folder_job_with_addressbook_contacts_enterprise(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=120):
        """
        1. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        2. Go to folder options, change options if need to change options. Back to folder landing view.
        3. Send folder job
        4. Validation scan job ticket to list options, scan common settings if changed.
        5. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        if select_contacts_from == "landing_view":
            logging.info("In folder landing view, Select Network Folder Path -> Folder Contacts")
            if address_book_type == "Local":
                self.select_folder_contact_from_summarize_settings(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        elif select_contacts_from == "options":
            logging.info("Go to folder option, Select Network Folder Path -> Folder Contacts")
            self.goto_options_list_from_scan_to_network_folder_screen()
            if address_book_type == "Local":
                logging.info("Select Address Book (Local), Click on the folder contact, back to landing view")
                self.select_folder_contact_from_option_screen(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        else:
            assert False, f"select contacts from type <{select_contacts_from}> not existing"

        if option_payload != None:
            self.goto_options_list_from_scan_to_network_folder_screen()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)
            self.back_to_scan_to_network_folder_from_options_list()

        if(pages > 1):
            self.goto_options_list_from_scan_to_network_folder_screen()
            self.scan_operations.select_add_more_pages_combo()
            self.back_to_scan_to_network_folder_from_options_list()

        self.save_to_network_folder_enterprise()

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()

        job_ticket = job.get_job_details("scanNetworkFolder")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if option_payload != None:
            logging.info("validation scan folder job ticket common settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, option_payload, scan_type="scanNetworkFolder")

        self.wait_for_scan_folder_job_to_complete_enterprise(cdm, udw, net,job, file_type, pages, time_out)

    def wait_for_scan_folder_job_to_complete(self, cdm, udw, net, job, file_type, pages=1, time_out=120):
        """
        wait for scan folder job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        scan_resource = common_instance.scan_resource()

        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages(type = "folder")
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
            if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"] and file_type in ["tiff", "pdf"]:
                # todo: need to add multiple page scene when bug DUNE-147017 fixed.
                self.spice.scan_settings.mdf_add_page_alert_done()
            elif configuration.productname == "jupiter" :
                for _ in range(pages-1):
                    self.validate_screen_buttons(net, False, NetworkFolderAppWorkflowObjectIds.button_network_folder_send, True)
                    udw.mainApp.ScanMedia.loadMedia("MDF")
                    sleep(2)

                self.validate_screen_buttons(net, False, NetworkFolderAppWorkflowObjectIds.button_network_folder_send, True)
                send_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send,  timeout=10.0)
                send_button.mouse_click()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "scanNetworkFolder", "status": "success"}], time_out=300)

    def wait_for_scan_folder_job_to_complete_enterprise(self, cdm, udw, net, job, file_type, pages=1, time_out=120):
        """
        wait for scan folder job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        scan_resource = common_instance.scan_resource()

        self.scan_operations.flatbed_scan_more_pages_enterprise(cdm, pages)

    def wait_for_main_action_button(self, scan_more_pages: bool = False, button_object_id = None, timeout=10):
        sleep(7)
        logging.info("Before press save to network folder button_object_id",button_object_id)
        self.spice.wait_for(button_object_id,timeout=10.0)
        current_button = self.spice.wait_for(button_object_id)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(timeout)
        logging.info("After press save to network folder")
        if scan_more_pages == True:
            self.scan_operations.flatbed_scan_more_pages()

    def start_to_network_folder(self, scan_more_pages: bool = False, wait_time=2):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        sleep(7)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_start,timeout=10.0)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_start)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(wait_time)
        logging.info("After press save to network folder")
        if scan_more_pages == True:
            self.scan_operations.flatbed_scan_more_pages()

    def save_to_network_folder(self, scan_more_pages: bool = False, wait_time=2, click_send=False):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        sleep(7)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(wait_time)
        logging.info("After press save to network folder")
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()

    def save_to_network_folder_enterprise(self, scan_more_pages: bool = False, wait_time=2):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        sleep(wait_time)
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        current_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_network_folder_send)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(wait_time)
        logging.info("After press save to network folder")
        if scan_more_pages == True:
            sleep(2)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_add_page_prompt_view)
            add_page_prompt_media_sizes_list = self.scan_operations.get_add_page_media_sizes_list_from_cdm(cdm)
            scroll_bar_step_value = 0
            media_size_id_radio_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.add_page_content_id} " + add_page_prompt_media_sizes_list[0])
            self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True)
            assert media_size_id_radio_button
            media_size_id_radio_button.mouse_click()

            self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, ScanAppWorkflowObjectIds.add_page_prompt_scroll_bar)
            self.add_page_pop_up_finish()

    def perform_scan_folder_job_with_addressbook_contacts_from_menu_scanapp_for_emulator(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=90, add_page_btn=True):
        """
        1. Navigation to Menu -> Scan app -> Scan to Network Folder landing view
        2. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        3. Go to folder options, change options if need to change options. Back to folder landing view.
        4. Send folder job
        5. Validation scan job ticket to list options, scan common settings if changed.
        6. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        self.spice.scan_settings.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_menu()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.perform_scan_folder_job_with_addressbook_contacts_for_emulator(cdm, udw, net, job, contact_name, select_contacts_from, option_payload, address_book_type, custom_book_name, pages, pdf_encryption_code, time_out, add_page_btn)

    def perform_scan_folder_job_with_addressbook_contacts_from_home_scanapp_for_emulator(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=120, add_page_btn=True):
        """
        1. Navigation to Home -> Scan app -> Scan to Network Folder landing view
        2. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        3. Go to folder options, change options if need to change options. Back to folder landing view.
        4. Send folder job
        5. Validation scan job ticket to list options, scan common settings if changed.
        6. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        self.spice.common_operations.goto_scan_app()
        self.spice.scan_settings.goto_folder_from_scanapp_at_home_screen()
        self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)

        self.perform_scan_folder_job_with_addressbook_contacts_for_emulator(cdm, udw, net, job, contact_name, select_contacts_from, option_payload, address_book_type, custom_book_name, pages, pdf_encryption_code, time_out, add_page_btn)

    def perform_scan_folder_job_with_addressbook_contacts_for_emulator(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=200, add_page_btn=True):
        """
        1. Go to folder option/landing view, Send Network Folder Path from Contacts -> Folder Contacts -> Select Local address book, Click on the folder contact, back to landing view.
        2. Go to folder options, change options if need to change options. Back to folder landing view.
        3. Send folder job
        4. Validation scan job ticket to list options, scan common settings if changed.
        5. Check scan folder job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param contact_name: contact name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
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
                'lighter&darker': 1 ,  # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
                "contrast": 1, # int
            }
        @param address_book_type: "Local"/"Custom"/"LDAP", default value is 'Local'
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        if select_contacts_from == "landing_view":
            logging.info("In folder landing view, Select Network Folder Path -> Folder Contacts")
            if address_book_type == "Local":
                self.select_folder_contact_from_summarize_settings(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        elif select_contacts_from == "options":
            logging.info("Go to folder option, Select Network Folder Path -> Folder Contacts")
            self.goto_options_list_from_scan_to_network_folder_screen()
            if address_book_type == "Local":
                logging.info("Select Address Book (Local), Click on the folder contact, back to landing view")
                self.select_folder_contact_from_option_screen(contact_name=contact_name)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        else:
            assert False, f"select contacts from type <{select_contacts_from}> not existing"

        if option_payload != None:
            self.goto_options_list_from_scan_to_network_folder_screen()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)
            self.back_to_scan_to_network_folder_from_options_list()

        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        scan_resource = common_instance.scan_resource()
        logging.info(f"scan_resource: {scan_resource}")

        if scan_resource == "ADF":
            self.save_to_network_folder(wait_time=0)  # wait_time=0 is needed to ensure job isn't already gone from the queue before calling job.get_job_details()
            if pdf_encryption_code:
                self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
                logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
                self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_save()
        elif scan_resource == "Glass":
            self.save_to_network_folder(wait_time=0)  # wait_time=0 is needed to ensure job isn't already gone from the queue before calling job.get_job_details()
            if pdf_encryption_code:
                self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
                logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
                self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_save()

            for _ in range(pages-1):
                scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page)
                self.spice.validate_button(scan_add_page_button)
                scan_add_page_button.mouse_click()
                sleep(2)

            if add_page_btn:
                    scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                    self.spice.validate_button(scan_add_page_done_button)
                    scan_add_page_done_button.mouse_click()
        elif scan_resource == "MDF":
            self.save_to_network_folder()
            if pdf_encryption_code:
                self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
                logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
                self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
                self.scan_operations.pdf_encryption_save()
            if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"] and file_type in ["tiff", "pdf"]:
                # todo: need to add multiple page scene when bug DUNE-147017 fixed.
                self.spice.scan_settings.mdf_add_page_alert_done()
            elif configuration.productname == "jupiter" :
                for _ in range(pages-1):
                    self.validate_screen_buttons(net, False, NetworkFolderAppWorkflowObjectIds.button_network_folder_send, True)
                    udw.mainApp.ScanMedia.loadMedia("MDF")
                    sleep(2)

                self.validate_screen_buttons(net, False, NetworkFolderAppWorkflowObjectIds.button_network_folder_send, True)
                self.save_to_network_folder()

        job_ticket = job.get_job_details("scanNetworkFolder")
        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if option_payload != None:
            logging.info("validation scan folder job ticket common settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, option_payload, scan_type="scanNetworkFolder")

        job.check_job_log_by_status_and_type_cdm([{"type": "scanNetworkFolder", "status": "success"}], time_out=300)

    def verify_paper_jam_message(self):
        '''
        Verify paper jam message.
        '''
        assert self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.paper_jam_window, timeout=30.0)
        hide_button = self.spice.wait_for(f"{NetworkFolderAppWorkflowObjectIds.hide_button}")
        hide_button.mouse_click()

    def goto_file_type_option_in_landing_page_and_verify_values(self, net):
        """
        Navigate to the file type option in the landing page and verify its values.
        """
        # Navigate to the file type combobox in the landing page
        self.workflow_common_operations.scroll_vertical_row_item_into_view(
            screen_id = NetworkFolderAppWorkflowObjectIds.scan_to_network_folder_landing_page_deatil_panel,
            menu_item_id = NetworkFolderAppWorkflowObjectIds.scan_folder_file_format_combobox_row,
            footer_item_id = NetworkFolderAppWorkflowObjectIds.scan_app_footer,
            top_item_id= NetworkFolderAppWorkflowObjectIds.scan_app_header,
            select_option = False
        )

        # Click the file type combobox
        file_type_combobox = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.scan_folder_file_format_combobox)
        file_type_combobox.mouse_click()

        # Verify the combobox values
        self.verify_options_combobox_with_values(net, "scan_fileFormat", "jpeg", "cDSFileTypeJpeg")

    def verify_options_combobox_with_values(self, net, option_id, value_id, expected_text):
        """
        Verify the values of a combobox.
        """
        # Construct the combobox ID and wait for it to be visible
        combobox_id = f"#{option_id}ComboBoxpopup"
        combobox = self.spice.wait_for(combobox_id)
        
        # Define the options list and the specific option value to verify
        options_list = f"#{option_id}ComboBoxpopupList"
        option_value = f"{options_list} #ComboBoxOptions{value_id}"
        scroll_bar = f"#{option_id}ComboBoxpopupverticalLayoutScrollBar"
        
        # Scroll to the specified option value in the combobox
        self.workflow_common_operations.goto_item(option_value, options_list, scrollbar_objectname=scroll_bar)
        
        # Get the text of the specified value in the combobox
        value_text = self.spice.wait_for(f"{option_value} #ComboBoxOptions{value_id}RadioButtonModel #RadioButtonText")["text"]
        
        # Get the expected translation for the value
        expected_translation = LocalizationHelper.get_string_translation(net, expected_text)
        
        # Assert that the actual value matches the expected translation
        assert value_text == expected_translation, f"Expected {expected_translation} but got {value_text}"
        
        # Click the back button to exit the combobox
        back_button = self.spice.query_item(NetworkFolderAppWorkflowObjectIds.button_back, query_index=1)
        back_button.mouse_click()

    def wait_for_verify_access_to_complete(self):
        '''
        Verify access completed message.
        '''
        try:
            verify_access_modal = self.spice.wait_for("#verifyingAccessFolder", timeout=30.0)
            self.spice.wait_until(lambda: verify_access_modal is None, timeout=30)
        except TimeoutError:
            logging.info("Verification modal did not disappear in time, checking for error dialog.")
        
        try:
            verify_failed = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.credential_access_error)
            if verify_failed:
                self.verify_accessing_error_msg()
        except TimeoutError:
            logging.info("No error dialog found, proceeding further.")
            
    def is_folder_path_edit_button_locked(self):
        """
        Checks if the folder path edit button is locked/disabled in the network folder UI.
        UI should be in the network folder landing view.
        Returns: Boolean - True if the button is locked, False otherwise.
        """
        folder_path_edit_button = self.spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select)
        return folder_path_edit_button["locked"] == True
