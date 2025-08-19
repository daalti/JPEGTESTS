from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowUICommonOperations import QuicksetsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.WorkflowUICommonLOperations import WorkflowUICommonLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.MenuAppWorkflowUILOperations import MenuAppWorkflowUILOperations


class QuicksetsAppWorkflowUILOperations(QuicksetsAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = WorkflowUICommonLOperations(self._spice)
        self.homemenu = MenuAppWorkflowUILOperations(self._spice)
