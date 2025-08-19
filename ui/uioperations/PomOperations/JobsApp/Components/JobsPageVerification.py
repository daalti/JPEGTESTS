from ...SignInApp.Components.Verification import Verification
from ...SignInApp.Page import Page
from ..Locators import Locators

import logging

class JobsPageVerification():
    def __init__(self, page:Page) -> None:
        self.__page = page
        self.__verification = Verification(page)

    def on_page(self) -> bool:
        if self.__verification.verify(Locators.JobsQueueApplicationStackView) == False:
            logging.error(f"Failed to find Jobs Application View: \'{Locators.JobsQueueApplicationStackView}\'")
            return False
        return True
