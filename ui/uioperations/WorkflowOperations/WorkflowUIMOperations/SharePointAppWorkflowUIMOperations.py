from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowUICommonOperations import SharePointAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ScanAppWorkflowUIMOperations import ScanAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class SharePointAppWorkflowUIMOperations(SharePointAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUIMOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations
        

