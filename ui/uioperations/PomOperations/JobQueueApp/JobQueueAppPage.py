from ..Base.BasePage import BasePage
from .Locators import Locators
import logging

class JobQueueAppPage(BasePage):

    def __init__(self, spice):
        super(JobQueueAppPage, self).__init__(spice)
        self.locators = Locators()

    def get_job_queue_app(self):
        logging.info("Waiting for job queue app")
        job_queue_app = self.spice.wait_for(self.spice.job_queue_app.locators.ui_job_queue_app)
        return job_queue_app