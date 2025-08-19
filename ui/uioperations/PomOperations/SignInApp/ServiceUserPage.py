import logging

from .Locators import Locators
from .Components.TextField import TextField
from .Components.PrinterUserPageVerification import PrinterUserPageVerification

"""
    Must be on Sign In page to used this class.
"""

class ServiceUserPage():
    def __init__(self, page):
        self.__page = page
        self.__password_field = TextField(page, Locators.ServiceUserPasswordInputField)
        #self.verify =  PrinterUserPageVerification(page)
    
    def select_method(self) -> bool:
        """
            Selects 'Service User' as sign in method
        """
        if self.verify.on_page() == True:
            logging.debug("Already on Service User Sign In page")
            return True
        
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.ServiceUser) == False:
            logging.error("Failed to switch to Service User sign in method")
            return False

        return self.verify.on_page()

    def enter_password(self, password:str) -> bool:
        logging.debug(f"Entering password for service user: {password}...")
        if self.__password_field.enter(password) == False:
            logging.error(f"Failed to enter password \'{password}\' into password field \'{self.__password_field.locator}\'")
            return False
        logging.debug(f"Successfully entered password: {password}")
        return True

    def click_sign_in_button(self) -> bool:
        logging.debug("Clicking Service User Sign In button...")
        return self.__page.wait_and_click(Locators.ServiceUserSignInButton)

    def click_cancel_button(self) -> bool:
        logging.debug("Clicking Service User Cancel button...")
        return self.__page.wait_and_click(Locators.ServiceUserCancelButton)

    def click_invalid_sign_in_button(self):
        logging.debug("Clicking Invalid Sign In button...")
        # This is the 'Sign In' buttton that is on the 'Invalid Sign In' screen
        return self.__page.wait_and_click(Locators.ServiceUserInvalidSignInButton)
