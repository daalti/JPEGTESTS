import sys
import logging
import time
from dunetuf.power.power import Power
from dunetuf.ui.uioperations.BaseOperations.IOOBEAppUIOperations import IOOBEAppUIOperations
from dunetuf.cdm import *
from selenium.common.exceptions import TimeoutException
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.keypad import KeypadController
from dunetuf.emulation.print.print_emulation_ids import DuneEngineMake


class OOBEAppWorkflowUICommonOperations(IOOBEAppUIOperations):
    """A class for all OOBE workflow common operations

    Args:
        spice: spice instance
    """
    device_language = { "option_en" : "en"    , "option_es" : "es"    , "option_de" : "de"    , "option_ar" : "ar"    , "option_ca" : "ca",
                        "option_cs" : "cs"    , "option_da" : "da"    , "option_el" : "el"    , "option_fi" : "fi"    , "option_fr" : "fr",
                        "option_hr" : "hr"    , "option_hu" : "hu"    , "option_id" : "id"    , "option_it" : "it"    , "option_ko" : "ko" ,
                        "option_nl" : "nl"    , "option_nb" : "nb"    , "option_pl" : "pl"    , "option_pt" : "pt"    , "option_ru" : "ru",
                        "option_sk" : "sk"    , "option_sl" : "sl"    , "option_sv" : "sv"    , "option_th" : "th"     , "option_tr" : "tr",
                        "option_ro" : "ro"    , "option_ja" : "ja"    , "option_he" : "he"    , "option_zh-CN" : "zh_dash_CN"   , "option_zh-TW" : "zh_dash_TW",}

    def __init__(self, spice):
        self.spice = spice
        self.ipaddress = self.spice.ipaddress
        self.cdm = CDM(self.ipaddress)
        self.workflow_common_operations = WorkflowUICommonOperations(spice)

    def clickPositionXInList(self, spice, objectName, position=0):
        listElements = spice.wait_for(objectName)
        listElements.__setitem__("_indexPosition", position)
        listElements.mouse_click()

    def select_first_language(self, spice) -> None:
        spice.wait_for("#DeviceLanguageView")
        self.clickPositionXInList(spice, "#DeviceLanguageView #SpiceListViewView")

        spice.wait_for("#langConfirmPopup")
        confirmButton = spice.wait_for("#ConfirmButton")
        confirmButton.mouse_click()

    def select_first_altitude(self, spice) -> None:
        spice.wait_for("#oobeAltitudeView")
        altitudeFirstPosition = spice.wait_for("#altitudeTextImageBranch0")
        altitudeFirstPosition.mouse_click()

    def accept_network_sumary(self, spice) -> None:
        spice.wait_for("#oobeNetworkSummary")
        continue_button = spice.wait_for("#oobeNetworkSummary #continueButton")
        spice.wait_until(lambda: continue_button["enabled"] == True)
        continue_button.mouse_click()

    def wait_internet_connection(self, spice) -> None:
        spice.wait_for("#oobeConnectionPermission")

    def accept_share_printer_analytics(self, spice, cdm) -> None:
        """
        Waits for 'Share Printer Analytics' screen and clicks the 'Yes' button
        Verify that actionHpCloudServicesPrompt is completed in the CDM 'Device Setup Status' endpoint
        Verify that telemetryConsent is accepted in the CDM 'Telemetry consent' endpoint

        Args:
            spice: The Spice object
            cdm: The CDM object
        """
        spice.wait_for("#oobeSharePrinterAnalytics")
        continue_button = spice.wait_for("#oobeSharePrinterAnalytics #yesButton")
        continue_button.mouse_click()

        # wait for a moment so the CDM is patched
        time.sleep(1)

        # verify action from CDM
        cdm_value = cdm.get(cdm.DEVICE_SETUP_STATUS)
        telemetry_status = cdm_value["actionHpCloudServicesPrompt"]["status"]
        assert telemetry_status == "completed", f"actionHpCloudServicesPrompt should be completed, but got {telemetry_status}"

        # verify consent from CDM
        cdm_value = cdm.get(cdm.TELEMETRY_CONSCENT)
        consent_state = cdm_value["telemetryConsent"]["consentState"]
        assert consent_state == "accepted", f"telemetryConsent should be accepted, but got {consent_state}"

    def decline_share_printer_analytics(self, spice, cdm) -> None:
        """
        Waits for 'Share Printer Analytics' screen and clicks the 'No' button
        Verify that actionHpCloudServicesPrompt is completed in the CDM 'Device Setup Status' endpoint
        Verify that telemetryConsent is declined in the CDM 'Telemetry consent' endpoint

        Args:
            spice: The Spice object
            cdm: The CDM object
        """
        spice.wait_for("#oobeSharePrinterAnalytics")
        continue_button = spice.wait_for("#oobeSharePrinterAnalytics #noButton")
        continue_button.mouse_click()

        # wait for a moment so the CDM is patched
        time.sleep(1)

        # verify action from CDM
        cdm_value = cdm.get(cdm.DEVICE_SETUP_STATUS)
        telemetry_status = cdm_value["actionHpCloudServicesPrompt"]["status"]
        assert telemetry_status == "completed", f"actionHpCloudServicesPrompt should be completed, but got {telemetry_status}"

        # verify consent from CDM
        cdm_value = cdm.get(cdm.TELEMETRY_CONSCENT)
        consent_state = cdm_value["telemetryConsent"]["consentState"]
        assert consent_state == "declined", f"telemetryConsent should be declined, but got {consent_state}"

    def skip_critical_fw_update(self, spice) -> None:
        spice.wait_for("#CheckingForUpdates")
        skip_button = spice.wait_for("#CheckingForUpdates #skipButton")
        skip_button.mouse_click()

    def skip_cloud_registration(self, spice) -> None:
        spice.wait_for("#RetrieveCode")
        cancel_button = spice.wait_for("#RetrieveCode #cancelButton")
        cancel_button.mouse_click()

        spice.wait_for("#SkipPairingPopup")
        skip_button = spice.wait_for("#SkipPairingPopup #Skip")
        skip_button.mouse_click()

    def goto_language_screen(self, spice) -> None:
        """Selects 'ok' on Setup Incomplete screen if presented in oobe flow and go to language screen.

            Args:
            spice: spice instance
            Returns:
            None
        """
        try:
            # Handler for Event Screen(55.00.08)
            event_screen = spice.wait_for("#systemEventErrorView #OK")
            event_screen.mouse_click()
            logging.info("After handling Event Screen")

            # Handler for Setup Incomplete Screen and Original HP Cartridge screen
            for i in range(2):
                message_screen = spice.wait_for(
                    '#AlertModelView #AlertFooter #OK')
                message_screen.mouse_click()
                time.sleep(1)

        except Exception as e:
            #logging.info('Exception occured : {}'.format(e))
            logging.info("OOBE workflow loaded without Event screen")
            time.sleep(1)

            try:
                # Handler for Setup Incomplete Screen and Original HP Cartridge screen
                for i in range(2):
                    message_screen = spice.wait_for(
                        '#AlertModelView #AlertFooter #OK')
                    message_screen.mouse_click()
                    time.sleep(1)

            except:
                # Handler for Simulator. Loaded without Event or Alert Screen generally.
                logging.info(
                    "Device launched with out any Event or Alert screen")
                time.sleep(1)

        logging.info("Entering Language Screen")
        assert spice.wait_for("#DeviceLanguageView")
        logging.info("At Language Screen")
        time.sleep(2)

    # English languague objectName - "#dune::spice::glossary_1::Language::Language.en" -Initial values

    def goto_language_confirmation_screen(self, spice, language="#DeviceLanguageView #DeviceLanguageViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView") -> None:
        """Selects the language in oobe flow and go to language confirmation screen

        Args:
            spice: spice instance
            language: objectName of the language list
        Returns:
            None
        """
        self.goto_language_screen(spice)

        # TBD: need to enable scrolling
        # spice.homeMenuUI().menu_navigation(spice, "#RadioButtonListLayout", language)

        languageList = spice.wait_for(language)

        # Set the index position based on the language to be set
        languageList.__setitem__("_indexPosition", "0")
        languageList.mouse_click()

        # Language Confirmation Screen
        logging.info("Entering Language Confirmation Screen")
        assert spice.wait_for("#langConfirmPopup")
        logging.info("At Language Confirmation Screen")
        time.sleep(2)

    def select_confirm_language(self, spice):
        """On language confirmation screen mouse click confirm button

        Args:
            spice: spice instance
        Returns:
            None
        """
        self.goto_language_confirmation_screen(spice)
        confirmButton = spice.wait_for("#ConfirmButton")
        confirmButton.mouse_click()

    def select_language_eng(self, spice):
        """On language screen mouse click language tab

        Args:
            spice: spice instance
        Returns:
            None
        """
        self.goto_language_screen(spice)
        language="#DeviceLanguageView #DeviceLanguageViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView"
        languageList = spice.wait_for(language)
        languageList.__setitem__("_indexPosition", "0")
        languageList.mouse_click()

    def goto_country_screen(self, spice, udw=None, language="en"):
        """Confirm the language  on oobe flow and goto Country screen

        Args:
            spice: spice instance
            udw: underware instance
        Returns:
            None
        """
        runner = self.select_confirm_language

        if udw != None:
            pe_engine_make = udw.mainApp.execute("ConnectorDriver PUB_getEngineMake")
            engine_make = DuneEngineMake(int(pe_engine_make)).name

            if engine_make == DuneEngineMake.canonHomepro.name:
                logging.info("Experience is [WorkflowSMB]")
                runner = self.select_language_eng

        runner(spice)

        # Country Selection Screen
        logging.info("Entering Country Screen")
        assert spice.wait_for("#OobeCountryRegionView")
        logging.info("At Country Screen")
        time.sleep(4)

    # 223 = United States -Initial value

    def goto_more_country_list_screen(self, spice, udw):
           """Select more country option on country list flow and go to more country list screen

           Args:
               spice: spice instance
               country: objectName of country list
           Returns:
               None
           """
           self.goto_country_screen(spice, udw)
           countryList = spice.wait_for("#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView")
           time.sleep(2)

           # TBD: need to enable scrolling
           # Set the index position based to click on More Countries
           countryList.__setitem__("_indexPosition", "30")
           spice.wait_for("#MoreCountryRegion").mouse_click()
           time.sleep(1)


    def select_country_from_more_country_list_screen(self, spice, cdm, udw,
            country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView") -> None:
           """Select the country from more country list on oobe flow and verify status of actionLanguageCountry"""

           self.goto_more_country_list_screen(spice, udw)
           countryList = spice.wait_for(country)
           # Set the index position based on the country to be set
           countryList.__setitem__("_indexPosition", "28")
           countryList.mouse_click()
           time.sleep(1)

           #Verify from CDM
           devicesetup_endpoint = "cdm/deviceSetup/v1/status"
           cdmvalue = cdm.get(devicesetup_endpoint)
           time.sleep(1)
           logging.info(cdmvalue["actionLanguageCountry"]["status"])
           assert cdmvalue["actionLanguageCountry"]["status"] == "completed"
           time.sleep(4)


    def goto_altitude_screen(self, spice, udw,
            country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView") -> None:
        """Select the country on oobe flow and goto altitude screen

        Args:
            spice: spice instance
            country: objectName of country list
        Returns:
            None
        """
        self.goto_country_screen(spice, udw)
        # TBD: need to enable scrolling
        countryList = spice.wait_for(country)

        # Set the index position based on the country to be set
        countryList.__setitem__("_indexPosition", "0")
        countryList.mouse_click()

        # Altitude Settings Screen
        logging.info("Entering Altitude Setting Screen")
        assert spice.wait_for("#oobeAltitudeView")
        logging.info("At Altitude Setting Screen")
        time.sleep(4)

    def goto_oobe_ipv4_screen(self, spice, udw, option="#ipConfigComboBox"):
        self.goto_network_settings_screen(spice, udw)
        spice.wait_for("#oobeNetworkSummary")
        ip_config_button = spice.wait_for(option)
        ip_config_button.mouse_click()

    def validate_ip_config_view(self, spice):
        assert spice.wait_for("#SettingsSpiceComboBoxpopup")

    def select_manual_ip_option(self, spice, udw):
        """Select manual ip option on ipv4 screen """
        self.goto_oobe_ipv4_screen(spice, udw)
        button = spice.wait_for("#ipv4ConfigManual")
        button.mouse_click()

    def validate_manual_ip_view(self, spice):
        assert spice.wait_for("#manualIpSettings")

    def goto_network_settings_screen(
        self, spice, udw=None,
        altitude="#oobeAltitudeView #oobeAltitudeViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView",
        country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView"
    ) -> None:
        """Select the altitude on oobe flow and goto network screen

        Args:
            spice: spice instance
            udw: underware instance
            altitude: objectName of altitude list
            country: objectName of country list
        Returns:
            None
        """
        response = self.cdm.get("cdm/deviceSetup/v1/status")

        if "actionAltitudeConfiguration" in response:
            self.goto_altitude_screen(spice, udw)
            altitudeList = spice.wait_for(altitude)

            # Set the index position based on the altitude to be set
            altitudeList.__setitem__("_indexPosition", "0")
            altitudeFirstPosition = spice.wait_for("#altitudeTextImageBranch0")
            altitudeFirstPosition.mouse_click()
        else:
            self.goto_country_screen(spice, udw)
            countryList = spice.wait_for(country)

            # Set the index position based on the country to be set
            countryList.__setitem__("_indexPosition", "0")
            countryList.mouse_click()

        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#oobeNetworkSummary")
        logging.info("At Network Setting Screen")
        time.sleep(4)


    def goto_proxy_settings_screen(self, spice, option="#continueButton") -> None:
        """Select the continue in network settings screen of  oobe flow and goto proxy settings screen

        Args:
            spice: spice instance
            option: object id of continue button
        Returns:
            None
        """
        self.goto_network_settings_screen(spice)
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()

        # Proxy Screen
        logging.info("Entering Proxy Settings Screen")
        assert spice.wait_for("#oobeProxyBanner")
        logging.info("At Proxy Settings Screen")
        time.sleep(4)

    def verify_oobe_language_cancel(self, spice, udw, cdm, locale, oobe):
        try:

            # Select English and got to Language confirmation screen
            self.goto_language_confirmation_screen(spice)

            # Validate displayed text
            confirmationText = spice.query_item(
                "#alertDetailDescription #contentItem")["text"]
            assert confirmationText == "You have selected \"English\" as your language."

            # Click Cancel Button
            cancelButton = spice.wait_for("#CancelButton")
            cancelButton.mouse_click()

            # Verify Ui transitions back to Language selection page
            assert spice.wait_for("#DeviceLanguageView")

        finally:
            # Disable the OOBE workflow
            oobe.oobe_operations.disable_oobe(udw)

    def verify_oobe_language_country(self, spice, udw, cdm, locale, oobe):
        try:
            configuration_endpoint = "cdm/system/v1/configuration"
            devicesetup_endpoint = "cdm/deviceSetup/v1/status"

            # Select English and got to Language confirmation screen
            self.goto_language_confirmation_screen(spice)

            # Validate displayed text
            confirmationText = spice.query_item(
                "#alertDetailDescription #contentItem")["text"]
            assert confirmationText == "You have selected \"English\" as your language."

            # Click Confirm Button
            cancelButton = spice.wait_for("#ConfirmButton")
            cancelButton.mouse_click()

            # Verify Ui transitions to country selection screen
            assert spice.wait_for("#OobeCountryRegionView")

            # Check the configuration_endpoint to see if the language is reflecting
            cdmvalue = cdm.get(configuration_endpoint)
            assert cdmvalue["deviceLanguage"] == "en"
            time.sleep(2)

            # objectName of country list
            country = "#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView"
            countryList = spice.wait_for(country)

            # Set the index position US from the list
            countryList.__setitem__("_indexPosition", "0")
            countryList.mouse_click()
            time.sleep(2)

            # Check the configuration_endpoint to see if the language is reflecting
            cdmvalue = cdm.get(configuration_endpoint)
            logging.info(cdmvalue["countryRegion"])
            assert cdmvalue["countryRegion"] == "US"

        finally:
            # Disable the OOBE workflow
            oobe.oobe_operations.disable_oobe(udw)

    def power_cycle(self, udw):
        logging.info("Entering power_cycle on Workflow UI")
        powerObj = Power(udw)
        response = powerObj.power_cycle()

    def goto_connect_to_internet_screen(self, spice, option="#skipButton") -> None:
        """Select skip  in proxy settings screen of  oobe flow and goto Connect to Internet screen

        Args:
            spice: spice instance
            option: object id of skip button
        Returns:
            None
        """
        self.goto_proxy_settings_screen(spice)

        # isEnabled = spice.query_item("#skipButton")["visible"]
        # logging.info(f"******Skip button visible {isEnabled}")

        optionButton = spice.wait_for(option)
        optionButton.mouse_click()
        time.sleep(2)

        logging.info("Entering Connect to Internet Screen")
        time.sleep(6)
        assert spice.wait_for('#oobeConnectionPermission')
        logging.info("At Connect to Internet Screen")
        time.sleep(4)

    def goto_retrieve_pairing_code_screen(self, spice, mode='e2e') -> None:
        """Navigates to Retrieve pairing code screen.
           For e2e: Proxy Settings  to Retrieve Pairing Code
           For flex: Connect To Internet and to Retrieve Pairing Code

        Args:
            spice: spice instance
            mode: 'e2e' for loyal and 'flex' for traditional
        Returns:
            None
        """
        if(mode == 'e2e'):

            self.goto_proxy_settings_screen(spice)
            optionButton = spice.wait_for("#skipButton")
            optionButton.mouse_click()
            time.sleep(6)

        else:

            self.goto_connect_to_internet_screen(spice)
            option = "#oobeConnectionPermissionFooter #continueButton"
            optionButton = spice.wait_for(option)
            optionButton.mouse_click()
            time.sleep(6)

        # Retrieve Pairing Code Screen
        logging.info("Entering Pairing Code Screen")
        assert spice.wait_for("#RetrieveCode")
        logging.info("At Retrieve Pairing Code Screen")
        time.sleep(12)

    def goto_pairing_code_screen(self, spice, mode='e2e') -> None:
        """Navigates to pairing code screen.
           For e2e: Let's activate to Pairing Code
           For flex: Directly presents Pairing code

        Args:
            spice: spice instance
            mode: 'e2e' for loyal and 'flex' for traditional
        Returns:
            None
        """
        self.goto_retrieve_pairing_code_screen(spice, mode)
        if(mode == 'e2e'):
            # Let's Activate HP+
            logging.info("Entering Let's Activate HP+ screen ")
            spice.wait_for("#hpplusScreenView")
            logging.info("At Let's Activate HP+ Screen")
            option = "#hpplusScreenFooter #continueButton"
            optionButton = spice.wait_for(option)
            optionButton.mouse_click()
            time.sleep(3)

        else:
            logging.info("No Activate HP plus screen for flex")

        spice.wait_for("#showPairingCodeText")
        logging.info("At Pairing Code Screen")
        time.sleep(3)

    def goto_skip_pairing_code(self, spice, mode='flex') -> None:
        """Skip pairing code for flex/'Traditional' devices

        Args:
            spice: spice instance
            mode: 'flex' for traditional
        Returns:
            None
        """

        self.goto_pairing_code_screen(spice, mode)
        # Selecting 'LearnMore' at pairing code screen
        optionButton = spice.wait_for("#IoTPairing #learnMoreButton")
        optionButton.mouse_click()
        time.sleep(6)

        assert spice.wait_for("#learnMorePopup")
        logging.info("At Pairing Benefits screen")

        option = "#learnMorePopup #AlertModelView #AlertFooter #skipButton"
        skipOption = spice.wait_for(option)
        skipOption.mouse_click()
        time.sleep(6)

    def get_pairing_code(self, spice, mode='e2e'):
        """Fetches the pairing code from  Pairing Code Screen

        Args:
            spice: spice instance
            mode: 'e2e' for loyal and 'flex' for traditional
        Returns:
            pair_code: pairing code presented on the control panel
        """
        self.goto_pairing_code_screen(spice, mode)
        pair_code = spice.query_item(
            "#showPairingCodeText #titleBigItem")["text"]

        logging.info("Pairing code fetched is {}".format(pair_code))
        return pair_code

    def get_pairing_code_e2e(self, spice):
        """Method to navigate from 'Connect to Internet Screen' to 'Pairing Code Screen'
           for **ENGINE*** set in e2e mode. Script as per current implementation.
           It fetches the pairing code from the control panel.

        Args:
            spice: spice instance
            Returns:pairing code
            pair_code: pairing code presented on the control panel
        """

        # Added for the current firmware implementation seen on HW..Connect to Internet screen not expected in Loyal workflow
        self.goto_connect_to_internet_screen(spice)
        logging.info("Handler for unexpected Connect to Internet Screen ")
        option = "#oobeConnectionPermissionFooter #continueButton"
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()
        time.sleep(6)

        # Pairing Code Screen
        logging.info("Entering Pairing Code Screen")
        assert spice.wait_for("#RetrieveCode")
        logging.info("At Retrieve Pairing Code Screen")
        time.sleep(12)

        # Let's Activate HP+
        logging.info("Entering Let's Activate HP+ screen ")
        spice.wait_for("#hpplusScreenView")
        logging.info("At Let's Activate HP+ Screen")
        option = "#hpplusScreenFooter #continueButton"
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()

        time.sleep(3)

        spice.wait_for("#showPairingCodeText")
        logging.info("At Pairing Code Screen")
        pair_code = spice.query_item(
            "#showPairingCodeText #titleBigItem")["text"]

        logging.info("Pairing code fetched is {}".format(pair_code))
        return pair_code

    def goto_pairing_printer_screen(self, spice) -> None:
        """Method to validate Pairing your printer Screen in OOBE flow
        Args:
            spice: spice instance
        Returns:
            None
        """

        spice.wait_for("#IoTPairing #PrinterIsPairingView")
        logging.info("At Pairing your printer Screen")

    def goto_home_from_thankyou_screen(self, spice) -> None:
        """Returns to home screen from Thank You screen
        Args:
            spice: spice instance
        Returns:
            None
        """

        spice.wait_for("#oobeThankYouMessageView")
        logging.info("At ThankYou Screen")

        time.sleep(8)

        option = "#oobeThankYouMessageView #oobeThankYouFooter #continueButton"
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()

        time.sleep(3)

    def enter_admin_pin(self, password:str, confirm_password:str):
        """Enters Admin Pin
        Args:
            spice: spice instance
            password: new admin pin
            confirmPassword: confirming admin pin
        Returns:
            None
        """
        logging.info("Entering new passwords for admin")
        assert self.is_on_edit_admin_pin_screen(), logging.error("Not on Edit Admin Pin screen")

        password_text_field = self.spice.wait_for(MenuAppWorkflowObjectIds.edit_admin_password_text_field)
        assert password_text_field, logging.error("Failed to get Password Text Field")
        password_text_field.mouse_click()
        self.spice.keyBoard.keyboard_set_text_with_out_dial_action(password, MenuAppWorkflowObjectIds.edit_admin_password_text_field)

        password_confirm_text_field = self.spice.wait_for(MenuAppWorkflowObjectIds.edit_admin_password_confirm_text_field)
        assert password_confirm_text_field, logging.error("Failed to get Password Confirm Text Field")
        password_confirm_text_field.mouse_click()
        self.spice.keyBoard.keyboard_set_text_with_out_dial_action(confirm_password, MenuAppWorkflowObjectIds.edit_admin_password_confirm_text_field)

        apply_button = self.spice.wait_for(MenuAppWorkflowObjectIds.edit_admin_password_apply_button)
        assert apply_button, logging.error("Failed to get Apply Button")
        apply_button.mouse_click()

    def goto_edit_admin_pin(self, spice):
        """Navigates from thank you screen to edit admin pin
        Args:
            spice: spice instance
        Returns:
            None
        """
        editPinButton = spice.wait_for("#editPinButton")
        editPinButton.mouse_click()
        assert spice.wait_for("#oobeAdminPasswordPromptHeaderHeaderView")
        editButton = spice.wait_for("#oobeAdminPasswordPromptFooter #editButton")
        editButton.mouse_click()

    def goto_disable_ethernet(self, ssh, udw, ble_class, device):
        '''
        disable network switch and reboot
        Args:
            ssh: SSH
            udw: Duneunderware command
            ble_class: class name
            device: DuneDeviceStatus
        Returns:
            None
        '''

        logging.info("Disable ethernet")
        self.spice.udw.connectivityApp.execute(
            "NetworkManagerStandard setNwSwitchControlState 2")
        result = device.device_ready(5)
        assert all(result.values()), "Device did not disable ethernet!"
        time.sleep(5)
        ble_class.printer_reboot(ssh, udw)
        time.sleep(10)

    def goto_complete_oobe(self, udw, device):
        '''
        skip/exit OOBE
        Args:
            udw: Duneunderware command
            device: DuneDeviceStatus
        Returns:
            None
        '''
        logging.info("Skip OOBE flow")
        udw.mainApp.execute(
            "DeviceSetupManager PUB_overrideCompletedPersistent true")
        result = device.device_ready(10)
        assert all(result.values()), "Device did not skip OOBE flow"
        time.sleep(2)

    def goto_complete_oobe_once(self, udw, device):
        '''
        Override OOBE for the current boot.
        OOBE screen will disappear and control panel will show HomeScreen. After reboot OOBE will prompt again.
        Args:
            udw: Duneunderware command
            device: DuneDeviceStatus
        Returns:
            None
        '''
        logging.info("Skip OOBE flow")
        udw.mainApp.execute(
            "DeviceSetupManager PUB_overrideCompletedOnce")
        result = device.device_ready(10)
        assert all(result.values()), "Device did not skip OOBE flow"
        time.sleep(1)


    def goto_connection_method_screen_select_wireless(self, spice, oobe, udw):
        '''click on wifi at connection method screen in OOBE '''
        self.goto_oobe_connection_method_screen(spice, oobe, udw)
        logging.info("At Network Setting Screen")
        self.spice.wait_for("#oobeNetworkSummary")
        backButton = self.spice.query_item("#BackButton")
        backButton.mouse_click()
        time.sleep(1)
        logging.info("At connection method screen")
        self.spice.wait_for("#wifiRow")
        confirmButton = self.spice.query_item("#wifiRow")
        confirmButton.mouse_click()
        time.sleep(5)

    def goto_connection_method_screen_select_eth(self, udw, device):
        '''click on ethernet at connection method screen in OOBE'''
        logging.info("At connection method screen")
        self.spice.wait_for("#ethernetRow")
        confirmButton = self.spice.query_item("#ethernetRow")
        confirmButton.mouse_click()
        time.sleep(5)
        self.goto_complete_oobe(udw, device)
        time.sleep(1)

    def goto_skip_proxy_settings_screen(self):
        '''click on skip at  Proxy Screen'''
        logging.info("Entering Proxy Settings Screen")
        self.spice.wait_for("#oobeProxyBanner")
        optionButton = self.spice.query_item("#skipButton")
        optionButton.mouse_click()
        time.sleep(2)

    def skip_connect_to_internet_screen(self):
        ''' Click on learn more at connect to internet Screen and click on skip internet button '''
        logging.info("Entering connect to internet Screen")
        self.spice.wait_for("#oobeConnectionPermission")
        optionButton = self.spice.query_item("#learnMoreButton")#########Check out the query here change to waitfor?
        optionButton.mouse_click()
        time.sleep(2)
        confirmButton = self.spice.wait_for("#skipButton")
        confirmButton.mouse_click()
        time.sleep(5)

    def skip_Issue_connect_to_internet_screen(self):
        ''' Click on skip when issue arises connecting to server  '''
        self.spice.wait_for("#CheckingForUpdatesverticalLayout")
        while self.spice.query_item("#CheckingForUpdatesverticalLayout", 0)["activeFocus"] == True:
            time.sleep(5)
        
        try:
            self.spice.wait_for("#IccErrorView")
            assert self.spice.query_item("#IccErrorView")["activeFocus"] == True
            self.spice.wait_for("#IccErrorView #SkipButton").mouse_click()
        except:
            logging.info("skip_issue_connect_to_internet_screen: No IccErrorView, checking ErrorView")

        try:
            self.spice.wait_for("#ErrorView")
            assert self.spice.query_item("#ErrorView")["activeFocus"] == True
            self.spice.wait_for("#ErrorView #SkipButton").mouse_click()
        except:
            logging.info("Firmware Update is already set in OOBE!")

    def goto_set_date_time_screen(self):
        ''' Click on continue at datetime screen '''

        logging.info("Entering set date and time Screen")
        self.spice.wait_for("#dateTimeView")
        # TODO check obj id for continue button
        continueButton = self.spice.query_item("#dateTimeSettingViewverticalLayout #continueButton")
        continueButton.mouse_click()
        time.sleep(2)

    def goto_oobe_connection_method_screen_and_set_wifi(self, spice, udw, oobe):
        '''
        Enter OOBE flow upto connection method screen and select wifi as connection method.
        Args:
            spice: spice instance
        Returns:
            None
        '''
        try:
            self.goto_country_screen(spice, udw)
            countryList = spice.wait_for("#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView")
            # Set the index position based on the country to be set
            countryList.__setitem__("_indexPosition", "0")
            countryList.mouse_click()
            self.goto_set_date_time_screen()
        except:
            logging.info("Language and Country is already set in OOBE!")

        time.sleep(1)
        try:
            # Commenting the below lines to work seamlessly on MaroniHi Pdl
            # logging.info("Handling QR Code Screen")
            # self.spice.wait_for("#trafficDirector")
            # The following line will skip the full set up screen on MaroniHi Pdl
            oobe.oobe_operations.skip_print_engine_oobe_step()
            # self.spice.query_item("#helpButton").mouse_click()
            self.spice.wait_for("#oobeProductSetupHeaderHeaderView")
            self.spice.query_item("#fullSetupRow_firstinfoBlockRow").mouse_click()
        except:
            # logging.info("QR Code is not supported!")
            logging.info("Full Set up screen is not supported!")
        # Network Settings Screen
        time.sleep(1)
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#oobeNetworkSummary")
        logging.info("At Network Setting Screen")
        time.sleep(1)
        # click on back button to go to oobe flow connection methods from n/w settings screen
        logging.info("At Network Setting Screen")
        backButton = self.spice.query_item("#BackButton")
        backButton.mouse_click()
        time.sleep(1)

    def goto_oobe_connection_method_screen(self, spice, oobe, udw):
        '''
        Enter OOBE flow upto connection method screen and select wifi as connection method.
        Args:
            spice: spice instance
        Returns:
            None
        '''
        try:
            self.goto_country_screen(spice, udw)
            countryList = spice.wait_for("#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView")
            # Set the index position based on the country to be set
            countryList.__setitem__("_indexPosition", "0")
            countryList.mouse_click()
        except:
            logging.info("Language and Country is already set in OOBE!")

        time.sleep(1)
        try:
            # Commenting the below lines to work seamlessly on MaroniHi Pdl
            # logging.info("Handling QR Code Screen")
            # self.spice.wait_for("#trafficDirector")
            # The following line will skip the full set up screen on MaroniHi Pdl
            oobe.oobe_operations.skip_print_engine_oobe_step()
            time.sleep(1)
            # help_button = self.spice.query_item("#helpButton")
            # time.sleep(1)
            # self.spice.validate_button(help_button)
            # help_button.mouse_click()
            spice.wait_for("#oobeProductSetupHeaderHeaderView")
            spice.query_item("#fullSetupRow_firstinfoBlockRow").mouse_click()

        except:
            # logging.info("QR Code is not supported!")
            logging.info("Full Set up screen is not supported!")

        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#oobeNetworkSummary")

    def goto_oobe_proxy_screen(self, spice):
        '''Go to proxy setting screen on oobe setting from network summary screen'''
        # On network summery screen click on proxy setting button
        spice.wait_for("#oobeNetworkSummary")
        spice.query_item("#oobeNetworkSuccessViewFooter #proxySettingsButton").mouse_click()

    def set_proxy_server_in_oobe(self, spice):
        '''Set proxy server name on oobe setting'''
        spice.wait_for("#oobeManualProxylist")
        spice.wait_for("#proxyServerTextField").mouse_click()
        spice.keyBoard.keyboard_set_text_with_out_dial_action('testServer', '#proxyServerTextField')
        time.sleep(1)

    def set_proxy_port_in_oobe(self, spice):
        '''Set proxy server port on oobe setting'''
        # spice.wait_for("#oobeManualProxylist")
        spice.wait_for("#proxyPortTextField").mouse_click()
        time.sleep(1)
        spice.keyBoard.keyboard_set_text_with_out_dial_action('8080', '#proxyPortTextField')
        time.sleep(1)

    def set_proxy_username_and_password_in_oobe(self, spice):
        '''Set proxy username and password on oobe setting'''
        spice.wait_for("#oobeManualProxylist")
        scroll_vertical = "#oobeManualProxylistverticalLayoutScrollBar"
        time.sleep(1)
        # Scroll to enter paxy username and password
        assert self.spice.wait_for("#userNameTextField")
        self.spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(position=1,
                                                                                  scrollbar_objectname=scroll_vertical)
        time.sleep(1)
        spice.wait_for("#userNameSettingsTextField").mouse_click()
        spice.keyBoard.keyboard_set_text_with_out_dial_action('testUser', '#userNameTextField')
        time.sleep(1)
        spice.wait_for("#passwordTextField").mouse_click()
        spice.keyBoard.keyboard_set_text_with_out_dial_action('test123', '#passwordTextField')

    def configure_proxy_on_oobe_setup(self, spice, oobe):
        '''Configure all the text field on proxy screen on oobe setupand click on apply button'''
        # Set langauage , country on oobe screen
        # self.goto_oobe_connection_method_screen(spice, oobe)
        # Click on proxy setting button on Network summary screen
        self.goto_oobe_proxy_screen(spice)
        # Set proxy server
        self.set_proxy_server_in_oobe(spice)
        # Set proxy username and password
        self.set_proxy_username_and_password_in_oobe(spice)
        # click on apply button
        spice.wait_for("#applyButton").mouse_click()
        time.sleep(1)
        logging.info("At Network Setting Screen")
        spice.wait_for("#oobeNetworkSummary")
        # assert self.spice.wait_for("#oobeNetworkSummary")
        backButton = self.spice.query_item("#BackButton")
        backButton.mouse_click()
        time.sleep(2)




    def goto_home_from_proxy_screen(self, udw, device):
        '''
        Skip proxy,connect to internet, continue on date and time click ok on hp s/w screen
        Args:
            udw: Duneunderware command
            device: DuneDeviceStatus
        Returns:
            None
        '''

        self.goto_skip_proxy_settings_screen()  # enter proxy screen
        time.sleep(2)
        self.skip_connect_to_internet_screen()
        time.sleep(2)
        # TODO OKbutton on thankyou screen not working
        self.goto_complete_oobe(udw, device)
        time.sleep(2)

    def get_thank_you_screen(self, spice):
        ''' Click on ok button and complete the last page '''
        ## Thank you message
        assert self.spice.wait_for("#oobeThankYouMessageView")
        try:
            consentButton = self.spice.wait_for("#oobeThankYouMessageView #continueButton")
            consentButton.mouse_click()
        except:
            logging.info("OOBEAppWorkflowUICommonOperations::get_thank_you_screen - Continue Button is not available for this experience")

    def get_driver_and_finish_setup(self, spice):
        """ Click on get driver and finish setup Continue button """
        optionButton = self.spice.wait_for("#DriversContinueButton")
        optionButton.mouse_click()

    def critical_firmware_update_page(self, spice):
        """ Click on critical firmware update Continue button """
        consentButton = self.spice.wait_for("#OobeAppApplicationStackView #cfuInfo #continueButton")
        consentButton.mouse_click(x=int(consentButton['width'] / 2.0), y=int(consentButton['height'] / 2.0))
        ## Skip critical firmware update if failed to connect to server after the above first try.
        self.skip_Issue_connect_to_internet_screen()

    def print_guidance_page_from_drivers_screen(self,spice):
        logging.info("Printing guidance page from install drivers screen")
        printButton = self.spice.wait_for("#OobeInstallDriversView #DriversPrintButton")
        printButton.mouse_click()

    def install_drivers_screen(self, spice):
        logging.info("Entering driver installation screen")
        continueButton = self.spice.wait_for("#OobeInstallDriversView #DriversContinueButton")
        continueButton.mouse_click()

    def get_printer_analytics(self, spice):
        logging.info("Entering printer analytics screen")
        assert spice.wait_for("#OobeSharePrinterAnalytics")
        consentButton = spice.wait_for("#YesButton")
        consentButton.mouse_click()

    def firmware_update_config_page(self, spice):
        """ Scroll down and click on confirm to validate """
        scroll_vertical = "#fwUpdateConfigverticalLayout #verticalScroll"
        ## Firmware update config page
        assert self.spice.wait_for("#fwUpdateConfig")
        self.spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(position=1,
                                                                                  scrollbar_objectname=scroll_vertical)
        consentButton = self.spice.wait_for("#nextButton")
        self.spice.wait_until(lambda: consentButton["enabled"] == True)
        consentButton.mouse_click()

    def select_firmware_update_option(self, spice):
        """ Select the option required for update"""
        ## Firmware update option page
        assert self.spice.wait_for("#FWUpdateConfigScreen")
        consentButton = self.spice.wait_for("#AutoRecommended")
        consentButton.mouse_click()
        consentButton = self.spice.wait_for("#saveButton")
        self.spice.wait_until(lambda: consentButton["visible"] == True)
        consentButtonCenterX = int(consentButton['width'] / 2.0)
        consentButtonCenterY = int(consentButton['height'] / 2.0)
        consentButton.mouse_click(consentButtonCenterX, consentButtonCenterY)

    def goto_thank_you_screen(self, oobe, configuration):
        """ Navigate from begining of oobe to the thank you screen"""

        self.select_device_language("en")
        self.click_language_confirmation_button()
        self.select_country()
        if configuration.productname in ["selene"]:
            self.click_network_settings_continue_button()
            self.click_share_analytics_yes_button()
            self.click_firmware_update_continue_button()
            self.is_on_firmware_update_error_screen(20)
            self.click_firmware_update_error_skip_button()
            self.click_drivers_and_finish_setup_continue_button()
        else:
            self.click_date_time_screen_continue_button()
            self.select_altitude()
            self.click_network_settings_continue_button()
            oobe.oobe_operations.skip_print_engine_oobe_step()
            try:
                self.skip_connect_to_internet_screen()
            except TimeoutError:
                logging.error("No 'Connect to internet' screen. Skipping...")
            self.goto_set_date_time_screen()

        assert self.is_on_thank_you_screen(), logging.error("Not on Thank You screen")

    def goto_thankyou_screen_from_success_adminpin(self, spice):
        """ After successful admin pin change go back to thank you screen"""

        assert self.spice.wait_for("#successViewModelFooter")
        manualSetupButton = spice.wait_for("#successViewModelFooter #continueButton")
        manualSetupButton.mouse_click()

    def goto_thankyou_screen_from_adminpin_prompt(self, spice):
        """ Admin pin prompt screen go back to thank you screen"""
        editPinButton = spice.wait_for("#editPinButton")
        editPinButton.mouse_click()
        skipButton = spice.wait_for("#oobeAdminPasswordPrompt #skipButton")
        skipButton.mouse_click()


    def retry_admin_pin(self, spice):
        """ Click retry on invalid admin pin screen"""
        retryButton = spice.wait_for("#AlertFooter #retryButton")
        retryButton.mouse_click()
        """Navigate back and again go to enter the new password screen"""
        backButton = spice.wait_for("#BackButton")
        backButton.mouse_click()
        assert spice.wait_for("#oobeAdminPasswordPromptHeaderHeaderView")
        editButton = spice.wait_for("#oobeAdminPasswordPromptFooter #editButton")
        editButton.mouse_click()

    def goto_get_software_screen(self, spice):
        """Click ok button on get software screen"""
        okButton = spice.wait_for("#getSoftwareFooter #okButton")
        okButton.mouse_click()

    def select_oobe_language_country(self, spice, cdm, udw, language,
                                     languageobj="#DeviceLanguageView #DeviceLanguageViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView",
                                     country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView",
                                     lang_position=""
                                     ) -> None:
        configuration_endpoint = "cdm/system/v1/configuration"
        languageList = spice.wait_for(languageobj)
        # Set the index position based on the language to be set
        languageList.__setitem__("_indexPosition", lang_position)
        selectedLang = self.device_language[language]
        # scroll_vertical = "#DeviceLanguageViewverticalLayout #hScroll"
        menu_item_id = MenuAppWorkflowObjectIds.language_obj_id.format(selectedLang)
        # self.spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(position=.3,
        #                                                                                scrollbar_objectname=scroll_vertical)
        # self.spice.homeMenuUI().menu_navigation(spice, screen_id = "#DeviceLanguageView", menu_item_id = menu_item_id, scrollbar_objectname = "#SpiceListViewViewScrollBar")
        selected_language = spice.wait_for(menu_item_id)
        selected_language.mouse_click()

        engine_make = int(udw.mainApp.execute("ConnectorDriver PUB_getEngineMake"))
        if (engine_make != DuneEngineMake.canonHomepro.value):
            assert spice.wait_for("#langConfirmPopup")
            confirmButton = spice.wait_for("#ConfirmButton")
            confirmButton.mouse_click()

        countryList = spice.wait_for(country)

        r = cdm.get(cdm.SYSTEM_CONFIGURATION)
        print("device language", r)
        assert r["deviceLanguage"] == language.split("_")[1]

        r = cdm.get(cdm.SYSTEM_IDENTITY)
        print("device language new", r)
        assert r["deviceLanguage"] == language.split("_")[1]

        time.sleep(2)
        countryList.__setitem__("_indexPosition", "0")
        countryList.mouse_click(x=2, y=1)

        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#oobeNetworkSummary")
        logging.info("At Network Setting Screen")
        time.sleep(4)

    def validate_network_settings_unhappy_path(self, spice, net, udw):
        ## Proxy settings button and screen validation
        proxy_button = spice.wait_for(MenuAppWorkflowObjectIds.proxy_button)
        proxy_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.proxy_screen)
        time.sleep(2)
        ## Select cancel button to go back to network settings
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_cancel)
        cancel_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.network_settings_screen)
        ## Select back button to go to Connection method
        if spice.uisize == "XS":
            try:
                keypad_controller: KeypadController = KeypadController(udw=udw)
                keypad_controller.press("BACK")
            except:
                logging.info("OOBEAppWorkflowUICommonOperations::validate_network_settings_unhappy_path - Feature not available for experience")
        else:
            optionButton = spice.wait_for(MenuAppWorkflowObjectIds.button_back)
            optionButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.connection_method_screen)
        ## Select Wifi option when ethernet is connected.
        wifi_button = spice.wait_for(MenuAppWorkflowObjectIds.wifi_connection_option)
        wifi_button.mouse_click()
        time.sleep(2)
        current_string = spice.query_item(MenuAppWorkflowObjectIds.wifi_info_text)["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cEthernetCableConnection")
        assert current_string == expected_string, "String mismatch"
        ## Going back to connection method
        wifi_button = spice.wait_for(MenuAppWorkflowObjectIds.ok_button)
        wifi_button.mouse_click()
        ## Select Ethernet in connection method
        wifi_button = spice.wait_for(MenuAppWorkflowObjectIds.ethernet_connection_option)
        wifi_button.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.network_settings_screen)
        ## Select back button in network settings and connection method.
        optionButton = spice.wait_for(MenuAppWorkflowObjectIds.button_back)
        optionButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.connection_method_screen)
        back_button = spice.wait_for(MenuAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.country_screen)

    def select_firmware_update_do_not_check_option(self, spice):
        """ Select the option required for update"""
        ## Firmware update option page
        assert self.spice.wait_for("#FWUpdateConfigScreen")
        consentButton = self.spice.wait_for(MenuAppWorkflowObjectIds.do_not_check)
        consentButton.mouse_click()
        consentButton = self.spice.wait_for("#FWUpdateConfigScreenlist1 #FooterView #FooterViewRight")
        consentButton.mouse_click()

    def select_firmware_update_notify_option(self, spice):
        """ Select the option required for update"""
        ## Firmware update option page
        assert self.spice.wait_for("#FWUpdateConfigScreen")
        consentButton = self.spice.wait_for(MenuAppWorkflowObjectIds.notify)
        consentButton.mouse_click()
        consentButton = self.spice.wait_for("#FWUpdateConfigScreenlist1 #FooterView #FooterViewRight")
        consentButton.mouse_click()

    def validate_date_and_time_unhappy_path(self, spice, password = "12345678"):
        ''' Click on continue at datetime screen '''

        logging.info("Entering set date and time Screen")
        self.spice.wait_for(MenuAppWorkflowObjectIds.date_time_screen)
        # Verifying the timezone is loaded.
        timezone = self.spice.wait_for(MenuAppWorkflowObjectIds.dateTime_timeZone)
        timezone.mouse_click()
        try:
            # Click in comboBoxList
            sign_in_combobox = spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)
            sign_in_combobox.mouse_click()

            # Click in the Administrator option
            admin_option = spice.wait_for(MenuAppWorkflowObjectIds.list_item_admin)
            admin_option.mouse_click()

            # Login
            spice.signIn.cleanup("admin", spice.signIn.enter_creds(True, "admin", password))
            time.sleep(2)
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout).mouse_click()
        except TimeoutError:
            logging.info("-----the timezone settings view is loaded without login-----")
        finally:
            ##Assert if the timezone screen doesn't appear
            assert spice.wait_for(MenuAppWorkflowObjectIds.timezones)
            logging.info("At Time zones screen")
            time.sleep(1)
        time.sleep(2)
        back_button = spice.wait_for("#BackButton")
        back_button.mouse_click()
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.date_time_screen)
        # Verifying the Date screen is loaded.
        date = self.spice.wait_for(MenuAppWorkflowObjectIds.dateTime_date)
        date.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.date_settings)
        apply_button = spice.wait_for(MenuAppWorkflowObjectIds.apply_button_date)
        apply_button.mouse_click()
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.date_time_screen)
        # Verify the Time screen is loaded
        time_option = spice.wait_for(MenuAppWorkflowObjectIds.dateTime_time)
        time_option.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.time_settings)
        apply_button = spice.wait_for(MenuAppWorkflowObjectIds.apply_button_time)
        apply_button.mouse_click()
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.date_time_screen)
        continueButton = self.spice.query_item("#dateTimeSettingViewverticalLayout #continueButton")
        continueButton.mouse_click()

    def validate_setting_up_printer_screen(self, spice):
        assert spice.wait_for("#settingupprinter")

    def critical_firmware_update(self, spice):
        """ Click on critical firmware update Continue button """
        consentButton = self.spice.wait_for("#OobeAppApplicationStackView #cfuInfoverticalLayout #continueButton")
        consentButton.mouse_click()
        ## Skip critical firmware update if failed to connect to server after the above first try.
        self.skip_critical_fw_update(spice)
    
    def click_button(self, button_locator:str, timeout:float=10) -> bool:
        button = self.spice.wait_for(button_locator)
        if not button:
            logging.error(f"Failed to get button: {button_locator}")
            return False
        try:
            self.spice.wait_until(lambda: button["visible"] == True, timeout=timeout)
        except:
            return False
        button.mouse_click()
        return True
    
    def is_on_device_language_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.device_language_view)
    
    def is_on_language_confirmation_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.language_confirmation_view)
    
    def is_on_country_select_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.country_region_view)
    
    def is_on_date_time_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime)
    
    def is_on_altitude_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.altitude_view)

    def is_on_network_settings_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.network_settings_screen)

    def is_on_thank_you_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.thank_you_view)
    
    def is_on_share_activity_screen(self) -> bool:
       return self.spice.wait_for(MenuAppWorkflowObjectIds.share_printer_analytics_view)
    
    def is_on_firmware_update_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.firmware_update_view)
    
    def is_on_firmware_update_error_screen(self, wait_timeout:float = 5) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.firmware_update_error_view, timeout=wait_timeout)
    
    def is_on_driver_and_finish_setup_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.driver_and_finish_setup_view)
    
    def is_on_admin_password_prompt_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.admin_password_prompt_view)
    
    def is_on_admin_password_rejected_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.admin_password_rejected_view)

    def is_on_admin_password_mismatch_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.admin_password_mismatch_view)

    def is_on_edit_admin_pin_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.edit_admin_password_view)
    
    def is_on_edit_admin_pin_success_screen(self) -> bool:
        return self.spice.wait_for(MenuAppWorkflowObjectIds.edit_admin_password_success_view)
    
    def select_device_language(self, language_abbreviation:str) -> None:
        assert self.is_on_device_language_screen(), logging.error("Not on OOBE device language screen")
        assert self.click_button(MenuAppWorkflowObjectIds.language_obj_id.format(language_abbreviation) + " " + MenuAppWorkflowObjectIds.language_button),\
            logging.error(f"Failed to select device language: {language_abbreviation}")
    
    def select_country(self) -> None:
        assert self.is_on_country_select_screen(), logging.error("Not on OOBE country region screen")
        
        country_list = self.spice.wait_for(MenuAppWorkflowObjectIds.country_region_list)
        assert country_list, logging.error("Failed to get Country List")
        self.spice.wait_until(lambda: country_list["visible"] == True)
        country_list.__setitem__("_indexPosition", "0")
        country_list.mouse_click()
    
    def select_altitude(self) -> None:
        assert self.is_on_altitude_screen(), logging.error("Not on OOBE altitude screen")
        assert self.click_button(MenuAppWorkflowObjectIds.altitude_button.format(0)),\
            logging.error("Failed to select altitude")

    def click_language_confirmation_button(self) -> None:
        assert self.is_on_language_confirmation_screen(), logging.error("Not on OOBE language confirmation popup screen")
        assert self.click_button(MenuAppWorkflowObjectIds.language_confirmation_confirm_button),\
            logging.error("Failed to click language confirmation button")

    def click_date_time_screen_continue_button(self) -> None:
        assert self.is_on_date_time_screen(), logging.error("Not on OOBE date time screen")
        assert self.click_button(MenuAppWorkflowObjectIds.continue_button),\
            logging.error("Failed to click date time continue button")

    def click_network_settings_continue_button(self) -> None:
        assert self.is_on_network_settings_screen(), logging.error("Not on OOBE network settings screen")
        assert self.click_button(MenuAppWorkflowObjectIds.network_settings_continue_button),\
            logging.error("Failed to click network settings continue button")
    
    def click_thank_you_ok_button(self) -> None:
        assert self.is_on_thank_you_screen(), logging.error("Not on OOBE thank you sceen")
        assert self.click_button(MenuAppWorkflowObjectIds.thank_you_ok_button),\
            logging.error("Failed to click thank you ok button")
    
    def click_thank_you_edit_pin_button(self) -> None:
        assert self.is_on_thank_you_screen(), logging.error("Not on OOBE thank you sceen")
        assert self.click_button(MenuAppWorkflowObjectIds.thank_you_edit_pin_button),\
            logging.error("Failed to click thank you ok button")

    def click_share_analytics_yes_button(self) -> None:
        assert self.is_on_share_activity_screen(), logging.error("Not on OOBE share analytics screen")
        assert self.click_button(MenuAppWorkflowObjectIds.share_printer_analytics_yes_button),\
            logging.error("Failed to click printer analytics yes button")
        
    def click_firmware_update_continue_button(self) -> None:
        assert self.is_on_firmware_update_screen(), logging.error("Not on OOBE firmware update screen")
        assert self.click_button(MenuAppWorkflowObjectIds.firmware_update_continue_button),\
            logging.error("Failed to click firmware update continue button")
    
    def click_firmware_update_error_skip_button(self) -> None:
        assert self.is_on_firmware_update_error_screen(), logging.error("Not on OOBE firmware update error screen")
        assert self.click_button(MenuAppWorkflowObjectIds.firmware_update_error_skip_button),\
            logging.error("Failed to click firmware update error skip button")
    
    def click_drivers_and_finish_setup_continue_button(self) -> None:
        assert self.is_on_driver_and_finish_setup_screen(), logging.error("Not on OOBE drivers and finish setup screen")
        assert self.click_button(MenuAppWorkflowObjectIds.driver_and_finish_setup_continue_button),\
            logging.error("Failed to click drivers and finish setup continue button")
    
    def click_admin_password_edit_button(self) -> None:
        assert self.is_on_admin_password_prompt_screen(), logging.error("Not on OOBE admin password prompt screen")
        assert self.click_button(MenuAppWorkflowObjectIds.admin_password_prompt_edit_button),\
            logging.error("Failed to click admin password edit button")
    
    def click_admin_password_skip_button(self) -> None:
        assert self.is_on_admin_password_prompt_screen(), logging.error("Not on OOBE admin password prompt screen")
        assert self.click_button(MenuAppWorkflowObjectIds.admin_password_prompt_skip_button),\
            logging.error("Failed to click admin password skip button")
    
    def click_admin_password_success_continue_button(self) -> None:
        assert self.is_on_edit_admin_pin_success_screen(), logging.error("Not on OOBE admin password success screen")
        assert self.click_button(MenuAppWorkflowObjectIds.edit_admin_password_success_continue_button),\
            logging.error("Failed to click admin password success continue button")
    
    def click_admin_password_rejected_retry_button(self) -> None:
        assert self.is_on_admin_password_rejected_screen(), logging.error("Not on OOBE admin password rejected screen")
        assert self.click_button(MenuAppWorkflowObjectIds.admin_password_rejected_retry_button),\
            logging.error("Failed to click admin password retry button")

    def click_language_confirmation(self) -> bool:
        list = self.workflow_common_operations.get_element("#DeviceLanguageView #DeviceLanguageViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView")
        list.__setitem__("_indexPosition", 0)
        en_button = self.workflow_common_operations.get_element("#DeviceLanguageView #dune::spice::glossary_1::Language::Language.en #SpiceRadioButton")
        if not en_button: return False
        if not self.workflow_common_operations.click(en_button, check_enabled=False): return False
        confirm_button = self.workflow_common_operations.get_element("#langConfirmPopup #FooterView #FooterViewRight #ConfirmButton #ButtonControl")
        if not confirm_button: return False
        return self.workflow_common_operations.click(confirm_button)
    
    def click_country(self) -> bool:
        list = self.workflow_common_operations.get_element("#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView")
        list.__setitem__("_indexPosition", 0)
        us_button = self.workflow_common_operations.get_element("#OobeCountryRegionView #232 #SpiceRadioButton")
        if not us_button: return False
        return self.workflow_common_operations.click(us_button, check_enabled=False)
    
    def click_network_continue_button(self) -> bool:
        time.sleep(5)
        continue_button = self.workflow_common_operations.get_element("#oobeNetworkSummary #continueButton")
        if not continue_button: return False
        return self.workflow_common_operations.click(continue_button)

    def click_share_analytics_no_button(self) -> bool:
        no_button = self.workflow_common_operations.get_element("#OobeSharePrinterAnalytics #OobeSharePrinterAnalyticsFooter #FooterView #FooterViewRight #NoButton #ButtonControl")
        if not no_button: return False
        return self.workflow_common_operations.click(no_button)
    
    def click_firmware_update_continue_button(self) -> bool:
        continue_button = self.workflow_common_operations.get_element("#OobeAppApplicationStackView #CriticalFwUpdate #panelsStack #FooterViewRight #continueButton #ButtonControl")
        if not continue_button: return False
        return self.workflow_common_operations.click(continue_button)
    
    def click_firmware_update_error_skip_button(self) -> bool:
        continue_button = self.workflow_common_operations.get_element("#OobeAppApplicationStackView #CriticalFwUpdate #ErrorView #FooterViewRight #SkipButton #ButtonControl")
        if not continue_button: return False
        return self.workflow_common_operations.click(continue_button)
    
    def click_install_driver_continue_button(self) -> bool:
        continue_button = self.workflow_common_operations.get_element("#OobeInstallDriversView #FooterView #FooterViewRight #DriversContinueButton #ButtonControl")
        if not continue_button: return False
        return self.workflow_common_operations.click(continue_button)

