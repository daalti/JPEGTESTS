import logging

from .Page import Page
from .Components.Button import Button
from .Components.SignIn import SignIn
from .Components.HomePageVerification import HomePageVerification
from ..MainApp.Locators import Locators as MainAppLocators

class HomePageApp(Page, SignIn):
    def __init__(self, spice):
        super(HomePageApp, self).__init__(spice)
        self.verify = HomePageVerification(self)
        self.__sign_in_button = Button(self, MainAppLocators.sign_in_app_button)
        self.__fax_app_button = Button(self, MainAppLocators.fax_app_button)
        self.__jobs_app_button = Button(self, MainAppLocators.job_queue_app_button)
        self.__menu_app_button = Button(self, MainAppLocators.menu_app_button)
        self.__copy_app_button = Button(self, MainAppLocators.copy_app_button)
        self.__scan_app_button = Button(self, MainAppLocators.scan_folder_app)
        self.__scan_to_email_app_button = Button(self, MainAppLocators.scan_to_email_app)
        self.__restricted_access_ok_button = Button(self, MainAppLocators.restricted_access_ok_button)
        self.__input_required_ok_button = Button(self, MainAppLocators.all_input_fields_required_ok_button)
        self.__usb_device_connected_ok_button = Button(self, MainAppLocators.usb_device_connected_ok_button)
        self.__persistent_sign_in_button = Button(self, MainAppLocators.persistent_sign_in_button)
        self.__persistent_sign_out_button = Button(self, MainAppLocators.persistent_sign_out_button)

    def __scroll_and_click(self, button:Button) -> bool:
        if self.__scroll_to_find(button.locator) == False:
            logging.error(f"Failed to scroll to locator \'{button.locator}\'")
            return False
        if button.click() == False:
            logging.error(f"Failed to click locator \'{button.locator}\'")
            return False
        return True

    def __scroll_to_find(self, locator:str) -> bool:
        logging.debug("Getting home dock screen width")
        screen_width = self.get_locator_attribute(MainAppLocators.home_dock_area, self.Attribute.Width)
        if screen_width == None:
            logging.error(f"Failed to get home dock \'{MainAppLocators.home_dock_area}\' {self.Attribute.Width}")
            return False

        logging.debug("Getting home dock entire width (including off screen)")
        screen_total_width = self.get_locator_attribute(MainAppLocators.home_dock_hscroll, self.Attribute.CumulativeWidthDock)
        if screen_total_width == None:
            logging.error(f"Failed to get home dock horizontal scroll \'{MainAppLocators.home_dock_hscroll}\' {self.Attribute.CumulativeWidthDock}")
            return False

        if self.scroll_horizontal(MainAppLocators.home_dock_hscrollbar, locator, screen_width) == False:
            logging.error(f"Failed to scroll to \'{locator}\'")
            return False

        return True

    def goto_sign_in_app(self) -> bool:
        logging.info("Navigating to Sign In app from Home page")
        if(self.wait_for_element(MainAppLocators.persistent_sign_in_button,timeout=20)):
            return self.__persistent_sign_in_button.click(False)
        elif(self.wait_for_element(MainAppLocators.persistent_sign_out_button,timeout=20)):
            return self.__persistent_sign_out_button.click(False)
        else:
            return self.__scroll_and_click(self.__sign_in_button)

    def goto_fax_app(self) -> bool:
        logging.info("Navigating to Fax app from Home page")
        return self.__scroll_and_click(self.__fax_app_button)

    def goto_jobs_app(self) -> bool:
        logging.info("Navigating to Jobs app from Home page")
        """
            NOTE: We need to scroll to the job queue app parent container
                  and then we need to click the clickable child object of the
                  parent container.
        """
        if self.__scroll_to_find(MainAppLocators.job_queue_app) == False:
            logging.error(f"Failed to scroll to locator \'{MainAppLocators.job_queue_app}\'")
            return False
        return self.__jobs_app_button.click()

    def goto_menu_app(self) -> bool:
        logging.info("Navigating to Menu app from Home page")
        return self.__scroll_and_click(self.__menu_app_button)
    
    def goto_copy_app(self) -> bool:
        logging.info("Navigating to Copy app from Home page")
        return self.__scroll_and_click(self.__copy_app_button)

    def goto_scan_app(self) -> bool:
        logging.info("Navigating to Scan app from Home page")
        return self.__scroll_and_click(self.__scan_app_button)
    
    def click_scan_to_email_app(self) -> bool:
        return self.__scroll_and_click(self.__scan_to_email_app_button)

    def click_restricted_access_ok_button(self) -> bool:
        """
            Button only appears on the Restricted Access page, which
            only prompts if you are accessing an App that you do not have
            access to.
        """
        logging.info("Clicking Restricted Access OK button...")
        return self.__restricted_access_ok_button.click()

    def click_input_required_ok_button(self) -> bool:
        """
            Button only appears on the "All input fields are required"
            page, which appears when you try to sign in without
            filling out all input fields (username field, password field, pin field, etc.)
        """
        logging.info("Clicking Input Required OK button...")
        return self.__input_required_ok_button.click()

    def click_usb_device_connected_ok_button(self) -> bool:
        logging.info("Clicking USB Device Connected OK button...")
        return self.__usb_device_connected_ok_button.click()

    def sign_out(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.select_universal_sign_out_from_home()\' method")
        return self.spice.signIn.select_universal_sign_out_from_home()

    def is_signed_in(self) -> bool:
        logging.warning("!!!!! DEPRECATED METHOD !!!!!")
        logging.warning("Using \'spice.signIn.is_signed_in()\' method")
        return self.spice.signIn.is_signed_in()
            
