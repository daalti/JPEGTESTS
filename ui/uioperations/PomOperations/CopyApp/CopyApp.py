import logging

from ..SignInApp.Page import Page
from .CopyAppVerification import CopyAppVerification
from ..SignInApp.Components.Button import Button
from .Locators import Locators

class CopyApp(Page):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        self.verify = CopyAppVerification(self)
        self.__copy_home_button = Button(self, Locators.home_button_clickable)

    def click_home_button(self) -> bool:
        logging.debug(f"Clicking Copy Home Button: {self.__copy_home_button.locator}")
        return self.__copy_home_button.click()

