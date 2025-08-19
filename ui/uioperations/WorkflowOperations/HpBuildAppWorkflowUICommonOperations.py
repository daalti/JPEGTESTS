from dunetuf.ui.uioperations.BaseOperations.IHpBuildAppUIOperations import IHpBuildAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HpBuildAppWorkflowObjectIds import HpBuildAppWorkflowObjectIds

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

from time import sleep
import logging

class HpBuildAppWorkflowUICommonOperations(IHpBuildAppUIOperations):
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    # Scan to HpBuild flow operations
    # Navigation from Home screen
    def goto_scan_to_hpbuild(self):
        '''
        Navigates to Scan then HpBuild screen starting from Home screen.
        UI Flow is Home->Scan->HpBuild
        '''
        self.scan_operations.goto_scan_app()
        sleep(3)
        self.workflow_common_operations.scroll_position(HpBuildAppWorkflowObjectIds.view_scan_screen, HpBuildAppWorkflowObjectIds.scan_hpbuild_app, HpBuildAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , HpBuildAppWorkflowObjectIds.scanFolderPage_column_name , HpBuildAppWorkflowObjectIds.scanFolderPage_Content_Item)
        current_button = self.spice.wait_for(HpBuildAppWorkflowObjectIds.scan_hpbuild_app + " MouseArea")
        current_button.mouse_click() 
        sleep(3)
        logging.info("UI: At Scan to hpbuild listview screen")