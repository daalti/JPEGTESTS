from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowUICommonOperations import SharePointAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.ScanAppWorkflowUIXSOperations import ScanAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations


class SharePointAppWorkflowUIXSOperations(SharePointAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUIXSOperations(self.spice)
        self.workflow_common_operations = WorkflowUICommonXSOperations(self.spice)

