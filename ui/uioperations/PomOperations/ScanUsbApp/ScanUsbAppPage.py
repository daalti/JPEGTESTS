from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class ScanUsbAppPage(BasePage):

    def __init__(self, spice):
        super(ScanUsbAppPage, self).__init__(spice)
        self.locators = Locators()
    
    def get_scan_usb_app(self):
        logging.info("Waiting for scan usb app")
        scan_usb_app = self.spice.wait_for(self.spice.scan_usb_app.locators.ui_scan_usb_app)
        return scan_usb_app

    def start_scan(self) -> None:
        logging.info("Starting scan")
        self.spice.scan_usb_app.wait_and_click_on_middle(self.spice.scan_usb_app.locators.scan_button)

    def finish_scan(self) -> None:
        logging.info("Finishing scan")
        self.spice.scan_usb_app.wait_and_click_on_middle(self.spice.scan_usb_app.locators.done_button)
     