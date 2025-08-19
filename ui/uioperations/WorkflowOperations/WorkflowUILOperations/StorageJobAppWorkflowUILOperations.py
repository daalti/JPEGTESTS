import logging
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.StorageJobAppWorkflowUICommonOperations import StorageJobAppWorkflowUICommonOperations

class StorageJobAppWorkflowUILOperations(StorageJobAppWorkflowUICommonOperations):
    """StorageJobAppWorkflowUILOperations class to initialize StorageJob workflow operations."""

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
