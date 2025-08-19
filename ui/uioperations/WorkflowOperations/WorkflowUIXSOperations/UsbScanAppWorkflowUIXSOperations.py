from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowUICommonOperations import UsbScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.UsbScanAppWorkflowObjectIds import UsbScanAppWorkflowObjectIds


class UsbScanAppWorkflowUIXSOperations(UsbScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = WorkflowUICommonXSOperations(self.spice)

    def goto_usb_quickset_view(self):
        '''
        This is helper method to goto usb quickset
        UI flow Select Landing-> click on any quickset button
        '''
        # for workflow, default quickset will not displayed in quickset list view, need't go to quickset list view.
        if not self.is_quickset_existing():
            return

        self.workflow_common_operations.scroll_to_rightmost_on_quickset_landing_view(UsbScanAppWorkflowObjectIds.quickset_selection_view, UsbScanAppWorkflowObjectIds.quickset_selection_view_horizontal_bar)

        view_all_btn = self.spice.wait_for(UsbScanAppWorkflowObjectIds.view_all_locator)
        self.spice.wait_until(lambda:view_all_btn["visible"] is True)
        view_all_btn.mouse_click()

        self.spice.wait_for(UsbScanAppWorkflowObjectIds.defaults_and_quick_sets_view)




