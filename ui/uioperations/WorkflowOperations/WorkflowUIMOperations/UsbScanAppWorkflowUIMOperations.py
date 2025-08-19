from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowUICommonOperations import UsbScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class UsbScanAppWorkflowUIMOperations(UsbScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations





