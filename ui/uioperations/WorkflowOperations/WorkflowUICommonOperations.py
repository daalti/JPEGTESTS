import sys
import time
import logging
import json
import os
import datetime
from datetime import timedelta

from typing import Any
from dunetuf.ui.uioperations.BaseOperations.IWorkflowUICommonOperations import IWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError, QmlTestServerItem
from dunetuf.ui.uioperations.WorkflowOperations.JamAutoNavUIObjectIds import JamAutoNavUIObjectIds
from dunetuf.qmltest.QmlTestServer import QmlTestServerItem, QmlTestServerError

class WorkflowUICommonOperations(IWorkflowUICommonOperations):
    DEFAULT_WAIT_TIME_SECONDS:float = 15

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice        
        self.maxtimeout = 120

    def click_button_on_middle(self, button):
        """
        Click in the middle of the received button 
        """
        try:
            # Validate object Button and click it on middle
            self._spice.wait_until(lambda: button["enabled"] == True) 
            middle_width = button["width"] / 2
            middle_height = int(button["height"] / 2)
            button.mouse_click(middle_width, middle_height)
            time.sleep(3)
        except:
            logging.info("FAILED: Button is not enabled")

    def is_back_navigating_button_available(self, back_button):
        if (self._spice.wait_for(back_button)["visible"] == True):
            return True
        else:
            return False
            
    def back_button_press(self, screen_id, landing_view, index: int = 0, timeout_val: int = 60):
        '''
        Press back button in specific screen.
        Args:
          screen_id: Screen object id
          landing_view: Landing screen after pressing back button
          index: Query index for the ui item
          timeout_val: Time out for scrolling
        '''
        if (self._spice.wait_for(screen_id + " " + "#BackButton")["visible"] == True):
            # TODO verify the code once the back button is in position
            back_button = self._spice.query_item(screen_id + " " + "#BackButton")
            back_button.mouse_click()
            #time.sleep(2)
            #assert self._spice.wait_for(landing_view)
            #time.sleep(1)

        else:
            logging.info("Navigating to home screen if back button is not present on the UI ")
            homeButton = self._spice.wait_for("#HomeButton")
            homeButton.mouse_click()
        time.sleep(3)
        self._spice.wait_for(landing_view)
        logging.info("At" +landing_view)
            #homeApp = self._spice.query_item("#HomeScreenView")
            #self._spice.wait_until(lambda: homeApp["activeFocus"] == True)
            #logging.info("At Home Screen")

    def back_or_close_button_press(self, close_or_back_button, landing_view):
        '''
        Press back/close button in specific screen.
        Args:
          close_or_back_button: close/back button object name
          landing_view: Landing screen after pressing back button
        '''
        back_or_close_button = self._spice.wait_for(close_or_back_button)
        back_or_close_button.mouse_click()
        self._spice.wait_for(landing_view)
        time.sleep(3)
        logging.info("At: " +landing_view)
    
    def click_on_back_button(self):
        '''
        Click on back button.
        '''
        back_button = self._spice.wait_for("#BackButton SpiceText")
        middle_width  = back_button["width"] / 2
        middle_height = back_button["height"] / 2
        back_button.mouse_click(middle_width, middle_height)  

    def find_object_scrolling_vertically(self, object_id, scrollbar_id=None, 
                                        view_id=None, scroll_value=0.2, mouse_wheel_scroll_value=-120, 
                                        timeout=2, max_timeout_to_scroll=120, click_option=False):
        """
        Method dispatcher to scroll ONLY in vertical direction until the given object is found.

        How to use this method:
            1: If you know the scrollbar id -> find_object(object_id, scrollbar_id="#scrollbar_id", scroll_value=<desired_value>).
            2: If you know the view id where the object is -> find_object(object_id, view_id="#view_id", mouse_wheel_scroll_value=<desired_value>).
            3: If you do not know the scrollbar id nor the view id -> find_object(object_id, mouse_wheel_scroll_value=<desired_value>).

            Reminder:
                If you do not specify what parameters are you passing to the method dispatcher, it could call the wrong method. 
                So, if you know the view id but not the scrollbar, then call the method like find_object(object_id, view_id="#view_id") 
                instead of find_object(object_id, "#view_id").

        Args:
            object_id `str`: The object we want to find. ex: "#colorModeComboBox".
            scrollbar_id `str`: The scrollbar object. Default is None.
            view_id `str`: The view id where the object we are seeking for is placed. Default is None.
            scroll_value `float`: How much we want to scroll down each step. Default value is 0.2. Use this parameter 
            when the scrollbar id is known and passed as a parameter.
            mouse_wheel_scroll_value `int`: How much we want to scroll down each step. Default value is -120. Use this 
            parameter if the scrollbar id is not known and/or not passed.
            timeout `int`: Maximum time to wait for the item. Default is 2. (used in wait_for method)
            max_timeout_to_scroll `int`: Maximum time to spent scrolling. Only used when scrollbar is unknown. Default value is 120 seconds.
            click_option `bool`: Set this to True if you want to click the object. Default value is False.

        Returns:
            `spice object`: If click option is set to False. Then it will return the desired object if has been found.
            `TimeoutError`: Raise a timeout error if the object has not been found.
        """
        if scrollbar_id:
            return self.scroll_vertically_to_object(object_id, scrollbar_id, scroll_value, timeout, click_option)
        elif view_id:
            return self.scroll_view_vertically_to_object(object_id, view_id, scroll_value=mouse_wheel_scroll_value, 
                                                        timeout=timeout, max_timeout_to_scroll=max_timeout_to_scroll, 
                                                        click_option=click_option)
        else:
            return self.scroll_vertically_with_no_scrollbar_or_view(object_id, scroll_value=mouse_wheel_scroll_value, 
                                                                    timeout=timeout, max_timeout_to_scroll=max_timeout_to_scroll, 
                                                                    click_option=click_option)
    
    def scroll_vertically_to_object(self, object_id, scrollbar_id, scroll_value=0.2, timeout=2, click_option=False):
        """
        Scroll in vertical direction until the given object is found and click it if click option is set to True.

        Args:
            object_id `str`: The object we want to find. ex: "#colorModeComboBox".
            scrollbar_id `str`: The scrollbar object.
            scroll_value `float`: How much we want to scroll down each step. Default value is 0.2
            timeout `int`: Maximum time to wait for the item. Default is 2. (used in wait_for method).
            click_option `bool`: Set this to True if you want to click the object. Default value is False.
        
        Returns:
            `spice object`: If click option is set to False. Then it will return the desired object if has been found.
            `TimeoutError`: Raise a timeout error if the object has not been found.
        """
        current_scroll_value = 0
        # Reset scrollbar position
        self.scroll_to_position_vertical(current_scroll_value, scrollbar_id)
        is_object_visible = False
        desired_object = None
        while is_object_visible == False and current_scroll_value < 1.1:
            try:
                desired_object = self._spice.wait_for(object_id, timeout)
            except TimeoutError as timeout_error:
                logging.info("%s", timeout_error)
                current_scroll_value += scroll_value
                self.scroll_to_position_vertical(min(current_scroll_value, 1.1), scrollbar_id)
            else:
                # No exception occurred
                logging.info("Is the object visible: {}".format(desired_object["visible"]))
                is_object_visible = desired_object["visible"]

        if is_object_visible:
            if click_option:
                desired_object.mouse_click()
                #self._spice.common_operations.click_button_on_middle(desired_object)
            else:
                return desired_object
        else:
            raise TimeoutError("Item '{}' not found".format(object_id))

    def checkingAlertMessageStrings(self,net, alertStringIdsArray,locale:str = "en-US"):
        """
        verify the message content of the alert message

        Args:
            alertStringIdsArray: the array of the alert message string id

        """
        alert:str = self._spice.wait_for(MenuAppWorkflowObjectIds.alertApp_click_alertHeader,60)
        for step_count in range(len(alertStringIdsArray["step"])):
            if step_count != 0:
                scrollbar = self._spice.wait_for("#bodyLayoutverticalLayoutScrollBar")
                scrollbar.__setitem__("position", "0.5")
                scrollbar.__setitem__("position", "0.5")
            for i in range(len(alertStringIdsArray["step"][step_count])):
                alert_body:str = self._spice.query_item(f"#InformationTemplate #rowPiece{str(int(step_count+1))} #columnforText{str(int(step_count+1))} #alertDetailDescription{str(int(step_count+1))} #textColumn #contentItem", i)
                alert_string_id = alertStringIdsArray["step"][step_count][i]
                if isinstance(alert_string_id, list):
                    expected_msg = str(LocalizationHelper.get_string_translation(net, alert_string_id, locale))
                else:
                    expected_msg = str(LocalizationHelper.get_string_translation(net, [alert_string_id], locale))
                logging.info("expected_msg: %s", expected_msg)
                logging.info("alert_body: %s", alert_body["text"])
                assert alert_body["text"] == expected_msg, "the strings are not equal expected one: %s, actual one: %s" % (expected_msg, alert_body["text"])
    
    def check_and_click_radioButton(self, radioButtonId, title, clickable=False):
        """
         check the name and click the radio button if required

         Args:

            radioButtonId: the object id of the radio button
            title: string to be checked
            clickable: if the radio button is clickable

        """
        index = 0
        found = False
        while not found:
            try:
                buttonTextQuery = self._spice.query_item(radioButtonId, index)
                logging.info("Button Text Query: " + str(buttonTextQuery["text"]))
            except (QmlItemNotFoundError, TimeoutError) as e:
                logging.info("Exception raised: " + str(e))
                logging.info("Alert: {0} not Found")
                return None, None
            if str(buttonTextQuery["text"]) == str(title):
                found = True
            else:
                found = False
                index += 1
        return buttonTextQuery["text"]
                
    def scroll_view_vertically_to_object(self, object_id, view_id, scroll_value=-120, timeout=2, max_timeout_to_scroll=120, click_option=False):
        """
        Scroll the view in vertical direction until the given object is found and click it if click option is set to True.
        Use this method if the scrollbar object name is unknown.

        Args:
            object_id `str`: The object we want to find. ex: "#colorModeComboBox".
            view_id `str`: The view id where the object we are seeking for is placed.
            scroll_value `int`: How much we want to scroll down each step. Default value is -120.
            timeout `int`: Maximum time to wait for the item. Default is 2. (used in wait_for method).
            max_timeout_to_scroll `int`: Maximum time to spent scrolling. Default value is 120.
            click_option `bool`: Set this to True if you want to click the object. Default value is False.

        Returns:
            `spice object`: If click option is set to False. Then it will return the desired object if has been found.
            `TimeoutError`: Raise a timeout error if the object has not been found.
        """
        current_view = self._spice.wait_for(view_id, timeout)
        self._spice.mouse(self._spice.MOUSE.CLICK, button=self._spice.MOUSE_BTN.MIDDLE)
        # Reset scrollbar position
        # mouse_wheel(0, 0) does not reset the view position
        current_view.mouse_wheel(0, 1000000)
        time.sleep(5)
        current_scroll_value = 0
        is_object_visible = False
        desired_object = None
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (is_object_visible == False and time_spent_waiting < max_timeout_to_scroll):
            time_spent_waiting = time.time() - start_time
            try:
                desired_object = self._spice.wait_for(object_id, timeout)
            except TimeoutError as timeout_error:
                logging.info("%s", timeout_error)
                current_view.mouse_wheel(0, scroll_value)
                current_scroll_value += scroll_value
            else:
                is_object_visible = desired_object["visible"]

        if is_object_visible:
            if click_option:
                desired_object.mouse_click()
            else:
                return desired_object
        else:
            raise TimeoutError("Item '{}' not found".format(object_id))


    def scroll_vertically_with_no_scrollbar_or_view(self, object_id, scroll_value=-120, 
                                                    timeout=2, max_timeout_to_scroll=120, click_option=False):
        """
        Scroll in vertical direction until the given object is found and click it if click option is set to True.
        Use this method if the view and scrollbar object names are unknown.

        Args:
            object_id `str`: The object we want to find. ex: "#colorModeComboBox".
            scroll_value `int`: How much we want to scroll down each step. Default value is -120.
            timeout `int`: Maximum time to wait for the item. Default is 2. (used in wait_for method).
            max_timeout_to_scroll `int`: Maximum time to spent scrolling. Default value is 120.
            click_option `bool`: Set this to True if you want to click the object. Default value is False.

        Returns:
            `spice object`: If click option is set to False. Then it will return the desired object if has been found.
            `TimeoutError`: Raise a timeout error if the object has not been found.
        """
        self._spice.mouse(self._spice.MOUSE.CLICK, button=self._spice.MOUSE_BTN.MIDDLE)
        # Reset scrollbar position
        # mouse(operation=MOUSE.WHEEL, 0) does not reset the view position
        self._spice.mouse(operation=self._spice.MOUSE.WHEEL, wheel_y=1000000)
        time.sleep(5)
        current_scroll_value = 0
        is_object_visible = False
        desired_object = None
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (is_object_visible == False and time_spent_waiting < max_timeout_to_scroll):
            time_spent_waiting = time.time() - start_time
            try:
                desired_object = self._spice.wait_for(object_id, timeout)
            except TimeoutError as timeout_error:
                logging.info("%s", timeout_error)
                self._spice.mouse(operation=self._spice.MOUSE.WHEEL, wheel_y=scroll_value)
                current_scroll_value += scroll_value
            else:
                is_object_visible = desired_object["visible"]

        if is_object_visible:
            if click_option:
                desired_object.mouse_click()
            else:
                return desired_object
        else:
            raise TimeoutError("Item '{}' not found".format(object_id))

    def goto_item(self, menu_item_id, screen_id, dial_value: int = -180, select_option: bool = True, scrolling_value=0.05, scrollbar_objectname="#scanMenuListlist1ScrollBar"):
        """
        This method searches and clicks a specified button on a specified menu
        Args:
            menu_item_id: pass the Object Id's in the form of string or list.
                        eg:string:"#ComboBoxOptionscolor"
                        list:["#scan_fileFormatSettingsComboBox", "scan_fileFormatComboBox"]
                        menu_item_id[0]: pass the row object id
                        menu_item_id[1]: pass the actual object id
            screen_id: Object Id of the screen
            dial_value: Direction for dialing
            select_option: Select True to click on the element
            scrolling_value : scrolling value between 0 and 1
            scrollbar_objectname : scrollbar object name

        """
        if type(menu_item_id) == str:
            isVisible = False
            step_value = 0
            self.scroll_to_position_vertical(step_value, scrollbar_objectname)
            while (isVisible is False and step_value <= 1):
                try:
                    current_screen = self._spice.wait_for(screen_id)
                    isVisible = self.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    while (isVisible is False and step_value <= 1):
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(2)
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                        step_value = step_value + scrolling_value
                    if select_option is True and isVisible is True:
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                        if isVisible is True:
                            current_button = self._spice.query_item(
                                screen_id + " " + menu_item_id)
                            self.click_button_on_middle(current_button)
                            logging.info("At Expected Menu")
                        else:
                            logging.info("item not found")

                except Exception as e:
                    logging.info("exception msg %s", e)
                    if str(e).find("Query selection returned no items") != -1:
                        step_value = step_value + scrolling_value
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(2)
                        pass
        else:
            isVisible = False
            step_value = 0
            self.scroll_to_position_vertical(step_value, scrollbar_objectname)
            while (isVisible is False and step_value <= 1):
                try:
                    current_screen = self._spice.wait_for(screen_id)
                    start_time = time.time()
                    time_spent_waiting = time.time() - start_time
                    isVisible = self.validateListObjectVisibility(screen_id, menu_item_id[0], "", 1)

                    while (isVisible is False and step_value <= 1):
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id[0], "", 1)
                        step_value = step_value + scrolling_value
                    if select_option is True and isVisible is True:
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id[0], menu_item_id[1], 1)
                        if isVisible is True:
                            current_button = self._spice.query_item(
                                screen_id + " " + menu_item_id[0] + " " + menu_item_id[1])
                            current_button.mouse_click()
                            logging.info("At Expected Menu")
                        else:
                            logging.info("item not found")

                except Exception as e:
                    logging.info("exception msg %s", e)
                    if str(e).find("Query selection returned no items") != -1:
                        step_value = step_value + scrolling_value
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        pass


    def is_item_available(self, menu_item_id, screen_id, dial_value: int = -180, scrolling_value=0.1, scrollbar_objectname="#scanMenuListlist1ScrollBar"):
        """
        This method searches a specified item on a specified menu
        Args:
            menu_item_id: pass the Object Id's in the form of string or list.
                        eg:string:"#ComboBoxOptionscolor"
                        list:["#scan_fileFormatSettingsComboBox", "scan_fileFormatComboBox"]
                        menu_item_id[0]: pass the row object id
                        menu_item_id[1]: pass the actual object id
            screen_id: Object Id of the screen
            dial_value: Direction for dialing
            scrolling_value : scrolling value between 0 and 1
            scrollbar_objectname : scrollbar object name

        """

        itemAvailable = False

        if type(menu_item_id) == str:
            isVisible = False
            step_value = 0
            while (isVisible is False and step_value <= 1):
                try:
                    current_screen = self._spice.wait_for(screen_id)
                    isVisible = self.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    while (isVisible is False and step_value <= 1):
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                        step_value = step_value + scrolling_value
                    
                    if isVisible is True:
                        itemAvailable =True
                        logging.info("At Expected Menu")
                    else:
                        logging.info("item not found")

                except Exception as e:
                    logging.info("exception msg %s", e)
                    if str(e).find("Query selection returned no items") != -1:
                        step_value = step_value + scrolling_value
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        pass
        else:
            isVisible = False
            step_value = 0
            while (isVisible is False and step_value <= 1):
                try:
                    current_screen = self._spice.wait_for(screen_id)
                    start_time = time.time()
                    time_spent_waiting = time.time() - start_time
                    isVisible = self.validateListObjectVisibility(screen_id, menu_item_id[0], "", 1)

                    while (isVisible is False and step_value <= 1):
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        isVisible = self.validateListObjectVisibility(screen_id, menu_item_id[0], "", 1)
                        step_value = step_value + scrolling_value
                    if isVisible is True:
                        itemAvailable =True
                        logging.info("At Expected Menu")
                    else:
                        logging.info("item not found")

                except Exception as e:
                    logging.info("exception msg %s", e)
                    if str(e).find("Query selection returned no items") != -1:
                        step_value = step_value + scrolling_value
                        self.scroll_to_position_vertical(step_value, scrollbar_objectname)
                        time.sleep(5)
                        pass
        
        return itemAvailable

    def goto_scan_app(self):
        """
        UI should be in Homescreen
        Navigates to Scan App screen starting from Home screen.
        UI Flow is Home->Scan
        """
        # make sure that you are in home screen
        self._spice.goto_homescreen()
        self._spice.home_operations.home_navigation(ScanAppWorkflowObjectIds.scan_app)

        assert self._spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        logging.info("At Scan App")

    def goto_item_navigation(self, menu_item_id, screen_id, dial_value: int = 180, select_option: bool = True):
        """
        This method searches and clicks a specified button on a specified menu from left to right.
        Args:
            menu_item_id: Object Id of the menu item to be pressed
            screen_id: Object Id of the screen
            dial_value: Direction for dialing
            select_option: Select True to click on the element
        """
        current_screen = self._spice.wait_for(screen_id)
        self._spice.wait_for(menu_item_id)
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (self._spice.query_item(menu_item_id)["visible"] == False and time_spent_waiting < self.maxtimeout):
            current_screen.mouse_wheel(0, 0)  # To do:will change later
            time_spent_waiting = time.time() - start_time
        if (self._spice.query_item(menu_item_id)["visible"] == False):
            if (dial_value == 0):
                dial_value = 180
            else:
                dial_value = 180
            current_screen = self._spice.wait_for(screen_id)
            start_time = time.time()
            time_spent_waiting = time.time() - start_time
            while (self._spice.query_item(menu_item_id)["visible"] == False and time_spent_waiting < self.maxtimeout):
                current_screen.mouse_wheel(dial_value, -180)  # To do:will change later
                time_spent_waiting = time.time() - start_time
        if select_option == True:
            current_button = self._spice.query_item(
                menu_item_id + " SpiceText")
            current_button.mouse_click()
            logging.info("At Expected Menu")

    def get_expected_translation_str_by_str_id(self, net, str_id, locale: str = "en-US"):
        logging.info(f"To get expected str of {str_id}")
        expected_translation_str = LocalizationHelper.get_string_translation(net, str_id, locale)
        logging.info(f"The expected str of str id__{locale}: {str_id} is: {expected_translation_str}")
        return expected_translation_str

    def get_actual_str(self, object_name, index: int = 0, isSpiceText: bool = False):
        logging.info(f"To get actual str of {object_name}")
        item = self._spice.wait_for(object_name, timeout = 20)
        self._spice.wait_until(lambda: item["visible"] is True, 20)
        if not isSpiceText:
            object_name = object_name + " SpiceText[visible=true]"
        for _ in range(3):            
            actual_str = self._spice.query_item(object_name,query_index=index)["text"]
            if actual_str:
                break
            time.sleep(3)

        logging.info(f"The actual str of oject name: {object_name} is: {actual_str}")
        return actual_str

    def verify_string(self, net, str_id, object_name, locale: str = "en-US", index: int = 0, isSpiceText: bool = False):
        expected_translation_str = self.get_expected_translation_str_by_str_id(net, str_id, locale)
        actual_str = self.get_actual_str(object_name, index, isSpiceText)
        assert expected_translation_str == actual_str

    def verify_string_param(self, net, str_id, user_name, object_name, locale: str = "en-US", index: int = 0, isSpiceText: bool = False):
        expected_translation_str = self.get_expected_translation_str_by_str_id(net, str_id, locale)
        actual_str = self.get_actual_str(object_name, index, isSpiceText)
        expected_translation_str = expected_translation_str + " (" +user_name +")"
        assert expected_translation_str == actual_str

    def validateListObjectVisibility(self, listObj, rowObject, elementObject, isVertical):
        """
        Validate object if it is visible

        Args:
            objectApp: Param1 -- Base object (can be list object),
                        Param2 -- Object within Base (can be row object),
                        Param3 -- Individual object with in Param2 (can be an object in row)
                        Param4 -- 1(Vertical), 0(Horizontal)
        """

        logging.info("----------------############------------------------")

        if (listObj != ""):
            isEnabled = self._spice.query_item(listObj)["visible"]
            if (isEnabled is False):
                return isEnabled

        if (rowObject != ""):
            isEnabled = self._spice.query_item(listObj + " " + rowObject)["visible"]
            if (isEnabled is False):
                return isEnabled

        if (elementObject != ""):
            isEnabled = self._spice.query_item(listObj + " " + rowObject + " " + elementObject)["visible"]
            if (isEnabled is False):
                return isEnabled

        widthOfListObj = self._spice.query_item(listObj)["width"]
        heightOfListObj = self._spice.query_item(listObj)["height"]
        contentYOfListObj = self._spice.query_item(listObj)["contentY"]
        contentXOfListObj = self._spice.query_item(listObj)["contentX"]
        lineThickness = 0.05
        if rowObject != "":
            rowObjectY = self._spice.query_item(listObj + " " + rowObject)["y"] 
            rowObjectX = self._spice.query_item(listObj + " " + rowObject)["x"]
            rowObjectWidth = self._spice.query_item(listObj + " " + rowObject)["width"]
            rowObjectHeight = self._spice.query_item(listObj + " " + rowObject)["height"]

        if (isVertical == 1):
            if (contentYOfListObj < 0):
                if (heightOfListObj + contentYOfListObj - rowObjectY - rowObjectHeight  >= 0):                 
                    return True
                else:
                    return False
            else:
                if (rowObjectY >= contentYOfListObj and rowObjectY <= heightOfListObj + contentYOfListObj - rowObjectHeight + lineThickness):
                    return True
                else:
                    return False
        else:
            if (contentXOfListObj < 0):
                if (widthOfListObj + contentXOfListObj - rowObjectX - rowObjectWidth / 2 > 0):
                    return True
                else:
                    return False
            else:
                if (rowObjectX >= contentXOfListObj and rowObjectX <= widthOfListObj + contentXOfListObj - rowObjectWidth):
                    return True
                else:
                    return False

    def scroll_to_position_horizontal(self, position: int) -> None:
        '''
        Scrolls to the provided position
        Parameters:
        spice: the spice object
        position: between 0-1
        '''
        assert (position >= 0 and position <= 1), "Wrong value. Postion can only be between 0 and 1"
        print("Moving scroll to position : " + str(position))
        logging.debug("********************scroll_to_position_horizontal::enter _spice.wait_for")
        scrollbar = self._spice.wait_for("#hScrollhorizontalScroll")
        logging.debug("********************scroll_to_position_horizontal::exit _spice.wait_for")
        logging.debug("********************scroll_to_position_horizontal::enter __setitem__")
        scrollbar.__setitem__("position", str(position))
        logging.debug("********************scroll_to_position_horizontal::exit __setitem__")

    def scroll_to_position_vertical(self, position: float, scrollbar_objectname: str) -> None:
        '''
        Scrolls to the provided position
        Parameters:
        spice: the spice object
        position: between 0-1
        '''
        scrollbar = self._spice.wait_for(scrollbar_objectname)
        size = scrollbar["size"]
        if position >= 0 and position <= 1.0-size:
            print("Moving scroll to position : " + str(position)+", step size "+str(size))
            scrollbar.__setitem__("position", str(position))
        else:
            logging.info("Wrong value. Postion can only be between 0 and 1 where position : " + str(position)+", step size "+str(size)+" ==> Now Setting position to Max Value")
            scrollbar.__setitem__("position", str(1.0-size))

    def scroll_to_widget(self, screenid = "#HomeScreenView", scrollbar_ = "#horizontalScroll", loader = "#widgetsLoader", element_id = None):

        #This scrollPosition function is special case for finding widget.
        screen_width = self._spice.wait_for(screenid + " " + scrollbar_, timeout=15.0)["width"]
        logging.info("screen_width = %s", screen_width)
        screen_total_width = self._spice.wait_for(screenid + " " + loader, timeout=15.0)["width"]
        logging.info("screen_total_width = %s", screen_total_width)

        #move scrollbar to postion 0
        scrollbar = self._spice.wait_for(scrollbar_, timeout=15.0)
        scrollbar.__setitem__("position", "0")

        location_element = self._spice.wait_for(screenid + " " + element_id, timeout=15.0)["x"]
        logging.info("location_element = %s", location_element)
        element_width = self._spice.wait_for(screenid + " " + element_id)["width"]
        logging.info("element_width = %s", element_width)
        location_element_width = location_element + element_width
        logging.info("location_element_width = %s", location_element_width)

        if (location_element_width > screen_width):
            if screen_total_width > 0:
                pos = (location_element/screen_total_width)
                position = round(pos, 2)
                logging.info("pos = %s", position)
                scrollbar = self._spice.wait_for(scrollbar_)
                scrollbar.__setitem__("position", position)

    def scroll_position(self, screenid , element_id , scrollbar_ , columnname = "", listItem = "", section_bottom_border = "",  delta = 0):

        #This scrollPosition function is special case for buttonTemplate.

        scrollBarObJName =  screenid + " " + scrollbar_
        scrollBarItem = self._spice.check_item(scrollBarObJName)

        if scrollBarItem is None:
            logging.info(f"scrollBar {scrollBarObJName} is not found")
            return

        screen_height = self._spice.wait_for(screenid + " " + scrollbar_)["height"]
        screen_total_height_element = (screenid + " " + listItem) if listItem != "" else screenid # select the item if the argument is used; otherwise use the list itself
        screen_total_height = self._spice.wait_for(screen_total_height_element)["contentHeight"]
        column_location = 0 if columnname == "" else self._spice.wait_for(screenid + " " + columnname)["y"]
        section_border_height = 0
        if( section_bottom_border != ""):
            section_border_height =  self._spice.wait_for(screenid + " " + section_bottom_border)["height"]

        #move scrollbar to postion 0
        scrollbar = self._spice.wait_for(scrollbar_)
        scrollbar.__setitem__("position", "0")
    
        location_element = self._spice.wait_for(screenid + " " + element_id)["y"]
        location_element = location_element + column_location
        element_height = self._spice.wait_for(screenid + " " + element_id)["height"]
        location_element_height = location_element + element_height 
        if (location_element_height > screen_height):
            if screen_total_height > 0:
                location_element = location_element - section_border_height
                pos = (location_element/screen_total_height) - delta 
                scrollbar.__setitem__("position", str(pos))

    def scroll_fixed_list(self, list_id, element_id, scrollbar_id):
        """
        Scrolls a list where if you reache the end you can't keep scrolling.
        An example of this list would be the Partners menu, where you can't scroll anymore.
        A counter-example would be the Tools menu, where you reach the end and the items can still go a bit up.
        """
        scrollbar = self._spice.wait_for(list_id + " " + scrollbar_id)
        screen_height = scrollbar["height"]
        list_element = self._spice.wait_for(list_id)
        screen_total_height = list_element["contentHeight"]

        #move scrollbar to postion 0
        scrollbar.__setitem__("position", "0")
    
        location_element = self._spice.wait_for(list_id + " " + element_id)["y"]
        element_height = self._spice.wait_for(list_id + " " + element_id)["height"]
        location_element_height = location_element + element_height 
        if (location_element_height > screen_height):
            if screen_total_height > 0:
                pos = (location_element/screen_total_height)
                max_position = (screen_total_height - screen_height) / screen_total_height

                if pos > max_position:
                    logging.info("Overriding scroll position, as the limit has been reached on a fixed scroll list")
                    pos = max_position
                scrollbar.__setitem__("position", str(pos))
    
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

    def convertfbsExtendedToCppEnumValue(self , key):
        """
        This function converts cdm value to cpp enum value
        """
        result_string = ""
        for i in range(0, len(key)):
            if key[i] == '-':
                result_string = result_string + "_dash_"
            elif key[i] == '+' :
                result_string = result_string + "_plus_" 
            elif key[i] == '*' :
                result_string = result_string + "_star_"
            elif key[i] == '.':
                result_string = result_string + "_dot_"
            elif key[i] == ':' :
                result_string = result_string + "_colon_"
            elif key[i] == '%' :
                result_string = result_string + "_percent_"
            elif key[i] == '@' : 
                result_string = result_string + "_at_"
            else :
                result_string = result_string + key[i]
        
        return result_string
    



    def compare_alert_toast_message(self, net, message_string_id, timeout = 30):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, any string type
        """

        toast_message= self.get_expected_translation_str_by_str_id(net, message_string_id)
        logging.info("Expected Toast message is : %s" % toast_message)
        start_time = time.time()
        actual_toast_message = ""
        while time.time()-start_time < timeout:
            try:
                self._spice.wait_for("#SpiceToast", timeout = 15.0)
                actual_toast_message = self._spice.query_item("#infoTextToastMessage")["text"]
                logging.info("Current Toast message is : %s" % actual_toast_message)
            except:
                logging.info("Still finding corresponding status.")
            if toast_message in actual_toast_message:
                break
        if toast_message not in actual_toast_message:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    def wait_until_object_not_visible(spice, object) -> None:
        # Wait for not visible situation
        spice.wait_until(lambda: object["visible"] == False)

    def verify_jam_autonav_ui_alert(self, net, stringID, stepID,installed_Trays, code, btn_click, locale: str = "en-US"):
        """
        Verify the alert message for Jam AutoNav UI
        """
        logging.info("verify_jam_autonav_ui_alert stepID %s", stepID)
        tray_count = 2
        jspath = os.path.dirname(os.path.realpath(__file__))
        with open( jspath + '/TestDataJamAutonav.json', 'r') as f:
            json_str = f.read()
        data = json.loads(json_str)
        autonavalert = None
        for alert in data['autoNavAlerts']['autoNavJam']:
            if str(alert['stringID']) == str(stringID) and str(alert['stepID']) == str(stepID):
                autonavalert = alert
        expected_title = autonavalert['title']
        if expected_title.endswith("%Tray%") == True:
            expected_title = expected_title.replace("%Tray%","")
            expected_title = str(LocalizationHelper.get_string_translation(net, [expected_title, int(tray_count)], locale))
        else:
            expected_title = str(LocalizationHelper.get_string_translation(net, autonavalert['title'], locale))
        logging.info("Alert expected_title: %s", str(expected_title))
        found = False
        attemps = 0
        alert_title = None
        qindex = 0
        timeout_delata = datetime.datetime.now() + timedelta(seconds=60)
        while(found == False and timeout_delata >datetime.datetime.now()):
            try:
                hidebtn = self._spice.query_item("#Hide",qindex)
                hidebtn.mouse_click()
                if self._spice.check_item("#Hide",query_index=self._spice.maxQueryIndex) == None:
                    logging.info("Hide button is not found")
                    found = True
                    break
                qindex += 1
            except:
                qindex = 0
            wait_until = datetime.datetime.now() + timedelta(seconds=2)
            while(wait_until>datetime.datetime.now()):
                pass
        if found == True:
            wait_until = datetime.datetime.now() + timedelta(seconds=5)
            while(wait_until>datetime.datetime.now()):
                pass
            self._spice._find_alert_in_alertApp_and_click(expected_title)
            logging.info("Alert Title: %s", str(alert_title))
        alertButton = self._spice.check_item("#HomeScreenView #persistentHeader #headerVar2RightContainer #alertButton")
        if alertButton != None:
            self._spice._find_alert_in_alertApp_and_click(expected_title)

        alert:str = self._spice.wait_for(MenuAppWorkflowObjectIds.alertApp_click_alertHeader)
        alert_title = alert["text"]

        logging.info("Alert Title: %s", str(alert_title))
        logging.info("Verify the Alert Title")
        assert alert_title == expected_title,"JAMAutonav Alert Title is not matching.Expected : %s Actual : %s"%(expected_title,alert_title)
        logging.info("Verify the Alert Message")
        section_count =  0
        for step in autonavalert['step']:
            step_count = len(step)
            logging.info("Step Count : %d",int(step_count))
            if section_count != 0:
                scrollbar = self._spice.wait_for("#bodyLayoutverticalLayoutScrollBar")
                scrollbar.__setitem__("position", "0.5")
                scrollbar.__setitem__("position", "0.5")
            for i in range(0,step_count):
                if i == 0 and section_count == 0:
                    logging.info("Verify the Alert Code")
                    alert_code = self._spice.wait_for(JamAutoNavUIObjectIds.jam_auto_nav_code)["text"]
                    expected_code =  str(LocalizationHelper.get_string_translation(net, ["cEventCodeParameter", str(code)], locale))
                    assert alert_code == expected_code,"JAMAutonav Alert Code is not matching.Expected : %s Actual : %s"%(expected_code,alert_code)
                logging.info("Verify the Alert Step")
                content_1 = self._spice.query_item("#InformationTemplate #rowPiece"+ str(int(section_count + 1)) +" #columnforText"+ str(int(section_count + 1)) +" #alertDetailDescription"+ str(int(section_count + 1)) +" #textColumn #contentItem", i)
                actual_step_message = str(content_1["text"])
                exp_step = str(step[i])
                expected_step_message = None
                if exp_step.endswith("%Tray%") == True:
                    exp_step = exp_step.replace("%Tray%","")
                    expected_step_message = str(LocalizationHelper.get_string_translation(net, [exp_step, int(tray_count)], locale))
                else:
                    expected_step_message = str(LocalizationHelper.get_string_translation(net, step[i], locale))
                assert actual_step_message == expected_step_message,"JAMAutonav Alert Step is not matching.Expected : %s Actual : %s section_count: %s step: %s"%(expected_step_message,actual_step_message,section_count,i)
            section_count = section_count + 1
        logging.info("Verify the Fooetr Button")
        okbtn = None
        hidebtn = None
        if autonavalert['ok'] == "Yes":
            logging.info("Ok Button")
            okbtn = self._spice.query_item("#OK SpiceText[visible=true]")
            assert okbtn["text"] == str(LocalizationHelper.get_string_translation(net, "cOKButton", locale)),"JAMAutonav Alert OK Button is not matching.Expected : %s Actual : %s"%(str(LocalizationHelper.get_string_translation(net, "cOKButton", locale)),okbtn["text"])
        if autonavalert['hide'] == "Yes":
            hidebtn = self._spice.query_item("#Hide SpiceText[visible=true]")
            assert hidebtn["text"] == str(LocalizationHelper.get_string_translation(net, "cHide", locale)),"JAMAutonav Alert Hide Button is not matching.Expected : %s Actual : %s"%(str(LocalizationHelper.get_string_translation(net, "cHide", locale)),hidebtn["text"])
        if btn_click == "OK":
            okbtn.mouse_click()
        elif btn_click == "HIDE":
            hidebtn.mouse_click()
        else:
            logging.info("No Button Clicked")

    def wait_until_property_value(self, object, property, state, timeout = 5, delay = 0.25):
        # Wait for object property to change to specific state
        self._spice.wait_until( lambda: object[property] == state , timeout, delay = delay)

    def scroll_vertical_row_item_into_view(self, screen_id, menu_item_id, footer_item_id=None, top_item_id=None, select_option: bool = True, time_delay=2, start_from_top=True, scroll_step: int = 2):
        """
        This function will make sure the row item on the top of screen directly instead of scroll step by step, also will make sure the last pages item always aligns to the bottom
        Also need to conside top objtec/footer object when it is included in scroll screen view
        screen id: the parent screen view of row item, this screen view should contain property "contentHeight"/"contentY"/"height"
        menu_item_id: row item
        top_item_id: some screen contains top item should subtract the height of this control
        footer_item_id: some screen contains footer item should subtract the height of this control
        select_option: Select True to click on the element
        start_from_top: always find item from top to bottom if True, and will find item from current location of screen if False
        """
        logging.info(f"scroll_vertical_row_item_into_view screen_id-> {screen_id}, menu_item_id -> {menu_item_id}, footer_item_id-> {footer_item_id}, top_item_id-> {top_item_id}")
        at_y_end = False
        is_in_view = False
        first_time_validate = True
        screen_view = self._spice.wait_for(screen_id)
        self._spice.wait_until(lambda: screen_view["visible"])
        align_step = -1
        # make sure all item loaded completely 
        time.sleep(2)

        if top_item_id:
            top_item_height = self._spice.wait_for(top_item_id)["height"]
            logging.info(f"top object is included in scroll screen view, top_heights: <{top_item_height}>")
        else:
            top_item_height = 0

        if footer_item_id:
            footer_height = self._spice.wait_for(footer_item_id)["height"]
            logging.info(f"footer object is included in scroll screen view, footer_heights: <{footer_height}>")
        else:
            footer_height = 0

        while(at_y_end is False and is_in_view is False):
            max_content_y = screen_view["contentHeight"] - screen_view["height"] + screen_view["originY"]
            logging.info(f"The current max_content_y is <{max_content_y}>")
            at_y_end = screen_view["atYEnd"]
            try:
                is_in_view = self.validate_list_object_is_in_vertical_screen_view(screen_id=screen_id, menu_item_id=menu_item_id, footer_item_id=footer_item_id, top_item_id=top_item_id)
                if not is_in_view:
                    menu_item_y = self._spice.query_item(f"{screen_id} {menu_item_id}")["y"]
                    align_step = align_step + 1
                    align_top_content_y_of_screen = menu_item_y - top_item_height - align_step
                    if align_top_content_y_of_screen >= max_content_y:
                        screen_view["contentY"] = max_content_y
                        time_delay = 3
                    else:
                        screen_view["contentY"] = align_top_content_y_of_screen
                time.sleep(time_delay)
                at_y_end = screen_view["atYEnd"]
                first_time_validate = False
            except Exception as err:
                logging.info(f"exception msg -> {err}")
                if str(err).find("Query selection returned no items") != -1 or str(err).find("not found within")!=-1:
                    if start_from_top and first_time_validate:
                        screen_view["contentY"] = screen_view["originY"]
                        logging.info("Item not found on first query, then find it again start from top of screen")
                        time.sleep(2)
                        at_y_end = False
                        first_time_validate = False
                    else:
                        logging.info("Item not found on second query, then find it again by next scroll down")
                        self.scroll_screen_via_height(screenid=screen_id, sroll_height=(screen_view["height"]-top_item_height-footer_height)/scroll_step, time_delay=time_delay)
                else:
                    raise Exception(str(err))
        if not is_in_view:
            # to check again 
            is_in_view = self.validate_list_object_is_in_vertical_screen_view(screen_id=screen_id, menu_item_id=menu_item_id, footer_item_id=footer_item_id, top_item_id=top_item_id)
        assert is_in_view, f"The item is not in view of screen, so that cannot click it"

        if select_option:
            logging.info(f"Click item {menu_item_id}")
            click_item = self._spice.wait_for(f"{screen_id} {menu_item_id}")
            click_item.mouse_click()
            time.sleep(1)
    
    def scroll_screen_via_height(self, screenid, sroll_height, time_delay=2):
        """
        Scroll screen via height, then could go through item one by one with limited max contentY to avoid last item displayed in center of screen  
        Especially for last item, cannot operation the last item normally in part screen when it is in screen center via function scroll_bar["position"] to set value position, actually this item 
        should display at the bottom of screen. At this time, this item will be reset to bottom location rather then clicked/checked box selected

        screen id: the parent screen of row item, this screen should contain property "contentHeight"/"contentY"/"height"
        sroll_height: the heght of row item
        """
        screen_view = self._spice.wait_for(screenid)
        self._spice.wait_until(lambda: screen_view["visible"])
        screen_height = screen_view["height"]
        content_height = screen_view["contentHeight"]
        screen_origin_y = screen_view["originY"]
        max_content_y = content_height - screen_height + screen_origin_y
        current_content_y = screen_view["contentY"]
        
        logging.info(f"screen_height is <{screen_height}>, content_height is <{content_height}>, current_content_y is <{current_content_y}>")

        if screen_view["atYEnd"]:
            logging.info("Already at the bottom of screen, no need to scroll")
            return

        if current_content_y + sroll_height > max_content_y:
            scroll_height = max_content_y
            time_delay = 5
            logging.info("Perhaps already at the bottom of screen")
        else:
            scroll_height = current_content_y + sroll_height
        
        logging.info(f"scroll to contentY: <{scroll_height}>")
        screen_view["contentY"] = scroll_height
        time.sleep(time_delay)

    def validate_list_object_is_in_vertical_screen_view(self, screen_id, menu_item_id, footer_item_id=None, top_item_id=None):
        """
        To check the item is in screen view then it can be click, need to conside Begining Y of screen
        -> one secnario is less then 0, such -60
        -> one secnario is 0, such as 0
        Also need to conside footer object when it is included in scroll screen view
        screen_id:
        menu_item_id:
        footer_item_id
        top_item_id
        """

        logging.info(f"To wait for screen <{screen_id}> is displayed")
        screen_widget = self._spice.wait_for(screen_id)

        width_of_screen = screen_widget["width"]
        height_of_screen = screen_widget["height"]
        content_y_of_screen = screen_widget["contentY"]
        content_x_of_screen = screen_widget["contentX"]

        if footer_item_id:
            footer_height = self._spice.wait_for(footer_item_id)["height"]
            logging.info(f"footer object is included in scroll screen view, footer_heights: <{footer_height}>")
        else:
            footer_height = 0
        
        if top_item_id:
            top_item_height = self._spice.wait_for(top_item_id)["height"]
            logging.info(f"top object is included in scroll screen view, top_heights: <{top_item_height}>")
        else:
            top_item_height = 0

        logging.info(f"To check whether item is present in screen")
        try:
            menu_item_widget = self._spice.query_item(screen_id + " " + menu_item_id)
            logging.info(f"The menu item is present under screen <{screen_id} {menu_item_id}>")
        except Exception as e:
            logging.info(f"The menu item is not present under screen <{screen_id} {menu_item_id}>")
            return False

        menu_item_y = menu_item_widget["y"] 
        menu_item_x = menu_item_widget["x"]
        menu_item_width = menu_item_widget["width"]
        menu_item_height = menu_item_widget["height"]

        if (0 + top_item_height <= menu_item_y - content_y_of_screen) and (menu_item_y - content_y_of_screen + menu_item_height <= height_of_screen - footer_height):
            return True
        else:
            return False


    def scroll_to_position_vertical_without_scrollbar(self, button_object_name: str, object_index = 0) -> None:
        """
        Scrolls vertically when the scrollbar is not visible or the object name is unknown, then clicks the desired button
        Parameters:
            -> spice: the spice object
            -> button_object_name: object name of the button to be clicked
            -> object_index: Item index
        """
        # Get the last SpiceScrollContainer object
        index = 0
        while True:
            try:
                spice_scroll_container = self._spice.query_item("SpiceScrollContainer", index)
                logging.info(f"Spice scroll container found with index: {index}")
                index += 1
            except QmlItemNotFoundError:
                # If query_item fails, we have gone through all SpiceScrollContainer objects
                break
        
        spice_scroll_container = self._spice.query_item("SpiceScrollContainer", index - 1)
        button = self._spice.wait_for(button_object_name, query_index = object_index)
        spice_scroll_container["contentY"] = button["y"]
        button.mouse_click()

    def get_element(self, locator:str, timeout:float = DEFAULT_WAIT_TIME_SECONDS) -> QmlTestServerItem:
        logging.debug(f"Attempting to get '{locator}' ...")
        element = None
        try:
            element = self._spice.wait_for(locator, timeout)
        except:
            logging.warning(f"Failed to get element '{locator}' in {timeout} seconds")
            
        return element
    
    def move_within_filter_view(self,scroll_bar_id,position):
        pass
    
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
        element.__setitem__(property, value)
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

    def click(self, button_element:QmlTestServerItem, click_center:bool = True, check_enabled:bool = True) -> bool:
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

        if check_enabled and not button_element.is_enabled():
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

    def scroll_horizontal(self, scroll_bar_element:QmlTestServerItem, scroll_to_element:QmlTestServerItem, scroll_area_width:float) -> bool:
        logging.debug(f"Scroll Area Width: {scroll_area_width}")
        logging.debug("Setting the scroll bar element position to 0")
        self.set_element_property(scroll_bar_element, "position", 0)
        
        scroll_to_element_left_x = self.get_element_property(scroll_to_element, "x")
        logging.debug(f"Element '{scroll_to_element.get_name()}' left x position: {scroll_to_element_left_x}")

        scroll_to_element_width = self.get_element_property(scroll_to_element, "width")
        logging.debug(f"Element '{scroll_to_element.get_name()}' width: {scroll_to_element_width}")

        scroll_to_element_right_x = scroll_to_element_left_x + scroll_to_element_width
        logging.debug(f"Element '{scroll_to_element.get_name()}' right x position: {scroll_to_element_right_x}")
        
        if scroll_to_element_right_x > scroll_area_width:
            """
                If the locator is out of view, then the scroll_to_element_right_x to scroll area width ratio will
                be greater that 1. We can subtract 1 from the ratio to get a value that is
                between 0 and 1 and scroll to that new ratio.
                Ex. scroll_to_element_right_x / scroll_area_width = 1.2
                    1.2 - 1 = 0.2
                    Set scroll bar position to 0.2 and the app should be in full view now
            """
            scroll_area_width_to_locator_ratio = (scroll_to_element_right_x / float(scroll_area_width)) - 1.0
            logging.debug(f"Element '{scroll_to_element.get_name()}' scroll area width to locator ratio: {scroll_area_width_to_locator_ratio}")
            if not self.set_element_property(scroll_bar_element, "position", scroll_area_width_to_locator_ratio):
                return False
        else:
            logging.debug(f"Element '{scroll_to_element.get_name()}' already in view")
        
        return True

    def scroll_vertical(self, scroll_bar_element:QmlTestServerItem, scroll_to_element:QmlTestServerItem, scroll_area_height:float) -> bool:
        logging.debug(f"Scroll Area Height: {scroll_area_height}")
        logging.debug("Setting the scroll bar element position to 0.0")
        self.set_element_property(scroll_bar_element, "position", 0.0)

        scroll_bar_height = self.get_element_property(scroll_bar_element, "height")
        logging.debug(f"Scroll Bar Height: {scroll_bar_height}")
        

        scroll_to_element_top_y = self.get_element_property(scroll_to_element, "y")
        logging.debug(f"Element '{scroll_to_element.get_name()}' top y position: {scroll_to_element_top_y}")

        scroll_to_element_height = self.get_element_property(scroll_to_element, "height")
        logging.debug(f"Element '{scroll_to_element.get_name()}' height: {scroll_to_element_height}")

        scroll_to_element_bottom_y = scroll_to_element_top_y + scroll_to_element_height
        logging.debug(f"Element '{scroll_to_element.get_name()}' bottom y position: {scroll_to_element_bottom_y}")

        if scroll_to_element_bottom_y > scroll_area_height:
            scroll_area_height_to_element_ratio = (scroll_to_element_bottom_y / scroll_area_height) - 1.0
            logging.debug(f"Element '{scroll_to_element.get_name()}' scroll area height to locator ratio: {scroll_area_height_to_element_ratio}")
            if not self.set_element_property(scroll_bar_element, "position", scroll_area_height_to_element_ratio):
               return False
        else:
            logging.debug(f"Element '{scroll_to_element.get_name()}' already in view")

        return True
