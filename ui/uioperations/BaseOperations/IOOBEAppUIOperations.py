import sys


class IOOBEAppUIOperations(object):

    def power_cycle(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def enable_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def disable_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_language_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_language_confirmation_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_country_screen(self, spice, udw, language):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_network_settings_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_proxy_settings_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_retrieve_code_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def cancel_retrieving_code(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_printer_pin_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_handsoff_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_network_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_proxy_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_date_time_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_auto_printer_update_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_get_software_screen(self, spice):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_thank_you_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def verify_oobe_language_cancel(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def verify_oobe_language_country(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_connect_to_internet_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_retrieve_pairing_code_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_pairing_code_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_skip_pairing_code(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def get_pairing_code(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_home_from_thankyou_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_pairing_printer_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_disable_ethernet(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_complete_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_connection_method_screen_select_wireless(self, spice, oobe, udw):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_connection_method_screen_select_eth(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_skip_proxy_settings_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def skip_connect_to_internet_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_set_date_time_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_oobe_connection_method_screen_and_set_wifi(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_home_from_proxy_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def firmware_update_config_page(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    def select_firmware_update_option(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    def get_thank_you_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def enter_admin_pin(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def goto_edit_admin_pin(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_thankyou_screen_from_success_adminpin(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_thankyou_screen_from_adminpin_prompt(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def retry_admin_pin(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def goto_complete_oobe_once(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def goto_oobe_connection_method_screen(self, spice, oobe, udw):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def goto_oobe_proxy_screen(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def set_proxy_server_in_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def set_proxy_port_in_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def set_proxy_username_and_password_in_oobe(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)
    
    def configure_proxy_on_oobe_setup(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_more_country_list_screen(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def select_country_from_more_country_list_screen(self, spice, cdm, udw):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def goto_oobe_ipv4_screen(self, spice, udw, option):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def validate_ip_config_view(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def select_manual_ip_option(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

    def validate_manual_ip_view(self):
        raise NotImplementedError('Unimplemented method %s' %
                                  sys._getframe().f_code.co_name)

