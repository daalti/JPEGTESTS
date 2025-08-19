import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WiFiAppWorkflowUICommonOperations import WifiAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations



class WifiAppWorkflowUILOperations(WifiAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.home_menu_workflow_ui_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self._spice)
        self.network_menu_workflow_ui_operations = NetworkAppWorkflowUICommonOperations(self._spice)

    def goto_select_ssid_name_screen(self):
        '''Click on SSID at SSID list'''
        if self._spice.is_HomeScreen():
            self.goto_wifi_setup_wizard_menu()

        logging.info("At select network name screen")
        try:
            logging.info("Already logged in screen")
            self.wait_for("#connectionAlreadySetupView #connectionAlreadySetupHeaderVar1HeaderView")
            logging.info("Click on yes button")
            yes_button = self.query_item("#connectionAlreadySetupFooter #yesButton")
            yes_button.mouse_click()
        except:
            logging.info("Wifi is not already connected")
        time.sleep(2)
        self.workflow_common_operations.goto_item_navigation("#ssidCard_testSecureAP", "#connectivity_selectNetworkName")
        time.sleep(2)

    def goto_wifi_info_connectivity_wifi(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Wifi option from connectivity menu
        '''
        self.goto_wifi_info_connectivity()
        time.sleep(1)
        #click on wireless menu
        logging.info("At Connectivity Screen")
        time.sleep(1)
        self.workflow_common_operations.goto_item_navigation("#wifiCardInTab", "#connectivityTabLayout")
        time.sleep(1)

    def goto_info_wifi_settings_button(self):
        '''
        UI should be on wifi info connectivity screen before calling this method
        Navigate to print details option from wifi info connectivity menu
        '''
        logging.info("At wifi expanded screen")
        self.goto_wifi_in_connectivity_tab()
        self.workflow_common_operations.goto_item_navigation("#wifiCardInTab", "#connectivityTabLayout")
        time.sleep(1)
        settingsButton = self._spice.query_item("#wifiSettingsButton")
        settingsButton.mouse_click()
        time.sleep(2)

    def goto_wifi_info_connectivity_eth(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ethernet option from connectivity menu
        '''
        self.goto_wifi_info_connectivity()
        time.sleep(1)
        logging.info("At Connectivity Screen")
        self.workflow_common_operations.goto_item_navigation("#ethernetCardInTab", "#connectivityTabLayout")
        time.sleep(2)

        self._spice.wait_for("#ethernetCardContentExpanded")
        self.goto_close_button_on_connectivity_tab()

    def goto_info_eth_settings_button(self):
        '''
        UI should be on eth info connectivity screen before calling this method
        Navigate to print details option from eth info connectivity menu
        '''
        self.workflow_common_operations.goto_item_navigation("#ethernetCardInTab", "#connectivityTabLayout")
        logging.info("At eth expanded screen")
        self._spice.wait_for("#ethernetCardContentExpanded")
        time.sleep(1)
        settingsButton = self._spice.query_item("#ethernetSettingsButton")
        settingsButton.mouse_click()
        time.sleep(1)
        self.goto_close_button_on_connectivity_tab()

    def set_wifi_state(self, default_state):
        ''' Method to enable or disable wifi from ui'''
        self._spice.wait_for('#wifiSwitch')
        default_wifi_state = self._spice.query_item("#wifiSwitch")["checked"]
        if default_state != default_wifi_state:
            wifi_switch_button = self._spice.query_item("#wifiSwitch")
            wifi_switch_button_height = wifi_switch_button["height"]/2
            wifi_switch_button_width = wifi_switch_button["width"]/2
            wifi_switch_button.mouse_click(wifi_switch_button_width,wifi_switch_button_height)