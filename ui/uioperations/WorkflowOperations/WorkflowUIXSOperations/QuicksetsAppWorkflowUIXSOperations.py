from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowUICommonOperations import QuicksetsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowUIXSOperations import MenuAppWorkflowUIXSOperations



class QuicksetsAppWorkflowUIXSOperations(QuicksetsAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = WorkflowUICommonXSOperations(self._spice)
        self.homemenu = MenuAppWorkflowUIXSOperations(self._spice)