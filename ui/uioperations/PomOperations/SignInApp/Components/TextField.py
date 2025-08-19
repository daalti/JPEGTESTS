import logging

from ..Page import Page
from ...SignInApp import Locators

class TextField():
    def __init__(self, page:Page, text_field_locator:str) -> None:
        self.__page:Page = page
        self.locator:str = text_field_locator

    def enter(self, value:str, is_display_text:bool = False) -> bool:
        element = self.__page.wait_for_element(self.locator)
        if element == None: return False
        logging.debug(f"Entering value \'{value}\' into text field \'{self.locator}\'")
        attribute = self.__page.Attribute.Text.value
        if is_display_text:
            attribute = self.__page.Attribute.DisplayText.value
        return self.__page.set_item_and_wait_for_completion(element, attribute, value)

    def click(self) -> bool:
        """
            Clicks the text field so the keyboard pops up
        """
        return self.__page.wait_and_click(self.locator)

    def get_text(self) -> str:
        text = self.__page.get_locator_attribute(self.locator + "", self.__page.Attribute.Text)
        return '' if text == None else text
    
    def get_display_text(self) -> str:
        display_text = self.__page.get_locator_attribute(self.locator + "", self.__page.Attribute.DisplayText)
        return '' if display_text == None else display_text
