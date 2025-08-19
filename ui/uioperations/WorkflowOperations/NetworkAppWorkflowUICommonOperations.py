import logging 
import time

from dunetuf.ui.uioperations.BaseOperations.INetworkAppUIOperations import INetworkAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

class NetworkAppWorkflowUICommonOperations(INetworkAppUIOperations):

    def __init__(self,spice):
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self._spice)
        self.sign_in_app_operations = spice.signIn
        
    def goto_settings_menu(self):
        '''Go to settings menu'''
        self._spice.goto_homescreen()
        self.home_menu_dial_operations.goto_menu_settings(self._spice)
        

    def goto_network_settings_menu(self):
        '''Go to network menu'''
        self._spice.homeMenuUI().goto_menu_settings(self._spice)
        self._spice.homeMenuUI().menu_navigation(self._spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_network, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_networkSettings, timeout=15.0)

    def goto_network_settings_menu_locked(self):
        '''Go to network menu'''
        self._spice.homeMenuUI().goto_menu_settings(self._spice)
        self._spice.homeMenuUI().menu_navigation(self._spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_network, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
    
    def goto_hp_cloud_connection_menu(self):
        '''Go to HP Cloud Connection from Settings Menu'''
        self._spice.homeMenuUI().goto_menu_settings(self._spice)
        self._spice.homeMenuUI().menu_navigation(self._spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_cloudConnection, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_cloudConnection, timeout=15.0)

    def goto_ethernet_menu(self):
        '''
        Go to ethernet menu
        '''
        self.goto_network_settings_menu()
        time.sleep(4)
        self.workflow_common_operations.goto_item_navigation("#cnxEthernetSettingsTextImage", "#networkSettingsMenuList")

    def goto_hostname(self):
        '''
        UI should on home screen before calling this method
        goto network hostname from network settings
        '''
        self.goto_network_settings_menu()
        logging.info("Go to HostName")
        time.sleep(2)
        self.workflow_common_operations.goto_item("#cnxHostName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
    
    def goto_ethernet_hostname(self):
        '''
        UI should on home screen before calling this method
        goto ethernet hostname from ethernet menu
        '''
        self.goto_ethernet_menu()
        logging.info("Go to Ethernet HostName")
        time.sleep(2)
        self.workflow_common_operations.goto_item("#cnxEthernetHostNameSettingsTextImage", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")

    def set_hostname_confirmation_dialog(self, new_host_name):
        '''
        Method to set hostname on the UI
        '''
        self.goto_hostname()
        time.sleep(1)
        logging.info("click Hostname!")
        hostNameTextField = self._spice.wait_for("#hostNameTextField")
        hostNameTextField.mouse_click()
        logging.info("Set New Hostname!")
        hostNameTextField.__setitem__('displayText', new_host_name)
        self._spice.wait_for("#enterKey1").mouse_click()
        time.sleep(15)
        self._spice.query_item("#hostNameFooter #hostNameApply").mouse_click()
        self._spice.wait_for("#hostnameChangedSuccessfullyView", timeout=15.0)
        self._spice.query_item('#hostnameChangedSuccessfullyViewFooter #okButton').mouse_click()
        logging.info("Confirm New Hostname Name!!!!!!!!!")
        self.workflow_common_operations.goto_item("#cnxHostName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        assert self._spice.wait_for("#hostNameTextField")["inputText"] == new_host_name

    def goto_bonjour_name(self):
        '''
        UI should be on home screen before calling this method
        goto network Bonjour from network settings
        '''
        self.goto_network_settings_menu()
        logging.info("Go to Bonjour name")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#cnxBonjourName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
    
    def goto_ethernet_bonjour_name(self):
        '''
        UI should be on home screen before calling this method
        goto ethernet Bonjour from ethernet menu
        '''
        self.goto_ethernet_menu()
        logging.info("Go to Ethernet Bonjour name")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#cnxEthernetBonjourNameSettingsTextImage", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
    
    def set_bonjour_name_confirmation_dialog(self, new_bonjour_name):
        '''
        Method to set bonjour name on the UI
        '''
        self.goto_bonjour_name()
        logging.info("click bonjour name!")
        bonjourNameTextField = self._spice.wait_for("#bonjourNameTextField")
        bonjourNameTextField.mouse_click()
        logging.info("Set new bonjour name!")
        bonjourNameTextField.__setitem__('displayText', new_bonjour_name)
        self._spice.wait_for("#enterKey1").mouse_click()
        self._spice.query_item("#bonjourNameFooter #bonjourNameApply").mouse_click()
        self._spice.wait_for("#BonjourNameUpdatedSuccessfully", timeout=15.0)
        self._spice.query_item('#BonjourNameSuccessfullyFooter #okButton').mouse_click()
        logging.info("Confirm new Bonjour Name!!!!!!!!!")
        self.workflow_common_operations.goto_item("#cnxBonjourName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        assert self._spice.wait_for("#bonjourNameTextField")["inputText"] == new_bonjour_name
    
    def goto_ethernet_view_details(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from ethernet.
        '''
        self.goto_ethernet_menu()
        logging.info("Entering View Details")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#ethernetViewDetailDelegate", "#cnxEthernetMenuList")

    def goto_ethernet_link_speed(self):
        '''
        UI should be on home screen before calling this method
        Navigate to link speed from ethernet and click on link speed combo box
        '''
        self.goto_ethernet_menu()
        logging.info("Entering link speed")
        time.sleep(1)
        self.workflow_common_operations.goto_item("#linkSpeedDelegateView", "#cnxEthernetMenuList",select_option=False, scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        linkSpeedComboBox = self._spice.query_item("#cnxLinkSpeed_WFComboBox")
        linkSpeedComboBox.mouse_click()
        time.sleep(1)

    def goto_network_report_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Network Report from network settings
        '''
        self.goto_network_settings_menu()
        logging.info("Entering Network Report")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#cnxNwReports_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")

    # TODO:Currently print is not working, need to update this method
    def set_network_report_config(self):
        '''Method to set config report'''
        time.sleep(5)
        self.workflow_common_operations.goto_item_navigation("#reportNetworkConfigButtonView", "#cnxNwReports_WFMenuList")
        logging.info("Click on Report Print Button")
        print_button = self._spice.query_item('#Print')
        self._spice.validate_button(print_button)
        time.sleep(2)
        print_button.mouse_click()

    def set_network_report_security(self):
        '''Method to set connectivity report'''
        time.sleep(5)
        logging.info("Setting Connectivity Report!")
        self.workflow_common_operations.goto_item_navigation("#reportSecurityButtonView","#cnxNwReports_WFMenuList")
        logging.info("Click on Report Print Button")
        print_button = self._spice.query_item('#Print')
        self._spice.validate_button(print_button)
        time.sleep(2)
        print_button.mouse_click()

    def goto_ethernet_ipv4(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 from ethernet.
        '''
        self.goto_ethernet_menu()
        logging.info("Entering IPV4")
        self.workflow_common_operations.goto_item("#ipv4SettingsEthernetRow", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        self._spice.wait_for("#changingIpWarning",timeout = 10)
        self._spice.wait_for("#AlertFooter")
        okButton = self._spice.wait_for("#changingIpWarningOk")
        okButton.mouse_click()

    def goto_ethernet_ipv6(self):
        '''
        UI should on home screen before calling this method
        Navigate to ipv6 from ethernet
        '''
        self.goto_ethernet_menu()
        logging.info("Entering IPV6")
        self.workflow_common_operations.goto_item("#ipv6SettingsEthernetRow", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        self._spice.wait_for("#changingIpWarning",timeout = 10)
        self._spice.wait_for("#AlertFooter")
        okButton = self._spice.wait_for("#changingIpWarningOk")
        okButton.mouse_click()
        time.sleep(1)
        
    def get_default_ipv6_state(self):
        ''' Method to get the default ipv6 status.'''
        time.sleep(1)
        default_ipv6_state = self._spice.query_item("#ipv6SettingsEthernetRow")["enabled"]
        logging.info("Default ipv6 state : %s", default_ipv6_state)
        return default_ipv6_state

    def goto_network_proxy(self):
        '''
        UI should be on home screen before calling this method
        Navigate to proxy from network setting.
        '''
        self.goto_network_settings_menu()
        logging.info("Entering Proxy")
        time.sleep(5)
        self.workflow_common_operations.goto_item("#cnxProxy_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        
    def get_default_proxy(self, net):
        '''
        Method to get default proxy settings. UI should be on Network app before calling this method.
        '''
        time.sleep(4)
        self._spice.wait_for("#proxyConfigView")
        time.sleep(2)
        proxy_button = self._spice.query_item("#proxyConfigView_2infoBlockRow")
        proxy_button.mouse_click()
        time.sleep(2)
        self._spice.wait_for("#proxySettingView")
        time.sleep(2)

        default_state = self._spice.query_item("#enabled")["checked"]
        if default_state:
            default_state = "true"
        else:
            default_state = "false"
        return default_state

    def goto_ble(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Bluetooth low energy from network settings
        '''
        self.goto_network_settings_menu()
        logging.info("Entering ble")
        time.sleep(5)
        self._spice.wait_for("#networkSettingsMenuList")
        time.sleep(5)
        ble_button = self._spice.query_item("#cnxBLE_WFSettingsTextImage")
        ble_button.mouse_click()

    def get_default_ble_state(self):
        '''
        Method to get ble default state. UI should be on Network on before calling this method.
        '''
        self._spice.wait_for('#BleView')
        time.sleep(1)
        default_ble_state = self._spice.query_item("#BleView")["checked"]
        logging.info("Default BLE state : %s", default_ble_state)
        if default_ble_state:
            default_ble_state = "true"
        else:
            default_ble_state = "false"
        return default_ble_state

    def set_ble_on_off(self, default_state=False):
        ''' Method to enable ble from ui'''
        time.sleep(2)
        self._spice.wait_for('#BleView')
        time.sleep(1)
        default_ble_state = self._spice.query_item("#BleView")["checked"]
        # Enable BLE.
        if default_state != default_ble_state:
            current_button = self._spice.query_item("#BleView")
            time.sleep(1)
            current_button.mouse_click()
    
    def goto_network_ipv4(self):
        '''This method will navigate to Network Ipv4 option'''
        self.goto_network_settings_menu()
        logging.info("Entering Network Report")
        time.sleep(5)
        self.workflow_common_operations.goto_item_navigation("#cnxIPv4Enable_WFMenuSwitch", "#networkSettingsMenuList", select_option= False)
       

    def goto_network_ipv6(self):
        '''This method will navigate to Network Ipv4 option'''
        self.goto_network_settings_menu()
        logging.info("Entering Network Report")
        self.workflow_common_operations.goto_item("#cnxIPv6Enable_WFMenuSwitch", "#networkSettingsMenuList", select_option= False, scrollbar_objectname="#networkSettingsMenuListScrollBar")        

    def get_default_IPV4_state(self):
        '''
        Method to get the default ipv4 status.
        '''
        self._spice.wait_for('#networkSettingsMenuList')
        time.sleep(1)
        default_ipv4_state = self._spice.query_item("#cnxIPv4Enable_WFMenuSwitch")["checked"]
        logging.info("Default IPV4 state : %s", default_ipv4_state)
        if default_ipv4_state:
            return 'true'
        else:
            return 'false'

    def get_default_IPV6_state(self):
        '''Method to get the default ipv6 status.'''
        self._spice.wait_for('#networkSettingsMenuList')
        time.sleep(1)
        default_ipv6_state = self._spice.query_item("#cnxIPv6Enable_WFMenuSwitch")["checked"]
        logging.info("Default IPv6 state : %s", default_ipv6_state)
        if default_ipv6_state:
            return 'true'
        else:
            return 'false'


    def goto_restore_network_settings(self):
        '''
        Method to goto restore network settings.
        '''
        self.goto_network_settings_menu()
        time.sleep(2)
        logging.info("Entering into Restore Network Settings")
        self.workflow_common_operations.goto_item("#cnxRNDSettingsButton", "#networkSettingsMenuList", select_option= False, scrollbar_objectname="#networkSettingsMenuListScrollBar")
        time.sleep(3)       
        self._spice.wait_for('#cnxRNDMenuButton')
        time.sleep(2)
        restore_button = self._spice.query_item("#cnxRNDMenuButton")
        time.sleep(2)
        restore_button.mouse_click()

    def confirm_restore_defaults(self):
        '''Comfirm Restore network defaults'''
        self._spice.wait_for("#RestoreNetworkSettings")
        restore_button = self._spice.wait_for("#RestoreButton")
        restore_button.mouse_click()
        # Wait for the restore to complete
        self._spice.wait_for("#RestoreNetworkSettingSuccess", timeout=30)
        ok_button = self._spice.wait_for("#RestoreNetworkSuccessOk")
        ok_button.mouse_click()
        assert self._spice.wait_for("#networkSettingsMenuList")

    def cancel_confirm_restore_defaults(self):
        '''Do not confirm Restore network defaults on Restore Network Confirm screen'''
        self._spice.wait_for("#RestoreNetworkSettings")
        cancel_button = self._spice.query_item("#CancelButton")
        cancel_button.mouse_click()
        assert self._spice.wait_for("#networkSettingsMenuList")


    def goto_sign_in(self, action:str):
        '''
        UI should be on home screen before calling this method
        Navigate to sign in

        Args:
            action: either "Sign In" or "Sign Out"
        '''        
        home_app = self._spice.query_item("#HomeScreenView")
        self._spice.wait_until(lambda: home_app["activeFocus"] is True)
        logging.info("At Home Screen")
        try:
            assert not self.sign_in_app_operations.is_signed_in() ,"Already signed In"
            self.workflow_common_operations.scroll_to_position_horizontal(.01)

            self.sign_in_app_operations.goto_sign_in_app(action)

            time.sleep(2)
            self.sign_in_app_operations.enter_creds(True, "admin", "12345678")
            logging.info("Verify the login")
            response = self.sign_in_app_operations.verify_auth("success")
            assert response
        except Exception as message:
            logging.debug("Sign_in not supported %s", message)

    def sign_out(self):
        self.workflow_common_operations.scroll_to_position_horizontal(.01)
        currentApp = self._spice.wait_for(SignInAppWorkflowObjectIds.menu_item_signinid + " #launcherButton")
        currentApp.mouse_click()

    def sign_in_cleanup(self):
        """Method to clear sign-in."""

        try:
            # Look for the home screen view
            currentpage = self._spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
            assert currentpage

            # Scroll to the sign-in app
            self.workflow_common_operations.scroll_to_position_horizontal(.01)

            # Click the "Sign Out" button
            self.sign_out()

            # Look for the home screen view
            currentpage = self._spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
            assert currentpage
        except Exception as message:
            logging.debug("Sign-In is not supported %s", message)

    def goto_network_sign_in(self, action:str):
        '''
        UI should be on home screen before calling this method
        Navigate to network settings menu

        Args:
            action: either "Sign In" or "Sign Out"
        '''
        logging.info("At network settings signin Screen")
        time.sleep(2)
        try:
            self._spice.wait_for("#loginAdminView")
            time.sleep(2)
            currentApp = self._spice.query_item("#adminPasswordInputField")
            currentApp.mouse_click()
            time.sleep(2)
            self.sign_in_app_operations.enter_creds(True, "admin", "12345678")
            logging.info("Verify the login")
            response = self.sign_in_app_operations.verify_auth("success")
            assert response
        except Exception as message:
            logging.debug("Sign_in not supported %s", message)

    def get_hostname_bonjour_ipv6_from_networksetting(self):
        BHIStatus = []
        self.goto_network_settings_menu()

        self.workflow_common_operations.goto_item("#cnxBonjourName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        bonjourName = self._spice.query_item("#bonjourNameTextField")["inputText"]
        BHIStatus.append(bonjourName)
        self._spice.click_backButton()

        self.workflow_common_operations.goto_item("#cnxHostName_WFSettingsTextImage", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        hostName = self._spice.query_item("#hostNameTextField")["inputText"]
        BHIStatus.append(hostName)
        self._spice.click_backButton()

        self.workflow_common_operations.goto_item("#cnxIPv6Enable_WFSettingsSwitch", "#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")
        ipv6status = self.get_default_IPV6_state()
        BHIStatus.append(ipv6status)

        return BHIStatus
            
    def get_hostname_bonjour_ipv6_from_ethernetsetting(self):
        BHIStatus = []
        self.goto_ethernet_menu()

        self.workflow_common_operations.goto_item("#cnxEthernetBonjourNameSettingsTextImage", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        bonjourName = self._spice.query_item("#bonjourNameTextField")["inputText"]
        BHIStatus.append(bonjourName)
        self._spice.click_backButton()

        self.workflow_common_operations.goto_item("#cnxEthernetHostNameSettingsTextImage", "#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        hostName = self._spice.query_item("#hostNameTextField")["inputText"]
        BHIStatus.append(hostName)
        self._spice.click_backButton()

        return BHIStatus
    
    def set_linkspeed(self, workFlowObjectName, proSlectObjectName):
        '''
        Method to set link speed
        '''
        logging.info("Entering link speed Menu")
        time.sleep(1)
        self.workflow_common_operations.goto_item(workFlowObjectName,"#cnxLinkSpeed_WFComboBoxpopupList",scrollbar_objectname="#comboBoxScrollBar")
        time.sleep(3)
        assert self._spice.wait_for("#cnxEthernetMenuList",timeout = 15)

    def goto_network_security(self):
        '''
        This method is used to navigate UI upto security.
        '''
        self.goto_network_settings_menu()
        self._spice.wait_for("#networkSettingsMenuList")
        self.workflow_common_operations.goto_item("#networkSecuritySettingsSettingsTextImage", "#networkSettingsMenuList",scrolling_value=0.07, scrollbar_objectname="#networkSettingsMenuListScrollBar")
        
    def push_session_button_click(self, button, screenID:None):
        button_ = self._spice.wait_for(button)
        button_.mouse_click()
        time.sleep(2)
        self._spice.wait_for("#HomeScreenView")
        
    def goto_announcement_agent(self):
        '''
        This method is used to navigate UI upto announcement and click on that.
        '''
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxAnnounceAgentSettingsSwitch", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        announcementAgentButton = self._spice.query_item("#cnxAnnounceAgentMenuSwitch")
        time.sleep(1)
        announcementAgentButton.mouse_click()

    def goto_disable_firewall(self,isFirewallEnabled):
        '''
        This method is used to disable firewall from UI.

        Args:
            isFirewallEnabled: either true or false
        '''
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxFirewallSettingsButton", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        disableFirewallButton = self._spice.query_item("#cnxFirewallMenuButton")
        time.sleep(1)
        disableFirewallButton.mouse_click()
        if(isFirewallEnabled):
            self.firewall_disable()
        else:
            self.firewall_already_disabled()
        self._spice.wait_for("#networkSecuritySettingsMenuList")

    def firewall_disable(self):
        self._spice.wait_for("#DisableFirewallWarning")
        self._spice.wait_for("#DisableFirewallWarningFooter")
        continueButton = self._spice.query_item("#continueButton")
        time.sleep(1)
        continueButton.mouse_click()
        self._spice.wait_for("#DisableFirewallSuccessfully",timeout = 15)
        self._spice.wait_for("#DisableFirewallSuccessfullyFooter")
        okButton = self._spice.query_item("#okButton")
        time.sleep(1)
        okButton.mouse_click()

    def firewall_already_disabled(self):
        self._spice.wait_for("#FirewallAlreadyDisabled")
        self._spice.wait_for("#FirewallAlreadyDisabledFooter")
        continueButton = self._spice.query_item("#continueButton")
        time.sleep(1)
        continueButton.mouse_click()

    def goto_reset_authentication(self):
        '''
        This method is used to reset the authentication 802x1.
        '''
        resetButton = self._spice.query_item("#cnxResetSecurityMenuButton")
        time.sleep(1)
        resetButton.mouse_click()
        self._spice.wait_for("#securityResetViewFooter")
        warningViewResetButton = self._spice.query_item("#securityResetViewReset")
        time.sleep(1)
        warningViewResetButton.mouse_click()
        time.sleep(5)
        self._spice.query_item("#securityResetSuccessfulViewFooter")
        successViewOkButton = self._spice.query_item("#securityResetSuccessfulViewOk")
        time.sleep(1)
        successViewOkButton.mouse_click()
        self._spice.wait_for("#networkSecuritySettingsSettingsTextImage")
        
    def goto_reset_security(self):
        '''
        This method is used to reset security.
        '''
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxResetSecuritySettingsButton", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        resetSecurityButton = self._spice.query_item("#cnxResetSecurityMenuButton")
        time.sleep(1)
        resetSecurityButton.mouse_click()
        self._spice.wait_for("#securityResetViewverticalLayout")
        self._spice.wait_for("#securityResetViewFooter")
        confirmResetButton = self._spice.query_item("#securityResetViewReset")
        time.sleep(1)
        confirmResetButton.mouse_click()
        self._spice.wait_for("#securityResetSuccessfulView",timeout = 15)
        self._spice.wait_for("#securityResetSuccessfulViewFooter")
        okButton = self._spice.query_item("#securityResetSuccessfulViewOk")
        time.sleep(1)
        okButton.mouse_click()
        self._spice.wait_for("#networkSecuritySettingsMenuList")

    def goto_primary_secondary_dns_textfield(self, dnsTextFieldObjectName, isDnsConfigurationMethodAutomatic = True):
        '''
        This method is used to goto primarydns and secondarydns text field and check the keyboard.

        Args:
            dnsTextFieldObjectName: primaryDns or secondaryDns
            isDnsConfigurationMethodAutomatic: either true or false
        '''
        self.workflow_common_operations.goto_item(dnsTextFieldObjectName, "#ipv4View", scrollbar_objectname="#ipv4ViewScrollBar",scrolling_value = 0.07)
        if(isDnsConfigurationMethodAutomatic == False):
            self._spice.wait_for("#spiceKeyboardView")
            enterKey = self._spice.wait_for("#enterKeyPositiveDecimalKeypad")
            enterKey.mouse_click()

    def ipv4_apply_button_click(self):
        '''
        This method is used to click on apply button in ipv4.
        '''
        self._spice.wait_for("#ipv4View")
        applyButton = self._spice.wait_for("#ipv4ViewFooterApply")
        applyButton.mouse_click()

    def ipv6_apply_button_click(self):
        '''
        This method is used to click on apply button in ipv6.
        '''
        self._spice.wait_for("#ipv6View")
        applyButton = self._spice.wait_for("#ipv6ViewFooterApply")
        applyButton.mouse_click()

    def check_constraint_message(self):
        '''
        This method is used to click on OK button of constraint message.
        '''
        self._spice.wait_for("#ConstraintMessage",timeout = 10)
        self._spice.wait_for("#FooterView")
        okButton = self._spice.query_item("#okButton")
        okButton.mouse_click()

    def click_on_ipv4_config_method(self):
        '''
        UI should be on homescreen before calling this method 
        This method navigates to ethernet >ipv4 settings and clicks on config method option
        '''
        self.goto_ethernet_ipv4()
        logging.info("#At config method selection view")
        self.workflow_common_operations.goto_item("#ipv4ConfigDelegate", "#ipv4View", scrollbar_objectname="#ipv4ViewScrollBar")
      
    def set_default_ipv4_config_method(self):
        '''
        Method to navigate to config method and set dhcp
        '''
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        dhcpButton = self._spice.query_item("#dhcpv4")
        dhcpButton.mouse_click()
        time.sleep(1)
        self.ipv4_apply_button_click()
        assert self._spice.wait_for("#cnxEthernetMenuList")
        time.sleep(1)

    def set_ipv4_config_method_autoip(self):
        '''Method to set config method to autoip'''
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        autoip = self._spice.query_item("#autoip")
        autoip.mouse_click()
        time.sleep(1)
        self.ipv4_apply_button_click()
        assert self._spice.wait_for("#cnxEthernetMenuList")
        time.sleep(1)

    def get_default_ipv4_config_method(self):
        '''
        Method to get default config method state. UI should be on Network on before calling this method.
        '''
        self.click_on_ipv4_config_method()
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        default_config_state = self._spice.query_item("#dhcpv4")["enabled"]
        self._spice.goto_homescreen()
        logging.info("Get default config method state : %s", default_config_state)
        return default_config_state      

    def get_ui_config_method_autoip(self):
        '''Method to get config method and check if it set to autoip'''
        self.click_on_ipv4_config_method()
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        config_method = self._spice.query_item("#autoip")["enabled"]
        logging.info("Get default config method state : %s", config_method)
        return config_method

    def select_manual_config_method(self):
        '''Method to set config method to manual'''
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        time.sleep(1)
        manualButton = self._spice.query_item("#manual")
        manualButton.mouse_click()
        time.sleep(1)

    def set_ipv4_config_method_to_manual(self):
        '''select manual option at manual config page'''
        self.select_manual_config_method()
        self._spice.wait_for("#suggestManualIPView")
        manualButton = self._spice.query_item("#manualButton")
        manualButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#manualIPConfigurationView")
        apply = self._spice.query_item("#manualIPConfigurationApply")
        apply.mouse_click()
        time.sleep(5)
        assert self._spice.wait_for("#ipv4View")
        time.sleep(1)
        self._spice.goto_homescreen()
        
    def select_no_at_suggest_manual_config(self):
        '''select suggest option at manual config page'''

        self.select_manual_config_method()
        self._spice.wait_for("#suggestManualIPView")
        manualButton = self._spice.query_item("#suggestButton")
        manualButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#suggestSuccessConfirmView")
        okButton = self._spice.query_item("#noButton")
        okButton.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for("#ipv4View")
        time.sleep(1)

    def select_suggested_ip_at_manual_config(self):
        '''select suggest option at manual config page'''

        self.select_manual_config_method()
        self._spice.wait_for("#suggestManualIPView")
        manualButton = self._spice.query_item("#suggestButton")
        manualButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#suggestSuccessConfirmView")
        okButton = self._spice.query_item("#yesButton")
        okButton.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for("#ipv4View")
        time.sleep(1)

    def get_ui_config_method_manual(self):
        '''
        UI should be on home screen before calling this method
        This method will check if manual method is selected and 
        return the config method selected
        '''
        self.click_on_ipv4_config_method()
        self._spice.wait_for("#SettingsSpiceComboBoxpopupList")
        config_method = self._spice.query_item("#manual")["enabled"]
        logging.info("Get default config method state : %s", config_method)
        return config_method

    def click_on_dns_config_method(self):
        '''
        UI should be on home screen before calling this method
        This method will click on DNS config option under ipv4 settings
        '''
        self.goto_ethernet_ipv4()
        logging.info("#At config method selection view")
        self._spice.wait_for("#ipv4View")
        dns = self._spice.query_item("#dnsConfigSettingsComboBoxViewModel", query_index = 1)
        dns.mouse_click()
        assert self._spice.wait_for("#ipv4View")
 
    def goto_primary_dns_textfield(self):
        '''
        This method is used to goto primarydns and secondarydns text field and check the keyboard.
        '''
        #TODO check the obj id for primarydns and secondary dns
        logging.info("At IPV4 settings view")
        self.workflow_common_operations.goto_item("#SettingsTextField", "#ipv4View", scrollbar_objectname="#ipv4ViewScrollBar")
        # pridns = self._spice.query_item("#SettingsTextField #primaryDns")
        # pridns.mouse_click()
        okButton = self._spice.wait_for("#ConstraintMessageFooter #okButton")
        okButton.mouse_click()
        time.sleep(1)

    def goto_disable_fips(self):
        '''
        This method is used to disable fips from UI.
        '''
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxFipsSettingsButton", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        disableFipsButton = self._spice.query_item("#cnxFipsMenuButton")
        time.sleep(1)
        disableFipsButton.mouse_click()
        self._spice.wait_for("#fipsDisableConfirmation")
        continueButton = self._spice.query_item("#continueButton")
        time.sleep(1)
        continueButton.mouse_click()
        self._spice.wait_for("#fipsDisabling")  
        
    def goto_enable_fips(self):
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxFipsSettingsButton", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        enableFipsButton = self._spice.wait_for("#cnxFipsMenuButton")
        enableFipsButton.mouse_click()
        spice.wait_for("#okButton").mouse_click()
        
    def goto_disable_ipsec(self, isIPSecEnabled):
        '''
        This method is used to disable ipsec from UI.
        Args:
            isIPSecEnabled: either true or false
        '''
        self._spice.wait_for("#networkSecuritySettingsMenuList")
        self.workflow_common_operations.goto_item("#cnxIPSecSettingsButton", "#networkSecuritySettingsMenuList", select_option=False, scrollbar_objectname="#networkSecuritySettingsMenuListScrollBar")
        disableIPSecButton = self._spice.query_item("#cnxIPSecMenuButton")
        time.sleep(1)
        disableIPSecButton.mouse_click()
        if(isIPSecEnabled):
            self._spice.wait_for("#disableIPsecWarningFooter")
            continueButton = self._spice.query_item("#continueButton")
            time.sleep(1)
            continueButton.mouse_click()
            self._spice.wait_for("#disableIPsecSuccessfullyFooter")
            okButton = self._spice.query_item("#okButton")
            time.sleep(1)
            okButton.mouse_click()
        else:
            self._spice.wait_for("#iPSecAlreadyDisabledFooter")
            continueButton = self._spice.query_item("#continueButton")
            time.sleep(1)
            continueButton.mouse_click()
            self._spice.wait_for("#networkSecuritySettingsMenuList")   
 
    def set_config_method(self, method):
        # Click in comboBoxList
        config_combobox = self._spice.wait_for("#ipv4ConfigDelegate #SettingsSpiceComboBox")
        config_combobox.mouse_click()

        # Click in the option
        option = self._spice.wait_for(method)
        option.mouse_click()
        if method == "#manualRadioButtonModel":
            manual_btn = self._spice.wait_for("#manualButton")
            manual_btn.mouse_click()
            time.sleep(1)
            apply_btn = self._spice.wait_for("#manualIPConfigurationApply")
            apply_btn.mouse_click()

    def set_config_method_manual(self):
        '''Method to navigate to config method and set manual'''
        configuration = self._spice.wait_for("#ipv4SettingsEthernetRow")
        self.set_config_method("#manualRadioButtonModel")

    def get_IPV4_config(self):
        '''
        Return IPV4 info from IPv4 Settings view.
        Return:
            configuration: string with the IPv4 configuration.
        '''
        self._spice.wait_for("#ipv4View")
        configuration = self._spice.wait_for("#ipv4View")
        config = self._spice.wait_for("#ipv4ConfigDelegate #SettingsSpiceComboBox #textColumn SpiceText[visible=true]")["text"]
        return config

    def goto_info_eth_connectivity_tab(self):
        '''
        Navigate to ethernet from Info->connectivity menu
        '''
        self._spice.homeMenuUI().goto_menu_info_connectivity(self._spice)
        logging.info("At Connectivity Screen")
        self._spice.wait_for("#connectivityTabLayout")
        optionButton = self._spice.wait_for("#ethernetCardInTab")
        optionButton.mouse_click()

    def goto_info_eth_settings_button(self):
        self.goto_info_eth_connectivity_tab()
        self._spice.wait_for("#ethernetCardContentExpanded")
        settingsButton = self._spice.query_item("#ethernetSettingsButton")
        settingsButton.mouse_click()