import logging

from enum import Enum
from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
#from ..MenuApp.Components.MenuPageVerification import MenuPageVerification
from .Locators import Locators

class ToolsAppPage(Page):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        #self.verify = 
        self.__spice = spice
        self.__home_button = Button(self, Locators.home_button)
        self.__service_tab_button = Button(self, Locators.service_app_button)

    def click_home_button(self) -> None:
        logging.info("Clicking Home button")
        return self.__home_button.click()

    def click_service(self) -> bool:
        return self.__service_tab_button.click()
    
