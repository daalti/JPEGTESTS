from .Locators import Locators
from .Components.StatusCenterVerification import StatusCenterVerification
from ..SignInApp.Page import Page
from ..SignInApp.Components.SignIn import SignIn

import logging
import time

class StatusCenterApp(Page, SignIn):
    def __init__(self, spice) -> None:
        super(StatusCenterApp, self).__init__(spice)
        self.verify = StatusCenterVerification(self)

    def __click_status_center(self) -> bool:
        if self.wait_and_click(Locators.ClickableStatusCenterRectangleBar, click_center=False) == False:
            logging.debug(f"Failed to click Status Center bar: {Locators.ClickableStatusCenterRectangleBar}")
            return False
        return True

    def expand(self) -> bool:
        logging.debug("Expanding Status Center...")
        notification_view = self.wait_for_element(Locators.NotificationCenterView)
        if notification_view == None: return False
        if self.check_element(notification_view, self.Attribute.Visible, True) == False:
            logging.error("Status Center bar is not visible")
            return False
        
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if current_state == Locators.StatusCenterState.Expanded.value:
            logging.debug("Status Center is already expanded")
            return True

        if current_state != Locators.StatusCenterState.Collapsed.value:
            logging.debug(f"Unrecognized Status Center state: {current_state}")
            return False

        # Status Center is collapsed. Expand it.
        if self.__click_status_center() == False: return False

        return self.verify.on_page()

    def collapse(self) -> bool:
        logging.debug("Collapsing Status Center...")
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if self.verify.on_page() == False and current_state == Locators.StatusCenterState.Collapsed.value:
            logging.debug("Status Center already collapsed")
            return True

        if current_state != Locators.StatusCenterState.Expanded.value:
            logging.debug(f"Unrecognized Status Center state: {current_state}")
            return False

        # Status Center is expanded. Collapse it.
        if self.__click_status_center() == False: return False

        return self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State) == Locators.StatusCenterState.Collapsed.value

    def click_sign_in(self) -> bool:
        logging.debug("Clicking Sign In Button in Status Center...")
        return self.wait_and_click(Locators.SignInButton)

    def click_sign_out(self) -> bool:
        logging.debug("Clicking Sign Out Button in Status Center...")
        return self.wait_and_click(Locators.SignOutButton)

    def click_confirm_sign_out_yes(self) -> bool:
        logging.debug("Clicking Confirm Sign Out 'Yes' button...")
        return self.wait_and_click(Locators.ConfirmSignOutYesButton)

    def click_confirm_sign_out_no(self) -> bool:
        logging.debug("Clicking Confirm Sign Out 'No' button...")
        return self.wait_and_click(Locators.ConfirmSignOutNoButton)
    
    def goto_sign_in_app(self) -> bool:
        logging.debug("Go to sign-in app...")
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if current_state == Locators.StatusCenterState.Collapsed.value:
            self.__click_status_center()
            if not self.verify.on_page(): return False
        
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if current_state == Locators.StatusCenterState.Expanded.value:
            if not self.click_sign_in(): return False
        else:
            logging.critical(f"StatusCenterApp.py: Failed to go to sign-in app. Unexpected status center state: {current_state}. Expected 'Expanded'")
            return False
        return True

    def sign_out(self) -> bool:
        logging.debug("Sign out...")
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if current_state == Locators.StatusCenterState.Collapsed.value:
            if not self.__click_status_center(): return False
        
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        if current_state == Locators.StatusCenterState.Expanded.value:
            if not self.click_sign_out(): return False
            if not self.verify.on_confirm_sign_out_page(): return False
            if not self.click_confirm_sign_out_yes(): return False
        else:
            logging.critical(f"StatusCenterApp.py: Failed to click sign out. Unexpected status center state: {current_state}. Expected 'Expanded'")
            return False
        
        return self.collapse()
    
    def is_expanded(self) -> bool:
        notification_view = self.wait_for_element(Locators.NotificationCenterView)
        if notification_view == None:
            logging.error("Failed to get Status Center View")
            return False
        if self.check_element(notification_view, self.Attribute.Visible, True) == False:
            logging.error("Status Center bar is not visible")
            return False
        
        current_state = self.get_locator_attribute(Locators.NotificationCenterView, self.Attribute.State)
        return current_state == Locators.StatusCenterState.Expanded.value
    
    def is_signed_in(self) -> bool:
        is_status_center_expanded = self.is_expanded()
        signed_in = False

        if not is_status_center_expanded:
            if not self.expand():
                logging.error("Failed to expand Status Center")
                return False
            time.sleep(10)
            if not self.check_locator(Locators.NotificationCenterView, self.Attribute.State, Locators.StatusCenterState.Expanded.value):
                logging.error("Failed to expand Status Center")
                return False

        # Check that Sign Out button is present
        sign_out_button = self.wait_for_element(Locators.SignOutButton)
        if sign_out_button != None:
            signed_in = True
        
        if not is_status_center_expanded:
            if not self.collapse():
                logging.error("Failed to collapse Status Center")
                return False
            time.sleep(10)
            if not self.check_locator(Locators.NotificationCenterView, self.Attribute.State, Locators.StatusCenterState.Collapsed.value):
                logging.error("Failed to collapse Status Center")
                return False
        
        return signed_in

