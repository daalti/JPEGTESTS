import logging
from enum import Enum
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.SignInAppProSelectUIOperations import SignInAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import KeyboardType, ProSelectHybridKeyboardOperations
from dunetuf.ui.uioperations.BaseOperations.ISignInAppUIOperations import ISignInAppUIOperations
from dunetuf.security.SecurityTypes import AuthenticationMethod
import time

class SigninAppProSelectUIHybridOperations(SignInAppProSelectUIOperations):

    #----------------------------------Function Keywords--------------------------------#
    menu_item_signinid = "#7db992ba-557a-461c-b941-6023aa8cfa34"
    
    ok_button_prefix = "#signInOkButton"
    user_button_prefix = "#enterUsernameButton"
    password_button_prefix = "#enterPasswordButton"

    # TODO determine why local admin cannot use the same enterPasswordButton and signInOkButton without breaking the other login types
    # does the button on each screen need to be unique?
    local_admin_password_button = "#localAdminPasswordButton"
    local_admin_ok_button = "#localAdminOkButton"

    # Views
    deviceUserView = "#DeviceUserView"
    localadminview = "#LocalAdminView"
    windowsView = "#WindowsView"
    ldapView = "#LdapView"

    current_row = 0
    current_pos = 0
    current_keyboard_type = KeyboardType.ALPHABET

    def __init__(self, spice):
        self.maxtimeout = 100
        super().__init__(spice)
        self.proselect_UI_Hybrid_operations= ProSelectHybridKeyboardOperations(self.spice )
        self.proselect_common_operations = ProSelectCommonOperations(self.spice)
    
    def click_cancel_button(self) -> bool:
        """
            ProSelect Hybrid does not have a cancel or back button on the sign-in page
        """
        self.spice.udw.mainUiApp.KeyHandler.setKeyPress("HOME")
        return True
    
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
        self.spice.keyBoard.keyboard_press_icon(ProSelectUIObjectIds.HybridKeyboardEnterButton, return_home=False)
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
        self.spice.keyBoard.keyboard_press_icon(ProSelectUIObjectIds.HybridKeyboardEnterButton, return_home=False)
        time.sleep(1)
        return True

    def set_service_pin(self,udw):
        defaultPin = udw.mainApp.AdminStandard.getDefaultDevicePassword()
        keyboardTextField = self.spice.query_item("#hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = defaultPin
        self.proselect_UI_Hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)

    def is_on_admin_password_required_view(self) -> bool:
        admin_password_required_view = self.proselect_common_operations.get_element(ProSelectUIObjectIds.AdminPasswordRequiredView)
        if not admin_password_required_view: return False

        return self.proselect_common_operations.get_element_property(admin_password_required_view, "visible")
    
    def on_sign_in_screen(self, waitForExists:bool=True) -> bool:
        return self.is_on_sign_in_page()

    def support_sign_in_app_from_fp(self):
        """
        This function is to check sign in app supported on printer ui or not

        Return:
              True: sign in app supported on UI
              False: sign in app doesn't supported on UI
        """

        self.spice.goto_homescreen()

        try:
            self.spice.wait_for(self.menu_item_signinid)
            return True

        except Exception as err:
            return False
        
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
        while (self.spice.query_item("#CurrentAppText")["text"] != "Sign In" and
         self.spice.query_item("#CurrentAppText")["text"] != "Sign Out" and 
         timeSpentWaiting < self.maxtimeout):
            homeApp.mouse_wheel(0,0)
            timeSpentWaiting = time.time() - startTime

        homeApp = self.spice.query_item(ProSelectUIObjectIds.homeScreenView)
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)
        homeApp.mouse_wheel(180,180)

        return self.spice.query_item("#CurrentAppText")["text"]

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

        self.reset_sign_in_page_scroll_bar_manually(authAgent)

        # Enter the username (if provided)
        #user auth method does not have a user name
        if authAgent != AuthenticationMethod.Admin:
            self.proselect_common_operations.goto_item(user_button, view)
            self.proselect_UI_Hybrid_operations.keyboard_set_text_with_out_dial_action(username)
            self.proselect_UI_Hybrid_operations.keyboard_press_icon_ok_button(ProSelectUIObjectIds.HybridKeyboardEnterButton)

        # NOTE: We do not enter the password for blank credentials

        result = self.spice.query_item(ok_button)["enabled"] is False
        assert result