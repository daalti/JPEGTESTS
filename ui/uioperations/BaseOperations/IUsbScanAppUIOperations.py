#########################################################################################
# @file      IUsbScanAppUIOperations.py
# @author    Anu Sebastian (anu.sebastian@hp.com)
# @date      15-02-2021
# @brief     Interface for all the Scan to USB UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from typing import Dict

class IUsbScanAppUIOperations(object):

    def goto_scan_to_usb_screen(self):
        '''
        Navigates to Scan then USB Drive screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->(Scan to USB landing view)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_scan_to_usb(self):
        """
        Navigates to Scan then USB Drive screen starting from Main menu
        UI Flow is Main menu->Scan->USB Drive
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_scan_to_usb_via_usb_drive_app(self):
        '''
        Navigates to USB Drive then Scan screen from Home screen.
        UI Flow is Home->USB Drive->Scan->(Scan to USB landing view)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_file_settings(self):
        '''
        UI should be in Scan to USB landing view.
        Navigates to File settings screen.
        UI Flow is USB Drive->File Name->(File Details settings view)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_scan_location_folders(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to scan location screen.
        UI Flow is (File Details settings view)->Scan Location->(Scan folder list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_file_name_setting(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to filename setting screen.
        UI Flow is (File Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_file_format_setting(self):
        '''
        UI should be in Scan to USB File settings screen.
        Navigates to fil format setting screen.
        UI Flow is (File Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_file_settings_via_usb(self):
        '''
        Navigates to File settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_scan_location_folders_via_usb(self):
        '''
        Navigates to scan location settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Scan Location->(Scan folder list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_file_name_setting_via_usb(self):
        '''
        UI should be in Scan to USB File settings screen starting from Home screen..
        Navigates to filename setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Filename->(Alphanumeric Keyboard)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_file_format_setting_via_usb(self):
        '''
        UI should be in Scan to USB File settings screen starting from Home screen.
        Navigates to fil format setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->FileType->(Scan File Type Settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_usb_from_file_settings(self):
        '''
        UI should be in file settings screen - Home->Scan->USB Drive->File Name->(File Details settings view)
        Navigates back to USB landing view.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_from_scan_to_usb(self):
        '''
        UI should be in Scan to USB screen.
        Navigates to Options screen starting from USB Scan screen.
        UI Flow is Scan to USB->Options->(Options list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_via_usb(self):
        '''
        Navigates to Options screen starting from Home screen.
        UI Flow is Home->USB Drive->Scan->Options->(Options list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_lighter_darker_settings_via_usb(self):
        '''
        Navigates to Lighter/Darker in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Lighter/Darker->(Lighter/Darker slide)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_contrast_settings_via_usb(self):
        '''
        Navigates to Lighter/Darker in USB Options starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Contrast->(Contrast slide)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_orientation_settings_via_usb(self):
        '''
        Navigates to Orientation in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Orientation->(Orientation settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_size_settings_via_usb(self):
        '''
        Navigates to Original Size in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Original Size->(Original Size settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_color_format_settings_via_usb(self):
        '''
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Color Format->(Color format settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_quality_settings_via_usb(self):
        '''
        Navigates to Color Format in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Quality->(Quality settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_long_original_settings_via_usb(self):
        '''
        Navigates to Long original in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Long Original->(Long original settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_edge_to_edge_settings_via_usb(self):
        '''
        Navigates to Long original in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Edge-to-Edge->(Edge-to-Edge settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_color_removal_via_usb(self):
        '''
        Navigates to Long original in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->background Color removal->(background Color removal settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_noise_removal_via_usb(self):
        '''
        Navigates to Long original in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->background Noise removal->(background Noise removal settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_resolution_settings_via_usb(self):
        '''
        Navigates to Resolution in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Resolution->(Resolution settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_paper_type_settings_via_usb(self):
        '''
        Navigates to Content type in USB Settings starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Original Paper Type->(Original Paper Type settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_settings_via_usb(self):
        '''
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->File Type->(File Type settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_settings_via_usb(self):
        '''
        Navigates to Sides in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Sides-> (Sides settings screen)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_usb_options_list_from_resolution_setting_screen(self):
        '''
        UI should be in resolution setting view
        Navigates back from resolution setting screen to scan settings view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_usb_from_options_list(self):
        '''
        UI should be in Options list.
        Navigates back from Options screen to USB landing view.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_home_from_scan_to_usb(self):
        '''
        UI should be in Scan to USB screen
        Navigates back from Scan to USB screen to Scan
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_usb_file_name_setting(self, filename: str):
        '''
        UI should be at alphanumeric keyboard view.
        Sets filename
        Args:
            filename: scan to usb filename
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_usb_folder_location(self, folder: str = None):
        '''
        UI should be at Scan folder list
        Sets folder location - todo
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_to_usb_fileformat(self, filetype: str):
        '''
        UI should be on File format settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def save_to_usb(self):
        '''
        UI should be at Scan USB landing view.
        Starts save to USB drive and verifies job is successful.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_save_to_usb(self, scan_more_pages: bool = False, time_out=5):
        '''
        UI should be at Scan USB landing view.
        Starts save to USB drive.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_scan_to_usb(self):
        '''
        UI should be at scan progress view.
        Cancel the scan to usb job.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_job_usb(self):
        '''
        UI flow is from Home screen.
        Starts save to USB drive and verifies job is successful.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_cancel_job_usb(self):
        '''
        Start save to USB drive and cancel job.
        UI flow is from Home screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def save_to_usb_with_settings(self, scan_options:Dict):
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
            'lighter_Darker': 1,
             'contrast': 1
        }
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_app_landing_view_from_scan_folder(self, net):
        '''
        Verify no USB device is connected by checking for no device screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_no_front_usb_device_constriant(self):
        '''
        UI should be at no USB device connected screen.
        Verify no front USB device connected screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_cancel_at_no_usb_device_screen(self):
        '''
        UI should be at no USB device connected screen.
        Press Cancel button in the No front USB device screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_to_usb_landing_view(self):
        '''
        This keyword verifies screen is in scan to usb landing view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_to_usb_success(self):
        '''
        This keyword verifies screen is in scan to usb success view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_string(self, filename):
        '''This method compares the filename string with the expected string

        Args:
            UI should be in file settings landing view
            filename: expected filename string
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

        
    def verify_selected_quickset_name(self, net,  stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check UsbQuicksetSelected Button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_as_default_usb_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_usb_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_usb_quickset(self, quickset_name):
        '''
        This is helper method to select usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def select_folder(self, foldername):
        '''
        This is helper method to select usb folder
        UI flow Select Send to usb -> Location -> Select Folder
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_to_usb_quickset_default(self, cdm, scan_options:Dict):
        '''
        This is helper method to save the quickset value. 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_save_to_usb_landing_view(self):
        '''
        This is helper method to wait for usb landing.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_usb_file_name_empty_and_verify_error(self):
        '''
        This is helper method to delete file name and veify error popup.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_scan_job_corresponding_status_displayed(self, status: str, time_out=30):
        """
        Wait until corresponding status displayed in FP UI.
        :param status: starting/scanning/sending/scanning_complete
        :param time_out: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_file_name_setting_interactive_summary(self):
        """
        UI should be in Scan to USB File settings screen.
        Navigates to filename setting screen.
        UI Flow is (File Details settings view)->Filename->(Alphanumeric Keyboard)
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_file_name_setting_interactive_summary_via_usb(self):
        """
        UI should be in Scan to USB File settings screen starting from Home screen..
        Navigates to filename setting screen.
        UI Flow is Home->Scan->USB Drive->File Name->(File Details settings view)->Filename->(Alphanumeric Keyboard)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is Sides-> (Sides Settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_settings_interactive_summary_via_usb(self):
        """
        UI should be in Scan to USB Sides Settings screen..
        Navigates to Sides setting screen.
        UI Flow is Home->Scan->USB Drive->Sides->(Sides Settings screen)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_settings_interactive_summary_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->File Type->(File Type settings screen)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is filetype-> (filetype Settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_resolution_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is resolution-> (resolution Settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_resolution_settings_interactive_summary_via_usb(self):
        """
        Navigates to File Type in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->resolution->(resolution settings screen)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_color_settings_interactive_summary(self):
        """
        UI should be on Scan interactive summary screen.
        UI Flow is color-> (color Settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_back_button_in_header(self):
        '''
        This is helper method to click back button in header
        Generic back button click in the header
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_multiple_usb_partition(self, count):
        '''
        This is a helper message to verify there are 2 partitioned USBs present
        UI Flow is Home->Scan->USB Drive->Select->Back->(Verify 2 Partitions)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_partition(self, name):
        '''
        This method used to select the partition with name
        UI flow Select Send to usb -> Location -> Select Folder -> Back -> Select Partition
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_read_only_enabled_screen_displayed(self, net):
        """
        This method is to check the filename read-only enabled
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)  

    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)  

    def press_ok_button_at_usb_unsupported_device_error_screen(self):
        """
        Click OK at usb unsupported device error screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name) 

    def verify_usb_unsupported_device_error_screen(self, net):
        """
        Verify usb unsupported device error screen displayed and check message.
        :param net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name) 

    def scrollto_usbfolder_in_folder_selection(self, folder_name:str):
        """
        UI should be on Usb Folder selection screen.
        UI Flow is Home > Scan > Scan to Usb > Edit
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_scan_to_usb_options_list_from_original_size_setting_screen_with_close_button(self):
        """
        UI should be in original size setting view
        Navigates back from original size setting screen to scan settings view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name) 

    def set_usb_file_name_empty(self):
        '''
        This is helper method to set filename as empty.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_empty_message(self, net):
        '''
        This is helper method to set filename as empty.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_usb_job_to_complete(self, cdm, udw, net, job,scan_emulation, file_type, pages=1, time_out=90, adf_loaded=False):
        """
        wait for scan usb job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_scan_resource_used(self, udw, scan_emulation):
        """
        Return current scan resouse is under used
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_usb_job_notification_setting(self):
        '''
        UI should be in Scan to USB job notification screen.
        Navigates to job notification setting screen.
        UI Flow is app landing view -> settings -> job notification setting
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_job_notification_setting(self, job_notification_setting: str, checked: bool = True):
        '''
        Verify job notification setting
        @param job_notification_setting: job notification setting
        @param checked: expected checked state
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_job_notification_include_thumbnail_setting(self, net, checked: bool = True, constrained: bool = False):
        '''
        Verify job notification option include thumbnail
        @param checked: expected checked state
        @param constrained: expected constrained state
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_job_notification_settings(self, net, donotnotify: bool, notifyafterjobfinishes: bool, notifyonlywhenjobfail: bool):
        '''
        Verify job notification settings and include thumbnail constraint behavior
        @param donotnotify: expected state of do not notify option
        @param notifyafterjobfinishes: expected state of notify after job finishes option
        @param notifyonlywhenjobfail: expected state of notify only when job fails option
        @param include_thumbnail_checked: expected checked state of include thumbnail option
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_job_notification_setting(self, job_notification_setting: str):
        '''
        Change job notification setting
        @param job_notification_setting: job notification setting
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_job_notification_done_buttom(self):
        '''
        Click on done button in job notification setting screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)