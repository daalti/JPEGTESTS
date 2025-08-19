import logging

from enum import Enum
from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
#from .Components.
from ..MenuApp.Components.MenuPageVerification import MenuPageVerification
from .Locators import Locators
from .GeneralTab.GeneralTab import GeneralTab

class SettingsAppPage(Page):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        #self.verify = 
        self.__spice = spice
        self.__general = None
        self.__general_tab_button = Button(self, Locators.general_tab_button)
        self.__home_button = Button(self, Locators.home_button)
    
    @property
    def general(self):
        if self.__general == None:
            self.__general = GeneralTab(self)
        return self.__general

    def click_home_button(self) -> None:
        logging.info("Clicking Home button")
        return self.__home_button.click()

    def click_general(self) -> bool:
        return self.__general_tab_button.click()
    
    def click_network(self):
        pass

    def click_print(self):
        pass
