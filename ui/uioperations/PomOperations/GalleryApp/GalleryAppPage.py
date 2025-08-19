from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class GalleryAppPage(BasePage):

    def __init__(self, spice):
        super(GalleryAppPage, self).__init__(spice)
        self.locators = Locators()
    
    def get_gallery_app(self):
        logging.info("Waiting for gallery app")
        gallery_app = self.spice.wait_for(self.spice.gallery_app.locators.ui_gallery_app)
        return gallery_app