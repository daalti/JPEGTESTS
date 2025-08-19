import logging

from ..SignInApp.Page import Page
from .Components.JobsPageVerification import JobsPageVerification
from ..SignInApp.Components.Button import Button
from .Locators import Locators

class JobsAppPage(Page):
    def __init__(self, spice):
        super(JobsAppPage, self).__init__(spice)
        self.verify = JobsPageVerification(self)
        self.__jobs_home_button = Button(self, Locators.JobsHomeButton)

    def click_home_button(self) -> bool:
        logging.debug(f"Clicking Jobs Home Button: {self.__jobs_home_button.locator}")
        return self.__jobs_home_button.click()