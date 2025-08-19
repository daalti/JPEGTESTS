import logging
from time import sleep, time
from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowObjectIds import JobStorageAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowUICommonOperations import JobStorageAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations

class JobStorageAppWorkflowUILOperations(JobStorageAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUILOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
