from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class MediaAppPage(BasePage):

    def __init__(self, spice):
        super(MediaAppPage, self).__init__(spice)
        self.locators = Locators()
           
    def get_media_app(self):
        logging.info("Waiting for media app")
        media_app = self.spice.wait_for(self.spice.media_app.locators.ui_media_app)
        return media_app        

