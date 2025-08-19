from dunetuf.addressBook.addressBook import *
from dunetuf.send.email.email import *
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowUICommonOperations import EmailAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
import logging, time
from dunetuf.send.common.common import Common as ScanCommon

class EmailAppWorkflowUILOperations(EmailAppWorkflowUICommonOperations):
    def __init__(self, spice):
        super(EmailAppWorkflowUILOperations, self).__init__(spice)
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUILOperations(self.spice)
        self.homemenu = spice.menu_operations

    def goto_email(self):
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        button_email = self.spice.query_item(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        button_email.mouse_click()
        logging.info("Inside scan to email")
    
    def goto_email_home(self):
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home)
        button_email = self.spice.query_item(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        button_email.mouse_click()
        logging.info("Inside scan to email")

    def goto_local_contacts_from_scan_to_email_landing_view(self, cdm):
        '''
        Go to local contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click toAddressBookButton -> email address book-> local
        '''
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook)
        self.spice.validate_button(email_address_btn)
        email_address_btn.mouse_click()

        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)

        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local + " MouseArea")
        button_addressbook_local.mouse_click()
        logging.info("Inside Contacts Screen")

    def goto_email_details(self):
        '''
        From scan email landing screen navigate to email details screen
        UI Flow is from email landing  screen -> click on send to field
        '''

    def back_to_email_landing_view_from_email_details(self):
        '''
        From email details screen go back to email landing screen
        UI Flow is from email details screen -> email landing screen
        '''
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        time.sleep(2)

    def back_to_email_landing_view_from_scan_settings(self):
        '''
        From scan settigns screen go back to email landing screen
        UI Flow is from email scan settings screen -> email landing view
        '''
        #self.workflow_common_operations.back_button_press(EmailAppWorkflowObjectIds.button_back, EmailAppWorkflowObjectIds.view_email_landing_view)
        scanAllOptionsModal = self.spice.wait_for("#scanOptions")
        self.spice.wait_until(lambda: scanAllOptionsModal["visible"] == True)
        scanMenuList =  self.spice.wait_for("#scanMenuList")
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        self.spice.validate_button(close_button)
        close_button.mouse_click()
        view_scan_email_landing = self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda:view_scan_email_landing["visible"])
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 35.0)
        # Wait for clickable situation
        self.spice.validate_button(send_button)
        time.sleep(5)
        logging.info("UI: At Scan to email landing screen")

    def  back_to_main_ui_from_scan_menu(self):
        '''
        from scan app navigates to menu app->home screen
        ui Flow is scan app ->menu app->home screen
        '''
        current_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_back)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        current_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_home)
        current_button.mouse_click()

    def email_details_filename_empty_and_verify_error(self):
        '''
        This is helper method to verity empty file name error popup.
        '''
        text = ""
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_filename)
        display_name_textbox = self.spice.query_item("#fileNameTextField")
        display_name_textbox.__setitem__('displayText', text)
        self.back_to_email_landing_view_from_scan_settings()
        
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send)
        send_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_email_send)
        send_button.mouse_click()

        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert)
        send_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()

    def goto_email_from_home_scanapp(self, already_created_profile=False):
        """
        Navigates to Scan to Email from Scan app at Home screen.
        UI Flow is Home->Scan->Email
        @param already_created_profile: true if already created profile otherwise false
        """
        self.spice.common_operations.goto_scan_app()
        self.spice.scan_settings.goto_email_from_scanapp_at_home_screen()
        if already_created_profile:
            self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_profile_view)
        else:
            self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
    
    def email_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5, need_to_wait_email_landing_view=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 20.0)
        self.spice.wait_until(lambda: current_button["visible"]==True)
        self.spice.wait_until(lambda: current_button["enabled"]==True)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        
        if need_to_wait_email_landing_view:
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        logging.info("Inside Email Details Screen")               

        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()
    
    def wait_for_scan_loading_toast_display(self, net, message: str = "complete", time_out=60, specific_str_checked=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, starting /scanning /complete
              timeout:
              specific_str_checked: 1. True, strings containing special characters should equal to toast message/False, just need to judge that the string is included in the toast message.
                                    2. Just to check the corresponding status, please using with False/Need to check its screen expected str, please using True
        @return:
        """
        status = False

        if message == "starting":
            scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
            scan_toast_specific_message = scan_toast_message_from_id + "..."
        elif message == 'scanning':
            scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
            scan_toast_specific_message = scan_toast_message_from_id + "..."
        elif message == 'complete':
            scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessfulMessage')
            scan_toast_specific_message= scan_toast_message_from_id
        elif message == 'successful':
            scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessful')
            scan_toast_specific_message= scan_toast_message_from_id + "!"
        elif message == 'Scan canceled':
            scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanCanceledMessage')
            scan_toast_specific_message= scan_toast_message_from_id + "!"

        time_step = 0.1
        while time_out > 0:
            try:
                toast_message = self.spice.wait_for(EmailAppWorkflowObjectIds.toast_message_text)["text"]
            except:
                toast_message = "Does not capture the status"
            time.sleep(time_step)
            time_out = time_out - time_step
            logging.info(f"current scan toast message is: <{toast_message}>")
            if specific_str_checked:
                logging.info(f"scan_toast_specific_message is <{scan_toast_specific_message}>")
                if scan_toast_specific_message == toast_message:
                    status = True
                    break
            else:
                logging.info(f"scan_toast_message_from_id is <{scan_toast_message_from_id}>")
                if scan_toast_message_from_id in toast_message:
                    status = True
                    break

        if not status:
            raise Exception(f"Timeout to find scan status <{message}>")

    def set_email_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        time.sleep(3)
        clear_text = self.spice.query_item("#scanMenuList #fileNameTextField " + EmailAppWorkflowObjectIds.clear_text_filename)
        clear_text.mouse_click()
        time.sleep(2)
        keyword_ok = self.spice.wait_for("#keyboardInputArea #enterKey1 MouseArea")
        keyword_ok.mouse_click()
        time.sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def perform_scan_email_job_with_addressbook_contacts(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, pages=1, pdf_encryption_code=None, time_out=120,scan_emulation= None):
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
                'lighter&darker': 1,   # int [1-9]
                "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
                "long_original": None, #True/False
                "background_color_removal": None, #True/False
                "background_noise_removal": None, #True/False
                "edge_to_edge_output": None, #True/False
                "file_name": None, # string
            }
        @param pages: set it when scan from Glass if scan Multi page
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param time_out: timeout to wait for job finish
        """
        ab = AddressBook(cdm, udw)
        if select_contacts_from == "landing_view":
            if address_book_type == "Local":
                abId, recordId = ab.get_addressbook_record_id(cdm, udw, "Local", contact_or_group_name)
                self.goto_local_contacts_from_scan_to_email_landing_view(cdm)
            elif address_book_type == "Custom":
                abId, recordId = ab.get_addressbook_record_id(cdm, udw, custom_book_name, contact_or_group_name)
                self.goto_custom_contacts_from_scan_to_email_landing_view(custom_book_name)
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"

            self.select_specific_email_contact_from_landing_view(cdm, recordId)
        elif select_contacts_from == "options":
            logging.info("Go to email option, Send to Contacts -> Email Contacts")
            if address_book_type == "Local":
                logging.info("Select Address Book (Local), Click on the email contact, back to landing view")
                abId, recordId = ab.get_addressbook_record_id(cdm, udw, "Local", contact_or_group_name)
                self.select_send_to_contacts()
                self.select_specific_email_contact(cdm, recordId)
            elif address_book_type == "Custom":
                raise Exception("Need to implement this test scenario")
            elif address_book_type == "LDAP":
                raise Exception("Need to implement this test scenario")
            else:
                assert False, "Address book type not existing"
        else:
            assert False, f"select contacts from type <{select_contacts_from}> not existing"

        if option_payload != None:
            self.goto_email_options()
            logging.info("change scan common setting options")
            self.scan_operations.set_scan_option_settings(option_payload)

            logging.info("change scan email setting options")
            self.set_email_setting_in_options_screen(option_payload)

            self.back_to_email_landing_view_from_email_details()
            self.wait_for_email_send_landing_view()

        scan_resource = self.get_scan_resource_used(udw, scan_emulation)
        self.email_send(wait_time=2)

        if pdf_encryption_code:
            self.scan_operations.check_spec_enter_pdf_encryption_password_screen(net)
            logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
            self.scan_operations.pdf_encryption_enter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_reenter_password(pdf_encryption_code)
            self.scan_operations.pdf_encryption_save()

        job_ticket = job.get_job_details("scanEmail")

        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]

        if option_payload != None:
            logging.info("validation scan job ticket email settings")
            self.validate_scan_job_ticket_email_setting(cdm, net, job_ticket, option_payload)

        if contact_payload != None:
            logging.info("validation scan email job ticket to list options")
            display_name = contact_payload.get("display_name", None)
            email_address = contact_payload.get("email_address", None)
            if display_name:
                assert job_ticket["dest"]["email"]["toList"][0]["displayName"] == display_name, "check send email job to list display name failed."
            if email_address:
                assert job_ticket["dest"]["email"]["toList"][0]['emailAddress'] == email_address, "check send email job to list email address failed."
        logging.info(f"scan_resource: {scan_resource}")
        adf_loaded = False
        if pages == 1 and scan_resource == "ADF" and scan_emulation != None:
            scan_emulation.media.load_media("ADF")
            adf_loaded = True

        self.wait_for_scan_email_job_to_complete(cdm, udw, job, file_type, pages, time_out,scan_emulation=scan_emulation, adf_loaded=adf_loaded)
