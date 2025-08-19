import logging

from ...SignInApp.Page import Page
from ...SignInApp.Components.Button import Button
#from .Components.
from ..Locators import Locators

class TimeZoneTab():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__time_zone_button = Button(page, Locators.time_zone_tab_button)

    def select(self) -> bool:
        logging.info("Selecting Time Zone Tab")
        return self.__time_zone_button.click()