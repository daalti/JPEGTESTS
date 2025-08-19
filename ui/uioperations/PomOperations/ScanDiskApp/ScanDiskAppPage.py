from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class ScanDiskAppPage(BasePage):

    def __init__(self, spice):
        super(ScanDiskAppPage, self).__init__(spice)
        self.locators = Locators()
    
    def get_scan_disk_app(self):
        logging.info("Waiting for scan disk app")
        scan_disk_app = self.spice.wait_for(self.spice.scan_disk_app.locators.ui_scan_disk_app)
        return scan_disk_app

    def start_scan(self) -> None:
        logging.info("Starting scan to disk")
        self.spice.scan_disk_app.wait_and_click_on_middle(self.spice.scan_disk_app.locators.scan_button) 