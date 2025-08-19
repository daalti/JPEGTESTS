import logging
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.StorageJobAppWorkflowUICommonOperations import StorageJobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations

class StorageJobAppWorkflowUISOperations(StorageJobAppWorkflowUICommonOperations):
    """StorageJobAppWorkflowUISOperations class to initialize StorageJob workflow operations."""

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self.spice)
        self.homemenu = spice.menu_operations
    
    def detailed_storeJob_selected(self):
        self.job_storage_click_button("continueButton")
        self.spice.wait_for('#DetailPanel')

    def delete_all_store_jobs(self, dunestorejob):
        """
        Select all the store jobs in print from job storage app
        """
        storeJobs = dunestorejob.get_all()
        logging.info(f"No of store jobs are: {len(storeJobs)}")
        assert len(storeJobs) > 0, 'No stored jobs found!'
        
        for storeJob in storeJobs:
            logging.info(f"Deleting store job: {storeJob}")
            storedJobId = storeJob.get('jobId')
            super().select_job_from_storage(storedJobId)
            
        self.delete_storeJob_selected()    