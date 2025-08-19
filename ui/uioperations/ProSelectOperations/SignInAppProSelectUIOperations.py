#########################################################################################
# @file      SignInAppProSelectUIOperations.py
# @author    Zachary Goodspeed (zachary.goodspeed@hp.com)
# @date      May 19, 2021
# @brief     Implementation Sign In UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
#########################################################################################
"""
Implementation Sign In UI navigation methods
"""
import time
import logging
from enum import Enum
from dunetuf.ui.uioperations.BaseOperations.ISignInAppUIOperations import ISignInAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from tests.security.accountManagement.WindowsAuth.WindowsAuthTestHelper import WindowsAuthTestHelper
from dunetuf.security.SecurityTypes import AuthenticationMethod


class SignInAppProSelectUIOperations(ISignInAppUIOperations):

    """
    SignInAppProSelectUIOperations module for Proselect Operations on SignInApp
    """
    TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY = 1
    TIMEOUT_SIGN_IN_SUCCESS = 90
    MAX_SCROLL_TIMEOUT = 30

    SIGN_IN_OPERATION_STRING = 'Sign In'
    SIGN_OUT_OPERATION_STRING = 'Sign Out'
    #----------------------------------Function Keywords--------------------------------#
    # Buttons
    menu_item_signinid = "#7db992ba-557a-461c-b941-6023aa8cfa34"

    identificationCode_button = "#identificationCodeButton"
    windows_button = "#windowsButton"
    ldap_button = "#ldapButton"
    printerUser_button = "#deviceUserButton"
    localadmin_button = "#adminButton"

    cancel_button = "#Cancel"

    signin_button_prefix = "#signInMethodButton"
    ok_button_prefix = "#signInOkButton"
    user_button_prefix = "#enterUsernameButton"
    password_button_prefix = "#enterPasswordButton"


    # TODO determine why local admin cannot use the same enterPasswordButton and signInOkButton without breaking the other login types
    # does the button on each screen need to be unique?
    local_admin_password_button = "#localAdminPasswordButton"
    local_admin_ok_button = "#localAdminOkButton"
    failedAuth_ok_button = "#failedOkButton"

    # Views
    localadminview = "#LocalAdminView"
    networkuserpasswordview = "#NetworkUserPasswordView"
    localuserpasswordview = "#LocalUserPasswordView"
    signinmethodview = "#signInMethodView"
    identificationCodeView = "#identificationCodeView"
    windowsView = "#WindowsView"
    ldapView = "#LdapView"
    deviceUserView = "#DeviceUserView"
    welcomeUserView = "#WelcomeUserView"
    signingInView = "#SigningInView"

    def __init__(self, spice):
        self.spice = spice
        self.proselect_common_operations = ProSelectCommonOperations(self.spice)
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self.spice)
        self.last_used_authentication_method:AuthenticationMethod = AuthenticationMethod.PrinterUser

    
    def get_view_mouse_area_locator(self, authentication_agent:AuthenticationMethod) -> str:
        logging.info(f"auth agent: {authentication_agent}")
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return ProSelectUIObjectIds.PrinterUserView + " MouseArea"
        elif authentication_agent == AuthenticationMethod.Windows:
            return ProSelectUIObjectIds.WindowsView
        elif authentication_agent == AuthenticationMethod.Ldap:
            return ProSelectUIObjectIds.LDAPView
        elif authentication_agent == AuthenticationMethod.Admin:
            return ProSelectUIObjectIds.AdminView
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent.value}'")
            return ""
    
    def get_username_button_locator(self, authentication_agent:AuthenticationMethod) -> str:
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return ProSelectUIObjectIds.PrinterUserNameButton
        elif authentication_agent == AuthenticationMethod.Windows:
            return ProSelectUIObjectIds.WindowsUserNameButton
        elif authentication_agent == AuthenticationMethod.Ldap:
            return ProSelectUIObjectIds.LdapUserNameButton
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent.value}'")
            return ""
    
    def get_password_button_locator(self, authentication_agent:AuthenticationMethod) -> str:
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return ProSelectUIObjectIds.PrinterUserPasswordButton
        elif authentication_agent == AuthenticationMethod.Windows:
            return ProSelectUIObjectIds.WindowsPasswordButton
        elif authentication_agent == AuthenticationMethod.Ldap:
            return ProSelectUIObjectIds.LdapPasswordButton
        elif authentication_agent == AuthenticationMethod.Admin:
            return ProSelectUIObjectIds.AdminPasswordButton
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent.value}'")
            return ""

    def __convert_authentication_agent_enumeration_to_agent_string(self, auth_agent:AuthenticationMethod) -> str:
        outcome = ''
        if auth_agent == AuthenticationMethod.PrinterUser: outcome = "user"
        elif auth_agent == AuthenticationMethod.Admin: outcome = "admin"
        elif auth_agent == AuthenticationMethod.Windows: outcome = "windows"
        elif auth_agent == AuthenticationMethod.Ldap: outcome = "ldap"
        elif auth_agent == AuthenticationMethod.IDCode: outcome = "identificationCode"
        elif auth_agent == AuthenticationMethod.Smartcard: outcome = "smartcard"
        else: assert False, logging.error(f"{auth_agent} not yet supported by this method")
        return outcome
    
    def __convert_authentication_agent_string_to_agent_enumeration(self, auth_agent:str) -> AuthenticationMethod:
        outcome = ''
        if auth_agent == "user": outcome = AuthenticationMethod.PrinterUser
        elif auth_agent == "admin": outcome = AuthenticationMethod.Admin
        elif auth_agent =="windows": outcome = AuthenticationMethod.Windows
        elif auth_agent == "ldap": outcome = AuthenticationMethod.Ldap
        elif auth_agent == "identificationCode": outcome = AuthenticationMethod.IDCode
        elif auth_agent == "smartcard": outcome = AuthenticationMethod.Smartcard
        else: assert False, logging.error(f"{auth_agent} not yet supported by this method")
        return outcome

    def get_authentication_agent_name_locator(self, authentication_agent:AuthenticationMethod) -> str:
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return ProSelectUIObjectIds.PrinterUser
        elif authentication_agent == AuthenticationMethod.Windows:
            return ProSelectUIObjectIds.Windows
        elif authentication_agent == AuthenticationMethod.Ldap:
            return ProSelectUIObjectIds.Ldap
        elif authentication_agent == AuthenticationMethod.Admin:
            return ProSelectUIObjectIds.Admin
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent.value}'")
            return ""

    def reset_sign_in_page_scroll_bar(self) -> bool:
        scroll_bar = self.proselect_common_operations.get_element(ProSelectUIObjectIds.SignInPageScrollBar)
        if not self.proselect_common_operations.set_element_property(scroll_bar, "position", 0.0):
            logging.error("Failed to scroll to position 0.0")
            return False
        logging.info(f"Sign-In Scroll Bar Position: {self.proselect_common_operations.get_element_property(scroll_bar, 'position')}")
        return True
    
    def reset_sign_in_page_scroll_bar_manually(self, auth_agent) -> bool:
        view_mouse_area_locator = self.get_view_mouse_area_locator(auth_agent)
        logging.debug(f"Reset Sign-In Page Scroll Bar Manually Mouse Area View Locator: {view_mouse_area_locator}")
        view_mouse_area = self.proselect_common_operations.get_element(view_mouse_area_locator)
        return self.proselect_common_operations.scroll_left_increment(view_mouse_area, 10)
    
    def scroll_sign_in_page_down_manually(self, auth_agent, amount) -> bool:
        view_mouse_area_locator = self.get_view_mouse_area_locator(auth_agent)
        view_mouse_area = self.proselect_common_operations.get_element(view_mouse_area_locator)
        if not self.proselect_common_operations.scroll_right_increment(view_mouse_area, amount):
            logging.error("Failed to scroll down on the sign-in page")
            return False
        return True
    
    def scroll_sign_in_page_down_to(self, auth_agent, locator, timeout=15) -> bool:
        view_mouse_area_locator = self.get_view_mouse_area_locator(auth_agent)
        view_mouse_area = self.proselect_common_operations.get_element(view_mouse_area_locator)
        element = self.proselect_common_operations.get_element(locator)
        if not element:
            return False
        while not self.proselect_common_operations.get_element_property(element, "activeFocus") and timeout > 0:
            self.proselect_common_operations.scroll_right_increment(view_mouse_area, 1)
            timeout -= 1
            time.sleep(1)
        return True

    def goto_sign_in_app(self, action:str, clickSignIn:bool = True):
        '''
        UI should be on home screen before calling this method
        Navigate to sign in

        Args:
            action: either "Sign In" or "SignOut"
        '''
        homeApp = self.spice.query_item(ProSelectUIObjectIds.homeScreenView)
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)
        logging.info("At Home Screen")

        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll to the next option first
        homeApp.mouse_wheel(180,180)
        # scroll till you reach the Sign In option
        while (self.spice.query_item("#CurrentAppText")["text"] != action and timeSpentWaiting < self.MAX_SCROLL_TIMEOUT):
            homeApp.mouse_wheel(0,0)
            timeSpentWaiting = time.time() - startTime
        
        if self.spice.query_item("#CurrentAppText")["text"] != action:
            logging.error(f"Failed to scroll to: {action}")
            return

        if clickSignIn:
            currentApp = self.spice.wait_for(self.menu_item_signinid)
            currentApp.mouse_click()     

    def select_sign_in_method(self, signInMethod, defaultAuthAgent):
        """
        Method to select the auth agent used for sign-in

        Args:
            signInMethod: Method to be selected (OPTIONS: "user", "customUser", "admin", "windows", "ldap")
            defualtAuthAgent: Auth agent expected as default (OPTIONS: "user", "admin", "windows", "ldap")
        """
        
        signInMethod = "User" if (signInMethod == "customUser") else signInMethod
        signInMethod = self.__convert_authentication_agent_string_to_agent_enumeration(signInMethod)
        if defaultAuthAgent:
            defaultAuthAgent = self.__convert_authentication_agent_string_to_agent_enumeration(defaultAuthAgent)
            currentSignInPage = self.get_authentication_method_from_current_sign_in_page()
            assert defaultAuthAgent == currentSignInPage,\
                logging.error(f"Default auth agent '{defaultAuthAgent}' does not match current sign in page '{currentSignInPage}'")
        # Declare the prefix for the sign-in method button
        signin_button = self.signin_button_prefix

        if signInMethod == AuthenticationMethod.Windows:
            methodButton = self.windows_button
        elif signInMethod == AuthenticationMethod.Ldap:
            methodButton = self.ldap_button
        elif signInMethod == AuthenticationMethod.Admin:
            methodButton = self.localadmin_button
        elif signInMethod == AuthenticationMethod.PrinterUser:
            methodButton = self.printerUser_button
        else:
            raise NotImplementedError(f"{signInMethod} is not yet implemented by this method.")

        if not defaultAuthAgent:
            defaultAuthAgent = self.get_authentication_method_from_current_sign_in_page()
        
        if defaultAuthAgent == AuthenticationMethod.Windows:
            methodView = self.windowsView
            signin_button += "Windows"
        elif defaultAuthAgent == AuthenticationMethod.Ldap:
            methodView = self.ldapView
            signin_button += "Ldap"
        elif defaultAuthAgent == AuthenticationMethod.Admin:
            methodView = self.localadminview
        elif defaultAuthAgent == AuthenticationMethod.PrinterUser:
            methodView = self.deviceUserView
            signin_button += "User"
        else:
            raise NotImplementedError(f"{defaultAuthAgent} is not yet implemented by this method.")

        self.proselect_common_operations.goto_item(signin_button, methodView)
        time.sleep(1)
        self.proselect_common_operations.goto_item(methodButton, self.signinmethodview)
        time.sleep(1)

    def has_password_reveal_icon(self) -> bool:
        """
            Proselect devices do not have password reveal icons on the password field
        """
        return False

    def enter_username(self, username: str) -> bool:
        agent = self.get_authentication_method_from_current_sign_in_page()
        if not self.reset_sign_in_page_scroll_bar_manually(agent):return False

        username_button_locator = self.get_username_button_locator(agent)
        logging.debug(f"Username Button Locator: {username_button_locator}")
        if not self.scroll_sign_in_page_down_to(agent, username_button_locator):
            logging.error("Failed to scroll to username button")
            return False
        username_button = self.proselect_common_operations.get_element(username_button_locator)
        if not self.proselect_common_operations.click(username_button):
            logging.error("Failed to click username field")
            return False
        
        try:
            self.spice.keyBoard.keyboard_set_text_with_out_dial_action(username)
        except AssertionError:
            logging.error(f"Failed to enter username '{username}'")
            return False
        
        time.sleep(1)
        return True
    
    def enter_password(self, password: str) -> bool:
        agent = self.get_authentication_method_from_current_sign_in_page()
        if not self.reset_sign_in_page_scroll_bar_manually(agent): return False
        
        password_button_locator = self.get_password_button_locator(agent)
        if not self.scroll_sign_in_page_down_to(agent, password_button_locator):
            logging.error("Failed to scroll to password button")
            return False
        password_button = self.proselect_common_operations.get_element(password_button_locator)
        if not password_button:
            logging.error("Failed to get password button")
            return False
        
        if not self.proselect_common_operations.click(password_button):
            logging.error("Failed to click password field")
            return False
        
        try:
            self.spice.keyBoard.keyboard_set_text_with_out_dial_action(password)
        except AssertionError:
            logging.error(f"Failed to enter password '{password}'")
            return False

        time.sleep(1)
        return True
    
    def click_sign_in_button(self) -> bool:
        agent = self.get_authentication_method_from_current_sign_in_page()
        if not self.reset_sign_in_page_scroll_bar_manually(agent): return False
        if agent == AuthenticationMethod.Admin:
            ok_button_locator = "#localAdminOkButton"
        else:
            ok_button_locator = ProSelectUIObjectIds.SignInOkButton + self.get_authentication_agent_name_locator(agent)
        if not self.scroll_sign_in_page_down_to(agent, ok_button_locator):
            logging.error("Failed to scroll to sign-in button")
            return False
        ok_button = self.proselect_common_operations.get_element(ok_button_locator)
        if not ok_button:
            logging.error("Failed to get Ok button")
            return False
        
        outcome = self.proselect_common_operations.click(ok_button)
        if outcome: time.sleep(1)
        return outcome
    
    def click_signing_in_cancel_button(self) -> bool:
        cancel_button = self.proselect_common_operations.get_element(ProSelectUIObjectIds.SigningInCancelButton)
        if not cancel_button:
            logging.error("Failed to get Signing In Cancel Button")
            return False
        return self.proselect_common_operations.click(cancel_button)


    def enter_creds(self, login:bool, authAgent, password, username=None):
        """
        Method to enter the username/password on the Workflow sign in screen

        Inputs:
            login: Set as True to press "Sign In" button after entering credentials
            password: The password for the role
            username: The username for the role (optional because admin role has no username)
        """
        self.enter_credentials(login, password, username)
        
    def enter_credentials(self, login:bool, password:str, username:str=None):
        if username:
            self.enter_username(username)

        self.enter_password(password)

        if login:
            self.click_sign_in_button()
    
    def enter_creds_blank_field(self, login:bool, password, username=None):
        """
        Method to enter the username/password on the Workflow sign in screen

        Inputs:
            login: Set as True to press "Sign In" button after entering credentials
            password: The password for the role
            username: The username for the role (optional because admin role has no username)
        """

        # Set the default user and pasword button
        user_button = self.user_button_prefix
        password_button = self.password_button_prefix
        ok_button = self.ok_button_prefix
        authAgent = self.get_authentication_method_from_current_sign_in_page()

        # Declare the view matching the chosen auth agent
        if authAgent == AuthenticationMethod.Windows:
            view = self.windowsView
            user_button += "Windows"
            password_button += "Windows"
            ok_button += "Windows"
        elif authAgent == AuthenticationMethod.Ldap:
            view = self.ldapView
            user_button += "Ldap"
            password_button += "Ldap"
            ok_button += "Ldap"
        elif authAgent == AuthenticationMethod.Admin:
            view = self.localadminview
            password_button = self.local_admin_password_button
            ok_button = self.local_admin_ok_button
        elif authAgent == AuthenticationMethod.PrinterUser:
            view = self.deviceUserView
            password_button += "User"
            user_button += "User"
            ok_button += "User"
        else:
            raise NotImplementedError(f"{authAgent} is not yet implemented by this method.")
        
        assert self.reset_sign_in_page_scroll_bar_manually(authAgent),\
            logging.error("Failed to reset the sign-in page scroll bar")

        # Enter the username (if provided)
        #user auth method does not have a user name
        if authAgent != AuthenticationMethod.Admin:
            self.proselect_common_operations.goto_item(user_button, view)
            self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(username)

        # Enter the password
        self.proselect_common_operations.goto_item(password_button, view)
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(password)

        result = self.spice.query_item(ok_button)["enabled"] is False
        assert result

    def cleanup(self, role, result):
        logging.critical("!!!!! DEPRECATED METHOD !!!!!")
        logging.critical("Using \'verify_authentication_and_cleanup()\'")
        self.verify_authentication_and_cleanup(result)
    
    def verify_authentication_and_cleanup(self, expected_outcome) -> bool:
        """
        Method to verify we are on the correct screen after signing in
        and cleans up by navigating back to homescreen (and potentially signs out)

        Args:
            expected_outcome: The outcome we are expecting. Can be "success", "failed" or "blankCreds".
        
        Returns:
            Returns a bool where True is we are on the page we expected and False is we are not on the page we expected.
        """
        result = False
        if expected_outcome == "success" and self.spice.home.is_on_home_screen() and self.is_signed_in():
            result = True
        elif expected_outcome == "failed" and self.on_invalid_sign_in_screen():
            result = True
        elif expected_outcome == "blankCreds":
            # You can't enter blank credentials on ProSelect (OK sign-in button is greyed out)
            result = True
        self.universal_cleanup()
        return result

    def universal_cleanup(self):
        user = self.last_used_authentication_method
        # Set the view corresponding to the auth agent
        if user == AuthenticationMethod.Windows:
            view = self.windowsView
        elif user == AuthenticationMethod.Ldap:
            view = self.ldapView
        elif user == AuthenticationMethod.Admin:
            view = self.localadminview
        elif user == AuthenticationMethod.PrinterUser:
            view = self.deviceUserView
        else:
            raise NotImplementedError(f"{user} is not yet implemented by this method.")
        
        if self.spice.home.is_on_home_screen():
            if self.is_signed_in():
                assert self.select_universal_sign_out_from_home()
                self.spice.wait_for(ProSelectUIObjectIds.homeScreenView)
            return
        if self.on_invalid_sign_in_screen():
            assert self.click_invalid_sign_in_button()
            self.spice.wait_for(ProSelectUIObjectIds.homeScreenView)
            return
        else: # Blank Credentials screen
            self.proselect_common_operations.back_button_press(
                view, ProSelectUIObjectIds.homeScreenView)
        return

    def is_signed_in(self) -> bool:
        """
        UI should be on home screen before calling this method
        Method to check if a user is currently signed in

        Return:
            True: user is currently signed in
            False: user is NOT currently signed in

        Raises an exception if it cannot find sign in app
        """
        startTime = time.time()
        timeSpentWaiting = 0
        currentScreen = self.spice.wait_for("#HomeScreenView")
        appLocated = False
        currentAppText = self.proselect_common_operations.get_element("#CurrentAppText", timeout = self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        text = self.proselect_common_operations.get_element_property(currentAppText, 'text')
        if text == self.SIGN_OUT_OPERATION_STRING or text == self.SIGN_IN_OPERATION_STRING:
            logging.debug(f"Sign In app available. Text: {text}")
            return text == self.SIGN_OUT_OPERATION_STRING
        logging.debug(f"Sign In app not available. Scrolling to locate...")
        while (self.spice.query_item(ProSelectUIObjectIds.HomeSignInButton) == None and timeSpentWaiting < 10):
            currentScreen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(5)
        currentAppText = self.proselect_common_operations.get_element("#CurrentAppText", timeout = self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        text = self.proselect_common_operations.get_element_property(currentAppText, 'text')
        if text == self.SIGN_OUT_OPERATION_STRING or text == self.SIGN_IN_OPERATION_STRING:
            logging.debug(f"Scrolled to Sign In app available. Text: {text}")
            return text == self.SIGN_OUT_OPERATION_STRING
        while (self.spice.query_item(ProSelectUIObjectIds.HomeSignInButton) == None and timeSpentWaiting < 10):
            currentScreen.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
            time.sleep(5)
        currentAppText = self.proselect_common_operations.get_element("#CurrentAppText", timeout = self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        text = self.proselect_common_operations.get_element_property(currentAppText, 'text')
        if text == self.SIGN_OUT_OPERATION_STRING or text == self.SIGN_IN_OPERATION_STRING:
            logging.debug(f"Sign In app available. Text: {text}")
            return text == self.SIGN_OUT_OPERATION_STRING
        time.sleep(5)
        return text == self.SIGN_OUT_OPERATION_STRING

    def verify_auth(self, expected_result:str, expected_display_name:str = ""):
        """
        Method to verify if user has successfully logged in or not based on current screen

        Args:
            expected_result: the expected result or login attempt "success" or anything else
        """
        if expected_result == "cancel":
            self.proselect_common_operations.goto_item(self.cancel_button, self.signingInView)
            # Verify User is not logged in
            home_screen = self.spice.wait_for(ProSelectUIObjectIds.homeScreenView, 120)
            self.spice.wait_until(lambda: home_screen["activeFocus"] == True, 60)
            assert home_screen
            self.goto_sign_in_app(self.SIGN_IN_OPERATION_STRING, False)
            retval = "cancel"
        elif expected_result == "success":
            toast_message = self.spice.wait_for(ProSelectUIObjectIds.ToastMessageView, 10)
            assert toast_message
            if(expected_display_name != ""):
                welcomeText = self.spice.wait_for(ProSelectUIObjectIds.ToastMessageText)
                assert welcomeText["text"] == f"Welcome, {expected_display_name}"
            retval = "success"
            time.sleep(4)
        elif expected_result == "blankCreds":
            logging.info("blank creds checked in previous method only returning true")
            retval = "blankCreds"
        else:
            failed_auth = self.spice.wait_for(ProSelectUIObjectIds.invalidSignInView, 120)
            assert failed_auth
            retval = "failed"
            time.sleep(4)

        return bool(retval == expected_result)

    def check_ok_button(self, spice, cdm):
        """
        This is not a function of the Workflow UI so the functionality has changed and is only for proselect UI
        """
        logging.debug("\ntest_ui_win_auth_ok_enabled")
        domain = WindowsAuthTestHelper.initialize(cdm, 'jsdomain')
        userinfo = WindowsAuthTestHelper.get_user('keymaster')
        assert cdm.winauth.set_winauth_cfg(enabled="true", defaultDomain=domain), "Configure winauth failed"
        time.sleep(2)
        spice.signIn.select_universal_sign_in_from_home()
        spice.signIn.select_sign_in_method("windows", "admin")

        spice.signIn.enter_credentials(False, "")
        result = spice.query_item(spice.signIn.ok_button)["enabled"]
        assert result is False, "test_ui_win_auth_ok_enabled Failed!!!"

        spice.signIn.enter_credentials(False, userinfo['SamAccountName'])
        result = spice.query_item(spice.signIn.ok_button)["enabled"]
        assert result is False, "test_ui_win_auth_ok_enabled Failed!!!"

        spice.signIn.enter_credentials(False, userinfo['Password'], "")
        result = spice.query_item(spice.signIn.ok_button)["enabled"]
        assert result is False, "test_ui_win_auth_ok_enabled Failed!!!"

        spice.signIn.enter_credentials(False, userinfo['Password'], userinfo['SamAccountName'])
        result = spice.query_item(spice.signIn.ok_button)["enabled"]
        assert result, "test_ui_win_auth_ok_enabled Failed!!!"
        spice.signIn.verify_authentication_and_cleanup( "failed")

    def verify_welcome(self):
        """
        This is not a function of the Workflow UI so the functionality has changed and is only for proselect UI
        """
        userinfo = WindowsAuthTestHelper.get_user('keymaster')
        return self.verify_auth("success", userinfo['SamAccountName'])

    def welcome_mail(self):
        userinfo = WindowsAuthTestHelper.get_user('keymaster')
        return self.verify_auth("success", userinfo['Email'])

    def go_home_from_sign_in(self):
        """
        Method returns to the home screen from the sign in page.

        Returns:
            True if successfull, False if unsuccessful
        """
        # Perform a long press to exit the Sign In screen
        navigationApp = self.spice.query_item("#CurrentAppText")
        navigationApp.mouse_press(button=self.spice.MOUSE_BTN.MIDDLE)

        # If the UI is still not on the home screen, use the longpress menu
        try:
            home_app = self.spice.query_item(ProSelectUIObjectIds.homeScreenView)
            self.spice.wait_until(lambda: home_app["activeFocus"] == True)
            return True
        except:
            pass
        
        try:
            self.spice.goto_homescreen()
            return True
        except:
            return False


    def verifyPermissionEnforced(self, expected):
        """
        Method to verify permission granted/denied in the UI.
        Will navigate out of the access denied screen if it appears.

        Inputs:
            expected: True = access granted, False = access denied

        Returns:
            True if permission is enforced as expected
        """
        # Check if the "Access Denied" screen is visible
        try:
            self.spice.wait_for("#NoAccessView")
        except:
            # If the screen is not visible, access was granted
            return bool(expected == True)

        # Perform a long press to exit the "Access Denied" screen
        navigationApp = self.spice.query_item("#CurrentAppText")
        navigationApp.mouse_press(button=self.spice.MOUSE_BTN.MIDDLE)

        return bool(expected == False)


#######################################################################################
#   UI NAVIGATE TO PERMISSION
#######################################################################################

    def goto_permission(self, permission_id, is_locked: False):
        """
        Method navigates to the input permission from the home menu

        Inputs:
            spice: spice object
            permission_id: GUID of permission being tested
            is_locked: Boolean if permission is locked to check for lock icon
        """

        if permission_id == "fc1f5a75-aeb4-474a-b712-4ef20c2a18e0": # View job status
            # Check for lock icon if expected to be locked
            if is_locked:
                assert self.spice.job_ui.has_lock_icon()
            # Go to Job Log
            self.spice.homeMenuUI().goto_joblog(self.spice)

        elif permission_id == "b8a43731-3f25-4db5-ad6c-523866af152d": # Print from USB
            # Check for lock icon if expected to be locked
            if is_locked:
                assert self.spice.print_from_usb.has_lock_icon()
            # Go to print from usb in menu
            self.spice.homeMenuUI().goto_menu_print_from_usb(self.spice)

        elif permission_id == "66799d55-60e4-43fc-8b28-a8413c810a8b": # Network settings
            # Check for lock icon if expected to be locked
            if is_locked:
                assert self.spice.network.has_lock_icon()
            # Go to Network settings in menu
            self.spice.homeMenuUI().goto_menu_settings_network(self.spice)

        elif permission_id == "2aea816f-87bc-4113-9a6c-8c140537c080": # Menu Supplies
            # Check for lock icon if expected to be locked
            if is_locked:
                assert self.spice.homeMenuUI().has_lock_icon(self.spice)
            # Go to Menu App, then supplies
            self.spice.homeMenuUI().goto_menu_supplies(self.spice)

        elif permission_id == "fe5fe3b1-82d0-446a-a9f5-271ce01e8756": # job storage
            # Check for lock icon if expected to be locked
            if is_locked:
                assert self.spice.storejob.has_lock_icon()
            # Go to job storage
            self.spice.homeMenuUI().goto_menu_job_storage(self.spice)

        elif permission_id == "example-permission-id": # Permission name
            # Add UI navigation for new permission here and check for lock icon
            pass
        else:
            assert False, f"Could not navigate to permission! ({permission_id} not found)"

    def goto_home_from_permission(self, permission_id, accessGranted):
        """
        Method navigates to the home menu from the input permission

        Inputs:
            permission_id: GUID of permission being tested
        """

        if permission_id == "fc1f5a75-aeb4-474a-b712-4ef20c2a18e0": # View job status
            # How to navigate back from the permission
            self.spice.goto_homescreen()

        elif permission_id == "b8a43731-3f25-4db5-ad6c-523866af152d": # Print from USB
             # How to navigate back from the permission
            self.spice.goto_homescreen()

        elif permission_id == "66799d55-60e4-43fc-8b28-a8413c810a8b": # Network settings
           # How to navigate back from the permission
            self.spice.goto_homescreen()

        elif permission_id == "2aea816f-87bc-4113-9a6c-8c140537c080": # Menu Supplies
            # How to navigate back from the permission
            self.spice.goto_homescreen()

        elif permission_id == "fe5fe3b1-82d0-446a-a9f5-271ce01e8756": # job storage
            # How to navigate back from the permission
            self.spice.goto_homescreen()

        elif permission_id == "example-permission-id": # Permission name
            # Add UI navigation for new permission here
            pass
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
            self.spice.wait_for(self.menu_item_signinid)
            logging.info("sign in app supported on UI")
            return True

        except Exception as err:
            logging.info("sign in app does not supported on UI")
            return False

    def set_service_pin(self,udw):
        keyboard =  self.spice.wait_for("#spiceKeyboardView")
        assert keyboard
        defaultPin = udw.mainApp.AdminStandard.getDefaultDevicePassword()
        assert len(defaultPin) > 0
        keyboard.__setitem__('currentText', defaultPin)

        while (self.spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
            keyboard.mouse_wheel(0,0)
            time.sleep(0.5)
        keyboard.mouse_click()

        assert self.spice.wait_for("#MenuListLayout")
        logging.info("At Service Screen")
        time.sleep(1)

    def select_universal_sign_in_from_home(self) -> bool:
        self.goto_universal_sign_in(self.SIGN_IN_OPERATION_STRING)
        return self.is_on_sign_in_page()

    def select_universal_sign_out_from_home(self) -> bool:
        self.goto_universal_sign_in(self.SIGN_OUT_OPERATION_STRING)
        return not self.is_signed_in()

    def goto_universal_sign_in(self, text:str):
        """
        This method will find any way to sign in. It will start with trying to
        sign in at the home screen, then status center and finally menu.

        *Some devices can only sign in a certain way so it's useful to have a method
        that just finds anyway to sign in instead of writing specific tests for specific
        ways to sign in

        text: Either "Sign In" or "Sign Out"

        Return:
            Nothing
            Raises and exception if it cannot sign in through home screen or status center.
        """
        
        self.goto_sign_in_app(text)

    
    def get_sign_in_status(self) -> str:
        """
        This method will check if a user (any user) is signed in or out of the device.

        Return:
            Returns a string containing "Sign In" or "Sign Out" or throws exception if neither
        """
        
        # Try to get status center sign in button text
        homeApp = self.spice.query_item(ProSelectUIObjectIds.homeScreenView)
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)

        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll to the next option first
        homeApp.mouse_wheel(180, 180)
        # scroll till you reach the Sign In option
        while (self.spice.query_item("#CurrentAppText")["text"] != self.SIGN_IN_OPERATION_STRING and
         self.spice.query_item("#CurrentAppText")["text"] != self.SIGN_OUT_OPERATION_STRING and 
         timeSpentWaiting < self.MAX_SCROLL_TIMEOUT):
            homeApp.mouse_wheel(0,0)
            timeSpentWaiting = time.time() - startTime

        homeApp = self.spice.query_item(ProSelectUIObjectIds.homeScreenView)
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)
        homeApp.mouse_wheel(180,180)

        return self.spice.query_item("#CurrentAppText")["text"]

    def verify_constraint_message_with_no_credentials(self):
        sign_in_ok_button = self.spice.wait_for("#signInOkButtonWindows #SpiceButton")
        # Make sure OK button is greyed out
        assert sign_in_ok_button["opacity"] != 1

    def is_on_sign_in_page(self) -> bool:
        sign_in_view = self.proselect_common_operations.get_element(ProSelectUIObjectIds.SignInView)
        if not sign_in_view: return False

        return self.proselect_common_operations.get_element_property(sign_in_view, "visible")
    
    def click_admin_password_required_ok_button(self) -> bool:
        # sign_in_view = self.proselect_common_operations.get_element(ProSelectUIObjectIds.SignInView)
        # if not sign_in_view: return False

        admin_password_required_ok_button = self.proselect_common_operations.get_element(ProSelectUIObjectIds.AdminPasswordRequiredOkButton)
        if not admin_password_required_ok_button:
            logging.error(f"Admin Ok Button: {ProSelectUIObjectIds.AdminPasswordRequiredOkButton}")
            return False

        return self.proselect_common_operations.click(admin_password_required_ok_button)

    def get_sign_in_page_locator_by_authentication_method(self, authentication_method: AuthenticationMethod) -> str:
        """
        This method will return the sign in page locator based on the authentication method.
        """
        if authentication_method == AuthenticationMethod.PrinterUser:
            return ProSelectUIObjectIds.PrinterUserSignInOkButton
        elif authentication_method == AuthenticationMethod.Admin:
            return ProSelectUIObjectIds.AdminSignInOkButton
        elif authentication_method == AuthenticationMethod.Windows:
            return ProSelectUIObjectIds.WindowsSignInOkButton
        elif authentication_method == AuthenticationMethod.Ldap:
            return ProSelectUIObjectIds.LdapSignInOkButton
        else:
            raise ValueError(f"Unsupported authentication method: {authentication_method}")
        
    def is_current_sign_in_page_for_authentication_method(self, authentication_method: AuthenticationMethod, waitForExists:bool=True) -> bool:
        """
        This method will check if the current sign in page is for the specified authentication method.
        """
        timeout = self.proselect_common_operations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        signInPageLocator = self.get_sign_in_page_locator_by_authentication_method(authentication_method)
        object = self.proselect_common_operations.get_element(signInPageLocator, timeout)
        outcome = False
        if object:
            outcome = self.proselect_common_operations.get_element_property(object, 'visible')
        if outcome:
            logging.info(f"Current Sign In page is for {authentication_method}.")
            self.last_used_authentication_method = authentication_method
        else:
            logging.info(f"Current Sign In page is NOT for {authentication_method}.")
        return outcome

    def is_on_administrator_sign_in_page(self, waitForExists:bool=True) -> bool:
        return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.Admin, waitForExists)

    def is_on_printer_user_sign_in_page(self, waitForExists:bool=True) -> bool:
        return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.PrinterUser, waitForExists)

    def is_on_windows_sign_in_page(self, waitForExists:bool=True) -> bool:
        return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.Windows, waitForExists)

    def is_on_ldap_sign_in_page(self, waitForExists:bool=True) -> bool:
       return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.Ldap, waitForExists)

    def is_on_last_used_sign_in_page(self, waitForExists:bool=True) -> bool:
        """
        This method will check if the last used sign in page is visible.
        """
        outcome = self.is_current_sign_in_page_for_authentication_method(self.last_used_authentication_method, waitForExists)
        if outcome: logging.info(f"Is on the last used Sign In Page: {self.last_used_authentication_method.name}")
        return outcome

    def get_authentication_method_from_current_sign_in_page(self)-> AuthenticationMethod:
        outcome = None
        if self.is_on_last_used_sign_in_page(False):
            outcome = self.last_used_authentication_method
        elif self.last_used_authentication_method != AuthenticationMethod.PrinterUser and self.is_on_printer_user_sign_in_page(False):
            outcome = AuthenticationMethod.PrinterUser
        elif self.last_used_authentication_method != AuthenticationMethod.Admin and self.is_on_administrator_sign_in_page(False):
            outcome = AuthenticationMethod.Admin
        elif self.last_used_authentication_method != AuthenticationMethod.Windows and self.is_on_windows_sign_in_page(False):
            outcome = AuthenticationMethod.Windows
        elif self.last_used_authentication_method != AuthenticationMethod.Ldap and self.is_on_ldap_sign_in_page(False):
            outcome = AuthenticationMethod.Ldap        
        else: assert False, logging.error("Unable to determine the current Sign In method")
        logging.info(f"Current Sign In method is {outcome.name}")
        return outcome

    def select_sign_in_method_by_enum(self, authenticationAgent:AuthenticationMethod, expectedDefaultAgent:AuthenticationMethod=None) -> bool:
        """
        Method to select the authentication method from the sign in combo box by AuthenticationMetod inputs.
        Optionally can validate the Default AuthAgent is set to the expected value.

        Inputs:
            authenticationAgent: The authentication method to select (Examples: 'AuthenticationMethod.Windows' or 'AuthenticationMethod.Admin)
            expectedDefaultAgent: The expected default authentication method (Examples: 'AuthenticationMethod.Windows' or 'AuthenticationMethod.Admin')

        Returns:
            bool: True if the expectedDefaultAgent was correct, or if the authenticationAgent was selected successfully, False otherwise.
        """
        defaultAgent = None
        agentToSelect = self.__convert_authentication_agent_enumeration_to_agent_string(authenticationAgent)
        if expectedDefaultAgent: defaultAgent = self.__convert_authentication_agent_enumeration_to_agent_string(expectedDefaultAgent)
        
        logging.info(f"Selecting authentication agent by enumeration '{authenticationAgent}' from drop down")
        self.select_sign_in_method(agentToSelect, defaultAgent)
        logging.info(f"Authentication Agent selected by enumeration '{authenticationAgent}' from drop down")
        return self.get_authentication_method_from_current_sign_in_page() == authenticationAgent

    def verify_welcome_user_toast_message(self, username:str=None, timeout:float = TIMEOUT_SIGN_IN_SUCCESS) -> bool:
        logging.info("Verifying Welcome User toast message..")

        logging.info("Wait for toast message to populate...")
        element = self.proselect_common_operations.get_element(ProSelectUIObjectIds.ToastMessageText, timeout)
        if not element:
            logging.error("Toast message not found")
            return False
        logging.info("Toast message found")
        outcome = True
        if username:
            text = self.proselect_common_operations.get_element_property(element, 'text')
            while text == "" and timeout > 0:
                timeout -= 1
                time.sleep(1)
                text = self.proselect_common_operations.get_element_property(element, 'text')
            if not text:
                logging.error("Toast message text not found")
                return False
            outcome = text == f"Welcome, {username}"
        logging.info("Toast message text found. Waiting for toast to disappear...")
        while element and timeout > 0:
            logging.debug("Toast is still visible...")
            timeout -= 1
            time.sleep(1)
            element = self.proselect_common_operations.get_element(ProSelectUIObjectIds.ToastMessageText, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        
        if not outcome:
            logging.error(f"Toast message text '{text}' does not match expected 'Welcome, {username}'")
        return outcome

    def on_invalid_sign_in_screen(self, waitForExists:bool=True) -> bool:
        timeout = self.proselect_common_operations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        invalid_sign_in_view = self.proselect_common_operations.get_element(ProSelectUIObjectIds.invalidSignInView, timeout=timeout)
        if not invalid_sign_in_view:
            logging.error(f"Failed to get Invalid Sign-In screen within {timeout} seconds")
            return False

        try:
            self.spice.wait_until(lambda: invalid_sign_in_view.is_visible() == True, timeout)
        except Exception as exception:
            logging.error(f"Invalid Sign-In View not visible. Caught exception: {exception}")
            return False
        
        return True
    
    def click_invalid_sign_in_button(self) -> bool:
        logging.debug("Clicking Invalid Sign In button...")
        # This is the 'Sign In' buttton that is on the 'Invalid Sign In' screen
        if not self.scroll_sign_in_page_down_manually(self.last_used_authentication_method, 1):
            return False
        failedOkButton = self.proselect_common_operations.get_element(ProSelectUIObjectIds.invalidSignInOkButton)
        if not failedOkButton:
            logging.error("Failed to get Invalid Sign In Ok button")
            return False
        return self.proselect_common_operations.click(failedOkButton)

    def click_cancel_button(self) -> bool:
        if not self.scroll_sign_in_page_down_to(self.last_used_authentication_method, ProSelectUIObjectIds.SignInBackButton):
            return False
        cancelButton = self.proselect_common_operations.get_element(ProSelectUIObjectIds.SignInBackButton, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not cancelButton:
            logging.error("Failed to get Sign In Cancel button")
            return False
        return self.proselect_common_operations.click(cancelButton)

    def verify_sign_in_success(self, expectedUserName):
        logging.info("Verifying Sign In was successful...")
        start_time = time.time()
        assert self.verify_welcome_user_toast_message(expectedUserName),\
            logging.error("Failed to find Welcome toast message")

        assert self.is_signed_in(),\
            logging.error("Failed to Sign In")

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Verify Sign In completed successfully and took {elapsed_time} seconds.")

    def verify_sign_in_success_and_sign_out(self, expectedUserName):
        logging.info("Verifying Sign In was successful and attempting to Sign Out...")
        start_time = time.time()
        self.verify_sign_in_success(expectedUserName)

        logging.info("Click Sign Out button")
        assert self.select_universal_sign_out_from_home()

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Verify Sign In and Sign Out completed successfully and took {elapsed_time} seconds.")
    
    def verify_sign_in_invalid_and_return_home(self):
        logging.info("Verifying Sign In was invalid and attempting to return to Home...")
        start_time = time.time()
        assert self.on_invalid_sign_in_screen(),\
            logging.error("Expected to be on Invalid Sign In page, but we are not")
        assert self.click_invalid_sign_in_button(),\
            logging.error("Failed to click the invalid sign in button")
        time.sleep(1)
        assert self.is_on_last_used_sign_in_page(),\
            logging.error("Not on Sign In page when we should be")
        assert self.click_cancel_button(),\
            logging.error("Failed to click Sign In Cancel button")
        time.sleep(1)
        if self.spice.status_center and self.spice.status_center.is_status_center_visible():
                self.spice.status_center.collapse()
                time.sleep(1)
                assert not self.spice.status_center.is_status_center_visible(),\
                    logging.error("Failed to collapse status center.")
        assert self.spice.home.is_on_home_screen(),\
            logging.error("Failed to return to Home Screen.")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Verify Sign In was Invalid and return to Home completed successfully and took {elapsed_time} seconds.")
    
    def wait_for_sign_in_page(self):
        """
            Method to wait for the sign-in page to appear. Used in tests where the sign-in page doesn't
            necessarily immediately popup when accessed.
        """
        self.spice.wait_for(ProSelectUIObjectIds.SignInView, timeout=5)
    
    def has_sign_in(self) -> bool:
        """
            Checks to see if the device has a way to sign-in.
        """
        try:
            self.is_signed_in()
        except Exception as exception:
            logging.warning("Device has no way to sign-in/sign-out")
            logging.warning(f"Exception (ProSelect):\n{exception}")
            return False
        return True