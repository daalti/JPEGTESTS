#########################################################################################
# @file      IFolderWidgetWorkflowUIOperations.py
# @author    Sundeep Kishan (sundeep.kishan@hp.com)
# @date      Dec 20, 2022
# @brief     Interface for all the Sign In UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class IFolderWidgetWorkflowUIOperations(object):
    def click_on_folder_widget(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_to_Folder_widget(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def check_for_folder_widget_ana_sign_in_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_mainMenu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_default_folder_not_configured_pop_up(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_default_folder_display_name_on_widget(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_for_homescreen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def scan_app_permissions_setup(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def configure_default_folder_to_not_set(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def configure_default_folder_with_specify_folder_option(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def configure_default_folder_with_specify_contact_option(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_displayname_string(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_landingview_click_done_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_scan_status_modal(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_widget(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ldap_sign_in_config(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ldap_sign_in(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_default_folder_widget_options_and_value(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_folder_widget(self):
        '''
        Clicking folder widget Item on Folder widget Home screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_start_button_on_folder_widget(self):
        '''
        Clicking start button on Folder widget Home screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_default_folder_widget_options_and_default_value(self, net, option):
        """
        Check default folder options and values on folder widget
        @param: option: default folder option on folder widget, "color_mode"/"content_type"/"resolution"/"file_type"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_option_button_on_folder_widget(self):
        '''
        Clicking option button on Folder widget Home screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
