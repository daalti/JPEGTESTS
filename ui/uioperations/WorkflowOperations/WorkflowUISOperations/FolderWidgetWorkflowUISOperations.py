"""
Implementation Folder Widget Workflow UI methods
"""
import logging
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.FolderWidgetWorkflowSObjectIds import FolderWidgetWorkflowSObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FolderWidgetWorkflowUICommonOperations import FolderWidgetWorkflowUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper


class FolderWidgetWorkflowUISOperations(FolderWidgetWorkflowUIOperations):
    """
    FolderWidgetWorkflowUISOperations module for Workflow Operations on Folder widget
    """
    def __init__(self, spice):
        self.maxtimeout = 100
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self.spice)


    def check_default_folder_display_name_on_widget(self, net, displayname_string_id = None, displayname = None):
        """
        Check default folder display name on folder widget
        """
        # waiting for folder widget display name
        self.spice.wait_for(FolderWidgetWorkflowSObjectIds.default_folder_displayName, timeout=7.0)
        # Verifying folder display name with param displayname
        if displayname == None:
            check_name_text = LocalizationHelper.get_string_translation(net, displayname_string_id)
        else:
            check_name_text = displayname

        self.verify_displayname_string(check_name_text)
    
    def verify_displayname_string(self, displayname):
        """
        This method compares the displayname string of network folder quickset with the expected string
        Args:
            UI should be in default network folder view
            displayname: expected displayname string
        """
        ui_displayname_string = self.spice.query_item(FolderWidgetWorkflowSObjectIds.default_folder_displayName)["text"]
        logging.info("displayname = " + ui_displayname_string)
        assert ui_displayname_string == displayname, "displayname mismatch"
