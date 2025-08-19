from ...SignInApp.Components.Verification import Verification
from ...SignInApp.Page import Page
from ..Locators import Locators

import logging

class AdminPageVerification():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__verification = Verification(page)

    def on_page(self) -> bool:
        logging.debug("Verifying we are on Admin Sign In page...")
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_on_administrator_sign_in_page()\' method")
        return self.__page.spice.signIn.is_on_administrator_sign_in_page()