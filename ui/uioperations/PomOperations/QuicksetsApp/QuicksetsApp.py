import logging

from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
from .Locators import Locators

class QuicksetsApp(Page):
    def __init__(self, spice) -> None:
        super().__init__(spice)
        self.__copy_list_button = Button(self, Locators.copy_list_quickset_button)
        self.__home_button = Button(self, Locators.home_button)
    
    def select_copy_quicksets(self) -> bool:
        logging.info("Selecting Copy Quicksets")
        return self.__copy_list_button.click()
    
    def select_quickset(self, quickset_name:str) -> bool:
        logging.info("Clicking first Copy Quickset")
        return self.wait_and_click(Locators.copy_list_row_quickset_button.format(quickset_name), click_center=True)

    def click_home_button(self) -> bool:
        return self.__home_button.click()