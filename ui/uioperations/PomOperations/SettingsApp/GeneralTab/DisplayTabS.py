
import logging

from ...SignInApp.Page import Page
from ...SignInApp.Components.Button import Button
from ...SignInApp.Components.TextComboBox import TextComboBox
from ..Locators import Locators
from .Display import Display
from enum import Enum

import time

class DisplayTabS():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__inactivity_timeout_button = Button(page, Locators.inactivity_timeout_combo_box + " #mouseArea") #TextComboBox(page, Locators.inactivity_timeout_combo_box, Locators.inactivity_timeout_combo_box_scroll_bar, "", Locators.inactivity_timeout_pop_up_list)

    def __scroll_to_app(self, locator:str) -> bool:
        height = self.__page.get_locator_attribute(Locators.display_tab_scroll_bar, self.__page.Attribute.Height)
        locator_height = self.__page.get_locator_attribute(locator, self.__page.Attribute.Height)
        return self.__page.scroll_vertical(Locators.display_tab_scroll_bar, locator, height - locator_height)

    def click_inactivity_timeout(self) -> bool:
        logging.info("Clicking Inactivity Timeout...")
        self.__page.wait_for_element(Locators.inactivity_timeout_combo_box)
        if self.__scroll_to_app(Locators.inactivity_timeout_combo_box) == False:
            logging.error(f"Failed to scroll to: {Locators.inactivity_timeout_combo_box}")
            return False
        return self.__inactivity_timeout_button.click()
    
    def select_inactivity_timeout(self, inactivity_timeout:Display.InactivityTimeout) -> bool:
        locator = Display.inactivity_timeout_string_to_element_locator(inactivity_timeout)
        return self.__page.wait_and_click(locator + " #mouseArea")
