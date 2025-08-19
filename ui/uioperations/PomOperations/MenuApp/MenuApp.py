import logging

from enum import Enum
from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
from .Components.MenuPageVerification import MenuPageVerification
from .Locators import Locators
from .Menu import Menu

class MenuApp(Page, Menu):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        logging.info(f"MenuApp Product Type: {spice.uitype}, Size: {spice.uisize}")
        self.verify = MenuPageVerification(self)
        self.__settings_app_button = Button(self, Locators.settings_app_button)
        self.__quicksets_app_button = Button(self, Locators.quickets_app_button)

    def goto_settings_app(self) -> bool:
        logging.info("Navigating to Setttings app")
        return self.__settings_app_button.click()

    def goto_quicksets_app(self) -> bool:
        logging.info("Navigating to Quicksets app")
        return self.__quicksets_app_button.click()