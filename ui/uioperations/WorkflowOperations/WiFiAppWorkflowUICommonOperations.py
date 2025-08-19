import logging 
import time
import sys


from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.BaseOperations.IWiFiAppUIOperations import IWiFiAppUIOperations


class WifiAppWorkflowUICommonOperations(IWiFiAppUIOperations):
    
    def __init__(self,spice):
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.home_menu_workflow_ui_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.network_menu_workflow_ui_operations= NetworkAppWorkflowUICommonOperations(self._spice)

    def goto_settings_menu(self):
        '''Go to settings menu'''
        self._spice.goto_homescreen()
        time.sleep(5)

    def goto_menu_info(self):
        '''
        UI should be on home screen before calling this method
        Navigate to info from home
        '''
        self._spice.homeMenuUI().goto_menu()
        logging.info("Entering Info menu")
        self.workflow_common_operations.goto_item("#landingPageMenuAppList","#infoView",scrollbar_objectname="#landingPageMenuAppListButtonTemplateViewverticalLayoutScrollBar")
 
    def goto_menu_info_connectivity(self):
        '''
        UI should be on home screen before calling this method
        Navigate to connectivity from info
        '''
        self._spice.homeMenuUI().goto_menu()
        logging.info("Entering Info menu")
        self.workflow_common_operations.goto_item("#infoView","#connectivityTabLayoutverticalLayout",scrollbar_objectname="#infoViewvwerticalLayoutScrollBar")
    
    def goto_wifi_info_connectivity(self):
        '''
        UI should be on home screen before calling this method
        Navigate to connectivity from info menu
        '''
        self.home_menu_workflow_ui_operations.goto_menu_info_connectivity(self._spice)

    def goto_wifi_in_connectivity_tab(self):
        '''
        UI should be on info>connectivity screen before calling this method
        Navigate to wifi from connectivity menu
        '''
        logging.info("At Connectivity Screen")
        self._spice.wait_for("#connectivityTabLayout")
        optionButton = self._spice.wait_for("#wifiCardInTab")
        optionButton.mouse_click()
        time.sleep(1)
    
    def goto_eth_in_connectivity_tab(self):
        '''
        UI should be on info>connectivity screen before calling this method
        Navigate to wifi from connectivity menu
        '''
        logging.info("At Connectivity Screen")
        self._spice.wait_for("#connectivityTabLayout")
        optionButton = self._spice.wait_for("#ethernetCardInTab")
        optionButton.mouse_click()
        time.sleep(2)

    def goto_close_button_on_connectivity_tab(self):
        '''
        UI should be on connectivity expanded menu
        Navigate to eth,wifi,wfd option from connectivity menu
        '''
        logging.info("At connectivity expanded screen")
        closeButton = self._spice.query_item("#closeButton")
        closeButton.mouse_click()
        assert self._spice.wait_for("#connectivityTabLayout")
        time.sleep(1)
 
    def goto_wifi_info_connectivity_wfd(self):
        '''
        UI should be on home screen before calling this method
        Navigate to WFD option from connectivity menu
        '''
        self.goto_wifi_info_connectivity()
        logging.info("Entering connectivity menu")
        self._spice.wait_for("#infoView")
        #click on wireless menu
        # optionButton = self._spice.query_item("#connectivityTab")
        # optionButton.mouse_click()
        self.workflow_common_operations.goto_item("#connectivityTabLayout","#wifiDirectCardInTab", scrollbar_objectname="#connectivityTabLayoutverticalLayoutScrollBar")
        time.sleep(1)
        self._spice.wait_for("#wifiDirectCardContent")
        self.goto_close_button_on_connectivity_tab()
        time.sleep(1)
        self._spice.goto_homescreen()

    def goto_wifi_info_connectivity_wifi(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Wifi option from connectivity menu
        '''
        self.goto_wifi_info_connectivity()
        time.sleep(1)
        #click on wireless menu
        logging.info("At Connectivity Screen")
        self.goto_wifi_in_connectivity_tab()
        self._spice.wait_for("#wifiCardContentExpanded")
        self.goto_close_button_on_connectivity_tab()

    def goto_wifi_info_connectivity_eth(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ethernet option from connectivity menu
        '''
        self.goto_wifi_info_connectivity()
        time.sleep(1)
        self.goto_eth_in_connectivity_tab()
        time.sleep(1)
        self._spice.wait_for("#ethernetCardContentExpanded")
        self.goto_close_button_on_connectivity_tab()

       
    def goto_info_wifi_print_details(self, cdm):
        '''
        UI should be on wifi info connectivity screen before calling this method
        Navigate to print details option from wifi info connectivity menu
        '''
        optionButton = self._spice.query_item("#wifiCardInTab")
        optionButton.mouse_click()
        time.sleep(1)
        logging.info("At wifi expanded screen")
        self._spice.wait_for("#wifiCardContentExpanded")
        time.sleep(1)
        printDetailsButton = self._spice.query_item("#wifiPrintDetailsButton")
        printDetailsButton.mouse_click()
        
        reports_print = cdm.get(cdm.CDM_PRINT_REPORTS)
        while reports_print['state'] != 'idle':
            time.sleep(1)
            reports_print = cdm.get(cdm.CDM_PRINT_REPORTS)
        okButton = self._spice.check_item("#okButton")
        if okButton:
            okButton.mouse_click()
        assert self._spice.wait_for("#connectivityTabLayout")
        
    def goto_info_wifi_settings_button(self):
        '''
        UI should be on wifi info connectivity screen before calling this method
        Navigate to print details option from wifi info connectivity menu
        '''
        logging.info("At wifi expanded screen")
        self.goto_wifi_in_connectivity_tab()
        self._spice.wait_for("#wifiCardContentExpanded")
        time.sleep(1)
        settingsButton = self._spice.query_item("#wifiSettingsButton")
        settingsButton.mouse_click()
        time.sleep(2)
        self.goto_close_button_on_connectivity_tab()
        # assert self._spice.wait_for("#cnxWiFi_WFMenuListListView")

    def goto_info_eth_print_details(self, cdm):
        '''
        UI should be on eth info connectivity screen before calling this method
        Navigate to print details option from eth info connectivity menu
        '''
        optionButton = self._spice.query_item("#ethernetCardInTab")
        middle_width = int(optionButton["width"] / 2)
        middle_height = int(optionButton["height"] / 2)
        optionButton.mouse_click(middle_width, middle_height)
        time.sleep(2)
        logging.info("At ethernet expanded screen")
        self._spice.wait_for("#ethernetCardContentExpanded")
        printDetailsButton = self._spice.query_item("#ethernetPrintDetailsButton")
        printDetailsButton.mouse_click()

        reports_print = cdm.get(cdm.CDM_PRINT_REPORTS)
        while reports_print['state'] != 'idle':
            time.sleep(1)
            reports_print = cdm.get(cdm.CDM_PRINT_REPORTS)
        okButton = self._spice.check_item("#okButton")
        if okButton:
            okButton.mouse_click()
        assert self._spice.wait_for("#connectivityTabLayout")
        
    def goto_info_eth_settings_button(self):
        '''
        UI should be on eth info connectivity screen before calling this method
        Navigate to print details option from eth info connectivity menu
        '''
        logging.info("At ethernet expanded screen")
        self.goto_eth_in_connectivity_tab()
        self._spice.wait_for("#ethernetCardContentExpanded")
        time.sleep(1)
        settingsButton = self._spice.query_item("#ethernetSettingsButton")
        settingsButton.mouse_click()
        time.sleep(1)
        self.goto_close_button_on_connectivity_tab()

    def goto_info_WFD_print_details(self):
        '''
        UI should be on WFD info connectivity screen before calling this method
        Navigate to print details option from WFD info connectivity menu
        '''
        self.workflow_common_operations.goto_item("#connectivityTabLayout","#wifiDirectCardInTab", scrollbar_objectname="#connectivityTabLayoutverticalLayoutScrollBar")
        time.sleep(1)
        logging.info("At WFD expanded screen")
        self._spice.wait_for("#wifiDirectCardContentExpanded")
        time.sleep(1)
        settingsButton = self._spice.query_item("#wifiDirectPrintDetailsButton")
        settingsButton.mouse_click()
        time.sleep(50)
        assert self._spice.wait_for("#connectivityTabLayout")

    def goto_info_WFD_settings_button(self):
        '''
        UI should be on WFD info connectivity screen before calling this method
        Navigate to print details option from WFD info connectivity menu
        '''
        logging.info("At WFD expanded screen")
        self.workflow_common_operations.goto_item("#connectivityTabLayout","#wifiDirectCardInTab", scrollbar_objectname="#connectivityTabLayoutverticalLayoutScrollBar")
        time.sleep(1)
        self._spice.wait_for("#wifiDirectCardContentExpanded" )
        time.sleep(1)
        settingsButton = self._spice.query_item("#wifiDirectSettingsButton")
        settingsButton.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for("#cnxWFDMenuListListView")

    def goto_wifi_view_details_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi view details from wifi menu
        '''
        self.goto_wifi_menu()
        logging.debug("Entering wi-fi view details")
        self.workflow_common_operations.goto_item("#wifiViewDetailDelegate","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")

    def goto_wifi_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi from network
        '''
        self.network_menu_workflow_ui_operations.goto_network_settings_menu()
        logging.debug("Entering wi-fi")
        self.workflow_common_operations.goto_item("#cnxWiFi_WFSettingsTextImage","#networkSettingsMenuList", scrollbar_objectname="#networkSettingsMenuListScrollBar")


    def goto_wifi_ipv4_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 config menthod from wifi menu
        '''
        self.goto_wifi_menu()
        logging.debug("Entering ipv4")
        self.workflow_common_operations.goto_item("#ipv4SettingsEthernetRow","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")
        self._spice.wait_for("#changingIpWarning")
        okButton = self._spice.query_item("#changingIpWarningOk")
        okButton.mouse_click()

    def goto_wifi_ipv4_settings_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 config method from ipv4 config settings menu
        '''
        self.goto_wifi_ipv4_menu()
        logging.debug("Entering ipv4 settings")
        self.workflow_common_operations.goto_item("#ipv4ConfigBranch","#ipv4View", scrollbar_objectname="#ipv4ViewScrollBar")
        time.sleep(1)
        self._spice.wait_for("#ipv4ConfigurationView")
        okButton = self._spice.query_item("#ipv4ConfigManual")
        okButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#suggestManualIPView")
        okButton = self._spice.query_item("#manualButton")
        okButton.mouse_click()
        time.sleep(2)


    def goto_wifi_setup_wizard_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi setup wizard from wifi menu
        '''
        self.goto_wifi_menu()
        logging.debug("Entering wi-fi")
        self.workflow_common_operations.goto_item("#Start","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")
   
    def goto_band_frequency_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to Band frequency from wifi menu
        '''
        self.goto_wifi_menu()
        logging.debug("Entering wi-fi")
        self.workflow_common_operations.goto_item("#bandFrequencySwitch","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")

    def goto_wifi_enter_network_name(self):
        '''
        UI should be on home screen before calling this method
        Navigate to SSID list from wi-fi setup wizard
        '''
        self.goto_wifi_setup_wizard_menu()
        logging.debug("Entering ssid list")
        self.workflow_common_operations.goto_item("#enterNetworkNameCard","#connectivity_selectNetworkName",scrollbar_objectname="#connectivity_selectNetworkNameverticalLayoutScrollBar")

    def goto_wifi_direct_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi from network
        '''
        self.network_menu_workflow_ui_operations.goto_network_settings_menu()
        logging.debug("Entering wi-fi Direct")
        self.workflow_common_operations.goto_item("#cnxWFDSettingsTextImage","#networkSettingsMenuList",scrollbar_objectname="#networkSettingsMenuListScrollBar")
        self.set_wfd_state(True)
        
    def set_wfd_state(self, default_state):
        ''' Method to enable wfd from ui'''
        self._spice.wait_for('#wfdSwitch')
        default_wfd_state = self._spice.query_item("#wfdSwitch")["checked"]
        # Enable WFD.
        if default_state != default_wfd_state:
            current_button = self._spice.query_item("#wfdSwitch")
            current_button.mouse_click()
            
    def get_default_wfd_state(self):
        '''
        Method to get wfd default state. UI should be on Network on before calling this method.
        '''
        self._spice.wait_for('#wfdSwitch')
        default_wfd_state = self._spice.query_item("#wfdSwitch")["checked"]
        logging.info("Default wfd state : %s", default_wfd_state)
        default_wfd_state = "true" if default_wfd_state else "false"
        return default_wfd_state

    def goto_wifi_direct_view_details_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct view deatils menu from network
        '''
        self.goto_wifi_direct_menu()
        logging.debug("Entering wi-fi Direct view details")
        self.workflow_common_operations.goto_item("#cnxWFDViewDetailsSettingsTextImage","#cnxWFDMenuList",scrollbar_objectname="#cnxWFDMenuListScrollBar")

    def navigate_to_wfd_channel(self,click_item = True):
        '''
        UI should be on wifi direct menu before calling this method.
        Scrolls/Navigates to WFD channels row.
        '''
        self.workflow_common_operations.goto_item("#wfdChannelTextImageBranch","#cnxWFDMenuList",select_option=click_item,scrollbar_objectname="#cnxWFDMenuListScrollBar")

        
    def goto_print_details_button_on_wifi_direct_view_details(self):
        '''
        Navigate to wi-fi Direct view deatils menu from network
        Navigate to wi-fi Direct printDetailsButton
        '''
        self.goto_wifi_direct_view_details_menu()
        printDetailsButton = self._spice.query_item("#cnxWFDViewDetailsSettingsTextImage")
        printDetailsButton.mouse_click()
        time.sleep(2)
        self._spice.wait_for("#wfdViewDetails")     
        confirmPrintDetailsButton = self._spice.query_item("#printDetailsButton")
        
    def get_wfd_status(self):
        '''
        Method to get wfd default state. UI should be on Network on before calling this method.
        '''
        self._spice.wait_for('#wfdViewDetails')
        default_wfd_state = self._spice.query_item("#wfdViewDetails")["wfdStatus"]
        logging.info("Default wfd state : %s", default_wfd_state)
        default_wfd_state = "true" if default_wfd_state else "false"
        return default_wfd_state
    
    def get_wfd_connection_method(self):
        '''
        Method to get wfd default state. UI should be on Network on before calling this method.
        '''
        self._spice.wait_for('#wfdViewDetails')
        default_wfd_state = self._spice.query_item("#wfdViewDetailsConnectionMethod #ValueText")["text"]
        logging.info("Default wfd state : %s", default_wfd_state)
        return default_wfd_state
    
    def get_wfd_name_method(self):
        '''
        Method to get wfd default state. UI should be on Network on before calling this method.
        '''
        self._spice.wait_for('#wfdViewDetails')
        time.sleep(1)
        default_wfd_state = self._spice.query_item("#wfdViewDetails")["wfdName"]
        logging.info("Default wfd state : %s", default_wfd_state)
        return default_wfd_state

    def goto_wifi_direct_print_details_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct print details from view deatils menu
        '''
        self.goto_wifi_direct_view_details_menu()
        logging.debug("Entering wi-fi Direct view details")
        self.workflow_common_operations.goto_item("#printDetailsButton","#DetailInfoverticalLayout", scrollbar_objectname="#DetailInfoverticalLayoutScrollBar")

    def goto_wifi_direct_name_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct connection method from network
        '''
        self.goto_wifi_direct_menu()
        logging.debug("Entering wi-fi Direct Name")
        self.workflow_common_operations.goto_item("#cnxWFDNameSettingsTextImage","#cnxWFDMenuList",scrollbar_objectname="#cnxWFDMenuListScrollBar")
        
    def change_wifi_direct_name(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct name from network
        '''
        self.goto_wifi_direct_name_menu()
        ssid_textfield = self._spice.wait_for("#wfdNameTextField")
        ssid_textfield.mouse_click()
        ssid_textfield.__setitem__('displayText', "text123")
        enterKey  = self._spice.wait_for("#enterKey1")
        enterKey.mouse_click()

    def goto_wifi_direct_channel_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct connection method from network
        '''
        self.goto_wifi_direct_menu()
        logging.debug("Entering wi-fi Direct channel")

    def goto_wifi_direct_connection_method_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct connection method from WFD
        '''
        self.goto_wifi_direct_menu()
        logging.debug("Entering wi-fi Direct connection methods")
        self.workflow_common_operations.goto_item("#cnxWFDConnectionMethod_WFMenuComboBox","#cnxWFDMenuList",scrollbar_objectname="#cnxWFDMenuListScrollBar")
        self._spice.wait_for("#cnxWFDConnectionMethod_WFMenuComboBox")

    def goto_wifi_direct_connection_method_selection_menu(self, wfd_connection_method):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct connection method selection from WFD and click the passed connection method.
        '''
        self.goto_wifi_direct_connection_method_menu()
        logging.debug("Entering wi-fi Direct connection method selection")
        wfd_connectionMethod_comboBox = self._spice.wait_for(wfd_connection_method)
        wfd_connectionMethod_comboBox.mouse_click()

    def goto_wps_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to WPS menu from network
        '''
        self.goto_wifi_menu()
        self.workflow_common_operations.goto_item("#reportWifiProtectedSetupButtonView","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")
        self._spice.wait_for("#reportWifiProtectedSetupButtonView")
        wpsStartButton = self._spice.query_item("#reportWifiProtectedSetupButtonView #Start")
        #start = self._spice.query_item("Start")
        wpsStartButton.mouse_click()

    def goto_wps_pushbutton_method(self):
        '''Select the WPS push button method'''
        #self.goto_WPS_menu()
        logging.debug("Select WPS connection method")
        #self._spice.wait_for("#WPSMenulist1")
        pushButton = self._spice.query_item("#pushButton")
        pushButton.mouse_click()
        self._spice.wait_for("#WpsPushButtonInstructionHeader")
        startPushButton = self._spice.query_item("#startButton")
        startPushButton.mouse_click()

    def goto_wps_pin_method(self):
        '''Select the WPS Pin method'''
        #self.goto_WPS_menu()
        logging.debug("Select WPS connection method")
        Pin = self._spice.query_item("#pin")
        Pin.mouse_click()
        #self._spice.wait_for("#WpsPinInstructionHeader")
        startPin = self._spice.query_item("#startButton")
        startPin.mouse_click()

    def goto_network_name_not_found_screen(self):
        '''
        UI should navigate from enetr SSID screen to network not found screen
        if incorrect SSID is typed
        '''
        self.goto_enter_network_name_screen_oobe_incorrect()
        self.click_connect_on_enter_network_name_screen()
        logging.debug("Entering network name not found view")
        self._spice.wait_for("#NetworkNameNotFoundView")
        retryButton = self._spice.query_item("#NetworkNameNotFoundRetry")
        retryButton.mouse_click()
        time.sleep(2)
        self.goto_cancel_button_on_enter_network_name_screen()
        self._spice.goto_homescreen()
        time.sleep(1)

    def goto_restore_network_defaults(self):
        '''
        UI should be on home screen before calling this method 
        navigate to restore network defaults from network settings menu
        '''
        self.network_menu_workflow_ui_operations.goto_network_settings_menu()
        logging.debug("Entering restore network defaults")
        self.workflow_common_operations.goto_item("#cnxRNDSettingsButton","#networkSettingsMenuList",scrollbar_objectname="#networkSettingsMenuListScrollBar")
        toggleButton = self._spice.query_item("#cnxRNDMenuButton")
        toggleButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#RestoreNetworkSettingsConfirm")
        yesButton = self._spice.query_item("#RestoreNetworkConfirmYes")
        yesButton.mouse_click()
        time.sleep(1)
        self._spice.wait_for("#RestoreNetworkSettingSuccess")
        okButton = self._spice.query_item("#RestoreNetworkSuccessOk")
        okButton.mouse_click()
        time.sleep(3)
        self._spice.goto_homescreen()
        time.sleep(1)

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
        self._spice.wait_for("#connectivity_selectNetworkName")
        ssidButton = self._spice.query_item("#ssidCard_testSecureAP")
        ssidButton.mouse_click()
        time.sleep(1)

    def click_on_refresh_button_at_select_ssid_screen(self):
        ''' UI should be on SSID screen'''
        if self._spice.is_HomeScreen():
            self.goto_wifi_setup_wizard_menu()

        logging.info("At select network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        refreshButton = self._spice.query_item("#refreshButton")
        refreshButton.mouse_click()
        self._spice.wait_for("#CheckingExistingProfileView")
        assert self._spice.wait_for("#connectivity_selectNetworkName")
        time.sleep(2)
    
    def goto_wifi_already_connected_screen(self):
        '''Click on yes at connection already exists screen'''
        
        self.workflow_common_operations.goto_item("#Start","#cnxWiFi_WFMenuList", scrollbar_objectname="#cnxWiFi_WFMenuListScrollBar")
        logging.info("at connection already setup screen")
        okButton = self._spice.wait_for("#connectionAlreadySetupFooter #yesButton")
        okButton.mouse_click()
        # time.sleep(1)
        self.goto_select_ssid_name_screen()
        # time.sleep(2)
        self.goto_enter_password_screen()
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("print123","#passwordTextField")
        # time.sleep(1)
        self.goto_submit_password_screen()
        logging.info("At enter confirm settings screen")
        self._spice.wait_for("#connectivity_confirmSettings")
        # time.sleep(1)
        confirmButton = self._spice.query_item("#confirmSettingsFooter #okButton")#showpasswordButton
        # time.sleep(1)
        confirmButton.mouse_click()
        time.sleep(1)
        logging.info("At trying to connect screen")
        self._spice.wait_for("#connectivity_statusTryingToConnectverticalLayout")
        cancelButton = self._spice.query_item("#cancelButton")
        cancelButton.mouse_click()
        time.sleep(1)

    def goto_restore_settings_in_wsw(self):
        '''click on restore settings > yes'''
        self._spice.wait_for("#restoreRetainSettingsView")
        yesButton = self._spice.query_item("#restoreRetainSettingsViewYes")
        yesButton.mouse_click()
        self._spice.wait_for("#restoredView")
        okButton = self._spice.query_item("#restoredViewOk")
        okButton.mouse_click()
        time.sleep(1)
    
    def goto_enter_network_name_screen(self):
        '''click on enter name and click on the filed to type SSID'''
        logging.info("At enter network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        ssidButton = self._spice.query_item("#enterNetworkNameCard")
        ssidButton.mouse_click()
        time.sleep(5)
        self._spice.wait_for("#enterNetworkNameView")
        ssidButton = self._spice.query_item("#enterNetworkNameTextField")
        ssidButton.mouse_click()
        time.sleep(5)
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("testSecureAP","#enterNetworkNameTextField")
        time.sleep(5)
        connectButton = self._spice.query_item("#connectButton")#or cancelButton
        connectButton.mouse_click()
        time.sleep(1)

    def goto_enter_network_name_screen_oobe_incorrect(self):
        '''click on enter name and click on the filed to type SSID'''
        logging.info("At enter network name screen")
        self.goto_enter_password_screen()
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("print1213","#passwordTextField")
        #self.workflow_common_operations.goto_item("#enterNetworkNameCard", "#connectivity_selectNetworkNameverticalLayout", scrollbar_objectname="#connectivity_selectNetworkNameverticalLayoutScrollBar")
        # self._spice.wait_for("#connectivity_selectNetworkName")
        # ssidButton = self._spice.query_item("#enterNetworkNameCard")
        # ssidButton.mouse_click()
        # time.sleep(5)
        # self._spice.wait_for("#enterNetworkNameView")
        # ssidButton = self._spice.query_item("#enterNetworkNameTextField")
        # ssidButton.mouse_click()
        # time.sleep(5)
        # self._spice.keyBoard.keyboard_set_text_with_out_dial_action("testSecure","#enterNetworkNameTextField")
        # time.sleep(5)

    def click_connect_on_enter_network_name_screen(self):
        '''click on connect at enter network name screen'''
        logging.info("At enter network name text field view")
        self._spice.wait_for("#enterNetworkNameView")
        connectButton = self._spice.query_item("#connectButton")#or cancelButton
        connectButton.mouse_click()
        time.sleep(1)

    # TODO: #DirectedScanInProgress ID is not working need to update this method
    def click_on_cancel_after_connecting_on_enter_ssid_screen(self):
        '''select cancel after clicking on connect to ssid '''
        # self.click_connect_on_enter_network_name_screen()
        self._spice.wait_for("#enterPasswordView")
        # cancelButton = self._spice.query_item("#enterPasswordFooter #cancelButton")
        cancelButton = self._spice.query_item("#cancelButton")
        cancelButton.mouse_click()
        time.sleep(1)
        # self.goto_submit_password_screen()
        # self._spice.wait_for("#connectivity_confirmSettings")
        # confirmButton = self._spice.query_item("#okButton")#showpasswordButton
        # confirmButton.mouse_click()
        # self._spice.wait_for("#DirectedScanInProgress")
        # cancelButton = self._spice.query_item("#cancelButton")
        # cancelButton.mouse_click()
        # time.sleep(2)
        # assert self._spice.wait_for("#connectivity_selectNetworkName")
    
    def goto_enter_network_name_screen_cancel(self):
        '''click on enter name and click on the filed to type SSID'''
        logging.info("At enter network name screen")
        self.goto_select_ssid_name_screen()
        time.sleep(3)
        logging.info("At enter network name screen")
        # self._spice.wait_for("#enterNetworkNameView")
        self._spice.wait_for("#enterPasswordView")
        cancelButton = self._spice.query_item("#enterPasswordFooter #cancelButton")
        self._spice.validate_button(cancelButton)
        cancelButton.mouse_click()
        time.sleep(1)
        logging.info("At select network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        backButton = self._spice.query_item("#BackButton")
        backButton.mouse_click()

        self._spice.goto_homescreen()

        time.sleep(1)
   
    def goto_cancel_button_on_enter_network_name_screen(self):
        '''click on cancel at enter network name  screen '''
        logging.info("At enter network name screen")
        self._spice.wait_for("#enterNetworkNameView")
        cancelButton = self._spice.query_item("#cancelButton")
        cancelButton.mouse_click()
        time.sleep(1)
        logging.info("At select network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        backButton = self._spice.query_item("#BackButton")
        backButton.mouse_click()
        time.sleep(1)
        self._spice.goto_homescreen()

    def goto_enter_password_screen(self):
        '''enter password screen type password submit password,confirm password for ssid'''
        logging.info("At enter password screen")
        self._spice.wait_for("#enterPasswordView")
        pswButton = self._spice.query_item("#passwordTextField")
        self._spice.validate_button(pswButton)
        pswButton.mouse_click()
        time.sleep(5)

    def set_incorrect_password_in_wifi_wizard(self, password):
        '''enter password screen type incorrect password submit password,confirm password'''
        self.goto_enter_password_screen()
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action(password,"#passwordTextField")
        time.sleep(2)
        self.goto_submit_password_screen()
        self.goto_confirm_settings_screen()

    def goto_retry_button_on_incorrect_password_screen_wsw(self):
        ''' click on retry at incorrect password screen at WSW'''

        logging.info("At incorrect password screen")
        self._spice.wait_for("#IncorrectPasswordViewverticalLayout")
        retryButton = self._spice.query_item("#retryButton")
        retryButton.mouse_click()
        assert self._spice.wait_for("#enterPasswordView")
        time.sleep(1)
        self._spice.goto_homescreen()

    def goto_printreport_button_on_incorrect_password_screen_wsw(self):
        ''' click on print report at incorrect password screen at WSW'''

        logging.info("At incorrect password screen")
        self._spice.wait_for("#IncorrectPasswordViewverticalLayout")
        retryButton = self._spice.query_item("#printReportButton")
        retryButton.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for("#IncorrectPasswordViewverticalLayout")
        time.sleep(1)

    def goto_exit_button_on_incorrect_password_screen_wsw(self):
        ''' click on exit at incorrect password screen at WSW'''

        logging.info("At incorrect password screen")
        self._spice.wait_for("#IncorrectPasswordViewverticalLayout")
        retryButton = self._spice.query_item("#wizardCompletionFooter #exitButton")
        retryButton.mouse_click()
        time.sleep(1)
        assert self._spice.wait_for("#cnxWiFi_WFMenuListListView")
        self._spice.goto_homescreen()
     
    def goto_submit_password_screen(self):
        '''click om submit  at password screen'''
        logging.info("At enter password submit screen")
        self._spice.wait_for("#enterPasswordView")
        submitButton = self._spice.query_item("#submitButton")
        submitButton.mouse_click()
        time.sleep(2)

    def goto_cancel_password_screen(self):
        '''click on cancel at trying to connect screen'''
        logging.info("At password cancel screen")
        self._spice.wait_for("#connectivity_statusTryingToConnect")
        cancelButton = self._spice.query_item("#cancelButton")
        cancelButton.mouse_click()
        time.sleep(2)
        assert self._spice.wait_for("#cnxWiFi_WFMenuList")
        self._spice.goto_homescreen()

 
    def goto_confirm_settings_screen(self):
        '''click on ok at confirm settings screen'''
        logging.info("At enter confirm settings screen")
        self._spice.wait_for("#connectivity_confirmSettings")
        confirmButton = self._spice.query_item("#confirmSettingsFooter #okButton")#showpasswordButton
        confirmButton.mouse_click()
        time.sleep(5)

    def goto_network_success_screen(self):
        '''click on continue at network sucess screen'''
        logging.info("At n/w sucess screen")
        self._spice.wait_for("#oobeNetworkSuccessView")
        continueButton = self._spice.query_item("#continueButton")
        continueButton.mouse_click()
        time.sleep(10)
        

    def goto_network_success_screen_wifi(self):
        '''click on continue at network success screen'''
        logging.info("At n/w success screen")
        okButton = self._spice.wait_for("#connectionSuccessfulFooter #okButton")
        okButton.mouse_click()
        time.sleep(1)

    def set_wifi_state(self, default_state):
        ''' Method to enable or disable wifi from ui'''
        self._spice.wait_for('#wifiSwitch')
        default_wifi_state = self._spice.query_item("#wifiSwitch")["checked"]
        if default_state != default_wifi_state:
            wifi_switch_button = self._spice.query_item("#wifiSwitch")
            wifi_switch_button.mouse_click()

    def get_default_wifi_state(self):
        '''
        Method to get wifi default state. UI should be on Wifi on before calling this method.
        '''
        self._spice.wait_for('#wifiSwitch')
        default_wifi_state = self._spice.query_item("#wifiSwitch")["checked"]
        logging.info("Default wifi state : %s", default_wifi_state)
        default_wifi_state = "true" if default_wifi_state else "false"
        return default_wifi_state
        
    def goto_network_success_compare_screen(self, udw, device, ipview = True):
        '''click on continue at network sucess screen'''
        logging.info("At n/w sucess screen")
        if ipview:
            self._spice.wait_for("#oobeNetworkSuccessView")
            continueButton = self._spice.query_item("#continueButton")
            continueButton.mouse_click()
            time.sleep(10)
            self._spice.oobeapp.goto_complete_oobe(udw, device)

        else:
            self._spice.wait_for("#oobeNetworkSuccessView")
            continueButton = self._spice.query_item("#editButton")
            continueButton.mouse_click()
            time.sleep(10)
            print ("#ipAddressSettingsTextField")
            time.sleep(5)
            self._spice.wait_for("#manualIpSettings")
            cancelButton = self._spice.query_item("#manualIpCancelButton")
            cancelButton.mouse_click()
            time.sleep(2)
            self._spice.oobeapp.goto_complete_oobe(udw, device)
            

    def goto_alert_window(self):
        '''click on alert screen'''
        alertButton = self._spice.query_item("#statusBar")
        alertButton.mouse_click()
        time.sleep(1)
        okButton = self._spice.query_item("#statusBar")
        okButton.mouse_click()
        time.sleep(1)
        
    def goto_manual_ipv4_config_ip_address(self, spice):
        '''click on Manual IP field at manual ip config screen'''
        spice.wait_for("#manualIPConfigurationView")
        okButton = spice.query_item("#nwIPField")
        okButton.mouse_click()
        time.sleep(1)

    def goto_manual_ipv4_config_subnet_mask(self):
        '''click on subnet mask field at manual ip config screen'''
        self._spice.wait_for("#manualIPConfigurationView")
        okButton = self._spice.query_item("#nwSubnetField")
        okButton.mouse_click()
        time.sleep(1)

    def goto_manual_ipv4_config_default_gateway(self):
        '''click on default gateway field at manual ip config screen'''
        self._spice.wait_for("#manualIPConfigurationView")
        okButton = self._spice.query_item("#nwGatewayField")
        okButton.mouse_click()
        time.sleep(1)

    def click_on_clear_button_in_host_name_field(self):
        '''clear the host name'''
        self.network_menu_workflow_ui_operations.goto_hostname()
        self._spice.wait_for("#hostNameTextField")
        clearButton = self._spice.query_item("#ClearMouseArea")
        clearButton.mouse_click()
        time.sleep(2)
        
    def goto_configuration_summary_from_ethernet_menu(self):
        ''' click on configuration summary at  ethernet setting menu '''
        self.network_menu_workflow_ui_operations.goto_ethernet_menu()
        logging.debug("Entering ethernet settings menu")
        self.workflow_common_operations.goto_item("#configurationSummaryViewDelegate","#cnxEthernetMenuList", scrollbar_objectname="#cnxEthernetMenuListScrollBar")
        logging.info("At config summary screen")
        #self.workflow_common_operations.goto_item("#configurationSummaryViewverticalLayoutScrollBar","#configurationSummaryViewverticalLayout", scrollbar_objectname="#configurationSummaryViewverticalLayoutScrollBar")
        self._spice.wait_for("#configurationSummaryView")
        okButton = self._spice.query_item("#okButton")
        okButton.mouse_click()
        time.sleep(2)
        self.goto_settings_menu()

    def configure_wireless_by_selecting_ssid(self):
        ''' Click WSW select SSID,enter password '''      
        self.goto_select_ssid_name_screen()
        self.goto_enter_password_screen()
        try:
            # Handle already wifi connection set-up screen 
            self.wait_for("#connectionAlreadySetupView")
            yes_button = self.query_item("#connectionAlreadySetupFooter #yesButton")
            yes_button.mouse_click()
        except:
            logging.info("Wifi is not already connected")
        
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("print123","#passwordTextField")
        time.sleep(5)
        self.goto_submit_password_screen()
        self.goto_confirm_settings_screen()
        self.goto_network_success_screen_wifi()
        time.sleep(2)
        assert self._spice.wait_for("#cnxWiFi_WFMenuList")

    def set_password_in_wifi_wizard_ssid(self, password):
        '''
            Method to set wifi password
            Args:
                password: Password to set for wifi
        '''
        try:
            # Handle already wifi connection set-up screen 
            self.wait_for("#connectionAlreadySetupView")
            yes_button = self.query_item("#connectionAlreadySetupFooter #yesButton")
            yes_button.mouse_click()
        except:
            logging.info("Wifi is not already connected")
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action(password,"#passwordTextField")
        time.sleep(1)
        self.goto_submit_password_screen()
        self.goto_confirm_settings_screen()
        self.goto_network_success_screen_wifi()

    def set_incorrect_pw_and_retry(self, password):
        '''
            Method to set wifi password
            Args:
                password: Password to set for wifi
        '''
        try:
            # Handle already wifi connection set-up screen 
            self.wait_for("#connectionAlreadySetupView")
            yes_button = self.query_item("#connectionAlreadySetupFooter #yesButton")
            yes_button.mouse_click()
        except:
            logging.info("Wifi is not already connected")
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action(password,"#passwordTextField")
        time.sleep(1)
        self.goto_submit_password_screen()
        self.goto_confirm_settings_screen()
        logging.info("At incorrect password screen")
        self._spice.wait_for("#IncorrectPasswordView")
        retryButton = self._spice.query_item("#wizardCompletionFooter #retryButton")
        retryButton.mouse_click()
        assert self._spice.wait_for("#enterPasswordView")
        time.sleep(1)
        self.goto_enter_password_screen()



    def goto_enter_password_screen_oobe(self):
        ''' Click wifi select SSID,enter password '''      
        
        self.goto_enter_password_screen()
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("print123","#passwordTextField")
        time.sleep(1)
        self.goto_submit_password_screen()
        self.goto_confirm_settings_screen()
        self._spice.wait_for("#oobeNetworkSummary")
        time.sleep(1)

    def goto_cancel_button_on_password_screen(self):
        ''' Click WSW select SSID,enter password and click on cancel '''  
        
        logging.info("At enter password screen")
        self.goto_enter_password_screen()
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("abcd","#passwordTextField")
        time.sleep(3)
        logging.info("At enter password submit screen")
        self._spice.wait_for("#enterPasswordView")
        cancelButton = self._spice.query_item("#cancelButton")
        cancelButton.mouse_click()
        time.sleep(2)
        assert self._spice.wait_for("#connectivity_selectNetworkName")
        backButton = self._spice.query_item("#BackButton")
        backButton.mouse_click()
        self._spice.goto_homescreen()