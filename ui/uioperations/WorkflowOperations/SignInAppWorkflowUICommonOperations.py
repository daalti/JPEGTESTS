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
import datetime
from enum import Enum
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.BaseOperations.ISignInAppUIOperations import ISignInAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.security.SecurityTypes import AuthenticationMethod
from dunetuf.qmltest.QmlTestServer import QmlTestServer

class SignInAppWorkflowUIOperations(ISignInAppUIOperations):
    """
    SignInAppWorkflowUIOperations module for Workflow Operations on SignInApp
    """

    ##!!!DO NOT_Increase this timeout value!!!##
    ##If your needs are not met by this timeout value - use or create a wait_for method instead of an 'is_on_<item>'.##
    #Methods prefixed with 'is_on_<item>' are existence methods and should be expected to an immediate return of True or False.
    #They cannot use 'spice.wait_for' default timeout function as it causes performance issues when checking for 'is_on_<item>' == False.
    #This low wait time rather than using a direct element query is to retry a missed element check due to netowork latency and allow a single retry at minimuim.
    TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY = 1
    TIMEOUT_SIGN_IN_SUCCESS = 90

    SIGN_IN_OPERATION_STRING = 'Sign In'
    SIGN_OUT_OPERATION_STRING = 'Sign Out'

    def __init__(self, spice):
        self.maxtimeout = 100
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.last_used_authentication_method:AuthenticationMethod = AuthenticationMethod.PrinterUser
        self.last_used_windows_domain_view_locator:str = ''
    
    def __is_home_screen_signed_in(self) -> bool:
        sign_in_home_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_button, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not sign_in_home_button:
            return False
        return self.workflow_common_operations.get_element_property(sign_in_home_button, "text") == self.SIGN_OUT_OPERATION_STRING

    def __is_status_center_signed_in(self) -> bool:
        return self.spice.status_center.is_signed_in()
    
    def __has_status_center_sign_in(self) -> bool:
        return self.spice.status_center.get_status_center()

    def __has_home_screen_sign_in(self) -> bool:
        return self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_button, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)

    def __goto_home_screen_sign_in(self, action:str, click_sign_in_button:bool=True) -> bool:
        sign_in_home_button_text = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_label, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        current_sign_in_status = self.workflow_common_operations.get_element_property(sign_in_home_button_text, "text")
        if current_sign_in_status != action:
            logging.error(f"Home screen sign-in is \"{current_sign_in_status}\".\nExpected: \"{action}\"")
            return False
        # Resetting the scroll bar on the home screen
        self.workflow_common_operations.scroll_to_position_horizontal(0.0)
        if not click_sign_in_button: return True
        sign_in_home_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_button, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        sign_in_home_button.mouse_click()
        return True

    def __goto_status_center_sign_in(self, action:str, click_sign_in_button:bool=True) -> bool:
        try:
            self.spice.status_center.goto_sign_in_app(action, click_sign_in_button)
        except:
            logging.error("Failed to navigate to status center sign-in app button")
            return False
        return True
    
    def get_password_input_field_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the password input field locator string depending on the authentication agent

        Args:
            No arguments

        Returns:
            str: The password input field locator string

        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserPasswordInputField
        elif authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminPasswordInputField
        elif authentication_agent == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsPasswordInputField
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapPasswordInputField
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodePinInputField
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartCardPinInputField
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""

    def get_password_input_field_text_box_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the password input field text box locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The password input field text box locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserPasswordInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminPasswordInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsPasswordInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapPasswordInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodePinInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardPinInputFieldTextInputBox
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
        
    def get_username_input_field_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the username input field locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The username input field locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserUsernameInputField
        elif authentication_agent == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsUsernameInputField
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapUsernameInputField
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
    
    def get_username_input_field_text_box_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the username input field text box locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The username input field text box locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserUsernameInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsUsernameInputFieldTextInputBox
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapUsernameInputFieldInputTextBox
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
        
    def get_password_reveal_icon_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the password reveal icon locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The password reveal icon locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserPasswordInputRevealIconButton
        elif authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminPasswordInputRevealIconButton
        elif authentication_agent == AuthenticationMethod.Windows:
            return self.get_current_windows_login_view_locator() + ' ' + SignInAppWorkflowObjectIds.windowsPasswordInputRevealIconButton
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapPasswordInputRevealIconButton
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodePinInputRevealIconButton
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardPinInputRevealIconButton
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
    
    def get_cancel_button_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the cancel button locator string depending on the authentication agent

        Args:
            authentication_agent: AuthenticationMethod enum value to determine the sign-in method

        Returns:
            str: The cancel button locator string
        """
        if authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminCancelButtonControl
        elif authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserCancelButtonControl
        elif authentication_agent == AuthenticationMethod.Windows:
            return self.get_current_windows_login_view_locator() + ' ' + SignInAppWorkflowObjectIds.windowsCancelButtonControl
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapCancelButtonControl
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeCancelButtonControl
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardCancelButtonControl
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
    
    def get_sign_in_button_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the sign-in button locator string depending on the authentication agent

        Args:
            authentication_agent: AuthenticationMethod enum value to determine the sign-in method
        
        Returns:
            str: The sign-in button locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminSignInButtonControl
        elif authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserSignInButtonControl
        elif authentication_agent == AuthenticationMethod.Windows:
            return self.get_current_windows_login_view_locator() + ' ' + SignInAppWorkflowObjectIds.windowsSignInButtonControl
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapSignInButtonControl
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeSignInButtonControl
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardSignInButtonControl
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""
    
    def get_current_sign_in_view_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
        Gets the sign-in view locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The sign-in view locator string
        
        Raises:
            None
        """
        if authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminLoginViewLayout
        elif authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserLoginViewLayout
        elif authentication_agent == AuthenticationMethod.Windows:
            #Windows Domain Multi-demnsional resolution here:
            return SignInAppWorkflowObjectIds.windowsLoginViewLayout_MultiDimensional.format(self.get_current_windows_login_view_locator())
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapLoginView
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeLoginView
        elif authentication_agent == AuthenticationMethod.Smartcard:
            #SmartCard Domain Multi-demnsional resolution here:
            return SignInAppWorkflowObjectIds.smartcardLoginView
        else:
            logging.error(f"Not implemented for authentication agent: '{authentication_agent}'")
            return ""

    def get_current_windows_login_view_locator(self) -> str:
        """
        Gets the current Windows login view locator string depending on the domain view type.
        Note: the Windows Auth Agent can have multiple views depending on the single or multi-domain option.

        Args:
            No arguments

        Returns:
            str: The current Windows login view locator string

        """
        assert self.is_on_sign_in_page(), "get_current_windows_login_view_locator() called when not on sign in page"
        windows_dimensional_view_locators = [
            SignInAppWorkflowObjectIds.windowsLoginView_base,
            SignInAppWorkflowObjectIds.windowsSingleDomainView,
            SignInAppWorkflowObjectIds.windowsMultipleDomainView]

        #We will check for the last used view locator first, if it exists and promote it.
        if self.last_used_windows_domain_view_locator:
            logging.debug(f'Promoting last used Windows view locator first check: {self.last_used_windows_domain_view_locator}')
            windows_dimensional_view_locators.remove(self.last_used_windows_domain_view_locator)
            windows_dimensional_view_locators.insert(0, self.last_used_windows_domain_view_locator)

        for locator in windows_dimensional_view_locators:
            view_layer = self.workflow_common_operations.get_element(locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
            if view_layer:
                logging.debug(f'Found Windows view locator: {locator}')
                self.last_used_windows_domain_view_locator = locator
                return locator
        assert False, f"Unable to locate any of the Windows Multi-dimensional view layers: {windows_dimensional_view_locators}"  

    def get_password_input_display_text(self) -> str:
        """
        Gets the password input display text locator string depending on the authentication agent

        Args:
            No arguments
        
        Returns:
            str: The password input display text locator string

        Raises:
            None
        """
        authentication_agent = self.get_authentication_method_from_current_sign_in_page()
        password_input_field_locator = self.get_password_input_field_text_box_locator(authentication_agent)
        password_field = self.workflow_common_operations.get_element(password_input_field_locator)
        return self.workflow_common_operations.get_element_property(password_field, "displayText")

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
        authAgent = authenticationAgent
        if isinstance(authenticationAgent, AuthenticationMethod):
            authAgent = self.__convert_authentication_agent_enumeration_to_agent_string(authenticationAgent)
        if expectedDefaultAgent:
            defaultAgent = expectedDefaultAgent
            if isinstance(authenticationAgent, AuthenticationMethod):
                defaultAgent = self.__convert_authentication_agent_enumeration_to_agent_string(expectedDefaultAgent)
        
        logging.info(f"Selecting authentication agent by enumeration '{authenticationAgent}' from drop down")
        self.select_sign_in_method(authAgent, defaultAgent)
        logging.info(f"Authentication Agent selected by enumeration '{authenticationAgent}' from drop down")
        return self.get_authentication_method_from_current_sign_in_page() == authenticationAgent

    def select_sign_in_method(self, signInMethod, defaultAuthAgent):
        """
        Method navigates to the sign in app and selects the authenticaion method

        Inputs:
            signInMethod: Method to be selected (OPTIONS: "user", "customUser", "admin", "windows", "ldap")
            defaultAuthAgent: Default auth agent expected in the sign in combo box
        """
        logging.info(f"Selecting authentication agent by string '{signInMethod}' from drop down")
        signInMethod = "User" if (signInMethod == "customUser") else signInMethod
        signInMethod = self.__convert_authentication_agent_string_to_agent_enumeration(signInMethod)
        if defaultAuthAgent:
            defaultAuthAgent = self.__convert_authentication_agent_string_to_agent_enumeration(defaultAuthAgent)
            logging.info(f"Default authentication agent is '{defaultAuthAgent}'")
            currentSignInPage = self.get_authentication_method_from_current_sign_in_page()
            logging.info(f"Current sign in page authentication agent is '{currentSignInPage}'")    
            assert defaultAuthAgent == currentSignInPage,\
                logging.error(f"Default auth agent '{defaultAuthAgent}' does not match current sign in page '{currentSignInPage}'")

        # Choose the prefix based on the defaultAuthAgent ("#windows", "#ldap", etc.)
        if not defaultAuthAgent:
            defaultAuthAgent = self.get_authentication_method_from_current_sign_in_page()
            
        if defaultAuthAgent == AuthenticationMethod.Windows:
            prefix = SignInAppWorkflowObjectIds.prefix_windows
        elif defaultAuthAgent == AuthenticationMethod.Ldap:
            prefix = SignInAppWorkflowObjectIds.prefix_ldap
        elif defaultAuthAgent == AuthenticationMethod.Admin:
            prefix = SignInAppWorkflowObjectIds.prefix_admin
        elif defaultAuthAgent == AuthenticationMethod.PrinterUser:
            prefix = SignInAppWorkflowObjectIds.prefix_user
        elif defaultAuthAgent == AuthenticationMethod.IDCode:
            prefix = SignInAppWorkflowObjectIds.prefix_identification_code
        elif defaultAuthAgent == AuthenticationMethod.Smartcard:
            prefix = SignInAppWorkflowObjectIds.prefix_smartcard
        else:
            raise NotImplementedError(f"{defaultAuthAgent} is not yet implemented by this method.")

        if signInMethod == AuthenticationMethod.Windows:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_windowsSelect
        elif signInMethod == AuthenticationMethod.Ldap:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_ldapSelect
        elif signInMethod == AuthenticationMethod.Admin:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_adminSelect
        elif signInMethod == AuthenticationMethod.PrinterUser:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_userSelect
        elif signInMethod == AuthenticationMethod.IDCode:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_identificationCodeSelect
        elif signInMethod == AuthenticationMethod.Smartcard:
            comboBoxItem = prefix + SignInAppWorkflowObjectIds.suffix_smartcardSelect
        else:
            raise NotImplementedError(f"{signInMethod} is not yet implemented by this method.")

        # Combine the prefix and suffix to create the combo box name. There is a typo in the dropdown ID for admin, use this as a workaround.
        comboBoxName = "#adminSigninInComboBox" if defaultAuthAgent == AuthenticationMethod.Admin else prefix + SignInAppWorkflowObjectIds.suffix_signindropdown
        comboBoxView = comboBoxName + "popupList"

        # Select the combo box and the desired option
        currentApp = self.spice.wait_for(comboBoxName)
        currentApp.mouse_click()
        time.sleep(3)

        self.workflow_common_operations.goto_item(comboBoxItem,comboBoxView, scrollbar_objectname = SignInAppWorkflowObjectIds.comboBoxScrollBar)
        time.sleep(5) # Safety sleep(TM)
        logging.info(f"Authentication Agent selected by string '{signInMethod}' from drop down")

    def enter_creds(self, login, authAgent, password, username=None):
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'enter_credentials()\' method")
        self.enter_credentials(login, password, username=username)

    def enter_credentials(self, login:bool, password, username=None):
        """
        Method to enter the username/password on the Workflow sign in screen

        Inputs:
            login: Set as True to press "Sign In" button after entering credentials
            password: The password for the role
            username: The username for the role (optional because admin role has no username)
        """
        # Enter username
        if username:
            self.enter_username(username)

        # Enter password
        self.enter_password(password)

        # Click the "Sign In" button
        if login:
            self.click_sign_in_button()
    
    def enter_username(self, username:str, ) -> bool:
        authentication_agent  = self.get_authentication_method_from_current_sign_in_page()
        logging.debug(f"Entering username for {authentication_agent} : {username}...")
        username_field_locator = self.get_username_input_field_text_box_locator(authentication_agent)
        username_field = self.workflow_common_operations.get_element(username_field_locator)
        if not username_field:
            logging.error(f"Failed to get username text field: '{username_field_locator}'")
            return False
        if not self.workflow_common_operations.set_element_property(username_field, "text", username):
            logging.error(f"Failed to enter username '{username}' into username field '{username_field_locator}'")
            return False
        return True

    def enter_password(self, password:str) -> bool:
        authentication_agent = self.get_authentication_method_from_current_sign_in_page()
        logging.debug(f"Entering password for {authentication_agent}: {password}...")
        password_field_locator = self.get_password_input_field_text_box_locator(authentication_agent)
        password_field = self.workflow_common_operations.get_element(password_field_locator)
        if not password_field:
            logging.error(f"Failed to get password text field: '{password_field_locator}'")
            return False
        if not self.workflow_common_operations.set_element_property(password_field, "text", password):
            logging.error(f"Failed to enter password '{password}' into password field '{password_field_locator}'")
            return False
        return True

    def enter_creds_blank_field(self, login:bool, password, username=None):
        """
        Method to enter the username/password on the Workflow sign in screen with one blank field

        Inputs:
            login: Set as True to press "Sign In" button after entering credentials
            password: The password for the role
            username: The username for the role (optional because admin role has no username)
        """
        authAgent = self.get_authentication_method_from_current_sign_in_page()

        if authAgent == AuthenticationMethod.Windows:
            prefix = SignInAppWorkflowObjectIds.prefix_windows
        elif authAgent == AuthenticationMethod.Ldap:
            prefix = SignInAppWorkflowObjectIds.prefix_ldap
        elif authAgent == AuthenticationMethod.Admin:
            prefix = SignInAppWorkflowObjectIds.prefix_admin
        elif authAgent == AuthenticationMethod.PrinterUser:
            prefix = SignInAppWorkflowObjectIds.prefix_user
        elif authAgent == AuthenticationMethod.IDCode:
            prefix = SignInAppWorkflowObjectIds.prefix_identification_code
        elif authAgent == AuthenticationMethod.Smartcard:
            prefix = SignInAppWorkflowObjectIds.prefix_smartcard
        else:
            raise NotImplementedError(f"{authAgent} is not yet implemented by this method.")

        # Enter username
        if username == "":
            currentApp = self.spice.wait_for(prefix + SignInAppWorkflowObjectIds.suffix_usernameinputfield)
        elif username:
            currentApp = self.spice.wait_for(prefix + SignInAppWorkflowObjectIds.suffix_usernameinputfield)
            currentApp.__setitem__('displayText', username)

        # Enter password
        if username == "":
            currentApp = self.spice.wait_for(prefix + SignInAppWorkflowObjectIds.suffix_passwordinputfield)
        elif username:
            currentApp = self.spice.wait_for(prefix + SignInAppWorkflowObjectIds.suffix_passwordinputfield)
            currentApp.__setitem__('displayText', password)

        # Click the "Sign In" button
        if login:
            currentApp = self.spice.wait_for(prefix + SignInAppWorkflowObjectIds.suffix_signinbutton)
            currentApp.mouse_click()

            # Sleep while the welcome message is displayed
            time.sleep(5)

    def cleanup(self, auth_agent, result):
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'verify_authentication_and_cleanup()\'")
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
        if expected_outcome == "success":
            if not self.spice.home.is_on_home_screen():
                logging.error("Verify Authentication Success is not on home screen")
            elif not self.is_signed_in():
                logging.error("Verify Authentication Success is not signed in")
            else:
                result = True
        elif expected_outcome == "failed" and self.spice.signIn.on_invalid_sign_in_screen(False):
            result = True
        elif expected_outcome == "blankCreds" and self.spice.signIn.on_blank_credentials_screen(False):
            result = True
        self.universal_cleanup()
        return result

    def universal_cleanup(self):
        """
        Method to navigate back to the home screen from a sign-in page.

        Args:
            user: The auth agent to sign out of (OPTIONS: "user", "customUser", "admin", "windows", "ldap")
            result: Cleanup after a "success" or "failed" login attempt
        """
        logging.info("UI Sign-In Universal Cleanup...")
        start_time = time.time()
        if not self.spice.home.is_on_home_screen():
            logging.info("UI is not left on Home Screen follwoing test. Attempting to navigate to Home Screen...")
            #Left on Invalid Page - Climb out of sign in
            if self.spice.signIn.on_invalid_sign_in_screen(False):
                logging.info("UI was on the Invalid Sign In form. Returning to Sign In form...")
                assert self.spice.signIn.click_invalid_sign_in_button(),\
                    logging.error("Failed to click the invalid sign in button")
                time.sleep(1)
            #Left on Blank Password form
            if self.spice.signIn.on_blank_credentials_screen(False):
                logging.info("UI was on the Blank Password Sign In form. Returning to Sign In form...")
                assert self.spice.signIn.click_blank_credentials_ok_button(),\
                    logging.error("Failed to click the invalid sign in button")
                time.sleep(1)
            #Left on User restricted prompt:
            if self.verifyPermissionEnforced(False):
                logging.info("UI was on the User Restricted Sign In form. Cleared message to return to home.")
                time.sleep(1)
            #Left on Sign In form
            if self.spice.signIn.on_sign_in_screen(False):
                logging.info("UI was on the Sign In form. Clicking Cancel...")
                assert self.spice.signIn.click_cancel_button(),\
                        logging.error("Failed to click LDAP Cancel button")
                time.sleep(1)
            if self.spice.home.has_persistent_header():
                logging.info("UI has Persistent Header. Verifying not left on User Sign Out Confirmation popup......")
                #Left on Persistent Header User Info Page
                if self.spice.signIn.on_user_info_page(False):
                    logging.info("UI was on the Persistent Header User Info Page. Signing Out...")
                    assert self.spice.signIn.click_sign_out_button()
                    time.sleep(1)
            elif self.spice.status_center.is_status_center_visible():
                #Left on with Status Center expanded
                logging.info("UI was left with the Status Center with expanded. Collapsing...")
                self.spice.status_center.collapse()
                time.sleep(1)
                assert not self.spice.status_center.is_status_center_visible(),\
                    logging.error("Failed to collapse status center.")
            logging.info("UI Sign In Errors States Cleared. Verifying UI is at Home and Signed Out.")
            assert self.spice.home.is_on_home_screen(),\
                logging.error("This test did not return UI to Home Screen as required.")

        #Verify we are Signed Out
        logging.info("UI is at Home Screen.")
        if self.spice.signIn.is_signed_in():
            logging.info("UI is at Home Screen, but user still signed in. Signing Out...")
            assert self.spice.signIn.select_universal_sign_out_from_home(),\
                logging.error("Failed to sign out user from Home Screen.")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"UI Sign In Cleanup completed in {elapsed_time} seconds.")

    def is_signed_in(self) -> bool:
        '''
        Return true if it's signed in or false if it's signed out.
        Handle cases where the sign-in app is not present.
        '''
        homeSignIn = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.menu_item_signinid, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if homeSignIn:
            logging.debug("Sign In app found on Home Screen")
            signInStateText = self.spice.query_item("#7db992ba-557a-461c-b941-6023aa8cfa34 SpiceText")["text"]
            if signInStateText == self.SIGN_OUT_OPERATION_STRING:
                logging.debug(f"Sign In app found on Home Screen with '{self.SIGN_OUT_OPERATION_STRING}' text")
                return True
            else:
                logging.debug(f"Sign In app found on Home Screen with '{self.SIGN_IN_OPERATION_STRING}' text")
                return False
        else:
            logging.debug("Sign In app not found on Home Screen. Moving on to locate Status Center Sign In...")

        signInButtonText = self.spice.status_center.get_sign_in_button_text()
        if signInButtonText == self.SIGN_IN_OPERATION_STRING:
            logging.debug(f"Sign In app found on in Status Center with '{self.SIGN_IN_OPERATION_STRING}' text")
            return False
        elif signInButtonText == self.SIGN_OUT_OPERATION_STRING:
            logging.debug(f"Sign In app found on in Status Center with '{self.SIGN_OUT_OPERATION_STRING}' text")
            return True
        else:
            logging.debug("Unable to get the sign-in/sign-out button text")
            return False

    def goto_sign_in_app(self, action:str, SignIn:bool = True, assertOnFailure:bool = True)->bool:
        '''
        UI should be on home screen before calling this method
        Navigate to sign in

        Args:
            action: either "Sign In" or "Sign Out"
        '''
        logging.debug("Locating Sign In app on Home Screen...")
        message = ""
        success = False
        if self.__has_home_screen_sign_in():
            success = self.__goto_home_screen_sign_in(action, SignIn)
            message = "Failed to goto home screen sign-in app"
        elif self.__has_status_center_sign_in():
            success = self.__goto_status_center_sign_in(action, SignIn)
            if action == self.SIGN_OUT_OPERATION_STRING:
                # Use longer timeout for sign-out operations as status center can take time to respond
                self.spice.status_center.wait_for_warning_prompt(True, timeout=25.0)
            message = "Failed to goto status center sign-in app"
        else:
            logging.error("Failed to find any sign-in button")
            return False
        if action == self.SIGN_IN_OPERATION_STRING:
            assert self.is_on_sign_in_page(waitForExists=True),\
                logging.error("Failed to navigate to sign-in app from Home Screen or Status Center")
        if not success:
            if assertOnFailure:
                assert False, logging.error(message)
            else:
                logging.debug(message)
            return False
        return True

    # This method selects the Device User sign in method when Admin is the currently selected option
    # This functionality is coverd by:
    # select_sign_in_method("user", "admin")
    # However, current_sigin_user_type() could be helpful for determining the current method
    def select_device_user_login(self):
        """
        UI should be on Device Administrator before calling this method.
        Method navigates to admin login screen and select printer user option.
        """
        self.select_sign_in_method_by_enum(AuthenticationMethod.PrinterUser)

    def current_sigin_user_type(self):
        """
        UI should be on Device Administrator before calling this method.
        This method is to determine the current sign in type since widget object name is different of user type
        return admin/user/ldap
        """
        self.is_on_sign_in_page(waitForExists=True)
        return self.get_authentication_agent_string_from_current_sign_in_page()

    def verify_auth(self, expected_result:str, expected_display_name:str=None):
        """
        Method to verify if user has successfully logged in or not based on current screen

        Args:
            expected_result: the expected result or login attempt "success" or anything else
        """
        if expected_result == "cancel":
            assert self.is_on_last_used_sign_in_page(),\
                logging.error("Device was not on Home screen following Cancel from Sign In page.")
            retval = "cancel"
        elif expected_result == "success":
            assert self.verify_welcome_user_toast_message(expected_display_name),\
                logging.error("Sign In success toast message did not arrive as expected.")
            retval = "success"
        elif expected_result == "blankCreds":
            assert self.on_blank_credentials_screen(),\
                logging.error("Device was not on Blank Credential screen as expected.")
            retval = "blankCreds"
        else:
            assert self.on_invalid_sign_in_screen(),\
                logging.error("Device was not on Invalid Sign In screen as expected.")
            retval = "failed"

        return bool(retval == expected_result)

    def wait_after_sign_in(self, waitTime = 12):
        """
        Method to wait during sign in loading and welcome screen
        """

        countdown = waitTime
        while countdown > 0:
            time.sleep(1)
            try:
                self.spice.query_item("#welcomeUserView")
                logging.info("Welcome screen is visible")
                countdown -= 1
                try:
                    # If the "Access Denied" screen appears, then the welcome view is no longer visible
                    self.spice.query_item("#noAccessView")
                    logging.info("Welcome screen is invisible (\"No Access view is present\"")
                    return
                except:
                    pass
                try:
                    # If the "Not Authenticated" screen appears, then the welcome view is no longer visible
                    self.spice.query_item("#notAuthetnicatedView")
                    logging.info("Welcome screen is invisible (\"Not Authenticated view is present\"")
                    return
                except:
                    pass
            except:
                logging.info("Welcome screen is invisible")
                return

        raise Exception(f"Welcome screen is not invisible in {waitTime} seconds!")

    def wait_for_admin_signin_page(self, time_out=10):
        """
        Method to wait admin signin screen
        """
        self.spice.wait_for(SignInAppWorkflowObjectIds.adminLoginView, time_out)

    def press_admin_signin_page_cancel_button(self):
        """
        Method to click cancel button in admin signin screen
        """
        cancel_button = self.spice.wait_for(SignInAppWorkflowObjectIds.adminCancelButtonControl)
        cancel_button.mouse_click()

    def check_ok_button(self):
        """
        This is not a function of the Workflow UI so the functionality has changed
        """
        return True

    def verify_welcome(self):
        """
        This is not a function of the Workflow UI so the functionality has changed
        """
        return True

    def welcome_mail(self):
        """
        This is not a function of the Workflow UI so the functionality has changed
        """
        return True

    def no_user_sign_in(self, net):
        '''
        UI should show Sign In string on home screen when no user login
        Args:
            net
        Return: sign in: True/False
        '''
        signin_ele = self.spice.wait_for(SignInAppWorkflowObjectIds.menu_item_signinid + " SpiceText")
        sign_in_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cSignIn")
        is_signout = signin_ele["text"] == sign_in_str
        return is_signout

    def goto_serviceuser_sign_in_app(self):
        '''
        UI should be on home screen before calling this method
        Navigate to service user sign in
        '''
        # Click Menu button and wait for menu screen
        self.spice.main_app.goto_menu_app()

        # Scroll to Tools app
        self.spice.homeMenuUI().scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_tools)

        tools_button = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools + " MouseArea")
        tools_button.mouse_click()
        
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.view_menuTools),\
            logging.error("Failed to get to Tools menu")

        service_button = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service + " MouseArea")
        logging.debug(f"Service Button Element: {service_button}")
        service_button.mouse_click()

        assert self.spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard),\
            logging.error("Failed to get Service sign in view")

    def sevice_user_signin(self, password:str):
        """
        UI should be on Home view screen before calling this method

        Args:
            password: password to authenticate with
        """
        currentApp = self.spice.wait_for(SignInAppWorkflowObjectIds.serviceUserPasswordInputFieldText)
        currentApp.__setitem__('displayText', password)
        currentApp = self.spice.wait_for(SignInAppWorkflowObjectIds.serviceUserSignInButtonControl)
        currentApp.mouse_click()

    def service_user_verify_auth(self, verify:str) -> bool:
        if verify == "success":
            try:
                screen_view = self.spice.wait_for(SignInAppWorkflowObjectIds.serviceUserMenuAccessItem)
            except TimeoutError:
                logging.error("Failed to get successful service user sign in view")
                return False
            self.spice.goto_homescreen()
            self.select_universal_sign_out_from_home()
        else:
            screen_view = self.spice.wait_for(MenuAppWorkflowObjectIds.view_access_denied)
            if(screen_view == None):
                logging.error("Failed to get invalid sign in view")
                return False
            self.click_invalid_sign_in_button()

        return True

    def service_user_cleanup(self, resultflow:str):
        """
        Method to navigate back to HomeScreenview

        Args:
            resultflow: the expected result flow, "success" -> good auth,  "failed" -> Onvalid auth
        """
        if resultflow == "success":

            self.spice.goto_homescreen()
            assert self.is_signed_in() == False,\
                logging.error("Device was not Signed Out following return to Home.")

        elif resultflow == "failed":
            assert self.on_invalid_sign_in_screen()
            assert self.click_invalid_sign_in_button()
            self.spice.goto_homescreen()
        else:
            assert False, f"resultflow value of '{resultflow}' is not supported by this method."
        self.workflow_common_operations.scroll_to_position_horizontal(.01)


    def go_home_from_sign_in(self):
        """
        Method returns to the home screen from the sign in page.
        Attempts to press all possible cancel buttons.

        Returns:
            True if successfull, False if unsuccessful
        """

        cancelButtonList = ["#windowsCancelButton", "#adminCancelButton", "#userCancelButton", "#ldapCancelButton"]

        for cancelButon in cancelButtonList:
            try: # Attempt to press every possible cancel button
                currentpage = self.spice.wait_for(cancelButon)
                currentpage.mouse_click()
                self.spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
                return True
            except: # If the attempt fails, try the next button
                pass

        # If no button presses were successful
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
        try:
            self.spice.wait_for("#noAccessView")
            result = False

            # Exit the "No Access" screen
            currentApp = self.spice.wait_for("#noAccessOkButton")
            currentApp.mouse_click()

        except:
            result = True

        return bool(expected == result)

    def verifySignInPopup(spice, expected):
        """
        Method to verify ana sign-in pop up shown in the UI.
        Inputs:
            expected: False = sign-in pop up shown, True = sign in pop up not shown
        Returns:
            False if sign in pop up is shown
        """
        try:
            logging.info("verifySignInPopup")
            spice.wait_for(SignInAppWorkflowObjectIds.printerUserLoginView)
            result = False
        except:
            result = True
        return bool(expected == result)

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

        if permission_id == "ea49d42d-281a-4f70-9c96-8c4b80d8c811": # Fax
            # Get fax app from Menu
            fax_ui = self.spice.fax_ui()
            fax_app_button = fax_ui.get_fax_app()
            if is_locked:
                assert fax_ui.has_lock_icon()
                logging.info("Fax app lock icon is present")

            fax_app_button.mouse_click()
            if not is_locked:
                # Need to skip past the Fax Setup page
                self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
                fax_setup_skip_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetupSkip)
                fax_setup_skip_button.mouse_click()
                self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
            
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
            #self.spice.email.email_select_profile(self.spice.cdm, self.spice.udw, "profile1")

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

    def goto_home_from_permission(self, permission_id, accessGranted):
        """
        Method navigates to the home menu from the input permission

        Inputs:
            spice: spice object
            permission_id: GUID of permission being tested
        """

        if permission_id == "ea49d42d-281a-4f70-9c96-8c4b80d8c811": # Fax
            if accessGranted:
                # Press the skip button when entering the fax app
                adminApp = self.spice.wait_for("#faxSetupHomeViewSkipButton")
                adminApp.mouse_click()

                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "ef92c290-8fa5-4403-85bc-f6becc86b787": # CP_COPY_APP
            try:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            except:
                pass

        elif permission_id == "68e44796-779b-479a-b96b-c8f289276210": # Addressbook (Contacts)
            if accessGranted:
                # Go to  Contacts Landing
                self.spice.contacts.back_to_contacts_screen_from_add_new_contact_screen()

            # Press the home button
            homeButton = self.spice.wait_for("#HomeButton")
            homeButton.mouse_click()
            self.workflow_common_operations.scroll_to_position_horizontal(.01)


        elif permission_id == "16798f84-1c9e-4dea-9047-dec431086661": # Send to Email->To Field
            if accessGranted:
                self.spice.email.check_keyboard_open_on_setting()
                # Check to see if we are on the Profile selection page
                try:
                    self.spice.wait_for("#EmailAppApplicationStackView " + EmailAppWorkflowObjectIds.view_email_profile_view)
                    proflie_button = self.spice.wait_for("#mouseArea")
                    proflie_button.mouse_click()
                except:
                    pass
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "6a482671-4f16-4fd2-9f10-123a58dc0ea4": # Send to Email->From Field
            if accessGranted:
                self.spice.email.check_keyboard_open_on_setting()
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "40132cc0-9ddc-498e-b2ed-1e152f9edc6f": # Send to Email->Subject Field
            if accessGranted:
                self.spice.email.check_keyboard_open_on_setting()
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "a4cc4bee-09f5-4d06-8bd7-3671472d507a": # Send to Email
            if accessGranted:
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "e1c20a2a-235b-4dfd-a92c-f65ae2a45687": # Send to USB
            if accessGranted:
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "dad496ae-3663-46ea-80a6-62fc7c85de25": # Send to Sharepoint
            if accessGranted:
                assert self.spice.sharepoint.verify_scan_sharepoint_setup_page()
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "06eefff9-532d-4026-820b-b9c7ab3f4d61": # Send to Computer
            if accessGranted:
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "aacb972e-6716-43ec-9133-4eb6ee2542dd": # Send to Folder
            if accessGranted:
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()

        elif permission_id == "fc1f5a75-aeb4-474a-b712-4ef20c2a18e0": # View jobs
            if accessGranted:
                # Press the home button
                homeButton = self.spice.wait_for("#HomeButton")
                homeButton.mouse_click()
                self.workflow_common_operations.scroll_to_position_horizontal(.01)
            else:
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
            self.spice.wait_for(SignInAppWorkflowObjectIds.menu_item_signinid, 3.0)
            logging.info("sign in app supported on UI")
            return True

        except Exception as err:
            logging.info("sign in app does not supported on UI")
            return False

    def select_universal_sign_in_from_home(self) -> bool:
        """
        Method to select the universal sign in from the home screen.
        This method will try to sign in from the home screen, status center, or persistent header.
        Returns:
            True if successfully signed in, False if not"""
        logging.info("Attempting to universally sign in from Home...")
        operation = self.SIGN_IN_OPERATION_STRING
        return self._perform_sign_in_or_sign_out_operation(operation)

    def select_universal_sign_out_from_home(self)-> bool:
        logging.info("Attempting to universally sign out from Home...")
        operation = self.SIGN_OUT_OPERATION_STRING
        return self._perform_sign_in_or_sign_out_operation(operation)

    def _perform_sign_in_or_sign_out_operation(self, operation:str) -> bool:
        originalText = self.get_sign_in_status()
        self.goto_universal_sign_in(operation)
        retrys = 0
        while retrys < 5 and self.get_sign_in_status() == originalText:
            time.sleep(.5)  #Sign In Text flip is used to determine sign in state and does not immediately flip
            retrys += 1
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

        # Try to sign in at home screen first
        signed_in = self.goto_sign_in_app(text, assertOnFailure=False)
        if signed_in:
            if text == self.SIGN_OUT_OPERATION_STRING:
                self.verify_user_sign_out_toast_message()
            return
        logging.debug(f"Failed to locate Sign In at Home Screen. Attempting 'text' from Status Center instead.")
        # Try to sign in at status center
        signed_in = True
        try:
            self.spice.status_center.goto_sign_in_app(text)
        except AssertionError:
            signed_in = False

        if text == self.SIGN_OUT_OPERATION_STRING:
            self.spice.status_center.wait_for_warning_prompt(True)
        
        if signed_in: return

        logging.critical("Cannot sign in on Home Screen or Status Center.")
        raise

    def get_sign_in_status(self):
        """
        This method will check if a user (any user) is signed in or out of the device.

        Return:
            Returns a string containing "Sign In" or "Sign Out" or throws exception if neither
        """

        # Try to get home screen sign in button text
        try:
            return self.spice.query_item(SignInAppWorkflowObjectIds.menu_item_signinid + " SpiceText")["text"]
        except:
            # Try to get status center sign in button text
            return self.spice.status_center.get_sign_in_button_text()

    def verify_constraint_message_with_no_credentials(self):
        message = self.spice.wait_for("#ConstraintMessage")
        assert message, logging.error(f"Did not find constraint message")
        logging.debug(f"Confirmed constraint message is showing")

        logging.info(f"Click OK button")
        button = self.spice.wait_for("#okButton")
        button.mouse_click()

        logging.info(f"Click Cancel button on sign in page")
        button = self.spice.wait_for("#windowsCancelButton")
        button.mouse_click()
    
    def has_password_reveal_icon(self) -> bool:
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        password_reveal_icon_button_locator = self.get_password_reveal_icon_locator(currentAgent)
        return self.workflow_common_operations.get_element(password_reveal_icon_button_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
    
    def is_password_input_revealed(self) -> bool:
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        password_input_field_locator = self.get_password_input_field_text_box_locator(currentAgent)
        password_input_field = self.workflow_common_operations.get_element(password_input_field_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        time.sleep(5)
        echo_mode = self.workflow_common_operations.get_element_property(password_input_field, "echoMode")
        #echo_mode = self.workflow_common_operations.wait_and_validate_property_value(password_input_field, "echoMode", 0, 5, 1)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def is_on_sign_in_page(self, waitForExists:bool=True) -> bool:
        # Increase timeout for the sign-in page detection
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS * 2 if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        try:
            self.spice.wait_for(SignInAppWorkflowObjectIds.signInStackView, timeout=timeout)
            sign_in_view = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.signInStackView)
            if not sign_in_view: return False
            return self.workflow_common_operations.get_element_property(sign_in_view, "visible")
        except TimeoutError:
            return False
    
    def is_on_admin_password_required_view(self, waitForExists:bool=True) -> bool:
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        admin_password_required_view = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.adminPasswordRequiredView, timeout=timeout)
        if not admin_password_required_view: return False

        return self.workflow_common_operations.get_element_property(admin_password_required_view, "visible")
    
    def click_cancel_button(self) -> bool:
        logging.info("Attempting to click the Sign In cancel button...")
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        cancel_button_locator = self.get_cancel_button_locator(currentAgent)
        cancel_button = self.workflow_common_operations.get_element(cancel_button_locator, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not cancel_button:
            logging.error(f"Cancel button not found for {currentAgent}. Cancel Button Locator == {cancel_button_locator}")
            return False
        logging.info(f"Clicking cancel button for {currentAgent}. Cancel Button Locator == {cancel_button_locator}")
        return self.workflow_common_operations.click(cancel_button)
    
    def click_signing_in_cancel_button(self) -> bool:
        logging.info("Attempting to click the Signing In cancel button...")
        signing_in_cancel_button_locator = SignInAppWorkflowObjectIds.signingInCancelButton + " #ButtonControl"
        signing_in_cancel_button = self.spice.wait_for(signing_in_cancel_button_locator)
        if not signing_in_cancel_button:
            logging.error(f"Failed to get signing in cancel button: {signing_in_cancel_button_locator}")
            return False
        return self.workflow_common_operations.click(signing_in_cancel_button)


    def click_admin_password_required_ok_button(self) -> bool:
        admin_password_required_ok_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.adminPasswordRequiredOkButton)
        if not admin_password_required_ok_button: return False

        return self.workflow_common_operations.click(admin_password_required_ok_button)
    
    def click_sign_in_button(self) -> bool:
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        sign_in_button_locator = self.get_sign_in_button_locator(currentAgent)
        sign_in_button = self.workflow_common_operations.get_element(sign_in_button_locator, self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not sign_in_button:
            logging.error("Failed to get sign-in button")
            return False
        return self.workflow_common_operations.click(sign_in_button)
    
    def click_password_input_reveal_icon(self) -> bool:
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        password_locator = self.get_password_input_field_locator(currentAgent)

        view_locator = self.get_password_reveal_icon_locator(currentAgent)
        self.scroll_sign_in_to_element_visible(password_locator)
        view = self.workflow_common_operations.get_element(view_locator)
        if not view:
            return False

        #reveal_icon_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.RevealIconButton)
        return self.workflow_common_operations.click(view)

    def on_invalid_sign_in_screen(self, waitForExists:bool=True) -> bool:
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        invalid_sign_in_view = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.invalidSignInView, timeout=timeout)
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
        invalid_sign_in_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.invalidSignInButton)
        outcome = self.workflow_common_operations.click(invalid_sign_in_button)
        time.sleep(1)
        return outcome

    def on_blank_credentials_screen(self, waitForExists:bool=True) -> bool:
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        currentpage = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.blank_creds_view, timeout=timeout)
        if not currentpage:
            logging.error(f"Failed to get Blank Credentials screen within {timeout} seconds")
            return False

        isVisible = self.workflow_common_operations.get_element_property(currentpage, 'visible')
        if not isVisible:
            logging.error(f"Blank Credentials screen is not visible.")

        return isVisible

    def click_blank_credentials_ok_button(self) -> bool:
            currentpage = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.blankCredsButton)
            return self.workflow_common_operations.click(currentpage)
        
    def on_sign_in_screen(self, waitForExists:bool=True) -> bool:
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        try:
            sign_in_view = self.spice.wait_for(SignInAppWorkflowObjectIds.signInStackView, timeout=timeout)
        except TimeoutError:
            sign_in_view = None
        if not sign_in_view:
            logging.error(f"Failed to get Sign-In screen within {timeout} seconds")
            return False
        
        try:
            self.spice.wait_until(lambda: sign_in_view.is_visible() == True, timeout)
        except Exception as exception:
            logging.error(f"Invalid Sign-In View not visible. Caught exception: {exception}")
            return False
    
        return True
    
    def verify_welcome_user_toast_message(self, username:str = None, wait_timeout:float = TIMEOUT_SIGN_IN_SUCCESS) -> bool:
        logging.debug("Verifying Welcome User Toast Message")
        #Alternate Checking for Toast or Invalid Sign In form
        QmlTestServer.wait_until(lambda:\
                self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.toastMessageText, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY) or\
                    self.on_invalid_sign_in_screen(False), timeout=wait_timeout)
        assert not self.on_invalid_sign_in_screen(False), "Sign In failed unexpectedly. Invalid screen was shown instead of the Toast Message."

        toast_message_text = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.toastMessageText, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not toast_message_text:
            logging.error("Failed to get Toast Message")
            return False
        
        if username:
            message = self.workflow_common_operations.get_element_property(toast_message_text, "text")
            if message != f"Welcome, {username}":
                logging.error(f"Toast Message text was not what was expected.\nExpected: {f'Welcome, {username}'}\nRecieved: {message}")
                return False

        timer = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS
        while toast_message_text and timer >= 0:
            toast_message_text = self.spice.check_item(SignInAppWorkflowObjectIds.toastMessageText)
            timer -= 1
            time.sleep(1)
        return not toast_message_text
    
    def verify_user_sign_out_toast_message(self, wait_timeout:float = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS) -> bool:
        logging.debug("Verifying Welcome User Toast Message")
        #Alternate Checking for Toast or Invalid Sign In form
        toast_message_text = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.toastMessageText, timeout=wait_timeout)
        logging.debug(f"Shreya Toast Message Text: {toast_message_text}")
        if not toast_message_text:
            logging.error("Failed to get Toast Message")
            return False
        message = self.workflow_common_operations.get_element_property(toast_message_text, "text")
        expected_message = "Signing out..."
        if message != expected_message:
            logging.error(f"Toast Message text was not what was expected.\nExpected: {expected_message}\nRecieved: {message}")
            return False

        timer = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS
        while toast_message_text and timer >= 0:
            toast_message_text = self.spice.check_item(SignInAppWorkflowObjectIds.toastMessageText)
            timer -= 1
            time.sleep(1)
        return not toast_message_text

    def perform_smartcard_sign_in(self, pin:str, domain:str = None, expected_success:bool = True, user_to_validate_in_toast_message:str = None, toast_message_wait_time:float = TIMEOUT_SIGN_IN_SUCCESS) -> bool:
        defaultSignInMethod = self.get_authentication_agent_string_from_current_sign_in_page()
        self.select_sign_in_method('smartcard', defaultSignInMethod)
        if domain:
            try:
                domain_combo_box = self.spice.query_item(SignInAppWorkflowObjectIds.smartcardDomainComboBox + " #control")
            except QmlItemNotFoundError as exception:
                logging.warning(f"There are not mutliple domains to choose from: {domain}.\nException: {exception}\nChecking for Single Domain View...")
                text_element = self.spice.wait_for(SignInAppWorkflowObjectIds.smartcardSingleDomainText)
                if not text_element:
                    logging.error("Failed to get Single Domain View")
                    return False
                if text_element["text"] != domain:
                    logging.error(f"Single Domain text does not match what was expected.\nExpected: {domain}\nActual: {text_element['text']}")
                    return False
            if domain_combo_box and domain_combo_box.is_visible():
                domain_combo_box.mouse_click()
                domain_item_locator = SignInAppWorkflowObjectIds.smartcardDomainComboBox + "Item_" + domain
                try:
                    self.workflow_common_operations.goto_item(domain_item_locator, SignInAppWorkflowObjectIds.smartcardDomainComboBox + "popupList", scrollbar_objectname = SignInAppWorkflowObjectIds.comboBoxScrollBar)
                except Exception as exception:
                    logging.error(f"Failed to go to item '{domain_item_locator}' in '{SignInAppWorkflowObjectIds.smartcardDomainComboBox + 'popupList'}'")
                    return False
            else: # Single Domain View
                text_element = self.spice.wait_for(SignInAppWorkflowObjectIds.smartcardSingleDomainText)
                if text_element["text"] != domain:
                    logging.error(f"Single Domain default domain is not what is expected.\nExpected: {domain}\nActual: {text_element['text']}")
                    return False
            
        password_field = self.spice.wait_for(SignInAppWorkflowObjectIds.smartCardPinInputField)
        if not password_field:
            logging.error("Failed to get smartcard password field")
            return False
        password_field.__setitem__('displayText', pin)

        sign_in_button = self.spice.wait_for(SignInAppWorkflowObjectIds.smartcardSignInButtonControl)
        if not sign_in_button:
            logging.error("Failed to get smartcard sign-in button")
            return False
        sign_in_button.mouse_click()

        if expected_success:
            return self.verify_welcome_user_toast_message(user_to_validate_in_toast_message, wait_timeout=toast_message_wait_time)
        
        return self.on_invalid_sign_in_screen()

    def get_sign_in_page_locator_by_authentication_method(self, authentication_method: AuthenticationMethod) -> str:
        """
        This method will return the sign in page locator based on the authentication method.
        """
        if authentication_method == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserCancelButtonControl
        elif authentication_method == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminCancelButtonControl
        elif authentication_method == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsCancelButtonControl
        elif authentication_method == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapCancelButtonControl
        elif authentication_method == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeCancelButtonControl
        elif authentication_method == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardCancelButtonControl
        else:
            raise ValueError(f"Unsupported authentication method: {authentication_method}")

    def is_current_sign_in_page_for_authentication_method(self, authentication_method: AuthenticationMethod, waitForExists:bool=True) -> bool:
        """
        This method will check if the current sign in page is for the specified authentication method.
        """
        logging.debug(f"Checking if the current sign in page is for {authentication_method}...")
        timeout = WorkflowUICommonOperations.DEFAULT_WAIT_TIME_SECONDS if waitForExists else self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY
        signInPageLocator = self.get_sign_in_page_locator_by_authentication_method(authentication_method)
        object = self.workflow_common_operations.get_element(signInPageLocator, timeout)
        outcome = False
        if object:
            outcome = self.workflow_common_operations.get_element_property(object, "visible")
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

    def is_on_idcodes_sign_in_page(self, waitForExists:bool=True) -> bool:
        return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.IDCode, waitForExists)

    def is_on_smartcard_sign_in_page(self, waitForExists:bool=True) -> bool:
        return self.is_current_sign_in_page_for_authentication_method(AuthenticationMethod.Smartcard, waitForExists)

    def is_on_last_used_sign_in_page(self, waitForExists:bool=True) -> bool:
        """
        This method will check if the last used sign in page is visible.
        """
        logging.info(f"Checking if the last used sign in page is visible: {self.last_used_authentication_method}")
        outcome = self.is_current_sign_in_page_for_authentication_method(self.last_used_authentication_method, waitForExists)
        if outcome: logging.info(f"Is on the last used Sign In Page: {self.last_used_authentication_method.name}")
        return outcome

    def get_authentication_method_from_current_sign_in_page(self)-> AuthenticationMethod:
        outcome = None
        assert self.is_on_sign_in_page(True), logging.error("Not on Sign In page was expected")
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
        elif self.last_used_authentication_method != AuthenticationMethod.IDCode and self.is_on_idcodes_sign_in_page(False):
            outcome = AuthenticationMethod.IDCode
        elif self.last_used_authentication_method != AuthenticationMethod.Smartcard and self.is_on_smartcard_sign_in_page(False):
            outcome = AuthenticationMethod.Smartcard
        else: assert False, logging.error("Unable to determine the current Sign In method")
        logging.info(f"Current Sign In method is {outcome.name}")
        return outcome

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
        auth_agent = auth_agent.lower()
        if auth_agent == "user": outcome = AuthenticationMethod.PrinterUser
        elif auth_agent == "admin": outcome = AuthenticationMethod.Admin
        elif auth_agent =="windows": outcome = AuthenticationMethod.Windows
        elif auth_agent == "ldap": outcome = AuthenticationMethod.Ldap
        elif auth_agent == "identificationcode": outcome = AuthenticationMethod.IDCode
        elif auth_agent == "smartcard": outcome = AuthenticationMethod.Smartcard
        else: assert False, logging.error(f"{auth_agent} not yet supported by this method")
        return outcome

    def get_authentication_agent_string_from_current_sign_in_page(self) -> str:
        """
        This method will return the authentication agent string from the current sign in page.
        It will return 'windows', 'ldap', 'admin', 'printerUser', 'idcodes' or 'smartcard'
        """
        auth_agent = self.get_authentication_method_from_current_sign_in_page()
        outcome = self.__convert_authentication_agent_enumeration_to_agent_string(auth_agent)
        logging.info(f"Current Sign In method is as string: {outcome}")
        return outcome

    def verify_sign_in_success(self, expectedDisplayName):
        logging.info("Verifying Sign In was successful...")
        start_time = time.time()
        assert self.verify_welcome_user_toast_message(expectedDisplayName),\
            logging.error("Failed to find Welcome toast message")

        assert self.is_signed_in(),\
            logging.error("Failed to Sign In")

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Verify Sign In completed successfully and took {elapsed_time} seconds.")

    def verify_sign_in_success_and_sign_out(self, expectedDisplayName):
        logging.info("Verifying Sign In was successful and attempting to Sign Out...")
        start_time = time.time()
        self.verify_sign_in_success(expectedDisplayName)

        logging.info("Step 6: Click Sign Out button")
        self.goto_universal_sign_in(self.SIGN_OUT_OPERATION_STRING)
        time.sleep(3)
        logging.info("Step 7: Verify Sign In button is present")
        assert not self.is_signed_in(),\
            logging.error("Failed to Sign Out")

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
        time.sleep(3)
        assert self.is_on_last_used_sign_in_page(),\
            logging.error("Not on Sign In page when we should be")
        assert self.click_cancel_button(),\
            logging.error("Failed to click Sign In Cancel button")
        time.sleep(1)
        if self.spice.status_center.is_status_center_visible():
                self.spice.status_center.collapse()
                time.sleep(1)
                assert not self.spice.status_center.is_status_center_visible(),\
                    logging.error("Failed to collapse status center.")
        assert self.spice.home.is_on_home_screen(),\
            logging.error("Failed to return to Home Screen.")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Verify Sign In was Invalid and return to Home completed successfully and took {elapsed_time} seconds.")

    def get_sign_in_scroll_bar_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
            This method will return the sign in scroll bar locator based on the authentication agent.

            :param authentication_agent: The authentication method (e.g., PrinterUser, Admin, Windows, Ldap, IDCode, Smartcard)

            :return: The locator string for the sign in scroll bar.
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserSignInScrollBar
        elif authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminSignInScrollBar
        elif authentication_agent == AuthenticationMethod.Windows:
            return SignInAppWorkflowObjectIds.windowsSignInScrollBar_MultiDimensional.format(self.get_current_windows_login_view_locator())
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapSignInScrollBar
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeSignInScrollBar
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardSignInScrollBar
        else:
            assert False, f"Not implemented for authentication agent: '{authentication_agent.value}'"

    def get_sign_in_footer_locator(self, authentication_agent:AuthenticationMethod) -> str:
        """
            This method will return the sign in footer locator based on the authentication agent.

            :param authentication_agent: The authentication method (e.g., PrinterUser, Admin, Windows, Ldap, IDCode, Smartcard)

            :return: The locator string for the sign in footer.
        """
        if authentication_agent == AuthenticationMethod.PrinterUser:
            return SignInAppWorkflowObjectIds.printerUserSignInFooter
        elif authentication_agent == AuthenticationMethod.Admin:
            return SignInAppWorkflowObjectIds.adminSignInFooter
        elif authentication_agent == AuthenticationMethod.Windows:
            multiDimensionalView = self.get_current_windows_login_view_locator()
            return SignInAppWorkflowObjectIds.windowsUserSignInFooter_MultiDimensional.format(multiDimensionalView)
        elif authentication_agent == AuthenticationMethod.Ldap:
            return SignInAppWorkflowObjectIds.ldapUserSignInFooter
        elif authentication_agent == AuthenticationMethod.IDCode:
            return SignInAppWorkflowObjectIds.idCodeSignInFooter
        elif authentication_agent == AuthenticationMethod.Smartcard:
            return SignInAppWorkflowObjectIds.smartcardUserSignInFooter
        else:
            assert False, f"Not implemented for authentication agent: '{authentication_agent.value}'"

    def scroll_sign_in_to_element_visible(self, elementLocator:str) -> bool:
        """
            This method will scroll the Sign In screen to make the specified element visible.

            :param elementLocator: The locator string for the element to scroll to.

            :return: True if the scroll was successful, False otherwise.
        """
        logging.info(f'signIn.scroll_to_element_visible({elementLocator})')
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        #If scroll bar is not present, return True
        scroll_bar_locator = self.get_sign_in_scroll_bar_locator(currentAgent)
        scroll_bar = self.workflow_common_operations.get_element(scroll_bar_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not scroll_bar:
            logging.error(f"Failed to get scroll_bar: {scroll_bar_locator}")
            return True
        logging.info(f"Located the Sign In scroll_bar: {scroll_bar_locator}. Scrolling to element visible: {elementLocator}")
        #Get the height of the Sign In screen
        view_locator = self.get_current_sign_in_view_locator(currentAgent)
        view = self.workflow_common_operations.get_element(view_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        signInScreenHeight = self.workflow_common_operations.get_element_property(view, "height")
        if not signInScreenHeight:
            logging.error(f"Failed to get height of the Sign In screen: {view_locator}")
            return False
        #Get the height of the Sign In screen Footer containing the Sign In and Cancel buttons.
        footerLocator = self.get_sign_in_footer_locator(currentAgent)
        footer_view = self.workflow_common_operations.get_element(footerLocator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        footer_height = self.workflow_common_operations.get_element_property(footer_view, "height")
        if not footer_height:
            logging.error(f"Failed to get height of the Sign In screen Footer: {footerLocator}")
            return False
        #Get the element we are scrolling to
        elementObject = self.workflow_common_operations.get_element(elementLocator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not elementObject:
            logging.error(f"Unable to locate element to scroll to: {elementLocator}")
            return False
        #Scoll to the height of the element on Sign In Screen minus the height of the Sign In footer to make element visible on UI
        heightToScrollTo = signInScreenHeight - footer_height
        logging.info(f"Scrolling to element {elementLocator} with height: {heightToScrollTo}")
        outcome = self.workflow_common_operations.scroll_vertical(scroll_bar, elementObject, heightToScrollTo)
        if not outcome:
            logging.error(f"Failed to scroll to element {elementLocator} with height: {heightToScrollTo}")
        return outcome

    def wait_for_sign_in_page(self):
        """
            Method to wait for the sign-in page to appear. Used in tests where the sign-in page doesn't
            necessarily immediately popup when accessed.
        """
        sign_in_page = self.spice.wait_for(SignInAppWorkflowObjectIds.signInStackView, timeout=30)
        self.spice.validate_button(sign_in_page)
    
    def has_sign_in(self) -> bool:
        """
            Checks to see if the device has a way to sign-in.
        """
        try:
            self.is_signed_in()
        except AssertionError:
            logging.warning("Device has no way to sign-in/sign-out")
            return False
        return True
    
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

    def sign_in_admin_through_status_center(self, password: str):
        """
            This method will sign in the user through the status center.
            It will expand the dashboard, click on the sign in button, select the Administrator option,
            enter the credentials, and collapse the dashboard.
        """
        time.sleep(2)
        
        # Expand dashboard
        self.spice.statusCenter_dashboard_expand()
        # Click on sign in button
        sign_in_button = self.spice.wait_for(SignInAppWorkflowObjectIds.sign_in)
        self.spice.wait_until(lambda: sign_in_button["visible"] and sign_in_button["enabled"])
        sign_in_button.mouse_click()
        
        # Click in comboBoxList
        sign_in_combobox = self.spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)
        self.spice.wait_until(lambda: sign_in_combobox["visible"] and sign_in_combobox["enabled"])
        sign_in_combobox.mouse_click() 
        
        # Click in the Administrator option
        admin_option = self.spice.wait_for(MenuAppWorkflowObjectIds.list_item_admin)
        self.spice.wait_until(lambda: admin_option["visible"] and admin_option["enabled"])
        admin_option.mouse_click()
        time.sleep(2)
        
        # Enter credentials
        self.enter_credentials(True, password)

        # Collapse dashboard
        self.spice.statusCenter_dashboard_collapse()
        
        # Wait for home screen
        self.spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
    
    def sign_out_through_status_center(self):
        """
            This method will sign out the user through the status center.
            It will expand the dashboard, click on the sign out button, confirm the sign out,
            and wait for the home screen to appear.
        """
        time.sleep(2)
        
        # Expand dashboard
        self.spice.statusCenter_dashboard_expand()
        
        # Click on sign out button
        sign_in_button = self.spice.wait_for(SignInAppWorkflowObjectIds.sign_out)
        self.spice.wait_until(lambda: sign_in_button["visible"] and sign_in_button["enabled"])
        sign_in_button.mouse_click()
        
        # Wait for Sign Out screen
        self.spice.wait_for(SignInAppWorkflowObjectIds.confirm_sign_out_view)
        
        # Confirm Sign Out
        confirm_button = self.spice.wait_for(SignInAppWorkflowObjectIds.confirmSignOutYesButton)
        self.spice.wait_until(lambda: confirm_button["visible"] and confirm_button["enabled"])
        confirm_button.mouse_click()
        
        # Wait for home screen
        self.spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
