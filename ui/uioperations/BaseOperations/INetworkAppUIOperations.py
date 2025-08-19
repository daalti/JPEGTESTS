#########################################################################################
# @file      INetworkAppProSelectUIOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      20-10-2020
# @brief     Interface for all the Network UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class INetworkAppUIOperations(object):


    def goto_ethernet_view_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ethernet_ipv4(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_network_proxy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_ipv4(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_network_ipv6(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_hostname(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_bonjour_name(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ethernet_ipv6(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_ethernet_link_speed(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ble(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_report_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_bonjour_name(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_hostname(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ble_on(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ble_off(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ble_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)     

    def set_ipv6(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_link_speed_link100half(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_link_speed_link100full(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_link_speed_automatic(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_link_speed_link10full(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_link_speed_link10half(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_link_speed_link1000full(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_network_report_config(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_network_report_security(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ipv6_no_on_warning_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ipv6_yes_on_warning_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_default_IPV4_state(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_default_IPV6_state(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_default_ble_state(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_default_proxy(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_default_ipv6_state(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_default_ipv4_config_method(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ethernet_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_hostname_bonjour_ipv6_from_networksetting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_hostname_bonjour_ipv6_from_ethernetsetting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def sign_in_cleanup(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_sign_in(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_on_ipv4_config_method(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_manual_ip_content(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)      
    
    def set_default_ipv4_config_method(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ipv4_config_method_autoip(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_ui_config_method_autoip(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_manual_config_method(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_ipv4_config_method_to_manual(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_no_at_suggest_manual_config(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_suggested_ip_at_manual_config(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_ui_config_method_manual(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_on_dns_config_method(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_primary_dns_textfield():
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_hostname_confirmation_dialog():
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_bonjour_name_confirmation_dialog():
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)






