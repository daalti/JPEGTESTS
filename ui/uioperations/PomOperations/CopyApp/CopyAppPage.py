from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class CopyAppPage(BasePage):

    def __init__(self, spice):
        super(CopyAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_copy_app(self):
        logging.info("Waiting for copy app")
        copy_app = self.spice.wait_for(self.spice.copy_app.locators.ui_copy_app)
        return copy_app

    def start_copy(self) -> None:
        logging.info("Starting copy")
        self.spice.copy_app.wait_and_click_on_middle(self.spice.copy_app.locators.copy_button)

    def finish_copy(self, expanded = False) -> None:
        logging.info("Finishing copy")
        if expanded:
            self.spice.copy_app.wait_and_click_on_middle(self.spice.copy_app.locators.copy_button_expanded)
        else:
            self.spice.copy_app.wait_and_click_on_middle(self.spice.copy_app.locators.copy_button)
            
        
    def wait_and_click_setting_view(self):
        logging.info("Waiting and clicking for setting view")
        self.spice.copy_app.wait_and_click_on_middle(self.spice.copy_app.locators.options_detail_panel_button)

    def get_setting_view(self):
        logging.info("Get setting view")
        setting_view = self.spice.wait_for(self.spice.copy_app.locators.copy_settings_view)
        return setting_view

    def close_setting_view(self):
        logging.info("Closing setting view")
        self.spice.copy_app.wait_and_click_on_middle(self.spice.copy_app.locators.close_copy_settings_button)        
