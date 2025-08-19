from ..Locators import Locators
from .Verification import Verification
from ..Page import Page

import logging
import time

class SignInPageVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page
    
    def on_page(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_on_sign_in_page()\' method")
        return self.__page.spice.signIn.is_on_sign_in_page()

    def on_invalid_sign_in_page(self, timeout:float = Page.DEFAULT_TIMEOUT) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.on_invalid_sign_in_screen()\' method")
        return self.__page.spice.signIn.on_invalid_sign_in_screen()
    
    def welcome_user_toast_message(self, user_name:str) -> bool:
        logging.debug("Verifying Welcome User Toast Message appears")
        if not self.__page.compare_locator_text(Locators.ToastMessageText, f"Welcome, {user_name}"): return False
        toast_message_view = self.__page.wait_for_element(Locators.ToastMessageView)
        timer:int = self.__page.DEFAULT_TIMEOUT
        while toast_message_view and timer >= 0:
            toast_message_view = self.__page.wait_for_element(Locators.ToastMessageView)
            timer -= 1
            time.sleep(1)
        return not toast_message_view
