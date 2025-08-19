import logging

from ...SignInApp.Page import Page
from ..Locators import Locators
from ...SignInApp.Components.Verification import Verification

class MenuPageVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page

    def on_page(self, timeout:float = Page.DEFAULT_TIMEOUT) -> bool:
        logging.debug("Verifying we are on Menu page...")
        return self.__verification.verify(Locators.ui_menu_app, False, timeout)