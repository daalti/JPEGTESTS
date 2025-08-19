import logging

from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
from .Components.MenuPageVerification import MenuPageVerification
from .Locators import Locators
from .Menu import Menu

class MenuAppS(Page, Menu):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        self.__spice = spice
        self.__settings_app_button:Button = Button(self, Locators.settings_app_button)
        self.__tools_app_button = Button(self, Locators.tools_app_button)
        self.verify = MenuPageVerification(self)
    
    def __scroll_to_app(self, locator:str) -> bool:
        height = self.get_locator_attribute(Locators.menu_scroll_bar, self.Attribute.Height)
        return self.scroll_vertical(Locators.menu_scroll_bar, locator, height)
    
    def goto_settings_app(self) -> bool:
        logging.info("Navigating to Setttings app")
        if self.__scroll_to_app(Locators.settings_app) == False:
            logging.error(f"Failed to scroll to: {self.__settings_app_button.locator}")
            return False
        return self.__settings_app_button.click()
    
    def goto_tools_app(self) -> bool:
        logging.info("Navigating to Tools app")
        if self.__scroll_to_app(Locators.tools_app) == False:
            logging.error(f"Failed to scroll to: {self.__tools_app_button.locator}")
            return False
        return self.__tools_app_button.click()

    