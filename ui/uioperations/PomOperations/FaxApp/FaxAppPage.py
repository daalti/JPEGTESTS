import logging

from ..SignInApp.Page import Page
from .Components.FaxPageVerification import FaxPageVerification
from ..SignInApp.Components.Button import Button
from ..MainApp.Locators import Locators as MainAppLocators
from .Locators import Locators

class FaxAppPage(Page):
    def __init__(self, spice):
        super(FaxAppPage, self).__init__(spice)
        self.verify = FaxPageVerification(self)
        self.__fax_home_button = Button(self, Locators.FaxHomeButton)
        self.__fax_setup_skip_button = Button(self, Locators.FaxSetupSkipButton)
        self.__fax_setup_continue_button = Button(self, Locators.FaxSetupContinueButton)
        self.__fax_configure_button = Button(self, Locators.FaxConfigureButton)
        self.__fax_configure_cancel_button = Button(self, Locators.FaxConfigureCancelButton)
        self.__fax_confirm_cancel_button = Button(self, Locators.FaxConfirmCancelButton)

    def click_fax_setup_skip_button(self) -> bool:
        logging.debug(f"Clicking Fax Setup Skip Button: {self.__fax_setup_skip_button.locator}")
        return self.__fax_setup_skip_button.click()

    def click_fax_setup_continue_button(self) -> bool:
        logging.debug(f"Clicking Fax Setup Continue Button: {self.__fax_setup_continue_button.locator}")
        return self.__fax_setup_continue_button.click()
    
    def click_fax_setup_configure_button(self) -> bool:
        logging.debug(f"Clicking Fax Configure Button: {self.__fax_configure_button.locator}")
        return self.__fax_configure_button.click()
    
    def click_fax_setup_configure_cancel_button(self) -> bool:
        logging.debug(f"Clicking Fax Configure Cancel Button: {self.__fax_configure_cancel_button.locator}")
        return self.__fax_configure_cancel_button.click()

    def click_home_button(self) -> bool:
        logging.debug(f"Clicking Fax Home Button: {self.__fax_home_button.locator}")
        return self.__fax_home_button.click()

    def click_fax_setup_confirm_cancel_button(self):
        logging.debug(f"Clicking Fax Confirm Cancel Button: {self.__fax_confirm_cancel_button.locator}")
        return self.__fax_confirm_cancel_button.click()