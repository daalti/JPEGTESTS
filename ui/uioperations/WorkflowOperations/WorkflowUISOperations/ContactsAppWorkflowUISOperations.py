
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowUICommonOperations import ContactsAppWorkflowUICommonOperations
# from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.MenuAppWorkflowUISOperations import MenuAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowObjectIds import ContactsAppWorkflowObjectIds


class ContactsAppWorkflowUISOperations(ContactsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
    
    def select_custom_addressbook(self,addressbook_name):
        #self.goto_more_options()
        super().select_custom_addressbook(addressbook_name)

    def click_search_button(self):
        #self.goto_more_options()
        super().click_search_button()

