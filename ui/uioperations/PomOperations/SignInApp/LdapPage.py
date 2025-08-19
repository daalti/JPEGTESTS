import logging

from .Locators import Locators
from .Components.TextField import TextField
from .Components.LdapAuthPageVerification import LdapAuthPageVerification
from dunetuf.security.SecurityTypes import AuthenticationMethod

"""
    Must be on Sign In page to used this class.
"""

class LdapPage():
    def __init__(self, page):
        self.__page = page
        self.__username_field = TextField(page, Locators.LdapUsernameInputField)
        self.__password_field = TextField(page, Locators.LdapPasswordInputField)
        self.verify =  LdapAuthPageVerification(page)
    
    def get_password_input_display_text(self) -> str:
        return self.__password_field.get_display_text()
    
    def select_method(self) -> bool:
        """
            Selects 'LDAP' as sign in method
        """
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_sign_in_method_by_enum()\' method")
        return self.__page.spice.signIn.select_sign_in_method_by_enum(AuthenticationMethod.Ldap)
    
    def is_password_input_revealed(self) -> bool:
        echo_mode = self.__page.get_locator_attribute(Locators.LdapPasswordInputField, self.__page.Attribute.EchoMode)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def has_password_reveal_icon(self) -> bool:
        return self.__page.wait_for_element(Locators.IDCodePinInputRevealIconButton) != None

    def enter_username(self, username:str) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.enter_username()\' method")
        return self.__page.spice.signIn.enter_username(username)

    def enter_password(self, password:str) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.enter_password()\' method")
        return self.__page.spice.signIn.enter_password(password)

    def click_sign_in_button(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.click_sign_in_button()\' method")
        return self.__page.spice.signIn.click_sign_in_button()

    def click_cancel_button(self) -> bool:
        logging.debug("Clicking Ldap Cancel button...")
        return self.__page.wait_and_click(Locators.LdapCancelButton)
    
    def click_password_input_reveal_icon(self) -> bool:
        if self.__page.wait_for_element(Locators.LdapSignInViewLayout) != None:
            height = self.__page.get_locator_attribute(Locators.LdapSignInViewLayout, self.__page.Attribute.Height)
            self.__page.scroll_vertical(Locators.LdapSignInScrollBar, Locators.LdapPasswordInput, height - 75)
        return self.__page.wait_and_click(Locators.LdapPasswordInputRevealIconButton)