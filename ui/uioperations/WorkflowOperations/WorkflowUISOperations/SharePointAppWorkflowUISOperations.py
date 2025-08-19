from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowUICommonOperations import SharePointAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ScanAppWorkflowUISOperations import ScanAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WorkflowUICommonSOperations import WorkflowUICommonSOperations


class SharePointAppWorkflowUISOperations(SharePointAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUISOperations(self.spice)
        self.workflow_common_operations = WorkflowUICommonSOperations(self.spice)

