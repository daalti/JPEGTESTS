from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowUICommonOperations import JobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowObjectIds import JobAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
import time


class JobAppWorkflowUISOperations(JobAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations


    def mismatch_alert_cancel_job(self):
        '''
        On the mismatch alert, click on cancel job button
        '''

        # Click on options button
        options_button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_options_button)
        options_button.mouse_click()

        try:
            button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_cancel_button)
        except:
            button = self.spice.wait_for(JobAppWorkflowObjectIds.size_mismatch_cancel_option3)
        button.mouse_click()

    def mismatch_alert_hold_job(self):
        '''
        On the mismatch alert, click on hold job button
        '''
        try:
            option_button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_options_button)
            option_button.mouse_click()
            button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_hold_button)
            button.mouse_click()
        except:
            button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_hold_button)
            button.mouse_click()

    def mismatch_alert_printanyway_job(self):
        '''
        On the mismatch alert, click on print anyway button
        '''
        # Click on options button
        options_button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_options_button)
        options_button.mouse_click()

        button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_printanyway_button)
        button.mouse_click()

    def verify_job_recovery_policy_index(self, spice, index):
        jobs_settings_job_recovery_mode_settings = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode_settings)
        spice.wait_until(lambda:jobs_settings_job_recovery_mode_settings["currentIndex"] == index)
    
    def cancel_selected_job(self, curing = False, supported_concurrency = 'true'):
        '''
        Cancel a job from the job details view.
        '''
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_button, 10)
        cancel_button.mouse_click()
        
        try:
            # Confirm cancel job (before print)
            cancel_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_confirmation_button)
            cancel_button_confirm.mouse_click()
        
        except:
            # Select cancel print only or cancel print and curing
            if curing == False:
                cancel_print_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_only_print_button, 10)
                cancel_print_button.mouse_click()
            else:
                cancel_print_and_curing_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_both_button, 10)
                cancel_print_and_curing_button.mouse_click()
            
            # Confirm cancel job
            cancel_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_yes_button, 10)
            cancel_button_confirm.mouse_click()
