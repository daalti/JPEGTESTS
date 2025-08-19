import logging

from .Page import Page
from .Components.SignIn import SignIn
from ..MainApp.Locators import Locators as MainAppLocators
from ..StatusCenterApp.Locators import Locators as StatusCenterLocators


class UniversalSignInWrapper(Page):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        self.__spice = spice
        self.__sign_in = self.__get_valid_sign_in_app()
    
    def __get_valid_sign_in_app(self) -> SignIn:

        sign_in_button = self.wait_for_element(MainAppLocators.persistent_sign_in_button,timeout=20)
        if sign_in_button != None:
            return self.__spice.home_app

        sign_out_button = self.wait_for_element(MainAppLocators.persistent_sign_out_button,timeout=20)
        if sign_out_button != None:
            return self.__spice.home_app

        home_page_sign_in_button = self.wait_for_element(MainAppLocators.sign_in_app_button, timeout=20)
        if home_page_sign_in_button != None:
            return self.__spice.home_app

        status_center_bar = self.wait_for_element(StatusCenterLocators.ClickableStatusCenterBar, timeout=20)
        if status_center_bar != None:
            return self.__spice.status_center_app

        if self.__spice.uitype == "ProSelect":
            return self.__spice.home_app_pro_select
			
        assert False, logging.error("UniversalSignInWrapper found no way to sign in")

    def goto_sign_in_app(self) -> bool:
        return self.__sign_in.goto_sign_in_app()

    def sign_out(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_universal_sign_out_from_home()\' method")
        return self.__spice.signIn.select_universal_sign_out_from_home()
    
    def is_signed_in(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_signed_in()\' method")
        return self.__spice.signIn.is_signed_in()

    