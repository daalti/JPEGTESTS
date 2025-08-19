#########################################################################################
# @file      WifiAppProSelectUIOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      17-11-2020
# @brief     Implementation Network Wifi UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import  sys
import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IWiFiAppUIOperations import IWiFiAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.NetworkAppProSelectUIOperations import NetworkAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.SignInAppProSelectUIOperations import SignInAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations

_logger = logging.getLogger(__name__)

class WifiAppProSelectUIOperations(IWiFiAppUIOperations):
    def __init__(self, spice):
        self._spice = spice
        self.proselect_common_operations = ProSelectCommonOperations(self._spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)
        self.sign_in_app_operations = SignInAppProSelectUIOperations(self._spice)

    def goto_wifi_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi from network
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.debug("Entering wi-fi")
        self.proselect_common_operations.goto_item("#cnxWiFiMenuButton", "#MenuListnetworkSettings")

    def goto_wifi_direct_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct from network
        '''
        self.proselect_common_operations.goto_network_settings_menu()
        _logger.debug("Entering wi-fi Direct")
        self.proselect_common_operations.goto_item("#cnxWFDMenuButton", "#MenuListnetworkSettings")

    def goto_wifi_direct_status_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct status menu from network
        '''
        self.goto_wifi_direct_menu()
        _logger.debug("Entering wi-fi Direct status menu")
        self.proselect_common_operations.goto_item("#cnxWFDStateMenuNameValue")

    def goto_wifi_direct_view_details_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct view deatils menu from network
        '''
        self.goto_wifi_direct_menu()
        _logger.debug("Entering wi-fi Direct view details")
        self.proselect_common_operations.goto_item("#cnxWFDViewDetailsMenuButton")

    def goto_wifi_direct_connection_method_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi Direct connection method from network
        '''
        self.goto_wifi_direct_menu()
        _logger.debug("Entering wi-fi Direct connection methods")
        self.proselect_common_operations.goto_item("#cnxWFDConnectionMethodMenuNameValue")

    def goto_wifi_setup_wizard_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wireless setup wizard screen from wifi menu
        '''
        self.goto_wifi_menu()
        _logger.debug("Entering Wifi wireless wizard screen")
        self.proselect_common_operations.goto_item("#cnxWiFiWSWMenuButton")
        time.sleep(2)
        
    def goto_select_ssid_name_screen(self):
        '''Click on SSID at SSID list'''
        _logger.debug("At select network name screen")
        self._spice.wait_for("#SsidListView")
        self.proselect_common_operations.goto_item("#testSecureAP")
        
    def goto_wifi_already_connected_screen(self, text):
        '''Click on yes at connection already exists screen'''
        _logger.debug("at connection already setup screen")
        self._spice.wait_for("#WSWConnectionAlreadySetup")
        self.proselect_common_operations.goto_item("#yesButton")
        self.goto_select_ssid_name_screen()
        time.sleep(5)
        self.goto_enter_password_screen(text)

    def goto_cancel_button_on_trying_to_connect_screen(self):
        '''click on cancel at WFW, trying to connect screen'''
        _logger.debug("At trying to connect screen")
        self._spice.wait_for("#connectivity_statusTryingToConnectverticalLayout")
        self.proselect_common_operations.goto_item("#cancelButton")
        self._spice.wait_for("#restoreRetainSettingsView")
        self.proselect_common_operations.goto_item("#restoreRetainSettingsViewYes")
        self._spice.wait_for("#restoredView")
        self.proselect_common_operations.goto_item("#restoredViewOk")
        time.sleep(1)
    
    def goto_enter_network_name_screen(self,text:str):
        '''
        click on enter name and click on the filed to type SSID
        Args:
          text: text to be entered
        '''
        _logger.debug("At enter network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        self.proselect_common_operations.goto_item("#enterNetworkNameCard")
        self._spice.wait_for("#enterNetworkNameView")
        self.proselect_common_operations.goto_item("#enterNetworkNameTextField")
        self.proselect_keyboard_operations.keyboard_enter_text("testSecureAP",True)
        time.sleep(5)
        self.proselect_common_operations.goto_item("#connectButton")#or cancelButton
        time.sleep(1)

    def goto_enter_network_name_screen_cancel(self, text:str):
        '''
        click on enter name and click on the filed to type SSID
        Args:
          text: text to be entered
        '''
        _logger.debug("At enter network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        self.proselect_common_operations.goto_item("#enterNetworkNameCard")
        self._spice.wait_for("#enterNetworkNameView")
        self.proselect_common_operations.goto_item("#enterNetworkNameTextField")
        self.proselect_keyboard_operations.keyboard_enter_text("testSecureAP",True)
        time.sleep(5)
        _logger.debug("At select network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        self.proselect_common_operations.goto_item("#BackButton")
        time.sleep(1)

    def goto_enter_network_name_screen_oobe_incorrect(self):
        '''click on enter name and click on the filed to type SSID'''
        _logger.debug("At enter network name screen")
        self._spice.wait_for("#connectivity_selectNetworkName")
        self.proselect_common_operations.goto_item("#enterNetworkNameCard")
        self._spice.wait_for("#enterNetworkNameView")
        self.proselect_common_operations.goto_item("#enterNetworkNameTextField")
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("testSecure","#enterNetworkNameTextField")
        self.proselect_common_operations.goto_item("#connectButton")#or cancelButton
        time.sleep(1)
        self._spice.wait_for("#DirectedScanInProgress")
        self.proselect_common_operations.goto_item("#cancelButton")
        time.sleep(2)
    
   
    def goto_connect_button_on_enter_network_name_screen(self):
        '''click on connect at enter network name  screen '''
        _logger.debug("At enter network name screen")
        self._spice.wait_for("#enterNetworkNameView")
        self.proselect_common_operations.goto_item("#cancelButton")
        time.sleep(1)

    def goto_enter_password_screen(self, text : "print123"):
        '''enter password screen type password submit password,confirm password for ssid'''
        _logger.debug("At enter password screen")
        self._spice.wait_for("#EnterWEPWPAPasswordView")
        self.proselect_keyboard_operations.keyboard_enter_password(text)
        _logger.debug("At enter confirm settings screen")
        self._spice.wait_for("#ConfirmSettingsView")
        self.proselect_common_operations.goto_item("#okButton")
        time.sleep(3)#TODO need to update sleep
        #self.goto_network_success_screen()

    def goto_enter_incorrect_password_WSW(self):
        '''enter password screen type password submit password,confirm password for oobe ssid'''
        _logger.debug("At enter password screen")
        self._spice.wait_for("#enterPasswordView")
        self.proselect_common_operations.goto_item("#passwordTextField")
        self._spice.keyBoard.keyboard_set_text_with_out_dial_action("print345","#passwordTextField")
        _logger.debug("At enter password submit screen")
        self._spice.wait_for("#enterPasswordView")
        self.proselect_common_operations.goto_item("#submitButton")
        _logger.debug("At enter confirm settings screen")
        self._spice.wait_for("#connectivity_confirmSettings")
        self.proselect_common_operations.goto_item("#okButton")#showpasswordButton
        _logger.debug("At incorrect password screen")
        self._spice.wait_for("#IncorrectPasswordViewverticalLayout")
        self.proselect_common_operations.goto_item("#retryButton")
        #self.goto_network_success_screen()


    def goto_submit_password_screen(self):
        '''click om submit  at password screen'''
        _logger.debug("At enter password submit screen")
        self._spice.wait_for("#enterPasswordView")
        self.proselect_common_operations.goto_item("#submitButton")
        time.sleep(2)

    def goto_cancel_password_screen(self,spice):
        '''click on cancel at password screen'''
        _logger.debug("At enter password cancel screen")
        spice.wait_for("#enterPasswordView")
        self.proselect_common_operations.goto_item("#cancelButton")
        time.sleep(2)

    def goto_confirm_settings_screen(self):
        '''click on ok at confirm settings screen'''
        _logger.debug("At enter confirm settings screen")
        self._spice.wait_for("#connectivity_confirmSettings")
        self.proselect_common_operations.goto_item("#okButton")#showpasswordButton
        time.sleep(12)

    def goto_network_success_screen(self):
        '''click on continue at network sucess screen'''
        _logger.debug("At n/w sucess screen")
        self._spice.wait_for("#oobeNetworkSuccessView")
        self.proselect_common_operations.goto_item("#continueButton")
        time.sleep(10)

        
    def goto_manual_ipv4_config_ip_address(self, spice):
        '''click on Manual IP field at manual ip config screen'''
        _logger.debug("At IP Configuration screen manual ip")
        spice.wait_for("#manualIPConfigurationView")
        self.proselect_common_operations.goto_item("#nwIPField")
        time.sleep(1)

    def goto_manual_ipv4_config_subnet_mask(self):
        '''click on subnet mask field at manual ip config screen'''
        _logger.debug("At Ip Configuration screen subnet mask")
        self._spice.wait_for("#manualIPConfigurationView")
        self.proselect_common_operations.goto_item("#nwSubnetField")
        time.sleep(1)

    def goto_manual_ipv4_config_default_gateway(self):
        '''click on default gateway field at manual ip config screen'''
        _logger.debug("At Ip Configuration screen default gateway")
        self._spice.wait_for("#manualIPConfigurationView")
        self.proselect_common_operations.goto_item("#nwGatewayField")
        time.sleep(1)

    def goto_band_frequency_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wifi band frequency
        '''
        self.goto_wifi_menu()
        _logger.debug("Entering Wifi wireless wizard screen")
        self.proselect_common_operations.goto_item("#cnxWiFiBandMenuNameValue", "#MenuListcnxWiFi")
        time.sleep(2)

    def goto_wifi_wireless_protected_setup(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wireless protected setup screen
        '''
        self.goto_wifi_menu()
        _logger.debug("Entering in to WPS screen")
        self.proselect_common_operations.goto_item("#cnxWiFiWPSMenuButton", "#MenuListcnxWiFi")
        time.sleep(2)

    def goto_wifi_view_details_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to wi-fi view details from wifi menu
        '''
        self.goto_wifi_menu()
        _logger.debug("Entering wi-fi view details")
        self.proselect_common_operations.goto_item("#cnxWiFiDetailsMenuButton", "#MenuListcnxWiFi")
        time.sleep(2)

    def goto_wifi_ipv4_menu(self):
        '''
        UI should be on home screen before calling this method
        Navigate to ipv4 config menthod from wifi menu
        '''
        self.goto_wifi_menu()
        _logger.debug("Entering wi-fi view details")
        self.proselect_common_operations.goto_item("#cnxWiFiIPMenuNameValue", "#MenuListcnxWiFi")
        time.sleep(2)

    def goto_network_success_screen_wifi(self):
        '''click on continue at network success screen'''
        _logger.debug("At n/w success screen")
        self._spice.wait_for("#ConnectionSuccessful")
        self.proselect_common_operations.goto_item("#okButton")#printReportButton

    def configure_wireless_by_selecting_ssid(self, text):
        ''' Click WSW select SSID,enter password '''    
        self.goto_select_ssid_name_screen()
        self.goto_enter_password_screen(text)
        self.goto_network_success_screen_wifi()

    def check_generic_confirmation_wifi_screen(self):
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        assert self._spice.query_item("#SsidListView")
        self.proselect_common_operations.goto_item("#EnterNetworkName")
        time.sleep(2)
        keyboardTextField = self._spice.query_item("#spiceKeyboardView", 0)
        keyboardTextField["currentText"] = "hp.inc.com"
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        self.proselect_common_operations.goto_item("#CancelButton")
        assert self._spice.query_item("#spiceKeyboardView")
        self.proselect_keyboard_operations.keyboard_press_icon("#ItemIconDelegateclose_xs",dial_val=0)
        exitbtn = self._spice.wait_for("#ExitButton")
        exitbtn.mouse_wheel(180,180)
        exitbtn.mouse_wheel(180,180)
        exitbtn.mouse_click()
        assert self._spice.wait_for("#SettingsAppApplicationStackView #SsidListView")

    def set_enter_network_name_confirmation(self):
        ''' Enter the newtwork name confirmation '''  
        new_network_name = "hp.com"
        updated_network_name = "hpinc.com"
        self.proselect_common_operations.goto_item("#EnterNetworkName")
        time.sleep(2)
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(new_network_name)
        self.home_menu_dial_operations.menu_navigation(self._spice,"#EnterNetworkNameView","#CancelButton")
        self.proselect_common_operations.goto_item("#EnterNetworkName")
        time.sleep(2)
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(updated_network_name)
        assert self._spice.wait_for("#DetailTexts #Version2Text")["text"] == "You have entered: hpinc.com"
        confirmbtn = self._spice.wait_for("#EnterNetworkNameView #ConfirmButton")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()