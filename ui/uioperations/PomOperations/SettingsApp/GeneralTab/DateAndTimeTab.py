import logging

from ...SignInApp.Page import Page
from ...SignInApp.Components.Button import Button
from .TimeZoneTab import TimeZoneTab
from ..Locators import Locators

class DateAndTimeTab():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__date_and_time_button = Button(page, Locators.date_and_time_button)
        self.time_zone_tab = TimeZoneTab(page)

    def select(self) -> bool:
        logging.info("Selecting Date and Time Tab")
        return self.__date_and_time_button.click()