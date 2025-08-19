#########################################################################################
# @file      INetworkFolderAppUIOperations.py
# @author    Lakshmi Narayanan (lakshmi-narayanan.v@hp.com)
# @date      06-03-2021
# @brief     Interface for all the Scan to Network Folder UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from typing import Dict

class INetworkFolderAppUIOperations(object):

    def goto_scan_to_network_folder_screen(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_folder_scan_details(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_folder_file_name_setting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_folder_filetype_setting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_file_name_setting_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_setting_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_network_folder_from_file_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_from_scan_to_network_folder_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_lighter_darker_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_contrast_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_long_original_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_edge_to_edge_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_color_removal_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_noise_removal_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_orientation_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_size_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_color_format_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_quality_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_resolution_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_settings_via_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_network_folder_from_options_list(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_home_from_scan_to_network_folder(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_network_folder_file_name_setting(self, filename: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_to_network_folder_filetype(self, filetype: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def save_to_network_folder_and_verify(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_save_to_network_folder(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_scan_to_network_folder(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_job_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_cancel_job_network_folder(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_job_network_folder_with_settings(self, abId, recordId, scan_options:Dict, scan_more_pages: bool = False):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_network_folder_setup(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_network_folder_software_setup(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_network_folder_browser_setup(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_button_press_scan(self, udw, screen_id, layer:int=0, timeout_val: int = 60):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_addressbook_from_scan_to_network_folder(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
      
    def goto_scan_to_network_folder_option(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_landing_view_via_selecting_quickset(self, quickset):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_selected_quickset_name(self, net,  stringId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_as_default_folder_ticket(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_folder_quickset_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_network_folder_from_quickset_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_folder_quickset(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_to_folder_quickset_default(self, cdm, abId, recordId, scan_options:Dict):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_network_landing_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def enter_quickset_pin(self, pin):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_pin_protected_quickset(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_invalid_pin_dialog_box(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_folder_pin_quickset_from_landing(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_folder_file_name_empty_and_verify_error(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_quickset_by_folder_name(self, folder_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_folder_quickset_by_quickset_name_from_list(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_quickset_and_verify_ldap_signin_error(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def validate_button_control(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_screen_buttons(self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_eject_button_operation(spice):
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
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_folder_file_name_setting_from_landing_view(self):
        """
        UI Flow is Scan to folder->Filename-> file name Keyboard
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_string(self, filename):
        """
        This method compares the filename string of network folder quickset with the expected string
        Args:
            UI should be in network folder landing view
            filename: expected filename string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_folder_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_empty_message(self, net):
        '''
        UI should be at folder landingview.
        Function will verify the filename empty message.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_local_address_from_scan_folder_landing_view(self, cdm):
        '''
        Go to local contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_custom_address_from_scan_folder_landing_view(self, custom_address_name):
        '''
        Go to custom contacts for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book-> custom address
        Args: custom_address_name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_ldap_address_from_scan_to_email_landing_view(self):
        '''
        Go to ldap addressbook for Folder path from scan to folder landing view
        UI Flow is scan to folder landing view, click folderContactSelectButton -> select address book -> LDAP 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
     
    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list: 
        @return: contacts_name_list the contacts list should be sorted
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_folder_contacts_from_contacts_view(self, contact_name):
        '''
        select folder contacts from contacts view
        UI Flow is in contacts view (already select address book)
        Args: contact_name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_folder_contact_from_custom_addressbook(self, abId,recordId, custom_address_name, contact_name):
        '''
        select folder contacts from custom addressbook view
        UI Flow should be in Scan app screen -> Scan to Network Folder -> click folderContactSelectButton -> select custom address book-> select contact.
        Args: 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_search_model_view(self):
        '''
        Go to search model view for search contact
        UI Flow is ldap contacts view, click to Search Button -> search model view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_search_contact_name(self, search_str):
        """
        Purpose: Enter search string.
        UI Flow is search model view, click Type here text field -> keyboard-> enter search string
        Args: search string which is provided on the test case
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_search_button_in_search_model_view(self):
        """
        Purpose: search input search string.
        UI Flow is search model view, click search button for search string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_no_entries_found(self, net):
        '''
        Check spec no entries found when search no contacts
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_select_addressbook_view_from_contacts_select_screen(self):
        """
        Back to Select Address Book screen from select contacts screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_folder_landing_view_from_select_addressbook_view(self, cdm):
        """
        Back to Scan folder landing screen from select addressbook screen through close button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_folder_set_up_software_screen_shows(self):
        """
        Help method to check set up software screen shows, there is no folder contacts/quicksets
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_folder_contact_from_option_screen(self, contact_name=None):
        """
        select folder contact from option screen, UI should in Scan To Folder options screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_folder_job_with_addressbook_contacts_from_home_scanapp(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=90):
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_folder_job_with_addressbook_contacts(self, cdm, udw, net, job, contact_name, select_contacts_from, option_payload=None, address_book_type='Local', custom_book_name=None, pages=1, pdf_encryption_code=None, time_out=90):
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_folder_job_to_complete(self, cdm, udw, job, file_type, pages=1, time_out=90):
        """
        wait for scan folder job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_scan_app_from_scan_to_network_folder(self):
        '''
        UI should be in Scan to Network Folder landing screen
        UI flow is Scan Folder landing view -> Scan app landing screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_folder_destination_path_text(self, path_text):
        """
        check scan to folder destination path text in landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_folder_destination_path_text_is_set(self, net):
        """
        check scan to folder destination path text in landing view is set
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_options_combobox_with_values(self, net, option_id, value_id, expected_text):
        """
        Verify the values of a combobox.
        @param net: Network object to interact with the UI.
        @param option_id: The ID of the combobox option to verify. 
                          Can get it from the csf file under interactive summary
        @param value_id: The ID of the value to check within the combobox.
        @param expected_text: The expected text value of the combobox option.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
