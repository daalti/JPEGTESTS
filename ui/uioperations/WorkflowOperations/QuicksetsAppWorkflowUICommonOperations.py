from dunetuf.ui.uioperations.BaseOperations.IQuicksetsAppUIOperations import IQuicksetsAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowObjectIds import QuicksetsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.send.email.email import *
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
import time
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.ui.uioperations.WorkflowOperations.copy_scan_ui_option_dict import *
from datetime import datetime
from dunetuf.localization.LocalizationHelper import LocalizationHelper
import os
from dunetuf.configuration import Configuration

class QuicksetsAppWorkflowUICommonOperations(IQuicksetsAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

    def goto_copyapp_landing_view_from_home_copyapp(self):
        """
        Printer Home screen -> Copy App -> Corresponding copy item
        """
        self._spice.copy_ui().goto_copy_from_copyapp_at_home_screen()

    def goto_copyapp_landing_view_from_menu_copyapp(self):
        """
        Printer Home screen -> Menu -> Copy App -> Corresponding copy item
        """
        self._spice.copy_ui().goto_copy()
    
    def goto_scanapp_landing_view_from_home_scanapp(self, quickset_type, quickset_name=None, profile_name=None, pin=None, check_default_quickset_is_selected=False):
        """
        Printer Home screen -> Scan App -> Corresponding scan app
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @param profile_name: should provide email profile name when qs type is emaila and server type is user defined server
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        assert quickset_type in ["email", "sharepoint", "usb", "folder"], "Please create quickser with quickset_type <email/sharepoint/usb/folder>"
        self._spice.common_operations.goto_scan_app()
        if quickset_type == "email":
            self._spice.scan_settings.goto_email_from_scanapp_at_home_screen()
            if profile_name:
                server_id = self._get_email_profile_id(self._spice.cdm, self._spice.udw, profile_name)
                SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
                logging.info("Objectname obtained for SMTP server profile")
                current_button = self._spice.wait_for(SCAN_EMAIL_PROFILE, timeout = 15.0)
                self._spice.validate_button(current_button)
                time.sleep(3)
                current_button.mouse_click()
                logging.info("Successfully selected email profile")
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.email_landing_view)
        elif quickset_type == "sharepoint":
            assert quickset_name, "Please provide quickset_name when qs type is sharepoint"
            self._spice.scan_settings.goto_sharepoint_from_scanapp_at_home_screen()
            qs_button = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.quickset_list_screen_view} #{quickset_name}")
            self._spice.validate_button(qs_button)
            qs_button.mouse_click()
            if pin:
                self._spice.sharepoint.check_screen_scan_to_sharepoint_pin_code_prompt()
                self._spice.sharepoint.enter_quickset_pin(pin)
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.sharepoint_landing_view)            
        elif quickset_type == "usb":
            self._spice.scan_settings.goto_usb_from_scanapp_at_home_screen()
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.usb_landing_view) 
        elif quickset_type == "folder":
            self._spice.scan_settings.goto_folder_from_scanapp_at_home_screen()
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.folder_landing_view)

        self._spice.wait_until(lambda: current_screen["visible"])
        time.sleep(1)
        if check_default_quickset_is_selected:
            if quickset_type == "sharepoint":
                assert self.is_quickset_selected(quickset_name, quickset_type), f"The quickset <{quickset_name}> is not in selected status"
                logging.info(f"The quickset <{quickset_name}> is in selected status")
            else:
                assert self.is_quickset_selected("Default", quickset_type), "The quickset <{Default}> is not in selected status"
                logging.info("The quickset <{Default}> is in selected status")

    def _get_email_profile_id(self, cdm, udw, name):
        email = Email(cdm, udw)
        server_id = email.get_email_profile_id(name)
        return server_id

    def goto_select_network_folder(self):
        '''
        UI Flow is Scan to folder->Select->select network folder
        '''
        assert self._spice.wait_for(NetworkFolderAppWorkflowObjectIds.view_scan_network_folder_landing)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, NetworkFolderAppWorkflowObjectIds.scrollbar_scan_to_network_folder_landing_page)
        select_button = self._spice.wait_for(NetworkFolderAppWorkflowObjectIds.button_Folder_contact_select, timeout=80.0)
        self._spice.wait_until(lambda: select_button["visible"]==True, timeout = 100.0)
        assert select_button["visible"] == True, "Select button is not visible"
        sleep(5)
        select_button.mouse_click()

    def goto_cc_and_bcc_checkbox_row_select_cc_checkbox(self):
        '''
        From scan to email landing screen navigate to cc and bcc checkbox row
        UI Flow is from email landing screen -> click on cc and bcc checkbox row
        '''
        logging.info("Navigating to email details screen to access CC and BCC checkbox row")
        assert self._spice.wait_for(EmailAppWorkflowObjectIds.screen_email_interactive_summary), "Email interactive summary screen not found"
        logging.info("Email interactive summary screen found, scrolling to CC and BCC checkbox row")
        
        self.workflow_common_operations.scroll_to_position_vertical(0.25, EmailAppWorkflowObjectIds.scrollbar_email_interactive_summary)

        logging.info("Scrolled to CC and BCC checkbox row, waiting for CC checkbox to be visible")
        
        self._spice.wait_for(EmailAppWorkflowObjectIds.checkbox_email_cc)
        current_button = self._spice.query_item(EmailAppWorkflowObjectIds.checkbox_email_cc)
        self._spice.validate_button(current_button)
        logging.info("Successfully located and verified visibility of CC checkbox")
        current_button.mouse_click()
        assert self._spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)

    def goto_scanapp_landing_view_from_menu_scanapp(self, quickset_type, quickset_name=None, profile_name=None, pin=None, check_default_quickset_is_selected=False):
        """
        Printer Home screen -> Menu -> Scan App -> Corresponding scan app
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @param profile_name: should provide email profile name when qs type is emaila and server type is user defined server
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        assert quickset_type in ["email", "sharepoint", "usb", "folder"], "Please create quickser with quickset_type <email/sharepoint/usb/folder>"

        if quickset_type == "email":
            self._spice.email.scan_operations.goto_scan_app()
            self._spice.email.goto_email()
            if profile_name:
                server_id = self._get_email_profile_id(self._spice.cdm, self._spice.udw, profile_name)
                SCAN_EMAIL_PROFILE = EmailAppWorkflowObjectIds.button_email_smtp_profile + server_id
                logging.info("Objectname obtained for SMTP server profile")
                current_button = self._spice.wait_for(SCAN_EMAIL_PROFILE,timeout=25.0)
                self._spice.validate_button(current_button)
                time.sleep(1)
                current_button.mouse_click()
                logging.info("Successfully selected email profile")
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.email_landing_view)
        elif quickset_type == "sharepoint":
            assert quickset_name, "Please provide quickset_name when qs type is sharepoint"
            self._spice.scan_settings.goto_scan_app() 
            self._spice.scan_settings.goto_sharepoint_from_scanapp_at_menu()
            qs_button = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.quickset_list_screen_view} #{quickset_name}")
            self._spice.validate_button(qs_button)
            qs_button.mouse_click()
            if pin:
                self._spice.sharepoint.check_screen_scan_to_sharepoint_pin_code_prompt()
                self._spice.sharepoint.enter_quickset_pin(pin)
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.sharepoint_landing_view)            
        elif quickset_type == "usb":
            self._spice.usb_scan.goto_scan_to_usb_screen()
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.usb_landing_view)
        elif quickset_type == "folder":
            self._spice.scan_settings.goto_scan_app() 
            self._spice.scan_settings.goto_folder_from_scanapp_at_menu()
            current_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.folder_landing_view)
        
        self._spice.wait_until(lambda: current_screen["visible"])
        time.sleep(1)
        if check_default_quickset_is_selected:
            if quickset_type == "sharepoint":
                assert self.is_quickset_selected(quickset_name, quickset_type), f"The quickset <{quickset_name}> is not in selected status"
                logging.info(f"The quickset <{quickset_name}> is in selected status")
            else:
                assert self.is_quickset_selected("Default", quickset_type), "The quickset <{Default}> is not in selected status"
                logging.info("The quickset <{Default}> is in selected status")

    def perform_signIn(self,spice):
        spice.signIn.select_sign_in_method("admin", "user")
        spice.signIn.enter_creds(True, "admin", "12345678")

    def goto_quicksetapp_landing_view(self, quickset_type):
        """
        Printer Home screen -> Menu -> Quicksets app -> Corresponding app
        @param quickset_type: email/sharepoint/usb/folder/copy
        """
        signed_in = False
        logging.info(f"goto_quicksetapp_landing_view and quickset_type is <{quickset_type}>")
        self._spice.homeMenuUI().goto_menu(self._spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.quick_set_button , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.utilities_section_bottom_border)
        time.sleep(1)
        self._spice.wait_for(MenuAppWorkflowObjectIds.quick_set_button + " SpiceText[visible=true]").mouse_click()
        #need to wait to load login screen
        time.sleep(2)
        #check if sign-in screen is displayed
        try:
            # Check if login page is visible
            login_view =  self._spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
            if login_view and login_view["visible"]:
                logging.info("Login page is visible, performing sign-in")
                self.perform_signIn(self._spice)
                signed_in = True
            else:
                logging.info("Login page is not visible, continuing without sign-in")
        except Exception as e:
            logging.info("Login check failed, continuing without sign-in")

        if quickset_type:
            self._spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)
            menu_list_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view)
            self._spice.wait_until(lambda: menu_list_screen["visible"])
            if quickset_type == 'sharepoint':
                time.sleep(1)
                if not menu_list_screen["atYEnd"]:
                    logging.info(f"need to scroll to screen bottom")
                    max_y = menu_list_screen["contentHeight"] - menu_list_screen["height"]
                    menu_list_screen["contentY"] = menu_list_screen["originY"] + max_y
                    time.sleep(2)

            if quickset_type == "copy":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.copy_item}"
            elif quickset_type == "email":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_email_item}"
            elif quickset_type == "sharepoint":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_sharepoint_item}"
            elif quickset_type == "usb":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_usb_item}"
            elif quickset_type == "folder":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_folder_item}"

            if quickset_type == 'copy':
                item = self._spice.wait_for(item_object)
                if not self._spice.query_item(item_object)["visible"]:
                    item = self._spice.query_item(item_object, 2)
            else:
                item = self._spice.wait_for(f"{item_object} MouseArea")
            item = self._spice.wait_for(f"{item_object} MouseArea")
            item.mouse_click()
            logging.info(f"At quicksetapp_landing_view and quickset_type is <{quickset_type}>")
        else:
            self._spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
            logging.info(f"No corresponding quickset app")
            
        return signed_in
    
    def select_folder_quickset_from_menu_quicksets(self, quickset_name, quickset_type):
        
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickser with quickset_type <email/sharepoint/usb/folder/copy>"
        
        if quickset_type == "email":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.email_landing_view
        elif quickset_type == "sharepoint":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.sharepoint_landing_view
        elif quickset_type == "usb":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.usb_landing_view
        elif quickset_type == "folder":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.folder_landing_view
        elif quickset_type == "copy":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.copy_landing_view


        quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.quicksets_landing_page_view} #{quickset_name} MouseArea")
        self._spice.wait_until(lambda: quickset_item["visible"])
        time.sleep(1)
        quickset_item.mouse_click()
        
        
        

    def is_quickset_selected(self, quickset_name, quickset_type):
        """
        To check if quickset is selectded or not
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @return:
        """
        is_selected = False

        if quickset_type == "email":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.email_landing_view} #{quickset_name}")
        elif quickset_type == "sharepoint":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} #{quickset_name}")
        elif quickset_type == "usb":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} #{quickset_name}")
        elif quickset_type == "folder":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} #{quickset_name}")
        elif quickset_type == "copy":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} #{quickset_name}")

        self._spice.wait_until(lambda: quickset_item["visible"])
        is_selected = quickset_item["checked"]
        logging.info(f"The <{quickset_name}> is selected <{is_selected}>")
        return is_selected

    def select_quickset_from_app_landing_view(self, quickset_name, quickset_type, start_option="user presses start", ana_sign_in_payload=None, pin=None):
        """
        Select quickset by name at scan app landing view
        @param quickset_name: 
        @return:
        """
        logging.info(f"select_quickset_from_app_landing_view <{quickset_name}>")
        is_selected = self.is_quickset_selected(quickset_name, quickset_type)

        if not is_selected:
            if quickset_type == "email":
                quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.email_landing_view} #{quickset_name}")
                quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.email_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            elif quickset_type == "sharepoint":
                quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} #{quickset_name}")
                quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            elif quickset_type == "usb":
                quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} #{quickset_name}")
                quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            elif quickset_type == "folder":
                quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} #{quickset_name}")
                quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            elif quickset_type == "copy":
                quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} #{quickset_name}")
                quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"

            at_end_x = False
            while not is_selected and not at_end_x:
                self._spice.wait_until(lambda: quickset_item["visible"])
                time.sleep(3)
                quickset_item.mouse_click()
                time.sleep(3)
                if pin:
                    if quickset_type == "folder":
                        self._spice.network_folder.enter_quickset_pin(pin)
                    elif quickset_type == "sharepoint":
                        self._spice.sharepoint.check_screen_scan_to_sharepoint_pin_code_prompt()
                        self._spice.sharepoint.enter_quickset_pin(pin)
                is_selected = self.is_quickset_selected(quickset_name, quickset_type)
                if not is_selected:
                    at_end_x = self._scroll_quickset_view_to_right(quickset_menu_view_object)
        
        if is_selected:
            logging.info(f"Success to select quickset <{quickset_name}>")
        else:
            raise Exception(f"Failed to select quickset <{quickset_name}>")

        if ana_sign_in_payload and pin:
            raise Exception("Please don't provide ana_sign_in_payload and pin value at the same time, please just take one of them")

        # if pin:
        #     if quickset_type == "folder":
        #         self._spice.network_folder.enter_quickset_pin(pin)
        #     elif quickset_type == "sharepoint":
        #         self._spice.sharepoint.check_screen_scan_to_sharepoint_pin_code_prompt()
        #         self._spice.sharepoint.enter_quickset_pin(pin)

        if ana_sign_in_payload:
            self._handle_ana_sign_in(ana_sign_in_payload, quickset_name, quickset_type, start_option)

    def _scroll_quickset_view_to_right(self, quickset_menu_view_object, scroll_width=60):
        """
        Scroll quickset view to right so that quickset could be clicked
        """
        quickset_screen = self._spice.wait_for(quickset_menu_view_object)
        quickset_screen_at_end = quickset_screen["atXEnd"]
        
        if not quickset_screen_at_end:
            screen_width = quickset_screen["width"]
            content_width = quickset_screen["contentWidth"]
            max_cotent_x = content_width - screen_width
            current_x = quickset_screen["contentX"]
            quickset_screen["contentX"] = min(current_x + scroll_width, max_cotent_x)
            time.sleep(2)

        quickset_screen_at_end = quickset_screen["atXEnd"]
        logging.info(f"is at x end {quickset_screen_at_end}")
        return quickset_screen_at_end
        
    def goto_viewall_menu_from_app_landing_view(self, quickset_type):
        """
        Click view all button from corresponding scanapp landing view
        """
        logging.info("goto_viewall_menu_from_app_landing_view")
        if quickset_type == "email":
            quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.email_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            quickset_view_all_object = f"{QuicksetsAppWorkflowObjectIds.email_landing_view} {QuicksetsAppWorkflowObjectIds.view_all_button}"
            view_all_screen_object = f"{QuicksetsAppWorkflowObjectIds.view_all_screen}"
        elif quickset_type == "sharepoint":
            quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            quickset_view_all_object = f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} {QuicksetsAppWorkflowObjectIds.view_all_button}"
            view_all_screen_object = f"{QuicksetsAppWorkflowObjectIds.view_all_screen}"
        elif quickset_type == "usb":
            quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            quickset_view_all_object = f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} {QuicksetsAppWorkflowObjectIds.view_all_button}"
            view_all_screen_object = f"{QuicksetsAppWorkflowObjectIds.view_all_screen}"
        elif quickset_type == "folder":
            quickset_menu_view_object = f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            quickset_view_all_object = f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} {QuicksetsAppWorkflowObjectIds.view_all_button}"
            view_all_screen_object = f"{QuicksetsAppWorkflowObjectIds.view_all_screen}"
        elif quickset_type == "copy":
            quickset_menu_view_object =  f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} {QuicksetsAppWorkflowObjectIds.quickset_list_on_landing_view}"
            quickset_view_all_object = f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} {QuicksetsAppWorkflowObjectIds.view_all_button}"
            view_all_screen_object = f"{QuicksetsAppWorkflowObjectIds.view_all_screen}"
        
        quickset_screen = self._spice.wait_for(quickset_menu_view_object)
        self._spice.wait_until(lambda: quickset_screen["visible"])
        time.sleep(2)
        quickset_screen_at_end = quickset_screen["atXEnd"]

        if not quickset_screen_at_end:
            screen_width = quickset_screen["width"]
            content_width = quickset_screen["contentWidth"]
            max_cotent_x = content_width - screen_width
            quickset_screen["contentX"] = max_cotent_x
            time.sleep(2)
        
        view_all_button = self._spice.wait_for(quickset_view_all_object)
        view_all_button.mouse_click()
        view_all_screen = self._spice.wait_for(view_all_screen_object)
        logging.info("At view all screen")
        
    def select_quickset_from_app_viewall_menu(self, quickset_name, quickset_type, pin=None, index=0):
        """
        Select quickset by name at scan view all menu
        @param quickset_name: 
        @return:
        """
        logging.info(f"select_quickset_from_app_viewall_menu <{quickset_type}> <{quickset_name}>")
        qs_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.view_all_screen} #{quickset_name}")
        self._spice.wait_until(lambda: qs_item["visible"])
        time.sleep(2)
        qs_item.mouse_click()
        if pin:
            self._spice.sharepoint.check_screen_scan_to_sharepoint_pin_code_prompt()
            self._spice.sharepoint.enter_quickset_pin(pin, index)
        time.sleep(2)
        is_selected = self.is_quickset_selected(quickset_name, quickset_type)

        assert is_selected, f"The quickset <{quickset_name}> is not in selected status"

    def select_quickset_from_menu_quicksetapp(self, quickset_name, quickset_type, start_option="user presses start", ana_sign_in_payload=None, pin=None, already_on_landing_view=False, short_cut_id=""):
        """
        Select quickset by name at correspoding scan app landing veiw under quickset app
        @param quickset_name:
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param start_option:"user presses start"/"start automatically"
        @param pin, pin for quickset if set this option
        @param ana_sign_in_payload: some printer support sigin feature and should provide authorization when folder/sharepoint sign-in method is "Use credentials of the user currently signed in"
                                    > Please set it to None if you already sign in from Home screen/Don't handle ana sign in with this function
                                    > payload format {"admin":{"password":"12345678"}}/{"printer_user":{"username":"xxxx", "password":"xxx"}}/{"ldap":{"username":"xxxx", "password":"xxx"}}/{"windows":{"username":"xxxx", "password":"xxx"}}
        @param already_on_landing_view, will go to quicksetapp landing view from Home screen if False, could set it True if printer already on quicksetapp landing view
        @return:
        """
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickser with quickset_type <email/sharepoint/usb/folder/copy>"
        assert start_option in ["user presses start", "start automatically"], 'Please take start_option from one of <"user presses start"/"start automatically">'
        signed_in = False

        if quickset_type == "email":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.email_landing_view
        elif quickset_type == "sharepoint":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.sharepoint_landing_view
        elif quickset_type == "usb":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.usb_landing_view
        elif quickset_type == "folder":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.folder_landing_view
        elif quickset_type == "copy":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.copy_landing_view

        if not already_on_landing_view:
            if self._spice.uitype != "Workflow2": 
                signed_in = self.goto_quicksetapp_landing_view(quickset_type)
            else: 
                self._spice.home_operations.goto_home_quicksetapp_landing_view(quickset_type)
        
        quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.quicksets_landing_page_view} #{quickset_name} MouseArea")
        self._spice.wait_until(lambda: quickset_item["visible"])
        time.sleep(1)
        quickset_item.mouse_click()
        logging.info(f"Success to select <{quickset_name}>")

        if ana_sign_in_payload and pin:
            raise Exception("Please don't provide ana_sign_in_payload and pin value at the same time, please just take one of them")

        if pin:
            if quickset_type == "folder":
                self._spice.network_folder.enter_quickset_pin(pin)
            elif quickset_type == "sharepoint":
                self._spice.sharepoint.enter_quickset_pin(pin)

        if self._spice.uitype != "Workflow2" and not signed_in:
            if ana_sign_in_payload:
                self._handle_ana_sign_in(ana_sign_in_payload, quickset_name, quickset_type, start_option)
        
        if start_option == "user presses start":
            logging.info(f"The printer is in screen <{corresponding_app_landing_view_object}>")
            corresponding_app_landing_screen = self._spice.wait_for(corresponding_app_landing_view_object)
            self._spice.wait_until(lambda: corresponding_app_landing_screen["visible"])
            time.sleep(2)
            if quickset_type == "copy":
                # In Copy App quickset name will be short_cut_id
                quickset_name = short_cut_id
            assert self.is_quickset_selected(quickset_name, quickset_type), f"The quickset <{quickset_name}> is not in selected status"

        elif start_option == "start automatically":
            logging.info(f"The quickset job <{quickset_name}> start automatically")
    
    def _handle_ana_sign_in(self, ana_sign_in_payload, quickset_name, quickset_type, start_option):
        self._spice.signIn.verifySignInPopup(expected = False)
        time.sleep(5)
        current_sign_type = self._spice.signIn.current_sigin_user_type()
        if "admin" in ana_sign_in_payload:
            sign_in_type = "admin"
            password = ana_sign_in_payload['admin']['password']
            user_name = None
        elif "printer_user" in ana_sign_in_payload:
            sign_in_type = "user"
            password = ana_sign_in_payload['printer_user']['password']
            user_name = ana_sign_in_payload['printer_user']['username']
        elif "ldap" in ana_sign_in_payload:
            sign_in_type = "ldap"
            password = ana_sign_in_payload['ldap']['password']
            user_name = ana_sign_in_payload['ldap']['username']
        elif "windows" in ana_sign_in_payload:
            sign_in_type = "windows"
            password = ana_sign_in_payload['windows']['password']
            user_name = ana_sign_in_payload['windows']['username']
        
        self._spice.signIn.select_sign_in_method(sign_in_type, current_sign_type)
        self._spice.signIn.enter_creds(True, sign_in_type, password, user_name)

    def _handle_pdf_encryption_code(self, pdf_encryption_code):
        """
        Input pdf encryption password
        """
        logging.info(f"Input pdf encryption password <{pdf_encryption_code}> since pdf encryption is enabled")
        self._spice.scan_settings.pdf_encryption_enter_password(pdf_encryption_code)
        self._spice.scan_settings.pdf_encryption_reenter_password(pdf_encryption_code)
        self._spice.scan_settings.pdf_encryption_save()

    def _handle_prompt(self,payload,pdf_encryption_code):
        """
        Handle prompt when pdf encryption is enabled
        """
        if pdf_encryption_code:
            self._handle_pdf_encryption_code(pdf_encryption_code)
        elif payload["scan_capture_mode"] == "bookMode":
            self._spice.scan_settings.book_mode_instructions_page_scan()
            self._spice.scan_settings.book_mode_instructions_page_finish()
        logging.info(f"Handled prompt <{payload}>")

    
    def compare_ui_copy_scan_settings_with_created_quickset(self, net, quickset_type, payload, job=None, id=None, profile_name=None, pin=None, already_on_setting_screen=False):
        """
        Compare ui scan settings with created quickset
        @param quickset_type: email/sharepoint/usb/folder/copy
        @param payload: please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin
        @param already_on_setting_screen
        @return:
        """
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickset with quickset_type <email/sharepoint/usb/folder>"

        logging.info(f"compare_ui_scan_settings_with_created_quickset: <{payload}>")
        quickset_name = payload['name']
        if not already_on_setting_screen:
            if quickset_type in ["email", "sharepoint", "usb", "folder"]:
                self.goto_scanapp_landing_view_from_menu_scanapp(quickset_type, quickset_name, profile_name, pin)
                self.select_quickset_from_app_landing_view(quickset_name, quickset_type, pin=pin)
            else:
                self.goto_copyapp_landing_view_from_menu_copyapp()
                self.select_quickset_from_app_landing_view(id, quickset_type, pin)
            
            self.goto_app_option_screen(quickset_type)

        if quickset_type == "copy":
            self.verify_common_current_copy_setting(net, payload)
        else:
            self.verify_common_current_scan_setting(net, payload,job)

        self.back_to_app_landing_view_from_option_screen(quickset_type)
    
    def verify_common_current_scan_setting(self, net, payload,job=None):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Settings/Options Landing view
        @param payload: please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        """
        logging.info(f"verify_common_current_scan_setting: <{payload}>")
        # common setting checking
        content_type = payload.get("content_type", None)
        if content_type:
            logging.info(f"verify scan option content type value, expect value is: {content_type}")
            self._spice.scan_settings.verify_setting_string(net, "content_type", scan_content_type_option_dict()[content_type])

        color_mode = payload.get("color_mode", None)
        if color_mode:
            logging.info(f"verify scan option color mode value, expect value is: {color_mode}")
            self._spice.scan_settings.verify_setting_string(net, "color", scan_color_mode_option_dict()[color_mode],job)
        
        original_paper_type = payload.get("original_paper_type", None)
        if original_paper_type:
            logging.info(f"verify scan option original paper type value, expect value is: {original_paper_type}")
            self._spice.scan_settings.verify_setting_string(net, "original_paper_type", scan_original_paper_type_option_dict()[original_paper_type])

        resolution = payload.get("resolution", None)
        if resolution:
            logging.info(f"verify scan option resolution value, expect value is: {resolution}")
            self._spice.scan_settings.verify_setting_string(net, "resolution", scan_scan_resolution_option_dict()[resolution])
        
        original_sides = payload.get("original_sides", None)
        if original_sides:
            logging.info(f"verify scan option original sides value, expect value is: {original_sides}")
            self._spice.scan_settings.verify_setting_string(net, "sides", scan_sides_option_dict()[original_sides])

        original_size = payload.get("original_size", None)
        if original_size:
            logging.info(f"verify scan option original size value, expect value is: {original_size}")
            self._spice.scan_settings.verify_setting_string(net, "size", scan_original_size_option_dict()[original_size])
        
        lighter_darker = payload.get("lighter&darker", None)
        if lighter_darker:
            logging.info(f"verify scan option lighter darker value, expect value is: {lighter_darker}")
            self._spice.scan_settings.verify_setting_lighter_darker_value(lighter_darker)
        
        long_original = payload.get("long_original", None)
        if long_original is not None:
            logging.info(f"verify scan option long original value, expect value is: {long_original}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("long_original", long_original)
        
        auto_release_original = payload.get("auto_release_original", None)
        if auto_release_original is not None:
            logging.info(f"verify scan option auto release original value, expect value is: {auto_release_original}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("auto_release_original", auto_release_original)
        
        black_enhancement = payload.get("black_enhancement", None)
        if black_enhancement is not None:
            logging.info(f"verify scan option black enhancement value, expect value is: {black_enhancement}")
            self._spice.scan_settings.verify_setting_black_enhancement_value(black_enhancement)
        
        detailed_background_removal = payload.get("detailed_background_removal", None)
        if detailed_background_removal:
            logging.info(f"verify scan option detailed background removal value, expect value is: {detailed_background_removal}")
            self._spice.scan_settings.verify_setting_detailed_background_removal_value(detailed_background_removal)
        
        output_size = payload.get("output_size", None)
        if output_size is not None:
            logging.info(f"verify scan option output size value, expect value is: {output_size}")
            self._spice.scan_settings.verify_output_settings_value(net, "output_size", scan_output_size_option_dict()[output_size])
        
        position = payload.get("position", None)
        if position is not None:
            logging.info(f"verify scan option position value, expect value is: {position}")
            self._spice.scan_settings.verify_output_settings_value(net, "position", scan_positioning_option_dict()[position])

        output_canvas_orientation = payload.get("output_canvas_orientation", None)
        if output_canvas_orientation is not None:
            logging.info(f"verify scan option output canvas orientation value, expect value is: {output_canvas_orientation}")
            self._spice.scan_settings.verify_output_settings_value(net, "output_canvas_orientation", scan_output_canvas_orientation_option_dict()[output_canvas_orientation])

        background_color_removal = payload.get("background_color_removal", None)
        if background_color_removal is not None:
            logging.info(f"verify scan option background color removal value, expect value is: {background_color_removal}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("background_color_removal", background_color_removal)
        
        background_noise_removal = payload.get("background_noise_removal", None)
        if background_noise_removal is not None:
            logging.info(f"verify scan option background noise removal value, expect value is: {background_noise_removal}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("background_noise_removal", background_noise_removal)
        
        automatic_desknew = payload.get("automatic_desknew", None)
        if automatic_desknew is not None:
            logging.info(f"verify scan option automatic desknew value, expect value is: {automatic_desknew}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("automatic_desknew", automatic_desknew)

        edge_to_edge_output = payload.get("edge_to_edge_output", None)
        if edge_to_edge_output is not None:
            logging.info(f"verify scan option edge to edge output value, expect value is: {edge_to_edge_output}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("edge_to_edge_output", edge_to_edge_output)
        
        reduce_scan_speed_to_enhance_quality = payload.get("reduce_scan_speed_to_enhance_quality", None)
        if reduce_scan_speed_to_enhance_quality is not None:
            logging.info(f"verify scan option reduce scan speed to enhance quality value, expect value is: {reduce_scan_speed_to_enhance_quality}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("reduce_scan_speed_to_enhance_quality", reduce_scan_speed_to_enhance_quality)
        
        invert_blueprint = payload.get("invert_blueprint", None)
        if invert_blueprint is not None:
            logging.info(f"verify scan option invert colors value, expect value is: {invert_blueprint}")
            self._spice.scan_settings.verify_scan_setting_toggle_option_value("invert_blueprint", invert_blueprint)
        
        file_type = payload.get("file_type", None)
        if file_type:
            logging.info(f"verify scan option file type value, expect value is: {file_type}")
            self._spice.scan_settings.verify_setting_string(net, "filetype", scan_file_type_option_dict()[file_type])
        
        pdf_encryption = payload.get("pdf_encryption", None)
        if pdf_encryption is not None:
            logging.info(f"verify scan option pdf encryption value, expect value is: {pdf_encryption}")
            self._spice.scan_settings.verify_settings_pdf_encryption_value(pdf_encryption)
        
        high_compression = payload.get("contenthigh_compression_type", None)
        if high_compression is not None:
            logging.info(f"verify scan option high compression value, expect value is: {high_compression}")
            self._spice.scan_settings.verify_settings_high_compression_value(high_compression)

        file_size = payload.get("file_size", None)
        if file_size:
            logging.info(f"verify scan option file size value, expect value is: {file_size}")
            self._spice.scan_settings.verify_setting_string(net, "filesize", scan_file_size_option_dict()[file_size])

        orientation = payload.get("orientation", None)
        if orientation:
            logging.info(f"verify scan option orientation value, expect value is: {orientation}")
            self._spice.scan_settings.verify_setting_string(net, "orientation", scan_orientation_option_dict()[orientation])
    
    def verify_common_current_copy_setting(self, net, payload):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Copy/Options Landing view
        @param payload: please refer to structure from copy_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        """
        paper_selection = {}
        logging.info(f"verify_common_current_copy_setting: <{payload}>")
        # copy common setting checking
        content_type = payload.get("content_type", None)
        if content_type:
            logging.info(f"verify copy option content type value, expect value is: {content_type}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "content_type", copy_content_type_option_dict()[content_type])
        
        original_sides = payload.get("original_size", None)
        if original_sides:
            logging.info(f"verify copy option original sides value, expect value is: {original_sides}")
            self._spice.copy_ui().verify_copy_mediasize_selected_option(net, "original", copy_original_size_option_dict()[original_sides])

        color_mode = payload.get("color_mode", None)
        if color_mode:
            logging.info(f"verify copy option color mode value, expect value is: {color_mode}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "color", copy_color_mode_option_dict()[color_mode])
        
        two_sided_pages_flip_up = payload.get("two_sided_pages_flip_up", None)
        if two_sided_pages_flip_up is not None:
            logging.info(f"verify copy option two sided pages flip up value, expect value is: {two_sided_pages_flip_up}")
            self._spice.copy_ui().verify_copy_setting_2sided_pages_flip_up_status(two_sided_pages_flip_up)

        lighter_darker = payload.get("lighter_darker", None)
        if lighter_darker:
            logging.info(f"verify copy option lighter darker value, expect value is: {lighter_darker}")
            self._spice.copy_ui().verify_copy_setting_lighter_darker_value(lighter_darker)
        
        number_of_copies = payload.get("number_of_copies", None)
        if number_of_copies:
            logging.info(f"verify copy option number of copies value, expect value is: {number_of_copies}")
            copies_value = self._spice.copy_ui().get_number_of_copies()
            assert copies_value == number_of_copies

        output_scale = payload.get("output_scale", None)
        output_scale_value = ""
        if output_scale:
            if output_scale == 'custom':
                precise_scaling_amount = payload.get("precise_scaling_amount", None)
                if precise_scaling_amount:
                    output_scale_value = copy_output_scale_option_dict()[output_scale] + " " + precise_scaling_amount + "%"
                else:
                    output_scale_value = copy_output_scale_option_dict()[output_scale] + " 100%" 
            else:
                output_scale_value = copy_output_scale_option_dict()[output_scale]
            logging.info(f"verify copy option output scale value, expect value is: {output_scale_value}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "output_scale", output_scale_value)   

        paper_size = payload.get("paper_size", None)
        if paper_size:
            paper_selection["paper_size"] = paper_size
        paper_tray = payload.get("paper_tray", None)
        if paper_tray: 
            paper_selection["paper_tray"] = paper_tray
        paper_type = payload.get("paper_type", None)
        if paper_type:
            paper_selection["paper_type"] = paper_type

        if paper_selection:
            self._spice.copy_ui().go_to_paper_selection()
            for key, val in paper_selection.items():
                logging.info(f"Verify paper selection option {key} value")
                self._spice.copy_ui().verify_copy_paper_selection_option(net, key, val)
            
            self._spice.copy_ui().go_back_to_setting_from_paper_selection()
        
        quality = payload.get("quality", None)
        if quality:
            logging.info(f"verify copy option quality value, expect value is: {quality}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "quality", copy_file_quality_option_dict()[quality])

        sides = payload.get("sides", None)
        if sides:
            logging.info(f"verify copy option sides value, expect value is: {sides}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "sides", copy_sides_option_dict()[sides])
        
        pages_per_sheet = payload.get("pages_per_sheet", None)
        if pages_per_sheet:
            logging.info(f"verify copy option pages per sheet value, expect value is: {pages_per_sheet}")
            self._spice.copy_ui().verify_copy_settings_selected_option(net, "pages_per_sheet", copy_pagesper_sheet_option_dict()[pages_per_sheet])

        collate = payload.get("collate", None)
        if collate is not None:
            logging.info(f"verify copy option collate value, expect value is: {collate}")
            self._spice.copy_ui().verify_copy_setting_collate_status(collate)

    def perform_quickset_job_from_home_app(self, net, job, ews_quicksets_app, quickset_type, payload, profile_name=None, pin=None, pages=1, time_out=90, pdf_encryption_code=None, select_from_view_all_menu=False, check_default_quickset_is_selected=False):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Scan/Copy -> Corresponding app - > perform quickset job
        5. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to structure from quickset_base_payload, scan_common_setting_payload and quickset_email_payload/quickset_sharepoint_payload/quickset_folder_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled 
        @param select_from_view_all_menu: select quickset from view all menu
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        logging.info(f"Perform quickset job from home app <{quickset_type}> <{payload}> <{profile_name}>")
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickser with quickset_type <email/sharepoint/usb/folder/copy>"

        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)
        
        logging.info(f"check {quickset_type} quickset option value with UI") 
        short_cut_id = ews_quicksets_app.csc.get_shortcut_id(payload["name"])
        self.compare_ui_copy_scan_settings_with_created_quickset(net, quickset_type, payload, job=job, id=short_cut_id, profile_name=profile_name, pin=pin, already_on_setting_screen=False)

        if quickset_type == "copy":
            logging.info(f"check {quickset_type} quickset payload with cdm")
            ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)
            self.goto_copyapp_landing_view_from_home_copyapp()
            if select_from_view_all_menu:
                self.goto_viewall_menu_from_app_landing_view(quickset_type=quickset_type)
                self.select_quickset_from_app_viewall_menu(quickset_name=short_cut_id, quickset_type=quickset_type)
            else:
                self.select_quickset_from_app_landing_view(short_cut_id, quickset_type)
            self.start_quickset_job(quickset_type)
            self.wait_for_copy_quickset_job_to_complete(net, job, sides=payload.get('sides'), time_out=time_out)
        else:
            logging.info(f"check {quickset_type} quickset payload with cdm")
            ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)
            self.goto_scanapp_landing_view_from_home_scanapp(quickset_type, quickset_name=payload["name"], profile_name=profile_name, pin=pin, check_default_quickset_is_selected=check_default_quickset_is_selected)
            if select_from_view_all_menu:
                self.goto_viewall_menu_from_app_landing_view(quickset_type=quickset_type)
                self.select_quickset_from_app_viewall_menu(quickset_name=payload["name"], quickset_type=quickset_type, pin=pin)
            else:
                self.select_quickset_from_app_landing_view(payload["name"], quickset_type, pin=pin)
            self.start_quickset_job(quickset_type)
            if pdf_encryption_code:
                self._handle_pdf_encryption_code(pdf_encryption_code)
            self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out)


    def media_mismatch_size_flow(self,net,locale: str = "en"):
        '''
        UI should be in Media size mismatch alert popup.
        Press Ok button from the media mismatch alert
        '''
        try:
            time.sleep(3)
            self._spice.wait_for(CopyAppWorkflowObjectIds.media_mismatch_flow)
            ok_button = self._spice.query_item(CopyAppWorkflowObjectIds.media_mismatch_alert_ok)
            ok_button.mouse_click()
            time.sleep(1)
        except Exception:
            logging.info("No mismatch pop-up displayed")

    def perform_quickset_job_from_menu_app(self,net, job, ews_quicksets_app, quickset_type, payload, profile_name=None, pin=None, pages=1, time_out=120, pdf_encryption_code=None, select_from_view_all_menu=False, check_default_quickset_is_selected=False,checkPrompt=False):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Menu -> Scan/Copy -> Corresponding app - > perform quickset job
        5. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to structure from quickset_base_payload, scan_common_setting_payload and quickset_email_payload/quickset_sharepoint_payload/quickset_folder_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param select_from_view_all_menu: select quickset from view all menu
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False 
        """
        logging.info(f"Perform quickset job from home menu app <{quickset_type}> <{payload}> <{profile_name}>")
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickser with quickset_type <email/sharepoint/usb/folder/copy>"
        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)
        
        logging.info(f"check {quickset_type} quickset option value with UI")  
        short_cut_id = ews_quicksets_app.csc.get_shortcut_id(payload["name"])
        self.compare_ui_copy_scan_settings_with_created_quickset(net, quickset_type, payload, job=job, id=short_cut_id, profile_name=profile_name, pin=pin, already_on_setting_screen=False)

        if quickset_type == "copy":
            ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)
            self.goto_copyapp_landing_view_from_menu_copyapp()
            if select_from_view_all_menu:
                self.goto_viewall_menu_from_app_landing_view(quickset_type=quickset_type)
                self.select_quickset_from_app_viewall_menu(quickset_name=short_cut_id, quickset_type=quickset_type)
            else:
                self.select_quickset_from_app_landing_view(short_cut_id, quickset_type)
            self.start_quickset_job(quickset_type)
            self.media_mismatch_size_flow(net)
            self.wait_for_copy_quickset_job_to_complete(net, job, sides=payload.get('sides'), time_out=time_out)
        else:
            logging.info(f"check {quickset_type} quickset payload with cdm")
            ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)
            self.goto_scanapp_landing_view_from_menu_scanapp(quickset_type, quickset_name=payload["name"], profile_name=profile_name, pin=pin, check_default_quickset_is_selected=check_default_quickset_is_selected)
            if select_from_view_all_menu:
                self.goto_viewall_menu_from_app_landing_view(quickset_type=quickset_type)
                self.select_quickset_from_app_viewall_menu(quickset_name=payload["name"], quickset_type=quickset_type, pin=pin)
            else:
                self.select_quickset_from_app_landing_view(payload["name"], quickset_type, pin=pin)
            self.start_quickset_job(quickset_type)
            if checkPrompt:
                self._handle_prompt(payload,pdf_encryption_code)
            self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out)

    def perform_quickset_job_from_menu_quicksetapp(self,net, job, ews_quicksets_app, quickset_type, payload, ana_sign_in_payload=None, pin=None, pages=1, time_out=90, pdf_encryption_code=None):
        """
        Home screen -> Menu -> Quicksets app
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Menu -> Quicksets app -> Corresponding app - > perform quickset job
        5. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to structure from quickset_base_payload, scan_common_setting_payload and quickset_email_payload/quickset_sharepoint_payload/quickset_folder_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param ana_sign_in_payload: some printer support sign in feature and should provide authorization when folder/sharepoint sign-in method is "Use credentials of the user currently signed in"
                                    > Please set it to None if you already sign in from Home screen/Don't handle ana sign in with this function
                                    > payload format {"admin":{"password":"12345678"}}/{"printer_user":{"username":"xxxx", "password":"xxx"}}/{"ldap":{"username":"xxxx", "password":"xxx"}}/{"windows":{"username":"xxxx", "password":"xxx"}} 
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled 
        """
        logging.info(f"Perform quickset job from menu quicksetapp <{quickset_type}> <{payload}>")

        start_option = payload.get("start_option", None)
        quickset_name = payload["name"]

        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)

        logging.info(f"check {quickset_type} quickset option value with UI")  
        short_cut_id = ews_quicksets_app.csc.get_shortcut_id(payload["name"])
        self.compare_ui_copy_scan_settings_with_created_quickset(net, quickset_type, payload, job=job, id=short_cut_id,  pin=pin, already_on_setting_screen=False)

        if quickset_type == "copy":
            self._spice.goto_homescreen()
    
        logging.info(f"check {quickset_type} quickset payload with cdm")
        ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)

        self.select_quickset_from_menu_quicksetapp(quickset_name, quickset_type, start_option=start_option, ana_sign_in_payload=ana_sign_in_payload, pin=pin, already_on_landing_view=False, short_cut_id=short_cut_id)
        
        if start_option == "user presses start":
            self.start_quickset_job(quickset_type)
        
        elif start_option == "start automatically":
            logging.info(f"The quickset job <{quickset_name}> start automatically")

        if quickset_type == "copy":
            self.media_mismatch_size_flow(net)
            self.wait_for_copy_quickset_job_to_complete(net, job, sides=payload.get("sides"), time_out=time_out)
        else:
            if pdf_encryption_code:
                self._handle_pdf_encryption_code(pdf_encryption_code)

            self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out)
    
    def is_tray_support_mediaSize(self, media_size_data, tray, media_size):
        """
        Check if the tray supports the media size and paper type
        """
        if(len(media_size_data) > 0):
            for media in media_size_data:
                if media == media_size:
                    return True
        else:
            logging.error(f"Tray {tray} does not support any media size / media size data is empty")
            return False
    
    def is_tray_support_mediaType(self, media_type_data, tray, paper_type):
        """
        Check if the tray supports the paper type
        """
        if( len(media_type_data) > 0):
            for paper in media_type_data:
                if paper == paper_type:
                    return True
        else:
            logging.error(f"Tray {tray} does not support any paper type / paper type data is empty")
            return False

    def perform_quickset_job_and_check_file_name(self, net, job, ews_quicksets_app, quickset_type, payload, file_name, file_type,
                                                    prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='',
                                                    prefix_username='admin', suffix_username='admin', profile_name=None,
                                                    pin=None, pages=1, time_out=90):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Home screen -> Menu -> Scan -> Corresponding app - > perform quickset job
        3. Get preview file name from job details, and check file name
        4. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder
        @param payload: mainly set filename info, please refer to structure from quickset_base_payload, scan_common_setting_payload and quickset_email_payload/quickset_sharepoint_payload/quickset_folder_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param file_name:  file_name from settings
        @param file_type:  file_type from settings, value from key of scan_file_type_option_dict
        @param prefix_type:  prefix_type from settings, value from key of scan_file_name_prefix_option_dict
        @param suffix_type:  suffix_type from settings, value from key of scan_file_name_suffix_option_dict
        @param custom_prefix_string: custom_prefix_string comes from Settings, only custom has Settings
        @param custom_suffix_string:  custom_suffix_string comes from Settings, only custom has Settings
        @param prefix_username: prefix_username select username from settings
        @param suffix_username: suffix_username select username from settings
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish 
        """
        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)

        self.goto_scanapp_landing_view_from_menu_scanapp(quickset_type, quickset_name=payload["name"], profile_name=profile_name, pin=pin)
        self.select_quickset_from_app_landing_view(payload["name"], quickset_type, pin=pin)

        if quickset_type == "email":
            job_type = 'scanEmail'
        elif quickset_type == "sharepoint":
            job_type = 'scanSharePoint'
        elif quickset_type == "usb":
            job_type = 'scanUsb'
        elif quickset_type == "folder":
            job_type = 'scanNetworkFolder'

        self.start_quickset_job(quickset_type)
        # get file name preview from job details and check file name
        job_ticket = job.get_job_details(job_type)
        preview_file_name = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileNamePreview"]
        logging.info(f'preview file name from job details is: {preview_file_name}')
        self.validate_scan_file_name(preview_file_name, file_name, file_type, prefix_type, suffix_type,
                                        custom_prefix_string, custom_suffix_string,
                                        prefix_username, suffix_username)
        
        self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out)
    
    def start_quickset_job(self, quickset_type, click_send: bool = False, wait_for_landing: bool = False):
        """
        Click send/copy button in Corresponding app landing view
        """
        logging.info(f"click send/copy button to start job in landing view")
        if quickset_type == "copy":
            self._spice.copy_ui().start_copy()
        elif quickset_type == "email":
            self._spice.email.email_send(need_to_wait_email_landing_view = wait_for_landing)
        elif quickset_type == "sharepoint":
            self._spice.sharepoint.save_to_sharepoint(wait_time=0)
        elif quickset_type == "usb":
            self._spice.usb_scan.press_save_to_usb(wait_time=0)
        elif quickset_type == "folder":
            self._spice.network_folder.save_to_network_folder(click_send=click_send)

    def wait_for_scan_quickset_job_to_complete(self, net, job, quickset_type, pages=1, time_out=90, final_job_status="success", wait_for_landing: bool = True):
        """
        @param quickset_type quickset_type:email/sharepoint/usb/folder
        """
        configuration = Configuration(self._spice.cdm)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        scan_resource = common_instance.scan_resource()

        if scan_resource == "Glass":
            try:
                for _ in range(pages-1):
                    scan_add_page_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                    self._spice.validate_button(scan_add_page_button)
                    scan_add_page_button.mouse_click()
                    time.sleep(2)

                scan_add_page_done_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                logging.info("#finish button found")
                self._spice.validate_button(scan_add_page_done_button)
                scan_add_page_done_button.mouse_click()
            except TimeoutError:
                logging.info("flatbed Add page is not available")

        elif scan_resource == "MDF":
            if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
                # todo: need to add multiple page scene when bug DUNE-147017 fixed.
                self._spice.scan_settings.mdf_add_page_alert_done()
            elif configuration.productname == "jupiter" :
                for _ in range(pages-1):
                    self._spice.scan_settings.validate_scan_send_button(net, ScanAppWorkflowObjectIds.button_start_detail_right_block)
                    self._spice.udw.mainApp.ScanMedia.loadMedia("MDF")
                    sleep(2)

                # All pages scanned, finish the job by pressing done button.
                scan_done_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_main_right_block)
                self._spice.validate_button(scan_done_button, time_out)
                scan_done_button.mouse_click()
        
        if quickset_type == "email":
            job_type = "scanEmail"
        elif quickset_type == "sharepoint":
            job_type = "scanSharePoint"
        elif quickset_type == "usb":
            job_type = "scanUsb"
        elif quickset_type == "folder":
            job_type = "scanNetworkFolder"
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": job_type, "status": final_job_status}])
        # wait for status dismiss
        time.sleep(7)

    def wait_for_copy_quickset_job_to_complete(self, net, job, sides='1_to_1_sided', time_out=90):
        """
        @param quickset_type quickset_type:copy
        """
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        scan_resource = common_instance.scan_resource()

        if scan_resource == "Glass":
            if sides in ["1_to_2_sided", "2_to_1_sided", "2_to_2_sided"]:
                self._spice.copy_ui().select_copy_2sided_operation(CopyAppWorkflowObjectIds.duplex_copy_continue)
                time.sleep(2)
        elif scan_resource == "MDF":
            self._spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()
        
        job.check_job_log_by_status_and_type_cdm([{"type": "copy", "status": "success"}])
        # wait for status dismiss
        time.sleep(7)
    
    def validate_scan_file_name(self, final_file_name: str, file_name: str, file_type: str, prefix_type: str, suffix_type: str,
                                custom_prefix_string: str = '', custom_suffix_string: str = '', prefix_username: str = 'admin',
                                suffix_username: str = 'admin'):
        """
        Validate scan file name
        :param final_file_name: ews page preview file name or preview file name get from job details.
        :param file_name:  file_name from settings
        :param file_type:  file_type from settings, value from key of scan_file_type_option_dict
        :param prefix_type:  prefix_type from settings, value from key of scan_file_name_prefix_option_dict
        :param suffix_type:  suffix_type from settings, value from key of scan_file_name_suffix_option_dict
        :param custom_prefix_string: custom_prefix_string comes from Settings, only custom has Settings
        :param custom_suffix_string:  custom_suffix_string comes from Settings, only custom has Settings
        :param prefix_username: prefix_username select username from settings
        :param suffix_username: suffix_username select username from settings
        :return:
        """
        preview_file, preview_file_type = os.path.splitext(final_file_name)
        preview_file_type = preview_file_type.lstrip(".")
        logging.info(f"preview file is:{preview_file}")
        logging.info(f"preview file type is:{preview_file_type}")
        logging.info(f"file name is:{file_name}") 
        # check file type
        if file_type == "pdf_a":
            assert preview_file_type == "pdf", 'File type error'
        elif file_type == "tiff":
            assert preview_file_type in ["tif", "tiff"], 'File type error'
        else:
            assert preview_file_type == file_type, 'File type error'

        assert file_name in preview_file, 'File name error'  # check file_name

        # check prefix
        if prefix_type == "custom":
            assert preview_file.startswith(custom_prefix_string + file_name)

        elif prefix_type == "user_name_security_username":
            assert preview_file.startswith(prefix_username + file_name)

        elif prefix_type == "time_device_time_hhmmss":
            file_pre = preview_file[:6]
            time_formatting = datetime.strptime(file_pre, '%H%M%S')
            logging.info("Prefix time formatting succeeded")

        elif prefix_type == "date_device_date_yyyymmdd":
            file_pre = preview_file[:8]
            date_formatting = datetime.strptime(file_pre, '%Y%m%d')
            logging.info("Prefix date formatting succeeded")

        elif prefix_type == "date_device_date_ddmmyyyy":
            file_pre = preview_file[:8]
            date_formatting = datetime.strptime(file_pre, '%d%m%Y')
            logging.info("Prefix date formatting succeeded")

        elif prefix_type == "date_device_date_mmddyyyy":
            file_pre = preview_file[:8]
            date_formatting = datetime.strptime(file_pre, '%m%d%Y')
            logging.info("Prefix date formatting succeeded")
        # TODO: Handle multiple suffix
        # else:
        #     raise ValueError('prefix_file_name args error')

        # check suffix
        if suffix_type == "custom":
            logging.info(f"custom_suffix_string is:{custom_suffix_string}")
            assert preview_file.endswith(file_name + custom_suffix_string)

        elif suffix_type == "user_name_security_username":
            assert preview_file.endswith(file_name + suffix_username)

        elif suffix_type == "time_device_time_hhmmss":
            file_suf = preview_file[-6:]
            time_formatting = datetime.strptime(file_suf, '%H%M%S')
            logging.info("Suffix time formatting succeeded")

        elif suffix_type == "date_device_date_yyyymmdd":
            file_suf = preview_file[-8:]
            date_formatting = datetime.strptime(file_suf, '%Y%m%d')
            logging.info("Suffix date formatting succeeded")

        elif suffix_type == "date_device_date_ddmmyyyy":
            file_suf = preview_file[-8:]
            date_formatting = datetime.strptime(file_suf, '%d%m%Y')
            logging.info("Suffix date formatting succeeded")

        elif suffix_type == "date_device_date_mmddyyyy":
            file_suf = preview_file[-8:]
            date_formatting = datetime.strptime(file_suf, '%m%d%Y')
            logging.info("Suffix date formatting succeeded")
        elif suffix_type == "date_device_date_yyyymmdd_time_device_time_hhmmss":
            file_suf_time = preview_file[-6:]
            time_formatting = datetime.strptime(file_suf_time, '%H%M%S')
            file_suf_date = preview_file[-15:-7]
            date_formatting = datetime.strptime(file_suf_date, '%Y%m%d')
            file_suffix = "_"+file_suf_date+"_"+file_suf_time
            logging.info(f"Suffix date formatting succeeded file_suffix = {file_suffix}")
            assert preview_file.endswith(file_name + file_suffix)
            logging.info(f"Suffix date formatting succeeded date_formatting = {date_formatting}")
        # TODO: Handle multiple suffix
        # else:
        #     raise ValueError('suffix_file_name args error')
        
        logging.info("check preview file name is pass")

    def perform_scan_quickset_job_with_changed_setting_from_ui(self, net, job, ews_quicksets_app, quickset_type, payload, changed_scan_option_pyload, profile_name=None, pin=None, pages=1, time_out=90):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Change the corresponding setting from printer UI
        3. Perform this quickset job
        4. Wait for job finish
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder
        @param payload: please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param changed_original_size: the original size set from UI
        """
        logging.info(f"perform_scan_quickset_job_with_changed_setting_from_ui <{quickset_type}> <{payload}> <{profile_name}>")
        assert quickset_type in ["email", "sharepoint", "usb", "folder"], "Please create quickser with quickset_type <email/sharepoint/usb/folder>"

        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)
        self.goto_scanapp_landing_view_from_menu_scanapp(quickset_type, quickset_name=payload["name"], profile_name=profile_name, pin=pin)
        self.goto_app_option_screen(quickset_type)
        self.change_scan_option_setting(changed_scan_option_pyload)
        self.verify_common_current_scan_setting(net, changed_scan_option_pyload)
        self.back_to_app_landing_view_from_option_screen(quickset_type)
        self.start_quickset_job(quickset_type)
        ews_quicksets_app.csc.validate_cdm_job_ticket_details(job, quickset_type, changed_scan_option_pyload)
        self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out)

    def goto_app_option_screen(self, quickset_type):
        """
        Goto app option screen from app landing view
        """
        logging.info(f"goto_app_option_screen <{quickset_type}>")
        if quickset_type == "email":
            option_button_object = f"{QuicksetsAppWorkflowObjectIds.email_landing_view} {QuicksetsAppWorkflowObjectIds.scan_options_button}"
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.emailappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
        elif quickset_type == "sharepoint":
            option_button_object = f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} {QuicksetsAppWorkflowObjectIds.scan_options_button}"
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.sharepointappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
        elif quickset_type == "usb":
            option_button_object = f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} {QuicksetsAppWorkflowObjectIds.scan_options_button}"
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.usbappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
        elif quickset_type == "folder":
            option_button_object = f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} {QuicksetsAppWorkflowObjectIds.scan_options_button}"
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.folderappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
        elif quickset_type == "copy":
            option_button_object = f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} {QuicksetsAppWorkflowObjectIds.copy_options_button}"
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.copyappapplicationstackview} {QuicksetsAppWorkflowObjectIds.copy_settings_screen}"

        option_button = self._spice.wait_for(option_button_object)
        self._spice.wait_until(lambda: option_button['visible'])
        time.sleep(2)
        option_button.mouse_click()
        screen_setting = self._spice.wait_for(screen_setting_object)
        self._spice.wait_until(lambda: screen_setting['visible'])
        time.sleep(2)
        logging.info("At the setting screen")

    def back_to_app_landing_view_from_option_screen(self, quickset_type):
        logging.info(f"back_to_app_landing_view_from_option_screen <{quickset_type}>")
        if quickset_type == "email":
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.emailappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
            colse_button_object = f"{screen_setting_object} {QuicksetsAppWorkflowObjectIds.close_button}"
        elif quickset_type == "sharepoint":
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.sharepointappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
            colse_button_object = f"{screen_setting_object} {QuicksetsAppWorkflowObjectIds.close_button}"
        elif quickset_type == "usb":
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.usbappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
            colse_button_object = f"{screen_setting_object} {QuicksetsAppWorkflowObjectIds.close_button}"
        elif quickset_type == "folder":
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.folderappapplicationstackview} {QuicksetsAppWorkflowObjectIds.scan_settings_screen}"
            colse_button_object = f"{screen_setting_object} {QuicksetsAppWorkflowObjectIds.close_button}"
        elif quickset_type == "copy":
            screen_setting_object = f"{QuicksetsAppWorkflowObjectIds.copyappapplicationstackview} {QuicksetsAppWorkflowObjectIds.copy_settings_screen}"
            colse_button_object = f"{screen_setting_object} {QuicksetsAppWorkflowObjectIds.close_button}"

        logging.info("Go back to app landing view")
        close_button = self._spice.wait_for(colse_button_object)
        self._spice.wait_until(lambda: close_button['visible'])
        close_button.mouse_click()
        time.sleep(1)

    def change_scan_option_setting(self, payload):
        """
        Change scan option on scan option setting screen
        @param payload: please refer to structure from scan_common_setting_payload from dunetuf.ews.copy_scan_ews_option_dict
        e.g.
        payload = {
            'file_type': 'pdf', # value from key of scan_file_type_option_dict
            'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
            'file_size': 'medium', # value from key of scan_file_size_option_dict
            'original_sides': '1-sided'', # value from key of scan_sides_option_dict
            'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
            'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
            'orientation': 'portrait', # value from key of scan_orientation_option_dict
            'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
            'lighter&darker': 1   # int [1-9]
        }
        """
        logging.info(f"change_scan_option_setting -> <{payload}>")
        self._spice.scan_settings.set_scan_option_settings(payload)

    def perform_folder_quickset_job_from_menu_quicksetapp(self,net, job, ews_quicksets_app, quickset_type, payload, start_option="user presses start", ana_sign_in_payload=None, pin=None, pages=1, time_out=90, pdf_encryption_code=None):

        start_option = payload.get("start_option", None)
        quickset_name = payload["name"]
        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)

        self.goto_scanapp_landing_view_from_menu_scanapp(quickset_type, quickset_name)
        self.select_quickset_from_app_landing_view(quickset_name, quickset_type,ana_sign_in_payload=ana_sign_in_payload)

        self.goto_app_option_screen(quickset_type)

        self.verify_common_current_scan_setting(net, payload,job)
        self.back_to_app_landing_view_from_option_screen(quickset_type)

        ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)

        self._spice.goto_homescreen()
        self._spice.signIn.goto_universal_sign_in("Sign Out")
        self.select_quickset_from_menu_quicksetapp(quickset_name, quickset_type, start_option=start_option, ana_sign_in_payload=ana_sign_in_payload, already_on_landing_view=False)

        if start_option == "user presses start":
            self.start_quickset_job(quickset_type)
        if pdf_encryption_code:
            self._handle_pdf_encryption_code(pdf_encryption_code)
    
    def is_landing_expanded(self, quickset_type):
        """
        Return true if app landing screen is expanded, only preview visible in main panel and detail panel with settings is not shown
        """
        if quickset_type == "email":
            landing = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.email_landing_view)
        elif quickset_type == "sharepoint":
            landing = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.sharepoint_landing_view)
        elif quickset_type == "usb":
            landing = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.usb_landing_view)
        elif quickset_type == "folder":
            landing = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.folder_landing_view)
        elif quickset_type == "copy":
            landing = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.copy_landing_view)

        if landing:
            return landing["isSecondaryCollapsed"]

        return None