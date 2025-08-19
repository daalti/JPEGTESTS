#########################################################################################
# @file     ICopyAppUIOperations.py
# @authors  Vinay Kumar M(vinay.kumar.m@hp.com)
# @date     16-03-2021
# @brief    Interface for all the Copy UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class ICopyAppUIOperations(object):

    def goto_menu_mainMenu(self, spice):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy(self, spice):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_copy_app(self):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu
        :param _spice: Takes 0 arguments
        :return: Copy App
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_blueprint_invert_toggle(self, blueprint_invert):
        """
        toggle invert blueprint settings switch
        Args: blueprint_invert: bool True or False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ui_select_copy_page(self, spice):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Copy
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ui_copy_set_no_of_pages(self, spice, value):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: Copy screen -> Set number of pages
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def close_option_mode(self):
        """
        Closes the menu opened by `goto_copy_options_list`
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_copy_side(self, side_mode:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_landing_view(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen to landing screen.
        UI Flow is Option screen->Landing screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_copy(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_copy_2sided_operation(self, operation_type:str):
        '''
        UI should be in Prompt screen.
        Navigates to Side screen starting from Prompt screen.
        UI Flow is Prompt screen->select option
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_quality_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_copy_quality(self, quality:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_selected_quickset_name(self, net,  stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check Copy QuicksetSelected Button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def save_as_default_copy_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_quickset_view(self):
        '''
        This is helper method to goto copy quickset
        UI flow Select Landing-> click on any quickset button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_copy_quickset(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def check_spec_on_copy_home(self, net):
        """
        check spec on COPY HOME
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_options_list(self, net):
        """
        check spec on OPTIONS_LIST
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_copy_pages_per_sheet_options(self):
        """
        Get the pages sheet option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_pages_per_sheet(self):
        """
        Go to pages per sheet option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_copy_options_pages_per_sheet(self, net):
        """
        check spec on copy_OptionsPagesPerSheet
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_copy_options_sides_and_select_side(self, net, side = "1_1_sided"):
        """
        check spec on copy_OptionsSides
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_copy_2sided_pages_flip_up_status(self):
        """
        Get the option status of 2 sided pages flip_up
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_copy_2sided_flip_up_options(self, two_sided_options="off"):
        """
        Set the status of 2side flip up option
        @param two_sided_options:str -> on/off
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_output_scale(self):
        """
        Go to output scale option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_copy_options_output_scale(self, net):
        """
        check spec on copy_OptionsOutputScale
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_output_scale_custom_menu(self):
        """
        Go to output scale custom option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_copy_custom_value_option(self, input_value=0):
        """
        set output scale custom value
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_copy_custom_value_option(self):
        """
        Get the custom value option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_copy_options_list_view(self, option_mode: str):
        """
        UI should be in the screen where the option content is set.
        Navigates to Option screen
        @param option_mode:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_content_type_screen(self):
        """
        Go into option content type screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_copy_margins_screen(self):
        """
        Go into option content type screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_options_content_type(self, net):
        """
        Check spec on COPY_OptionsContentType
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_options_color(self, net):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_options_quality(self, net):
        """
        Check spec on COPY_OptionsQuality
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_original_size_screen(self):
        """
        Go to original size screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_common_list_item_values(self, expected_value_list, net, index=2, locale: str = "en-US"):
        """
        Check spec when a large number of values appear
        @param expected_value_list, net, locale
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_original_size(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsOriginalSize
        @param expected_value_list, net, locale
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_paper_size(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsPaperSelectionPaperSize
        @param expected_value_list, net, locale
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_paper_type(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsPaperSelectionPaperType
        @param expected_value_list, net, locale
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_paper_size_screen(self):
        """
        Go to media size screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_paper_type_screen(self):
        """
        Go to paper type screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_paper_tray_screen(self):
        """
        Go to paper tray screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_options_paperSelection(self, net):
        """
        Check spec on COPY_OptionsPaperSelection
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_copy_paper_tray(self, net):
        """
        Purpose: Navigates to Copy app screen from the widget
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    #Copy Widget Functions
    def goto_copy_app_widget(self):
        """
        Check spec copy_options_paperSelection_paperTray
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_copy_widget(self):
        '''
        UI should be in Homescreen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def change_num_copies(self, num_copies=1):
        '''
        Change the number of copies for a copy job on the widget.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_copy_start_button_disabled(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Chech copy button disabled
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_copy_delete_quickset_successfully(self, copy_name):
        """
        Check corresponding quickset is deleted from FP UI.
        @param copy_name:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_from_copyapp_at_home_screen(self):
        """
        Purpose: Navigates to Copy app screen by clicking copy icon on Home screen
        Ui Flow: Any screen -> Home screen -> Copy app
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_collate(self, collate_option="off"):
        """
        Set the status of collate option
        @param collate_option:str -> on/off
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_copy_status_toast(self, net, configuration, message: str = "Complete", timeout= 30):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, Starting... -> Scanning... -> Copying... -> Copy complete
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_job_toast_or_modal_not_appear(self, net, configuration, message: str = "Complete", timeout= 30):
        """
        Purpose: Wait for the given toast not appears
        Args: message: str, Starting... -> Scanning... -> Copying... -> Copy complete
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_copy_job_status_modal(self,net, configuration, message: str = "Complete", timeout= 60):
        """
        Purpose: Wait for the given modal to appear in non concurrent products
        Args: message: str,  Scanning... -> Copying... -> Copy complete
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def wait_for_copy_job_status_toast_or_modal(self, net, configuration, message: str = "Complete", timeout= 60):
        """
        Purpose: Wait for the given toast/modal to appear while copying
        Args: message: str,  Scanning... -> Copying... -> Copy complete
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_copy_settings_selected_option(self, net, setting, setting_value, screen_id = None):
        """
        This method compares the selected setting string with the expected string from  string id
        Args:
            UI should be in Settings/Options Landing view
            setting: Setting to be validated -> such as color mode/output_scale and so on.
            setting_value: Value of the setting
            screen_id: screen_id of the string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_item_unavailable(self,objname):
        '''
        verifies that item with objectname->objname is not availble
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_copy_paper_selection_option(self, net, setting, setting_value):
        """
        This method compares the paper selection setting string with the expected string from string id
        Args:
            UI should be in Copy paper selection settings view
            setting: paper_selection to be validated -> e.g.: "paper_size", "paper_type", "paper_tray".
            setting_value: Value of the setting
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_copy_landing_selected_option(self, net, setting, setting_value, screen_id = None):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Copy Landing view
            setting: Setting to be validated -> e.g.: color mode.
            setting_value: Value of the setting
            screen_id: screen_id of the string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def start_copy_from_preview_panel(self):
        '''
        Ui Should be in previewpanel
        Ui flow click on previewbutton->waith for preview to complete->Click on cancel button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def goto_preview_panel(self):
        '''
        This is helper method to preview panel settings
        UI flow Landing Page-> click on exapndbutton
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def cancel_copy_from_preview_panel(self):
        '''
        Ui Should be in previewpanel
        Ui flow click on previewbutton->waith for preview to complete->Click on cancel button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def media_mismatch_flow(self):
        """
        Purpose: Handling media size mismatch alert
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def copy_duplex_continue(self):
        """
        Purpose: Adding more than one page for duplex copying
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_copy_constrained_message(self):
        """
        Purpose: Checking the constraint Message text and close the modal
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_main_panel(self):
        '''
        This is helper method to go to main panel
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def refresh_preview_from_preview_panel_refresh_button(self):
        '''
        Ui Should be in previewpanel
        Click on refresh button to refresh preview
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def refresh_preview_from_warning_icon(self):
        '''
        Ui Should be in previewpanel
        Click on Preview Image Warning Icon > Refresh Modal Dailog > Refresh button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_copy_setting_lighter_darker_value(self, setting_value):
        """
        UI should be on lighter_darker slider in Copy settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_copy_setting_collate_status(self, setting_value):
        """
        UI should be on Copy settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_copy_setting_2sided_pages_flip_up_status(self, setting_value):
        """
        UI should be on Copy settings screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_select_setting_with_payload_and_back_landing_view(self, udw, net, settings:dict, copy_path=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def copy_job_ticket_general_method(self,loadmedia, copy_path, copy_settings: dict, udw, net, print_emulation=None, familyname="", scan_emulation=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_documentcopy_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> Copy >> Document copy
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def goto_idcopy_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> Copy >> idcopy copy
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copywidget_option_landingview_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> copywidget option >> copylanding view
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_home_screen_at_copy_app(self):
        """
        Purpose: Navigates to Home screen -> Copy app
        Ui Flow: Any screen -> Home screen -> Copy app
        :param spice : Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_background_noise_removal_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy background noise removal-> (copy background noise removal settings screen).
        return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_scan_settings_background_noise_removal(self, noise_removal: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy background noise removal: copy background noise removal toggle - True/False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_background_color_removal_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy background Color removal-> (copy background Color removal settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_copy_settings_background_color_removal(self, colorremoval: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy background Color removal: copy background Color removal toggle - True/False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_black_enhancements_settings(self):
        """
        UI should be on copy options list screen.
        Go to Black Enhancement and settings
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_black_enhancements_settings(self, black_enhancements = None):
        """
        UI should be on copy options list screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_detailed_original_media(self, value):
        """
        UI should be on copy options list screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_original_paper_type_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy original paper type-> (copy original paper type settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_edge_to_edge_output(self, value: bool = False):
        """
        UI should be on Scan settings view.
        Args:
            copy edge to edge output: copy edge to edge output - True/False  
        True: open edge_to_edge_output switch
        False: close edge_to_edge_output switch
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_edge_to_edge_output_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy edge to edge output-> (copy edge to edge output settings screen).
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_original_size(self, option):
        #change originalSize
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_option_original_size_screen(self):
        """
        Go to original size screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_original_size_value(self, option, net):
        """
        Check if the selected value is expected
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def verify_paper_size_value_under_paper_selection(self, net, option):
        """
        Ui Should be on paper selection screen
        Check if the selected paper size value is expected
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_paper_type_value(self, option, net):
        """
        Check if the selected value is expected
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    

    def is_original_size_visible_ui(self, original_size):
        """
        Ui Should be on original size list screen
        Check if the original_size value is visible
        """   
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_copy_sides_value(self, option, net):
        """
        Ui Should be on Sides screen
        Check if the selected sides value is expected
        @param option:str -> 1_1_sided/1_2_sided/2_1_sided/2_2_sided
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_to_copy_option_original_size_item(self):
        """
        scroll to original size item
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_paper_type_option_available(self, option):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_option_staple(self):
        """
        Go to staple option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_option_punch(self):
        """
        Go to punch option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_staple_option(self, option):
        """
        Select staple option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_punch_option(self, option):
        """
        Select punch option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_option_fold(self):
        """
        Go to fold option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fold_option(self, option):
        """
        Select fold option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_booklet_option(self):
        """
        Go to booklet option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
              
    def select_bookletMaker_option(self, option):
        """
        Select BookletMaker option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    