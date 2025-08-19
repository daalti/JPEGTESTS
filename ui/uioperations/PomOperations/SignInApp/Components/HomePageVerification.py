from ...MainApp.Locators import Locators
from ...StatusCenterApp.Locators import Locators as StatusCenterLocators
from .Verification import Verification
from ..Page import Page
from dunetuf.localization.LocalizationHelper import LocalizationHelper

import logging
import time

class HomePageVerification():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__verification = Verification(page)
        
    def on_input_required_page(self) -> bool:
        logging.debug("Verifying we are on Input Required page...")
        if self.__verification.verify(Locators.all_input_fields_required_text_view, verify_active_focus=False) == False:
            logging.error("Failed to find All Input Fields Required page")
            return False
        text = self.__page.get_locator_attribute(Locators.all_input_fields_required_text_view, self.__page.Attribute.Text)
        if text == None: return False
        if text != Locators.all_input_fields_required_text:
            logging.error(f"All Input Fields Required page text is not what was expected.\nActual: {text}\nExpected: {Locators.all_input_fields_required_text}")
            return False
        logging.debug(f"All Input Fields Required page text: {text}")
        return True

    def on_usb_connected_page(self) -> bool:
        logging.debug("Verifying we are on the USB Device Connected page...")
        if self.__verification.verify(Locators.usb_device_connected_text_view, verify_active_focus=False) == False:
            logging.error("Failed to find USB Device Connected page")
            return False
        text = self.__page.get_locator_attribute(Locators.usb_device_connected_text_view, self.__page.Attribute.Text)
        if text == None: return False
        if text != Locators.usb_device_connected_text:
            logging.error(f"USB Device Connected page text is not what was expected.\nActual: {text}\nExpected: {Locators.usb_device_connected_text}")
            return False
        logging.debug(f"USB Device Connected page text: {text}")
        return True
