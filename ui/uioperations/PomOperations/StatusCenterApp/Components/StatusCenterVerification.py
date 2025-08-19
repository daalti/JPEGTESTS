from ...SignInApp.Components.Verification import Verification
from ...SignInApp.Page import Page
from ..Locators import Locators

import logging
import time

class StatusCenterVerification():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__verification = Verification(page)

    def on_page(self) -> bool:
        if self.__verification.verify(Locators.NotificationCenterView, verify_active_focus=False) == False:
            return False
        
        state = self.__page.get_locator_attribute(Locators.NotificationCenterView, self.__page.Attribute.State)
        timeout = Page.DEFAULT_TIMEOUT

        """
            NOTE: We use a 'time.sleep(1)' here to make sure we are waiting a second before checking to see if
                  the status center is expanded. The status center can take a few seconds to expand fully.
        """

        while state == Locators.StatusCenterState.Collapsed.value and timeout > 0:
            state = self.__page.get_locator_attribute(Locators.NotificationCenterView, self.__page.Attribute.State)
            timeout -= 1
            time.sleep(1)

        return state == Locators.StatusCenterState.Expanded.value

    def on_confirm_sign_out_page(self) -> bool:
        return self.__verification.verify(Locators.ConfirmSignOutView, verify_active_focus=True)

    def sign_in_button_present(self) -> bool:
        if self.__verification.verify(Locators.SignInButton, verify_active_focus=False) == False: return False
        return self.__page.get_locator_attribute(Locators.SignInButtonText, self.__page.Attribute.Text) == "Sign In"

    def sign_out_button_present(self) -> bool:
        if self.__verification.verify(Locators.SignOutButton, verify_active_focus=False) == False:
            logging.error("Failed to find Status Center Sign Out button")
            return False
        return self.__page.get_locator_attribute(Locators.SignOutButton, self.__page.Attribute.Text) == "Sign Out"
