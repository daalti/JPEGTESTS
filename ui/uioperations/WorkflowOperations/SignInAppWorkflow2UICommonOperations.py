#########################################################################################
# @file      SignInAppWorkflowUIOperations.py
# @author    Thomas Perdew (thomas.perdew@hp.com), Joshua Byers (joshua.byers@hp.com)
# @date      Mar 3, 2022
# @brief     Implementation Sign In Workflow UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
"""
Implementation Sign In Workflow UI navigation methods
"""
import time
import logging
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.BaseOperations.ISignInAppUIOperations import ISignInAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.BaseOperations.ISignInAppUIOperations import ISignInAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflow2ObjectIds import StatusCenterWorkflow2ObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.security.SecurityTypes import AuthenticationMethod
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds

class SignInAppWorkflow2UIOperations(SignInAppWorkflowUIOperations):

    """
    SignInAppWorkflowUIOperations module for Workflow Operations on SignInApp

    Note: it inherits SignInAppWorkflowUIOperations and overides those methods for Worklfow2.
    """

    def goto_sign_in_app(self, action:str, SignIn:bool = True):
        '''
        UI should be on home screen before calling this method
        Navigate to sign in

        Args:
            action: either "Sign In" or "Sign Out"
        '''
        self.spice.wait_for(SignInAppWorkflowObjectIds.home_swipe_view, timeout=15)
        logging.info("At Home Screen")

        sign_in_button = None
        if action == "Sign In":
            button_name = StatusCenterWorkflow2ObjectIds.button_sign_in
        elif action == "Sign Out":
            button_name = StatusCenterWorkflow2ObjectIds.button_sign_out
        else:
            return None
        
        if self.spice.uisize in {"XS", "S"}:
            # Make sure to Wait for Toast messages to complete before finding the sign-in app 
            # Because Toast messages can cover the sign-in app on small screens
            time.sleep(20) 
    
        try:
            sign_in_button = self.spice.wait_for(button_name, timeout=25.0)
            self.spice.wait_until(lambda: sign_in_button["visible"] == True)
        except QmlItemNotFoundError:
            logging.info("Failed to find the Sign In/Out button.")

        logging.info(f"Sign In button: {sign_in_button}")
        assert sign_in_button != None, logging.error(f"Sign In button does not match what was requested")

        sign_in_button.mouse_click()

    def is_signed_in(self) -> bool:
        return self.spice.home.is_persistent_header_signed_in()

    # def check_signIn_button(self):
    #     """
    #     This is not a function of the Workflow UI so the functionality has changed
    #     """
    #     currentpage = self.spice.wait_for(SignInAppWorkflowObjectIds.invalidSignInView)
    #     assert currentpage
    #     currentpage = self.spice.wait_for(SignInAppWorkflowObjectIds.invalidSignInButton)
    #     currentpage.mouse_click()
    #     #currentpage = self.spice.wait_for(SignInAppWorkflowObjectIds.windowsloginView)
    #     #assert currentpage
    #     currentpage = self.spice.wait_for(SignInAppWorkflowObjectIds.windowsCancelButtonControl)
    #     currentpage.mouse_click()
    #     currentpage = self.spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
        assert currentpage

    def no_user_sign_in(self, net):
        '''
        UI should show Sign In string on home screen when no user login
        Args:
            net
        Return: sign in: True/False
        '''
        sign_in_button = self.spice.status_center.get_sign_in_button("Sign In")
        return sign_in_button != None

    def service_user_verify_auth(self, verify:str) -> bool:
        if verify == "success":
            try:
                screen_view = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service)
            except TimeoutError:
                logging.error("Failed to get successful service user sign in view")
                return False
        else:
            screen_view = self.spice.wait_for(MenuAppWorkflowObjectIds.view_not_authenticated_view)
            if(screen_view == None):
                logging.error("Failed to get invalid sign in view")
                return False

        return True

