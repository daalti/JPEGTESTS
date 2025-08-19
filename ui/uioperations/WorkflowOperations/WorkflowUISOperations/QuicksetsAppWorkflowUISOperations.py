from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowUICommonOperations import QuicksetsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WorkflowUICommonSOperations import WorkflowUICommonSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.MenuAppWorkflowUISOperations import MenuAppWorkflowUISOperations

class QuicksetsAppWorkflowUISOperations(QuicksetsAppWorkflowUICommonOperations):
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = WorkflowUICommonSOperations(self._spice)
        self.homemenu = MenuAppWorkflowUISOperations(self._spice)
