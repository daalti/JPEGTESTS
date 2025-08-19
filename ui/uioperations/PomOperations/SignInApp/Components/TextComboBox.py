import logging
import time
from ..Page import Page

"""
    If a Combo Box has 1 item, then it's a Text Field.
    If a Combo Box has more than 1 item, then it's a Combo Box that can be clicked
"""

class TextComboBox():
    def __init__(self, page:Page, combo_box_locator:str, combo_box_scroll_bar_locator:str, text_field:str, popup_list_locator:str = None) -> None:
        self.__page:Page = page
        self.text_field:str = text_field # The element that is holding the currently selected combo box item text
        self.combo_box_locator:str = combo_box_locator # The locator of the entire combo box
        self.combo_box_scroll_bar_locator:str = combo_box_scroll_bar_locator # The scroll bar child element of the combo box
        self.popup_list_locator:str = popup_list_locator # Used if the combo_box_locator and popup_list_locator don't have the same naming convension

    def get_item_count(self) -> int:
        pass

    def get_selected_text(self) -> str:
        locator = self.combo_box_locator + " #control SpiceText[visible=true]"
        text = self.__page.get_locator_attribute(locator, self.__page.Attribute.Text)
        if text == None:
            logging.error(f"Failed to get \'{self.__page.Attribute.Text}\' attribute from \'{locator}\'")
            
        return text

    def has_multiple_items(self) -> bool:
        return self.__page.check_locator(self.combo_box_locator, self.__page.Attribute.Visible, True)

    def click_combo_box(self) -> bool:
        if not self.has_multiple_items():
            logging.warning("This is a single item combo box. It can not be clicked.")
            return False
        locator = self.combo_box_locator + " #control"
        return self.__page.wait_and_click(locator)

    def select_item(self, item_text:str) -> bool:
        """
            popup_list_locator:str - Used if the 
        """
        current_text = self.get_selected_text()
        if current_text == item_text:
            logging.debug(f"Textbox item is already set to \'{item_text}\'")
            return True
        if not self.has_multiple_items():
            logging.warning(f"This is a single item combo box. There is only one item. Item is \'{current_text}\'")
            return False
        
        if self.popup_list_locator == None:
            self.popup_list_locator = self.combo_box_locator + "popupList"
        popup_list_element = self.__page.wait_for_element(self.popup_list_locator)
        if popup_list_element == None:
            logging.debug(f"Combobox Popup List does not exis \'{self.popup_list_locator}\'. Attempting to click combobox drop down...")
            if self.click_combo_box() == False:
                logging.error("No combobox popup list exists. Failed to click combo box drop down.")
                return False
            else:
                popup_list_element = self.__page.wait_for_element(self.popup_list_locator)

        if popup_list_element == None:
            logging.error(f"No combobox popup list exists, \'{self.popup_list_locator}\'")
            return False

        item_locator = self.combo_box_locator + "Item_" + item_text
        item_element = self.__page.wait_for_element(item_locator)
        if item_element == None:
            logging.error(f"No item element matching \'{item_locator}\'")
            return False

        height = self.__page.get_locator_attribute(self.popup_list_locator, self.__page.Attribute.Height)

        if self.__page.scroll_vertical(self.combo_box_scroll_bar_locator, item_locator, height) == False:
            logging.error(f"Failed to scroll to \'{item_locator}\'")
            return False

        if self.__page.wait_and_click(item_locator + " #mouseArea") == False:
            logging.error(f"Failed to click \'{item_locator + ' #mouseArea'}\'")
            return False

        # Verify popup list disappears after selecting an item
        counter = 0
        popup_list_element = self.__page.wait_for_element(self.popup_list_locator, timeout=1)
        while popup_list_element != None and counter < 3:
            popup_list_element = self.__page.wait_for_element(self.popup_list_locator, timeout=1)
            time.sleep(1)
            counter += 1

        if popup_list_element != None:
            logging.error(f"Combo Box Pop Up List is still visible after selecting an item.")
            return False
        
        return True
