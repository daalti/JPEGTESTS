import time
import logging

from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MenuAppWorkflowUIXLOperations import MenuAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations



class NetworkAppWorkflowUIXLOperations(NetworkAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.home_menu_workflow_xl_operations = MenuAppWorkflowUIXLOperations(self._spice)
        self.sign_in_app_operations = SignInAppWorkflowUIOperations(self._spice)
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self._spice)

    def goto_settings_menu(self):
        '''Go to settings menu'''
        self.home_menu_workflow_xl_operations.goto_menu_settings(self._spice)

    def goto_ethernet_menu(self):
        '''
        Go to ethernet menu
        '''
        self.goto_network_settings_menu()
        time.sleep(4)
        self.workflow_common_operations.goto_item("#cnxEthernetSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        
    def set_hostname(self, hostname):
        '''Method to set hostname on the UI'''
        self._spice.wait_for("#hostNameTextField")
        time.sleep(2)
        logging.info("Set New Hostname!")
        self.workflow_keyboard_operations.keyboard_set_text_with_out_dial_action(hostname, "#hostNameTextField")
        time.sleep(3)
        self._spice.wait_for("#hostnameChangedSuccessfullyViewverticalLayout")
        time.sleep(2)
        logging.info("Confirm New Hostname Name!!!!!!!!!")
        confirm_button = self._spice.query_item('#hostnameChangedSuccessfullyViewFooter #okButton')
        confirm_button.mouse_click()
        time.sleep(2)
        self._spice.wait_for("#networkSettingsMenuList")
        time.sleep(2)
        self._spice.goto_homescreen()
        time.sleep(2)
        
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
        configuration = self._spice.wait_for("#ipv4SettingsEthernetRow")
        self.set_config_method("#autoip")

    def set_config_method_manual(self):
        '''Method to navigate to config method and set manual'''
        configuration = self._spice.wait_for("#ipv4SettingsEthernetRow")
        self.set_config_method("#manual")

    def set_config_method(self, method):
        # Click in comboBoxList
        config_combobox = self._spice.wait_for("#ipv4ConfigDelegate #SettingsSpiceComboBox")
        config_combobox.mouse_click()

        # Click in the option
        option = self._spice.wait_for(method)
        option.mouse_click()
        if method == "#manual":
            manual_btn = self._spice.wait_for("#manualButton")
            manual_btn.mouse_click()
            time.sleep(1)
            apply_btn = self._spice.wait_for("#manualIPConfigurationApply")
            apply_btn.mouse_click()

    def set_config_method_dhcp(self):
        '''
        Method to navigate to config method and set dhcp
        '''
        configuration = self._spice.wait_for("#ipv4SettingsEthernetRow")
        self.set_config_method("#dhcpv4")

    def goto_network_proxy(self):
        '''
        UI should be on home screen before calling this method
        Navigate to proxy from network setting.
        '''
        self.goto_network_settings_menu()
        logging.info("Entering Proxy")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#proxyConfigView", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
       

    def get_default_proxy(self, net):
        '''
        Method to get default proxy settings. UI should be on Network app before calling this method.
        '''
        self._spice.wait_for("#proxyConfigView")
        time.sleep(2)
        proxy_button = self._spice.query_item("#proxyConfigView_2infoBlockRow")
        time.sleep(2)
        proxy_button.mouse_click()
        time.sleep(3)
        self._spice.wait_for("#proxySettingView")
        time.sleep(2)
        default_state = self._spice.query_item("#enabled")["checked"]
        if default_state:
            default_state = "true"
        else:
            default_state = "false"
        return default_state
