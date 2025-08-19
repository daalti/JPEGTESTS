import logging

from .Locators import Locators
from .Components.TextField import TextField
from .Components.IDCodePageVerification import IDCodePageVerification
from dunetuf.security.SecurityTypes import AuthenticationMethod

"""
    Must be on Sign In page to used this class.
"""

class IDCodePage():
    def __init__(self, page):
        self.__page = page
        self.__password_field = TextField(page, Locators.IDCodePasswordInputField)
        self.verify =  IDCodePageVerification(page)
    
    def get_password_input_display_text(self) -> str:
        return self.__password_field.get_display_text()
    
    def select_method(self) -> bool:
        """
            Selects 'ID Code' as sign in method
        """
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_sign_in_method_by_enum()\' method")
        return self.__page.spice.signIn.select_sign_in_method_by_enum(AuthenticationMethod.IDCode)
    
    def is_password_input_revealed(self) -> bool:
        echo_mode = self.__page.get_locator_attribute(Locators.IDCodePasswordInputField, self.__page.Attribute.EchoMode)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def has_password_reveal_icon(self) -> bool:
        return self.__page.wait_for_element(Locators.IDCodePinInputRevealIconButton) != None

    def enter_password(self, password:str) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.enter_password()\' method")
        return self.__page.spice.signIn.enter_password(password)

    def click_sign_in_button(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.click_sign_in_button()\' method")
        return self.__page.spice.signIn.click_sign_in_button()

    def click_cancel_button(self) -> bool:
        logging.debug("Clicking ID Code Cancel button...")
        return self.__page.wait_and_click(Locators.IDCodeUserCancelButton)
    
    def click_password_input_reveal_icon(self) -> bool:
        if self.__page.wait_for_element(Locators.IDCodeSignInViewLayout) != None:
            height = self.__page.get_locator_attribute(Locators.IDCodeSignInViewLayout, self.__page.Attribute.Height)
            self.__page.scroll_vertical(Locators.IDCodeSignInScrollBar, Locators.IDCodePasswordInput, height - 50)
        return self.__page.wait_and_click(Locators.IDCodePinInputRevealIconButton)