#########################################################################################
# @file      IScanAppUIOperations.py
# @author    Anu Sebastian (anu.sebastian@hp.com)
# @date      11-02-2021
# @brief     Interface for all the Scan settings UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import logging
import sys

class IScanAppUIOperations(object):

    def goto_scan_app(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_email_from_scanapp_at_home_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_folder_from_scanapp_at_home_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_filetype_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_pdf_encryption_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_high_compression_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_resolution_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_paper_type_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def goto_filesize_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_2_sided_format_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_scan_mode_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_color_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_original_size_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_orientation_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_lighter_darker_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_contrast_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_long_original_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_edge_to_edge_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_color_removal_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_background_noise_removal_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_blank_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_filetype(self, filetype: str):
        '''
        UI should be on File type settings screen.
        Args:
            filetype: The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_pdf_encryption(self, encryption: bool = False):
        '''
        UI should be on Scan settings view.
        Args:
            encryption: PDF encryption toggle - True/False
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_long_original(self, longplot: bool = False):
        '''
        UI should be on long original switch in Scan settings screen.
        Args:
            long original: The long original toggle value to set - ( True/False)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_edge_to_edge(self):
        '''
        UI should be on Edge-to-Edge switch in Scan settings screen.
        Args:
            edge_to_edge: The Edge-to-Edge toggle value to set - ( True/False)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_background_color_removal(self):
        '''
        UI should be on Scan settings view.
        Args:
            Scan background Color removal: Scan background Color removal toggle - True/False
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_background_noise_removal(self):
        '''
        UI should be on Scan settings view.
        Args:
            Scan background Noise removal: Scan background Noise removal toggle - True/False
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    

    def set_scan_settings_resolution(self, resolution: str):
        '''
        UI should be on Resolution settings screen.
        Args:
            resolution: The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                        e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_original_paper_type(self, originalpaper_type: str):
        '''
         UI should be on original paper type settings screen.
        Args
            originalpaper_type: The original paper type to set - white, translucent, blueprint
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_filesize(self, filesize: str):
        '''
        UI should be on FileSize settings screen.
        Args:
            FileSize: The FileSize to set - lowest, low, medium,high,highest
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_high_compression(self, compression: bool = False):
        '''
        UI should be on Scan settings view.
        Args:
            compression: The compression toggle value - True/False
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_sides(self, sides: str):
        '''
        UI should be on Sides settings screen.
        Args:
            sides: The sides to set - simplex, duplex
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_2_sided_format_settings(self, style: str):
       
        """
        UI should be on 2 sided format settings screen.
        Args:
            style: The style to set - flipstyle, bookstyle
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_scan_mode_settings(self, mode: str):
        """
        UI should be on scan mode settings screen.
        Args:
            mode: The mode to set - standard, bookmode
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_scancapture_mode(self, scancapturemode: str):
        '''
        UI should be on ScanCapture settings screen.
        Args:
            scancapturemode : The scancapture mode to set - standard,bookmode,idcard,jobbuild
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_color(self, color: str):
        '''
        UI should be on Color format settings screen.
        Args:
            color: The color to set - color, blackonly, grayscale, autodetect
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_original_size(self, size: str):
        '''
        UI should be on Original size settings screen.
        Args:
            size: The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_orientation(self, orientation: str):
        '''
        UI should be on Orienation settings screen.
        Args:
            orientation: The orientation to set - portrait, landscape
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_contrast(self, contrast: int = 1):
        '''
        UI should be on Contrast slider in Scan settings screen.
        Args:
            contrast: The Contrast value to set - ( Range is 1 to 9)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
 
    def set_scan_setting(self, setting, setting_value):
        '''
        UI should be on specific settings screen.
        Args:
            setting: The setting that has to be set - filetype, resolution, filesize, sides, color,
            size, orientation
            setting_value: Value to set for the setting
                The filetype to set - pdf, tiff, jpeg, pdfa, ppm, pgm, png, raw
                The resolution to set - e75dpi, e100dpi, e150dpi, e200dpi,
                    e240dpi, e300dpi, e400dpi, e500dpi, e600dpi, e1200dpi
                The filesize to set - lowest,low,medium,high,highest
                The sides to set - simplex, duplex
                The color to set - color, blackonly, grayscale, autodetect
                The original size to set - letter, legal, a4, a5, a6 ,b2, b3, jis_b4, b5_envelope,
                    jis_b6, a0, a1, a2, a3, a4, a5, a6,  ledger, custom, anycustom, executive,
                    officio_8_5x13, 4x6in, 5x7in, 5x8in, jis_b5, jis_b6, 100x150mm, 16k_195x270mm,
                    16k_184x260mm, 16k, jpostcard, jdoublepostcard, personal_3_625x6_5in, envelope_10,
                    envelope_monarch, envelope_c5, envelope_dl, photo4x11, photo5x5, photo5x11, photo8x8,
                    iso_c6, envelope_a2, chou_3_envelope, statement, index_3x5in, oe_photo_l_3_5x5in,
                    letter_8x10in
                The orientation to set - portrait, landscape
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def pdf_encryption_enter_password(self, text:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def pdf_encryption_reenter_password(self, text:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def pdf_encryption_save(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def pdf_encryption_cancel(self):
        '''
        This method clicks the cancel button in pdf encryption prompt
        UI Flow is pdf encryption prompt -> cancel button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def pdf_encryption_password_not_match_ok(self):
        """
        This method clicks the ok button in pdf encryption password not match error
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_pdf_encryption_password_not_match(self, net):
        """
        Check spec on pdf encryption password not match screen
        @param net: 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_insert_usb_storage(self, net):
        """
        Check spec on insert usb storage screen
        @param net: 
        """
        logging.info("Check spec on pdf encryption password not match screen")
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def verify_string(self, net, string_oid, expected_id, menu_level: int = 0):
        '''This method verifies the string on the screen with the expected string from  string id

        Args:
            string_oid: Object Id of string on the screen to be validated
            expected_id: String Id of the of the expected string
            menu_level: Menu level number
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_setting_is_selected(self, net, setting, setting_value, menu_level: int = 0):
        '''This method compares the selected setting value is checked and at activefocus
        Args:
            UI should be in specific Setting(e.g.: Resolution) value selection screen
            setting: Setting to be validated
            setting_value: setting value
            menu_level: Menu level number
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_setting_string(self, net, setting, setting_value,job=None, screen_id = "#MenuListLayout"):
        '''This method compares the selected setting string with the expected string from  string id
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
            setting_value: Value of the setting
            menu_level: Menu level number
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_setting_lighter_darker_value(self, setting_value):
        """
        UI should be on lighter_darker slider in Scan settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_settings_pdf_encryption_value(self, setting_value:bool):
        """
        UI should be on pdf encryption toggle button in Scan settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_status_toast(self, net, message: str = "complete", time_out=60, specific_str_checked=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, starting /scanning /complete
              timeout:
              specific_str_checked: 1. True, strings containing special characters should equal to toast message/False, just need to judge that the string is included in the toast message.
                                    2. Just to check the corresponding status, please using with False/Need to check its screen expected str, please using True
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_enter_pdf_encryption_password_screen(self, net):
        """
        Check spec on enter pdf encryption password screen
        @param net: 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_filename_string(self, filename):
        '''
        This method compares the filename string with the expected string
        UI should be in file settings landing view
        Args: filename: expected filename string
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_string_scanapps_at_home_screen(self, object_name):
        """
        UI should be on Scan app screen from home.
        UI Flow is Home -> Scan app.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_string_not_visibile_scanapps_at_home_screen(self, object_name):
        """
        UI should be on Scan app screen from home.
        UI Flow is Home -> Scan app.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_home_from_preview(self):
        '''
        UI should be in Preview screen
        UI flow is scan home -> main ui
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def preview_cancel(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_expand_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_preview_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_preview_and_verify_preview_added(self):
        '''
        This is helper method to verify preview
        UI flow Landing Page->click Expand Button->click Preview Button->check Preview is added
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
 
    def start_send_from_preview_panel(self, button_object_id = None, scan_more_pages: bool = False):
        '''
        Ui Should be in previewpanel
        Click on send button starts send
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_document_feeder_jam_screen(self):
        """
        Check alert displayed when document feeder jam occurs.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_constrained_message_for_page_insertion(self,net):
        """
        Check the constrained message for page insertion and close the modal.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_scan_settings_editable(self, net, setting, editable: bool = True):
        """
        This method verify scan settings editable filename, filetype
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated
                    filename, filetype
            editable: Need to pass bool values True/False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_input_field_constraint_message_displayed(self, net, message):
        '''
        This is to verify that the file type cannot be changed.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_input_field_constraint_screen_ok_button(self):
        """
        This method is to click OK button at the read-only enabled display screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_on_alert_dialog(self):
        '''
        Click on OK Button on the alert dialog screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_add_more_button_on_add_page(self):
        """"
        UI should be at add page view
        add more page from flatbed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_clip_in_scanner_screen(self, timeout=9.0):
        '''
        This method will verify current screen is clipInScanner alert
        Args: timeout: max time to wait
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_collapse_button(self):
        '''
        This method will collapse the preview panel
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def refresh_preview_from_preview_panel_refresh_button(self):
        '''
        Ui Should be in previewpanel
        Click on refresh button to refresh the preview
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_preview(self):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def refresh_preview_from_warning_icon(self):
        '''
        Ui Should be in previewpanel
        Click on Preview image > Refresh Modal Dialog > Refresh Button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, footer_item_id=None, scroll_height=60):
        """
        Scroll contact/group into center of sceen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items.
        UI is in Addressbook contacts list view 
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                footer_item_id: object name for footer view, keep it as None if it does not inculded in scroll view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_sort_order(self, sort):
        '''
        Select sort order
        @param:sort: only two order: AtoZ/ZtoA 
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_settings_high_compression_value(self, setting_value:bool):
        """
        UI should be on high_compression toggle button in Scan settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_scan_setting_toggle_option_value(self, setting, setting_value:bool):
        """
        This method compares the toggle status with expected value
        Args:
            UI should be in Settings/Options Landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_menu_app_from_scan_app(self):
        '''
        UI should be in Scan app
        UI flow is Scan App landing view -> Menu app screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_button_on_non_concurrent_scan_complete_screen(self):
        """
        Click ok button when scan job compelete successfully for non concurrent product
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_invert_blueprint_settings(self):
        """
        UI should be on Scan options list screen.UI Flow is go to Scan Invert BluePrint
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_reduce_scan_speed_to_enhance_quality_settings(self):
        """
        UI should be on Scan options list screen.UI Flow is go to Reduce Scan Speed to Enhance Quality 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_blueprint_invert(self, blueprint_invert:bool = True):
        """
        UI should be on Scan settings view.
        Purpose: toggle invert blueprint settings switch
        Args: blueprint_invert: bool True or False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_reduce_speed_enhance(self, reduce_speed:bool = True):
        """
        UI should be on Scan settings view.
        Purpose: toggle Reduce Scan Speed to Enhance Quality 
        Args: reduce_speed: bool True or False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_auto_release_original_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is to to Scan Auto Release Original
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_black_enhancement_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is go to Scan Black Enhancement
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_detailed_background_removal_settings(self):
        """
        UI should be on Scan options list screen. UI Flow is got to Detailed Background Removal
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_output_size_settings(self):
        """
        UI should be on Scan Output Size settings screen. UI Flow is go to Options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_output_size_position_settings(self):
        """
        UI should be on Scan Output Size list screen. UI Flow is go to Positioning
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_output_size_orientation_settings(self):
        """
        UI should be on Scan Output Size list screen. UI Flow is go to Orientation
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_auto_release_original(self, auto_release: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            auto_release: Scan Auto Release Original toggle - True/False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_black_enhancement(self, black_enhancement_value: int):
        """
        UI should be on Black Enhancement in Scan settings screen.
        Args:
            black_enhancement_value: The black enhancement value to set - ( Range is 0 to 255)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_detailed_background_removal(self, background_removal_value: int = 1):
        """
        UI should be on Detailed Background Removal slider in Scan settings screen.
        Args:
            background_removal_value: The Detailed Background Removal value to set - ( Range is -6 to 6)
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_output_size(self, output_size: str, custom_output_size_width=None, custom_output_size_length=None):
        """
        UI should be Output Size settings screen.
        Args
            output_size: The Output Size to set 
            custom_output_size_width: set custom width when output size is custom, int [66-914]
            custom_output_size_length: set custom length when output size is custom, int [66-2377]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_save_as_multiple_files(self, save_as_multiple_files: bool = False):
        """
        UI should be Save As Multiple Files settings screen.
        Args
            save_as_multiple_files: value to set (on/off) 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_position(self, position_type: str):
        """
        UI should be Position settings screen.
        Args
            position_type: The position to set 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_output_size_orientation(self, orientation_type: str):
        """
        UI should be on Orientation type settings screen.
        Args
            orientation_type: The Orientation to set
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_output_settings_value(self, net, setting, setting_value):
        """
        This method compares the selected output setting string with the expected string from string id
        UI should be in options screen
        Args:
            setting: Setting to be validated
            setting_value: Value of the setting
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_output_size_menu_list(self):
        """
        Go to output settings menu screen from scan options settings screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_options_screen_from_output_size_screen(self):
        """
        click Back button back to scan options screen from output size screen 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_options_screen_from_save_as_multiple_files_screen(self):
        """
        click Back button back to scan options screen from save as multiple files screen 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_setting_detailed_background_removal_value(self, setting_value):
        """
        UI should be on background_removal_level slider in Scan settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_scan_send_button(self, net,  button_object_id = None):
        """
        validate scan send button
        :param button_object_id: button object name
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_eject_button_visible(self, visible: bool, timeout = 10.0):
        '''
        Check eject button is visible or not
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_eject_button_enabled(self, enabled: bool, timeout = 10.0):
        '''
        Check eject button is enable or not
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_eject_button(self):
        """
        Click eject button
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
