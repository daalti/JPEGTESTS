from ..Locators import Locators
from .Verification import Verification
from ..Page import Page

import logging

class WindowsAuthPageVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page
    
    def on_page(self) -> bool:
        """
            NOTE: There are two windows sign in pages. One that shows
                  a single domain in the domain field, and one that shows
                  multiple domains via a drop down box.
        """
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_on_windows_sign_in_page()\' method")
        return self.__page.spice.signIn.is_on_windows_sign_in_page()