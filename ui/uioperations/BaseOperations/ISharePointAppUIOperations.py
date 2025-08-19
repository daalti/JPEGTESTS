#########################################################################################
# @file      ISharePointAppUIOperations.py
# @author    Shubham Khandelwal (shubham.khandelwal@hp.com)
# @date      31-05-2021
# @brief     Interface for all the Scan to SharePoint UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from typing import Dict

class ISharePointAppUIOperations(object):

    def goto_scan_to_sharepoint(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_from_scan_to_sharepoint_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_landing_view_by_selecting_quickset(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_sharepoint_from_options_list(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_selected_quickset_name(self, net,  stringId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_as_default_usb_ticket(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_to_sharepoint(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def save_to_sharepoint_quickset_default(self, cdm, scan_options:Dict):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_sharepoint_landing_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def enter_quickset_pin(self, pin, index=0):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_pin_protected_quickset(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_invalid_pin_dialog_box(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_sharepoint_pin_quickset_from_landing(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_sharepoint_file_name_from_landingview(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_sharepoint_file_name_empty_and_verify_error(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_sharepoint_file_name_setting(self, filename: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_scan_to_sharepoint_from_file_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_size_settings_from_sharepoint_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_filename_string(self, filename):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_scan_to_sharepoint(self):
        """
        UI should be at scan progress view.
        Cancel the scan to sharepoint job.
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_sharepoint_quickset_from_landing(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sharepoint_quickset_view_all(self):
        '''
        This is helper method to goto sharepoint quickset
        UI flow Select Landing-> click view all quickset button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_sharepoint_quickset_by_quickset_name_from_list(self, quickset_name):
        '''
        This is helper method to select sharepoint quickset in View All screen.
        UI flow Select quickset
        Args: quickset_name: str, quickset name
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

    def perform_scan_to_sharepoint_job(self,cdm, net, job, ews_quicksets_app, scan_path,  ews_sharepoint_settings=None, ews_qs_settings=None, pin=None, ui_changed_setting=None, pdf_encryption_code=None, pages=1,media_source_type=None, time_out=90):
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_scan_quickset_job_to_complete(self, job,  file_type, pages=1, time_out=90):
        """
        wait for scan sharepoint job complete
        @param job
        @param file_type
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def selecting_quickset_from_sharepoint_created_initial_list(self, quickset_name):
        '''
        UI should navigate to created sharepoints by clicking a quickset from Quickset initial list.
        '''  
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
