from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowUICommonOperations import JobStorageAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ScanAppWorkflowUISOperations import ScanAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WorkflowUICommonSOperations import WorkflowUICommonSOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowObjectIds import JobStorageAppWorkflowObjectIds
import time
from time import sleep
import logging
class JobStorageAppWorkflowUISOperations(JobStorageAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUISOperations(self.spice)
        self.workflow_common_operations = WorkflowUICommonSOperations(self.spice)
        self.homemenu = spice.menu_operations

    def input_pin_in_landing_view(self, pin):
        """
        input for pin  in landing view, UI should in Scan to job storage landing view
        @param: job_name: str
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.3, JobStorageAppWorkflowObjectIds.scrollbar_scan_to_job_storage_landing_page)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_pin_model)
        current_button.mouse_click()
        keyboard_view = self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        job_name_textbox = self.spice.wait_for(f"{JobStorageAppWorkflowObjectIds.textbox_job_pin_field} {JobStorageAppWorkflowObjectIds.textbox_job_pin_model}")
        job_name_textbox.__setitem__('displayText', pin)
        try:
            ok_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
            ok_button.mouse_click()
        except  TimeoutError:
            logging.info('keypad is not displayed')
    
    def click_on_pin_text_field(self):
        """
        click on pin text field
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.3, JobStorageAppWorkflowObjectIds.scrollbar_scan_to_job_storage_landing_page)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_pin_model)
        current_button.mouse_click()
    
    def go_to_more_options(self):
        """
        Go to more options
        """
        option_button =  self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options_detail_panel)
        self.spice.wait_until(lambda: option_button["enabled"] == True, 15)
        self.spice.wait_until(lambda: option_button["visible"] == True, 15)
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options_detail_panel).mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options_view)
        logging.info("UI: At Options list screen")