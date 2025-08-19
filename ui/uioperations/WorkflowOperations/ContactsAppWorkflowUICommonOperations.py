import time as t
import logging
from socket import timeout
from time import sleep

from dunetuf.addressBook.addressBook import *
from dunetuf.ui.uioperations.BaseOperations.IContactsAppUIOperations import IContactsAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowObjectIds import ContactsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.send.common.defaultjoboptions.defaultjoboptionsutils import DefaultJobOptionsUtils, JobType

class ContactsAppWorkflowUICommonOperations(IContactsAppUIOperations):

    def __init__(self, spice):
        self.ContactsAppWorkflowObjectIds = ContactsAppWorkflowObjectIds()
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    def search_contact_ldap_addressbook(self, searchString:str):
        '''
        UI Method to do a search on LDAP AddressBook. Tries to find the exact match for the search string.
        Fails if there are no records in the LDAP AB with the searchString.
        Args:
            searchString: string value to be looked for in the LDAP AB.
        '''
        self.goto_menu_contacts_screen()
        self.select_custom_addressbook("Ldap")
        self.click_search_button()
        self.input_search_text_in_search_screen(searchString)
        self.click_search_button_in_search_screen()
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.custom_section)

    def goto_menu_contacts_screen(self):
        '''
        Navigates to Menu Contacts screen starting from Home screen.
        UI Flow is Home->Menu->Contacts
        '''
        self.spice.home_operations.goto_home_contacts()
        contacts_menu_view = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_menuContacts)
        self.spice.wait_until(lambda:contacts_menu_view["visible"])
        logging.info("At Contacts Screen")

    def get_menu_contacts_button(self):
        self.homemenu.goto_menu(self.spice)
       # self.workflow_common_operations.goto_item(ContactsAppWorkflowObjectIds.contacts_menu,
        #                                          ContactsAppWorkflowObjectIds.view_menu_landing_view,
         #                                         scrollbar_objectname=ContactsAppWorkflowObjectIds.scroll_bar_menu_contact)
        #self.spice.wait_for(ContactsAppWorkflowObjectIds.view_contacts)
        self.homemenu.scroll_position_utilities(ContactsAppWorkflowObjectIds.menu_button_contacts)
        current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.menu_button_contacts + " MouseArea")
        return current_button

    def goto_add_new_screen(self):
        '''
        Navigates to Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contact)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_contact)
        current_button.mouse_click()
        logging.info("UI: At Contacts Add New Options view")

    def goto_add_contact_screen(self):
        '''
        Navigates to Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contact)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_contact)
        current_button.mouse_click()
        logging.info("UI: At Contacts Add New Options view")

    def goto_add_group_screen(self):
        '''
        Navigates to Add Contact details view screen starting from Add New Contacts screen.
        UI Flow is Add New->Add Contact->New Contact details screen
        '''
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_group)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_group)
        current_button.mouse_click()
        sleep(2)
        # Need to unckeck after we get the correct view ID.
        # assert self.spice.wait_for(ContactsAppWorkflowObjectIds.view_add_group, timeout = 15.0)
        logging.info("UI: At New group details screen")

    def wait_for_edit_contact_screen(self):
        '''
        Waits for Edit Contact details view screen.
        '''
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_edit_contacts)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_edit_contacts)
        if not current_button["visible"]:
            current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_edit_contacts, 1)
        
        assert current_button["visible"], "Please make the button's visible attribute is True, then could could click it"
        current_button.mouse_click()

        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.view_edit_contacts)
        logging.info("UI: At Edit Contact details screen")

    def wait_for_add_contact_screen(self):
        '''
        Waits for Add Contact view screen.
        '''
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.view_add_contacts)

    def wait_for_add_group_screen(self):
        '''
        Waits for Add Group view screen.
        '''
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.view_add_group)

    def wait_for_edit_group_screen(self):
        '''
        Waits for Edit group details view screen.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_edit_group)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_edit_group)
        if not current_button["visible"]:
            current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_edit_group, 1)
        
        assert current_button["visible"], "Please make the button's visible attribute is True, then could could click it"
        current_button.mouse_click()
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.view_edit_group)
        logging.info("UI: At Edit Group details screen")

    def back_to_add_new_screen_from_new_contact_details_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from New Contact details screen to add new contact screen.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_back)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_back)
        current_button.mouse_click()

    def back_to_contacts_screen_from_add_new_contact_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from add new contact screen to Contacts landing screen.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contacts_cancel)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_contacts_cancel)
        current_button.mouse_click()

    def back_to_contacts_screen_from_add_new_group_screen(self):
        '''
        UI should be at New Contact details screen.
        Navigates back from add new group screen to Contacts landing screen.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_cancel)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_group_cancel)
        current_button.mouse_click()

    def select_contact(self, contacts_name: str, with_search_screen=False):
        '''
        Select contact in contacts list view
        Args:
            contacts_name:
            with_search_screen:True: select contact in search screen, screen include top item, need to add top item id when scroller into contact.
                               False: select contact in contacts landing view
        '''
        # record_contact1Row
        current_screen = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_menuContacts)
        self.spice.wait_until(lambda:current_screen["visible"])
        sleep(2)
        contact = "#record_" + contacts_name + "Row"
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
        self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.contacts_landing_view_list, contact, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar, ContactsAppWorkflowObjectIds.footer_view, top_item_id=ContactsAppWorkflowObjectIds.custom_section)

        assert self.spice.wait_for(contact)
        current_button = self.spice.wait_for(contact)
        current_button.mouse_click()
        sleep(2)

    def set_new_contact(self, contact_details: dict):
        '''
        UI should be at New Contact details screen.
        Sets display name, first name, last name,email address, fax number.
        Args:
            contact_details: new contact details to be set
        '''
        print("contact_details", contact_details)

        display_name = contact_details.get("display_name", None)
        print("display_name", display_name)
        first_name = contact_details.get("first_name", None)
        print("first_name", first_name)
        last_name = contact_details.get("last_name", None)
        print("last_name", last_name)
        email = contact_details.get("email", None)
        print("email", email)
        fax = contact_details.get("fax", None)
        print("fax", fax)
        notes = contact_details.get("notes", None)
        print("notes", notes)


        if display_name:
            sleep(1)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_display_name)
            display_name_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_display_name)
            display_name_textbox.mouse_click()
            display_name_textbox.__setitem__('displayText', display_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if first_name:
            sleep(1)
            first_name_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_first_name)
            first_name_textbox.mouse_click()
            first_name_textbox.__setitem__('displayText', first_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if last_name:
            sleep(1)
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_last_name_field, ContactsAppWorkflowObjectIds.textbox_last_name],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_last_name)
            last_name_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_last_name)
            last_name_textbox.mouse_click()
            last_name_textbox.__setitem__('displayText', last_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if email:
            sleep(1)
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_email, ContactsAppWorkflowObjectIds.textbox_email],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox.mouse_click()
            display_email_textbox.__setitem__('displayText', email)
            display_email_textbox.__setitem__('inputText', email)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if fax:
            sleep(1)
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_fax, ContactsAppWorkflowObjectIds.textbox_fax],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            fax_number_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_fax)
            fax_number_textbox.mouse_click()
            self.input_fax_number_for_add_contact(fax)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_number_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if notes:
            sleep(1)
            self.workflow_common_operations.scroll_to_position_vertical(1, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_notes)
            notes_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_notes)
            notes_textbox.mouse_click()
            notes_textbox.__setitem__('displayText', notes)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        sleep(2)


    def select_verify_access_checkbox(self, checked = False):
        '''
        UI should be at New Contact details screen.
        Checks verify access checkbox.
        '''
        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_verify_access,ContactsAppWorkflowObjectIds.checkbox_verify_access],ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)

    def verify_network_folder_constrained(self):
        '''
        UI should be at New Contact details screen.
        Verifies network folder constrained.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.view_contacts_networkFolderType)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.view_contacts_networkFolderType)
        current_button.mouse_click()
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_modal)

    
    def goto_network_folder_path(self):
        '''
        UI should be at New Contact details screen.
        Sets network folder path.
        Args:
            network_folder_path: network folder path to be set
        '''
        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_network_folder_path, ContactsAppWorkflowObjectIds.combobox_network_folder_path],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)

    def select_standard_network_folder_in_contacts(self, path = "Standard"):
        self.goto_network_folder_path()
        self.spice.wait_for("#SettingsSpiceComboBoxpopupList")
        if path == "Standard":
            current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.settings_network_folder_option_standard)
        else:
            current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.settings_network_folder_option_none)
        current_button.mouse_click()
    
    def select_network_folder_path_in_contacts(self,path_details: dict):
        '''
        UI should be at New Contact details screen.
        Sets network folder path.
        Args: 
            network_folder_path: network folder path to be set
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.view_add_contacts)
        unc_folder_path = path_details.get("network_folder_path", None)
        windows_domain = path_details.get("windows_domain", None)
        username = path_details.get("username", None)
        password = path_details.get("password", None)
        if unc_folder_path: 
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_unc_folder_path, ContactsAppWorkflowObjectIds.textbox_uncFolder_path],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_uncFolder_path)
            network_folder_path_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_uncFolder_path)
            network_folder_path_textbox.mouse_click()
            network_folder_path_textbox.__setitem__('displayText',unc_folder_path)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if windows_domain:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_windows_domain, ContactsAppWorkflowObjectIds.textbox_windows_domain],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            windows_domain_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_windows_domain)
            windows_domain_textbox.mouse_click()
            windows_domain_textbox.__setitem__('displayText', windows_domain)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if username:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_username, ContactsAppWorkflowObjectIds.textbox_username],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            username_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_username)
            username_textbox.mouse_click()
            username_textbox.__setitem__('displayText', username)
            username_textbox.__setitem__('inputText', username)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if password:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_password, ContactsAppWorkflowObjectIds.textbox_password],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_password)
            password_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_password)
            password_textbox.mouse_click()
            password_textbox.__setitem__('displayText', password)
            password_textbox.__setitem__('inputText', password) 
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()


    

    def edit_network_folder_path_in_contacts(self,path_details: dict):
        '''
        UI should be at Edit Contact details screen.
        Update network folder path.
        Args:
            network_folder_path: network folder path to be updated
        '''
        screen = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_edit_contacts_list_view)
        screen_height = screen['contentHeight']
        unc_folder_path = path_details.get("network_folder_path", None)
        username = path_details.get("username", None)
        password = path_details.get("password", None)
        if unc_folder_path:
                    self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_unc_folder_path, ContactsAppWorkflowObjectIds.textbox_uncFolder_path],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
                    unc_folder_path_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_uncFolder_path)
                    unc_folder_path_textbox.mouse_click()
                    self.click_back_button_singleLine()
                    unc_folder_path_textbox.__setitem__('displayText', unc_folder_path)
                    keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
                    keyboard_ok_button.mouse_click()
       
        #scroll to password field
        # click on it, check if the password field is empty on click
        #Then enter the password and close keyboard
        if password:
                    self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_password, ContactsAppWorkflowObjectIds.textbox_password],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
                    password_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_password)
                    password_textbox.mouse_click()
                    keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
                    info_value = password_textbox.__getitem__('displayText')
                    assert info_value == ""
                    password_textbox.__setitem__('displayText', password)
                    keyboard_ok_button.mouse_click()


    def create_multiple_contacts(self, contact_details: list):
        '''
        Creates multiple contact details starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Contact->New Contact details screen
        Args:
            contact_details: new contact details to be set
        '''
        self.goto_menu_contacts_screen()
        # self.create_new_contact_from_home_screen(contact_details[0])
        # self.press_save_contact()
        contact_list_len = len(contact_details)
        print("contact_list_len", contact_list_len)

        for i in range(0, contact_list_len):
            self.goto_add_new_screen()
            sleep(2)
            print("contact_details[i]", contact_details[i])
            self.set_new_contact(contact_details[i])
            sleep(2)
            self.press_save_contact()
            sleep(2)

    def set_new_group(self, group_details: dict, execute_member_selection: bool = False):
        '''
        UI should be at New group details screen.
        Sets group name, members.
        Args:
            group_details: new group details to be set
            execute_member_selection: boolean flag to indicate whether to execute cancel member selection and select again or not.
        '''
        group_name = group_details.get("group_name", None)
        members = group_details.get("members", None)
        notes = group_details.get("notes", None)
        if group_name:
            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group)
            display_email_textbox = self.spice.wait_for("#groupNameButtonModel")
            display_email_textbox.__setitem__('displayText', group_name)
            sleep(2)
            self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_add_group} {ContactsAppWorkflowObjectIds.textbox_group_name} {ContactsAppWorkflowObjectIds.contact_name_inputtextbox}").mouse_click()
            sleep(6)
            current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            current_button.mouse_click()

        if notes:
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group_notes)
            notes_textbox = self.spice.wait_for("#groupNotesTextFieldRowModel")
            notes_textbox.mouse_click()
            notes_textbox.__setitem__('displayText', notes)
            sleep(2)
            self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_add_group_notes} {ContactsAppWorkflowObjectIds.textbox_group_notes} {ContactsAppWorkflowObjectIds.contact_name_inputtextarea}").mouse_click()
            sleep(6)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()

        if members:
            if execute_member_selection:
                self.workflow_common_operations.goto_item(["#groupMembersButtonRow_firstinfoBlockRow" + "#groupMembersButtonRow_2infoBlockRow"], ContactsAppWorkflowObjectIds.button_add_member, ContactsAppWorkflowObjectIds.view_add_group, select_option=False,scrollbar_objectname=ContactsAppWorkflowObjectIds.add_group_scrollbar)
                assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_member)
                button_add_member = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_member)
                button_add_member.mouse_click()

                for i, value in enumerate(members):
                    contact = "#contact_" + members[i] + "Model"
                    row_item_id = f"#contact_" + members[i] + "Row"
                    logging.info(f"scroll into contact {row_item_id}")
                    # self.workflow_common_operations.goto_item(row_item_id,ContactsAppWorkflowObjectIds.view_add_group_member,select_option=False,scrollbar_objectname=ContactsAppWorkflowObjectIds.scroll_bar_add_group_member)
                    assert self.spice.wait_for(contact)
                    contact_checkbox = self.spice.wait_for(contact)
                    contact_checkbox.mouse_click()
                    self.spice.wait_until(lambda:contact_checkbox["checked"])

                sleep(2)
                self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_group_member_cancel)
                click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_group_member_cancel)
                click_save_button.mouse_click()
                sleep(2)

            self.workflow_common_operations.goto_item(["#groupMembersButtonRow_firstinfoBlockRow" + "#groupMembersButtonRow_2infoBlockRow"], ContactsAppWorkflowObjectIds.button_add_member, ContactsAppWorkflowObjectIds.view_add_group, select_option=False,scrollbar_objectname=ContactsAppWorkflowObjectIds.add_group_scrollbar)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_member)
            button_add_member = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_member)
            button_add_member.mouse_click()

            for i, value in enumerate(members):
                contact = "#contact_" + members[i] + "Model"
                row_item_id = f"#contact_" + members[i] + "Row"
                logging.info(f"scroll into contact {row_item_id}")
                self.workflow_common_operations.goto_item(row_item_id,ContactsAppWorkflowObjectIds.view_add_group_member,select_option=False,scrollbar_objectname=ContactsAppWorkflowObjectIds.scroll_bar_add_group_member)
                assert self.spice.wait_for(contact)
                contact_checkbox = self.spice.wait_for(contact)
                contact_checkbox.mouse_click()
                self.spice.wait_until(lambda:contact_checkbox["checked"])

            sleep(2)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_group_member_done)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_group_member_done)
            click_save_button.mouse_click()
            sleep(2)


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
        sleep(5)
        self.set_new_contact(contact_details)
        logging.info("UI: At add contacts details view")

    def click_back_button_singleLine(self):
        if (self.spice.uisize == "XS" or self.spice.uisize == "S"):
            keyboard_backspace_button = self.spice.wait_for("#ClearMouseArea")
        else:
            keyboard_backspace_button = self.spice.wait_for("#backspaceKey")
        keyboard_backspace_button.mouse_click(10)

    def edit_contact(self, edit_contact_details: dict):
        '''
        UI should be at Edit Contact details screen.
        Edits display name, email address, fax number.
        Args:
            edit_contact_details: edit contact details to be set
        '''
        screen = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_edit_contacts_list_view)
        screen_height = screen['contentHeight']
        display_name = edit_contact_details.get("display_name", None)
        first_name = edit_contact_details.get("first_name", None)
        last_name = edit_contact_details.get("last_name", None)
        email = edit_contact_details.get("email", None)
        fax = edit_contact_details.get("fax", None)
        notes = edit_contact_details.get("notes", None)
        if display_name:
            display_name_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_display_name)
            display_name_textbox.mouse_click()
            self.click_back_button_singleLine()
            display_name_textbox.__setitem__('displayText', display_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if first_name:
            first_name_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_first_name)
            first_name_textbox.mouse_click()
            self.click_back_button_singleLine()
            first_name_textbox.mouse_click()
            first_name_textbox.__setitem__('displayText', first_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if last_name:
            last_name_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_last_name)
            last_name_textbox.mouse_click()
            sleep(2)
            self.click_back_button_singleLine()
            last_name_textbox.__setitem__('displayText', last_name)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if email:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_email, ContactsAppWorkflowObjectIds.textbox_email],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
            display_email_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox.mouse_click()
            #Remove already exist content
            self.spice.keyBoard.keyboard_empty_text(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox.mouse_click()
            self.spice.email.input_text_from_keyboard(email)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if fax:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_fax, ContactsAppWorkflowObjectIds.textbox_fax],
                                                     ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                     scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
            fax_number_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_fax)
            fax_number_textbox.mouse_click()
            self.spice.keyBoard.keyboard_empty_text(ContactsAppWorkflowObjectIds.textbox_fax)
            fax_number_textbox.mouse_click()
            self.input_fax_number_for_add_contact(fax)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_number_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if notes:
            self.workflow_common_operations.scroll_to_position_vertical(1, scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contacts_list_view)
            self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_notes)
            notes_textbox = self.spice.query_item(ContactsAppWorkflowObjectIds.textbox_notes)
            notes_textbox.mouse_click()
            self.click_back_button_singleLine()
            notes_textbox.__setitem__('displayText', notes)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        
    def delete_entry_from_contact(self, display_name=False, email_address=False, fax_number=False):
        """
        Delete entry from contact screen
        """
        screen = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_edit_contacts_list_view)
        screen_height = screen['contentHeight']
        if display_name:
            display_name_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_display_name)
            display_name_textbox.mouse_click()
            self.click_back_button_singleLine()
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()        
        if email_address:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_email, ContactsAppWorkflowObjectIds.textbox_email],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
            display_email_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox.mouse_click()
            #Remove already exist content
            self.spice.keyBoard.keyboard_empty_text(ContactsAppWorkflowObjectIds.textbox_email)
            display_email_textbox.mouse_click()
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        if fax_number:
            self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_fax, ContactsAppWorkflowObjectIds.textbox_fax],
                                                     ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                     scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
            fax_number_textbox = self.spice.wait_for(ContactsAppWorkflowObjectIds.textbox_fax)
            fax_number_textbox.mouse_click()
            #Remove already exist content
            self.spice.keyBoard.keyboard_empty_text(ContactsAppWorkflowObjectIds.textbox_fax)
            keyboard_ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_number_keyboard_ok)
            keyboard_ok_button.mouse_click()

    def press_save_contact(self):
        """
        Purpose: Press the save button in add contacts view.
        :param spice: Takes 1 arguments
        :return: None
        """
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contacts_save)
        save_contact_button1 = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_contacts_save)
        self.spice.wait_until(lambda:save_contact_button1["visible"])
        self.spice.wait_until(lambda:save_contact_button1["enabled"])
        save_contact_button1.mouse_click()
        logging.info("UI: At Contacts landing home screen view")
        sleep(1)

    def press_save_group(self):
        """
        Purpose: Press the save button in add group view.
        :param spice: Takes 1 arguments
        :return: None
        """
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_save)
        save_group_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_save)
        save_group_button.mouse_click()
        logging.info("UI: At Contacts landing home screen view")

    def delete_contact(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Delete
        '''
        delete_contacts_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_contacts)
        delete_contacts_button.mouse_click()
        delete_contacts_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_delete)
        delete_contacts_button.mouse_click()
        logging.info("UI: At Contacts landing home screen view")

    def delete_contact_cancel(self):
        '''
        Navigates to Delete Contact details view screen starting from Edit Contacts screen.
        UI Flow is Delete Contact->Delete Contact confirmation screen->Cancel
        '''
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_contacts)
        delete_contacts_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_contacts)
        delete_contacts_button.mouse_click()
        sleep(2)
        try:
            self.spice.wait_for(ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel)
            delete_contacts_button = self.spice.wait_for(
            ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel)
            delete_contacts_button.mouse_click()
        except:
            self.spice.wait_for(ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel_for_Beam_MFP)
            delete_contacts_button = self.spice.wait_for(
            ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel_for_Beam_MFP)
            delete_contacts_button.mouse_click()
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contacts_cancel)
        delete_contacts_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contacts_cancel)
        delete_contacts_button.mouse_click()
        logging.info("UI: At Contacts landing home screen view")

    def create_new_group_from_home_screen(self, group_details: dict):
        '''
        Creates new contacts group starting from home screen.
        UI Flow is Home->Menu->Contacts->Add New->Add Group->New Group details screen
        Args:
            contact_details: new contact details to be set
        '''
        self.goto_menu_contacts_screen()
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
        notes= edit_group_details.get("notes", None)

        if group_name:
            sleep(1)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group)
            display_email_textbox = self.spice.wait_for("#groupNameButtonModel")
            display_email_textbox.__setitem__('displayText', group_name)            
            sleep(2)
            self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_add_group} {ContactsAppWorkflowObjectIds.textbox_group_name} {ContactsAppWorkflowObjectIds.contact_name_inputtextbox}").mouse_click()
            sleep(6)
            current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            current_button.mouse_click()
        
        if notes:
            sleep(1)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group_notes)
            notes_textbox = self.spice.wait_for("#groupNotesTextFieldRowModel")
            notes_textbox.mouse_click()
            notes_textbox.__setitem__('displayText', notes)
            sleep(2)
            self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_add_group_notes} {ContactsAppWorkflowObjectIds.textbox_group_notes} {ContactsAppWorkflowObjectIds.contact_name_inputtextarea}").mouse_click()
            sleep(6)
            current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            current_button.mouse_click()

        if members:
            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_member)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_member)
            click_save_button.mouse_click()
            # Remove all
            sleep (2)
            assert self.spice.wait_for("#editMembersContactsView")
            more_options = self.spice.wait_for("#dropDownButtonLeft")
            more_options.mouse_click()
            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_removeall)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_group_edit_removeall)
            click_save_button.mouse_click()
            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_removeall_confirm)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_group_edit_removeall_confirm)
            click_save_button.mouse_click()
            # click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_group_edit_removeall_confirm)
            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_add)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_group_edit_add)
            click_save_button.mouse_click()
            sleep(2)
            member_list_len = len(members)
            print("contact_list_len", member_list_len)
            #Select Contacts
            
            for i in range(0, member_list_len):
                contact = "#contact_" + members[i] + "Model"
                print("contact", contact)
                assert self.spice.wait_for(contact)
                sleep(2)
                current_button = self.spice.query_item(contact)
                sleep(2)
                current_button.mouse_click()

            sleep(2)
            assert self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_group_member_done)
            click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_add_group_member_done)
            click_save_button.mouse_click()

            sleep(2)
            click_save_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_back)
            click_save_button.mouse_click()
            sleep(2)

        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group)
        sleep(2)
        self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_add_group} {ContactsAppWorkflowObjectIds.textbox_group_name} {ContactsAppWorkflowObjectIds.contact_name_inputtextbox}").mouse_click()
        sleep(2)
        current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_keyboard_ok)
        current_button.mouse_click()        

    def click_multiple_textfield_without_clicking_ok(self, group_details: dict):
        '''
            This function is written to test on activeFocusChanged scenario
            If there are multiple textfields in the screen, this function will click on each textfield and then click on the next textfield without hiding the keyboard
            At first click on textfield it hides the existing keyboard and then on second click it opens keyboard of focused textfield
            The reason why the textfield click is called two times in the following function
        '''
        group_name = group_details.get("group_name", None)
        members = group_details.get("members", None)
        notes = group_details.get("notes", None)

        # Declare selectors if group_name and notes are present
        if group_name and notes:
            group_name_selector = f"{ContactsAppWorkflowObjectIds.row_add_group} {ContactsAppWorkflowObjectIds.textbox_group_name} {ContactsAppWorkflowObjectIds.contact_name_inputtextbox}"
            notes_selector = f"{ContactsAppWorkflowObjectIds.row_add_group_notes} {ContactsAppWorkflowObjectIds.textbox_group_notes} {ContactsAppWorkflowObjectIds.contact_name_inputtextarea}"

            def click_group_name():
                sleep(2)
                assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group)
                display_email_textbox = self.spice.query_item("#groupNameButtonModel")
                display_email_textbox.__setitem__('displayText', group_name)
                sleep(2)
                self.spice.wait_for(group_name_selector).mouse_click()
                sleep(6)

            def click_notes():
                assert self.spice.wait_for(ContactsAppWorkflowObjectIds.row_add_group_notes)
                notes_textbox = self.spice.query_item("#groupNotesTextFieldRowModel")
                notes_textbox.mouse_click()
                notes_textbox.mouse_click()
                notes_textbox.__setitem__('displayText', notes)
                sleep(2)
                text_box_notes = self.spice.wait_for(notes_selector)
                text_box_notes.mouse_click()
                sleep(6)
                return text_box_notes

            def click_multiple_times(element, times):
                for _ in range(times):
                    element.mouse_click()
                    sleep(2)

            def click_group_name_multiple_times(times):
                for _ in range(times):
                    click_group_name()
                    sleep(2)

            # Perform initial clicks
            click_group_name()
            text_box_notes = click_notes()

            # Perform repeated clicks
            click_multiple_times(text_box_notes, 2)
            click_group_name_multiple_times(2)
            click_multiple_times(text_box_notes, 2)
            click_group_name_multiple_times(2)
            click_multiple_times(text_box_notes, 2)

            # Click OK button
            keyboard_ok_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_keyboard_ok)
            keyboard_ok_button.mouse_click()
        else:
            pass   


    def delete_contacts_member_from_group(self, members: list):
        '''
        UI should be at Edit group details screen.
        delete some contacts member from group.
        Args:
            members: contacts list to delete
        '''

        add_member_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_member)
        add_member_button.mouse_click()
        sleep(2)
        member_list_len = len(members)
        print("contact_list_len", member_list_len)
        #Select Contacts
        
        for i in range(0, member_list_len):
            contact = "#contact_" + members[i] + "Model"
            row_item_id = f"#contact_" + members[i] + "Row"
            logging.info(f"scroll into contact {row_item_id}")
            is_visible = self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.list_view_edit_group_member, row_item_id, ContactsAppWorkflowObjectIds.scroll_bar_edit_group_member)
            assert is_visible, f"The row item <{row_item_id}> does not in center of screen that could be clicked"
            contact_checkbox = self.spice.wait_for(contact)
            contact_checkbox.mouse_click()
            self.spice.wait_until(lambda:contact_checkbox["checked"])

        sleep(2)
        remove_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_remove)
        self.spice.validate_button(remove_button)
        remove_button.mouse_click()

        remove_confirm_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_remove_confirm)
        self.spice.validate_button(remove_confirm_button)
        remove_confirm_button.mouse_click()
        sleep(2)

        back_button = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.view_edit_group_members} {ContactsAppWorkflowObjectIds.button_back}")
        back_button.mouse_click()
    
    def cancel_delete_contacts_member_from_group(self, members: list):
        '''
        UI should be at Edit group details screen.
        cancel to delete some contacts member from group.
        Args:
            members: contacts list to delete
        '''

        add_member_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_member)
        add_member_button.mouse_click()
        sleep(2)
        member_list_len = len(members)
        print("contact_list_len", member_list_len)
        #Select Contacts
        
        for i in range(0, member_list_len):
            contact = "#contact_" + members[i] + "Model"
            row_item_id = f"#contact_" + members[i] + "Row"
            logging.info(f"scroll into contact {row_item_id}")
            is_visible = self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.list_view_edit_group_member, row_item_id, ContactsAppWorkflowObjectIds.scroll_bar_edit_group_member)
            assert is_visible, f"The row item <{row_item_id}> does not in center of screen that could be clicked"
            contact_checkbox = self.spice.wait_for(contact)
            contact_checkbox.mouse_click()
            self.spice.wait_until(lambda:contact_checkbox["checked"])

        sleep(2)
        remove_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_remove)
        self.spice.validate_button(remove_button)
        remove_button.mouse_click()

        remove_cancel_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_group_edit_remove_cancel)
        self.spice.validate_button(remove_cancel_button)
        remove_cancel_button.mouse_click()
        sleep(2)

        back_button = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.view_edit_group_members} {ContactsAppWorkflowObjectIds.button_back}")
        back_button.mouse_click()

    def delete_group(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Delete
        '''
        self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.enter_edit_frame} {ContactsAppWorkflowObjectIds.button_edit_contacts} {ContactsAppWorkflowObjectIds.edit_name_text}").mouse_click()
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_group)
        click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_delete_group)
        click_save_button.mouse_click()
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_group_confirmation_delete)
        click_save_button = self.spice.query_item(
            ContactsAppWorkflowObjectIds.button_delete_group_confirmation_delete)
        click_save_button.mouse_click()

    def delete_group_cancel(self):
        '''
        Navigates to Delete group details view screen starting from Edit Group screen.
        UI Flow is Delete Group->Delete group confirmation screen->Cancel
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_delete_group)
        click_save_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_delete_group)
        click_save_button.mouse_click()
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel)
        click_save_button = self.spice.query_item(
            ContactsAppWorkflowObjectIds.button_contacts_delete_confirmation_cancel)
        click_save_button.mouse_click()
        logging.info("UI: At Contacts landing home screen view")

    def scroll_to_next_page_in_landing_page(self):
        '''
        This will scroll to end of the list in contacts landing page.
        '''
        self.workflow_common_operations.scroll_to_position_vertical(1, scrollbar_objectname=ContactsAppWorkflowObjectIds.scroll_bar_contact_landing_view)
        sleep(3)

    def scroll_to_start_page_in_landing_view_list_scroll_bar(self):
        '''
        This will scroll to start of the list in landing view contacts list1 scroll bar.
        '''
        self.workflow_common_operations.scroll_to_position_vertical(0, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar)
        sleep(1)

    def contacts_wait_for_item(self, item:str):
        '''
        This will wait for given item in parameter
        '''
        record_objectName = "record_" + item + "Row"
        self.spice.wait_for(record_objectName)

    def goto_more_options(self):
        sleep(2)
        current_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_more_option)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        sleep(2)
        current_button.mouse_click(6)

        logging.info("UI: At Contacts More Options view")

    def select_custom_addressbook(self,addressbook_name):
        self.spice.wait_for(ContactsAppWorkflowObjectIds.button_address_book)
        current_button = self.spice.query_item(ContactsAppWorkflowObjectIds.button_address_book)
        current_button.mouse_click()

        self.spice.wait_for("#addressbook_" + addressbook_name)
        current_button = self.spice.query_item("#addressbook_" + addressbook_name)
        current_button.mouse_click()

        logging.info("UI: At Select addressbook view")
    
    def input_password_for_custom_addressbook(self, password):
        '''
        input password for selected custom addressbook
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.enter_password_view)
        password_view = self.spice.wait_for(ContactsAppWorkflowObjectIds.password_edit)
        password_view.mouse_click()
        password_view.__setitem__('displayText', password)
        self.spice.query_item(ContactsAppWorkflowObjectIds.ok_button_keyboard).mouse_click()
    
    def click_submit_button_input_custom_addressbook_password_screen(self):
        '''
        click submit button on input custom addressbook password screen
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.enter_password_view)
        submit_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.submit_button_locator)
        self.spice.validate_button(submit_button)
        submit_button.mouse_click()
    
    def click_cancel_button_input_custom_addressbook_password_screen(self):
        '''
        click cancel button on input custom addressbook password screen
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.enter_password_view)
        cancel_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.cancel_button_locator)
        self.spice.validate_button(cancel_button)
        cancel_button.mouse_click()
    
    def check_contacts_is_existed_by_display_name(self, display_name):
        '''
        This is helper method to verify contact is shows on contacts landing view.
        UI should be in Home->Menu->Contacts
        '''
        current_screen = self.spice.wait_for(ContactsAppWorkflowObjectIds.view_menuContacts)
        self.spice.wait_until(lambda:current_screen["visible"])
        # Wait all contacts load completed
        sleep(2)
        item_object_name = f"#record_{display_name}Row"
        self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.contacts_landing_view_list, item_object_name, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar, ContactsAppWorkflowObjectIds.footer_view, top_item_id=ContactsAppWorkflowObjectIds.custom_section)
        try:
            contacts_item = self.spice.wait_for(item_object_name)
            self.spice.wait_until(lambda:contacts_item["visible"])
        except TimeoutError:
            print(f"TimeoutError: Failed to find the item '{item_object_name}' within the specified time.")
            contacts_item = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            contacts_item = None

    def check_first_and_last_name_in_contacts_detail_view(self, display_name,first_name, last_name):
        '''
        This is helper method to verify first and last name in contact detail view.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.check_contacts_is_existed_by_display_name(display_name)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_first_name)
        first_name_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_first_name_text} {ContactsAppWorkflowObjectIds.text_view}")
        self.spice.wait_until(lambda:first_name_text_view["visible"])
        assert first_name_text_view['text'] == first_name, f"First name is not matched, expected: {first_name}, actual: {first_name_text_view['text']}"
        last_name_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_last_name_text} {ContactsAppWorkflowObjectIds.text_view}")
        self.spice.wait_until(lambda:last_name_text_view["visible"])
        assert last_name_text_view['text'] == last_name, f"Last name is not matched, expected: {last_name}, actual: {last_name_text_view['text']}"
    
    def check_contacts_display_name_in_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list: the contacts list should be sorted
        @return:
        """
        self.spice.wait_for(ContactsAppWorkflowObjectIds.view_menuContacts)
        # Wait all contacts load completed
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)

        sleep(1)
        for display_name in expected_contact_list:
            item_object_name = f"#record_{display_name}Row"
            self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.contacts_landing_view_list, item_object_name, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar, ContactsAppWorkflowObjectIds.footer_view, top_item_id=ContactsAppWorkflowObjectIds.custom_section)
            self.spice.wait_for(item_object_name)
            logging.info(f"-found:{display_name}")
        
        logging.info(f"Check contacts name list {expected_contact_list} success")
        self.workflow_common_operations.scroll_to_position_vertical(0, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar)
    
    def get_sorted_contacts_name_list(self, expect_contacts_list):
        """
        Get contacts name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_contacts_list: 
        @return: contacts_name_list the contacts list should be sorted
        """
        self.spice.wait_for(ContactsAppWorkflowObjectIds.view_menuContacts)
        # Wait all contacts load completed
        sleep(2)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)

        contact_name_to_y_list = []

        for contacts_name in expect_contacts_list:
            item_object_name = f"#record_{contacts_name}Row"
            self.scroll_contact_or_group_item_into_view(ContactsAppWorkflowObjectIds.contacts_landing_view_list, item_object_name, ContactsAppWorkflowObjectIds.contacts_landing_view_list_scroll_bar, ContactsAppWorkflowObjectIds.footer_view, top_item_id=ContactsAppWorkflowObjectIds.custom_section,scroll_height= 50)

            y_coordinate = self.spice.wait_for(item_object_name)["y"]
            contact_name_to_y_list.append({
                "contacts_name": contacts_name,
                "y_coordinate": y_coordinate
            })
            logging.info(f"(get_sorted_contacts_name_list) -found without scroll:{contacts_name}, {y_coordinate}")

        logging.info("(get_sorted_contacts_name_list) sorted list by y coordinate")
        contact_name_to_y_list.sort(key = lambda item: item["y_coordinate"])
        logging.info("(get_sorted_contacts_name_list) get contacts name list sorted by y coordinate")
        contacts_name_list = [i["contacts_name"] for i in contact_name_to_y_list]
        logging.info(f"(get_sorted_contacts_name_list) contacts name list after sorted by y coordinate is <{contacts_name_list}>")
        return contacts_name_list

    def get_email_address_of_contacts(self):
        '''
        get email address from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_email_address)
        email_address_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_email_address_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        email_address_text = email_address_text_view['text']
        return email_address_text

    def get_first_name_of_contacts(self):
        '''
        get first name from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_first_name)
        first_name_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_first_name_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        first_name_text = first_name_text_view['text']
        return first_name_text
    
    def get_last_name_of_contacts(self):
        '''
        get last name from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_last_name)
        last_name_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_last_name_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        last_name_text = last_name_text_view['text']
        return last_name_text
    
    def get_notes_of_contacts(self):
        '''
        get notes from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_view_notes)
        notes_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_notes_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        notes_text = notes_text_view['text']
        return notes_text
    
    def goto_contact_details_network_folder(self):
        '''
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_network_path, ContactsAppWorkflowObjectIds.row_network_path_text],
                                                  ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
    def get_fax_number_of_contacts(self):
        '''
        get fax number from contacts detail screen.
        UI should be in Home->Menu->Contacts->Select a contact.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_fax_number,5)
        fax_number_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_fax_number_text} {ContactsAppWorkflowObjectIds.text_view}",20)
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        fax_number_text = fax_number_text_view['text']
        return fax_number_text
    
    def get_members_text_of_group(self):
        '''
        get members text from group detail screen.
        UI should be in Home->Menu->Contacts->Select a group.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_members)
        members_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_members_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        members_text = members_text_view['text']
        return members_text
    
    def get_notes_text_of_group(self, job, group_name):
        '''
        get members text from group detail screen.
        UI should be in Home->Menu->Contacts->Select a group.
        '''
        acms_supported = job.check_autocolormodeselection_supported(JobType.SCAN_EMAIL)
        if acms_supported == True:
            self.select_contact(group_name)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.row_notes_contact)
        notes_text_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.row_notes_contact_text} {ContactsAppWorkflowObjectIds.text_view}")
        # Wait a few seconds for the actual value to load completed
        sleep(2)
        notes_text = notes_text_view['text']
        return notes_text

    def check_spec_required_fields_empty_message(self, net):
        '''
        Check spec on required fields is empty message screen
        '''
        logging.info("Check spec on required fields is empty message screen")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_string_msg)
        self.spice.common_operations.verify_string(net, "cAllFieldsMarked", ContactsAppWorkflowObjectIds.constrain_description_view)
    
    def check_missing_invalid_entries_message(self, net):
        '''
        Check missing or invalid entries message screen
        '''
        logging.info("Check missing or invalid entries message screen")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_string_msg)
        self.spice.common_operations.verify_string(net, "cCheckInvalidEntries", ContactsAppWorkflowObjectIds.constrain_description_view)
    
    def check_contacts_limit_range_exceeded_message(self, net):
        '''
        Check if no of contacts exceeds the limit
        '''
        logging.info("Check spec on required fields is empty message screen")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.alert_msg, timeout=50)
        self.spice.common_operations.verify_string(net, "cContactsLimitReached", ContactsAppWorkflowObjectIds.message_description_view)
        
    def click_ok_button_required_fields_empty_message_screen(self):
        '''
        click ok button on required fields is empty message screen
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_constrain_screen)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def click_ok_button_contact_name_length_exceeded_screen(self):
        '''
        click ok button on contacts limit range exceeded message screen
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_constrain_screen)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def click_ok_button_maxContacts_message_screen(self):
        '''
        click ok button on max limit reached message screen
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_alert_description)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def check_missing_entries_for_display_name(self, net):
        '''
        Check missing entries for display name
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cCheckInvalidEntries", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.textbox_display_name} {ContactsAppWorkflowObjectIds.helper_message_text_view}",isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str
    
    def check_invalid_entries_for_display_name(self, net):
        '''
        Check invalid entries for display name
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, ["cInvalidCharacters",str("?|")], "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.textbox_display_name} {ContactsAppWorkflowObjectIds.helper_message_text_view}",isSpiceText=True)
        logging.info("AAAAAAA:::::", actual_str, expected_str)
        assert expected_str.replace("%1$s", "") in actual_str

    def check_invalid_path_format_for_network_folder(self, net):
        '''
        Check invalid entries for network folder
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cCheckInvalidEntries", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.textbox_uncFolder_path} {ContactsAppWorkflowObjectIds.helper_message_text_view}",isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str

    def click_ok_button_invalid_path(self,net):
        '''
        Check invalid entries for network folder
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_modal_ok_button)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def check_invalid_credentials_for_network_folder(self, net):
        '''
        Check invalid entries for network folder
        '''
        self.spice.wait_for("#errorMessage",timeout=60)
        expected_str = LocalizationHelper.get_string_translation(net, "cInvokeCmdFailure")
        actual_str = self.spice.wait_for("#errorMessage #alertDetailDescription #contentItem")["text"]
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_model)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def check_network_folder_path_exist_or_not(self, net):
        '''
        Check network folder path exist or not
        '''
        self.spice.wait_for("#errorMessage")
        expected_str = LocalizationHelper.get_string_translation(net, "cPathDoesNotExist")
        actual_str = self.spice.wait_for("#errorMessage #alertDetailDescription #contentItem")["text"]
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_model)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def check_invalid_entries_for_first_name(self, net):
        '''
        Check invalid entries for first name
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cCheckInvalidEntries", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.textbox_first_name} {ContactsAppWorkflowObjectIds.helper_message_text_view}",isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str

    def check_description_message_for_unc_folderpath(self, net):
        '''
        Check description message  for unc folder path
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNoticeUNCPathChange", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.row_object_unc_folder_path} {ContactsAppWorkflowObjectIds.textbox_descriptionText}",isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str

    def check_username_and_password_filed_empty(self, net):
        '''
        Check username and password field values are empty
        '''
        assert self.spice.wait_for("#userNameFieldModel #TextInputBox",2)["text"] == ""
        assert self.spice.wait_for("#passwordFieldModel #TextInputBox",2)["text"] == ""

    def check_username_and_password_filled(self, net, user, isPassSet):
        '''
        Check username and password field values
        '''
        #scroll to username and check the value as per the user
        #then scroll to password and check if the password is already set or not.
        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_username, ContactsAppWorkflowObjectIds.textbox_username],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
        
        userItem = self.spice.wait_for("#userNameFieldModel #TextInputBox", timeout = 2)
        assert userItem["text"] == user

        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_object_password, ContactsAppWorkflowObjectIds.textbox_password],
                                                   ContactsAppWorkflowObjectIds.view_edit_contacts_list_view, select_option = False,
                                                   scrollbar_objectname = ContactsAppWorkflowObjectIds.view_edit_contact_list_scrollbar)
        passwordItem = self.spice.wait_for("#passwordFieldModel #TextInputBox", timeout = 2)
        assert passwordItem["isPasswordAlreadySet"] == isPassSet

    def check_invalid_entries_for_last_name(self, net):
        '''
        Check invalid entries for last name
        '''
        expected_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cCheckInvalidEntries", "en-US")
        actual_str = self.spice.common_operations.get_actual_str(f"{ContactsAppWorkflowObjectIds.textbox_last_name} {ContactsAppWorkflowObjectIds.helper_message_text_view}", isSpiceText=True)
        assert expected_str.replace("%1$s", "") in actual_str

    def check_invalid_entries_for_email_address(self, net):
        '''
        Check invalid entries for email address
        '''
        self.spice.common_operations.verify_string(net, "cInvalidEmailAddress", f"{ContactsAppWorkflowObjectIds.textbox_email} {ContactsAppWorkflowObjectIds.helper_message_text_view}", isSpiceText=True)
    
    def check_invalid_entries_for_fax_number(self, net):
        '''
        Check invalid entries for fax number
        '''
        self.spice.common_operations.verify_string(net, "cCheckInvalidEntries", f"{ContactsAppWorkflowObjectIds.textbox_fax} {ContactsAppWorkflowObjectIds.helper_message_text_view}", isSpiceText=True)

    def check_invalid_entries_for_group_name(self, net):
        '''
        Check invalid entries for group name
        '''
        self.spice.common_operations.verify_string(net, "cCheckInvalidEntries", f"{ContactsAppWorkflowObjectIds.textbox_group_name} {ContactsAppWorkflowObjectIds.helper_message_text_view}", isSpiceText=True)
    
    def check_retry_password_alert_description(self, net):
        '''
        Check retry password description when input invalid password for custom addressbook
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.alert_description)
        self.spice.common_operations.verify_string(net, "cRetryPassword", ContactsAppWorkflowObjectIds.alert_description)
    
    def click_ok_button_on_retry_password_alert_description(self):
        '''
        click ok button on retry password alert description screen
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_alert_description)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def verify_restricted_alert_string(self, net):
        """
        Purpose: Check restricted alert text.
        Should on the restricted alert screen with ok button
        Args: net
        """
        self.spice.wait_for("#noAccessView")
        expected_str = LocalizationHelper.get_string_translation(net, "cItemRestricted")
        actual_str = self.spice.wait_for("#noAccessView #alertDetailDescription #contentItem")["text"]
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_constraint_screen)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def click_search_button(self):
        """
        Click search button in contacts landing view.
        """
        search_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_search_landing_view)
        self.spice.validate_button(search_button)
        search_button.mouse_click()
    
    def input_search_text_in_search_screen(self, search_text):
        """
        Input search text in search screen.
        @param:search_text: str
        """
        logging.info("wait for Search screen")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.view_search_model)
        search_input_view = self.spice.wait_for(ContactsAppWorkflowObjectIds.text_field_search)
        self.spice.wait_until(lambda:search_input_view["visible"])
        self.spice.wait_until(lambda:search_input_view["enabled"])
        search_input_view.mouse_click()
        search_input_view.__setitem__('displayText', search_text)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.hide_keyboard_key).mouse_click()
    
    def click_search_button_in_search_screen(self):
        """
        Click search button in search screen.
        """
        search_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_search)
        self.spice.validate_button(search_button)
        search_button.mouse_click()
    
    def click_cancel_button_in_search_screen(self):
        """
        Click cancel button in search screen.
        """
        cancel_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_cancel)
        self.spice.validate_button(cancel_button)
        cancel_button.mouse_click()
        sleep(2)
    
    def check_spec_search_field_empty_message(self, net):
        '''
        Check spec when search text is empty
        '''
        logging.info("Check spec when search text is empty")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_string_msg)
        self.spice.common_operations.verify_string(net, "cSearchContactName", ContactsAppWorkflowObjectIds.constrain_description_view)
    
    def click_ok_button_search_field_empty_message_screen(self):
        '''
        click ok button on search field is empty message screen
        '''
        ok_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button_constrain_screen)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def click_reset_button(self):
        '''
        click reset button on search result contacts landing view screen
        '''
        reset_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_reset_search)
        sleep(2)
        self.spice.validate_button(reset_button)
        reset_button.mouse_click()
        
    def wait_for_reset_button(self, expected):
        try:
            self.spice.wait_for(ContactsAppWorkflowObjectIds.button_reset_search)
            visible = True
        except:
            visible = False

        return bool(expected == visible)    
    
    def check_spec_no_entries_found(self, net):
        '''
        Check spec no entries found when search no contacts
        '''
        logging.info("Check spec no entries found when search no contacts")
        self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
        actual_text = self.spice.wait_for(ContactsAppWorkflowObjectIds.text_view_empty_record)["text"]
        expected_text = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNoEntriesFound")
        assert actual_text == expected_text, "Failed to check spec no entries found when search no contacts"
    
    def check_spec_search_contacts_ldap_addressbook(self, net):
        '''
        Check spec search contacts when select LDAP address book
        '''
        logging.info("Check spec search contacts when select LDAP address book")
        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
        self.spice.wait_for(ContactsAppWorkflowObjectIds.text_view_search_contacts)
        actual_text = self.spice.wait_for(ContactsAppWorkflowObjectIds.text_view_search_contacts)["text"]
        expected_text = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cSearchContacts")
        assert actual_text == expected_text, "Failed to check spec search contacts when select LDAP address book"
    
    def check_search_result_number_in_contacts_list_view(self, expected_contacts_list):
        """
        Check Search Result numbers shows in contacts list view screen.
        Retries until the expected count matches the actual count or timeout occurs.
        @param: expected_contacts_list: List of expected contacts.
        """
        timeout = 100.0  # Internal timeout value in seconds
        retry_interval = 1.0  # Internal retry interval in seconds

        assert self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)

        start_time = t.time()
        end_time = start_time + timeout  # Calculate the end time outside the loop

        while t.time() < end_time:
            result_number_view = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.search_result_count} {ContactsAppWorkflowObjectIds.text_view}", timeout=60)
            if not result_number_view:
                logging.warning("result_number_view not found. Retrying...")
                sleep(retry_interval)
                continue

            self.spice.wait_until(lambda: result_number_view["visible"], timeout=30)
            result_message = result_number_view["text"]

            if result_message.isdigit() and len(expected_contacts_list) == int(result_message):
                logging.info("check search result number success")
                return

            logging.warning(f"Expected count {len(expected_contacts_list)} does not match actual count {result_message}. Retrying...")
            sleep(retry_interval)

        # Final check after timeout
        if not result_number_view:
            raise ValueError("Failed to locate result_number_view after timeout.")
        result_message = result_number_view["text"]
        assert result_message.isdigit(), f"Search result contains invalid value: '{result_message}'"
        assert len(expected_contacts_list) == int(result_message), f"Search result numbers is error. Expected: {len(expected_contacts_list)}, Actual: {result_message}"
        logging.info("check search result number success")

    def select_sort_order(self, net, sort):
        '''
        Select sort order
        @param:sort: only two order: AtoZ/ZtoA 
        '''
        sort_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_sort)
        sort_icon_string = sort_button['icon']
        logging.info("sort_button is %s,%s,%s", sort_button, sort_icon_string, sort)

        if sort == 'AtoZ':
            if sort_icon_string == "qrc:/images/Glyph/SortAZ.json":
                logging.info("current sorting is Z to A, click sort button to change sort order")
                sort_button.mouse_click()
            else:
                logging.info("current sorting is already A to Z, don't need to click sort button")
        elif sort == 'ZtoA':
            if sort_icon_string == "qrc:/images/Glyph/SortZA.json":
                logging.info("current sorting is A to Z, click sort button to change sort order")
                sort_button.mouse_click()
            else:
                logging.info("current sorting is already Z to A, don't need to click sort button")
        else:
            assert False, f"Sort: {sort} not existing"
        sleep(2)
    
    def back_to_menu_contacts_app(self):
        '''
        UI should be at Menu-> Contacts app landing view.
        Navigates back from Contacts landing view screen to Menu Contacts screen.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
        back_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.back_button_contacts_landing_view)
        back_button.mouse_click()
        if self.spice.uitype != "Workflow2":
            self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
            logging.info("At Menu Screen")
    
    def add_new_contacts(self, contact_details: dict):
        '''
        Add New Contacts screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New -> set contacts details -> Press the save button in add contacts view.
        Args:
            contact_details: new contact details to be set
        '''
        self.goto_add_contact_screen()
        self.set_new_contact(contact_details)
        self.press_save_contact()
    
    def add_new_group(self, group_details: dict):
        '''
        Add New Group screen starting from Contacts Landing Home screen.
        UI Flow is Contacts->Add New Group -> set group details -> Press the save button in add group view.
        Sets group name, members.
        Args:
            group_details: new group details to be set
        '''
        self.goto_add_group_screen()
        self.set_new_group(group_details)
        self.press_save_group()
    
    def select_and_delete_contact(self, contact_name, with_search_screen=False):
        '''
        Delete a Contacts starting from Contacts Landing Home screen.
        UI Flow is Contacts landing view -> Select a contact -> click edit -> click delete button to delete.
        Args:
            contact_name: contact name need to be deleted
            with_search_screen:
        '''
        self.select_contact(contact_name, with_search_screen)
        self.wait_for_edit_contact_screen()
        self.delete_contact()
    
    def select_and_edit_contact(self, contact_name, payload, with_search_screen=False):
        '''
        Edit a Contacts starting from Contacts Landing Home screen.
        UI Flow is Contacts landing view -> Select a contact -> click edit -> edit contacts details -> click save.
        Args:
            contact_name: edit contact name
            payload: edit contact details to be set
            with_search_screen:
        '''
        self.select_contact(contact_name, with_search_screen)
        self.wait_for_edit_contact_screen()
        self.edit_contact(payload)
        self.press_save_contact()
    
    def back_to_contacts_landing_screen_from_contacts_details_screen(self, udw):
        '''
        UI should be at Contact details screen.
        Navigates back from Contact details screen to contact landing screen.
        '''
        # Big screen no need to click back button, UI is already in contact landingview
        ui_size = udw.mainUiApp.ControlPanel.getBreakPoint()
        if ui_size not in ["L","XL","M"]:
            current_button = self.spice.wait_for(f"{ContactsAppWorkflowObjectIds.contacts_details_view_list} {ContactsAppWorkflowObjectIds.button_back}")
            self.spice.validate_button(current_button)
            current_button.mouse_click()
    
    ################# validation method ##########################################################################
    def check_contacts_details_info_ui(self, net, expected_email = "Not Set", expected_fax = "Not Set"):
        """
        check contacts details info with UI
        If the contacts not set email address or number, the default text in UI shows 'Not Set'
        @param: expected_email: default is "Not Set"/ user created
                expected_fax: default is "Not Set"/ user created
        """
        if expected_email == "Not Set":
            expected_email = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
        email_text = self.get_email_address_of_contacts()
        assert email_text == expected_email, "check email address is failed with UI"

        if self.spice.cdm.address_book.get_addressbook_fax_support():
            if expected_fax == "Not Set":
                expected_fax = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
            fax_text = self.get_fax_number_of_contacts()
            assert fax_text == expected_fax, "check fax number is failed with UI"

    def check_contact_name_details_info_ui(self,net,expected_first_name = "Not Set", expected_last_name = "Not Set"):
        """
        check contact name details info with UI
        If the contacts not set first name or last name, the default text in UI shows 'Not Set'
        @param: expected_first_name: default is "Not Set"/ user created
                expected_last_name: default is "Not Set"/ user created
        """
        if expected_first_name == "Not Set":
            expected_first_name = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
        first_name_text = self.get_first_name_of_contacts()
        assert first_name_text == expected_first_name, "check first name is failed with UI"
        
        if expected_last_name == "Not Set":
            expected_last_name = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
        last_name_text = self.get_last_name_of_contacts()
        assert last_name_text == expected_last_name, "check last name is failed with UI"

    def check_contact_notes_details_info_ui(self, net, expected_notes = "Not Set"):
        """
        check contact notes details info with UI
        If the contacts not set notes, the default text in UI shows 'Not Set'
        @param: expected_notes: default is "Not Set"/ user created
        """
        if expected_notes == "Not Set":
            expected_notes = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
        notes_text = self.get_notes_of_contacts()
        assert notes_text == expected_notes, "check notes is failed with UI"

    
    def check_group_details_info_ui(self, net, expected_email = "0 email addresses", expected_fax = "0 fax numbers", expected_members = "0 members"):
        """
        check group details info with UI
        If the group not add contacts or add contacts without set email address or number, the default text in UI shows '"0 email addresses"'/'0 fax numbers'/'0 members'
        @param: expected_email:
                expected_fax:
                expected_members:
        """
        c_email_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cEmailAddressesInGroup")
        email_text = self.get_email_address_of_contacts()
        assert email_text == expected_email.replace("email addresses", c_email_str.replace("%1$d ", "")), "check email address is failed with UI"

        if self.spice.cdm.address_book.get_addressbook_fax_support():
            c_fax_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cFaxNumbersInGroup")
            fax_text = self.get_fax_number_of_contacts()
            assert fax_text == expected_fax.replace("fax numbers", c_fax_str.replace("%1$d ", "")), "check fax number is failed with UI"
        
        c_members_str = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cMembersInGroup")
        members_text = self.get_members_text_of_group()
        assert members_text == expected_members.replace("members", c_members_str.replace("%1$d ", "")), "check members for group is failed with UI"

    def check_group_notes_info_ui(self, net, job, group_name, expected_notes = "Not Set"):
        """
        check group notes details info with UI
        If the group not set notes, the default text in UI shows 'Not Set'
        @param: expected_notes: default is "Not Set"/ user created
        """
        if expected_notes == "Not Set":
            expected_notes = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNotSet")
        notes_text = self.get_notes_text_of_group(job, group_name)
        logging.info(f"notes_text <{notes_text}>")
        assert notes_text == expected_notes, "check notes is failed with UI"

    
    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, scroll_bar, footer_item_id=None,  top_item_id=None, scroll_height=60):
        """
        Scroll contact/group into center of screen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items. One more thing, there are 2 screen to show 100 contacts
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                scroll_bar: object name scroll bar 
                footer_item_id: object name for footer view, keep it as None if it does not included in scroll view
                top_item_id: object name for top view, keep it as None if it does not included in scroll view
        """
        logging.info(f"Try to scroll <{row_item_id}> into view of screen <{row_item_id}>")
        current_screen = self.spice.wait_for(screen_id)
        at_y_end = False
        is_visible = False
        while(is_visible is False and at_y_end is False):
            try:
                is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id, top_item_id)
                while (is_visible is False and at_y_end is False):
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, scroll_height)
                    is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id, top_item_id)
                    at_y_end = current_screen["atYEnd"]
            except Exception as err:
                logging.info(f"exception msg {err}")
                if str(err).find("Query selection returned no items") != -1:
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, scroll_height)
                    at_y_end = current_screen["atYEnd"]
                else:
                    raise Exception(err)
        
        logging.info(f"The item <{row_item_id}> is in screen view <{screen_id}> now: <{is_visible}>")

        return is_visible

    def has_lock_icon(self):
        lock_icon_id = ContactsAppWorkflowObjectIds.view_menuContacts + " #statusIconRect SpiceLottieImageView"

        try:
            lock_icon = self.spice.wait_for(lock_icon_id)
        except:
            logging.info("Failed to find lock icon for Contacts App")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True)
        return lock_icon["visible"] == True
        
    def check_constraint_message(self):
        '''
        This method is used to click on OK button of constraint message.
        '''
        self.spice.wait_for(ContactsAppWorkflowObjectIds.constraint_string_msg) 
        okButton = self.spice.wait_for(ContactsAppWorkflowObjectIds.ok_button) 
        okButton.mouse_click

    def input_fax_number_for_add_contact(self, number:str):
        '''
        This method is input fax number on add contact screen
        Arg: number is string type. eg: '123' '312*'
        '''
        self.spice.wait_for("#keyboard")
        for num in number:
            logging.info(num)
            if num == "*":
                key = self.spice.wait_for("#keyAsterisk")
            elif num == "#":
                key = self.spice.wait_for("#keyHash")
            else:
                key = self.spice.wait_for("#key" + num)
            key.mouse_click()
        
    def select_and_check_selected_contact_checkbox_is_checked(self, item: str):
        """
        Select a contact and verify that its checkbox is checked.
        Args:
            item: The selector for the contact checkbox.
        """
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logging.info(f"Attempt {attempt + 1}: Selecting contact with selector: {item}")
                contact1 = self.spice.wait_for(item)
                self.spice.validate_button(contact1)
                contact1.mouse_click()
                sleep(retry_delay)  # Wait for the UI to update
                if self.spice.wait_for(item)["checked"] == True:
                    logging.info("Contact is successfully selected.")
                    break  # Exit the retry loop if successful
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
            else:
                # If no exception occurs, exit the loop
                break
        else:
            # If all retries fail, raise an error
            raise AssertionError("contact1 is not selected after multiple attempts.")

        sleep(2)
        self.spice.email.click_reset_button()
        back_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        sleep(2)
        self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_contacts_view)
        back_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_back, 2)
        back_button.mouse_click()
    
    def goto_fax_textbox(self):
        '''
        This method is used to go to fax textbox on add contact screen
        '''
        self.workflow_common_operations.goto_item([ContactsAppWorkflowObjectIds.row_fax, ContactsAppWorkflowObjectIds.textbox_fax],
                                                   ContactsAppWorkflowObjectIds.add_contact_list, scrollbar_objectname = ContactsAppWorkflowObjectIds.add_contact_list_scrollbar)
    
    def check_group_member_list_navigation(self):
        logging.info("check_group_member_list_navigation")
        members_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.row_members)
        members_button.mouse_click()
        back_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        # To check whether back button of landing view when pressed exits the application
        if self.spice.uitype != "Workflow2":
            self.spice.wait_for(ContactsAppWorkflowObjectIds.contacts_landing_view_list)
            back_button.mouse_click()
        self.spice.wait_for("#HomeScreenView")

    def is_add_contact_button_locked(self):
        """
        Check if the Add Contact button is locked.
        """
        add_contact_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_contact)
        return add_contact_button["locked"] == True
    
    def is_add_group_button_locked(self):
        """
        Check if the Add Group button is locked.
        """
        add_group_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_add_group)
        return add_group_button["locked"] == True
    
    def is_edit_contact_button_locked(self):
        """
        Check if the Edit Contact button is locked.
        """
        edit_contact_button = self.spice.wait_for(ContactsAppWorkflowObjectIds.button_edit_contacts)
        return edit_contact_button["locked"] == True
