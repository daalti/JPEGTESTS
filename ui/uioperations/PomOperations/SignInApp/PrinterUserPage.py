import logging

from .Locators import Locators
from .Components.TextField import TextField
from .Components.PrinterUserPageVerification import PrinterUserPageVerification
from dunetuf.security.SecurityTypes import AuthenticationMethod

"""
    Must be on Sign In page to used this class.
"""

class PrinterUserPage():
    def __init__(self, page):
        self.__page = page
        self.__username_field = TextField(page, Locators.PrinterUserUsernameInputField)
        self.__password_field = TextField(page, Locators.PrinterUserPasswordInputField)
        self.verify =  PrinterUserPageVerification(page)
    
    def get_password_input_display_text(self) -> str:
        return self.__password_field.get_display_text()

    def select_method(self) -> bool:
        """
            Selects 'Printer User' as sign in method
        """
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_sign_in_method_by_enum()\' method")
        return self.__page.spice.signIn.select_sign_in_method_by_enum(AuthenticationMethod.PrinterUser)
    
    def is_password_input_revealed(self) -> bool:
        echo_mode = self.__page.get_locator_attribute(Locators.PrinterUserPasswordInputField, self.__page.Attribute.EchoMode)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def has_password_reveal_icon(self) -> bool:
        return self.__page.wait_for_element(Locators.PrinterUserPasswordInputRevealIconButton) != None

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
        logging.debug("Clicking Printer User Cancel button...")
        return self.__page.wait_and_click(Locators.PrinterUserCancelButton)
    
    def click_password_input_reveal_icon(self) -> bool:
        if self.__page.wait_for_element(Locators.PrinterUserSignInViewLayout) != None:
            height = self.__page.get_locator_attribute(Locators.PrinterUserSignInViewLayout, self.__page.Attribute.Height)
            footer = self.__page.wait_for_element(Locators.FooterRectangle)
            if(footer != None):
             # NOTE: We must scroll a little more to account for devices where the sign-in button is in a footer and not in a scroll area
             self.__page.scroll_vertical(Locators.PrinterUserSignInScrollBar, Locators.PrinterUserPasswordInput, height - 80)
            else:
             self.__page.scroll_vertical(Locators.PrinterUserSignInScrollBar, Locators.PrinterUserPasswordInput, height)
        return self.__page.wait_and_click(Locators.PrinterUserPasswordInputRevealIconButton)