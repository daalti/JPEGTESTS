
import logging
import time

from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

class MenuAppProSelectUILoOperations(MenuAppProSelectUIOperations):

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
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(spice)

    def has_lock_icon(self, spice):
        """
        Starting from Home Screen
        """
        self.goto_menu(spice)
        menu_supplies_icon_id =  "#a5e59604-d216-4977-a901-4774fcacbcb4MenuButton #ContentItem SpiceImage"
        current_screen = spice.wait_for("#MenuListLayout")
        for i in range(3):
            current_screen.mouse_wheel(180, 180)

        lock_icon = spice.wait_for(menu_supplies_icon_id)

        return lock_icon["width"] > 0
    
    def goto_menu_settings_printerUpdate_autoUpdateOptions(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        self.menu_navigation(spice, "#autoFirmwareUpdate", "#SetPrinterUpdateMode")
        assert spice.wait_for("#afuDsMsg")
        logging.info("At Printer Update IRIS Message Screen")
        
    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        currentScreen = spice.wait_for("#afuDsMsg")
        self._spice.homeMenuUI().menu_navigation(self._spice, "#afuDsMsg", "#nextButton")
        assert spice.wait_for("#printerUpdateOptions")
        logging.info("At printer update options Screen")
        time.sleep(1)
        
    def set_printerUpdate_allowAutoUpdate_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        self.menu_navigation(spice, "#printerUpdateOptions", "#installAutomatically")
        current_screen = spice.wait_for("#PrivacyNotice")
        while (spice.query_item("#PrivacyNotice")["visible"] == True):
            current_screen.mouse_wheel(180, 180)
            ok_button = spice.wait_for("#Continue")
            ok_button.mouse_click()
            if(spice.wait_for("#autoFirmwareUpdate")["visible"] == True):
                break

        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("At printer update Screen")
        time.sleep(1)
        
    def set_printerUpdate_notifyWhenAvailable_navigation(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        self.menu_navigation(spice, "#printerUpdateOptions", "#RadioButtonListLayout #SpiceRadioButton", True, 1, 1)
        current_screen = spice.wait_for("#PrivacyNotice")
        while (spice.query_item("#PrivacyNotice")["visible"] == True):
            current_screen.mouse_wheel(180, 180)
            ok_button = spice.wait_for("#Continue")
            ok_button.mouse_click()
            if(spice.wait_for("#autoFirmwareUpdate")["visible"] == True):
                break
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("Set Notifywhen available to true")
        time.sleep(1)
    
    def set_printerUpdate_doNotCheck_navigation(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        self.menu_navigation(spice, "#printerUpdateOptions", "#RadioButtonListLayout #SpiceRadioButton", True, 1, 2)
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("Set donotcheck to true")
        time.sleep(1)
        
    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        currentScreen = spice.wait_for("#afuDsMsg")
        self._spice.homeMenuUI().menu_navigation(self._spice, "#afuDsMsg", "#nextButton")
        assert spice.wait_for("#printerUpdateOptions")
        logging.info("At printer update options Screen")

    def goto_menu_job_queue_app(self, spice):
        self.goto_menu_status(spice)

    def check_inactivity_timeout_options_visible(self, spice):
        """
        Check timeout options shows in inactivity timeout screen.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_30sec)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_1min)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_2mins)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_5mins)["visible"] == True

    def selected_inactivity_value_locator(self, spice, selected_value):
        '''
        Verifying Inactivity Value Locator
            inactivity_value: 30/60/120/300
        '''
        spice.wait_until(lambda: spice.wait_for(
            f"{MenuAppWorkflowObjectIds.menu_button_inactivity_Timeout_option_pro} {MenuAppWorkflowObjectIds.inactivity_timeout_text_view_proselect}")[
            "visible"])
        selected_value_locator = spice.query_item(
            f"{MenuAppWorkflowObjectIds.menu_button_inactivity_Timeout_option_pro} {MenuAppWorkflowObjectIds.inactivity_timeout_text_view_proselect}")[
            "text"]
        logging.info("\n Selected value locator'{}':".format(selected_value_locator))
        assert selected_value_locator == selected_value, "Selected inactivity timeout value failed!!!"


    def verify_selected_inactivity_timeout_value(self, spice, inactivity_value,isEnterPriseProduct=False):
        '''
        This is helper method to verify selected inactivity timeout value
        UI flow Menu > Settings > General > Inactivity Timeout
        Args: inactivity_value: 30/60/120/300
        '''
        if inactivity_value == 30:
            spice.homeMenuUI().selected_inactivity_value_locator(spice, '30 Seconds')
        elif inactivity_value == 60:
            spice.homeMenuUI().selected_inactivity_value_locator(spice, '1 Minute')
        elif inactivity_value == 120:
            spice.homeMenuUI().selected_inactivity_value_locator(spice, '2 Minutes')
        elif inactivity_value == 300:
            spice.homeMenuUI().selected_inactivity_value_locator(spice, '5 Minutes')
        else:
            assert False, "invalid inactivity timeout"

        assert spice.query_item(f"{MenuAppWorkflowObjectIds.menu_button_inactivity_Timeout_option_pro} {MenuAppWorkflowObjectIds.inactivity_timeout_text_view_proselect}")[
                "visible"], "Failed to verify selected inactivity timeout value in UI."

        assert spice.query_item(
                f"{MenuAppWorkflowObjectIds.menu_button_inactivity_Timeout_option_pro} {MenuAppWorkflowObjectIds.inactivity_timeout_text_view_proselect}")[
                "text"], "Failed to verify selected inactivity timeout value in UI."
        

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

    def goto_restorefactorydefaults_popuprestore(self,spice):
        spice.homeMenuUI().goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_mfp(spice)
        spice.common_operations.goto_item("#RestoreButton")

