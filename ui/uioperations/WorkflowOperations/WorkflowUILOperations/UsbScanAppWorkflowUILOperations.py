from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowUICommonOperations import UsbScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowObjectIds import UsbScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from time import sleep
import logging

class UsbScanAppWorkflowUILOperations(UsbScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice=spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    def goto_usb_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        # at present, click function cannot click item when have 3 quickset in list and after invoking below method
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return
        
        view_all_btn = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_all_locator)
        view_all_btn.mouse_click()

        self.spice.wait_for(UsbScanAppWorkflowObjectIds.quick_sets_view)

    def select_usb_quickset(self, quickset_name):
        '''
        This is helper method to select usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        quickset_item = self.spice.wait_for(UsbScanAppWorkflowObjectIds.quick_sets_view + " " + quickset_name)
        quickset_item.mouse_click()
        self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_scan_usb_landing)

    def goto_blank_page_suppression_settings_via_usb(self):
        """
        Navigates to blank_page_suppression in USB Settings screen starting from Home screen.
        UI Flow is Home->Scan->USB Drive->Options->Blank Page Suppression->(Blank Page Suppression settings screen)
        """
        self.goto_options_list_via_usb()
        sleep(2)
        self.scan_operations.goto_blank_settings()


    def check_original_side_constrained(self, net, side_mode:str, constrained_message: str = ""):
        self.scan_operations.goto_sides_settings()
        to_select_item = ScanAppWorkflowObjectIds.sides_custom_dict[side_mode][1]
        current_button = self.spice.query_item(to_select_item)  
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        super().verify_constrained_message(net,constrained_message )
        self.workflow_common_operations.back_or_close_button_press(f"{ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom} {ScanAppWorkflowObjectIds.back_button}", ScanAppWorkflowObjectIds.menu_list_scan_settings)
