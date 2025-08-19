#########################################################################################
# @file      SharePointAppWorkflowUICommonOperations.py
# @author    Bandna Kumari (bandna.kumari@hp.com)
# @date      10-02-2022
# @brief     Implementation for all the Scan to SharePoint UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################

import logging
import sys
from time import sleep
from enum import Enum
from typing import Dict
from dunetuf.addressBook.addressBook import *
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from dunetuf.ui.uioperations.BaseOperations.ISharePointAppUIOperations import ISharePointAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
import time
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.servers.sharepointserver import SharepointServer

class SharePointAppWorkflowUICommonOperations(ISharePointAppUIOperations):
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    # Scan to SharePoint flow operations
    # Navigation from Home screen
    def goto_scan_to_sharepoint(self):
        '''
        Navigates to Scan then SharePoint screen starting from Home screen.
        UI Flow is Home->Scan->SharePoint
        '''
        self.scan_operations.goto_scan_app()
        sleep(3)
        if self.spice.uitype == "Workflow2":
            self.spice.home_operations.home_navigation(SharePointAppWorkflowObjectIds.scan_sharepoint_app,MenuAppWorkflowObjectIds.home_folder_view)
        else:
            self.workflow_common_operations.scroll_position(SharePointAppWorkflowObjectIds.view_scan_screen, SharePointAppWorkflowObjectIds.scan_sharepoint_app, SharePointAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , SharePointAppWorkflowObjectIds.scanFolderPage_column_name , SharePointAppWorkflowObjectIds.scanFolderPage_Content_Item)
        self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app + " MouseArea")
        current_button.mouse_click() 
        sleep(3)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_initial_list,timeout=16.0)
        logging.info("UI: At Scan to sharepoint listview screen")

    def check_sharepoint_button(self):
        """
        Purpose: check if scan to sharepoint under Scan app is visible or not.
        @return: visible
        """
        try:
            self.spice.wait_for(
                SharePointAppWorkflowObjectIds.scan_sharepoint_app)
            visible = True
        except:
            visible = False
        logging.info(
            "[check_sharepoint_button] visible={}".format(visible))
        return visible

    # Navigation in Options
    def goto_options_list_from_scan_to_sharepoint_screen(self):
        '''
        UI should be in Scan to SharePoint screen.
        Navigates to Options screen starting from SharePoint Scan screen.
        UI Flow is Scan to SharePoint->Options->(Options list)
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, timeout=40.0)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_sharepoint_options, timeout=35.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(3)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.menu_list_scan_settings, timeout=40.0)
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
        UI should navigate to sharepoint landing view by clicking a quickset from Quickset initial list.
        '''        
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_initial_list)
        assert self.spice.wait_for(quickset_name)
        current_button = self.spice.wait_for(quickset_name)
        current_button.mouse_click()
        # Wait for Landing screen
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, timeout = 16.0)
        sleep(5)
        
    def goto_landing_view_by_selecting_quickset_and_sign_in(self, quickset_name):
        '''
        UI should navigate to sharepoint landing view by clicking a quickset from Quickset initial list.
        '''        
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_initial_list)
        assert self.spice.wait_for(quickset_name)
        current_button = self.spice.wait_for(quickset_name)
        current_button.mouse_click()
        try:
            (self.spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_creds(True, "admin", "12345678")
        # Wait for Landing screen
        finally:
            assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, timeout = 16.0)

    def back_to_scan_to_sharepoint_from_options_list(self):
        '''
        UI should be in Options list.
        Navigates back from Options screen to SharePoint landing view.
        '''
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        self.spice.validate_button(close_button)
        close_button.mouse_click()
        sleep(4)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        sleep(1)
        logging.info("UI: At Scan to sharepoint landing screen")

    def verify_selected_quickset_name(self, name):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check SharepointQuicksetSelected Button
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        assert self.spice.wait_for(f"#{name}")
        sleep(2)
        assert self.spice.wait_for(f"#{name} {SharePointAppWorkflowObjectIds.radiobutton_spiceradiobutton}")["checked"] == True

    def save_as_default_sharepoint_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        sharepoint_quickset_save_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.save_as_default_button)
        sharepoint_quickset_save_button.mouse_click()
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
            self.spice.wait_for(SharePointAppWorkflowObjectIds.view_menu_save_options)
            if (self.spice.wait_for(SharePointAppWorkflowObjectIds.sharepoint_quickset_as_defaults_option)["visible"] == True):
                current_option = self.spice.wait_for(SharePointAppWorkflowObjectIds.sharepoint_quickset_as_defaults_option)
                current_option.mouse_click()
            current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.ok_under_save_option_veiw)
            current_button.mouse_click()
            self.spice.wait_for(SharePointAppWorkflowObjectIds.save_as_default_alert_view)
            sleep(2)
            save_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.save_as_default_alert_save_button)
            save_button.mouse_click()
            sleep(3)
            assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)

    def save_to_sharepoint(self, scan_more_pages: bool = False, dial_value: int = 0, wait_time = 5):
        '''
        UI should be at Scan SharePoint landing view.
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        time.sleep(2)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "sharepoint"):
            self.scan_operations.flatbed_scan_more_pages()

    def save_to_sharepoint_enterprise(self, scan_more_pages: bool = False, dial_value: int = 0, wait_time = 5):
        '''
        UI should be at Scan SharePoint landing view.
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send, timeout = 25.0)
        # wait for element to be clickable state
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout=30.0)
        self.spice.wait_until(lambda: current_button["enabled"] == True, timeout=30.0)
        time.sleep(2)
        current_button.mouse_click()
        time.sleep(wait_time)
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

    def add_page_pop_up_finish(self):
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_sharepoint_add_more_page)
        sleep(4)
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
        current_button.mouse_click()

    def add_page_pop_up_cancel(self):
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.button_sharepoint_add_more_finish)
        scan_add_page_flatbed_duplex_cancel_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_sharepoint_add_more_finish)
        scan_add_page_flatbed_duplex_cancel_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_no)
        scan_add_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        assert scan_add_page_cancel_page_yes_button
        scan_add_page_cancel_page_yes_button.mouse_click()

    def wait_for_sharepoint_landing_view(self):
        '''
        UI should be at Scan SharePoint landing view.
        '''
        sharepoint_landing_view = self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        self.spice.wait_until(lambda: sharepoint_landing_view["visible"] == True)

    def save_to_sharepoint_with_settings(self, scan_options:Dict, scan_more_pages: bool = False, wait_time = 5):
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
            'tiffcompression':'automatic',
            'orientation': 'portrait',
            'lighter_darker': 1,
            'blankPageSuppression': true
        }
        '''
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
            'blankPageSuppression': scan_options.get('blankPageSuppression', None)
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
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker = settings['lighter_darker'])
        if settings['blankPageSuppression'] != None:
            self.scan_operations.goto_blank_settings()
            self.scan_operations.set_scan_setting('blankPageSuppression', settings['blankPageSuppression'])

        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.back_to_scan_to_sharepoint_from_options_list()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        current_button.mouse_click()
        sleep(wait_time) 
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "sharepoint"):
            self.scan_operations.flatbed_scan_more_pages()
            
    def do_sharepoint_send(self):
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        time.sleep(2)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        self.spice.validate_button(current_button)
        current_button.mouse_click()                    

    def verify_scan_sharepoint_not_setup(self):
        '''
        Verify Not setup message for sharepoint.
        UI flow is from Home screen and reaches not setup view.
        '''
        if self.spice.is_HomeScreen():
            self.scan_operations.goto_scan_app()
        self.scan_operations.goto_sharepoint_from_scanapp_at_home_screen()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepointapp_not_setup)
        sleep(1)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_not_setup_ok)
        current_button.mouse_click()
        sleep(1)

    def verify_scan_sharepoint_setup_page(self):
        '''
        Verify setup message for sharepoint.
        UI flow is from Home screen and reaches setup view.
        '''
        self.scan_operations.goto_scan_app()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app)
        current_button.mouse_click()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_not_setup)
    
    def save_to_sharepoint_quickset_default(self, cdm, scan_options:Dict):
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
        self.goto_scan_to_sharepoint()
        self.goto_landing_view_by_selecting_quickset("#sharepoint1")
        self.goto_options_list_from_scan_to_sharepoint_screen()
        
        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanSharePoint"
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
            'lighter_darker': scan_options.get('lighter_darker', None)
            }
        if (settings['filetype'] != None) and (scan_options["filetype"] != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["fileType"]):
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if (settings['resolution'] != None) and (scan_options["resolution"] != ticket_default_body["src"]["scan"]["resolution"].lower()):
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_setting('resolution', settings['resolution'])
        if (settings['filesize'] != None) and (filesize_dict.get(scan_options["filesize"]) != ticket_default_body["pipelineOptions"]["sendFileAttributes"]["qualityAndFileSize"]):
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
        self.back_to_scan_to_sharepoint_from_options_list()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        self.save_as_default_sharepoint_ticket()

    def enter_quickset_pin(self, pin, index=0):
        '''
        This is helper method to enter quickset pin
        UI flow Select quickset->enter pin
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.quicksets_pin_view)
        sleep(2)
        custom_element = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.enter_pin_field} {SharePointAppWorkflowObjectIds.enter_pin_frame} {SharePointAppWorkflowObjectIds.scan_sharepoint_enterpin_inputtextbox}")
        custom_element.mouse_click()
        sleep(4)

        try:
            # enter pin with keyboard
            num_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_numeric_keypad_switch)
            num_button.mouse_click()
            sleep(1)
            for i in  range(len(pin)):
                num = pin[i]
                logging.info(num)
                key = self.spice.wait_for("#key" + num)
                key.mouse_click()
            ok_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_keyboard_ok)
            sleep(2)
            ok_button.mouse_click()
            sleep(2)
        except  TimeoutError:
            logging.info('keypad is not displayed')

        sleep(1)
        logging.info("click the confirm button")
        button_confirm = self.spice.query_item(SharePointAppWorkflowObjectIds.button_keyboard_pin_confirm, index)
        self.spice.validate_button(button_confirm)
        button_confirm.mouse_click()

    def select_pin_protected_quickset(self, quickset_name):
        '''
        This is helper method to select pin quickset
        UI flow Select pin protected quickset
        '''
        assert self.spice.wait_for(quickset_name)
        current_button = self.spice.wait_for(quickset_name)
        current_button.mouse_click()
        # Wait for pin protected screen
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_pin_protected)

    def select_non_pin_protected_quickset(self, quickset_name):
        '''
        This is helper method to select non pin quickset
        UI flow Select non pin protected quickset
        ''' 
        assert self.spice.wait_for(quickset_name)
        current_button = self.spice.wait_for(quickset_name + " SpiceText[visible=true]")
        current_button.mouse_click()

    def verify_invalid_pin_dialog_box(self):
        '''
        This is helper method to verify invalid pin dialog box
        UI flow Select INVALID PIN
        '''
        # Wait for pin protected screen
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_pin_protected)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_pin_protected_helper_message)
        actual_error_msg = self.workflow_common_operations.get_actual_str(SharePointAppWorkflowObjectIds.scan_sharepoint_pin_protected_helper_message)
        assert actual_error_msg == "The access code is incorrect."
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_pin_protected)

    def select_sharepoint_pin_quickset_from_landing(self, quickset_name):
        '''
        This is helper method to select sharepoint pin quickset
        UI flow Select QuicksetList viewAll-> click on pin quickset
        UI flow Select View All view-> click on pin quickset
        Args: quickset_name: quickset name id, not str
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        sleep(3)
        quickset_name_button = self.spice.wait_for(f"{quickset_name} {SharePointAppWorkflowObjectIds.radiobutton_spiceradiobutton}")
        quickset_name_button.mouse_click()

    def goto_sharepoint_quickset_view_all(self):
        '''
        This is helper method to goto sharepoint quickset
        UI flow Select Landing-> click view all quickset button
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        view_all_btn = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_view_all)
        view_all_btn.mouse_click()

        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_list_view)

    def select_sharepoint_quickset_by_quickset_name_from_list(self, quickset_name):
        '''
        This is helper method to select sharepoint quickset in View All screen.
        UI flow Select quickset
        Args: quickset_name: str, quickset name
        '''
        self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_list_view)
        quickset_name_button = self.spice.wait_for(f"#{quickset_name}")
        quickset_name_button.mouse_click()
        #Commenting wait_for because if sharepoint quickset has PIN, it will show PIN entry screen instead of landing view
        #self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)

    def goto_sharepoint_file_name_from_landingview(self):
        '''
        UI should be at Sharepoint Landing view.
        Click on file name input text Keyboard should be shown in the UI.
        '''
        self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        self.workflow_common_operations.scroll_to_position_vertical(0.3, SharePointAppWorkflowObjectIds.scrollbar_scan_to_sharepoint_landing_page)
        current_textfield = self.spice.wait_for(SharePointAppWorkflowObjectIds.file_name_text_field_scan_sharepoint)
        current_textfield.mouse_click()

    def select_sharepoint_file_name_empty_and_verify_error(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.common_keyboard_view)
        logging.info("Inside enter filename keyboard view")
        self.workflow_common_operations.goto_item([SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_row, SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_inputtext], 
                                                    SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing,
                                                    scrolling_value=0.3,
                                                    scrollbar_objectname=SharePointAppWorkflowObjectIds.scrollbar_scan_to_sharepoint_landing_page)
        sleep(2)
        file_name_textbox = self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_inputtext)
        file_name_textbox.__setitem__('inputText', "")
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        current_button.mouse_click()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_constraint_message)
        #verify text on constraint view pending
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.constraint_message_ok_button)
        current_button.mouse_click()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
    
    def set_sharepoint_file_name_setting(self, filename: str):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to sharepoint filename
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_common_keyboard)
        logging.info("Inside enter filename keyboard view")
        file_name_textbox = self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_inputtext)
        file_name_textbox.__setitem__('displayText', filename)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)

    def back_to_scan_to_sharepoint_from_file_settings(self):
        '''
        UI should be in file settings screen - Home->Scan->Sharepoint->File Name->(File Details settings view)
        Navigates back to Sharepoint landing view.
        '''
        # NA for workflow. No such view.
        # self.workflow_common_operations.back_button_press(SharePointAppWorkflowObjectIds.scan_sharepoint_details_view, SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, index = 3)

    def send_scan_to_share_point_job(self, dial_value=0):
        # make sure in scan to sharepoint screen
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        current_button.mouse_click()

    def select_sharepoint_quickset_from_landing(self, quickset_name):
        '''
        This is helper method to select sharepoint quickset from Scan to SharePoint landing screen
        Args: quickset_name: quickset name id, not str
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        quickset_name_button = self.spice.wait_for(f"{quickset_name} {SharePointAppWorkflowObjectIds.radiobutton_spiceradiobutton}")
        quickset_name_button.mouse_click()
        logging.info("Need some time for Send button to be active")
        sleep(3)

    def send_scan_to_sharepoint_job_from_menu_scan(self,dial_value=0):
        # make sure in menu scan sharepoint screen
        current_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_scan_sharepoint_send)
        current_button.mouse_click()

    def enter_pdf_encryption_password(self, password):
        '''
        This is an auxiliary method for entering a file protection password
        UI flow Select quickset->enter password
        The two passwords must be consistent
        '''
        self.scan_operations.pdf_encryption_enter_password(password)

    def reenter_pdf_encryption_password(self, password):
        '''
        This is an auxiliary method for reentering a file protection password
        UI flow Select quickset->reenter password
        The two passwords must be consistent
        '''
        self.scan_operations.pdf_encryption_reenter_password(password)

    def save_pdf_encryption_password(self):
        '''
        This is an auxiliary method to click save button
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_pdf_encryption)
        self.scan_operations.pdf_encryption_save()
        
    def check_spec_scan_to_sharepoint_application(self, net, sharepoint_path= None, sharepoint_name= None):
        logging.info("check the current screen")
        logging.info("verify the title")
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        #self.workflow_common_operations.verify_string(net, "cScanToSharepoint", SharePointAppWorkflowObjectIds.scan_sharepoint_landing_header)
        logging.info("check the sharepoint path about scan to path")
        actual_str = self.workflow_common_operations.get_actual_str(SharePointAppWorkflowObjectIds.scan_sharepoint_landing_sharepointpath)
        assert sharepoint_path in actual_str, "Error sharepoint path"
        logging.info("check the str about sharepoint name")
        #no defaults and quicksets title text on selene workflow
        #self.workflow_common_operations.verify_string(net, "cDefaultsAndQuickSets","#SharePointQuickSetSelected #NameText")
        assert self.spice.wait_for(f"#{sharepoint_name}")
        #commented below line because of SpiceRadioButton object index is changing every time.
        #assert self.spice.wait_for(f"#{sharepoint_name} {SharePointAppWorkflowObjectIds.radiobutton_spiceradiobutton}")["checked"]

    def check_loading_screen(self, net):
        # No loading screen
        logging.info(net+" No loading screen")
    
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

        self.spice.wait_for(SharePointAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout = 20.0)
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                self.spice.wait_for(SharePointAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
                status = self.spice.wait_for(SharePointAppWorkflowObjectIds.text_toastInfoText)["text"]
                logging.info("Current Toast message is : %s" % status)
                self.spice.wait_for(SharePointAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
            except:
                logging.info("Still finding corresponding status.")
            if option in status:
                break
        if option not in status:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    def check_screen_scan_to_sharepoint_pin_code_prompt(self):
        pin_view = self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_pin_protected)
        assert pin_view, "Failed to find pin Protected screen"
        logging.info("pin protected screen is shown")

    def check_scan_to_sharepoint_delete_quickset_successfully(self,sharepoint_name):
        try:
            sharepoint_quickset_option = spice.wait_for(f"#{sharepoint_name}")
            assert not sharepoint_quickset_option, f"Fail to delete quickset <{sharepoint_name}>"
        except:
            logging.info(f"Success to delete quickset <{sharepoint_name}>")
    
    def verify_filename_string(self, filename):
        """
        This method compares the filename string of sharepoint quickset with the expected string
        Args:
            UI should be in share point landing view
            filename: expected filename string
        """
        # Wait for Landing screen
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, timeout = 16.0)
        ui_filename_string = self.spice.wait_for(SharePointAppWorkflowObjectIds.file_name_text_field_scan_sharepoint)["displayText"]
        logging.info("Filename = " + ui_filename_string)
        assert ui_filename_string == filename, "Filename mismatch"

    def cancel_scan_to_sharepoint(self):
        """
        UI should be at scan progress view.
        Cancel the scan to sharepoint job.
        :return:
        """
        sharepoint_scan_cancel_button = self.spice.wait_for(SharePointAppWorkflowObjectIds.button_cancel_scan_sharepoint_job)
        sharepoint_scan_cancel_button.mouse_click()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)

    def verify_filename_read_only_enabled_screen_displayed(self, net):
        """
        This method is to check the filename read-only enabled
        :return:
        """
        current_screen = self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_view, timeout=9)
        self.spice.wait_until(lambda: current_screen["visible"])
        logging.info("UI: Read-Only Enabled screen display")
        display_message = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_view} {SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_content_item}")["text"]
        expected_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cReadOnly')
        assert display_message == expected_message, "Filename read-only enabled message is not shown"

    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        :return:
        """
        self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_view)
        logging.info("Click ok button to exit Read-Only Enabled display screen")
        ok_button = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_view} {SharePointAppWorkflowObjectIds.scan_sharepoint_file_name_read_only_ok_button}")
        ok_button.mouse_click()

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        self.spice.scan_settings.click_expand_button()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)["isPreviewButtonVisible"] == False
        

    def perform_scan_to_sharepoint_job(self,cdm, net, job, ews_quicksets_app, scan_path,  ews_sharepoint_settings=None, ews_qs_settings=None, pin=None, ui_changed_setting=None, pdf_encryption_code=None, pages=1,media_source_type=None, time_out=120):
        """
        1. Create sharepoint quickset.
        2. Navigation to Scan to Sharepoint quickset select screen with corresponding scan_path.  
        3. Select sharepoint quickset, make sure quickset is checked.
        4. Go to sharepoint options, change options if need to change options in UI. Back to sharepoint landing view.
        5. Send sharepoint job
        6. Validation scan job ticket scan common settings list options if ews/ui options changed.
        7. Check scan sharepoint job complete.
        @param cdm
        @param net
        @param job
        @param ews_quicksets_app
        @param scan_path: 'homeApp'/'menuApp'/'quicksetApp'
        @param ews_qs_settings: sharepoint quickset settings. If no quickset ews option change, None, create default sharepoint quickset.
        @param ews_sharepoint_settings: ews sharepoint settings. If no ews option change, None, use default sharepoint option.
        @param ui_changed_setting: scan common settings. If no ui option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            ui_changed_setting = {
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
        @param pin: pin for quickset if set this option
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param pages: set it when scan from Glass if scan Multi page
        @param media_source_type: 'adf'/'flatbed', set it if want to check media source type
        @param time_out: timeout to wait for job finish
        """
        sharepoint_server = SharepointServer()
        server_details = sharepoint_server.get_sharepoint_details()
        default_sharepoint_setting = {
            "name" : "sharepoint_quickset", # string
            "sharepoint_path": server_details[0]["sharepoint_details"][0]["read_write"]["Kerberose"], # string
            "sign_in_method": "following_credentials",  # value from key of signin_method_option_dict
            "windows_domain": server_details[0]["domainname"], # string
            "user_name": server_details[0]["username"], # string
            "password": server_details[0]["password"] # string
        }

        final_sharepoint_payload = {}
        sharepoint_payload = {}
        sharepoint_payload.update(default_sharepoint_setting)
        if ews_sharepoint_settings != None:
            final_sharepoint_payload.update(ews_sharepoint_settings)
        if ews_qs_settings != None:
            sharepoint_payload.update(ews_qs_settings)
            final_sharepoint_payload.update(ews_qs_settings)

        logging.info(f'create sharepoint quickset {sharepoint_payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets("sharepoint", sharepoint_payload)
        quickset_name = sharepoint_payload["name"]

        if scan_path == "homeApp":
            logging.info("Go to sharepoint from Home -> Scan -> Scan to Sharepoint")
            self.workflow_common_operations.goto_scan_app()
            self.scan_operations.goto_sharepoint_from_scanapp_at_home_screen()
        elif scan_path=='menuApp':
            logging.info("Go to sharepoint from Menu -> Scan -> Scan to Sharepoint")
            self.scan_operations.goto_scan_app() 
            self.scan_operations.goto_sharepoint_from_scanapp_at_menu()
        elif scan_path=='quicksetApp':
            logging.info("Go to sharepoint from Menu -> Quickset -> Scan -> Scan to Sharepoint")
            raise Exception("Need to implement function goto sharepoint from quickset app")
    
        qs_button = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_list_view} #{quickset_name}")
        self.spice.validate_button(qs_button)
        qs_button.mouse_click()
        if pin:
            self.check_screen_scan_to_sharepoint_pin_code_prompt()
            self.enter_quickset_pin(pin)

        self.wait_for_sharepoint_landing_view()
        quickset_item = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing} #{quickset_name}")
        self.spice.wait_until(lambda: quickset_item["checked"])

        if ui_changed_setting != None:
            final_sharepoint_payload.update(ui_changed_setting)
            self.goto_options_list_from_scan_to_sharepoint_screen()
            logging.info("change sharepoint scan common setting options in UI")
            self.scan_operations.set_scan_option_settings(ui_changed_setting)
            self.back_to_scan_to_sharepoint_from_options_list()

        self.save_to_sharepoint(wait_time=0)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()
            self.wait_for_sharepoint_landing_view()
        
        job_ticket = job.get_job_details("scanSharePoint")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if media_source_type != None:
            assert job_ticket['src']['scan']['mediaSource'] == media_source_type, "Media Source setting is mismatched"

        if final_sharepoint_payload != None:
            logging.info("validation scan sharepoint job ticket common change settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, final_sharepoint_payload, scan_type="scanSharePoint")

        self.wait_for_scan_quickset_job_to_complete(job,  file_type, pages=pages, time_out=time_out)

    def perform_scan_to_sharepoint_job_enterprise(self,cdm, net, job, ews_quicksets_app, scan_path,  ews_sharepoint_settings=None, ews_qs_settings=None, pin=None, ui_changed_setting=None, pdf_encryption_code=None, pages=1,media_source_type=None, time_out=120):
        """
        1. Create sharepoint quickset.
        2. Navigation to Scan to Sharepoint quickset select screen with corresponding scan_path.  
        3. Select sharepoint quickset, make sure quickset is checked.
        4. Go to sharepoint options, change options if need to change options in UI. Back to sharepoint landing view.
        5. Send sharepoint job
        6. Validation scan job ticket scan common settings list options if ews/ui options changed.
        7. Check scan sharepoint job complete.
        @param cdm
        @param net
        @param job
        @param ews_quicksets_app
        @param scan_path: 'homeApp'/'menuApp'/'quicksetApp'
        @param ews_qs_settings: sharepoint quickset settings. If no quickset ews option change, None, create default sharepoint quickset.
        @param ews_sharepoint_settings: ews sharepoint settings. If no ews option change, None, use default sharepoint option.
        @param ui_changed_setting: scan common settings. If no ui option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            ui_changed_setting = {
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
        @param pin: pin for quickset if set this option
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param pages: set it when scan from Glass if scan Multi page
        @param media_source_type: 'adf'/'flatbed', set it if want to check media source type
        @param time_out: timeout to wait for job finish
        """
        sharepoint_server = SharepointServer()
        server_details = sharepoint_server.get_sharepoint_details()
        default_sharepoint_setting = {
            "name" : "sharepoint_quickset", # string
            "sharepoint_path": server_details[0]["sharepoint_details"][0]["read_write"]["Kerberose"], # string
            "sign_in_method": "following_credentials",  # value from key of signin_method_option_dict
            "windows_domain": server_details[0]["domainname"], # string
            "user_name": server_details[0]["username"], # string
            "password": server_details[0]["password"] # string
        }

        final_sharepoint_payload = {}
        sharepoint_payload = {}
        sharepoint_payload.update(default_sharepoint_setting)
        if ews_sharepoint_settings != None:
            final_sharepoint_payload.update(ews_sharepoint_settings)
        if ews_qs_settings != None:
            sharepoint_payload.update(ews_qs_settings)
            final_sharepoint_payload.update(ews_qs_settings)

        logging.info(f'create sharepoint quickset {sharepoint_payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets("sharepoint", sharepoint_payload)
        quickset_name = sharepoint_payload["name"]

        if scan_path == "homeApp":
            logging.info("Go to sharepoint from Home -> Scan -> Scan to Sharepoint")
            self.workflow_common_operations.goto_scan_app()
            self.scan_operations.goto_sharepoint_from_scanapp_at_home_screen()
        elif scan_path=='menuApp':
            logging.info("Go to sharepoint from Menu -> Scan -> Scan to Sharepoint")
            self.scan_operations.goto_scan_app() 
            self.scan_operations.goto_sharepoint_from_scanapp_at_menu()
        elif scan_path=='quicksetApp':
            logging.info("Go to sharepoint from Menu -> Quickset -> Scan -> Scan to Sharepoint")
            raise Exception("Need to implement function goto sharepoint from quickset app")
    
        qs_button = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_list_view} #{quickset_name}")
        self.spice.validate_button(qs_button)
        qs_button.mouse_click()
        if pin:
            self.check_screen_scan_to_sharepoint_pin_code_prompt()
            self.enter_quickset_pin(pin)

        self.wait_for_sharepoint_landing_view()
        quickset_item = self.spice.wait_for(f"{SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing} #{quickset_name}")
        self.spice.wait_until(lambda: quickset_item["checked"])

        if ui_changed_setting != None:
            final_sharepoint_payload.update(ui_changed_setting)
            self.goto_options_list_from_scan_to_sharepoint_screen()
            logging.info("change sharepoint scan common setting options in UI")
            self.scan_operations.set_scan_option_settings(ui_changed_setting)
            self.back_to_scan_to_sharepoint_from_options_list()
        
        if(pages > 1):
            self.goto_options_list_from_scan_to_sharepoint_screen()
            self.scan_operations.select_add_more_pages_combo()
            self.back_to_scan_to_sharepoint_from_options_list()

        self.save_to_sharepoint_enterprise(wait_time=0)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()
            self.wait_for_sharepoint_landing_view()
        
        job_ticket = job.get_job_details("scanSharePoint")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if media_source_type != None:
            assert job_ticket['src']['scan']['mediaSource'] == media_source_type, "Media Source setting is mismatched"

        if final_sharepoint_payload != None:
            logging.info("validation scan sharepoint job ticket common change settings")
            CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, final_sharepoint_payload, scan_type="scanSharePoint")

        self.wait_for_scan_quickset_job_to_complete_enterprise(cdm, job, file_type, pages=pages, time_out=time_out)    

    def wait_for_scan_quickset_job_to_complete(self, job,  file_type, pages=1, time_out=120):
        """
        wait for scan sharepoint job complete
        @param job
        @param file_type
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        scan_resource = common_instance.scan_resource()
        #prompt_for_additional_pages =  common_instance.get_prompt_for_additional_pages(type = "sharepoint")
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
        elif scan_resource == "MDF" and file_type in ["tiff", "pdf"]:
            self.spice.scan_settings.mdf_add_page_alert_done()
        
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "scanSharePoint", "status": "success"}], time_out)
        # wait for status dismiss
        time.sleep(7)
    
    def wait_for_scan_quickset_job_to_complete_enterprise(self, cdm, job, file_type, pages=1, time_out=120):
        """
        wait for scan sharepoint job complete
        @param job
        @param file_type
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        scan_resource = common_instance.scan_resource()

        self.scan_operations.flatbed_scan_more_pages_enterprise(cdm, pages)
        

    def selecting_quickset_from_sharepoint_created_initial_list(self, quickset_name):
        '''
        UI should navigate to created sharepoints by clicking a quickset from Quickset initial list.
        '''        
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_initial_list)
        self.workflow_common_operations.goto_item(quickset_name,
                                                    SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_list_view,
                                                    scrollbar_objectname=SharePointAppWorkflowObjectIds.scan_sharepoint_intial_scroll_bar
                                                    )
        sleep(2)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_landing, timeout = 16.0)
        sleep(5)
