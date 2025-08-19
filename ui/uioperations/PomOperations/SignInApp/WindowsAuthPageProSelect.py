import logging
import time

from .LocatorsProSelect import LocatorsProSelect
from .Components.TextField import TextField
from .Components.WindowsAuthPageVerification import WindowsAuthPageVerification

"""
    Must be on Sign In page to used this class.
"""

class WindowsAuthPageProSelect():
    def __init__(self, page):
        self.__page = page
        self.__username_field = TextField(page, LocatorsProSelect.EnterUserNameView)
        self.__password_field = TextField(page, LocatorsProSelect.PasswordView)

    def select_method(self) -> bool:
        """
            Selects 'Windows' as sign in method
        """
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.Windows) == False:
            logging.error("Failed to switch to Windows sign in method")
            return False
        
        return True

    def select_domain(self, domain:str) -> bool:
        pass

    def enter_username(self, username:str) -> bool:
        windows_view = self.__page.wait_for_element(LocatorsProSelect.WindowsView)
        self.__page.scroll_right_increment(windows_view, 2)

        if not self.__page.wait_and_click(LocatorsProSelect.WindowsUserNameButton):
            logging.error("Failed to click User Name field")
            return False
        
        if not self.__username_field.enter(username):
            logging.error(f"Failed to enter \'{username}\' in username field")
            return False
        
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        if not self.__page.scroll_left_increment(tumbler, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(windows_view, 6): return False

        return True
    
    def enter_password(self, password:str) -> bool:
        windows_view = self.__page.wait_for_element(LocatorsProSelect.WindowsView)
        self.__page.scroll_right_increment(windows_view, 3)

        if not self.__page.wait_and_click(LocatorsProSelect.WindowsPasswordButton):
            logging.error("Failed to click Password field")
            return False
        
        if not self.__password_field.enter(password):
            logging.error(f"Failed to enter \'{password}\' in password field")
            return False
        
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        if not self.__page.scroll_left_increment(tumbler, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(windows_view, 7): return False

        return True

    def click_sign_in_button(self) -> bool:
        windows_view = self.__page.wait_for_element(LocatorsProSelect.WindowsView)
        if not self.__page.scroll_right_increment(windows_view, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.WindowsSignInOkButton): return False

        return True

    def click_cancel_button(self) -> bool:
        return False