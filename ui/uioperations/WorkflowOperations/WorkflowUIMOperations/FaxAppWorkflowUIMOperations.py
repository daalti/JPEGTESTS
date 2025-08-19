
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
class FaxAppWorkflowUIMOperations(FaxAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.homeoperations = spice.home_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def select_multiple_contacts_from_local_contacts(self,payload_list):
        """
        Purpose: Selects fax contacts to send to multi destination using addressbook (send to contacts) option
        UI should be in Fax screen -> Fax Recipients screen -> Sent to Contacts
        UI Flow: Main SendToContacts -> Local -> Select Fax Recipients
        Args: record_id_list which is passed on sequentially from create_fax_multiple_contacts keyword.
        """
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        for payload in payload_list:
            # current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            AddressBook_name = payload['displayName']
            addressBook_name_item = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Row'
            addressBook_name_model = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, addressBook_name_item, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view,scroll_height=50)
            if(self.spice.wait_for(addressBook_name_model)["checked"] == False):
                current_button = self.spice.wait_for(addressBook_name_model, timeout = 10.0)
                current_button.mouse_click()
            assert self.spice.wait_for(addressBook_name_model)["checked"] == True, 'Contact is not checked'
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def goto_menu_fax_send_settings_dialing(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout =5.0)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()

        if self.is_fax_dual_line_enabled():
            line2 = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing_line2)
            line2.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list , 15)
        else:
            self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_menu_list, timeout =15.0)
    
    def fax_set_dialing_prefix(self, prefix, index_val=0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        self.fax_scroll_bar_move_to_bottom()
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        # to check if alredy has prefix
        try:
            self.spice.query_item(f"{FaxAppWorkflowObjectIds.text_field_dialing_prefix} {FaxAppWorkflowObjectIds.item_in_text_field_dialing_prefix}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        
        self.enter_numeric_keyboard_values(prefix)
        logging.info("Move the scroll bar.")
        self.fax_scroll_bar_move_to_top()
        
    def is_fax_dual_line_enabled(self):
        try:
            self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list , 10)
            return True
        except Exception as e:
            return False
        
    def fax_scroll_bar_move_to_bottom(self):
        """
        Purpose: Move the scroll bar to bottom
        Args: None
        """
        logging.info("Move the scroll bar to bottom.")
        if self.is_fax_dual_line_enabled():
            self.workflow_common_operations.scroll_to_position_vertical(1, scrollbar_objectname="#faxLine2MenuListScrollBar")
        else:
            self.workflow_common_operations.scroll_to_position_vertical(1, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
    
    def fax_scroll_bar_move_to_top(self):
        """
        Purpose: Move the scroll bar to top
        Args: None
        """
        logging.info("Move the scroll bar to top.")
        if self.is_fax_dual_line_enabled():
            self.workflow_common_operations.scroll_to_position_vertical(0, scrollbar_objectname="#faxLine2MenuListScrollBar")
        else:
            self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxDialing)

    def fax_delete_prefix_value(self, index_val):
        """
        Purpose: Delete dial Prefix value
        Args: Index value: Stack 0 or 1
        """
        self.fax_scroll_bar_move_to_bottom()
        already_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        already_field.mouse_click()
        clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()
        logging.info("Move the scroll bar to top.")
        self.fax_scroll_bar_move_to_top()
