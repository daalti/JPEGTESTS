
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowUICommonOperations import ContactsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowObjectIds import ContactsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class ContactsAppWorkflowUILOperations(ContactsAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.ContactsAppWorkflowObjectIds = ContactsAppWorkflowObjectIds()
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    def check_group_member_list_navigation(self):
        logging.info("check_group_member_list_navigation")
        # To check whether the group member list back button is navigating to landing view
        members_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.row_members)
        members_button.mouse_click()
        back_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        # To check whether back button of landing view when pressed exits the application
        if self.spice.uitype != "Workflow2":
            self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
            back_button.mouse_click()
        self.spice.wait_for("#HomeScreenView")
        
        
        
        