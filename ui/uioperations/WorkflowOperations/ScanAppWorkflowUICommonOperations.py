import logging
import time
from dunetuf.ui.uioperations.BaseOperations.IScanAppUIOperations import IScanAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.copy_scan_ui_option_dict import *
from dunetuf.send.common.defaultjoboptions.defaultjoboptionsutils import  JobType
import dunetuf.common.commonActions as CommonActions
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.scan.ScanAction import ScanAction

class ScanAppWorkflowUICommonOperations(IScanAppUIOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))
    
    # The same setting value have a different defined reference key between EWS and spice
    # EWS reference key defined in /work/dune_dev/dune_code_dev/dune/src/test/dunetuf/dunetuf/ews/pom/quick_sets/quicksets_enum.py - Enum
    # Spice reference key defined in /work/dune_dev/dune_code_dev/dune/src/test/dunetuf/dunetuf/ui/uioperations/WorkflowOperations/ScanAppWorkflowObjectIds.py - .._dict
    # Need to set corresponding setting in EWS, then check it from UI, so need map the same setting key from EWS to UI
    filetype_dict_ews_map_ui_key = {
        "pdf": "pdf",
        "tiff": "tiff",
        "jpeg": "jpeg",
        "pdf_a": "pdfa"
    }

    side_dict_ews_map_ui_key = {
        "one_side": "simplex",
        "two_side": "duplex"
    }

    colorformat_dict_ews_map_ui_key = {
        "color":"color",
        "black_only":"blackonly",
        "grayscale":"grayscale",
        "automatic":"autodetect"
    }

    resolution_dict_ews_map_ui_key = {
        "s_75_dpi": "e75dpi",
        "s_100_dpi": "e100dpi",
        "s_150_dpi": "e150dpi",
        "s_200_dpi": "e200dpi",
        "s_240_dpi": "e240dpi",
        "s_300_dpi": "e300dpi",
        "s_400_dpi": "e400dpi",
        "s_600_dpi": "e600dpi"
    }

    filesize_dict_ews_map_ui_key = {
        "lowest": "lowest",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "highest": "highest"
    }

    orientation_dict_ews_map_ui_key = {
        "landscape": "landscape",
        "portrait": "portrait"
    }

    original_size_dict_ews_map_ui_key = {
        "custom": "custom",
        "A2_420x594_mm": "a2",
        "A3_297x420_mm": "a3",
        "A4_210x297_mm": "a4",
        "A5_148x210_mm": "a5",
        "A6_105x148_mm":"a6",
        "Envelope_B5_176x250_mm": "b5_envelope",
        "B6_JIS_128x182_mm": "jis_b6",
        "Envelop_Monarch": "envelope_monarch",
        "Envelope_C5_162x229_mm": "envelope_c5",
        "Envelope_C6_114x162_mm": "iso_c6",
        "Envelope_DL_110x220_mm": "envelope_dl",
        "B5_JIS": "jis_b5",
        "Japanese_Envelope_Chou_3_120x235_mm": "chou_3_envelope",
        "Postcard_JIS": "jpostcard",
        "Double_Postcard_JIS": "jdoublepostcard",
        "Executive_7_25x10_5_in_": "executive",
        "Oficio_8_5x13_in_": "oficio_8_5x13",
        "Letter_8inx10in": "letter_8x10in",
        "s_4x6_in_": "4x6in",
        "s_5x7_in_": "5x7in",
        "s_5x8_in_": "5x8in",
        "Legal_8_5x14_in_": "legal",
        "Letter_8_5x11_in_": "letter",
        "Envelope_10_4_1x9_5_in_": "envelope_10",
        "Oficio_216x340_mm": "oficio_8_5x13_4in",
        "s_16K_184x260_mm": "16k_184x260mm",
        "s_16K_195x270_mm": "16k_195x270mm",
        "s_16K_197x273_mm": "16k",
        "Statement_8_5x5_5_in_": "na_invoice_5.5x8.5in"
    }
    
    watermark_text_options_dict = {
        "none": [ScanAppWorkflowObjectIds.copy_watermark_text_none_str_id],
        "draft": [ScanAppWorkflowObjectIds.copy_watermark_text_draft_str_id],
        "confidential"  : [ScanAppWorkflowObjectIds.copy_watermark_text_confidential_str_id],
        "secret": [ScanAppWorkflowObjectIds.copy_watermark_text_secret_str_id],
        "top_secret": [ScanAppWorkflowObjectIds.copy_watermark_text_top_secret_str_id],
        "urgent": [ScanAppWorkflowObjectIds.copy_watermark_text_urgent_str_id]
    }

    def goto_scan_app(self):
        """ 
        Purpose: Navigates to Scan app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Scan app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.home_operations.goto_home_scan_folder()
        logging.info("At Scan App")

    def get_scan_app(self):
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_scan , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item)
        scan_app = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_app_menu + " MouseArea")
        return scan_app

    def goto_email_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Email.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        email_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan+ " MouseArea")
        email_button.mouse_click()
        logging.info("At scan to email screen")
    
    def goto_folder_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Network Folder.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At scan to folder screen")

    def goto_folder_from_scanapp_at_menu(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Network Folder.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan + " MouseArea")
        folder_button.mouse_click()
        logging.info("At scan to folder screen")
    
    def back_to_menu_app_from_scan_app(self):
        '''
        UI should be in Scan app
        UI flow is Scan App landing view -> Menu app screen
        '''
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_app_landing} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()

    def goto_filetype_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is File Type-> (File Type Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_file_type, ScanAppWorkflowObjectIds.combobox_scan_file_type],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        constrained = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.row_object_scan_file_type}")["constrained"]
        if not constrained:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
            logging.info("UI: At File Type settings screen")

    def goto_pdf_encryption_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is PDF Encryption-> (PDF Encrytion settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_pdf_encryption, ScanAppWorkflowObjectIds.toggle_button_scan_pdf_encryption],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At PDF Encryption settings")

    def goto_long_original_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Long original-> (Long original settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_long_original, ScanAppWorkflowObjectIds.toggle_button_scan_long_original],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Long original settings")

    def goto_edge_to_edge_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Edge-to-Edge-> (Edge-to-Edge settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_edge_to_edge_output, ScanAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Edge-to-Edge settings")

    def goto_background_color_removal_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Scan background Color removal-> (Scan background Color removal settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_background_color_removal, ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan background Color removal settings")

    def goto_auto_release_original_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is to to Scan Auto Release Original
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_auto_release, ScanAppWorkflowObjectIds.toggle_button_scan_auto_release],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan Auto Release Original settings")

    def goto_black_enhancement_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is go to Scan Black Enhancement
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_black_enhancement, ScanAppWorkflowObjectIds.spinbox_black_enhancement],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan Black Enhancement settings")

    def goto_detailed_background_removal_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is got to Detailed Background Removal
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_background_removal_level, ScanAppWorkflowObjectIds.slider_scan_background_removal_level],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Detailed Background Removal settings slider")
    
    def goto_output_size_settings(self):
        """
        UI should be on Scan Output Size settings screen. UI Flow is go to Options
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_output_settings_list)
        logging.info("Go to output size settings screen")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.view_scan_output_settings_list, ScanAppWorkflowObjectIds.row_object_scan_output_size, top_item_id="#SpiceHeaderVar2", select_option=True)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_output_size_menu_list)
        logging.info("UI: At Output Size settings screen")

    def goto_output_size_position_settings(self):
        """
        UI should be on Scan Output Size list screen. UI Flow is go to Positioning
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_output_size_positioning, ScanAppWorkflowObjectIds.combobox_scan_output_size_positioning],
                                                  ScanAppWorkflowObjectIds.view_scan_output_settings_list, scrollbar_objectname = ScanAppWorkflowObjectIds.scroll_bar_output_setting_list)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_positioning)
        logging.info("UI: At Positioning settings screen")
    
    def goto_output_size_orientation_settings(self):
        """
        UI should be on Scan Output Size list screen. UI Flow is go to Orientation
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_output_size_orientation, ScanAppWorkflowObjectIds.combobox_scan_output_size_orientation],
                                                  ScanAppWorkflowObjectIds.view_scan_output_settings_list, scrollbar_objectname = ScanAppWorkflowObjectIds.scroll_bar_output_setting_list)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_orientation)
        logging.info("UI: At Orientation settings screen")

    def goto_background_noise_removal_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Scan background Noise removal-> (Scan background Noise removal settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_background_noise_removal, ScanAppWorkflowObjectIds.toggle_button_scan_background_noise_removal],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan background Noise removal settings")

    def goto_high_compression_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is High Compression-> (High Compression settings).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_high_compression, ScanAppWorkflowObjectIds.toggle_button_scan_high_compression],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At High compression settings")

    def goto_resolution_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Resolution-> (Resolution Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_resolution, ScanAppWorkflowObjectIds.combobox_scan_resolution],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen)
        logging.info("UI: At Resolution settings screen")

    def goto_filesize_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen
        UI Flow is filesize-> (filesize Settings screen).
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_filesize, ScanAppWorkflowObjectIds.combobox_scan_filesize],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_filesize_screen)
        logging.info("UI: At filesize settings screen")

    def check_filesize_constrained(self, filesize: str, filetype: str):
        """
        UI should be on Scan options list screen
        Args:
            filesize: The filesize to check - lowest, low, medium, high, highest
            filetype: The filetype to check - pdf, tiff, jpeg, pdf_a
        if file type is tiff, file size settings should be constrained. 
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_filesize, ScanAppWorkflowObjectIds.combobox_scan_filesize],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        if filetype == "mtiff":
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal, timeout=20.0)
            logging.info("UI: At filesize constraint modal")
            current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
            self.spice.wait_until(lambda: current_button["visible"] == True)
            current_button.mouse_click()
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_filesize_screen, timeout=20.0)
            logging.info("UI: At filesize settings screen")

    def goto_sides_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Sides-> (Sides Settings screen).
        """
        if self.configuration.productname in ["citrine","jasper","moonstone","pearl","bell","curie"]:
            self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_sides_custom,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom)
        else:
            self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_sides, ScanAppWorkflowObjectIds.combobox_scan_sides],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen)
        logging.info("UI: At Sides settings screen")
    
    def goto_2_sided_format_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is 2 sided format-> (2 sided format Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_2_sided_format, ScanAppWorkflowObjectIds.combobox_scan_2_sided_format],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_2_sided_format_screen)
        logging.info("UI: At 2 sided format settings screen")
    
    def goto_scan_mode_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is scan mode-> (scan mode Settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.menu_list_scan_settings,menu_item_id=ScanAppWorkflowObjectIds.row_object_scan_mode_setting,top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen,select_option = True)
        scan_mode_settings_view = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_mode_settings_view)
        self.spice.wait_until(lambda: scan_mode_settings_view["visible"] == True)
        logging.info("At scan mode screen")
        self.workflow_common_operations.scroll_to_position_vertical(0.1, ScanAppWorkflowObjectIds.scan_mode_settings_scrollbar)    
    
    def goto_invert_blueprint_settings(self):
        """
        UI should be on Scan options list screen.UI Flow is go to Scan Invert BluePrint
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_invert_colors, ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan Invert BluePrint settings")

    def goto_reduce_scan_speed_to_enhance_quality_settings(self):
        """
        UI should be on Scan options list screen.UI Flow is go to Reduce Scan Speed to Enhance Quality 
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_reduce_speed, ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option = False)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan Reduce Scan Speed to Enhance Quality settings")

    def is_two_sided_option_available(self):
        '''
        UI should be on Scan options list screen.
        '''
        available = False
        available = self.workflow_common_operations.is_item_available([ScanAppWorkflowObjectIds.row_object_scan_sides, ScanAppWorkflowObjectIds.combobox_scan_sides],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        
        return available

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

    def goto_color_settings_enterprise(self, dial_val: int = 180):#TODO will make this method common for enterprise and other products
        """
        UI should be on Scan options list screen.
        UI Flow is Color-> (Color Settings screen).
        """
        # Color option will be covered when scroll bar slide downward. Click color option will click dropdown box so scroll vertical position to 0 before goto color option.
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.workflow_common_operations.goto_item(["#scan_colorModeWithAutoDetectSettingsComboBox", "#scan_colorModeWithAutoDetectComboBox"],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for("#scan_colorModeWithAutoDetectComboBoxpopupList")
        logging.info("UI: At Color settings screen")

    def goto_original_size_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Original Size-> (Original Size Settings screen).
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_original_Size, ScanAppWorkflowObjectIds.combobox_scan_original_Size],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen)
        logging.info("UI: At Original size settings screen")

    def goto_orientation_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Orientation-> (Orientation Settings screen).
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_orientation, ScanAppWorkflowObjectIds.combobox_scan_orientation],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        time.sleep(2)
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.combobox_scan_orientation)
        current_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_orientation_screen, timeout=19.0)
        logging.info("UI: At Orientation settings screen")
    
    def check_orientation_constraint(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the orientation is constrained or not.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_orientation, ScanAppWorkflowObjectIds.combobox_scan_orientation],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cContentOrientationOption')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()

    def check_resolution_constraint_blocked_settings(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the resolution is constrained or not after preview
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Scan options list screen")
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_resolution, ScanAppWorkflowObjectIds.combobox_scan_resolution],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, ['cMessageNotAllowModifySettings', 'Resolution'])
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()

    def goto_lighter_darker_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Lighter/Darker-> (Lighter/Darker slider).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_lighter_darker, ScanAppWorkflowObjectIds.slider_scan_lighter_darker],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Lighter/Darker settings slider")
    
    def goto_contrast_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Contrast-> (Contrast slider).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_contrast, ScanAppWorkflowObjectIds.slider_scan_contrast],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Contrast settings slider")
    
    def goto_sharpness_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Sharpness-> (Sharpness slider).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_sharpness, ScanAppWorkflowObjectIds.slider_scan_sharpness],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At Sharpness settings slider")
        
    def goto_backgroundcleanup_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is backgroundCleanup-> (backgroundCleanup slider).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_backgroundcleanup, ScanAppWorkflowObjectIds.slider_scan_backgroundcleanup],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("UI: At backgroundCleanup settings slider")

    def goto_content_type_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is contenttype-> (contenttype Settings screen).
        """
        time.sleep(3)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_content_type, ScanAppWorkflowObjectIds.combobox_scan_content_type],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_content_type_screen)
        logging.info("UI: At Orientation settings screen")

    def goto_original_paper_type_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is originalPaperType-> (originalPaperType Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_original_paper_type, ScanAppWorkflowObjectIds.combobox_scan_original_paper_type],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_original_paper_type)
        logging.info("UI: At Original Paper Type settings screen")

    def goto_tiff_compression_color_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is tiff Compression-> (Tiff Compression Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_scan_tiff_compression_color, ScanAppWorkflowObjectIds.combobox_scan_tiff_compression_color],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_color_screen)
        logging.info("UI: At tiff compression setting")

    def goto_tiff_compression_mono_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is tiff Compression-> (Tiff Compression Settings screen).
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_mono_tiff, ScanAppWorkflowObjectIds.scan_monoTiffCompression],ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_mono_screen)
        logging.info("UI: At tiff compression setting")

    def set_scan_settings_tiff_mono_compression(self, compression: str):
        '''
        UI should be on tiff_compression settings screen.
        Args:
            tiff compression Mono: The tiff_compression to set - G3, G4 and Automatic
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_mono_screen)
        # Get the object name in ui for the tiff compression value passed
        compression_id = ScanAppWorkflowObjectIds.tiffcompression_mono_dict[compression.lower()][1]
        self.workflow_common_operations.goto_item(compression_id, ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_color_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_tiff_color_compression(self, compression: str):
        """
        UI should be on tiff_compression settings screen.
        Args:
            tiff compression color: The tiff_compression to set - G3, tiff6 and tiff post
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_color_screen)
        tiffcompression_color_id = ScanAppWorkflowObjectIds.tiffcompression_color_dict[compression.lower()][1]
        self.workflow_common_operations.goto_item(tiffcompression_color_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_color_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        """
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_lighter_darker)
        slider_bar = self.spice.query_item(ScanAppWorkflowObjectIds.slider_scan_lighter_darker)
        slider_bar.__setitem__('value', lighter_darker)

    def set_scan_settings_contrast(self, contrast: int = 1):
        """
        UI should be on Contrast slider in Scan settings screen.
        Args:
            Contrast: The Contrast value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_contrast)
        slider_bar = self.spice.query_item(ScanAppWorkflowObjectIds.slider_scan_contrast)
        slider_bar.__setitem__('value', contrast )
    
    def set_scan_settings_sharpness(self, sharpness: int = 1):
        """
        UI should be on sharpness slider in Scan settings screen.
        Args:
            sharpness: The sharpness value to set - ( Range is 1 to 5)
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_sharpness)
        slider_bar = self.spice.query_item(ScanAppWorkflowObjectIds.slider_scan_sharpness)
        slider_bar.__setitem__('value', sharpness )
    
    def set_scan_settings_backgroundcleanup(self, backgroundCleanup: int = 1):
        """
        UI should be on backgroundCleanup slider in Scan settings screen.
        Args:
            backgroundCleanup: The backgroundCleanup value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_backgroundcleanup)
        slider_bar = self.spice.query_item(ScanAppWorkflowObjectIds.slider_scan_backgroundcleanup)
        slider_bar.__setitem__('value', backgroundCleanup )

    def set_scan_settings_pdf_encryption(self, encryption: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            encryption: PDF encryption toggle - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        encryption_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_pdf_encryption)["checked"]
        if encryption != encryption_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            pdf_encryption_toggle_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.toggle_button_scan_pdf_encryption} MouseArea")
            pdf_encryption_toggle_button.mouse_click()
        pdf_encryption_toggle_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_pdf_encryption)
        self.spice.wait_until(lambda: pdf_encryption_toggle_btn["visible"] == True)
        self.spice.wait_until(lambda: pdf_encryption_toggle_btn["checked"] == True)
        actual_val = pdf_encryption_toggle_btn["checked"]
        logging.info(f"Get value of pdf encryption toggle button: <{actual_val}>")
        assert actual_val == encryption, "pdf encryption toggle button value is unexpected."

    def set_scan_settings_long_original(self, longplot: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            Long original: PDF Long original toggle - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_long_original)
        longplot_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_long_original)["checked"]
        logging.info("Long plot status: %s ",longplot_toggled_state)
        if longplot != longplot_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            longplot_toggle_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.toggle_button_scan_long_original} MouseArea")
            longplot_toggle_button.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.view_long_original_confirmation_screen)
            longplot_ok_button = self.spice.wait_for("#OKButton")
            longplot_ok_button.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        longplot_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_long_original)["checked"]
        assert longplot_toggled_state == longplot ,"Long original setting mismatch"

    def set_scan_settings_edge_to_edge(self, edgeoutput: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            Edge-to-Edge: Edge-to-Edge toggle - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        edgeoutput_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output)["checked"]
        if edgeoutput != edgeoutput_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            edge_toggle_button = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output)
            edge_toggle_button.mouse_click()
        edgeoutput_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output)["checked"]
        assert edgeoutput_toggled_state == edgeoutput, "Edge-to-Edge Output setting mismatch"

    def set_scan_settings_background_color_removal(self, colorremoval: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            Scan background Color removal: Scan background Color removal toggle - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        colorremoval_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal)["checked"]
        if colorremoval != colorremoval_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            colorremoval_toggle_button = self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings + " " + ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal + " MouseArea")
            colorremoval_toggle_button.mouse_click()
            # It is needed because sometimes it is checked very fast
            self.spice.wait_until(lambda: self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal)["checked"] == colorremoval)
        colorremoval_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal)["checked"]
        assert colorremoval_toggled_state == colorremoval, "background Color removal setting mismatch"

    def set_scan_settings_background_noise_removal(self, noiseremoval: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            Scan background Noise removal: Scan background Noise removal toggle - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        noiseremoval_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_background_noise_removal)["checked"]
        if noiseremoval != noiseremoval_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            noiseremoval_toggle_button = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_background_noise_removal)
            noiseremoval_toggle_button.mouse_click()
        noiseremoval_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_background_noise_removal)["checked"]
        assert noiseremoval_toggled_state == noiseremoval, "background Noise removal setting mismatch"

    def set_scan_settings_auto_release_original(self, auto_release: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            auto_release: Scan Auto Release Original toggle - True/False
        """
        logging.info(f"set auto release original status : {auto_release}")
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        auto_release_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_auto_release)["checked"]
        if auto_release != auto_release_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            auto_release_toggle_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.toggle_button_scan_auto_release} MouseArea")
            auto_release_toggle_button.mouse_click()
        auto_release_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_auto_release)["checked"]
        assert auto_release_toggled_state == auto_release, "background Noise removal setting mismatch"

    def set_scan_settings_black_enhancement(self, black_enhancement_value: int):
        """
        UI should be on Black Enhancement in Scan settings screen.
        Args:
            black_enhancement_value: The black enhancement value to set - ( Range is 0 to 255)
        """
        logging.info(f"set black enhancement value: {black_enhancement_value}")
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        black_enhancement_spinbox = self.spice.wait_for(ScanAppWorkflowObjectIds.spinbox_black_enhancement)
        black_enhancement_spinbox.__setitem__('value', black_enhancement_value)   

    def set_scan_settings_detailed_background_removal(self, background_removal_value: int = 1):
        """
        UI should be on Detailed Background Removal slider in Scan settings screen.
        Args:
            background_removal_value: The Detailed Background Removal value to set - ( Range is -6 to 6)
        """
        logging.info(f"set detailed background removal value: {background_removal_value}")
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        slider_bar = self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_background_removal_level)
        slider_bar.__setitem__('value', background_removal_value)
    
    def set_scan_settings_output_size(self, output_size: str, custom_output_size_width=None, custom_output_size_length=None):
        """
        UI should be Output Size settings screen.
        Args
            output_size: The Output Size to set 
            custom_output_size_width: set custom width when output size is custom, int [66-914]
            custom_output_size_length: set custom length when output size is custom, int [66-2377]
        """
        logging.info(f"set output size: output size type is: {output_size}, custom_output_size_width is: {custom_output_size_width}, custom_output_size_length is {custom_output_size_length} ")
        if output_size == "automatic":
            automatic_radio_button = self.spice.wait_for(ScanAppWorkflowObjectIds.radio_button_automatic)
            automatic_radio_button.mouse_click()
        elif output_size == "custom":
            custom_radio_button = self.spice.wait_for(ScanAppWorkflowObjectIds.radio_button_custom)
            custom_radio_button.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.view_output_size_custom)
            if custom_output_size_width != None:
                time.sleep(2)
                width = self.spice.wait_for(ScanAppWorkflowObjectIds.spin_box_output_size_custom_width)
                width.__setitem__('value', custom_output_size_width)
            if custom_output_size_length != None:
                time.sleep(2)
                length = self.spice.wait_for(ScanAppWorkflowObjectIds.spin_box_output_size_custom_length)
                length.__setitem__('value', custom_output_size_length)
            self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_output_size_custom} {ScanAppWorkflowObjectIds.back_button}").mouse_click()

        elif output_size == "roll_1" or output_size == "roll_2":
            loaded_paper_radio_button = self.spice.wait_for(ScanAppWorkflowObjectIds.radio_button_loaded_paper)
            loaded_paper_radio_button.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.view_output_size_loaded_paper)
            output_size_id = ScanAppWorkflowObjectIds.scan_output_size_option_dict[output_size][1]
            self.spice.wait_for(output_size_id).mouse_click()
        else:
            standard_size_radio_button = self.spice.wait_for(ScanAppWorkflowObjectIds.radio_button_standard_size)
            standard_size_radio_button.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.view_output_size_standard_size)
            output_size_id = ScanAppWorkflowObjectIds.scan_output_size_option_dict[output_size][1]
            self.workflow_common_operations.goto_item(output_size_id,
                                                  ScanAppWorkflowObjectIds.view_output_size_standard_size,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scroll_bar_output_size_standard_size)

        logging.info("Back to output size menu list view from output size settings view")
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_output_size_menu_list} {ScanAppWorkflowObjectIds.back_button}")
        back_button.mouse_click()

    def set_scan_settings_save_as_multiple_files(self, option: str):
        """
        UI should be save as multiple files settings screen.
        Args
            option: Option to set - "on" or "off"
        """
        logging.info(f"set option: {option} ")
        if option == "off":
            save_as_multiple_file_off_button = self.spice.wait_for(ScanAppWorkflowObjectIds.save_as_multiple_file_off_button)
            save_as_multiple_file_off_button.mouse_click()
        else:
            save_as_multiple_file_on_button = self.spice.wait_for(ScanAppWorkflowObjectIds.save_as_multiple_file_on_button)
            save_as_multiple_file_on_button.mouse_click()
            
        save_as_multiple_file_done_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_save_as_multiple_files_settings_list} {ScanAppWorkflowObjectIds.save_as_multiple_file_done_button}")
        save_as_multiple_file_done_button.mouse_click()

    def select_book_mode_options(self, bookmode: str):
        """
        UI should be on Book Mode Instructions screen.
        Args
            bookmode : The bookmode to set - scan bothsides ,skip left page ,skip right page
        """
        logging.info(f"bookmode: {bookmode} ")
        if bookmode == "scanBothSides":
            book_mode_scan_both_sides_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_both_sides_for_book_mode)
            book_mode_scan_both_sides_button.mouse_click()
        elif (bookmode == "skipLeftPage" or bookmode == "skipTopPage"):
            book_mode_skip_left_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_skip_left_side_for_book_mode)
            book_mode_skip_left_page_button.mouse_click()
        else:
            book_mode_skip_right_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_skip_right_side_for_book_mode)
            book_mode_skip_right_page_button.mouse_click()

    def set_scan_settings_scancapture_mode(self, scancapturemode: str, checkBox_for_scan_mode_prompt:bool = False):
        """
        UI should be on Scan Capture settings view.
        Args
            scancapturemode : The scancapture mode to set - standard,bookmode,idCard
        """
        logging.info(f"scancapturemode: {scancapturemode} ")
        if scancapturemode == "bookMode":
            button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_capture_mode_option_dict[scancapturemode][1])
            self.spice.wait_until(lambda: button["visible"] == True)
            button.mouse_click()
        elif scancapturemode == "idCard":
            size_id = ScanAppWorkflowObjectIds.scan_capture_mode_option_dict[scancapturemode][1]
            button = self.spice.wait_for(size_id)
            button.mouse_click()
        elif scancapturemode == "standard":
            button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_capture_mode_option_dict[scancapturemode][1])
            self.spice.wait_until(lambda: button["visible"] == True)
            button.mouse_click()
            check_box_additional_pages_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_mode_option_prompt_for_additonal_pages_checkbox)
            if(checkBox_for_scan_mode_prompt != check_box_additional_pages_button["checked"]):
                check_box_additional_pages_button.mouse_click()
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_mode_done_button)
        button.mouse_click()
    
    def set_scancapture_mode_as_idcard_and_disable_prompt(self):
        size_id = ScanAppWorkflowObjectIds.scan_capture_mode_option_dict['idCard'][1]
        button = self.spice.wait_for(size_id)
        button.mouse_click()
        check_box_scan_both_sides_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_mode_option_prompt_for_scan_both_sided)
        if(check_box_scan_both_sides_button["checked"] == True):
            check_box_scan_both_sides_button.mouse_click()
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_mode_done_button)
        button.mouse_click()
           
    def book_mode_instructions_page_scan(self):
        scan_book_mode_instructions_page_scan_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_book_mode_instructions_scan)
        scan_book_mode_instructions_page_scan_button.mouse_click()
        scan_mode_send_button = self.spice.wait_for(ScanAppWorkflowObjectIds.send_button)
        scan_mode_send_button.mouse_click()

    def book_mode_instructions_page_finish(self):
        scan_book_mode_instructions_page_scan_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_book_mode_instructions_finish)
        scan_book_mode_instructions_page_scan_button.mouse_click()

    def book_mode_instructions_page_cancel(self):
        scan_book_mode_instructions_page_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_book_mode_instructions_cancel)
        scan_book_mode_instructions_page_cancel_button.mouse_click()
        scan_book_mode_instructions_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        scan_book_mode_instructions_page_cancel_page_yes_button.mouse_click()

    def set_scan_settings_position(self, position_type: str):
        """
        UI should be Position settings screen.
        Args
            position_type: The position to set 
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_positioning)
        position_type_id = ScanAppWorkflowObjectIds.scan_positioning_option_dict[position_type][1]
        self.workflow_common_operations.goto_item(position_type_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_positioning,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_output_settings_list)
    
    def set_scan_settings_output_size_orientation(self, orientation_type: str):
        """
        UI should be on Orientation type settings screen.
        Args
            orientation_type: The Orientation to set
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_orientation)
        orientation_type_id = ScanAppWorkflowObjectIds.scan_output_canvas_orientation_option_dict[orientation_type][1]
        self.workflow_common_operations.goto_item(orientation_type_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_scan_output_size_orientation,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_output_settings_list)

    def set_scan_settings_high_compression(self, compression: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            compression: The compression toggle value - True/False
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        compression_toggled_state = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_high_compression)["checked"]
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_high_compression,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_option_screen)
        if compression != compression_toggled_state:
            self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
            high_compression_toggle_button = self.spice.wait_for(
                ScanAppWorkflowObjectIds.toggle_button_scan_high_compression)
            self.workflow_common_operations.click_button_on_middle(high_compression_toggle_button)
        compression_toggled_state = self.spice.query_item(ScanAppWorkflowObjectIds.toggle_button_scan_high_compression)["checked"]
        assert compression_toggled_state == compression, "High compression setting mismatch"
    
    def set_blueprint_invert(self, blueprint_invert:bool = True):
        """
        UI should be on Scan settings view.
        Purpose: toggle invert blueprint settings switch
        Args: blueprint_invert: bool True or False
        """
        setting_view = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors)
        self.spice.wait_until(lambda: setting_view["visible"] == True)

        actual_state = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors)["checked"]
        if blueprint_invert != actual_state:
            blueprint_invert_button = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors + " MouseArea")
            blueprint_invert_button.mouse_click()
            time.sleep(3)
        else:
            logging.info(f"Current invert blueprint state is {blueprint_invert}")
        
        actual_state = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors)["checked"]
        assert actual_state == blueprint_invert, "invert blueprint setting mismatch"

    def set_reduce_speed_enhance(self, reduce_speed:bool = True):
        """
        UI should be on Scan settings view.
        Purpose: toggle Reduce Scan Speed to Enhance Quality 
        Args: reduce_speed: bool True or False
        """
        setting_view = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed)
        self.spice.wait_until(lambda: setting_view["visible"] == True)

        actual_state = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed)["checked"]
        if reduce_speed != actual_state:
            reduce_speed_button = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed + " MouseArea")
            reduce_speed_button.mouse_click()
            time.sleep(3)
        else:
            logging.info(f"Current invert blueprint state is {reduce_speed}")
        
        actual_state = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed)["checked"]
        assert actual_state == reduce_speed, "invert blueprint setting mismatch"

    def pdf_encryption_enter_password(self, text:str):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt)
        logging.info("At PDF Encryption prompt view")
        scan_pdf_encryption_keyboard = self.spice.wait_for(ScanAppWorkflowObjectIds.text_box_pdf_encryption_enter_password)
        # Probably we cannot set password with scan_pdf_encryption_reenter_password.__setitem__('displayText', text) directly.
        # We need click input widget firstly, then input password and click OK button.
        self.spice.wait_for(f"{ScanAppWorkflowObjectIds.row_object_scan_password_frame} {ScanAppWorkflowObjectIds.text_box_pdf_encryption_enter_password} {ScanAppWorkflowObjectIds.text_box_password_input}").mouse_click()
        scan_pdf_encryption_keyboard.__setitem__('displayText', text)
        self.spice.wait_for(ScanAppWorkflowObjectIds.keyboard_entry_key_button).mouse_click()
        # scan_pdf_encryption_keyboard.mouse_click()
        # assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_keyboard, timeout = 9.0)
        # self.workflow_keyboard_operations.keyboard_enter_text(text)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt)

    def pdf_encryption_reenter_password(self, text:str):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt)
        logging.info("At PDF Encryption prompt view")
        scan_pdf_encryption_reenter_password = self.spice.wait_for(ScanAppWorkflowObjectIds.text_box_pdf_encryption_reenter_password)
        # we need to check error when password is not match fist time input, so we need click input widget firstly, then input wrong 
        # password and click OK button, then we can get the error info. We cannot get password mismatch error if we set password
        # scan_pdf_encryption_reenter_password.__setitem__('displayText', text) directly.
        self.spice.wait_for(f"{ScanAppWorkflowObjectIds.row_object_scan_reenterpassword_frame} {ScanAppWorkflowObjectIds.text_box_pdf_encryption_reenter_password} {ScanAppWorkflowObjectIds.text_box_password_input}").mouse_click()
        scan_pdf_encryption_reenter_password.__setitem__('displayText', text)
        self.spice.wait_for(ScanAppWorkflowObjectIds.keyboard_entry_key_button).mouse_click()
        # scan_pdf_encryption_reenter_password.mouse_click()
        # assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_keyboard, timeout=9.0)
        # self.workflow_keyboard_operations.keyboard_enter_text(text)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt)

    def pdf_encryption_save(self):
        """
        This method clicks the save button in pdf encryption prompt
        UI Flow is pdf encryption prompt -> save button
        """
        #assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        scan_pdf_encryption_save = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_pdf_encryption_save)
        scan_pdf_encryption_save.mouse_click()

    def pdf_encryption_cancel(self):
        """
        This method clicks the cancel button in pdf encryption prompt
        UI Flow is pdf encryption prompt -> cancel button
        """
        #assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt, timeout = 9.0)
        logging.info("At PDF Encryption prompt view")
        scan_pdf_encryption_cancel = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_pdf_encryption_cancel)
        scan_pdf_encryption_cancel.mouse_click()
    
    def check_spec_enter_pdf_encryption_password_screen(self, net):
        """
        Check spec on enter pdf encryption password screen
        @param net: 
        """
        # verify input field
        scan_pdf_encryption_enter_password = self.spice.wait_for(ScanAppWorkflowObjectIds.text_box_pdf_encryption_enter_password)
        self.spice.wait_until(lambda: scan_pdf_encryption_enter_password["visible"])
        scan_pdf_encryption_reenter_password = self.spice.wait_for(ScanAppWorkflowObjectIds.text_box_pdf_encryption_reenter_password)
        self.spice.wait_until(lambda: scan_pdf_encryption_reenter_password["visible"])

        # verify button
        cancel_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.row_pdf_encription_prompt_footer} {ScanAppWorkflowObjectIds.button_scan_pdf_encryption_cancel}")
        self.spice.validate_button(cancel_button)
        save_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.row_pdf_encription_prompt_footer} {ScanAppWorkflowObjectIds.button_scan_pdf_encryption_save}")
        self.spice.validate_button(save_button)
        
        # verify string
        logging.info("Check spec on enter pdf encryption password screen")
        enter_expect_str_from_id = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cEnterPassword")
        enter_expect_str = enter_expect_str_from_id + "*"
        enter_actual_str = self.spice.common_operations.get_actual_str(ScanAppWorkflowObjectIds.row_object_scan_password_frame)
        assert enter_actual_str == enter_expect_str

        reenter_expect_str_from_id = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cFileTypeReenterPassword")
        reenter_expect_str = reenter_expect_str_from_id + "*"
        reenter_actual_str = self.spice.common_operations.get_actual_str(ScanAppWorkflowObjectIds.row_object_scan_reenterpassword_frame)
        assert reenter_actual_str == reenter_expect_str
    
    def pdf_encryption_password_not_match_ok(self):
        """
        This method clicks the ok button in pdf encryption password not match error
        """
        #assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_pdf_encryption_prompt, timeout = 9.0)
        logging.info("At PDF Encryption enter error password prompt view")
        ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.pdf_encryption_password_not_match_ok)
        ok_button.mouse_click()

    def check_spec_pdf_encryption_password_not_match(self, net):
        """
        Check spec on pdf encryption password not match screen
        @param net: 
        """
        logging.info("Check spec on pdf encryption password not match screen")
        self.spice.common_operations.verify_string(net, "cPasswordNotMatch", ScanAppWorkflowObjectIds.constraint_description)

    def check_spec_insert_usb_storage(self, net):
        """
        Check spec on insert usb storage screen
        @param net: 
        """
        logging.info("Check spec on pdf encryption password not match screen")
        self.spice.common_operations.verify_string(net, "cInsertUSBStorage", ScanAppWorkflowObjectIds.constraint_description)

    def verify_string(self, net, string_oid, expected_id, menu_level: int = 0):
        """
        This method verifies the string on the screen with the expected string from  string id
        Args:
            string_oid: Object Id of string on the screen to be validated
            expected_id: String Id of the of the expected string
            menu_level: Menu level number
        """
        ui_string = self.spice.query_item(string_oid, menu_level)["text"]
        # Get string translation for English "en-US"
        expected_string = LocalizationHelper.get_string_translation(net, expected_id)
        assert ui_string == expected_string, "String mismatch"

    def verify_setting_is_selected(self, net, setting, setting_value, menu_level: int = 0):
        """
        This method compares the selected setting value is checked and at visible
        Args:
            UI should be in specific Setting(e.g.: Resolution) value selection screen
            setting: Setting to be validated
            setting_value: setting value
            menu_level: Menu level number
        """
        setting_id = ""
        #Get the ui object name of the passed setting
        if (setting.lower() == "filetype"):
            setting_id = ScanAppWorkflowObjectIds.filetype_dict[setting_value.lower()][1]
        elif (setting.lower() == "resolution"):
            setting_id = ScanAppWorkflowObjectIds.resolution_dict[setting_value.lower()][1]
        elif (setting.lower() == "filesize"):
            setting_id = ScanAppWorkflowObjectIds.filesize_dict[setting_value.lower()][1]
        elif (setting.lower() == "sides"):
            setting_id = ScanAppWorkflowObjectIds.sides_dict[setting_value.lower()][1]
        elif (setting.lower() == "color"):
            setting_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][1]
        elif (setting.lower() == "size"):
            setting_id = ScanAppWorkflowObjectIds.orgsize_dict[setting_value.lower()][1]
        elif (setting.lower() == "orientation"):
            setting_id = ScanAppWorkflowObjectIds.orientation_dict[setting_value.lower()][1]
        elif (setting.lower() == "blankpagesuppression"):
            setting_id = ScanAppWorkflowObjectIds.scan_blank_page_suppression_dict[setting_value.lower()][1]
        else:
            assert False, "Setting not existing"
        #Check if the passed setting is the selected option
        assert self.spice.wait_for(setting_id)["visible"] == True

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
            index = 1
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
            cstring_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][0]
            if job!=None and job.check_autocolormodeselection_supported(JobType.SCAN_NETWORK_FOLDER) == True:
                setting_id = ScanAppWorkflowObjectIds.combobox_scan_auto_color
                row_object_id = ScanAppWorkflowObjectIds.row_object_scan_auto_color
            else:
                setting_id = ScanAppWorkflowObjectIds.combobox_scan_color
                row_object_id = ScanAppWorkflowObjectIds.row_object_scan_color
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
        
    def verify_setting_string_for_colormode(self, net, configuration, setting, setting_value, screen_id = ScanAppWorkflowObjectIds.menu_list_scan_settings):
        """
        This method compares the colormode setting string with the expected string from  string id
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
        index = 1
        cstring_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][0]
        if configuration.familyname == "enterprise":
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_auto_color
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_auto_color
        else:
            logging.info("Auto color mode is not supported")
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_color
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_color
            
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id, row_object_id, top_item_id="#SpiceHeaderVar2", select_option=False)    
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText", index)["text"]
        logging.info(f"Get current option <{setting}> is {ui_setting_string}")
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"
        
    def verify_output_settings_value(self, net, setting, setting_value):
        """
        This method compares the selected output setting string with the expected string from string id
        UI should be in options screen
        Args:
            setting: Setting to be validated
            setting_value: Value of the setting
        """
        logging.info("Go to output size menu screen from scan options settings screen")
        self.goto_output_size_menu_list()
        time.sleep(2)
        if (setting.lower() == "output_size"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combox_object_scan_output_size
            cstring_id = ScanAppWorkflowObjectIds.scan_output_size_option_dict[setting_value.lower()][0]
        elif (setting.lower() == "position"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_output_size_positioning
            cstring_id = ScanAppWorkflowObjectIds.scan_positioning_option_dict[setting_value.lower()][0]
        elif (setting.lower() == "output_canvas_orientation"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_output_size_orientation
            cstring_id = ScanAppWorkflowObjectIds.scan_output_canvas_orientation_option_dict[setting_value.lower()][0]
        else:
            assert False, "Setting not existing"
        
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]", index)["text"]
        logging.info(f"Get current option <{setting}> is {ui_setting_string}")
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_setting_string == expected_string, "Setting value mismatch"

        logging.info("click back button back to scan options settings screen")
        self.back_to_options_screen_from_output_size_screen()
    
    def goto_output_size_menu_list(self):
        """
        Go to output settings menu screen from scan options settings screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to output size menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_output_size, ScanAppWorkflowObjectIds.combox_object_scan_output_size],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_output_settings_list)

    def back_to_options_screen_from_output_size_screen(self):
        """
        click Back button back to scan options screen from output size screen 
        """
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_output_settings_list} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()

    def goto_save_as_multiple_files_menu_list(self):
        """
        Go to save as multiple files settings menu screen from scan options settings screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to save as multiple files menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_save_as_multiple_pages,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_save_as_multiple_files_settings_list)

    def goto_erase_edges_menu_list(self):
        """
        Go to erase edges settings menu screen from scan options settings screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to save as multiple files menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_edge_erase,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen)
    
    def check_erase_edges_constraints(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the erase edges is constrained or not.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to save as multiple files menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_edge_erase,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cEraseEdgesOption')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()
        
    def back_to_options_screen_from_edge_erase_screen(self):
        """
        click Back button back to scan options screen from edge erase screen 
        """
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()
             
    def verify_edge_erase_settings_and_mirror_front_side_options(self):
        """
        Verify the edge erase settings 
        """
        logging.info("Verify the edge erase settings")
        self.set_unit_of_measurement_settings("millimeters")
        topEdgeValue = 1
        rightEdgeValue = 3
        leftedgeValue = 4
        topEdge = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_top_edge_front} {ScanAppWorkflowObjectIds.spinbox}")
        topEdge.__setitem__('value', topEdgeValue)
        rightEdge = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_right_edge_front} {ScanAppWorkflowObjectIds.spinbox}")
        rightEdge.__setitem__('value', rightEdgeValue)
        leftEdge = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_left_edge_front} {ScanAppWorkflowObjectIds.spinbox}")
        leftEdge.__setitem__('value', leftedgeValue)
        
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.mirror_front_checkbox_view, ScanAppWorkflowObjectIds.mirror_front_side_checkbox], ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen, select_option=False, scrolling_value=0.06, scrollbar_objectname=ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.mirror_front_side_checkbox)         
        mirror_checkbox = self.spice.wait_for(ScanAppWorkflowObjectIds.mirror_front_side_checkbox)
        mirror_checkbox.mouse_click()
        time.sleep(2)
        logging.info("Front side mirror checked")
        
        # when mirror front is enabled, right edge backside should be equal to left edge front
        right_edge_back_box = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_right_edge_back} {ScanAppWorkflowObjectIds.spinbox}")
        right_edge_back_value = right_edge_back_box["displayText"]
        logging.info(f"Get value of right_edge_back_value : <{right_edge_back_value}>")
        assert str(right_edge_back_value) == str(leftedgeValue), "right_edge_back value is unexpected."
        
        # when mirror front is enabled, left edge backside should be equal to right edge front
        left_edge_back_box = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_left_edge_back} {ScanAppWorkflowObjectIds.spinbox}")
        left_edge_back_value = left_edge_back_box["displayText"]
        logging.info(f"Get value of left_edge_back_value : <{left_edge_back_value}>")
        assert str(left_edge_back_value) == str(rightEdgeValue), "left_edge_back value is unexpected."
    
    def set_unit_of_measurement_settings(self, measurement_unit: str):
        """
        UI should be on edge erase settings screen.
        Args:
            measurement_unit: inches, millimeters
        """
        product_name = self.configuration.productname
        logging.info('product name is  %s', product_name)
        if product_name in ["citrine","jasper","moonstone","pearl","bell","curie"]:
            self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_view,ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox], ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_List)
            unit = ScanAppWorkflowObjectIds.scan_edge_erase_measurement_unit_dict[measurement_unit][1]
            self.workflow_common_operations.goto_item(unit, ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_List,
                                                      scrollbar_objectname=ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
        else:
            self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_view, ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_List)
            unit = ScanAppWorkflowObjectIds.scan_edge_erase_measurement_unit_dict[measurement_unit][1]
            self.workflow_common_operations.goto_item(unit, ScanAppWorkflowObjectIds.unit_of_measurement_settings_combobox_List,
                                                    scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        
    def verify_edge_erase_settings_and_all_edges_with_same_width_options(self):
        """
        Verify the edge erase settings 
        """
        time.sleep(5)
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.same_width_to_all_edges_checkbox_view,ScanAppWorkflowObjectIds.same_width_to_all_edges_checkbox],ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
        time.sleep(5)
        logging.info("Click on apply same width to all edges checkbox")
        
        alledge_value = 2 
        allEdge = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.front_all_edges_spin_box} {ScanAppWorkflowObjectIds.spinbox}")
        allEdge.__setitem__('value', alledge_value) 
        time.sleep(3)
        
        # when all edges same width is enabled, all edges backside should be equal to all edges frontside
        all_edge_back_box = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_left_edge_back} {ScanAppWorkflowObjectIds.spinbox}")
        all_edge_back_value = all_edge_back_box["displayText"]
        logging.info(f"Get value of left_edge_back_value : <{all_edge_back_value}>")
        assert str(all_edge_back_value) == str(alledge_value), "all_edge_back value is unexpected."
        time.sleep(1)
        
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.back_all_edges_spin_box,ScanAppWorkflowObjectIds.spinbox], ScanAppWorkflowObjectIds.view_scan_settings_edge_erase_screen, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.edge_erase_scroll_bar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        okButton.mouse_click()
    
    def goto_cropping_menu_list(self):
        """
        Go to cropping settings menu screen from scan options settings screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to save as multiple files menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_cropping,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_cropping_screen)

    def set_cropping_option(self, option):
        """
        Sets the cropping option in the scan settings.

        Args:
            option (str): The cropping option to set. This should be the object ID of the cropping option 
                        (e.g., `ScanAppWorkflowObjectIds.button_scan_settings_cropping_contentCrop`).

        Raises:
            AssertionError: If the cropping settings screen or required UI elements are not found.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_cropping_screen)
        logging.info(f"Set {option}")
        option_button = self.spice.wait_for(option)
        option_button.mouse_click()
        done_button = self.spice.wait_for("#footerDoneButton")
        done_button.mouse_click()

    def verify_edge_erase_constraint_message(self):
        """
        Verify constraint message _ edge erase
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_edge_erase,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        edge_erase_button = self.spice.wait_for(ScanAppWorkflowObjectIds.row_object_scan_edge_erase)
        edge_erase_button.mouse_click()

        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        constraints_ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        constraints_ok_button.mouse_click()

        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_edge_erase_on(self):
        """
        Set Edge erase on
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        edge_erase_button = self.spice.wait_for(ScanAppWorkflowObjectIds.row_object_scan_edge_erase)
        edge_erase_button.mouse_click()        

        topEdgeValue = 1
        topEdge = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spin_box_top_edge_front} {ScanAppWorkflowObjectIds.spinbox}")
        topEdge.__setitem__('value', topEdgeValue)

        self.back_to_options_screen_from_edge_erase_screen()

    def verify_cropping_contentCrop_constraint_message(self):
        """
        Verify constraint message _ Crop to content
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        cropping_option_button = self.spice.wait_for(ScanAppWorkflowObjectIds.row_object_scan_cropping)
        cropping_option_button.mouse_click()

        contentCrop_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_settings_cropping_contentCrop)
        contentCrop_button.mouse_click()

        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        constraints_ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        constraints_ok_button.mouse_click()

        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_cropping_screen)

        done_button = self.spice.wait_for("#footerDoneButton")
        done_button.mouse_click()
        
    def goto_scan_capture_mode_as_book_mode(self):
        """
        Go to scan capture mode as book mode
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.menu_list_scan_settings,menu_item_id=ScanAppWorkflowObjectIds.row_object_scan_mode_setting,top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen,select_option = True)
        scan_mode_settings_view = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_mode_settings_view)
        self.spice.wait_until(lambda: scan_mode_settings_view["visible"] == True)
        logging.info("At scan mode screen")
        self.workflow_common_operations.scroll_to_position_vertical(0.1, ScanAppWorkflowObjectIds.scan_mode_settings_scrollbar)

    def back_to_options_screen_from_save_as_multiple_files_screen(self):
        """
        click Back button back to scan options screen from output size screen 
        """
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_save_as_multiple_files_settings_list} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()

    def verify_setting_lighter_darker_value(self, setting_value):
        """
        UI should be on lighter_darker slider in Scan settings screen.
        """
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_lighter_darker, ScanAppWorkflowObjectIds.slider_scan_lighter_darker],
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        
        slider_bar = self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_lighter_darker)
        lighter_darker = slider_bar["value"]
        logging.info(f"Get value of lighter darker: <{lighter_darker}>")
        if isinstance(setting_value, int):
            setting_value_number = setting_value
        elif isinstance(setting_value, str):
            setting_value_number = int(setting_value.split(' ')[0])
        else:
            raise ValueError("setting_value must be an integer or a string containing a number.")
        assert str(lighter_darker) == str(setting_value_number), "lighter/darker value is unexpected."
    
    def verify_setting_black_enhancement_value(self, setting_value):
        """
        UI should be on black_enhancement input value in Scan settings screen.
        """
        spinbox_black_enhancement = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.spinbox_black_enhancement} {ScanAppWorkflowObjectIds.spinbox}")
        black_enhancement_value = spinbox_black_enhancement["displayText"]
        logging.info(f"Get value of black enhancement : <{black_enhancement_value}>")
        assert str(black_enhancement_value) == str(setting_value), "black enhancement value is unexpected."
    
    def verify_setting_detailed_background_removal_value(self, setting_value):
        """
        UI should be on background_removal_level slider in Scan settings screen.
        """
        slider_bar = self.spice.wait_for(ScanAppWorkflowObjectIds.slider_scan_background_removal_level)
        background_removal_level = slider_bar["value"]
        logging.info(f"Get value of detailed background removal: <{background_removal_level}>")
        assert str(background_removal_level) == str(setting_value), "detailed background removal value is unexpected."

    def verify_settings_pdf_encryption_value(self, setting_value:bool):
        """
        UI should be on pdf encryption toggle button in Scan settings screen.
        """
        pdf_encryption_toggle_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_pdf_encryption)
        actual_val = pdf_encryption_toggle_btn["checked"]
        logging.info(f"Get value of pdf encryption toggle button: <{actual_val}>")
        assert actual_val == setting_value, "pdf encryption toggle button value is unexpected."
    
    def verify_settings_high_compression_value(self, setting_value:bool):
        """
        UI should be on high_compression toggle button in Scan settings screen.
        """
        high_compression_toggle_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.toggle_button_scan_high_compression)
        actual_val = high_compression_toggle_btn["checked"]
        logging.info(f"Get value of high_compression toggle button: <{actual_val}>")
        assert actual_val == setting_value, "high_compression toggle button value is unexpected."
    
    def verify_scan_setting_toggle_option_value(self, setting, setting_value:bool):
        """
        This method compares the toggle status with expected value
        Args:
            UI should be in Settings/Options Landing view
        """
        button_id = ""
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        if (setting.lower() == "long_original"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_long_original
        elif (setting.lower() == "background_color_removal"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_background_color_removal
        elif (setting.lower() == "edge_to_edge_output"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_edge_to_edge_output 
        elif (setting.lower() == "background_noise_removal"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_background_noise_removal
        elif (setting.lower() == "automatic_desknew"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_auto_desknew
        elif (setting.lower() == "auto_release_original"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_auto_release
        elif (setting.lower() == "reduce_scan_speed_to_enhance_quality"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_reduce_speed
        elif (setting.lower() == "invert_blueprint"):
            button_id = ScanAppWorkflowObjectIds.toggle_button_scan_invert_colors
        else:
            assert False, "Setting not existing"
        
        current_toggle_btn = self.spice.wait_for(button_id)
        actual_val = current_toggle_btn["checked"]
        logging.info(f"Get current option <{setting}> toggle button is: <{actual_val}>")
        assert actual_val == setting_value, "Setting value mismatch."
    
    def verify_filename_string(self, filename):
        '''
        This method compares the filename string with the expected string
        UI should be in scan options screen.
        Args: filename: expected filename string
        '''
        ui_filename_string = self.spice.query_item(ScanAppWorkflowObjectIds.text_file_name_field_scan_option)["displayText"]
        logging.info("Filename = " + ui_filename_string)
        assert ui_filename_string.find(filename) != -1, "Filename mismatch"

    def flatbed_scan_more_pages(self, number_of_pages=1):
        """
        This method used to scan the more pages
        :param number_of_pages: number of pages
        :return:
        """
        if number_of_pages > 1:
            while (number_of_pages >= 1):
                scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.add_page_prompt_add_button)
                scan_add_page_button.mouse_click()
                time.sleep(3)
                assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_send_detail_right_block)
                scan_add_page_start_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_send_detail_right_block)
                scan_add_page_start_button.mouse_click()
                time.sleep(3)
                number_of_pages = number_of_pages - 1
            scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
            scan_add_page_done_button.mouse_click()
        elif number_of_pages == 1:
            scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done, timeout = 30.0)
            time.sleep(2)
            scan_add_page_done_button.mouse_click()
    
    def flatbed_scan_more_pages_enterprise(self, cdm, number_of_pages=1):
        """
        This method used to scan the more pages
        :param number_of_pages: number of pages
        :return:
        """
        if number_of_pages > 1:
            while (number_of_pages >= 1):
                assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_add_page_prompt_view)
                add_page_prompt_media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)
                scroll_bar_step_value = 0
                time.sleep(2)
                media_size_id_radio_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.add_page_content_id} " + add_page_prompt_media_sizes_list[0])
                self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True)
                assert media_size_id_radio_button
                media_size_id_radio_button.mouse_click()
                time.sleep(1)
                number_of_pages = number_of_pages - 1
                self.add_page_pop_up_add_more()                
            self.add_page_pop_up_finish()
            
        # elif number_of_pages == 1:
        #     scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done, timeout = 30.0)
        #     time.sleep(2)
        #     scan_add_page_done_button.mouse_click()

    def add_page_pop_up_finish(self):
        time.sleep(2)
        add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.add_prompt_done)
        add_page_done_button.mouse_click()

    def get_add_page_media_sizes_list_from_cdm(self, cdm):
        logging.info("Get the media sizes list from CDM")
        media_sizes_object_names_list = []
        response = cdm.get("/cdm/jobTicket/v1/configuration/defaults/scanEmail/constraints")

        for data in response["validators"]:
            if data["propertyPointer"] == "src/scan/mediaSize":
                media_sizes_options_list_from_cdm = data["options"]
                break

        media_sizes_object_names_list = list(map(lambda media: "#"+media.get("seValue").replace(".","_dot_").replace('-','_dash_'), media_sizes_options_list_from_cdm))

        if len(media_sizes_object_names_list) == 0:
            logging.error("Media sizes list is empty")
        else:
            return media_sizes_object_names_list

    def start_send_job(object_name,scan_more_pages: bool = False, wait_time=2):
        '''
        Common function to perform send job
        '''
        current_button = self.spice.wait_for(object_name, timeout = 20.0)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(wait_time)
        if scan_more_pages == True:    
            time.sleep(2)
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_add_page_prompt_view)
            add_page_prompt_media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)
            scroll_bar_step_value = 0
            media_size_id_radio_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.add_page_content_id} " + add_page_prompt_media_sizes_list[0])
            self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True)
            assert media_size_id_radio_button
            media_size_id_radio_button.mouse_click()

            self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, ScanAppWorkflowObjectIds.add_page_prompt_scroll_bar)
            self.add_page_pop_up_finish()

    def set_scan_option_settings(self, scan_options):
        '''
        Change scan option on scan option setting screen
        UI flow is on option screen.
        e.g.:
        scan_options = {
            'content_type': 'mixed', # value from key of scan_content_type_option_dict
            'file_type': 'pdf', # value from key of scan_file_type_option_dict
            'pdf_encryption': True, # True/False
            "high_compression": False, # True/False
            'resolution': 75_dpi, # value from key of scan_scan_resolution_option_dict
            'file_size': 'medium', # value from key of scan_file_size_option_dict
            'original_sides': '1-sided'', # value from key of scan_sides_option_dict
            'original_sides_auto': 'true', # value from key of scan_sides_auto_option_dict
            'color_mode': 'grayscale', # value from key of scan_color_mode_option_dict
            'original_size': 'letter_8.5x11in', # value from key of scan_original_size_option_dict
            'orientation': 'portrait', # value from key of scan_orientation_option_dict
            'blankPageSuppression': 'true', #value from key of scan_blank_page_suppression_dict
            'tiff_compression': "tiff_6_0", # value from key of scan_tiff_compression_option_dict 
            'lighter&darker': 1 ,  # int [1-9]
            "original_paper_type": None, # value from key of scan_original_paper_type_option_dict
            "long_original": None, #True/False
            "background_color_removal": None, #True/False
            "background_noise_removal": None, #True/False
            "edge_to_edge_output": None, #True/False
            "file_name": None, # string
            "contrast": 1, # int
        }
        '''
        content_type = scan_options.get('content_type', None)
        if content_type != None:
            self.goto_content_type_settings()
            self.set_scan_setting('content_type', scan_content_type_option_dict()[content_type])
        file_type = scan_options.get('file_type', None)
        if file_type != None:
            self.goto_filetype_settings()
            self.set_scan_setting('filetype', scan_file_type_option_dict()[file_type])
        pdf_encryption = scan_options.get('pdf_encryption', None)
        if pdf_encryption != None:
            self.goto_pdf_encryption_settings()
            self.set_scan_settings_pdf_encryption(pdf_encryption)
        high_compression = scan_options.get('high_compression', None)
        if high_compression != None:
            self.goto_high_compression_settings()
            self.set_scan_settings_high_compression(high_compression)
        resolution = scan_options.get('resolution', None)
        if resolution != None:
            self.goto_resolution_settings()
            self.set_scan_setting('resolution', scan_scan_resolution_option_dict()[resolution])
        file_size = scan_options.get('file_size', None)
        if file_size != None:
            self.goto_filesize_settings()
            self.set_scan_setting('filesize', scan_file_size_option_dict()[file_size])
        original_sides = scan_options.get('original_sides', None)
        if original_sides != None:
            # click original sides will click dash board if original sides scroll to top with function goto_item.
            # So scroll with function scroll_vertical_row_item_into_view instead of goto_item.
            if self.configuration.productname in ["citrine","jasper","moonstone","pearl","bell","curie"]:
                self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_scan_sides_custom, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
                self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.row_object_scan_sides_custom}").mouse_click()
                self.set_scan_setting('sides', scan_sides_option_dict()[original_sides])
            else:
                self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_scan_sides, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
                self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.combobox_scan_sides}").mouse_click()
                self.set_scan_setting('sides', scan_sides_option_dict()[original_sides])
        original_sides_auto = scan_options.get('original_sides_auto', None)
        if original_sides_auto != None:
            # click original sides will click dash board if original sides scroll to top with function goto_item.
            # So scroll with function scroll_vertical_row_item_into_view instead of goto_item.
            self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_scan_sides_custom, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.row_object_scan_sides_custom}").mouse_click()
            self.set_scan_setting('sides_auto', scan_sides_auto_option_dict()[original_sides_auto])
        color_mode = scan_options.get('color_mode', None)
        if color_mode != None:
            self.goto_color_settings()
            self.set_scan_setting('color', scan_color_mode_option_dict()[color_mode])
        original_size = scan_options.get('original_size', None)
        if original_size != None:
            self.goto_original_size_settings()
            self.set_scan_setting('size', scan_original_size_option_dict()[original_size])
        orientation = scan_options.get('orientation', None)
        if orientation != None:
            self.goto_orientation_settings()
            self.set_scan_setting('orientation', scan_orientation_option_dict()[orientation])
        blankPageSuppression = scan_options.get('blankPageSuppression', None)
        if blankPageSuppression != None:
            self.goto_blank_settings()
            self.set_scan_setting('blankPageSuppression', scan_blank_page_suppression_dict()[blankPageSuppression])
        lighter_darker = scan_options.get('lighter&darker', None)
        if lighter_darker != None: 
            self.goto_lighter_darker_settings()
            self.set_scan_settings_lighter_darker(lighter_darker = lighter_darker)
        original_paper_type = scan_options.get('original_paper_type', None)
        if original_paper_type != None: 
            self.goto_original_paper_type_settings()
            self.set_scan_setting("originalpaper_type", scan_original_paper_type_option_dict()[original_paper_type])
        long_original = scan_options.get('long_original', None)
        if long_original != None: 
            self.goto_long_original_settings()
            self.set_scan_settings_long_original(long_original)
        edge_to_edge_output = scan_options.get('edge_to_edge_output', None)
        if edge_to_edge_output != None:
            self.goto_edge_to_edge_settings()
            self.set_scan_settings_edge_to_edge(edge_to_edge_output)
        background_color_removal = scan_options.get('background_color_removal', None)
        if background_color_removal != None:
            self.goto_background_color_removal_settings()
            self.set_scan_settings_background_color_removal(background_color_removal)
        background_noise_removal = scan_options.get('background_noise_removal', None)
        if background_noise_removal != None:
            self.goto_background_noise_removal_settings()
            self.set_scan_settings_background_noise_removal(background_noise_removal)
        auto_release_original = scan_options.get('auto_release_original', None)
        if auto_release_original != None:
            self.goto_auto_release_original_settings()
            self.set_scan_settings_auto_release_original(auto_release_original)
        black_enhancement = scan_options.get('black_enhancement', None)
        if black_enhancement != None:
            self.goto_black_enhancement_settings()
            self.set_scan_settings_black_enhancement(black_enhancement)
        detailed_background_removal = scan_options.get('detailed_background_removal', None)
        if detailed_background_removal != None:
            self.goto_detailed_background_removal_settings()
            self.set_scan_settings_detailed_background_removal(detailed_background_removal)
        reduce_scan_speed = scan_options.get('reduce_scan_speed_to_enhance_quality', None)
        if reduce_scan_speed != None:
            self.goto_reduce_scan_speed_to_enhance_quality_settings()
            self.set_reduce_speed_enhance(reduce_scan_speed)
        invert_blueprint = scan_options.get('invert_blueprint', None)
        if invert_blueprint != None:
            self.goto_invert_blueprint_settings()
            self.set_blueprint_invert(invert_blueprint)
        output_size = scan_options.get('output_size', None)
        if output_size != None:
            custom_output_size_width = scan_options.get('custom_output_size_width', None)
            custom_output_size_length = scan_options.get('custom_output_size_length', None)
            self.goto_output_size_menu_list()
            self.goto_output_size_settings()
            self.set_scan_settings_output_size(output_size, custom_output_size_width, custom_output_size_length)
            self.back_to_options_screen_from_output_size_screen()
        position = scan_options.get('position', None)
        if position != None:
            self.goto_output_size_menu_list()
            self.goto_output_size_position_settings()
            self.set_scan_settings_position(position)
            self.back_to_options_screen_from_output_size_screen()
        output_canvas_orientation = scan_options.get('output_canvas_orientation', None)
        if output_canvas_orientation != None:
            self.goto_output_size_menu_list()
            self.goto_output_size_orientation_settings()
            self.set_scan_settings_output_size_orientation(output_canvas_orientation)
            self.back_to_options_screen_from_output_size_screen()
        contrast = scan_options.get('contrast', None)
        if contrast != None:
            self.goto_contrast_settings()
            self.set_scan_settings_contrast(contrast=contrast)
        file_name = scan_options.get('file_name', None)
        if file_name != None:
            self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_filename, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
            file_name_textbox = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.text_file_name_field_scan_option}")
            file_name_textbox.mouse_click()
            file_name_textbox.__setitem__('displayText', file_name)
            keyword_ok = self.spice.wait_for(ScanAppWorkflowObjectIds.keyboard_entry_key_button)
            keyword_ok.mouse_click()

        tiff_compression = scan_options.get('tiff_compression', None)
        if tiff_compression != None:
            if color_mode == 'color':
                self.goto_tiff_compression_color_settings()
                self.set_scan_setting('tiffcompression_color', scan_tiff_compression_option_dict()[tiff_compression])
            elif color_mode == 'black_only' or color_mode == 'grayscale':
                self.goto_tiff_compression_mono_settings()
                self.set_scan_setting('tiffcompression_mono', scan_tiff_compression_option_dict()[tiff_compression])
            else:
                assert False, "Setting not existing"

    def set_scan_setting(self, setting, setting_value, scrolling_value = 0.1):
        """
        UI should be on specific settings screen.
        Args:
            setting: The setting that has to be set - filetype, resolution, filesize, sides, color,
            size, orientation
            setting_value: Value to set for the setting
                The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
                The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                    e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
                The filesize to set - best, draft, standard
                The sides to set - simplex, duplex
                The sides_auto to set - false, true
                The color to set - color, blackonly, grayscale, autodetect
                The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
                The orientation to set - portrait, landscape
                The blankPageSuppression to set - true, false
                The tiff compression color- Tiff6 and Tiff post
                The tiff compression Mono- G3, G4 and Automatic
        """
        setting_id = ""
        items = 2
        if (setting.lower() == "filetype"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen
            setting_id = ScanAppWorkflowObjectIds.filetype_dict[setting_value.lower()][1]
            items = 8
        elif (setting.lower() == "resolution"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen
            setting_id = ScanAppWorkflowObjectIds.resolution_dict[setting_value.lower()][1]
            items = 10
        elif (setting.lower() == "filesize"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_filesize_screen
            setting_id = ScanAppWorkflowObjectIds.filesize_dict[setting_value.lower()][1]
            items = 3
        elif (setting.lower() == "sides"):
            if self.configuration.productname in ["citrine","jasper","moonstone","pearl","bell","curie"]:
                screen = ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom
                setting_id = ScanAppWorkflowObjectIds.sides_custom_dict[setting_value.lower()][1]
                assert self.spice.wait_for(screen)
                logging.info("Go to Original Sides option menu for Enterprise")
                self.workflow_common_operations.goto_item(setting_id, screen, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_original_sides_screen)
                back_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom + " " + ScanAppWorkflowObjectIds.back_button)
                back_button.mouse_click()
                return
            else:
                self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen)
                screen = ScanAppWorkflowObjectIds.view_scan_settings_sides_screen
                setting_id = ScanAppWorkflowObjectIds.sides_dict[setting_value.lower()][1]
            items = 2
        elif (setting.lower() == "sides_auto"):
            original_sides_auto_button = self.spice.wait_for(ScanAppWorkflowObjectIds.row_originalSidesAuto_option)
            assert original_sides_auto_button["checked"] == False
            original_sides_auto_button = self.spice.wait_for(ScanAppWorkflowObjectIds.row_originalSidesAuto_option + " SpiceText")
            original_sides_auto_button.mouse_click()
            time.sleep(3)

            back_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom + " " + ScanAppWorkflowObjectIds.back_button)
            back_button.mouse_click()
            return
        elif (setting.lower() == "color"):
            try:
                self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_color_screen)
                screen = ScanAppWorkflowObjectIds.view_scan_settings_color_screen
            except:
                self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_auto_color_screen)
                screen = ScanAppWorkflowObjectIds.view_scan_settings_auto_color_screen
            setting_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][1]
            items = 4
        elif (setting.lower() == "size"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen
            setting_id = ScanAppWorkflowObjectIds.orgsize_dict[setting_value.lower()][1]
            items = 49
            scrolling_value = 0.04
        elif (setting.lower() == "tiffcompression_color"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_color_screen
            setting_id = ScanAppWorkflowObjectIds.tiffcompression_color_dict[setting_value.lower()][1]
            items = 4
        elif (setting.lower() == "tiffcompression_mono"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_tiff_compression_mono_screen
            setting_id = ScanAppWorkflowObjectIds.tiffcompression_mono_dict[setting_value.lower()][1]
            items = 5
        elif (setting.lower() == "orientation"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_orientation_screen
            setting_id = ScanAppWorkflowObjectIds.orientation_dict[setting_value.lower()][1]
            items = 2
        elif (setting.lower() == "blankpagesuppression"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_blank_page_suppression_screen
            setting_id = ScanAppWorkflowObjectIds.scan_blank_page_suppression_dict[setting_value.lower()][1]
            items = 2
        elif (setting.lower() == "content_type"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_content_type_screen
            setting_id = ScanAppWorkflowObjectIds.file_contenttype_dict[setting_value.lower()][1]
            items = 3
        elif (setting.lower() == "originalpaper_type"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_scan_original_paper_type
            setting_id = ScanAppWorkflowObjectIds.file_originalpapertype_dict[setting_value.lower()][1]
            items = 3

        else:
            assert False, "Setting not existing"

        assert self.spice.wait_for(screen)
        # Black Only ID for Color popup is different in Eddington. 
        if setting_value.lower() == "blackonly":
            try:
                self.spice.wait_for(ScanAppWorkflowObjectIds.black_only_color_format)
                black_only_text = self.spice.query_item(ScanAppWorkflowObjectIds.black_only_color_format + " #contentItem")["text"]
                assert black_only_text == "Black Only"
                setting_id = ScanAppWorkflowObjectIds.black_only_color_format
                logging.info(f"Black Only ID for Color popup is {setting_id}")

            except:
                logging.info(f"Black Only ID for Color popup is still {setting_id}")
        
        # TIFF ID for file type popup is different in Jupiter. 
        if setting_value.lower() == "tiff":
            try:
                self.spice.wait_for(ScanAppWorkflowObjectIds.file_type_tiff)
                file_type_tiff_text = self.spice.query_item(ScanAppWorkflowObjectIds.file_type_tiff + " #contentItem")["text"]
                assert file_type_tiff_text == "TIFF"
                setting_id = ScanAppWorkflowObjectIds.file_type_tiff
                logging.info(f"TIFF ID for file type popup is {setting_id}")

            except:
                logging.info(f"TIFF ID for file type popup is still {setting_id}")

        self.workflow_common_operations.goto_item(setting_id, screen, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_combobox, scrolling_value = scrolling_value)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_filetype(self, filetype: str):
        """
        UI should be on File type settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen)
        filetype_id = ScanAppWorkflowObjectIds.filetype_dict[filetype][1]
        self.workflow_common_operations.goto_item(filetype_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_resolution(self, resolution: str):
        """
          UI should be on Resolution settings screen.
        Args:
            resolution: The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                        e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen)
        time.sleep(3)
        resolution_id = ScanAppWorkflowObjectIds.resolution_dict[resolution][1]
        self.workflow_common_operations.goto_item(resolution_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_filesize(self, filesize: str):
        """
        UI should be on FileSize settings screen.
        Args:
            FileSize: The FileSize to set - lowest,low,medium,high,highest
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_filesize_screen)
        filesize_id = ScanAppWorkflowObjectIds.filesize_dict[filesize][1]
        self.workflow_common_operations.goto_item(filesize_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_filesize_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_sides(self, sides: str):
        """
        UI should be on Sides settings screen.
        Args:
            sides: The sides to set - simplex, duplex
        """
        product_name = self.configuration.productname
        logging.info('product name is  %s', product_name)
        if product_name in ["citrine","jasper","moonstone","pearl","bell","curie"]:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom)
            sides_id = ScanAppWorkflowObjectIds.sides_custom_dict[sides][1]
            self.workflow_common_operations.goto_item(sides_id, ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom,
                                                      scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_original_sides_screen)
            back_button = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen_custom + " " + ScanAppWorkflowObjectIds.back_button)
            back_button.mouse_click()
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen)
            sides_id = ScanAppWorkflowObjectIds.sides_dict[sides][1]
            self.workflow_common_operations.goto_item(sides_id, ScanAppWorkflowObjectIds.view_scan_settings_sides_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        
    def check_original_sides_constraint(self, net):
        """
        UI should be on Scan options list screen.
        UI Flow is to check if the orientation is constrained or not
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.row_object_scan_sides, top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen, select_option=False)
        self.spice.wait_for(f"{ScanAppWorkflowObjectIds.menu_list_scan_settings} {ScanAppWorkflowObjectIds.combobox_scan_sides}").mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_sides_screen, timeout=9.0)
        self.workflow_common_operations.goto_item('#ComboBoxOptionssimplex', ScanAppWorkflowObjectIds.view_scan_settings_sides_screen, select_option=True,
                                                scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cScanOriginalSides')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_sides_combobox_view} {ScanAppWorkflowObjectIds.back_button}")
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
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen, timeout=9.0)
        size_id = ScanAppWorkflowObjectIds.orgsize_dict['letter'][1]
        self.workflow_common_operations.goto_item(size_id,
                                                ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen,
                                                scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        
                   
    def set_scan_2_sided_format_settings(self, style: str):
        """
        UI should be on 2 sided format settings screen.
        Args:
            style: The style to set - flipstyle, bookstyle
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_2_sided_format_screen)
        style_id = ScanAppWorkflowObjectIds.scan_side_format_dict[style][1]
        self.workflow_common_operations.goto_item(style_id, ScanAppWorkflowObjectIds.view_scan_settings_2_sided_format_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
    
    def set_scan_scan_mode_settings(self, mode: str):
        """
        UI should be on scan mode settings screen.
        Args:
            mode: The mode to set - standard, bookmode
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_mode_settings_view)
        mode_id = ScanAppWorkflowObjectIds.scan_capture_mode_option_dict[mode][1]
        
        button = self.spice.query_item(mode_id)
        button.mouse_click()

        logging.info("At scan mode screen")
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_mode_settings_view} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        self.spice.wait_until(lambda: back_button["visible"] == True)
        back_button.mouse_click()

    def select_add_more_pages_combo(self):
        """
        UI should be on scan mode settings screen.
        Select add more pages combo box
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.menu_list_scan_settings,menu_item_id=ScanAppWorkflowObjectIds.row_object_scan_mode_setting,top_item_id=ScanAppWorkflowObjectIds.header_view_in_options_screen,select_option = True)
        scan_mode_settings_view = self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_mode_settings_view)
        self.spice.wait_until(lambda: scan_mode_settings_view["visible"] == True)
        logging.info("At scan mode screen")
        self.workflow_common_operations.scroll_to_position_vertical(1, ScanAppWorkflowObjectIds.scan_mode_settings_scrollbar)
        check_box_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_mode_option_prompt_for_additonal_pages_checkbox)
        check_box_value = self.spice.query_item(ScanAppWorkflowObjectIds.scan_mode_option_prompt_for_additonal_pages_checkbox)["checked"]
        if(check_box_value == False):
            check_box_button.mouse_click()
        
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_mode_settings_view} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()

        #assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings, timeout=9.0)

    def set_scan_settings_color(self, color: str):
        """
         UI should be on Color format settings screen.
        Args:
            color: The color to set - color, blackonly, grayscale, autodetect
        """
        try:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_color_screen)
            scan_setting_screen = ScanAppWorkflowObjectIds.view_scan_settings_color_screen
        except:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_auto_color_screen)
            scan_setting_screen = ScanAppWorkflowObjectIds.view_scan_settings_auto_color_screen

        color_id = ScanAppWorkflowObjectIds.colorformat_dict[color][1]
        self.workflow_common_operations.goto_item(color_id, scan_setting_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_color_enterprise(self, color: str):#TODO will make this method common for enterprise and other products
        """
         UI should be on Color format settings screen.
        Args:
            color: The color to set - color, blackonly, grayscale, autodetect
        """
        assert self.spice.wait_for("#scan_colorModeWithAutoDetectComboBoxpopupList")
        color_id = ScanAppWorkflowObjectIds.colorformat_dict[color][1]
        self.workflow_common_operations.goto_item(color_id, "#scan_colorModeWithAutoDetectComboBoxpopupList",
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_content_type(self, content_type: str):
        """
         UI should be on content type settings screen.
        Args
            content_type: The content type to set - mixed, text, photograph
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_content_type_screen)
        content_type_id = ScanAppWorkflowObjectIds.file_contenttype_dict[content_type][1]
        self.workflow_common_operations.goto_item(content_type_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_content_type_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_original_paper_type(self, originalpaper_type: str):
        """
         UI should be on original paper type settings screen.
        Args
            originalpaper_type: The original paper type to set - white, translucent, blueprint
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_scan_original_paper_type)
        origianlpaper_type_id = ScanAppWorkflowObjectIds.file_originalpapertype_dict[originalpaper_type][1]
        self.workflow_common_operations.goto_item(origianlpaper_type_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_scan_original_paper_type,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def set_scan_settings_original_size(self, size: str):
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
        scan_setting_screen =  self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.spice.wait_until(lambda: scan_setting_screen['visible'])

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
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_original_size_screen)
        back_button = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.view_scan_settings_original_size_layout} {ScanAppWorkflowObjectIds.back_button}")
        self.spice.validate_button(back_button)
        back_button.mouse_click()
        scan_setting_screen =  self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        self.spice.wait_until(lambda: scan_setting_screen['visible'])


    def set_scan_settings_orientation(self, orientation: str):
        """
        UI should be on Orienation settings screen.
        Args:
            orientation: The orientation to set - portrait, landscape
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_settings_orientation_screen)
        orientation_id = ScanAppWorkflowObjectIds.orientation_dict[orientation][1]
        self.workflow_common_operations.goto_item(orientation_id,
                                                  ScanAppWorkflowObjectIds.view_scan_settings_orientation_screen,
                                                  scrollbar_objectname=ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def goto_network_folder_from_scanapp(self):
        """
        Go to network folder from scanapp screen
        """
        # make sure in scanapp
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.scan_network_folder)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_network_folder_landing)

    def select_network_folder_by_property_text(self, text):
        """
        Select network folder by property text
        """
        self._spice.common_operations.goto_item(f"#{text}", "#FolderAppApplicationStackView")

    def send_scan_to_network_folder_job(self):
        """
        Send scan to folder job on network folder screen
        """
        # make sure in scan to network folder screen
        time.sleep(2)
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_network_folder_save)
        self.spice.validate_button(current_button)
        current_button.mouse_click()

    def goto_sharepoint_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        if self.spice.uitype == "Workflow2":
            self.spice.home_operations.home_navigation(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, MenuAppWorkflowObjectIds.home_folder_view)
        else :
            self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan +" SpiceText[visible=true]")
        folder_button.mouse_click()
        logging.info("At Scan to SharePoint screen")

    def goto_sharepoint_from_scanapp_at_menu(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to SharePoint.
        """
        self.goto_sharepoint_from_scanapp_at_home_screen()
        logging.info("At Scan to SharePoint screen")

    def set_scan_setting_interactive_summary(self, setting, setting_value):
        """
        UI should be on specific settings screen.
        Args:
            setting: The setting that has to be set - filetype, resolution, sides, color.
            setting_value: Value to set for the setting
                The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
                The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                    e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
                The sides to set - simplex, duplex
                The color to set - color, blackonly, grayscale, autodetect
        """
        setting_id = ""
        items = 2
        if (setting.lower() == "filetype"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_file_type_screen
            setting_id = ScanAppWorkflowObjectIds.filetype_dict[setting_value.lower()][1]
            items = 8
        elif (setting.lower() == "resolution"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_resolution_screen
            setting_id = ScanAppWorkflowObjectIds.resolution_dict[setting_value.lower()][1]
            items = 10
        elif (setting.lower() == "sides"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_sides_screen
            setting_id = ScanAppWorkflowObjectIds.sides_dict[setting_value.lower()][1]
            items = 2
        elif (setting.lower() == "color"):
            screen = ScanAppWorkflowObjectIds.view_scan_settings_color_screen
            setting_id = ScanAppWorkflowObjectIds.colorformat_dict[setting_value.lower()][1]
            items = 4

        else:
            assert False, "Setting not existing"

        assert self.spice.wait_for(screen)
        # Black Only ID for Color popup is different in Eddington/MarconiHi. 
        if setting_value.lower() == "blackonly":
            try:
                self.spice.wait_for(ScanAppWorkflowObjectIds.black_only_color_format)
                black_only_text = self.spice.query_item(ScanAppWorkflowObjectIds.black_only_color_format + " #contentItem")["text"]
                assert black_only_text == "Black Only"
                setting_id = ScanAppWorkflowObjectIds.black_only_color_format
                logging.info(f"Black Only ID for Color popup is {setting_id}")

            except:
                logging.info(f"Black Only ID for Color popup is still {setting_id}")
        self.workflow_common_operations.goto_item(setting_id, screen, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_combobox)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_interactive_summary_screen_id)
    
    def wait_for_scan_status_toast(self, net, message: str = "complete", time_out=60, specific_str_checked=False, wait_for_toast_dismiss=False, locale: str = "en"):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, starting /scanning /complete
              timeout:
              specific_str_checked: 1. True, strings containing special characters should equal to toast message/False, just need to judge that the string is included in the toast message.
                                    2. Just to check the corresponding status, please using with False/Need to check its screen expected str, please using True
        @return:
        """
        status = False
        job_concurrent_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        
        if job_concurrent_supported == 'true':
            scan_toast_specific_message = ""
            if message == "starting":
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
                scan_toast_specific_message = scan_toast_message_from_id + "..."
            elif message == 'Sending':
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSending')
                scan_toast_specific_message = scan_toast_message_from_id + "..."
            elif message == 'scanning':
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
                scan_toast_specific_message = scan_toast_message_from_id + "..."
            elif message == 'complete':
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessfulMessage')
                scan_toast_specific_message= scan_toast_message_from_id
            elif message == 'successful':
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessful')
                scan_toast_specific_message= scan_toast_message_from_id + "!"
            elif message == 'Scan canceled':
                scan_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanCanceledMessage')
                scan_toast_specific_message= scan_toast_message_from_id + "!"

            for i in range(time_out):
                try:
                    toast_message = self.spice.wait_for(ScanAppWorkflowObjectIds.toast_message_text)["text"]
                except:
                    toast_message = "Does not capture the status"
                time.sleep(1)
                logging.info(f"current scan toast message is: <{toast_message}>")
                if specific_str_checked:
                    logging.info(f"scan_toast_specific_message is <{scan_toast_specific_message}>")
                    if scan_toast_specific_message == toast_message:
                        status = True
                        break
                else:
                    logging.info(f"scan_toast_message_from_id is <{scan_toast_message_from_id}>")
                    if scan_toast_message_from_id in toast_message:
                        status = True
                        break
                
            if wait_for_toast_dismiss:
                start_time = time.time()
                toast_status = ""
                while time.time()-start_time < time_out:
                    try:
                        toast_status = self.spice.wait_for(ScanAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=2)["text"]
                        logging.info(f"Still corresponding status <{toast_status}> dispay in screen")
                    except Exception as err:
                        logging.info("Toast screen already dismiss")
                        break

        #TODO Currently for non concurrent machines, there are only two states: Scanning and Successfully sent, more states need to be added.
        else:
            scan_screen_specific_message = ""
            if message == "scanning":
                scan_screen_message_from_id = str(LocalizationHelper.get_string_translation(net, ["cStringEllipsis", str(LocalizationHelper.get_string_translation(net, "cScanning", locale))], locale))
                scan_screen_specific_message = scan_screen_message_from_id
            elif message == 'successful':
                scan_screen_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSuccessfullySent')
                scan_screen_specific_message = scan_screen_message_from_id
            elif message == 'complete':
                scan_screen_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSuccessfullySent')
                scan_screen_specific_message = scan_screen_message_from_id
            elif message == 'Scan canceled':
                scan_screen_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanCanceledMessage')
                scan_screen_message_from_id = scan_screen_message_from_id.replace("Scan", '"Scan"')
                scan_screen_specific_message = scan_screen_message_from_id
            
            for i in range(time_out):
                try:
                    screen_message = self.spice.wait_for("#ActiveJobModalView #ViewColumn SpiceText", 1)["text"]
                except:
                    screen_message = "Does not capture the status"
                time.sleep(1)
                logging.info(f"current scan screen message is: <{screen_message}>")
                if specific_str_checked:
                    logging.info(f"scan_screen_specific_message is <{scan_screen_specific_message}>")
                    if scan_screen_specific_message == screen_message:
                        status = True
                        break
                else:
                    logging.info(f"scan_screen_message_from_id is <{scan_screen_message_from_id}>")
                    if scan_screen_message_from_id in screen_message:
                        status = True
                        break

        if not status:
            raise Exception(f"Timeout to find scan status <{message}>")
        
    def wait_for_scan_status_toast_is_not_visible(self, timeout = 5):
        """
        Purpose: Wait for the toast to disappear
        Args: timeout: int
        """
        
        toast_status = ""
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                toast_status = self.spice.query_item(ScanAppWorkflowObjectIds.toast_message_text)["text"]
                logging.info("Current Toast message is : %s" % toast_status)
                
                if toast_status == "":
                    logging.info("Toast dissapeared")
                    break
            except:
                logging.info("Still finding corresponding status.")
    
    def wait_for_non_concurrent_scan_complete_screen(self, time_out=20):
        """
        Purpose: Wait for the scan complete wizard screen to appear. This screen only appears on non-concurrent printers.
        Args: time_out: The maximum time to wait for the screen to appear.
        @return: None
        """
        for i in range(time_out):
            try:
                screen_message = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_status_complete_message_non_concurrent)["text"]
            except Exception as e:
                screen_message = "Does not capture the status"
                logging.error(f"Exception occurred: {e}")
            # sleep for 0.5 seconds to avoid too frequent query
            time.sleep(0.1)
            logging.info(f"current scan screen message is: <{screen_message}>")
            if "successful" in screen_message.lower():  # Ensure case-insensitive check
                logging.info("The scan complete wizard screen appears")
                return
        raise Exception("Failed to wait for Scan complete screen within the given timeout")

    def wait_for_non_concurrent_scan_complete_screen_dismiss(self, time_out=15):
        """
        Purpose: Wait for the scan complete wizard screen appears then dismiss, the screen only appears on non-concurrent printer.
        Args: timeout:
        @return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok, time_out)
        logging.info("The scan complete wizard screen appears")
        dismiss_flag = False

        while time_out > 0:
            try:
                self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok, 3)
            except Exception as err:
                logging.info("The scan complete wizard screen dismiss already")
                dismiss_flag = True
                break
            
            time_out = time_out - 2
            time.sleep(2)
        
        assert dismiss_flag, "Scan complete screen does not dismiss"

    def click_ok_button_on_non_concurrent_scan_complete_screen(self):
        """
        Click ok button when scan job compelete successfully for non concurrent product
        """
        okButton = spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok)
        okButton.mouse_click()

    def wait_for_non_concurrent_scan_inprogress_screen(self, time_out=15):
        """
        Purpose: Wait for the scan complete wizard screen appears, the screen only appears on non-concurrent printer.
        Args: timeout:
        @return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_inprogress_wizard_screen, time_out)
        logging.info("The scan in progress wizard screen appears")        
        
    def verify_string_scanapps_at_home_screen(self, object_name):
        """
        UI should be on Scan app screen from home.
        UI Flow is Home -> Scan app.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        if object_name == "scan_to_usb":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan
        elif object_name == "scan_to_network_folder":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan
        elif object_name == "scan_to_email":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_email_from_home_scan
        elif object_name == "scan_to_sharepoint":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan
        elif object_name == "scan_to_computer":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_computer_from_home_scan
        else:
            assert False, "object name not existing"

        if self.spice.uitype == "Workflow2":
            self.spice.home_operations.home_navigation(scan_setting_id, MenuAppWorkflowObjectIds.home_folder_view, select_option=False)
        else:
            self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, scan_setting_id, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)

        assert self.spice.query_item(scan_setting_id)["visible"] == True, "object name is not found"

    def verify_string_not_visibile_scanapps_at_home_screen(self, object_name):
        """
        UI should be on Scan app screen from home.
        UI Flow is Home -> Scan app.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        if object_name == "scan_to_usb":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan
        elif object_name == "scan_to_network_folder":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan
        elif object_name == "scan_to_email":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_email_from_home_scan
        elif object_name == "scan_to_sharepoint":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan
        elif object_name == "scan_to_computer":
            scan_setting_id = ScanAppWorkflowObjectIds.scan_to_computer_from_home_scan
        else:
            assert False, "object name not existing"
            
        try:
            self.spice.query_item(scan_setting_id)["visible"] ==  False
        except Exception as e:
            logging.info("exception msg %s", e)
            if str(e).find("Query selection returned no items") != -1:
                logging.info(f"{object_name} is disabled")

    def back_to_home_from_preview(self):
        '''
        UI should be in Preview screen
        UI flow is scan home -> main ui
        '''
        homeButton = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        homeButton.mouse_click()
        # make sure that you are in the home screen
        logging.info("At Home Screen")

    def preview_cancel(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)
        cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_stop_cancel)
        cancel_button.mouse_click()

    def click_expand_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_expand)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.button_scan_landing_expand)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
    
    def click_collapse_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_collapse_secondarypanel)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.button_collapse_secondarypanel)
        current_button.mouse_click()

    def click_preview_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_panel)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_landing_preview)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.button_scan_landing_preview)
        current_button.mouse_click()

    def goto_preview_and_verify_preview_added(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        self.click_expand_button()
        self.click_preview_button()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)
        time.sleep(4)
        fitpage_layout = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)
    
    def goto_preview_and_verify_preview_added_for_idcard_mode(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        self.click_expand_button()
        self.click_preview_button()
        self.idcard_scan_pop_up_scan()
        time.sleep(1)
        self.idcard_scan_pop_up_done()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)
        time.sleep(4)
        fitpage_layout = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)
    
    def goto_preview_and_verify_preview_added_for_idcard_mode(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        self.click_expand_button()
        self.click_preview_button()
        self.idcard_scan_pop_up_scan()
        time.sleep(1)
        self.idcard_scan_pop_up_done()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout =9.0)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout =9.0)
        time.sleep(4)
        assert self.spice.query_item(ScanAppWorkflowObjectIds.fitpage_layout)["isPreviewImageAvailable"] == True
    
    def refresh_preview_from_preview_panel_refresh_button(self):
        '''
        Ui Should be in previewpanel
        Click on refresh button to refresh the preview
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        refresh_button = self.spice.wait_for(ScanAppWorkflowObjectIds.refresh_preview_button)
        refresh_button.mouse_click()
    
    def verify_preview(self):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image)
        time.sleep(4)
        assert self.spice.query_item(ScanAppWorkflowObjectIds.fitpage_layout)["isPreviewImageAvailable"] == True

    def wait_for_preview_available(self, timeout = 9.0):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout)
        #time.sleep(4)
        fitpage_layout = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)
    
    def refresh_preview_from_warning_icon(self):
        '''
        Ui Should be in previewpanel
        Click on Preview image > Refresh Modal Dialog > Refresh Button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        preview_image_button = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_image)
        preview_image_button.mouse_click()
        time.sleep(2)
        self.spice.wait_for(ScanAppWorkflowObjectIds.refresh_modal_dialog_screen)
        refresh_button = self.spice.wait_for(ScanAppWorkflowObjectIds.refresh_modal_dialog_refresh_button)
        refresh_button.mouse_click()
 
    def start_send_from_preview_panel(self, button_object_id = None, scan_more_pages: bool = False, wait_time=2, pin=None, type="usb"):
        '''
        Ui Should be in previewpanel
        Click on send button starts send
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout=30)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout=30)
        current_button = self.spice.wait_for(button_object_id, timeout=60)
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout = 30)
        self.spice.wait_until(lambda: current_button["enabled"] == True, timeout = 60)
        current_button.mouse_click()
        time.sleep(wait_time)
        if pin:
            self.pdf_encryption_enter_password("123456")
            self.pdf_encryption_reenter_password("123456")
            self.pdf_encryption_save()

        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, type):
            self.scan_operations.flatbed_scan_more_pages()
    
    def verify_prepreview_screen_mdf(self,udw,net):
        udw.mainApp.ScanMedia.unloadMedia("MDF")
        ui_string =self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout +" "+ ScanAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net,'cSelectScanOptions')
        assert ui_string == expected_string, "String mismatch"
        udw.mainApp.ScanMedia.loadMedia("MDF")
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout +" "+ ScanAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net,'cScanAndSend')
        assert ui_string == expected_string, "String mismatch"
    
    def verify_prepreview_enabled_screen_string(self, net):
        current_string_id = self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout +" "+ ScanAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        assert current_string_id != "", "Error: String ID Not found"
        expected_string_id = self.spice.common_operations.get_expected_translation_str_by_str_id(net, ScanAppWorkflowObjectIds.prepreview_enabled_string_id)
        assert expected_string_id != "", "Error: String ID Not not trnaslated"
        assert current_string_id == expected_string_id, f"Error: String mismatch {current_string_id} != {expected_string_id}"
    
    def verify_prepreview_disabled_screen_string(self, net):
        current_string_id = self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout +" "+ ScanAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        assert current_string_id != "", "Error: String ID Not found"
        expected_string_id = self.spice.common_operations.get_expected_translation_str_by_str_id(net,ScanAppWorkflowObjectIds.prepreview_disabled_string_id)
        assert expected_string_id != "", "Error: String ID Not not trnaslated"
        assert current_string_id == expected_string_id, f"Error: String mismatch {current_string_id} != {expected_string_id}"

    def verify_document_feeder_jam_screen(self, net):
        """
        Check alert displayed when document feeder jam occurs.
        """
        logging.info("verify document feeder jam screen displayed")
        self.spice.common_operations.verify_string(net, "cDocumentFeederJam", ScanAppWorkflowObjectIds.alert_details_description)
        alert_ok = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_jam_alert_hide_button)
        alert_ok.mouse_click()

    def verify_constrained_message_for_page_insertion(self,net):
        """
        Check the constrained message for page insertion and close the modal.
        """
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cInsertPageInScanner')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()

    def verify_constrained_message_for_id_card_original_size(self,net):
        """
        Check the constrained message for unsupported mediaSizes when scanmode is IdCard and close the modal.
        """
        ui_string = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)["message"]
        expected_string = self.spice.common_operations.get_expected_translation_str_by_str_id(net, 'cOriginalSizeSidedID')
        assert ui_string == expected_string, "String mismatch"
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        button.mouse_click()

    def verify_scan_settings_editable(self, net, setting, editable: bool = True):
        """
        This method verify scan settings editable filename, filetype
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
                    filename, filetype
            editable: Need to pass bool values True/False
        """
        setting_id = ""
        #Get the ui object name of the passed setting
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        time.sleep(2)
        if (setting.lower() == "filename"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.text_file_name_field_scan_option
            row_object_id = ScanAppWorkflowObjectIds.row_object_filename

        elif (setting.lower() == "filetype"):
            index = 0
            setting_id = ScanAppWorkflowObjectIds.combobox_scan_file_type
            row_object_id = ScanAppWorkflowObjectIds.row_object_scan_file_type

        else:
            assert False, "Editable settings not existing"

        self.workflow_common_operations.goto_item([row_object_id, setting_id], ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True)
        self.verify_input_field_constraint_message_displayed(net, message = 'cReadOnly')
        self.press_input_field_constraint_screen_ok_button()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_filetype_is_constrained(self):
        """
        This method verify file type is constrained
        """
        #Get the ui object name of the passed setting
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)

        setting_id = ScanAppWorkflowObjectIds.combobox_scan_file_type
        row_object_id = ScanAppWorkflowObjectIds.row_object_scan_file_type

        self.workflow_common_operations.goto_item([row_object_id, setting_id], ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True)
        self.press_input_field_constraint_screen_ok_button()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
    
    def verify_scan_settings_save_as_multiple_files(self, setting_value, net):
        cstring_id = ""
        setting_id = ""
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        setting_id = ScanAppWorkflowObjectIds.row_object_scan_save_as_multiple_pages
        cstring_id = ScanAppWorkflowObjectIds.save_as_option_dict[setting_value][0]
        index = 1
        screen_id = ScanAppWorkflowObjectIds.menu_list_scan_settings
        self.workflow_common_operations.goto_item(setting_id, screen_id, select_option=False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]", index)["text"]
        logging.info("UI Setting id is %s", ui_setting_string)
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)

        assert ui_setting_string == expected_string, "Setting value mismatch"
        
    def verify_scan_option_save_as_multiple_files_constrained(self):
        """
        Go to save as multiple files option menu and verify save as multiple files is constrained
        @return:
        """
        logging.info("Go to save as multiple files option")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.row_object_scan_save_as_multiple_pages, ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)

        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        okButton.mouse_click()

    def verify_scan_option_2_sided_format_constrained(self):
        """
        Go to 2 sided format option menu and verify it is constrained
        @return:
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to 2 sided format option")
        self.workflow_common_operations.goto_item([ScanAppWorkflowObjectIds.row_object_scan_2_sided_format,ScanAppWorkflowObjectIds.combobox_scan_2_sided_format], ScanAppWorkflowObjectIds.menu_list_scan_settings, select_option=True, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal, timeout=30.0)

        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        self.spice.validate_button(okButton)
        okButton.mouse_click()
        
    def verify_file_type_cannot_be_changed_notification_message_displayed(self, net):
        '''
        This is to verify that the file type cannot be changed.
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_description)
        message = self.spice.query_item(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        expected_string = LocalizationHelper.get_string_translation(net,'cEmbeddedWebServer')
        assert message == expected_string, "The prompt information is not displayed correctly"

    def click_ok_button_on_file_type_notification_screen(self):
        '''
        Click ok button on sharepoint licationstack.
        UI Should be in sharepoin licationstack.
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_description)
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_file_type_notification_screen_ok)
        current_button.mouse_click()

    def validate_string_id_in_current_view(self, object_name, expected_string, net):
        # Verify the message string id in view
        actual_result = self.spice.wait_for(object_name)["message"]
        expected_result = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, expected_string)
        assert actual_result == expected_result, "String mismatch"
    
    def verify_input_field_constraint_message_displayed(self, net, message, setting = None):
        '''
        This is to verify that the file type cannot be changed.
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_description)
        displayed_message = self.spice.query_item(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        expected_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, message)
        if setting:
            expected_message = expected_message.replace("%1$s", setting)
        assert displayed_message == expected_message, "Constraint message is not shown"

    def validate_scan_send_button(self, net, button_object_id = None, is_visible = True, is_enabled = True, timeout = 5):
        """
        validate scan send button
        :param button_object_id: button object name
        """
        #Get Send button
        sendButton = self.spice.wait_for(button_object_id, timeout)
        self.spice.wait_until(lambda: sendButton["visible"] == is_visible)
        self.spice.wait_until(lambda: sendButton["enabled"] == is_enabled)

    # def validate_scan_send_main_block_button(self, net, sendButtonStringId, is_visible = True, is_enabled = True, timeout = 5):
    #     """
    #     validate scan send button that's in the main block of landing view.
    #     :param sendButtonStringId: "cStart"/"cSend"/"cDoneButton"
    #     """
    #     #Get Send button
    #     sendButton = self.spice.wait_for(ScanAppWorkflowObjectIds.button_startsend_previewpanel, timeout)
    #     self.spice.wait_until(lambda: sendButton["visible"] == is_visible, timeout = timeout)
    #     self.spice.wait_until(lambda: sendButton["enabled"] == is_enabled, timeout = timeout)

    #     actual_button_text = self.spice.query_item(f"{ScanAppWorkflowObjectIds.button_startsend_previewpanel} {ScanAppWorkflowObjectIds.property_text_button}")["text"]
    #     expected_button_text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, sendButtonStringId)
    #     assert actual_button_text == expected_button_text, "Send button text shows not match with expected text" 

    def press_input_field_constraint_screen_ok_button(self):
        """
        This method is to click OK button at the read-only enabled display screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_description)
        logging.info("Click ok button to exit constraint message screen")
        ok_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_constraint_message_ok)
        ok_button.mouse_click()

    def verify_clip_in_scanner_screen(self,timeout=9.0):
        '''
        This method will verify current screen is clipInScanner alert
        Args:
            timeout: max time to wait
        '''
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.clip_in_scanner_screen, timeout)

    def click_ok_on_alert_dialog(self):
        '''
        Click on OK Button on the alert dialog screen
        '''
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.ok_button_alertscreen)
        current_button.mouse_click()
        
    def click_add_more_button_on_add_page(self):
        """"
        UI should be at add page view
        add more page from flatbed
        """
        add_more_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, 30.0)
        self.spice.wait_until(lambda: add_more_button["visible"] == True)
        add_more_button.mouse_click()

    def mdf_add_page_alert_done(self):
        """
        UI should be on MDF release page alert scan and click on finish button 
        to send the scan job.
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_mdfAddPage_alert)
        time.sleep(2)
        finish_button = self.spice.wait_for(ScanAppWorkflowObjectIds.mdf_alert_finish_button)
        finish_button.mouse_click()

    def mdf_add_page_alert_release_page(self):
        """
        UI should be on MDF release page alert scan and click on scan release page to scan more
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_mdfAddPage_alert)
        time.sleep(2)
        finish_button = self.spice.wait_for(ScanAppWorkflowObjectIds.mdf_scan_release_page)
        finish_button.mouse_click()

    def mdf_addpage_window_alert_click_option(self, button_click: str = "send"):
        """
        Check if the MDF add page alert is displayed and click the specified button.

        Args:
            button_click: The button to click if the alert is displayed ("eject" or "send").

        Returns:
            None
        """
        try:
            alert_displayed = self.spice.wait_for(ScanAppWorkflowObjectIds.view_mdfAddPage_alert, timeout=25)
            if alert_displayed:
                if button_click == "send": 
                    self.mdf_add_page_alert_done()
                elif button_click == "eject":
                   self.mdf_add_page_alert_release_page() 
                else:
                    raise ValueError("Invalid button_click value. Must be 'eject' or 'send'.")
        except TimeoutError:
            logging.info("MDF add page alert not displayed. Continuing without action.")

    def cancel_send_from_preview_panel(self):
        """
        UI should be at scan progress view.
        Cancel the scan job.
        :return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.button_preview_cancel).mouse_click()

    def click_on_no_access_button(self):
        '''
        This method is used to click on no access ok button
        '''
        button_no_access_ok = self.spice.wait_for(ScanAppWorkflowObjectIds.button_no_access_ok)
        button_no_access_ok.mouse_click()
    
    def verify_prepreview_screen(self):
        """
        Verify pre-preview screen
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)
    
    def start_send_from_secondary_panel(self, button_object_id = None, scan_more_pages: bool = False, wait_time=2, type="usb"):
        '''
        Ui Should be in secondary panel
        Click on send button starts send
        '''
        current_button = self.spice.wait_for(button_object_id)
        current_button.mouse_click()
        time.sleep(wait_time)
        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, type):
            self.scan_operations.flatbed_scan_more_pages()

    def has_lock_icon(self):
        lock_icon_ids = []
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan_menu_app + " #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_email_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_sharepoint_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_network_folder + " #statusIconRect SpiceLottieImageView")
        lock_icon_ids.append(ScanAppWorkflowObjectIds.scan_to_computer_from_home_scan + "MenuApp #statusIconRect SpiceLottieImageView")

        for index, lock_icon_id in enumerate(lock_icon_ids):
            try:
                #self.workflow_common_operations.scroll_to_position_vertical(0.1 * (index + 1), ScanAppWorkflowObjectIds.scroll_bar_scan_app_home)
                lock_icon = self.spice.wait_for(lock_icon_id)
            except:
                logging.info("Failed to find lock icon")
                return False
            self.spice.wait_until(lambda: lock_icon["visible"] == True)
        return True
    
    def select_sort_order(self, sort):
        '''
        Select sort order
        @param:sort: only two order: AtoZ/ZtoA 
        '''
        sort_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_sort)
        sort_icon_string = sort_button['icon']

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
    
    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, footer_item_id=None, scroll_height=60):
        """
        Scroll contact/group into center of sceen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items.
        UI is in Addressbook contacts list view 
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                footer_item_id: object name for footer view, keep it as None if it does not inculded in scroll view
        """
        logging.info(f"Try to scroll <{row_item_id}> into view of screen <{row_item_id}>")
        current_screen = self.spice.wait_for(screen_id)
        at_y_end = False
        is_visible = False
        while(is_visible is False and at_y_end is False):
            try:
                is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id)
                while (is_visible is False and at_y_end is False):
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, scroll_height)
                    is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id)
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

    def go_and_verify_manually_stop_scanner_screen(self, udw, net, locale, stack_view_original, time_out=10.0):
        """
        UI should be on a scan app (send o print) with a scan job started
        net and local libraries needed
        UI flow stop scan button clicked -> show message of manually stopped -> go to animation of how to release page -> close animation -> press release button -> back to main scan app
        """
        stopButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stop_scan_button)
        stopButton.mouse_click()
        assert(stopButton['text'] == LocalizationHelper.get_string_translation(net, "cStopScan", locale))

        #Check if the modal title is correct
        modalTitle = self.spice.wait_for(ScanAppWorkflowObjectIds.stop_scan_modal_dialog_header)
        assert(modalTitle['text'] == LocalizationHelper.get_string_translation(net, "cPageScanCanceled", locale))

        #Check if the modal buttons are correct
        removeManualAnimationButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stop_scan_modal_dialog_footer_manually_remove_animation_button)
        assert(removeManualAnimationButton['text'] == LocalizationHelper.get_string_translation(net, "cRemove", locale))

        #Tap on Remove button
        removeManualAnimationButton.mouse_click()

        #The close button of the modal, the next animation button and the button that stops and plays the animation
        closeAnimationButton = self.spice.wait_for(stack_view_original + ScanAppWorkflowObjectIds.stop_scan_close_animation_button)

        #The frame to check visibility
        comprobeVisibility = self.spice.wait_for(stack_view_original + ScanAppWorkflowObjectIds.stop_scan_steps_visibility)
        
        #The visibility attribute
        visibilityAttribute = comprobeVisibility["visible"]

        #Check if the frame is visible
        assert(visibilityAttribute)

        #Close all tabs
        closeAnimationButton.mouse_click()

        # Check that release button is visible between dialog stack transition
        releaseButtonOnAlert = self.spice.wait_for(ScanAppWorkflowObjectIds.stop_scan_modal_dialog_footer_release_button, 0)
        self.spice.wait_until(lambda: releaseButtonOnAlert["visible"] == True)
        self.spice.wait_until(lambda: releaseButtonOnAlert["enabled"] == True)
        assert(releaseButtonOnAlert['text'] == LocalizationHelper.get_string_translation(net, "cReleaseButton", locale))        
        releaseButtonOnAlert.mouse_click()

        # Set scan ready to ensure that all returns to the initial state
        scan_action = ScanAction()
        scan_action.set_udw(udw)
        scan_action.set_scan_state(1) # 1 - ScannerState.READY

    def set_scan_settings_blank_page_suppression(self, option: str):
        """
        UI should be save as blank_page_suppression settings screen.
        Args
            option: Option to set - "on" or "off"
        """
        logging.info(f"set option: {option} ")
        if option == "off":
            combo_option_blankPageSuppression_off = self.spice.wait_for(ScanAppWorkflowObjectIds.combo_option_blankPageSuppression_off)
            combo_option_blankPageSuppression_off.mouse_click()
        else:
            combo_option_blankPageSuppression_on = self.spice.wait_for(ScanAppWorkflowObjectIds.combo_option_blankPageSuppression_on)
            combo_option_blankPageSuppression_on.mouse_click()

    def check_eject_button_visible(self, visible: bool, timeout = 10.0):
        '''
        Check eject button is visible or not
        '''
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button)
        self.spice.wait_until(lambda: button["visible"] == visible)
    
    def check_eject_button_enabled(self, enabled: bool, timeout = 10.0):
        '''
        Check eject button is enable or not
        '''
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button)
        self.spice.wait_until(lambda: button["enabled"] == enabled)

    def click_eject_button(self):
        '''
        Click eject button
        '''
        eject_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button)
        eject_btn.mouse_click()

    def click_eject_button_dashboard(self):
        '''
        Click eject button
        '''
        self.spice.statusCenter_dashboard_expand()
        eject_btn = self.spice.wait_for(ScanAppWorkflowObjectIds.eject_button_dashboard_mouse_area)
        self.spice.validate_button(eject_btn)
        eject_btn.mouse_click()
        # Can't check if dashboard button is not visible because it is
        # completely destroyed.

    def check_discard_button_active(self, active: bool, timeout = 10.0):
        '''
        Check discard button is active or not
        '''
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.discard_button)
        self.spice.wait_until(lambda: button["active"] == active)

    def check_number_of_previews(self, num_previews, timeout = 10.0):
        '''
        Check number of previews shown
        In case of num_previews==0, check prePreview component is visible
        '''
        if num_previews == 0:
            prePreview = self.spice.wait_for(ScanAppWorkflowObjectIds.pre_preview_layout)
            self.spice.wait_until(lambda: prePreview["isVisiblePrePreviewTextAndImage"] == True, timeout)
        else:
            preview_handler = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_preview_fitpage_container)
            self.spice.wait_until(lambda: preview_handler["numberOfPages"] == num_previews, timeout)


    def wait_for_preview_n(self, preview_index, timeout=10 ):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_index = preview_index-1 #[0..n]

        thumbnail_objectname = ScanAppWorkflowObjectIds.preview_image_without_index + str(preview_index) # "#image_0" 
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout)
        thubmnail_object = self.spice.wait_for(thumbnail_objectname, timeout )   

        fitpage_layout = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)

    def wait_and_click_preview_n(self, preview_index ):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_index = preview_index-1 #[0..n]

        thumbnail_objectname = ScanAppWorkflowObjectIds.preview_image_without_index + str(preview_index) # "#image_0" 
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        thubmnail_object = self.spice.wait_for(thumbnail_objectname)
        thubmnail_object.mouse_click()     

    def wait_for_preview_window(self):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_window_objectname = ScanAppWorkflowObjectIds.previewWindow
        assert self.spice.wait_for(preview_window_objectname)

    def back_from_preview(self):
        '''
        Ui Should be in previewpanel
        Press back button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_back_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_back_button)
        current_button.mouse_click()
    
    def verify_preview_layout_header(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_header)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_header_moreOptions)

    def verfiy_preview_edit_header(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_header)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_header_moreOptions)    

    def check_edit_button_active(self, active: bool, timeout = 10.0):
        '''
        Check edit button is active or not
        '''
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_button)
        self.spice.wait_until(lambda: button["active"] == active)  

    def click_on_edit_button(self):
        '''
        Ui Should be in previewpanel
        Click on edit button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_button)
        time.sleep(2)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_button)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        time.sleep(1)    

    def click_on_edit_done_button(self):
        '''
        Ui Should be in preview edit panel
        Click on edit done button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_done_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_done_button)
        current_button.mouse_click()
        time.sleep(1)    

    def click_on_brightness_button(self):
        '''
        Ui Should be in preview edit panel
        Click on brightness button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_brightness_button)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_screen)
        time.sleep(1)    

    def click_on_edit_operation_done_button(self):
        '''
        Ui Should be in brightness panel
        Click on brightness done button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_operation_done_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_operation_done_button)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        time.sleep(1)

    def cancel_current_job_modal_alert(self, cancel_job=True):
        '''
        UI should come from scan progress view and be in the modal alert of canceling current job.
        Cancels (or not) the job.
        '''

        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_cancel_job_warning_prompt)
        if cancel_job:
            cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_cancel_job_warning_prompt_primary_button)
            self.spice.validate_button(cancel_button)
            cancel_button.mouse_click()
        else:
            do_not_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_cancel_job_warning_prompt_secondary_button)
            self.spice.wait_until(lambda: do_not_cancel_button["visible"] == True)

    def goto_homescreen_with_ongoing_scan_job(self):
        '''
        UI should be in a Scan app with a scan job in progress.
        Cancels the job and goes to the homescreen.
        '''
        home_button = self.spice.wait_for("#HomeButton")
        home_button.mouse_click()

        self.cancel_current_job_modal_alert(cancel_job=True)

    def clear_job_cancel_warning_prompt(self):
        warning_prompt= self.spice.wait_for(ScanAppWorkflowObjectIds.scan_cancel_job_warning_prompt)
        if warning_prompt:
            yes_Cancel_Button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_cancel_job_warning_prompt_cancel_button)
            yes_Cancel_Button.mouse_click()
    
    def goto_stamp_menu(self, select_option = True):
        """
        Navigate to the Stamp menu in the Scan options view.
        """
        logging.info("Navigated to the Stamp menu.")
        self.homemenu.menu_navigation(self.spice, ScanAppWorkflowObjectIds.menu_list_scan_settings, ScanAppWorkflowObjectIds.list_stamp_menu, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        if select_option == True:
            self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_menu).mouse_click() 
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_view)
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_value)
            
    def verify_stamp_menu_constraint(self):
        """
        Verify the Stamp menu constraint in the Scan options view.
        """
        self.goto_stamp_menu(select_option = False)
        self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_menu).mouse_click() 
        
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        okButton.mouse_click()
    
    def back_from_stamp_location_view(self):
        """
        Back to the Stamp menu in the Stamp settings view.
        """
        logging.info("Back to the Stamp menu.")
        backButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_location_view_back_button)
        backButton.mouse_click()
            
    def verify_stamp_menu_value(self, net, location, setting_values):
        """
        Verify the Stamp menu value in the Scan options view.
        """
        if location != "main":
            self.goto_stamp_settings_view(location, select_option = False)
        if location == "main":
            self.goto_stamp_menu(select_option = False)
        
        customString = False
        expected_strings = []

        setting_id = ScanAppWorkflowObjectIds.stamp_location_dict[location][1]
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        
        for setting_value in setting_values:
            if setting_value in ScanAppWorkflowObjectIds.stamp_content_format_string_dict:
                cstring_id = ScanAppWorkflowObjectIds.stamp_content_format_string_dict[setting_value][0]
            else:
                customString = True
            
            if customString == True:
                expected_string = setting_value
            else:   
                expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
            expected_strings.append(expected_string)
            
        if len(expected_strings) > 1:
            result_string = ", ".join(expected_strings)
        else:
            result_string = expected_strings[0]
            
        assert ui_setting_string == result_string, "Setting value mismatch"
            
    def goto_stamp_settings_view(self, location, select_option = True):
        """
        Navigate to the Stamp settings view in the Stamp list view.
        """
        logging.info("Navigated to the Stamp view.")

        if location not in ScanAppWorkflowObjectIds.stamp_location_dict:
            raise ValueError(f"Invalid location: {location}")

        menu_item_id, value_id = ScanAppWorkflowObjectIds.stamp_location_dict[location]

        self.homemenu.menu_navigation(self.spice, ScanAppWorkflowObjectIds.list_stamp_view, menu_item_id, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_view_scroll_bar)
        
        if select_option == True:
            self.spice.wait_for(menu_item_id).mouse_click()
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view)
        else:
            assert self.spice.wait_for(value_id)
            
    def back_from_stamp_setting_view(self):
        """
        Back to the Stamp menu in the Stamp settings view.
        """
        logging.info("Back to the Stamp menu.")
        doneButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_settings_done_button)
        doneButton.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_view)
        
    def goto_stamp_content_view(self):
        """
        Navigate to the Stamp content view in the Stamp options view.
        """
        logging.info("Navigated to the Stamp content view.")
        self.workflow_common_operations.goto_item(f"{ScanAppWorkflowObjectIds.stamp_settings_content_button}", ScanAppWorkflowObjectIds.list_stamp_settings_view, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_settings_view_scroll_bar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_content_view)
        
    def back_from_stamp_contents_view(self):
        """
        Back to the Stamp settings view in the Stamp options view.
        """
        logging.info("Back to the Stamp settings view.")
        doneButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_content_done_button)
        doneButton.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view)
        
    def select_stamp_content_option(self, option, checked):
        """
        This function selects options one by one in the Stamp Content view.
        """
        for i in option:
            row_id, checkBox_id = ScanAppWorkflowObjectIds.stamp_content_checkbox_dict[i]
            self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_content_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
            checkBoxElement = self.spice.wait_for(checkBox_id + " MouseArea")
            checkBoxProperties = self.spice.wait_for(checkBox_id)
             
            if checked is True:
                if checkBoxProperties["checked"] is False:
                    checkBoxElement.mouse_click()

            else:
                if checkBoxProperties["checked"] is True:
                    checkBoxElement.mouse_click()           
    
    def verify_stamp_content_checked(self, option, checked=True, customText=None):
        """
        This function is used to verify whether the Stamp content options are checked in the Stamp Content view.
        """
        for i in option:
            row_id, checkBox_id = ScanAppWorkflowObjectIds.stamp_content_checkbox_dict[i]
            self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_content_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
            checkBoxElement = self.spice.wait_for(checkBox_id)
            assert checkBoxElement['checked'] == checked, f"{i} is not checked"
            
            if i == "userDefined1" or "userDefined2" or "adminDefined1" or "adminDefined2" or "adminDefined3":
                if customText != None:
                    assert self.spice.query_item(checkBox_id + " SpiceText[visible=true]")["text"] == customText, "Custom Text is not matched"
            
    def verify_stamp_content_exist(self, option, visible=False):
        """
        This function is used to check whether the Option is visible when adminDefined is defined or some Stamp content is disabled by EWS Optional Stamp.
        """
        for i in option:
            row_id = ScanAppWorkflowObjectIds.stamp_content_checkbox_dict[i][0]
            if visible == False:
                try:
                    self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_content_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
                    assert self.spice.wait_for(row_id, timeout=5.0) == False, f"{i} is visible in the Stamp content view. but it should not be."
                except:
                    logging.info(f"{i} is not visible in the Stamp content view.")
                    continue
            else:      
                self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_content_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
                stamp_content = self.spice.wait_for(row_id)
                self.spice.wait_until(lambda: stamp_content["visible"] == visible, timeout=10.0)
    
    def verify_stamp_content_constraint(self, net, option):
        message_dict = {
            "date": "cDateUnavailable",
            "dateAndTime": "cDateTimeUnavailable"
        }
        row_id, checkBox_id = ScanAppWorkflowObjectIds.stamp_content_checkbox_dict[option]
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_content_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        checkBoxElement = self.spice.wait_for(checkBox_id + " MouseArea")
        checkBoxElement.mouse_click()
        
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        self.validate_string_id_in_current_view(ScanAppWorkflowObjectIds.constraint_modal, message_dict.get(option), net)
        
        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        okButton.mouse_click()
        
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_content_view)
    
    def goto_stamp_edit_order_view(self):
        """
        Navigate to the Stamp edit order view in the Stamp Content view.
        """
        logging.info("Navigated to the Stamp edit order view.")
        editOrderButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_content_edit_button)
        editOrderButton.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_edit_order_view)
        
    def back_from_stamp_order_view(self):
        """
        Back to the Stamp content view in the Stamp Order view.
        """
        logging.info("Back to the Stamp content view.")
        doneButton = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_edit_order_done_button)
        doneButton.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_content_view)
        
    def edit_stamp_content_order(self, option, direction, num_of_moves=1):
        """
        This function is used to edit the Stamp content order in the Stamp edit order view.
        """  
        direction_dict = {
            "up": ScanAppWorkflowObjectIds.stamp_edit_order_up_button,
            "down": ScanAppWorkflowObjectIds.stamp_edit_order_done_button
        }
        
        row_id, radio_id = ScanAppWorkflowObjectIds.stamp_content_radio_dict[option]
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_edit_order_view, row_id, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        radioElement = self.spice.wait_for(radio_id + " MouseArea")
        radioElement.mouse_click()
        
        direction_button = self.spice.wait_for(direction_dict.get(direction))
        
        for i in range(0, num_of_moves):
            direction_button.mouse_click()
        
    def goto_stamp_content_text_field(self):
        """
        Navigate to the Stamp content text field in the Stamp options view.
        """
        logging.info("Navigated to the Stamp content text field.")
        self.workflow_common_operations.goto_item(f"{ScanAppWorkflowObjectIds.stamp_settings_content_button}", ScanAppWorkflowObjectIds.list_stamp_settings_view, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_settings_view_scroll_bar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_settings_text_feild)
        
    def add_user_defined_stamp_content(self, custom_texts):
        '''
        This is helper method to enter new userDefined stamp content.
        UI flow is common keyboard -> enter new userDefined content
        '''
        self.goto_stamp_content_text_field()
        for custom_text in custom_texts:
            stamp_content_textbox = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.list_stamp_settings_view} {ScanAppWorkflowObjectIds.stamp_settings_text_feild}")
            stamp_content_textbox.mouse_click()
            stamp_content_textbox.__setitem__('text', custom_text)
            
            keyword_ok = self.spice.wait_for(ScanAppWorkflowObjectIds.keyboard_entry_key_button)
            keyword_ok.mouse_click()
        
    def delete_stamp_content_on_text_field(self, index):
        """
        Delete the Stamp content text field in the Stamp content text field.
        """
        self.goto_stamp_content_text_field()
        stamp_content_button = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_settings_bubbule + str(index) + " #bubbleMouseArea")
        stamp_content_button.mouse_click()
        
        stamp_content_delete_button = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_settings_bubbule + str(index) + " #clearButton")
        stamp_content_delete_button.mouse_click()
        
    def verify_stamp_content_text_on_text_field(self, net, index, bubbleText):
        """
        Verify the Stamp content text field in the Stamp content text field.
        """
        self.goto_stamp_content_text_field()
        
        customString = False
        stamp_content_button_text = self.spice.query_item(ScanAppWorkflowObjectIds.stamp_settings_bubbule + str(index) + " #EmailText")["text"]
        
        if bubbleText in ScanAppWorkflowObjectIds.stamp_content_format_string_dict:
            cstring_id = ScanAppWorkflowObjectIds.stamp_content_format_string_dict[bubbleText][0]
        else:
            customString = True
            
        if customString == True:
            expected_string = bubbleText
        else:   
            expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
         
        assert stamp_content_button_text == expected_string, f"Expected bubble text '{expected_string}', but got '{stamp_content_button_text}'"
        
    def verify_stamp_user_defined_constraint_message(self, net):
        """
        Verify the Stamp user defined constraint message in the Stamp options view.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal)
        self.validate_string_id_in_current_view(ScanAppWorkflowObjectIds.constraint_modal, 'cUserCustomStampsLimited', net)
        
        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_modal_Ok_button)
        okButton.mouse_click()
        
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_settings_text_feild)
        
    def goto_stamp_starting_page_spinBox(self):
        """
        Navigate to the Stamp starting page spinBox in the Stamp options view.
        """
        logging.info("Navigated to the Stamp starting page spinBox.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_starting_page_spinBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_page_spinBox)
    
    def change_stamp_starting_page(self, value=1):
        """
        Change the Stamp starting page value in the Stamp options view.
        """
        self.goto_stamp_starting_page_spinBox()
        startingPageElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_page_spinBox)
        startingPageElement.__setitem__('value', value)
        
    def verify_stamp_starting_page(self, expect_value=1):
        """
        Verify the Stamp starting page value in the Stamp options view.
        """
        self.goto_stamp_starting_page_spinBox()
        startingPageElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_page_spinBox)
        actual_value = startingPageElement.__getitem__('value')
        assert actual_value == expect_value, f"Expected {expect_value}, but got {actual_value}"
        
    def verify_stamp_starting_page_option_visible(self, visible=True):
        """
        Verify the visibility of the Stamp starting page option in the Stamp options view.
        """
        if visible == True:
            self.goto_stamp_starting_page_spinBox()
            startingPageElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_page_spinBox)
            assert startingPageElement['visible'] == True, f"Stamp starting page option visibility mismatch: expected {visible}, got {startingPageElement['visible']}"
        else:
            try:
                self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_starting_page_spinBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
                startingPageElement = self.spice.wait_for(ScanAppWorkflowObjectIds.row_stamp_starting_page_spinBox, timeout=5.0)
                assert startingPageElement['visible'] == False, f"Stamp starting page option visibility mismatch: expected {visible}, got {startingPageElement['visible']}"
            except:
                logging.info(f"Stamp starting page option is not visible as expected")
    
    def goto_stamp_starting_number_spinBox(self):
        """
        Navigate to the Stamp starting number spinBox in the Stamp options view.
        """
        logging.info("Navigated to the Stamp starting number spinBox.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_starting_number_spinBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_number_spinBox)
        
    def change_stamp_starting_number(self, value=1):
        """
        Changed the Stamp starting number value in the Stamp options view.
        """
        self.goto_stamp_starting_number_spinBox()
        startingNumberElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_number_spinBox)
        startingNumberElement.__setitem__('value', value)
        
    def verify_stamp_starting_number(self, expect_value=1):
        """
        Verify the Stamp starting number value in the Stamp options view.
        """
        self.goto_stamp_starting_number_spinBox()
        startingNumberElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_number_spinBox)
        actual_value = startingNumberElement.__getitem__('value')
        assert actual_value == expect_value, f"Expected {expect_value}, but got {actual_value}"
        
    def verify_stamp_starting_number_option_visible(self, visible=True):
        """
        Verify the visibility of the Stamp starting number option in the Stamp options view.
        """
        if visible == True:
            self.goto_stamp_starting_number_spinBox()
            startingNumberElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_starting_number_spinBox)
            assert startingNumberElement['visible'] == True, f"Stamp starting number option visibility mismatch: expected {visible}, got {startingNumberElement['visible']}"
        else:
            try:
                self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_starting_number_spinBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
                startingNumberElement = self.spice.wait_for(ScanAppWorkflowObjectIds.row_stamp_starting_number_spinBox, timeout=5.0)
                assert startingNumberElement['visible'] == False, f"Stamp starting number option visibility mismatch: expected {visible}, got {startingNumberElement['visible']}"
            except:
                logging.info(f"Stamp starting number option is not visible as expected")
        
    def goto_stamp_number_of_digit_spinBox(self):
        """
        Navigate to the Stamp number of digit spinBox in the Stamp options view.
        """
        logging.info("Navigated to the Stamp number of digit spinBox.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_number_of_digit_spinBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_number_of_digit_spinBox)
        
    def change_stamp_number_of_digit(self, value=1):
        """
        Change the Stamp number of digit value in the Stamp options view.
        """
        self.goto_stamp_number_of_digit_spinBox()
        numberOfDigitElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_number_of_digit_spinBox)
        numberOfDigitElement.__setitem__('value', value)
        
    def verify_stamp_number_of_digit(self, expect_value=1):
        """
        Verify the Stamp number of digit value in the Stamp options view.
        """
        self.goto_stamp_number_of_digit_spinBox()
        numberOfDigitElement = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_number_of_digit_spinBox)
        actual_value = numberOfDigitElement.__getitem__('value')
        assert actual_value == expect_value, f"Expected {expect_value}, but got {actual_value}"
        
    def goto_stamp_page_numbering_option(self, select_option = True):
        """
        Navigate to the Stamp page numbering option in the Stamp options view.
        """
        logging.info("Navigated to the Stamp page numbering option.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_page_numbering_comboBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        
        if select_option == True:
            self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_page_numbering_comboBox).mouse_click()    
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_stamp_comboBox, timeout = 9.0)
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_page_numbering_comboBox)
        
    def select_stamp_page_numbering_option(self, option):
        """
        Select the appropriate option from the Stamp page numbering Combobox.
        """
        self.goto_stamp_page_numbering_option()
        
        page_numbering_dict = {
            "number": f"{ScanAppWorkflowObjectIds.combo_stamp_number}",
            "pagePlusNumber": f"{ScanAppWorkflowObjectIds.combo_stamp_page_plus_number}",
            "hyphenNumber": f"{ScanAppWorkflowObjectIds.combo_stamp_hyphen_number}"
        }
        
        to_select_item = page_numbering_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, ScanAppWorkflowObjectIds.view_stamp_comboBox, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_comboBox_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view, timeout = 9.0)
        
    def verify_stamp_page_numbering_option(self, net, setting_value):
        """
        Verify the Stamp page numbering option in the Stamp options view.
        """
        self.goto_stamp_page_numbering_option(select_option = False)

        setting_id = ScanAppWorkflowObjectIds.stamp_page_numbering_comboBox
        cstring_id = ScanAppWorkflowObjectIds.stamp_page_numbering_format_string_dict[setting_value.lower()][0]
            
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id) 
        assert ui_setting_string == expected_string, "Setting value mismatch"
    
    def goto_stamp_text_color_option(self, select_option = True):
        """
        Navigate to the Stamp text color option in the Stamp options view.
        """
        logging.info("Navigated to the Stamp text color option.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_text_color, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        
        if select_option == True:
            self.spice.wait_for(ScanAppWorkflowObjectIds.row_stamp_text_color).mouse_click() 
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_text_color)
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.row_stamp_text_color_value)
        
    def select_stamp_text_color_option(self, option):
        """
        Select the appropriate option from the Stamp text color list.
        """
        self.goto_stamp_text_color_option()
        
        stamp_text_color_dict = {
            "black": ScanAppWorkflowObjectIds.row_text_color_black,
            "yellow": ScanAppWorkflowObjectIds.row_text_color_yellow,
            "green": ScanAppWorkflowObjectIds.row_text_color_green,
            "red": ScanAppWorkflowObjectIds.row_text_color_red,
            "blue": ScanAppWorkflowObjectIds.row_text_color_blue,
            "skyBlue": ScanAppWorkflowObjectIds.row_text_color_skyBlue,
            "purple": ScanAppWorkflowObjectIds.row_text_color_purple
        }

        to_select_item = stamp_text_color_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_view_text_color, to_select_item, top_item_id='#SpiceHeaderVar2', scroll_step=1)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view, timeout = 9.0)
        
    def verify_stamp_text_color_option(self, net, setting_value):
        """
        Verify the Stamp text color option in the Stamp options view.
        """
        self.goto_stamp_text_color_option(select_option = False)

        setting_id = ScanAppWorkflowObjectIds.row_stamp_text_color_value
        cstring_id = ScanAppWorkflowObjectIds.stamp_text_color_format_string_dict[setting_value.lower()][0]
            
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id) 
        assert ui_setting_string == expected_string, "Setting value mismatch"
        
    def goto_stamp_text_font_option(self, select_option = True):
        """
        Navigate to the Stamp page numbering option in the Stamp options view.
        """
        logging.info("Navigated to the Stamp page numbering option.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_text_font_comboBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        
        if select_option == True:
            self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_text_font_comboBox).mouse_click()    
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_stamp_comboBox, timeout = 9.0)
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_text_font_comboBox)
        
    def select_stamp_text_font_option(self, option):
        """
        Select the appropriate option from the Stamp text font Combobox.
        """
        self.goto_stamp_text_font_option()
        
        text_font_dict = {
            "antique": f"{ScanAppWorkflowObjectIds.combo_stamp_antiqueOlive}",
            "century": f"{ScanAppWorkflowObjectIds.combo_stamp_centurySchoolbook}",
            "garamond": f"{ScanAppWorkflowObjectIds.combo_stamp_garamond}",
            "letter": f"{ScanAppWorkflowObjectIds.combo_stamp_letterGothic}",
        }
        
        to_select_item = text_font_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, ScanAppWorkflowObjectIds.view_stamp_comboBox, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_comboBox_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view, timeout = 9.0)
        
    def verify_stamp_text_font_option(self, net, setting_value):
        """
        Verify the Stamp text font option in the Stamp options view.
        """
        self.goto_stamp_text_font_option(select_option = False)

        setting_id = ScanAppWorkflowObjectIds.stamp_text_font_comboBox
        cstring_id = ScanAppWorkflowObjectIds.stamp_text_font_format_string_dict[setting_value.lower()][0]
            
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id) 
        assert ui_setting_string == expected_string, "Setting value mismatch"
        
    def goto_stamp_text_size_option(self, select_option = True):
        """
        Navigate to the Stamp text size option in the Stamp options view.
        """
        logging.info("Navigated to the Stamp text size option.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_text_size_comboBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        
        if select_option == True:
            self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_text_size_comboBox).mouse_click()    
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_stamp_comboBox, timeout = 9.0)
        else:
            assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_text_size_comboBox)
        
    def select_stamp_text_size_option(self, option):
        """
        Select the appropriate option from the Stamp text size Combobox.
        """
        self.goto_stamp_text_size_option()
        
        text_size_dict = {
            "8point": f"{ScanAppWorkflowObjectIds.combo_stamp_eightPoint}",
            "12point": f"{ScanAppWorkflowObjectIds.combo_stamp_twelvePoint}",
            "20point": f"{ScanAppWorkflowObjectIds.combo_stamp_twentyPoint}",
        }
        
        to_select_item = text_size_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, ScanAppWorkflowObjectIds.view_stamp_comboBox, scrollbar_objectname = ScanAppWorkflowObjectIds.stamp_comboBox_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_stamp_settings_view, timeout = 9.0)
        
    def verify_stamp_text_size_option(self, net, setting_value):
        """
        Verify the Stamp text size option in the Stamp options view.
        """
        self.goto_stamp_text_size_option(select_option = False)

        setting_id = ScanAppWorkflowObjectIds.stamp_text_size_comboBox
        cstring_id = ScanAppWorkflowObjectIds.stamp_text_size_format_string_dict[setting_value.lower()][0]
            
        ui_setting_string = self.spice.query_item(setting_id + " SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id) 
        assert ui_setting_string == expected_string, "Setting value mismatch"
        
    def goto_stamp_white_background_option(self):
        """
        Navigate to the Stamp white background option in the Stamp options view.
        """
        logging.info("Navigated to the Stamp white background option.")
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_stamp_settings_view, ScanAppWorkflowObjectIds.row_stamp_white_background_checkBox, top_item_id='#SpiceHeaderVar2', select_option=False, scroll_step=1)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_white_background_checkBox)
        
    def set_stamp_white_background_option(self, checked):
        """
        Set the Stamp white background option in the Stamp options view.
        """
        self.goto_stamp_white_background_option()
        white_background_checkBox = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_white_background_checkBox)
        if checked is True:
            if white_background_checkBox["checked"] is False:
                white_background_checkBox.mouse_click()
                
        else:
            if white_background_checkBox["checked"] is True:
                white_background_checkBox.mouse_click()
                
    def verify_stamp_white_background_option(self, checked):
        """
        Verify the Stamp white background option in the Stamp options view.
        """
        self.goto_stamp_white_background_option()
        white_background_checkBox = self.spice.wait_for(ScanAppWorkflowObjectIds.stamp_white_background_checkBox)
        if checked is True:
            assert white_background_checkBox["checked"] is True
        else:
            assert white_background_checkBox["checked"] is False

    def verify_scan_jam_screen(self):
        """
        Check alert displayed when scan jam occurs.
        """
        logging.info("verify scan jam screen displayed")
        screen = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_jam_alert)
        
        assert screen
    
    def verify_scan_mispick_screen(self):
        """
        Check alert displayed when scan mispick occurs.
        """
        logging.info("verify scan mispick screen displayed")
        screen = self.spice.wait_for(ScanAppWorkflowObjectIds.miss_pick_alert)
        
        assert screen

    def click_on_scan_alert_screen_start_button(self):
        """
        Click on start button on scan jam screen.
        """
        start_button = self.spice.wait_for(ScanAppWorkflowObjectIds.start_button)
        start_button.mouse_click()
    
    def click_on_scan_alert_screen_cancel_button(self):
        """
        Click on cancel button on scan jam screen.
        """
        cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.cancel_button)
        cancel_button.mouse_click()
    
    def restart_job_after_scan_jam(self):
        """
        Restart the job after scan jam.
        """
        self.verify_scan_jam_screen()
        self.click_on_scan_alert_screen_start_button()
    

    def cancel_job_after_scan_jam(self):
        """
        Restart the job after scan jam.
        """
        self.verify_scan_jam_screen()
        self.click_on_scan_alert_screen_cancel_button()
    
    def restart_job_after_scan_mispick(self):
        """
        Restart the job after scan mispick.
        """
        self.verify_scan_mispick_screen()
        self.click_on_scan_alert_screen_start_button()
    

    def cancel_job_after_scan_mispick(self):
        """
        Restart the job after scan mispick.
        """
        self.verify_scan_mispick_screen()
        self.click_on_scan_alert_screen_cancel_button()
    
    def patch_operation_on_default_send_job_ticket(self,cdm,url,ticket_default_body):

        response = cdm.patch_raw(url, ticket_default_body)
        assert response.status_code == 200, "PATCH OPERATION WAS UNSUCCESSFUL" + url
    
    def get_operation_on_default_send_job_ticket(self,cdm,url):

        ticket_default_response = cdm.get_raw(url)
        assert ticket_default_response.status_code == 200, "GET OPERATION WAS UNSUCCESSFUL" + url
        return ticket_default_response.json()    
    
    def verify_preview_view_in_extensibility(self):
        assert self.spice.wait_for("#previewLandingView") 
        fitpage_layout = self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout=15.0)
        self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout =15.0)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)
        preview_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_add_page)
        self.spice.wait_until(lambda: preview_add_page_button["visible"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: preview_add_page_button["enabled"] == True, timeout = 15.0)
        copy_button = self.spice.wait_for(ScanAppWorkflowObjectIds.extensibility_preview_button, timeout=15.0)
        self.spice.wait_until(lambda: copy_button["enabled"] == True, timeout = 15.0)
        self.spice.wait_for(ScanAppWorkflowObjectIds.first_preview_image, timeout =15.0)

    def click_copy_button_in_extensibility(self):
        copy_button = self.spice.wait_for("#FooterView #FooterViewRight #mainActionButtonPreviewPanel")
        self.spice.wait_until(lambda: copy_button['enabled'] == True)
        copy_button.mouse_click()

    def click_copy_cancel_button_in_extensibility(self):
        cancel_button = self.spice.wait_for("#FooterView #FooterViewRight #cancelJobButtonPreviewPanel")
        self.spice.wait_until(lambda: cancel_button['enabled'] == True)
        cancel_button.mouse_click()

    def click_on_preview_add_page_button(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout)
        preview_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_add_page)
        self.spice.wait_until(lambda: preview_add_page_button['visible'] == True)
        self.spice.wait_until(lambda: preview_add_page_button['enabled'] == True, timeout = 15)
        preview_add_page_button.mouse_click()
    
    def add_page_pop_up_add_more(self):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_add_page_prompt_view)
        logging.info("At Add Page Pop Up")
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_copy_add_page_add)
        assert current_button
        current_button.mouse_click()
    
    def idcard_scan_pop_up_scan(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_prompt, timeout = 15.0)
        logging.info("At idcard scan Pop Up")
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_scan_button, timeout = 15.0)
        self.spice.wait_until(lambda: current_button["visible"] == True)
        current_button.mouse_click()
    
    def idcard_scan_pop_up_done(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_prompt, timeout=15.0)
        logging.info("At idcard scan Pop Up")
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_done_button, timeout=15.0)
        self.spice.wait_until(lambda: current_button["visible"] == True)
        current_button.mouse_click()

    def idcard_scan_pop_up_cancel(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_prompt, timeout = 15.0)
        logging.info("At idcard scan Pop Up")
        current_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_2_sided_id_cancel_button, timeout = 15.0)
        self.spice.wait_until(lambda: current_button["visible"] == True)
        current_button.mouse_click()
        yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_flatbed_cancel_job_prompt_yes_button, timeout = 15.0)
        yes_button.mouse_click()

    def goto_watermark_option(self):
        """
        Go to watermark option menu
        @return:
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)
        logging.info("Go to output size menu screen from scan options settings screen")
        self.workflow_common_operations.goto_item(ScanAppWorkflowObjectIds.list_watermark,
                                                  ScanAppWorkflowObjectIds.menu_list_scan_settings,
                                                  scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark)
        
    def verify_watermark_option_list_screen(self, option):
        """
        Go to watermark text option list screen and verify the option
        :return:
        """
        watermark_type_view = self.spice.wait_for(ScanAppWorkflowObjectIds.combo_watermarkType)
        self.spice.wait_until(lambda: watermark_type_view["visible"] == True, timeout=10.0)

        if option == "none":
            result = False
        else:
            result = True
        
        watermark_text_option = self.spice.wait_for(ScanAppWorkflowObjectIds.list_watermark_text)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.list_view_watermark, menu_item_id=ScanAppWorkflowObjectIds.list_watermark_text, select_option=False)
        self.spice.wait_until(lambda: watermark_text_option["visible"] == result, timeout=10.0)
        logging.info("at watermark text option list screen")

        first_page_only = self.spice.wait_for(ScanAppWorkflowObjectIds.list_watermark_first_page_only)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.list_view_watermark, menu_item_id=ScanAppWorkflowObjectIds.list_watermark_first_page_only, select_option=False)
        self.spice.wait_until(lambda: first_page_only["visible"] == result, timeout=10.0)
        logging.info("at watermark text option list screen")

    def goto_watermark_type_screen(self):
        """
        Go into option watermark type screen
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        menu_item_id = [ScanAppWorkflowObjectIds.row_combo_watermarkType, ScanAppWorkflowObjectIds.combo_watermarkType]
        self.workflow_common_operations.goto_item(menu_item_id, ScanAppWorkflowObjectIds.list_view_watermark, scrollbar_objectname = ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_watermarkType)

    def select_send_watermark_type(self, option):
        """
        Go to watermark type option menu and select the option
        @return:
        """
        self.goto_watermark_type_screen()
        watermark_options_dict = {
            "none": f"{ScanAppWorkflowObjectIds.combo_watermarkType_option_none}",
            "text": f"{ScanAppWorkflowObjectIds.combo_watermarkType_option_text}"
        }
        to_select_item = watermark_options_dict.get(option)
        current_button = self.spice.wait_for(to_select_item + "")
        current_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark, timeout = 9.0)

    def verify_send_watermark_constrained(self, net, constrained_message : str = ""):
        """
        Go to watermark menu and verify that option is cosntrained
        @return:
        """
        constrained_message = ScanAppWorkflowObjectIds.scan_settings_watermark_constraints_message
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_constraint_message)
        
        self.verify_constrained_message(net, constrained_message)

        okButton = self.spice.wait_for(ScanAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

    def goto_send_watermark_text(self):
        '''
        UI should be in Copy watermark screen.
        Navigates to watermark text screen starting from watermark screen.
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark)
        watermark_text_view = self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark + " " + ScanAppWorkflowObjectIds.button_watermark_text_MoreOptions, timeout = 10)
        assert watermark_text_view
        self.spice.wait_until(lambda: watermark_text_view["enabled"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: watermark_text_view["visible"] == True, timeout = 15.0)

        if (watermark_text_view["enabled"] == True and watermark_text_view["visible"] == True):
            watermark_text_view.mouse_click()
            self.spice.wait_for(ScanAppWorkflowObjectIds.view_watermark_text_MoreOptions_view)

    def select_send_watermark_text(self, option):

        self.goto_send_watermark_text()

        watermark_text_dict = {
            "draft": {
                "item_id": ScanAppWorkflowObjectIds.radio_watermark_text_draft,
                "row_id": ScanAppWorkflowObjectIds.row_watermark_text_draft
                },
            "confidential": {
                "item_id": ScanAppWorkflowObjectIds.radio_watermark_text_confidential,
                "row_id": ScanAppWorkflowObjectIds.row_watermark_text_confidential
                },
            "secret": {
                "item_id": ScanAppWorkflowObjectIds.radio_watermark_text_secret,
                "row_id": ScanAppWorkflowObjectIds.row_watermark_text_secret
                },
            "topSecret": {
                "item_id": ScanAppWorkflowObjectIds.radio_watermark_text_top_secret,
                "row_id": ScanAppWorkflowObjectIds.row_watermark_text_top_secret
                },
            "urgent": { 
                "item_id": ScanAppWorkflowObjectIds.radio_watermark_text_urgent,
                "row_id": ScanAppWorkflowObjectIds.row_watermark_text_urgent
            }
        }

        to_select_item = watermark_text_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.view_watermark_text_MoreOptions_view, menu_item_id=to_select_item["row_id"])
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark, timeout = 12.0)

    def enter_new_custom_watermark_text(self, custom_text):
        '''
        This is helper method to enter new email address from email options
        UI flow is common keyboard -> enter new email address
        '''
        self.workflow_common_operations.scroll_vertical_row_item_into_view(ScanAppWorkflowObjectIds.list_view_watermark, ScanAppWorkflowObjectIds.watermark_text_field, select_option=False)
        file_name_textbox = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.list_view_watermark} {ScanAppWorkflowObjectIds.watermark_text_field_text}")
        file_name_textbox.mouse_click()
        file_name_textbox.__setitem__('displayText', custom_text)
        keyword_ok = self.spice.wait_for(ScanAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
   
    def verify_send_watermark_selection_option(self, net, setting_value):
        """
        This method compares the watermark text setting string with the expected string from string id
        Args:
            UI should be in Copy watermark settings view
            setting: watermark format to be validated -> e.g.: "watermark text", "default or custom".
            setting_value: Value of the setting
        """
        expected_string_id = ""
        actual_string_id = ""
        self.homemenu.menu_navigation(self.spice,ScanAppWorkflowObjectIds.menu_list_scan_settings, 
                                      ScanAppWorkflowObjectIds.list_watermark, 
                                      scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_option_screen, select_option=False)
 
        expected_string_id = self.watermark_text_options_dict[setting_value.lower()][0]
        actual_string_id = ScanAppWorkflowObjectIds.list_watermark_value

        expected_string = LocalizationHelper.get_string_translation(net, expected_string_id)
        actual_string_id = self.spice.wait_for(actual_string_id + " SpiceText[visible=true]")["text"]
        assert  actual_string_id == expected_string, "watermark text settings value mismatch"
        
    def select_first_page_only_option(self):
        """
        Go to first page only option menu and select the option
        @return:
        """
        # self.goto_copy_first_page_only_option()
        first_page_only_checkbox = self.spice.wait_for(ScanAppWorkflowObjectIds.checkbox_first_page_only)

        if first_page_only_checkbox["checked"] is False:
            first_page_only_checkbox.mouse_click()
            assert first_page_only_checkbox["checked"] is True
        else:
            first_page_only_checkbox.mouse_click()
            assert first_page_only_checkbox["checked"] is False

    def goto_watermark_text_font_screen(self):
        """
        Go into option watermark text font screen
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        menu_item_id = [ScanAppWorkflowObjectIds.row_combo_text_font, ScanAppWorkflowObjectIds.combo_text_font]
        self.workflow_common_operations.goto_item(menu_item_id, ScanAppWorkflowObjectIds.list_view_watermark, scrollbar_objectname = ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark)

    def select_send_watermark_text_font(self, option):
        """
        Go to watermark text font option menu and select the option
        @return:
        """
        self.goto_watermark_text_font_screen()
        text_font_options_dict = {
            "Letter Gothic": f"{ScanAppWorkflowObjectIds.combo_text_font_letter_gothic}",
            "Antique Olive": f"{ScanAppWorkflowObjectIds.combo_text_font_antique_olive}",
            "Century Schoolbook": f"{ScanAppWorkflowObjectIds.combo_text_font_century_schoolbook}",
            "Garamond Antiqua": f"{ScanAppWorkflowObjectIds.combo_text_font_garamond}"
        }
        to_select_item = text_font_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, ScanAppWorkflowObjectIds.view_text_font, 
            scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_combobox, select_option=False)
        current_button = self.spice.query_item(to_select_item + "")
        current_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark, timeout = 9.0)

    def goto_watermark_text_size_screen(self):
        """
        Go into option watermark text size screen
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        menu_item_id = [ScanAppWorkflowObjectIds.row_combo_text_size, ScanAppWorkflowObjectIds.combo_text_size]
        self.workflow_common_operations.goto_item(menu_item_id, ScanAppWorkflowObjectIds.list_view_watermark, scrollbar_objectname = ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark)

    def select_send_watermark_text_size(self, option):
        """
        Go to watermark text size option menu and select the option
        @return:
        """
        self.goto_watermark_text_size_screen()
        text_size_options_dict = {
            "thirtyPoint": f"{ScanAppWorkflowObjectIds.combo_text_size_thirtyPoint}",
            "fortyPoint": f"{ScanAppWorkflowObjectIds.combo_text_size_fortyPoint}",
            "sixtyPoint": f"{ScanAppWorkflowObjectIds.combo_text_size_sixtyPoint}"
        }
        to_select_item = text_size_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, ScanAppWorkflowObjectIds.view_text_size, 
            scrollbar_objectname = ScanAppWorkflowObjectIds.scrollbar_combobox, select_option=False)
        current_button = self.spice.query_item(to_select_item + "")
        current_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark, timeout = 9.0)

    def goto_watermark_text_color_screen(self):
        """
        Go to watermark text color option menu
        @return:
        """
        logging.info("Go to watermark text color option menu")
        self.homemenu.menu_navigation(self.spice,ScanAppWorkflowObjectIds.list_view_watermark, ScanAppWorkflowObjectIds.list_text_color, scrollbar_objectname = ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_text_color)

    def select_send_watermark_text_color(self, option):

        self.goto_watermark_text_color_screen()

        watermark_text_color_dict = {
            "black": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_black,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_black
                },
            "yellow": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_yellow,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_yellow
                },
            "green": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_green,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_green
                },
            "red": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_red,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_red
                },
            "blue": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_blue,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_blue
            },
            "skyBlue": {
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_skyBlue,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_skyBlue
            },
            "purple": { 
                "item_id": ScanAppWorkflowObjectIds.radio_text_color_purple,
                "row_id": ScanAppWorkflowObjectIds.row_text_color_purple
            }
        }

        to_select_item = watermark_text_color_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=ScanAppWorkflowObjectIds.list_view_text_color, menu_item_id=to_select_item["row_id"])
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark, timeout = 9.0)
    
    def goto_watermark_darkness_option(self):
        """
        go to watermark darkness option
        """
        logging.info("Go to watermark darkness option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        menu_item_id = [ScanAppWorkflowObjectIds.row_slider_watermark_darkness, ScanAppWorkflowObjectIds.slider_watermark_darkness]
        self.workflow_common_operations.goto_item(menu_item_id, ScanAppWorkflowObjectIds.list_view_watermark, select_option = False, scrollbar_objectname = ScanAppWorkflowObjectIds.copy_watermark_options_scrollbar)
        
    def select_watermark_darkness(self, value: int):
        """
        UI should be on Watermark settings view.
        Args:
            value: The watermark darkness value to set - ( Range is 1 to 5)
        """
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.list_view_watermark), "Error: Not in Watermark settings view"
        self.goto_watermark_darkness_option()
        current_slider_value = self.spice.query_item(ScanAppWorkflowObjectIds.slider_watermark_darkness)
        logging.info("Current watermark darkness value is: %s" % current_slider_value["value"])

        watermark_darkness_slider = self.spice.wait_for(ScanAppWorkflowObjectIds.slider_watermark_darkness)
        watermark_darkness_slider.__setitem__('value', value)

        current_slider_value = self.spice.query_item(ScanAppWorkflowObjectIds.slider_watermark_darkness)["value"]
        logging.info("After setting watermark darkness value is: %s" % current_slider_value)
    
    def go_back_to_setting_from_watermark(self):
        self.workflow_common_operations.back_or_close_button_press(f"{ScanAppWorkflowObjectIds.watermark_done_button}", ScanAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_constrained_message(self, net , constrained_message : str = ""):
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.view_constraint_message)

        if(constrained_message != ""):
            constrained_message_text = self.spice.wait_for(ScanAppWorkflowObjectIds.constraint_message_text)["text"]
            assert constrained_message_text == self.workflow_common_operations.get_expected_translation_str_by_str_id(net, constrained_message)

    def validate_settings_used_in_send(self, job_ticket, watermark_type=None, watermark_Id=None, watermark_custom_text=None, watermark_first_page_only=None, watermark_text_font=None, 
                                   watermark_text_size=None, watermark_text_color=None, watermark_darkness=None, stamp_location=None, stamp_location_id=None, 
                                   stamp_policy=None, stamp_content=None, stamp_text_color=None, stamp_text_font=None, stamp_text_size=None, stamp_starting_page=None, 
                                   stamp_starting_number=None, stamp_num_of_digit=None, stamp_page_numbering=None, stamp_white_background=None) -> None:
        """
        Verify all the settings used for send job using cdm
        :param job_ticket:
        :param watermark_type:
        :param watermark_Id:
        :param watermark_custom_text:
        :param watermark_first_page_only:
        :param watermark_text_font:
        :param watermark_text_size:
        :param watermark_text_color:
        :param watermark_darkness:
        :param stamp_location:
        :param stamp_location_id:
        :param stamp_policy:
        :param stamp_content:
        :param stamp_text_color:
        :param stamp_text_font:
        :param stamp_text_size:
        :param stamp_starting_page:
        :param stamp_starting_number:
        :param stamp_num_of_digit:
        :param stamp_page_numbering:
        :param stamp_white_background:
        """
        logging.info("Verify all the values used for job using cdm")
        send_job_details = job_ticket
 
        if watermark_type:
            logging.info("Check watermark type Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["watermarkType"] == watermark_type, "Wrong watermark type"
 
        if watermark_Id:
            logging.info("Check watermark text Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["watermarkId"] == watermark_Id, "Wrong watermark text"
        if watermark_custom_text:
            logging.info("Check watermark custom text Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["customText"] == watermark_custom_text, "Wrong watermark custom text"
        if watermark_first_page_only:
            logging.info("Check watermark first page only Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["onlyFirstPage"] == watermark_first_page_only, "Wrong watermark first page only"
 
        if watermark_text_font:
            logging.info("Check watermark text font Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["textFont"] == watermark_text_font, "Wrong watermark text font"
 
        if watermark_text_size:
            logging.info("Check watermark text size Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["textSize"] == watermark_text_size, "Wrong watermark text size"
 
        if watermark_text_color:
            logging.info("Check watermark text color Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["textColor"] == watermark_text_color, "Wrong watermark text color"
 
        if watermark_darkness:
            logging.info("Check watermark darkness Setting")
            assert send_job_details["pipelineOptions"]["watermark"]["darkness"] == watermark_darkness, "Wrong watermark darkness"
        if stamp_location_id:
            logging.info("Check stamp location id Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["locationId"] == stamp_location_id, "Wrong stamp location id"
        if stamp_policy:
            logging.info("Check stamp policy Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["policy"] == stamp_policy, "Wrong stamp policy"
        if stamp_content:
            logging.info("Check stamp content Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["stampContent"] == stamp_content, "Wrong stamp content"
        if stamp_text_color:
            logging.info("Check stamp text color Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["textColor"] == stamp_text_color, "Wrong stamp text color"
        if stamp_text_font:
            logging.info("Check stamp text font Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["textFont"] == stamp_text_font, "Wrong stamp text font"
        if stamp_text_size:
            logging.info("Check stamp text size Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["textSize"] == stamp_text_size, "Wrong stamp text size"
 
        if stamp_starting_page:
            logging.info("Check stamp starting page Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["startingPage"] == stamp_starting_page, "Wrong stamp starting page"
        if stamp_starting_number:
            logging.info("Check stamp starting number Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["startingNumber"] == stamp_starting_number, "Wrong stamp starting number"
        if stamp_num_of_digit:
            logging.info("Check stamp number of digit Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["numberOfDigits"] == stamp_num_of_digit, "Wrong stamp number of digit"
        if stamp_page_numbering:
            logging.info("Check stamp page numbering Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["pageNumberingStyle"] == stamp_page_numbering, "Wrong stamp page numbering"
        if stamp_white_background:
            logging.info("Check stamp white background Setting")
            assert send_job_details["pipelineOptions"][stamp_location]["whiteBackground"] == stamp_white_background, "Wrong stamp white background"

    def login_and_out_to_cross_session_boundary(self):
        """
        Helper function to login and logout to cross session boundary and bring RBAC setting live to the UI.
        """
        self.spice.goto_homescreen()
        self.spice.signIn.goto_universal_sign_in("Sign In")
        self.spice.signIn.select_sign_in_method("admin", "user")
        self.spice.signIn.enter_creds(login=True,authAgent="admin", password="12345678")
        response = self.spice.signIn.verify_auth("success")
        assert response, "Login with valid device user credentials failed"
        self.spice.signIn.goto_universal_sign_in("Sign Out")


