#########################################################################################
# @file      IContactsAppUIOperations.py
# @author    Lakshmi Narayanan (lakshmi-narayanan.v@hp.com)
# @date      06-04-2021
# @brief     Interface for all the Scan to Contacts UI navigation methods from Home Menu
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from typing import Dict

class IContactsAppUIOperations(object):

    def goto_menu_contacts_screen(self):
        '''
        Navigates to Menu Contacts screen starting from Home screen.
        UI Flow is Home->Menu->Contacts
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_add_new_screen(self):
        '''
        Navigates to Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_add_contact_screen(self):
        '''
        Navigates to Add Contact details view screen starting from Add New Contacts screen.
        UI Flow is Add New->Add Contact->New Contact details screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_add_group_screen(self):
        '''
        Navigates to Add Contact details view screen starting from Add New Contacts screen.
        UI Flow is Add New->Add Contact->New Contact details screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    
    def goto_more_options(self):
        '''
        Navigates to Contacts App view screen starting from Menu.
        UI Flow is Contacts App->More Options
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_custom_addressbook(self,addressbook_name: str):
        '''
        Navigates to select address-book prompt and selects custom address-book starting from Contacts App.
        UI Flow is Contacts App->More Options->AddressBook->(Selects custom Address-book)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_edit_group_screen(self):
        '''
        Waits for Edit group details view screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_add_contact_screen(self):
        '''
        Waits for Add Contact view screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_add_group_screen(self):
        '''
        Waits for Add Group view screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    

    def back_to_add_new_screen_from_new_contact_details_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from New Contact details screen to add new contact screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_contacts_screen_from_add_new_contact_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from add new contact screen to Contacts landing screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_contacts_screen_from_add_new_group_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from add new group screen to Contacts landing screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_new_contact(self, contact_details: dict):
        '''
        UI should be at New Contact details screen.
        Sets display name, email address, fax number.
        Args:
            contact_details: new contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def create_multiple_contacts(self, contact_details: list):
        '''
        Creates multiple contact details starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Contact->New Contact details screen
        Args:
            contact_details: new contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_new_group(self, group_details: dict):
        '''
        UI should be at New group details screen.
        Sets group name, members.
        Args:
            group_details: new group details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def create_new_contact_from_home_screen(self, contact_details):
        '''
        Creates new contact details starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Contact->New Contact details screen
        Args:
            contact_details: new contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def edit_contact(self, edit_contact_details: dict):
        '''
        UI should be at Edit Contact details screen.
        Edits display name, email address, fax number.
        Args:
            edit_contact_details: edit contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_save_contact(self):
        '''
        UI should be at New Contact details screen.
        Starts to save contacts.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_save_group(self):
        '''
        UI should be at New group details screen.
        Starts to save group.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def delete_contact(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Delete
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def delete_contact_cancel(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Cancel
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def create_new_group_from_home_screen(self, group_details):
        '''
        Creates new contacts group starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Group->New Group details screen
        Args:
            contact_details: new contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def edit_group(self, edit_group_details: dict):
        '''
        UI should be at Edit group details screen.
        Edits group name and memebers.
        Args:
            edit_group_details: edit group details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def delete_group(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Delete
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def delete_group_cancel(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Cancel
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_to_next_page_in_landing_page(self):
        '''
        This will scroll to end of the list in contacts landing page.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def contacts_wait_for_item(self, item:str):
        '''
        This will wait for given item in parameter
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, scroll_bar, footer_item_id=None, top_item_id=None, scroll_height=60):
        """
        Scroll contact/group into center of sceen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items. One more thing, there are 2 screen to show 100 contacts
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                scroll_bar: object name scroll bar 
                footer_item_id: object name for footer view, keep it as None if it does not inculded in scroll view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def delete_contacts_member_from_group(self, members: list):
        '''
        UI should be at Edit group details screen.
        delete some contacts member from group.
        Args:
            members: contacts list to delete
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_delete_contacts_member_from_group(self, members: list):
        '''
        UI should be at Edit group details screen.
        cancel to delete some contacts member from group.
        Args:
            members: contacts list to delete
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_password_for_custom_addressbook(self, password):
        '''
        input password for selected custom addressbook
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_submit_button_input_custom_addressbook_password_screen(self):
        '''
        click submit button on input custom addressbook password screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_cancel_button_input_custom_addressbook_password_screen(self):
        '''
        click cancel button on input custom addressbook password screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_contacts_is_existed_by_display_name(self, display_name):
        '''
        This is helper method to verify contact is shows on contacts landing view.
        UI should be in Home->Menu->Contacts
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_contacts_display_name_in_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list: 
        @return: contacts_name_list
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_email_address_of_contacts(self):
        '''
        get email address from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_fax_number_of_contacts(self):
        '''
        get fax number from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def get_members_text_of_group(self):
        '''
        get members text from group detail screen.
        UI should be in Home->Menu->Contacts->Select a group.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_required_fields_empty_message(self, net):
        '''
        Check spec on required fields is empty message screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_required_fields_empty_message_screen(self):
        '''
        click ok button on required fields is empty message screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_invalid_entries_for_display_name(self, net):
        '''
        Check invalid entries for display name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_invalid_entries_for_email_address(self, net):
        '''
        Check invalid entries for email address
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_invalid_entries_for_fax_number(self, net):
        '''
        Check invalid entries for fax number
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_invalid_entries_for_group_name(self, net):
        '''
        Check invalid entries for group name
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_retry_password_alert_description(self, net):
        '''
        Check retry password description when input invalid password for custom addressbook
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_on_retry_password_alert_description(self):
        '''
        click ok button on retry password alert description screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_search_text_in_search_screen(self, search_text):
        """
        Input search text in search screen.
        @param:search_text: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_search_button_in_search_screen(self):
        """
        Click search button in search screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_cancel_button_in_search_screen(self):
        """
        Click cancel button in search screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_search_field_empty_message(self, net):
        '''
        Check spec when search text is empty
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_search_field_empty_message_screen(self):
        '''
        click ok button on search field is empty message screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_reset_button(self):
        '''
        click reset button on search result contacts landing view screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_reset_button(self):
        '''
        Check reset button is visible on contacts landing view screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    
    
    def check_spec_no_entries_found(self, net):
        '''
        Check spec no entries found when search no contacts
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_search_contacts_ldap_addressbook(self, net):
        '''
        Check spec search contacts when select LDAP address book
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_search_result_number_in_contacts_list_view(self, expected_contacts_list):
        """
        Check Search Result numbers shows in contacts list view screen.
        @param:expected_file_list: 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_sort_order(self, net, sort):
        '''
        Select sort order
        @param:sort: only two order: AtoZ/ZtoA 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_menu_contacts_app(self):
        '''
        UI should be at Menu-> Contacts app landing view.
        Navigates back from Contacts landing view screen to Menu Contacts screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def add_new_contacts(self, contact_details: dict):
        '''
        Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New -> set contacts details -> Press the save button in add contacts view.
        Args:
            contact_details: new contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def add_new_group(self, group_details: dict):
        '''
        Add New Group screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New Group -> set group details -> Press the save button in add group view.
        Sets group name, members.
        Args:
            group_details: new group details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_and_delete_contact(self, contact_name, with_search_screen=False):
        '''
        Delete a Contacts starting from Contacts Landing Home screen.
        UI Flow is Contacts landing view -> Select a contact -> click edit -> click delete button to delete.
        Args:
            contact_name: contact name need to be deleted
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_and_edit_contact(self, contact_name, payload, with_search_screen=False):
        '''
        Edit a Contacts starting from Contacts Landing Home screen.
        UI Flow is Contacts landing view -> Select a contact -> click edit -> edit contacts details -> click save.
        Args:
            contact_name: edit contact name
            payload: edit contact details to be set
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_contacts_details_info_ui(self, net, expected_email = "Not Set", expected_fax = "Not Set"):
        """
        check contacts details info with UI
        If the contacts not set email address or number, the default text in UI shows 'Not Set'
        @param: expected_email: default is "Not Set"/ user created
                expected_fax: default is "Not Set"/ user created
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_group_details_info_ui(self, net, expected_email = "0 email addresses", expected_fax = "0 fax numbers", expected_members = "0 members"):
        """
        check group details info with UI
        If the group not add contacts or add contacts without set email address or number, the default text in UI shows '"0 email addresses"'/'0 fax numbers'/'0 members'
        @param: expected_email:
                expected_fax:
                expected_members:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_contacts_landing_screen_from_contacts_details_screen(self):
        '''
        UI should be at Contact details screen.
        Navigates back from Contact details screen to contact landing screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_search_button(self):
        """
        Click search button in contacts landing view.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_textbox(self):
        """
        Go to fax number textbox in add contacts screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
