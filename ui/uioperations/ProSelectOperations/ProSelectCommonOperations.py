#########################################################################################
# @file      ProSelectCommonOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      19-10-2020
# @brief     Common UI dial methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
import time
import logging
import pytest
from typing import Any
from dunetuf.ui.uioperations.BaseOperations.IProSelectCommonOperations import IProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.qmltest.QmlTestServer import QmlTestServerItem, QmlTestServerError

alpha_numeric_keys = {
    "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
    "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23,
    "x": 24, "y": 25, "z": 26, "0": 27, "1": 28, "2": 29, "3": 30, "4": 31, "5": 32, "6": 33, "7": 34,
    "8": 35, "9": 36, "!": 37, "\"": 38, "#": 39, "$": 40, "%": 41, "&": 42, "'": 43, "(": 44, ")": 45,
    "*": 46, "+": 47, ",": 48, "-": 49, ".": 50, "/": 51, ":": 52, "[": 53, "]": 54, "\\": 55, "^": 56, "_": 57,
    "`": 58, ";": 59, "<": 60, "=": 61, ">": 62, "?": 63, "@": 64, "{": 65, "|": 66, "}": 67, "~": 68
}
icon_keys = {
    "spacebar": 69, "done": 70, "backspace": 71, "language": 72, "shift_off": 73, "symbols": 74, "alphabet": 75, "numeric": 76,
}

_logger = logging.getLogger(__name__)

