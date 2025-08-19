from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowUICommonOperations import QuicksetsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.WorkflowUICommonMOperations import WorkflowUICommonMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.MenuAppWorkflowUIMOperations import MenuAppWorkflowUIMOperations


class QuicksetsAppWorkflowUIMOperations(QuicksetsAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = WorkflowUICommonMOperations(self._spice)
        self.homemenu = MenuAppWorkflowUIMOperations(self._spice)