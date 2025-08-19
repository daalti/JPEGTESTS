#########################################################################################
# @file      UsbScanAppProSelectUIOperations.py
# @author    Anu Sebastian (anu.sebastian@hp.com)
# @date      15-02-2021
# @brief     Implementation for all the Scan to USB UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
import time
import logging
from enum import Enum
from typing import Dict
from dunetuf.ui.uioperations.BaseOperations.IUsbScanAppUIOperations import IUsbScanAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.job.job import Job
from dunetuf.cdm import CDM
from dunetuf.send.common.common import Common as ScanCommon

_logger = logging.getLogger(__name__)

class UsbScanAppProSelectUIOperations(IUsbScanAppUIOperations):
    USB_DRIVE_APP = "#USBDriveFolderGUID"
    SCAN_USB_DRIVE = "#df4a8a01-7659-486f-95d5-e125ccd1529a"

    SCAN_USB_LANDING_VIEW = "#scanUsbLandingView"
    SCAN_USB_SCAN_LOCATION = "#UsbScanButton"
    SCAN_USB_PREVIEW = "#UsbPreviewButton"
    SCAN_USB_SAVE = "#UsbSaveButton"
    SCAN_USB_OPTIONS = "#UsbOptionsButton"

    SCAN_USB_QUICKSET_LIST_VIEW = "#QuickSetListView"
    SCAN_USB_QUICKSET_BUTTON = "#UsbQuickSetSelectedButton"
    SCAN_USB_QUICKSET_SAVE_BUTTON = "#UsbQuicksetSaveButton"
    SCAN_USB_QUICKSET_SAVE_OPTION_VIEW = "#QuickSetSaveOptionsView"
    SCAN_USB_AS_DEFAULT_BUTTON = "#AsDefault"

    SCAN_PROGRESS_VIEW = "#SystemProgressView"
    SCAN_PROGRESS_CANCEL = "#SystemProgressButton"

    SCAN_USB_SAVE_SUCCESS_VIEW = "#saveSuccessfulView"
    SCAN_USB_SUCCESS_COMPLETE = "#UsbScanSuccessfulTimeout"
    SCAN_USB_SUCCESS_OK = "#UsbScanOkButton"

    SCAN_USB_DETAILS_VIEW = "#usbDetailsView"
    SCAN_USB_LOCATION = "#UsbScanLocationButton"
    SCAN_USB_FILENAME = "#UsbFileNameButton"
    SCAN_USB_FILETYPE = "#UsbFileTypeButton"

    SCAN_STATUS_ERROR_VIEW = "#statusErrorView"
    SCAN_USB_NO_FRONT_DEVICE_VIEW = "#usbAppNoFrontDeviceView"
    SCAN_USB_NO_FRONT_DEVICE_CANCEL = "#UsbNoFrontDeviceCancelButton"

    SCAN_USB_FOLDER_VIEW = "#usbSelectFolderView"
    SCAN_USB_SELECTED_DIRECTORY = "#selectedDirectory"
    SCAN_USB_SAVE_HERE = "#UsbSaveHereButton"
    COMMON_KEYBOARD_VIEW = "#commonKeyboardView"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)
        self.menu_dial_operations = MenuAppProSelectUIOperations(self._spice)

    # Scan to USB flow operations
    # Navigations from Home screen
    def goto_scan_to_usb_screen(self):
        '''
        Navigates to Scan then USB Drive screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->(Scan to USB landing view)
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.SCAN_USB_DRIVE, "#ButtonListLayout")
        time.sleep(2)
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)

    def goto_usb_drive_app(self):
        self.menu_dial_operations.home_navigation(self._spice, app_name="USB Drive",home_screen_view="#HomeScreenView")

        time.sleep(2)

        # enter the USB Drive App screen
        logging.info("Entering USB Drive App")
        usb_app = self._spice.wait_for(self.USB_DRIVE_APP)
        usb_app.mouse_click()
        time.sleep(2)

        # make sure you are in the USB Drive App
        assert self._spice.query_item("#Version1Text",0)["text"] == "USB Drive"
        logging.info("At USB Drive Screen")
        time.sleep(5)

    def goto_scan_to_usb_via_usb_drive_app(self):
        '''
        Navigates to USB Drive then Scan screen from Home screen.
        UI Flow is Home->USB Drive->Scan->(Scan to USB landing view)
        '''
        # make sure that you are in home screen
        #Uncomment once bug on homescreen activefocus DUNE-35036 is fixed

        self.goto_usb_drive_app()
        self.dial_common_operations.goto_item(self.SCAN_USB_DRIVE, "#ButtonListLayout")
        self._spice.wait_for(self.SCAN_USB_LANDING_VIEW)

    #Navigations in Scan File settings - Location, File name and File type
    def goto_usb_file_settings(self):
        '''
        UI should be in Scan to USB landing view.
        Navigates to File settings screen.
        UI Flow is USB Drive->File Name->(File Details settings view)
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_SCAN_LOCATION, self.SCAN_USB_LANDING_VIEW, dial_value = 0)
        assert self._spice.wait_for(self.SCAN_USB_DETAILS_VIEW)
        logging.info("UI: At File details screen in USB Settings")

    def goto_usb_scan_location_folders(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to scan location screen.
        UI Flow is (File Details settings view)->Scan Location->(Scan folder list)
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_LOCATION, self.SCAN_USB_DETAILS_VIEW)
        assert self._spice.wait_for(self.SCAN_USB_FOLDER_VIEW)
        logging.info("UI: At Scan location folder list screen")

    def goto_usb_file_name_setting(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to filename setting screen.
        UI Flow is (File Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_FILENAME, self.SCAN_USB_DETAILS_VIEW)
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW)
        logging.info("UI: At Scan Filename settings screen")

    def goto_usb_file_format_setting(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to fil format setting screen.
        UI Flow is (File Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_FILETYPE, self.SCAN_USB_DETAILS_VIEW)
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_FILETYPE_VIEW)
        logging.info("UI: At Scan Filename settings screen")

    def goto_file_settings_via_usb(self):
        '''
        Navigates to File settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)
        '''
        self.goto_scan_to_usb_screen()
        self.goto_usb_file_settings()

    def goto_scan_location_folders_via_usb(self):
        '''
        Navigates to scan location settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Scan Location->(Scan folder list)
        '''
        self.goto_file_settings_via_usb()
        self.goto_usb_scan_location_folders()

    def goto_file_name_setting_via_usb(self):
        '''
        UI should be in Scan to USB File settings screen starting from Home screen..
        Navigates to filename setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        self.goto_file_settings_via_usb()
        self.goto_usb_file_name_setting()

    def goto_file_format_setting_via_usb(self):
        '''
        UI should be in Scan to USB File settings screen starting from Home screen.
        Navigates to fil format setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.goto_file_settings_via_usb()
        self.goto_usb_file_format_setting()

    def back_to_scan_to_usb_from_file_settings(self):
        '''
        UI should be in file settings screen - Home->Scan->USB Drive->File Name->(File Details settings view)
        Navigates back to USB landing view.
        '''
        self.dial_common_operations.back_button_press(self.SCAN_USB_DETAILS_VIEW, self.SCAN_USB_LANDING_VIEW, index = 2)

    # Navigations in Options
    def goto_options_list_from_scan_to_usb(self):
        '''
        UI should be in Scan to USB screen.
        Navigates to Options screen starting from USB Scan screen.
        UI Flow is Scan to USB->Options->(Options list)
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_OPTIONS, self.SCAN_USB_LANDING_VIEW) #"#ButtonListLayout"
        # Wait for Options screen
        options_view = self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_VIEW, timeout = 9.0) 
        self._spice.wait_until(lambda: options_view["visible"] == True, timeout = 10.0)
        assert options_view, 'Settings not shown'
        logging.info("UI: At Options in Scan USB Settings")

    def goto_options_list_via_usb(self):
        '''
        Navigates to Options screen starting from Home screen.
        UI Flow is Home->USB Drive->Scan->Options->(Options list)
        '''
        self.goto_scan_to_usb_screen()
        self.goto_options_list_from_scan_to_usb()

    def goto_lighter_darker_settings_via_usb(self):
        '''
        Navigates to Lighter/Darker in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Lighter/Darker->(Lighter/Darker slide)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_lighter_darker_settings()

    def goto_orientation_settings_via_usb(self):
        '''
        Navigates to Orientation in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Orientation->(Orientation settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_orientation_settings()

    def goto_original_size_settings_via_usb(self):
        '''
        Navigates to Original Size in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Original Size->(Original Size settings screen)
        '''
        self.goto_options_list_via_usb()
        time.sleep(1)
        self.scan_operations.goto_original_size_settings()

    def goto_color_format_settings_via_usb(self):
        '''
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Color Format->(Color format settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_color_settings()

    def goto_quality_settings_via_usb(self):
        '''
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Quality->(Quality settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_quality_settings()

    def goto_resolution_settings_via_usb(self):
        '''
        Navigates to Resolution in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Resolution->(Resolution settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_resolution_settings()

    def goto_filetype_settings_via_usb(self):
        '''
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->File Type->(File Type settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_filetype_settings()

    def goto_sides_settings_via_usb(self):
        '''
        Navigates to Sides in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Sides-> (Sides settings screen)
        '''
        self.goto_options_list_via_usb()
        self.scan_operations.goto_sides_settings()

    def back_to_scan_to_usb_options_list_from_resolution_setting_screen(self):
        '''
        UI should be in resolution setting view
        Navigates back from resolution setting screen to scan settings view
        '''
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_SETTINGS_RESOLUTION_VIEW, self.scan_operations.SCAN_SETTINGS_VIEW, index = 3, timeout_val = 60)

    def back_to_scan_to_usb_from_options_list(self):
        '''
        UI should be in Options list.
        Navigates back from Options screen to USB landing view.
        '''
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_SETTINGS_VIEW, self.SCAN_USB_LANDING_VIEW, index = 2, timeout_val = 60)    

    def back_to_home_from_scan_to_usb(self):
        '''
        UI should be in Scan to USB screen
        Navigates back from Scan to USB screen to Scan
        '''
        self.dial_common_operations.back_button_press(self.SCAN_USB_LANDING_VIEW, self.scan_operations.SCAN_APP, index = 1, timeout_val = 60)
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_APP, "#HomeScreenView")
        logging.info("At Home Screen")

    # Scan to USB functional operations
    def set_usb_file_name_setting(self, filename: str):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to usb filename
        '''
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.proselect_keyboard_operations.keyboard_enter_text(filename)
        assert self._spice.wait_for(self.SCAN_USB_DETAILS_VIEW, timeout = 9.0)
        self.verify_filename_string(filename)
    
    def set_usb_file_name_empty_and_verify_error(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", 0)
        time.sleep(2)
        #assert self._spice.query_item("#Version1Text",4)["text"] == "Unavailable"
        assert self._spice.wait_for("#MessageLayout")
        assert self._spice.query_item("#okButton")

    def set_usb_folder_location(self, folder: str = None):
        '''
        UI should be at Scan folder list.
        Sets folder location
        '''
        '''
        #todo - Need to be reworked with folder list available
        if folder != None:
            selected = self._spice.query_item(self.SCAN_USB_SELECTED_DIRECTORY + " SpiceText")["text"]
            if selected != folder:
                folderview = self._spice.query_item(self.SCAN_USB_FOLDER_VIEW)
                start_time = time.time()
                time_spent_waiting = time.time() - start_time
                # scroll till you reach the folder passed
                while (self._spice.query_item("#CurrentAppText")["text"] != folder and time_spent_waiting < self.maxtimeout):
                    folderview.mouse_wheel(180,180)
                    time_spent_waiting = time.time() - start_time
                time.sleep(2)

                current_item = self._spice.query_item("#CurrentAppText")["text"]
                if current_item == folder:
                    self._spice.click()
                    time.sleep(2)
                selected = self._spice.query_item(self.SCAN_USB_SELECTED_DIRECTORY + " SpiceText")["text"]
            assert selected == folder
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_SAVE_HERE,self.SCAN_USB_FOLDER_VIEW)
        assert self._spice.wait_for(self.SCAN_USB_DETAILS_VIEW)

    def set_scan_to_usb_fileformat(self, filetype: str):
        '''
        UI should be on File format settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        '''
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_FILETYPE_VIEW, timeout = 9.0)
        filetype_id = self.scan_operations.filetype_dict[filetype.lower()][1]
        self.dial_common_operations.goto_item(filetype_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.SCAN_USB_DETAILS_VIEW, timeout = 9.0)

    def add_page_pop_up_finish(self):
        self._spice.wait_for("#MessageLayout", timeout = 9.0)
        self.dial_common_operations.goto_item(self.SCAN_USB_ADD_PAGE_FINISH_BUTTON, "#MessageLayout")

    def save_to_usb(self, scan_more_pages: bool = False, dial_value = 0):
        '''
        UI should be at Scan USB landing view.
        Starts save to USB drive and verifies job is successful.
        '''
        time.sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_USB_SAVE, self.SCAN_USB_LANDING_VIEW, dial_value)
        time.sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def wait_for_save_to_usb_landing_view(self):
        '''
        UI should be at Scan USB landing view.
        '''
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 15.0)

    def press_save_to_usb(self, scan_more_pages: bool = False, time_out=5):
        '''
        UI should be at Scan USB landing view.
        Starts save to USB drive.
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_SAVE, self.SCAN_USB_LANDING_VIEW)
        time.sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def cancel_scan_to_usb(self):
        '''
        UI should be at scan progress view.
        Cancel the scan to usb job.
        '''
        self._spice.wait_for(self.SCAN_PROGRESS_VIEW, timeout = 9.0)
        self.dial_common_operations.goto_item(self.SCAN_PROGRESS_CANCEL, self.SCAN_PROGRESS_VIEW)
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)
        time.sleep(2)

    def start_scan_job_usb(self):
        '''
        UI flow is from Home screen.
        Starts save to USB drive and verifies job is successful.
        '''
        self.goto_scan_to_usb_screen()
        self.save_to_usb()

    def start_scan_cancel_job_usb(self):
        '''
        Start save to USB drive and cancel job.
        UI flow is from Home screen.
        '''
        self.goto_scan_to_usb_screen()
        current_button = self._spice.query_item(self.SCAN_USB_SAVE + " SpiceText")
        current_button.mouse_click()
        assert self._spice.wait_for(self.SCAN_PROGRESS_VIEW, timeout = 9.0)
        current_button = self._spice.query_item(self.SCAN_PROGRESS_CANCEL + " SpiceText")
        current_button.mouse_click()
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)
        time.sleep(2)

    def save_to_usb_with_settings(self, scan_options:Dict, scan_more_pages: bool = False):
        '''
        Start save to USB drive with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        scan_options = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'quality': 'best',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'tiffcompression':'postTiff6'
            'orientation': 'portrait',
            'lighter_Darker': 1
        }
        '''
        self.goto_scan_to_usb_screen()
        self.goto_options_list_from_scan_to_usb()

        settings = {
            'filetype': scan_options.get('filetype', None),
            'resolution': scan_options.get('resolution', None),
            'quality': scan_options.get('quality', None),
            'sides': scan_options.get('sides', None),
            'color': scan_options.get('color', None),
            'size': scan_options.get('size', None),
            'tiffcompression': scan_options.get('tiffcompression', None),
            'orientation': scan_options.get('orientation', None),
            'lighter_darker': scan_options.get('lighter_darker', None)            
            }

        if settings['filetype'] != None:
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if settings['resolution'] != None:
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if settings['quality'] != None:
            self.scan_operations.goto_quality_settings()
            self.scan_operations.set_scan_setting('quality', settings['quality'])
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
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker = settings['lighter_darker'])
        self.back_to_scan_to_usb_from_options_list()
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 15.0)
        time.sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_USB_SAVE, self.SCAN_USB_LANDING_VIEW, 0)
        time.sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "usb"):
            self.scan_operations.flatbed_scan_more_pages()

    def goto_usb_app_landing_view_from_scan_folder(self, net):
        '''
        Verify no USB device is connected by checking for no device screen
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_DRIVE, "#ButtonListLayout")
        self._spice.wait_for(self.SCAN_USB_NO_FRONT_DEVICE_VIEW, timeout = 9.0)
        time.sleep(1)
        # verify the message content by comparing the ui content with the stringid in the specification
        self.scan_operations.verify_string(net, "#Version1Text", "cNoUSBInserted", 2)
        self.scan_operations.verify_string(net, "#Version2Text", "cInsertUSBStorage", 3)

    def press_cancel_at_no_usb_device_screen(self):
        '''
        UI should be at no USB device connected screen.
        Press Cancel button in the No front USB device screen
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_NO_FRONT_DEVICE_CANCEL, self.SCAN_USB_NO_FRONT_DEVICE_VIEW)
        self._spice.wait_for(self.scan_operations.SCAN_APP, timeout = 9.0)

    def verify_scan_to_usb_landing_view(self):
        '''
        This keyword verifies screen is in scan to usb landing view
        '''
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)

    def verify_scan_to_usb_success(self):
        '''
        This keyword verifies screen is in scan to usb success view
        '''      
        progress_view =  self._spice.wait_for(self.SCAN_USB_SAVE_SUCCESS_VIEW, timeout = 15.0)
        assert progress_view, 'Scan progress not shown'
        self._spice.wait_until(lambda: progress_view["visible"] == False, timeout = 100.0)
        assert self._spice.wait_for(self.SCAN_USB_SAVE_SUCCESS_VIEW, timeout = 12.0)
        logging.info("Inside Scan to USB Successful Screen")
        #This screen automatically goes to USB landing view after save success view.
        #Screen changes before OK button gets clicked.
        #current_button = self._spice.query_item(self.SCAN_USB_SUCCESS_OK + " SpiceText")
        #current_button.mouse_click()
        time.sleep(3)
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)

    def verify_filename_string(self, filename):
        '''This method compares the filename string with the expected string

        Args:
            UI should be in file settings landing view
            filename: expected filename string
        '''
        ui_filename_string = self._spice.query_item(self.SCAN_USB_SCAN_LOCATION + " SpiceText")["text"]
        logging.info("Filename = " + ui_filename_string)
        assert ui_filename_string.find(filename) != -1, "Filename mismatch"
    
    def verify_selected_quickset_name(self, net,  stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check UsbQuicksetSelected Button
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_QUICKSET_BUTTON, self.SCAN_USB_LANDING_VIEW, 180, False)
        assert self._spice.query_item(self.SCAN_USB_QUICKSET_BUTTON + " SpiceText")[
            "text"] == LocalizationHelper.get_string_translation(net, stringId)
    
    def save_as_default_usb_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_QUICKSET_SAVE_BUTTON, self.SCAN_USB_LANDING_VIEW, 0, True)
        self.dial_common_operations.goto_item(self.SCAN_USB_AS_DEFAULT_BUTTON, self.SCAN_USB_QUICKSET_SAVE_OPTION_VIEW, 180, True)
        assert self._spice.wait_for(self.SCAN_USB_LANDING_VIEW)
    
    def goto_usb_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        self.dial_common_operations.goto_item(self.SCAN_USB_QUICKSET_BUTTON, self.SCAN_USB_LANDING_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_USB_QUICKSET_LIST_VIEW)

    def select_usb_quickset(self, quickset_name):
        '''
        This is helper method to select usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        self.dial_common_operations.goto_item(quickset_name, self.SCAN_USB_QUICKSET_LIST_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_USB_LANDING_VIEW)

    def select_folder(self, foldername):
        self.dial_common_operations.goto_item("#"+foldername, self.SCAN_USB_FOLDER_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_USB_SAVE_HERE,self.SCAN_USB_FOLDER_VIEW)
    
    def save_to_usb_quickset_default(self, cdm, scan_options:Dict):
        '''
        Start save to USB drive with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        scan_options = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'quality': 'best',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'orientation': 'portrait',
            'lighter_darker': 1
        }
        '''
        time.sleep(2)
        self.goto_scan_to_usb_screen()
        self.goto_options_list_from_scan_to_usb()
        
        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanUsb"        
        ticket_default_response = cdm.get_raw(uri)
        assert ticket_default_response.status_code < 300
        ticket_default_body = ticket_default_response.json()

        settings = {
            'filetype': scan_options.get('filetype', None),
            'resolution': scan_options.get('resolution', None),
            'quality': scan_options.get('quality', None),
            'sides': scan_options.get('sides', None),
            'color': scan_options.get('color', None),
            'size': scan_options.get('size', None),
            'orientation': scan_options.get('orientation', None),
            'lighter_darker': scan_options.get('lighter_darker', None)
            }
        if (settings['filetype'] != None) and (scan_options["filetype"] != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["fileType"]):
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if (settings['resolution'] != None) and (scan_options["resolution"] != ticket_default_body["src"]["scan"]["resolution"]):
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if (settings['quality'] != None) and (scan_options["quality"] != ticket_default_body["src"]["scan"]["scanCaptureMode"]):
            self.scan_operations.goto_quality_settings()
            self.scan_operations.set_scan_setting('quality', settings['quality'])
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
        self.back_to_scan_to_usb_from_options_list()
        self._spice.wait_for(self.SCAN_USB_LANDING_VIEW, timeout = 9.0)
        self.save_as_default_usb_ticket()
