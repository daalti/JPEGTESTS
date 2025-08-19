import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations



class NetworkAppWorkflowUIXSOperations(NetworkAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.home_menu_workflow_s_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    def goto_settings_menu(self):
        '''Go to settings menu'''
        self.home_menu_workflow_s_operations.goto_menu_settings(self._spice)

    def goto_network_settings_menu(self):
        '''Go to network menu'''
        self._spice.homeMenuUI().goto_menu_settings_network(self._spice)

    def goto_ethernet_menu(self):
        '''
        Go to ethernet menu
        '''
        self.goto_network_settings_menu()
        time.sleep(4)
        self.workflow_common_operations.goto_item("#cnxEthernetSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")

    def set_bonjour_name(self, bonjour_name):
        '''
        Method to set bonjour name on the UI
        '''
        self._spice.wait_for("#bonjourNameTextField")
        time.sleep(2)
        logging.info("Set New Bonjour Name!")
        self.workflow_keyboard_operations.keyboard_set_text_with_out_dial_action(bonjour_name, "#bonjourNameTextField")
        time.sleep(3)
        self._spice.wait_for("#BonjourNameUpdatedSuccessfullyverticalLayout")
        time.sleep(2)
        logging.info("Confirm New Bonjour Name!!!!!!!!!")
        confirm_button = self._spice.query_item('#BonjourNameSuccessfullyFooter #okButton')
        confirm_button.mouse_click()
        time.sleep(2)
        self._spice.wait_for("#networkSettingsMenuList")
        time.sleep(2)
        self._spice.goto_homescreen()
        time.sleep(2)

    def goto_ethernet_ipv4(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from ethernet.
        '''
        self.goto_ethernet_menu()
        logging.info("Entering IPV4")
        time.sleep(5)
        currentScreen = self._spice.wait_for("#cnxEthernetMenuList")
        time.sleep(5)
        row = self._spice.wait_for("#ipv4SettingsEthernetRow")
        row.mouse_click()
        ok_button = self._spice.wait_for("#changingIpWarningOk")
        ok_button.mouse_click()
        
    def get_default_ipv4_state(self):
        '''
        Method to get IPv4 default state. UI should be on IPV4 view before calling this method.
        '''
        time.sleep(1)
        default_ipv4_state = self._spice.query_item("#ipv4SettingsEthernetRow")["enabled"]
        logging.info("IPV4 default state : %s", default_ipv4_state)
        time.sleep(4)
        return default_ipv4_state  
        
    def goto_ethernet_ipv6(self):
        '''
        UI should on home screen before calling this method
        Navigate to ipv6 from ethernet
        '''
        self.goto_ethernet_menu()
        logging.info("Entering IPV6")
        time.sleep(5)
        currentScreen = self._spice.wait_for("#cnxEthernetMenuList")
        currentScreen.mouse_wheel(180, -180)
        time.sleep(5)
        self._spice.query_item("#ipv6SettingsEthernetRow")

    def get_default_config_method(self):
        '''
        Method to get default config method state. UI should be on Network on before calling this method.
        '''
        self.workflow_common_operations.goto_item_navigation("#IPV4View","#DHCP")
        time.sleep(2)
        current_screen = self._spice.wait_for('#IPV4ConfigView')
        time.sleep(1)
        default_config_state = self._spice.query_item("#DHCP")["enabled"]
        logging.info("Get default config method state : %s", default_config_state)
        current_button = self._spice.wait_for("#DHCP")
        return default_config_state

    def set_config_method_autoip(self):
        '''Method to navigate to config method and set manual'''
        time.sleep(2)
        self.workflow_common_operations.goto_item_navigation("#IPV4ConfigView","#Auto IP")
        self._spice.goto_homescreen()

    def set_config_method_manual(self):
        '''Method to navigate to config method and set manual'''
        configuration = self._spice.wait_for("#ipv4SettingsEthernetRow")
        configuration.mouse_click()
        manual_activated = self._spice.wait_for("#manual")["checked"]
        if not manual_activated:
            manual = self._spice.wait_for("#manual")
            manual.mouse_click()
            self._spice.wait_for("#manualIPConfigurationView")
            button_apply = self._spice.wait_for("#manualIPConfigurationApply")
            button_apply.mouse_click()

    def set_config_method_dhcp(self):
        '''
        Method to navigate to config method and set dhcp
        '''
        time.sleep(2)
        self.workflow_common_operations.goto_item_navigation("#IPV4ConfigView","#DHCP")

    def goto_network_proxy(self):
        '''
        UI should be on home screen before calling this method
        Navigate to proxy from network setting.
        '''
        self.goto_network_settings_menu()
        logging.info("Entering Proxy")
        time.sleep(5)
        self._spice.wait_for("#networkSettingsMenuList")
        scroll_vertical = "#networkSettingsMenuListScrollBar"
        time.sleep(1)
        # Scroll to click pn proxy 
        self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(position=0.5, scrollbar_objectname=scroll_vertical)
        time.sleep(1)
        self._spice.wait_for("#proxyConfigView").mouse_click()

    def get_default_proxy(self, net):
        '''
        Method to get default proxy settings. UI should be on Network app before calling this method.
        '''
        time.sleep(3)
        self._spice.wait_for("#proxySettingView")
        time.sleep(2)
        default_state = self._spice.query_item("#enabled")["checked"]
        if default_state:
            default_state = "true"
        else:
            default_state = "false"
        return default_state

    def goto_network_ipv6(self):
        '''This method will navigate to Network Ipv4 option'''
        self.goto_network_settings_menu()
        logging.info("Entering Network Report")
        self.workflow_common_operations.goto_item("#cnxIPv6Enable_WFSettingsSwitch", "#networkSettingsMenuList",select_option= False, scrollbar_objectname="#networkSettingsMenuListScrollBar" )

    def get_IPV4_config(self):
        '''
        Return IPV4 info from IPv4 Settings view.
        Return:
            configuration: string with the IPv4 configuration.
        '''
        self._spice.wait_for("#ipv4View")
        configuration = self._spice.wait_for("#ipv4ConfigBranch")
        configuration.mouse_click()
        config = {}
        config["dhcp"] = bool(self._spice.wait_for("#dhcpv4")["checked"])
        config["auto_ip"] = bool(self._spice.wait_for("#autoip")["checked"])
        config["manual"] = bool(self._spice.wait_for("#manual")["checked"])
        return config
