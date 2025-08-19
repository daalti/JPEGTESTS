
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowUICommonOperations import ContactsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations

class ContactsAppWorkflowUIXSOperations(ContactsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)