#########################################################################################
# @file      IPrintFromMyhomeAppUIOperations.py
# @author    Gwangeun Sim (gwangeun.sim@hp.com)
# @date      26-06-2023
# @brief     Interface for all the Print from My home UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class IPrintFromMyhomeAppUIOperations(object):

    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_joblog_from_ui(self, expected_list=[{"index": 2, "expect_value_list": ["Print from Network", "Success"]}]):
        """
        Check the job log from print ui under status menu
        @param expected_list:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_job_log_from_cdm(self, job, completion_state_list=["success"], time_out=30):
        """
        Check the job from cdm
        make sure invoke function job.bookmark_jobs() before performing a job
        @param job:
        @param completion_state_list:[success, cancelled]
        @param time_out:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_print_from_myhome(self):
        """
        Purpose: navigate to Print from My home under Print app.
        Ui Flow: Home_Print -> Print from My home app(ERROR_MESSAGE/LDAP_NOT_CONFIGURED/CONNECTING_TO_NETWORK)
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_visible_print_from_myhome(self):
        """
        Purpose: check if Print from My home under Print app is visible or not.
        @return: isVisible
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_print_from_myhome_home(self, net, header_text):
        """
        check spec on FOLDER_STRUCTURE in Print From My home app.
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_connecting_screen(self):
        """
        wait for connecting screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_print_file_or_folder_by_name(self, name: str, dial_value: int = 180):
        """
        UI should be in FOLDER_STRUCTURE of print from My home.
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_print_file_is_selected(self, name:str):
        """
        check print file is selected since select print file by name
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_value_of_no_of_copies(self):
        """
        Get the copy number
        @return: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_no_of_copies(self, value):
        """
        Set number of pages in detail panel of Print My home app 
        @param value:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_print(self):
        """
        UI should be in FOLDER_STRUCTURE of print from My home.
        Navigates to Side screen starting from FOLDER_STRUCTURE.
        UI Flow is click on print button
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_downloading_screen(self):
        """
        wait for downloading screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_downloading_screen_completed(self):
        """
        wait for downloading screen completed
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def press_cancel_button_from_downloading_screen(self):
        """
        press for downloading screen completed
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_myhome_print_file(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_print_complete_successfully(self, net, time_out=300):
        """
        Wait for print job complete
        @param time_out:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_menu(self):
        """
        Go to options menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_myhome_print_options(self, net, color_str_id, quality_str_id, two_sided="off", collate="off"):
        """
        Check spec on MyhomePrint_Options
        @param net:
        @param color_str_id:
        @param quality_str_id:
        @param two_sided:
        @param collate:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_copy_2sided_options_status(self):
        """
        Get the option status of 2sided setting
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_copy_2sided_options(self, two_sided_options="off"):
        """
        Set the status of 2side option
        @param two_sided_options:str -> on/off
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_color_options(self):
        """
        Get the color option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_color_options_menu(self):
        """
        Go to color option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_myhome_print_options_color(self, net):
        """
        Check spec on MyhomePrint_OptionsColor
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_color_options(self, net, color_options="color", locale: str = "en-US"):
        """
        Set the color option
        @param net:
        @param color_options: str -> color/auto/grayscale
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_collate_options_status(self):
        """
        Get collate option status
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_collate_options(self, collate_options="off"):
        """
        Set collate option
        @param collate_options:str -> on/off
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_quality_options(self):
        """
        Get quality option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_quality_options_menu(self):
        """
        Go to quality option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_myhome_print_options_quality(self, net):
        """
        check spec on MyhomePrint_OptionsQuality
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_quality_options(self, net, quality_options="standard", locale: str = "en-US"):
        """
        Set quality option
        @param net:
        @param quality_options:str -> best/standard/draft
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_paper_selection_options(self):
        """
        Get paper selection option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_paper_type_options(self):
        """
        Get paper type option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_myhome_print_options_paper_type(self):
        """
        Go to MyhomePrint_OptionsPaperType from MyhomePrint_OptionsPaperSelection screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_myhome_print_options_paper_type(self, net):
        """
        Check spec on MyhomePrint_OptionsPaperType
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_paper_type_options(self, net, paperType_options="Plain", locale: str = "en-US"):
        """
        Set paper type option
        @param net:
        @param paperType_options: str -> Plain/Custom
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_myhome_print_options_paper_selection(self):
        """
        Goto MyhomePrint_OptionsPaperSelection from MyhomePrint_Options
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_myhome_print_options_paper_size(self):
        """
        Go to MyhomePrint_OptionsPaperSize from SBPrint_OptionsPaperSelection screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_paper_size_options(self, quality_options="A4(210x297mm)"):
        """
        Set paper size
        @param quality_options:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_print_margins_options(self):
        """
        Get print margins option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_print_margins_options(self, net, print_margins_options="clip_from_contents"):
        """
        Set print margins option
        @param net:
        @param print_margins_options:str -> clip_from_contents/add_to_contents/oversize
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_myhome_print_options_print_margins(self, net, print_margins=None):
        """
        Check spec on Print Margins in Print My home option
        @param net:
        @param print_margins:str -> clip_from_contents/add_to_contents/oversize
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_output_scale_options(self):
        """
        Get output scale option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_output_scale_options(self, net, configuration, output_scale_options="none", detail_option=None):
        """
        Set print output scale option
        @param net:
        @param output_scale_options:str -> none/custom/loaded_paper/standard_sizes
        @param detail_option:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_myhome_print_options_output_scale(self, net, output_scale=None):
        """
        Check spec on Output Scale in print My home option
        @param net:
        @param output_scale:str -> none/...
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_print_from_myhome_not_configuration_view(self, net):
        """
        Check Print from My home not configuration view.
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_print_from_myhome_not_configuration_ok_button(self):
        """
        Select Print from My home not configuration ok button
        @param:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_print_no_file_found(self, net):
        """
        Check spec MyhomePrint_NoFileFound
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_current_print_job_by_click_cancel_button(self):
        """
        Click cancel button during printing process
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_printing_localized_files(self, file_name_list=None, file_name=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_print_file_or_folder_by_property_text(self, file_name= None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def go_back_to_print_from_options(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def go_back_to_options_from_paper_selection(self):
         raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_back_button_from_folder_view(self, screen_id, landing_view, index):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_load_paper_error_view(self):
        """
        Wait for load paper error view
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_load_paper_error_view(self):
        """
        Click ok button in load paper error view
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_media_mismatch_type_view(self):
        """
        Wait for media mismatch type view
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_media_mismatch_type_view(self):
        """
        Click ok button in media mismatch type view
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_media_mismatch_size_view(self):
        """
        Wait for media mismatch size view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_folder_name_in_myhome_folder_list_screen(self, folder_name):
        """
        Check folder name on printMyhomeFolderListView screen.
        @param folder_name:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_media_mismatch_size_view(self, tray):
        """
        Click ok button in media mismatch size view
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_sort_filter_search_options_menu(self):
        """
        Go to sort filter search options menu.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_sort_filter_search_option(self, option:str):
        """
        Select corresponding option
        @param:option sort/filter/search
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_specific_filter_option(self, option:str):
        """
        Select corresponding option
        @param:option all_file_types/jpeg/png/tiff/pdf/ppt/doc/ps
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_save_button_on_filter_screen(self):
        """
        Click save button in filter screen.
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_file_names_in_folder_list_view(self, expected_file_list):
        """
        Check expect files shows in folder list view screen.
        @param:expected_file_list: 
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_search_result_number_in_folder_list_view(self, expected_file_list):
        """
        Check Search Result numbers shows in folder list view screen.
        @param:expected_file_list: 
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_search_text_in_search_screen(self, search_text):
        """
        Input search text in search screen.
        @param:search_text: str
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_search_button_in_search_screen(self):
        """
        Click search button in search screen.
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_connecting_network_screen(self):
        """
        wait for connecting network screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_specific_sort_option(self, option:str):
        """
        Select sort option
        @param:option AtoZ/ZtoA/OldToNew/NewToOld
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_save_button_on_sort_screen(self):
        """
        Click save button in sort screen.
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_sorted_file_name_list(self, expect_all_file_list):
        """
        Get file name list sorted by y coordinate from UI.
        @param:expect_all_file_list: 
        @return:file_name_list
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_print_status_toast(self, net, message: str = "complete", timeout=60, specific_str_checked=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, starting /printing /print complete/print canceled
              timeout
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_print_status(self, net, job, message: str = "complete", timeout=60, specific_str_checked=False):
        """
        Purpose: Wait for the given toast/modal message to appear in screen and success if given toast/modal appears
        Args: message: str, starting /printing /print complete/print canceled
              timeout
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_quickset(self, quick_name):
        """
        Purpose: select quickset from detail panel
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_selected_quickset(self, quick_name):
        """
        Purpose: check quickset is selected
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)