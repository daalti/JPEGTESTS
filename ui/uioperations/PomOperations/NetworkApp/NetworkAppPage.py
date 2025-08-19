from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class NetworkAppPage(BasePage):

    def __init__(self, spice):
        super(NetworkAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_network_app(self):
        logging.info("Waiting for network app")
        network_app = self.spice.wait_for(self.spice.network_app.locators.ui_network_app)
        return network_app
