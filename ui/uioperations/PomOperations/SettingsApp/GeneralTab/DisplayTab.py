import logging

from ...SignInApp.Page import Page
from ...SignInApp.Components.Button import Button
from ...SignInApp.Components.TextComboBox import TextComboBox
from ..Locators import Locators
from .Display import Display
from enum import Enum

import time

class DisplayTab(Display):
    class InactivityTimeout(str, Enum):
        Timeout30Seconds = "30 Seconds"
        Timeout1Minute = "1 Minute"
        Timeout2Minutes = "2 Minutes"
        Timeout5Minutes = "5 Minutes"

    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__inactivity_timeout_combo_box = TextComboBox(page, Locators.inactivity_timeout_combo_box, Locators.inactivity_timeout_combo_box_scroll_bar, "", Locators.inactivity_timeout_pop_up_list)

    def _select_item(self, inactivity_timeout:InactivityTimeout) -> bool:
        current_text = self.__inactivity_timeout_combo_box.get_selected_text()
        if current_text == inactivity_timeout.value:
            logging.debug(f"Textbox item is already set to \'{inactivity_timeout.value}\'")
            return True
        if not self.__inactivity_timeout_combo_box.has_multiple_items():
            logging.warning(f"This is a single item combo box. There is only one item. Item is \'{current_text}\'")
            return False
        
        popup_list_element = self.__page.wait_for_element(self.__inactivity_timeout_combo_box.popup_list_locator)
        if popup_list_element == None:
            logging.error(f"No combobox popup list exists, \'{self.__inactivity_timeout_combo_box.popup_list_locator}\'")
            return False

        item_locator = Display.inactivity_timeout_string_to_element_locator(inactivity_timeout)
        item_element = self.__page.wait_for_element(item_locator)
        if item_element == None:
            logging.error(f"No item element matching \'{item_locator}\'")
            return False

        height = self.__page.get_locator_attribute(self.__inactivity_timeout_combo_box.popup_list_locator, self.__page.Attribute.Height)

        if self.__page.scroll_vertical(self.__inactivity_timeout_combo_box.combo_box_scroll_bar_locator, item_locator, height) == False:
            logging.error(f"Failed to scroll to \'{item_locator}\'")
            return False

        if self.__page.wait_and_click(item_locator + " #mouseArea") == False:
            logging.error(f"Failed to click \'{item_locator + ' #mouseArea'}\'")
            return False

        # Wait for popup list to disappears after selecting an item
        popup_list_element = self.__page.wait_for_element("#SettingsSpiceComboBoxpopupList")
        timeout = self.__page.DEFAULT_TIMEOUT
        while(popup_list_element != None and timeout > 0):
            popup_list_element = self.__page.wait_for_element("#SettingsSpiceComboBoxpopupList")
            timeout -= 1
            time.sleep(1)
            
        if popup_list_element != None:
            logging.error(f"Combo Box Pop Up List is still visible after selecting an item.")
            return False
        
        return True
    
    def click_inactivity_timeout(self) -> bool:
        logging.info("Clicking Inactivity Timeout Combo Box...")
        return self.__inactivity_timeout_combo_box.click_combo_box()
    
    def select_inactivity_timeout(self, inactivity_timeout:InactivityTimeout) -> bool:
        if self.click_inactivity_timeout() == False: return False

        current_selected_text = self.__inactivity_timeout_combo_box.get_selected_text()
        if current_selected_text == inactivity_timeout.value:
            logging.info(f"Current Inactivity Timeout is already {inactivity_timeout.value}")
            logging.info(f"Collapsing Combo Box")
            return self.click_inactivity_timeout_combo_box()
        return self._select_item(inactivity_timeout)

