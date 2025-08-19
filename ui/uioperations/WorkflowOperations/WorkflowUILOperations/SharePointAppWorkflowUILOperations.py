import logging
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowUICommonOperations import SharePointAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations

class SharePointAppWorkflowUILOperations(SharePointAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUILOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations


    # Scan to SharePoint flow operations
    # Navigation from Home screen 
    def goto_scan_to_sharepoint(self):
        '''
        Navigates to Scan then SharePoint screen starting from Home screen.
        UI Flow is Home->Scan->SharePoint
        '''
        self.scan_operations.goto_scan_app()
        sleep(3)
        self.workflow_common_operations.scroll_position(SharePointAppWorkflowObjectIds.view_scan_screen, SharePointAppWorkflowObjectIds.scan_sharepoint_app, SharePointAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , SharePointAppWorkflowObjectIds.scanFolderPage_column_name , SharePointAppWorkflowObjectIds.scanFolderPage_Content_Item)
        self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app, timeout = 20.0)
        current_button = self.spice.query_item(SharePointAppWorkflowObjectIds.scan_sharepoint_app + " MouseArea")
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout = 30.0)
        current_button.mouse_click() 
        sleep(3)
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_quickset_initial_list,timeout=16.0)
        logging.info("UI: At Scan to sharepoint listview screen")

    def click_preview_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_panel)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_preview)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.button_scan_landing_preview + " MouseArea")
        current_button.mouse_click()

    def verify_scan_sharepoint_not_setup(self):
        '''
        Verify Not setup message for sharepoint.
        UI flow is from Home screen and reaches not setup view.
        '''
        if self.spice.is_HomeScreen():
            self.scan_operations.goto_scan_app()
            assert self.spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_app)
            current_button = self.spice.query_item(SharePointAppWorkflowObjectIds.scan_sharepoint_app + " MouseArea")
            current_button.mouse_click()
        assert self.spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepointapp_not_setup)
        sleep(1)
        current_button = self.spice.query_item(SharePointAppWorkflowObjectIds.button_scan_sharepoint_not_setup_ok)
        current_button.mouse_click()