#######################################################################################
#   UI NAVIGATE TO PERMISSION
#######################################################################################

    def goto_permission(self, permission_id, is_locked = False):
        """
        Method navigates to the input permission from the home menu

        Inputs:
            spice: spice object
            permission_id: GUID of permission being tested
        """

        if permission_id == "81a487d1-b295-47c2-8f86-242d53f5356e": # Fax
            # Get fax app from Menu
            fax_app_button = self.spice.wait_for(MenuAppWorkflowObjectIds.fax_app_button + " MouseArea")
            if is_locked:
                lock_icon = self.spice.wait_for(MenuAppWorkflowObjectIds.fax_app_button + " #statusIconRect SpiceLottieImageView")
                assert lock_icon
                self.spice.wait_until(lambda: lock_icon["visible"] == True)
                logging.info("Fax app lock icon is present")

            fax_app_button.mouse_click()
            if not is_locked:
                # Need to skip past the Fax Setup page
                self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
                fax_cancel_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxNotConfCancel)
                fax_cancel_button.mouse_click()
                logging.info("used cancel button for fax setup")
            
        elif permission_id == "ef92c290-8fa5-4403-85bc-f6becc86b787": # CP_COPY_APP
            # Wait for the app to become clickable
            time.sleep(5) # Need 4-5 second sleep here (Appears like goto_permission is executing before sign-in "welcome" message disappears)
            copy_ui = self.spice.copy_ui()
            if is_locked:
                assert copy_ui.has_lock_icon()
                logging.info("Copy app lock icon is present")
            adminApp = copy_ui.get_copy_app()
            adminApp.mouse_click()

        elif permission_id == "68e44796-779b-479a-b96b-c8f289276210": # Addressbook (Contacts)
            # Move to the Contacts App
            self.spice.contacts.get_menu_contacts_button()
            self.spice.contacts.goto_menu_contacts_screen()
            self.spice.contacts.goto_add_contact_screen()

        elif permission_id == "16798f84-1c9e-4dea-9047-dec431086661": # Send to Email->To Field
            # Move to the Email App->To Field
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.email.goto_email()
            if not is_locked:
                self.spice.email.goto_email_setup_profile()
                #self.spice.email.goto_email_input_field_interactive_summary(setting="toField")

        elif permission_id == "6a482671-4f16-4fd2-9f10-123a58dc0ea4": # Send to Email->From Field
            # Move to the Email App->From Field
            self.spice.scan_settings.goto_scan_app()
            logging.info(f"From Field Test")
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.email.goto_email()
            if not is_locked:
                self.spice.email.goto_email_setup_profile()
                # Check if there is a profile already created and click it, if not pass
                try:
                    profile = self.spice.wait_for("smtpServerc850d3cf-3264-4013-b257-d151dc38a8a9 MouseArea")
                    profile.mouse_click()
                except:
                    pass
                self.spice.email.goto_email_input_field_interactive_summary(setting="fromField")
                self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
                ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
                ok_button.mouse_click()

        elif permission_id == "40132cc0-9ddc-498e-b2ed-1e152f9edc6f": # Send to Email->Subject Field
            # Move to the Email App->Subject Field
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.email.goto_email()
            if not is_locked:
                self.spice.email.goto_email_setup_profile()
                self.spice.email.goto_email_input_field_interactive_summary(setting="subject")

        elif permission_id == "a4cc4bee-09f5-4d06-8bd7-3671472d507a": # Send to Email
            # Move to the Email App
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.email.goto_email()
            self.spice.email.email_select_profile(self.spice.cdm, self.spice.udw, "profile1")

        elif permission_id == "e1c20a2a-235b-4dfd-a92c-f65ae2a45687": # Send to USB
            # Move to the Email App
            self.spice.usb_scan.goto_scan_to_usb()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")

        elif permission_id == "dad496ae-3663-46ea-80a6-62fc7c85de25": # Send to Sharepoint
            # Move to the Sharepoint App
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.scan_settings.goto_sharepoint_from_scanapp_at_menu()

        elif permission_id == "06eefff9-532d-4026-820b-b9c7ab3f4d61": # Send to Computer
            # Move to the Send To Computer App
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.scan_computer.goto_scan_to_computer()

        elif permission_id == "aacb972e-6716-43ec-9133-4eb6ee2542dd": # Send to Folder
            # Move to the Folder App
            self.spice.scan_settings.goto_scan_app()
            if is_locked:
                assert self.spice.scan_settings.has_lock_icon()
                logging.info("Scan app lock icons are present")
            self.spice.scan_settings.goto_folder_from_scanapp_at_menu()

        elif permission_id == "fc1f5a75-aeb4-474a-b712-4ef20c2a18e0": # View Jobs
            job_app = self.spice.job_ui
            if is_locked:
                assert job_app.has_lock_icon()
                logging.info("Jobs app lock icons are present")
            self.spice.main_app.scroll_to_find(self.spice.main_app.locators.job_queue_app_button)
            self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.job_queue_app_button)
        else:
            assert False, f"Could not navigate to permission! ({permission_id} not found)"

    def support_sign_in_app_from_fp(self):
        """
        This function is to checek sign in app supported on printer ui or not

        Return:
              True: sign in app supported on UI
              False: sign in app doesn't supported on UI
        """

        self.spice.goto_homescreen()

        try:
            return self.is_signed_in()

        except Exception as err:
            logging.info("sign in app does not supported on UI")
            return False

    def goto_universal_sign_in(self, text:str):
        """
        This method attempt to click the sign-in/sign-out button in the persistent header on Workflow 2.0 device.

        Args:
            text: Either "Sign In" or "Sign Out"

        Return:
            Nothing
            Raises an exception if user is already signed in or already signed out
        """
        if self.spice.home.is_persistent_header_signed_in():
            if text == "Sign Out":
                self.spice.home.click_sign_out_button()
                assert self.click_sign_out_button()
                assert self.verify_user_sign_out_toast_message()
            else:
                assert False, logging.error(f"Cannot sign in because the device is already signed in")
        else:
            if text == "Sign In":
                self.spice.home.click_sign_in_button()
                assert self.is_on_sign_in_page(),\
                    logging.error(f"Failed to navigate to sign in page.")
            else:
                assert False, logging.error("Cannot sign out because device is already signed out")
    
    def goto_universal_sign_out(self, verify_sign_out_string:bool=False):
        """
        This method attempts to click the sign-out button in the persistent header on Workflow 2.0 device.

        Args:
            verify_sign_out_string: If True, it will verify that the sign-out string is present after clicking the button.

        Return:
            Nothing
            Raises an exception if user is already signed out or cannot find the sign-out button
        """
        if not self.spice.home.is_persistent_header_signed_in():return
        self.spice.home.click_sign_out_button()
        assert self.click_sign_out_button(), logging.error("Failed to click sign out button")
        if verify_sign_out_string:
            assert self.verify_user_sign_out_toast_message()
        else:
            assert self.wait_for_toast_message_to_complete()

    def wait_for_toast_message_to_complete(self, wait_timeout:float=WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS) -> bool:
        toast_message_text=self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.toastMessageText, timeout=wait_timeout)
        timer=wait_timeout
        while toast_message_text and timer >= 0:
            toast_message_text=self.spice.check_item(SignInAppWorkflowObjectIds.toastMessageText)
            timer -= 1
            time.sleep(1)
        return not toast_message_text

    def get_sign_in_status(self):
        """
        This method will check if a user (any user) is signed in or out of the device.

        Return:
            Returns a string containing "Sign In" or "Sign Out" or throws exception if neither
        """
        button = self.spice.query_item("#HomeScreenView #persistentHeader #SignInButton")
        if not button:
            logging.error("Failed to get any sign-in/sign-out button from the persistent header")
            raise
        if self.spice.home.is_persistent_header_signed_in(): return "Sign Out"
        else: return "Sign In"

    def on_user_info_page(self, waitForExists:bool=True) -> bool:
        """
        Check if the user info page is displaying

        Args:
            No arguments
        
        Returns:
            bool: True if user info page is displaying, False otherwise
        
        Raises:
            None
        """
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        return self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoView, timeout=timeout)
    
    def get_user_info_initials(self) -> str:
        """
        Gets the user's initials from the user info page

        Args:
            No arguments
        
        Returns:
            str: The user's initials
        
        Raises:
            None
        """
        initials = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoInitial)
        return self.workflow_common_operations.get_element_property(initials, "text")
    
    def get_user_info_username(self) -> str:
        """
        Gets the user's username from the user info page

        Args:
            No arguments
        
        Returns:
            str: The user's username
        
        Raises:
            None
        """
        username = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoUsername)
        return self.workflow_common_operations.get_element_property(username, "text")

    def get_user_info_email_address(self) -> str:
        """
        Gets the user's email address from the user info page

        Args:
            No arguments
        
        Returns:
            str: The user's email address
        
        Raises:
            None
        """
        email = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoEmail)
        return self.workflow_common_operations.get_element_property(email, "text")

    def click_sign_out_button(self) -> bool:
        """
        Clicks the sign-out button from the user info page

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' was performed, False otherwise
        
        Raises:
            None
        """
        sign_out_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoSignOutButton)
        return self.workflow_common_operations.click(sign_out_button)
    
    def click_switch_accounts_button(self) -> bool:
        """
        Clicks the switch account button on the user info page

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' was performed, False otherwise
        
        Raises:
            None
        """
        switch_account_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoSwitchAccountButton)
        return self.workflow_common_operations.click(switch_account_button)

    def click_user_info_close_button(self) -> bool:
        """
        Clicks the close button ('x' in the top right corner) on the user info page

        Args:
            No arguments

        Returns:
            bool: True if the 'click' was perfomred, False otherwise

        Raises:
            None
        """
        close_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.userInfoCloseButton)
        return self.workflow_common_operations.click(close_button)
    
    def login_and_out_to_cross_session_boundary(self, spice, username, password):
        """
        Helper function to login and logout to cross session boundary and bring RBAC setting live to the UI.
        """
        spice.goto_homescreen()
        self.goto_universal_sign_in("Sign In")
        self.select_device_user_login()
        self.enter_creds(login=True,authAgent="user", password=password, username=username)
        response = self.verify_auth("success")
        assert response, "Login with valid device user credentials failed"
        self.goto_universal_sign_in("Sign Out")
