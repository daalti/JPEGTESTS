import sys
import logging
import time

from dunetuf.ui.uioperations.BaseOperations.IJobUIOperations import IJobUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper


class JobAppProSelectUICommonOperations(IJobUIOperations):
    """JobAppProSelectUICommonOperations class to initialize job proselect operations."""

    def __init__(self, spice):
        self.spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self.spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self.spice)

    def goto_created_job(self, job_id):
        self.home_menu_dial_operations.menu_navigation(self.spice, "#MenuListLayout", "#ActiveJobsListView #SpiceButton", selectOption=False)
        # Spice wasn't clicking the job button directly so I had to click another object to go into the job details app.
        logging.info("Using CurrentAppText to press the button")
        button = self.spice.query_item("#CurrentAppText")
        button.mouse_click()
        self.spice.wait_for("#cancelButton")

    def cancel_selected_job(self):
        if self.spice.uitheme == "hybridTheme":
            logging.info("Using Keyhandler UDW command for Cancel button: Hybrid UI")
            self.spice.udw.mainUiApp.KeyHandler.setKeyPress("Cancel")
        else:
            self.home_menu_dial_operations.menu_navigation(self.spice, "#ActiveJobsListView", "#cancelButton")
    
    def get_job_info(self, job_id, index=0):
        return self.spice.query_item("#ActiveJobsListView #SpiceButton", index)['text']

    def goto_menu_jobs_settings(self):
        logging.error("Jobs Settings Screen in Settings Menu is not implemented")
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        return False        

    def has_lock_icon(self):
        """
        Starting from Home Screen
        """
        self.home_menu_dial_operations.goto_menu_status(self.spice)
        job_app_lock_icon_id = "#joblogButton #ContentItem SpiceImage"
        lock_icon = self.spice.wait_for(job_app_lock_icon_id)

        return lock_icon["width"] > 0
    
    def navigate_to_selectedjobdetails(self):
        # navigate to selected job details screen 
        selectedJob = self.spice.wait_for("#ActiveJobsListView")
        selectedJob.mouse_click()
        self.spice.wait_for("#cancelButton")

    def job_details_screen_navigation(self):
        # navigate to job history item and scroll up and down in details and navigate back
        selectedJob = self.spice.wait_for("#SpiceView SpiceButton")
        selectedJob.mouse_click()
        currentScreen = self.spice.wait_for("#MenuListLayout")
        scrolling_down = [currentScreen.mouse_wheel(180,180) for _ in range(10)]
        scrolling_up = [currentScreen.mouse_wheel(0,0) for _ in range(10)]

    def goto_job(self, job_id):
        '''
        Go to a job inside job queue list.
        Args:
            job_id: ID of the job to open
        '''

        # Press the Job History Button
        self.spice.homeMenuUI().menu_navigation(self.spice, "#MenuListLayout", "#joblogButton #SpiceButton", selectOption=True)
        view = self.spice.wait_for("#jobLogView")

        #Set up variables
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 180
        found = False

        #Start looking
        while found == False and (time_spent_waiting < max_timeout):
            try:
                self.home_menu_dial_operations.menu_navigation(self.spice, "#jobLogView", "#" + job_id + " #SpiceButton", selectOption=True)

                job_view = self.spice.wait_for("#jobLogInfoView")
                assert job_view["visible"] == True

                found = True
            except:
                time_spent_waiting = time.time() - start_time
        assert found


    def recover_job_status(self):
        '''
        Recover the job status text
        '''
        return self.spice.wait_for("#completionNode #ValueText")["text"]
    

    def is_job_status_expected(self, net):
        '''
        Check if the job status is the expected successful / completed value
        '''
        return self.recover_job_status() == LocalizationHelper.get_string_translation(net, "cCompletionStateTypeSuccess", 'en-US')

    def recover_job_color_mode(self):
        '''
        Recover the job color mode text. 
        However, proselect products currently don't support color mode
        '''
        return None
    def recover_job_start_time(self):
        '''
        Recover the job start time value inside the job details view.
        '''
        return self.spice.wait_for("#startTimeNode #ValueText")["text"]

    def recover_job_user_name(self):
        '''
        Recover the job user name value inside the job details view.
        '''
        return self.spice.wait_for("#userNameNode #ValueText")["text"]
    def recover_job_completion_time(self):
        '''
        Recover the job completion time value inside the job details view.
        '''
        return self.spice.wait_for("#completionNode #ValueText")["text"]

    def recover_job_type(self):
        '''
        Recover the job type value inside the job details view.
        '''
        return self.spice.wait_for("#jobTypeNode #ValueText")["text"]
