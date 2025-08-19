import logging

from enum import Enum
from ...SignInApp.Page import Page
from ...SignInApp.Components.Button import Button
from .DateAndTimeTab import DateAndTimeTab
from .DisplayTab import DisplayTab
from .DisplayTabS import DisplayTabS
from ..Locators import Locators

class GeneralTab():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__display = None
        self.__display_button = Button(page, Locators.display_button)
        self.date_and_time_tab = DateAndTimeTab(page)
        
    @property
    def display(self):
        if self.__display == None:
            self.__display = self.__get_display_tab()
        return self.__display

    def __get_display_tab(self):
        logging.info(f"UI Size: {self.__page.spice.uisize}")
        if self.__page.spice.uitype in ["Workflow", "Workflow2"]:
            if self.__page.spice.uisize == "XS":
                return DisplayTabS(self.__page)
            if self.__page.spice.uisize == "S":
                return DisplayTabS(self.__page)
            if self.__page.spice.uisize == "L":
                # Create New 'DisplayTabL' class
                return DisplayTab(self.__page)
            if self.__page.spice.uisize == "XL":
                return DisplayTab(self.__page)

    def click_display(self) -> bool:
        logging.info("Clicking Display")
        return self.__display_button.click()

    