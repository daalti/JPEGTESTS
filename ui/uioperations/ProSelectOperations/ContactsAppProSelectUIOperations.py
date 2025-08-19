#########################################################################################
# @file      ContactsAppProSelectUIOperations.py
# @author    Lakshmi Narayanan (lakshmi-narayanan.v@hp.com)
# @date      06-04-2021
# @brief     Implementation for all the Contacts UI navigation methods from Home Menu
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
import time
from time import sleep
import logging
from enum import Enum
from dunetuf.addressBook.addressBook import *
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.BaseOperations.INetworkFolderAppUIOperations import INetworkFolderAppUIOperations
from dunetuf.ui.uioperations.BaseOperations.IContactsAppUIOperations import IContactsAppUIOperations


_logger = logging.getLogger(__name__)
maxtimeout = 10


class ContactsAppProSelectUIOperations(IContactsAppUIOperations):

    contacts_menu = "#2b328d57-7fff-401c-9665-315ada3010f0MenuButton"
    contacts_root_view = "#HomeScreenView"
    contacts_landing_view = "#selectedContactOptionView"
    contacts_search_button = "#SearchButton"
    contacts_search_sort = "#SearchSortButton"
    contacts_search_keyboard_view = "#addContactKeyboard"
    contacts_add_new = "#AddNew"
    select_addressbook_view = "#contactSelectAddressBookView"
    contacts_add_new_options_view = "#addContactsOptionsView"
    contacts_add_contact = "#addContactObject"
    contacts_add_group = "#addGroupObject"
    ldap_addressbook_button = "#LdapAddressBook"
    contacts_add_contact_details_view = "#addContact"
    contacts_display_name = "#basicDisplayNameButton"
    contacts_email_address = "#basicEmailAddressButton"
    contacts_fax_number = "#basicFaxNumberButton"
    contacts_save = "#basicSaveButton"
    contacts_search_results_view = "#searchContactOptionView"
    contacts_edit_contact_details_view = "#editContact"

    contacts_delete = "#basicDeleteButton"
    contacts_delete_confirmation_view = "#DeleteConfirmationView"
    contacts_delete_confirmation_cancel = "#CancelButton"
    contacts_delete_confirmation_delete = "#DeleteButton"

    contacts_add_group_details_view = "#ContactsAppApplicationStackView"
    contacts_group_name = "#basicDisplayGroupNameButton"
    contacts_group_members = "#basicGroupMembersButton"
    contacts_group_select_members_view = "#addMembersContactsView"
    contacts_group_done = "#DoneButton"
    contacts_group_save = "#basicGroupSaveButton"

    contacts_edit_group_details_view = "#editGroup"
    contacts_group_edit_members_view = "#editMembersContactsView"

    contacts_delete_group = "#basicGroupDeleteButton"

    common_keyboard_view = "#commonKeyboardView"
    spice_keyboard_view = "#spiceKeyboardView"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.dial_keyboard_operations = ProSelectKeyboardOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)
        self.menu_operations = MenuAppProSelectUIOperations(self._spice)

    # Navigation from Home screen
    def goto_menu_contacts_screen(self):
        '''
        Navigates to Menu Contacts screen starting from Home screen.
        UI Flow is Home->Menu->Contacts
        '''
        self.menu_operations.goto_menu(self._spice)
        self.dial_common_operations.goto_item(self.contacts_menu, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_root_view, timeout = 15.0)
        logging.info("UI: At Contacts landing home screen view")

    def goto_add_new_screen(self):
        '''
        Navigates to Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New
        '''
        self.dial_common_operations.goto_item(self.contacts_add_new, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_add_new_options_view, timeout = 15.0)
        logging.info("UI: At Contacts Add New Options view")

    def goto_add_contact_screen(self):
        '''
        Navigates to Add Contact details view screen starting from Add New Contacts screen.
        UI Flow is Add New->Add Contact->New Contact details screen
        '''
        self.dial_common_operations.goto_item(self.contacts_add_contact, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_add_contact_details_view, timeout = 15.0)
        logging.info("UI: At New Contact details screen")

    def goto_add_group_screen(self):
        '''
        Navigates to Add Contact details view screen starting from Add New Contacts screen.
        UI Flow is Add New->Add Contact->New Contact details screen
        '''
        self.dial_common_operations.goto_item(self.contacts_add_group, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_add_group_details_view, timeout = 15.0)
        logging.info("UI: At New group details screen")

    def wait_for_edit_contact_screen(self):
        '''
        Waits for Edit Contact details view screen.
        '''
        assert self._spice.wait_for(self.contacts_edit_contact_details_view, timeout = 15.0)
        logging.info("UI: At Edit Contact details screen")

    def wait_for_edit_group_screen(self):
        '''
        Waits for Edit group details view screen.
        '''
        assert self._spice.wait_for(self.contacts_edit_group_details_view, timeout = 15.0)
        logging.info("UI: At Edit Contact details screen")

    def back_to_add_new_screen_from_new_contact_details_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from New Contact details screen to add new contact screen.
        '''
        self.dial_common_operations.back_button_press(self.contacts_add_contact_details_view, self.contacts_add_new_options_view, 3)
        logging.info("UI: At Contacts Add New Options view")

    def back_to_contacts_screen_from_add_new_contact_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from add new contact screen to Contacts landing screen.
        '''
        self.dial_common_operations.back_button_press(self.contacts_add_new_options_view, self.contacts_root_view, 2)
        logging.info("UI: At Contacts landing home screen view")

    # Scan to contacts functional operations
    def search_contact_ldap_addressbook(self, searchString:str):
        '''
        UI Method to do a search on LDAP AddressBook. Tries to find the exact match for the search string.
        Fails if there are no records in the LDAP AB with the searchString.
        Args:
            searchString: string value to be looked for in the LDAP AB.
        '''
        self.menu_operations.goto_menu(self._spice)
        self.dial_common_operations.goto_item(self.contacts_menu, "#MenuListLayout")
        assert self._spice.wait_for(self.select_addressbook_view)
        self.dial_common_operations.goto_item(self.ldap_addressbook_button, self.select_addressbook_view)
        assert self._spice.wait_for(self.contacts_landing_view)
        self.dial_common_operations.goto_item(self.contacts_search_button, self.contacts_landing_view)
        assert self._spice.wait_for(self.contacts_search_keyboard_view)
        self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(searchString)
        assert self._spice.wait_for(self.contacts_search_results_view)
        sleep(2)
        recordButton = "#" + searchString
        self.dial_common_operations.goto_item(recordButton, self.contacts_search_results_view)

    def set_new_contact(self, contact_details: dict):
        '''
        UI should be at New Contact details screen.
        Sets display name, email address, fax number.
        Args:
            contact_details: new contact details to be set
        '''
        display_name = contact_details.get("display_name", None)
        email = contact_details.get("email", None)
        fax = contact_details.get("fax", None)

        if display_name:
            self.dial_common_operations.goto_item(self.contacts_display_name, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(display_name)
            assert self._spice.wait_for(self.contacts_add_contact_details_view)

        if email:
            self.dial_common_operations.goto_item(self.contacts_email_address, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(email)
            assert self._spice.wait_for(self.contacts_add_contact_details_view)

        if fax:
            self.dial_common_operations.goto_item(self.contacts_fax_number, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(fax)
            assert self._spice.wait_for(self.contacts_add_contact_details_view)

    def create_multiple_contacts(self, contact_details: list):
        '''
        Creates multiple contact details starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Contact->New Contact details screen
        Args:
            contact_details: new contact details to be set
        '''

        self.create_new_contact_from_home_screen(contact_details[0])
        self.press_save_contact()
        contact_list_len = len(contact_details)
        for i in range(1,contact_list_len):
            self.goto_add_new_screen()
            self.goto_add_contact_screen()
            self.set_new_contact(contact_details[i])
            self.press_save_contact()

    def set_new_group(self, group_details: dict):
        '''
        UI should be at New group details screen.
        Sets group name, members.
        Args:
            group_details: new group details to be set
        '''
        group_name = group_details.get("group_name", None)
        members = group_details.get("members", None)

        if group_name:
            self.dial_common_operations.goto_item(self.contacts_group_name, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(group_name)
            assert self._spice.wait_for(self.contacts_add_group_details_view)

        if members:
            self.dial_common_operations.goto_item(self.contacts_group_members, "#MenuListLayout" )
            current_screen = self._spice.wait_for("#addMembersContactsView")
        
            scroll_size=len(members)+1
            for i in range(scroll_size):
                current_screen.mouse_wheel(0, 0)
                sleep(0.5)
            
            for member in members:              
                current_screen = self._spice.wait_for("#addMembersContactsView")
                while (self._spice.query_item("#"+member,1)["activeFocus"] == False):
                    current_screen.mouse_wheel(180,180)
                sleep(1)
                assert self._spice.query_item("#"+member,1)["activeFocus"] == True
                current_button = self._spice.wait_for("#"+member+" SpiceText")
                current_button.mouse_click()
                sleep(1)

            self.dial_common_operations.goto_item(self.contacts_group_done, "#MenuListLayout" )
            assert self._spice.wait_for(self.contacts_add_group_details_view)

    def create_new_contact_from_home_screen(self, contact_details):
        '''
        Creates new contact details starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Contact->New Contact details screen
        Args:
            contact_details: new contact details to be set
        '''
        self.goto_menu_contacts_screen()
        self.goto_add_new_screen()
        self.goto_add_contact_screen()
        self.set_new_contact(contact_details)
        logging.info("UI: At add contacts details view")

    def edit_contact(self, edit_contact_details: dict):
        '''
        UI should be at Edit Contact details screen.
        Edits display name, email address, fax number.
        Args:
            edit_contact_details: edit contact details to be set
        '''
        display_name = edit_contact_details.get("display_name", None)
        email = edit_contact_details.get("email", None)
        fax = edit_contact_details.get("fax", None)

        if display_name:
            self.dial_common_operations.goto_item(self.contacts_display_name, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(display_name)
            assert self._spice.wait_for(self.contacts_edit_contact_details_view)

        if email:
            self.dial_common_operations.goto_item(self.contacts_email_address, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(email)
            assert self._spice.wait_for(self.contacts_edit_contact_details_view)

        if fax:
            self.dial_common_operations.goto_item(self.contacts_fax_number, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(fax)
            assert self._spice.wait_for(self.contacts_edit_contact_details_view)

    def press_save_contact(self):
        '''
        UI should be at New Contact details screen.
        Starts to save contacts.
        '''
        self.dial_common_operations.goto_item(self.contacts_save, self.contacts_root_view)
        assert self._spice.wait_for(self.contacts_root_view, timeout = 15.0)
        logging.info("UI: At Contacts landing home screen view")

    def press_save_group(self):
        '''
        UI should be at New group details screen.
        Starts to save group.
        '''
        self.dial_common_operations.goto_item(self.contacts_group_save, self.contacts_root_view)
        assert self._spice.wait_for(self.contacts_root_view, timeout = 15.0)
        logging.info("UI: At Contacts landing home screen view")

    def delete_contact(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Delete
        '''
        self.dial_common_operations.goto_item(self.contacts_delete, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_delete_confirmation_view, timeout = 15.0)
        self.dial_common_operations.goto_item(self.contacts_delete_confirmation_delete, self.contacts_root_view)
        logging.info("UI: At Contacts landing home screen view")

    def delete_contact_cancel(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Cancel
        '''
        self.dial_common_operations.goto_item(self.contacts_delete, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_delete_confirmation_view, timeout = 15.0)
        self.dial_common_operations.goto_item(self.contacts_delete_confirmation_cancel, self.contacts_root_view)
        logging.info("UI: At Contacts landing home screen view")

    def create_new_group_from_home_screen(self, group_details):
        '''
        Creates new contacts group starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Group->New Group details screen
        Args:
            contact_details: new contact details to be set
        '''
        self.goto_menu_contacts_screen()
        self.goto_add_new_screen()
        self.goto_add_group_screen()
        self.set_new_group(group_details)
        logging.info("UI: At add group details view")

    def edit_group(self, edit_group_details: dict):
        '''
        UI should be at Edit group details screen.
        Edits group name and memebers.
        Args:
            edit_group_details: edit group details to be set
        '''
        group_name = edit_group_details.get("group_name", None)
        members = edit_group_details.get("members", None)

        if group_name:
            self.dial_common_operations.goto_item(self.contacts_group_name, "#MenuListLayout" )
            assert self._spice.wait_for(self.spice_keyboard_view)
            self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(group_name)
            assert self._spice.wait_for(self.contacts_edit_group_details_view)

        if members:
            self.dial_common_operations.goto_item(self.contacts_group_members, "#MenuListLayout" )
            current_screen = self._spice.wait_for("#editMembersContactsView")
        
            scroll_size=len(members)+1
            for i in range(scroll_size):
                current_screen.mouse_wheel(0, 0)
                sleep(0.5)
            
            for member in members:              
                current_screen = self._spice.wait_for("#editMembersContactsView")
                while (self._spice.query_item("#"+member,1)["activeFocus"] == False):
                    current_screen.mouse_wheel(180,180)
                sleep(1)
                assert self._spice.query_item("#"+member,1)["activeFocus"] == True
                current_button = self._spice.wait_for("#"+member+" SpiceText")
                current_button.mouse_click()
                sleep(1)

            self.dial_common_operations.goto_item(self.contacts_group_done, "#MenuListLayout" )
            assert self._spice.wait_for(self.contacts_edit_group_details_view)

    def delete_group(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Delete
        '''
        self.dial_common_operations.goto_item(self.contacts_delete_group, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_delete_confirmation_view, timeout = 15.0)
        self.dial_common_operations.goto_item(self.contacts_delete_confirmation_delete, self.contacts_root_view)
        logging.info("UI: At Contacts landing home screen view")

    def delete_group_cancel(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Cancel
        '''
        self.dial_common_operations.goto_item(self.contacts_delete_group, "#MenuListLayout")
        assert self._spice.wait_for(self.contacts_delete_confirmation_view, timeout = 15.0)
        self.dial_common_operations.goto_item(self.contacts_delete_confirmation_cancel, self.contacts_root_view)
        logging.info("UI: At Contacts landing home screen view")
