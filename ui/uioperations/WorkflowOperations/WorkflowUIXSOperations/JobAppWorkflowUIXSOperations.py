from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowUICommonOperations import JobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowObjectIds import JobAppWorkflowObjectIds


class JobAppWorkflowUIXSOperations(JobAppWorkflowUICommonOperations):
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

        # Click on cancel button
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.size_mismatch_cancel_option3)
        cancel_button.mouse_click()
