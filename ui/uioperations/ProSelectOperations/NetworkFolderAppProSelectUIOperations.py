#########################################################################################
# @file      NetworkFolderAppProSelectUIOperations.py
# @author    Lakshmi Narayanan (lakshmi-narayanan.v@hp.com)
# @date      06-03-2021
# @brief     Implementation for all the Scan to Network Folder UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
import time
from time import sleep

import logging
from enum import Enum
from dunetuf.addressBook.addressBook import *
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.BaseOperations.INetworkFolderAppUIOperations import INetworkFolderAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.send.common.common import Common as ScanCommon

_logger = logging.getLogger(__name__)


class NetworkFolderAppProSelectUIOperations(INetworkFolderAppUIOperations):

    scan_network_folder = "#65acca51-619d-4e29-b1d0-6414e52f908b"

    scan_select_addressbook_view = "#scanSelectAddressBookView"
    scan_addressbook_select_folder_contact_view = "#selectFolderContactView"
    scan_to_folder_quickset_address_book_view = "#QuickSetsAddressBookView"

    scan_network_folder_landing_view = "#folderLandingView"
    scan_folder_scan_to_button = "#FolderScanToFileNamebutton"
    scan_folder_options = "#FolderOptionsButton"
    scan_pdf_encryption = "#scanPdfEncryption"
    scan_settings_view = "#MenuListscanSettingsPage"
    scan_folder_save = "#FolderSaveButton"

    scan_folder_quickset_list_view = "#QuickSetListView"
    scan_folder_quickset_button = "#FolderQuickSetSelectedButton"
    scan_folder_quickset_save_button = "#FolderQuicksetSaveButton"
    scan_folder_quickset_save_option_view = "#QuickSetSaveOptionsView"
    scan_folder_save_as_default = "#AsDefault"

    scan_network_folder_details_view = "#folderDetailsView"
    scan_folder_filename_setting = "#FileNameDetailButton"
    scan_folder_filetype_setting = "#FileTypeDetailButton"

    scan_progress_view = "#SystemProgressView"
    scan_progress_cancel = "#SystemProgressButton"

    scan_folder_save_success_view = "#folderSaveSuccessfulView"
    scan_folder_success_complete = "#scanSuccessfulTimeout"
    scan_folder_success_ok = "#FolderOkButton"

    scan_network_folder_not_setup_view = "#folderSetupView"
    scan_network_folder_setup_using_software = "#FolderSetUpSoftwareButton"
    scan_network_folder_setup_using_browser = "#FolderSetUpWebBrowserButton"
    scan_network_folder_setup_using_software_ok = "#FolderSoftwareSetUpOkButton"
    scan_network_folder_setup_using_browser_ok = "#BrowserSetupOkButton"
    scan_network_folder_keyboard_pin_protected_view = "#quicksetPinKeyboardView"
    scan_network_folder_invalid_pin_view = "#inCorrectPinView"
    scan_network_folder_invalid_pin_ok_button = "#OKFooterButton"
    COMMON_KEYBOARD_VIEW = "#commonKeyboardView"

    common_keyboard_view = "#commonKeyboardView"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)
        self.dial_keyboard_operations = ProSelectKeyboardOperations(self._spice)

    # Scan to Network Folder flow operations
    # Navigation from Home screen
    def goto_scan_to_network_folder_screen(self, abId, recordId):
        '''
        Navigates to Scan then Network Folder screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder(Scan to Network Folder landing view)
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.scan_network_folder, "#ButtonListLayout")
        self._spice.wait_for(self.scan_select_addressbook_view, timeout = 13.0)
        sleep(2)
        self.dial_common_operations.goto_item("#ScanAddressBook" + abId, "#ButtonListLayout")
        sleep(2)
        self.dial_common_operations.goto_item("#FolderContact" + recordId, "#ButtonListLayout")
    #Navigates to Scan Details - Location, File name and File type
    def goto_network_folder_scan_details(self, abId, recordId):
        '''
        Navigates to Scan Details screen starting from Home screen.
        UI Flow is Network Folder->Scan To->(Scan Details settings view)
        '''        
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.dial_common_operations.goto_item(self.scan_folder_scan_to_button, self.scan_network_folder_landing_view, dial_value = 0)
        logging.info("UI: At Scan details screen in Network folder Settings")

    def goto_network_folder_file_name_setting(self):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen.
        Navigates to file name setting screen.
        UI Flow is (Scan Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        self.dial_common_operations.goto_item(self.scan_folder_filename_setting, self.scan_network_folder_details_view)
        assert self._spice.wait_for(self.common_keyboard_view, timeout = 9.0)
        logging.info("UI: At Scan Filename settings screen")

    def goto_network_folder_filetype_setting(self):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen.
        Navigates to file format setting screen.
        UI Flow is (Scan Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.dial_common_operations.goto_item(self.scan_folder_filetype_setting, self.scan_network_folder_details_view)
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_FILETYPE_VIEW, timeout = 9.0)
        logging.info("UI: At Scan File Format settings screen")

    def goto_file_name_setting_via_network_folder(self, abId, recordId):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen starting from Home screen.
        Navigates to filename setting screen.
        UI Flow is Home->Scan->Network Folder->File Name->(Scan Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        self.goto_network_folder_scan_details(abId, recordId)
        self.goto_network_folder_file_name_setting()

    def goto_filetype_setting_via_network_folder(self, abId, recordId):
        '''
        UI should be in Scan to Network Folder Scan Details settings screen starting from Home screen.
        Navigates to file format setting screen.
        UI Flow is Home->Scan->Network Folder->File Type->(Scan Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        self.goto_network_folder_scan_details(abId, recordId)
        self.goto_network_folder_filetype_setting()

    def back_to_scan_to_network_folder_from_file_settings(self):
        '''
        UI should be in scan details settings screen - Home->Scan->Network Folder->File Name->(Scan Details settings view)
        Navigates back to Network Folder landing view.
        '''
        sleep(2)
        self.dial_common_operations.back_button_press(self.scan_network_folder_details_view, self.scan_network_folder_landing_view, index = 4, timeout_val = 60)
        self._spice.wait_for(self.scan_network_folder_landing_view, timeout = 9.0)

    # Navigation in Options
    def goto_options_list_from_scan_to_network_folder_screen(self):
        '''
        UI should be in Scan to Network Folder screen.
        Navigates to Options screen starting from Network Folder Scan screen.
        UI Flow is Scan to Network Folder->Options->(Options list)
        '''
        sleep(2)
        self.dial_common_operations.goto_item(self.scan_folder_options, self.scan_network_folder_landing_view) #"#ButtonListLayout"
        # Wait for Options screen
        options_view = self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_VIEW, timeout = 9.0) 
        self._spice.wait_until(lambda: options_view["visible"] == True, timeout = 10.0)
        assert options_view, 'Settings not shown'
        logging.info("UI: At Options in Scan Network Folder Settings")

    def goto_options_list_via_network_folder(self, abId, recordId ):
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
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_color_settings()

    def goto_quality_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Color Format in Network Folder Settings starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Quality->(Quality settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
        self.scan_operations.goto_quality_settings()

    def goto_resolution_settings_via_network_folder(self, abId, recordId):
        '''
        Navigates to Resolution in Network Folder Settings screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder->Options->Resolution->(Resolution settings screen)
        '''
        self.goto_options_list_via_network_folder(abId, recordId)
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

    def back_to_scan_to_network_folder_from_options_list(self, layer:int =4):
        '''
        UI should be in Options list.
        Navigates back from Options screen to Network Folder landing view.
        '''
        #self.dial_common_operations.back_button_press(self.scan_operations.SCAN_SETTINGS_VIEW, self.scan_network_folder_landing_view)
        self.back_button_press_scan(self.scan_operations.SCAN_SETTINGS_VIEW, self.scan_network_folder_landing_view, layer)
        sleep(2)

    def back_to_home_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder screen
        Navigates back from Scan to Network Folder screen to Scan
        '''
        self.dial_common_operations.back_button_press(self.scan_network_folder_landing_view, self.scan_addressbook_select_folder_contact_view)
        self.dial_common_operations.back_button_press(self.scan_addressbook_select_folder_contact_view, self.scan_select_addressbook_view)
        self.dial_common_operations.back_button_press(self.scan_select_addressbook_view, self.scan_operations.SCAN_APP)
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_APP, "#HomeScreenView")
        logging.info("At Home Screen")

    # Scan to network folder functional operations
    def set_network_folder_file_name_setting(self, filename: str):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to network folder filename
        '''
        assert self._spice.wait_for(self.common_keyboard_view, timeout = 9.0)
        #self.dial_common_operations.keyboard_enter_text(filename)
        self.dial_keyboard_operations.keyboard_enter_text(filename)
        assert self._spice.wait_for(self.scan_network_folder_details_view, timeout = 9.0)


    def set_scan_to_network_folder_filetype(self, filetype: str):
        '''
        UI should be on File type settings screen.
        Args:
            filetype: The filetype to set
            example: filetype options are: jpeg,pdf,pdfa,tiff.
        '''
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_FILETYPE_VIEW, timeout = 9.0)
        filetype_id = self.scan_operations.filetype_dict[filetype.lower()][1]
        self.dial_common_operations.goto_item(filetype_id, "#RadioButtonListLayout")
        assert self._spice.wait_for(self.scan_settings_view, timeout = 9.0)

    def wait_for_scan_network_landing_view(self):
        sleep(4)
        assert self._spice.wait_for(self.scan_network_folder_landing_view, timeout = 15.0)
        logging.info("Inside Scan to folder Successful Screen")

    def press_save_to_network_folder(self, scan_more_pages: bool = False, dial_value:int = 0):
        '''
        UI should be at Scan Network Folder landing view.
        Starts save to Network Folder.
        '''
        sleep(2)
        self.dial_common_operations.goto_item(self.scan_folder_save, self.scan_network_folder_landing_view, dial_value)
        sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()
    
    def add_page_pop_up_finish(self):
        self._spice.wait_for("#MessageLayout", timeout = 9.0)
        self.dial_common_operations.goto_item(self.scan_network_folder_add_page_finish_button, "#MessageLayout")

    def cancel_scan_to_network_folder(self):
        '''
        UI should be at scan progress view.
        Cancel the scan to network folder job.
        '''
        self._spice.wait_for(self.scan_progress_view, timeout = 9.0)
        self.dial_common_operations.goto_item(self.scan_progress_cancel, self.scan_network_folder_landing_view)
        sleep(3)

    def start_scan_job_network_folder(self, abId, recordId):
        '''
        UI flow is from Home screen.
        Starts save to Network Folder and verifies job is successful.
        '''
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.save_to_network_folder_and_verify()

    def start_scan_job_network_folder_with_settings(self, abId, recordId, scan_options:Dict, scan_more_pages: bool = False):
        '''
        Start save to Network Folder with scan settings and verify job is success
        UI flow is from Home screen.
        '''
        self.goto_options_list_via_network_folder(abId, recordId)

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
            self.set_scan_to_network_folder_filetype(settings['filetype'])
        if settings['resolution'] != None:
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_settings_resolution(settings['resolution'])
        if settings['quality'] != None:
            self.scan_operations.goto_quality_settings()
            self.scan_operations.set_scan_settings_quality(settings['quality'])
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
            self.scan_operations.set_scan_settings_orientation(orientation = settings['orientation'])
        if settings['lighter_darker'] != None:
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker = settings['lighter_darker'])
        self.back_to_scan_to_network_folder_from_options_list()
        assert self._spice.wait_for(self.scan_network_folder_landing_view, timeout = 15.0)
        sleep(2)
        self.dial_common_operations.goto_item(self.scan_folder_save, self.scan_network_folder_landing_view, 0)
        sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "folder"):
            self.scan_operations.flatbed_scan_more_pages()
        
    def verify_scan_network_folder_setup(self):
        '''
        Verify no network folder is connected by checking for setup screen
        UI flow is from Home screen and reaches not setup view.
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.scan_network_folder, "#ButtonListLayout")
        self._spice.wait_for(self.scan_network_folder_not_setup_view, timeout = 9.0)

    def verify_scan_network_folder_software_setup(self):
        '''
        UI should be at Scan Network Folder not setup view.
        Verify network folder setup using software by checking for setup screen
        '''
        self.verify_scan_network_folder_setup()
        sleep(2)
        self.dial_common_operations.goto_item(self.scan_network_folder_setup_using_software, "#ButtonListLayout")
        self.dial_common_operations.goto_item(self.scan_network_folder_setup_using_software_ok, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_network_folder_not_setup_view, timeout = 9.0)

    def verify_scan_network_folder_browser_setup(self):
        '''
        UI should be at Scan Network Folder not setup view.
        Verify network folder setup using browser by checking for setup screen
        '''
        self.verify_scan_network_folder_setup()
        self.dial_common_operations.goto_item(self.scan_network_folder_setup_using_browser, "#ButtonListLayout")
        self.dial_common_operations.goto_item(self.scan_network_folder_setup_using_browser_ok, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_network_folder_not_setup_view, timeout = 9.0)

    def back_button_press_scan(self, udw, screen_id, layer:int=0, timeout_val: int = 60):
        '''
        Press back button in specific screen.
        Args:
          screen_id: Screen object id
          layer: UI layer of back button
          timeout_val: Time out for scrolling
        '''
        current_screen = self._spice.wait_for(screen_id)
        start_time = time()
        time_spent_waiting = time() - start_time
        while (self._spice.query_item("#BackButton", layer)["activeFocus"] == False and time_spent_waiting < timeout_val):
            current_screen.mouse_wheel(0,0)
            time_spent_waiting = time() - start_time
        sleep(1)
        assert self._spice.query_item("#BackButton", layer)["activeFocus"] == True, "Back button not in active focus"
        current_button = self._spice.query_item("#BackButton SpiceText", layer)
        current_button.mouse_click()
        sleep(1)

    def start_scan_cancel_job_network_folder(self, abId, recordId):
        '''
        Start save to Network Folder and cancel job.
        UI flow is from Home screen.        
        '''

        self.goto_scan_to_network_folder_screen(abId, recordId)
        sleep(2)
        self.dial_common_operations.goto_item(self.scan_folder_save, self.scan_network_folder_landing_view)
        current_button = self._spice.query_item(self.scan_progress_cancel)
        current_button.mouse_click()
        sleep(2)
    
    def back_to_addressbook_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder screen
        Navigates back from Scan to Network Folder screen to Address Book
        '''
        self.dial_common_operations.back_button_press(self.scan_network_folder_landing_view, self.scan_addressbook_select_folder_contact_view)
    
    def goto_scan_to_network_folder_option(self):
        '''
        Navigates to Scan then Network Folder screen starting from Home screen.
        UI Flow is Home->Scan->Network Folder
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.scan_network_folder, "#ButtonListLayout")
    
    def goto_landing_view_via_selecting_quickset(self, quickset):
        '''
        Navigates to Landingk screen starting from Quickset screen.
        UI Flow is QuicksetAddressBook -> Folder Landing View
        '''
        assert self._spice.wait_for(self.scan_to_folder_quickset_address_book_view)
        assert self._spice.wait_for(quickset)
        self.dial_common_operations.goto_item(quickset, self.scan_to_folder_quickset_address_book_view, 180, True)
        assert self._spice.wait_for(self.scan_network_folder_landing_view)
    

    def verify_selected_quickset_name(self, net,  stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check FolderQuicksetSelected Button
        '''
        self.dial_common_operations.goto_item(self.scan_folder_quickset_button, self.scan_network_folder_landing_view, 180, False)
        assert self._spice.query_item(self.scan_folder_quickset_button + " SpiceText")[
            "text"] == LocalizationHelper.get_string_translation(net, stringId)
    
    def save_as_default_folder_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        self.dial_common_operations.goto_item(self.scan_folder_quickset_save_button, self.scan_network_folder_landing_view, 0, True)
        self.dial_common_operations.goto_item(self.scan_folder_save_as_default, self.scan_folder_quickset_save_option_view, 180, True)
        assert self._spice.wait_for(self.scan_network_folder_landing_view)
    
    def goto_folder_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        self.dial_common_operations.goto_item(self.scan_folder_quickset_button, self.scan_network_folder_landing_view, 180, True)
        self._spice.wait_for(self.scan_folder_quickset_list_view)

    def select_folder_quickset(self, quickset_name):
        '''
        This is helper method to select usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        self.dial_common_operations.goto_item(quickset_name, self.scan_folder_quickset_list_view, 180, True)
        self._spice.wait_for(self.scan_network_folder_landing_view)
    
    def save_to_folder_quickset_default(self, cdm, abId, recordId, scan_options:Dict):
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
        sleep(2)
        self.goto_scan_to_network_folder_screen(abId, recordId)
        self.goto_options_list_via_network_folder(abId, recordId)
        
        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanNetworkFolder"
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
        self.back_to_scan_to_network_folder_from_options_list()
        assert self._spice.wait_for(self.scan_network_folder_landing_view)
        self.save_as_default_folder_ticket()

    def enter_quickset_pin(self, pin):
        '''
        This is helper method to enter quickset pin
        UI flow Select quickset->enter pin
        '''
        self._spice.wait_for(self.scan_network_folder_keyboard_pin_protected_view)
        self.dial_keyboard_operations.keyboard_enter_pin(pin)
    
    def select_pin_protected_quickset(self, quickset_name):
        '''
        This is helper method to select pin quickset
        UI flow Select pin protected quickset
        '''      
        self._spice.wait_for(self.scan_to_folder_quickset_address_book_view)
        self.dial_common_operations.goto_item(
            quickset_name, self.scan_to_folder_quickset_address_book_view)
        # Wait for pin protected screen
        assert self._spice.wait_for(self.scan_network_folder_keyboard_pin_protected_view)

    def verify_invalid_pin_dialog_box(self):
        '''
        This is helper method to verify invalid pin dialog box
        UI flow Select INVALID PIN
        '''
        self._spice.wait_for(self.scan_network_folder_invalid_pin_view)
        self.dial_common_operations.goto_item(self.scan_network_folder_invalid_pin_ok_button, self.scan_network_folder_invalid_pin_view)
        # Wait for pin protected screen
        assert self._spice.wait_for(self.scan_network_folder_keyboard_pin_protected_view)


    def select_folder_pin_quickset_from_landing(self, quickset_name):
        '''
        This is helper method to select folder pin quickset
        UI flow Select QuicksetList view-> click on pin quickset
        '''
        self.dial_common_operations.goto_item(self.scan_folder_quickset_button, self.scan_network_folder_landing_view, 180, True)
        assert self._spice.wait_for(self.scan_folder_quickset_list_view)
        self.dial_common_operations.goto_item(quickset_name, self.scan_folder_quickset_list_view, 180, True)
        assert self._spice.wait_for(self.scan_network_folder_keyboard_pin_protected_view)
    
    def set_folder_file_name_empty_and_verify_error(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.dial_keyboard_operations.keyboard_clear_text()
        self.dial_keyboard_operations.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", 0)
        sleep(2)
        #assert self._spice.query_item("#Version1Text",4)["text"] == "Unavailable"
        assert self._spice.wait_for("#MessageLayout")
        assert self._spice.query_item("#okButton")
    
    def select_quickset_by_folder_name(self, folder_name):
        """
        Select file by property text
        """
        logging.info("select the property text")
        self._spice.common_operations.goto_item(f"#{folder_name}")

    def select_quickset_by_folder_name_from_home_scan(self, folder_name):
        """
        Select file by property text
        """
        logging.info("select the property text")
        self._spice.common_operations.goto_item(f"#{folder_name}", "#ButtonListLayout")

    def send_scan_job_from_menu_scan(self):
        # make sure in menu scan network folder screen
        self._spice.common_operations.goto_item(self.scan_folder_save)

    def check_spec_scan_to_folder_application(self, net, folder_path= None, folder_name= None):
        logging.info("check the current screen")
        logging.info("verify the title")
        self._spice.common_operations.verify_string(net, "cFolderAppHeading","#folderLandingView #TitleText")
        logging.info("check the folder path about scan to path")
        actual_str = self._spice.common_operations.get_actual_str("#FolderScanToFileNamebutton")
        assert folder_path in actual_str, "Error Folder Path"

        logging.info("check the str about folder name")
        self._spice.common_operations.verify_string(net, "cDefaultsAndQuickSets","#FolderQuickSetSelected #NameText")
        
        actual_folder_name_str = self._spice.common_operations.get_actual_str("#FolderQuickSetSelectedButton")
        assert actual_folder_name_str == folder_name

    def wait_for_scan_status_complete(self, time_out= 30):
        logging.info("check the status after scan")
        self._spice.wait_for("#ToastSystemToastStackView", 20)
        #todo: update the method for complete status

    def check_loading_screen(self, net):
        excepted_str = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        loading_view = self._spice.wait_for("#processingscreen SpiceText", 20)
        assert excepted_str == loading_view["text"], "Failed to find loading screen"
        logging.info("loading screen is shown at scan quickset screen")

    def check_screen_scan_to_folder_pin_code_prompt(self):
        pin_keyboard_view = self._spice.wait_for("#quicksetPinKeyboardView", 20)
        assert pin_keyboard_view, "Failed to find pin keyboard screen"
        logging.info("pin keyboard screen is shown")
    
    def check_scan_to_folder_delete_quickset_successfully(self,folder_name):
        try:
            folder_quickset_option = spice.wait_for(f"#{folder_name}")
            assert not folder_quickset_option, f"Fail to delete quickset <{folder_name}>"
        except:
            logging.info(f"Success to delete quickset <{folder_name}>")
