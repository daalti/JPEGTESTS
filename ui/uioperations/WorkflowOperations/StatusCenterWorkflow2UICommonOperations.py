#########################################################################################
# @file      StatusCenterWorkflow2UICommonOperations.py
# @author    Ramya Sadasivan (ramya.sadasivan1@hp.com)
# @date      Oct 8, 2024
# @brief     Implementation of Status Center Workflow2 UI navigation methods
# (c) Copyright HP Inc. 2024. All rights reserved.
###########################################################################################
"""
Implementation Sign In Workflow UI navigation methods
"""
import logging
from time import sleep
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.BaseOperations.IStatusCenterUIOperations import IStatusCenterUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflow2UICommonOperations import SignInAppWorkflow2UIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflow2ObjectIds import StatusCenterWorkflow2ObjectIds

class StatusCenterWorkflow2UICommonOperations(IStatusCenterUIOperations):
    """
    SignInAppWorkflowUIOperations module for Workflow2 Operations on SignInApp
    """
    def __init__(self, spice, cdm):
        self.maxtimeout = 100
        self.spice = spice
        self.cdm = cdm
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_sign_in_common_operations = SignInAppWorkflow2UIOperations(self.spice)

    def goto_sign_in_app(self, action:str):
        '''
        UI should be on home screen before calling this method
        Navigate to Sign In via Peristent Header

        Navigation: Home Screen > Peristent Header

        Arguments:
            action (string): either "Sign In" or "Sign Out"
        '''
        self.spice.goto_homescreen()

        sign_in_button = self.get_sign_in_button(action)

        logging.info(f"Sign In button: {sign_in_button}")
        assert sign_in_button != None, logging.error(f"Sign In button does not match what was requested")

        sign_in_button.mouse_click()

    def get_sign_in_button(self, action:str):
        '''
        UI should be on Status Center before calling this method
        Get button on Status Center that either says "Sign In" or "Sign Out"

        Navigation: Stays on current page

        Arguments:
            action (string): either "Sign In" or "Sign Out"
        '''
        button = None
        if action == "Sign In":
            button_name = StatusCenterWorkflow2ObjectIds.button_sign_in
        elif action == "Sign Out":
            button_name = StatusCenterWorkflow2ObjectIds.button_sign_out
        else:
            return None

        try:
            button = self.spice.wait_for(button_name, timeout=25.0)
            self.spice.wait_until(lambda: button["visible"] == True)
        except QmlItemNotFoundError:
            logging.info("Failed to find the Sign In/Out button.")
            return None
        
        return button


    def compare_homescreen_and_status_center_sign_in_buttons(self, spice):
        """
            Compares two sign in buttons to see if they both are "Sign In" buttons or "Sign Out" buttons
            Returns True if they are the same and False otherwise
        """
        return True

    def get_sign_in_button_text(self):
        """
            Get the text of the sign in button on the status center

            Arguments:
                None

            Returns:
                string: "Sign In" or "Sign Out"
        """

        current_value = None

        # Try to get "Sign In" button
        try:
            self.spice.wait_for(StatusCenterWorkflow2ObjectIds.button_sign_in)
            current_value = "Sign In"
        except QmlItemNotFoundError:
            pass
        except TimeoutError:
            pass

        # If you can't get "Sign In" button, then try to get "Sign Out" button
        try:
            self.spice.wait_for(StatusCenterWorkflow2ObjectIds.button_sign_out)
            current_value = "Sign Out"
        except QmlItemNotFoundError:
            pass
        except TimeoutError:
            pass

        return current_value
    
    def expand(self):
        """
            Expand the Status Center
        """
        pass

    def wait_for_warning_prompt(self, confirm:bool, timeout:int=10, checkHomeScreen:bool=True):
        """
            confirm:bool - True = click Yes, False = click No
        """
        # TODO Need to verify the toast message and remove the sleep in future
        sleep(5)
        pass

    def is_status_center_visible(self):
        """
            Check if the status center is visible
        """
        return False
    
    def collapse(self):
        """
            Collapse the Status Center
        """
        pass
    
    def cancel_job_from_persistent_header(self, job):
        """
            Cancel the job from the persistent header
        """
        try:
            #Make sure the job Button is seen
            print("Finding Job Button from Persistent Header")
            jobButton = self.spice.wait_for(StatusCenterWorkflow2ObjectIds.job_button)
            print("Job Button found")
            self.spice.wait_until(lambda: jobButton["visible"] == True, 10)
            print("Job Button is visible")
            jobButton.mouse_click()

            #Wait for JobQueueApp to open up
            self.spice.wait_for(StatusCenterWorkflow2ObjectIds.jobQueueApp)["text"] == "In Progress"

            #get job List and last job
            job_queue = job.get_job_queue()
            job_id = job_queue[-1]["jobId"]

            #Go to the job and cacnel it
            self.spice.job_ui.goto_created_job(job_id)
            self.spice.job_ui.cancel_selected_job()
        finally:
            self.spice.goto_homescreen()

    def click_on_reset_session_button(self):
        """
            Click on the ResetButton via Persistent Header
                - If the UI size is Medium (M), Large (L), or Extra Large (XL), it directly clicks the Reset button available in the persistent header.
                - For smaller UI sizes, it first opens the "More Options" menu and then selects the Reset option.
        """
        if self.spice.uisize in ["M", "L", "XL"] :
            self.spice.wait_for(StatusCenterWorkflow2ObjectIds.button_reset_Session)
            reset_button = self.spice.query_item(StatusCenterWorkflow2ObjectIds.button_reset_Session)
            self.spice.wait_until(lambda: reset_button["visible"] == True)
            reset_button.mouse_click()
        else :
            more_options_button = self.spice.wait_for(StatusCenterWorkflow2ObjectIds.persistent_header_more_options_button)
            self.spice.wait_until(lambda: more_options_button["visible"] == True)
            more_options_button.mouse_click()
            self.spice.wait_for(StatusCenterWorkflow2ObjectIds.persistent_header_more_options_dialog)
            reset_option = self.spice.wait_for(StatusCenterWorkflow2ObjectIds.reset_session_button)
            self.spice.wait_until(lambda: reset_option["visible"] == True)
            reset_option.mouse_click()
 
    def click_alert_in_alert_app(self, index):
        """
            Click the alert in the alert app
        """
        alertButton = self.spice.wait_for(StatusCenterWorkflow2ObjectIds.alert_button)
        self.spice.wait_until(lambda: alertButton["visible"] == True)
        alertButton.mouse_click()
        self.spice.wait_for("#alertAppView #alertAppHeader")
        self.spice.wait_for("#alertAppView #alert"+str(index))
        alert0 = self.spice.wait_for("#alertAppView #alert"+str(index))
        alert0.mouse_click()

    def click_persistent_header_reset_button(self):
        """
            Click the reset button in the persistent header
        """
        self.spice.wait_for(StatusCenterWorkflow2ObjectIds.button_reset_Session)
        resetButton = self.spice.query_item(StatusCenterWorkflow2ObjectIds.button_reset_Session)
        self.spice.wait_until(lambda: resetButton["visible"] == True)
        resetButton.mouse_click()