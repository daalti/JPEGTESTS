from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class SuppliesAppPage(BasePage):

    def __init__(self, spice):
        super(SuppliesAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_supplies_app(self):
        logging.info("Waiting for supplies app")
        supplies_app = self.spice.wait_for(self.spice.supplies_app.locators.ui_supplies_app)
        return supplies_app