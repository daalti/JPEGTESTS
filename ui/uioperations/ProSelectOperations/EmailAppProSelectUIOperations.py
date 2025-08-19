#########################################################################################
# @file      EmailAppProSelectUIOperations.py
# @author    Nevin Thomas (nevin.thomas@hp.com)
# @date      15-02-2021
# @brief     Implementation for all the Scan to Email UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
import time
from time import sleep
import logging
from enum import Enum
from dunetuf.job.job import Job
from typing import Dict
from dunetuf.ui.uioperations.BaseOperations.IEmailAppUIOperations import IEmailAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.UsbScanAppProSelectUIOperations import UsbScanAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.send.email.email import *
from dunetuf.send.common.common import Common as ScanCommon
_logger = logging.getLogger(__name__)


class EmailAppProSelectUIOperations(IEmailAppUIOperations):
    SCAN_EMAIL = "#b8460c9e-43c8-4290-a0f8-8ce450867f09"
    SCAN_EMAIL_SETUP_VIEW = "#scanEmailSetupView"
    SCAN_EMAIL_QUICKSET_LIST_VIEW = "#QuickSetListView"
    SCAN_EMAIL_QUICKSET_LANDING_VIEW = "#quickSetsLandingView"
    SCAN_EMAIL_QUICKSET_BUTTON = "#EmailQuickSetSelectedButton"
    SCAN_EMAIL_SAVE_BUTTON = "#EmailSaveButton"

    SCAN_EMAIL_QUICKSET_SAVE_OPTION_VIEW = "#QuickSetSaveOptionsView"
    SCAN_EMAIL_AS_DEFAULT_BUTTON = "#AsDefault"

    SCAN_EMAIL_SEND_TO_OPTIONS_VIEW = "#sendToOptionsView"
    SCAN_EMAIL_SEND_TO_CONTACTS = "#EmailSendContactsButton"
    SCAN_EMAIL_SEND_TO_NEW_ADDRESS = "#EmailNewAddressButton"
    SCAN_EMAIL_NEW_ADDRESS_VIEW = "#emailNewAddressView"

    SCAN_EMAIL_CONTACTS_VIEW = "#selectContactView"
    SCAN_EMAIL_ADDRESS_BOOK_RECORDS = '#addressBookRecords'
    SCAN_EMAIL_ADDRESS_BOOK_RECORD = '#AddressBook'

    SCAN_EMAIL_LANDING_VIEW = "#emailLandingView"
    SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON = "#SendButton"
    SCAN_EMAIL_LANDING_VIEW_SEND_TO_BUTTON = "#SendToButton"
    SCAN_EMAIL_ADD_RECIPIENT_BUTTON = "#addRecipientButton"
    SCAN_EMAIL_OPTIONS_BUTTON = "#OptionsButton"

    SCAN_EMAIL_REMOVE_CONTACT_VIEW = "#removeContactView"
    SCAN_EMAIL_REMOVE_CONTACT_BUTTON = "#EmailRemoveButton"
    SCAN_EMAIL_REMOVE_CONTACT_CANCEL_BUTTON = "#EmailCancelButton"
    SCAN_EMAIL_TO_LIST_BUTTON = "#toListButton"

    SCAN_PROGRESS_VIEW = "#SystemProgressView"
    SCAN_EMAIL_SEND_SUCCESSFUL_VIEW = "#emailSendSuccessfulView"

    SCAN_EMAIL_SETUP_PROFILE_VIEW = "#emailSetupView"
    SCAN_EMAIL_SETUP_USING_HP_SOFTWARE = "#emailSetupSoftware"
    SCAN_EMAIL_SETUP_USING_WEB_BROWSER = "#emailSetupWebBrowserButton"

    SCAN_EMAIL_SETUP_USING_HP_SOFTWARE_VIEW = "#emailSoftwareSetupView"
    SCAN_EMAIL_SETUP_USING_HP_SOFTWARE_OK_BUTTON = "#emailSetupOkButton"

    SCAN_EMAIL_SETUP_USING_WEB_BROWSER_VIEW = "#browserSetupView"
    SCAN_EMAIL_SETUP_USING_WEB_BROWSER_OK_BUTTON = "#BrowserSetupOkButton"

    SCAN_EMAIL_DETAILS_VIEW = "#emailDetailsView"
    SCAN_EMAIL_DETAILS_TO_ADDRESS = "#addRecipientButton"
    SCAN_EMAIL_DETAILS_FROM_ADDRESS = "#fromNameButton"
    SCAN_EMAIL_DETAILS_SUBJECT = "#subjectNameButton"
    SCAN_EMAIL_DETAILS_FILENAME = "#fileNameButton"
    SCAN_EMAIL_DETAILS_MESSAGE = "#messageNameButton"

    SCAN_EMAIL_SELECT_PROFILE_VIEW = "#selectFromProfileView"
    SCAN_EMAIL_PIN_KEYBOARD_VIEW = "#emailProfilePinKeyboardView"

    SCAN_EMAIL_TO_ADDRESS_EMPTY_LIST_VIEW = "#ToListEmptyView"
    SCAN_EMAIL_TO_ADDRESS_EMPTY_OK_BUTTON = "#OK"
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.dial_keyboard_operations = ProSelectKeyboardOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)
        self.scan_usb = UsbScanAppProSelectUIOperations(self._spice)

    #Email Flow Keywords

    def goto_email_send_options(self):
        '''
        Navigates to Scan then Email screen starting from Home screen.
        UI Flow is Home->Scan->Email
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.SCAN_EMAIL, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SELECT_PROFILE_VIEW,timeout = 9.0)
        logging.info("Inside scan to email")

    def goto_email(self):
        '''
        Navigates to Email screen from Scan Home
        UI Flow is Scan Home -> Email
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW,timeout = 18.0)
        logging.info("Inside scan to email")

    def back_to_scan_home_from_send_to_options(self):
        '''
        Navigate back to scan home from send to options screen
        UI Flow is send to options view -> scan home view
        '''
        self.dial_common_operations.back_button_press(self.SCAN_EMAIL_SELECT_PROFILE_VIEW, self.scan_operations.SCAN_APP, 1)

    def back_to_main_ui_from_scan_home(self):
        '''
        Navigate back to main ui from scan home
        UI flow is scan home -> main ui
        '''
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_APP, "#HomeScreenView")

    def select_send_to_contacts(self):
        '''
        From send options screen navigate to send to contacts screen
        UI Flow is Send Options -> Send to contacts
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SEND_TO_CONTACTS, "#ButtonListLayout")
        contacts_view = self._spice.wait_for(self.SCAN_EMAIL_CONTACTS_VIEW, timeout = 9.0)
        self._spice.wait_until(lambda: contacts_view["visible"] == True, timeout = 10.0)
        assert contacts_view, 'Contacts view not shown'
        logging.info("Inside Contacts Screen")

    def select_and_specify_send_to_contacts(self, cdm, recordId):
        '''
        From send options screen navigate to send to contacts screen
        UI Flow is Send Options -> Send to contacts
        '''
        self.select_send_to_contacts()
        self.select_specific_email_contact(recordId)

    def goto_email_new_address(self):
        '''
        From send options screen navigate to new address screen
        UI Flow is Send Options -> new address
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SEND_TO_NEW_ADDRESS, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_NEW_ADDRESS_VIEW, timeout = 9.0)
        logging.info("Inside Contacts Screen")

    def select_specific_email_contact(self, recordId):
        '''
        From send to contacts screen navigate to email landing view
        UI Flow is select email contact out of multiple contacts listed -> email landing view
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_ADDRESS_BOOK_RECORD+recordId, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 9.0)
        logging.info("Inside Email Landing View")
    
    def goto_to_list_button_and_select_email_contact(self):
        '''
        From send to contacts screen navigate to email Details view. 
        Click on Scan to button and select email to list. 
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_TO_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, dial_value = 0)
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW, timeout = 9.0)        
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_TO_LIST_BUTTON, self.SCAN_EMAIL_DETAILS_VIEW)
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 9.0)
        logging.info("Inside Email Landing View")

    def goto_email_landing(self):
        '''
        From send to contacts screen navigate to email landing view
        UI Flow is select email contact -> email landing view
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_ADDRESS_BOOK_RECORDS, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 9.0)
        logging.info("Inside Email Landing View")

    def back_to_scan_app_from_email_landing(self):
        '''
        From email landing view go back to send to options view
        UI FLow is email landing view -> send to options view
        '''
        self.dial_common_operations.back_button_press(self.SCAN_EMAIL_LANDING_VIEW, self.scan_operations.SCAN_APP, 2)

    def goto_email_add_recipient(self):
        '''
        From email landing view navigate to add recepient screen
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_ADD_RECIPIENT_BUTTON, self.SCAN_EMAIL_DETAILS_VIEW )
        assert self._spice.wait_for(self.SCAN_EMAIL_SEND_TO_OPTIONS_VIEW, timeout = 9.0)
        logging.info("Inside Email add recepients (send to options)")

    def back_to_email_landing_view_from_add_recepient(self):
        '''
        From add recepient screen go back to email landing view
        UI Flow is add recepient screen -> email landing view
        '''
        self.dial_common_operations.back_button_press(self.SCAN_EMAIL_SEND_TO_OPTIONS_VIEW, self.SCAN_EMAIL_LANDING_VIEW)

    def goto_email_options(self):
        '''
        From email landing view navigate to options screen
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_OPTIONS_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_operations.SCAN_SETTINGS_VIEW, timeout = 9.0)
        logging.info("Inside Email options")

    def goto_email_options_from_home(self, cdm, udw, name: str, recordId):
        '''
        From home screen navigate to options screen
        '''
        self.scan_operations.goto_scan_app()
        self.email_select_profile(cdm, udw, name)
        self.goto_email_details()
        self.goto_email_details_to_address()
        self.select_send_to_contacts()
        self.select_specific_email_contact(recordId)
        self.goto_email_options()
        logging.info("Inside Email options")

    def goto_email_setup_profile(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> screen with instructions to set up email profile
        '''
        sleep(1)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SETUP_PROFILE_VIEW, timeout = 9.0)
        logging.info("Inside Email Profile Setup Screen")

    def goto_email_setup_profile_hp_software(self):
        '''
        From scan email setup profile screen click on setup using HP Software
        UI Flow is from screen with instructions to set up email profile -> click setup using Hp Software
        '''
        sleep(3)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SETUP_USING_HP_SOFTWARE, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SETUP_USING_HP_SOFTWARE_VIEW)
        logging.info("Inside Email Profile Setup Using HP Software Screen")

    def goto_email_setup_profile_web_browser(self):
        '''
        From scan email setup profile screen click on setup using Web Broswer
        UI Flow is from screen with instructions to set up email profile -> setup using Web Browser
        '''
        sleep(3)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SETUP_USING_WEB_BROWSER, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SETUP_USING_WEB_BROWSER_VIEW)
        logging.info("Inside Email Profile Setup Using Web Browser Screen")

    def goto_email_details(self):
        '''
        From scan email landing screen navigate to email details screen
        UI Flow is from email landing  screen -> click on send to field
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_TO_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, dial_value = 0)
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW, timeout = 9.0)
        logging.info("Inside Email Details Screen")

    def goto_email_details_to_address(self):
        '''
        From scan email details screen navigate into To address
        UI Flow is from email details screen -> click on To address
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_TO_ADDRESS, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SEND_TO_OPTIONS_VIEW, timeout = 9.0)
        logging.info("On Email Send To Contacts Screen")

    def goto_email_details_from_address(self):
        '''
        From scan email details screen navigate to from address screen
        UI Flow is from email details screen -> click on from address
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_FROM_ADDRESS, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW, timeout = 9.0)
        logging.info("Inside email details From address Screen")

    def goto_email_details_subject(self):
        '''
        From scan email details screen navigate to subject screen
        UI Flow is from email details screen -> click on subject
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_SUBJECT, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW)
        logging.info("Inside Email Details Subject Screen")

    def goto_email_details_filename(self):
        '''
        From scan email details screen navigate to filename screen
        UI Flow is from email details screen -> click on filename
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_FILENAME, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW)
        logging.info("Inside Email Details Filename Screen")

    def goto_email_details_message(self):
        '''
        From scan email details screen navigate to filename screen
        UI Flow is from email details screen -> click on filename
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_MESSAGE, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW)
        logging.info("Inside Email Details MESSAGE Screen")

    def back_to_email_landing_view_from_email_details(self):
        '''
        From email details screen go back to email landing screen
        UI Flow is from email details screen -> email landing screen
        '''
        self.dial_common_operations.back_button_press(self.SCAN_EMAIL_DETAILS_VIEW, self.SCAN_EMAIL_LANDING_VIEW, 3)

    def back_to_email_landing_view_from_scan_settings(self):
        '''
        From scan settigns screen go back to email landing screen
        UI Flow is from email scan settings screen -> email landing view
        '''
        self.dial_common_operations.back_button_press(self.scan_operations.SCAN_SETTINGS_VIEW, self.SCAN_EMAIL_LANDING_VIEW, 3)

    #Email Functional Keywords
    
    def email_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, dial_value)
        sleep(2)

        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()

    def wait_for_email_send_landing_view(self):
        '''
        UI wait for email landing view.
        '''
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 15.0)        

    def email_send_with_encryption(self):
        '''
        From email details screen navigate to pdf encryption password prompt
        UI Flow is select email details -> pdf encryption password prompt
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_PDF_ENCRYPTION_PROMPT_VIEW)
        logging.info("At PDF Encryption prompt view")

    def cancel_email_send(self):
        '''
        From email send progress screen click on cancel button
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.scan_usb.SCAN_PROGRESS_VIEW, timeout = 9.0)
        assert self._spice.wait_until(self.scan_usb.SCAN_PROGRESS_CANCEL)
        logging.info("Back to email landing view")

    def email_details_to_address_remove_contact(self):
        '''
        In scan email remove contact screen, remove contact
        UI Flow is from email remove contact screen -> click on Remove
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_REMOVE_CONTACT_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW)
        logging.info("Back to email details Screen")

    def email_details_to_address_remove_contact_cancel(self):
        '''
        From scan email remove contact screen go back to email details screen by clicking cancel
        UI Flow is from email remove contact screen -> click on Cancel
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_REMOVE_CONTACT_CANCEL_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW)
        logging.info("Back to email details Screen")

    def email_setup_profile_hp_software_click_ok(self):
        '''
        From scan email setup profile using HP Software screen click on Ok button
        UI Flow is from set up email profile using Hp Software screen -> click Ok button
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SETUP_USING_HP_SOFTWARE_OK_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SETUP_PROFILE_VIEW)
        logging.info("Back to Email Profile Setup Main Screen")

    def email_setup_profile_web_browser_click_ok(self):
        '''
        From scan email setup profile using web browser screen click on Ok button
        UI Flow is from set up email profile using web browser screen -> click Ok button
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SETUP_USING_WEB_BROWSER_OK_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SETUP_PROFILE_VIEW)
        logging.info("Back to Email Profile Setup Main Screen")

    def email_enter_pin(self, text: str):
        '''
        Once inside the keyboard view enter the pin
        UI Flow is keyboard view -> enter pin passed as argument
        Note - PIN has to be a 4 digit number
        '''
        assert self._spice.wait_for(self.SCAN_EMAIL_PIN_KEYBOARD_VIEW, timeout = 9.0)
        logging.info("Inside enter pin keyboard view")
        self.dial_keyboard_operations.keyboard_enter_text(text, False)
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)
        logging.info("Pin entered successfully")

    def email_enter_wrong_pin(self, text: str):
        '''
        Once inside the keyboard view enter the wrong pin
        UI Flow is keyboard view -> enter the wrong pin passed as argument
        Note - PIN has to be a 4 digit number
        '''
        assert self._spice.wait_for(self.SCAN_EMAIL_PIN_KEYBOARD_VIEW, timeout = 9.0)
        logging.info("Inside enter pin keyboard view")
        self.dial_keyboard_operations.keyboard_enter_text(text, False)
        assert self._spice.wait_for(self.scan_usb.SCAN_STATUS_ERROR_VIEW)
        #assert self._spice.wait_until(self.)

    def email_select_profile(self, cdm, udw, name: str):
        '''
        Once inside email home, select the profile
        UI Flow is Email home -> select the email profile
        Arg:
        name -> is the name provided in the display_name field while creating email profile
        cdm -> cdm instance
        udw -> udw instance
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_SELECT_PROFILE_VIEW, timeout = 15.0)
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = '#smtpServer'+server_id
        logging.info("Objectname obtained for SMTP server profile")
        self.dial_common_operations.goto_item(SCAN_EMAIL_PROFILE, "#ButtonListLayout")
        logging.info("Successfully selected email profile")

    def email_details_enter_text_to_field(self, text: str):
        '''
        This is helper method to enter text into any of the fields under Email Details screen
        UI flow is common keyboard view -> enter text
        '''
        assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.dial_keyboard_operations.keyboard_enter_text(text)
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW)
    
    def email_details_filename_empty_and_verify_error(self):
        '''
        This is helper method to verity empty file name error popup.
        '''        
        assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        self.dial_keyboard_operations.keyboard_clear_text()
        self.dial_keyboard_operations.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", 0)
        sleep(2)
        #assert self._spice.query_item("#Version1Text",4)["text"] == "Unavailable"
        assert self._spice.wait_for("#MessageLayout")
        assert self._spice.query_item("#okButton")
        
    def enter_new_email_address(self, text: str):
        '''
        This is helper method to enter new email address
        UI flow is common keyboard -> enter new email address
        '''
        #assert self._spice.wait_for(self.scan_usb.COMMON_KEYBOARD_VIEW, timeout = 9.0)
        assert self._spice.wait_for(self.SCAN_EMAIL_NEW_ADDRESS_VIEW, timeout = 9.0)
        sleep(2)
        self.dial_keyboard_operations.keyboard_enter_text(text)
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)

    def pdf_encryption_screen_cancel(self):
        '''
        This is helper method to click on cancel in the pdf encryption password screen
        UI flow is pdf encryption password screen -> cancel
        '''
        self.scan_operations.pdf_encryption_cancel(self.SCAN_EMAIL_LANDING_VIEW)
    
    def select_email_quickset(self, quickset_name):
        '''
        This is helper method to select email quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        self.dial_common_operations.goto_item(quickset_name, self.SCAN_EMAIL_QUICKSET_LIST_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)

    def select_email_quickset_entered_from_menu_quickset_shortcut(self, quickset_name):
        """
        This is helper method to select email quickset
        For entered quickset as following step: Menu->Quick Sets and Shortcuts
        """
        self.dial_common_operations.goto_item(quickset_name, self.SCAN_EMAIL_QUICKSET_LANDING_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)
    
    def goto_email_quickset_view(self):
        '''
        This is helper method to goto email quickset
        UI flow Select Landing-> click on any quickset button
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_QUICKSET_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_EMAIL_QUICKSET_LIST_VIEW)

    def check_spec_on_scan_to_email_application_screen(self, spice, net, email_address):
        """
        Check spec on scan to email application screen
        @param spice: 
        @param email_address: 
        @param net: 
        """
        logging.info("check the string on current screen")

        #spice.common_operations.verify_string(net, "cScanToEmailSettings","#LandingLayoutView #Version1Text")
        # check scan to email
        spice.common_operations.verify_string(net, "cScanToEmailSettings","#TitleText")
        #send
        spice.common_operations.verify_string(net, "cSend", "#SendButton")
        #defaults and quckets
        spice.common_operations.verify_string(net, "cDefaultsAndQuickSets", "#NameText")
        #options
        spice.common_operations.verify_string(net, "cOptions", "#OptionsButton")
        expected_email_address_str = spice.common_operations.get_expected_translation_str_by_str_id(net, "cSendParameter", "en-US").replace("%1$s + %2$d", email_address)
        logging.info(f"expected email address string for sending to is <{expected_email_address_str}>")
        actual_email_address_str = spice.common_operations.get_actual_str("#SendToButton")
        assert expected_email_address_str == actual_email_address_str, "Spec check failed"

    def check_loading_screen_for_selected_quickset(self, net):
        excepted_str = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        loading_view = self._spice.wait_for("#processingscreen SpiceText", 20)
        assert excepted_str == loading_view["text"], "Failed to find loading screen"
        logging.info("loading screen is shown at scan quickset screen")

    def wait_for_scan_loading_toast_display(self, time_out= 30):
        logging.info("check the status after scan")
        self._spice.wait_for("#ToastSystemToastStackView", time_out)
        #todo: update the method for complete status
    
    def save_as_default(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_SAVE_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, 0, True)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_AS_DEFAULT_BUTTON, self.SCAN_EMAIL_QUICKSET_SAVE_OPTION_VIEW, 180, True)
        self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)

    def verify_selected_quickset(self, net, string_id):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check EmailQuicksetSelected Button
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_QUICKSET_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, 180, False)
        assert self._spice.query_item(self.SCAN_EMAIL_QUICKSET_BUTTON+ " SpiceText")["text"] ==  LocalizationHelper.get_string_translation(net, string_id)

    def start_scan_email_job_with_settings(self, job, cdm, udw, name: str, recordId, scan_options: Dict, scan_more_pages: bool = False):
        '''
        Start scan to email with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        cdm -> cdm instance
        udw -> udw instance
        name -> is the name provided in the display_name field while creating email profile
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
        self.goto_email_options_from_home(cdm, udw, name, recordId)

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
        self.back_to_email_landing_view_from_scan_settings()
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 9.0)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, 0)
        
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()

    def add_page_pop_up_finish(self):
        self._spice.wait_for("#MessageLayout", timeout = 9.0)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_ADD_PAGE_FINISH_BUTTON, "#MessageLayout")

    def verify_error_msg_email_send_without_recipient(self, net):
        '''
        From email landing view click on send button and check for error prompt
        UI Flow is email landing view -> send -> error prompt
        '''
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_TO_ADDRESS_EMPTY_LIST_VIEW, timeout=9.0)
        # verify the message content by comparing the ui content with the stringid in the specification
        self.scan_operations.verify_string(net, "#Version2Text", "cNoRecipients", 5)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_TO_ADDRESS_EMPTY_OK_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW)
        logging.info("Back to email landing view")
    
    def save_to_email_quickset_default(self, cdm, udw, name, recordId, scan_options:Dict):
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
        self.goto_email_options_from_home(cdm, udw, name, recordId)
        
        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanEmail"
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
        
        self.back_to_email_landing_view_from_scan_settings()
        assert self._spice.wait_for(self.SCAN_EMAIL_LANDING_VIEW, timeout = 9.0)
        self.save_as_default()

    def goto_email_send_when_default_profile_is_set(self):
        self.dial_common_operations.goto_item(self.SCAN_EMAIL, "#ButtonListLayout")
        sleep(2)

    def select_email_profile_from_email_landing_view(self, cdm, udw, name: str):
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_LANDING_VIEW_SEND_TO_BUTTON, self.SCAN_EMAIL_LANDING_VIEW, dial_value = 0)
        assert self._spice.wait_for(self.SCAN_EMAIL_DETAILS_VIEW, timeout = 9.0)
        sleep(2)
        self.dial_common_operations.goto_item(self.SCAN_EMAIL_DETAILS_FROM_ADDRESS, self.SCAN_EMAIL_LANDING_VIEW, dial_value = 180)
        sleep(2)
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = '#smtpServer'+ server_id
        logging.info("Objectname obtained for SMTP server profile")
        self.dial_common_operations.goto_item(SCAN_EMAIL_PROFILE, "#ButtonListLayout")        
        sleep(2)
        self.dial_common_operations.back_button_press(self.SCAN_EMAIL_DETAILS_VIEW, self.SCAN_EMAIL_LANDING_VIEW, 2)
        sleep(2)

    def goto_email_quickset_options_from_default(self):
        """
        Send scan to email _defult
        """
        self._spice.common_operations.goto_item(r"#EmailQuickSetSelectedButton","#EmailAppApplicationStackView")
