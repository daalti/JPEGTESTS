from ...SignInApp.Components.Verification import Verification
from ...SignInApp.Page import Page
from ..Locators import Locators

import logging

class FaxPageVerification():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__verification = Verification(page)

    def on_page(self) -> bool:
        if self.__verification.verify(Locators.SendFaxApplicationStackView) == False:
            logging.error(f"Failed to find Fax Application View: \'{Locators.SendFaxApplicationStackView}\'")
            return False
        return True

    def on_checking_for_fax_setup_page(self) -> bool:
        if self.__verification.verify(Locators.CheckingForFaxSetupView) == False:
            logging.error(f"Failed to find Checking Fax Setup View: \'{Locators.CheckingForFaxSetupView}\'")
            return False
        return True

    def on_send_recipients_page(self) -> bool:
        if self.__verification.verify(Locators.SendRecipientsView) == False:
            logging.error(f"Failed to find Fax Send Recipients View: \'{Locators.SendRecipientsView}\'")
            return False
        return True
    
    def on_fax_configure_alert_page(self) -> bool:
        if self.__verification.verify(Locators.FaxNotConfiguredAlertView) == False:
            logging.warning(f"Failed to find Fax Not Configured Alert View: \'{Locators.FaxNotConfiguredAlertView}\'")
            return False
        return True