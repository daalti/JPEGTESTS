import logging, time
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.send.common.common import Common as ScanCommon

class ScanAppWorkflowUILOperations(ScanAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def goto_scan_app(self):
        """
        Purpose: Navigates to Scan app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Scan app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.home_operations.goto_home_scan_folder()
        logging.info("At Scan App")

    def goto_folder_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Network Folder.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan + " MouseArea")
        self.workflow_common_operations.click_button_on_middle(folder_button)
        logging.info("At scan to folder screen")

    def goto_email_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Email.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        email_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan + " MouseArea")
        self.workflow_common_operations.click_button_on_middle(email_button)
        logging.info("At scan to email screen")
    
    def click_preview_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_panel)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_preview)

        current_button = self.spice.query_item("#itempreview #SpiceView #gridLayoutView #previewButtonLargeScreen")
        self.spice.validate_button(current_button)
        self.workflow_common_operations.click_button_on_middle(current_button)


    def click_preview_button_and_verify_preview(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_panel)
        
        # Wait for Action button to be enabled 
        # To make sure job is ready state
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_send_detail_right_block)
        self.spice.wait_until(lambda: current_button["enabled"] == True)

        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_preview_Expand)
        self.spice.validate_button(current_button)
        current_button.mouse_click()

        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)

    def start_send_from_preview_panel(self, button_object_id = None, scan_more_pages: bool = False, wait_time=2, pin=None, type="usb"):
        '''
        Ui Should be in previewpanel
        Click on send button starts send
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)
        current_button = self.spice.wait_for(button_object_id)
        current_button.mouse_click()
        if pin:
            self.pdf_encryption_enter_password(pin)
            self.pdf_encryption_reenter_password(pin)
            self.pdf_encryption_save()
        time.sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, type):
            self.flatbed_scan_more_pages()
    
    def cancel_send_from_preview_panel(self):
        """
        UI should be at scan progress view.
        Cancel the scan job.
        :return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_cancel).mouse_click()
        
    def goto_sharepoint_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At Scan to SharePoint screen")

    def goto_sharepoint_from_scanapp_at_menu(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        #self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At Scan to SharePoint screen")

    def has_lock_icon(self):
        lock_icon_ids = []
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan_menu_app + " #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_network_folder + " #statusIconRect SpiceLottieImageView")

        for index, lock_icon_id in enumerate(lock_icon_ids):
            try:
                #self.workflow_common_operations.scroll_to_position_vertical(0.1 * (index + 1), ScanAppWorkflowObjectIds.scroll_bar_scan_app_home)
                lock_icon = self.spice.wait_for(lock_icon_id)
            except:
                logging.info("Failed to find lock icon")
                return False
            self.spice.wait_until(lambda: lock_icon["visible"] == True)
        return True

    def verify_setting_string(self, net, setting, setting_value, job=None, screen_id = ScanAppWorkflowObjectIds.menu_list_scan_settings):
        """
        This method compares the selected setting string with the expected string from  string id
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
            setting_value: Value of the setting
            screen_id: screen_id of the string
        """
        cstring_id = ""
        setting_id = ""
        #Get the ui object name of the passed setting
        #Get the cstring id for the value string
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        time.sleep(2)
        if (setting.lower() == "filetype"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_file_type
            cstring_id = ScanAppWorkflowObjectIds.filetype_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_file_type
        elif (setting.lower() == "resolution"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_resolution
            cstring_id = ScanAppWorkflowObjectIds.resolution_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_resolution
        elif (setting.lower() == "filesize"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_filesize
            cstring_id = ScanAppWorkflowObjectIds.filesize_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_filesize
        elif (setting.lower() == "sides"):
            index = 0
            if self.configuration.productname in ["citrine","jasper","moonstone","pearl","bell","curie"]:
                setting_id = ScanAppWorkflowObjectIds.row_object_scan_sides_custom_2info_block
                cstring_id = ScanAppWorkflowObjectIds.sides_custom_dict[setting_value.lower()][0]
                row_object_id = ScanAppWorkflowObjectIds.row_object_scan_sides_custom
            else:
                setting_id = ScanAppWorkflowObjectIds.combobox_scan_sides
                cstring_id = ScanAppWorkflowObjectIds.sides_dict[setting_value.lower()][0]
                row_object_id = ScanAppWorkflowObjectIds.row_object_scan_sides
        elif (setting.lower() == "color"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_auto_color
            cstring_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_auto_color
        elif (setting.lower() == "size"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_original_Size
            cstring_id = ScanAppWorkflowObjectIds.orgsize_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_original_Size
        elif (setting.lower() == "orientation"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_orientation
            cstring_id = ScanAppWorkflowObjectIds.orientation_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_orientation
        elif (setting.lower() == "content_type"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_content_type
            cstring_id = ScanAppWorkflowObjectIds.file_contenttype_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_content_type
        elif (setting.lower() == "original_paper_type"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_original_paper_type
            cstring_id = ScanAppWorkflowObjectIds.file_originalpapertype_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_original_paper_type
        elif (setting.lower() == "blankpagesuppression"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_blank_page_suppression
            cstring_id = ScanAppWorkflowObjectIds.scan_blank_page_suppression_dict[setting_value.lower()][0]
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_blank_page_suppression
        else:
            assert False, "Setting not existing"

        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id, row_object_id, top_item_id="#SpiceHeaderVar2", select_option=False)
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]", 0)["text"]
        logging.info(f"Get current option <{setting}> is {ui_setting_string}")
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"

    def goto_color_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Color-> (Color Settings screen).
        """
        # Color option will be covered when scroll bar slide downward. Click color option will click dropdown box so scroll vertical position to 0 before goto color option.
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.scrollbar_option_screen)
        try:
            self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_color, ScanAppWorkflowObjectIds.combobox_scan_color],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_color_screen)
        except:
            self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_auto_color, ScanAppWorkflowObjectIds.combobox_scan_auto_color],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_auto_color_screen)         
        logging.info("UI: At Color settings screen")

    def goto_blank_settings(self, dial_val: int =180):
        """
        UI should be on Scan options list screen.
        UI Flow is blankPageSuppression-> (blankPageSuppression Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_blank_page_suppression, ScanAppWorkflowObjectIds.combobox_scan_blank_page_suppression],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_blank_page_suppression_screen)
        logging.info("UI: At blankPageSuppression settings screen")

    def click_expand_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_collaps)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.button_scan_landing_collaps)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
    def goto_usb_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to USB.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan +" MouseArea")
        button.mouse_click()
        logging.info("At Scan to USB screen")

    def click_on_main_action_button(self, button_object_id = ScanAppWorkflowObjectIds.button_send_detail_right_block):
        current_button = self.spice.wait_for(button_object_id)
        self.spice.validate_button(current_button)
        current_button.mouse_click()    

    def click_on_preview_button(self):
        preview_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_preview_large, timeout=40.0)
        self.spice.validate_button(preview_button)
        preview_button.mouse_click()    
            
    def goto_filetype_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is File Type-> (File Type Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_file_type, ScanAppWorkflowObjectIds.combobox_scan_file_type],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        constrained = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.row_object_scan_file_type} {ScanAppWorkflowObjectIds.combobox_scan_file_type}")["constrained"]
        if not constrained:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
            logging.info("UI: At File Type settings screen")
            
    def check_original_sides_constraint(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the orientation is constrained or not
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_scan_sides_custom, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=True)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom, timeout=9.0)
        self.workflow_common_operations.goto_item('#RadioButtonOptionssimplex', ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom, select_option=True)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cScanOriginalSides')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()
            
    def check_original_size_constraints(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the original size options are constrained or not
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_original_Size, ScanAppWorkflowObjectIds.combobox_scan_original_Size],
                                                ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen, timeout=9.0)
        logging.info("UI: At Original size settings screen")
        size_id = ScanAppWorkflowObjectIds.orgsize_dict['any'][1]
        self.workflow_common_operations.goto_item(size_id,
                                                ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen,
                                                scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cOriginalSizeSidedID')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()


    def set_scan_settings_original_size_for_idcard(self, size: str, net):
        """
        UI should be on Original size settings screen.
        Args:
            size: The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen)
        size_id = ScanAppWorkflowObjectIds.orgsize_dict[size][1]
        # unable to use scroll_vertical_row_item_into_view due to SpiceListView pagination
        self.workflow_common_operations.goto_item(size_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        self.verify_constrained_message_for_id_card_original_size(net)
        scan_setting_screen =  self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.spice.wait_until(lambda: scan_setting_screen['visible'])
        
        
                   
