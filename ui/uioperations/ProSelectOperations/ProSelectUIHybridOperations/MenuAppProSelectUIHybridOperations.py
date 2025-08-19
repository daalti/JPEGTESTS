import logging
import time

from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import ProSelectHybridKeyboardOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIObjectIds import MenuAppProSelectUIObjectIds

class MenuAppProSelectUIHybridOperations(MenuAppProSelectUIOperations):

    view_service = "#MenuListservice"

    inactivity_shutdown_options_dict = {
        "20 Minutes": [MenuAppWorkflowObjectIds.twenty_minutes_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_20mins_pro],
        "1 Hour": [MenuAppWorkflowObjectIds.one_hour_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_1hrs_pro],
        "2 Hours": [MenuAppWorkflowObjectIds.two_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_2hrs_pro],
        "3 Hours": [MenuAppWorkflowObjectIds.three_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_3hrs_pro],
        "4 Hours": [MenuAppWorkflowObjectIds.four_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_4hrs_pro],
        "5 Hours": [MenuAppWorkflowObjectIds.five_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_5hrs_pro],
        "6 Hours": [MenuAppWorkflowObjectIds.six_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_6hrs_pro],
        "7 Hours": [MenuAppWorkflowObjectIds.seven_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_7hrs_pro],
        "8 Hours": [MenuAppWorkflowObjectIds.eight_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_8hrs_pro],
        "Never": [MenuAppWorkflowObjectIds.never_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_never_pro]
    }

    def __init__(self, spice):
        super().__init__(spice)
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.proselect_common_operations = ProSelectCommonOperations(spice)
        self.proselect_keyboard_hybrid_operations = ProSelectHybridKeyboardOperations(spice)

    def goto_menu_print(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuButton")
        assert spice.wait_for("#MenuList02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
        logging.info("At Print Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_keytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceKeyTestMenuMenuButton")

    def goto_menu_tools_servicemenu_systemconfiguration_serialnumber(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#systemConfigurationSerialNumberMenuMenuButton")

        assert spice.wait_for("#serialNumberView")
        logging.info("At Service Id Menu")
        time.sleep(1)

    def goto_menu_tools_servicemenu_systemconfiguration_serviceid(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#systemConfigurationServiceIdMenuMenuButton")
        assert spice.wait_for("#serviceIdEditorView")
        logging.info("At Service Id Menu")
        time.sleep(1)

    def goto_menu_tools_servicemenu_information(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#informationMenuMenuButton")

    def goto_menu_tools_servicemenu_information_servicecounts(self, spice, udw):
        self.goto_menu_tools_servicemenu_information(spice, udw)
        self.menu_navigation(spice, "#MenuListinformationMenu", "#serviceCountsMenuButton")

        assert spice.wait_for("#serviceCountsView")
        logging.info("At Service Counts Screen")
        time.sleep(1)

    def get_current_serviceID_SystemConfigMenu(self, spice):
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def set_wrong_serviceID_SystemConfigMenu(self, spice, SERVICE_ID,net):
        self.menu_navigation(spice, "#serviceIdEditorView", "#setButton")
        keyboardTextField = self._spice.query_item("#serviceIdEditorView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = SERVICE_ID
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        assert spice.wait_for("#ConstraintMessage #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid service id entry message")
        okbutton= spice.wait_for("#MessageLayout #okButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.wait_for("#serviceIdEditorView #hybridKeyboardTextInputArea")["inputText"]

    def update_serviceID_SystemConfigMenu(self,spice, UPDATED_SID, net):
        keyboardTextField = self._spice.query_item("#serviceIdEditorView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = UPDATED_SID
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful service id message")
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def update_new_serviceID_SystemConfigMenu(self, spice,new_serice_id,net):
        self.menu_navigation(spice, "#serviceIdEditorView", "#setButton")
        keyboardTextField = self._spice.query_item("#serviceIdEditorView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = new_serice_id
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationFailedText", "en")),"Operation failed message is not visible"
        logging.info("Validating Operation failed service id message")
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()

    def set_wrong_serialNumber_SystemConfigMenu(self, spice, NEW_SN,net):
        self.menu_navigation(spice, "#serialNumberView", "#setButton")
        keyboardTextField = self._spice.query_item("#serialNumberView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = NEW_SN
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        assert spice.wait_for("#ConstraintMessage #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid serial number entry message")
        okbutton= spice.wait_for("#MessageLayout #okButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.wait_for("#serialNumberView #hybridKeyboardTextInputArea")["inputText"]

    def updatewrong_serialNumber_SystemConfigMenu(self, spice,UPDATE_SN,net):
        keyboardTextField = self._spice.query_item("#serialNumberView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = UPDATE_SN
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful serial number message")
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def validate_restore_network_settings(self,spice,net):
        assert spice.wait_for("#RestoreNetworkSettingView #DetailTexts #Version2Text") ["text"] == str(LocalizationHelper.get_string_translation(net,"cRestoreOriginalSettings", "en"))
        logging.info("Validating the Restorenetworksettings confirmation text")
        yesbutton = spice.wait_for("#nativeStackView #RestoreNetworkSettingView #Yes #SpiceButton")
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_click()
        time.sleep(2)
        assert spice.wait_for("#RestoreNetworkSettingSuccess #DetailTexts #Version2Text",15) ["text"] == str(LocalizationHelper.get_string_translation(net,"cNetworkDefaultsRestored", "en"))
        logging.info("Validated the Restorenetworksettings success message")
        spice.wait_for("#nativeStackView #RestoreNetworkSettingSuccess #OK #SpiceButton",10).mouse_click()
        logging.info("Performed the okay operation")


    def set_serialNumber_SystemConfigMenu(self, spice, NEW_SN):
        #select "Set"
        self.menu_navigation(spice, "#serialNumberView", "#setButton")
        keyboardTextField = self._spice.query_item("#serialNumberView #hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = NEW_SN
        self.proselect_keyboard_hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        assert spice.wait_for("#serialNumberView")

    # Menu Settings General Energy prevent Shutdown

    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        assert spice.wait_for("#energyPreventShutdownMenuSwitch")
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyPreventShutdownMenuSwitch", selectOption=False)
        logging.info("At Energy PreventShutdown Settings Screen")
        return spice.query_item("#energyPreventShutdownMenuSwitch")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyPreventShutdownMenuSwitch")
        logging.info("At Energy PreventShutdown donotdisable Settings Screen")
        time.sleep(1)

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyPreventShutdownMenuSwitch")
        logging.info("At Energy PreventShutdown whenportsare active Settings Screen")
        time.sleep(1)
        
    def select_energy_inactivity_shutdown_value(self, spice, inactivity_shutdown_value):
        '''
        Select an inactivity shutdown value in inactivity shutdown screen.
        Args: inactivity_shutdown_value: inactivity shutdown value
        '''
        logging.info(f"Select energy inactivity shutdown value is <{inactivity_shutdown_value}>")
        item_location = self.inactivity_shutdown_options_dict[inactivity_shutdown_value][1]
        self.proselect_common_operations.goto_item(item_location,MenuAppWorkflowObjectIds.view_energySettings_shutdown_pro)
        time.sleep(2)
        spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_pro)
        logging.info(f"Set Energy Shutdown to <{inactivity_shutdown_value}>")
        
    def verify_inactivity_shutdown_options_list_display_in_ui(self, net, spice, inactivity_shutdown_options):
        """
        UI Workflow should be: Inactivity Shutdown screen
        Verify inactivity shutdown options list display correctly.
        Args: inactivity_shutdown_options: inactivity shutdown options type list
        """
        logging.info("Verify inactivity shutdown options list display in ui")

        for item in inactivity_shutdown_options:
            logging.info(f'To check item: <{item}>')
            cstring_id = self.inactivity_shutdown_options_dict[item][0]
            expected_inactivity_shutdown_value = self.proselect_common_operations.get_expected_translation_str_by_str_id(
                net, cstring_id)
            logging.info(f'The expect inactivity shutdown value is {expected_inactivity_shutdown_value}')

            item_location = self.inactivity_shutdown_options_dict[item][1]
            current_inactivity_shutdown_value = \
                spice.wait_for(f"{item_location} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view_pro}")["text"]
            logging.info(f'The current inactivity shutdown value is {current_inactivity_shutdown_value}')
            assert current_inactivity_shutdown_value == expected_inactivity_shutdown_value, "Check inactivity shutdown value failed!"

        logging.info('The current inactivity shutdown option list display completely and correctly')
        
    def verify_set_inactivity_shutdown_option_display_in_ui(self, spice, inactivity_shutdown_value):
        """
        UI Workflow should be: Energy  Settings screen
        Verify set inactivity shutdown option display correctly.
        Args: inactivity_shutdown_value: inactivity shutdown value
        """
        energy_settings_view = spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_pro)
        spice.wait_until(lambda: energy_settings_view["visible"])

        spice.wait_until(lambda: spice.query_item(
            f"{MenuAppWorkflowObjectIds.menu_button_inactivity_shutdown_option_pro} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view_pro_v}")[
            "visible"])
        current_inactivity_shutdown_option = spice.query_item(
            f"{MenuAppWorkflowObjectIds.menu_button_inactivity_shutdown_option_pro} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view_pro_v}")[
            "text"]
        assert inactivity_shutdown_value == current_inactivity_shutdown_option, "Set inactivity shutdown option failed!!!"

    def goto_menu_job_queue_app(self, spice):
        self.goto_menu_status(spice)

    # Menu Tools Service Menu Service Resets

    def goto_menu_tools_servicemenu_serviceresets_usersettingsreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceResetsUserSettingsResetMenuButton")
        assert spice.wait_for("#UserSettingsResetView")
        logging.info("At User Settings Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_userdatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceResetsUserDataResetMenuButton")
        assert spice.wait_for("#UserDataResetView")
        logging.info("At User Data Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceResetsFactoryDataResetMenuButton")
        assert spice.wait_for("#FactoryResetView")
        logging.info("At Factory Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_repairmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceResetsRepairModeMenuButton")
        assert spice.wait_for("#RepairModeView")
        logging.info("At Repair Mode Screen")
        time.sleep(1)

    def get_service_menu_view(self):
        return self.view_service
    
    def click_network_button(self) -> bool:
        try:
            self._spice.wait_for(MenuAppProSelectUIObjectIds.SettingsView)
        except:
            logging.error(f"Failed to get: {MenuAppProSelectUIObjectIds.SettingsView}")
            return False

        menu_view_list = None
        try:
            menu_view_list = self._spice.wait_for(MenuAppProSelectUIObjectIds.MenuViewList)
        except:
            logging.error(f"Failed to get menu list view: {MenuAppProSelectUIObjectIds.MenuViewList}")
            return False

        timeout = ProSelectCommonOperations.DEFAULT_WAIT_TIME_SECONDS
        button = self._spice.wait_for(MenuAppProSelectUIObjectIds.NetworkButton)
        while not button["activeFocus"] and timeout > 0:
            timeout -= 1
            time.sleep(1)
            menu_view_list.mouse_wheel(180, 0)
            logging.info("=====================================SCROLLING MENU")
            button = self._spice.wait_for(MenuAppProSelectUIObjectIds.NetworkButton)
        
        if not button["activeFocus"]:
            logging.error("==========================================NOT ACTIVE FOCUS")
            return False
        button.mouse_click()
        return True
    
    def is_on_network_page(self) -> bool:
        network_view = None
        try:
            network_view = self._spice.wait_for(MenuAppProSelectUIObjectIds.NetworkView)
        except:
            logging.error(f"Failed to get: {MenuAppProSelectUIObjectIds.NetworkView}")
            return False
        return network_view["visible"]

    def verify_quality_drop_down_menu_items_economode_detailed(self, spice):
        spice.wait_for("#qualityComboBoxpopupList")
        assert spice.wait_for("#ComboBoxOptionsnormalRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionsdetailedRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionseconomodeRadioButtonModel")
    
    def verify_network_menu_item(self, spice): 
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxEthernetMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxAirPrintButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxIPv4EnableButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxIPv6EnableButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxHostNameButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxBonjourNameButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxProxyButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#networkSecuritySettingsMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxNwReportsMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxRNDMenuButton", False)
        