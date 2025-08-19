import logging
import time

from .LocatorsProSelect import LocatorsProSelect
from .Components.TextField import TextField

"""
    Must be on Sign In page to used this class.
"""

class LdapPageProSelect():
    def __init__(self, page):
        self.__page = page
        self.__username_field = TextField(page, LocatorsProSelect.EnterUserNameView)
        self.__password_field = TextField(page, LocatorsProSelect.PasswordView)

    def select_method(self) -> bool:
        """
            Selects 'LDAP' as sign in method
        """
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.LDAP) == False:
            logging.error("Failed to switch to LDAP sign in method")
            return False
        
        return True

    def select_domain(self, domain:str) -> bool:
        pass

    def enter_username(self, username:str) -> bool:
        ldap_view = self.__page.wait_for_element(LocatorsProSelect.LDAPView)
        self.__page.scroll_right_increment(ldap_view, 1)

        if not self.__page.wait_and_click(LocatorsProSelect.LdapUserNameButton):
            logging.error("Failed to click User Name field")
            return False
        
        if not self.__username_field.enter(username):
            logging.error(f"Failed to enter \'{username}\' in username field")
            return False
        
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        if not self.__page.scroll_left_increment(tumbler, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(ldap_view, 6): return False

        return True
    
    def enter_password(self, password:str) -> bool:
        ldap_view = self.__page.wait_for_element(LocatorsProSelect.LDAPView)
        self.__page.scroll_right_increment(ldap_view, 2)

        if not self.__page.wait_and_click(LocatorsProSelect.LdapPasswordButton):
            logging.error("Failed to click Password field")
            return False
        
        if not self.__password_field.enter(password):
            logging.error(f"Failed to enter \'{password}\' in password field")
            return False
        
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        if not self.__page.scroll_left_increment(tumbler, 5): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(ldap_view, 7): return False

        return True

    def click_sign_in_button(self) -> bool:
        ldap_view = self.__page.wait_for_element(LocatorsProSelect.LDAPView)
        if not self.__page.scroll_right_increment(ldap_view, 3): return False

        if not self.__page.wait_and_click(LocatorsProSelect.LdapSignInOkButton): return False

        return True

    def click_cancel_button(self) -> bool:
        return False