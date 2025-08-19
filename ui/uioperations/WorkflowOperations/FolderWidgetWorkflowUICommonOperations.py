#########################################################################################
# @file      FolderWidgetWorkflowUICommonOperations.py
# @author    Sundeep Kishan(sundeep.kishan@hp.com)
# @date      Dec 20, 2022
# @brief     Implementation Folder Widget Workflow UI methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
"""
Implementation Folder Widget Workflow UI methods
"""
import logging
from time import sleep
from dunetuf.ui.uioperations.BaseOperations.IFolderWidgetWorkflowUIOperations import IFolderWidgetWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FolderWidgetWorkflowObjectIds import FolderWidgetWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from tests.send.ews.contacts.contacts_sample_payload import *
from dunetuf.ews.DefaultFolderEws import *
from dunetuf.ui.uioperations.PomOperations.MainApp.MainAppPage import MainAppPage

DEVICEUSER_ROLE_USER = "a69a546c-dd68-4e4b-8302-97cd6471a0a4"
GuestRoleGuid = "0a52b510-5db2-49f2-b95d-7f5c37c50235"

class FolderWidgetWorkflowUIOperations(IFolderWidgetWorkflowUIOperations):
    """
    FolderWidgetWorkflowUIOperations module for Workflow Operations on Folder widget
    """
    def __init__(self, spice):
        self.maxtimeout = 100
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self.spice)

    def scroll_to_Folder_widget(self):
        '''
        Scrolls to folder widget on Homescreen
        '''
        sleep(2)
        self.goto_menu_mainMenu()
        assert self.spice.wait_for("#HomeScreenView #folderWidget", timeout=15.0)["visible"] == True, 'Widget not visible'

        self.workflow_common_operations.scroll_to_widget(loader= FolderWidgetWorkflowObjectIds.widgets_grid_layout,element_id = FolderWidgetWorkflowObjectIds.folder_widget_app)


    def click_on_folder_widget(self, clicked_item = None):
        '''
        Clicking Item on Folder widget Home screen.
        '''
        sleep(2)
        self.goto_menu_mainMenu()
        assert self.spice.query_item("#HomeScreenView #folderWidget")["visible"] == True, 'Widget not visible'
        item = self.spice.wait_for(clicked_item, timeout=7.0)
        item.mouse_click()
    
    def click_folder_widget(self):
        '''
        Clicking folder widget Item on Folder widget Home screen.
        '''
        sleep(2)
        self.goto_menu_mainMenu()
        assert self.spice.query_item(f"{FolderWidgetWorkflowObjectIds.home_screen_view} {FolderWidgetWorkflowObjectIds.folder_widget}")["visible"] == True, 'Widget not visible'
        item = self.spice.wait_for(FolderWidgetWorkflowObjectIds.folder_widget)
        self.spice.validate_button(item)
        item.mouse_click()
    
    def click_start_button_on_folder_widget(self):
        '''
        Clicking start button on Folder widget Home screen.
        '''
        sleep(2)
        self.goto_menu_mainMenu()
        assert self.spice.query_item(f"{FolderWidgetWorkflowObjectIds.home_screen_view} {FolderWidgetWorkflowObjectIds.folder_widget}")["visible"] == True, 'Widget not visible'
        start_button = self.spice.wait_for(FolderWidgetWorkflowObjectIds.folder_widget_start_button, timeout=7.0)
        self.spice.validate_button(start_button)
        start_button.mouse_click()
    
    def click_option_button_on_folder_widget(self):
        '''
        Clicking option button on Folder widget Home screen.
        '''
        sleep(2)
        self.goto_menu_mainMenu()
        assert self.spice.query_item(f"{FolderWidgetWorkflowObjectIds.home_screen_view} {FolderWidgetWorkflowObjectIds.folder_widget}")["visible"] == True, 'Widget not visible'
        option_button = self.spice.wait_for(FolderWidgetWorkflowObjectIds.folder_widget_options_button, timeout=7.0)
        self.spice.validate_button(option_button)
        option_button.mouse_click()

    def check_for_folder_widget_ana_sign_in_screen(self):
        self.spice.wait_for(FolderWidgetWorkflowObjectIds.folder_widget, timeout=7.0)
        sign_in_button = self.spice.wait_for(f"{FolderWidgetWorkflowObjectIds.folder_widget} {FolderWidgetWorkflowObjectIds.folder_widget_sign_in_button}", timeout=7.0)
        self.spice.validate_button(sign_in_button)
        sign_in_button.mouse_click()
        self.spice.signIn.verifySignInPopup(expected = False)

    def goto_menu_mainMenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
        logging.info("At Home Screen")
        # TODO - Need to check the menu app is visible or not
        # check whether the menu is visible on the screen
        menuApp = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp)
        self.spice.wait_until(lambda: menuApp["visible"] == True)

    def verify_default_folder_not_configured_pop_up(self, expected):
        """
        Method to verify default network folder is not configured pop up shown in the UI.
        Inputs:
            expected: True = default folder not configured pop up is shown, False = pop up not shown
        Returns:
            True if default folder not configured pop up is shown
        """
        try:
            logging.info("Not configured InPopup")
            self.spice.wait_for(FolderWidgetWorkflowObjectIds.not_config_alert_message, timeout=7.0)
            result = True
            # Exit the pop up
            okbutton = self.spice.wait_for(FolderWidgetWorkflowObjectIds.not_config_alert_message_ok_button, timeout=7.0)
            okbutton.mouse_click()
        except:
            result = False
        return bool(expected == result)

    def check_default_folder_display_name_on_widget(self, net, displayname_string_id = None, displayname = None):
        """
        Check default folder display name on folder widget
        """
        # waiting for folder widget display name
        self.spice.wait_for(FolderWidgetWorkflowObjectIds.default_folder_displayName, timeout=7.0)
        # Verifying folder display name with param displayname
        if displayname == None:
            self.spice.common_operations.verify_string(net, displayname_string_id, FolderWidgetWorkflowObjectIds.default_folder_displayName )
        else:
            self.verify_displayname_string(displayname)

    def check_for_homescreen(self):
        # HomeScreen
        home = self.spice.main_app.get_home()
        self.spice.main_app.wait_locator_enabled(self.spice.main_app.locators.ui_main_app)
        self.spice.validate_app(home, False)
        
    def scan_app_permissions_setup(self, ews,cdm,spice,permissionID,user,access):
        if access:
            if not cdm.rbac.is_permission_granted_to_role(user, permissionID):
                cdm.rbac.grant_permission_to_role(user, permissionID)
        else:
            if cdm.rbac.is_permission_granted_to_role(user, permissionID):
                cdm.rbac.deny_permission_to_role(user, permissionID)
        cdm.device_user.create_user('tester', '', 'Test@12345', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)
        logging.info("Step 1: Enter valid credentials")
        # spice.signIn.goto_sign_in_app("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@12345", username="tester")
        response = spice.signIn.verify_auth("success")
        assert response, "Login with valid device user credentials failed"
        
    def configure_default_folder_to_not_set(self, ews):
        ews.default_folder_settings_ews.default_folder_page_load()
        # Check Apply, Cancel Buttons
        ews.default_folder_settings_ews.verify_apply_button_is_visible(True)
        ews.default_folder_settings_ews.verify_cancel_button_is_visible(True)
        ews.default_folder_settings_ews.select_default_folder_config_type(
            DefaultFolderConfigType.NOT_SET)
        # Apply settings
        ews.default_folder_settings_ews.click_apply_btn_default_folder()
        # Check that the successful toast is show
        ews.default_folder_settings_ews.check_successful_toast()
        
    def configure_default_folder_with_specify_folder_option(self, ews, sharedfoldertype = 'standardsharedfolder', folderpath = None, username = None, password = None, displayname = None, domain = None ,signedin = None):
        ews.default_folder_settings_ews.default_folder_page_load()
        # Check Apply, Cancel Buttons
        ews.default_folder_settings_ews.verify_apply_button_is_visible(True)
        ews.default_folder_settings_ews.verify_cancel_button_is_visible(True)
        ews.default_folder_settings_ews.select_default_folder_config_type(
            DefaultFolderConfigType.SPECIFY_FOLDER)
        ews.default_folder_settings_ews.input_default_folder_displayname(
            displayname)
        if sharedfoldertype == 'personalsharedfolder':
            ews.default_folder_settings_ews.select_default_folder_type(
                DefaultFolderType.PERSONAL)
            ews.default_folder_settings_ews.set_personal_folder_options()
        else:
            foldertypeavailablity = ews.default_folder_settings_ews.wait_for_shared_folder_type_label()
            if foldertypeavailablity == True:
                ews.default_folder_settings_ews.select_default_folder_type(
                    DefaultFolderType.SMB)
            ews.default_folder_settings_ews.set_standard_folder_common_options(
                folderpath)
            ews.default_folder_settings_ews.set_standard_folder_credential_options(
                    username, password, domain, signedin)
        # Apply settings
        ews.default_folder_settings_ews.click_apply_btn_default_folder()
        # Check that the successful toast is show
        ews.default_folder_settings_ews.check_successful_toast()
        
    def configure_default_folder_with_specify_contact_option(self, cdm, ews, addresbook, displayname):
        # Load digitalSends contacts page
        ews.contacts.contacts_page_load()
        status = ews.contacts.contacts_page_initialized()
        assert status == True, "Contacts page load Failed!!!"
        # Get Fax support
        faxsupport = addresbook.get_addressbobook_fax_support(cdm)
        # test create a contact with a network folder
        ews.contacts.create_contact(
            contact_details_with_network_folder, faxsupport, True)
        ews.default_folder_settings_ews.default_folder_page_load()
        # Check Apply, Cancel Buttons
        ews.default_folder_settings_ews.verify_apply_button_is_visible(True)
        ews.default_folder_settings_ews.verify_cancel_button_is_visible(True)
        ews.default_folder_settings_ews.select_default_folder_config_type(
            DefaultFolderConfigType.CONTACT)
        ews.default_folder_settings_ews.input_default_folder_displayname(
            displayname)
        # select the record created
        ews.default_folder_settings_ews.set_contact_created_for_default_folder()
        # Apply settings
        ews.default_folder_settings_ews.click_apply_btn_default_folder()
        # Check that the successful toast is show
        ews.default_folder_settings_ews.check_successful_toast() 
    
    def verify_displayname_string(self, displayname):
        """
        This method compares the displayname string of network folder quickset with the expected string
        Args:
            UI should be in default network folder view
            displayname: expected displayname string
        """
        ui_displayname_string = self.spice.query_item(FolderWidgetWorkflowObjectIds.default_folder_displayName+" #contentItem")["text"]
        logging.info("displayname = " + ui_displayname_string)
        assert ui_displayname_string == displayname, "displayname mismatch"

    def verify_landingview_click_done_button( self, net):
        #Check for Folder App Landing view
        assert self.spice.wait_for(FolderWidgetWorkflowObjectIds.view_scan_network_folder_landing, timeout=7.0)
        self.validate_screen_buttons(net, False, FolderWidgetWorkflowObjectIds.button_network_folder_send, True)
        self.spice.network_folder.wait_and_click_on_middle(FolderWidgetWorkflowObjectIds.button_network_folder_send)

    def wait_for_scan_status_modal(self, message: str = "complete", timeout=60):
        if message == "scanning":
            self.spice.wait_for(FolderWidgetWorkflowObjectIds.job_modal_progress_view, timeout)
        elif message == "complete":
            self.spice.wait_for(FolderWidgetWorkflowObjectIds.job_modal_complete_view, timeout)
            ok_button = self.spice.query_item("#OK")
            ok_button.mouse_click()

    def wait_for_widget(self, expected):
        try:
            self.spice.wait_for("#HomeScreenView #folderWidget")
            visible = True
        except:
            visible = False

        return bool(expected == visible)

    def ldap_sign_in_config(self,ews):
        logging.debug("\n Configuring LDAP SignIn")
        ldapSignInConfig = {'enableLdap': True,
                'serverAddress': '15.6.28.181',
                'port': 389,
                'securessl': False,
                'credentialType': "admin",
                'bindPrefix': 'cn',
                'userName': 'cn=keymaster,cn=users,dc=jsdomain,dc=boi,dc=rd,dc=hpicorp,dc=net',
                'userPassword': 'Pass1701',
                'ldapBindRoots': 'DC=ds2016,DC=boi,DC=rd,DC=hpicorp,DC=net',
                'matchLdapNameAttribute': 'uid',
                'retrieveLdapEmailAttribute': 'mail',
                'retrieveLdapNameAttribute': 'displayName',
                'retrieveLdapGroupAttribute': 'objectClass',
                'enableGroupExactMatch': False}

        # Enable LDAP configuration
        ews.security_app.access_control_page.ldap_setup_tab.configure_ldapSettings(ldapSignInConfig)

    def ldap_sign_in(self):
        self.spice.goto_homescreen()
        self.spice.signIn.goto_sign_in_app("Sign In")
        self.spice.signIn.select_sign_in_method("ldap", "admin")
        self.spice.signIn.enter_creds(True, "ldap", "Pass1701", "cn=keymaster,cn=users,dc=jsdomain,dc=boi,dc=rd,dc=hpicorp,dc=net")
        self.spice.signIn.verify_auth("success")
        
        
    def check_default_folder_widget_options_and_value(self, net, option_id:str, option_string:str, value_id:str, value_string:str):
        """
        Check default folder folder options and values on folder widget
        """
        self.spice.wait_for(option_id, timeout=7.0)
        self.spice.common_operations.verify_string(net, option_string, option_id)
        self.spice.wait_for(value_id, timeout=7.0)
        self.spice.common_operations.verify_string(net, value_string, value_id)
    
    def check_default_folder_widget_options_and_default_value(self, net, option):
        """
        Check default folder options and values on folder widget
        @param: option: default folder option on folder widget, "color_mode"/"content_type"/"resolution"/"file_type"
        """
        if (option == "color_mode"):
            option_id = FolderWidgetWorkflowObjectIds.color_mode_option
            option_string = FolderWidgetWorkflowObjectIds.color_mode_option_text
            value_id = FolderWidgetWorkflowObjectIds.color_mode_value
            value_string = FolderWidgetWorkflowObjectIds.color_value_text
        elif (option == "content_type"):
            option_id = FolderWidgetWorkflowObjectIds.content_type_option
            option_string = FolderWidgetWorkflowObjectIds.content_type_option_text
            value_id = FolderWidgetWorkflowObjectIds.content_type_value
            value_string = FolderWidgetWorkflowObjectIds.mixed_value_text
        elif (option == "resolution"):
            option_id = FolderWidgetWorkflowObjectIds.resolution_option
            option_string = FolderWidgetWorkflowObjectIds.resolution_option_text
            value_id = FolderWidgetWorkflowObjectIds.resolution_value
            value_string = FolderWidgetWorkflowObjectIds.three_hundred_dpi_value_text
        elif (option == "file_type"):
            option_id = FolderWidgetWorkflowObjectIds.file_type_option
            option_string = FolderWidgetWorkflowObjectIds.file_type_text
            value_id = FolderWidgetWorkflowObjectIds.file_type_value
            value_string = FolderWidgetWorkflowObjectIds.tiff_value_text
        else:
            assert False, "Setting not existing"

        self.spice.wait_for(option_id, timeout=7.0)
        self.spice.common_operations.verify_string(net, option_string, option_id)
        self.spice.wait_for(value_id, timeout=7.0)
        self.spice.common_operations.verify_string(net, value_string, value_id)

    def validate_screen_buttons(self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible):
        button_ids = [
            NetworkFolderAppWorkflowObjectIds.button_network_folder_send,
            NetworkFolderAppWorkflowObjectIds.button_network_folder_start,
            NetworkFolderAppWorkflowObjectIds.button_network_folder_main_send
        ]

        button = None
        for button_id in button_ids:
            if buttonObjectId == button_id:
                try:
                    button = self.spice.wait_for(button_id, 60)
                    logging.info("Found button with ID %s", button_id)
                    self.spice.network_folder.wait_and_validate_property_value(button, "visible", True, 30, delay = 0.01)
                    self.spice.network_folder.wait_and_validate_property_value(button, "enabled", True, 30, delay = 0.01)
                    self.spice.network_folder.wait_and_validate_property_value(button, "constrained", isButtonConstrained, 30, delay = 0.01)
                    break
                except:
                    logging.info("Button with ID %s not found", button_id)
                    continue

        if button is None:
            logging.error("Button with ID %s not found", buttonObjectId)
            raise ValueError(f"Button with ID {buttonObjectId} not found")
        #Get Eject
        ejectButton = self.spice.wait_for( FolderWidgetWorkflowObjectIds.eject_button,10)

        #Validate eject
        self.spice.network_folder.wait_and_validate_property_value(ejectButton, "visible", isEjectButtonVisible, delay = 0.01)