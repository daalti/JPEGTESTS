from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from ..Base.BasePage import BasePage
from .Locators import Locators
import logging


class MainWorkflowOperations(BasePage):
    def __init__(self, spice):
        super(MainAppPage, self).__init__(spice)
        self.locators = Locators()

class MainWorkflowOperations(BasePage):
    def __init__(self, spice):
        super(MainAppPage, self).__init__(spice)
        self.locators = Locators()

class MainAppPage(BasePage):

    def __init__(self, spice):
        super(MainAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_home(self):
        logging.info("Waiting for home app")
        home_app = self.spice.wait_for(self.spice.main_app.locators.ui_main_app)
        return home_app

    def scroll_to_find(self, locator: str) -> None:
        if self.spice.uitype == "Workflow2":
            self.spice.home_operations.home_navigation(locator)
        else:
            #get viewport size
            screen_width = self.spice.main_app.get_property_of_element(self.spice.main_app.locators.home_dock_area, "width")
            #get total width of the scroll area
            screen_total_width = self.spice.main_app.get_property_of_element(self.spice.main_app.locators.home_dock_hscroll, "cumulativeWidthDock")

            #move scrollbar to postion 0
            scrollbar = self.spice.wait_for(self.spice.main_app.locators.home_dock_hscrollbar)
            scrollbar.__setitem__("position", "0")

            #location of element = x of the element + width of element
            element_id = locator.strip("MouseArea")
            location_element = self.spice.main_app.get_property_of_element(element_id,"x")
            location_element_width = self.spice.main_app.get_property_of_element(element_id,"width")
            location_element_width = location_element + location_element_width

            #location exceeds screenwidth, scrolling needs to be done
            if (location_element_width > screen_width):
                if screen_total_width > 0:
                    #scroll according to item location
                    pos = location_element/screen_total_width
                else:
                    #default ratio 0.55 if screen_total_width is invalid
                    pos = 0.55
                logging.info("Item is out of Viewport")
                #moving the scroll bar by ratio (Scale: 0-1.0)
                scrollbar.__setitem__("position", str(pos))

    def goto_menu_app(self) -> None:
        logging.info("Going to menu app")
        self.spice.home_operations.goto_home_menu()

    def goto_menu_app_floating_dock(self) -> None:
        logging.info("Go to menu app from floating dock")
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.menu_app_button_floating_dock)

    def goto_info_app(self) -> None:
        logging.info("Going to info app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.info_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.info_app_button)

    def goto_network_app(self) -> None:
        logging.info("Going to network app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.network_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.network_app_button)

    def goto_supplies_app(self) -> None:
        logging.info("Going to supplies app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.supplies_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.supplies_app_button)

    def goto_media_app(self) -> None:
        logging.info("Going to media app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.media_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.media_app_button)

    def goto_scan_usb_app(self) -> None:
        logging.info("Going to scan usb app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.scan_usb_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.scan_usb_app_button)

    def goto_scan_disk_app(self) -> None:
        logging.info("Going to scan disk app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.scan_disk_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.scan_disk_app_button)

    def goto_copy_app(self) -> None:
        logging.info("Going to copy app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.copy_app_button)
        if self.spice.uitype != "Workflow2":
            self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.copy_app_button)

    def goto_job_queue_app(self) -> None:
        logging.info("Going to job queue app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.job_queue_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.job_queue_app_button)
    
    def goto_job_storage_app(self) -> None:
        logging.info("Going to job storage app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.job_storage_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.job_storage_app_button)
    
    def goto_gallery_app(self) -> None:
        logging.info("Going to gallery app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.gallery_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.gallery_app_button)

    def goto_quick_forms_app(self) -> None:
        logging.info("Going to quick forms app")
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.quick_forms_app_button)
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.quick_forms_app_button)
