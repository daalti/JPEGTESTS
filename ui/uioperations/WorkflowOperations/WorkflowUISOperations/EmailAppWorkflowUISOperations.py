from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowUICommonOperations import EmailAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations

class EmailAppWorkflowUISOperations(EmailAppWorkflowUICommonOperations):
    def __init__(self, spice):
        super(EmailAppWorkflowUISOperations, self).__init__(spice)
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations







