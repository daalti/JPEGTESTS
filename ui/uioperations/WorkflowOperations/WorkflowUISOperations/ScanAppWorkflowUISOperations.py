import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM

class ScanAppWorkflowUISOperations(ScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.homemenu = spice.menu_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def goto_filetype_settings(self, dial_val: int = 180):
            """
            UI should be on Scan options list screen.
            UI Flow is File Type-> (File Type Settings screen).
            """
            self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_file_type, ScanAppWorkflowObjectIds.combobox_scan_file_type],
                                                    ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
            constrained = self.spice.query_item(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.row_object_scan_file_type}")["constrained"]
            if not constrained:
                assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
                logging.info("UI: At File Type settings screen")

    def click_on_main_action_button(self, button_object_id = ScanAppWorkflowObjectIds.button_send_detail_right_block):
        current_button = self.spice.wait_for(button_object_id)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        if button_object_id == ScanAppWorkflowObjectIds.button_preview_detail_right_block:
            self.scan_operations.click_expand_button()

    def click_on_preview_button(self):
        preview_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_preview)
        self.spice.validate_button(preview_button)
        preview_button.mouse_click()    