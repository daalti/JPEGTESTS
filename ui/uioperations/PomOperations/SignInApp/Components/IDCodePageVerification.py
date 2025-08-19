from ..Locators import Locators
from .Verification import Verification
from ..Page import Page

import logging

class IDCodePageVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page
    
    def on_page(self) -> bool:
        logging.debug("Verifying we are on ID Code Sign In page...")
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_on_idcodes_sign_in_page()\' method")
        return self.__page.spice.signIn.is_on_idcodes_sign_in_page()