from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowUICommonOperations import NetworkFolderAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ScanAppWorkflowUIMOperations import ScanAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class NetworkFolderAppWorkflowUIMOperations(NetworkFolderAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUIMOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

