import logging

from dunetuf.qmltest.QmlTestServer import QmlTestServerItem, QmlTestServerError
from ..Page import Page

class Button():
    def __init__(self, page:Page, button_locator:str) -> None:
        self.__page:Page = page
        self.locator:str = button_locator

    def click(self, click_center:bool = True) -> bool:
        return self.__page.wait_and_click(self.locator, click_center=click_center)

    def get_element(self) -> QmlTestServerItem:
        return self.__page.wait_for_element(self.locator)

    def get_text(self) -> str:
        ''' Gets text on the button (if any)'''
        return self.__page.get_locator_attribute(self.locator + "", self.__page.Attribute.Text)