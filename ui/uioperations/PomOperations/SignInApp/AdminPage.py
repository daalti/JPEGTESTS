import logging

from .Locators import Locators
from .Components.TextField import TextField
from .Components.Button import Button
from .Components.AdminPageVerification import AdminPageVerification
from dunetuf.security.SecurityTypes import AuthenticationMethod

"""
    Must be on Sign In page to used this class.
"""

class AdminPage():
    def __init__(self, page):
        self.__sign_in_page = page
        self.__password_field = TextField(page, Locators.AdminPasswordInputField)
        self.__sign_in_button = Button(page, Locators.AdminSignInButton)
        self.__cancel_button = Button(page, Locators.AdminCancelButton)
        self.verify = AdminPageVerification(page)
    
    def get_password_input_display_text(self) -> str:
        return self.__password_field.get_display_text()

    def select_method(self) -> bool:
        """
            Selects 'Admin' as sign in method
        """
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_sign_in_method_by_enum()\' method")
        return self.__sign_in_page.spice.signIn.select_sign_in_method_by_enum(AuthenticationMethod.Admin)
    
    def is_password_input_revealed(self) -> bool:
        echo_mode = self.__sign_in_page.get_locator_attribute(Locators.AdminPasswordInputField, self.__sign_in_page.Attribute.EchoMode)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def has_password_reveal_icon(self) -> bool:
        return self.__sign_in_page.wait_for_element(Locators.AdminPasswordInputRevealIconButton) != None

    def enter_password(self, password:str) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.enter_password()\' method")
        return self.__sign_in_page.spice.signIn.enter_password(password)

    def click_sign_in_button(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.click_sign_in_button()\' method")
        return self.__sign_in_page.spice.signIn.click_sign_in_button()

    def click_cancel_button(self) -> bool:
        logging.debug("Clicking Admin Cancel button")
        return self.__cancel_button.click()
    
    def click_password_input_reveal_icon(self) -> bool:
        if self.__sign_in_page.wait_for_element(Locators.AdminSignInViewLayout) != None:
            height = self.__sign_in_page.get_locator_attribute(Locators.AdminSignInViewLayout, self.__sign_in_page.Attribute.Height)
            self.__sign_in_page.scroll_vertical(Locators.AdminSignInScrollBar, Locators.AdminPasswordInput, height - 50)
        return self.__sign_in_page.wait_and_click(Locators.AdminPasswordInputRevealIconButton)