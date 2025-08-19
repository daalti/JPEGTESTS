from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class MenuAppPage(BasePage):

    def __init__(self, spice):
        super(MenuAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_menu_app(self):
        logging.info("Waiting for menu app")
        menu_app = self.spice.wait_for(self.spice.menu_app.locators.ui_menu_app)
        return menu_app