class ProSelectCommonOperations(IProSelectCommonOperations):
    SCAN_APP = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32"
    DEFAULT_WAIT_TIME_SECONDS:float = 15.0

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        self.maxtimeout = 120
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)
    
    def get_element(self, locator:str, timeout:float = DEFAULT_WAIT_TIME_SECONDS) -> QmlTestServerItem:
        logging.debug(f"Attempting to get '{locator}' ...")
        element = None
        try:
            element = self._spice.wait_for(locator, timeout)
        except:
            logging.warning(f"Failed to get element '{locator}' in {timeout} seconds")
            
        return element
    
    def query_element(self, locator:str, index:int = 0, timeout:float = DEFAULT_WAIT_TIME_SECONDS) -> QmlTestServerItem:
        logging.debug(f"Attempting to query \'{locator}\', index {index}...")
        try:
            element = self._spice.query_item(locator, index)
        except:
            logging.warning(f"Failed to query element '{locator}' at index {index}")
            raise
        return element
    
    def get_element_property(self, element:QmlTestServerItem, property:str) -> Any:
        """
            Gets the given element's property value.
            Raises QmlTestServerError if property doesn't exist on element
        """
        logging.debug(f"Attempting to get element '{element.get_name()}' property '{property}'")
        logging.debug(f"Verifying that property '{property}' is a valid")
        try:
            value = element[property]
        except QmlTestServerError:
            logging.error(f"Invalid property '{property}' on element '{element.get_name()}'")
            raise

        logging.debug(f"Element \'{element}\' property \'{property}\' is: {value}")
        return value

    def set_element_property(self, element:QmlTestServerItem, property:str, value, timeout:float = DEFAULT_WAIT_TIME_SECONDS) -> bool:
        """
            Sets the given element's property value and waits for the property to update to the 'value' specified.
            Returns False if it fails to update the property value.
            
            NOTE: UI element property values don't update immediately, so waiting is neccessary.
            NOTE: UI element property values that are float or int can be clamped at a certain value.
            Ex. If we set a 'scroll_bar' UI element property 'position' to '1.2', it's possible that
            the 'position' value is clamped to a max of '1.0'. So if we were to wait for the property
            to update to '1.2' it would never happen because the property value is being clamped to '1.0'.
            This is why we return False "if item_value != value and item_value == original_value".
        """
        original_value = self.get_element_property(element, property)
        if original_value == value: return True
        try:
            element.__setitem__(property, value)
        except QmlTestServerError:
            raise
        item_value = self.get_element_property(element, property)
        logging.info(f"Property '{property}' after set: {item_value}. Expected set value: {value}")
        timer = timeout
        while(item_value != value and timer > 0):
            timer -= 1
            time.sleep(1)
            item_value = self.get_element_property(element, property)
        if item_value != value and item_value == original_value:
            logging.error(f"Failed to set element '{element.get_name()}' property '{property}' to '{value}' within {timeout} seconds")
            logging.error(f"Current Value: {item_value}")
            return False
        return True

    def click(self, button_element:QmlTestServerItem, click_center:bool = True) -> bool:
        """
            Clicks the center of the given button element.
            Return True if button was visible and enabled.
            NOTE: It is critical that you make sure that the button you are attempting to click is:
                    A. Clickable - check the 'acceptedMouseButtons' property of the element in Gammaray.
                    B. In view to be clicked. This method clicks the center of the button. If the
                       button's center is not in view the 'click' will register but nothing will happen.
        """
        logging.info(f"Attempting to click button '{button_element}'...")
        if not button_element.is_visible():
            logging.error(f"Button '{button_element.get_name()}' is not visible")
            return False
        if not button_element.is_enabled():
            logging.error(f"Button '{button_element.get_name()}' is not enabled")
            return False

        if click_center:
            button_width = self.get_element_property(button_element, "width")
            button_height = self.get_element_property(button_element, "height")
            button_coordinate_x = self.get_element_property(button_element, "x")
            button_coordinate_y = self.get_element_property(button_element, "y")
            center_coordinate_x = button_coordinate_x + (button_width / 2.0)
            center_coordinate_y = button_coordinate_y + (button_height / 2.0)
            button_element.mouse_click(x=center_coordinate_x, y=center_coordinate_y)
        else:
            button_element.mouse_click()

        return True

    def goto_item(self, menu_item_id, screen_id="#MenuListLayout", dial_value: int = 180, select_option: bool = True):
        '''
        This method searches and clicks a specified button on a specified menu
        Args:
            menu_item_id: Object Id of the menu item to be pressed
            screen_id: Object Id of the screen
            dial_value: Direction for dialing
            select_option: Select True to click on the element
        '''
        current_screen = self._spice.wait_for(screen_id)
        self._spice.wait_for(menu_item_id)
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        # Search for item in menu (down - 180, up - 0)
        while (self._spice.query_item(menu_item_id)["activeFocus"] == False and time_spent_waiting < self.maxtimeout):
            current_screen.mouse_wheel(dial_value, dial_value)
            time_spent_waiting = time.time() - start_time
        time.sleep(1)

        if (self._spice.query_item(menu_item_id)["activeFocus"] == False):
            # Search for item in reverse direction
            if (dial_value == 180):
                dial_value = 0
            else:
                dial_value = 180

            current_screen = self._spice.wait_for(screen_id)
            start_time = time.time()
            time_spent_waiting = time.time() - start_time
            while (self._spice.query_item(menu_item_id)["activeFocus"] == False and time_spent_waiting < self.maxtimeout):
                current_screen.mouse_wheel(dial_value, dial_value)
                time_spent_waiting = time.time() - start_time
            time.sleep(1)

        if select_option == True:
            current_button = self._spice.query_item(menu_item_id + " SpiceText")
            current_button.mouse_click()
            logging.info("At Expected Menu")
        time.sleep(1)

    def back_button_press(self, screen_id, landing_view, index: int = 0, timeout_val: int = 60):
        '''
        Press back button in specific screen.
        Args:
          screen_id: Screen object id
          landing_view: Landing screen after pressing back button
          index: Query index for the ui item
          timeout_val: Time out for scrolling
        '''
        current_screen = self._spice.wait_for(screen_id)

        if self._spice.uitheme == "hybridTheme":
            logging.info("Using Keyhandler UDW command for BACK Button: Hybrid UI")
            self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")

        else:
            start_time = time.time()
            time_spent_waiting = time.time() - start_time
            while (self._spice.query_item("#BackButton", index)["activeFocus"] == False and time_spent_waiting < timeout_val):
                current_screen.mouse_wheel(0, 0)
                time_spent_waiting = time.time() - start_time
            time.sleep(1)

            # assert self._spice.query_item("#BackButton", index)["activeFocus"] == True, "Back button is not in focus"

            current_button = self._spice.query_item("#BackButton SpiceText", index)
            current_button.mouse_click()
        
        time.sleep(1)
        assert self._spice.wait_for(landing_view)
        # time.sleep(1)
    
    def back_or_close_button_press(self, close_or_back_button, landing_view):
        '''
        Press back/close button in specific screen.
        Args:
          close_or_back_button: close/back button object name
          landing_view: Landing screen after pressing back button
        '''
        if self._spice.ui_theme() == "hybridTheme":
            logging.info("Using Keyhandler UDW command for BACK Button: Hybrid UI")
            self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")
        else:
            back_or_close_button = self._spice.wait_for(close_or_back_button)
            back_or_close_button.mouse_click()
            self._spice.wait_for(landing_view)
            time.sleep(3)
            logging.info("At: " + landing_view)

    def goto_sub_menu(self, current_screen, sub_menu_item_id, select_option: bool = True):
        '''
        Method to go to sub menu from main menu.
        Args:
            current_screen: Object Id of sun menu view screen
            sub_menu_item_id: Object Id of the item to be clicked in the sub menu.
        '''
        currentScreen = self._spice.wait_for(current_screen)
        time.sleep(1)
        # enable item from ui
        while (self._spice.query_item(sub_menu_item_id)["activeFocus"] == False):
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self._spice.query_item(sub_menu_item_id)["activeFocus"] == True
        currentButton = self._spice.wait_for(sub_menu_item_id + " SpiceText")
        if select_option == True:
            currentButton.mouse_click()
            time.sleep(2)

    def verify_help_content(self, net, spice, buttonObjectId, stringIdList, menuLevelList: list = [0], language: str = "English"):
        # validate the back button functionality
        currentElement = spice.query_item("#BackButton SpiceText")
        currentElement.mouse_click()
        logging.info("Back button works as expected.")
        time.sleep(1)

        # navigate back to the help screen
        currentElement = spice.query_item(buttonObjectId + " SpiceText")
        currentElement.mouse_click()
        time.sleep(1)

        # verify the help content by comparing the ui content with the stringId in the specification
        spice.homeMenuUI().compare_string(net, spice, "#Version2Text", stringIdList, menuLevelList, "English")

        # validate the OK button functionality
        spice.homeMenuUI().menu_navigation(spice, "#MenuListLayout", "#OK")

        # check if the navigation is accurate
        assert spice.query_item(buttonObjectId + " SpiceText")
        logging.info("OK button works as expected.")

    def get_expected_translation_str_by_str_id(self, net, str_id, locale: str = "en-US"):
        logging.info("To get expected str of {str_id}")
        expected_translation_str = LocalizationHelper.get_string_translation(net, str_id, locale)
        logging.info(f"The expected str of str id__{locale}: {str_id} is: {expected_translation_str}")
        return expected_translation_str

    def get_actual_str(self, object_name):
        logging.info(f"To get actual str of {object_name}")
        item = self._spice.wait_for(object_name)
        self._spice.wait_until(lambda: item["visible"] is True, 20)
        actual_str = self._spice.query_item(object_name + " SpiceText")["text"]
        logging.info(f"The actual str of object name: {object_name} is: {actual_str}")
        return actual_str

    def verify_string(self, net, str_id, object_name, locale: str = "en-US"):
        expected_translation_str = self.get_expected_translation_str_by_str_id(net, str_id, locale)
        actual_str = self.get_actual_str(object_name)
        assert expected_translation_str == actual_str

    # Scan App
    def goto_scan_app(self):
        '''
        UI should be in Homescreen
        Navigates to Scan App screen starting from Home screen.
        UI Flow is Home->Scan
        '''
        # Uncomment once bug on homescreen activefocus DUNE-35036 is fixed
        # self._spice.goto_homescreen()
        home_app = self._spice.query_item("#HomeScreenView")
        #self._spice.wait_until(lambda: home_app["activeFocus"] == True)
        logging.info("At Home Screen")
        start_time = time.time()
        time_spent_waiting = time.time() - start_time

        # make sure that you are in left most App - Menu
        while (self._spice.query_item("#CurrentAppText")["text"] != "Menu" and time_spent_waiting < self.maxtimeout):
            home_app.mouse_wheel(0, 0)
            time_spent_waiting = time.time() - start_time
        time.sleep(2)
        # scroll till you reach the Scan option (TODO - Need to avoid use of text)
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (self._spice.query_item("#CurrentAppText")["text"] != "Scan" and time_spent_waiting < self.maxtimeout):
            home_app.mouse_wheel(180, 180)
            time_spent_waiting = time.time() - start_time
        time.sleep(2)

        current_button = self._spice.wait_for(self.SCAN_APP)
        current_button.mouse_click()
        logging.info("At Scan App")
        time.sleep(2)

    '''*********************Network app navigation methods******************** '''
    def goto_settings_menu(self):
        '''
        UI should be on home screen
        Navigate to settings from menu app
        '''
        self._spice.goto_homescreen()
        _logger.info("Entering Menu app")
        self.home_menu_dial_operations.goto_menu(self._spice)
        _logger.info("Looking for Settings")
        time.sleep(5)
        self.goto_item("#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuButton")

    def goto_network_settings_menu(self):
        '''
        UI should on home screen before calling this method
        Navigate to network from settings
        '''
        self.goto_settings_menu()
        _logger.info("Entering Network")
        time.sleep(5)
        self.goto_item("#networkSettingsMenuButton")
        # Sign-in as admin user when prompted at Network app
        try:
            (self._spice.query_item("#DeviceUserView")["visible"])
            self.home_menu_dial_operations.perform_signIn(self._spice)
                
        except:
                logging.info("Already signed in or sign-in not supported ")


    def goto_ethernet_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ethernet from network
        '''
        self.goto_network_settings_menu()
        _logger.info("Entering Ethernet")
        time.sleep(5)
        self.goto_item("#cnxEthernetMenuButton")

    def scroll_item_into_view(self, comboboxpopuplist, scroll_bar, list_item):
        """
        This scroll function is special case for ComboBoxpopupList. And scroll item into view then it can be selected.
        """
        self._spice.wait_for(comboboxpopuplist)
        # wail for all item show
        time.sleep(3)
        content_height = self._spice.wait_for(comboboxpopuplist)["contentHeight"]
        list_item_location = self._spice.wait_for(list_item)["y"]
        pos = list_item_location/content_height
        scrollbar_element = self._spice.wait_for(scroll_bar)
        logging.info(f"Scroll to position: <{pos}>")
        scrollbar_element.__setitem__("position", str(pos))

    def scroll_to(self, view_locator:str, item_locator:str, timeout:float = 30) -> bool:
        view = self.get_element(view_locator)
        if not view: return False

        item = self.get_element(item_locator)
        if not item: return False
        
        # Initial check - see if item already has activeFocus
        if self.get_element_property(item, "activeFocus"):
            return True
        
        # Attempt scrolling
        counter = 0
        while counter < timeout:
            # Check current button state
            item = self.get_element(item_locator)
            if item and self.get_element_property(item, "activeFocus"):
                return True
                
            # Scroll if activeFocus not found
            self.scroll_right_increment(view)
            time.sleep(0.3)  # Wait for UI update after scrolling
            counter += 1
        
        # Final check
        item = self.get_element(item_locator)
        return item and self.get_element_property(item, "activeFocus")

    def scroll_right_increment(self, element:QmlTestServerItem, amount:int = 1) -> bool:
        for _ in range(amount):
            try:
                element.mouse_wheel(180, 180)
            except Exception as exception:
                logging.error(f"Failed to scroll right. Caught exception:\n{exception}")
                return False
        return True

    def scroll_left_increment(self, element:QmlTestServerItem, amount:int = 1) -> bool:
        for _ in range(amount):
            try:
                element.mouse_wheel(0, 0)
            except Exception as exception:
                logging.error(f"Failed to scroll left. Caught exception:\n{exception}")
                return False
        return True

