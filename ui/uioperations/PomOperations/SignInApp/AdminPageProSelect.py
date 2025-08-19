import logging
import time

from .LocatorsProSelect import LocatorsProSelect
from .Components.TextField import TextField

"""
    Must be on Sign In page to used this class.
"""

class AdminPageProSelect():
    def __init__(self, page):
        self.__page = page
        self.__password_field = TextField(page, LocatorsProSelect.AdminPasswordView)

    def select_method(self) -> bool:
        """
            Selects 'Admin' as sign in method
        """
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.Admin) == False:
            logging.error("Failed to switch to Admin sign in method")
            return False
        
        return True
    
    def enter_password(self, password:str) -> bool:
        admin_view = self.__page.wait_for_element(LocatorsProSelect.AdminView)
        self.__page.scroll_right_increment(admin_view, 1)

        if not self.__page.wait_and_click(LocatorsProSelect.AdminPasswordButton):
            logging.error("Failed to click Password field")
            return False
        
        if not self.__password_field.enter(password):
            logging.error(f"Failed to enter \'{password}\' in password field")
            return False
        
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        if not self.__page.scroll_left_increment(tumbler, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(admin_view, 7): return False

        return True

    def click_sign_in_button(self) -> bool:
        admin_view = self.__page.wait_for_element(LocatorsProSelect.AdminView)
        if not self.__page.scroll_right_increment(admin_view, 2): return False

        if not self.__page.wait_and_click(LocatorsProSelect.AdminSignInOkButton): return False

        return True