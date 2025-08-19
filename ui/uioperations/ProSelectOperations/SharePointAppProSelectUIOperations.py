#########################################################################################
# @file      SharePointAppProSelectUIOperations.py
# @author    Shubham Khandelwal (shubham.khandelwal@hp.com)
# @date      06-03-2021
# @brief     Implementation for all the Scan to SharePoint UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################

from time import sleep
import logging
import time
from typing import Dict
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.BaseOperations.ISharePointAppUIOperations import ISharePointAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.send.common.common import Common as ScanCommon

_logger = logging.getLogger(__name__)


class SharePointAppProSelectUIOperations(ISharePointAppUIOperations):

    SCAN_SHAREPOINT = "#a3d696df-b7ff-4d3d-9969-5cd7f18c0c92"

    SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW = "#QuickSetsView"
    SCAN_SHAREPOINT_LANDING_VIEW = "#sharepointLandingView"
    SCAN_SAVE_SUCCESSFUL_VIEW = "#folderSaveSuccessfulView"
    SCAN_PROGRESS_VIEW = "#SystemProgressView"

    SCAN_SHAREPOINT_OPTIONS = "#FolderOptionsButton"
    SCAN_SHAREPOINT_SAVE_BUTTON = "#FolderSaveButton"
    SCAN_SHAREPOINT_NOT_SETUP_OK_BUTTON = "#SPFolderNotSetUpOkButton"
    SCAN_SHAREPOINT_NOT_SETUP_VIEW = "#sharepointNotSetupView"

    SCAN_SHAREPOINT_QUICKSET_LIST_VIEW = "#QuickSetListView"
    SCAN_SHAREPOINT_QUICKSET_BUTTON = "#SharePointQuickSetSelectedButton"
    SCAN_SHAREPOINT_QUICKSET_SAVE_BUTTON = "#SharePointQuicksetSaveButton"
    SCAN_SHAREPOINT_QUICKSET_SAVE_OPTION_VIEW = "#QuickSetSaveOptionsView"
    SCAN_SHAREPOINT_AS_DEFAULT_BUTTON = "#AsDefault"
    SCAN_SHAREPOINT_KEYBOARD_PIN_PROTECTED_VIEW = "#quicksetPinKeyboardView"
    SCAN_SHAREPOINT_INVALID_PIN_VIEW = "#inCorrectPinView"
    SCAN_SHAREPOINT_INVALID_PIN_OK_BUTTON = "#OKFooterButton"
    SCAN_SHAREPOINT_SCAN_FILE_NAME_BUTTON = "#FolderScanToFileNamebutton"
    SCAN_SHAREPOINT_FILE_NAME = "#FileNameDetailButton"
    SCAN_SHAREPOINT_DETAILS_VIEW = "#sharepointDetailsView"
    COMMON_KEYBOARD_VIEW = "#commonKeyboardView"
    
    ENTER_PASSWORD_BUTTON = "#EnterPasswordButton"
    REENTER_PASSWORD_BUTTON= "#ReEnterPasswordButton"
    PDFENCRYPTIONPROMPTVIEW = "#pdfEncryptionPromptView"
    SAVE = "#Save"
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)

    # Scan to SharePoint flow operations
    # Navigation from Home screen
    def goto_scan_to_sharepoint(self):
        '''
        Navigates to Scan then SharePoint screen starting from Home screen.
        UI Flow is Home->Scan->SharePoint
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(
            self.SCAN_SHAREPOINT, "#ButtonListLayout")
        self._spice.wait_for(self.SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW)

    # Navigation in Options

    def goto_options_list_from_scan_to_sharepoint_screen(self):
        '''
        UI should be in Scan to SharePoint screen.
        Navigates to Options screen starting from SharePoint Scan screen.
        UI Flow is Scan to SharePoint->Options->(Options list)
        '''
        self.dial_common_operations.goto_item(
            self.SCAN_SHAREPOINT_OPTIONS, self.SCAN_SHAREPOINT_LANDING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_VIEW)
        logging.info("UI: At Options in Scan SharePoint Settings")

    def goto_original_size_settings_from_sharepoint_screen(self):
        '''
        UI should be in Scan to SharePoint screen.
        Navigates to Options screen starting from SharePoint Scan screen.
        UI Flow is Scan to SharePoint->Options->(Options list) > Orginal size
        '''
        self.goto_options_list_from_scan_to_sharepoint_screen()
        self.scan_operations.goto_original_size_settings()    

    def goto_landing_view_by_selecting_quickset(self, quickset_name):
        '''
        '''        
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW)
        assert self._spice.wait_for(quickset_name)
        self.dial_common_operations.goto_item(
            quickset_name, self.SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW, 180)
        # Wait for Landing screen
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_LANDING_VIEW)

    def back_to_scan_to_sharepoint_from_options_list(self):
        '''
        UI should be in Options list.
        Navigates back from Options screen to SharePoint landing view.
        '''
        self.dial_common_operations.back_button_press(
            self.scan_operations.SCAN_SETTINGS_VIEW, self.SCAN_SHAREPOINT_LANDING_VIEW, 3)

    def verify_selected_quickset_name(self, name):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check SharepointQuicksetSelected Button
        '''
        self.dial_common_operations.goto_item(
            self.SCAN_SHAREPOINT_QUICKSET_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, 180, False)
        assert self._spice.query_item(self.SCAN_SHAREPOINT_QUICKSET_BUTTON + " SpiceText")[
            "text"] == name

    def save_as_default_sharepoint_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        self.dial_common_operations.goto_item(
            self.SCAN_SHAREPOINT_QUICKSET_SAVE_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, 0, True)
        self.dial_common_operations.goto_item(
            self.SCAN_SHAREPOINT_AS_DEFAULT_BUTTON, self.SCAN_SHAREPOINT_QUICKSET_SAVE_OPTION_VIEW, 180, True)
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_LANDING_VIEW)

    def save_to_sharepoint(self, scan_more_pages: bool = False, dial_value: int = 0):
        '''
        UI should be at Scan SharePoint landing view.
        '''
        sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_SAVE_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, dial_value)
        sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "sharepoint"):
            self.scan_operations.flatbed_scan_more_pages()

    def add_page_pop_up_finish(self):
        self._spice.wait_for("#MessageLayout", timeout = 9.0)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_ADD_PAGE_FINISH_BUTTON, "#MessageLayout")

    def wait_for_sharepoint_landing_view(self):
        '''
        UI should be at Scan SharePoint landing view.
        '''
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_LANDING_VIEW, timeout = 15.0)

    def save_to_sharepoint_with_settings(self, scan_options:Dict, scan_more_pages: bool = False):
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
            'tiffcompression':'automatic',
            'orientation': 'portrait',
            'lighter_darker': 1
        }
        '''
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
        self.back_to_scan_to_sharepoint_from_options_list()
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_LANDING_VIEW, timeout = 15.0)
        sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_SAVE_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, 0)
        sleep(2)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "sharepoint"):
            self.scan_operations.flatbed_scan_more_pages()

    def verify_scan_sharepoint_not_setup(self):
        '''
        Verify Not setup message for sharepoint.
        UI flow is from Home screen and reaches not setup view.
        '''
        
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT, "#ButtonListLayout")
        self._spice.wait_for(self.SCAN_SHAREPOINT_NOT_SETUP_VIEW)
        sleep(1)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_NOT_SETUP_OK_BUTTON, "#ButtonListLayout")
        sleep(1)
    
    def save_to_sharepoint_quickset_default(self, cdm, scan_options:Dict):
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
        self.goto_scan_to_sharepoint()
        self.goto_landing_view_by_selecting_quickset("#sharepoint1")
        self.goto_options_list_from_scan_to_sharepoint_screen()
        
        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanSharePoint"
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
        self.back_to_scan_to_sharepoint_from_options_list()
        self.save_as_default_sharepoint_ticket()
    
    def enter_quickset_pin(self, pin):
        '''
        This is helper method to enter quickset pin
        UI flow Select quickset->enter pin
        '''
        self._spice.wait_for(self.SCAN_SHAREPOINT_KEYBOARD_PIN_PROTECTED_VIEW)
        self.proselect_keyboard_operations.keyboard_enter_pin(pin)
    
    def select_pin_protected_quickset(self, quickset_name):
        '''
        This is helper method to select pin quickset
        UI flow Select pin protected quickset
        '''        
        self._spice.wait_for(self.SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW)
        self.dial_common_operations.goto_item(
            quickset_name, self.SCAN_SHAREPOINT_QUICKSET_INITIAL_VIEW)
        # Wait for pin protected screen
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_KEYBOARD_PIN_PROTECTED_VIEW)

    def verify_invalid_pin_dialog_box(self):
        '''
        This is helper method to verify invalid pin dialog box
        UI flow Select INVALID PIN
        '''
        self._spice.wait_for(self.SCAN_SHAREPOINT_INVALID_PIN_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_INVALID_PIN_OK_BUTTON, self.SCAN_SHAREPOINT_INVALID_PIN_VIEW)
        # Wait for pin protected screen
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_KEYBOARD_PIN_PROTECTED_VIEW)


    def select_sharepoint_pin_quickset_from_landing(self, quickset_name):
        '''
        This is helper method to select sharepoint pin quickset
        UI flow Select QuicksetList view-> click on pin quickset
        '''
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_QUICKSET_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, 180, True)
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_QUICKSET_LIST_VIEW)
        self.dial_common_operations.goto_item(quickset_name, self.SCAN_SHAREPOINT_QUICKSET_LIST_VIEW, 180, True)
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_KEYBOARD_PIN_PROTECTED_VIEW)

    def goto_sharepoint_file_name_from_landingview(self):
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_SCAN_FILE_NAME_BUTTON, self.SCAN_SHAREPOINT_LANDING_VIEW, 0, True)
        self.dial_common_operations.goto_item(self.SCAN_SHAREPOINT_FILE_NAME, self.SCAN_SHAREPOINT_DETAILS_VIEW, 180, True)
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW)

    def select_sharepoint_file_name_empty_and_verify_error(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", 0)
        sleep(2)
        #assert self._spice.query_item("#Version1Text",4)["text"] == "Unavailable"
        assert self._spice.wait_for("#MessageLayout")
        assert self._spice.query_item("#okButton")
    
    def set_sharepoint_file_name_setting(self, filename: str):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to sharepoint filename
        '''
        assert self._spice.wait_for(self.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.proselect_keyboard_operations.keyboard_enter_text(filename)
        assert self._spice.wait_for(self.SCAN_SHAREPOINT_DETAILS_VIEW, timeout = 9.0)
    
    def back_to_scan_to_sharepoint_from_file_settings(self):
        '''
        UI should be in file settings screen - Home->Scan->Sharepoint->File Name->(File Details settings view)
        Navigates back to Sharepoint landing view.
        '''
        self.dial_common_operations.back_button_press(self.SCAN_SHAREPOINT_DETAILS_VIEW, self.SCAN_SHAREPOINT_LANDING_VIEW, index = 3)

    def send_scan_to_share_point_job(self, dial_value=0):
        # make sure in scan to sharepoint screen
        self._spice.common_operations.goto_item(self.SCAN_SHAREPOINT_SAVE_BUTTON,dial_value=dial_value)

    def select_file_by_property_text(self, text):
        """
        Select file by property text
        """
        logging.info("select the property text")
        self._spice.common_operations.goto_item(f"#{text}")

    def send_scan_to_sharepoint_job_from_menu_scan(self,dial_value=0):
        # make sure in menu scan sharepoint screen
        self._spice.common_operations.goto_item(self.SCAN_SHAREPOINT_SAVE_BUTTON,dial_value=dial_value)

    def enter_pdf_encryption_password(self, password):
        '''
        This is an auxiliary method for entering a file protection password
        UI flow Select quickset->enter password
        The two passwords must be consistent
        '''
        self._spice.common_operations.goto_item(self.ENTER_PASSWORD_BUTTON, "#pdfEncryptionPromptView")
        self.proselect_keyboard_operations.keyboard_enter_password(password)

    def reenter_pdf_encryption_password(self, password):
        '''
        This is an auxiliary method for reentering a file protection password
        UI flow Select quickset->reenter password
        The two passwords must be consistent
        '''
        self._spice.common_operations.goto_item(self.REENTER_PASSWORD_BUTTON,"#pdfEncryptionPromptView")
        self.proselect_keyboard_operations.keyboard_enter_password(password)

    def save_pdf_encryption_password(self):
        '''
        This is an auxiliary method to click save button
        '''
        self._spice.common_operations.goto_item(self.SAVE,'#pdfEncryptionPromptView')

    def check_spec_scan_to_sharepoint_application(self, net, sharepoint_path= None, sharepoint_name= None):
        logging.info("check the current screen")
        logging.info("verify the title")
        self._spice.common_operations.verify_string(net, "cScanToSharepoint","#SharePointAppApplicationStackView #TitleText")
        logging.info("check the sharepoint path about scan to path")
        actual_str = self._spice.common_operations.get_actual_str("#FolderScanToFileNamebutton")
        assert sharepoint_path in actual_str, "Error sharepoint path"

        logging.info("check the str about sharepoint name")
        self._spice.common_operations.verify_string(net, "cDefaultsAndQuickSets","#SharePointQuickSetSelected #NameText")
        
        actual_sharepoint_name_str = self._spice.common_operations.get_actual_str("#SharePointQuickSetSelected #SpiceButton")
        assert actual_sharepoint_name_str == sharepoint_name

    def check_loading_screen(self, net):
        excepted_str = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        loading_view = self._spice.wait_for("#processingscreen SpiceText", 20)
        assert excepted_str == loading_view["text"], "Failed to find loading screen"
        logging.info("loading screen is shown at scan quickset screen")
    
    def wait_for_scan_status_complete(self, time_out= 30):
        for i in range(time_out):
            time.sleep(1)
            self._spice.wait_for("#LandingLayoutView")
            #todo: update the method for complete status

    def check_screen_scan_to_sharepoint_pin_code_prompt(self):
        pin_keyboard_view = self._spice.wait_for("#quicksetPinKeyboardView", 20)
        assert pin_keyboard_view, "Failed to find pin keyboard screen"
        logging.info("pin keyboard screen is shown")

    def check_scan_to_sharepoint_delete_quickset_successfully(self,sharepoint_name):
        try:
            sharepoint_quickset_option = spice.wait_for(f"#{sharepoint_name}")
            assert not sharepoint_quickset_option, f"Fail to delete quickset <{sharepoint_name}>"
        except:
            logging.info(f"Success to delete quickset <{sharepoint_name}>")
