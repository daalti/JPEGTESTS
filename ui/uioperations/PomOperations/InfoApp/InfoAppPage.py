from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class InfoAppPage(BasePage):

    def __init__(self, spice):
        super(InfoAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_info_app(self):
        logging.info("Waiting for info app")
        info_app = self.spice.wait_for(self.spice.info_app.locators.ui_info_app)
        return info_app

