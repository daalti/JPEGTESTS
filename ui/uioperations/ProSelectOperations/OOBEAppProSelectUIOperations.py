#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import time
import requests
import unicodedata

from dunetuf.udw import DuneUnderware
from dunetuf.power.power import Power


from dunetuf.ui.uioperations.BaseOperations.IOOBEAppUIOperations import IOOBEAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from dunetuf.yeti.yetiudw_commands import YetiUdw


class OOBEAppProSelectUIOperations(IOOBEAppUIOperations):

    # Move the below dictionaries to a external json file later
    device_language_options = {"option_es": "Español", "option_de": "Deutsch", "option_ar": "العربية", "option_ca": "Català",
                               "option_cs": "Čeština", "option_da": "Dansk", "option_el": "Ελληνικά", "option_fi": "Suomi", "option_fr": "Français",
                               "option_hr": "Hrvatski", "option_hu": "Magyar", "option_id": "Bahasa Indonesia", "option_it": "Italiano", "option_ko": "한글",
                               "option_nl": "Nederlands", "option_nb": "Norsk", "option_pl": "Polski", "option_pt": "Português", "option_ru": "Русский",
                               "option_sk": "Slovenčina", "option_sl": "Deusch", "option_sv": "Svenska", "option_th": "ไทย", "option_tr": "Türkçe",
                               "option_ro": "xxx", "option_ja": "xxx", "option_he": "xxx", "option_zh-CN": "xxx", "option_zh-TW": "xxx", }

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.commonops = ProSelectCommonOperations(self.spice)
        self.keyboardops = ProSelectKeyboardOperations(self.spice)
   
    def get_language_name(self, locale):
        languagedict = {"en_US": "English", "es_ES": "Español", "eu_ES": " ", "de_DE": " ", "fr_FR": " ", "ja_JP": " ", "zh_CN": " ", "zh_TW": " ", "th_TH": " ", "it_IT": " ",
                        "pt_BR": " ", "id_ID": " ", "nl_NL": " ", "ar_SA": " ", "ru_RU": " ", "tr_TR": " ", "pl_PL": " ", "el_GR": " ", "da_DK": " ", "sv_SE": " ", "nb_NO": " ",
                        "fi_FI": " ", "cs_CZ": " ", "hu_HU": " ", "ca_ES": " ", "sk_SK": " ", "bg_BG": " ", "hr_HR": " ", "fr_FR": " ", "ro_RO": " ", "sl_SI": " ", "he_IL": " ",
                        "ko_KR": " ", "uk_UA": " ", "vi_VN": " "}
        logging.info(languagedict[locale])
        return languagedict[locale]

    def get_language_objectid(self, locale):
        languagedict = {"en_US": "#option_en", "es_ES": "#option_es", "eu_ES": " ", "de_DE": " ", "fr_FR": " ", "ja_JP": " ", "zh_CN": " ", "zh_TW": " ", "th_TH": " ", "it_IT": " ",
                        "pt_BR": " ", "id_ID": " ", "nl_NL": " ", "ar_SA": " ", "ru_RU": " ", "tr_TR": " ", "pl_PL": " ", "el_GR": " ", "da_DK": " ", "sv_SE": " ", "nb_NO": " ",
                        "fi_FI": " ", "cs_CZ": " ", "hu_HU": " ", "ca_ES": " ", "sk_SK": " ", "bg_BG": " ", "hr_HR": " ", "fr_FR": " ", "ro_RO": " ", "sl_SI": " ", "he_IL": " ",
                        "ko_KR": " ", "uk_UA": " ", "vi_VN": " "}
        logging.info(languagedict[locale])
        return languagedict[locale]

    def get_country_name(self, country_code):
        countrydict = {"AE": "United Arab Emirates", "AR": "Argentina", "AT": "Austria", "AU": "Australia", "BE": "Belgium",
                       "BG": "Bulgaria", "BR": "Brazil", "BY": "Belarus", "CA": "Canada", "CH": "Switzerland", "CL": "Chile", "CN": "China",
                       "CO": "Colombia", "CR": "Costa Rica", "CZ": "Czech Republic", "DE": "Germany", "DK": "Denmark", "EC": "Ecuador", "EE": "Estonia",
                       "EG": "Egypt", "ES": "Spain", "FI": "Finland", "FR": "France", "GB": "United Kingdom", "GR": "Greece", "GT": "Guatemala",
                       "HK": "Hong Kong", "HR": "Crotia", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India",
                       "IS": "Iceland", "IT": "Italy", "JO": "Jordan", "JP": "Japan", "KR": "Republic of Korea", "KW": "Kuwait", "KZ": "Kazakhstan",
                       "LB": "Lebanon", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MA": "Morocco", "MX": "Mexico", "MY": "Malaysia",
                       "NL": "Netherlands", "NO": "Norway", "NZ": "New Zealand", "PA": "Panama", "PE": "Peru", "PH": "Philippines", "PK": "Pakistan",
                       "PL": "Poland", "PT": "Portugal", "PY": "Paraguay", "QA": "Qatar", "RO": "Romania", "RU": "Russia", "SA": "Saudi Arabia",
                       "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia", "SK": "Slovakia", "TH": "Thailand", "TN": "Tunisia", "TR": "Turkey",
                       "TW": "Taiwan", "UA": "Ukraine", "US": "United States", "UY": "Uruguay", "VE": "Venezuela", "VN": "Vietnam", "ZA": "South Africa",
                       "AO": "Angola", "MZ": "Mozambique", "YE": "Yemen"}
        logging.info(countrydict[country_code])
        return countrydict[country_code]

    def get_country_objectid(self, country_code):
        countrydict = {"AE": "#cCountryRegionUnitedArabEmirates", "AR": " ", "AT": " ", "AU": "#cCountryRegionAustralia",
                       "BE": " ", "BG": " ", "BR": " ",
                       "BY": " ",
                       "CA": "#cCountryRegionCanada", "CH": " ", "CL": " ", "CN": " ",
                       "CO": " ", "CR": " ", "CZ": " ", "DE": " ",
                       "DK": " ", "EC": " ", "EE": " ", "EG": "#cCountryRegionEgypt",
                       "ES": "#cCountryRegionSpain", "FI": " ", "FR": " ", "GB": "#cCountryRegionUnitedKingdom",
                       "GR": " ",
                       "GT": " ", "HK": "#cCountryRegionHongKongSAR", "HR": " ",
                       "HU": " ", "ID": "#cCountryRegionIndonesia", "IE": "#cCountryRegionIreland", "IL": "#cCountryRegionIsrael",
                       "IN": "#cCountryRegionIndia", "IS": "#cCountryRegionIceland", "IT": " ",
                       "JO": "#cCountryRegionJordan",
                       "JP": " ", "KR": " ", "KW": " ", "KZ": " ",
                       "LB": "#cCountryRegionLebanon", "LT": " ", "LU": " ", "LV": " ",
                       "MA": " ",
                       "MX": " ", "MY": "#cCountryRegionMalaysia", "NL": " ",
                       "NO": " ", "NZ": "#cCountryRegionNewZealand", "PA": " ", "PE": " ",
                       "PH": "#cCountryRegionPhilippines", "PK": "#cCountryRegionPakistan", "PL": " ",
                       "PT": " ",
                       "PY": " ", "QA": " ", "RO": " ", "RU": " ",
                       "SA": "#cCountryRegionSaudiArabia", "SE": " ", "SG": "#cCountryRegionSingapore", "SI": " ",
                       "SK": " ",
                       "TH": "#cCountryRegionThailand", "TN": " ", "TR": " ",
                       "TW": " ", "UA": " ", "US": "#cCountryRegionUnitedStates", "UY": " ",
                       "VE": " ",
                       "VN": "#cCountryRegionVietnam", "ZA": "#cCountryRegionSouthAfrica", "AO": " ",
                       "MZ": " ", "YE": " "}
        logging.info(countrydict[country_code])
        return countrydict[country_code]

    def get_country_order(self, locale):
        country_order_dict = {"en_US": ["US", "CA", "GB", "AU", "IN", "SG", "NZ", "ZA", "HK", "IL", "TH", "SA", "AE", "MY", "PH", "IE", "ID", "EG", "JO", "PK", "LB", "VN", "IS"],
                              "fr_FR": ["FR", "CA", "CH", "BE", "MA", "TN", "LU"], "de_DE": ["DE", "CH", "AT", "BE"], "es_ES": ["US", "ES", "MX", "AR", "CL", "PE"], "eu_ES": ["FR", "ES"], "it_IT": ["IT", "CH"],
                              "sl_SI": ["SE", "FI", "IS"], "da_DK": ["DK", "IS"], "nb_NO": ["NO"], "nl_NL": ["NL", "BE"], "fi_FI": ["FI"], "pt_BR": ["BR", "PT"], "pl_PL": ["PL"],
                              "tr_TR": ["TR"], "zh_TW": ["HK", "TW"], "zh_CN": ["CN", "HK", "SG"], "ru_RU": ["RU", "LT", "LV", "EE", "BY", "UA"], "cs_CZ": ["CZ", "SK"], "hu_HU": ["HU"],
                              "ko_KR": ["KR"], "he_IL": ["IL"], "el_GR": ["GR"], "ar_SA": ["SA", "AE", "EG", "MA", "LB", "TN", "JO"], "hr_HR": ["HR"], "ro_RO": ["RO"], "sk_SK": ["SK"],
                              "sl_SI": ["SI"], "th_TH": ["TH"], "id_ID": ["ID"], "ca_ES": ["ES"], "uk_UA": ["UA"], "vi_VN": ["VN"]}
        logging.info(country_order_dict[locale])
        return country_order_dict[locale]

    def get_location_ids_by_language(self, language, short_list=True):
        location_ids_by_language = {
            "en": {
                "short_list": [
                    "#cCountryRegionUnitedStates", "#cCountryRegionCanada", "#cCountryRegionUnitedKingdom", "#cCountryRegionAustralia", "#cCountryRegionIndia", "#cCountryRegionSingapore", "#cCountryRegionNewZealand",
                    "#cCountryRegionSouthAfrica", "#cCountryRegionHongKongSAR", "#cCountryRegionIsrael", "#cCountryRegionThailand", "#cCountryRegionSaudiArabia", "#cCountryRegionUnitedArabEmirates", "#cCountryRegionMalaysia",
                    "#cCountryRegionPhilippines", "#cCountryRegionIreland", "#cCountryRegionIndonesia", "#cCountryRegionEgypt", "#cCountryRegionJordan", "#cCountryRegionPakistan", "#cCountryRegionLebanon", "#cCountryRegionVietnam",
                    "#cCountryRegionIceland", "#cCountryRegionChile", "#cCountryRegionMexico", "#cCountryRegionPeru", "#cCountryRegionMalta", "#cCountryRegionBrunei", "#cCountryRegionCambodia", "#cCountryRegionSriLanka"
                ],
                "long_list": [
                    "#cCountryRegionAfghanistan", "#cCountryRegionAlbania", "#cCountryRegionAlgeria", "#cCountryRegionAmericanSamoa", "#cCountryRegionAndorra", "#cCountryRegionAngola", "#cCountryRegionAnguilla", "#cCountryRegionAntarctica",
                    "#cCountryRegionAntiguaAndBarbuda", "#cCountryRegionArgentina", "#cCountryRegionArmenia", "#cCountryRegionAruba", "#cCountryRegionAustria", "#cCountryRegionAzerbaijan", "#cCountryRegionBahamas", "#cCountryRegionBahrain",
                    "#cCountryRegionBangladesh", "#cCountryRegionBarbados", "#cCountryRegionBelarus", "#cCountryRegionBelgium", "#cCountryRegionBelize", "#cCountryRegionBenin", "#cCountryRegionBermuda", "#cCountryRegionBhutan",
                    "#cCountryRegionBolivia", "#cCountryRegionBonaireSintEustatiusSaba", "#cCountryRegionBosniaAndHerzegovina", "#cCountryRegionBotswana", "#cCountryRegionBrazil", "#cCountryRegionBritishVirginIslands", "#cCountryRegionBulgaria",
                    "#cCountryRegionBurkinaFaso", "#cCountryRegionBurundi", "#cCountryRegionCameroon", "#cCountryRegionCapeVerde", "#cCountryRegionCaymanIslands", "#cCountryRegionCentralAfricanRepublic", "#cCountryRegionChad",
                    "#cCountryRegionChina", "#cCountryRegionColombia", "#cCountryRegionComoros", "#cCountryRegionCostaRica", "#cCountryRegionCroatia", "#cCountryRegionCuracao", "#cCountryRegionCyprus", "#cCountryRegionCzechRepublic",
                    "#cCountryRegionDemocraticRepublicOfTheCongo", "#cCountryRegionDenmark", "#cCountryRegionDjibouti", "#cCountryRegionDominica", "#cCountryRegionDominicanRepublic", "#cCountryRegionEcuador", "#cCountryRegionElSalvador",
                    "#cCountryRegionEquatorialGuinea", "#cCountryRegionEritrea", "#cCountryRegionEstonia", "#cCountryRegionSwaziland", "#cCountryRegionEthiopia", "#cCountryRegionFalklandIslands", "#cCountryRegionFaroeIslands",
                    "#cCountryRegionFederatedStatesOfMicronesia", "#cCountryRegionFiji", "#cCountryRegionFinland", "#cCountryRegionFrance", "#cCountryRegionFrenchGuiana", "#cCountryRegionFrenchPolynesia", "#cCountryRegionGabon",
                    "#cCountryRegionGambia", "#cCountryRegionGeorgia", "#cCountryRegionGermany", "#cCountryRegionGhana", "#cCountryRegionGibraltar", "#cCountryRegionGreece", "#cCountryRegionGreenland", "#cCountryRegionGrenada",
                    "#cCountryRegionGuadeloupe", "#cCountryRegionGuam", "#cCountryRegionGuatemala", "#cCountryRegionGuinea", "#cCountryRegionGuineaBissau", "#cCountryRegionGuyana", "#cCountryRegionHaiti", "#cCountryRegionHonduras",
                    "#cCountryRegionHungary", "#cCountryRegionIraq", "#cCountryRegionItaly", "#cCountryRegionIvoryCoast", "#cCountryRegionJamaica", "#cCountryRegionJapan", "#cCountryRegionKazakhstan", "#cCountryRegionKenya", "#cCountryRegionKiribati",
                    "#cCountryRegionKosovo", "#cCountryRegionKuwait", "#cCountryRegionKyrgyzstan", "#cCountryRegionLaos", "#cCountryRegionLatvia", "#cCountryRegionLesotho", "#cCountryRegionLiberia", "#cCountryRegionLibya", "#cCountryRegionLiechtenstein",
                    "#cCountryRegionLithuania", "#cCountryRegionLuxembourg", "#cCountryRegionMacauSAR", "#cCountryRegionMadagascar", "#cCountryRegionMalawi", "#cCountryRegionMaldives", "#cCountryRegionMali", "#cCountryRegionMarshallIslands",
                    "#cCountryRegionMartinique", "#cCountryRegionMauritania", "#cCountryRegionMauritius", "#cCountryRegionMayotte", "#cCountryRegionMoldova", "#cCountryRegionMonaco", "#cCountryRegionMongolia", "#cCountryRegionMontenegro",
                    "#cCountryRegionMontserrat", "#cCountryRegionMorocco", "#cCountryRegionMozambique", "#cCountryRegionMyanmar", "#cCountryRegionNamibia", "#cCountryRegionNauru", "#cCountryRegionNepal", "#cCountryRegionNetherlands",
                    "#cCountryRegionNewCaledonia", "#cCountryRegionNicaragua", "#cCountryRegionNiger", "#cCountryRegionNigeria", "#cCountryRegionNiue", "#cCountryRegionMacedonia", "#cCountryRegionNorthernMarianaIslands", "#cCountryRegionNorway",
                    "#cCountryRegionOman", "#cCountryRegionPalau", "#cCountryRegionPalestinianTerritories", "#cCountryRegionPanama", "#cCountryRegionPapuaNewGuinea", "#cCountryRegionParaguay", "#cCountryRegionPoland", "#cCountryRegionPortugal",
                    "#cCountryRegionPuertoRico", "#cCountryRegionQatar", "#cCountryRegionRepublicOfCongo", "#cCountryRegionRomania", "#cCountryRegionRussia", "#cCountryRegionRwanda", "#cCountryRegionSaintKittsAndNevis", "#cCountryRegionSaintLucia",
                    "#cSaintMartin", "#cCountryRegionSaintVincentAndTheGrenadines", "#cCountryRegionSamoa", "#cCountryRegionSanMarino", "#cCountryRegionSaoTomeAndPrincipe", "#cCountryRegionSenegal", "#cCountryRegionSerbia", "#cCountryRegionSeychelles",
                    "#cCountryRegionSierraLeone", "#cCountryRegionSintMaarten", "#cCountryRegionSlovakia", "#cCountryRegionSlovenia", "#cCountryRegionSolomonIslands", "#cCountryRegionSomalia", "#cCountryRegionSouthKorea", "#cCountryRegionSouthSudan",
                    "#cCountryRegionSpain", "#cCountryRegionSuriname", "#cCountryRegionSweden", "#cCountryRegionSwitzerland", "#cCountryRegionTaiwan", "#cCountryRegionTajikistan", "#cCountryRegionTanzania", "#cCountryRegionTimorLeste", "#cCountryRegionTogo",
                    "#cCountryRegionTonga", "#cCountryRegionTrinidadAndTobago", "#cCountryRegionTunisia", "#cCountryRegionTurkey", "#cCountryRegionTurkmenistan", "#cCountryRegionTurksAndCaicosIslands", "#cCountryRegionTuvalu", "#cCountryRegionUSVirginIslands",
                    "#cCountryRegionUganda", "#cCountryRegionUkraine", "#cCountryRegionUruguay", "#cCountryRegionUzbekistan", "#cCountryRegionVanuatu", "#cCountryRegionVaticanCity", "#cCountryRegionVenezuela", "#cCountryRegionWesternSahara",
                    "#cCountryRegionYemen", "#cCountryRegionZambia", "#cCountryRegionZimbabwe"
                ]
            }
        }

        list_key = 'short_list' if short_list else 'long_list'
        return location_ids_by_language[language][list_key]

    def set_default_language_country(self, cdm):
        default_payload = {"deviceLanguage": "en",
                           "countryRegion": "US"}

        configuration_endpoint = "cdm/system/v1/configuration"
        response = cdm.patch_raw(configuration_endpoint, default_payload)
        assert response.status_code == 200, "Unable to set to default Country-Language through CDM"

    def power_cycle(self, udw):
        powerObj = Power(udw)
        response = powerObj.power_cycle()

    def goto_language_screen(self, spice):

        try:
            # Handler for cartridge screen at boot up
            for i in range(2):
                message_screen = spice.wait_for('#MessageLayout')
                message_screen.mouse_click()
                time.sleep(1)

        except Exception as e:
            logging.info('Exception occured : {}'.format(e))
            logging.info("OOBE workflow loaded without message screen")

        logging.info("Entering Language Screen")
        assert spice.wait_for("#DeviceLanguageView")
        logging.info("At Language Screen")

    def goto_country_screen(self, spice, udw, language="en"):
        logging.info("goto_country_screen - Choosing language: %s", language)
        self.goto_language_screen(spice)
        logging.info("goto_country_screen - Locating language: %s", language)
        langStr = "#option_" + language
        spice.homeMenuUI().menu_navigation(spice, "#DeviceLanguageView", langStr)

        # Country Selection Screen
        logging.info("goto_country_screen - Locating Country Screen")
        assert spice.wait_for("#OobeCountryRegionView")
        logging.info("At Country Screen")

    def goto_more_country_list_screen(self, spice, udw):
        self.goto_country_screen(spice, udw)
        spice.homeMenuUI().list_navigation(spice,
            ProSelectUIObjectIds.OobeCountryRegionView,
            ProSelectUIObjectIds.OobeMoreLocationsButton)

        # More Country List Screen
        logging.info("Entering More Country List Screen")
        assert spice.wait_for(ProSelectUIObjectIds.OobeMoreLocationsView)
        logging.info("At More Country List Screen")

    def select_country_from_more_country_list_screen(self, spice, cdm, udw, country="Afghanistan"):
        self.goto_more_country_list_screen(spice, udw)
        spice.homeMenuUI().list_navigation(spice,
            ProSelectUIObjectIds.OobeMoreLocationsView,
            ProSelectUIObjectIds.OobeCountryRegionPrefix + country)

        #Verify from CDM
        devicesetup_endpoint = "cdm/deviceSetup/v1/status"
        cdm_value = cdm.get(devicesetup_endpoint)
        logging.info(cdm_value["actionLanguageCountry"]["status"])
        assert cdm_value["actionLanguageCountry"]["status"] == "completed"

    def goto_network_settings_screen(self, spice, udw=None, country="#cCountryRegionUnitedStates"):
        self.goto_country_screen(spice, udw)
        spice.homeMenuUI().menu_navigation(spice, "#OobeCountryRegionView", country)

        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#OOBENetworkSettingsView")
        logging.info("At Network Setting Screen")

    def goto_proxy_settings_screen(self, spice, option="#NetworkContinueButton"):
        self.goto_network_settings_screen(spice)
        currentScreen = spice.wait_for("#OOBENetworkSettingsView")
        for x in range(11):
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
        spice.homeMenuUI().menu_navigation(spice, "#OOBENetworkSettingsView", option)

        # Proxy Screen
        logging.info("Entering Proxy Settings Screen")
        assert spice.wait_for("#ProxySettingsView")
        logging.info("At Proxy Settings Screen")

    def goto_oobe_ipv4_screen(self, spice, udw, option="#NetworkIPV4Button"):
        self.goto_network_settings_screen(spice)
        spice.homeMenuUI().menu_navigation(spice, "#OOBENetworkSettingsView", option)

    def get_printer_analytics(self, spice):
        spice.homeMenuUI().menu_navigation(spice, "#OobeSharePrinterAnalytics", "#YesButton")

    def firmware_update_config_page(self, spice):
        """ Scroll down and click on confirm to validate """
        spice.homeMenuUI().menu_navigation(spice, "#AutoPrinterUpdateMessageScreen", "#AutoButton")

    def select_firmware_update_option(self, spice):
        """ Select the option required for update"""
        spice.homeMenuUI().menu_navigation(spice, "#FWUpdateConfigScreen", "#AutoUpdateButton")
    
    def select_manual_ip_option(self, spice, udw):
        """Select manual ip option on ipv4 screen """
        spice.homeMenuUI().menu_navigation(spice, "#IPV4ConfigView", "#Manual")

    def goto_set_date_time_screen(self):
        ''' Click on continue at datetime screen '''

        logging.info("Entering set date and time Screen")
        self.spice.homeMenuUI().menu_navigation(self.spice, "#DateTimeView", "#applyButton")

    def get_thank_you_screen(self, spice):
        """ Check if the THank you screen is shown"""
        assert spice.wait_for("#thankYouScreen")

    def critical_firmware_update_page(self, spice):
        """ Click on critical firmware update Continue button """
        logging.info("Entering CFU info screen")
        spice.homeMenuUI().menu_navigation(spice, "#cfuInfo", "#continueButton", True, 2)
        self.skip_Issue_connect_to_internet_screen(spice)

    def skip_Issue_connect_to_internet_screen(self, spice):
        ''' Click on skip when issue arises connecting to server  '''
        spice.wait_for("#CheckingForUpdates")
        while spice.query_item("#CheckingForUpdates", 0)["activeFocus"] == True:
            time.sleep(5)
        try:
            spice.wait_for("#IccErrorView")
            if (spice.query_item("#IccErrorView")["activeFocus"] == True):
                logging.info("Issue in connecting to internet ")
                spice.homeMenuUI().menu_navigation(spice, "#IccErrorView", "#SkipButton")
        except:
            logging.info("Firmware Update is already set in OOBE!")

    def wait_for_firmware_checking_completion(self) -> bool:
        """
        Wait for 'Checking for firmware updates...' screen to complete.
        
        Returns:
            bool: True if completed successfully, False otherwise.
        """
        try:
            self.spice.wait_for("#CheckingForUpdates")
            
            # Wait for checking to complete (activeFocus becomes False)
            while self.spice.query_item("#CheckingForUpdates", 0)["activeFocus"] == True:
                time.sleep(1)
                
            return True
                
        except Exception as e:
            logging.warning(f"Error during firmware checking wait: {e}")
            return False

    def install_drivers_screen(self, spice):
        logging.info("Entering driver installation screen")
        spice.homeMenuUI().menu_navigation(spice, "#OobeInstallDriversView", "#DriversContinueButton")

    def goto_retrieve_code_screen(self, spice, option="#SkipProxyButton"):
        self.goto_proxy_settings_screen(spice)

        spice.homeMenuUI().menu_navigation(spice, "#ProxySettingsView", option)

        # Retrieve Code Screen
        logging.info("Entering Retrieve Code Screen")
        assert spice.wait_for("#RetrieveCode")
        logging.info("At Retrieve Code Screen")

    def cancel_retrieving_code(self, spice):
        self.goto_retrieve_code_screen(spice)

        spice.homeMenuUI().menu_navigation(spice, "#RetrieveCode", "#Cancel")

        # Connect Options Screen
        logging.info("Entering Connect Options Screen Screen")
        assert spice.wait_for("#OobeConnectOptions")
        logging.info("At Connect Options Screen Screen")

    def goto_printer_pin_screen(self, spice, option="#NetworkContinueButton"):

        self.goto_network_settings_screen(spice)
        spice.homeMenuUI().menu_navigation(spice, "#OOBENetworkSettingsView", option)

        # IP Address / PIN Screen
        logging.info("Entering IP Address / PIN Screen")
        assert spice.wait_for("#PrinterPinScreens")
        logging.info("At IP Address / PIN Screen")

    def goto_handsoff_screen(self, spice):

        self.goto_printer_pin_screen(spice)
        spice.homeMenuUI().menu_navigation(
            spice, "#PrinterPinScreens", "#PrinterPinDoneButton")

        # Hand Off Screen
        logging.info("Entering Hand Off Screen")
        assert spice.wait_for("#HandOffScreens")
        logging.info("At Hand Off Screen")

    def goto_network_screen(self, spice):

        self.goto_handsoff_screen(spice)
        currentScreen = spice.wait_for("#MessageLayout")
        currentScreen.mouse_wheel(180, 180)
        currentScreen.mouse_wheel(180, 180)
        assert spice.query_item("#ManualSetupButtonHandOff")[
            "activeFocus"] == True
        manualSetupButton = spice.wait_for(
            "#ManualSetupButtonHandOff SpiceText")
        manualSetupButton.mouse_click()

        # Network Settings Screen
        logging.info("Entering Network Settings Screen")
        assert spice.wait_for("#OOBENetworkSettingsView")
        logging.info("At Network Settings Screen")

    def goto_proxy_screen(self, spice):

        self.goto_network_settings_screen(spice)

        currentScreen = spice.wait_for("#OOBENetworkSettingsView")
        for x in range(11):
            currentScreen.mouse_wheel(180, 180)
        spice.homeMenuUI().menu_navigation(spice, "#OOBENetworkSettingsView", "#NetworkContinueButton")

        # Proxy Setup Screen
        logging.info("Entering Proxy Screen")
        assert spice.wait_for("#ProxySettingsView")
        logging.info("At Proxy Setup Screen")

        currentScreen = spice.wait_for("#MessageLayout")

        #TBD: fix the hard coded scrolls, menu_navigation() won't work because button is always active focus
        scrolls_to_skip_proxy_button = 5
        for n in range(scrolls_to_skip_proxy_button):
            currentScreen.mouse_wheel(180, 180)

        assert spice.query_item("#SkipProxyButton")[
            "activeFocus"] == True
        manualSetupButton = spice.wait_for("#SkipProxyButton")
        manualSetupButton.mouse_click()

    def skip_connect_to_internet_screen(self, spice):

        self.goto_proxy_screen(spice)

        logging.info("Entering connect to internet Screen")
        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#LearnMoreButton")

        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#SkipButton")
       
    def goto_date_time_screen(self, spice):

        self.goto_proxy_screen(spice)
        self.firmware_update_config_page(spice)
        self.select_firmware_update_option(spice)
        spice.homeMenuUI().menu_navigation(spice, "#DateTimeView", "#applyButton")
        
        # Date & Time Screen
        logging.info("Entering Date / Time Settings Screen")
        assert spice.wait_for("#DateTimeView")
        logging.info("At Date / Time Settings Screen")


    def goto_auto_printer_update_screen(self, spice):

        self.goto_date_time_screen(spice)
        spice.homeMenuUI().menu_navigation(spice, "#MenuListLayout", "#applyButton")

        # Auto Printer Update Screen
        logging.info("Entering Auto Printer Update Message Screen")
        assert spice.wait_for("#AutoPrinterUpdateMessageScreen")
        logging.info("At Auto Printer Update Message Screen")

    def goto_get_software_screen(self, spice):

        self.goto_auto_printer_update_screen(spice)
        currentScreen = spice.wait_for("#MessageLayout")
        currentScreen.mouse_wheel(180, 180)
        assert spice.query_item("#ContinueButton")["activeFocus"] == True
        manualSetupButton = spice.wait_for("#ContinueButton SpiceText")
        manualSetupButton.mouse_click()

        # Get Software Screen
        logging.info("Entering Get Software Screen")
        assert spice.wait_for("#GetSoftwareScreen")
        logging.info("At Get Software Screen")

    def goto_thank_you_screen(self, oobe):

        self.goto_date_time_screen(self.spice)

        # Thank You Screen
        logging.info("Entering Thank You Screen")
        assert self.spice.wait_for("#thankYouScreen")
        logging.info("At Thank You Screen")

    def goto_connect_to_internet_screen(self, spice, option="#SkipProxyButton"):

        self.goto_proxy_settings_screen(spice)
        spice.homeMenuUI().menu_navigation(spice, "#ProxySettingsView", option)

        # Connect to Internet Screen
        logging.info("Entering Connect to Internet Screen")
        assert spice.wait_for('#InternetConsentScreen')
        logging.info("At Connect to Internet Screen")

    def goto_retrieve_pairing_code_screen(self, spice, mode='e2e'):

        if(mode == 'e2e'):
            self.goto_proxy_settings_screen(spice)
            spice.homeMenuUI().menu_navigation(spice, "#ProxySettingsView", "#SkipProxyButton")

        else:
            self.goto_connect_to_internet_screen(spice)
            spice.homeMenuUI().menu_navigation(
                spice, "#InternetConsentScreen", "#ContinueButton")

        # Pairing Code Screen
        logging.info("Entering Pairing Code Screen")
        assert spice.wait_for("#RetrieveCode")
        logging.info("At Pairing Code Screen")

    def get_pairing_code(self, spice, mode='e2e'):

        self.goto_retrieve_pairing_code_screen(spice, mode)
        spice.wait_for("#ShowPairingCode")
        logging.info("At Pairing Code Screen")
        pair_code = spice.query_item("#PairingCode")["text"]
        #pair_code="KRWT JQZP"
        logging.info(f"Pairing code fetched is {pair_code}")
        return pair_code

    def verify_oobe_language_country(self, spice, udw, cdm, locale, oobe):
        try:
            configuration_endpoint = "cdm/system/v1/configuration"
            status_endpoint = "cdm/system/v1/status"
            devicesetup_endpoint = "cdm/deviceSetup/v1/status"

            maxtimeout = 240

            # Enable the OOBE workflow
            # self.enable_oobe(spice, udw)
            oobe.oobe_operations.enable_oobe(udw)

            # Recheck to make sure that the the Language Screen is loaded
            assert spice.wait_for("#DeviceLanguageView")
            logging.info("At Language Screen")

            # Fetch the objectid for the locale
            languageObjectId = self.get_language_objectid(locale)

            # Select the language
            spice.homeMenuUI().menu_navigation(
                spice, "#RadioButtonListLayout", languageObjectId)

            # Check the configuration_endpoint to see if the language is reflecting
            cdmvalue = cdm.get(configuration_endpoint)
            if locale not in ["zh_CN", "zh_TW"]:
                logging.info(cdmvalue["deviceLanguage"])
                logging.info(locale.split("_")[0])
                assert cdmvalue["deviceLanguage"] == locale.split("_")[0]
            else:
                assert cdmvalue["deviceLanguage"] == locale

            # Make sure that the country screen appears
            assert spice.wait_for("#OobeCountryRegionView")
            logging.info("At Country Screen")

            # Fetch the objectid for the country
            countryObjectId = self.get_country_objectid(locale.split("_")[1])

            # Click on the country
            logging.info("Entering Country Screen")
            assert spice.wait_for("#OobeCountryRegionView")
            logging.info("At Country Screen")
            spice.homeMenuUI().menu_navigation(
                spice, "#RadioButtonListLayout", countryObjectId)

            # Check the configuration_endpoint to see if the language is reflecting
            cdmvalue = cdm.get(configuration_endpoint)
            logging.info(cdmvalue["countryRegion"])
            assert cdmvalue["countryRegion"] == locale.split("_")[1]

            '''
            # Check the devicesetup_endpoint to see if the language is reflecting
            cdmvalue = cdm.get(devicesetup_endpoint)
            logging.info(cdmvalue["actionLanguageCountry"])
            assert cdmvalue["actionLanguageCountry"]["status"] == "completed"
            '''

        finally:
            # Disable the OOBE workflow
            oobe.oobe_operations.disable_oobe(udw)

    def goto_home_from_thankyou_screen(self, spice) -> None:
        """Returns to home screen from Thank You screen
        Args:
            spice: spice instance         
        Returns:
            None 
        """

        assert spice.wait_for("#thankYouScreen")
        logging.info("At ThankYou Screen")

        manualSetupButton = spice.wait_for("#continueButton")
        manualSetupButton.mouse_click()

    def enter_admin_pin(self, spice, password, confirmPassword):
        """Enters Admin Pin
        Args:
            spice: spice instance 
            password: new admin pin
            confirmPassword: confirming admin pin         
        Returns:
            None 
        """
        logging.info("Entering new passwords for admin")
        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#passwordButton")
        self.keyboardops.keyboard_set_text_with_out_dial_action(password)

        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#passwordConfirmButton")
        self.keyboardops.keyboard_set_text_with_out_dial_action(confirmPassword)

        currentScreen = spice.wait_for("#MessageLayout")
        currentScreen.mouse_wheel(90, 90)
        saveButton = spice.wait_for("#saveButton")
        saveButton.mouse_click()
        

    def goto_edit_admin_pin(self, spice):
        """Navigates from thank you screen to edit admin pin 
        Args:
            spice: spice instance        
        Returns:
            None 
        """
        currentScreen = spice.wait_for("#thankYouScreen")
        currentScreen.mouse_wheel(90, 90)
        editPinButton = spice.wait_for("#editPinButton SpiceText")
        editPinButton.mouse_click()

        assert spice.wait_for("#MessageLayout")
        #TBD: fix the hard coded scrolls, menu_navigation() won't work because button is always active focus
        scrolls_to_edit_button = 13
        for n in range(scrolls_to_edit_button):
            currentScreen.mouse_wheel(180, 180)
        
        editButton = spice.wait_for("#editButton")
        editButton.mouse_click()

    def goto_thankyou_screen_from_success_adminpin(self, spice):
        """ After successful admin pin change go back to thank you screen"""

        currentScreen = spice.wait_for("#passwordSuccessAlert")
        currentScreen.mouse_wheel(180, 180)
        manualSetupButton = spice.wait_for("#continueButton")
        manualSetupButton.mouse_click()

    def goto_thankyou_screen_from_adminpin_prompt(self, spice):
        """ Admin pin prompt screen go back to thank you screen"""
         
        logging.info("Step 1: Click edit pin")
    
        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#editPinButton")
        spice.homeMenuUI().menu_navigation(spice, "#MessageLayout", "#skipButton")

    def retry_admin_pin(self, spice):
        """ Click retry on invalid admin pin screen"""
        
        currentScreen = spice.wait_for("#passwordRejectedErrorAlert")
        #TBD: fix the hard coded scrolls, menu_navigation() won't work because button is always active focus
        scrolls_to_retry_button = 8
        for n in range(scrolls_to_retry_button):
            currentScreen.mouse_wheel(180, 180)
        
        editButton = spice.wait_for("#retryButton")
        editButton.mouse_click()
    
    def validate_setting_up_printer_screen(self, spice):
        assert spice.wait_for("#SettingUpPrinter")

    def validate_country_language_screen(self, spice, language="en", country="#cCountryRegionUnitedStates"):
        self.goto_language_screen(spice)
        languageId = "#option_" + language
        spice.homeMenuUI().list_navigation(spice, "#DeviceLanguageView", languageId)
        # Country Selection Screen
        logging.info("Entering Country Screen")
        assert spice.wait_for("#OobeCountryRegionView")
        logging.info("At Country Screen")
        spice.homeMenuUI().list_navigation(spice, "#DeviceLanguageView", country)
        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#OOBENetworkSettingsView")
        logging.info("At Network Setting Screen")

    def validate_oobe_url_screen(self, spice, cdm, language="en", country="#cCountryRegionUnitedStates"):
        self.goto_language_screen(spice)
        languageId = "#option_" + language
        spice.homeMenuUI().list_navigation(spice, "#DeviceLanguageView", languageId)
        # Country Selection Screen
        logging.info("Entering Country Screen")
        assert spice.wait_for("#OobeCountryRegionView")
        logging.info("At Country Screen")
        spice.homeMenuUI().list_navigation(spice, "#DeviceLanguageView", country)
        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#OOBENetworkSettingsView")
        logging.info("At Network Setting Screen")
        currentScreen = spice.wait_for("#OOBENetworkSettingsView")
        spice.homeMenuUI().list_navigation(spice, "#OOBENetworkSettingsView","#NetworkContinueButton")
        currentScreen = spice.wait_for("#OOBENetworkSettingsView")
        self.get_printer_analytics(spice)
        currentScreen = spice.wait_for("#AutoPrinterUpdateMessageScreen")
        logging.info("Entering FW Update Screen")
        spice.homeMenuUI().list_navigation(spice, "#AutoPrinterUpdateMessageScreen", "#DoNotCheckButton")
        logging.info("At FW Update Screen")
        currentScreen = spice.wait_for("#OobeInstallDriversView")
        logging.info("Entering url driver screen")
        identity_endpoint = cdm.IDENTITY_URL
        guidancePageProductNums = ["8X3D2A","8X3D4A","8X3D8A","8X3E1A","8X3E6A"]
        response = cdm.get(identity_endpoint)
        if response["productNumber"] in guidancePageProductNums:
            spice.homeMenuUI().list_navigation(spice, "#OobeInstallDriversView", "#DriversPrintButton")
        spice.homeMenuUI().list_navigation(spice, "#OobeInstallDriversView", "#DriversContinueButton", direction = "UP")
        logging.info("At url driver screen")

    def validate_ip_config_view(self,spice):
        assert spice.wait_for("#IPV4ConfigView")
    
    def validate_manual_ip_view(self,spice):
        assert spice.wait_for("#OOBEManualNetworkSettingsView")
    
    def navigate_to_network_page(self) -> bool:
        self.click_language_confirmation()
        self.click_country()
    
    def click_language_confirmation(self, language="#option_en"):
        self.spice.homeMenuUI().menu_navigation(self.spice, ProSelectUIObjectIds.OobeDeviceLanguageView, language)
        logging.info("Entering Language Confirmation Screen")

    def click_country(self, country="#cCountryRegionUnitedStates"):
        logging.info("Entering Country Screen")
        self.spice.homeMenuUI().menu_navigation(self.spice, ProSelectUIObjectIds.OobeCountryRegionView, country)
        logging.info("At Country Screen")

    def click_network_continue_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeNetworkSettingsView, ProSelectUIObjectIds.OobeNetworkContinueButton):
            return False
        continue_button = self.commonops.get_element(ProSelectUIObjectIds.OobeNetworkContinueButton)
        if not continue_button: return False
        return self.commonops.click(continue_button)
    
    def click_proxy_setup_skip_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeProxySettingsView, ProSelectUIObjectIds.OobeProxySettingsSkipButton):
            return False
        skip_button = self.commonops.get_element(ProSelectUIObjectIds.OobeProxySettingsSkipButton)
        if not skip_button: return False
        return self.commonops.click(skip_button)

    def click_share_analytics_no_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeSharePrinterAnalyticsView, ProSelectUIObjectIds.OobeSharePrinterAnalyticsNoButton):
            return False
        no_button = self.commonops.get_element(ProSelectUIObjectIds.OobeSharePrinterAnalyticsNoButton)
        if not no_button: return False
        return self.commonops.click(no_button)
    
    def click_firmware_update_auto_button(self) -> bool:
        """Clicks the "Auto" button on the OOBE Firmware Update options screen.

        Returns:
            bool: True if the button was clicked successfully, False otherwise.
        """
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeFirmwareUpdateOptionsView, ProSelectUIObjectIds.OobeFirmwareUpdateOptionsAutoButton):
            return False
        auto_button = self.commonops.get_element(ProSelectUIObjectIds.OobeFirmwareUpdateOptionsAutoButton)
        if not auto_button: return False
        return self.commonops.click(auto_button)
    
    def click_firmware_update_continue_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeFirmwareUpdateView, ProSelectUIObjectIds.OobeFirmwareUpdateContinueButton):
            return False
        continue_button = self.commonops.get_element(ProSelectUIObjectIds.OobeFirmwareUpdateContinueButton)
        if not continue_button: return False
        return self.commonops.click(continue_button)
    
    def click_firmware_update_cancel_button(self) -> bool:
        cancel_button = self.commonops.get_element(ProSelectUIObjectIds.OobeFirmwareUpdateCancelButton)
        if not cancel_button: return False
        return self.commonops.click(cancel_button)

    def click_firmware_update_error_skip_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeFirmwareUpdateErrorView, ProSelectUIObjectIds.OobeFirmwareUpdateErrorSkipButton):
            return False
        skip_button = self.commonops.get_element(ProSelectUIObjectIds.OobeFirmwareUpdateErrorSkipButton)
        if not skip_button: return False
        return self.commonops.click(skip_button)

    def click_install_driver_continue_button(self) -> bool:
        if not self.commonops.scroll_to(ProSelectUIObjectIds.OobeInstallDriversView, ProSelectUIObjectIds.OobeInstallDriversContinueButton):
            return False
        continue_button = self.commonops.get_element(ProSelectUIObjectIds.OobeInstallDriversContinueButton)
        if not continue_button: return False
        return self.commonops.click(continue_button)

    def validate_locations_lists(self, language):
        """Validate the short and long country lists for a given language.

        Args:
            language (str): The language to validate like 'en'

        Returns:
            None
        """
        self.validate_short_locations_list(language)
        self.spice.homeMenuUI().list_navigation(self.spice,
            ProSelectUIObjectIds.OobeCountryRegionView,
            ProSelectUIObjectIds.OobeMoreLocationsButton)
        self.validate_more_locations_list(language)

    def validate_short_locations_list(self, language):
        self.spice.homeMenuUI().validate_list_content(
            self.get_location_ids_by_language(language, True),
            ProSelectUIObjectIds.OobeCountryRegionView)

    def validate_more_locations_list(self, language):
        self.spice.homeMenuUI().validate_list_content(
            self.get_location_ids_by_language(language, False),
            ProSelectUIObjectIds.OobeMoreLocationsView)
