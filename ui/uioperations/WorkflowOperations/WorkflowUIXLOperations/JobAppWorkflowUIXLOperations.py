from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowUICommonOperations import JobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowObjectIds import JobAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
import time


class JobAppWorkflowUIXLOperations(JobAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    def mismatch_alert_hold_job(self):
        '''
        On the mismatch alert, click on hold job button
        '''  
        try:
            try:
                button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_hold_button)
                button.mouse_click()
            except:
                button = self.spice.wait_for(JobAppWorkflowObjectIds.pause_button)
                button.mouse_click()
        except:
            option_button=self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_options_button)
            option_button.mouse_click()
            button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_hold_button)
            button.mouse_click()

    
    def delete_job_ui(self, net):
        '''
        Delete a job from the job details view.
        '''
        #Make sure we are on the correct view
        self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
        #Click on the delete button
        self.spice.wait_for(JobAppWorkflowObjectIds.delete_button).mouse_click()
        assert self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button)
        self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button).mouse_click()
        job_view = self.spice.wait_for(JobAppWorkflowObjectIds.job_view, timeout=40)
        self.spice.wait_until(lambda:job_view["visible"])
        assert self.spice.wait_for(JobAppWorkflowObjectIds.job_view, timeout=10)
    

        

