from dunetuf.ui.uioperations.BaseOperations.IEmailAppUIOperations import IEmailAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.send.email.email import *
from dunetuf.addressBook.addressBook import *
import logging
import time
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.send.common.common import Common as ScanCommon


special_char_keys ={
    "@":"#keyAt", "#":"#keyNumberSign", "%":"#keyPercent", "&":"#keyAmpersand", "*":"#keyAsterisk", "-":"#keyMinus",
    "+":"#keyPlus", "(":"#keyParentLeft", ")":"#keyParentRight", "!":"#keyExclam", "<":"#keyLess", ">":"#keyGreater",
    "'":"#keyApostrophe", ":":"#keyColon", ";":"#keySemicolon", "?":"#keyQuestion", "{":"#keyBraceLeft", "/":"#keySlash", 
    "~":"#keyAsciiTilde", "`":"#keyAgrave", "|":"#keyBar", ".":"#keyPeriod", "√":"#keySquareroot", "÷":"#keyDivision",
    "×":"#keyMultiply", "½":"#keyOnehalf", "{":"#keyBraceLeft", "}":"#keyBraceRight", "$":"#keyDollar", "€":"#keyEuro",
    "£":"#keyPound", "¢":"#keyCent", "¥": "#keyYen", "=":"#keyEqual", "§":"#keySection", "[":"#keyBracketLeft",
    "]":"#keyBracketRight", "_":"#keyUnderScore", "™":"#keyTradeMark", "®":"#keyRegisterMark", "«":"#keyGuillemotleft",
    "»":"#keyGuillemotright", "^": "#keyAsciiCircum" , ",":"#keyComma"
}
class EmailAppWorkflowUICommonOperations(IEmailAppUIOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.homemenu = spice.menu_operations

    def goto_email_send_options(self):
        """
        Navigates to Scan then Email screen starting from Home screen.
        UI Flow is Main menu->Scan->Email
        """
        self.scan_operations.goto_scan_app()
        self.workflow_common_operations.scroll_position(EmailAppWorkflowObjectIds.view_scan_screen, EmailAppWorkflowObjectIds.button_scan_email_home , EmailAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , EmailAppWorkflowObjectIds.scanFolderPage_column_name , EmailAppWorkflowObjectIds.scanFolderPage_Content_Item)
        button_email = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        button_email.mouse_click()
        # Need to Uncomment with proper view ID.
        # self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_profile_view, timeout=9.0)
        #self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_profile_view, timeout=9.0)
        logging.info("Inside scan to email")

    def goto_email(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        button_email = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea", timeout=25)
        self.spice.validate_button(button_email)
        button_email.mouse_click()
        # Need to Uncomment with proper view ID.
        # self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_profile_view, timeout=9.0)
        logging.info("Inside scan to email")

    def check_scan_email_button(self):
        """
        Purpose: check if scan to email under Scan app is visible or not.
        @return: visible
        """
        try:
            self.spice.wait_for(
                EmailAppWorkflowObjectIds.button_scan_email_home) 
            visible = True
        except:
            visible = False

        logging.info(
            "[check_scan_email_button] visible={}".format(visible))
        return visible

    def goto_email_userdefined_email_profile(self,  cdm, udw,name: str):
        button_email = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        self.spice.wait_until(lambda: button_email["visible"] == True)
        button_email.mouse_click()
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_profile_view)
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
        assert self.scrollto_emailfolder_in_profile_selection(SCAN_EMAIL_PROFILE)
        current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 20.0)
        time.sleep(2)
        current_button.mouse_click()
        
        logging.info("Inside scan to email")

    def goto_scan_to_usb(self):
        button_usb = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_usb + " MouseArea")
        self.spice.wait_until(lambda: button_usb["visible"] == True)
        button_usb.mouse_click()
        logging.info("Inside scan to usb")

    def goto_email_home(self):
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home)
        button_email = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home + " MouseArea")
        button_email.mouse_click()
        logging.info("Inside scan to email")

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
    
    def goto_email_setup_screen_from_home_scanapp(self):
        """
        Navigates to EmailSetupApp from Scan app at Home screen.
        UI Flow is Home->Scan->EmailSetupApp
        """
        self.spice.common_operations.goto_scan_app()
        self.spice.scan_settings.goto_email_from_scanapp_at_home_screen()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.email_setup_select_method_screen)
    
    def goto_hp_server_screen(self):
        """
        Navigates to HP Server screen from Email Setup screen.
        UI Flow is EmailSetupApp->HP Server
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.EmailSetUpView)
        button_hp_server = self.spice.wait_for(EmailAppWorkflowObjectIds.hp_server_row)
        button_hp_server.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.hp_server_info_screen)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.hp_server_continue_button)     
            
    def goto_smtp_server_screen(self):
        """
        Navigates to SMTP Server screen from Email Setup screen.
        UI Flow is EmailSetupApp->SMTP Server
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.EmailSetUpView)
        button_smtp_server = self.spice.wait_for(EmailAppWorkflowObjectIds.smtp_server_row)
        button_smtp_server.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.smtp_server_info_screen)
        
        

    def goto_menu_email_emailsetup(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Email Settings -> Email Setup
        Args: None
        """
        self.homemenu.goto_menu_settings_email(self.spice)
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_emailSetupMenuButton)
    
    def check_description_message_for_smtpaddress(self, net):
        '''
        Check description message  for smtpaddress
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNoticeSMTPServerChange", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{EmailAppWorkflowObjectIds.textbox_serverName} {EmailAppWorkflowObjectIds   .textbox_descriptionText}",isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str

    def got_to_email_server_setup_view(self):
        '''
        Navigate to email setup view
        '''
        okButton = self.spice.wait_for(EmailAppWorkflowObjectIds.button_emailSetupMenuButton)
        okButton.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.EmailSetUpView)
        logging.info("At EmailSetUp App Screen")

    def click_servername_row(self):
        '''
        Click server name row
        '''
        serverButton = self.spice.wait_for(EmailAppWorkflowObjectIds.leftPanel_serverName)
        serverButton.mouse_click()

    def check_server_address(self, responseGet):
        '''
        Check server address
        '''
        if responseGet['servers'] :
            serverAddress = responseGet['servers'][0]['serverAddress']
            assert self.spice.wait_for("#serviceNameFieldModel #TextInputBox",2)["text"] == serverAddress

    def click_email_server_row(self):
        '''
        Click email server row
        '''
        emailButton = self.spice.wait_for(EmailAppWorkflowObjectIds.leftPanel_email_server_row)
        self.spice.validate_button(emailButton)
        emailButton.mouse_click()

    def click_credential_row(self):
        '''
        Click credential row
        '''
        credentialsRowButton = self.spice.wait_for(EmailAppWorkflowObjectIds.leftPanel_cerdentials_row)
        self.spice.validate_button(credentialsRowButton)
        credentialsRowButton.mouse_click()

    def click_help_me_find_smtp(self):
        '''
        Click help me find smtp
        '''
        # helpmeFindSmtpButton = self.spice.wait_for("#helpmySmtp #helpsmtpModel")
        helpmeFindSmtpButton = self.spice.wait_for("#helpsmtpModel")
        self.workflow_common_operations.goto_item(["#helpmySmtp","#helpsmtpModel"], screen_id = EmailAppWorkflowObjectIds.email_setup_view_list, scrollbar_objectname = EmailAppWorkflowObjectIds.email_setup_view_list_scroll_bar)

    def click_back_button(self):
        '''
        Click back button
        '''
        backButton = self.spice.wait_for("#autoFindSmtpServerListHeader #BackButton")
        backButton.mouse_click()

    def verify_authentication_checked(self):
        '''
        Verify authentication checked
        '''
        return self.spice.wait_for("#authenticationCheckBoxRow #authenticationCheckBoxModel")["checked"] == True

    def verify_always_credential_visible(self):
        '''
        Verify always credential visible
        '''
        return self.spice.wait_for("#alwaysCredentials #alwaysCredentialsModel")["visible"] == True

    def verify_username(self, responseGet):
        '''
        Verify username
        '''
        if responseGet['servers'] :
            return self.spice.wait_for("#userNameFieldRow #TextInputBox")["text"] == responseGet['servers'][0]['credential']['userName']

    def verify_always_credential_constraint(self):
        '''
        Verify always credential constraint
        '''
        element = self.spice.wait_for("#alwaysCredentials #alwaysCredentialsModel")
        self.spice.validate_button(element)
        return element["constrained"] == True

    def config_smtp_server(self, cdm, smtp, resource):
        '''
        Configure smtp server
        '''
        response = cdm.put_raw(smtp,resource)
        assert response.status_code == 200

    def back_to_scan_home_from_send_to_options(self):
        '''
        Navigate back to scan home from send to options screen
        UI Flow is send to options view -> scan home view
        '''
        #self.workflow_common_operations.back_button_press(EmailAppWorkflowObjectIds.button_back, EmailAppWorkflowObjectIds.view_email_option)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        time.sleep(5)

    def back_to_main_ui_from_scan_home(self):
        '''
        Navigate back to main ui from scan home
        UI flow is scan home -> main ui
        '''        
        try:
            self.workflow_common_operations.back_button_press(screen_id = "#SpiceViewButtonTemplateView", landing_view = MenuAppWorkflowObjectIds.view_homeScreen)
        except:
            # May be traversed via Menu Navigation
            back_button = self.spice.wait_for("#SpiceHeaderVar2 #SpiceBreadcrumb #BackButton")
            back_button.mouse_click()

    def select_send_to_contacts(self):
        '''
        From send options screen navigate to send to contacts screen
        UI Flow is Send Options -> Send to contacts
        '''
        try:
            self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_option, timeout=20.0)
        except:
            self.goto_email_options()
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.textbox_email_to_field,EmailAppWorkflowObjectIds.button_email_to_addressbook],
                                                  EmailAppWorkflowObjectIds.view_email_option, scrollbar_objectname =EmailAppWorkflowObjectIds.scroll_bar_email_options)
        
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local, timeout=20.0)
        time.sleep (2)
        button_addressbook_local = self.spice.query_item(EmailAppWorkflowObjectIds.button_addressbook_local)
        button_addressbook_local.mouse_click()
        logging.info("Inside Contacts Screen")
        time.sleep(1)

    def select_and_specify_send_to_contacts(self, cdm, recordId):
        '''
        Method that will try to select To email from interactive summary
        If cannot, try to select from address book in more options

        @param:
            cdm: cdm object
            recordId: recordId of the contact
        '''
        if not self.try_select_contact_at_interactive_summary(cdm, recordId):
            self.select_send_to_contacts()
            self.select_specific_email_contact(cdm, recordId)

    def select_send_to_contacts_from_drop_down_options(self):
        '''
        From send options screen navigate to send to contacts screen
        UI Flow is Send Options -> Send to contacts
        '''
        try:
            button_drop_down = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_dropDown)
            button_drop_down.mouse_click()
            time.sleep (1)
        except:
            print("More options button not displayed.")

        self.workflow_common_operations.scroll_to_position_vertical_without_scrollbar(EmailAppWorkflowObjectIds.button_email_options_from_dropDown)
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.textbox_email_to_field,EmailAppWorkflowObjectIds.button_email_to_addressbook],
                                                  EmailAppWorkflowObjectIds.view_email_option, scrollbar_objectname =EmailAppWorkflowObjectIds.scroll_bar_email_options)
        
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        time.sleep (2)
        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        button_addressbook_local.mouse_click()
        logging.info("Inside Contacts Screen")
        time.sleep(1)
        
    def select_contact_at_interactive_summary(self, cdm, recordId):
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field)
        # I have tried to wait for this button visible and enabled propertied and clicking it.
        # Test clicks but UI doesn't recognize it and signal isn't launched.
        # So I'm waiting a bit.
        time.sleep (2)
        addressbook_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook)
        addressbook_button.mouse_click()
        time.sleep (2)
        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        button_addressbook_local.mouse_click()
        time.sleep(2)
        self.select_specific_email_contact_from_interactivesummary(cdm, recordId)

    def try_select_contact_at_interactive_summary(self, cdm, recordId):
        result=False
        if self.spice.check_item(EmailAppWorkflowObjectIds.textbox_email_to_field):
            addressbook_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook )
            addressbook_button.mouse_click()
            # I have tried to wait for this button visible and enabled propertied and clicking it.
            # Test clicks but UI doesn't recognize it and signal isn't launched.
            # So I'm waiting a bit.
            time.sleep (2)
            button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
            button_addressbook_local.mouse_click()
            time.sleep(2)
            self.select_specific_email_contact_from_interactivesummary(cdm, recordId)
            result=True
        
        return result
    
    def select_cc_contact_at_interactive_summary(self, cdm, recordId):
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_cc_field)
        time.sleep (2)
        addressbook_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cc_addressbook )
        addressbook_button.mouse_click()
        time.sleep (2)
        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        button_addressbook_local.mouse_click()
        time.sleep(2)
        self.select_specific_email_contact_from_interactivesummary(cdm, recordId)

        
    def goto_local_contacts_from_scan_to_email_landing_view(self, cdm):
        '''
        Go to local contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click toAddressBookButton -> email address book-> local
        '''
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook)
        self.spice.validate_button(email_address_btn)
        # I have tried to wait for this button visible and enabled propertied and clicking it.
        # Test clicks but UI doesn't recognize it and signal isn't launched.
        # So I'm waiting a bit.
        time.sleep(2)
        email_address_btn.mouse_click()
        
        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view, timeout=50.0)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True , timeout=30.0)
        
        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        # + " #SpiceView")
        self.spice.wait_until(lambda: button_addressbook_local["visible"]==True)
        self.spice.wait_until(lambda: button_addressbook_local["enabled"] == True)
        button_addressbook_local.mouse_click()
        logging.info("Inside Contacts Screen")
    
    def goto_from_addressbook_in_scan_to_email(self, cdm):
        '''
        Go to local contacts for from address from scan to email landing view
        UI Flow is scan to email landing view, click toAddressBookButton -> email address book-> local
        '''
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_from_field, EmailAppWorkflowObjectIds.screen_email_interactive_summary, select_option=False, scrolling_value=0.06,scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_from_more_options)
        self.spice.validate_button(email_address_btn)
        time.sleep(2)
        email_address_btn.mouse_click()
        from_addressbook_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.from_address_book)
        self.spice.validate_button(from_addressbook_btn)
        from_addressbook_btn.mouse_click()
        
        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)
        
        button_addressbook_local = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_local)
        self.spice.wait_until(lambda: button_addressbook_local["visible"]==True)
        button_addressbook_local.mouse_click()
        logging.info("Inside Contacts Screen")
    
    def goto_custom_contacts_from_scan_to_email_landing_view(self, custom_address_name):
        '''
        Go to custom contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click toAddressBookButton -> email address book-> custom address
        Args: custom_address_name
        '''
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook)
        self.spice.validate_button(email_address_btn)
        email_address_btn.mouse_click()

        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)

        button_addressbook_custom = self.spice.wait_for(f"#addressbook_{custom_address_name}")
        button_addressbook_custom.mouse_click()
        logging.info("Inside Contacts Screen")

    def goto_custom_contacts_for_cc_address_from_scan_to_email_landing_view(self,cdm , custom_address_name , recordId):
        '''
        Go to custom contacts for cc address from scan to email landing view
        UI Flow is scan to email landing view, click ccAddressBookButton -> email address book-> custom address
        Args: custom_address_name
        '''
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cc_addressbook)
        self.spice.validate_button(email_address_btn)
        email_address_btn.mouse_click()

        time.sleep (2)
        addressbook_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cc_addressbook)
        addressbook_button.mouse_click()
        time.sleep (2)
        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)

        button_addressbook_custom = self.spice.wait_for(f"#addressbook_{custom_address_name}")
        button_addressbook_custom.mouse_click()
        logging.info("Inside Contacts Screen")
        self.select_specific_email_contact_from_interactivesummary(cdm, recordId)

    def goto_ldap_contacts_for_cc_address_from_scan_to_email_landing_view(self):
        '''
        Go to ldap contacts for cc address from scan to email landing view
        UI Flow is scan to email landing view, click ccAddressBookButton -> email address book-> ldap
        '''
        # wait for this button visible and enabled propertied and clicking it.
        # Test clicks but UI doesn't recognize it and signal isn't launched.
        # So waiting a bit.
        time.sleep(2)
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cc_addressbook)
        self.spice.validate_button(email_address_btn)
        email_address_btn.mouse_click()
        
        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.select_address_book_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)
        
        button_addressbook_ldap = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_ldap)
        self.spice.wait_until(lambda: button_addressbook_ldap["visible"]==True)
        button_addressbook_ldap.mouse_click()

        ldap_address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.validate_button(ldap_address_book_screen)
        logging.info("Inside LDAP Contacts Screen")

    def goto_ldap_contacts_from_scan_to_email_landing_view(self):
        '''
        Go to ldap contacts for To address from scan to email landing view
        UI Flow is scan to email landing view, click to AddressBookButton -> email address book-> ldap
        '''
        # I have tried to wait for this button visible and enabled propertied and clicking it.
        # Test clicks but UI doesn't recognize it and signal isn't launched.
        # So I'm waiting a bit.
        time.sleep(2)
        email_address_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_to_addressbook)
        self.spice.validate_button(email_address_btn)
        email_address_btn.mouse_click()
        
        address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_contacts_view)
        self.spice.wait_until(lambda: address_book_screen["visible"]==True)
        
        button_addressbook_ldap = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_ldap)
        self.spice.wait_until(lambda: button_addressbook_ldap["visible"]==True)
        button_addressbook_ldap.mouse_click()

        ldap_address_book_screen = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.validate_button(ldap_address_book_screen)
        logging.info("Inside LDAP Contacts Screen")
    
    def select_ldap_address_book(self):
        '''
        select ldap address book in select address book screen
        UI Flow should be in scan to email landing view, click to AddressBookButton -> select address book screen
        '''
        button_addressbook_ldap = self.spice.wait_for(EmailAppWorkflowObjectIds.button_addressbook_ldap)
        self.spice.wait_until(lambda: button_addressbook_ldap["visible"]==True)
        button_addressbook_ldap.mouse_click()
    
    def check_spec_search_contacts_ldap_addressbook(self, net):
        '''
        Check spec search contacts 'Search to view a list of contacts' when select LDAP address book
        '''
        logging.info("Check spec search contacts when select LDAP address book")
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        actual_text = self.spice.wait_for(EmailAppWorkflowObjectIds.text_view_empty_record)["text"]
        expected_text = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cSearchContacts")
        assert actual_text == expected_text, "Failed to check spec search contacts when select LDAP address book"

    def goto_search_model_view_from_ldap_contacts(self):
        '''
        Go to search model view for search contact from ldap contacts view
        UI Flow is ldap contacts view, click to Search Button -> search model view
        '''
        logging.info("Click Search button")
        search_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_search_header_right, timeout=15.0)
        self.spice.validate_button(search_btn)
        search_btn.mouse_click(6)
        logging.info("Goto search model view from ldap contacts")
        time.sleep(2)
        search_model_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_search_model_screen, timeout=15.0)
        self.spice.wait_until(lambda: search_model_view["visible"]==True)

    def input_search_contact_name(self, search_str):
        """
        Purpose: Enter search string.
        UI Flow is search model view, click Type here text field -> keyboard-> enter search string
        Args: search string which is provided on the test case
        """
        logging.info("Click Type here text field")
        contact_name_input_field = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_contact_name_to_field_text)
        contact_name_input_field.mouse_click()
        logging.info("Input a search string")
        self.input_text_from_keyboard(search_str)
        key_ok  = self.spice.wait_for(EmailAppWorkflowObjectIds.hide_keyboard_key)
        key_ok.mouse_click()
    
    def click_cancel_button_in_search_screen(self):
        """
        Click cancel button in search screen.
        """
        cancel_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_cancel_body_row)
        self.spice.validate_button(cancel_button)
        cancel_button.mouse_click()
    
    def click_reset_button(self):
        '''
        click reset button on search result contacts landing view screen
        '''
        reset_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_reset)
        self.spice.validate_button(reset_button)
        reset_button.mouse_click()

    def check_keyboard_open_on_setting(self):
        """
        Purpose: Check if keyboard opens on click of a setting(toField/fromField/subject) search string.
        UI Flow click  field -> keyboard -> click Ok
        """
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def search_input_contact_name_in_search_model_view(self):
        """
        Purpose: search input search string.
        UI Flow is search model view, click search button for search string
        """
        logging.info("Click Search button")
        search_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_search_body_row)
        self.spice.validate_button(search_btn)
        search_btn.mouse_click()
    
    def check_search_result_number_in_contacts_list_view(self, expected_contacts_list):
        """
        Check Search Result numbers shows in contacts list view screen.
        @param:expected_file_list: 
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        result_text_box = self.spice.wait_for(EmailAppWorkflowObjectIds.view_search_result_number_text)
        self.spice.wait_until(lambda:result_text_box['visible']== True)
        result_message = result_text_box["text"]
        assert len(expected_contacts_list) == int(result_message), "Search result numbers is error"
        logging.info("check search result number success")

    def check_contacts_display_name_in_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list: the contacts list should be sorted
        @return:
        """
        local_contact_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.wait_until(lambda: local_contact_view["visible"]==True)
        
        time.sleep(2)
        for contact_name in expected_contact_list:
            contacts_name_item = '#checkBox_'+ contact_name + 'Row'
            logging.info(f"Contacts name is: <{contact_name}>")
            self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, contacts_name_item, scroll_height=86)
            self.spice.wait_for(contacts_name_item)
            logging.info(f"-found:{contact_name}")
        
        logging.info(f"Check contacts name list {expected_contact_list} success")
    
    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list: 
        @return: contacts_name_list the contacts list should be sorted
        """
        # Wait all contacts load completed
        time.sleep(2)
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)

        contact_name_to_y_list = []

        for contacts_name in expect_contacts_list:
            item_object_name = f'#checkBox_{contacts_name}Row'
            self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, item_object_name, scroll_height=86)

            y_coordinate = self.spice.wait_for(item_object_name)["y"]
            contact_name_to_y_list.append({
                "contacts_name": contacts_name,
                "y_coordinate": y_coordinate
            })
            logging.info(f"(get_sorted_contacts_name_list) -found with scroll:{contacts_name}, {y_coordinate}")

        logging.info("(get_sorted_contacts_name_list) sorted list by y coordinate")
        contact_name_to_y_list.sort(key = lambda item: item["y_coordinate"])
        logging.info("(get_sorted_contacts_name_list) get contacts name list sorted by y coordinate")
        contacts_name_list = [i["contacts_name"] for i in contact_name_to_y_list]
        logging.info(f"(get_sorted_contacts_name_list) contacts name list after sorted by y coordinate is <{contacts_name_list}>")
        return contacts_name_list
    
    def select_available_contact_from_ldap_contacts_view(self, display_name):
        '''
        Select contacts from ldap contacts view
        UI Flow: Ldap contact screen -> select contact -> Back to send to email landing screen
        Args: display_name which is provided on the test case
        '''
        logging.info("In ldap contacts screen")
        ldap_contact_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.wait_until(lambda: ldap_contact_view["visible"]==True)

        contact_name = f'#checkBox_{display_name}Model'
        logging.info(f"Contacts name is: <{contact_name}>")
        self.spice.wait_for(contact_name)
        checkbox_contact = self.spice.wait_for(contact_name)
        checkbox_contact.mouse_click()
        button_select = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)
        self.spice.validate_button(button_select)
        button_select.mouse_click()
        email_landing_view=self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda: email_landing_view["visible"]==True)
        
    def verify_group_email_contact_avaialble(self, cdm, recordId):
        '''
        Check group email contact available
        '''
        ab= AddressBook(cdm, None)
        display_name = ab.get_addressBook_display_name(recordId)
        local_contact_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.wait_until(lambda: local_contact_view["visible"]==True)
        contact_name = f'#radioButton_{display_name}Model'
        logging.info(f"Contacts name is: <{contact_name}>")
        assert contact_name not in ScanAppWorkflowObjectIds.contacts_list_view, "Display name is present on the screen"
        button_cancel = self.spice.query_item(EmailAppWorkflowObjectIds.button_email_addressbook_cancel,1)
        button_cancel.mouse_click()
        time.sleep(2)
        email_landing_view=self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda: email_landing_view["visible"]==True)
        
    def select_specific_email_contact_from_landing_view(self, cdm, recordId):
        '''
        Select contacts for To address from scan to email landing view
        UI Flow: Local contact screen -> select specific contact -> Back to send to email landing screen
        '''
        ab= AddressBook(cdm, None)
        display_name = ab.get_addressBook_display_name(recordId)
        
        local_contact_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.wait_until(lambda: local_contact_view["visible"]==True)
        contacts_name = '#checkBox_'+ display_name + 'Model'
        logging.info(f"Contacts name is: <{contacts_name}>")
        self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, f"#checkBox_{display_name}Row", scroll_height=86)
        checkbox_contact = self.spice.wait_for(contacts_name)
        checkbox_contact.mouse_click()
        self.spice.wait_until(lambda:checkbox_contact["checked"])

        button_select = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)
        self.spice.validate_button(button_select)
        button_select.mouse_click()
        email_landing_view=self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda: email_landing_view["visible"]==True)
    
    def select_specific_email_groups_from_landing_view(self, cdm, group_name):
        '''
        Select Groups for To address from scan to email landing view
        UI Flow: Local contact screen -> select specific groups -> Back to send to email landing screen
        '''
        local_contact_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_local_contact_screen)
        self.spice.wait_until(lambda: local_contact_view["visible"]==True,timeout=20.0)
        contacts_name = '#checkBox_'+ group_name + 'Model'
        logging.info(f"Contacts name is: <{contacts_name}>")
        self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, f"#checkBox_{group_name}Row", scroll_height=30)
        checkbox_contact = self.spice.wait_for(contacts_name)
        self.spice.wait_until(lambda: checkbox_contact["visible"]==True)
        self.spice.wait_until(lambda: checkbox_contact["enabled"] == True)
        checkbox_contact.mouse_click()
        self.spice.wait_until(lambda:checkbox_contact["checked"])

        button_select = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)
        self.spice.validate_button(button_select)
        button_select.mouse_click()
        email_landing_view=self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda: email_landing_view["visible"]==True)

    def change_keyboard_shift_to_upper_case(self):
        '''
        Purpose: Change keyboard shift to upper case
        UI Flow is scan to email landing view, click To address text field -> keyboard
        '''
        if self.spice.wait_for("#symbolModeKey")["displayText"] == "abc":    
            self.keyboard_press_icon("#symbolModeKey")
        key_shift_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)
        self.spice.validate_button(key_shift_button)

        if self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)["uppercased"]:
            logging.info("The keyboard is already in upper case")
        else:
            logging.info("The keyboard in lower case, Change the keyboard shift to upper case")
            shift_mode_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)
            self.spice.validate_button(shift_mode_btn)
            shift_mode_btn.mouse_click()
            time.sleep(1)
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)["uppercased"], 'The keyboard shift change to upper case failed!!!'
    
    def change_keyboard_shift_to_lower_case(self):
        '''
        Purpose: Change keyboard shift to lower case
        UI Flow is scan to email landing view, click To address text field -> keyboard
        '''
        time.sleep(3)
        if self.spice.wait_for("#symbolModeKey")["displayText"] == "abc":    
            self.keyboard_press_icon("#symbolModeKey")
        time.sleep(3)
        key_shift_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)
        time.sleep(3)
        self.spice.validate_button(key_shift_button)
        
        if self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)["uppercased"]:
            logging.info("The keyboard in upper case, Change the keyboard shift to lower case")
            shift_mode_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)
            self.spice.validate_button(shift_mode_btn)
            shift_mode_btn.mouse_click()
            time.sleep(1)
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_shift_mode_keyboard)["uppercased"]==False, 'The keyboard shift change to lower case failed!!!'
        else:
            logging.info("The keyboard is already in lower case")

    def keyboard_press_icon(self, object_id, index_value = 0, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Numerics, Close, Language, Alphabet, Symbols, Space)
          dial_val: Direction for dialing
        '''
        assert self.spice.wait_for("#spiceKeyboardView")
        key = self.spice.wait_for(object_id)
        key.mouse_click()     
        time.sleep(0.5)
			        
    def input_text_from_keyboard(self, text):
        '''
        Purpose: input email address in keyboard
        UI Flow is scan to email landing view, click To address text field -> keyboard ->input email address
        '''
        for char in text:
            if char.isalpha():
                if char.isupper():
                    self.change_keyboard_shift_to_upper_case()
                    key = self.spice.wait_for("#key" + char)
                    self.spice.validate_button(key)
                    key.mouse_click()
                else:
                    self.change_keyboard_shift_to_lower_case()
                    key = self.spice.wait_for("#key" + char.upper())
                    self.spice.validate_button(key)
                    key.mouse_click()
                    time.sleep(1)
            elif char.isdigit():
                symbol_mode_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_symbol_mode_keyboard)
                self.spice.validate_button(symbol_mode_btn)
                symbol_mode_btn.mouse_click()
                key = self.spice.wait_for("#key" + char)
                self.spice.validate_button(key)
                key.mouse_click()
                time.sleep(1)
                symbol_mode_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_symbol_mode_keyboard)
                self.spice.validate_button(symbol_mode_btn)
                symbol_mode_btn.mouse_click()
                time.sleep(1)
            elif char == "@":
                key_at_btn = self.spice.wait_for(EmailAppWorkflowObjectIds.button_key_at)
                self.spice.validate_button(key_at_btn)
                key_at_btn.mouse_click()
            elif char == ".":
                try:
                    if self.spice.wait_for("#symbolModeKey")["displayText"] == "&123":
                        self.keyboard_press_icon("#symbolModeKey")    
                    key = self.spice.wait_for(special_char_keys[char], 5)
                    key.mouse_click()
                except Exception as e:
                    self.keyboard_press_icon("#key1By21")
                    key_period = self.spice.wait_for(EmailAppWorkflowObjectIds.button_key_period)
                    self.spice.validate_button(key_period)
                    key_period.mouse_click()
                finally:
                    if self.spice.wait_for("#symbolModeKey")["displayText"].lower() == "abc":
                        self.keyboard_press_icon("#symbolModeKey")
            else:
                logging.info("Unexpected character.")

    def enter_multiple_email_address(self, email_list, use_keyboard=False):
        """
        Purpose: Enter Multiple email address.
        UI Flow is scan to email landing view, click To address text field -> keyboard-> enter multi email address
        Args: email_list which is provided on the test case
        """
        email_input_field = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text + " MouseArea")
        self.spice.wait_until(lambda: email_input_field["visible"] == True)
        self.spice.wait_until(lambda: email_input_field["enabled"] == True)
        email_input_field.mouse_click(10)
        if use_keyboard:
            for email_detail in email_list:
                self.input_text_from_keyboard(email_detail)
                key_space = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_enter)
                self.spice.validate_button(key_space)
                key_space.mouse_click()
                email_input_field.mouse_click(10)

            time.sleep(3)
            key_ok  = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            key_ok.mouse_click()

        else:
            for email_detail in email_list:
                to_address_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.textbox_email_to_field_text} {EmailAppWorkflowObjectIds.text_input}")
                self.spice.validate_button(to_address_textbox)
                to_address_textbox.__setitem__('text', email_detail)
                to_address_textbox.mouse_click()
                # added wait_time to button get visible state
                time.sleep(2.5)
                keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok, timeout=45.0)
                self.spice.validate_button(keyword_ok)
                keyword_ok.mouse_click()

    def goto_email_new_address(self):
        '''
        From send options screen navigate to new address screen
        UI Flow is Send Options -> new address
        '''
        #Click on to text box
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()
        time.sleep(3)
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.textbox_email_to_field, EmailAppWorkflowObjectIds.textbox_email_to_field_text], EmailAppWorkflowObjectIds.view_email_option, scrollbar_objectname =EmailAppWorkflowObjectIds.scroll_bar_email_options)
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        # current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text)
        # current_button.mouse_click()
        # logging.info("Inside Contacts Screen")

    def select_specific_email_contact(self, cdm, recordId):
        '''
        From send to contacts screen navigate to email landing view
        UI Flow is select email contact out of multiple contacts listed -> email landing view
        '''

        ab= AddressBook(cdm, None)
        dispname = ab.get_addressBook_display_name(recordId)
        print ("dispname",dispname)
        
        self.spice.scan_settings.scroll_contact_or_group_item_into_view(ScanAppWorkflowObjectIds.contacts_list_view, f"#checkBox_{dispname}Row", scroll_height=30)
        contacts_name = '#checkBox_'+ dispname + 'Model'
        print("Contacts_name",contacts_name )
        self.spice.wait_for(contacts_name)
        checkbox_contact = self.spice.wait_for(contacts_name)
        checkbox_contact.mouse_click()
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)        
        button_select = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)
        button_select.mouse_click()
        self.back_to_landing_view_from_options_view_with_close_button()
        
    def select_specific_email_contact_from_interactivesummary(self, cdm, recordId):
        ab= AddressBook(cdm, None)
        dispname = ab.get_addressBook_display_name(recordId)
        print ("dispname",dispname)
        
        contacts_name = '#checkBox_'+ dispname + 'Model'
        print("Contacts_name",contacts_name )
        self.spice.wait_for(contacts_name)
        checkbox_contact = self.spice.wait_for(contacts_name)
        checkbox_contact.mouse_click()
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)        
        button_select = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_addressbook_select)
        button_select.mouse_click()

    def goto_to_list_button_and_select_email_contact(self):
        '''
        From send to contacts screen navigate to email Details view.
        Click on Scan to button and select email to list.
        '''
        # NA For workflow
       

    def goto_email_landing(self):
        '''
        From send to contacts screen navigate to email landing view
        UI Flow is select email contact -> email landing view
        '''
        #NA for Workflow
        # self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.email_address_book_record ,  EmailAppWorkflowObjectIds.view_email_menu_list)
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_landing_view, timeout = 9.0)
        # logging.info("Inside Email Landing View")

    def back_to_scan_app_from_email_landing(self):
        '''
        From email landing view go back to scan app
        UI FLow is email landing view -> send to scan app view
        '''
        current_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_landing_view} {EmailAppWorkflowObjectIds.button_back}")
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(2)
        # self.spice.wait_for(EmailAppWorkflowObjectIds.scan_app_landing_view)

    def  back_to_main_ui_from_scan_menu(self):
        '''
        from scan app navigates to menu app->home screen
        ui Flow is scan app ->menu app->home screen
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_scan_screen)
        current_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_scan_screen} {EmailAppWorkflowObjectIds.button_back}")
        current_button.mouse_click()
        time.sleep(2)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_home)
        current_button.mouse_click()
        

    
    def back_to_landing_view_from_options_view_with_close_button(self):
        '''
        From options view go back to landing view
        UI FLow is email options view -> send email landing view
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_back_close).mouse_click()

    def goto_email_add_recipient(self):
        '''
        From email landing view navigate to add recepient screen
        '''
        #NA For workflow
        # current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_add_recipient_button)
        # current_button.mouse_click()
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_send_to_options_view, timeout = 9.0)
        # logging.info("Inside Email add recepients (send to options)")
        
    def back_to_email_landing_view_from_add_recepient(self):
        '''
        From add recepient screen go back to email landing view
        UI Flow is add recepient screen -> email landing view
        '''
        #NA for Workflow
        # self.workflow_common_operations.back_button_press(EmailAppWorkflowObjectIds.scan_email_send_to_options_view, EmailAppWorkflowObjectIds.scan_email_landing_view)

    def goto_email_options(self):
        '''
        From email landing view navigate to options screen
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        self.spice.wait_until(lambda: current_button["visible"]==True)
        self.spice.wait_until(lambda: current_button["enabled"]==True)
        # wait for the Options icon loads successfully
        time.sleep(5)
        current_button.mouse_click()
        # wait for all options screen after clicking all options button. It needs large timeout value for NFT case.
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_option, timeout = 120.0)
        logging.info("Inside Email options")
        time.sleep(2)

    def goto_email_options_from_home(self, cdm, udw, name: str, recordId):
        '''
        From home screen navigate to options screen
        '''
        self.scan_operations.goto_scan_app()
        self.email_select_profile(cdm, udw, name)
        self.goto_email_details()
        self.goto_email_details_to_address()
        self.select_send_to_contacts()
        self.select_specific_email_contact(cdm, recordId)
        self.goto_email_options()
        logging.info("Inside Email options")
    
    def goto_email_setup_profile(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> screen with instructions to set up email profile
        '''
        time.sleep(1)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home+ " MouseArea")
        current_button.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_scansetup_no_profile)
        logging.info("Inside Email Profile Setup Screen")
    
    def goto_default_smtp_profile(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> screen with instructions to set up email profile
        '''
        time.sleep(1)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home+ " MouseArea")
        current_button.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.setup_dialog)
        logging.info("Inside Email Profile Setup Screen")

    def goto_configureSmtp(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> continue button
        '''
        time.sleep(1)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_continue)
        current_button.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.emailsetup_dialog)
        logging.info("Inside Email Profile Setup Screen")

    def cancel_smtpsetup(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> cancel configure SMTP
        '''
        time.sleep(1)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cancelSMTPDialog)
        current_button.mouse_click()
        logging.info("Going back to scan menu")

    def validate_serverName(self,net):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> cancel configure SMTP
        '''
        time.sleep(1)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_serverName} {EmailAppWorkflowObjectIds.textbox_serverName_text}").mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        self.input_text_from_keyboard("smtp@")
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        time.sleep(2)
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_serverName_text} {EmailAppWorkflowObjectIds.helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInputInvalidPattern')
        assert message == expected_string, "Invalid characters"

    def validate_defaultPort(self):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> cancel configure SMTP
        '''
        time.sleep(1)
        port_number= self.spice.wait_for(EmailAppWorkflowObjectIds.portno_text)["inputText"]
        assert port_number == "25", "to field text mismatch"

    def validate_fromAddress(self,net):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> configure SMTP -> validate from Address
        '''
        time.sleep(2)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_fromAddress} {EmailAppWorkflowObjectIds.textbox_fromAddress_text}").mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        self.input_text_from_keyboard("asdf?")
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_fromAddress_text} {EmailAppWorkflowObjectIds.helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddress')
        assert message == expected_string, "The format of the email address is invalid."

    def validateErrorMessage(self):
        '''
        From scan to email set up constrained message should be displayed
        if mandatory fields are not filled
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.next_btn)
        current_button.mouse_click()
        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_constraint_ok)
        current_button.mouse_click()

    def check_smtpauto_find_notFound(self, net):
        '''
        Check NoSmtpServersFound
        '''
        logging.info("Check NoSmtpServersFound")
        self.spice.wait_for("#errorMessage",timeout=100)
        expected_str = LocalizationHelper.get_string_translation(net, "cNoSmtpServersFound")
        actual_str = self.spice.wait_for("#errorMessage #alertDetailDescription #contentItem")["text"]
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"
        ok_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_constraint_ok)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def enter_displayName(self, display_name = "asdf"):
        '''
        From scan home screen click on email with no profile added in EWS
        UI Flow is from scan app select emai -> configure SMTP -> validate display name
        '''
        time.sleep(1)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_displayName} {EmailAppWorkflowObjectIds.textbox_displayName_text}").mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        self.input_text_from_keyboard(display_name)
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def enter_server_name(self):
        '''
        Enter server name for email setup
        '''
        time.sleep(1)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_serverName} {EmailAppWorkflowObjectIds.textbox_serverName_text}").mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        self.input_text_from_keyboard("smtp3")
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        time.sleep(2)

    def gotoNextScreen(self):
        '''
        go to next screen in email setup
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.next_btn)
        self.spice.validate_button(current_button)
        current_button.mouse_click()

    def pressFinishButton(self):
        '''
        press finish button in email setup
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.finish_btn)
        self.spice.validate_button(current_button)
        current_button.mouse_click()

    def finishSetUp(self):
        '''
        finish email setup and go to landing page
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.finish_btn)
        current_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout=25.0)
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text).mouse_click(10)
        time.sleep(2)
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        time.sleep(6)
        self.input_text_from_keyboard("abcd@hp.com")
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 20.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(2)        

    def validate_icon_status(self, objectName, expected_value):
        '''
        Validating icon status
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.leftPanel_serverName)
        contentRow = self.spice.wait_for(objectName)
        icon_value = str(contentRow["image"])
        assert icon_value == expected_value, f"Icon is not set to <{expected_value}>"
        
    def enter_from_address(self, email_address = "asdf@hp.com"):
        '''
        enter from address in email setup
        '''
        time.sleep(1)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_fromAddress} {EmailAppWorkflowObjectIds.textbox_fromAddress_text}").mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        self.input_text_from_keyboard(email_address)
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def select_verify_access_checkbox(self):
        '''

        Checks verify access checkbox.
        '''
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.row_object_verify_access, EmailAppWorkflowObjectIds.checkbox_verify_access], screen_id = EmailAppWorkflowObjectIds.email_setup_view_list, scrolling_value = 1, scrollbar_objectname = EmailAppWorkflowObjectIds.email_setup_view_list_scroll_bar)

    def wait_for_okButton_and_click(self):
        '''
        wait for ok button and click
        '''
        ok_button = self.spice.wait_for(EmailAppWorkflowObjectIds.verify_access_result_ok_button, timeout = 30.0)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def validatefromAddressNotEditable(self):
        '''
        If tried to modify from address constraint should be displayed
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.finish_btn)
        current_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_from_field).mouse_click(10)
        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert)
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()

    def goto_userEditableCheckbox(self):
        '''
        unselect user editable checkbox
        '''
        #self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.row_usereditable_Checkbox,EmailAppWorkflowObjectIds.model_usereditable], "#scanMenuListlist1", select_option=True)
        assert self.spice.wait_for(f"{EmailAppWorkflowObjectIds.row_usereditable_Checkbox} {EmailAppWorkflowObjectIds.model_usereditable}")
        check_selectall = self.spice.wait_for(EmailAppWorkflowObjectIds.model_usereditable)
        check_selectall.mouse_click()
        sleep(2)

    def validatefromAddressEditable(self):
        '''
        Should be able to modify from address
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.finish_btn)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        text_box_button = self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_from_field)
        self.spice.validate_button(text_box_button)
        text_box_button.mouse_click(10)
        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert)
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()

    def goto_email_details(self):
        '''
        From scan email landing screen navigate to email details screen
        UI Flow is from email landing  screen -> click on send to field
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options) 
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        self.spice.validate_button(current_button)
        current_button.mouse_click()      
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_option)
        logging.info("Inside Email Details Screen")
    
    def goto_email_details_to_address(self):
        '''
        From scan email details screen navigate into To address
        UI Flow is from email details screen -> click on To address
        '''
        #NA FOr workflow        
    
    def goto_email_details_from_address(self):
        '''
        From scan email details screen navigate to from address screen
        UI Flow is from email details screen -> click on from address
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_from_field,"#scanMenuListlist1", scrollbar_objectname ="#scanMenuListlist1ScrollBar")

        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_from_more_options)
        current_button.mouse_click()  
        logging.info("Inside email details From address Screen")


    def goto_email_details_cc_and_bcc_checkbox_row(self):
        '''
        From scan email details screen navigate to cc and bcc checkbox row
        UI Flow is from email details screen -> click on cc and bcc checkbox row
        '''
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.checkbox_cc_bcc_row,EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)

    def select_cc_checkbox(self):
        logging.info("Marking cc checkbox ")  
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.checkbox_cc_bcc_row,"#ccCheckBox"],EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)

    def select_bcc_checkbox(self):
        logging.info("Marking bcc checkbox ")
        self.workflow_common_operations.goto_item([EmailAppWorkflowObjectIds.checkbox_cc_bcc_row,"#bccCheckBox"],EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
    
    def verify_cc_checkbox(self , expected_value :bool = True):
        '''
        Verify if cc checkbox is set to true
        '''
        cc_checkbox = self.spice.wait_for("#ccCheckBox")
        logging.info(f"CC checkbox value is {cc_checkbox['checked']}")
        assert cc_checkbox["checked"] == expected_value, f"CC checkbox is not set to <{expected_value}>"
    
    def verify_bcc_checkbox(self , expected_value :bool = True):
        '''
        Verify if bcc checkbox is set to true
        '''
        bcc_checkbox = self.spice.wait_for("#bccCheckBox")
        logging.info(f"BCC checkbox value is {bcc_checkbox['checked']}")
        assert bcc_checkbox["checked"] == expected_value, f"BCC checkbox is not set to <{expected_value}>"

    def verify_cc_address_in_all_options(self, expected_cc_address:str):
        '''
        Verify the expected email field is present in cc address field
        '''
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.checkbox_cc_bcc_row,EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        
    def goto_email_details_subject(self,text:str):
        '''
        From scan email details screen navigate to subject screen
        UI Flow is from email details screen -> click on subject
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()       
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_subject,"#scanMenuListlist1", scrollbar_objectname ="#scanMenuListlist1ScrollBar")
        time.sleep(2)        
        display_name_textbox = self.spice.wait_for("#subjectEditor")
        display_name_textbox.__setitem__('displayText', text)
        time.sleep(2)

    def goto_email_details_filename(self):
        '''
        From scan email details screen navigate to filename screen
        UI Flow is from email details screen -> click on filename
        '''        
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_filename, ScanAppWorkflowObjectIds.text_file_name_field_scan_option],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
    def goto_email_details_message(self, text:str):
        '''
        From scan email details screen navigate to filename screen
        UI Flow is from email details screen -> click on filename
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()       
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_message,"#scanMenuListlist1", scrollbar_objectname ="#scanMenuListlist1ScrollBar")
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_message)
        display_name_textbox = self.spice.wait_for("#messageEditor")
        display_name_textbox.__setitem__('displayText', text)
        logging.info("Inside Email Details MESSAGE Screen")
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def goto_cc_text_field(self):
        '''
        From scan email  screen navigate to cc text field
        UI Flow is from email screen -> click on cc text field
        '''
        setting_id = EmailAppWorkflowObjectIds.text_box_cc_field
        row_object_id = EmailAppWorkflowObjectIds.textbox_email_cc_field
        self.workflow_common_operations.goto_item([row_object_id, setting_id], EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary,select_option=False)

    def goto_bcc_text_field(self):
        '''
        From scan email screen navigate to bcc text field
        UI Flow is from email screen -> click on bcc text field
        '''
        setting_id = EmailAppWorkflowObjectIds.text_box_bcc_field
        row_object_id = EmailAppWorkflowObjectIds.textbox_email_bcc_field
        self.workflow_common_operations.goto_item([row_object_id, setting_id], EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)

    def  goto_email_body_field_in_options(self):
        '''
        From scan email details screen navigate to body field in options screen
        UI Flow is from email details screen -> click on body field
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_message,"#scanMenuListlist1", scrollbar_objectname ="#scanMenuListlist1ScrollBar")
        meesage_textbox = self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_message)
        meesage_textbox.mouse_click()
        
    def click_cancel_button_on_signin_user_screen(self):
        """
        Navigate to home screen and disable fax permissions from EWS > Security > Access Control, printer user screen pop up.
        Click Cancel button on Printer User screen return to previous screen.
        """
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
        cancel_button = self.spice.wait_for(MenuAppWorkflowObjectIds.signin_cancel)
        self.spice.wait_until(lambda: cancel_button["visible"] is True)
        cancel_button.mouse_click()        

    def goto_email_input_field_interactive_summary(self,setting:str):
        common_instance = common.Common(self.spice.cdm, self.spice.udw)
        scan_resource = common_instance.scan_resource()
        ui_size = self.spice.udw.mainUiApp.ControlPanel.getBreakPoint()

        if (setting.lower() == "subject"):
            setting_id = EmailAppWorkflowObjectIds.text_box_subject_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_subject
        elif (setting.lower() == "message"):
            setting_id = EmailAppWorkflowObjectIds.text_box_message
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_message
        elif (setting.lower() == "tofield"):
            setting_id = EmailAppWorkflowObjectIds.textbox_email_to_field_text
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_to_field
        elif (setting.lower() == "fromfield"):
            setting_id = EmailAppWorkflowObjectIds.text_box_from_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_from_field
        elif(setting.lower() == "ccfield"):
            setting_id = EmailAppWorkflowObjectIds.text_box_cc_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_cc_field
        elif(setting.lower() == "bccfield"):
            setting_id = EmailAppWorkflowObjectIds.text_box_bcc_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_bcc_field
        if(setting.lower() != "subject"):
            self.workflow_common_operations.goto_item([row_object_id, setting_id], EmailAppWorkflowObjectIds.screen_email_interactive_summary, scrollbar_objectname=EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        elif (setting.lower() == "subject") and scan_resource == "MDF" and ui_size in ["XL"]:
            self.wait_for_email_send_landing_view()
            # sleep is added to ensure the scroll bar is ready for intaraction.it prevents intermittent failure, for subject field we need to scroll to the position of subject field.
            time.sleep(2)
            self.workflow_common_operations.scroll_to_position_vertical(0.1, EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
            subject_filed = self.spice.wait_for(setting_id)
            self.spice.validate_button(subject_filed)
            subject_filed.mouse_click()   
        else:
            self.wait_for_email_send_landing_view()
            self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.screen_email_interactive_summary, row_object_id, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            subject_filed = self.spice.wait_for(setting_id)
            self.spice.validate_button(subject_filed)
            subject_filed.mouse_click()   
    
    def input_from_address_in_landing_view(self, from_address):
        """
        input from address in landing view, UI should in email landing view
        @param: from_address: str, from address to input
        """
        self.goto_email_input_field_interactive_summary("fromfield")
        keyboard_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)

        display_name_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.text_box_from_field}")
        display_name_textbox.__setitem__('displayText', from_address)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
    
    def input_to_address_in_landing_view(self, to_address, use_keyboard=True):
        """
        input to address in landing view, UI should in email landing view
        @param: to_address: str, to address to input
                use_keyboard: default value is True, input to address using keyboard.
                              If address with very long characters, it is very time-consuming input address using keyboard, so set value is False.
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text).mouse_click(10)
        keyboard_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        if use_keyboard:
            self.input_text_from_keyboard(to_address)
            time.sleep(2)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()
        else:
            to_address_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.textbox_email_to_field_text} {EmailAppWorkflowObjectIds.text_input}")
            to_address_textbox.__setitem__('text', to_address)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()
    
    def input_cc_address_in_landing_view(self, cc_address):
        """
        input for cc address  in landing view, UI should in email landing view
        @param: cc_address: str, cc address to input
        """
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_cc_field_text, timeout=40.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click(10)
        keyboard_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        cc_address_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.textbox_email_cc_field_text} {EmailAppWorkflowObjectIds.text_input}")
        cc_address_textbox.__setitem__('text', cc_address)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
            
    def input_bcc_address_in_landing_view(self, bcc_address):
        """
        input for bcc address  in landing view, UI should in email landing view
        @param: bcc_address: str, bcc address to input
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_bcc_field_text).mouse_click(10)
        keyboard_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        bcc_address_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.textbox_email_bcc_field_text} {EmailAppWorkflowObjectIds.text_input}")
        bcc_address_textbox.__setitem__('text', bcc_address)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
    
    def verify_cc_address_field_text_in_all_options(self, cc_text: str):
        """
        verify cc field text in all options
        """
        cc_field_text= self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_cc_field)
        self.spice.wait_until(lambda: cc_field_text["visible"] == True)
        logging.info("cc_field_text.__getitem__('text'): %s", cc_field_text.__getitem__('displayText'))
        assert cc_field_text.__getitem__('displayText') == cc_text, "cc field text mismatch"

    def verify_bcc_address_field_text_in_all_options(self, bcc_text: str, timeout: int = 60, wait_time: int = 1):
        """
        Verify BCC field text in all options with a timeout.
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            bcc_field_text = self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_bcc_field, timeout=25.0)
            self.spice.wait_until(lambda: bcc_field_text["visible"] == True, 30)
            logging.info("bcc_field_text.__getitem__('text'): %s", bcc_field_text.__getitem__('displayText'))
            if bcc_field_text.__getitem__('displayText') == bcc_text:
                logging.info("BCC field text matches the expected value: %s", bcc_text)
                return
            time.sleep(wait_time)
        assert bcc_field_text.__getitem__('displayText') == bcc_text, "bcc field text mismatch"

    def check_cc_bcc_checkbox_row_visible( self,expected_value :bool = True):
        '''
        Check cc/bcc checkbox row is visible
        '''
        try:
            cc_bcc_checkbox_row = self.spice.wait_for(EmailAppWorkflowObjectIds.checkbox_cc_bcc_row)
            self.spice.wait_until(lambda: cc_bcc_checkbox_row["visible"] == True)
            visible = cc_bcc_checkbox_row["visible"]
        except:
            visible = False
        assert (expected_value == visible), "CheckBox Row is not available"

    def verify_invalid_email_address_message_under_from_address(self, net):
        '''
        verify invalid email address error message under from address
        '''
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.text_box_from_field} {EmailAppWorkflowObjectIds.helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddress')
        assert message == expected_string, "Error message under from address is not displayed correctly"
    
    def check_visible_helper_message_under_from_address(self):
        """
        Purpose: check if helper message item under from address is visible or not.
        @return: isVisible
        """
        isVisible = False
        try:
            helper_message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.text_box_from_field} {EmailAppWorkflowObjectIds.helper_message_item_text}")
            isVisible = helper_message["visible"]
        except:
            isVisible = False

        logging.info("[check helper message under from address ] isVisible={}".format(isVisible))
        return isVisible
    
    def verify_invalid_email_address_message_under_to_address(self, net):
        '''
        verify invalid email address error message under to address
        '''
        time.sleep(2)
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_to_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}", timeout=15.0) ["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddress')
        assert message == expected_string, "Error message under to address is not displayed correctly"

    def verify_restricted_email_address_message_under_cc_address(self, net):
        '''
        verify restricted email address error message under cc address
        '''
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_cc_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddressDomain')
        assert message == expected_string, "Error message under cc address is not displayed correctly"

    def verify_invalid_email_address_message_under_cc_address(self, net):
        '''
        verify invalid email address error message under cc address
        '''
        self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.screen_email_interactive_summary, EmailAppWorkflowObjectIds.textbox_email_cc_field, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_cc_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddress')
        assert message == expected_string, "Error message under cc address is not displayed correctly"

    def verify_invalid_email_address_message_under_bcc_address(self, net):
        '''
        verify invalid email address error message under bcc address
        '''
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_bcc_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInvalidEmailAddress')
        assert message == expected_string, "Error message under bcc address is not displayed correctly"
    
    def verify_to_email_field_text_in_landing_view(self, to_address: str):
        """
        verify to email field text in landing view
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        time.sleep(2)
        to_field_text= self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text)["inputText"]
        assert to_field_text == to_address, "to field text mismatch"
    
    def check_visible_helper_message_under_to_address(self):
        """
        Purpose: check if helper message item under to address is visible or not.
        @return: isVisible
        """
        isVisible = False
        try:
            helper_message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_to_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")
            isVisible = helper_message["visible"]
        except:
            isVisible = False

        logging.info("[check helper message under to address ] isVisible={}".format(isVisible))
        return isVisible
    
    def check_visible_helper_message_under_cc_address(self):
        """
        Purpose: check if helper message item under cc address is visible or not.
        @return: isVisible
        """
        isVisible = False
        try:
            helper_message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_cc_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")
            self.spice.wait_until(lambda: helper_message["visible"] == True)
            isVisible = helper_message["visible"]
        except:
            isVisible = False

        logging.info("[check helper message under cc address ] isVisible={}".format(isVisible))
        return isVisible
    
    def check_visible_helper_message_under_bcc_address(self):
        """
        Purpose: check if helper message item under cc address is visible or not.
        @return: isVisible
        """
        isVisible = False
        try:
            helper_message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_bcc_field_text} {EmailAppWorkflowObjectIds.to_address_helper_message_item_text}")
            isVisible = helper_message["visible"]
        except:
            isVisible = False

        logging.info("[check helper message under bcc address ] isVisible={}".format(isVisible))
        return isVisible
    

    def input_subject_in_landing_view(self, subject):
        """
        input subject in landing view, UI should in email landing view
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.screen_email_interactive_summary, EmailAppWorkflowObjectIds.textbox_email_subject, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
        subject_field_text = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.screen_email_interactive_summary} {EmailAppWorkflowObjectIds.text_box_subject_field}")
        subject_field_text.mouse_click()
        subject_field_text.__setitem__('displayText', subject)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def verify_subject_field_text_in_landing_view(self, subject_text: str):
        """
        verify subject field text in landing view
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        time.sleep(2)
        subject_field_text= self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_subject_field)["inputText"]
        assert subject_field_text == subject_text, "subject field text mismatch"
    
    def verify_information_missing_or_incorrect_message_under_subject(self, net):
        '''
        verify "The required information is either missing or incorrect. Try again." error message under subject. 
        '''
        message = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.text_box_subject_field} {EmailAppWorkflowObjectIds.helper_message_item_text}")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cInformationMissing')
        assert message == expected_string, "Error message under subject is not displayed correctly"

    
    def back_to_email_landing_view_from_email_details(self):
        '''
        From email details screen go back to email landing screen
        UI Flow is from email details screen -> email landing screen
        '''
        #self.workflow_common_operations.back_button_press(EmailAppWorkflowObjectIds.button_back, EmailAppWorkflowObjectIds.view_email_option)
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        time.sleep(2)
        close_button.mouse_click()
        time.sleep(3)
        
    def add_page_pop_up_add_more(self):
        scan_add_page_add_more_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page)
        assert scan_add_page_add_more_button
        scan_add_page_add_more_button.mouse_click()
    
    def add_page_pop_up_done(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_flatbed_AddPage)
        logging.info("At Add Page Pop Up")
        scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
        assert scan_add_page_done_button
        self.spice.wait_until(lambda: scan_add_page_done_button["enabled"] == True)
        scan_add_page_done_button.mouse_click()

    def add_page_pop_up_cancel(self):
        scan_add_page_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbedduplex_cancel)
        assert scan_add_page_cancel_button
        scan_add_page_cancel_button.mouse_click()
        button_duplex_cancel_no = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_no)
        assert button_duplex_cancel_no
        scan_add_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        assert scan_add_page_cancel_page_yes_button
        scan_add_page_cancel_page_yes_button.mouse_click()

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
        time.sleep(5)
        logging.info("UI: At Scan to email landing screen")
    #Email Functional Keywords
    
    def email_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=2, need_to_wait_email_landing_view=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 35.0)
        # Wait for clickable situation
        self.spice.wait_until(lambda: current_button["visible"] == True, 30)
        self.spice.wait_until(lambda: current_button["enabled"] == True, 30)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(wait_time)
        if need_to_wait_email_landing_view:
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        logging.info("Inside Email Details Screen")

        # time.sleep(2)
        # current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_landing_view_send_button,EmailAppWorkflowObjectIds.scan_email_landing_view )
        # current_button.mouse_click()

        # time.sleep(2)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()
    
    def email_send_enterprise(self, cdm, scan_more_pages: bool = False, dial_value: int = 180, wait_time=2, need_to_wait_email_landing_view=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 20.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(wait_time)
        if need_to_wait_email_landing_view:
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        logging.info("Inside Email Details Screen")

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
    
    def get_add_page_media_sizes_list_from_cdm(self, cdm):
        logging.info("Get the media sizes list from CDM")
        media_sizes_object_names_list = []
        response = cdm.get("/cdm/jobTicket/v1/configuration/defaults/scanEmail/constraints")

        for data in response["validators"]:
            if data["propertyPointer"] == "src/scan/mediaSize":
                media_sizes_options_list_from_cdm = data["options"]
                break

        media_sizes_object_names_list = list(map(lambda media: "#"+media.get("seValue").replace(".","_dot_").replace('-','_dash_'), media_sizes_options_list_from_cdm))

        if len(media_sizes_object_names_list) == 0:
            logging.error("Media sizes list is empty")
        else:
            return media_sizes_object_names_list

    def wait_for_email_send_landing_view(self):
        '''
        UI wait for email landing view.
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send)
        

    def wait_for_textfield(self):
        '''
        UI wait for message textarea found in email landing view.
        '''
        self.spice.homeMenuUI().workflow_common_operations.goto_item("#emailMessageFieldDestination","#DetailPanelverticalLayout", scrollbar_objectname = EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_message)
        text_box_message___ = self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_message)
        text_box_message___.mouse_click()
        enter_key_ = self.spice.wait_for(EmailAppWorkflowObjectIds.enter_key_keyboard)
        enter_key_.mouse_click()
        enter_key_.mouse_click()
        ok_key = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_enter)
        ok_key.mouse_click()

    def wait_for_email_setup_no_profile(self):
        '''
        UI Wait for Email setup screen
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_scansetup_no_profile)

    def wait_and_validate_property_value(self, object, property, state, timeout = 5, delay = 0.25):
        self.workflow_common_operations.wait_until_property_value(object, property, state, timeout, delay = delay)
        assert object[property] == state

    def validate_screen_buttons(self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible, click = False):
        button_ids = [
            EmailAppWorkflowObjectIds.button_email_send,
            EmailAppWorkflowObjectIds.button_email_start
        ]

        button = None
        for button_id in button_ids:
            if buttonObjectId == button_id:
                try:
                    button = self.spice.wait_for(button_id, 60)
                    logging.info("Found button with ID %s", button_id)
                    self.wait_and_validate_property_value(button, "visible", True, 30, delay = 0.01)
                    self.wait_and_validate_property_value(button, "enabled", True, 30, delay = 0.01)
                    self.wait_and_validate_property_value(button, "constrained", isButtonConstrained, 30, delay = 0.01)
                    if click:
                        button.mouse_click()
                    break
                except:
                    logging.info("Button with ID %s not found", button_id)
                    continue

        if button is None:
            logging.error("Button with ID %s not found", buttonObjectId)
            raise ValueError(f"Button with ID {buttonObjectId} not found")

        #Get Eject
        ejectButton = self.spice.wait_for( EmailAppWorkflowObjectIds.eject_button,10)

        #Validate eject
        self.wait_and_validate_property_value(ejectButton, "visible", isEjectButtonVisible, delay = 0.01)

    def verify_constrained_message(self, net, message):
        '''
        Verify constrained message.
        :param net, message
        '''
        sleep(2)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_constraint_message, timeout=30.0)
        self.workflow_common_operations.verify_string(net, message, f"{EmailAppWorkflowObjectIds.view_constraint_message} {EmailAppWorkflowObjectIds.constrain_description_view}")
        ok_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.ok_button_message}")
        ok_button.mouse_click()
        logging.info("Verify constrained message")    
   
    def wait_and_click_on_middle(self, locator: str) -> None:
        """
        Waits for object in clickable state (visible and enabled) and
        it clicks on the middle of the object
        """
        # Validate for object if not exist
        object = self.spice.wait_for(locator)

        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True)
        self.spice.wait_until(lambda: object["visible"] == True)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)
   
    def wait_stateMachine_state(self, state, timeout = 10 ):
        emailLanding = self.spice.wait_for( EmailAppWorkflowObjectIds.view_email_landing_view , 5 )
        self.spice.wait_until( lambda: emailLanding["state"] == state , timeout )
    
    def wait_mainButton_type(self, state, timeout = 10 ):
        emailLanding = self.spice.wait_for( EmailAppWorkflowObjectIds.view_email_landing_view , 5 )
        self.spice.wait_until( lambda: emailLanding["mainButtonType"] == state , timeout )

    def email_send_with_encryption(self):
        '''
        From email details screen navigate to pdf encryption password prompt
        UI Flow is select email details -> pdf encryption password prompt
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send)
        current_button.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_scan_pdf_encryption_prompt_view)
        logging.info("At PDF Encryption prompt view")
    
    def cancel_email_send(self):
        '''
        From email send progress screen click on cancel button
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send)
        self.spice.wait_until(lambda: current_button["visible"] == True)
        self.spice.wait_until(lambda: current_button["enabled"] == True)
        current_button.mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cancel)
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout = 30.0)
        self.spice.wait_until(lambda: current_button["enabled"] == True, timeout = 30.0)
        current_button.mouse_click()
        logging.info("Back to email landing view")
    
    def email_details_to_address_remove_contact(self):
        '''
        In scan email remove contact screen, remove contact
        UI Flow is from email remove contact screen -> click on Remove
        '''
        #NA For Workflow
        # current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_remove_contact_button)
        # current_button.mouse_click()
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_details_view)
        # logging.info("Back to email details Screen")
    
    def email_details_to_address_remove_contact_cancel(self):
        '''
        From scan email remove contact screen go back to email details screen by clicking cancel
        UI Flow is from email remove contact screen -> click on Cancel
        '''
        #NA For workflow
        # current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_remove_contact_cancel_button)
        # current_button.mouse_click()
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_details_view)
        # logging.info("Back to email details Screen")

    def email_setup_profile_hp_software_click_ok(self):
        '''
        From scan email setup profile using HP Software screen click on Ok button
        UI Flow is from set up email profile using Hp Software screen -> click Ok button
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_scansetup_no_profile)
        logging.info("Back to Email Profile Setup Main Screen")
        ok_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scanSetUp_okButton)
        ok_button.mouse_click()
        time.sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_app)

    def email_setup_profile_web_browser_click_ok(self):
        '''
        From scan email setup profile using web browser screen click on Ok button
        UI Flow is from set up email profile using web browser screen -> click Ok button
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_setup_web)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_setup_no_profile)
        logging.info("Back to Email Profile Setup Main Screen")
        print_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_no_setup_print)
        print_button.mouse_click()

    def email_enter_pin(self, text: str):
        '''
        Once inside the keyboard view enter the pin
        UI Flow is keyboard view -> enter pin passed as argument
        Note - PIN has to be a 4 digit number
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_enter_pin_view)
        logging.info("Inside enter_spice pin keyboard view")
        display_name_textbox = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_enter_pin)
        display_name_textbox.__setitem__('displayText', text)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_enter_pin_row} {EmailAppWorkflowObjectIds.textbox_email_enter_pin} {EmailAppWorkflowObjectIds.textbox_email_enter_pin_textbox}").mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        current_button.mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_done)
        current_button.mouse_click()
       

    def email_enter_wrong_pin(self, text: str):
        '''
        Once inside the keyboard view enter the wrong pin
        UI Flow is keyboard view -> enter the wrong pin passed as argument
        Note - PIN has to be a 4 digit number
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_enter_pin_view)
        logging.info("Inside enter_spice pin keyboard view")
        display_name_textbox = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_enter_pin)
        display_name_textbox.__setitem__('displayText', text)
        self.spice.wait_for(f"{EmailAppWorkflowObjectIds.textbox_email_enter_pin_row} {EmailAppWorkflowObjectIds.textbox_email_enter_pin} {EmailAppWorkflowObjectIds.textbox_email_enter_pin_textbox}").mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        current_button.mouse_click()
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_done)
        current_button.mouse_click()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_wrong_pin)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        current_button.mouse_click()
        #adding below code for navigating back to the previous screen
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_cancel)
        current_button_pin_cancel = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_cancel)
        self.spice.validate_button(current_button_pin_cancel)
        current_button_pin_cancel.mouse_click()
       
    def email_select_profile(self, cdm, udw, name: str):
        '''
        Once inside email home, select the profile
        UI Flow is Email home -> select the email profile
        Arg:
        name -> is the name provided in the display_name field while creating email profile
        cdm -> cdm instance
        udw -> udw instance
        '''
        self.goto_email()
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
        logging.info("Objectname obtained for SMTP server profile")

        current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE  + " MouseArea", timeout = 19.0)
        #self.spice.wait_until(lambda: current_button["visible"] == True)
        current_button.mouse_click()

    
    def email_select_profile_home(self, cdm, udw, name: str):
        '''
        Once inside email home, select the profile
        UI Flow is Email home -> select the email profile
        Arg:
        name -> is the name provided in the display_name field while creating email profile
        cdm -> cdm instance
        udw -> udw instance
        '''
        self.goto_email_home()
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
        logging.info("Objectname obtained for SMTP server profile")
        self.spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 20.0)
        current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE)
        current_button.mouse_click()
        logging.info("Successfully selected email profile")

    def email_details_enter_text_to_field(self, text: str):
        '''
        This is helper method to enter text into any of the fields under Email Details screen
        UI flow is common keyboard view -> enter text
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_filename)
        display_name_textbox = self.spice.wait_for("#fileNameTextField")
        display_name_textbox.__setitem__('displayText', text)
        #Uncheck after keyboard tuf implimentation
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.common_keyboard_view, timeout = 9.0)
        # self.workflow_keyboard_operations.keyboard_enter_text(text)
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_details_view)
    
    def set_email_file_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
        time.sleep(3)
        clear_text = self.spice.wait_for(EmailAppWorkflowObjectIds.clear_text_filename)
        clear_text.mouse_click() 
        time.sleep(2)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        keyword_ok.mouse_click()
        time.sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_filename_empty_message(self, net):
        '''
        UI should be at email constraint message screen.
        Function will verify the filename empty message.
        '''
        message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()


    def verify_input_field_constraint_message_displayed(self, net):
        '''
        This is to verify that the constrained message displayed .
        Click on ok button to exit the constraint message screen
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_description)
        displayed_message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        logging.info("Click ok button to exit constraint message screen")
        ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok)
        ok_button.mouse_click()

    def enter_new_email_address(self, to_address, use_keyboard=False):
        '''
        This is helper method to enter new email address from email options
        UI flow is common keyboard -> enter new email address
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)   
        time.sleep(2)
        if use_keyboard:
            self.input_text_from_keyboard(text)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()
        else:
            to_address_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.textbox_email_to_field_text} {EmailAppWorkflowObjectIds.text_input}")
            to_address_textbox.__setitem__('text', to_address)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()

        self.back_to_scan_home_from_send_to_options()
        #Uncheck after keyboard tuf implimentation
        # self.workflow_keyboard_operations.keyboard_enter_text(text)
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_landing_view)
    
    def pdf_encryption_screen_cancel(self):
        '''
        This is helper method to click on cancel in the pdf encryption password screen
        UI flow is pdf encryption password screen -> cancel
        '''
        self.scan_operations.pdf_encryption_cancel(EmailAppWorkflowObjectIds.view_email_landing_view)
    
    def select_email_quickset(self, quickset_name):
        '''
        This is helper method to select email quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        current_button = self.spice.wait_for(quickset_name)
        current_button.mouse_click()
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

    def goto_email_signing_and_encryption(self):
        '''
        This is helper method to navigate to email signing and encryption screen
        UI flow is email landing view -> click on signing and encryption
        '''
        row_object_id = EmailAppWorkflowObjectIds.button_email_signing_and_encryption
        self.workflow_common_operations.goto_item(row_object_id, ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname=EmailAppWorkflowObjectIds.scroll_bar_email_options)
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_signing_and_encryption)

    def select_email_signing_and_encryption(self):
        '''
        This is helper method to select email signing and encryption
        UI flow is email soptions screen -> click on email signing and encryption
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_signing_and_encryption)
        current_button.mouse_click()
    
    def set_email_signing_and_encryption(self, signing_value: bool, encryption_value: bool):
        '''
        This is helper method to set email signing and encryption
        UI flow is email signing and encryption screen -> set signing and encryption
        '''
        email_signing_on = self.spice.wait_for(EmailAppWorkflowObjectIds.checkbox_email_signing)
        if signing_value :
            if email_signing_on["checked"] == False:
                email_signing_on.mouse_click()
        else :
            if email_signing_on["checked"] == True:
                email_signing_on.mouse_click()
        email_encryption_on = self.spice.wait_for(EmailAppWorkflowObjectIds.checkbox_email_encryption)
        if encryption_value:
            if email_encryption_on["checked"] == False:
                email_encryption_on.mouse_click()
        else:
            if email_encryption_on["checked"] == True:
                email_encryption_on.mouse_click()
        back_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_signing_and_encryption} {EmailAppWorkflowObjectIds.button_back}")
        back_button.mouse_click()
        
    def verify_email_signing_and_encryption_on_options(self, net, signing_value: bool = False,encryption_value : bool =False):
        '''
        This is helper method to verify email signing and encryption
        '''
        cstring_id = ""
        setting_id = ""
        setting_value = "off"
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        setting_value = "on" if signing_value and encryption_value else "signing" if signing_value else "encryption" if encryption_value else "off"
        setting_id = EmailAppWorkflowObjectIds.button_email_signing_and_encryption
        row_object_id = EmailAppWorkflowObjectIds.button_email_signing_and_encryption
        cstring_id = EmailAppWorkflowObjectIds.email_signing_and_encryption_option_dict[setting_value][0]
        index = 1
        screen_id = ScanAppWorkflowObjectIds.menu_list_scan_settings
        self.workflow_common_operations.goto_item(row_object_id, ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=False, scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]", index)["text"]
        logging.info("UI Setting id is %s", ui_setting_string)
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"


    def goto_email_send_when_default_profile_is_set(self):
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email_home)
        current_button.mouse_click()
        time.sleep(2)
        
    def check_spec_on_scan_to_email_application_screen(self, spice, net, email_address):
        """
        Check spec on scan to email application screen
        @param spice: 
        @param email_address: 
        @param net: 
        """
        logging.info("Check header string Scan to Email")
        # Todo: Update once bug fix. HMDE-662: Object ID is not available for header string "Scan to Email".
        # self.workflow_common_operations.verify_string(net, "cScanToEmailSettings", EmailAppWorkflowObjectIds.header_scan_to_email)

        logging.info("Check quickset list")
        self.workflow_common_operations.verify_string(net, "cDefault", EmailAppWorkflowObjectIds.item_default)
        self.workflow_common_operations.verify_string(net, "cViewAll", EmailAppWorkflowObjectIds.item_view_all)

        logging.info("Check setting options")
        expected_to_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cTo") # expected_to_str=To
        actual_to_str = self.workflow_common_operations.get_actual_str(EmailAppWorkflowObjectIds.title_to) # actual_to_str=To*
        assert expected_to_str in actual_to_str, 'Spec check failed'

        self.workflow_common_operations.verify_string(net, "cFrom", EmailAppWorkflowObjectIds.title_from)
        self.workflow_common_operations.verify_string(net, "cScanToEmailSubject", EmailAppWorkflowObjectIds.title_subject)

        expected_file_name_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cFileName") # expected_file_name_str=File Name
        actual_file_name_str = self.workflow_common_operations.get_actual_str(EmailAppWorkflowObjectIds.textbox_email_filename) # actual_to_str=File Name*
        assert expected_file_name_str in actual_file_name_str, 'Spec check failed'
        
        expected_sides_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cSides") # expected_file_name_str=File Name
        actual_sides_str = self.workflow_common_operations.get_actual_str(EmailAppWorkflowObjectIds.combobox_email_two_sided) # actual_to_str=File Name*
        assert expected_sides_str in actual_sides_str, 'Spec check failed'
        self.workflow_common_operations.verify_string(net, "cFileType", EmailAppWorkflowObjectIds.combobox_email_file_format)
        self.workflow_common_operations.verify_string(net, "cColorMode", EmailAppWorkflowObjectIds.combobox_email_color_mode)

        logging.info("Check Send button")
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout=9.0)

    
    def wait_for_scan_loading_toast_display(self, time_out= 30):
        logging.info("check the status after scan")
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_systemToastMessagesScreen)
        #todo: update the method for complete status

    def select_options_scan_email(self, cdm, udw, name: str, recordId, scan_options: Dict):
        '''
        Select scan settings in email more options
        UI flow is from Home screen.
        e.g.:
        cdm -> cdm instance
        udw -> udw instance
        name -> is the name provided in the display_name field while creating email profile
        recordId: recordId of the contact
        scan_options = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'orientation': 'portrait',
            'lighter_darker': 1,
            'contrast': 1
        }
        '''
        self.goto_email_options_from_home(cdm, udw, name, recordId)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        time.sleep(2)

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
            'contrast': scan_options.get('contrast', None)
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
        if settings['contrast'] != None:
            self.scan_operations.goto_contrast_settings()
            self.scan_operations.set_scan_settings_contrast(contrast=settings['contrast'])
        self.back_to_email_landing_view_from_scan_settings()

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
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'orientation': 'portrait',
            'lighter_darker': 1,
            'contrast': 1
        }
        recordId: recordId of the contact
        '''
        self.select_options_scan_email(cdm, udw, name, recordId, scan_options)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.email_send()

        # self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.button_email_send,EmailAppWorkflowObjectIds.view_email_landing_view, 0)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()

    def add_page_pop_up_finish(self):
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_add_more_page)
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_add_more_finish)
        current_button.mouse_click()

    def verify_error_msg_email_send_without_recipient(self, net):
        '''
        From email landing view click on send button and check for error prompt
        UI Flow is email landing view -> send -> error prompt
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 20.0)
        send_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_email_send)
        
        self.wait_and_validate_property_value(send_button, "visible", True, 10)
        self.wait_and_validate_property_value(send_button, "enabled", True, 10)
        self.wait_and_validate_property_value(send_button, "constrained", True, 10)
        send_button.mouse_click()

        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert, timeout = 20.0)
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()

        # self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.email_landing_send_to_button)
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_landing_view, timeout=9.0)
        # # verify the message content by comparing the ui content with the stringid in the specification
        # self.scan_operations.verify_string(net, "#Version2Text", "cNoRecipients", 5)
        # self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.email_landing_send_to_button, "#ButtonListLayout")
        # assert self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_landing_view)
        # logging.info("Back to email landing view")    
        
    def select_email_profile_from_email_landing_view(self, cdm, udw, name: str):  
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        time.sleep(2)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        time.sleep(2) 
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_from_more_options) 
        send_button.mouse_click()        
        time.sleep(2)
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_from_profile) 
        send_button.mouse_click()       
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
        screen_id =  f"{EmailAppWorkflowObjectIds.view_email_profile_view} {'#SpiceListViewView'}"
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id,SCAN_EMAIL_PROFILE, select_option=False,start_from_top=True)
        time.sleep(2)   
        assert self.scrollto_emailfolder_in_profile_selection(SCAN_EMAIL_PROFILE)
        logging.info("Objectname obtained for SMTP server profile")
        current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 20.0)
        time.sleep(2)
        current_button.mouse_click()
        logging.info("Successfully selected email profile")
        
    def verify_from_email_field_text(self, from_address: str):
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        time.sleep(2)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)
        time.sleep(2)
        from_feild_address= self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_from_field)["inputText"]
        assert from_feild_address == from_address, "from email address mismatch"

    def verify_selected_quickset(self, net, stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check Copy QuicksetSelected Button
        '''
        if not self.is_quickset_existing():
            return

        text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, stringId)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        assert self.spice.wait_for(f"#{text}")["checked"]


    def save_to_email_quickset_default(self, cdm, udw, name, recordId, scan_options:Dict):
        '''
        Start save to email drive with scan settings and verify job is success
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
        time.sleep(2)
        self.goto_email_options_from_home(cdm, udw, name, recordId)

        # ticket_default_body = get_sharepoint_default_ticket(cdm)
        uri = "cdm/jobTicket/v1/configuration/defaults/scanEmail"
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

        self.back_to_email_landing_view_from_scan_settings()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.save_as_default()

    def save_as_default(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''   
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_save_default_option)
        logging.info("Click the save button")
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_save_default_option)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        logging.info("Select as defaults")
        time.sleep(3)
        try:
            (self.spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_credentials(True, "12345678")
            time.sleep(3)
        finally:
            self.spice.wait_for(EmailAppWorkflowObjectIds.button_as_defaults, timeout = 20.0)
            current_butoon = self.spice.wait_for(EmailAppWorkflowObjectIds.button_as_defaults)
            self.spice.validate_button(current_butoon)
            current_butoon.mouse_click()
            logging.info("Click ok button")
            ok_button= self.spice.wait_for(EmailAppWorkflowObjectIds.button_save_option_ok)
            self.spice.validate_button(ok_button)
            ok_button.mouse_click()
            logging.info("Confirm save")
            self.spice.wait_for(EmailAppWorkflowObjectIds.message_confirm_save)
            confirm_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_confirm_save)
            self.spice.validate_button(confirm_button)
            confirm_button.mouse_click()
            self.spice.wait_for(EmailAppWorkflowObjectIds.view_systemToastMessagesScreen)

    def select_email_quickset_by_quickset_name_from_list(self, quickset_name):
        '''
        This is helper method to select folder quickset in View All screen.
        UI flow Select quickset
        Args: quickset_name: str, quickset name
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.scan_email_quickset_list_view)
        quickset_name_button = self.spice.wait_for(f"#{quickset_name}")
        quickset_name_button.mouse_click()

        email_landing_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.wait_until(lambda: email_landing_view["visible"] == True)

    def goto_email_quickset_view(self):
        '''
        This is helper method to goto email quickset
        UI flow Select Landing-> click on View All
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return
        view_all_btn = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.button_view_all} MouseArea")
        self.spice.validate_button(view_all_btn)
        view_all_btn.mouse_click()

    def check_loading_screen_for_selected_quickset(self, net):
        """
        Check loading screen when selected quickset.
        """
        # at present, loading screen exists shortly. The function will be updated when the locator can be captured.
        pass

    def goto_email_quickset_options_from_default(self):
        """
        Send scan to email _defult
        """
        # NA for workflow.
        pass
    
    def is_quickset_existing(self):
        '''
        This is helper method to verify is quickset existing
        '''
        try:
            self.spice.wait_for(EmailAppWorkflowObjectIds.item_default, 5)
            return True
        except:
            logging.info("No email quicksets in Scan to Email screen")
            return False

    def verify_preview_button_not_available(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        self.spice.scan_settings.click_expand_button()
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)["isPreviewButtonVisible"] == False

    def verify_email_settings_editable(self, net, setting, editable: bool = True):
        """
        This method verify email settings editable subject, message
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
                    subject, message
            editable: Need to pass bool values True/False
        """
        message = 'cSettingNotUserEditable'
        setting_id = ""
        #Get the ui object name of the passed setting
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        time.sleep(2)
        if (setting.lower() == "subject"):
            index = 0
            setting_id = EmailAppWorkflowObjectIds.text_box_subject_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_subject
        elif (setting.lower() == "message"):
            index = 0
            setting_id = EmailAppWorkflowObjectIds.text_box_message
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_message
        elif (setting.lower() == "to"):
            index = 0
            setting_id = EmailAppWorkflowObjectIds.textbox_email_to_field_text
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_to_field
        elif (setting.lower() == "from"):
            index = 0
            setting_id = EmailAppWorkflowObjectIds.text_box_from_field
            row_object_id = EmailAppWorkflowObjectIds.textbox_email_from_field
        else:
            assert False, "Editable settings not existing"

        self.workflow_common_operations.goto_item([row_object_id, setting_id], ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True)
        self.spice.scan_settings.verify_input_field_constraint_message_displayed(net, message, setting)
        self.spice.scan_settings.press_input_field_constraint_screen_ok_button()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_email_options_signing_and_encryption_constrained(self,setting):
        """
        This method verify email settings editable signing and encryption
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
                    signing, encryption, signing and encryption"""
        setting_id = ""
        #Get the ui object name of the passed setting
        if (setting.lower() == "signing"):
            signing_constrained = self.spice.wait_for(EmailAppWorkflowObjectIds.checkbox_email_signing)
            logging.info(f'Signing  constrainesd is: <{signing_constrained["constrained"]}>')
            assert signing_constrained["constrained"] == True,f"signing_constrained[constrained] is not true"
        elif (setting.lower() == "encryption"):
            encryption_constrained = self.spice.wait_for(EmailAppWorkflowObjectIds.checkbox_email_encryption)
            logging.info(f'Encryption  constrained is: <{encryption_constrained["constrained"]}>')
            assert encryption_constrained["constrained"] == True,f"encryption_constrained[constrained] is not true"
        elif(setting.lower() == "signing and encryption"):
            signing_and_encryption_constrained = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_signing_and_encryption)
            logging.info(f'Signing and Encryption Both constrained is: <{signing_and_encryption_constrained["constrained"]}>')
            assert signing_and_encryption_constrained["constrained"] == True,f"signing_and_encryption_constrained[constrained] is not true"
        else:
            assert False, "Editable settings not existing"
        logging.info("Click ok button to exit constraint message screen")
        ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok)
        ok_button.mouse_click()
        
        if(setting.lower() == "signing" or setting.lower() == "encryption"):
            back_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_signing_and_encryption} {EmailAppWorkflowObjectIds.button_back}")
            back_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_email_signing_and_encryption_both_constrained(self, net):
        row_object_id = EmailAppWorkflowObjectIds.button_email_signing_and_encryption
        self.workflow_common_operations.goto_item(row_object_id, ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname=EmailAppWorkflowObjectIds.scroll_bar_email_options)
        row_object_id["constrained"] == True, "Signing and Encryption both are not constrained"
    
    def is_contacts_existing(self, contacts_name):
        '''
        This is helper method to verify is contacts existing in scan to email address book
        '''
        try:
            contacts_name = '#checkBox_'+ contacts_name + 'Row'
            logging.info(f"Contacts name is: <{contacts_name}>")
            self.spice.wait_for(contacts_name)
            return True
        except:
            logging.info(f"Contacts {contacts_name} not in Scan to Email address book screen")
            return False
        
    def back_to_select_addressbook_view_from_contacts_select_screen(self):
        """
        Back to Select Address Book screen from select contacts screen through back button.
        """
        back_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_local_contact_screen} {EmailAppWorkflowObjectIds.button_back}")
        self.spice.wait_until(lambda: back_button["visible"] == True)
        back_button.mouse_click()
    
    def back_to_email_landing_view_from_select_addressbook_view(self):
        """
        Back to Scan email landing screen from select addressbook screen through close button.
        """
        close_button = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.select_address_book_view} {EmailAppWorkflowObjectIds.button_back_close}")        
        close_button.mouse_click()

    def back_to_contacts_select_screen_from_search_contacts_screen(self):
        '''
        From search contact screen go back to contacts select screen through close button
        UI Flow is from email search contact -> contacts select view
        '''
        cancel_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_cancel_body_row)
        cancel_button.mouse_click()
        
    def verify_contact_search_string(self, expected_string):
        '''
        This method verify the search string on added contacts screen. 
        '''
        search_string = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_contact_name_to_field_text)["displayText"]
        logging.info("search_string = " + search_string)
        assert search_string == expected_string, "search String mismatch"
    
    def perform_scan_email_job_and_check_file_name(self, cdm, udw, net, job, to_address, file_name, file_type, prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='', prefix_username='admin', suffix_username='admin', profile_name=None, time_out=90, scan_emulation=None):
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
        self.spice.scan_settings.goto_scan_app()
        if profile_name:
            self.email_select_profile(cdm, udw, profile_name)
        else:
            self.goto_email()
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

        self.enter_multiple_email_address(to_address)

        self.email_send(wait_time=0)
        job_ticket = job.get_job_details("scanEmail")
        file_name_preview_from_job = job_ticket['pipelineOptions']['sendFileAttributes']['fileNamePreview']
        logging.info(f'preview file name from job details is: {file_name_preview_from_job}')
        self.spice.quickset_ui.validate_scan_file_name(file_name_preview_from_job, file_name, file_type, prefix_type, suffix_type, custom_prefix_string, custom_suffix_string, prefix_username, suffix_username)
        
        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]
        self.wait_for_scan_email_job_to_complete(cdm, udw, job, file_type, pages = 1, time_out = 180, scan_emulation=scan_emulation)
        # wait for status dismiss
        time.sleep(7)
    

    def set_email_setting_in_options_screen(self, payload):
        """
        Set email settings in email options screen
        @param payload: please refer to structure from quickset_email_payload from dunetuf.ews.copy_scan_ews_option_dict
                        In scan email ui setting, only can set from_address/to_address/subject/message option.
        @return:
        """
        logging.info("change email setting options")
        from_address = payload.get('from_address', None)
        if from_address != None:
            self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.view_email_option, EmailAppWorkflowObjectIds.textbox_email_from_field, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.text_box_from_field}").mouse_click()
            self.spice.wait_for(EmailAppWorkflowObjectIds.view_common_keyboard)
            self.input_text_from_keyboard(from_address)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()

        to_address = payload.get('to_address', None)
        if to_address != None:
            self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.view_email_option, EmailAppWorkflowObjectIds.textbox_email_to_field, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.textbox_email_to_field_text}").mouse_click()
            self.input_text_from_keyboard(to_address)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()

        message = payload.get('message', None)
        if message != None:
            self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.view_email_option, EmailAppWorkflowObjectIds.textbox_email_message, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            display_name_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.text_box_message}")
            display_name_textbox.mouse_click()
            display_name_textbox.__setitem__('displayText', message)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()

        subject = payload.get('subject', None)
        if subject != None:
            self.workflow_common_operations.scroll_vertical_row_item_into_view(EmailAppWorkflowObjectIds.view_email_option, EmailAppWorkflowObjectIds.textbox_email_subject, top_item_id=EmailAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            display_name_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.text_box_subject_field}")
            display_name_textbox.mouse_click()
            display_name_textbox.__setitem__('displayText', subject)
            keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
            keyword_ok.mouse_click()


    def validate_scan_job_ticket_email_setting(self, cdm, net, job_ticket, payload):
        """
        Compare cdm scan email settings with job ticket
        @param job_ticket: get job ticket from cdm
        @param payload: include email settings and scan common settings. 
                        In scan email ui setting, only can change from_address/to_address/subject/message email option.
                        Scan common settings please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        @return:
        """
        from_address = payload.get("from_address", None)
        if from_address != None:
            logging.info(f"To check option from_address, the expected_result is <{from_address}>")
            assert job_ticket["dest"]["email"]["from"]["emailAddress"] == from_address

        to_address = payload.get("to_address", None)
        if to_address != None:
            logging.info(f"To check option to_address, the expected_result is <{to_address}>")
            assert job_ticket["dest"]["email"]["toList"][0]["emailAddress"] == to_address

        subject = payload.get("subject", None)
        if subject != None:
            logging.info(f"To check option subject, the expected_result is <{subject}>")
            assert job_ticket["dest"]["email"]["subject"] == subject

        message = payload.get("message", None)
        if message != None:
            logging.info(f"To check option message, the expected_result is <{message}>")
            assert job_ticket["dest"]["email"]["body"] == message

        logging.info("validation scan email job ticket common settings")
        CDMShortcuts(cdm, net).compare_cdm_scan_common_option_settings(job_ticket, payload, scan_type="scanEmail")

    def complete_email_send(self, cdm, udw, job, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5, need_to_wait_email_landing_view=True, button=ScanAppWorkflowObjectIds.send_button):
        self.email_send(scan_more_pages,wait_time,need_to_wait_email_landing_view)

    def get_scan_resource_used(self, udw, scan_emulation):
        """
        Return current scan resouse is under used
        """
        list_input_devices = udw.mainApp.ScanMedia.listInputDevices().lower()
        logging.info(f"list_input_devices: {list_input_devices}")
        is_media_loaded_in_adf = scan_emulation.media.is_media_loaded('ADF')
        logging.info(f"scan_emulation.media.is_media_loaded('ADF'): {scan_emulation.media.is_media_loaded('ADF')}")
        if "adf" in list_input_devices:
            logging.info("The device support ADF")
            if is_media_loaded_in_adf == True or scan_emulation.media.is_media_loaded('ADF') == 'Success':
                logging.info("The scan resource from ADF")
                return "ADF"
            else:
                logging.info("The scan resource from glass")
                return "Glass"
        elif "mdf" in list_input_devices:
            logging.info("The scan resource from MDF")
            return "MDF"

        elif "glass" in list_input_devices:
            logging.info("The scan resource from glass")
            return "Glass"
        else:
            logging.info(f"The scan resource is from <{list_input_devices}>")
            raise Exception("Please add corresponding scan resource into if condition")

    def wait_for_scan_email_job_to_complete(self, cdm, udw, job, file_type, pages=1, time_out=120,scan_emulation=None, number_of_jobs_to_check=1, adf_loaded=False):
        """
        wait for scan email job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        common_instance = ScanCommon(cdm, udw)
        if scan_emulation==None:
            scan_resource = common_instance.scan_resource()
        else:
            scan_resource = self.get_scan_resource_used(udw, scan_emulation)    
        logging.info("Scan resource used in Common: %s", scan_resource)
        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages(type = "email")
        if not adf_loaded:
            if scan_resource == "Glass":
                try:
                    for _ in range(pages-1):
                        scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                        self.spice.validate_button(scan_add_page_button)
                        scan_add_page_button.mouse_click()
                        time.sleep(2)

                    scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                    logging.info("#finish button found")
                    self.spice.validate_button(scan_add_page_done_button)
                    scan_add_page_done_button.mouse_click()
                except TimeoutError:
                    logging.info("flatbed Add page is not available")
            elif scan_resource == "MDF" and file_type in ["tiff", "pdf"]:
                self.spice.scan_settings.mdf_add_page_alert_done()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "scanEmail", "status": "success"}] , time_out)

    def perform_scan_email_job_with_addressbook_contacts_from_home_scanapp(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, profile_name=None, pages=1, pdf_encryption_code=None, time_out=120, scan_emulation= None):
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
        self.workflow_common_operations.goto_scan_app()
        self.scan_operations.goto_email_from_scanapp_at_home_screen()
        if profile_name:
            server_id = Email(cdm, udw).get_email_profile_id(profile_name)
            SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
            current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 20.0)
            time.sleep(3)
            current_button.mouse_click()

        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

        self.perform_scan_email_job_with_addressbook_contacts(cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload, custom_book_name, option_payload, pages, pdf_encryption_code, time_out,scan_emulation)
    

    def perform_scan_email_job_with_addressbook_contacts_from_home_scanapp_enterprise(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, profile_name=None, pages=1, pdf_encryption_code=None, time_out=120, scan_emulation= None):
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
        self.workflow_common_operations.goto_scan_app()
        self.scan_operations.goto_email_from_scanapp_at_home_screen()
        if profile_name:
            server_id = Email(cdm, udw).get_email_profile_id(profile_name)
            SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
            current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 20.0)
            time.sleep(3)
            current_button.mouse_click()

        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

        self.perform_scan_email_job_with_addressbook_contacts_enterprise(cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload, custom_book_name, option_payload, pages, pdf_encryption_code, time_out,scan_emulation)

    def perform_scan_email_job_with_addressbook_contacts_enterprise(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, pages=1, pdf_encryption_code=None, time_out=120, scan_emulation=None):
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
            self.goto_email_options()
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
        
        if(pages > 1):
            self.spice.email.goto_email_options()
            self.scan_operations.select_add_more_pages_combo()
            self.back_to_email_landing_view_from_scan_settings()

        self.email_send_enterprise(cdm)

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

        self.wait_for_scan_email_job_to_complete_enterprise(cdm, udw, job, file_type, pages, time_out,scan_emulation=scan_emulation)

    def wait_for_scan_email_job_to_complete_enterprise(self, cdm, udw, job, file_type, pages=1, time_out=120, number_of_jobs_to_check=1,scan_emulation=None):
        """
        wait for scan email job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        common_instance = ScanCommon(cdm, udw)
        if scan_emulation==None:
            scan_resource = common_instance.scan_resource()
        else:
            scan_resource = self.get_scan_resource_used(udw, scan_emulation)    
        logging.info("Scan resource used in Common: %s", scan_resource)
        
        self.scan_operations.flatbed_scan_more_pages_enterprise(cdm, pages)

    def perform_scan_email_job_with_addressbook_contacts_from_menu_scanapp(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, profile_name=None, pages=1, pdf_encryption_code=None, time_out=120, scan_emulation= None):
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
        self.scan_operations.goto_scan_app()
        if profile_name:
            self.email_select_profile(cdm, udw, profile_name)
        else:
            self.goto_email()
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

        self.perform_scan_email_job_with_addressbook_contacts(cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload, custom_book_name, option_payload, pages, pdf_encryption_code, time_out, scan_emulation=scan_emulation)


    def perform_scan_email_job_with_addressbook_contacts(self, cdm, udw, net, job, address_book_type, contact_or_group_name, select_contacts_from, contact_payload=None, custom_book_name=None, option_payload=None, pages=1, pdf_encryption_code=None, time_out=120, scan_emulation=None):
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
            self.goto_email_options()
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
        # wait time should be 0 for stage2 envirement, since job is getting out from the queue immediately  
        self.email_send(wait_time=0)

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



    def verify_to_field_error_value(self, error):
        '''
        Check to field error is false
        @param error: "true/false"
        '''
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_to_field_text)["error"] == error
    
    def get_actual_displayed_message_in_options_screen(self):
        '''
        To get actual displayed message in options screen
        Return: actual displayed message
        '''
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_message,EmailAppWorkflowObjectIds.view_email_option, scrollbar_objectname =EmailAppWorkflowObjectIds.scroll_bar_email_options)
        self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_message)
        actual_displayed_message_str = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.text_box_message} {EmailAppWorkflowObjectIds.textbox_email_enter_pin_textbox}")["text"]

        return actual_displayed_message_str
    
    def verify_displayed_message_in_options_screen(self, input_message):
        '''
        To verify the input message match the actual displayed message
        Args: input message
        '''
        actual_displayed_message_str = self.get_actual_displayed_message_in_options_screen()
        assert actual_displayed_message_str == input_message, "The displayed message is inconsistent with the input message!!!"
        logging.info("The actual displayed message match the input message correctly!")

    def input_message_in_options_screen(self, message, clear_input_box: bool = False):
        """
        input message in options screen, UI should in options screen
        Args:
        message: need to input message
        clear_input_box: clear input box before input message or not
        """
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_message,EmailAppWorkflowObjectIds.view_email_option, scrollbar_objectname =EmailAppWorkflowObjectIds.scroll_bar_email_options)
        message_textbox = self.spice.wait_for(f"{EmailAppWorkflowObjectIds.view_email_option} {EmailAppWorkflowObjectIds.text_box_message}")
        message_textbox.mouse_click()
        if clear_input_box:
            clear_text = self.spice.wait_for(EmailAppWorkflowObjectIds.clear_text_message)
            clear_text.mouse_click()
            self.input_text_from_keyboard(message)
        else:
            self.input_text_from_keyboard(message)
        keyword_ok = self.spice.wait_for(EmailAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def is_landing_expanded(self):
        """
        Return if copy landing sceen is expanded, only preview visible in main panel and detail panel with settings is not shown
        """
        landing_view = self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        return landing_view["isSecondaryCollapsed"]
    
    def scrollto_emailfolder_in_profile_selection(self, folder_name:str):
        """
        UI should be on Usb Folder selection screen.
        UI Flow is Home > Scan > Scan to Usb > Edit
        """
        logging.info("scrolling to folder: %s", folder_name)
        sleep(3)
        logging.info(f"Try to scroll <{folder_name}> into view of screen")
        screen_id =  f"{EmailAppWorkflowObjectIds.view_email_profile_view} {'#SpiceListViewView'}"
        current_screen = self.spice.wait_for(screen_id)
        at_y_end = False
        is_visible = False
        while(is_visible is False and at_y_end is False):
            try:
                is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, folder_name)
                while (is_visible is False and at_y_end is False):
                    self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id,folder_name, top_item_id=EmailAppWorkflowObjectIds.view_email_profile_list_header, select_option=False, start_from_top=True)
                    is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, folder_name)
                    at_y_end = current_screen["atYEnd"]
            except Exception as err:
                logging.info(f"exception msg {err}")
                if str(err).find("Query selection returned no items") != -1:
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, 20)
                    at_y_end = current_screen["atYEnd"]
                else:
                    raise Exception(err)
        logging.info(f"The item <{folder_name}> is in screen view <{screen_id}> now: <{is_visible}>")

        return is_visible
    
    def back_to_back_email_jobs(self, scan_resource, cdm, udw, job, scan_emulation, times=1,send_instance=None):
        """
        Back to back email jobs
        """
        for i in range(times):
            if scan_resource == "MDF":
                scan_emulation.media.load_media('MDF', 1)
            else:
                scan_emulation.media.load_media('ADF', 1)
            self.spice.email.complete_email_send(cdm, udw, job)
            if job.job_concurrency_supported == "false":
                ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok, 10)
                ok_button.mouse_click()
                self.spice.scan_settings.wait_for_non_concurrent_scan_complete_screen_dismiss()
            job.wait_for_no_active_jobs()
            self.spice.email.wait_for_email_send_landing_view()
            if send_instance:
                send_instance.wait_for_corresponding_scanner_status_with_cdm(timeout=30)

    def goto_email_from_scanapp_menu(self, cdm, udw, name: str):
        '''
        Go to email from scanapp menu and select the email profile
        @param name: email profile name
        '''
        button_email = self.spice.wait_for(EmailAppWorkflowObjectIds.button_scan_email + " MouseArea")
        self.spice.wait_until(lambda: button_email["visible"] == True)
        button_email.mouse_click()
        logging.info("Inside scan to email")

        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
        logging.info("Objectname obtained for SMTP server profile")

        current_button = self.spice.wait_for(SCAN_EMAIL_PROFILE  + " MouseArea", timeout = 19.0)
        current_button.mouse_click()
        
    def  goto_email_body_field_in_options(self):
        '''
        From scan email details screen navigate to body field in options screen
        UI Flow is from email details screen -> click on body field
        '''
        current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_options)
        current_button.mouse_click()
        self.workflow_common_operations.goto_item(EmailAppWorkflowObjectIds.textbox_email_message,"#scanMenuListlist1", select_option = False,scrollbar_objectname ="#scanMenuListlist1ScrollBar")
        
    def is_cc_field_locked(self):
        '''
        Checks if the CC field in the email compose form is locked (read-only)
        Returns:
            bool: True if the CC text field is locked, False otherwise
        '''
        text_field = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_cc_field_text)
        return text_field["locked"] == True
    
    def is_bcc_field_locked(self):
        '''
        Checks if the BCC field in the email compose form is locked (read-only)
        Returns:
            bool: True if the BCC text field is locked, False otherwise
        '''
        text_field = self.spice.wait_for(EmailAppWorkflowObjectIds.textbox_email_bcc_field_text)
        return text_field["locked"] == True
    
    def is_body_field_locked(self):
        '''
        Checks if the BCC field in the email compose form is locked (read-only)
        Returns:
            bool: True if the BCC text field is locked, False otherwise
        '''
        text_field = self.spice.wait_for(EmailAppWorkflowObjectIds.text_box_message)
        return text_field["locked"] == True
    
    def verify_continue_button_locked(self, locked=False):
        """
        Verify continue button is locked
        """
        continue_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_continue)
        assert continue_button["locked"] == locked, f"Continue button locked state should be {locked}"
        
    def select_continue_button_in_email_setup_dialog(self):
        """
        Select continue button in email setup dialog
        """
        continue_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_continue)
        continue_button.mouse_click()
        logging.info("Continue button clicked in email setup dialog")
    
    def select_cancel_button_in_email_setup_dialog(self):
        """
        Select cancel button in email setup dialog
        """
        cancel_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_cancelSMTPDialog)
        cancel_button.mouse_click()
        logging.info("Cancel button clicked in email setup dialog")
        
    def verify_email_setup_screen(self):
        """
        Verify email setup screen is displayed
        """
        self.spice.wait_for(EmailAppWorkflowObjectIds.EmailSetUpView)
        logging.info("Email setup screen is displayed")
