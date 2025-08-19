"""
Implementation Folder Widget Workflow UI methods
"""
import logging
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FolderWidgetWorkflowUICommonOperations import FolderWidgetWorkflowUIOperations


class FolderWidgetWorkflowUIXLOperations(FolderWidgetWorkflowUIOperations):
    """
    FolderWidgetWorkflowUIXLOperations module for Workflow Operations on Folder widget
    """
    def __init__(self, spice):
        self.maxtimeout = 100
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self.spice)
