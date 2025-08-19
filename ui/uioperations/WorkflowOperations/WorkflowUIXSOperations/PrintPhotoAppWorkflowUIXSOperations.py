from dunetuf.ui.uioperations.WorkflowOperations.PrintPhotoAppWorkflowUICommonOperations import PrintPhotoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintPhotoAppWorkflowObjectIds import PrintPhotoAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
import logging

class PrintPhotoAppWorkflowUIXSOperations(PrintPhotoAppWorkflowUICommonOperations):
    def __init__(self, spice):
        """
        PrintFromUsbAppUIXSOperations class to initialize print from usb options operations.
        @param spice:
        """
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.home_screen_view = PrintPhotoAppWorkflowObjectIds.home_screen_view
