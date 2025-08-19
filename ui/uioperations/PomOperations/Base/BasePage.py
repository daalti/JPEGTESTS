import logging
from typing import ClassVar

class BasePage(object):

    WAIT_TIMEOUT: ClassVar[float] = 7
    """Default wait timeout (s)."""

    def __init__(self, spice):
        self.spice = spice

    def wait_for_it(self, locator: str) -> None:
        logging.info("Waiting for {}".format(locator))
        self.spice.wait_for(locator)

    def wait_until_it(self, locator: str) -> None:
        logging.info("Waiting until {}".format(locator))
        self.spice.wait_until(locator)

    def wait_locator_enabled(self, locator: str, timeout: float = WAIT_TIMEOUT, query_index: int = 0) -> None:
        logging.info("Waiting until locator enabled {}".format(locator))
        # Validate for object if not exist
        object = self.spice.wait_for(locator, timeout, query_index)
        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True, timeout)

    def wait_locator_disabled(self, locator: str) -> None:
        logging.info("Waiting until locator disabled {}".format(locator))
        # Validate for object if not exist
        object = self.spice.wait_for(locator)
        # Wait for not clickable situation
        self.spice.wait_until(lambda: object["enabled"] == False)

    def wait_locator_visible(self, locator: str, timeout: float = WAIT_TIMEOUT, query_index: int = 0) -> None:
        logging.info("Waiting until locator visible {}".format(locator))
        # Validate for object if not exist
        object = self.spice.wait_for(locator, timeout, query_index)
        # Wait for visible situation
        self.spice.wait_until(lambda: object["visible"] == True)

    def wait_locator_not_visible(self, locator: str) -> None:
        logging.info("Waiting until locator not visible {}".format(locator))
        # Validate for object if not exist
        object = self.spice.wait_for(locator)
        # Wait for not visible situation
        self.spice.wait_until(lambda: object["visible"] == False)

    def get_element(self, locator: str):
        logging.info("Getting element {}".format(locator))
        element = self.spice.query_item(locator)
        return element
    
    def get_element_with_index(self, locator: str, index: int):
        logging.info("Getting element {}".format(locator))
        element = self.spice.query_item(locator,index)
        return element
    
    def get_property_of_element(self, locator: str, property: str):
        logging.info("Waiting for {}".format(locator))
        return self.spice.wait_for(locator)["{}".format(property)]

    def goto(self, locator: str) -> None:
        logging.info("Going to {}".format(locator))
        navigable_element = self.spice.query_item(locator)
        navigable_element.mouse_click()

    def wait_and_click_on_middle(self, locator: str, timeout=15) -> None:
        """
        Waits for object in clickable state (visible and enabled) and
        it clicks on the middle of the object
        """
        # Validate for object if not exist
        object = self.spice.wait_for(locator, timeout)

        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True, timeout)
        self.spice.wait_until(lambda: object["visible"] == True, timeout)

        # Click on the middle of the object
        center_x = object["width"] / 2
        center_y = object["height"] / 2
        object.mouse_click(center_x, center_y)

    def goto_home(self) -> None:
        logging.info('Going to home')
        self.spice.main_app.wait_and_click_on_middle(self.spice.main_app.locators.home_button)
        
    def get_text_object(self, locator: str, property: str):
        logging.info("Waiting for {}".format(locator))         
        return self.spice.wait_for(locator + " {}".format(property))["text"]

    def wait_until_text_button(self, button_object_name: str, expected_button_string_id: str, timeout=15) -> None:
        # Wait until text of button_object_name equals expected_button_string_id
        object = self.spice.wait_for("{} {}".format(button_object_name, self.spice.copy_app.locators.property_text_button))
        self.spice.wait_until(lambda: object["text"] == expected_button_string_id, timeout)