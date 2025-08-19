import logging
import time

from enum import Enum
from typing import Any
from dunetuf.qmltest.QmlTestServer import QmlTestServerItem, QmlTestServerError

class Page(object):
    """Default wait time in seconds"""
    DEFAULT_TIMEOUT: float = 15

    class Attribute(str, Enum):
        Enabled = "enabled"
        Visible = "visible"
        ActiveFocus = "activeFocus"
        Width = "width"
        Height = "height"
        CumulativeWidthDock = "cumulativeWidthDock"
        X = "x"
        Y = "y"
        AcceptedMouseButtons = "acceptedMouseButtons"
        Text = "text"
        DisplayText = "displayText"
        State = "state"
        Error = "error"
        EchoMode = "echoMode"
        ShowSignIn = "showSignIn"

    def __init__(self, spice) -> None:
        self.spice = spice

    def __wait_until(self, element:QmlTestServerItem, attribute:Attribute, value_to_wait_for, timeout:float = DEFAULT_TIMEOUT) -> bool:
        logging.debug(f"Attempting to wait until attribute \'{attribute}\' is equal to \'{value_to_wait_for}\'")
        logging.debug(f"Verifying element contains attribute key \'{attribute}\'...")
        try:
            value = element[attribute.value]
        except KeyError:
            logging.error(f"Element has no attribute \'{attribute}\'")
            return False
        logging.debug(f"Verifying element attribute \'{attribute}\' is equal to \'{value_to_wait_for}\'...")
        try:
            self.spice.wait_until(lambda: element[attribute.value] == value_to_wait_for, timeout)
        except Exception as exception:
            logging.error(f"Element attribute \'{attribute}\' not equal to \'{value_to_wait_for}\' after {timeout} seconds")
            logging.debug(f"Exception: {exception}")
            return False
        logging.debug(f"Element attribute \'{attribute}\' is equal to: \'{element[attribute.value]}\'.")
        return True

    def __reset_scroll_bar(self, scroll_bar_locator:str) -> QmlTestServerItem:
        scroll_bar = self.wait_for_element(scroll_bar_locator)
        if scroll_bar == None: return None
        logging.debug("Setting Scroll Bar position to 0")
        if self.set_item_and_wait_for_completion(scroll_bar, "position", 0) == False: return None
        return scroll_bar
    
    def __locator_exists(self, expected_view_locator:str, verify_active_focus:bool = True, timeout = DEFAULT_TIMEOUT) -> bool:
        element = self.wait_for_element(expected_view_locator, timeout=timeout)
        if element == None: return False
        if verify_active_focus == False: return True
        return self.check_element(element, self.Attribute.ActiveFocus, True, timeout)

    def get_locator_attribute(self, locator:str, attribute:Attribute, timeout:float = DEFAULT_TIMEOUT) -> Any:
        logging.debug(f"Attempting to get \'{locator}\' attribute \'{attribute}\' value...")
        element = self.wait_for_element(locator, timeout)
        if element == None: return None
        logging.debug(f"Verifying that attribute \'{attribute}\' is a valid key")
        try:
            value = element[attribute.value]
        except QmlTestServerError:
            logging.error(f"Invalid attribute \'{attribute}\'")
            raise

        logging.debug(f"Locator \'{locator}\' attribute \'{attribute}\' is: {element[attribute.value]}")
        return element[attribute.value]

    def get_item(self, element:QmlTestServerItem, key:str, timeout:float = DEFAULT_TIMEOUT) -> Any:
        item_value = element.__getitem__(key)
        timer = timeout
        while(item_value == None and timer > 0):
            timer -= 1
            time.sleep(1)
            item_value = element.__getitem__(key)
        if item_value == None:
            logging.error(f"Element failed to get \'{key}\' after {timeout} seconds")
            return None
        return item_value

    def set_item_no_wait(self, element:QmlTestServerItem, key:str, value:Any) -> None:
        """
            Sets the items value, but does not wait for the value to be set.
            This is useful because some item values are capped at a certain amount.
            
            For example, scroll bar position values are capped. If you want to scroll to
            position 8.73, the position value may be capped at something like 0.993. Thus,
            setting the value to 8.73 and then getting the value would return 0.993.
        """
        element.__setitem__(key, str(value))
        logging.debug(f"Set item \'{key}\' to value \'{value}\'")
        item_value = element.__getitem__(key)
        logging.debug(f"Item \'{key}\' value after set: {item_value}")

    def set_item_and_wait_for_completion(self, element:QmlTestServerItem, key:str, value:Any, timeout:float = DEFAULT_TIMEOUT) -> bool:
        element.__setitem__(key, str(value))
        item_value = element.__getitem__(key)
        logging.debug(f"Get Item, Key: \'{key}\', Value: \'{item_value}\'")
        timer = timeout
        while(item_value != value and timer > 0):
            timer -= 1
            time.sleep(1)
            item_value = element.__getitem__(key)
            logging.debug(f"Get Item, Key: \'{key}\', Value: \'{item_value}\'")
        if item_value != value:
            logging.error(f"Element failed to set \'{key}\' to \'{value}\' after {timeout} seconds")
            return False
        return True

    def check_locator(self, locator:str, attribute:Attribute, condition:Any, timeout:float = DEFAULT_TIMEOUT) -> bool:
        element = self.wait_for_element(locator, timeout)
        if element == None: return False
        return self.__wait_until(element, attribute, condition, timeout)

    def check_element(self, element:QmlTestServerItem, attribute:Attribute, condition:Any, timeout:float = DEFAULT_TIMEOUT) -> bool:
        return self.__wait_until(element, attribute, condition, timeout)

    def wait_for_element(self, locator:str, timeout:float = DEFAULT_TIMEOUT) -> QmlTestServerItem:
        logging.debug(f"Attempting to get \'{locator}\'...")
        element = None
        try:
            element = self.spice.wait_for(locator, timeout)
        except Exception as e:
            logging.warning(f"Failed to get element \'{locator}\' in {timeout} seconds")
            logging.warning(f"Exception: {e}")
            
        return element

    def query_element(self, locator:str, index:int = 0) -> QmlTestServerItem:
        logging.debug(f"Attempting to query \'{locator}\', index {index}...")
        try:
            element = self.spice.query_item(locator, index)
        except:
            logging.error(f"Failed to query element \'{locator}\' at index {index}")
            return None
        return element

    def wait_and_click(self, locator_button:str, click_center:bool = True, check_enabled:bool = True, timeout:float = DEFAULT_TIMEOUT) -> bool:
        logging.info(f"Attempting to click button \'{locator_button}\'...")
        button = self.wait_for_element(locator_button)
        if button == None: return False
        if check_enabled and self.check_element(button, self.Attribute.Enabled, True, timeout) == False: return False
        if self.check_element(button, self.Attribute.Visible, True, timeout) == False: return False

        """
            NOTE: It is critical that you make sure that the button you are attempting to click is:
                    A. Clickable - check the 'acceptedMouseButtons' property of the element in Gammaray
                    B. In view to be clicked. This method clicks the center of the button. If the
                       button's center is not in view the 'click' will register but nothing will happen.
        """

        if click_center:
            button_width = self.get_locator_attribute(locator_button, self.Attribute.Width)
            button_height = self.get_locator_attribute(locator_button, self.Attribute.Height)
            button_coordinate_x = self.get_locator_attribute(locator_button, self.Attribute.X)
            button_coordinate_y = self.get_locator_attribute(locator_button, self.Attribute.Y)
            center_coordinate_x = button_coordinate_x + (button_width / 2.0)
            center_coordinate_y = button_coordinate_y + (button_height / 2.0)
            button.mouse_click(x=int(center_coordinate_x), y=int(center_coordinate_y))
        else:
            button.mouse_click()

        return True

    def scroll_horizontal(self, scroll_bar_locator:str, scroll_to_locator:str, scroll_area_width:float) -> bool:
        logging.debug(f"Scroll Area Width: {scroll_area_width}")
        scroll_bar = self.__reset_scroll_bar(scroll_bar_locator)
        if scroll_bar == None: return False

        scroll_to_locator_left_x = self.get_locator_attribute(scroll_to_locator, self.Attribute.X)
        if scroll_to_locator_left_x == None: return False
        logging.debug(f"Locator \'{scroll_to_locator}\' left x position: {scroll_to_locator_left_x}")

        scroll_to_locator_width = self.get_locator_attribute(scroll_to_locator, self.Attribute.Width)
        if scroll_to_locator_width == None: return False
        logging.debug(f"Locator \'{scroll_to_locator}\' width: {scroll_to_locator_width}")

        scroll_to_locator_right_x = scroll_to_locator_left_x + scroll_to_locator_width
        logging.debug(f"Locator \'{scroll_to_locator}\' right x position: {scroll_to_locator_right_x}")
        
        if scroll_to_locator_right_x > scroll_area_width:
            """
                If the locator is out of view, then the right_x to scroll area width ratio will
                be greater that 1. We can subtract 1 from the ratio to get a value that is
                between 0 and 1 and scroll to that new ratio.
                Ex. right_x / scroll_area_width = 1.2
                    1.2 - 1 = 0.2
                    Set scroll bar position to 0.2 and the app should be in full view now
            """
            scroll_area_width_to_locator_ratio = (scroll_to_locator_right_x / scroll_area_width) - 1
            logging.debug(f"Locator \'{scroll_to_locator}\' scroll area width to locator ratio: {scroll_area_width_to_locator_ratio}")
            if self.set_item_and_wait_for_completion(scroll_bar, "position", scroll_area_width_to_locator_ratio) == False:
                return False
        else:
            logging.debug(f"Locator \'{scroll_to_locator}\' already in view")
        
        return True

    def scroll_vertical(self, scroll_bar_locator:str, scroll_to_locator:str, scroll_area_height:float) -> bool:
        logging.debug(f"Scroll Area Height: {scroll_area_height}")
        scroll_bar = self.__reset_scroll_bar(scroll_bar_locator)
        if scroll_bar == None: return False

        scroll_to_locator_top_y = self.get_locator_attribute(scroll_to_locator, self.Attribute.Y)
        if scroll_to_locator_top_y == None: return False
        logging.debug(f"Locator \'{scroll_to_locator}\' top y position: {scroll_to_locator_top_y}")

        scroll_to_locator_height = self.get_locator_attribute(scroll_to_locator, self.Attribute.Height)
        if scroll_to_locator_height == None: return False
        logging.debug(f"Locator \'{scroll_to_locator}\' height: {scroll_to_locator_height}")

        scroll_to_locator_bottom_y = scroll_to_locator_top_y + scroll_to_locator_height
        logging.debug(f"Locator \'{scroll_to_locator}\' bottom y position: {scroll_to_locator_bottom_y}")

        if scroll_to_locator_bottom_y > scroll_area_height:
            scroll_area_height_to_locator_ratio = (scroll_to_locator_bottom_y/ scroll_area_height) - 1
            logging.debug(f"Locator \'{scroll_to_locator}\' scroll area height to locator ratio: {scroll_area_height_to_locator_ratio}")
            self.set_item_no_wait(scroll_bar, "position", scroll_area_height_to_locator_ratio)
            if self.get_item(scroll_bar, "position") == 0:
                return False
        else:
            logging.debug(f"Locator \'{scroll_to_locator}\' already in view")

        return True

    def scroll_right_increment(self, element, amount:int = 1):
        for _ in range(amount):
            try:
                element.mouse_wheel(180, 180)
            except Exception as exception:
                logging.error(f"Failed to scroll right. Caught exception:\n{exception}")
                return False
        return True

    def scroll_left_increment(self, element, amount:int = 1):
        for _ in range(amount):
            try:
                element.mouse_wheel(0, 0)
            except Exception as exception:
                logging.error(f"Failed to scroll left. Caught exception:\n{exception}")
                return False
        return True

    def compare_locator_text(self, locator:str, expected_text:str) -> bool:
        """
            Gets the 'locator' 'Text' attribute and compares it to the 'expected_text' string.
            If 'locator' does not exist, returns False.
            If 'locator' has no 'Text' attribute, returns False.
            If 'locator' 'Text' attribute is not equal to 'expected_text', returns False.
        """
        if self.__locator_exists(locator, verify_active_focus=False, timeout=20) == False:
            logging.error(f"Failed to find locator \'{locator}\'")
            return False
        text = self.get_locator_attribute(locator, self.Attribute.Text)
        if text == None:
            logging.warning("Failed to get locator 'Text' attribute. Locator may not have 'Text' attribute.")
            return False
        if text != expected_text:
            logging.error(f"Locator Text is \'{text}\', but we expected \'{expected_text}\'")
            return False
        logging.debug(f"Locator Text: {text}")
        return True