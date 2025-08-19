
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations




class WorkflowUICommonXSOperations(WorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice

    def click_home_button(self):
        print("Click Home button")
        self._spice.udw.mainUiApp.KeyHandler.setKeyPress("HOME")

    def click_back_button(self):
        print("Click Back button")
        self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")

    def goto_item_for_vertical_menu(self, menu_item_id, screen_id,  scrollbar_objectname, select_option: bool = True, scrolling_value=0.05):
        """
        This is an alternative method for function "goto_item()" under WorkflowUICommonOperations, please have a try to chose item with 
        this method when "goto_item()" does not work
        Args:
            menu_item_id: pass the Object Id's in the form of string or list. it's entire row object, eg:string:"#ComboBoxOptionscolor"
            screen_id: Object Id of the screen
            select_option: Select True to click on the element
            scrolling_value : scrolling value between 0 and 1
            scrollbar_objectname : scrollbar object name
        """
        isVisible = False
        step_value = 0
        current_screen = self._spice.wait_for(screen_id)
        # to make sure item displayed completely
        time.sleep(2)
        origin_y_of_screen = current_screen["originY"]
        scroll_bar = self._spice.wait_for(scrollbar_objectname)

        isVisible = self.validate_list_object_is_in_screen_view(menu_item_id, screen_id, origin_y_of_screen)

        while (isVisible is False and step_value <= 1):
            self.scroll_to_position_vertical(step_value, scrollbar_objectname)
            time.sleep(3)
            isVisible = self.validate_list_object_is_in_screen_view(menu_item_id, screen_id, origin_y_of_screen)
            step_value = step_value + scrolling_value
            if select_option is True and isVisible is True:
                current_button = self._spice.query_item(screen_id + " " + menu_item_id)
                current_button.mouse_click()
                time.sleep(3)
                logging.info("At Expected Menu")

        if not isVisible:
            raise Exception(f"Failed to go to item <{screen_id} {menu_item_id}>")

        logging.info(f"Success to go to item <{screen_id} {menu_item_id}>")

    def validate_list_object_is_in_screen_view(self, menu_item_id, screen_id, origin_y_of_screen):
        """
        To check the item is in screen view then it can be click
        """

        logging.info(f"To wait for screen <{screen_id}> is displayed")
        screen_widget = self._spice.query_item(screen_id)

        width_of_screen = screen_widget["width"]
        height_of_screen = screen_widget["height"]
        content_y_of_screen = screen_widget["contentY"]
        content_x_of_screen = screen_widget["contentX"]

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

        if (0 <= menu_item_y - content_y_of_screen + origin_y_of_screen) and (menu_item_y - content_y_of_screen + menu_item_height <= height_of_screen):
            return True
        else:
            return False
   
    def scroll_to_rightmost_on_quickset_landing_view(self, horizontal_screen_id, horizontal_scroll_bar, scrolling_value=0.1):
        """
        Scroll to rightmost on quickset_landing_view so that we can see view all button and click it
        """
        is_at_x_end = False
        
        current_horizontal_screen = self._spice.wait_for(horizontal_screen_id)
        is_at_x_end = current_horizontal_screen["atXEnd"]
        step_value = self._spice.wait_for(horizontal_scroll_bar)["position"]
        
        while (is_at_x_end is False and step_value <= 1):
            self.scroll_to_position_vertical(step_value, horizontal_scroll_bar)
            time.sleep(3)
            step_value = step_value + scrolling_value
            is_at_x_end = current_horizontal_screen["atXEnd"]

        if not is_at_x_end:
            raise Exception(f"Failed to scroll_to_rightmost_on_quickset_landing_view <{horizontal_screen_id} {horizontal_scroll_bar}>")

        logging.info(f"Success to scroll_to_rightmost_on_quickset_landing_view <{horizontal_screen_id} {horizontal_scroll_bar}>")


