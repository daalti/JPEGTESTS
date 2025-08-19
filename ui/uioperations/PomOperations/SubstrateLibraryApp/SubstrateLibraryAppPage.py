from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class SubstrateLibraryAppPage(BasePage):

    def __init__(self, spice):
        super(SubstrateLibraryAppPage, self).__init__(spice)
        self.locators = Locators()
    
    def get_substrate_library_app(self):
        logging.info("Waiting for Substrate Library app")
        substrate_library_app = self.spice.wait_for(self.spice.substrate_library_app.locators.ui_substrate_library_app)
        return substrate_library_app