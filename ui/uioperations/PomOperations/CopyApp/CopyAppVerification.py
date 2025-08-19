from .Locators import Locators
from ..SignInApp.Components.Verification import Verification
from ..SignInApp.Page import Page

import logging

class CopyAppVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page
    
    def on_page(self) -> bool:
        logging.debug("Verifying we are on Copy App page...")
        return self.__verification.verify(Locators.ui_copy_app)

