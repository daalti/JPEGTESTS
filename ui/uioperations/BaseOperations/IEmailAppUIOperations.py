#########################################################################################
# @file      IEmailAppUIOperations.py
# @author    Nevin Thomas (nevin.thomas@hp.com)
# @date      15-02-2021
# @brief     Interface for all the Scan to Email UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from typing import Dict

class IEmailAppUIOperations(object):

    def goto_email_send_options(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_home_from_send_to_options(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_main_ui_from_scan_home(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_send_to_contacts(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_and_specify_send_to_contacts(self, cdm, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    

    def goto_email_new_address(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_specific_email_contact(self, cdm, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_landing(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_app_from_email_landing(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_add_recipient(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_email_landing_view_from_add_recepient(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_options(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_options_from_home(self, cdm, udw, name: str, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_setup_profile(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_setup_profile_hp_software(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_setup_profile_web_browser(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details_to_address(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details_from_address(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details_subject(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details_filename(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_details_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_input_field_interactive_summary(self,setting: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_email_landing_view_from_email_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_email_landing_view_from_scan_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5, need_to_wait_email_landing_view=True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def complete_email_send(self, cdm, udw, job, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5, need_to_wait_email_landing_view=True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_send_with_encryption(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_email_send(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_details_to_address_remove_contact(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_details_to_address_remove_contact_cancel(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_setup_profile_hp_software_click_ok(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_setup_profile_web_browser_click_ok(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_enter_pin(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_enter_wrong_pin(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_select_profile(self, cdm, udw, name: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_details_enter_text_to_field(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def enter_new_email_address(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def pdf_encryption_screen_cancel(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_email_quickset(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_email_quickset_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_as_default(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_selected_quickset(self, name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_email_job_with_settings(self, job, cdm, udw, name: str, recordId, scan_options: Dict, scan_more_pages: bool = False):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_error_msg_email_send_without_recipient(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def save_to_email_quickset_default(self, cdm, udw, name, recordId, scan_options:Dict):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_email_send_landing_view(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_send_when_default_profile_is_set(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_email_profile_from_email_landing_view(self, cdm, udw, name: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def email_details_filename_empty_and_verify_error(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_to_list_button_and_select_email_contact(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_scan_to_email_application_screen(self, spice, net, email_address):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_email_quickset_by_quickset_name_from_list(self, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_loading_screen_for_selected_quickset(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_quickset_options_from_default(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_loading_toast_display(self, time_out= 30):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_email_setup_no_profile(self):
        '''
        UI Wait for Email setup screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_quickset_existing(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_from_home_scanapp(self, already_created_profile=False):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def  back_to_main_ui_from_scan_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    
    def select_send_to_contacts_from_scan_to_email_landing_view(self, cdm, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def enter_multiple_email_address(self, email_list):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_email_home(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def email_select_profile_home(self, cdm, udw, name: str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_specific_email_groups_from_landing_view(self, cdm, group_name):
        '''
        Select Groups for To address from scan to email landing view
        UI Flow: Local contact screen -> select specific groups -> Back to send to email landing screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ldap_contacts_from_scan_to_email_landing_view(self):
        '''
        Go to ldap contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click to AddressBookButton -> email address book-> ldap
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_search_model_view_from_ldap_contacts(self):
        '''
        Go to search model view for search contact from ldap contacts view
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

    def check_keyboard_open_on_setting(self):
        """
        Purpose: Check if keyboard opens on click of a setting(toField/fromField/subject) search string.
        UI Flow click  field -> keyboard -> click Ok
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def search_input_contact_name_in_search_model_view(self):
        """
        Purpose: search input search string.
        UI Flow is search model view, click search button for search string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_available_contact_from_ldap_contacts_view(self, display_name):
        '''
        Select contacts from ldap contacts view
        UI Flow: Ldap contact screen -> select contact -> Back to send to email landing screen
        Args: display_name which is provided on the test case
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_keyboard_shift_to_upper_case(self):
        '''
        Purpose: Change keyboard shift to upper case
        UI Flow is scan to email landing view, click To address text field -> keyboard
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_keyboard_shift_to_lower_case(self):
        '''
        Purpose: Change keyboard shift to lower case
        UI Flow is scan to email landing view, click To address text field -> keyboard
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def input_text_from_keyboard(self, text):
        '''
        Purpose: input email address in keyboard
        UI Flow is scan to email landing view, click To address text field -> keyboard ->input email address
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_email_settings_editable(self, net, setting, editable: bool = True):
        """
        This method verify email settings editable subject, message
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
                    subject, message
            editable: Need to pass bool values True/False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_email_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_filename_empty_message(self, net):
        '''
        UI should be at email landingview.
        Function will verify the filename empty message.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_custom_contacts_from_scan_to_email_landing_view(self, custom_address_name):
        '''
        Go to custom contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click toAddressBookButton -> email address book-> custom address
        Args: custom_address_name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_search_contacts_ldap_addressbook(self, net):
        '''
        Check spec search contacts 'Search to view a list of contacts' when select LDAP address book
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_cancel_button_in_search_screen(self):
        """
        Click cancel button in search screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_reset_button(self):
        '''
        click reset button on search result contacts landing view screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_search_result_number_in_contacts_list_view(self, expected_contacts_list):
        """
        Check Search Result numbers shows in contacts list view screen.
        @param:expected_file_list: 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_contacts_display_name_in_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list: the contacts list should be sorted
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def is_contacts_existing(self, contacts_name):
        '''
        This is helper method to verify is contacts existing in scan to email address book
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def back_to_select_addressbook_view_from_contacts_select_screen(self):
        """
        Back to Select Address Book screen from select contacts screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_email_landing_view_from_select_addressbook_view(self):
        """
        Back to Scan email landing screen from select addressbook screen through close button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list: 
        @return: contacts_name_list the contacts list should be sorted
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_ldap_address_book(self):
        '''
        select ldap address book in select address book screen
        UI Flow should be in scan to email landing view, click to AddressBookButton -> select address book screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_contacts_select_screen_from_search_contacts_screen(self):
        '''
        From search contact screen go back to contacts select screen through close button
        UI Flow is from email search contact -> contacts select view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_contact_search_string(self, expected_string):
        '''
        This method verify the search string on added contacts screen. 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_email_job_and_check_file_name(self, cdm, udw, net, job, to_address, file_name, file_type, prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='', prefix_username='admin', suffix_username='admin', profile_name=None, time_out=90):
        """
        1. Home screen -> Menu -> Scan -> Scan to Email -> Select profile
        2. Input to address -> Send email job
        3. Get preview file name from job details, and check file name
        4. Wait for job complete
        @param cdm
        @param udw
        @param net
        @param job
        @param to_address: 
        @param file_name:  file_name from settings
        @param file_type:  file_type from settings, value from key of scan_file_type_option_dict
        @param prefix_type:  prefix_type from settings, value from key of scan_file_name_prefix_option_dict
        @param suffix_type:  suffix_type from settings, value from key of scan_file_name_suffix_option_dict
        @param custom_prefix_string: custom_prefix_string comes from Settings, only custom has Settings
        @param custom_suffix_string:  custom_suffix_string comes from Settings, only custom has Settings
        @param prefix_username: prefix_username select username from settings
        @param suffix_username: suffix_username select username from settings
        @param profile_name: should provide email profile name when server type is user defined server
        @param time_out: timeout to wait for job finish 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_email_setting_in_options_screen(self, payload):
        """
        Set email settings in email options screen
        @param payload: please refer to structure from quickset_email_payload from dunetuf.ews.copy_scan_ews_option_dict
                        In scan email ui setting, only can set from_address/to_address/subject/message option.
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_scan_job_ticket_email_setting(self, cdm, net, job_ticket, payload):
        """
        Compare cdm scan email settings with job ticket
        @param job_ticket: get job ticket from cdm
        @param payload: include email settings and scan common settings. 
                        In scan email ui setting, only can change from_address/to_address/subject/message email option.
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def start_email_send(self, wait_time=5, need_to_wait_email_landing_view=True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_scan_email_job_to_complete(self, cdm, udw, job, file_type, pages=1, time_out=90, scan_emulation=None, number_of_jobs_to_check=1, adf_loaded=False):
        """
        wait for scan email job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_email_job_with_addressbook_contacts_from_home_scanapp(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, profile_name=None, pages=1, pdf_encryption_code=None, time_out=90):
        """
        1. Navigation to Home -> Scan app -> Scan to Email landing view
        2. Go to email option/landing view, Send to Contacts -> Email Contacts -> Select address_book_type, Click on the email contact, back to landing view.
        3. Go to email options, change options if need to change options. Back to email landing view.
        4. Send email job
        5. Validation scan job ticket to list options, email settings and scan common settings if changed.
        6. Check scan email job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param address_book_type: "Local"/"Custom"/"LDAP"
        @param contact_or_group_name: contact name or group name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
        @param contact_payload: contact payload if need to check, default is None
            contact_payload = {
                "display_name": contact_or_group_name, # string
                "email_address": "dsuser02@ds2016.boi.rd.hpicorp.net", # string, if select group, email address not shows in job ticket, not give email address key.
            }
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param option_payload:include email settings and scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                "subject": "subject_string", # string
                "message": "test_message", # string
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
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_email_job_with_addressbook_contacts_from_menu_scanapp(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, profile_name=None, pages=1, pdf_encryption_code=None, time_out=90,scan_emulation=None):
        """
        1. Navigation to Menu -> Scan app -> Scan to Email landing view
        2. Go to email option/landing view, Send to Contacts -> Email Contacts -> Select address_book_type, Click on the email contact, back to landing view.
        3. Go to email options, change options if need to change options. Back to email landing view.
        4. Send email job
        5. Validation scan job ticket to list options, email settings and scan common settings if changed.
        6. Check scan email job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param address_book_type: "Local"/"Custom"/"LDAP"
        @param contact_or_group_name: contact name or group name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
        @param contact_payload: contact payload if need to check, default is None
            contact_payload = {
                "display_name": contact_or_group_name, # string
                "email_address": "dsuser02@ds2016.boi.rd.hpicorp.net", # string, if select group, email address not shows in job ticket, not give email address key.
            }
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param option_payload:include email settings and scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                "subject": "subject_string", # string
                "message": "test_message", # string
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
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pages: set it when scan from Glass if scan Multi page 
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_scan_email_job_with_addressbook_contacts(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, pages=1, pdf_encryption_code=None, time_out=90, scan_emulation=False):
        """
        1. Go to email option/landing view, Send to Contacts -> Email Contacts -> Select address_book_type, Click on the email contact, back to landing view.
        2. Go to email options, change options if need to change options. Back to email landing view.
        3. Send email job
        4. Validation scan job ticket to list options, email settings and scan common settings if changed.
        5. Check scan email job complete.
        @param cdm
        @param udw
        @param net
        @param job
        @param address_book_type: "Local"/"Custom"/"LDAP"
        @param contact_or_group_name: contact name or group name which want to select from address book
        @param select_contacts_from: "landing_view"/"options"
            "landing_view" means select to address contacts from landing view -> to address book.
            "options" means select to address contacts from landing view -> options-> to address book.
        @param contact_payload: contact payload if need to check, default is None
            contact_payload = {
                "display_name": contact_or_group_name, # string
                "email_address": "dsuser02@ds2016.boi.rd.hpicorp.net", # string, if select group, email address not shows in job ticket, not give email address key.
            }
        @param custom_book_name: if address book type is Custom, need to give custom address book name.
        @param option_payload:include email settings and scan common settings. If no option change, None
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
            e.g.  
            option_payload = {
                "subject": "subject_string", # string
                "message": "test_message", # string
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
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_to_field_error_value(self, error):
        '''
        Check to field error is false
        @param error: "true/false"
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_from_address_in_landing_view(self, from_address):
        """
        input from address in landing view, UI should in email landing view
        @param: from_address: str, from address to input
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_to_address_in_landing_view(self, to_address, use_keyboard=True):
        """
        input to address in landing view, UI should in email landing view
        @param: to_address: str, to address to input
                use_keyboard: default value is True, input to address using keyboard.
                              If address with very long characters, it is very time-consuming input address using keyboard, so set value is False.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_invalid_email_address_message_under_from_address(self, net):
        '''
        verify invalid email address error message under from address
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_visible_helper_message_under_from_address(self):
        """
        Purpose: check if helper message item under from address is visible or not.
        @return: isVisible
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_invalid_email_address_message_under_to_address(self, net):
        '''
        verify invalid email address error message under to address
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_to_email_field_text_in_landing_view(self, to_address: str):
        """
        verify to email field text in landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_visible_helper_message_under_to_address(self):
        """
        Purpose: check if helper message item under to address is visible or not.
        @return: isVisible
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_subject_in_landing_view(self, subject):
        """
        input subject in landing view, UI should in email landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_subject_field_text_in_landing_view(self, subject_text: str):
        """
        verify subject field text in landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_information_missing_or_incorrect_message_under_subject(self, net):
        '''
        verify "The required information is either missing or incorrect. Try again." error message under subject. 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_actual_displayed_message_in_options_screen(self):
        '''
        To get actual displayed message in options screen
        Return: actual displayed message
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_displayed_message_in_options_screen(self, input_message):
        '''
        To verify the input message match the actual displayed message
        Args: input message
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def input_message_in_options_screen(self, message, clear_input_box: bool = False):
        """
        input message in options screen, UI should in options screen
        Args:
        message: need to input message
        clear_input_box: clear input box before input message or not
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scrollto_emailfolder_in_profile_selection(self, folder_name:str):
        """
        UI should be on Usb Folder selection screen.
        UI Flow is Home > Scan > Scan to Usb > Edit
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_back_email_jobs(self, scan_resource, cdm, udw, job, scan_emulation, times=1,send_instance=None):
        """
        Back to back email jobs
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
