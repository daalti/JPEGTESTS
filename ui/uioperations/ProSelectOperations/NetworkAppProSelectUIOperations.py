#########################################################################################
# @file      NetworkAppProSelectUIOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      15-10-2020
# @brief     Implementation Network UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
from email.policy import default
import  sys
import time
import logging
import pytest
from dunetuf.ui.uioperations.BaseOperations.INetworkAppUIOperations import INetworkAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import ProSelectHybridKeyboardOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.ProSelectOperations.SignInAppProSelectUIOperations import SignInAppProSelectUIOperations

_logger = logging.getLogger(__name__)


class NetworkAppProSelectUIOperations(INetworkAppUIOperations):
    def __init__(self, spice):
        self._spice = spice
        self.proselect_common_operations = ProSelectCommonOperations(self._spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)
        if (self._spice.uitheme == "hybridTheme"):
            self.proselect_keyboard_operations = ProSelectHybridKeyboardOperations(self._spice)
        else:
            self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)
        self.sign_in_app_operations = SignInAppProSelectUIOperations(self._spice)

    def goto_ethernet_view_details(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from ethernet.
        '''
        self.proselect_common_operations.goto_ethernet_menu()
        _logger.info("Entering View Details")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxEthernetDetailsMenuButton")

    def goto_ethernet_ipv4(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from ethernet.
        '''
        self.proselect_common_operations.goto_ethernet_menu()
        _logger.info("Entering IPV4")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxEthernetIPMenuNameValue")
    
    def goto_network_ipv4(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from network.
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Entering ipv4")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxIPv4EnableMenuNameValue")
    
    def goto_network_ipv6(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv6 from network.
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Entering ipv6")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxIPv6EnableMenuNameValue")

    def goto_network_proxy(self):
        '''
        UI should be on home screen before calling this method
        Navigate to proxy from network setting.
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Entering Proxy")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxProxyMenuNameValue")

    def set_network_proxy_server_name(self,new_proxy_server_name,updated_proxy_server_name):
        self.proselect_common_operations.goto_item("#ProxyStatusButton")
        ONbtn = self._spice.wait_for("#onRadioButton")
        ONbtn.mouse_wheel(0,0)
        ONbtn.mouse_click()
        logging.info("clicking the ON proxy menu button")

        self.proselect_common_operations.goto_item("#proxyServerButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(new_proxy_server_name)
        logging.info("Validating the old text in the dialer")
        assert self._spice.query_item("#proxyServerButton #SpiceButton")["text"] == new_proxy_server_name
        self.proselect_common_operations.goto_item("#proxyServerButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(updated_proxy_server_name)

    def set_network_proxy_port_number(self,new_proxy_number,updated_proxy_number):
        self.proselect_common_operations.goto_item("#portButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(new_proxy_number)
        logging.info("Validating the old text in the dialer")
        assert self._spice.query_item("#portButton #SpiceButton")["text"] == new_proxy_number
        self.proselect_common_operations.goto_item("#portButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(updated_proxy_number)
        self.proselect_common_operations.goto_item("#applyButton")
        OKbtn = self._spice.wait_for("#MessageLayout #OK")
        OKbtn.mouse_wheel(180,180)
        OKbtn.mouse_wheel(180,180)
        OKbtn.mouse_wheel(180,180)
        OKbtn.mouse_wheel(180,180)
        OKbtn.mouse_click()

    def set_network_proxy_user_name(self,new_proxy_user_name,updated_proxy_user_name):
        self.proselect_common_operations.goto_item("#ProxyStatusButton")
        ONbtn = self._spice.wait_for("#onRadioButton")
        ONbtn.mouse_wheel(0,0)
        ONbtn.mouse_click()
        logging.info("clicking the ON Authentication menu button")
        aythtbtn = self._spice.wait_for("#authenticationButton")
        aythtbtn.mouse_wheel(180,180)
        aythtbtn.mouse_wheel(180,180)
        aythtbtn.mouse_wheel(180,180)
        aythtbtn.mouse_wheel(180,180)
        logging.info("clicking the proxy user name button")
        aythtbtn.mouse_click()
        aythtbtn.mouse_wheel(180,180)
        aythtbtn.mouse_click()
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(new_proxy_user_name)
        self.home_menu_dial_operations.menu_navigation(self._spice,"#MessageLayout","#CancelButton")
        assert self._spice.query_item("#TextInputArea")["inputText"] == new_proxy_user_name
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(updated_proxy_user_name)
        confirmbtn = self._spice.wait_for("#MessageLayout #ConfirmButton")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        okaybtn = self._spice.wait_for("#OK")
        okaybtn.mouse_wheel(180,180)
        okaybtn.mouse_click()

    def check_generic_confirmation_screen(self):
        aythtbtn = self._spice.wait_for("#ProxyButton")
        aythtbtn.mouse_click()
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        self.proselect_common_operations.goto_item("#CancelButton")
        assert self._spice.query_item("#spiceKeyboardView")
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        exitbtn = self._spice.wait_for("#ExitButton")
        exitbtn.mouse_wheel(180,180)
        exitbtn.mouse_wheel(180,180)
        exitbtn.mouse_click()
        assert self._spice.wait_for("#ProxyButton")
        aythtbtn.mouse_click()
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        assert self._spice.wait_for("#ProxyButton")

    def get_default_proxy(self, net):
        '''
        Method to get default proxy settings. UI should be on Network app before calling this method.
        '''
        current_screen = self._spice.wait_for('#ProxyView')
        time.sleep(1)
        statusButtonText = self._spice.query_item("#ProxyStatusButton SpiceText")["text"]
        if statusButtonText == LocalizationHelper.get_string_translation(net, 'cOn'):
            defaultProxy = "true"
        else:
            defaultProxy = "false"
        return defaultProxy

    def get_default_IPV4_state(self):
        '''
        Method to get IPv4 default state. UI should be on IPV4 enable disable view before calling this method.
        '''
        current_screen = self._spice.wait_for('#ipv4EnableDisableView')
        time.sleep(1)
        default_ipv4_state = self._spice.query_item("#onButton")["checked"]
        logging.info("IPV4 default state : %s" , default_ipv4_state)
        if default_ipv4_state :
            default_ipv4_state = "true"
        else:
            default_ipv4_state = "false"
        return default_ipv4_state

    def get_default_IPV6_state(self):
        '''
        Method to get IPv6 default state. UI should be on IPV6 enable disable view before calling this method.
        '''
        current_screen = self._spice.wait_for('#ipv6EnableDisableView')
        time.sleep(1)
        default_ipv6_state = self._spice.query_item("#onButton")["checked"]
        logging.info("IPV6 default state : %s" , default_ipv6_state)
        if default_ipv6_state :
            default_ipv6_state = "true"
        else:
            default_ipv6_state = "false"
        return default_ipv6_state

    def get_default_ble_state(self):
        '''
        Method to get ble default state. UI should be on Network on before calling this method.
        '''
        current_screen = self._spice.wait_for('#bleView')
        time.sleep(1)
        default_ble_state = self._spice.query_item("#onRadioButton")["checked"]
        logging.info("Default BLE state : %s", default_ble_state)
        if default_ble_state :
            default_ble_state = "true"
        else:
            default_ble_state = "false"
        return default_ble_state

    def get_default_config_method(self):
        '''
        Method to get default config method state. UI should be on Network on before calling this method.
        '''
        self.proselect_common_operations.goto_sub_menu("#IPV4View","#DHCP")
        time.sleep(2)
        current_screen = self._spice.wait_for('#IPV4ConfigView')
        time.sleep(1)
        default_config_state = self._spice.query_item("#DHCP")["enabled"]
        logging.info("Get default config method state : %s", default_config_state)
        current_button = self._spice.wait_for("#DHCP")
        return default_config_state

    def get_default_ipv6_state(self):
        '''
        Method to get the default ipv6 status.
        '''
        current_screen = self._spice.wait_for('#IPV6ToggleView')
        time.sleep(1)
        default_ble_state = self._spice.query_item("#IPV6ToggleViewSwitch")["enabled"]
        logging.info("Default BLE state : %s", default_ble_state)
        current_button = self._spice.wait_for("#IPV6ToggleViewSwitch")
        return default_ble_state
       
    def goto_hostname(self):
        '''
        UI should on home screen before calling this method
        goto network hostname from network settings
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Go to HostName")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxHostNameMenuNameValue")

    def goto_bonjour_name(self):
        '''
        UI should be on home screen before calling this method
        goto network Bonjour from network settings
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Go to Bonjour name")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxBonjourNameMenuNameValue")

    def goto_ethernet_ipv6(self):
        '''
        UI should on home screen before calling this method
        Navigate to ipv6 from ethernet
        '''
        self.proselect_common_operations.goto_ethernet_menu()
        _logger.info("Entering IPV6")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxEthernetIPV6MenuButton")

    def goto_ethernet_link_speed(self):
        '''
        UI should be on home screen before calling this method
        Navigate to link speed from ethernet
        '''
        self.proselect_common_operations.goto_ethernet_menu()
        _logger.info("Entering link speed")
        time.sleep(2)
        self.proselect_common_operations.goto_item("#cnxLinkSpeedMenuButton")

    def goto_ble(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Bluetooth low energy from network settings
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Entering ble")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxBLEMenuButton")

    def goto_network_report_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Network Report from network settings
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.info("Entering Network Report")
        time.sleep(5)
        self.proselect_common_operations.goto_item("#cnxNwReportsMenuButton")

    def set_bonjour_name(self, bonjour_name):
        '''
        Method to set bonjour name on the UI
        '''
        time.sleep(5)
        # Click ok on warning 
        current_button = self._spice.wait_for('#MessageLayout')
        current_button.mouse_click()
        time.sleep(5)
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(bonjour_name)
        time.sleep(2)
        # Confirm Bonjour name change
        ok_button = self._spice.wait_for('#MessageLayout')
        ok_button.mouse_click()
        time.sleep(2)
        self._spice.goto_homescreen()

    def set_bonjour_name_confirmation_dialog(self, update_bonjor_name):
        '''
        Method to set bonjour name on the UI
        '''
        # Click ok on warning 
        bonjour_name = 'Test Bonjour Name'
        self.goto_bonjour_name()
        current_button = self._spice.wait_for('#MessageLayout')
        current_button.mouse_click()
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(bonjour_name)
        self.home_menu_dial_operations.menu_navigation(self._spice,"#MessageLayout","#CancelButton")
        assert self._spice.wait_for("#TextInputArea")["inputText"] == bonjour_name
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(update_bonjor_name)
        confirmbtn = self._spice.wait_for('#MessageLayout')
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert self._spice.wait_for("#cnxBonjourNameButton #SpiceButton")["text"] == update_bonjor_name

    def set_hostname(self, host_name):
        '''
        Method to set hostname on the UI
        '''
        time.sleep(5)
        self.proselect_keyboard_operations.keyboard_clear_text()
        time.sleep(1)
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(host_name)
        time.sleep(2)
        self._spice.goto_homescreen()

    def set_hostname_confirmation_dialog(self, update_host_name):
        '''
        Method to set hostname on the UI
        '''
        # Click ok on warning
        self.goto_hostname()
        current_button = self._spice.wait_for('#MessageLayout')
        current_button.mouse_click()
        time.sleep(2)

        self.proselect_keyboard_operations.keyboard_clear_text()

        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(update_host_name)

        if (self._spice.uitheme == "hybridTheme"):
            self.proselect_keyboard_operations.keyboard_press_icon("#SpiceKeyBoardbutton_en", return_home = False)
        else:
            confirmbtn = self._spice.wait_for('#MessageLayout #ConfirmButton')
            confirmbtn.mouse_wheel(180,180)
            confirmbtn.mouse_click()
            time.sleep(2)

        assert self._spice.wait_for("#cnxHostNameButton #SpiceButton")["text"] == update_host_name

        if (self._spice.uitheme == "hybridTheme"):
            self.proselect_keyboard_operations.reset()

    def set_ble_on(self):
        '''
        Method to enable ble from ui
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#bleView", "#onRadioButton")

    def set_ble_off(self):
        '''
        Method to disbale ble from ui
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#bleView", "#offRadioButton")
  
    def click_ble_button(self):
        self.proselect_common_operations.goto_item("#cnxBLEMenuButton")
        time.sleep(2)

    def set_ipv4(self):
        '''
        Method to set IPv4
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV4View","#IPV4", False)

    def set_config_method_autoip(self):
        '''
        Method to navigate to config method and set manual
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV4ConfigView","#Auto IP")
        self._spice.goto_homescreen()

    def set_config_method_manual(self):
        '''
        Method to navigate to config method and set manual
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV4ConfigView","#Manual")
        self._spice.goto_homescreen()

    def set_config_method_dhcp(self):
        '''
        Method to navigate to config method and set dhcp
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV4ConfigView","#DHCP")

    def set_ipv6(self):
        '''
        Method to enable ipv6.
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV6ToggleView","#IPV6ToggleViewSwitch")

    def set_ipv6_no_on_warning_message(self):
        '''
        Method to click No on ipv6 warning message
        '''
        time.sleep(2)
        self.proselect_common_operations.goto_sub_menu("#IPV6WarningMessageView","#noButton")

    def set_ipv6_yes_on_warning_message(self):
        '''
        Method to click Yes on ipv6 warning message
        '''
        self.proselect_common_operations.goto_sub_menu("#IPV6WarningMessageView","#yesButton")
        time.sleep(6)

    def set_linkspeed(self, workFlowObjectName, proSlectObjectName):
        '''
        Method to set enable link speed as link100half
        '''
        self.proselect_common_operations.goto_sub_menu("#RadioButtonLinkSpeedView",proSlectObjectName)
        time.sleep(5)
        self._spice.wait_for("#MenuListLayout", timeout = 10)

    def set_network_report_config(self):
        '''
        Method to set config report
        '''
        time.sleep(5)
        self.proselect_common_operations.goto_sub_menu("#networkReportView","#networkReportButton")

    def set_network_report_security(self):
        '''
        Method to set security report
        '''
        time.sleep(5)
        self.proselect_common_operations.goto_sub_menu("#networkReportView","#securityReportButton")
    
    def goto_sign_in(self, action:str):
        '''
        UI should be on home screen before calling this method
        Navigate to sign in

        Args:
            action: either "Sign In" or "Sign Out"
        ''' 
        self.sign_in_app_operations.goto_sign_in_app(action)
        time.sleep(5)
        #self.sign_in_app_operations.select_sign_in_method("admin", "admin")
        self.sign_in_app_operations.enter_creds(True, "12345678", None)
        time.sleep(5)

    def sign_in_cleanup(self):
        """
        Method to clear sign-in.
        """
        self.sign_in_app_operations.cleanup("admin", "success")
        time.sleep(5)

    def push_session_button_click(self, button, screenId):
        self._spice.wait_for("#pushButtonStatus")
        self.proselect_common_operations.goto_item(button,screenId)
        time.sleep(2)
        self._spice.wait_for("#HomeScreenView")
        
    def goto_network_security(self):
        '''
        Method used to navigate inside security menu.
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        self._spice.wait_for("#MenuListnetworkSettings")
        self.proselect_common_operations.goto_item("#networkSecuritySettingsMenuButton")
        self._spice.wait_for("#MenuListnetworkSecuritySettings")
       
    def goto_announcement_agent(self):
        '''
        Method to navigate to announcement agent and click on that.
        '''
        self.proselect_common_operations.goto_item("#cnxAnnounceAgentMenuSwitch")

    def goto_disable_firewall(self,isFirewallEnabled):
        '''
        Method to disable the firewall
        '''
        self.proselect_common_operations.goto_item("#cnxFirewallMenuButton")
        if isFirewallEnabled:
            self.proselect_common_operations.goto_sub_menu("#DisableFirewallWarning","#Continue")
            current_screen = self._spice.wait_for("#DisableFirewallSuccessfully",timeout = 15)
            current_screen.mouse_click()
        else:
            self.proselect_common_operations.goto_sub_menu("#FirewallAlreadyDisabled","#Continue")
        self._spice.wait_for("#MenuListnetworkSecuritySettings")


    def goto_reset_authentication(self):
        '''
        Method to reset authentication 802X1.
        '''
        self.proselect_common_operations.goto_item("#cnxReset802_1xMenuButton")
        self.proselect_common_operations.goto_item("#Yes")
        self._spice.wait_for("#MenuListnetworkSecuritySettings",timeout = 15)

    def goto_reset_security(self):
        '''
        Method to reset the security.
        '''
        self.proselect_common_operations.goto_item("#cnxResetSecurityMenuButton")
        time.sleep(2)
        reset_area = self._spice.wait_for("#MenuListnetworkSecuritySettings")
        for _ in range(4):
            reset_area.mouse_wheel(180, 180)
        time.sleep(2)
        self.proselect_common_operations.goto_item("#Reset","#SecurityResetState")
        logging.info("Clicked on reset")
        time.sleep(3)
        self.proselect_common_operations.goto_sub_menu("#SecurityResetSuccessful","#OK")

    def has_lock_icon(self):
        """
        Starting from Home Screen
        """
        self.home_menu_dial_operations.goto_menu_settings(self._spice)
        network_settings_lock_icon_id = "#networkSettingsMenuButton #ContentItem SpiceImage"
        current_screen = self._spice.wait_for(network_settings_lock_icon_id)
        current_screen.mouse_wheel(180, 180)
        lock_icon = self._spice.wait_for(network_settings_lock_icon_id, 15)

        return lock_icon["width"] > 0

    def click_on_ipv4_config_method(self, cdm_config):
        '''
        UI should be on homescreen before calling this method 
        This method navigates to ethernet >ipv4 settings and clicks on config method option
        '''
        self.goto_ethernet_ipv4()
        logging.info("#At config method selection view")
        if(cdm_config == 'dhcpv4'):
            current_config_method = "#DHCP"
        elif(cdm_config == 'manual'):
            current_config_method = "#Manual"
        elif(cdm_config == 'autoip'):
            current_config_method = "#Auto IP"
        self.proselect_common_operations.goto_item(current_config_method , "#IPV4View")

    def select_manual_config_method(self):
        '''Method to set config method to manual'''
        manualButton = self._spice.query_item("#manualButton")
        manualButton.mouse_click()

    def check_manual_ip_content(self):
        ip_address_text = self._spice.wait_for("#ip")["buttonText"]
        print (ip_address_text)
        assert len(ip_address_text) != 0, 'IPAddress doesnt exist'

        subnet_mask_text = self._spice.wait_for("#subnet")["buttonText"]
        print (subnet_mask_text)
        assert len(subnet_mask_text) != 0, 'SubnetMask doesnt exist'

        gateway_text = self._spice.wait_for("#gateway")["buttonText"]
        print (gateway_text)
        assert len(gateway_text) != 0, 'Gateway doesnt exist'
