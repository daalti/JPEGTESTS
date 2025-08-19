import logging

from .Page import Page
from .Components.Button import Button
from .Components.SignIn import SignIn
from .Components.HomePageVerification import HomePageVerification
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from enum import Enum

class HomePageAppProSelect(Page, SignIn):
    class Apps(str, Enum):
        Menu = "Menu"
        SignIn = "Sign In"
        SignOut = "Sign Out"
        Print = "Print"
        USBDrive = "USB Drive"
        Trays = "Trays"
        Supplies = "Supplies"
        Help = "Help"

    def __init__(self, spice):
        super(HomePageAppProSelect, self).__init__(spice)
        #self.verify = HomePageVerification(self)
        self.__app_list = [
            self.Apps.Menu, 
            self.Apps.SignIn,
            self.Apps.Print,
            self.Apps.USBDrive, 
            self.Apps.Trays, 
            self.Apps.Supplies, 
            self.Apps.Help]
        #self.__sign_in_button = Button(self, LocatorsProSelect.SignInButton)

    def __scroll_to(self, app) -> bool:
        home_screen = self.wait_for_element(ProSelectUIObjectIds.homeScreenView)

        if app == self.Apps.SignOut:
            app = self.Apps.SignIn
        current_app_index = self.__get_current_app_index()
        desired_app_index = self.__get_app_index(app)
        distance = current_app_index - desired_app_index
        if distance > 0:
            if not self.scroll_left_increment(home_screen, distance):
                logging.error("Failed to scroll left")
                return False
        elif distance < 0:
            if not self.scroll_right_increment(home_screen, abs(distance)):
                logging.error("Failed to scroll right")
                return False
        return True

    def __scroll_and_click(self, app) -> bool:
        if not self.__scroll_to(app): return False
        
        app_locator = self.__get_app_locator(app)
        return self.wait_and_click(app_locator)
        
    def __get_current_app_index(self) -> int:
        current_app = self.__get_current_app()
        return self.__get_app_index(current_app)
    
    def __get_app_index(self, app) -> int:
        for index, list_app in enumerate(self.__app_list):
            if list_app.value == app.value:
                return index
        logging.error(f"Failed to app find index for \'{app.value}\'")
        return -1
    
    def __get_current_app_text(self) -> str:
        return self.get_locator_attribute(ProSelectUIObjectIds.CurrentAppText, self.Attribute.Text)

    def __get_current_app(self) -> Apps:
        text = self.__get_current_app_text()
        if text == "Sign Out": return self.Apps.SignIn
        for app in self.__app_list:
            logging.info(f"App Text: {app.value}")
            if app.value == text:
                return app
        logging.error(f"Failed to find app text for \'{text}\'")
        return None
    
    def __get_app_locator(self, app):
        if app == self.Apps.SignIn or self.Apps.SignOut:
            return ProSelectUIObjectIds.SignInOkButton
        
        return None
    
    def goto_sign_in_app(self) -> bool:
        logging.info("Navigating to Sign In app from Home page")
        return self.__scroll_and_click(self.Apps.SignIn)

    def is_signed_in(self) -> bool:
        if not self.__scroll_to(self.Apps.SignOut): return False
        text = self.__get_current_app_text()
        logging.info(f"Current App Text: {text}")
        return text == "Sign Out"

    def sign_out(self) -> bool:
        logging.info("Navigating to Sign Out app from Home page")
        return self.__scroll_and_click(self.Apps.SignOut)