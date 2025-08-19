import logging
import sys


class IQuicksetsAppUIOperations(object):

    def goto_copyapp_landing_view_from_home_copyapp(self):
        """
        Printer Home screen -> Copy App -> Corresponding copy item
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copyapp_landing_view_from_menu_copyapp(self):
        """
        Printer Home screen -> Menu -> Copy App -> Corresponding copy item
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_scanapp_landing_view_from_home_scanapp(self, quickset_type, quickset_name=None, profile_name=None, pin=None, check_default_quickset_is_selected=False):
        """
        Printer Home screen -> Scan App -> Corresponding scan app
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @param profile_name: should provide email profile name when qs type is emaila and server type is user defined server
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_scanapp_landing_view_from_menu_scanapp(self, quickset_type, quickset_name=None, profile_name=None, pin=None, check_default_quickset_is_selected=False):
        """
        Printer Home screen -> Menu -> Scan App -> Corresponding scan app
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @param profile_name: should provide email profile name when qs type is emaila and server type is user defined server
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_quicksetapp_landing_view(self, quickset_type):
        """
        Printer Home screen -> Menu -> Quicksets app -> Corresponding app
        @param quickset_type: email/sharepoint/usb/folder/copy
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_quickset_selected(self, quickset_name, quickset_type):
        """
        To check if quickset is selectded or not
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_quickset_from_app_landing_view(self, quickset_name, quickset_type,  start_option="user presses start", ana_sign_in_payload=None, pin=None):
        """
        Select quickset by name at scan app landing view
        @param quickset_name: 
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_viewall_menu_from_app_landing_view(self, quickset_type):
        """
        Click view all button from corresponding scanapp landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def select_quickset_from_app_viewall_menu(self, quickset_name, quickset_type, pin=None, index=0):
        """
        Select quickset by name at scan view all menu
        @param quickset_name: 
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_quickset_from_menu_quicksetapp(self, quickset_name, quickset_type, start_option="user presses start", ana_sign_in_payload=None, pin=None, already_on_landing_view=False):
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def compare_ui_copy_scan_settings_with_created_quickset(self, net, quickset_type, payload, profile_name=None, pin=None, already_on_setting_screen=False,job=None):
        """
        Compare ui scan settings with created quickset
        @param quickset_type: email/sharepoint/usb/folder/copy
        @param payload: please refer to comment from function "edit_common_email_quicksets" from QuickSetsApp.py: src/test/dunetuf/dunetuf/ews/pom/quick_sets/QuickSetsApp.py
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin
        @param already_on_setting_screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_common_current_scan_setting(self, net, payload,job=None):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Settings/Options Landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_common_current_copy_setting(self, net, payload):
        """
        This method compares the selected setting string with the expected string from string id
        Args:
            UI should be in Copy/Options Landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def perform_quickset_job_from_home_app(self, net, job, ews_quicksets_app, quickset_type, payload, profile_name=None, pin=None, pages=1, time_out=120, pdf_encryption_code=None, select_from_view_all_menu=False, check_default_quickset_is_selected=False):
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
        @param payload: please refer to comment from function "create_common_quicksets" from quicksets.py: src/test/dunetuf/dunetuf/ews/quicksets.py
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled 
        @param select_from_view_all_menu: select quickset from view all menu
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def perform_quickset_job_from_menu_app(self,net, job, ews_quicksets_app, quickset_type, payload, profile_name=None, pin=None, pages=1, time_out=120, pdf_encryption_code=None, select_from_view_all_menu=False, check_default_quickset_is_selected=False):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Menu -> Scan/Copy -> Corresponding app - > perform quickset job
        5. Wait for job compele
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to comment from function "create_common_quicksets" from quicksets.py: src/test/dunetuf/dunetuf/ews/quicksets.py
        @param profile_name: should provide email profile name when qs type is email and server type is user defined server
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled
        @param select_from_view_all_menu: select quickset from view all menu 
        @param check_default_quickset_is_selected: to check default is selected on landing view screen when its value is True and will not check if it is False
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def perform_quickset_job_from_menu_quicksetapp(self,net, job, ews_quicksets_app, quickset_type, payload, ana_sign_in_payload=None, pin=None, pages=1, time_out=120, pdf_encryption_code=None):
        """
        Home screen -> Menu -> Quicksets app
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Menu -> Quicksets app -> Corresponding app - > perform quickset job
        5. Wait for job compele
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to comment from function "create_common_quicksets" from quicksets.py: src/test/dunetuf/dunetuf/ews/quicksets.py
        @param ana_sign_in_payload: some printer support sigin feature and should provide authorization when folder/sharepoint sign-in method is "Use credentials of the user currently signed in"
                                    > Please set it to None if you already sign in from Home screen/Don't handle ana sign in with this function
                                    > payload format {"admin":{"password":"12345678"}}/{"printer_user":{"username":"xxxx", "password":"xxx"}}/{"ldap":{"username":"xxxx", "password":"xxx"}}/{"windows":{"username":"xxxx", "password":"xxx"}} 
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def perform_quickset_job_and_check_file_name(self, net, job, ews_quicksets_app, quickset_type, payload, file_name, file_type, prefix_type, suffix_type, custom_prefix_string='', custom_suffix_string='', prefix_username='admin', suffix_username='admin', profile_name=None, pin=None, pages=1, time_out=120):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Home screen -> Menu -> Scan -> Corresponding app - > perform quickset job
        3. Get preview file name from job details, and check file name
        4. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder
        @param payload: mainly set filename info, please refer to comment from function "create_common_quicksets" from quicksets.py: src/test/dunetuf/dunetuf/ews/quicksets.py
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def start_quickset_job(self, quickset_type, click_send=False):
        """
        Click send/copy button in Corresponding app landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_scan_quickset_job_to_complete(self, net, job, quickset_type, pages=1, time_out=120, final_job_status="success", wait_for_landing: bool = True):
        """
        @param quickset_type quickset_type:email/sharepoint/usb/folder
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_scan_file_name(self, final_file_name: str, file_name: str, file_type: str, prefix_type: str, suffix_type: str, custom_prefix_string: str = '', custom_suffix_string: str = '', prefix_username: str = 'admin', suffix_username: str = 'admin'):
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
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def perform_scan_quickset_job_with_changed_setting_from_ui(self, net, job, ews_quicksets_app, quickset_type, payload, changed_scan_option_pyload, profile_name=None, pin=None, pages=1, time_out=120):
        """
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Change the corresponding setting from printer UI
        3. Perform this quickset job
        4. Wait for job finish
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder
        @param payload: please refer to comment from function "create_common_quicksets" from quicksets.py: src/test/dunetuf/dunetuf/ews/quicksets.py
        @param changed_original_size: the original size set from UI
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_app_option_screen(self, quickset_type):
        """
        Goto app option screen from app landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_app_landing_view_from_option_screen(self, quickset_type):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_scan_option_setting(self, payload):
        """
        Change scan option on scan option settting screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def is_landing_expanded(self, quickset_type):
        """
        Return true if app landing screen is expanded, only preview visible in main panel and detail panel with settings is not shown
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name) 
