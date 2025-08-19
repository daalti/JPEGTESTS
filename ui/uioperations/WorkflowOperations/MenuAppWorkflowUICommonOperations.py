import time
import json
import logging
from dunetuf.cdm import CDM
from dunetuf.copy.copy import Copy
from datetime import datetime, timezone
from dunetuf.send.email.email import Email
from dunetuf.configuration import Configuration
from dunetuf.qmltest.QmlTestServer import QmlTestServer
from dunetuf.qmltest.QmlTestServer import QmlTestServerError
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ews.pom.quick_sets.quicksets_enum import QuickSetStartOption
from dunetuf.ui.uioperations.WorkflowOperations.objectidvalidation import objectidvalidation
from dunetuf.ui.uioperations.BaseOperations.IMenuAppUIOperations import IMenuAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.cdm.CdmEndpoints import *

positive_integer_key_pad_map = {
    0: "#key0PositiveIntegerKeypad",
    1: "#key1PositiveIntegerKeypad",
    2: "#key2PositiveIntegerKeypad",
    3: "#key3PositiveIntegerKeypad",
    4: "#key4PositiveIntegerKeypad",
    5: "#key5PositiveIntegerKeypad",
    6: "#key6PositiveIntegerKeypad",
    7: "#key7PositiveIntegerKeypad",
    8: "#key8PositiveIntegerKeypad",
    9: "#key9PositiveIntegerKeypad",
}

class MenuAppWorkflowUICommonOperations(IMenuAppUIOperations):


    device_language_options = {"option_en" : "English"   , "option_es" : "Español"     , "option_de" : "Deutsch"         , "option_ar" : "العربية"  , "option_ca" : "Català",
                               "option_cs" : "Čeština"   , "option_da" : "Dansk"       , "option_el" : "Ελληνικά"        , "option_fi" : "Suomi"    , "option_fr" : "Français",
                               "option_hr" : "Hrvatski"  , "option_hu" : "Magyar"      , "option_id" : "Bahasa Indonesia", "option_it" : "Italiano" , "option_ko" : "한글" ,
                               "option_nl" : "Nederlands", "option_nb" : "Norsk"       , "option_pl" : "Polski"          , "option_pt" : "Português", "option_ru" : "Русский",
                               "option_sk" : "Slovenčina", "option_sl" : "Slovenščina" , "option_sv" : "Svenska"         , "option_th" : "ไทย"      , "option_tr" : "Türkçe",
                               "option_ro" : "Română"    , "option_ja" : "xxx"         , "option_he" : "עברית"            , "option_zh-CN" : "[[]]"   , "option_zh-TW" : "[[]]", "option_bg" : "bulgarian",}

    country_code_iso = {"Argentina" : "AR"   , "United States" : "US", "None": "None"}

    device_language = { "option_en" : "en"    , "option_es" : "es"    , "option_de" : "de"    , "option_ar" : "ar"    , "option_ca" : "ca",
                        "option_cs" : "cs"    , "option_da" : "da"    , "option_el" : "el"    , "option_fi" : "fi"    , "option_fr" : "fr",
                        "option_hr" : "hr"    , "option_hu" : "hu"    , "option_id" : "id"    , "option_it" : "it"    , "option_ko" : "ko" ,
                        "option_nl" : "nl"    , "option_nb" : "nb"    , "option_pl" : "pl"    , "option_pt" : "pt"    , "option_ru" : "ru",
                        "option_sk" : "sk"    , "option_sl" : "sl"    , "option_sv" : "sv"    , "option_th" : "th"     , "option_tr" : "tr",
                        "option_ro" : "ro"    , "option_ja" : "ja"    , "option_he" : "he"    , "option_zh-CN" : "zh_dash_CN"   , "option_zh-TW" : "zh_dash_TW", "option_bg" : "bg",}

    inactivity_shutdown_options_dict = {
        "20 Minutes": [MenuAppWorkflowObjectIds.twenty_minutes_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_20mins],
        "1 Hour": [MenuAppWorkflowObjectIds.one_hour_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_1hrs],
        "2 Hours": [MenuAppWorkflowObjectIds.two_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_2hrs],
        "3 Hours": [MenuAppWorkflowObjectIds.three_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_3hrs],
        "4 Hours": [MenuAppWorkflowObjectIds.four_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_4hrs],
        "5 Hours": [MenuAppWorkflowObjectIds.five_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_5hrs],
        "6 Hours": [MenuAppWorkflowObjectIds.six_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_6hrs],
        "7 Hours": [MenuAppWorkflowObjectIds.seven_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_7hrs],
        "8 Hours": [MenuAppWorkflowObjectIds.eight_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_8hrs],
        "Never": [MenuAppWorkflowObjectIds.never_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_never]
    }

    jam_recovery_textimage_map = {
        "#auto_": "cAutomatic",
        "#off": "cOff",
        "#on": "cOn"
    }

    time_zone_option_dict = {
        # """String id for element value"""
        "GMT": "cGMT", # "(GMT) Coordinated Universal Time"
        "Baghdad": "cBaghdad", # "(GMT+03:00) Baghdad"
        "Bahia": "cBahia", # "(GMT-03:00) Salvador"
        "Cancun": "cCancun", # "(GMT-05:00) Chetumal"
        "Caracas": "cCaracas", # "(GMT-04:00) Caracas"
    }

    VOLUME_SLIDER_UNIT_X_VALUE = 2.436
    DISPLAY_BRIGHTNESS_SLIDER_UNIT_X_VALUE = 25.95
    MOUSE_CLICK_Y = 7.8

    def __init__(self, spice):
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.maxtimeout = 120
        self.workflow_common_operations = spice.basic_common_operations
        self._spice = spice

    def goto_menu(self, spice):

        # make sure that you are in home screen
        spice.goto_homescreen()

        # Implementation for floating dock implementation for hme screen
        try:
            spice.query_item("#floatingDock")
            logging.info("Printer Having Foating Dock Homescreen")
            self.goto_menu_app_floating_dock(spice)

        except:
            logging.info("Printer Having Regular Homescreen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
            homeApp = spice.query_item(MenuAppWorkflowObjectIds.view_homeScreen)
            spice.wait_until(lambda: homeApp["visible"] == True)
            logging.info("At Home Screen")
            # move the scrollbar firstly.
            self.workflow_common_operations.scroll_to_position_horizontal(0)
            logging.info("Reset horizontal scrollbar")
            time.sleep(2)
            # Printer goes into sleep mode once cdm/ews calls[that execution time is greater than sleep time] in test before UI naviation, for
            # this scenario need to check printer in sleep or not when perform UI navigation
            currentState = int(spice.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
            logging.debug('Printer Sleep status is: %s',currentState)
            if currentState >= 2:
                logging.debug("Waking up printer")
                spice.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
                time.sleep(2)

            # enter the menu screen
            logging.info("Entering Menu")
            adminApp = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp +" MouseArea" )
            # Wait for clickable situation
            spice.wait_until(lambda: adminApp["enabled"] == True)
            spice.wait_until(lambda: adminApp["visible"] == True)
            adminApp.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, timeout = 15.0)
        logging.info("At Menu Screen")
        time.sleep(1)

    def goto_menu_app_floating_dock(self, spice) -> None:
        logging.info("Go to menu app from floating dock")

        # Validate for object if not exist
        object = spice.wait_for(MenuAppWorkflowObjectIds.menu_app_button_floating_dock)

        # Wait for clickable situation
        spice.wait_until(lambda: object["enabled"] == True, 15)
        spice.wait_until(lambda: object["visible"] == True, 15)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)


    def goto_menu_scan_scan_to_email(self, spice):
        """
        Menu app-> Scan -> Scan to email
        @param spice:
        """
        self.goto_menu_scan(spice)
        scan_to_email_btn = spice.query_item(MenuAppWorkflowObjectIds.scan_to_email_button + " MouseArea")
        spice.validate_button(scan_to_email_btn)
        scan_to_email_btn.mouse_click()
        email_landing_view = spice.wait_for(EmailAppWorkflowObjectIds.email_app_view)
        spice.wait_until(lambda: email_landing_view["visible"] == True)

    def menu_navigation(self, spice, screen_id, menu_item_id,  dial_value: int = -180, select_option: bool = True, scrolling_value = 0.1, scrollbar_objectname = "#landingPageMenuAppListButtonScrollContainerverticalScroll", signInRequired = True):
        '''
        method searches and clicks a specified button on a specified menu
        Args:
            menu_item_id:pass the Object Id's in the form of string.
            screen_id:Object Id of the screen
            dial_value:Direction for dialing
            select_option:Select True to click on the element
            scrolling_value:scrolling value between 0 and 1
            scrollbar_objectname: scrollbar object name
        Returns:
        '''
        isVisible = False
        step_value = 0
        while (isVisible is False and step_value <= 1):
            try:
                current_screen = spice.wait_for(screen_id)
                isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                while (isVisible is False and step_value <= 1):
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    step_value = step_value + scrolling_value
                if select_option is True and isVisible is True:
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    if isVisible is True:
                        current_button = spice.query_item(screen_id + " " + menu_item_id)
                        # Clicking in the mid height of the button to avoid click on header or section
                        try:
                            current_button_height = round(current_button["height"]/2)
                            current_button.mouse_click(0, current_button_height)
                        except:
                            current_button.mouse_click()
                        time.sleep(1)
                        logging.info("Clicked Menu item : {0}".format(menu_item_id))

                        if signInRequired:
                            # Checking for signin screen
                            login_found = False
                            try:
                                if spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"]:
                                    login_found = True
                            except Exception:
                                try:
                                    if spice.query_item(MenuAppWorkflowObjectIds.login_admin_view)["visible"]:
                                        login_found = True
                                except Exception:
                                    logging.info("At Expected Menu")
                            
                            if login_found and signInRequired:
                                logging.info("Risham: trying to login")
                                self.perform_signIn(spice)
                                time.sleep(5)
                            else:
                                logging.info("At Expected Menu")
                        else:
                            logging.info("At Expected Display")
                    else:
                        logging.info("Menu item not found : {0}".format(menu_item_id))

            except Exception as e:
                logging.info("exception msg %s", e)
                if str(e).find("Query selection returned no items") != -1:
                    step_value = step_value + scrolling_value
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    time.sleep(5)
                    pass

    def scroll_position_utilities(self, menu_item_id, delta = 0, use_bottom_border = True):
        try:
            if use_bottom_border:
                bottom_border = MenuAppWorkflowObjectIds.utilities_section_bottom_border
            else:
                bottom_border = ""
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, menu_item_id , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , bottom_border , delta)
        except Exception:
            if use_bottom_border:
                bottom_border = MenuAppWorkflowObjectIds.empty_section_bottom_border
            else:
                bottom_border = ""
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, menu_item_id , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.empty_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , bottom_border , delta)

    def check_menu_visible(self, spice, screen_id, menu_item_id,  dial_value: int = -180, select_option: bool = True, scrolling_value = 0.1, scrollbar_objectname = "#landingPageMenuAppListButtonScrollContainerverticalScroll"):
        '''
        method searches and returns if a specified button on a specified menu exists or not.
        Args:
            menu_item_id:pass the Object Id's in the form of string.
            screen_id:Object Id of the screen
            dial_value:Direction for dialing
            select_option:Select True to click on the element
            scrolling_value:scrolling value between 0 and 1
            scrollbar_objectname: scrollbar object name
        Returns: isVisible
        '''
        logging.info("[check_menu_visible]")
        isVisible = False
        step_value = 0
        while (isVisible is False and step_value <= 1):
            try:
                current_screen = spice.wait_for(screen_id)
                isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                while (isVisible is False and step_value <= 1):
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    time.sleep(5)
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    step_value = step_value + scrolling_value
                if select_option is True and isVisible is True:
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    if isVisible is True:
                        logging.info("Menu item not found : {0}".format(menu_item_id))
                    else:
                        logging.info("Menu item not found : {0}".format(menu_item_id))

            except Exception as e:
                logging.info("exception msg %s", e)
                if str(e).find("Query selection returned no items") != -1:
                    step_value = step_value + scrolling_value
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    time.sleep(5)
                    pass
        logging.info("[check_menu_visible] isVisible={}".format(isVisible))
        return isVisible

    def wait_for_visible_enabled_and_click(self, spice, object_name):
        """
        Helper method to wait for an object to be visible and enabled, then click it.
        Includes comprehensive property checks without exception handling.
        
        Args:
            spice: The spice object
            object_name: The object identifier to wait for and click
        """
        clickable_item = spice.wait_for(object_name)
        
        # Check if object supports dictionary-like access
        if not hasattr(clickable_item, "__getitem__"):
            # If no property access, just click directly
            clickable_item.mouse_click()
            return
        
        # Check for visible property
        has_visible = False
        try:
            has_visible = isinstance(clickable_item["visible"], bool)
        except (KeyError, TypeError):
            has_visible = False

        # Check for enabled property  
        has_enabled = False
        try:
            has_enabled = isinstance(clickable_item["enabled"], bool)
        except (KeyError, TypeError):
            has_enabled = False

        # Wait for conditions only if properties exist and are not True
        if has_visible and has_enabled and (not clickable_item["visible"] or not clickable_item["enabled"]):
            spice.wait_until(lambda: clickable_item["visible"] == True and clickable_item["enabled"] == True)
        elif has_visible and not clickable_item["visible"]:
            spice.wait_until(lambda: clickable_item["visible"] == True)
        elif has_enabled and not clickable_item["enabled"]:
            spice.wait_until(lambda: clickable_item["enabled"] == True)
        
        # Perform the click
        clickable_item.mouse_click()

    def menu_navigation_radiobutton(self, spice, screen_id, menu_item_id, obj_id, dial_value: int = -180, select_option: bool = True, scrolling_value = 0.05, scrollbar_objectname="#landingPageMenuListListViewlist1ScrollBar", step_value = 0):
        '''
        method searches and clicks a specified button on a specified menu
        Args:
            menu_item_id:pass the Object Id's in the form of string.
            screen_id:Object Id of the screen
            obj_id: Object id of the radio button
            dial_value:Direction for dialing
            select_option:Select True to click on the element
            scrolling_value:scrolling value between 0 and 1
            scrollbar_objectname: scrollbar object name
            step_value : scrollbar position to start the search (0-1)
        Returns:
        '''
        isVisible = False
        while (isVisible is False and step_value <= 1):
            try:
                current_screen = spice.wait_for(screen_id)
                isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                while (isVisible is False and step_value <= 1):
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    time.sleep(5)
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    step_value = step_value + scrolling_value
                if select_option is True and isVisible is True:
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 1)
                    if isVisible is True:
                        current_button = spice.query_item(
                            screen_id + " " + obj_id)
                        current_button.mouse_click()
                        logging.info("At Expected Menu")
                    else:
                        logging.info("item not found")

            except Exception as e:
                logging.info("exception msg %s", e)
                if str(e).find("Query selection returned no items") != -1:
                    step_value = step_value + scrolling_value
                    self.workflow_common_operations.scroll_to_position_vertical(step_value, scrollbar_objectname)
                    time.sleep(5)
                    pass

    def goto_menu_info(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_info)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_info + " MouseArea")
        #current_button = spice.query_item(MenuAppWorkflowObjectIds.view_menulistLandingpage + " " +  MenuAppWorkflowObjectIds.menu_button_info)
        current_button.mouse_click()
        logging.info("At Expected Menu")
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo)
        logging.info("At Info Screen")

    def goto_menu_substrate(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_substrates)
        #current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_info + " MouseArea")"60ce8d1a-64b1-4850-875b-5b9acfc95963MenuApp"
        #current_button = spice.query_item(MenuAppWorkflowObjectIds.view_menulistLandingpage + " " +  MenuAppWorkflowObjectIds.menu_button_info)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_substrates + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        time.sleep(2)

    def goto_menu_subtrateLibrary(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_substratesList)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_substratesList + " MouseArea")
        #current_button = spice.query_item(MenuAppWorkflowObjectIds.view_menulistLandingpage + " " +  MenuAppWorkflowObjectIds.menu_button_info)
        current_button.mouse_click()
        logging.info("At Expected Menu")
        time.sleep(2)

    def goto_copy_quicksets(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_quicksets_copy)
        jobButton.mouse_click()

    def goto_scanToUSB_quicksets(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_quicksets_scantoUSB)
        jobButton.mouse_click()

    def goto_outputCard_media(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_media_cardTab)
        jobButton.mouse_click()

    def goto_menu_supplies(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_supplies)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_supplies + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_suppliesSummary)
        logging.info("At Supply Summary Screen")
        time.sleep(1)

    def goto_menu_directCartridgesView(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_supplies)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_supplies + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_directCartridgesView)
        logging.info("At Supply Cartridges Screen")
        time.sleep(1)

    def goto_menu_mediaApp(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_mediaApp + " MouseArea")
        current_button.mouse_click()
        logging.info("At MediaApp Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_mediaAppSummary)
        logging.info("At mediaApp Summary Screen")
        time.sleep(1)

    def goto_menu_tools_partner(self, spice, udw):

        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname

        # go to Tools menu
        spice.homeMenuUI().goto_menu_tools(spice)

        # go to Partner menu
        try:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.tools_menu_list, MenuAppWorkflowObjectIds.menu_button_partner,
                                                            MenuAppWorkflowObjectIds.tools_menu_list_scrollbar,
                                                            MenuAppWorkflowObjectIds.tools_menu_list_column, MenuAppWorkflowObjectIds.tools_menu_list_item)
        except Exception as ex:
            logging.warning("Unexpected exception while scrolling to Partners menu: {}".format(ex))

        but = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_partner + " MouseArea")
        but.mouse_click()

        # login
        but =  spice.wait_for("#authenticationPartnerModalTextField")
        but.mouse_click()
        time.sleep(1)

        assert spice.wait_for("#spiceKeyboardView")

        if(printerName.startswith("beam/beam") or ( printerName == "jupiter")):
            product_pin = "1768"
        else:
            product_pin = "12345678"

        but.__setitem__('displayText', product_pin) #just to show the password populated on keyboard
        but.__setitem__('inputText', product_pin)

        time.sleep(2)

        spice.query_item("#enterKey1").mouse_click()
        time.sleep(3)
        signInButton = spice.wait_for("#partnerAppSignInButton")
        signInButton.mouse_click()
        logging.info("At Partner Menu")
        time.sleep(2)

    def goto_menu_tools(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        cdmvalue= spice.cdm.get(spice.cdm.SYSTEM_CONFIGURATION)
        # object id will be localization when using different language

        try:
            if cdmvalue["deviceLanguage"] == "es":
                self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,"#UtilidadeslandingPageMenuAppListcolumn" , MenuAppWorkflowObjectIds.landingPage_Content_Item , "#UtilidadessectionBottomBorder")
            else:
                self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.utilities_section_bottom_border)
        except Exception:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.empty_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.empty_section_bottom_border)

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuTools)
        logging.info("At Tools Screen")

    def goto_menu_copy(self, spice):
        """
        It will enter the 'copy' menu.
        For Large Format printers, this will go directly to the copy menu;
        for other printer will only enter the list of 'copy' options.
        :param spice:
        """
        self.goto_menu(spice)

        large_format = True
        try:
            # lfp product?
            self.workflow_common_operations.scroll_position(
                    MenuAppWorkflowObjectIds.view_menulistLandingpage,
                    MenuAppWorkflowObjectIds.button_menu_copy_copy,
                    MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage,
                    MenuAppWorkflowObjectIds.app_column_name,
                    MenuAppWorkflowObjectIds.landingPage_Content_Item,
                    MenuAppWorkflowObjectIds.app_section_bottom_border
            )
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")
        except TimeoutError:
            # id copy product?
            try:
                self.workflow_common_operations.scroll_position(
                        MenuAppWorkflowObjectIds.view_menulistLandingpage,
                        MenuAppWorkflowObjectIds.menu_button_copy,
                        MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage,
                        MenuAppWorkflowObjectIds.app_column_name,
                        MenuAppWorkflowObjectIds.landingPage_Content_Item,
                        MenuAppWorkflowObjectIds.app_section_bottom_border
                )
                current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_copy + " MouseArea")
                large_format = False
            except TimeoutError as e:
                raise TimeoutError(f"Couldn't find copy element '{MenuAppWorkflowObjectIds.menu_button_copy}', nor '{MenuAppWorkflowObjectIds.button_menu_copy_copy}'", e)

        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuCopy_LargeFormat if large_format else MenuAppWorkflowObjectIds.view_menuCopy)
        logging.info("At Menu Copy Screen")

    def goto_menu_scan(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_scan , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.app_section_bottom_border)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_scan + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuScan)
        logging.info("At Menu Scan Screen")
        time.sleep(1)

    def goto_menu_scan_scan_to_network_folder(self, spice):
        """
        Menu app-> Scan -> Scan to network folder
        @param spice:
        """
        self.goto_menu_scan(spice)
        scan_to_usb_button = spice.wait_for(MenuAppWorkflowObjectIds.button_menu_scan_scan_to_folder)
        scan_to_usb_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_folder_screen)
        logging.info("At Menu Scan Screen")

    def goto_menu_scan_scan_to_usb(self, spice):
        """
        Menu app -> Scan -> Scan to usb
        :param spice:
        """
        self.goto_menu_scan(spice)
        scan_to_usb_button = spice.wait_for(MenuAppWorkflowObjectIds.button_menu_scan_scan_to_usb)
        scan_to_usb_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_scan_to_usb)
        logging.info("At Menu Scan Screen")

    def goto_menu_scan_scan_to_sharepoint(self, spice):
        """
        Menu app -> Scan -> Scan to sharepoint
        :param spice:
        """
        self.goto_menu_scan(spice)
        scan_to_sharepoint_button = spice.wait_for(MenuAppWorkflowObjectIds.scan_sharepoint)
        scan_to_sharepoint_button.mouse_click()
        logging.info("At Menu scan sharepoint quickset initial list")

    def goto_menu_scan_scan_to_computer(self, spice):
        """
        Menu app -> Scan -> Scan to computer
        :param spice:
        """
        self.goto_menu_scan(spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuScan, MenuAppWorkflowObjectIds.menu_button_scan_computer, MenuAppWorkflowObjectIds.scroll_bar_scan , MenuAppWorkflowObjectIds.scanFolderPage_column_name , MenuAppWorkflowObjectIds.scanFolderPage_Content_Item)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_scan_computer)
        current_button = spice.query_item(MenuAppWorkflowObjectIds.menu_button_scan_computer)
        current_button.mouse_click()  


    def goto_joblog(self, spice):
        spice.main_app.goto_job_queue_app()
        logging.info("At Job Log Screen Screen")
        time.sleep(1)

    def goto_job_queue_app(self, spice):
        self.wait_for_visible_enabled_and_click(spice, MenuAppWorkflowObjectIds.menu_button_jobApp)
        logging.info("At Job queue app Screen")
        time.sleep(1)

    def goto_menu_jobs(self, spice):
        self.goto_menu(spice)
        self.goto_job_queue_app(spice)

    def goto_menu_scan_scanToCloud(self,spice):
        # Navigate to Cloud Apps
        self.goto_menu_scan(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuScan, MenuAppWorkflowObjectIds.menu_button_scan_scanToCloud,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuScan+"ScrollBar")

    def goto_menu_print(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_print , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.app_section_bottom_border)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_print + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuPrint)
        logging.info("At Menu Print Screen")
        time.sleep(1)


    """
    Navigates to the Menu Job Storage screen.
    """
    def goto_menu_jobStorage(self, spice):
        self.goto_menu(spice)

        is_job_storage_available_in_menu = False
        try:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_jobStorage , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.app_section_bottom_border)
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.job_storage + " MouseArea")
            current_button.mouse_click()
            time.sleep(1)
            is_job_storage_available_in_menu = True
        except Exception as e:
            # If the print app is not found in the main screen, go directly to job storage.
            logging.info("Print app not found in Main Menu, trying to access job storage app directly")

        # If the job storage app is not available in the main menu, go to the print app and access the job storage app from there.
        if not is_job_storage_available_in_menu:
            self.goto_menu_print(spice)
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.job_storage + " MouseArea")
            current_button.mouse_click()
            time.sleep(1)

        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)

        logging.info("At Menu Job Storage Screen")
        time.sleep(1)

    def goto_menu_contacts(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_contacts)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_contacts + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuContacts)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_contacts)
        logging.info("At Menu Contacts Screen")
        time.sleep(1)

    def goto_menu_fax(self, spice):
        self.goto_menu(spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_fax , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.app_section_bottom_border)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_faxsetuphomeview)
        logging.info("At Fax Screen")
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax_setup_skip)
        currentElement.mouse_click()
        time.sleep(1)

    def goto_menu_settings_fax(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, FaxAppWorkflowObjectIds.button_menuFaxSettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettingsScreen, 3)
        logging.info("At Fax Settings Screen")

    def goto_menu_settings_email(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, EmailAppWorkflowObjectIds.button_menuEmailSettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(EmailAppWorkflowObjectIds.view_EmailSettingsScreen, 3)
        logging.info("At Email Settings Screen")

    def goto_menu_settings(self, spice, signInRequired = True):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_settings)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        logging.info("At settings Screen")

    def goto_security_settings(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_security + " MouseArea")
        jobButton.mouse_click()

    def goto_status_reports(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_reports_status)
        jobButton.mouse_click()

    def goto_ink_reports(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_reports_ink)
        jobButton.mouse_click()

    def goto_demo_reports(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_reports_demo)
        jobButton.mouse_click()

    def goto_event_log_reports(self, spice, password="12345678"):
        menu_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_reports_eventlog)
        menu_button.mouse_click()

        try:
            # Click in comboBoxList
            sign_in_combobox = spice.wait_for("#userSignInComboBox")
            sign_in_combobox.mouse_click()

            # Click in the Administrator option
            admin_option = spice.wait_for("#userSignInComboBoxItem_admin")
            admin_option.mouse_click()

            # Login
            spice.signIn.enter_creds(True, "admin", password)
        except:
            logging.info("Event log view is load without login")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_eventlog)
        logging.info("At Event Log Screen")

    def goto_maintenance_restore_settings(self, spice):
        menu_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore)
        menu_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings)
        logging.info("At Restore Settings Menu Screen")

    def goto_firmware_maintenace(self, spice):
        menu_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_firmware)
        menu_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_firmwareVersion)
        logging.info("At Firmware Screen")

    def goto_user_maintenance(self, spice):
        menu_button = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenance_userMaintenance_button)
        menu_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenance_user_maintenance)
        logging.info("At User Maintenance Screen")

    def goto_service_package_info(self, spice):
        menu_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_service_package)
        menu_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.service_package_info)
        logging.info("At Service Package screen")

    def goto_information_service(self, spice):
        prod_config = Configuration(spice.cdm)
        self.product_name = prod_config.productname
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_service_information_alt)
        else:
            jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_service_information)
        jobButton.mouse_click()

    def goto_pakages_substrateLibrary(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_substrateLibrary_package)
        jobButton.mouse_click()

    def goto_substrates_substrateLibrary(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_substrateLibrary_substrates)
        jobButton.mouse_click()

    def go_back(self, spice, parent):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_back_button.format(parent))
        jobButton.mouse_click()

    def goto_menu_settings_mismatch_actions(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        mismatch_actions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions)
        mismatch_actions_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)
        logging.info("At Mismatch Actions Screen")

    def goto_menu_settings_traysettings_trayassignment(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_traysettings,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_traySettings)
        logging.info("At Tray Settings screen")
        time.sleep(1)

    def goto_menu_settings_traysettings(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_traysettings,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_traySettings)
        logging.info("At Tray Settings screen")
        time.sleep(1)

    def goto_menu_Settings_print_optimize_setting(self, spice):
        self.goto_menu_settings_print_printquality(spice)
        # optimize_button = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_print_optimize,2)
        optimize_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_optimize,2)
        optimize_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_print_optimizesetting)
        time.sleep(2)
        logging.info("At optimize settings screen")
    def goto_optimize_setting_backround(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#backgroundSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_backround)
        sides_button.mouse_click()
        logging.info("At backround screen")

    def goto_optimize_setting_normalpaper(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#normalPaperModeSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_normalpaper)
        sides_button.mouse_click()
        logging.info("At Normal paper mode screen")

    def goto_optimize_setting_envelopeControl(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#envelopeControlModeSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_envelopeControl)
        sides_button.mouse_click()
        logging.info("At Envelope mode screen")

    def goto_optimize_setting_tray1cleaning(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#tray1CleaningSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_tray1Cleaning)
        sides_button.mouse_click()
        logging.info("At Envelope mode screen")

    def goto_optimize_setting_uniformitycontrol(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#uniformityControlSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_uniformityControl)
        sides_button.mouse_click()
        logging.info("At uniformityControl  mode screen")

    def goto_optimize_setting_heavyPaper(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        spice.homeMenuUI().scroll_to_list_item(
            spice,
            "#optimizesettingsMenuList",
            "#heavyPaperSettingsComboBox",
            "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_heavyPaper)
        sides_button.mouse_click()
        logging.info("At heavypaper  mode screen")
    
    def goto_optimize_setting_transferControl(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        self.workflow_common_operations.goto_item( "#transferControlSettingsComboBox","#optimizesettingsMenuList", scrollbar_objectname = "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_transferControl)
        sides_button.mouse_click()
        logging.info("At transfer  mode screen")

    def goto_optimize_setting_registrationMode(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        self.workflow_common_operations.goto_item( "#registrationSettingsComboBox","#optimizesettingsMenuList", scrollbar_objectname = "#optimizesettingsMenuListScrollBar")     
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_registrationControl)
        sides_button.mouse_click()
        logging.info("At registration  mode screen")

    def goto_optimize_setting_CaCo3Paper(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        view.mouse_wheel(0,-400)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_switch_caCo3Paper)
        logging.info("At Caco3Screen screen")

    def change_settings_optimizesettings_caCo3Paper(self, spice, enable_option = True):
        caCo3PaperToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_switch_caCo3Paper)
        if(caCo3PaperToggleSwitch["checked"] != enable_option):
            caCo3PaperToggleSwitch.mouse_click()
            time.sleep(1)
            assert caCo3PaperToggleSwitch["checked"] == enable_option, "caCo3 Paper Enable/Disbale failed"

    def verify_settings_optimizesettings_caCo3Paper(self, spice, enable_option):
        caCo3PaperToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_switch_caCo3Paper)
        assert caCo3PaperToggleSwitch["checked"] == enable_option, "caCo3 Pape value is not as expected in UI"

    def goto_optimize_setting_preRotationMode(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.combo_box_preRotationMode)
        sides_button.mouse_click()
        logging.info("At prerotaion  mode screen")

    def goto_optimize_setting_Restorescreen(self, spice):
        self.goto_menu_Settings_print_optimize_setting(spice)
        view = spice.wait_for("#optimizesettingsMenuList")
        self.workflow_common_operations.goto_item( "#resetOptimizationSettingsButton","#optimizesettingsMenuList", scrollbar_objectname = "#optimizesettingsMenuListScrollBar")
        sides_button = spice.wait_for("#resetOptimizationSettingsButton #resetOptimizationMenuButton")
        sides_button.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_reset_optimizesettings)
        logging.info("At Reset optimize screen screen")

    def goto_adjustpaper_Restorescreen(self, spice):
        self.goto_Settings_print_adjust_papertype(spice)
        view = spice.wait_for(MenuAppWorkflowObjectIds.view_settings_print_printmodes)
        self.workflow_common_operations.goto_item("#SettingsButton #resetPrintModeOption",
        "#printModesConfiguration", scrollbar_objectname = "#printModesConfigurationScrollBar")
        sides_button = spice.wait_for(MenuAppWorkflowObjectIds.reset_paper_Button)
        sides_button.mouse_click()        
        assert spice.wait_for("#restorePrintmodesView",2)
        logging.info("At Reset Adjust PaperScreen screen screen")

    def goto_menu_mediaApp(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_mediaApp + " MouseArea")
        current_button.mouse_click()
        logging.info("At MediaApp Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_mediaAppSummary)
        logging.info("At mediaApp Summary Screen")
        time.sleep(1)

    def goto_menuapp_tray1(self,spice):
        self.goto_menu_mediaApp(spice)
        trayButton = spice.wait_for(MenuAppWorkflowObjectIds.button_tray)
        trayButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_tray_details)
        time.sleep(1)
        logging.info("At mediaApp tray1 Screen")

    def goto_menuapp_tray2(self,spice):
        self.goto_menu_mediaApp(spice)
        trayButton = spice.wait_for(MenuAppWorkflowObjectIds.button_tray)
        trayButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_tray_details)
        time.sleep(1)
        logging.info("At mediaApp tray2 Screen")

    def click_mediatypes_tray2(self,spice):
        print("Click on modify Button")
        modify_button = spice.wait_for(MenuAppWorkflowObjectIds.button_modify)
        modify_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_tray_configuration)

        print("Click on Media type Option")
        sizeSettingsButton = spice.wait_for(MenuAppWorkflowObjectIds.button_media_type_settings)
        sizeSettingsButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_media_type_selection)
        print("Click on Media type screen")
        
    def goto_settings_print_printQuality(self,spice):
        self.goto_menu_settings_print(spice)
        printquality_button= spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_printquality, 2)
        printquality_button.mouse_click()
        logging.info("At Print Quality Screen")
        
    def goto_settings_print_printQuality_colorAdjustment(self, spice):
        self.goto_settings_print_printQuality(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.button_settings_print_printquality_colorAdjustment,60).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_print_printquality_colorAdjustment), "not in colorAdjustmentView" #check view
        logging.info("At colorAdjustment screen")
    
    def goto_settings_print_quality_auto_sense_behavior(self, spice):
        """Navigate to the Auto Sense Behavior settings screen under Print Quality.
        
        This method navigates from the main menu through Settings -> Copy/Print -> Print Quality
        to the Auto Sense Behavior configuration screen. It performs the necessary UI
        navigation and validation to ensure the user reaches the correct settings page.
        
        Args:
            spice: The spice automation framework instance used for UI interactions.
            
        Raises:
            AssertionError: If the Auto Sense Behavior view is not displayed after navigation.
        """
        self.goto_settings_print_printQuality(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_printQuality_autoSenseBehavior, 20).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_printQuality_autoSenseBehavior), "not in autoSenseBehaviorView"
        logging.info("At autosenesBehavior screen")

    def goto_Settings_print_adjust_papertype(self, spice):
        self.goto_settings_print_printQuality(spice)
        papertype_button = spice.wait_for(MenuAppWorkflowObjectIds.papertype_printmode_Text_Image,2)
        papertype_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_print_printmodes)
        logging.info("At adjust papertype menu list  screen")
    
    def goto_menu_Settings_print_printmodes_paper_type_option(self, spice,paper_type):
        self.goto_Settings_print_adjust_papertype(spice)
        i = 0
        paper_type_button = ""
        for x in range(15):
            paper_type_text = spice.wait_for("#adjustPaperTypesTextImageBranch"+ str(x) +" #contentItem",2)['text']
            if str(paper_type_text) == str(paper_type):
                paper_type_button = spice.wait_for(f"#adjustPaperTypesTextImageBranch{x}_2infoBlockRow")
                paper_type_button.mouse_click()
                break
            i = i + 1
        time.sleep(2)
        if i >= 4 :
            currentScreen.mouse_wheel(0,-400)
            #Scroll up to make Hook Operations Button visible
            scrollbar = spice.wait_for("#printModesConfigurationScrollBar")
            scrollbar.__setitem__("position",0.2)
            scrollbar.__setitem__("position",0.2)
        time.sleep(2)

    def goto_menu_Settings_print_printmodes_find_value(self, spice,print_mode):
        i = 0
        print_mode_button = ""
        for x in range(10):
            print_mode_text = spice.wait_for("#comboBoxBranch"+ str(x) +" #contentItem",2)['text']
            if str(print_mode_text) == str(print_mode):
                text_value = spice.wait_for(f"#comboBoxBranch{x} #SettingsSpiceComboBox #textColumn SpiceText[visible=true]",50)["text"]
                return text_value 
                break
            i = i + 1
        time.sleep(2)
        currentScreen = spice.wait_for("#printModesComboBoxView")
        if i >= 4 :
            currentScreen.mouse_wheel(0,-400)
            #Scroll up to make Hook Operations Button visible
            scrollbar = spice.wait_for("#printModesComboBoxViewScrollBar")
            scrollbar.__setitem__("position",0.2)
            scrollbar.__setitem__("position",0.2)
            #time.sleep(5)
        time.sleep(2)

    def goto_menu_Settings_print_printmodes_printmode_option(self, spice,print_mode):
        i = 0
        print_mode_button = ""
        for x in range(10):
            print_mode_text = spice.wait_for("#comboBoxBranch"+ str(x) +" #contentItem",2)['text']
            if str(print_mode_text) == str(print_mode):
                print_mode_button = spice.wait_for(f"#comboBoxBranch{x} #SettingsSpiceComboBox")
                print_mode_button.mouse_click()
                break
            i = i + 1
        time.sleep(2)
        currentScreen = spice.wait_for("#printModesComboBoxView")
        if i >= 4 :
            currentScreen.mouse_wheel(0,-400)
            #Scroll up to make Hook Operations Button visible
            scrollbar = spice.wait_for("#printModesComboBoxViewScrollBar")
            scrollbar.__setitem__("position",0.2)
            scrollbar.__setitem__("position",0.2)
        time.sleep(2)
        

    def goto_menu_traysettings_paperoutaction(self, spice):
        self.goto_menu_settings_traysettings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_traySettings, MenuAppWorkflowObjectIds.menu_button_settings_traysettings_paperoutaction, scrollbar_objectname = MenuAppWorkflowObjectIds.view_traySettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperoutaction)
        logging.info("At Paper out action screen")

    def goto_menu_Settings_print_printmodes_papertype_print_option(self, spice,print_mode):
        i = 0
        print_mode_button = ""
        for x in range(10):
            print_mode_text = spice.wait_for("#comboBoxBranch"+ str(x) +" #contentItem",2)['text']
            if str(print_mode_text) == str(print_mode):
                print_mode_button = "#comboBoxBranch"+ str(x)
                break
            i = i + 1
        time.sleep(2)
        currentScreen = spice.wait_for("#printModesComboBoxView")
        if i >= 4 :
            currentScreen.mouse_wheel(0,-400)
            #Scroll up to make Hook Operations Button visible
            scrollbar = spice.wait_for("#printModesComboBoxViewScrollBar")
            scrollbar.__setitem__("position",0.2)
            scrollbar.__setitem__("position",0.2)
            #time.sleep(5)
        current_button = spice.query_item(print_mode_button)
        current_button.mouse_click()
        time.sleep(2)

    def goto_menu_traysettings_trayassignment(self, spice):
        self.goto_menu_settings_traysettings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_traySettings, MenuAppWorkflowObjectIds.menu_button_settings_traysettings_trayassignment, scrollbar_objectname = MenuAppWorkflowObjectIds.view_traySettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_trayassignment)
        logging.info("At Tray Assignment screen")

    def goto_menu_traysettings_traylock(self, spice):
        self.goto_menu_settings_traysettings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_traySettings, MenuAppWorkflowObjectIds.menu_button_settings_traysettings_traylock, scrollbar_objectname = MenuAppWorkflowObjectIds.view_traySettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_traylock)
        logging.info("At Tray Lock screen")

    def click_autocontinue_action_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_autocontinue_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_paperoutaction, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_paper_out_action)

    def click_autocontinue_timeout_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_autocontinue_timeout_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_paperoutaction, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_paper_out_action)

    def click_defaulttray_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_trayassignment_defaulttray_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_trayassignment, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tray_assignment)

    def click_traylock_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_traylock_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_traySettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tray_settings)

    def click_use_requested_tray_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_use_requested_tray_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_traySettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tray_settings)

    def click_use_another_tray_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_use_another_tray_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_traySettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tray_settings)

    # Added for Fax Speaker Mode
    def click_fax_speaker_mode_combobox(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_fax_speaker_mode_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_fax, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_fax)

    def goto_mismatch_actions(self, spice):
        self.workflow_common_operations.scroll_to_position_vertical(0.2, MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        mismatch_actions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions)
        mismatch_actions_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)
        logging.info("At Mismatch Actions Screen")

    def goto_menu_settings_mismatch_actions_substrate_mismatch(self, spice):
        self.goto_menu_settings_mismatch_actions(spice)
        substrate_mismatch_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_substrate_mismatch)
        substrate_mismatch_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_substrateMismatch)
        logging.info("At Substrate Mismatch Screen")

    def set_mismatch_actions_print_anyway(self, spice):
        print_anyway_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_print_anyway)
        print_anyway_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_substrateMismatch)

    def set_mismatch_actions_pause_and_ask(self, spice):
        mismatch_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_pause_and_ask)
        mismatch_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_substrateMismatch)

    def set_mismatch_actions_hold_and_continue(self, spice):
        hold_and_continue_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_hold_job)
        hold_and_continue_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_substrateMismatch)

    def goto_menu_settings_printerUpdate(self, spice):
        self.goto_menu_settings(spice)
        firmware_update = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate)
        firmware_update.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("At Printer Update WF Screen")

    def goto_printerUpdate(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("At Printer Update WF Screen")

    def goto_outputDestination(self, spice):
        self.menu_navigation(spice,MenuAppWorkflowObjectIds.view_menuSettings,"#outputDestinationsSettingsTextImage_firstinfoBlockRow" )

    def goto_menu_settings_printerUpdate_autoUpdateOptions(self, spice):
        self.goto_menu_settings(spice)
        self.goto_printerUpdate(spice)
        firmware_update_autoupdateoptions = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions)
        firmware_update_autoupdateoptions.mouse_click()
        time.sleep(2)
        # Check if Sign-in screen exists
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("No Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("At Printer Update IRIS Message Screen")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris)

    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1.0, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def match_privacy_notice_content(self, spice, is_auto = True):
        assert spice.wait_for("#alertDetailBlock")
        assert spice.wait_for("#alertDetailDescription")
        assert spice.wait_for("#alertDetailBlock #alertDetailDescription")
        alert_description = spice.query_item("#alertDetailBlock #alertDetailDescription SpiceText[visible=true]")["text"]
        if is_auto:
            option_text = "Auto Update (Recommended)"
        else:
            option_text = "Notify When Available"
        correct_string = "Setting: " + option_text + "\n\nWhen set to \"" + option_text + "\", your printer will connect to HP to check for or install firmware updates. Necessary data will be collected and used to provide functionality. Visit hp.com/privacy to learn more."
        print(correct_string)
        assert alert_description == correct_string
        logging.info("Privacy Notice content matched")

    def set_printerUpdate_allowAutoUpdate_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        autoUpdateButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate)
        autoUpdateButton.mouse_click()
        saveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save)
        saveButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        self.match_privacy_notice_content(spice,True)
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_ok)
        ok_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")
        time.sleep(1)

    def goto_menu_settings_print(self, spice):
        item = spice.check_item(MenuAppWorkflowObjectIds.menu_button_menuApp)
        if item != None and item["visible"] == True:
            self.goto_menu_settings(spice)
        else:
            self._spice.home.goto_home_settings_app(spice)
        spice.homeMenuUI().workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.menu_button_settings_print,MenuAppWorkflowObjectIds.view_menuSettings, select_option = False, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        printOptions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print)
        printOptions_button.mouse_click()
        logging.info("At Print Settings Screen")

    def goto_menu_settings_print_lesspapercurl(self, spice):
        #Check for less paper curl under Print
        self.goto_menu_settings_print(spice)

        spice.wait_for("#printSettingsMenuList", timeout = 10)

        try:
            spice.wait_for("#lessPaperCurlWFMenuSwitch", timeout = 10)
        except Exception as e:
            #If less paper curl isn't under Print, it will be under Print Quality
            logging.info("Less Paper Curl not found under Print. Looking under Print Quality")
            self.workflow_common_operations.goto_item("#printQualitySettingsTextImage", "#printSettingsMenuList", 0, True, 0.1, "#printSettingsMenuListScrollBar")
            spice.wait_for("#printQualityMenuList", timeout = 10)
            
            try:
                spice.wait_for("#lessPaperCurlWFMenuSwitch", timeout = 10)
            except Exception as f:
                #Catch the exception to print this line
                logging.info("Less Paper Curl not found under Print Quality")
                #but still raise the error since we didn't find it
                raise
        
        logging.info("At Screen with Less Paper Curl")

    def goto_menu_settings_print_defaultprintoptions_paperOptions(self, spice):
        self.goto_menu_settings_print(spice)
        defaultprintoptions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions)
        defaultprintoptions_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)
        paperOptions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_paperOptions)
        paperOptions_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperOptions)
        logging.info("Paper Options screen")

    def goto_menu_settings_print_defaultprintoptions(self, spice):
        self.goto_menu_settings_print(spice)
        defaultprintoptions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions)
        defaultprintoptions_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)
        logging.info("At Default Print Options screen")

    def goto_job_settings(self, spice):
        jobButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings + " MouseArea")
        jobButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_jobs_settings)

    def goto_menu_settings_jobs_settings(self, spice):
        self.goto_menu_settings(spice)
        logging.info("At Expected Menu Setting job")
        self.goto_job_settings(spice)
        logging.info("At Job Settings WF Screen")

    def goto_menu_settings_coloroptions(self, spice, net, locale):
        self.goto_menu_settings_print_defaultprintoptions(spice)
        self.goto_advancedoptions_from_defaultprintoptions(spice, net, locale)
        coloroptions_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_coloroptions)
        coloroptions_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_coloroptions)
        logging.info("At Default Print Options screen")

    def goto_defaultprintoptions(self, spice):
        defaultprintoptions_button = spice.wait_for("#printSettingsSettingsTextImage_firstinfoBlockRow")
        defaultprintoptions_button.mouse_click()
        logging.info("At Default Print Options screen")

    def click_defaultprintoptions_sides(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_defaultprintoptions, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_print_default_print_options)

    def check_printerUpdate_allowAutoUpdate_visible(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate)

    def check_printerUpdate_notifyWhenAvailable_visible(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable)

    def check_printerUpdate_doNotCheck_visible(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotCheck)


    def set_printerUpdate_notifyWhenAvailable_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        notifyButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable)
        notifyButton.mouse_click()
        saveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save)
        saveButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        self.match_privacy_notice_content(spice,False)
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_ok)
        ok_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)

    def set_printerUpdate_doNotCheck_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        donotcheckButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotCheck)
        donotcheckButton.mouse_click()
        saveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save)
        saveButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set DoNot Check to true")
        time.sleep(1)

    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1.0, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def goto_menu_settings_printer_update_next(self, spice):
        self.workflow_common_operations.scroll_to_position_vertical(0.8, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def goto_menu_settings_general(self, spice, signInRequired = True):
        self.goto_menu_settings(spice, signInRequired)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_display(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("At Display Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_display_continuable_event(self, spice):
        self.goto_menu_settings_general_display(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_display_settings)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings,MenuAppWorkflowObjectIds.menu_button_settings_general_display_continuable_event)

    def goto_menu_settings_general_jam_recovery(self, spice):
        self.goto_menu_settings(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        self.workflow_common_operations.scroll_to_position_vertical(0.4, MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")
        jam_recovery_option = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_jam_recovery)
        jam_recovery_option.mouse_click()
        jam_recovery_box_view = spice.wait_for(MenuAppWorkflowObjectIds.view_jamRecovery)
        spice.wait_until(lambda:jam_recovery_box_view["visible"])
        logging.info("At Jam Recovery Screen")

    def get_jam_recovery_option_text(self, spice, button_id):
        self.goto_menu_settings_general_jam_recovery(spice)
        autoButton = spice.wait_for(button_id)
        autoButton.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_jam_recovery)
        textView = "#" + self.jam_recovery_textimage_map[button_id] + "itemContainerTextImage SpiceText[visible=true]"
        jam_recovery_option_text_view = spice.wait_for(textView)
        return jam_recovery_option_text_view['text']


    def set_continuable_event_value(self,spice,type):
        if (type == "Manual"):
            spice.wait_for("#Manual SpiceText") ["text"] == "Manual"
            spice.wait_for("#Auto-Continue").mouse_click()
        elif (type == "Auto-Continue"):
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings,"#continuableEventsWFMenuComboBox #SettingsSpiceComboBox")
            spice.wait_for("#Manual").mouse_click()

    def get_updated_continuable_event_manual_value_ui(self,spice):
        spice.wait_for("#displayMenuList #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #BreadcrumbView #BackButton").mouse_click()
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")
        return spice.wait_for("#ManualitemContainerTextImage SpiceText[visible=true]") ["text"]

    def get_updated_continuable_event_autocontinue_value_ui(self,spice):
        spice.wait_for("#displayMenuList #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #BreadcrumbView #BackButton").mouse_click()
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")
        return spice.wait_for("#Auto-ContinueitemContainerTextImage SpiceText[visible=true]") ["text"]

    def get_continuable_event_after_reboot(self,spice):
        return spice.wait_for("#Auto-ContinueitemContainerTextImage SpiceText[visible=true]") ["text"]

    def goto_menu_settings_general_dateTime(self,spice):
        self.goto_menu_settings_general(spice)

        try:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.datetime_settings)
        except Exception as e:
            logging.info(f"Product has automatic datetime by default: {e}")
            # Disable automatic datetime by default
            spice.cdm.patch(spice.cdm.CLOCK_CONFIGURATION, {"systemTimeSync": "none"})
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.automatic_datetime_settings)
        finally:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime)
            logging.info("At Date time Settings Screen")
            time.sleep(1)

    def perform_signIn(self,spice):
        spice.signIn.select_sign_in_method("admin", None)
        spice.signIn.enter_creds(True, "admin", "12345678")

    def goto_menu_settings_selection_and_productivity_view(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_selection_and_productivity + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_selection_and_productivity)

    def goto_selection_and_productivity_view(self, spice):
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_selection_and_productivity + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_selection_and_productivity)

    def goto_menu_settings_paper_type_protection_view(self,spice):
        self.goto_menu_settings_selection_and_productivity_view(spice)
        time.sleep(1)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_paper_type_protection + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paper_type_protection)
        time.sleep(1)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_mediafamily_0 + " MouseArea")
        current_button.mouse_click()

    def goto_menu_settings_general_dateTime_timeZone(self,spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_timeZone)
        ##Assert Time Zone Screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_timeZone)
        logging.info("At time zone continent Settings Screen")

    def goto_menu_settings_general_dateTime_time(self,spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname=MenuAppWorkflowObjectIds.dateTime_scrollbar)
        ##Assert Time Zone Screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        logging.info("At Time Settings Screen")

    def goto_menu_settings_general_dateTime_date(self,spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.goto_date_from_menu_settings_general_date_time(spice)

    def goto_date_from_menu_settings_general_date_time(self, spice):
        """
        goto set Data screen from menu -> settings->general -> date and time screen
        UI should be in Menu -> Settings-> General -> Date and Time screen
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_date, scrollbar_objectname=MenuAppWorkflowObjectIds.dateTime_scrollbar)
        spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        logging.info("At Date Settings Screen")

    def press_exitButton_dateTimeScreens(self,spice):
        exitButton = spice.wait_for(MenuAppWorkflowObjectIds.dateTime_exit)
        exitButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime)
        logging.info("At Date Time Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_dateTime_updatedate(self,spice):
        self.goto_menu_settings_general_dateTime(spice)
        previous_time = spice.query_item("#timeSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("previous_time = ", previous_time)
        previous_hour = previous_time[0:2]
        print("previous_hour = ", previous_hour)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_date,scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        spice.wait_for("#Day #upBtn").mouse_click()
        if spice.check_item("#dateSettingsListViewlist1ScrollBar")!=None:
            self.workflow_common_operations.goto_item("StringIds.cMonth", MenuAppWorkflowObjectIds.view_dateTime_date, select_option = False, scrollbar_objectname="#dateSettingsListViewlist1ScrollBar")
        spice.wait_for("#Month #upBtn").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.date_applyButton)
        applyButton.mouse_click()
        present_time = spice.query_item("#timeSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("present_time = ", present_time)
        present_hour = present_time[0:2]
        print("present_hour = ", present_hour)
        previous_hour == present_hour
        logging.info("At DateTime Settings Screen")
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_date, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        spice.wait_for("#Day #downBtn").mouse_click()
        if spice.check_item("#dateSettingsListViewlist1ScrollBar")!=None:
            self.workflow_common_operations.goto_item("StringIds.cMonth", MenuAppWorkflowObjectIds.view_dateTime_date, select_option = False, scrollbar_objectname="#dateSettingsListViewlist1ScrollBar")
        spice.wait_for("#Month #downBtn").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.date_applyButton)
        applyButton.mouse_click()
        logging.info("At DateTime Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_dateTime_updatetime(self,spice):
        self.goto_menu_settings_general_dateTime(spice)
        previous_date = spice.query_item("#dateSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("previous_date = ", previous_date)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        spice.wait_for("#Hour #upBtn").mouse_click()
        spice.wait_for("#Minute #downBtn").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()
        present_date = spice.query_item("#dateSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("present_date = ", present_date)
        previous_date == present_date
        logging.info("At DateTime Settings Screen")
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        spice.wait_for("#Hour #downBtn").mouse_click()
        spice.wait_for("#Minute #upBtn").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()
        time.sleep(1)

    def goto_menu_settings_general_update_date(self, spice):
        self.goto_menu_settings_general_dateTime(spice)
        previous_date = spice.wait_for("#dateSettingsTextImageBranch_2infoBlockRow SpiceText[visible=true]")["text"]
        print("previous_date = ", previous_date)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_date, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        # To test the date change functionality, simply modify the day number
        # Since we have date +/- selectors, we need to check that we are not at the upper limit where the + button would be disabled
        dayText=spice.wait_for("#Day")
        dayNumber= dayText["value"]
        if dayNumber >= 28:
            increaseDecreaseDay = False
        else:
            increaseDecreaseDay = True

        if increaseDecreaseDay:
            self.wait_for_visible_enabled_and_click(spice, "#Day #upBtn")
        else:
            self.wait_for_visible_enabled_and_click(spice, "#Day #downBtn")
        self.wait_for_visible_enabled_and_click(spice, MenuAppWorkflowObjectIds.date_applyButton)
        time.sleep(5)
        present_date = spice.wait_for("#dateSettingsTextImageBranch_2infoBlockRow SpiceText[visible=true]")["text"]
        print("present_date = ", present_date)
        assert previous_date != present_date, "Date not changed"
        logging.info("At DateTime Settings Screen")
        time.sleep(2)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen, MenuAppWorkflowObjectIds.dateTime_date, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        if increaseDecreaseDay:
            self.wait_for_visible_enabled_and_click(spice, "#Day #downBtn")      
        else:
            self.wait_for_visible_enabled_and_click(spice, "#Day #upBtn")
        
        self.wait_for_visible_enabled_and_click(spice, MenuAppWorkflowObjectIds.date_applyButton)
        time.sleep(5)
        present_date = spice.wait_for("#dateSettingsTextImageBranch_2infoBlockRow SpiceText[visible=true]")["text"]
        assert previous_date == present_date, "Date not restored"

    def goto_menu_settings_general_update_time(self, spice):
        self.goto_menu_settings_general_dateTime(spice)
        previous_time = spice.query_item("#timeSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("previous_time = ", previous_time)
        previous_hour = previous_time[0:2]
        previous_minute = previous_time[3:5]
        print("previous_hour = ", previous_hour)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen,  MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        # Handle cases where hour is 12 (when AM/PM) or 23 (when 24 hours) and cannot be increased
        if previous_hour == "12" or previous_hour == "23":
            adjust_hour_btn = "#downBtn"
            restore_hour_btn = "#upBtn"
        else:
            adjust_hour_btn = "#upBtn"
            restore_hour_btn = "#downBtn"
        # Handle cases where minute is 00 and cannot be decreased
        if previous_minute == "00":
            adjust_minute_btn = "#upBtn"
            restore_minute_btn = "#downBtn"
        else:
            adjust_minute_btn = "#downBtn"
            restore_minute_btn = "#upBtn"
        spice.wait_for(f"#Hour {adjust_hour_btn}").mouse_click()
        spice.wait_for(f"#Minute {adjust_minute_btn}").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()
        time.sleep(5)
        present_time = spice.query_item("#timeSettingsTextImageBranch_2infoBlockRow SpiceText")["text"]
        print("present_time = ", present_time)
        present_hour = present_time[0:2]
        print("present_hour = ", present_hour)
        assert previous_hour != present_hour, "Time not changed"
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.date_time_screen,  MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname = "#dateTimeViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        spice.wait_for(f"#Hour {restore_hour_btn}").mouse_click()
        spice.wait_for(f"#Minute {restore_minute_btn}").mouse_click()
        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()
        time.sleep(5)

    def goto_menu_settings_general_dateTime_Time_TimeFormat(self,spice,cdm):
        configuration_endpoint = CdmEndpoints.CLOCK_CONFIGURATION
        r = cdm.get_raw(configuration_endpoint)
        data = r.json()
        print(data)

        if data.get("timeFormat") == "hr12":
           logging.info("Time format is already set by 12 Hour Format. So changed into 24Hr format")
           cdm.patch(configuration_endpoint, { "timeFormat": "hr24"})

        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname=MenuAppWorkflowObjectIds.dateTime_scrollbar)
        ##Assert Time Zone Screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        TimeFormat = spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time_TimeFormat)
        TimeFormat.mouse_click()
        hr12Format = spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time_Time12hrFormat)
        hr12Format.mouse_click()
        screenValue = spice.wait_for("#SettingsComboBox #timePeriod SpiceText[visible=true]")["text"]
        print("screenvalue at 12hrformat = ",screenValue)
        assert screenValue == "Time Period"
        logging.info("At Time Settings Screen")

    def goto_menu_settings_general_energy(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("At Energy Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_energy_inactivity_shutdown(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("At Energy Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_energy_scheduleOnOff(self, spice):
        self.goto_menu_settings_general_energy(spice)
        logging.info("At schedule Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_energy_scheduleOnOff_screen(self, spice):
        try:
            self.goto_menu_settings_general_energy_scheduleOnOff(spice)
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOnOff,scrollbar_objectname = MenuAppWorkflowObjectIds.view_energySettings+"ScrollBar")
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen)
            logging.info("At schedule On Off screen Settings Screen")
            time.sleep(1)
        except Exception as e:
            logging.info(f"Failed to navigate to schedule On Off screen: {e}")
    
    def is_schedule_not_available_screen_visible(self, spice,timeout=9.0):
        '''
        Purpose: check schedule not available screen display or not.
        If schedule on/off already set before, will check the time interval between schedule on and schedule off when toggle enable shchedule on/off.
        If the time interval is less than one hour, schedule not available screen display, otherwise schedule not available screen will not display.
        Only click ok button on schedule not available screen can we set schedule days and hours.
        '''
        try:
            schedule_not_available_view = spice.wait_for(MenuAppWorkflowObjectIds.title_text_schedule_on_off_error, timeout=timeout)
            spice.wait_until(lambda:schedule_not_available_view["visible"]==True)
            return True
        except Exception as err:
            return False
    
    def is_schedule_day_hours_screen_visible(self, spice,timeout=9.0):
        '''
        Purpose: check schedule day hours screen display or not.
        If schedule not available screen display when toggle schedule on/off enable, click ok button can goto schedule day and hours screen directly.
        If schedule not available screen not display when toggle schedule on/off enable, screen still stay on schedule on/off screen, need to click corresponding menu goto schedule day and hours screen.
        '''
        try:
            schedule_day_hours_view = spice.wait_for(MenuAppWorkflowObjectIds.view_schedule_day_hours, timeout=timeout)
            spice.wait_until(lambda:schedule_day_hours_view["visible"]==True)
            return True
        except Exception as err:
            return False

    def click_schedule_on_toggle_button(self, spice, select=True):
        '''
        click schedule on toggle button to enable or disable schedule on
        select: True->enable /False ->disable
        '''
        toggle_schedule_on = spice.wait_for(f'{MenuAppWorkflowObjectIds.toggle_button} {MenuAppWorkflowObjectIds.schedule_on_locator}')
        is_enable_schedule_on = toggle_schedule_on['checked']
        if (not is_enable_schedule_on) & (select==True):
            spice.validate_button(toggle_schedule_on)
            toggle_schedule_on.mouse_click()
            time.sleep(2)
            if self.is_schedule_not_available_screen_visible(spice, timeout=3):
                self.click_ok_btn_on_schedule_on_off_not_available_alert_screen(spice)
            else:
                is_enable_schedule_on = toggle_schedule_on['checked']
                assert is_enable_schedule_on==True, "Failed to enable schedule on"

        elif is_enable_schedule_on & (select==True):
            logging.info("Schedule On has been enabled")
        
        elif (not is_enable_schedule_on) & (select==False):
            logging.info("Schedule On no need to be selected")

        elif is_enable_schedule_on & (select==False):
            spice.validate_button(toggle_schedule_on)
            toggle_schedule_on.mouse_click()
            time.sleep(2)
            is_enable_schedule_on = toggle_schedule_on['checked']
            assert is_enable_schedule_on==False, "Failed to disable Schedule On"
        else:
            raise Exception("Invalid senario")

    def click_schedule_off_toggle_button(self, spice, select=True):
        '''
        click schedule off toggle button to enable or disable schedule off
        select: True->enable /False ->disable
        '''
        toggle_schedule_off = spice.wait_for(f'{MenuAppWorkflowObjectIds.schedule_off_locator}')
        is_enable_schedule_off = toggle_schedule_off['checked']
        if (not is_enable_schedule_off) & (select==True):
            spice.validate_button(toggle_schedule_off)
            toggle_schedule_off.mouse_click()
            time.sleep(2)
            if self.is_schedule_not_available_screen_visible(spice, timeout=3):
                self.click_ok_btn_on_schedule_on_off_not_available_alert_screen(spice)
            else:
                is_enable_schedule_off = toggle_schedule_off['checked']
                assert is_enable_schedule_off==True, "Failed to enable Schedule Off"

        elif is_enable_schedule_off & (select==True):
            logging.info("Schedule Off has been enabled")
        
        elif (not is_enable_schedule_off) & (select==False):
            logging.info("Schedule Off no need to be selected")

        elif is_enable_schedule_off & (select==False):
            spice.validate_button(toggle_schedule_off)
            toggle_schedule_off.mouse_click()
            time.sleep(2)
            is_enable_schedule_off = toggle_schedule_off['checked']
            assert is_enable_schedule_off==False, "Failed to disable Schedule Off"
        else:
            raise Exception("Invalid senario")

    def goto_schedule_on_or_off_screen(self, spice, schedule_option):
        '''
        From Schedule Printer On/Off screen to Schedule On screen or Schedule Off screen
        schedule_option: schedule on / schedule off
        '''
        logging.info("Check the current state of schedule on or off")
        if schedule_option == "schedule on":
            try:
                self.click_schedule_on_toggle_button(spice, select=True)
                logging.info("Need to click date/time to set date or time")
                if not self.is_schedule_day_hours_screen_visible(spice, timeout=3):
                    self.goto_menu_general_energy_schedule_on_screen_has_set_before(spice)
            except:
                logging.info("The schedule on has not set before, please click Not Set button to set schedule on time/date")
                self.goto_menu_general_energy_schedule_on_screen_not_set_before(spice)
        elif schedule_option == "schedule off":
            try:
                self.click_schedule_off_toggle_button(spice, select=True)
                logging.info("Need to click date/time to set date or time")
                if not self.is_schedule_day_hours_screen_visible(spice, timeout=3):
                    self.goto_menu_general_energy_schedule_off_screen_has_set_before(spice)
            except:
                logging.info("The schedule off has not set before, please click Not Set button to set schedule off time/date")
                self.goto_menu_general_energy_schedule_off_screen_not_set_before(spice)
        else:
            raise Exception(f"Invalid schedule operation value <{schedule_option}>")

    def change_units(self, spice, units):
        '''
        Navigates to the general settings menu and changes the units based on the provided radio button model
        units: Identifier of the radio button to select
        '''
        spice.homeMenuUI().goto_menu_settings_general(spice)
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.50, "#generalSettingsMenuList" + "ScrollBar")
        
        spice.wait_for(MenuAppWorkflowObjectIds.units_menu_combo_box).mouse_click()
        
        spice.wait_for(units).mouse_click()
    
    def set_schedule_on_off_date_time(self, spice, days, schedule_mins):
        '''
        Set date and time on Schedule On screen or Schedule Off screen
        days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        schedule_mins: need to set time
        '''
        logging.info("Set schedule on/off date")
        self.select_days_on_schedule_onoff(spice)
        self.set_energy_schedule_onoff_days(spice, days)
        self.click_next_button_schedule_onoff(spice)

        logging.info("Set schedule on/off time")
        logging.info("Get current time")
        response = spice.cdm.get(spice.cdm.CLOCK_CONFIGURATION)
        system_time = datetime.strptime(response["systemTime"], '%Y-%m-%dT%H:%M:%SZ')
        logging.info(f"The current time is {system_time}")

        schedule_time = (system_time + timedelta(minutes=schedule_mins)).replace(second=0)
        logging.info(f"The schedule time is {schedule_time}")
        min_value = schedule_time.__getattribute__('minute')
        hr_value = schedule_time.__getattribute__('hour')
        self.schedule_onoff_min_set(spice, min_value)
        self.schedule_onoff_hr_set(spice, hr_value)

        time.sleep(2)
        self.click_done_button_schedule_onoff(spice)
        self.click_save_button_schedule_onoff(spice)
    
    def goto_menu_general_energy_schedule_on_screen_not_set_before(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off(Not set before) ->Schedule On
        '''
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOnscreen)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnScreen), "Not schedule on view"

    def goto_menu_general_energy_schedule_off_screen_not_set_before(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off(Not set before) ->Schedule Off
        '''
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen), "Not schedule off view"
 
    def goto_menu_general_energy_schedule_on_screen_has_set_before(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off(has set before) ->Schedule On
        '''
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleON_secondview)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnScreen), "Not schedule on view"

    def goto_menu_general_energy_schedule_off_screen_has_set_before(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off(has set before) ->Schedule Off
        '''
        scroll_bar_id = f'{MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffListScreen} {MenuAppWorkflowObjectIds.schedule_on_off_list_view} {MenuAppWorkflowObjectIds.scroll_bar_schedule_on_off_view}'
        scroll_bar_item = spice.query_item(scroll_bar_id)
        if scroll_bar_item['visible'] == True:
            self.workflow_common_operations.scroll_to_position_vertical(0.2, scroll_bar_id)
        else:
            logging.info("No need to scroll bar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_secondview)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen), "Not schedule off view"
    
    def select_days_on_schedule_onoff(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off ->Days
        '''
        days_options = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView)
        days_options.mouse_click()
        time.sleep(1)
        logging.info("At Schedule On/Off day list Screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOndaysview), "Not in Days View"

    def select_hours_on_schedule_onoff(self, spice):
        '''
        Negative to Menu->General->Energy->Schedule printer on/off ->Hours
        '''
        hours_options = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleON_scheduleHoursView)
        hours_options.mouse_click()
        time.sleep(1)
        logging.info("At Schedule On/Off hour list Screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnHoursView), "Not in Hours View"
    
    def set_energy_schedule_onoff_days(self, spice, days):
        '''
        Set days in energy schedule on/off
        days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        '''
        all_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        unselect_days = list(set(all_days) - set(days))

        scroll_bar_id = f'{MenuAppWorkflowObjectIds.view_energySettings_scheduleOndaysview} {MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffListScreen} {MenuAppWorkflowObjectIds.scroll_bar_schedule_on_off_view}'
        scroll_bar_item = spice.query_item(scroll_bar_id)
        spice.wait_until(lambda: scroll_bar_item['visible'] == True)

        logging.info("Start select the need select days")
        for day in days:
            if day == 'Sunday':
                self.workflow_common_operations.scroll_to_position_vertical(0.0, scroll_bar_id)
                self.click_sunday_on_energy_schedule_onoff(spice, select=True)
            
            elif day == 'Monday':
                self.workflow_common_operations.scroll_to_position_vertical(0.0, scroll_bar_id)
                self.click_monday_on_energy_schedule_onoff(spice, select=True)

            elif day == 'Tuesday':
                self.workflow_common_operations.scroll_to_position_vertical(0.3, scroll_bar_id)
                self.click_tuesday_on_energy_schedule_onoff(spice, select=True)

            elif day == 'Wednesday':
                self.workflow_common_operations.scroll_to_position_vertical(0.3, scroll_bar_id)
                self.click_wednesday_on_energy_schedule_onoff(spice, select=True)

            elif day == 'Thursday':
                self.workflow_common_operations.scroll_to_position_vertical(0.5, scroll_bar_id)
                self.click_thursday_on_energy_schedule_onoff(spice, select=True)

            elif day == 'Friday':
                self.workflow_common_operations.scroll_to_position_vertical(0.6, scroll_bar_id)
                self.click_friday_on_energy_schedule_onoff(spice, select=True)

            elif day == 'Saturday':
                self.workflow_common_operations.scroll_to_position_vertical(0.7, scroll_bar_id)
                self.click_saturday_on_energy_schedule_onoff(spice, select=True)
            else:
                raise Exception(f"Invalid day <{day}>")

        if unselect_days!=[]:
            logging.info("Need to unselect the days which is not set")
            self.unselect_energy_schedule_onoff_days(spice, days=unselect_days)

    def click_sunday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Sunday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        sunday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{sunday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            sunday_option = spice.wait_for(sunday_id)
            sunday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{sunday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Sunday"
        elif is_check_box_enable & (select==True):
            logging.info("Sunday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Sunday no need to be selected")

        elif is_check_box_enable & (select==False):
            sunday_option = spice.wait_for(sunday_id)
            sunday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{sunday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Sunday"
        else:
            raise Exception("Invalid senario")

    def click_monday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Monday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        monday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Monday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{monday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            monday_option = spice.wait_for(monday_id)
            monday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{monday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Monday"
        elif is_check_box_enable & (select==True):
            logging.info("Monday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Monday no need to be selected")

        elif is_check_box_enable & (select==False):
            monday_option = spice.wait_for(monday_id)
            monday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{monday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Monday"
        else:
            raise Exception("Invalid senario")

    def click_tuesday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Tuesday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        tuesday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Tuesday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{tuesday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            tuesday_option = spice.wait_for(tuesday_id)
            tuesday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{tuesday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Tuesday"
        elif is_check_box_enable & (select==True):
            logging.info("Tuesday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Tuesday no need to be selected")

        elif is_check_box_enable & (select==False):
            tuesday_option = spice.wait_for(tuesday_id)
            tuesday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{tuesday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Tuesday"
        else:
            raise Exception("Invalid senario")

    def click_wednesday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Wednesday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        wednesday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Wednesday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{wednesday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            wendesday_option = spice.wait_for(wednesday_id)
            wendesday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{wednesday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Wednesday"
        elif is_check_box_enable & (select==True):
            logging.info("Wednesday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Wednesday no need to be selected")

        elif is_check_box_enable & (select==False):
            wendesday_option = spice.wait_for(wednesday_id)
            wendesday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{wednesday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Wednesday"
        else:
            raise Exception("Invalid senario")
    
    def click_thursday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Thursday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        thursday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Thursday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{thursday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            thursday_option = spice.wait_for(thursday_id)
            thursday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{thursday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Thursday"
        elif is_check_box_enable & (select==True):
            logging.info("Thursday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Thursday no need to be selected")

        elif is_check_box_enable & (select==False):
            thursday_option = spice.wait_for(thursday_id)
            thursday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{thursday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Thursday"
        else:
            raise Exception("Invalid senario")

    def click_friday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Friday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        friday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Friday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{friday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            friday_option = spice.wait_for(friday_id)
            friday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{friday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Friday"
        elif is_check_box_enable & (select==True):
            logging.info("Friday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Friday no need to be selected")

        elif is_check_box_enable & (select==False):
            friday_option = spice.wait_for(friday_id)
            friday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{friday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Friday"
        else:
            raise Exception("Invalid senario")

    def click_saturday_on_energy_schedule_onoff(self, spice, select=True):
        '''
        click Saturday on schedule On/Off screen
        select: True->Need select False->No need select
        '''
        saturday_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Saturday
        checkbox_id = MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_checkboxView
        is_check_box_enable = spice.wait_for(f'{saturday_id} {checkbox_id}').__getitem__('checked')
        if (not is_check_box_enable) & (select==True):
            saturday_option = spice.wait_for(saturday_id)
            saturday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{saturday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==True, "Failed to unselect Saturday"
        elif is_check_box_enable & (select==True):
            logging.info("Saturday has been selected")
        
        elif (not is_check_box_enable) & (select==False):
            logging.info("Saturday no need to be selected")

        elif is_check_box_enable & (select==False):
            saturday_option = spice.wait_for(saturday_id)
            saturday_option.mouse_click()
            time.sleep(2)
            is_check_box_enable = spice.wait_for(f'{saturday_id} {checkbox_id}').__getitem__('checked')
            assert is_check_box_enable==False, "Failed to unselect Saturday"
        else:
            raise Exception("Invalid senario")
    
    def unselect_energy_schedule_onoff_days(self, spice, days):
        '''
        To unselect days for schedule on/off
        days: The days no need to select
        '''
        scroll_bar_id = f'{MenuAppWorkflowObjectIds.view_energySettings_scheduleOndaysview} {MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffListScreen} {MenuAppWorkflowObjectIds.scroll_bar_schedule_on_off_view}'
        scroll_bar_item = spice.query_item(scroll_bar_id)
        spice.wait_until(lambda: scroll_bar_item['visible'] == True)
        for day in days:
            if day == 'Sunday':
                self.workflow_common_operations.scroll_to_position_vertical(0.0, scroll_bar_id)
                self.click_sunday_on_energy_schedule_onoff(spice, select=False)
            
            elif day == 'Monday':
                self.workflow_common_operations.scroll_to_position_vertical(0.0, scroll_bar_id)
                self.click_monday_on_energy_schedule_onoff(spice, select=False)

            elif day == 'Tuesday':
                self.workflow_common_operations.scroll_to_position_vertical(0.3, scroll_bar_id)
                self.click_tuesday_on_energy_schedule_onoff(spice, select=False)

            elif day == 'Wednesday':
                self.workflow_common_operations.scroll_to_position_vertical(0.3, scroll_bar_id)
                self.click_wednesday_on_energy_schedule_onoff(spice, select=False)

            elif day == 'Thursday':
                self.workflow_common_operations.scroll_to_position_vertical(0.5, scroll_bar_id)
                self.click_thursday_on_energy_schedule_onoff(spice, select=False)

            elif day == 'Friday':
                self.workflow_common_operations.scroll_to_position_vertical(0.6, scroll_bar_id)
                self.click_friday_on_energy_schedule_onoff(spice, select=False)

            elif day == 'Saturday':
                self.workflow_common_operations.scroll_to_position_vertical(0.7, scroll_bar_id)
                self.click_saturday_on_energy_schedule_onoff(spice, select=False)
            else:
                raise Exception(f"Invalid day <{day}>")
    
    def click_next_button_schedule_onoff(self, spice):
        '''
        Click Next Button at schedule on/off 
        '''
        next_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_nextButton)
        spice.validate_button(next_button)
        next_button.mouse_click()
        time.sleep(5)
        
    def click_done_button_schedule_onoff(self, spice):
        '''
        Click Done Button at schedule on/off 
        '''
        done_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_doneButton)
        spice.validate_button(done_button)
        done_button.mouse_click()
        time.sleep(2)
    
    def click_save_button_schedule_onoff(self, spice):
        '''
        Click Save Button at schedule on/off 
        '''
        save_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_saveButton)
        spice.validate_button(save_button)
        save_button.mouse_click()
        time.sleep(2)
    
    def schedule_onoff_min_set(self, spice, value):
        """
        Purpose: Set minute for schedule on/off
        Ui Flow: Energy -> schedule on/off
        :return: None
        """
        min_set = spice.wait_for(MenuAppWorkflowObjectIds.minute_set_input)
        min_set.__setitem__('value', value)

    def schedule_onoff_hr_set(self, spice, value):
        """
        Purpose: Set hour for schedule on/off
        Ui Flow: Energy -> schedule on/off
        :return: None
        """
        min_set = spice.wait_for(MenuAppWorkflowObjectIds.hour_set_input)
        min_set.__setitem__('value', value)

    def check_schedule_on_off_not_available_alert_screen(self, spice, net):
        '''
        check title and alert text schedule on off not available alert screen
        '''
        spice.wait_for(MenuAppWorkflowObjectIds.view_schedule_on_off_error, 10)

        title_text =  spice.wait_for(MenuAppWorkflowObjectIds.title_text_schedule_on_off_error)["text"]
        expect_title_text = LocalizationHelper.get_string_translation(net,"cScheduleNotAvailable")
        assert title_text == expect_title_text, f"Failed to check title text, actual text is {title_text}, expect text is {expect_title_text}"

        alert_text =  spice.wait_for(MenuAppWorkflowObjectIds.alert_text_schedule_on_off_error)["text"]
        expect_alert_text = LocalizationHelper.get_string_translation(net,"cTimePrinterOff")
        assert alert_text == expect_alert_text, f"Failed to check alert text, actual text is {alert_text}, expect text is {expect_alert_text}"
    
    def click_ok_btn_on_schedule_on_off_not_available_alert_screen(self, spice):
        '''
        click ok button on schedule on off not available alert screen
        '''
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.ok_btn_schedule_on_off_error)
        spice.validate_button(ok_button)
        ok_button.mouse_click()
        time.sleep(2)

    def goto_menu_settings_general_energy_scheduleTurnOnscreen(self, spice):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOn_2infoBlockRow #contentItem")["text"]
            # Check if the schedule_set_not is found or not
            if schedule_set_not == "Not Set":
                self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOnscreen)
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnScreen)
                cancelButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_cancelButton)
                cancelButton.mouse_click()
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen)
                logging.info("At schedule On Screen")
                time.sleep(1)
            else:
                print("Schedule is already set so going to home screen ")
                spice.goto_homescreen()

        except Exception as e:
            logging.info(f"An error occurred: {e}")
            spice.goto_homescreen()
            
    def goto_menu_settings_general_energy_scheduleTurnOffscreen(self, spice):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOff_2infoBlockRow #contentItem")["text"]
            # **This code runs only if the schedule was found**
            if schedule_set_not == "Not Set":
                self.menu_navigation(spice,MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen,MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen)
                cancelButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_cancelButton)
                cancelButton.mouse_click()
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen)
                logging.info("At schedule On Screen")
                time.sleep(1)
            else:
                print("Schedule is already set, going to home screen.")
                spice.goto_homescreen()

        except Exception as e:
            logging.info(f"An error occurred: {e}")
            spice.goto_homescreen()

    def test_views_spice_menu_settings_General_Energy_ScheduleON_DaysHours_Sch(self, spice):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOn_2infoBlockRow #contentItem")["text"]
            # Check if the schedule_set_not is found or not
            if schedule_set_not == "Not Set":
                print("Set a new schedule ")
                self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOnscreen)
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnScreen)

                DaysOption = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleON_scheduleDaysView)
                DaysOption.mouse_click()
                logging.info("At Schedule On/Off day list Screen")
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOndaysview), "Not in Days View"
                Sunday = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday)
                Sunday.mouse_click()
                self.click_next_button_schedule_onoff(spice)
                self.click_done_button_schedule_onoff(spice)
                self.click_save_button_schedule_onoff(spice)
                logging.info("At schedule turn On day list Screen")
                time.sleep(1)
            else:
                print("Schedule is already set so going to home screen ")
                spice.goto_homescreen()
        except Exception as e:
            print(f"An error occurred: {e}")
            spice.goto_homescreen()

    def test_views_spice_menu_settings_General_Energy_ScheduleON_DaysHourssettingview(self, spice):
        self.test_views_spice_menu_settings_General_Energy_ScheduleON_DaysHours_Sch(spice)
        logging.info("At schedule turn On hours list Screen")
        time.sleep(1)

    def test_views_spice_menu_settings_General_Energy_ScheduleOFF_DaysHours_Sch(self, spice):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOff_2infoBlockRow #contentItem")["text"]
            
            # Check if the schedule_set_not is found or not
            if schedule_set_not == "Not Set":
                print("Set a new schedule")
                
                self.menu_navigation(spice, 
                                    MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, 
                                    MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
                
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen)

                DaysOption = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleON_scheduleDaysView)
                DaysOption.mouse_click()
                logging.info("At Schedule On/Off day list Screen")
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOndaysview), "Not in Days View"
                
                Sunday = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday)
                Sunday.mouse_click()
                
                self.click_next_button_schedule_onoff(spice)
                spice.wait_for("#Hour #upBtn").mouse_click()
                spice.wait_for("#Hour #upBtn").mouse_click()
                spice.wait_for("#Hour #upBtn").mouse_click()
                self.click_done_button_schedule_onoff(spice)
                self.click_save_button_schedule_onoff(spice)
                
                logging.info("At schedule turn Off day list Screen")
                time.sleep(1)
            else:
                print("Schedule is already set, going to home screen")
                spice.goto_homescreen()
        
        except Exception as e:
            print(f"An error occurred: {e}")
            spice.goto_homescreen()

    def test_views_spice_menu_settings_General_Energy_ScheduleOFF_DaysHourssettingview(self, spice):
        self.test_views_spice_menu_settings_General_Energy_ScheduleOFF_DaysHours_Sch(spice)
        logging.info("At schedule turn On hours list Screen")
        time.sleep(1)
        
    def energy_scheduleOnOff_screen_view(self, spice):
        self. goto_menu_settings_general_energy_scheduleOnOff(spice)
        
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOnOff,scrollbar_objectname = MenuAppWorkflowObjectIds.view_energySettings+"ScrollBar")
        logging.info("At schedule On/Off screen Settings Screen")
    
    def energy_scheduleOnOff_enterprise_ScheduleOn_screen(self , spice):
        self.energy_scheduleOnOff_screen_view(spice)
        try:
            schedule_set_not = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_On_secondtext)
            schedule_set_not_text = schedule_set_not["text"]
            # Check if the schedule_set_not is found or not
            if schedule_set_not_text == "Not Set":
                print("check the screen for scheduleOn ")
                click_scheduleOn = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_On_secondtext_onclick)
                click_scheduleOn.mouse_click()
                title_text = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_title_text)["text"]
                title_text = title_text.split("(")[0].strip()
                print("title_text = ", title_text)
                assert title_text == "Set Time", f"Failed to check title text, actual text is {title_text}, expect text is Schedule On"
            else:
                print("Schedule is already present so csnnot see the setting screen ")
        except: 
            # Handle any exceptions that occur during the wait or click
            print("An error occurred: ")
            
    def energy_scheduleOnOff_enterprise_ScheduleOff_screen(self , spice):
        self.energy_scheduleOnOff_screen_view(spice)
        try:
            schedule_set_not = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_Off_secondtext)["text"]
            # Check if the schedule_set_not is found or not
            if schedule_set_not == "Not Set":
                print("check the screen for scheduleOff")
                click_scheduleOff = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_Off_secondtext_onclick)
                click_scheduleOff.mouse_click()
                title_text = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_title_text)["text"]
                title_text = title_text.split("(")[0].strip()
                print("title_text = ", title_text)
                assert title_text == "Set Time", f"Failed to check title text, actual text is {title_text}, expect text is Schedule Off"
            else:
                print("Schedule is already present so going to home screen ")
        except: 
            # Handle any exceptions that occur during the wait or click
            print("An error occurred: ")
            
    def energy_scheduleOnOff_enterprise_set_scheduleOn(self,spice):
        self.energy_scheduleOnOff_enterprise_ScheduleOn_screen(spice)
        try:
            save_button = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_save_button, timeout = 20) #days and time is saved in the save button
            save_button.mouse_click()
        except TimeoutError as e:
            raise TimeoutError(f"Failed to find the save button: {e}")
            

    def energy_scheduleOnOff_enterprise_set_scheduleOff(self,spice):
        self.energy_scheduleOnOff_enterprise_ScheduleOff_screen(spice)
        try:
            save_button = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_save_button, timeout = 20) #days and time is saved in the save button
            save_button.mouse_click()
        except TimeoutError as e:
            raise TimeoutError(f"Failed to find the save button: {e}")
        
    def energy_scheduleOnOff_enterprise_deleteScheduleOn(self,spice,cdm):
        self.energy_scheduleOnOff_screen_view(spice)
        try:
            schedule_available = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_On_secondtext)["text"]
            print("schedule_available = ", schedule_available)
            if(schedule_available == "Not Set"):
                click_scheduleOn = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_On_secondtext_onclick)
                click_scheduleOn.mouse_click()
                
                save_button = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_save_button) #days and time is saved in the save button
                save_button.mouse_click()
                
                availableschedule = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_ScheduleOn_settings_second_row)
                availableschedule.mouse_click()
                time.sleep(3)
                configuration_endpoint = CdmEndpoints.POWER_CONFIG
                spice.goto_homescreen()
                delete_url = f"{configuration_endpoint}/powerOnSchedule/0"
                print(f"[DELETE] Calling: {delete_url}")
                cdm.delete(delete_url)
            else:
                logging.info("No schedule available")
        finally:
            logging.info("Not deleteing the schedule")
       
    def energy_scheduleOnOff_enterprise_deleteScheduleOff(self,spice,cdm):
        self.energy_scheduleOnOff_screen_view(spice)
        try:
            schedule_available = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_Off_secondtext)["text"]
            print("schedule_available = ", schedule_available)
            if(schedule_available == "Not Set"):
                click_scheduleOn = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_Off_secondtext_onclick)
                click_scheduleOn.mouse_click()
                save_button = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_save_button, timeout = 20) #days and time is saved in the save button
                save_button.mouse_click()
                availableschedule = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_ScheduleOff_settings_second_row)
                availableschedule.mouse_click()
                time.sleep(3)
                configuration_endpoint = CdmEndpoints.POWER_CONFIG
                spice.goto_homescreen()
                delete_url = f"{configuration_endpoint}/powerOffSchedule/0"
                print(f"[DELETE] Calling: {delete_url}")
                cdm.delete(delete_url)
                logging.info("Schedule deleted")
            else:
                logging.info("No schedule available")
        except TimeoutError as e:
                raise TimeoutError(f"Failed to find the save button: {e}")
        finally:
            logging.info("Not deleting the schedule")

    def energy_scheduleOnOff_set_scheduleOff(self,spice):
        self.energy_scheduleOnOff_screen_view(spice)
        
        click_scheduleOff = spice.wait_for("#multipleScheduleOffTextImageBranch_2infoBlockRow")
        click_scheduleOff.mouse_click()
        time.sleep(1)
        
        hour_spinbox = spice.wait_for("#schOnOffViewSettings #rowlayoutdays #hourSpinBox #SpinBoxTextFieldMouseArea", timeout=5)
        assert hour_spinbox, "Hour spinbox not found."
        hour_spinbox.mouse_click()
        # assert spice.wait_for("#spiceKeyboardView")
        # logging.info("At spinbox keyboard")
        
        # Verify keyboard appears
        assert spice.wait_for("#spiceKeyboardView", timeout=5), "Keyboard did not appear."
        logging.info("At spinbox keyboard.")
        
        spice.query_item("#key2PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
        
        save_button = spice.wait_for("#saveButton")
        save_button.mouse_click()

        ok_button = spice.wait_for("#okButton")
        ok_button.mouse_click()
    
    def energy_scheduleOnOff_set_scheduleOff_newinstance(self,spice):
        self.energy_scheduleOnOff_screen_view(spice)
        click_scheduleOff = spice.wait_for("#multipleScheduleOffTextImageBranch_2infoBlockRow")
        click_scheduleOff.mouse_click()
                
        availableschedule = spice.wait_for("#multipleSch1_firstinfoBlockRow")
        availableschedule.mouse_click()
        time.sleep(2)
        
        spice.query_item("#mainPanel #schOnOffViewUpdate #hourSpinBox #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At spinbox keyboard")
        spice.query_item("#key2PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
        
        save_button = spice.wait_for("#saveButton")
        save_button.mouse_click()

        ok_button = spice.wait_for("#okButton")
        ok_button.mouse_click()
        logging.info("Schedule set but there is a conflict")
    
    def energy_scheduleOnOff_enterprise_multipleScheduleOff(self, spice):
        self.energy_scheduleOnOff_screen_view(spice)
        try:
            schedule_set_not = spice.wait_for(MenuAppWorkflowObjectIds.view_energy_scheduleOnOff_screen_Schedule_On_secondtext)["text"]
            # Check if the schedule_set_not is found or not
            if (schedule_set_not == "Not Set"):
                print("check the screen for scheduleOn there is no schedule set through Cdm patch")
                return False
            else:
                print("Schedule is set")
                return True
        except: 
            # Handle any exceptions that occur during the wait or click
            print("An error occurred: ")
            return

    def goto_menu_settings_general_energy_sleep(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_sleep, scrollbar_objectname = MenuAppWorkflowObjectIds.view_energySettings+"ScrollBar")

        try:
            (spice.query_item(MenuAppWorkflowObjectIds.view_energySettings_sleep)["visible"])
        except Exception as e:
            logging.info("Navigate to sleep view")
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_sleep).mouse_click()
        else:
            logging.info("At expected Menu")
        finally:
            ##Assert Energy sleep Screen
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_sleep)
            logging.info("At Energy Sleep Settings Screen")
            time.sleep(1)

    def get_general_energy_sleep_value_from_ui(self, spice):
        """
        Method to get general energy sleep value from ui
        return sleep_value_list: energy sleep value list, such as ["5 Minutes", "10 Minutes"]
        """
        sleep_value_list = []
        for i in range(0, 15):
            try:
                radio_button = spice.query_item(MenuAppWorkflowObjectIds.radio_button_locator_energy_sleep, i)
                current_radio_button_text = radio_button["text"]
                sleep_value_list.append(current_radio_button_text)
            except:
                logging.info(f"Cannot find energy sleep value RadioButton {i}")
                break
        logging.info(f"Get energy sleep value list from ui is: {sleep_value_list}")
        return sleep_value_list

    def goto_menu_settings_general_energy_shutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.1, "#energySettingsMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_shutdown)

        try:
            (spice.query_item(MenuAppWorkflowObjectIds.view_energySettings_shutdown)["visible"])
        except Exception as e:
            logging.info("Navigate to shutdown view")
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_shutdown).mouse_click()
        else:
            logging.info("At expected Menu")
        finally:
            ##Assert Energy shutdown Screen
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_shutdown)
            logging.info("At Energy Shutdown Settings Screen")
            time.sleep(1)

    def goto_menu_settings_general_energy_autoshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        isVisible = self.workflow_common_operations.validateListObjectVisibility(MenuAppWorkflowObjectIds.view_energySettings,  MenuAppWorkflowObjectIds.menu_button_settings_general_energy_autoshutdown, "", 1)
        if(isVisible == False):
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_autoshutdown, scrollbar_objectname = MenuAppWorkflowObjectIds.view_energySettings+"ScrollBar")

    def goto_menu_settings_general_energy_shutdown_already_signin(self, spice):
        '''
        UI flow: Menu > Settings > General > Energy > Inactivity Shutdown(Already sign in from sign app)
        '''
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_shutdown, scrollbar_objectname = MenuAppWorkflowObjectIds.view_energySettings+"ScrollBar")
        ##Assert Energy shutdown Screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_shutdown)
        logging.info("At Energy Shutdown Settings Screen")
        time.sleep(1)

    # Menu Settings General Energy voltage frequency
    def goto_menu_settings_general_energy_voltageFrequency(self, spice):

        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1, "#energySettingsMenuListScrollBar")
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_voltageFrequency)
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.view_energySettings_voltageFrequency)["visible"])
        except Exception as e:
            logging.info("Navigate to voltage frequency view")
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_voltageFrequency).mouse_click()
        else:
            logging.info("At expected Menu")
        finally:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_voltageFrequency)
            logging.info("At Energy Voltage Frequency Settings Screen")
            time.sleep(1)

    def set_energyVoltageFrequency_50Hz(self, spice):
        self.goto_menu_settings_general_energy_voltageFrequency(spice)
        freq50Hz = spice.wait_for(MenuAppWorkflowObjectIds.energy_voltage_frequency_50Hz)
        freq50Hz.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set frequency to 50Hz")
        time.sleep(1)

    def set_energyVoltageFrequency_60Hz(self, spice):
        self.goto_menu_settings_general_energy_voltageFrequency(spice)
        freq60Hz = spice.wait_for(MenuAppWorkflowObjectIds.energy_voltage_frequency_60Hz)
        freq60Hz.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set frequency to 60Hz")
        time.sleep(1)

    # End Menu Settings General Energy voltage frequency

    # Menu Settings General Energy prevent Shutdown
    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        assert spice.wait_for("#energycheckbox #CheckBoxView")
        return spice.query_item("#energycheckbox #CheckBoxView")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.3, "#energySettingsMenuListScrollBar")
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown, scrollbar_objectname = "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        # Checking for signin screen
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except Exception as e:
            logging.info("At Expected Menu")
        else:
            #SignIn Screen
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("At Expected Menu")
        logging.info("Set Energy prevent Shutdown to none(do not disable)")
        time.sleep(1)

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.3, "#energySettingsMenuListScrollBar")
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown, scrollbar_objectname = "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        # Checking for signin screen
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except Exception as e:
            logging.info("At Expected Menu")
        else:
            #SignIn Screen
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("At Expected Menu")
        logging.info("Set Energy prevent Shutdown to when ports are active")
        time.sleep(1)
    # Menu Settings General Energy Shutdown

    def set_energyshutdown_20Minutes(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.workflow_common_operations.scroll_to_position_vertical(.0001, "#comboBoxScrollBar")
            twentyminsButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_shutdown_20minutes)
            twentyminsButton.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            logging.info("Set Energy Shutdown to 20minutes")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 20minutes: ")
            spice.goto_home_screen()

    def set_energyshutdown_onehour(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.workflow_common_operations.scroll_to_position_vertical(0, "#comboBoxScrollBar")
            oneHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_shutdown_1hour)
            oneHourButton.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            logging.info("Set Energy Shutdown to 1 hour")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 1 hour: ")
            spice.goto_home_screen()
            
    def set_energyshutdown_twohours(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            twoHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_shutdown_2hours)
            twoHourButton.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            logging.info("Set Energy Shutdown to 2 hours")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 1 hour: ")
            spice.goto_home_screen()

    def set_energyshutdown_fourhours(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            fourHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_shutdown_4hours)
            fourHourButton.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            logging.info("Set Energy Shutdown to 4 hours")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 4 hours: ")
            spice.goto_home_screen()

    # Menu Settings General Energy Sleep

    def set_energysleep_oneminute(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0, "#comboBoxScrollBar")
        oneMinuteButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_1min)
        oneMinuteButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 1 Minute")
        time.sleep(1)

    def set_energysleep_fiveminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0, "#comboBoxScrollBar")
        fiveMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_5mins)
        fiveMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 5 minutes")
        time.sleep(1)

    def set_energysleep_tenminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0, "#comboBoxScrollBar")
        tenMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_10mins)
        tenMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 10 minutes")
        time.sleep(1)

    def set_energysleep_fifteenminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)

        self.workflow_common_operations.scroll_to_position_vertical(.1, "#comboBoxScrollBar")
        fifteenMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_15mins)
        fifteenMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 15 minutes")
        time.sleep(1)

    def set_energysleep_thirtyminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        #self.menu_navigation(spice, "#EnergySleepValuelist1", MenuAppWorkflowObjectIds.energy_sleep_30mins, scrollbar_objectname = "#EnergySleepValuelist1ScrollBar")

        self.workflow_common_operations.scroll_to_position_vertical(.2, "#comboBoxScrollBar")
        thirtyMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_30mins)
        thirtyMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 30 minutes")
        time.sleep(1)

    def set_energysleep_onehour(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        #self.menu_navigation(spice, "#EnergySleepValuelist1SpiceListViewView", MenuAppWorkflowObjectIds.energy_sleep_1hour, scrollbar_objectname = "#EnergySleepValuelist1SpiceListViewViewScrollBar")
        self.workflow_common_operations.scroll_to_position_vertical(.3, "#comboBoxScrollBar")
        oneHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_1hour)
        oneHourButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 1 hour")
        time.sleep(1)

    # Menu settings job settings
    def scroll_job_settings_view(self, spice, position:float):
        """
        Helper method to scroll the job settings scroll bar to the indicated position.
        @param spice:
        @param Position: scroll position. Range: [0, 1]
        """
        assert position >= 0.0 and position <= 1.0
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.view_settings_jobs_settings + "ScrollBar")
        scroll_position = (1.0 - scrollbar["visualSize"]) * position
        scrollbar.__setitem__("position", str(scroll_position))
        spice.wait_until(lambda:abs(scrollbar["position"] - scroll_position) <= 0.01)


    def goto_job_recovery_mode_options(self, spice):
        """
        Helper method to display the menu to select the job recovery policy.
        UI Should be in Jobs Settings menu
        @param spice:
        """
        job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        job_recovery_policy_combo_box.mouse_click()
        spice.wait_until(lambda:spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_options_view)["visible"] == True)


    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        """
        Helper method to indicate if the job settings button in settings menu is shown
        UI Should be in Settings menu
        @param spice:
        """
        try:
            item = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings)
            logging.info("Item '%s' found", MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings)
            return item['visible']
        except Exception:
            logging.info("Item '%s' NOT found", MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings)
            return False


    def is_visible_hide_deleted_jobs(self, spice) -> bool:
        """
        Helper method to indicate if hideDeletedJobs is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            hide_deleted_jobs_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
            return hide_deleted_jobs_switch['visible']
        except TimeoutError:
            return False

    def get_hide_deleted_jobs(self, spice) -> bool:
        """
        Helper method to return if hideDeletedJobs is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        hide_deleted_jobs_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        assert hide_deleted_jobs_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        return hide_deleted_jobs_switch["checked"]

    def set_hide_deleted_jobs(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable hideDeletedJobs
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        hide_deleted_jobs_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        assert hide_deleted_jobs_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)

        old_enable = hide_deleted_jobs_switch["checked"]
        if old_enable != enable:
            self.scroll_job_settings_view(spice, 0.0)
            hide_deleted_jobs_switch.mouse_click(x=2, y=2)
            spice.wait_until(lambda:hide_deleted_jobs_switch["checked"] == enable)

        return old_enable


    def is_visible_cancel_jobs_on_hold_delay(self, spice) -> bool:
        """
        Helper method to indicate if cancelJobsOnHoldDelay is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            cancel_jobs_on_hold_spinbox = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
            return cancel_jobs_on_hold_spinbox['visible']
        except TimeoutError:
            return False

    def get_cancel_jobs_on_hold_delay(self, spice) -> int:
        """
        Helper method to return the value of cancelJobsOnHoldDelay
        UI Should be in Jobs Settings menu
        @param spice:
        """
        cancel_jobs_on_hold_spinbox = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        assert cancel_jobs_on_hold_spinbox["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        return cancel_jobs_on_hold_spinbox['value']

    def set_cancel_jobs_on_hold_delay(self, spice, value:int, expected_value:int = None) -> int:
        """
        Helper method to set the new value cancelJobsOnHoldDelay
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        cancel_jobs_on_hold_spinbox = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        assert cancel_jobs_on_hold_spinbox["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)

        old_value = cancel_jobs_on_hold_spinbox['value']
        if old_value != value:
            self.scroll_job_settings_view(spice, 0.25)
            cancel_jobs_on_hold_spinbox.__setitem__("value", value)
            spice.wait_until(lambda:cancel_jobs_on_hold_spinbox["value"] == (value if expected_value is None else expected_value))

        return old_value


    def is_visible_job_queue_recovery_mode(self, spice) -> bool:
        """
        Helper method to indicate if jobQueueRecoveryMode is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
            return job_recovery_policy_combo_box['visible']
        except TimeoutError:
            return False

    def get_job_queue_recovery_mode(self, spice) -> int:
        """
        Helper method to return the current value of jobQueueRecoveryMode
        UI Should be in Jobs Settings menu
        @param spice:
        """
        job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        assert job_recovery_policy_combo_box["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        return job_recovery_policy_combo_box['currentIndex']

    def verify_job_recovery_policy_index(self, spice, index):
        job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        spice.wait_until(lambda:job_recovery_policy_combo_box["currentIndex"] == index)

    def set_job_queue_recovery_mode(self, spice, value:str) -> int:
        """
        Helper method to set the new value to jobQueueRecoveryMode
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        assert job_recovery_policy_combo_box["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)

        self.scroll_job_settings_view(spice, 0.50)
        self.goto_job_recovery_mode_options(spice)

        if value == "putOnHold":
            index = 0
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_put_on_hold)
        elif value == "cancel":
            index = 1
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_cancel)
        else:
            raise Exception(f"Invalid job queue recovery mode <{value}>")

        job_recovery_policy_combo_box_settings = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_settings)
        old_value = job_recovery_policy_combo_box_settings['currentIndex']
        current_button.mouse_click()
        self.verify_job_recovery_policy_index(spice, index)

        return old_value


    def is_visible_job_on_hold_for_manual_release(self, spice) -> bool:
        """
        Helper method to indicate if holdJobForManualRelease is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            jobs_for_manual_release_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
            return jobs_for_manual_release_switch['visible']
        except TimeoutError:
            return False

    def get_job_on_hold_for_manual_release(self, spice) -> bool:
        """
        Helper method to return if holdJobForManualRelease is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        jobs_for_manual_release_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        assert jobs_for_manual_release_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        return jobs_for_manual_release_switch["checked"]

    def set_job_on_hold_for_manual_release(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable holdJobForManualRelease
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        jobs_for_manual_release_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        assert jobs_for_manual_release_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)

        old_enable = jobs_for_manual_release_switch["checked"]
        if old_enable != enable:
            try:
                self.scroll_job_settings_view(spice, 0.75)
            except TimeoutError:
                print("Scrollbar not found")
            finally:
                jobs_for_manual_release_switch.mouse_click(x=2, y=2)
                spice.wait_until(lambda:jobs_for_manual_release_switch["checked"] == enable)

        return old_enable


    def is_visible_reprint_resend_jobs_enabled(self, spice) -> bool:
        """
        Helper method to indicate if reprintResendJobsEnabled control is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            reprint_resend_jobs_enabled_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
            return reprint_resend_jobs_enabled_switch['visible']
        except TimeoutError:
            return False

    def get_reprint_resend_jobs_enabled(self, spice) -> bool:
        """
        Helper method to return if reprintResendJobsEnabled is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        reprint_resend_jobs_enabled_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        assert reprint_resend_jobs_enabled_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        return reprint_resend_jobs_enabled_switch["checked"]

    def set_reprint_resend_jobs_enabled(self, spice, enable:bool, confirm_disabled:bool = False) -> bool:
        """
        Helper method to enable/disable reprintResendJobsEnabled
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        reprint_resend_jobs_enabled_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        assert reprint_resend_jobs_enabled_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)

        old_enable = reprint_resend_jobs_enabled_switch["checked"]
        if old_enable != enable:
            self.scroll_job_settings_view(spice, 1.0)
            reprint_resend_jobs_enabled_switch.mouse_click(x=2, y=2)

            # Answer confirmation dialog if the setting is disabled
            if (enable == False):
                confirmation_dialog = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog)
                spice.wait_until(lambda: confirmation_dialog["visible"] == True, 5)

                button_name = MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog_yes_button \
                    if confirm_disabled else MenuAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog_no_button

                confirmation_dialog = spice.query_item(button_name)
                confirmation_dialog.mouse_click()

                time.sleep(2)

                control_enabled = not confirm_disabled
            else:
                control_enabled = True

            spice.wait_until(lambda:reprint_resend_jobs_enabled_switch["checked"] == control_enabled)

        return old_enable

    def is_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        """
        Helper method to indicate if promoteToInterruptPrintJob control is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
            return promote_to_interrupt_print_jobs_enabled_switch['visible']
        except TimeoutError:
            return False

    def get_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        """
        Helper method to return if promoteToInterruptPrintJob is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
        assert promote_to_interrupt_print_jobs_enabled_switch["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
        return promote_to_interrupt_print_jobs_enabled_switch["checked"]

    def set_visible_promote_to_interrupt_print_job_enabled(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable promoteToInterruptPrintJob
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable promote to interrupt print job False to Disable
        """
        promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled, 5)
        assert promote_to_interrupt_print_jobs_enabled_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)

        old_enable = promote_to_interrupt_print_jobs_enabled_switch["checked"]

        if old_enable != enable:
            self.scroll_job_settings_view(spice, 1.0)
            promote_to_interrupt_print_jobs_enabled_switch.mouse_click(x=2,y=2)
            spice.wait_until(lambda:promote_to_interrupt_print_jobs_enabled_switch["checked"] == enable, 15)
            return enable

        return old_enable

    # Menu tools
    def goto_menu_tools_maintenance(self,spice):
        self.goto_menu_tools(spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_tools_maintenance , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.query_item(MenuAppWorkflowObjectIds.view_menuTools + " " +  MenuAppWorkflowObjectIds.menu_button_tools_maintenance)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings)
        logging.info("At Maintenance Screen")

    def goto_menu_tools_maintenance_user_maintenance(self, spice):
        self.goto_menu_tools_maintenance(spice)
        time.sleep(2)
        menu_button_tools_maintenance_user_maintenance = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenance_userMaintenance_button)
        menu_button_tools_maintenance_user_maintenance.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenance_user_maintenance)
        logging.info("At User Maintenance Screen")
        time.sleep(1)

    # Restore Settings Menu
    def goto_menu_tools_maintenance_restoresettingsmenu(self,spice):
        self.goto_menu_tools_maintenance(spice)
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_maintenanceSettings, MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore +" MouseArea")
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " +  MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore)
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings)
        logging.info("At Restore Settings Menu Screen")

    # BackUp and Restore Menu
    def goto_menu_tools_maintenance_backupandrestoremenu(self, spice):
        self.goto_menu_tools_maintenance(spice)
        button_backupandrestore = spice.query_item(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " + MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore)
        button_backupandrestore.mouse_click()
        time.sleep(3)
        # Check if Sign-in screen exists
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("User Allowed to perform Backup or Restore")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_backupAndRestore_menu)
        logging.info("At Backup And Restore Menu")

    #Perform Backup
    def goto_menu_tools_maintenance_backupandrestoremenu_backup(self, spice):
        try:
            self.goto_menu_tools_maintenance(spice)
        except Exception as e:
            logging.info("Failed to navigate to Maintenance Menu, exception="+str(e))
            return False

        backupAndRestore = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " +  MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore, timeout = 3.0)
        backupAndRestore.mouse_click()
        button_backupdata = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_backupData, timeout = 3.0)
        button_backupdata.mouse_click()
        # Checking for signin screen
        try:
           spice.wait_for(MenuAppWorkflowObjectIds.login_user_view, timeout = 3.0)
           #SignIn Screen
           self.perform_signIn(spice)
           time.sleep(5)
        except Exception as e:
            logging.info("DUT doesn't have a Sign-in Screen")
        finally:
            logging.info("User allowed to perform backup")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_backupData)
        logging.info("At Backup initiate screen")
        return True

    def perform_backup_and_check_backup_success(self, spice, net):
        """
        Helper method to complete backup and check backup success.
        UI Should be in Menu -> Tools -> Maintenance -> Back Up And Restore -> Back Up Date screen.
        UI flow is Continue -> Back Up -> Back Up success -> OK
        """
        self.click_backup_continue_btn_on_backup_date_screen(spice)
        self.click_backup_btn_on_backup_usbdisk_screen(spice)
        # The method check_backup_successful_screen cannot be used on the engine due to its slow response time. Comment out that line and verify the `backup_successful_screen` using the method `click_ok_btn_on_backup_successful_screen`. 
        # This script can confirm that the `backup_successful_screen` is displayed, as it will only function when the OK button is visible and clickable on the 'backup_successful_screen'.
        #self.check_backup_successful_screen(spice, net)
        self.click_ok_btn_on_backup_successful_screen(spice)
        self.click_back_btn_on_backup_restore(spice)
    
    def click_backup_continue_btn_on_backup_date_screen(self, spice):
        """
        Helper method to click Continue button on Back Up Date screen
        UI Should be in Menu -> Tools -> Maintenance -> Back Up And Restore -> Back Up Date screen.
        """
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_backup_continue, 15)
        spice.validate_button(continue_button)
        continue_button.mouse_click()

    def click_backup_btn_on_backup_usbdisk_screen(self, spice):
        """
        Helper method to click Back Up button on usbdisk screen. 
        UI should be in usbdisk screen, flow is Menu -> Tools -> Maintenance -> Back Up And Restore -> Back Up Date -> Continue.
        """
        backup_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_backup_continue_backup, 15)
        spice.validate_button(backup_button)
        backup_button.mouse_click()

    def check_backup_successful_screen(self, spice, net):
        """
        Helper method to check Back Up successful screen when complete back up. 
        UI should be in Back Up complete screen, flow is Menu -> Tools -> Maintenance -> Back Up And Restore -> Back Up Date -> Continue -> Back Up.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_backup_successful, timeout = 30)
        success_text = spice.wait_for(MenuAppWorkflowObjectIds.view_text_backup_success)["text"]
        expect_text = LocalizationHelper.get_string_translation(net,"cCompletedBackupSuccessfully")
        assert success_text == expect_text, f"Failed to check backup successful text, actual text is {success_text}" 

    def click_ok_btn_on_backup_successful_screen(self, spice):
        """
        Helper method to click OK button on back up successful screen when complete back up. 
        """
        okay_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_backup_continue_backup_ok)
        spice.validate_button(okay_button)
        okay_button.mouse_click()
    
    def click_back_btn_on_backup_restore(self, spice):
        """
        Helper method to click Back button back to Maintenance screen from Back Up And Restore screen.
        UI should be in Back Up And Restore screen.
        """
        back_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_back)
        spice.validate_button(back_button)
        back_button.mouse_click()

    #Perform Restore
    def goto_menu_tools_maintenance_backupandrestoremenu_restore(self, spice):
        try:
            self.goto_menu_tools_maintenance(spice)
        except Exception as e:
            logging.info("Failed to navigate to Maintenance Menu, exception="+str(e))
            return False
        
        backupAndRestore = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " +  MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore, timeout = 3.0)
        backupAndRestore.mouse_click()
        button_restoredata = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_backupAndRestore_restoreData, timeout = 3.0)
        button_restoredata.mouse_click()
        # Checking for signin screen
        try:
            spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
            #SignIn Screen
            self.perform_signIn(spice)
            time.sleep(5)
        except Exception as e:
            logging.info("DUT doesn't have a Sign-in Screen")
        finally:
            logging.info("User allowed to perform restore")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreData)
        logging.info("At Restore initiate screen")
        return True

    # Import Export Menu
    def goto_menu_tools_maintenance_import_export_menu(self, spice):
        self.goto_menu_tools_maintenance(spice)
        button_importexport = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " + MenuAppWorkflowObjectIds.menu_button_tools_maintenance_import_export)
        button_importexport.mouse_click()
        time.sleep(3)
        # Check if Sign-in screen exists
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("User Allowed to perform Import Export")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_import_export_menu)
        logging.info("At Import Export Menu")

    #Perform Export
    def goto_menu_tools_maintenance_import_export_menu_export(self, spice):
        self.goto_menu_tools_maintenance_import_export_menu(spice)
        button_exportdata = spice.wait_for(MenuAppWorkflowObjectIds.view_import_export_menu + " " + MenuAppWorkflowObjectIds.menu_button_tools_maintenance_importExport_exportData)
        button_exportdata.mouse_click()
        # Checking for signin screen
        try:
           spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
           #SignIn Screen
           self.perform_signIn(spice)
           time.sleep(5)
        except Exception as e:
            logging.info("DUT doesn't have a Sign-in Screen")
        finally:
            logging.info("User allowed to perform export")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_exportData)
        logging.info("At Export initiate screen")

    def perform_export_and_check_export_success(self, spice, net, password):
        """
        Helper method to complete export and check export success.
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Export Settings screen.
        UI flow is Continue -> Export -> enter password -> re_enter password-> Export success -> OK
        
        @param password: set the password when do export settings
        """
        self.click_export_continue_btn_on_export_settings_screen(spice)
        self.click_export_btn_on_export_usbdisk_screen(spice)
        self.enter_export_password(spice,password)
        self.re_enter_export_password(spice,password)
        self.click_ok_btn_on_export_password_screen(spice)
        self.check_export_successful_screen(spice,net)
        self.click_ok_btn_on_export_successful_screen(spice)

    def click_export_continue_btn_on_export_settings_screen(self, spice):
        """
        Helper method to click Continue button on Export Settings screen
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Export Settings screen.
        """
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.view_exportData+ " " + MenuAppWorkflowObjectIds.button_continue, 15)
        spice.validate_button(continue_button)
        continue_button.mouse_click()
    
    def click_export_btn_on_export_usbdisk_screen(self, spice):
        """
        Helper method to click Export button on usbdisk screen. 
        UI should be in usbdisk screen, flow is Menu -> Tools -> Maintenance -> Export and Import -> Export Settings -> Continue.
        """
        export_button = spice.wait_for(MenuAppWorkflowObjectIds.button_export, 15)
        spice.validate_button(export_button)
        export_button.mouse_click()
    
    def enter_export_password(self, spice, pwd):
        """
        Helper method to enter password when do export operation. 
        UI flow is Menu -> Tools -> Maintenance -> Export and Import -> Export Settings -> Continue -> Export.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_export_password, timeout = 10)
        password_field = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_importExport_enterPasswordField)
        password_field.mouse_click()
        password_field.__setitem__('displayText', pwd)
        spice.wait_for(MenuAppWorkflowObjectIds.keyboard_entry_key_button).mouse_click()

    def re_enter_export_password(self, spice, pwd):
        """
        Helper method to re enter password when do export operation. 
        UI flow is Menu -> Tools -> Maintenance -> Export and Import -> Export Settings -> Continue -> Export.
        """
        re_enter_password_field = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_importExport_reEnterPasswordField)
        re_enter_password_field.mouse_click()
        re_enter_password_field.__setitem__('displayText', pwd)
        spice.wait_for(MenuAppWorkflowObjectIds.keyboard_entry_key_button).mouse_click()
    
    def click_ok_btn_on_export_password_screen(self, spice):
        """
        Helper method to click Ok button on enter password screen when do export operation. 
        UI flow is Menu -> Tools -> Maintenance -> Export and Import -> Export Settings -> Continue -> Export.
        """
        okay_button = spice.wait_for(MenuAppWorkflowObjectIds.view_export_password+ " " +MenuAppWorkflowObjectIds.button_ok)
        spice.validate_button(okay_button)
        okay_button.mouse_click()

    def check_export_successful_screen(self, spice, net):
        """
        Helper method to check Export successful screen when complete export. 
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_export_successful, timeout = 20)
        success_text = spice.wait_for(MenuAppWorkflowObjectIds.view_export_successful_text)["text"]
        expect_text = LocalizationHelper.get_string_translation(net,"cELExportCompletedSuccessfully")
        assert success_text == expect_text, f"Failed to check export successful text, actual text is {success_text}" 

    def click_ok_btn_on_export_successful_screen(self, spice):
        """
        Helper method to click OK button on Export successful screen.
        """
        okay_button = spice.wait_for(MenuAppWorkflowObjectIds.view_export_successful+ " " +MenuAppWorkflowObjectIds.button_ok)
        spice.validate_button(okay_button)
        okay_button.mouse_click()

    #Perform Import
    def goto_menu_tools_maintenance_import_export_menu_import(self, spice):
        self.goto_menu_tools_maintenance_import_export_menu(spice)
        button_importdata = spice.query_item(MenuAppWorkflowObjectIds.view_import_export_menu + " " + MenuAppWorkflowObjectIds.menu_button_tools_maintenance_importExport_importData)
        button_importdata.mouse_click()
        # Checking for signin screen
        try:
           spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
           #SignIn Screen
           self.perform_signIn(spice)
           time.sleep(5)
        except Exception as e:
            logging.info("DUT doesn't have a Sign-in Screen")
        finally:
            logging.info("User allowed to perform import")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_importData)
        logging.info("At Import initiate screen")

    def perform_import_and_check_import_success(self, spice, net, bck_file, password):
        """
        Helper method to complete import and check import success.
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Import Settings screen.
        UI flow is Continue -> select file -> Import -> enter password -> Import success -> OK
        
        @param bck_file: the file need to import.
        @param password: the password is same with export password when do export settings.
        """
        self.click_import_continue_btn_on_import_settings_screen(spice)
        self.select_import_file_on_import_usbdisk_screen(spice, bck_file)
        self.click_import_btn_on_import_usbdisk_screen(spice)
        self.enter_import_password(spice, password)
        self.click_ok_btn_on_import_password_screen(spice)
        self.check_import_successful_screen(spice,net)
        self.click_ok_btn_on_import_successful_screen(spice)

    def click_import_continue_btn_on_import_settings_screen(self, spice):
        """
        Helper method to click Continue button on Import Settings screen
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Import Settings screen.
        """
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.button_continue, 15)
        spice.validate_button(continue_button)
        continue_button.mouse_click()
    
    def select_import_file_on_import_usbdisk_screen(self, spice, file_name):
        """
        Helper method to select exp file to import on import usbdisk screen.
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Import Settings -> Continue-> usbdisk screen.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_import_export_File, timeout = 2)
        backup_file_name_locator = "#fileListButton_"+ file_name
        backup_file = spice.wait_for(backup_file_name_locator)
        backup_file.mouse_click()
    
    def click_import_btn_on_import_usbdisk_screen(self, spice):
        """
        Helper method to click Import button after select import file.
        UI Should be in Menu -> Tools -> Maintenance -> Export and Import -> Import Settings -> Continue-> usbdisk screen.
        """
        import_button = spice.wait_for(MenuAppWorkflowObjectIds.button_import, 15)
        spice.validate_button(import_button)
        import_button.mouse_click()
    
    def enter_import_password(self, spice, pwd):
        """
        Helper method to enter password when do import operation. 
        UI flow is Menu -> Tools -> Maintenance -> Export and Import -> Import Settings -> Continue -> select file -> Import -> enter password screen.
        @param pwd: the password is same with export password when do export settings.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_import_password, timeout = 2)
        password_field = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_importExport_enterPasswordField)
        password_field.mouse_click()
        password_field.__setitem__('displayText', pwd)
        spice.query_item(MenuAppWorkflowObjectIds.keyboard_entry_key_button).mouse_click()
    
    def click_ok_btn_on_import_password_screen(self, spice):
        """
        Helper method to click OK button on enter import password screen when do import operation. 
        UI flow is Menu -> Tools -> Maintenance -> Export and Import -> Import Settings -> Continue -> select file -> Import -> enter password screen.
        """
        okay_button = spice.query_item(MenuAppWorkflowObjectIds.view_import_password+ " " +MenuAppWorkflowObjectIds.button_ok)
        spice.validate_button(okay_button)
        okay_button.mouse_click()

    def check_import_successful_screen(self, spice, net):
        """
        Helper method to check Import successful screen when complete import operation. 
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_import_successful, timeout = 20)
        success_text = spice.wait_for(MenuAppWorkflowObjectIds.view_import_successful_text)["text"]
        expect_text = LocalizationHelper.get_string_translation(net,"cELImportCompletedSuccessfully")
        assert success_text == expect_text, f"Failed to check import successful text, actual text is {success_text}" 

    def click_ok_btn_on_import_successful_screen(self, spice):
        """
        Helper method to click OK button on Import successful screen.
        """
        okay_button = spice.query_item(MenuAppWorkflowObjectIds.view_import_successful+ " " +MenuAppWorkflowObjectIds.button_ok)
        spice.validate_button(okay_button)
        okay_button.mouse_click()

    def goto_menu_tools_maintenance_restore_settings_restore_network_settings(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        button_restorenetworksettings = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_networksettings)
        button_restorenetworksettings.mouse_click()
        logging.info("At Restore Network Settings Screen")

    def validate_restore_network_settings(self,spice,net):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restore_network_settings_confirm_text,timeout = 15) ["text"] == str(LocalizationHelper.get_string_translation(net,"cRestoreOriginalSettings", "en"))
        logging.info("Validating the Restorenetworksettings confirmation text")
        spice.wait_for(MenuAppWorkflowObjectIds.button_restore_network_settings_yes).mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restore_network_settings_success_text,15)["text"] == str(LocalizationHelper.get_string_translation(net,"cSettingRestoredSuccessfully", "en"))
        logging.info("Validated the Restorenetworksettings success message")
        spice.wait_for(MenuAppWorkflowObjectIds.button_restore_network_settings_Ok,15).mouse_click()
        logging.info("Performed the Ok operation")

    def goto_menu_tools_maintenance_restoresettingsmenu_regionreset(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        # self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_restoreSettings, MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_regionreset + " mouseArea")
        button_regionreset = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_regionreset)
        button_regionreset.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_regionreset)
        logging.info("At RegionReset Menu Screen")

    def reset_printer_region(self,spice):
        region_reset = spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_regionreset)
        region_reset.mouse_click(2,2)
        logging.info("At Reset Printer Supply Region Screen")
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_printer_region_reset)
        currentElement.mouse_click()
        # Validating the progress bar
        assert spice.wait_for(MenuAppWorkflowObjectIds.resetting_printer_supply_progress_bar)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.country_region_reset_completeok,timeout=15)
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_regionreset)



    def goto_menu_tools_maintenance_restoresettingsmenu_resetusersettings(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_restoreSettings, MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_usersettings)
        button_resetusersettings = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_usersettings)
        button_resetusersettings.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_usersettings)
        logging.info("At Restore Settings Menu Screen")

    def restore_user_settings(self,spice):
        logging.info("At Reset User Settings Screen")
        button_resetusersettings = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_button)
        button_resetusersettings.mouse_click()
        logging.info("At Restore Confirmation Screen")
        time.sleep(15)

    def goto_menu_tools_maintenance_restoresettingsmenu_resetuserdata(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_restoreSettings, MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_userdata)
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        button_resetuserdata = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_userdata)
        button_resetuserdata.mouse_click()
        time.sleep(2)
        view = spice.check_item(MenuAppWorkflowObjectIds.view_restoreSettings_userdata)
        if view == None:
            spice.signIn.goto_universal_sign_in("Sign In")
            spice.signIn.select_sign_in_method("admin", "user")
            spice.signIn.enter_creds(True, "admin", "12345678")
            logging.info("at sign in screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_userdata)
        logging.info("At Restore Settings Menu Screen")

    def click_reset_button(self, spice):
        """
        click reset button under reset user settings and reset user data
        """
        restore_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_button)
        spice.validate_button(restore_button)
        restore_button.mouse_click()

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_mfp(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            "#RestoreAllFactoryDefaults",
            MenuAppWorkflowObjectIds.view_restoreSettings,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.menu_button_tools_maintenence_restore_settings_menuList_scrollBar)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_factorydefaults)
        currentElement.mouse_click()

        # Checking for signin screen
        try:
           spice.wait_for(MenuAppWorkflowObjectIds.login_user_view, timeout = 3.0)
           #SignIn Screen
           self.perform_signIn(spice)
        except Exception as e:
            logging.info("DUT doesn't have a Sign-in Screen")
        finally:
            logging.info("User allowed to perform Restore All Factory Defaults")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_factorydefaults)
        logging.info("At Restore Settings Menu Screen mfp")

    def goto_restorefactorydefaults_popuprestore(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_mfp(spice)
        Restore_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_factorydefaults_button)
        Restore_button.mouse_click()

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_sfp(self,spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.workflow_common_operations.goto_item(
            "#RestoreAllFactoryDefaults",
            MenuAppWorkflowObjectIds.view_restoreSettings,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.menu_button_tools_maintenence_restore_settings_menuList_scrollBar)
        button_resetfactorydefaults = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_factorydefaults)
        button_resetfactorydefaults.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_factorydefaults)
        logging.info("At Restore Settings Menu Screen sfp")

    def restoresettingsmenu_restoreallfactorydefaults_sfp_click_close_button(self, spice):
        '''
        Click the close button on the restore all factory defaults sfp screen
        Assumes we are on that screen when this function is called
        '''
        #Check if were on the screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_factorydefaults)

        #Validate the close button functionality
        currentElement = spice.query_item("#Cancel SpiceText")
        currentElement.mouse_click()
        logging.info("Close button works as expected.")


    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_generatedialingtonespulses(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_dialingtones)
        time.sleep(2)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        logging.info("At Generate Dial Tone Pulses Screen")

    def goto_menu_tools_servicemenu_faxdiagnostics_ringSettings(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_ringsettings,
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_ringsettings)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_ringsettings)
        logging.info("At RingSettings Screen")


    def goto_menu_tools_servicemenu_faxdiagnostics(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt)
        else:
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        logging.info("At FaxDiagnostics Screen")

    def goto_menu_tools_supplies(self, spice):
        self.goto_menu_tools(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_supplies)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_reports)
        logging.info("At Reports Screen")

    def goto_menu_tools_reports(self, spice):
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_reports , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_reports + " MouseArea")
        if not current_button["visible"] or not current_button["enabled"]:
            spice.wait_until(lambda: current_button["visible"] == True and current_button["enabled"] == True)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_reports)
        #to check whether content is available in secondary panels
        if spice.uisize not in ["XS", "S"]:
            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_report_content_secondaryPanel)
        logging.info("At Reports Screen")

    def goto_menu_tools_reports_statusreports(self, spice):
        self.goto_menu_tools_reports(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_reports, MenuAppWorkflowObjectIds.menu_button_reports_status_reports, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_menureportspage)
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.list_checkboxButtonListLayout)
        logging.info("At Status Reports Screen")

    def select_status_reports_mode_from_menu_tools_reports_status_reports(self, spice, status_reports_mode, check_expected=True):
        '''
        This is helper method to select status reports mode from tools -> reports -> status reports
        UI should be Menu->Tools-> Reports -> Status Reports
        Args: status_reports_mode: status reports mode, such as Network Security Report/Usage RePORT /Web Access Test Report/ Job Log and so on...
                                   add different status reports mode implementation if necessary
        '''
        troubleshooting_fax_t30_repmode_view = spice.wait_for(MenuAppWorkflowObjectIds.list_checkboxButtonListLayout)
        spice.wait_until(lambda:troubleshooting_fax_t30_repmode_view["visible"])
        logging.info(f"Select fax T30 report mode: <{status_reports_mode}>")

        if status_reports_mode == "Job Log":
            row_object_report_name = MenuAppWorkflowObjectIds.row_object_job_log_status_reports
            control_object_report_name = MenuAppWorkflowObjectIds.control_object_job_log_status_reports
            if spice.uisize in ["XS", "S"]:
                self.workflow_common_operations.goto_item(row_object_report_name,MenuAppWorkflowObjectIds.view_status_report, select_option=False,scrollbar_objectname = MenuAppWorkflowObjectIds.status_report_scrollbar_name)

        elif(status_reports_mode == "Color Usage Job Log"):
            row_object_report_name = MenuAppWorkflowObjectIds.viewObject_report_colorUsageJobLog
            control_object_report_name = MenuAppWorkflowObjectIds.control_object_colorUsageJob_log_status_reports

        else:
            raise logging.info(f"{status_reports_mode} is not supported to select")

        spice.wait_for(row_object_report_name)
        current_button = spice.wait_for(control_object_report_name)
        current_button.mouse_click()
        assert spice.wait_for(control_object_report_name)['checked'] == check_expected

    def print_prt_log_list(self, spice):
        self.workflow_common_operations.scroll_vertical_row_item_into_view(
            MenuAppWorkflowObjectIds.list_checkboxButtonListLayout,
            MenuAppWorkflowObjectIds.row_object_configuration_reports,
            top_item_id = MenuAppWorkflowObjectIds.status_reports_header)
        spice.wait_for(MenuAppWorkflowObjectIds.row_object_configuration_reports)
        report_button = spice.query_item(MenuAppWorkflowObjectIds.control_object_configuration_reports)
        report_button.mouse_click()

        self.workflow_common_operations.scroll_vertical_row_item_into_view(
            MenuAppWorkflowObjectIds.list_checkboxButtonListLayout,
            MenuAppWorkflowObjectIds.row_object_job_log_status_reports,
            top_item_id = MenuAppWorkflowObjectIds.status_reports_header)
        spice.wait_for(MenuAppWorkflowObjectIds.row_object_job_log_status_reports)
        report_button = spice.query_item(MenuAppWorkflowObjectIds.control_object_job_log_status_reports)
        report_button.mouse_click()

        # Enterprise devices have a sign-in screen when printing the job log report
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("user signed in")

        self.workflow_common_operations.scroll_vertical_row_item_into_view(
            MenuAppWorkflowObjectIds.list_checkboxButtonListLayout,
            MenuAppWorkflowObjectIds.row_object_supplies_status_reports,
            top_item_id = MenuAppWorkflowObjectIds.status_reports_header)
        spice.wait_for(MenuAppWorkflowObjectIds.row_object_supplies_status_reports)
        report_button = spice.query_item(MenuAppWorkflowObjectIds.control_object_supplies_status_reports)
        report_button.mouse_click()

        self.workflow_common_operations.scroll_vertical_row_item_into_view(
            MenuAppWorkflowObjectIds.list_checkboxButtonListLayout,
            MenuAppWorkflowObjectIds.row_object_usage_reports,
            top_item_id = MenuAppWorkflowObjectIds.status_reports_header)
        spice.wait_for(MenuAppWorkflowObjectIds.row_object_usage_reports)
        report_button = spice.query_item(MenuAppWorkflowObjectIds.control_object_usage_reports)
        report_button.mouse_click()

        print_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_print_button)
        spice.validate_button(print_button)
        print_button.mouse_click()

    def print_status_reports_with_click_print_button(self, spice):
        '''
        This is helper method to click print button to printing status reports.
        UI should be Menu->Tools-> Reports -> Status Reports
        '''
        spice.query_item(MenuAppWorkflowObjectIds.menu_button_print_button).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo)["text"] == "Printing..."

    def print_eventlog_with_click_print_button(self, spice):
        '''
        This is helper method to click print button to print the eventlog.
        UI should be Menu->Tools-> Reports -> Event Logs
        '''
        print("Navigating to Print button to print eventlog")
        print_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_print_eventlog)
        print_button.mouse_click()

    def goto_menu_tools_reports_faxreports(self, spice):
        self.goto_menu_tools_reports(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_reports, MenuAppWorkflowObjectIds.menu_button_reports_fax_reports)
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.list_checkboxButtonListLayout)
        logging.info("At Fax Reports Screen")

    def goto_menu_tools_reports_eventlog(self, spice):
        self.goto_menu_tools_reports(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_reports, MenuAppWorkflowObjectIds.menu_button_reports_eventlog)
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_eventlog, timeout = 10)
        logging.info("At Event Log Screen")

    def goto_menu_tools_troubleshooting(self, spice):
        item = spice.check_item(MenuAppWorkflowObjectIds.menu_button_menuApp)
        if item != None and item["visible"] == True:
            self.goto_menu_tools(spice)
        else:
            spice.home.goto_home_tools()
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_troubleshooting , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("user signed in")
        status_center_service_stack_view = spice.check_item(MenuAppWorkflowObjectIds.view_troubleshooting)
        if status_center_service_stack_view != None:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_menu_list)
        logging.info("At Troubleshooting Screen")

    def goto_menu_tools_troubleshooting_print_Quality(self,spice):
        self.goto_menu_tools_troubleshooting(spice)
        printQuality = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printQuality).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printQuality)
        logging.info("At Print Quality screen")

    def goto_menu_tools_troubleshooting_diagnosticTestView(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        diagnostic_test = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        diagnostic_test.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        logging.info("In diagnosticTestView page")
        time.sleep(2)

    def goto_troubleshooting_printQuality_cleaningpage(self, spice):
        self.goto_menu_tools_troubleshooting_print_Quality(spice)
        cleaningPage = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_cleaningPage).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_cleaningPage)
        logging.info("In cleaning page view")

    def goto_troubleshooting_printQuality_colorBandTest(self, spice):
        self.goto_menu_tools_troubleshooting_print_Quality(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printQuality, timeout = 60)
        #click printQuality pages
        spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printQualityPages,60).mouse_click()
        logging.info("At printQualityPages page")
        #click colorBand Test
        spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_colorBandTest,60).mouse_click()
        logging.info("At colorBandTest page")

    def goto_troubleshooting_diagnostictestview_paperpathtest(self, spice):
        self.goto_menu_tools_troubleshooting_diagnosticTestView(spice)
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button)
        continue_button.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_paperpathtest)
        paperpath_test = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_paperpathtest)
        #assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_paperpathtest)
        paperpath_test.mouse_click()
        logging.info("in paperpathTestview")

    def goto_troubleshooting_diagnostictestview_printStopTest(self, spice):
        self.goto_menu_tools_troubleshooting_diagnosticTestView(spice)
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button)
        continue_button.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest)
        printStopTest = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest)
        printStopTest.mouse_click()
        logging.info("in printStopTestview")

    """
     * Navigate to the Troubleshooting Diagnostic Test View through Home Apps.
     * @param self The instance of the class.
     * @param spice The spice object.
     */
    """
    def goto_troubleshooting_diagnostictestview_printStopTest_through_home_apps(self, spice):
        spice.home_operations.home_navigation("#tools")
        current_button = spice.query_item("#f6d66534-9b96-4f12-9f51-cea0ab19dc79 MouseArea")
        # Clicking in the mid height of the button to avoid click on header or section
        current_button_height = current_button["height"] / 2
        current_button.mouse_click(0, current_button_height)
        logging.info("At Troubleshooting Screen")
        diagnostic_test = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        diagnostic_test.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests, 60)
        logging.info("In diagnosticTestView page")
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button, 60)
        continue_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest, 60)
        printStopTest = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest)
        printStopTest.mouse_click()
        logging.info("in printStopTestview")

    def goto_troubleshooting_diagnostictestview_printStopTest_without_clearing_alerts(self, spice):
        try:
            spice.query_item("#floatingDock")
            logging.info("Printer Having Foating Dock Homescreen")
            self.goto_menu_app_floating_dock(spice)

        except:
            logging.info("Printer Having Regular Homescreen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
            homeApp = spice.query_item(MenuAppWorkflowObjectIds.view_homeScreen)
            spice.wait_until(lambda: homeApp["visible"] == True)
            logging.info("At Home Screen")
            # move the scrollbar firstly.
            self.workflow_common_operations.scroll_to_position_horizontal(0)
            logging.info("Reset horizontal scrollbar")
            time.sleep(2)
            # Printer goes into sleep mode once cdm/ews calls[that execution time is greater than sleep time] in test before UI naviation, for
            # this scenario need to check printer in sleep or not when perform UI navigation
            currentState = int(spice.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
            logging.debug('Printer Sleep status is: %s',currentState)
            if currentState >= 2:
                logging.debug("Waking up printer")
                spice.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
                time.sleep(2)

            # enter the menu screen
            logging.info("Entering Menu")
            adminApp = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp +" MouseArea" )
            # Wait for clickable situation
            spice.wait_until(lambda: adminApp["enabled"] == True)
            spice.wait_until(lambda: adminApp["visible"] == True)
            adminApp.mouse_click()
            time.sleep(5)

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, timeout = 9.0)
        logging.info("At Menu Screen")
        time.sleep(1)
        cdmvalue= spice.cdm.get(spice.cdm.CONTROL_PANEL_CONFIGURATION_ENDPOINT)
        # object id will be localization when using different language

        try:
            if cdmvalue["currentLanguage"] == "es":
                self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,"#UtilidadeslandingPageMenuAppListcolumn" , MenuAppWorkflowObjectIds.landingPage_Content_Item , "#UtilidadessectionBottomBorder")
            else:
                self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.utilities_section_bottom_border)
        except Exception:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_tools , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.empty_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.empty_section_bottom_border)

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuTools)
        logging.info("At Tools Screen")
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_troubleshooting , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        status_center_service_stack_view = spice.check_item(MenuAppWorkflowObjectIds.view_troubleshooting)
        if status_center_service_stack_view != None:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_menu_list)
        logging.info("At Troubleshooting Screen")
        diagnostic_test = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        diagnostic_test.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        logging.info("In diagnosticTestView page")
        time.sleep(2)
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button)
        continue_button.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest)
        printStopTest = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printStopTest)
        printStopTest.mouse_click()
        logging.info("in printStopTestview")


    def click_Paperpathtest_paperTray(self,spice):
        paperTray = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_papertray)
        paperTray.mouse_click()
        logging.info("in paper_tray")

    def click_Paperpathtest_outputSides(self,spice):
        output_Side = spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_outputsides)
        output_Side.mouse_click()
        logging.info("in ouput_sides")

    def goto_menu_tools_troubleshooting_diagnosticTests_option(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        diagnostic_test = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        diagnostic_test.mouse_click()
        # assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_diagnostic_tests)
        logging.info("In diagnosticTestView page")
        time.sleep(2)

    def goto_troubleshooting_diagnostictestview_runfaxtest(self, spice):
        self.goto_menu_tools_troubleshooting_diagnosticTests_option(spice)
        view = spice.check_item(MenuAppWorkflowObjectIds.maintenancemode_view)
        if view == None:
            spice.signIn.select_sign_in_method("admin", "user")
            spice.signIn.enter_creds(True, "admin", "Pass2468")
            logging.info("at sign in screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_view)
        time.sleep(1)
        # diagnostictest = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_view)
        # diagnostictest.mouse_click()
        # time.sleep(1)
        continuebutton = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button)
        continuebutton.mouse_click()
        time.sleep(2)

    def goto_troubleshooting_diagnostictestview_maintenancemode_view(self, spice):
        self.goto_menu_tools_troubleshooting_diagnosticTests_option(spice)
        logging.info("Checking Maintenance Mode")
        assert spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_view)
        time.sleep(1)

    #spinwidget copies
    def change_num_copies(self,spice, num_copies):
        numCopiesElement = spice.wait_for("#paperpathspinbox #SpinBoxTextInput")
        numCopiesElement.__setitem__('text', num_copies)

    def get_number_of_copies(self,spice):
        '''
        return total number of copies in spinbox textinput
        '''
        numCopiesElement = spice.wait_for("#paperpathspinbox #SpinBoxTextInput")
        valuee = numCopiesElement.__getitem__('text')
        return valuee

    def change_delay_timer(self,spice, timer):
        delayTimerElement = spice.wait_for("#delayTimerspinbox #SpinBoxTextInput")
        delayTimerElement.__setitem__('text', timer)

    def get_timer_value(self,spice):
        '''
        return timer value in spinbox
        '''
        delayTimerElement = spice.wait_for("#delayTimerspinbox #SpinBoxTextInput")
        value = delayTimerElement.__getitem__('text')
        return value

    def click_Paperpathtest_numberofcopies_increase(self, spice, value_num):
        '''
        This function will increase the count of copies using the upbtn
        '''
        upbutton = spice.wait_for("#paperpathspinbox #upBtn")
        for i in range(0, value_num):
            upbutton.mouse_click()

    def click_Paperpathtest_numberofcopies_decrease(self, spice, value_num):
        '''
        This function will decrease the count of copies using the downbtn
        '''
        downButton = spice.wait_for("#paperpathspinbox #downBtn")
        for i in range(0, value_num):
            downButton.mouse_click()

    def goto_menu_tools_troubleshooting_printquality(self, spice, isFaxSupported = True):
        self.goto_menu_tools_troubleshooting(spice)
        if (isFaxSupported):
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_calibration).mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_printheads)
        logging.info ("At Troubleshooting -> Print Quality")

    def goto_menu_tools_troubleshooting_print_quality_tray_alignment(self, spice, cdm):
        try:
            isMfp = cdm.get_raw(cdm.SCANNER_STATUS).status_code == 200
            logging.info(f"Scanner OK: {isMfp}")
        except HTTPError as e:
            logging.info(f"Failed to get scanner status: {e}")
            isMfp = False
        self.goto_menu_tools_troubleshooting_printquality(spice, isMfp)
        self.workflow_common_operations.scroll_to_position_vertical(0.8, MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_printquality)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality_image_registration).mouse_click()
        logging.info ("At Troubleshooting -> Print Quality -> Image Registration")

    def goto_menu_tools_troubleshooting_Fax(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        ## TODO: Need to replace FAX menu navigation with menu_navigation() after FAX object names/ids are added
        faxButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax)
        faxButton.mouse_click()
        #self.menu_navigation(spice, qml, MenuAppWorkflowObjectIds.view_troubleshooting, MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax)
        #assert spice.wait_for("#SpiceView")
        logging.info("At Troubleshooting -> FAX Screen")

        # Added for Troubleshooting -> FAX Screen
    def goto_menu_tools_troubleshooting_Fax_Menu(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        faxButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_menu)
        faxButton.mouse_click()
        logging.info("At Troubleshooting -> FAX Screen")
    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_faxT30)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_faxT30)
        logging.info("At Troubleshooting -> FAX Screen -> faxT30Button")

    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode_enterprise(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_menu)
        currentElement.mouse_click()
        logging.info("At Troubleshooting -> FAX Screen -> faxT30Button")

    def goto_menu_tools_troubleshooting_Fax_RunFaxTest(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        currentElement = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_runFaxTest)
        currentElement.mouse_click()

    def goto_menu_tools_troubleshooting_Fax_ClearFaxLogMemory(self, spice, pressClearButton2 = True):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_troubleshooting_fax, MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_clearFaxLogs, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_fax)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_clearLogs).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_clearLogs)
        if (pressClearButton2):
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_clearLogs_clearbutton2).mouse_click()

    def goto_menu_tools_troubleshooting_Fax_PBXRingDetect(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        ## Further Navigation is not required for PBX Ring Detect in workflow.
        
    def goto_home_settings_outputBins_staplerStacker_operationMode(self, spice):
        item = spice.check_item(MenuAppWorkflowObjectIds.menu_button_menuApp)
        if item != None and item["visible"] == True:
            self.goto_menu_settings(spice)
        else:
            self._spice.home.goto_home_settings_app(spice)
        logging.info("At the settings menu screen")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.settings_outputDestination,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        spice.wait_for(MenuAppWorkflowObjectIds.settings_outputDestination_staplerStacker, 60).mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.settings_operationMode, 60).mouse_click()
        logging.info("At the operation mode screen")
        
    def goto_home_tools_maintanence_resetUserdata(self,spice):
        item = spice.check_item(MenuAppWorkflowObjectIds.menu_button_menuApp)
        if item != None and item["visible"] == True:
            self.goto_menu_tools(spice)
        else:
            spice.home.goto_home_tools()
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, "#9da37e46-9b8a-4dc2-a24c-017fee6b088f" , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for("#9da37e46-9b8a-4dc2-a24c-017fee6b088f MouseArea",60)
        current_button_height = current_button["height"] / 2
        current_button.mouse_click(0, current_button_height)
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings)
        current_button1 = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings + " " +  MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore)
        current_button1.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings)
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        button_resetuserdata = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_restore_userdata)
        button_resetuserdata.mouse_click()
        time.sleep(2)
        view = spice.check_item(MenuAppWorkflowObjectIds.view_restoreSettings_userdata)
        if view == None:
            spice.signIn.goto_universal_sign_in("Sign In")
            spice.signIn.select_sign_in_method("admin", "user")
            spice.signIn.enter_creds(True, "admin", "12345678")
            logging.info("at sign in screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_userdata)
        logging.info("At Restore Settings Menu Screen")
        logging.info("At reset screen")
    
    def goto_menu_settings_general_display(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)

    def goto_menu_settings_general_display_high_contrast(self, spice , isClicked=True):
        self.goto_menu_settings_general_display(spice)
        time.sleep(2)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_highContrast_switch , select_option = False , scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_display_settings)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_highContrast_switch)
        logging.info("At High Contrast Settings Screen")
        

    def get_high_contrast_toggle_state(self, spice):
        try:
            high_contrast_toggle = spice.wait_for(MenuAppWorkflowObjectIds.menu_highContrast_switch, timeout=5)
            try:
                state = high_contrast_toggle["checked"]
            except (KeyError, AttributeError):
                state = False
            logging.info(f"High contrast toggle state: {state}")
            return state
        except Exception as e:
            logging.error(f"Failed to get high contrast toggle state: {e}")
            raise

    def toggle_high_contrast_mode(self, spice):
        try:
            high_contrast_toggle = spice.wait_for(MenuAppWorkflowObjectIds.menu_highContrast_switch, timeout=5)
            try:
                initial_state = high_contrast_toggle.__getitem__('checked')
            except (KeyError, AttributeError):
                initial_state = False
            
            # Click the toggle
            high_contrast_toggle.mouse_click()
            
            # Wait for state to change
            def check_state_changed():
                try:
                    current_state = high_contrast_toggle.__getitem__('checked')
                except (KeyError, AttributeError):
                    current_state = False
                return current_state != initial_state
            
            spice.wait_until(check_state_changed, timeout=5)
            
            try:
                new_state = high_contrast_toggle.__getitem__('checked')
            except (KeyError, AttributeError):
                new_state = False
            
            logging.info(f"High contrast toggle changed from {initial_state} to {new_state}")
            return "true" if new_state else "false"
        except Exception as e:
            logging.error(f"Failed to toggle high contrast mode: {e}")
            raise

    def verify_high_contrast_toggle_functionality(self, spice):
        try:
            # Get initial toggle state
            initial_state = self.get_high_contrast_toggle_state(spice)
            logging.info(f"Initial high contrast toggle state: {initial_state}")
            
            # Test toggle functionality - first toggle
            new_state = self.toggle_high_contrast_mode(spice)
            expected_new_state = "false" if initial_state == "true" else "true"
            
            if new_state != expected_new_state:
                raise AssertionError(f"Toggle state should have changed from {initial_state} to {expected_new_state}, got {new_state}")
            
            # Test toggle functionality - return to original state
            final_state = self.toggle_high_contrast_mode(spice)
            
            if final_state != initial_state:
                raise AssertionError(f"Toggle should return to initial state {initial_state}, got {final_state}")
            
            logging.info("High contrast toggle functionality verification completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"High contrast toggle functionality verification failed: {e}")
            raise

    def verify_high_contrast_toggle_interactive(self, spice):
        try:
            high_contrast_toggle = spice.wait_for(MenuAppWorkflowObjectIds.menu_highContrast_switch, timeout=5)
            
            # Verify toggle is not None
            if high_contrast_toggle is None:
                raise AssertionError("High contrast toggle should be visible")
            
            # Validate that the toggle is interactive
            spice.validate_button(high_contrast_toggle)
            
            logging.info("High contrast toggle is present and interactive")
            return True
            
        except Exception as e:
            logging.error(f"High contrast toggle interaction verification failed: {e}")
            raise

    def goto_menu_settings_general_language(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_display_language , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
        assert spice.wait_for("#languageWFMenuSelectionList")
        logging.info("At Language Screen")
        time.sleep(1)

    def goto_menu_settings_general_region(self, spice, signInRequired=True):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_region , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_country_region, timeout=50)
        logging.info("At country/Region setting Screen")
        time.sleep(1)

    def goto_menu_settings_general_theme(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_display_theme , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
        assert spice.wait_for(MenuAppWorkflowObjectIds.theme_menu_view)
        logging.info("At color theme screen")
        time.sleep(1)

    def region_settings_sampletest(self, spice):
        # click the country/region dropdown
        spice.homeMenuUI().goto_menu_settings_general_region(spice)
        time.sleep(10)
        self.menu_navigation_radiobutton(spice, "#countryRegionWFMenuSelectionList", "#AOcountryRegion", "#MenuValueAO",
                                         scrollbar_objectname="#countryRegionWFMenuSelectionListScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Menu")
        time.sleep(2)

    def region_settings_all(self, spice, net, cdm):

        # click the country/region dropdown
        spice.homeMenuUI().goto_menu_settings_general_region(spice)
        time.sleep(10)

        # this method extracts the the supported region values from the constraints
        count = 0
        regions = []
        options = []
        res = cdm.get(cdm.SYSTEM_CONFIGURATION_CONSTRAINTS)

        options = res["validators"][1]["options"]
        print (options)

        for region in options:
            regions.append(region["seValue"])
            count = count + 1

        i = 0
        for region in regions:
            menu_item_id = "#"+region+"countryRegion"
            obj_id = "#MenuValue"+region
            self.menu_navigation_radiobutton(spice, MenuAppWorkflowObjectIds.view_settings_country_region, menu_item_id, obj_id, scrollbar_objectname="#countryRegionMenuSelectionListScrollBar")
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
            logging.info("At general Settings Menu")
            time.sleep(10)
            i=i+1
            self.menu_navigation(spice, "#generalSettingsMenuList", MenuAppWorkflowObjectIds.menu_button_settings_region)
            time.sleep(10)

        assert i==count

    # Menu Settings General Inactivity Timeout

    def goto_menu_settings_general_inactivitytimeout(self, spice, password = "12345678"):
        isEnterPriseProduct = False
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
        time.sleep(1)
        isscrollbarDisplaySettingsScrollAvailable = False
        scrollbar_display_settings = spice.check_item(MenuAppWorkflowObjectIds.scrollbar_display_settings)
        if scrollbar_display_settings != None:
            logging.info("scrollbar_display_settings is not None")
            isscrollbarDisplaySettingsScrollAvailable = scrollbar_display_settings["visible"]
        logging.info("isscrollbarDisplaySettingsScrollAvailable "+str(isscrollbarDisplaySettingsScrollAvailable))

        try:
            if isscrollbarDisplaySettingsScrollAvailable:
                self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout_enterprise, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout_enterprise_input).mouse_click()
            isEnterPriseProduct = True
        except Exception as e:
            if isscrollbarDisplaySettingsScrollAvailable:
                self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
            try:
                (spice.query_item(MenuAppWorkflowObjectIds.view_inactivity_timeout_settings)["visible"])
            except Exception as e:
                spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout_input).mouse_click()
            else:
                logging.info("At expected Menu")
        else:
            logging.info("At expected Menu")
        try:
            try:
                # Execute sign-in only for non-homepro devices
                spice.homeMenuUI().perform_signIn(spice)
            except Exception as e:
                logging.info("DUT doesn't have a Sign-in Screen")
            time.sleep(10)

            # Combobox in small screen (text image branch) will move directly to list after signin
            if isEnterPriseProduct:
                print('it is Enterprise Product')
            else:
                try:
                    (spice.query_item(MenuAppWorkflowObjectIds.view_inactivity_timeout_settings)["visible"])
                except Exception as e:
                    logging.info("-----inactivity list is not found-----")
                    spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout_input).mouse_click()
                else:
                    logging.info("-----inactivity list is found-----")
        except TimeoutError:
            logging.info("-----the network settings view is load without login-----")
        finally:
            ##Assert Energy sleep Screen
            if not isEnterPriseProduct:
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_inactivity_timeout_settings)
            logging.info("At Inactivity Timeout Settings Screen")
            time.sleep(1)
            return isEnterPriseProduct

    def setInactivityTimeoutForEnterprise(self, spice, value):
        inactivityVal = str(value)
        for i in inactivityVal:
            keyboard_button = spice.wait_for(f"#key{i}PositiveIntegerKeypad")
            keyboard_button.mouse_click()
        keyboard_button = spice.wait_for("#enterKeyPositiveIntegerKeypad")
        keyboard_button.mouse_click()

    def set_inactivitytimeout_thirtyseconds(self, spice, already_in_setting = False):
        isEnterPriseProduct = False
        if not already_in_setting:
            isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)
        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,30)
        else:
            spice.query_item(MenuAppWorkflowObjectIds.view_inactivity_timeout_settings,MenuAppWorkflowObjectIds.inactivity_timeout_30sec).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("Set Inactivity Timeout to 30 seconds")
        time.sleep(1)

    def set_inactivitytimeout_oneminute(self, spice, already_in_setting = False):
        if not already_in_setting:
            isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)

        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,60)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_inactivity_timeout_settings, MenuAppWorkflowObjectIds.inactivity_timeout_1min)

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("Set Inactivity Timeout to 1 minute")
        time.sleep(1)

    def set_inactivitytimeout_twominutes(self, spice, already_in_setting = False):
        if not already_in_setting:
            isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)
        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,120)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_inactivity_timeout_settings, MenuAppWorkflowObjectIds.inactivity_timeout_2mins)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("Set Inactivity Timeout to 2 mins")
        time.sleep(1)

    def set_inactivitytimeout_fiveminutes(self, spice, already_in_setting = False):
        if not already_in_setting:
            isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)

        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,300)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_inactivity_timeout_settings, MenuAppWorkflowObjectIds.inactivity_timeout_5mins, scrollbar_objectname="#comboBoxScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("Set Inactivity Timeout to 5 mins")
        time.sleep(10)

    def goto_menu_settings_network(self, spice, password = "12345678", success_login_expected = True):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_network, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
        

    def goto_menu_settings_ldb(self, spice, success_login_expected = True, password = "12345678"):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_ldb, scrollbar_objectname="#settingsMenuListListViewlist1ScrollBar")
        spice.wait_for("#LaserJetDebugBridgeMenuTextImageBranch", 60).mouse_click()
        if success_login_expected:
            spice.signIn.select_sign_in_method("admin", "user")
            spice.signIn.enter_creds(True, "admin", password)
    
    def verify_network_menu_item(self, spice): 
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxEthernetSettingsTextImage_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxEthernetSettingsTextImage_2infoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxWFDSettingsTextImage_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxWFDSettingsTextImage_2infoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxAirPrint_WFSettingsSwitch", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxIPv4Enable_WFSettingsSwitch", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxIPv6Enable_WFMenuSwitch", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxIPv6Enable_WFSettingsSwitchImageContainer", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxHostName_WFSettingsTextImage_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#cnxBonjourName_WFSettingsTextImage_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#proxyConfigView_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#networkSecuritySettingsSettingsTextImage_firstinfoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_networkSettings, "#networkSecuritySettingsSettingsTextImage_2infoBlockRow", False, scrollbar_objectname = "#cnxEthernetMenuListScrollBar")



    def goto_menu_help(self, spice):
        self.goto_menu(spice)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_help)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help + " MouseArea")
        current_button.mouse_click()
        logging.info("At Expected Menu")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp)
        logging.info("At help Screen")

    def verify_network_wifi_image_container_height(self, spice):

        # move scrollbar to postion 0
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_menu_networkpage)
        scrollbar.__setitem__("position", "0")

        # check height of the conatiner that should equal to default icon size
        image_container_height = str(spice.query_item(MenuAppWorkflowObjectIds.network_wifi_image_container)["height"])
        logging.info("wifi image container height :"+image_container_height)
        assert image_container_height == "29.53846153846154" or image_container_height == "27.5"

    def get_system_alert_and_close(self,spice):
        """
        Waits for UI to show a system alert and return event properties
        """
        spice.wait_for("#SystemEventErrorView")
        time.sleep(1)
        alertEvent = dict()
        alertEvent["errorCode"]   = spice.query_item("#titleObject")["text"]
        alertEvent["description"] = spice.query_item("#alertDetailDescription #contentItem")["text"]

        okButton = spice.wait_for("#OK")
        okButton.mouse_click()
        spice.wait_for("#HomeScreenView")

        return alertEvent

    def get_system_alert_and_close_with_details(self, spice):
        """
        Handle system alert by first clicking the details button, then closing the alert.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.systemEventErrorView)
        detailsButton = spice.wait_for(MenuAppWorkflowObjectIds.systemEventDetailButton)
        detailsButton.mouse_click()

        alertDetailOkButton = spice.wait_for(MenuAppWorkflowObjectIds.alertDetailOkButton)
        #ok button click is added two times because first one is to  check details buttons Ok and then main alert OK button 
        alertDetailOkButton.mouse_click()
        time.sleep(1)
        okButton = spice.wait_for(MenuAppWorkflowObjectIds.okButtonAlert)
        okButton.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)


    def verify_system_alert(self,spice):
        """
        Verifies the contents of System Alert
        """
        errorscreen = spice.wait_for("#SystemEventErrorView")
        titleText = spice.query_item("#titleObject")["text"]
        print(titleText)
        eventCode = spice.query_item("#contentItem")["text"]
        print(eventCode)
        okButton = spice.wait_for("#OK")
        okButton.mouse_click()
        spice.wait_for("#HomeScreenView")
        assert titleText == "Event Code: F0.02.05.09"
        assert eventCode == "F0.02.05.09"


    # Menu Settings General Language
    def set_language(self, spice, net, cdm, language, scrollspeed=0.02):
        self.goto_menu_settings_general_language(spice)
        selectedLang = self.device_language[language]
        logging.info(selectedLang)
        menu_item_id = MenuAppWorkflowObjectIds.language_menu_item_id.format(elementid=selectedLang)
        obj_id = MenuAppWorkflowObjectIds.language_menu_obj_id.format(elementid=selectedLang)
        self.menu_navigation_radiobutton(spice, MenuAppWorkflowObjectIds.language_list_view, menu_item_id, obj_id, scrolling_value=scrollspeed, scrollbar_objectname=MenuAppWorkflowObjectIds.language_list_view_scrollbar)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings, timeout=50)
        logging.info("At General - Display Settings Menu")

        # Validate if the cdm reflects the set language
        device_language = language.split("_")[1]
        QmlTestServer.wait_until(condition=lambda:cdm.get(cdm.SYSTEM_CONFIGURATION)["deviceLanguage"] == device_language, timeout=30, current_state_method=cdm.get(cdm.SYSTEM_CONFIGURATION)["deviceLanguage"], delay=5)
        QmlTestServer.wait_until(condition=lambda:cdm.get(cdm.SYSTEM_IDENTITY)["deviceLanguage"] == device_language, timeout=30, current_state_method=cdm.get(cdm.SYSTEM_IDENTITY)["deviceLanguage"], delay=5)
        logging.info("Set Language Successfully to " + self.device_language_options[language])

    # Menu Settings General Region
    def set_region(self, spice, net, cdm, region, scrollspeed = 0.02):

        actualcountry = self.get_current_region_code(spice)
        if (actualcountry != region):
            menu_item_id= MenuAppWorkflowObjectIds.region_menu_item_id.format(region = region)
            obj_id = MenuAppWorkflowObjectIds.region_menu_obj_id.format(region = region)

            self.menu_navigation_radiobutton(spice, MenuAppWorkflowObjectIds.region_list_view, menu_item_id, obj_id, scrolling_value = scrollspeed ,scrollbar_objectname=MenuAppWorkflowObjectIds.region_list_view_scrollbar)

        logging.info("At General Settings Menu")
        time.sleep(2)

    # Menu > Settings > General > Display > Color theme
    def set_theme(self, spice, theme):
        '''
        This is helper method to select a new color theme
        UI flow Menu > Settings > General > Display > Color theme
        '''
        current_theme = spice.udw.mainUiApp.ApplicationEngine.getTheme()
        assert current_theme != theme, "Selected theme is same as current theme."

        supported_themes = spice.udw.mainUiApp.ApplicationEngine.getSupportedThemes().splitlines()
        assert theme in supported_themes, "Selected theme not supported."

        self.goto_menu_settings_general_theme(spice)

        theme_setting = spice.wait_for(MenuAppWorkflowObjectIds.theme_item_objectName.format(theme = theme.replace('Theme', '')))
        theme_setting.mouse_click()

        # Workaround to not reload the theme at runtime until fix UI issues
        okButton = spice.wait_for(MenuAppWorkflowObjectIds.theme_ok_button)
        okButton.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("Color theme changed to " + theme)

    def get_theme(self, spice):
        '''
        This is helper method to get selected color theme
        UI flow Menu > Settings > General > Display > Color theme
        '''
        self.goto_menu_settings_general_theme(spice)

        current_theme = spice.udw.mainUiApp.ApplicationEngine.getTheme()
        supported_themes = spice.udw.mainUiApp.ApplicationEngine.getSupportedThemes().splitlines()
        for theme in supported_themes:
            if spice.wait_for(MenuAppWorkflowObjectIds.theme_item_objectName.format(theme = theme.replace('Theme', '')))["checked"] == True:
                assert current_theme == theme, "Selected theme not matched with UI setting."

        logging.info("Current color theme is " + current_theme)
        return current_theme

    def goto_menu_tools_servicemenu_serviceresets(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_service_reset_alt)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_service_reset)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_reset)
        logging.info("At Service Reset Screen")
        time.sleep(1)

    def goto_serviceresets_servicemenu(self, spice):
        if self.product_family == 'enterprise':
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_service_reset_alt)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_service_reset)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_reset)
        logging.info("At Service Reset Screen")

    def goto_menu_tools_servicemenu_serviceresets_usersettingsreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        logging.info("At User Settings Reset Screen")
        spice.wait_for("#userSettingsResetMenuButton").mouse_click()


    def goto_menu_tools_servicemenu_serviceresets_userdatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        logging.info("At User Data Reset Screen")
        spice.wait_for("#userDataResetMenuButton").mouse_click()

    def goto_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)

        resetButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_factorydata_reset)
        resetButton.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_restore_all_data_popup)
        logging.info("At Factory Reset Screen")
        time.sleep(1)

    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)

        # Click on Restore Button
        restoreButton = spice.query_item("#RestoreAllDataReset #FooterView #ContentItem #ContentItemText")
        assert restoreButton["text"] == "Restore", "Could not find Restore Button"
        restoreButton.mouse_click()
        spice.wait_for("#HomeScreenView")

    def goto_menu_tools_servicemenu_serviceresets_transferkitreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        logging.info("At Transfer Kit Reset Screen")

    def goto_menu_tools_servicemenu_serviceresets_repairmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.workflow_common_operations.scroll_to_position_vertical(0.20, MenuAppWorkflowObjectIds.scrollbar_tools_service_serviceresets)
        spice.wait_for("#repairModeMenuButton").mouse_click()
        logging.info("At Repair Mode Screen")

    def goto_menu_tools_servicemenu_systemconfiguration(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_system_configuration_alt, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_serviceMenu)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_system_configuration, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_serviceMenu)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_system_configuration)

    def goto_menu_tools_service(self,spice,cdm,udw):
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        spice.homeMenuUI().goto_menu_tools(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service + " MouseArea").mouse_click()
        keyboard = spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard
        product_pin = "12345678"
        if printerName == "camden":
            product_pin = "12048020"
        elif printerName == "busch":
            product_pin = "12043020"
        elif printerName == "bell":
            product_pin = "10680022"
        elif printerName == "curie":
            product_pin = "10580022"
        elif printerName == "edison":
            product_pin = "10570022"
        elif printerName == "fenway":
            product_pin = "12045520"
        elif printerName == "hopper":
            product_pin = "10670022"
        elif printerName == "wrigley":
            product_pin = "12040620"
        keyboard.__setitem__('displayText', product_pin)
        keyboard.__setitem__('inputText', product_pin)
        doneButton = spice.wait_for(MenuAppWorkflowObjectIds.view_service_sign_in_button).mouse_click()

    def goto_menu_tools_service_systemConfiguration(self,spice,cdm,udw):
        self.goto_menu_tools_service(spice,cdm,udw)
        if self.product_family == 'enterprise':
            SystemConfigBtn = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_system_configuration_alt)
        else:
            SystemConfigBtn = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_system_configuration)
        assert SystemConfigBtn,"System Configuration Button not found"
        SystemConfigBtn.mouse_click()

    def goto_systemconfiguration_servicemenu(self, spice):
        if self.product_family == 'enterprise':
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_system_configuration_alt)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_system_configuration)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_system_configuration)

    def get_serialNumber_SystemConfigMenu(self, spice):
        return spice.wait_for("#SerialNumberTextField")["displayText"]

    def get_current_serviceID_SystemConfigMenu(self, spice):
        return spice.wait_for("#ServiceIDTextField")["displayText"]

    def get_serviceID_SystemConfigMenu(self, spice):
        return spice.wait_for("#ServiceIDTextField")["displayText"]

    def get_ethernetMacaddress_SystemConfigMenu(self, spice):
        return spice.wait_for("#ethernetMacaddressTextField")["displayText"]

    def get_wirelessMacAddress_SystemConfigMenu(self, spice):
        return spice.wait_for("#wirelessMacaddressTextField")['displayText']

    def get_SystemConfigMenu_View(self, spice):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_system_configuration)

    def get_SystemConfigMenu_View(self, spice):
        return MenuAppWorkflowObjectIds.view_system_configuration

    def get_bootModeCurrentView(self, spice):
        return "#BootMode"

    def get_bootModeButton(self, spice):
        return spice.wait_for("#setBootModeToUserModeMenuMenuButton")

    def get_coldResetPaperCombobox(self, spice):
        return spice.wait_for("#coldResetMediaSizeMenuCombobox")

    def get_RestoreAllFactoryResets_BackButton_View(self):
        return "#RestoreAllDataReset"

    def get_UserSettingsReset_BackButton_View(self):
        return "#UserSettingsReset"

    def get_UserDataReset_BackButton_View(self):
        return "#UserDataReset"

    def RepairModeView(self):
        return "#serviceResetsMenuList"

    def get_service_menu_view(self):
        return MenuAppWorkflowObjectIds.view_service

    def get_Service_Reset_MenuList_View(self):
        return "#serviceResetsMenuList"

    def set_serialNumber(self, spice, NEW_SN):
        self.menu_navigation(spice, screen_id= MenuAppWorkflowObjectIds.view_system_configuration, menu_item_id= "#SerialNumberTextField", scrollbar_objectname= MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)
        assert spice.wait_for("#spiceKeyboardView")

        keyboardView = spice.wait_for("#SerialNumberTextField")
        keyboardView.__setitem__('displayText', NEW_SN)
        spice.query_item("#enterKey1").mouse_click() #click ok button

    def set_serialNumber_SystemConfigMenu(self, spice, NEW_SN):
        self.set_serialNumber(spice,NEW_SN)
        SNConfirmationButton = spice.wait_for("#FooterViewRight")
        SNConfirmationButton.mouse_click()

    def set_wrong_serialNumber_SystemConfigMenu(self, spice, NEW_SN,net):
        self.set_serialNumber(spice,NEW_SN)
        assert spice.wait_for("#textColumn #titleSmallItem")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid serial number entry message")
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()
        return spice.wait_for("#SerialNumberTextField #TextInputBox")["text"]

    def updatewrong_serialNumber_SystemConfigMenu(self, spice,UPDATE_SN,net):
        self.set_serialNumber(spice,UPDATE_SN)
        assert spice.wait_for("#textColumn #titleSmallItem")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful serial number message")
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()
        return spice.wait_for("#SerialNumberTextField #TextInputBox")["text"]

    def set_service_ID(self, spice, SERVICE_ID):
        spice.query_item("#ServiceIDTextField").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At Service Id Edit Menu")
        keyboardView = spice.wait_for("#ServiceIDTextField")
        keyboardView.__setitem__('displayText', SERVICE_ID)
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

    def set_serviceID_SystemConfigMenu(self, spice, SERVICE_ID):
        self.set_service_ID(spice,SERVICE_ID)
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()

    def set_wrong_serviceID_SystemConfigMenu(self, spice, SERVICE_ID,net):
        self.set_service_ID(spice,SERVICE_ID)
        assert spice.wait_for("#textColumn #titleSmallItem")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid service id entry message")
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()
        return spice.wait_for("#ServiceIDTextField #TextInputBox")["text"]

    def update_serviceID_SystemConfigMenu(self, spice,UPDATED_SID,net):
        self.set_service_ID(spice,UPDATED_SID)
        assert spice.wait_for("#textColumn #titleSmallItem")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful service id message")
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()
        return spice.wait_for("#ServiceIDTextField #TextInputBox")["text"]

    def update_new_serviceID_SystemConfigMenu(self, spice,new_serice_id,net):
        self.set_service_ID(spice,new_serice_id)
        assert spice.wait_for("#textColumn #titleSmallItem")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationFailedText", "en")),"Operation failed message is not visible"
        logging.info("Validating Operation failed service id message")
        SIConfirmationButton = spice.wait_for("#FooterViewRight")
        SIConfirmationButton.mouse_click()

    def goto_menu_tools_servicemenu_systemconfiguration_switchbootmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        bootModeButtonRow = "#setBootModeToUserModeMenuSettingsButton"
        self.menu_navigation(spice, screen_id = MenuAppWorkflowObjectIds.view_system_configuration, menu_item_id = bootModeButtonRow, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)
        bootModeButton = "#setBootModeToUserModeMenuMenuButton"
        spice.wait_for(bootModeButton).mouse_click()

        assert spice.wait_for("#SpiceView")
        logging.info("At Switch Boot Mode Screen")

    def goto_menu_settings_supplies(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_menuSettings,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Supply Settings Screen")

    def goto_menu_settings_network_proxy(self, spice):
        self.goto_menu_settings_network(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_menu_network,
                             MenuAppWorkflowObjectIds.menu_button_network_proxy,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_networkpage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_network_proxy)
        logging.info("At proxy network Screen")

    def goto_supplies_settings(self, spice):
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_menuSettings,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Supply Settings Screen")

    def goto_menu_settings_supplies_verylowbehavior(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_verylow)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies_verylow)
        logging.info("At Very Low Behavior Supply Settings Screen")

    def goto_supplies_settings_blackverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_black_verylow).mouse_click()
        logging.info("At Very Low Behavior - Black Supply Settings Screen")

    def goto_supplies_settings_colorverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_color_verylow).mouse_click()
        logging.info("At Very Low Behavior - Color Supply Settings Screen")

    def goto_menu_settings_supplies_lowwarningthreshold(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_low,
                             scrollbar_objectname=MenuAppWorkflowObjectIds.view_settings_supplies + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies_low)
        logging.info("At Low Warning Thresholds Supply Settings Screen")

    def goto_menu_settings_supplies_storesupplyusagedata(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_storedatausage,
                             select_option=False,
                             scrollbar_objectname=MenuAppWorkflowObjectIds.view_settings_supplies + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Store Supply Usage Data Supply Settings Screen")

    def goto_menu_settings_supplies_authorizedhpcartridgepolicy(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_supplypolicy_setting,
                             select_option=False,
                             scrollbar_objectname=MenuAppWorkflowObjectIds.view_settings_supplies + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Authorized HP Cartridge Policy Supply Settings Screen")

    def goto_menu_settings_supplies_cartridgeprotection(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_antitheft,
                             scrollbar_objectname=MenuAppWorkflowObjectIds.view_settings_supplies + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Cartridge Protection Supply Settings Screen")

    def goto_menu_tools_servicemenu(self, spice, udw):
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        self.product_family = self.configuration.familyname
        logging.info(f'printerName-----: {printerName}')

        self.goto_menu_tools(spice)
        time.sleep(1)
        if printerName == "marconi/marconi" or printerName == "marconi/marconihipdl":
            # scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_menutoolspage)
            # scrollbar.__setitem__("position",0.26)
            logging.info('Marconi product')
        else:
            self.workflow_common_operations.scroll_position(
                MenuAppWorkflowObjectIds.view_menuTools,
                MenuAppWorkflowObjectIds.menu_button_service ,
                MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,
                MenuAppWorkflowObjectIds.tools_column_name ,
                MenuAppWorkflowObjectIds.tools_Content_Item)

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        keyboard = spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard

        json_path = "/code/dunetuf/dunetuf/ui/uioperations/WorkflowOperations/ServicePins.json"
        with open(json_path) as json_file:
            service_pins = json.load(json_file)

        if printerName == "marconi/marconi" or printerName == "marconi/marconihipdl":
            product_pin = service_pins.get(printerName.strip(), "9100")
        else:
            product_pin = service_pins.get(printerName.strip(), "12345678")

        keyboard.__setitem__('displayText', product_pin) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', product_pin)

        time.sleep(2)

        doneButton = spice.wait_for(MenuAppWorkflowObjectIds.view_service_sign_in_button)
        doneButton.mouse_click()

        time.sleep(5)

        #In service menu now.
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service)
        logging.info("At Service Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_dynamicservicetests(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            self.workflow_common_operations.goto_item_navigation(
                MenuAppWorkflowObjectIds.menu_button_service_servicetests_alt,
                MenuAppWorkflowObjectIds.view_service)
        else:
            self.workflow_common_operations.goto_item_navigation(
                MenuAppWorkflowObjectIds.menu_button_service_servicetests,
                MenuAppWorkflowObjectIds.view_service)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests)
        #service_tests = spice.wait_for("#dynamicServiceTestsMenuSettingsTextImage")
        #service_tests.mouse_click()
        #logging.info("At Tools -> Service -> Service Tests Screen")

    def goto_menu_tools_servicemenu_serviceresets(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        #verify service resets screen
        if self.product_family == 'enterprise':
            service_resets = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets_alt)
        else:
            service_resets = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets)
        service_resets.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_reset)

    # Open Secure Restore to Factory Defaults Screen
    def goto_menu_tools_servicemenu_serviceresets_securerestore(self, spice, udw, menu_present = False):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        if(menu_present):
            #verify secure restore Screen
            self.menu_navigation(spice,
                        MenuAppWorkflowObjectIds.view_service_reset,
                        MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securerestore,
                        scrollbar_objectname=MenuAppWorkflowObjectIds.view_service_reset + "ScrollBar")
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securerestore)
        else:
            logging.info("No Menu Item")

    # Select Erase Paths according to Capabilities
    def goto_menu_tools_servicemenu_serviceresets_securerestore_option(self, spice, udw, option):
        logging.info("The option is::")
        logging.info(option)
        self.goto_menu_tools_servicemenu_serviceresets_securerestore(spice, udw, True)
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()

        # Going to Warning Screen by selecting the erase method
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securerestore_warning)

        # Going to Progress Screen by pressing "Confirm" in warning
        confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securerestore_warning_no)
        confirm_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securerestore)

    # Open Secure Job Erase Screen
    def goto_menu_tools_servicemenu_serviceresets_securejoberase(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        #verify secure restore Screen
        self.menu_navigation(spice,
                    MenuAppWorkflowObjectIds.view_service_reset,
                    MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securejoberase,
                    scrollbar_objectname=MenuAppWorkflowObjectIds.view_service_reset + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securejoberase)

    # Select Erase Paths according to Capabilities
    def goto_menu_tools_servicemenu_serviceresets_securejoberase_option(self, spice, udw, option):
        logging.info("The option is::")
        logging.info(option)
        self.goto_menu_tools_servicemenu_serviceresets_securejoberase(spice, udw)
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()

        # Going to Warning Screen by selecting the erase method
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securejoberase_warning)

        # Going to Progress Screen by pressing "Confirm" in warning
        confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securejoberase_warning_no)
        confirm_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securejoberase)

    # Open Secure File Erase Mode Screen
    def goto_menu_tools_servicemenu_serviceresets_securefileerasemode(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        #verify secure file erase Screen
        self.menu_navigation(spice,
                     MenuAppWorkflowObjectIds.view_service_reset,
                     MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securefileerasemode,
                     scrollbar_objectname=MenuAppWorkflowObjectIds.view_service_reset + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securefileerasemode)

    #click selected option
    def goto_menu_tools_servicemenu_serviceresets_securefileerasemode_option(self, spice, udw, option):
        logging.info("The option in file::")
        logging.info(option)
        self.goto_menu_tools_servicemenu_serviceresets_securefileerasemode(spice, udw)
        optionButton = spice.wait_for(option)
        optionButton.mouse_click()
        #verify secure file erase Screen
        # self.menu_navigation(spice,
        #              MenuAppWorkflowObjectIds.view_service_serviceresets_securefileerasemode,
        #              option,
        #              scrollbar_objectname=MenuAppWorkflowObjectIds.view_service_serviceresets_securefileerasemode + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_reset)



    # <-Secure File Erase Buttons->
    # menu_button_service_serviceresets_securefileerasemode = "#secureFileEraseWF"

    # menu_button_service_serviceresets_securefileerasemode_nonSecureFast     = "#nonSecureFastEraseRadio"
    # menu_button_service_serviceresets_securefileerasemode_securefast        = "#secureFastEraseRadio"
    # menu_button_service_serviceresets_securefileerasemode_securesanitize    = "#sanitizeEraseRadio"
    # menu_button_service_serviceresets_securefileerasemode_cryptographic     = "#cryptographicEraseRadio"
    # scroll = serviceResetsMenuListScrollBar
    # <-Secure Restore views->
    # view_service_serviceresets = "#serviceResetsMenuList"
    # view_service_serviceresets_securerestore = "#SecureRestoreToFactoryDefaultsView"
    # view_service_serviceresets_securerestore_warning = "#secureResetWarningView"
    # view_service_serviceresets_securerestore_progress = "#secureResetProgressView"

    #     menu_button_service_serviceresets = "#serviceResetsSettingsButton"
    # # <- Secure Restore Buttons ->
    # secureRestoreSettingsTextImage
    # menu_button_service_serviceresets_securerestore = "#secureRestoreSettingsTextImage"
    # # Option Buttons
    # menu_button_service_serviceresets_securerestore_nonSecure = "nonSecureFastEraseBranch"
    # menu_button_service_serviceresets_securerestore_secure = "secureFastEraseBranch"
    # menu_button_service_serviceresets_securerestore_sanitizing = "sanitizeEraseBranch"
    # menu_button_service_serviceresets_securerestore_crypto = "cryptographicEraseBranch"
    # # Confirm/Cancel Buttons
    # menu_button_service_serviceresets_securerestore_warning_yes = "confirmButton"
    # menu_button_service_serviceresets_securerestore_warning_no = "cancelButton"

    # # <-Secure File Erase Buttons->
    # menu_button_service_serviceresets_securefile = "#secureFileEraseWF"

    def goto_menu_tools_servicemenu_serviceresets_securerestore_nonsecure_erase_warning(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_securerestore(spice, udw)
        #verify non-secure path
        non_secure_erase = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securerestore_nonSecure)
        non_secure_erase.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securerestore_warning)

    def goto_menu_tools_servicemenu_serviceresets_securerestore_nonsecure_erase_warning_progress(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_securerestore_nonsecure_erase_warning(spice, udw)
        #verify non-secure path
        confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_serviceresets_securerestore_warning_yes)
        confirm_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_serviceresets_securerestore_progress)

    def goto_service_test(self,spice):
        service_tests = spice.wait_for("#dynamicServiceTestsMenuSettingsTextImage")
        service_tests.mouse_click()

    def goto_service_backButton(self,spice):
        service_tests = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton2)
        service_tests.mouse_click()

    def goto_menu_tools_servicemenu_servicetests(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            self.menu_navigation(spice,
                                MenuAppWorkflowObjectIds.view_service,
                                MenuAppWorkflowObjectIds.menu_button_service_servicetests_alt,
                                scrollbar_objectname=MenuAppWorkflowObjectIds.view_service + "ScrollBar")
        else:
            self.menu_navigation(spice,
                                 MenuAppWorkflowObjectIds.view_service,
                                 MenuAppWorkflowObjectIds.menu_button_service_servicetests,
                                 scrollbar_objectname=MenuAppWorkflowObjectIds.view_service + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests)
        logging.info("At Tools -> Service -> Service Tests Screen")

    def goto_servicetests_servicemenu(self, spice):
        if self.product_family == 'enterprise':
            self.menu_navigation(spice,
                                 MenuAppWorkflowObjectIds.view_service,
                                 MenuAppWorkflowObjectIds.menu_button_service_servicetests_alt,
                                 scrollbar_objectname=MenuAppWorkflowObjectIds.view_service + "ScrollBar")
        else:
            self.menu_navigation(spice,
                                 MenuAppWorkflowObjectIds.view_service,
                                 MenuAppWorkflowObjectIds.menu_button_service_servicetests,
                                 scrollbar_objectname=MenuAppWorkflowObjectIds.view_service + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests)
        logging.info("At Tools -> Service -> Service Tests Screen")

    def goto_document(self, spice):
        """
        Go to Copy Home by click Copy item on Menu Copy Screen
        """
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_copyScreen)

    def wait_for_menu_quickSets_screen(self, spice):
        spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    #Because the display time of loading screen is too short, the method of direct click is adopted
    def goto_menu_quickSets_and_check_loading_screen(self, spice, net, quickset_type=None):
        #excepted_str = spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        self.goto_menu_quickSets(spice, quickset_type)

    def goto_menu_quickSets(self, spice, quickset_type=None):
        """
        Flow -> Home -> Menu -> Quickset item -> Sepecific quickset
        quickset_type:
        1. copy -> Copy
        2. scanToEmail -> Scan to Email
        3. scanToFolder -> Network Folder
        4. scanToSharePoint -> SharePoint
        5. scanToUSB -> Scan to USB
        """
        signed_in = False
        self.goto_menu(spice)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.quick_set_button)
        quickset_button = spice.wait_for(MenuAppWorkflowObjectIds.quick_set_button)
        quickset_button_locked = quickset_button["locked"] == True
        time.sleep(1)
        spice.query_item(MenuAppWorkflowObjectIds.quick_set_button + " SpiceText").mouse_click()
        time.sleep(2)
        if quickset_button_locked:
            spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"]
            self.perform_signIn(spice)
            spice.wait_until(lambda: spice.check_item(MenuAppWorkflowObjectIds.view_toast_window) == None, 20)
            signed_in = True
        if quickset_button_locked:
            spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"]
            self.perform_signIn(spice)
            spice.wait_until(lambda: spice.check_item(MenuAppWorkflowObjectIds.view_toast_window) == None, 20)
            signed_in = True
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except Exception as e:
            logging.info("At Expected Menu")
        else:
            spice.homeMenuUI().perform_signIn(spice)            
        finally:
            logging.info("At Expected Menu")
            time.sleep(1)
        try:
            if quickset_type:
                spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)
                if quickset_type == 'scanToSharePoint':
                    self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)
                    time.sleep(1)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()
                elif quickset_type == 'copy':
                    quickset_type = 'copyList'
                    time.sleep(3)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()
                    time.sleep(3)
                else:
                    self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)
                    time.sleep(1)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()


            else:
                assert spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
        except Exception:
            raise Exception(f"Failed to find item for quickset type: <{quickset_type}>")
        return signed_in
        return signed_in

    def select_copy_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        Args: start_option: QuickSetStartOption.user_presses_start/QuickSetStartOption.start_automatically
        '''

        logging.info("Select quickset by quickset name")
        #Currenlt only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #need to update listview id when DUNE-72516 is fixed.
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(quickset_name + " MouseArea")
        quickset_item.mouse_click()
        time.sleep(2)

        if start_option == QuickSetStartOption.user_presses_start:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_copyScreen)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    def select_network_folder_quickset_from_menu_quickset(self, spice, quickset_name, ana_sign_in=False, start_option=QuickSetStartOption.user_presses_start):
        '''
        This is helper method to select network folder quickset
        UI flow Select QuicksetList view-> click on any quickset
        Args: start_option: QuickSetStartOption.user_presses_start/QuickSetStartOption.start_automatically
        '''

        logging.info("Select quickset by quickset name")
        #Currently only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(quickset_name + " MouseArea")
        quickset_item.mouse_click()
        time.sleep(2)

        if ana_sign_in == False:
            if start_option == QuickSetStartOption.user_presses_start:
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_folder_screen)
            else:
                assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    def select_scan_to_usb_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start):
        '''
        This is helper method to select scan to usb quickset
        UI flow Select QuicksetList view-> click on any quickset
        Args: start_option: QuickSetStartOption.user_presses_start/QuickSetStartOption.start_automatically
        '''
        logging.info("Select quickset by quickset name")
        #Currenlt only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(quickset_name + " MouseArea")
        quickset_item.mouse_click()
        time.sleep(2)

        if start_option == QuickSetStartOption.user_presses_start:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_scan_to_usb)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    def goto_menu_info_printer(self, spice):
        # navigate to the menu / info screen
        self.goto_menu_info(spice)

        #Click on Printer tab
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_Info_printer)
        current_button.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_printer)

        logging.info("At printer information Tab")

    def goto_menu_info_connectivity(self, spice):
        # navigate to the menu / info screen
        self.goto_menu_info(spice)

        #Click on connectivity tab
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_Info_connectivity)
        current_button.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_connectivity)

        logging.info("At Connectivity information Tab")

    def goto_menu_tools_servicemenu_connectivitymenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.workflow_common_operations.scroll_position(screenid = '#nativeStackView' , element_id = MenuAppWorkflowObjectIds.menu_button_service_connectivity_button ,
                scrollbar_= MenuAppWorkflowObjectIds.scrollbar_serviceMenu, columnname ='#panelsStack' , listItem =  MenuAppWorkflowObjectIds.view_service)
        spice.query_item("#connectivityMenuSettingsButton").mouse_click()
        assert spice.wait_for("#connectivityMenuViewlist1")
        logging.info("At Connectivity Screen")

    def goto_connectivitydiagnostics_menu(self, spice):
        spice.wait_for('#wifiDiagnosticButton').mouse_click()

    def get_connectivitydiagnostics_wifidisabled_ethernetenabled_message(self, spice):
        return spice.wait_for('#constraintDescription #contentItem')['text']

    def goto_menu_info_printer_card(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_info_printer(spice)

        #Click on Printer Information
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_Info_printer_card + " " + MenuAppWorkflowObjectIds.text_view_object)
        current_button.mouse_click()

        #Printer Information card expanded
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_printercard)["visible"]
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(0.4, MenuAppWorkflowObjectIds.scrollbar_menuprinterinfo)

        logging.info("At printer information card Tab")

    def goto_menu_info_license_card(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_info_printer(spice)

        #Click on Printer Information
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_Info_licenses_card + " " + MenuAppWorkflowObjectIds.text_view_object)
        current_button.mouse_click()

        #Printer Information card expanded
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_licensecard)["visible"]
        time.sleep(5)

        logging.info("At printer information card Tab")

    def goto_menu_info_license_card_install_select_file(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_info_license_card(spice)

        #Click on Install
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_Info_licenses_card_install + " " + MenuAppWorkflowObjectIds.text_view_object)
        current_button.mouse_click()

        #Wait for file view
        assert spice.wait_for("#fileView")["visible"]
        #Click on the file
        file_button = spice.wait_for("#fileCard")
        file_button.mouse_click()
        time.sleep(5)

        #Wait for confirmation screen
        assert spice.wait_for("#licenseConfirmationModal")["visible"]
        #Accept Confirmation
        assert spice.wait_for("#continueButton")["visible"]
        continue_button = spice.wait_for("#continueButton")
        continue_button.mouse_click()

        # continue_button.mouse_click()
        time.sleep(5)

    # Menu shortcuts
    def goto_menu_shortcuts(self,spice):
        self.goto_menu(spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_shortcuts , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item ,  MenuAppWorkflowObjectIds.utilities_section_bottom_border)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_menulistLandingpage + " " +  MenuAppWorkflowObjectIds.menu_button_shortcuts)["activeFocus"] == False

    def goto_menu_tools_servicemenu_systemconfiguration_serviceid(self, spice, udw):
        '''
        This is helper method for UI Navigation to Menu -> Tools -> Service -->
        System configuration and verify service ID field is present
        '''

        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)

        spice.wait_for("#ServiceIDTextField")
        logging.info("At Service ID View")
        time.sleep(1)

    def goto_menu_tools_servicemenu_systemconfiguration_serialnumber(self, spice, udw):
        '''
        This is helper method for UI Navigation to Menu -> Tools -> Service -->
        System configuration and verify service ID field is present
        '''

        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)

        spice.wait_for("#SerialNumberTextField")
        logging.info("At Serial Number View")
        time.sleep(1)

    def select_scan_to_email_quickset_from_menu_quickset(self, spice, cdm, udw, quickset_name, start_option=QuickSetStartOption.user_presses_start, profile_name=None):
        '''
        This is helper method to select scan to email quickset
        UI flow Select QuicksetList view-> click on any quickset
        Args: start_option: QuickSetStartOption.user_presses_start/QuickSetStartOption.start_automatically
        '''
        logging.info("Select quickset by quickset name")
        #Currently only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(f"#{quickset_name}" + " MouseArea")
        #SpiceView")
        quickset_item.mouse_click()
        time.sleep(2)

        if not profile_name is None:
            email = Email(cdm, udw)
            server_id = email.get_email_profile_id(profile_name)
            profile_name_locator = MenuAppWorkflowObjectIds.button_email_smtp_profile + server_id
            profile_button = spice.query_item(profile_name_locator)
            profile_button.mouse_click()
            logging.info("Successfully selected email profile")

        if start_option == QuickSetStartOption.user_presses_start:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_scan_to_email, timeout = 20)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    def select_sharepoint_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start, pin=None):
        '''
        This is helper method to select sharepoint quickset
        UI flow Select QuicksetList view-> click on any quickset
        Args: start_option: QuickSetStartOption.user_presses_start/QuickSetStartOption.start_automatically
        '''

        logging.info("Select quickset by quickset name")
        #Currently only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(f"#{quickset_name} MouseArea")
        quickset_item.mouse_click()
        time.sleep(2)

        if not pin is None:
            logging.info("Enter pin code")
            pin_required_view = spice.wait_for(SharePointAppWorkflowObjectIds.view_scan_sharepoint_pin_protected)
            spice.wait_until(lambda: pin_required_view["visible"] == True)
            pin_text_field = spice.wait_for(SharePointAppWorkflowObjectIds.text_secure_pin_enter_password)
            pin_text_field.mouse_click()
            pin_text_field.__setitem__('displayText', pin)
            spice.query_item(SharePointAppWorkflowObjectIds.button_keyboard_ok).mouse_click()
            confirm_btn = spice.wait_for(SharePointAppWorkflowObjectIds.scan_sharepoint_pin_protected_confirm_button)
            spice.validate_button(confirm_btn)
            confirm_btn.mouse_click()

        if start_option == QuickSetStartOption.user_presses_start:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_sharepoint_screen)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)

    def check_spec_on_quicksets_home_screen(self, spice, net, quickset_name):
        """
        Check spec on quicksets_home_screen when entered quicksets shortcuts from menu app
        @param spice:
        @param net:
        @param quickset_name:
        """
        # Note: Workflow changed, Quickset Home screen is different from ProSelect UI.
        # logging.info("check the string on current screen")
        # spice.common_operations.verify_string(net, "cQuickSetsAppHeading", "#QuickSetsAppList")
        # spice.common_operations.verify_string(net, "cScan", "#Scan")
        # actual_quickset_name = spice.common_operations.get_actual_str(f"#{quickset_name}")
        # logging.info(f"Actual quickset name : {actual_quickset_name}")
        # assert actual_quickset_name == quickset_name
        # logging.info("verify the back button existed")
        # spice.wait_for("#BackButton", 1)
        pass

    def select_onetouch_quickset_from_menu_quickset(self, spice, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''

        logging.info("Select quickset by quickset name")
        #Currenlt only work fine when exist less than 3 quickset, since base function goto_item does not apply in quickset view list
        #need to update listview id when DUNE-72516 is fixed.
        #self.spice.common_operations.goto_item(quickset_name, listview id, select_option=True)
        quickset_item = spice.wait_for(quickset_name + " MouseArea")
        spice.validate_button(quickset_item)
        quickset_item.mouse_click()
        time.sleep(2)

    def scroll_to_list_item(self, spice, listName, rowName, scrollbarName):
        ops = spice.basic_common_operations
        scroll_pos = 0
        scroll_delta = 0.1
        ops.scroll_to_position_vertical(scroll_pos, scrollbarName)
        while scroll_pos < 1:
            if ops.validateListObjectVisibility(listName, rowName, "", 1):
                break
            scroll_pos += scroll_delta
            ops.scroll_to_position_vertical(scroll_pos, scrollbarName)
            time.sleep(0.1)

    def goto_menu_settings_general_quietmode(self, spice, schedule_supported=False):
        """
        Navigates to Menu App --> Settings --> General --> Quiet Mode (in view)
        @param spice:
        """
        self.goto_menu_settings_general(spice)
        # Scroll "Quiet Mode" into view
        if schedule_supported:
            self.scroll_to_list_item(
                spice,
                MenuAppWorkflowObjectIds.view_generalSettings,
                MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_menuitem,
                MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
            # When Quiet Mode Schedule is supported, we first need to enter the
            # Quiet Mode Schedule screen, and then click on the toggle.
            quietModeMenuItem = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_menuitem)
            quietModeMenuItem.mouse_click()
        else:
            self.scroll_to_list_item(
                spice,
                MenuAppWorkflowObjectIds.view_generalSettings,
                MenuAppWorkflowObjectIds.menu_button_settings_general_quietmode,
                MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)

    def change_settings_general_quietmode(self, spice, enable_option=True, schedule_supported=False):
        """
        Helper method to enable/disable quiet mode
        UI Should be in Menu App --> Settings --> General and enable/disable Quiet Mode
        @param spice:
        @param enable_option: True to enable Quiet mode False to Disable
        @param schedule_supported: True if schedule supported False if not supported (Quiet Mode is a menu item)
        """
        if schedule_supported:
            quiet_mode_toggle_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_quietmode)
        else:
            quiet_mode_toggle_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmode)
        if(quiet_mode_toggle_switch["checked"] != enable_option):
            quiet_mode_toggle_switch.mouse_click()
            time.sleep(1)
            assert quiet_mode_toggle_switch["checked"] == enable_option, "Quiet mode Enable/Disbale failed"

    def change_settings_general_quietmode_schedule(self, spice, enable_option=True):
        """
        Helper method to enable/disable quiet mode
        UI Should be in Menu App --> Settings --> General and enable/disable Quiet Mode
        @param spice:
        @param enable_option: True to enable Quiet mode False to Disable
        """
        quiet_mode_toggle_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_schedule)
        if(quiet_mode_toggle_switch["checked"] != enable_option):
            quiet_mode_toggle_switch.mouse_click()
            time.sleep(1)
            assert quiet_mode_toggle_switch["checked"] == enable_option, "Quiet Mode Schedule Enable/Disbale failed"

    def verify_settings_general_quietmode(self, spice, enabledOption, schedule_supported=False):
        """
        Helper method to verify the enabled/disabled state of Quiet Mode
        UI Should be in Menu App --> Settings --> General and enable/disable Quiet Mode
        @param spice:
        @param enabledOption: True to verify enabled state and False to verify Disabled state
        @param schedule_supported: True if schedule supported False if not supported (Quiet Mode is a menu item)
        """
        if schedule_supported:
            quiet_mode_toggle_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_quietmode)
        else:
            quiet_mode_toggle_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmode)
        assert quiet_mode_toggle_switch["checked"] == enabledOption, "Quiet mode value is not as expected in UI"

    def goto_menu_help_howtovideos(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)
        #self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp, MenuAppWorkflowObjectIds.menu_button_help_howtovideos, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_howtovideos)
        logging.info("At how to videos screen")

    def goto_menu_help_product_tour(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuHelp_for_scroll_position, MenuAppWorkflowObjectIds.menu_button_help_producttour , MenuAppWorkflowObjectIds.scrollbar_help ,MenuAppWorkflowObjectIds.help_colum_name , MenuAppWorkflowObjectIds.help_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_producttour + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_producttour)
        logging.info("At product tour screen")

    def goto_menu_help_workingsmarttips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuHelp_for_scroll_position, MenuAppWorkflowObjectIds.menu_button_help_workingsmarttips , MenuAppWorkflowObjectIds.scrollbar_help ,MenuAppWorkflowObjectIds.help_colum_name , MenuAppWorkflowObjectIds.help_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_workingsmarttips)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips)
        logging.info("At working smart tips screen")

    def goto_menu_help_digitalofficetips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp, MenuAppWorkflowObjectIds.menu_button_help_digitalofficetips, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips)
        logging.info("At how to videos screen")

    def goto_menu_help_digitalofficetips_usbprinting(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips, MenuAppWorkflowObjectIds.menu_button_help_digitalOfficeTips_USBPrinting, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_digitalOfficeTips)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips_USBPrinting)
        logging.info("At digital office tips usb printing screen")

    def goto_menu_help_hpenvironmentaltips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp, MenuAppWorkflowObjectIds.menu_button_help_hpenvironmentaltips, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips)
        logging.info("At how to videos screen")

    #goto_menu_help_howtovideos
    def goto_menu_help_howtovideos_loadpaperintray2legal(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray2Legal, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        #Assert the button exists
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray2Legal)
        #Assert that a video plays
        assert spice.wait_for("#Video")
        logging.info("At how to video loadpaperintray2legal")

    def goto_menu_help_howtovideos_clearajaminthedocumentfeeder(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamDocumentFeeder, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamDocumentFeeder)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajaminthedocumentfeeder screen")

    def goto_menu_help_howtovideos_loadpaperintray3legal(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray3Legal, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray3Legal)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadpaperintray3legal screen")

    def goto_menu_help_howtovideos_loadpaperintray3(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray3, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray3)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadpaperintray3 screen")

    def goto_menu_help_howtovideos_clearajamintray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray2, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray2)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajamintray2 screen")

    def goto_menu_help_howtovideos_insertausbdevicejobstorage(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToInsertUSBDeviceStorage, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToInsertUSBDeviceStorage)
        assert spice.wait_for("#Video")
        logging.info("At how to videos insertausbdevicejobstorage screen")

    def goto_menu_help_howtovideos_manualduplexfromtray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToManualDuplexTray1, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToManualDuplexTray1)
        assert spice.wait_for("#Video")
        logging.info("At how to videos manualduplexfromtray1 screen")

    def goto_menu_help_howtovideos_clearajamintray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray1, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray1)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajamintray1 screen")

    def goto_menu_help_howtovideos_connectanextensionphone(self, spice):
        self.goto_menu_help_howtovideos(spice)
        #button takes a moment to load due to capability check for fax
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectExtensionPhone+"[visible=true]")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectExtensionPhone, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectExtensionPhone)
        assert spice.wait_for("#Video")
        logging.info("At how to videos connectanextensionphone screen")

    def goto_menu_help_howtovideos_cleanthescannerglass(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToCleanScannerGlass, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToCleanScannerGlass)
        assert spice.wait_for("#Video")
        logging.info("At how to videos cleanthescannerglass screen")

    def goto_menu_help_howtovideos_insertausbdevicewalkup(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToInsertUSBDeviceWalkUp, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToInsertUSBDeviceWalkUp)
        assert spice.wait_for("#Video")
        logging.info("At how to videos insertausbdevicewalkup screen")

    def goto_menu_help_howtovideos_loadoriginalsonthescannerglass(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadOriginalScannerGlass, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadOriginalScannerGlass)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadoriginalsonthescannerglass screen")

    def goto_menu_help_howtovideos_loadpaperintray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray2, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray2)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadpaperintray2 screen")

    def goto_menu_help_howtovideos_replacethecyancartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceCyanCartridge, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceCyanCartridge)
        assert spice.wait_for("#Video")
        logging.info("At how to videos replacethecyancartridge screen")

    def goto_menu_help_howtovideos_connectafaxcable(self, spice):
        self.goto_menu_help_howtovideos(spice)
        #button takes a moment to load due to capability check for fax
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectFaxCable+"[visible=true]")
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectFaxCable, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToConnectFaxCable)
        assert spice.wait_for("#Video")
        logging.info("At how to videos connectafaxcable screen")

    def goto_menu_help_howtovideos_loadpaperintray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray1, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadPaperTray1)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadpaperintray1 screen")

    def goto_menu_help_howtovideos_manualduplexfromtray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToManualDuplexTray2, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToManualDuplexTray2)
        assert spice.wait_for("#Video")
        logging.info("At how to videos manualduplexfromtray2 screen")

    def goto_menu_help_howtovideos_replacetheyellowcartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceYellowCartridge, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceYellowCartridge)
        assert spice.wait_for("#Video")
        logging.info("At how to videos replacetheyellowcartridge screen")

    def goto_menu_help_howtovideos_replacethemagentacartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceMagentaCartridge, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceMagentaCartridge)
        assert spice.wait_for("#Video")
        logging.info("At how to videos replacethemagentacartridge screen")

    def goto_menu_help_howtovideos_loadoriginalsinthedocumentfeeder(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadOriginalsInTheDocumentFeeder, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToLoadOriginalsInTheDocumentFeeder)
        assert spice.wait_for("#Video")
        logging.info("At how to videos loadoriginalsinthedocumentfeeder screen")

    def goto_menu_help_howtovideos_replacetheblackcartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceBlackCartridge, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToReplaceBlackCartridge)
        assert spice.wait_for("#Video")
        logging.info("At how to videos replacetheblackcartridge screen")

    def goto_menu_help_howtovideos_clearajamintray3(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray3, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamTray3)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajamintray3 screen")

    def goto_menu_help_howtovideos_clearajaminsidetheprinter(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamInsidePrinter, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamInsidePrinter)
        assert spice.wait_for("#Video")
        logging.info("At how to videos learajaminsidetheprinter screen")

    def goto_menu_help_howtovideos_clearajamintheoutputbin(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamOutputBin, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamOutputBin)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajamintheoutputbin screen")

    def goto_menu_help_howtovideos_clearajaminthecartridgearea(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_howtovideos, MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamCartridge, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_howtovideos)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_howtovideos_howToClearJamCartridge)
        assert spice.wait_for("#Video")
        logging.info("At how to videos clearajaminthecartridgearea creen")


    def goto_menu_help_product_tour_play_demo_once(self, spice):
        self.goto_menu_help_product_tour(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_producttour, MenuAppWorkflowObjectIds.menu_button_help_producttour_playDemoOnce, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_producttour)

        logging.info("At product tour screen")
        #checking for animation to complete and go back to the previous screen
        animation = spice.query_item("#ProductTourOverlay")
        while animation != None and animation["running"]:
            time.sleep(1)
            try:
                animation = spice.query_item("#ProductTourOverlay")
            except:
                animation = None
        spice.query_item("#playDemoOnceMenuButton")
        logging.info("Animation Done")

    def goto_menu_help_product_tour_play_demo_repeat(self, spice):
        self.goto_menu_help_product_tour(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_producttour, MenuAppWorkflowObjectIds.menu_button_help_producttour_playDemoRepeat, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_producttour)

        logging.info("At product tour screen")

    def goto_menu_help_hpenvironmentaltips_shutdown(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips, MenuAppWorkflowObjectIds.menu_button_help_hpEnvironmentalTips_Shutdown, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_hpEnvironmentalTips)

        logging.info("At how to videos screen")

    def goto_menu_tools_troubleshooting_more_options(self, spice):
        try:
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options, timeout = 10)
        except:
            self.goto_menu_tools_troubleshooting(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options)
        current_button.mouse_click()
        time.sleep(1)

        logging.info("At Troubleshooting -> More options (...)")

    def launch_printhead_alignment_verification_plot(self, spice):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_align_plot)
        current_button.mouse_click()

    def launch_paper_advance_calibration(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        current_button = spice.wait_for("#calibrationsCardContent", timeout = 10)
        current_button.mouse_click()
        time.sleep(2)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.paper_advance_calibration_button, timeout = 10)
        current_button.mouse_click()
        time.sleep(5)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button, timeout = 10)
        current_button.mouse_click()

    def launch_nozzle_health(self, spice, input_selection_screen=False):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_nozzle_health)
        current_button.mouse_click()
        if input_selection_screen:
            logging.info("Wait for input selection screen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

    def launch_control_print(self, spice):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_control_print)
        current_button.mouse_click()

    def launch_pretreatment_max_saturation(self, spice):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical_without_scrollbar(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_pretreatment_max_saturation)

    def goto_reset_calibrations(self, spice):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical_without_scrollbar(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_reset_calibrations)
        assert spice.wait_for(MenuAppWorkflowObjectIds.reset_calibration_modal_view)

    def goto_menu_help_hpenvironmentaltips_sleep(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips, MenuAppWorkflowObjectIds.menu_button_help_hpEnvironmentalTips_Sleep, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_hpEnvironmentalTips)

        logging.info("At how to videos screen")

    def goto_menu_help_hpenvironmentaltips_recycle(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips, MenuAppWorkflowObjectIds.menu_button_help_hpEnvironmentalTips_Recycle, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_hpEnvironmentalTips)

        logging.info("At how to videos screen")

    def goto_menu_help_hpenvironmentaltips_twosidedcopying(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips, MenuAppWorkflowObjectIds.menu_button_help_hpEnvironmentalTips_TwoSidedCopying, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_hpEnvironmentalTips)

        logging.info("At how to videos screen")

    def goto_menu_help_hpenvironmentaltips_twosidedprinting(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips, MenuAppWorkflowObjectIds.menu_button_help_hpEnvironmentalTips_TwoSidedPrinting, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_hpEnvironmentalTips)

        logging.info("At how to videos screen")

    def goto_menu_help_digitalofficetips_documentscanning(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips, MenuAppWorkflowObjectIds.menu_button_help_digitalOfficeTips_DocumentScanning, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_digitalOfficeTips)

        logging.info("At how to videos screen")

    def goto_menu_help_digitalofficetips_mobileprinting(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips, MenuAppWorkflowObjectIds.menu_button_help_digitalOfficeTips_MobilePrinting, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_digitalOfficeTips)

        logging.info("At how to videos screen")

    def goto_menu_help_workingsmarttips_wifidirect(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips, MenuAppWorkflowObjectIds.menu_button_help_workingSmartTips_WifiDirect, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_workingSmartTips)

        logging.info("At how to videos screen")

    def goto_menu_help_workingsmarttips_idcardcopy(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips, MenuAppWorkflowObjectIds.menu_button_help_workingSmartTips_IdCardCopy, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_workingSmartTips)

        logging.info("At how to videos screen")

    def goto_menu_help_workingsmarttips_twosideddocumentswithfax(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips, MenuAppWorkflowObjectIds.menu_button_help_workingSmartTips_TwoSidedDocumentsWithFaxSettings, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_workingSmartTips)

        logging.info("At how to videos screen")


    def goto_menu_help_workingsmarttips_twosideddocumentswithoutfax(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips, MenuAppWorkflowObjectIds.menu_button_help_workingSmartTips_TwoSidedDocumentsWithoutFaxSettings, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_workingSmartTips)

        logging.info("At how to videos screen")

    def goto_menu_help_workingsmarttips_copycollate(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips, MenuAppWorkflowObjectIds.menu_button_help_workingSmartTips_CopyCollate, scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_help_workingSmartTips)

        logging.info("At how to videos screen")

    def start_media_advance_calibration(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.media_advance)

    def start_full_calibration(self, spice, allowed_calibrations):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.full_calibration)

        # Validate allowed calibrations for the currently loaded media
        for calibration in allowed_calibrations:
            spice.wait_for(calibration)

        # Click on "Continue" button
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.full_calibration_continue_button)
        continue_button.mouse_click()

    def reset_color_calibration(self, spice):
        clc_reset_checkbox = spice.wait_for(MenuAppWorkflowObjectIds.clc_reset_checkbox)
        clc_reset_checkbox.mouse_click()

        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.reset_calibrations_continue_button)
        continue_button.mouse_click()

    def reset_media_advance_calibration(self, spice):
        media_advance_reset_checkbox = spice.wait_for(MenuAppWorkflowObjectIds.media_advance_reset_checkbox)
        media_advance_reset_checkbox.mouse_click()

        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.reset_calibrations_continue_button)
        continue_button.mouse_click()

    def start_calibration(self, spice, calibration):
        align_button = spice.wait_for(calibration + " MouseArea")
        align_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view)
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()

    def select_fax_t30_report_mode_from_troubleshooting_fax(self, spice, fax_t30_report_mode):
        '''
        This is helper method to select fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        troubleshooting_fax_t30_repmode_view = spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode)
        spice.wait_until(lambda:troubleshooting_fax_t30_repmode_view["visible"])
        logging.info(f"Select fax T30 report mode: <{fax_t30_report_mode}>")
        if fax_t30_report_mode == "Never automatically print":
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_never_auto_print)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print after every fax":
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_every_fax)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after sending fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.2, MenuAppWorkflowObjectIds.scrollbar_fax_t30_repmode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_send)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after receiving fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.2, MenuAppWorkflowObjectIds.scrollbar_fax_t30_repmode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_receive)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after problems sending fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_fax_t30_repmode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_send_errors)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after problems receiving fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scrollbar_fax_t30_repmode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_receive_errors)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print after any fax problems":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scrollbar_fax_t30_repmode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_any_fax_errors)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        else:
            raise logging.info(f"{fax_t30_report_mode} is not supported to select")

    def click_save_button_fax_t30_report_mode_view(self, spice):
        '''
        This is helper method to save fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        '''
        button_troubleshooting_fax_faxT30_save = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_faxT30_save)
        spice.wait_until(lambda:button_troubleshooting_fax_faxT30_save["visible"])
        button_troubleshooting_fax_faxT30_save.mouse_click()

    # Added to print  fax t30 trace report
    def click_print_button_fax_t30_report_mode_view(self, spice):
        '''
        This is helper method to save fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        '''
        button_troubleshooting_fax_faxT30_print = spice.wait_for(MenuAppWorkflowObjectIds.button_troubleshooting_fax_faxT30_print)
        spice.wait_until(lambda:button_troubleshooting_fax_faxT30_print["visible"])
        button_troubleshooting_fax_faxT30_print.mouse_click()

    def verify_set_fax_t30_report_mode_successfully(self, spice, fax_t30_report_mode):
        '''
        This is helper method to verify set fax T30 report mode successfully
        UI should be Menu->Tools->Troubleshooting->Fax
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        troubleshooting_fax_view = spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax)
        spice.wait_until(lambda:troubleshooting_fax_view["visible"])

        spice.wait_until(lambda:spice.query_item(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_faxT30 + " SpiceText",1)["visible"])
        current_report_mode = spice.query_item(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_faxT30 + " SpiceText",1)["text"]
        assert fax_t30_report_mode==current_report_mode, "Set fax T30 report mode failed!!!"
# FAX T30 Report Mode
    def verify_set_fax_t30_report_mode_successfully_enterprise(self, spice, fax_t30_report_mode):
        '''
        This is helper method to verify set fax T30 report mode successfully
        UI should be Menu->Tools->Troubleshooting->Fax
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        troubleshooting_fax_view = spice.wait_for(MenuAppWorkflowObjectIds.view_fax)
        spice.wait_until(lambda:troubleshooting_fax_view["visible"])

        spice.wait_until(lambda:spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu + " #TextView",1)["visible"])
        current_report_mode = spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu + " #TextView",1)["text"]
        assert fax_t30_report_mode==current_report_mode, "Set fax T30 report mode failed!!!"

    def select_energy_inactivity_shutdown_value(self,spice, inactivity_shutdown_value):
        '''
        Select an inactivity shutdown value in inactivity shutdown screen.
        Args: inactivity_shutdown_value: inactivity shutdown value
        '''
        logging.info(f"Select energy inactivity shutdown value is <{inactivity_shutdown_value}>")
        item_location = self.inactivity_shutdown_options_dict[inactivity_shutdown_value][1]

        if inactivity_shutdown_value == "3 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)
        elif inactivity_shutdown_value == "4 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)
        elif inactivity_shutdown_value == "5 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)
        elif inactivity_shutdown_value == "6 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.4, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)
        elif inactivity_shutdown_value == "7 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)
        elif inactivity_shutdown_value == "8 Hours":
            self.workflow_common_operations.scroll_to_position_vertical(0.6, MenuAppWorkflowObjectIds.scrollbar_energy_inactivity_shutdown_view)

        time.sleep(2)
        inactivity_shutdown_item = spice.wait_for(item_location)
        inactivity_shutdown_item.mouse_click()

        spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
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
            expected_inactivity_shutdown_value = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, cstring_id)
            logging.info(f'The expect inactivity shutdown value is {expected_inactivity_shutdown_value}')

            item_location = self.inactivity_shutdown_options_dict[item][1]
            current_inactivity_shutdown_value = spice.wait_for(f"{item_location} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view}")["text"]
            logging.info(f'The current inactivity shutdown value is {current_inactivity_shutdown_value}')
            assert current_inactivity_shutdown_value == expected_inactivity_shutdown_value, "Check inactivity shutdown value failed!"

        logging.info('The current inactivity shutdown option list display completely and correctly')

    def verify_set_inactivity_shutdown_option_display_in_ui(self, spice, inactivity_shutdown_value):
            """
            UI Workflow should be: Energy  Settings screen
            Verify set inactivity shutdown option display correctly.
            Args: inactivity_shutdown_value: inactivity shutdown value
            """
            energy_settings_view = spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            spice.wait_until(lambda:energy_settings_view["visible"])

            spice.wait_until(lambda:spice.query_item(f"{MenuAppWorkflowObjectIds.menu_button_inactivity_shutdown_option} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view}")["visible"])
            current_inactivity_shutdown_option = spice.query_item(f"{MenuAppWorkflowObjectIds.menu_button_inactivity_shutdown_option} {MenuAppWorkflowObjectIds.inactivity_shutdown_text_view}")["text"]
            assert inactivity_shutdown_value == current_inactivity_shutdown_option, "Set inactivity shutdown option failed!!!"

    # User needs to be at Troubleshoting Screen
    def goto_printheads_cleaning(self, spice):
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.ph_cleaning + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_printheads)
        logging.info("At Printhead Cleaning Screen")


    def continue_ph_cleaning_selection(self, spice):
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.printheads_cleaning_continue_button)
        continue_button.mouse_click()

    # signout from homescreen
    def signout_from_homescreen(self, spice):
        spice.goto_homescreen()
        try:
            (spice.wait_for("#7db992ba-557a-461c-b941-6023aa8cfa34")["visible"])
        except Exception as e:
            pass
        else:
            if(spice.wait_for("#7db992ba-557a-461c-b941-6023aa8cfa34 SpiceText[visible=true]")["text"] == "Sign Out"):
                spice.signIn.goto_sign_in_app("Sign Out")
        finally:
            logging.info("At Home Screen")


    def check_if_volume_slider_accessible(self,spice):
        self.goto_menu_settings_general_display(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.volume_settings_slider) ,"Volume slider is not accessible"


    def get_default_volume_slider_value(self,spice):
        self.goto_menu_settings_general_display(spice)
        current_value = spice.query_item(MenuAppWorkflowObjectIds.volume_settings_slider)["value"]
        logging.info("Default volume value on Slider: "+str(current_value))
        return current_value

    def set_volume_slider_value(self,spice,set_val):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for(MenuAppWorkflowObjectIds.volume_settings_slider)
        slider.__setitem__('value',set_val)


    def move_cursor_validate_and_get_volume_slider_value(self,spice,cdm_set_value):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for(MenuAppWorkflowObjectIds.volume_settings_slider+" #Slider")

        MOUSE_CLICK_X =  cdm_set_value*self.VOLUME_SLIDER_UNIT_X_VALUE
        slider.mouse_click(MOUSE_CLICK_X,self.MOUSE_CLICK_Y)

        current_value = spice.query_item(MenuAppWorkflowObjectIds.volume_settings_slider)["value"]
        logging.info("Current volume value on Slider: "+str(current_value))
        assert int(current_value) >=0 and int(current_value) <= 100,"Volume value is out of range"
        return int(current_value)

    def check_if_brightness_slider_accessible(self,spice):
        self.goto_menu_settings_general_display(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.display_brightness_settings_slider),"Brightness slider is not accessible"


    def get_default_brightness_slider_value(self,spice):
        self.goto_menu_settings_general_display(spice)
        current_value = spice.query_item(MenuAppWorkflowObjectIds.display_brightness_settings_slider)["value"]
        logging.info("Default brightness value on slider: "+str(current_value))
        return current_value

    def set_brightness_slider_value(self,spice,set_val):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for(MenuAppWorkflowObjectIds.display_brightness_settings_slider)
        slider.__setitem__('value',set_val)

    def get_max_brightness_slider_value(self, spice):
        '''
        UI should be in Menu -> Setting -> General -> Display screen.
        '''
        max_brightness_value = spice.query_item(MenuAppWorkflowObjectIds.display_brightness_settings_slider)["to"]
        logging.info("Max brightness value on slider: "+str(max_brightness_value))
        return max_brightness_value

    def move_cursor_validate_and_get_brightness_slider_value(self,spice,cdm_set_value):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for(MenuAppWorkflowObjectIds.display_brightness_settings_slider+" #Slider")

        MOUSE_CLICK_X = (cdm_set_value-1)*self.DISPLAY_BRIGHTNESS_SLIDER_UNIT_X_VALUE #When brightness value is 1,x coordinate value is 0
        slider.mouse_click(MOUSE_CLICK_X,self.MOUSE_CLICK_Y)

        current_value = spice.query_item(MenuAppWorkflowObjectIds.display_brightness_settings_slider)["value"]
        logging.info("Current brightness Value on Slider: "+str(current_value))
        assert int(current_value) >= 1 and int(current_value) <= 9,"Brightness value is out of range"
        return int(current_value)

    def check_inactivity_timeout_options_visible(self, spice):
        """
        Check timeout options shows in inactivity timeout screen.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_30sec)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_1min)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_2mins)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.inactivity_timeout_5mins)["visible"] == True

    def check_margin_layout_options_visible(self, spice):
        """
        Check layout options shows in margin layout screen.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.margin_layout_clipcontents)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.margin_layout_oversize)["visible"] == True

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

    def check_margin_values_visible(self, spice):
        """
        Check values are shown in margins screen.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        #assert spice.wait_for(MenuAppWorkflowObjectIds.margin_value_0mm)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.margin_value_3mm)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.margin_value_5mm)["visible"] == True

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def get_margin_layout_option_selected(self, spice) -> MenuAppWorkflowObjectIds:
        """
        Get the selected layout option from margin layout screen.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        if spice.wait_for(MenuAppWorkflowObjectIds.margin_layout_clipcontents)["selected"] == True:
            margin_layout_selected = MenuAppWorkflowObjectIds.margin_layout_clipcontents
        elif spice.wait_for(MenuAppWorkflowObjectIds.margin_layout_oversize)["selected"] == True:
            margin_layout_selected = MenuAppWorkflowObjectIds.margin_layout_oversize
        else:
            assert False, "There is no valid margin layout option selected."

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        return margin_layout_selected

    def get_margin_value_selected(self, spice) -> MenuAppWorkflowObjectIds:
        """
        Get the selected layout option from margin layout screen.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        """
        if spice.wait_for(MenuAppWorkflowObjectIds.margin_value_0mm)["selected"] == True:
            margin_value_selected = MenuAppWorkflowObjectIds.margin_value_0mm
        """
        if spice.wait_for(MenuAppWorkflowObjectIds.margin_value_3mm)["selected"] == True:
            margin_value_selected = MenuAppWorkflowObjectIds.margin_value_3mm
        elif spice.wait_for(MenuAppWorkflowObjectIds.margin_value_5mm)["selected"] == True:
            margin_value_selected = MenuAppWorkflowObjectIds.margin_value_5mm
        else:
            assert False, "There is no valid margin value selected."

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        return margin_value_selected

    def verify_selected_inactivity_timeout_value(self, spice, inactivity_value,isEnterPriseProduct=False):
        '''
        This is helper method to verify selected inactivity timeout value
        UI flow Menu > Settings > General > Inactivity Timeout
        Args: inactivity_value: 30/60/120/300
        '''
        inactivityItemObjectName = ""
        # Combobox in small screen (text image branch) can only be verified after closing the popup screen
        if not isEnterPriseProduct:
            try:
                if spice.uisize == "XS":
                    spice.click_backButton()
                else:
                    backButton = spice.wait_for(MenuAppWorkflowObjectIds.view_inactivity_timeout_settings_screen + " " + MenuAppWorkflowObjectIds.button_back)
                    backButton.mouse_click()
            except:
                logging.info('Inactivity timeout settings screen back button not found!')

            inactivityItemObjectName = f"{MenuAppWorkflowObjectIds.menu_button_inactivity_Timeout_option} {MenuAppWorkflowObjectIds.inactivity_timeout_text_view}"
        else:
            keyboard_button = spice.wait_for("#enterKeyPositiveIntegerKeypad")
            keyboard_button.mouse_click()
            inactivityItemObjectName = f"{MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout_enterprise} #SpinBoxTextInput"

        spice.wait_until(lambda: spice.wait_for(inactivityItemObjectName)["visible"])
        selected_value_locator = spice.query_item(inactivityItemObjectName)["text"]
        logging.info("\n Selected value locator'{}':".format(selected_value_locator))

        if selected_value_locator.isdigit():
            selected_value = int(selected_value_locator)
            assert inactivity_value == selected_value, "Selected inactivity timeout value failed!!!"
        elif inactivity_value == 30:
            assert selected_value_locator == '30 Seconds', "Selected inactivity timeout value failed!!!"
        elif inactivity_value == 60:
            assert selected_value_locator == '1 Minute', "Selected inactivity timeout value failed!!!"
        elif inactivity_value == 120:
            assert selected_value_locator == '2 Minutes', "Selected inactivity timeout value failed!!!"
        elif inactivity_value == 300:
            assert selected_value_locator == '5 Minutes', "Selected inactivity timeout value failed!!!"
        else:
            assert False, "invalid inactivity timeout"

        assert spice.query_item(inactivityItemObjectName)["visible"], "Failed to verify selected inactivity timeout value in UI."
        assert spice.query_item(inactivityItemObjectName)["text"], "Failed to verify selected inactivity timeout value in UI."

    def verify_selected_margin_layout_option(self, spice, net, locale, expected_option):
        '''
        This is helper method to verify selected margin layout option
        UI flow Menu > Settings > Print > Margins > Margin Layout
        '''
        margin_layout_strings = { MenuAppWorkflowObjectIds.margin_layout_clipcontents: "cClipContentsByMargins",
                                  MenuAppWorkflowObjectIds.margin_layout_oversize:     "cOversize" }

        margin_layout_selected = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout+" SpiceText[visible=true]")
        assert margin_layout_selected["text"] == str(LocalizationHelper.get_string_translation(net, margin_layout_strings[expected_option], locale))

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        assert spice.wait_for(expected_option)["selected"]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

    def verify_selected_rotation_value(self, spice, net, locale, expected_option):
        '''
        This is helper method to verify selected paper size
        UI flow Menu > Settings > Print > Default Print Options > Paper Options > Rotation
        '''
        rotation_values_string = { MenuAppWorkflowObjectIds.value_Rotation_0: 0,
                                    MenuAppWorkflowObjectIds.value_Rotation_90: 90,
                                    MenuAppWorkflowObjectIds.value_Rotation_180: 180,
                                    MenuAppWorkflowObjectIds.value_Rotation_270: 270}


        rotation_selected = spice.wait_for(MenuAppWorkflowObjectIds.rotationLayout_TextView + " SpiceText")

        assert rotation_selected["text"] == str(rotation_values_string[expected_option])

    def verify_selected_paperSize_value(self, spice, net, locale, expected_option):
        '''
        This is helper method to verify selected paper size
        UI flow Menu > Settings > Print > Default Print Options > Paper Options > Paper Sizes
        '''
        paperSize_values_string = { MenuAppWorkflowObjectIds.value_A0: "A0 (841x1189 mm)",
                                    MenuAppWorkflowObjectIds.value_A1: "A1 (594x841 mm)",
                                    MenuAppWorkflowObjectIds.value_A2: "A2 (420x594 mm)",
                                    MenuAppWorkflowObjectIds.value_A3: "A3 (297x420 mm)",
                                    MenuAppWorkflowObjectIds.value_A4: "A4 (210x297 mm)",
                                    MenuAppWorkflowObjectIds.value_A5: "A5 (148x210 mm)",
                                    MenuAppWorkflowObjectIds.value_A6: "A6 (105x148 mm)"}

        paperSize_selected = spice.wait_for(MenuAppWorkflowObjectIds.comboBox_paperSizeLayout+" SpiceText")

        assert paperSize_selected["text"] == paperSize_values_string[expected_option]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_paperOptions,
                             MenuAppWorkflowObjectIds.comboBox_paperSizeLayout,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.view_paperOptions + "ScrollBar")

        assert spice.wait_for(expected_option)["selected"]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_paperOptions,
                             MenuAppWorkflowObjectIds.comboBox_paperSizeLayout,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.view_paperOptions + "ScrollBar")

    def verify_selected_margin_value(self, spice, net, locale, expected_option, units="metric"):
        '''
        This is helper method to verify selected margin value
        UI flow Menu > Settings > Print > Margins > Margins
        '''
        margin_values_string = { "metric": { MenuAppWorkflowObjectIds.margin_value_0mm: 0,
                                             MenuAppWorkflowObjectIds.margin_value_3mm: 3,
                                             MenuAppWorkflowObjectIds.margin_value_5mm: 5 },
                                "imperial": { MenuAppWorkflowObjectIds.margin_value_0mm: 0,
                                             MenuAppWorkflowObjectIds.margin_value_3mm: 118,
                                             MenuAppWorkflowObjectIds.margin_value_5mm: 197 } }
        margin_values_unit = { "metric":  str(LocalizationHelper.get_string_translation(net, "cUnitOfMeasureMillimeters", locale)),
                               "imperial": "mils" } #String "cUnitOfMeasureMils" is neither defined nor translated yet

        margin_selected = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value+" SpiceText[visible=true]")
        assert margin_selected["text"] == str(LocalizationHelper.get_string_translation(net,
                                                                                        ["cValueUnit",
                                                                                         margin_values_string[units][expected_option],
                                                                                         margin_values_unit[units]],
                                                                                        locale))

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        assert spice.wait_for(expected_option)["selected"]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")


    def check_pageOrder_values(self, spice, net, locale):
        """
        Check values are shown in color mode combo box.
        """
        #Wait for menu title
        current_string = MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder_title + " SpiceText"
        expected_string = str(LocalizationHelper.get_string_translation(net, "cPageOrder", locale))
        spice.wait_until(lambda:spice.wait_for(current_string)["text"] == expected_string, 10)

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_pageOrder_firstPageOnTop)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_pageOrder_lastPageOnTop)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_pageOrder_firstPageOnTop + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cFirstPageOnTop", locale))
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_pageOrder_lastPageOnTop + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cLastPageOnTop", locale))

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def set_pageOrder_to(self, spice, combo_box_option):
        """
        Set page order option to "combo_box_option".
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_pageOrder, combo_box_option, scrollbar_objectname = MenuAppWorkflowObjectIds.view_pageOrder_any_popup_list_scrollbar)

    def verify_selected_pageOrder(self, spice, combo_box, expected_option):
        """
        Verify page order selected is the passed by parameter.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")
        assert spice.wait_for(expected_option)["selected"]
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def check_colormode_values(self, spice, net, locale):
        """
        Check values are shown in color mode combo box.
        """
        expected_string = str(LocalizationHelper.get_string_translation(net, "cColorMode", locale))
        logging.info("Debugging: " + expected_string + " is " + str(spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_colormode_title + " SpiceText")["text"]) + "?")
        spice.wait_until(lambda: spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_colormode_title + " SpiceText")["text"] == expected_string, 5)

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_colormode, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_color)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_grayscale)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_onlyblack)["visible"] == True

        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_color + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cColor", locale))
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_grayscale + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cChromaticModeGrayscale", locale))
        assert spice.wait_for(MenuAppWorkflowObjectIds.combobox_option_onlyblack + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cBlackOnly", locale))

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_colormode, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def set_colormode_to(self, spice, combo_box_option):
        """
        Set color mode option to "combo_box_option".
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_colormode, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_colormode, combo_box_option, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

    def verify_selected_colormode(self, spice, combo_box, expected_option):
        """
        Verify color mode selected is the passed by parameter.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

        assert spice.wait_for(expected_option)["selected"]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def verify_selected_coloroption(self, spice, combo_box, expected_option):
        """
        Verify color option selected is the passed by parameter.
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")

        assert spice.wait_for(expected_option)["selected"]

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, combo_box, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")

    def check_rgbsource_profiles(self, spice, cdm, net, locale):
        """
        Check combo box values are shown and selectable in RGB source profile menu.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_rgbsourceprofile_title + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cRGBSourceProfile", locale))

        rgb_source_profiles_list = {
            MenuAppWorkflowObjectIds.combobox_profile_none :            {  "String" : "cNone",              "CDM" : "native"        },
            MenuAppWorkflowObjectIds.combobox_profile_srgb :            {  "String" : "cRGBColorProfile",   "CDM" : "srgb"          },
            MenuAppWorkflowObjectIds.combobox_profile_adobergb :        {  "String" : "cAdobeRGB",          "CDM" : "adobeRgb"      },
            MenuAppWorkflowObjectIds.combobox_profile_applergb :        {  "String" : "cAppleRGB",          "CDM" : "appleRgb"      },
            MenuAppWorkflowObjectIds.combobox_profile_colormatchrgb :   {  "String" : "cColorMatchRGB",     "CDM" : "colorMatchRgb" }
            #MenuAppWorkflowObjectIds.combobox_profile_prophotorgb :     {  "String" : "cProPhotoRGB",      "CDM" : "proPhotoRgb"   }
        }

        for profile_button, profile_info in rgb_source_profiles_list.items():
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_rgbsourceprofile, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_rgbsourceprofile, profile_button, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_rgbsourceprofile + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, profile_info["String"], locale))
            assert cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)["dest"]["print"]["rgbSourceProfile"] == profile_info["CDM"]

    def set_rgbsourceprofile_to(self, spice, combo_box_option):
        """
        Set RGB Source Profile option to "combo_box_option".
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_rgbsourceprofile, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_rgbsourceprofile, combo_box_option, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

    def check_cmyksource_profiles(self, spice, cdm, net, locale):
        """
        Check combo box values are shown and selectable in CMYK source profile menu.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_cmyksourceprofile_title + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cCMYKSourceProfile", locale))

        # These are just a few of them (not feasable to test them all via UI due to slowness)
        cmyk_source_profiles_list = {
            MenuAppWorkflowObjectIds.combobox_profile_coatedfogra39 :           {  "String" : "cCoatedFOGRA39",           "CDM" : "coatedFogra39"                   },
            MenuAppWorkflowObjectIds.combobox_profile_coatedgracol2006 :        {  "String" : "cCoatedGRACoL",            "CDM" : "coatedGracol2006"                },
            MenuAppWorkflowObjectIds.combobox_profile_uswebuncoated :           {  "String" : "cUSWebUncoated",           "CDM" : "usWebUncoated"                   },
            MenuAppWorkflowObjectIds.combobox_profile_euroscaleuncoated :       {  "String" : "cEuroscaleUncoated",       "CDM" : "euroScaleUncoated"               },
            MenuAppWorkflowObjectIds.combobox_profile_webcoatedswop2006grade3 : {  "String" : "cWebCoatedSWOPGrade3",     "CDM" : "webCoatedSwop2006Grade3Paper"    },
            MenuAppWorkflowObjectIds.combobox_profile_isocoatedv2eci :          {  "String" : "cISOCoated",               "CDM" : "isoCoatedV2Eci"                  },
            MenuAppWorkflowObjectIds.combobox_profile_japanwebcoated :          {  "String" : "cJapanWebCoated",          "CDM" : "japanWebCoated"                  }
        }

        for profile_button, profile_info in cmyk_source_profiles_list.items():
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_cmyksourceprofile, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_cmyksourceprofile, profile_button, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_cmyksourceprofile + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, profile_info["String"], locale))
            assert cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)["dest"]["print"]["cmykSourceProfile"] == profile_info["CDM"]

    def set_cmyksourceprofile_to(self, spice, combo_box_option):
        """
        Set CMYK Source Profile option to "combo_box_option".
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_cmyksourceprofile, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_cmyksourceprofile, combo_box_option, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

    def check_renderingintents(self, spice, cdm, net, locale):
        """
        Check combo box values are shown and selectable in Rendering Intent menu.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_renderingintent_title + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cRenderIntent", locale))

        rendering_intents_list = {
            MenuAppWorkflowObjectIds.combobox_profile_perceptual :           {  "String" : "cPerceptual",           "CDM" : "perceptual"           },
            MenuAppWorkflowObjectIds.combobox_profile_absolutecolorimetric : {  "String" : "cAbsoluteColorimetric", "CDM" : "absoluteColorimetric" },
            MenuAppWorkflowObjectIds.combobox_profile_relativecolorimetric : {  "String" : "cRelativeColorimetric", "CDM" : "relativeColorimetric" },
            MenuAppWorkflowObjectIds.combobox_profile_saturation :           {  "String" : "cSaturation",           "CDM" : "saturation"           }
        }

        for profile_button, profile_info in rendering_intents_list.items():
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_renderingintent, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_renderingintent, profile_button, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_renderingintent + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, profile_info["String"], locale))
            assert cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)["dest"]["print"]["renderIntent"] == profile_info["CDM"]

    def set_renderingintents_to(self, spice, combo_box_option):
        """
        Set Rendering Intent option to "combo_box_option".
        """
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_renderingintent, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_coloroptions_renderingintent, combo_box_option, scrollbar_objectname = MenuAppWorkflowObjectIds.view_coloroptions_any_popup_list_scrollbar)

    def set_blackpointcompensation_to(self, spice, cdm, net, locale, combo_box_option):
        """
        Set Black Point Compensation option to True/False.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_blackpoint_title + " SpiceText[visible=true]")["text"] == str(LocalizationHelper.get_string_translation(net, "cBlackPointCompensation", locale))

        if (bool(spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_blackpoint)["checked"]) != combo_box_option):
            self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_blackpoint, MenuAppWorkflowObjectIds.view_coloroptions)
            time.sleep(1)

        assert bool(eval(cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)["dest"]["print"]["blackPointCompensation"].capitalize())) == combo_box_option

    def set_pantonedigitalcolor_to(self, spice, cdm, net, locale, combo_box_option):
        """
        Set PANTONE® Digital Color option to True/False.
        """
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_pantone_title + " SpiceText[visible=true]")["text"] == "PANTONE® Digital Color" # Hardcoding it as LocalizationHelper does not work with char ®

        if (bool(spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_pantone)["checked"]) != combo_box_option):
            self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_pantone, MenuAppWorkflowObjectIds.view_coloroptions)
            time.sleep(1)

        assert bool(eval(cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)["dest"]["print"]["pantoneEmulation"].capitalize())) == combo_box_option

    # Service package (Tupperware)
    def goto_menu_tools_maintenance_servicepackage_info(self,spice):
        self.goto_menu_tools_maintenance(spice)
        time.sleep(2)
        menu_button_tools_maintenance_servicepackage = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_service_package)
        menu_button_tools_maintenance_servicepackage.mouse_click()
        assert spice.wait_for("#servicePackageInfo")
        logging.info("At service pkg info file")
        time.sleep(1)

    def goto_menu_tools_maintenance_servicepackage_info_install(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_tools_maintenance_servicepackage_info(spice)

        #Click on Install and sign in
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.install_button + " " + MenuAppWorkflowObjectIds.text_view_object)
        current_button.mouse_click()
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("user signed in")

    def goto_menu_tools_maintenance_servicepackage_info_select_file(self, spice, mock_file_name):
        #navigate to the menu /info/printer/servicepackage/install screen
        self.goto_menu_tools_maintenance_servicepackage_info_install(spice)

        #Wait for file view
        assert spice.wait_for("#fileView")["visible"]
        #Click on the file
        file_button = spice.wait_for("#fileCard_"+mock_file_name)
        file_button.mouse_click()
        time.sleep(5)

        #Wait for confirmation screen
        assert spice.wait_for("#tpwConfirmationModal")["visible"]
        #Accept Confirmation
        assert spice.wait_for("#continueButton")["visible"]
        continue_button = spice.wait_for("#continueButton")
        continue_button.mouse_click()

        time.sleep(5)


    #####

    # Firmware Upgrade Submenu
    def goto_menu_tools_maintenance_firmware(self, spice):
        self.goto_menu_tools_maintenance(spice)
        time.sleep(2)
        menu_button_tools_maintenance_firmware = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance_firmware)
        menu_button_tools_maintenance_firmware.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_firmwareVersion)
        logging.info("At Firmware Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_checkforupdate(self, spice):
        spice.homeMenuUI().goto_menu_tools_maintenance_firmware(spice)
        fwupdate_check = spice.wait_for("#fwUpCheckUpdate", 30)
        fwupdate_check.mouse_click()

    def goto_menu_tools_maintenance_firmware_update_available_scroll_yes(self, spice):
        self.goto_menu_tools_maintenance_firmware_checkforupdate(spice)
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(1, MenuAppWorkflowObjectIds.scrollbar_fwupdate_update_available)
        confirm_yes = spice.wait_for("#fwupdateAvailableConfirmYes", 30)
        confirm_yes.mouse_click()
        time.sleep(5)

    def goto_menu_tools_maintenance_firmware_update_available_scroll_no(self, spice):
        self.goto_menu_tools_maintenance_firmware_checkforupdate(spice)
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(1, MenuAppWorkflowObjectIds.scrollbar_fwupdate_update_available)
        confirm_no = spice.wait_for("#fwupdateAvailableConfirmNo", 30)
        confirm_no.mouse_click()

    def goto_menu_tools_maintenance_firmware_update_start_download(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_available_scroll_yes(spice)
        start_update = spice.wait_for("#ContinueButton")
        start_update.mouse_click()

    def verify_icc_error_view(self, spice):
        icc_error_reason = spice.query_item("#IccErrorReason SpiceText[visible=true]")["text"]
        logging.info(f"ICC error reason: {icc_error_reason}")
        return icc_error_reason

    def skip_icc_error_view(self, spice):
        #Click skip to go back to the previous screen
        skip_button = spice.wait_for("#SkipButton")
        skip_button.mouse_click()

    def goto_menu_tools_maintenance_firmware_updatehistory(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        update_history_button = spice.wait_for("#fwUpUpdateHistory")
        update_history_button.mouse_click()
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except Exception as e:
            logging.info("At Expected Menu")
        else:
            #SignIn Screen
            self.perform_signIn(spice)
        finally:
            logging.info("At Expected Menu")
        assert spice.wait_for("#updateHistoryLayout")
        logging.info("At update history screen")

    def get_current_region_code(self, spice):
        country = spice.wait_for(MenuAppWorkflowObjectIds.get_region_value)['text']
        countrycode = self.country_code_iso[country]
        return countrycode

    # Get the country/region text
    def get_current_region_text(self, spice):
        country = spice.wait_for(MenuAppWorkflowObjectIds.get_region_value)['text']
        return country

    def get_servicetest_category(self, spice, index):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_categories.format(index), timeout=15)

    def get_servicetest_category_subsystem(self, spice, index):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_subsystems.format(index), timeout=15)

    def get_servicetest_test(self, spice, index):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_tests.format(index), timeout=15)

    def get_servicetest_test_start_button(self, spice, index):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_tests_start_button.format(index), timeout=15)

    def get_servicetests_USBSettings(self, spice):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_USBSettings)

    def go_back_servicetest(self, spice):
        sub = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton_aux)
        sub.mouse_click()

    def get_servicetest_category_subsystem_option(self, spice, index):
        return spice.wait_for(MenuAppWorkflowObjectIds.view_service_category_subsystem_option.format(index), timeout=15)

    def goback_on_servicetest_view(self, spice):
        backButton = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton, timeout=15)
        middle_width  = backButton["width"] / 2
        middle_height = backButton["height"] / 2
        backButton.mouse_click(middle_width, middle_height)

    def go_back_servicetest_subsystem(self, spice):
        try:
            sub = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton_aux_subsystem, timeout=5)
        except:
            sub = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton_subsystem, timeout=5)
        sub.mouse_click()

    def go_back_servicetest_category(self, spice):
        try:
            sub = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton_category, timeout=5)
        except:
            sub = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_backbutton_aux_category, timeout=5)
        sub.mouse_click()

    def get_calibration_header(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_header.format(index))['text']

    def get_calibration_estimated_duration_name(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_duration_name.format(index))

    def get_calibration_estimated_duration_value(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_duration_value.format(index))

    def get_calibration_estimated_substrate_used_name(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_substrate_used_name.format(index))

    def get_calibration_estimated_substrate_used_value(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_substrate_used_value.format(index))

    def get_calibration_estimated_ink_used_name(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_ink_used_name.format(index))

    def get_calibration_estimated_ink_used_value(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_estimated_ink_used_value.format(index))

    def get_calibration_description_title(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_description_title.format(index))['text']

    def get_calibration_description_content(self, spice, index=""):
        return spice.wait_for(MenuAppWorkflowObjectIds.calibration_description_content.format(index))['text']

    def get_product_name(self, udw):
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        return printerName

    def check_troubleshooting_fax_visible(self, spice):
        """
        Check if fax options shows in troubleshooting screen.
        """
        spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        try:
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax)
            return True
        except:
            logging.info('Fax option does not display on troubleshooting screen')
            return False

    def verify_alert_setup_incomplete(self, spice, net):
        # Creating setup incomplete alert message using UDW command
        spice.udw.mainApp.execute("RtpManager PUB_triggerRtpEvent 15 0 3")
        assert spice.wait_for("#printerNeedsWSRegistrationNowWindow")
        current_string = spice.wait_for("#alertDetailDescription #contentItem")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cSetupIncompleteCannotPrintActivate")
        assert current_string == expected_string, "String mismatch"
        okbutton = spice.wait_for("#OK")
        okbutton.mouse_click()
        spice.statusCenter_dashboard_expand()
        alert_option = spice.wait_for("#alertStatusCenterText")
        alert_option.mouse_wheel(0, -150)
        time.sleep(5)
        alert_option.mouse_click()
        time.sleep(2)
        spice.udw.mainApp.execute("RtpManager PUB_unpublishRtpEvent 15")
        spice.statusCenter_dashboard_collapse()

    def goto_advancedoptions_from_defaultprintoptions(self, spice, net, locale):
        margins_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions+" SpiceText[visible=true]")
        assert margins_button["text"] == str(LocalizationHelper.get_string_translation(net, "cSettingAdvanceOptions", locale))

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions+"ScrollBar")

    def goto_copymode_from_advancedoptions(self, spice):
        # Click copy mode button
        select_copy_mode = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_copymode)
        select_copy_mode.mouse_click()

    def goto_copymodeoptions(self, spice, net, locale):
        # Navigate to copymode in settings
        self.goto_menu_settings_print_defaultprintoptions(spice)
        self.goto_advancedoptions_from_defaultprintoptions(spice, net, locale)
        self.goto_copymode_from_advancedoptions(spice)

    def goto_menu_tools_servicemenu_servicetests_continuousAutoSensing(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_service_servicetests,
                             MenuAppWorkflowObjectIds.menu_button_service_servicetests_continuousAutoSensing,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        time.sleep(3)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_continuousautoSensing)
        logging.info("At Tools -> Service -> Service Tests -> Continuous Auto Sensing Screen")

    def servicemenu_servicetests_continuous_autoSensing_oneSide_Test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service Menu -> Service Tests -> Continuous Auto Sensing Oneside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_continuousautoSensing)
        assert currentScreen

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["checked"] == False, "twoside checked"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["checked"] == False, "saveToDisk checked"
        #continuous copy start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_continuousAutoSensing_startStopButton)
        startButton.mouse_click()

        logging.info("wait until complete")
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        Copy(cdm, udw).validate_settings_used_in_copy(
            input_plex_mode = "simplex",
            sides = "oneSided"
        )
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["constrained"] == True, "twoside constrained"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["constrained"] == True, "twoside constrained"
        time.sleep(4)
        #continuous copy stop
        stopButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_continuousAutoSensing_startStopButton)
        stopButton.mouse_click()
        logging.info("wait until Cancel")
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Canceling')
        #checkBox status check : constrained = True
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["constrained"] == False, "twoside not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def servicemenu_servicetests_continuous_autoSensing_twoside_Test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service Menu -> Service Tests -> Continuous Auto Sensing Twoside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_continuousautoSensing)
        assert currentScreen, "continuousCopy page not found"

        checkBoxButton = spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)
        checkBoxButton.mouse_click()
        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["checked"] == True, "twoside checked"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["checked"] == True, "saveToDisk checked"
        #continuous copy start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_continuousAutoSensing_startStopButton)
        startButton.mouse_click()
        time.sleep(3)

        logging.info("wait until complete")
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        Copy(cdm, udw).validate_settings_used_in_copy(
            input_plex_mode = "duplex",
            sides = "oneSided"
        )
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["constrained"] == True, "twoside constrained"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["constrained"] == True, "twoside constrained"
        time.sleep(4)
        #continuous copy stop
        stopButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_continuousAutoSensing_startStopButton)
        stopButton.mouse_click()
        logging.info("wait until Cancel")
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Canceling')
        #checkBox status check : constrained = True
        assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        # assert spice.wait_for(MenuAppWorkflowObjectIds.continuousAutoSensing_saveToDiskCheckBox)["constrained"] == False, "twoside not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def set_defaultprintoptions_marginlayout_clipcontents(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_marginlayout, MenuAppWorkflowObjectIds.margin_layout_clipcontents)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)

    def set_defaultprintoptions_marginlayout_oversize(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_marginlayout, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_marginlayout, MenuAppWorkflowObjectIds.margin_layout_oversize)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)

    def set_defaultprintoptions_marginlayout(self, spice, marginlayout):
        """
        Set a layout option from margin layout screen.
        """
        if marginlayout == MenuAppWorkflowObjectIds.margin_layout_clipcontents:
            self.set_defaultprintoptions_marginlayout_clipcontents(spice)
        elif marginlayout == MenuAppWorkflowObjectIds.margin_layout_oversize:
            self.set_defaultprintoptions_marginlayout_oversize(spice)
        else:
            assert False, "Requested margin layout option does not exist."

    def presset_Paperoptions_removeWhiteAreas(self, spice):
        spice.wait_for(MenuAppWorkflowObjectIds.switchSettingsRemoveWhiteAreasLayout)
        removeWhiteAreas_button = spice.wait_for(MenuAppWorkflowObjectIds.switchViewRemoveWhiteAreasLayout)
        previousState = removeWhiteAreas_button["checked"]

        removeWhiteAreas_mouseArea = spice.wait_for(MenuAppWorkflowObjectIds.switchViewRemoveWhite)
        removeWhiteAreas_mouseArea.mouse_click()

        currentState = removeWhiteAreas_button["checked"]
        assert previousState != currentState

    def set_defaultPaperoptions_rotationLayout(self, spice, paperSizelayout):
        """
        Set a layout option from paper size layout screen.
        """
        if paperSizelayout == MenuAppWorkflowObjectIds.value_Rotation_0:
            self.set_defaultprintoptions_rotation_Value_Option(spice, MenuAppWorkflowObjectIds.value_Rotation_0)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_Rotation_90:
            self.set_defaultprintoptions_rotation_Value_Option(spice, MenuAppWorkflowObjectIds.value_Rotation_90)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_Rotation_180:
            self.set_defaultprintoptions_rotation_Value_Option(spice, MenuAppWorkflowObjectIds.value_Rotation_180)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_Rotation_270:
            self.set_defaultprintoptions_rotation_Value_Option(spice, MenuAppWorkflowObjectIds.value_Rotation_270)
        else:
            assert False, "Requested paper size layout option does not exist."

    def set_defaultprintoptions_rotation_Value_Option(self, spice, option):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_paperOptions,
                             MenuAppWorkflowObjectIds.settingsSpiceComboBox_rotationLayout,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.view_paperOptions + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperOptions)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.settingsSpiceComboBoxpopupList_rotationLayout,
                             option,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scroolbar_menu_PaperOptions)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperOptions)

    def set_defaultPaperoptions_paperSizeLayout(self, spice, paperSizelayout):
        """
        Set a layout option from paper size layout screen.
        """
        if paperSizelayout == MenuAppWorkflowObjectIds.value_A0:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A0)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A1:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A1)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A2:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A2)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A3:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A3)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A4:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A4)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A5:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A5)
        elif paperSizelayout == MenuAppWorkflowObjectIds.value_A6:
            self.set_defaultprintoptions_paperSizeValue_Option(spice, MenuAppWorkflowObjectIds.value_A6)
        else:
            assert False, "Requested paper size layout option does not exist."

    def set_defaultprintoptions_paperSizeValue_Option(self, spice, option):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_paperOptions,
                             MenuAppWorkflowObjectIds.comboBox_paperSizeLayout,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.view_paperOptions + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperOptions)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_paperOptions_paperSize_values,
                             option,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scroolbar_menu_PaperOptions)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_paperOptions)

    def set_defaultprintoptions_marginvalue_0mm(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions_margins_value, MenuAppWorkflowObjectIds.margin_value_0mm)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)

    def set_defaultprintoptions_marginvalue_3mm(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions_margins_value, MenuAppWorkflowObjectIds.margin_value_3mm)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)

    def set_defaultprintoptions_marginvalue_5mm(self, spice):
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_advancedoptions_margins_value, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")

        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions_margins_value, MenuAppWorkflowObjectIds.margin_value_5mm)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)


    def set_defaultprintoptions_marginvalue(self, spice, marginvalue):
        """
        Set a margin value from margins screen.
        """
        """
        if marginvalue == MenuAppWorkflowObjectIds.margin_value_0mm:
            self.set_defaultprintoptions_marginvalue_0mm(spice)
        elif
        """
        if marginvalue == MenuAppWorkflowObjectIds.margin_value_3mm:
            self.set_defaultprintoptions_marginvalue_3mm(spice)
        elif marginvalue == MenuAppWorkflowObjectIds.margin_value_5mm:
            self.set_defaultprintoptions_marginvalue_5mm(spice)
        else:
            assert False, "Requested margin value does not exist."


    def set_defaultprintoptions_pageOrdervalue(self, spice, pageOrdervalue):
        """
        Set a pageOrder value from margins screen.
        """
        if pageOrdervalue == MenuAppWorkflowObjectIds.view_pageorder_firstPageOnTop:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, MenuAppWorkflowObjectIds.view_pageorder_firstPageOnTop)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)
        elif pageOrdervalue == MenuAppWorkflowObjectIds.view_pageorder_lastPageOnTop:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_defaultprintoptions, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, scrollbar_objectname = MenuAppWorkflowObjectIds.view_defaultprintoptions_advancedoptions+"ScrollBar")
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_pageOrder, MenuAppWorkflowObjectIds.view_pageorder_lastPageOnTop)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions)
        else:
            assert False, "Requested pageOrder value does not exist."

    def status_center_ipaddress_validation(self, spice, net):
        # Validating the printer IP in status center
        ipaddress = net.ip_address
        print(ipaddress)
        spice.statusCenter_dashboard_expand()
        displayed_ipaddress = spice.query_item("#statusCenterServiceStackView #grid #infoBlockRow #textColumn SpiceText[visible=true]", query_index=1)["text"]
        print("ip address data", displayed_ipaddress)
        assert ipaddress == displayed_ipaddress

    def cancel_calibration_flow(self, spice, confirm_cancel=True):
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration, timeout=40)
        cancel_button.mouse_click()
        if confirm_cancel:
            confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_confirm_cancel)
            confirm_button.mouse_click()

    def object_id_validation(self, cdm, spice, active_screen, objectId_list):
        #Main validation function for object IDs 
        object_ids = spice.udw.mainUiApp.SpiceTestServer.getObjectTreeHeirarchy(active_screen)
        failed_obj = 0
        if objectId_list in [objectidvalidation.menu_scan_screen_object_ids, objectidvalidation.home_scan_screen_object_ids]:
            failed_obj = self._validate_scan_screen(cdm, spice, active_screen, objectId_list, object_ids)
        elif objectId_list in [objectidvalidation.menu_print_screen_object_ids, objectidvalidation.home_print_screen_object_ids]:
            self._validate_print_screen(cdm, objectId_list)
        elif objectId_list == objectidvalidation.fax_screen_object_id:
            self._validate_fax_screen(cdm, objectId_list)
        else:
            object_ids = spice.udw.mainUiApp.SpiceTestServer.getObjectTreeHeirarchy(active_screen)
            
            refresh_wait_time = 5
            time.sleep(refresh_wait_time)
            
            failed_obj = self._perform_generic_validation(object_ids, objectId_list)

        if failed_obj != 0:
            assert False, ("One or more Object ID not found. Please fix the changed object ID")
        else:
            print("All object id is matching")
            
    def _validate_scan_screen(self, cdm, spice, active_screen, objectId_list, object_ids):
        #Validates the scan screen object IDs
        self._filter_scan_buttons_by_availability(cdm, objectId_list)
        object_ids = spice.udw.mainUiApp.SpiceTestServer.getObjectTreeHeirarchy(active_screen)
        failed_obj = 0
        if "HomeFolderView" in active_screen or "MenuAppList" in active_screen:
            failed_obj = self._validate_scan_screen_with_swipe(spice, active_screen, objectId_list, object_ids)
            
        return failed_obj
        
    def _filter_scan_buttons_by_availability(self, cdm, objectId_list):
        #Filters scan buttons from the object ID list
        scan_to_email = cdm.get_raw(cdm.JOB_TICKET_SCAN_EMAIL_JOB)
        if scan_to_email.status_code == 404:
            del objectId_list["scan_to_email_button"]
            
        scan_to_network_folder = cdm.get_raw(cdm.JOB_TICKET_SCAN_NETWORK_FOLDER)
        if scan_to_network_folder.status_code == 404:
            del objectId_list["scan_to_network_folder_button"]
            
        scan_to_sharepoint = cdm.get_raw(cdm.JOB_TICKET_SCAN_SHAREPOINT_JOB)
        if scan_to_sharepoint.status_code == 404:
            del objectId_list["scan_to_sharepoint_button"]
            
        scan_to_usb = cdm.get_raw(cdm.JOB_TICKET_SCAN_USB_JOB)
        if scan_to_usb.status_code == 404:
            del objectId_list["scan_to_usb_button"]
            
        scan_to_computer = cdm.get_raw(cdm.CDM_REPORTS).json()
        found = 0
        for report in scan_to_computer['reports']:
            if report['reportId'] == 'scanToComputerSetupReport':
                found = found + 1
        if found == 0:
            del objectId_list["scan_to_computer_button"]
        else:
            logging.debug("Scan to computer menu is available")
            
    def _validate_scan_screen_with_swipe(self, spice, active_screen, objectId_list, object_ids):
        #Validates scan screen object IDs in a swipe view
        try:
            from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
            
            try:
                workflow_common_operations = spice.basic_common_operations
            except:
                workflow_common_operations = Workflow2UICommonOperations(spice)
            
            home_scan_view_id = objectidvalidation.home_scan_screen_object_ids["scan_app_landing_view"]
            menu_scan_view_id = objectidvalidation.menu_scan_screen_object_ids["scan_app_landing_view"]
            swipe_view_id = home_scan_view_id if "HomeFolderView" in active_screen else menu_scan_view_id
            swipe_view = spice.query_item(swipe_view_id)
            max_pages = swipe_view["count"]
            page_navigation_count = 0
            
            found_items = {}
            missing_items = []
            
            failed_obj = 0
            if objectId_list == objectidvalidation.home_scan_screen_object_ids:
                failed_obj = self._validate_home_scan_screen(spice, active_screen, objectId_list, object_ids, swipe_view, max_pages)
            
            for name, obj_id in list(objectId_list.items()):
                page_found = workflow_common_operations.find_item_across_pages(swipe_view_id, obj_id)
                if page_found >= 0:
                    navigation_increment = 2
                    page_navigation_count += navigation_increment
                
                if page_found >= 0:
                    found_items[name] = page_found
                else:
                    missing_items.append(name)
                    
            return failed_obj
            
        except Exception as e:
            logging.error(f"Error during page Navigation validation: {str(e)}")
            return 0
            
    def _validate_home_scan_screen(self, spice, active_screen, objectId_list, object_ids, swipe_view, max_pages):
        #Validates home scan screen object IDs
        page_map = {}
        page_ids_map = {}
        original_index = swipe_view["currentIndex"]
        
        all_ids = object_ids.split(",")
        
        scan_keywords = []
        for key in objectidvalidation.home_scan_screen_object_ids:
            if "scan" in key or "usb" in key or "email" in key or "computer" in key or "share" in key or "network" in key or "folder" in key:
                scan_keywords.append(key.replace("_button", "").replace("scan_to_", ""))
        
        scan_related_ids = [id for id in all_ids if any(keyword in id.lower() for keyword in scan_keywords)]
        
        sharepoint_id_full = objectidvalidation.home_scan_screen_object_ids["scan_to_sharepoint_button"]
        sharepoint_id = sharepoint_id_full.split("#")[1][:8]  # Extract the first part of the ID
        matching_ids = [id for id in all_ids if sharepoint_id.lower() in id.lower()]
        
        failed_obj = 0
        found_obj = 0
        all_pages_object_ids = ""
        page_navigation_count = 0
        
        for page in range(max_pages):
            swipe_view["currentIndex"] = page
            page_navigation_count += 1
            
            wait_time = 4
            time.sleep(wait_time)
            
            page_object_ids = spice.udw.mainUiApp.SpiceTestServer.getObjectTreeHeirarchy(active_screen)
            page_ids = page_object_ids.split(",")
            page_ids_map[page] = page_ids
            
            all_pages_object_ids += page_object_ids + ","
            
            items_on_page = []
            ids_on_page = []
            
            for name, obj_id in list(objectId_list.items()):
                clean_id = obj_id.split("#")[1]
                try:
                    item = spice.check_item(obj_id)
                    is_visible = False
                    if item:
                        try:
                            is_visible = item["visible"]
                        except Exception:
                            logging.info("exception in index")
                            try:
                                is_visible = item["visible"]
                            except:
                                pass
                    
                    if item and is_visible:
                        items_on_page.append(name)
                        ids_on_page.append(clean_id)
                except Exception as e:
                    logging.debug(f"Error checking '{name}': {str(e)}")
            
            if items_on_page:
                page_map[page] = {
                    "names": items_on_page,
                    "ids": ids_on_page
                }
        
        len_id = len(objectId_list)
        tuple_obj = tuple(objectId_list.values())
        for x in range(len_id):
            split_value = tuple_obj[x].split("#")[1]
            if split_value in all_pages_object_ids:
                found_obj += 1
            else:
                failed_obj += 1
        
        swipe_view["currentIndex"] = original_index
        
        return failed_obj
    
    def _validate_print_screen(self, cdm, objectId_list):
        #Validates print screen object IDs.
        usb_print = cdm.get_raw(cdm.JOB_TICKET_CONFIGURATION_USB_PRINT)
        if usb_print.status_code == 404:
            del objectId_list["print_from_usb_button"]
            
        job_storage = cdm.get_raw(cdm.FOLDERS_ENDPOINT)
        if job_storage.status_code == 404:
            del objectId_list["print_job_storage_button"]
            
        quickset_forms = cdm.get_raw(cdm.CDM_REPORTS).json()
        found = 0
        for report in quickset_forms['reports']:
            if report['reportId'] == 'QuickFormsChecklist':
                found = found + 1
        if found == 0:
            del objectId_list["print_quickforms_button"]
    
    def _validate_fax_screen(self, cdm, objectId_list):
        #Validates fax screen object IDs.
        found = 0
        fax_original_sides = cdm.get_raw(cdm.FAX_SCAN_ENDPOINT).json()
        for value in fax_original_sides['validators']:
            if value['propertyPointer'] == "src/scan/plexMode":
                for flex in value["options"]:
                    if flex["seValue"] == "duplex":
                        found = found + 1
        if found == 0:
            del objectId_list["combo_box_row_2sidedOriginal"]
            del objectId_list["combo_box_2sidedOriginal"]
    
    def _perform_generic_validation(self, object_ids, objectId_list):
        #Performs generic validation of object IDs
        failed_obj = 0
        len_id = len(objectId_list)
        tuple_obj = tuple(objectId_list.values())
        for x in range(len_id):
            split_value = tuple_obj[x].split("#")[1]
            if (split_value in object_ids):
                logging.debug(f"{split_value} - Object ID available and matching")
            else:
                failed_obj = failed_obj + 1
                logging.warning(f"{split_value} - Object ID not found.")
                
        return failed_obj

    def dual_cancel_calibration_flow(self, spice):
        button_clicked = False
        timeout_start = time.time()
        TIMEOUT = 120

        # Ensure button is clicked by using a try-except block to handle its intermittent visibility
        while(button_clicked == False and time.time() < timeout_start + TIMEOUT):
            try:
                cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration)
                cancel_button.mouse_click()
                button_clicked = True
            except QmlTestServerError:
                pass

        assert button_clicked == True, "Cancel button could not be found"
        cancel_printing_and_curing_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_print_and_curing)
        cancel_printing_and_curing_button.mouse_click()
        confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.confirm_cancel_calibration)
        confirm_button.mouse_click()

    def goto_menu_status(self, spice):
        spice.main_app.goto_job_queue_app()
        logging.info("At Job Status Screen")
        time.sleep(1)

    def goto_menu_job_queue_app(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_jobApp)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_jobApp + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.job_list_view, 25)
        logging.info("At Menu Job queue Screen")
        time.sleep(1)

    def goto_menu_trays(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_trays)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_trays + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuTrays)
        logging.info("At Menu Trays Screen")
        time.sleep(1)

    def verify_all_location_names(self, spice, options):
        """
        Navigates to each location option and verifies the name is as expected
        @param spice : spice object
        @param options : a list of tuples with each tuple is a pair of
        location code and location name.
        Eg:[('AF', 'Afghanistan'), ('AL', 'Albania')]
        """

        scroll_bar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_countryregion_wf)

        for option in options:
            menu_item = "#" + option[0] + "countryRegionWF"
            obj_id = "#MenuValue" + option[0]
            expected_location_text = option[1]
            scroll_bar_pos = scroll_bar.__getitem__("position")

            print("Verifying location : " + expected_location_text)
            self.menu_navigation_radiobutton(spice, MenuAppWorkflowObjectIds.view_settings_country_region_wf, menu_item, obj_id, select_option=False,
                    scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_countryregion_wf, step_value = scroll_bar_pos, scrolling_value=0.01)

            print("Verify UI shows the expected location name")
            ui_location_text = spice.query_item(obj_id + " SpiceText")["text"]
            assert ui_location_text  == expected_location_text , "Location name mismatch"

    def change_settings_tray_manual_feed(self, spice, enable_option = True):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable Manual feed
        @param spice:
        @param enable_option: True to enable manual feed False to Disable
        """
        manualFeedToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_tray_manualfeed)
        if(manualFeedToggleSwitch ["checked"] != enable_option):
            manualFeedToggleSwitch .mouse_click()
            time.sleep(1)
            assert manualFeedToggleSwitch ["checked"] == enable_option, "Manual feed Enable/Disbale failed"
    
    def change_settings_tray_alternative_letterhead_mode(self, spice, enableOption = True):
        """
        Helper method to enable/disable Alternative Letterhead Mode
        UI Should be in Menu App --> Settings --> tray and enable/disable Alternative Letterhead Mode
        @param spice:
        @param enableOption: True to enable Alternative Letterhead Mode, False to disable
        """
        ALMtoggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_tray_Alternative_Letter_Head_Mode)
        if(ALMtoggleSwitch ["checked"] != enableOption):
            ALMtoggleSwitch.mouse_click()
            time.sleep(1)
            assert ALMtoggleSwitch ["checked"] == enableOption, "Alternative Letterhead Mode Enable/Disbale failed"

    def change_settings_tray_override_size_errors(self, spice, enableOption = True):
        """
        Helper method to enable/disable override size errors
        UI Should be in Menu App --> Settings --> tray and enable/disable override size errors
        @param spice:
        @param enableOption: True to enable override size errors, False to Disable
        """
        toggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_tray_overridesizeerrors)
        if(toggleSwitch ["checked"] != enableOption):
            toggleSwitch .mouse_click()
            time.sleep(1)
            assert toggleSwitch ["checked"] == enableOption, "Override size errors Enable/Disbale failed"

    def change_settings_size_type_prompt(self, spice, enable_option = True):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable size/type Prompt
        @param spice:
        @param enable_option: True to enable size/type Prompt False to Disable
        """
        sizeTypePromptToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_tray_sizeTypePrompt)
        if(sizeTypePromptToggleSwitch ["checked"] != enable_option):
            sizeTypePromptToggleSwitch.mouse_click(x=2, y=2)
            time.sleep(1)
            assert sizeTypePromptToggleSwitch ["checked"] == enable_option, "Size/Type Prompt Enable/Disbale failed"

    def goto_menu_tools_servicemenu_information(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice,udw)
        self.goto_information_service(spice)

    def goto_menu_tools_servicemenu_information_eventlog(self, spice, udw):
        self.goto_menu_tools_servicemenu_information(spice, udw)
        prod_config = Configuration(spice.cdm)
        self.product_name = prod_config.productname
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            self.menu_navigation(spice,
                                '#serviceInformationMenuList',
                                "#infoEventLogSettingsTextImage",
                                scrollbar_objectname = '#serviceInformationMenuListScrollBar')
        elif self.product_family == 'designjet' and self.product_name == 'sunspot':
            self.menu_navigation(spice,
                                MenuAppWorkflowObjectIds.view_service_information,
                                "#notPrintableInfoEventLogSettingsTextImage",
                                scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_information)
        else:
            self.menu_navigation(spice,
                                MenuAppWorkflowObjectIds.view_service_information,
                                "#infoEventLogSettingsTextImage",
                                scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_information)
        time.sleep(3)
        assert spice.wait_for("#eventLogView")
        logging.info("At Tools -> Service -> Information -> Event Logs")

    def goto_menu_tools_servicemenu_information_servicecounts(self, spice, udw):
        self.goto_menu_tools_servicemenu_information(spice, udw)
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            self.menu_navigation(spice,
                                '#serviceInformationMenuList',
                                "#serviceCountsSettingsTextImage",
                                scrollbar_objectname = '#serviceInformationMenuListScrollBar')
            assert spice.wait_for("#toolsServiceCounts")    
        else:
            self.menu_navigation(spice,
                                MenuAppWorkflowObjectIds.view_service_information,
                                MenuAppWorkflowObjectIds.menu_button_service_information_servicecounts,
                                scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_information)
            time.sleep(3)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_information_servicecounts)
        logging.info("At Tools -> Service -> Information -> Service Counts")

    '''def click_autocontinue_timeout_scrollbar(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.menu_button_settings_autocontinue_timeout_combobox, "#SettingsSpiceComboBox"],
        MenuAppWorkflowObjectIds.view_paperoutaction,scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_autocontinue_timeout_action)'''

    def goto_menu_tools_servicemenu_servicetests_service_continuous_scan(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_service_servicetests,
                             MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        time.sleep(3)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_continuous_scan)
        logging.info("At Tools -> Service -> Service Tests -> Continuous Scan")

    def servicemenu_servicetests_service_continuous_scan_oneside_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Continuous Scan Oneside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_continuous_scan)
        assert currentScreen, "continuous scan page not found"

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["checked"] == False, "twoside unchecked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["checked"] == False, "saveToDisk unchecked"
        #continuous scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        startButton.mouse_click()
        time.sleep(1)
        #checkBox status check : constrained = True
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == True, "twoside constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == True, "saveToDisk constrained"
        time.sleep(1)
        #continuous scan stop
        stopButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        stopButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Cancel")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == False, "saveToDisk not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def servicemenu_servicetests_service_continuous_scan_twoside_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Continuous Scan Twoside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_continuous_scan)
        assert currentScreen, "continuous scan page not found"

        checkBoxButton = spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)
        checkBoxButton.mouse_click()
        time.sleep(1)

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["checked"] == True, "twoside checked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["checked"] == False, "saveToDisk unchecked"
        #continuous scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        startButton.mouse_click()
        time.sleep(1)
        #checkBox status check : constrained = True
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == True, "twoside constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == True, "saveToDisk constrained"
        time.sleep(1)
        #continuous scan stop
        stopButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        stopButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Cancel")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == False, "saveToDisk not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def servicemenu_servicetests_service_continuous_scan_save_to_disk_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Continuous Scan SaveToDisk Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_continuous_scan)
        assert currentScreen, "continuous scan page not found"

        checkBoxButton = spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)
        checkBoxButton.mouse_click()
        time.sleep(1)

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["checked"] == False, "twoside unchecked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["checked"] == True, "saveToDisk checked"
        #continuous scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        startButton.mouse_click()
        time.sleep(1)
        #checkBox status check : constrained = True
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == True, "twoside constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == True, "saveToDisk constrained"
        time.sleep(1)
        #continuous scan stop
        stopButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceContinuousScan_startStopButton)
        stopButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Cancel")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceContinuousScan_saveToDiskCheckBox)["constrained"] == False, "saveToDisk not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def goto_menu_tools_servicemenu_servicetests_service_raw_scan(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_service_servicetests,
                             MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceRawScan,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        time.sleep(3)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_raw_scan)
        logging.info("At Tools -> Service -> Service Tests -> Raw Scan")

    def servicemenu_servicetests_service_raw_scan_oneside_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Raw Scan Oneside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_raw_scan)
        assert currentScreen, "Raw Scan page not found"

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["checked"] == False, "twoside unchecked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["checked"] == False, "mechanicalCalibration unchecked"
        #Raw Scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceRawScan_startStopButton)
        startButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Job Complete")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["constrained"] == False, "mechanicalCalibration not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def servicemenu_servicetests_service_raw_scan_twoside_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Raw Scan Twoside Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_raw_scan)
        assert currentScreen, "Raw Scan page not found"

        checkBoxButton = spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)
        checkBoxButton.mouse_click()
        time.sleep(1)

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["checked"] == True, "twoside checked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["checked"] == False, "mechanicalCalibration unchecked"
        #Raw Scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceRawScan_startStopButton)
        startButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Job Complete")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["constrained"] == False, "mechanicalCalibration not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def servicemenu_servicetests_service_raw_scan_mechanicalCalibration_test(self, spice, cdm, udw, net, configuration):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service -> Service Tests -> Raw Scan MechanicalCalibration Test
        """
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_service_raw_scan)
        assert currentScreen, "Raw Scan page not found"

        checkBoxButton = spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)
        checkBoxButton.mouse_click()
        time.sleep(1)

        #checkBox status check : checked = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["checked"] == False, "twoside unchecked"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["checked"] == True, "mechanicalCalibration checked"
        #Raw Scan start
        startButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_serviceRawScan_startStopButton)
        startButton.mouse_click()
        time.sleep(4)
        logging.info("wait until Job Complete")
        #checkBox status check : constrained = False
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_twosideCheckBox)["constrained"] == False, "twoside not constrained"
        assert spice.wait_for(MenuAppWorkflowObjectIds.serviceRawScan_mechanicalCalibrationCheckBox)["constrained"] == False, "mechanicalCalibration not constrained"
        time.sleep(5)
        ## Workaround for goto_homescreen() not going to Home Menu.
        spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        ## TODO: Menu Navigation for few objects is not working due to validateListObjectVisibility() issues so
        ##       scroll down by 0.3 to make transmitsignalloss button visible.
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        scrollbar.__setitem__("position",0.3)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_transmitsignalloss)
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_transmitsignalloss)
        logging.info("At Fax Diagnostic Transmit Signal Loss Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt)
        else:
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxmenudiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxregulatorytest)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        logging.info("At Tools -> Service -> Diagnostics ->Fax ->Fax Regulatory Test Screen")

    def goto_menu_tools_servicemenu_faxdiagnostics_faxV29SpeedSelection(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        if self.product_family == 'enterprise':
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt)
        else:
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxmenudiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxv29selection)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxv29selection)
        logging.info("At Tools -> Service -> Diagnostics ->Fax ->Fax v29 Speed Selection Screen")

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        # Scroll up to make Hook Operations Button visible
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        scrollbar.__setitem__("position",0)
        # Query Hook Operations
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_hookoperations)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_hookoperations)
        logging.info("At Hook Operations View")

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        time.sleep(1)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_randomdata)
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata)
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen")

    def goto_menu_tools_servicemenu_faxdiagnostics_generatesinglemodemtonemenu(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_singlemodemtone,
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_singlemodemtone)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_singlemodemtone)
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generateDialNumber(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_generate_dial_phone_no,
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_generate_dial_phone_no)
        time.sleep(1)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_dial_phone_number)
        logging.info("At Fax Diagnostic Generate/Dial Phone No Screen")
        time.sleep(1)

    def updateSpinBox(self,spice,spinBox_up,spinBox_down,spinBox_text,setValue):
        currentValue = float(spice.query_item(spinBox_text)["text"])
        while float(currentValue) != float(setValue):
            if float(currentValue) < float(setValue):
                spice.query_item(spinBox_up).mouse_click()
            else:
                spice.query_item(spinBox_down).mouse_click()
            currentValue = float(spice.query_item(spinBox_text)["text"])


    # Get imageregistration card view
    def get_data_from_card_views(self, spice, spice_item_dict,index,scroll):
        position = 0.3
        if scroll == True:
            scrollbar = spice.wait_for("#imageRegistrationPagelist1ScrollBar")
            scrollbar.__setitem__("position", position)
        sizeIndex = index
        if index != 0:
            sizeIndex = (index + 1)
        spice_item_dict2 = { }
        time.sleep(5)
        for key in spice_item_dict.keys():
            ids_data = spice_item_dict[key]
            if ids_data == MenuAppWorkflowObjectIds.imageregistration_mediasize:
                sizeIndex = index
                if index != 0:
                    sizeIndex = (index + 1)
                    obj_state = spice.query_item(ids_data,sizeIndex)["text"]
                else:
                    obj_state = spice.query_item(ids_data,index)["text"]
            else:
                obj_state = spice.query_item(ids_data,index)["text"]
            spice_item_dict2 [len(spice_item_dict2)] = obj_state
        return spice_item_dict2

    def goto_menu_tools_troubleshooting_printquality_imageRegistartion(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        time.sleep(5)
        spice.wait_for("#printQualitySettingsTextImage").mouse_click()
        imageRegistrationPage = spice.wait_for("#imageRegistrationPageSettingsTextImage").mouse_click()
        if(imageRegistrationPage == None):
            scrollbar = spice.check_item("#printQualityMenuListScrollBar")
            if scrollbar != None:
                scrollbar.__setitem__("position", "0.5")
            spice.wait_for("#imageRegistrationPageSettingsTextImage").mouse_click()
        assert spice.wait_for("#imageRegistrationPagelist1ScrollBar"),"Image Registration Page not found"
        logging.info ("At Troubleshooting -> Print Quality -> Image Registration -> ImageRegsiatrion")


    def goto_menu_tools_troubleshooting_printquality_Menu_navigation(self, spice, menu_Id):
        view = spice.wait_for("#printQualityMenuList")
        fullCalibrationView = spice.wait_for(menu_Id).mouse_click()
        if(fullCalibrationView == None):
            scrollbar = spice.check_item("#printQualityMenuListScrollBar")
            if scrollbar != None:
                scrollbar.__setitem__("position", "0.4")
            spice.wait_for(menu_Id).mouse_click()
        logging.info ("Callibration Initialted")

    def goto_menu_tools_troubleshooting_printquality_Menu_Item(self, spice, menu_Id, scroll_pos):
        start_time = time.time()
        timeout = 15
        scrollbar = spice.wait_for("#printQualityMenuListScrollBar")
        while time.time()-start_time < timeout:
            menu_ = spice.check_item(menu_Id)
            if menu_ != None:
                break
            else:
                scrollbar.__setitem__("position", scroll_pos)

    def signin_from_homescreen(self,spice):
        spice.signIn.goto_sign_in_app("Sign In")

    def goto_menu_settings_print_systemPrintOption(self, spice):
        self.goto_menu_settings_print(spice)
        systemPrintOptionButton = spice.wait_for("#systemPrintOptionsSettingsTextImage")
        systemPrintOptionButton.mouse_click()
        time.sleep(1)
        pclAndPostScriptSettingsButton = spice.wait_for("#pclAndPostScriptSettingsSettingsTextImage")
        pclAndPostScriptSettingsButton.mouse_click()

    def goto_menu_settings_print_systemFontSettings(self,spice):
        self.goto_menu_settings_print_systemPrintOption(spice)
        pclConfigSettingsButton = spice.wait_for("#pclConfigSettingsTextImage")
        pclConfigSettingsButton.mouse_click()
        time.sleep(1)

    def goto_usage_reports(self,spice):
        self.workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.row_object_usage_report,MenuAppWorkflowObjectIds.view_status_report, select_option=False,scrollbar_objectname = MenuAppWorkflowObjectIds.status_report_scrollbar_name)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.control_object_usage_reports)
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.control_object_usage_reports)['checked'] == True

    def toggle_auto_shutdown_switch(self, spice):
        auto_shutdown = spice.wait_for("#autoshutdownSwitch")
        auto_shutdown.mouse_click(x=2, y=2)
        try:
            spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
            ##Sign IN
            self.perform_signIn(spice)
        except:
            logging.info("DUT doesn't have a Sign-in Screen")

    def goto_serviceinfinitehs_black_only(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.row_object_serviceinfinitehs_Black, MenuAppWorkflowObjectIds.object_name_infinitehs_black],
        MenuAppWorkflowObjectIds.view_service_servicetests, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        # To check serviceinfinitehs_black screen is displayed
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_infinitehs_screen_black)
        # To check start button is visible and enabled
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["enabled"] == True

    def goto_serviceinfinitehs_color(self, spice):
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.row_object_serviceinfinitehs_color, MenuAppWorkflowObjectIds.object_name_infinitehs_color],
        MenuAppWorkflowObjectIds.view_service_servicetests, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        # To check serviceinfinitehs_color screen is displayed
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_infinitehs_screen_color)
        # To check start button is visible and enabled
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["visible"] == True
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["enabled"] == True

    def goto_serviceinfinitehs_start(self, spice):
        startbutton = spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)
        startbutton.mouse_click()
        # To check that toast message pops-up saying, "Printing"
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_infinitehs_toastinfo)["text"] == "Printing..."
        # To check cancel  button is enabled while printing
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_cancel)["enabled"] == True
        # To check start button is disabled while printing
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["enabled"] == False

    def goto_serviceinfinitehs_cancel(self, spice):
        cancelbutton = spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_cancel)
        cancelbutton.mouse_click()
        # To check that toast message pops-up saying, "Print canceled"
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        time.sleep(2)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_infinitehs_toastinfo)["text"] == "Print canceled"
        # To check cancel  button is disappears
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_cancel)["visible"] == False
        # To check start button is enable
        assert spice.wait_for(MenuAppWorkflowObjectIds.infinitehs_start)["enabled"] == True

    def bring_up_keyboard(self, spice):
        spice.goto_homescreen()
        self.signin_from_homescreen(spice)
        spice.signIn.select_sign_in_method("user", "user")
        # spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.2, "#bodyLayoutverticalLayoutScrollBar")
        user_name = spice.wait_for("#userUsernameInputField")
        user_name.mouse_click()

    def getProperty_Sevalues_FromCdm(self,alerts, propertyPointer,):
        seValue = ""
        if(alerts[0]['data']):
            for i in range(len(alerts[0]['data'])):
                if(alerts[0]['data'][i]['propertyPointer'] == propertyPointer):
                    seValue = alerts[0]['data'][i]['value']['seValue']
                    break
        return seValue

# Added for Fax V34 Speed Enable/Disable
    def change_troubleshooting_fax_speed(self, spice, enableOption = False):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App -->Tools---> Troubleshooting --> fax Disable Fax V34 Speed
        @param spice:
        @param enableOption: Set False to Disable Fax V34 Speed
        """
        fax34SpeedToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_toggle_fax34_speed)
        if(fax34SpeedToggleSwitch ["checked"] != enableOption):
            fax34SpeedToggleSwitch.mouse_click(10,10)
            time.sleep(1)
            assert fax34SpeedToggleSwitch ["checked"] == enableOption, "Fax V34 Speed Enable/Disbale failed"

    def change_troubleshooting_jbig_compression(self, enableOption = False):
        """
        Helper method to enable/disable JBIG Compression
        UI Should be in Menu App -->Tools---> Troubleshooting --> Fax --> JBIG Compression
        @param enableOption: Set False to Disable JBIG Compression
        """
        jbigCompressionSwitch = self._spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_fax_toggle_jbig_compression)
        if(jbigCompressionSwitch ["checked"] != enableOption):
            jbigCompressionSwitch.mouse_click(10,10)
            time.sleep(1)
            assert jbigCompressionSwitch ["checked"] == enableOption, "JBIG Compression Enable/Disbale failed"
    
    def change_troubleshooting_jbig_compression_dualfax(self,  enableOption = False,line:str ="line1"):
        """
        Helper method to enable/disable JBIG Compression for dual fax
        UI Should be in Menu App -->Tools---> Troubleshooting --> Fax --> JBIG Compression  
        """
        self._spice.wait_for("#jbigCompressionDualFaxSettingsTextImage_2infoBlockRow")
        current_button = self._spice.wait_for("#jbigCompressionDualFaxSettingsTextImage_2infoBlockRow")
        current_button.mouse_click()
        if line == "line1":
            switch = "#jbigCompressionFaxLine1MenuSwitchspiceSwitch"
        elif line == "line2":
            switch = "#jbigCompressionFaxLine2MenuSwitchspiceSwitch"
        else:
            raise ValueError("Invalid line specified. Use 'line1' or 'line2'.")
        jbigCompressionSwitch = self._spice.wait_for(switch)
        if(jbigCompressionSwitch ["checked"] != enableOption):
            jbigCompressionSwitch.mouse_click(10,10)
            time.sleep(1)
            assert jbigCompressionSwitch ["checked"] == enableOption, "JBIG Compression Enable/Disbale failed"
    
    def goto_menu_tools_troubleshooting_Fax_JBIG_Compression(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)

    def change_troubleshooting_Fax_JBIG_Compression(self, spice, enableOption = False):
        '''
        Navigate to Menu -> Tools -> Troubleshooting -> Fax -> JBIG Compression
        '''
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_troubleshooting_fax, MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_jbig, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_fax)
        jbig_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_jbig_switch)
        if(jbig_switch ["checked"] != enableOption):
            jbig_switch.mouse_click(10,10)
            time.sleep(1)
            assert jbig_switch ["checked"] == enableOption, "JBIG Compression Enable/Disbale failed"

# Added- Fax speaker mode Normal/Diagnostic
    def set_fax_speaker_mode_value(self):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App -->Tools---> Troubleshooting --> fax -->Fax speaker mode
        @param spice:
        @param enableOption: Change the fax speakermode to diagnostic
        """
        diagnostic_button = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_diagnostic)
        diagnostic_button.mouse_click(10,10)
        time.sleep(1)

#Added for Troubleshooting fax t30 Report
    def select_fax_t30_report_mode_from_troubleshooting_fax_enterprise(self, spice, fax_t30_report_mode):
        '''
        This is helper method to select fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        troubleshooting_fax_t30_repmode_view = spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu)
        troubleshooting_fax_t30_repmode_view.mouse_click()
        spice.wait_until(lambda:troubleshooting_fax_t30_repmode_view["visible"])
        logging.info(f"Select fax T30 report mode: <{fax_t30_report_mode}>")
        if fax_t30_report_mode == "Never automatically print":
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_never_auto_print)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print after every fax":
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_every_fax)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after sending fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_fax_t30_report_mode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_send)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print only after receiving fax":
            currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu)
            currentScreen.mouse_wheel(0, -100)
            time.sleep(2)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_receive)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
            time.sleep(2)
        elif fax_t30_report_mode == "Print only after problems sending fax":
            currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu)
            currentScreen.mouse_wheel(0, -130)
            time.sleep(2)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_send_errors)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
            time.sleep(2)
        elif fax_t30_report_mode == "Print only after problems receiving fax":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scrollbar_fax_t30_report_mode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_receive_errors)
            spice.wait_until(lambda:current_fax_t30_report_mode["visible"])
            current_fax_t30_report_mode.mouse_click()
        elif fax_t30_report_mode == "Print after any fax problems":
            menu_item_id = [MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_any_fax_errors, MenuAppWorkflowObjectIds.view_model_settings_radio_button]
            self.workflow_common_operations.goto_item(menu_item_id,MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode_menu, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_fax_t30_report_mode)
            current_fax_t30_report_mode = spice.wait_for(MenuAppWorkflowObjectIds.option_troubleshooting_fax_t30_repmode_print_after_fax_any_fax_errors)
            current_fax_t30_report_mode.mouse_click()
        else:
            raise logging.info(f"{fax_t30_report_mode} is not supported to select")

    def goto_menu_tools_servicemenu_faxdiagnostics_showallfaxlocations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_showalllocations,
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_showalllocations)
        currentElement.mouse_click()
        time.sleep(2)
        logging.info("At Tools -> Service -> Fax show ALL Location")

    def goto_menuapp_tray(self, spice):
        spice.homeMenuUI().goto_menu_trays(spice)
        spiceCard = spice.wait_for(MenuAppWorkflowObjectIds.view_menuTray)
        spiceCard.mouse_click()
        logging.info("At Tray Detailed Screen")
        time.sleep(2)
        close_button = spice.wait_for("#inputCloseAction")
        close_button.mouse_click()
        time.sleep(2)
        spice.wait_for(MenuAppWorkflowObjectIds.button_back).mouse_click()

    def get_advance_factor_value(self, spice):
        """
            Returns the current value of the manual paper advance factor from the UI
        """
        value = spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_calibration_spin_box)
        return int(value["text"], 10)

    def set_advance_factor_value(self, spice, value = None, dir = None , step = None):
        """
            Sets the value of the manual paper advance factor
        """
        value_input = spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_calibration_spin_box)
        # read current value
        if dir is None and step is None:
            value_input.mouse_click()
            time.sleep(1)
            value_input["text"] = value
            spice.wait_for("#enterKeyIntegerKeypad").mouse_click()
        else :
            initial_value = int(value_input["text"], 10)
            while step != 0 :
                if step is not None:
                    if dir == "up":
                        while step != 0 :
                            spice.wait_for(MenuAppWorkflowObjectIds.plus_button).mouse_click()
                            step -= 1
                    elif dir == "down":
                        while step != 0 :
                            spice.wait_for(MenuAppWorkflowObjectIds.minus_button).mouse_click()
                            step -= 1
                    else :
                        assert False , "Unknown Advance factor Increment/Decrement Direction"
                else:
                    assert False, "Step value is None"

    def navigate_through_pagination(self, spice, scroll_bar_id,screen_name,row_name, click):
        """
            Navigates through objects in pagination modal to get the specific descText object
            scroll_bar_id: Scroll bar id
            screen_name Name of the list view
            row_name: Name of the 1st object in the row
            click: True: Click the event, False: Verify the contents
        """
        list_screeen = spice.wait_for(screen_name)
        row_name = row_name
        scroll_bar = spice.wait_for(scroll_bar_id)
        scrollbar_size = scroll_bar["visualSize"]
        scroll_bar_position = scroll_bar["position"] 
        list_screen_size = list_screeen["height"]
        try:
            row_object = spice.query_item(row_name)
            row_size = row_object["height"]
            skip_size = scrollbar_size/(list_screen_size/row_size)
        except Exception as err:
            skip_size = scrollbar_size/(list_screen_size/57)
            logging.info("skip size: {}".format(skip_size))
            skip_size = 0.08

        while((scroll_bar["visualPosition"] < scrollbar_size) and scroll_bar):
            try:
                row_item = spice.wait_for(row_name)
                logging.info(f"Pagination Navigation: Row item: {row_item}")
                if row_item:
                    if click:
                        row_item.mouse_click()
                        if spice.wait_for("#eventLogDetailInfo #errorCode"):
                            logging.info("Pagination Navigation: Object found:")
                            back_button = spice.wait_for("#BackButton")
                            back_button.mouse_click()
                            logging.info("Pagination Navigation: Back button clicked")
                            break
                    else:
                        break
                else:
                    logging.info("Pagination Navigation: Object not found")
                    scroll_bar_position+=skip_size
                    scroll_bar.__setitem__("position", scroll_bar_position)
                    time.sleep(2)
            except Exception as err:
                logging.info(f"An Exception occured: {err}")
                scroll_bar_position+=skip_size
                scroll_bar.__setitem__("position", scroll_bar_position)
                time.sleep(2)
                    
    def navigate_through_checkboxes(self, spice, scroll_bar_id, checkbox_id, action,verify=False):
        """
            Navigates through checkboxes in the UI
            action: True for checking the checkbox, False for unchecking the checkbox
        """
        scroll_bar = spice.wait_for(scroll_bar_id)
        scrollbar_size = scroll_bar["visualSize"]
        scroll_bar_position = scroll_bar["position"]
        #Currently there are 5 options within the Eventlogs filter menu
        skip_position = scrollbar_size/5
        status = False
        while(scroll_bar["visualPosition"] <= scrollbar_size):
            try:
                checkbox = spice.query_item(checkbox_id)
                if action and not checkbox["checked"]:
                    if not checkbox["checked"]:
                        logging.info("Checkbox {} is not checked--> checking".format(checkbox_id))
                        checkbox.mouse_click()
                        if not verify:
                            break
                else:
                    if checkbox["checked"] and not action:
                        logging.info("Checkbox {} checkbox is checked--> unchecking".format(checkbox_id))
                        checkbox.mouse_click()
                if action and checkbox["checked"]:
                    status = True
                    break
                if not action and not checkbox["checked"]:
                    status = True
                    break
                scroll_bar_position+=skip_position
                scroll_bar.__setitem__("position", scroll_bar_position)
                time.sleep(2)
            except Exception as err:
                logging.info(f"An Exception occured: {err}")
                scroll_bar_position+=skip_position
                scroll_bar.__setitem__("position", scroll_bar_position)
                time.sleep(2)
        return status

    def is_network_settings_locked(self) -> bool:
        menu_settings_view = self.workflow_common_operations.get_element(MenuAppWorkflowObjectIds.view_menuSettings)
        if not menu_settings_view: return False

        lock_icon = self.workflow_common_operations.get_element(MenuAppWorkflowObjectIds.menu_button_settings_network + " #grid #networkSettingsSettingsTextImage_2infoBlockRow #secondInfoBlockModelLocked")
        return lock_icon

    def is_on_network_page(self) -> bool:
        network_view = self.workflow_common_operations.get_element(MenuAppWorkflowObjectIds.view_menu_network)
        if not network_view: return False

        return self.workflow_common_operations.get_element_property(network_view, "visible")

    def click_network_button(self) -> bool:
        button = self.workflow_common_operations.get_element(MenuAppWorkflowObjectIds.menu_button_settings_network)
        if not button: return False
        return self.workflow_common_operations.click(button)


    def goto_settings_general_quietmode_from_to(self, spice):
        """
        Goto quite mode From-To
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> enable Quiet mode
        """
        self.scroll_to_list_item(
            spice,
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_list,  # listName
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmode_settings_from_to,  # rowName
            MenuAppWorkflowObjectIds.scrollbar_quietmode_setting_list)  # scrollbarName

        from_to = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmode_settings_from_to)
        spice.wait_until(lambda: from_to["visible"] == True, 15)
        from_to.mouse_click()

    def set_from_to_start_time(self, spice, from_hour=None, from_minutes=None):
        """
        Set from to start time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To
        """
        logging.info(f"set quite mode start time hour is {from_hour}, minutes is {from_minutes}")
        if from_hour != None:
            self.set_hour_value_on_settings_general_quietmode_from_to(spice, from_hour)
        if from_minutes != None:
            self.set_minutes_value_on_settings_general_quietmode_from_to(spice, from_minutes)

    def set_from_to_end_time(self, spice, to_hour=None, to_minutes=None):
        """
        Set from to end time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To -> Next
        """
        logging.info(f"set quite mode start time hour is {to_hour}, minutes is {to_minutes}")
        if to_hour != None:
            self.set_hour_value_on_settings_general_quietmode_from_to(spice, to_hour)
        if to_minutes != None:
            self.set_minutes_value_on_settings_general_quietmode_from_to(spice, to_minutes)

    def set_hour_value_on_settings_general_quietmode_from_to(self, spice, value:str):
        """
        Set from to time hour value
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To
        """
        self.scroll_to_list_item(
            spice,
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_list,  # listName
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_hours_row,  # rowName
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_list_scrollbar)  # scrollbarName
        hour_locator = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_hours_spin_text)
        hour_locator.mouse_click()
        hour_locator.__setitem__('text', value)
        hour_locator.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad).mouse_click()

    def set_minutes_value_on_settings_general_quietmode_from_to(self, spice, value:str):
        """
        Set from to time minutes value
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To 
        """
        self.scroll_to_list_item(
            spice,
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_list,  # listName
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_minutes_row,  # rowName
            MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_list_scrollbar) 
        minutes_locator = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_setTime_minutes_spin_text)
        minutes_locator.mouse_click()
        minutes_locator.__setitem__('text', value)
        minutes_locator.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad).mouse_click()

    def click_next_btn_on_from_to_screen(self, spice):
        """
        Click next button on from to set time screen
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To 
        """
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.ok_button_set_time_modal)
        spice.validate_button(ok_button)
        ok_button.mouse_click()
        time.sleep(2)

    def get_quitemode_from_to_time(self, spice):
        """
        Get current From-To time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode
        """
        from_to_text_location = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_time, 15)
        time.sleep(1)
        from_to_text = from_to_text_location["text"]
        time_list = from_to_text.split("-")
        from_time = time_list[0].strip()
        to_time = time_list[1].strip()
        return from_time, to_time
    
    def verify_settings_general_quickmode_schedule(self, spice, enable_status):
        """
        Helper method to verify the enabled/disabled state of Quiet Mode Schedule
        UI Should be in Menu App --> Settings --> General --> Quiet Mode (schedule must be support)
        @param spice:
        @param enabledOption: True to verify enabled state and False to verify Disabled state
        """
        quietModeToggleSwitch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_quietmodesettings_schedule)
        assert quietModeToggleSwitch["checked"] == enable_status, "Quiet Mode Schedule Enable/Disbale failed"

    def get_date_value_on_menu_settings_general_datetime(self, spice):
        date_item = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_date)
        # wait 1 secons to wait correct text show, to skip get default text
        time.sleep(1)
        return date_item["text"]

    def get_time_value_on_menu_settings_general_date_time(self, spice):
        time_item = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_time)
        # wait 1 secons to wait correct text show, to skip get default text
        time.sleep(1)
        return time_item["text"]
    
    def set_menu_settings_general_date_time_date_day(self, spice, day_value:int, data_format="DD-MM-YYYY"):
        spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        if data_format == "YYYY-MM-DD":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scroll_bar_date_time_date)
        day_locator = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_date_day)
        day_locator.mouse_click()
        day_locator.__setitem__('text', day_value)
        day_locator.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad).mouse_click()

    def set_menu_settings_general_date_time_date_month(self, spice, month_value:int, data_format="DD-MM-YYYY"):
        spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        if data_format != "YYYY-MM-DD":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scroll_bar_date_time_date)
        month_locator = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_date_month)
        month_locator.mouse_click()
        month_locator.__setitem__('text', month_value)
        month_locator.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad).mouse_click()

    def set_menu_settings_general_date_time_date_year(self, spice, year_value:int, data_format="DD-MM-YYYY"):
        spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_date)
        if data_format != "YYYY-MM-DD":
            self.workflow_common_operations.scroll_to_position_vertical(0.5, MenuAppWorkflowObjectIds.scroll_bar_date_time_date)
        year_locator = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_date_year)
        year_locator.mouse_click()
        year_locator.__setitem__('text', year_value)
        year_locator.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad).mouse_click()

    def check_menu_settings_general_date_time_option_time_zone(self, spice, net):
        '''
        Check Time Zone option
        '''
        logging.info('Check Time Zone option')
        expected_string = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cTimeZone")
        actual_string = spice.wait_for(f'{MenuAppWorkflowObjectIds.dateTime_timeZone} {MenuAppWorkflowObjectIds.text_view_object}')["text"]
        assert actual_string == expected_string, f'The {actual_string} is not match {expected_string}'
        logging.info('Check Time Zone option Successfully')
        return actual_string

    def check_menu_settings_general_date_time_option_date(self, spice, net):
        '''
        Check Date option
        '''
        logging.info('Check Date option')
        expected_string = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cDate")
        actual_string = spice.wait_for(f'{MenuAppWorkflowObjectIds.dateTime_date} {MenuAppWorkflowObjectIds.text_view_object}')["text"]
        assert actual_string == expected_string, f'The {actual_string} is not match {expected_string}'
        logging.info('Check Date option Successfully')
        return actual_string

    def check_menu_settings_general_date_time_option_time(self, spice, net):
        '''
        Check Time option
        '''
        logging.info('Check Time option')
        expected_string = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cTime")
        actual_string = spice.wait_for(f'{MenuAppWorkflowObjectIds.dateTime_time} {MenuAppWorkflowObjectIds.text_view_object}')["text"]
        assert actual_string == expected_string, f'The {actual_string} is not match {expected_string}'
        logging.info('Check Time option Successfully')
        return actual_string

    def get_options_menu_settings_general_date_time(self, spice, net):
        '''
        Get all options from date and time screen
        '''
        date_time_option_list = []
        date_time_option_1 = self.check_menu_settings_general_date_time_option_time_zone(spice, net)
        date_time_option_2 = self.check_menu_settings_general_date_time_option_date(spice, net)
        date_time_option_3 = self.check_menu_settings_general_date_time_option_time(spice, net)
        date_time_option_list = [date_time_option_1, date_time_option_2, date_time_option_3]
        return date_time_option_list

    def goto_menu_settings_general_datetime_date_dateformat(self,spice):
        '''
        Negative to Menu->General->Date and Time ->Date ->Date Format screen
        '''
        self.goto_menu_settings_general_dateTime_date(spice)
        date_format_item = spice.wait_for(MenuAppWorkflowObjectIds.combo_datetime_date_dateformat)
        date_format_item.mouse_click()
        date_format_screen = spice.wait_for(MenuAppWorkflowObjectIds.view_date_format_screen)
        spice.wait_until(lambda: date_format_screen["visible"] == True, 15)

    def select_date_format_option_on_dateformat_screen(self, spice, option):
        '''
        select date format option on date format screen
        '''
        spice.wait_for(MenuAppWorkflowObjectIds.item_date_format)
        if option == 'DD-MM-YYYY':
            select_button = spice.query_item(MenuAppWorkflowObjectIds.item_date_format, query_index=0)
            spice.validate_button(select_button)
            select_button.mouse_click()
            logging.info("Select DD-MM-YYYY successfully")
        elif option == 'MM-DD-YYYY':
            select_button = spice.query_item(MenuAppWorkflowObjectIds.item_date_format, query_index=1)
            spice.validate_button(select_button)
            select_button.mouse_click()
            logging.info("Select MM-DD-YYYY successfully")
        elif option == 'YYYY-MM-DD':
            select_button = spice.query_item(MenuAppWorkflowObjectIds.item_date_format, query_index=2)
            spice.validate_button(select_button)
            select_button.mouse_click()
            logging.info("Select YYYY-MM-DD successfully")
        else:
            raise Exception(f"Invalid date option{option}>")

    def verify_date_format_reflect_on_date_time_screen(self, spice, date_format):
        '''
        Verify date format reflect successfully on date time screen
        '''
        date_value = self.get_date_value_on_menu_settings_general_datetime(spice)
        get_date_format = self.get_date_format_on_datetime_screen(date_value)
        assert get_date_format == date_format, 'The date format apply on UI failed'
        logging.info("Verify date format reflect on UI successfully")

    def is_yyyymmdd_date_format_on_datetime_screen(self, date):
        '''
        Check date format if yyyymmdd
        '''
        try:
            datetime.strptime(date, '%Y/%b/%d')
            return True
        except ValueError:
            return False

    def is_mmddyyyy_date_format_on_datetime_screen(self, date):
        '''
        Check date format if mmddyyyy
        '''
        try:
            datetime.strptime(date, '%b/%d/%Y')
            return True
        except ValueError:
            return False

    def is_ddmmyyyy_date_format_on_datetime_screen(self, date):
        '''
        Check date format if ddmmyyyy
        '''
        try:
            datetime.strptime(date, '%d/%b/%Y')
            return True
        except ValueError:
            return False

    def get_date_format_on_datetime_screen(self, date):
        '''
        get the date format for the current date
        '''
        if self.is_yyyymmdd_date_format_on_datetime_screen(date):
            logging.info("The date format is YYYY-MM-DD")
            date_format = 'YYYY-MM-DD'
        elif self.is_mmddyyyy_date_format_on_datetime_screen(date):
            logging.info("The date format is MM-DD-YYYY")
            date_format = 'MM-DD-YYYY'
        elif self.is_ddmmyyyy_date_format_on_datetime_screen(date):
            logging.info("The date format is DD-MM-YYYY")
            date_format = 'DD-MM-YYYY'
        else:
            raise Exception(f"Invalid date <{date}>")

        return date_format

    def goto_menu_settings_general_datetime_time_timeformat(self,spice):
        '''
        Negative to Menu->General->Date and Time ->Time ->Time Format screen
        '''
        self.goto_menu_settings_general_dateTime_time(spice)
        time_format_item = spice.wait_for(MenuAppWorkflowObjectIds.combo_datetime_time_dateformat)
        time_format_item.mouse_click()
        time_format_screen = spice.wait_for(MenuAppWorkflowObjectIds.view_time_format_screen)
        spice.wait_until(lambda: time_format_screen["visible"] == True, 15)

    def select_time_format_option_on_timeformat_screen(self, spice, option):
        '''
        select time format option on time format screen
        option: string ->hr12 or hr24
        '''
        if option == 'hr12':
            select_button = spice.wait_for(MenuAppWorkflowObjectIds.item_time_format_12hr)
            spice.validate_button(select_button)
            select_button.mouse_click()
            logging.info("Select 12hr successfully")
        elif option == 'hr24':
            select_button = spice.wait_for(MenuAppWorkflowObjectIds.item_time_format_24hr)
            spice.validate_button(select_button)
            select_button.mouse_click()
            logging.info("Select 24hr successfully")
        else:
            raise Exception(f"Invalid time option{option}>")

    def click_apply_btn_at_time_screen(self, spice):
        '''
        Click Apply button at time screen
        '''
        apply_button = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        spice.validate_button(apply_button)
        apply_button.mouse_click()

    def get_time_value_on_menu_settings_general_dateTime(self, spice):
        '''
        Get time value on date and time screen
        '''
        time = spice.query_item(MenuAppWorkflowObjectIds.text_view_date_time_time)["text"]
        return time

    def is_ampm_time_format_on_datetime_screen(self, time):
        '''
        Check time format if 12 hr
        '''
        try:
            datetime.strptime(time, '%I:%M %p')
            return True
        except ValueError:
            return False

    def get_time_format_on_datetime_screen(self, time):
        '''
        get the time format for the current time
        '''
        if self.is_ampm_time_format_on_datetime_screen(time):
            logging.info("The time format is hr12")
            time_format = 'hr12'
        else:
            logging.info("The time format is hr24")
            time_format = 'hr24'

        return time_format

    def verify_time_format_reflect_on_date_time_screen(self, spice, time_format):
        '''
        Verify time format reflect successfully on date time screen
        '''
        # wait seconds to avoid to get default value
        time.sleep(2)
        time_value = self.get_time_value_on_menu_settings_general_dateTime(spice)
        get_time_format = self.get_time_format_on_datetime_screen(time_value)
        assert get_time_format == time_format, 'The time format apply on UI failed'
        logging.info("Verify time format reflect on UI successfully")


    def get_time_zone_value_on_menu_settings_general_dateTime(self, spice):
        '''
        Get time zone value on date and time screen
        '''
        time_zone_item = spice.wait_for(MenuAppWorkflowObjectIds.text_view_date_time_time_zone)
        # wait 1 secons to wait correct text show, to skip get default text
        time.sleep(1)
        return time_zone_item["text"]

    def verify_time_zone_reflect_on_date_time_screen(self, spice, net, time_zone):
        '''
        Verify time zone reflect successfully on date time screen
        '''
        actual_time_zone_value = self.get_time_zone_value_on_menu_settings_general_dateTime(spice)
        expected_time_zone_value = LocalizationHelper.get_string_translation(net, self.time_zone_option_dict[time_zone])
        assert actual_time_zone_value == expected_time_zone_value, 'The date format apply on UI failed'
        logging.info("Verify date format reflect on UI successfully")


    def set_menu_settings_general_date_time_date(self, spice, date, month, year, data_format="DD-MM-YYYY"):
        """
        set menu settings general date time date
        UI should be in Menu -> Settings-> General -> Date and Time -> Date screen
        data_format: must be in "DD-MM-YYYY"/"MM-DD-YYYY"/"YYYY-MM-DD"
        """
        if data_format == "DD-MM-YYYY":
            self.set_menu_settings_general_date_time_date_day(spice, date, data_format)
            self.set_menu_settings_general_date_time_date_month(spice, month)
            self.set_menu_settings_general_date_time_date_year(spice, year, data_format)
        elif data_format == "MM-DD-YYYY":
            self.set_menu_settings_general_date_time_date_month(spice, month)
            self.set_menu_settings_general_date_time_date_day(spice, date, data_format)
            self.set_menu_settings_general_date_time_date_year(spice, year, data_format)
        elif data_format == "YYYY-MM-DD":
            self.set_menu_settings_general_date_time_date_year(spice, year, data_format)
            self.set_menu_settings_general_date_time_date_month(spice, month)
            self.set_menu_settings_general_date_time_date_day(spice, date, data_format)
        else:
            raise Exception(f"Data format <{data_format}> is invalid, please select correct fata format.")
        self.click_apply_btn_at_date_screen(spice)
    
    def click_apply_btn_at_date_screen(self, spice):
        '''
        Click Apply button at date screen
        '''
        apply_button = spice.wait_for(MenuAppWorkflowObjectIds.date_applyButton)
        spice.validate_button(apply_button)
        apply_button.mouse_click()

    def goto_automatic_paper_advance_calibration(self, spice, cdm):
        """
        Navigates to the Automatic Paper Advance screen in Beam / Pixiu
        """
        if not spice.is_HomeScreen():
            spice.goto_homescreen()

        # Navigate to Print Quality tab if MFP
        try:
            isMfp = cdm.get_raw(cdm.SCANNER_STATUS).status_code == 200
            logging.info(f"Scanner OK: {isMfp}")
        except HTTPError as e:
            logging.info(f"Failed to get scanner status: {e}")
            isMfp = False

        spice.homeMenuUI().goto_menu_tools_troubleshooting_printquality(spice, isMfp)
        
        # Confirm that we are on the Troubleshooting app and past the "Loading" screen.
        # Must see "#TroubleShootingApplicationStackView"
        spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_app, 15)
        logging.info("[OK] Troubleshooting app is loaded")
        
        # Must NOT see "#loadingProgressContent"
        try:
            spice.query_item(MenuAppWorkflowObjectIds.loading_data_progress_content)
            assert False, "[ERROR] Stuck on Troubleshooting loading screen"
        except QmlItemNotFoundError:
            # We expect an exception to be raised
            logging.info("[OK] Troubleshooting loading screen is gone")
    
        # Select "Paper-Advance Calibration" (linefeed)
        spice.wait_for(MenuAppWorkflowObjectIds.paper_advance_calibration_option, 15).mouse_click()
        
        # Select "Automatic Paper-Advance Calibration"
        spice.wait_for(MenuAppWorkflowObjectIds.automatic_paper_advance_calibration_option, 15).mouse_click()
        
        # Click "Start" button
        spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button, 15).mouse_click()
        
    def goto_menu_settings_printerUpdate_allowUpgrades(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowUpgrades).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris)
        logging.info("At Printer Update IRIS Message Screen")

    def goto_menu_settings_printerUpdate_allowUpgrades_iris_options(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        scrollAmount = 0.8
        while (scrollAmount <= 1.2 and spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowUpgrades_next)["enabled"] == False):
            self.workflow_common_operations.scroll_to_position_vertical(scrollAmount, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
            scrollAmount += 0.1
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowUpgrades_next).mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")

    def set_printerUpdate_notifyWhenAvailable(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set Notify to true")

    def set_printerUpdate_doNotCheck(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotcheck).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set Do Not Check to true")

    def set_printerUpdate_allowAutoUpdate_goto_iris_message_screen(self, spice, net):
        self.set_printerUpdate_allowAutoUpdate(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        auto_update_note = spice.wait_for("#alertDetailDescription #textColumn #contentItem")["text"]
        assert LocalizationHelper.get_string_translation(net, "cAutoRecommendedCP", "en") in auto_update_note
        spice.wait_for("#Continue").mouse_click()

    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, net, enterNav=True):
        self.set_printerUpdate_notifyWhenAvailable(spice, enterNav)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        notify_when_available_note = spice.wait_for("#alertDetailDescription #textColumn #contentItem")["text"]
        assert LocalizationHelper.get_string_translation(net, "cNotifyWhenAvailableCP", "en") in notify_when_available_note
        spice.wait_for("#Continue").mouse_click()

    def menu_settings_General_Datetime_SystemtimeChange (self, spice):
        #set system time as 9 hours and 0 minute
        self.menu_settings_General_Datetime_SetSystemTime(spice,9,0)

    def find_positive_integer_key_pad(self,number):
        key_value = positive_integer_key_pad_map[number]
        return(key_value)

    def menu_settings_General_Datetime_SetSystemTime (self, spice, given_hour, given_minute):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname=MenuAppWorkflowObjectIds.dateTime_scrollbar)
        try:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
            logging.info("At Time Settings Screen")
            try:
                spice.wait_for("#Hour #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At spinbox keyboard")
                    for digit in str(given_hour):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for Hour Spin Box: {e}")
            try:
                spice.wait_for("#Minute #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At the spinbox keyboard")

                    for digit in str(given_minute):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for Minute Spin Box: {e}")
            try:
                applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
                applyButton.mouse_click()
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for time apply button: {e}")
        except AssertionError:
            logging.info("Could not find the keyboard view")
        finally:
            spice.goto_homescreen()

    def energy_scheduleOff_set_time_day_after_schedule(self, spice, cdm, net):
        setschedhour=10
        setschedminute=0
        setsyshouraftersched=10
        setsysminuteaftersched=3

        self.menu_settings_general_energy_scheduleOnOff_setdayandtime(spice,"schedule off",setschedhour,setschedminute)
        self.validate_poweroff_scheduled_data(cdm,setschedhour,setschedminute)
        self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)

        self.menu_settings_General_Datetime_SetSystemTime(spice, setsyshouraftersched, setsysminuteaftersched)

        clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
        clock_data = clock.json()
        system_time = clock_data['systemTime']
        time_part = system_time.split('T')[1]
        hour_minute = time_part.split(':')[0:2]
        hour = int(hour_minute[0])
        minute = int (hour_minute[1])

        assert(hour==setsyshouraftersched)
        assert(minute==setsysminuteaftersched)
        return

    def menu_settings_general_energy_scheduleOnOff_setdayandtime(self,spice,given_screen,given_hour,given_minute):
        spice.homeMenuUI().goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        spice.homeMenuUI().goto_schedule_on_or_off_screen(spice, given_screen)

        logging.info("Set schedule on date and time")
        try:
            if not spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen):
                logging.info("Failed to find the schedule off screen")
                spice.goto_homescreen()
                return
            steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView, "Failed to select days option"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday, "Failed to select Sunday"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_nextButton, "Failed to click next button"),
                (MenuAppWorkflowObjectIds.view_energySettings_scheduleOnHoursView, "Failed to set hour"),
            ]
            for step, error_message in steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.warning(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return
            try:
                spice.wait_for("#timeSettingsListView #Hour #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.warning("Failed to find the spinbox keyboard:")
                logging.info("At spinbox keyboard")
                for digit in str(given_hour):
                    spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()

            except Exception as e:
                logging.info(f"Failed to set hour: {e}")
                spice.goto_homescreen()
                return

            try:
                spice.wait_for("#timeSettingsListView #Minute #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At the spinbox keyboard")
                for digit in str(given_minute):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()
            except Exception as e:
                logging.info(f"Failed to set minute to 0: {e}")
                spice.goto_homescreen()
                return

            final_steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_doneButton, "Failed to click done button"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_saveButton, "Failed to click save button"),
            ]
            for step, error_message in final_steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.info(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return
        except Exception as e:
            logging.info(f"Failed to verify schedule off {e}")
            return

    def validate_poweroff_scheduled_data(self,cdm,sethour,setminute):
        cdmPowerData = cdm.get_raw(cdm.POWER_CONFIG)
        logging.info(cdmPowerData.json())
        statusGet = cdmPowerData.status_code
        assert statusGet == 200, "status=%d" % statusGet

        # Validate powerOffScheduleEnabled as True
        assert(cdmPowerData.json()["powerOffScheduleEnabled"] == "true")

        # Validate poweroff schedule data
        hourOffset=0
        minuteOffset=0

        powerOffSchedule = cdmPowerData.json().get("powerOffSchedule", [])
        for schedule in powerOffSchedule:
            timesOfDay = schedule.get("timesOfDay", [])
            for time in timesOfDay:
                hourOffset = time.get("hourOffset")
                minuteOffset = time.get("minuteOffset")

        assert(hourOffset == sethour)
        assert(minuteOffset == setminute)
        return

    def energy_scheduleOff_set_time_day_before_schedule(self, spice, cdm, net):
        setschedhour=10
        setschedminute=0
        setsyshourbeforesched=9
        setsysminutebeforesched=57

        self.menu_settings_general_energy_scheduleOnOff_setdayandtime(spice,"schedule off",setschedhour,setschedminute)
        self.validate_poweroff_scheduled_data(cdm,setschedhour,setschedminute)
        self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)

        self.menu_settings_General_Datetime_SetSystemTime(spice, setsyshourbeforesched, setsysminutebeforesched)

        clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
        clock_data = clock.json()
        system_time = clock_data['systemTime']
        time_part = system_time.split('T')[1]
        hour_minute = time_part.split(':')[0:2]
        hour = int(hour_minute[0])
        minute = int (hour_minute[1])

        assert(hour==setsyshourbeforesched)
        assert(minute==setsysminutebeforesched)
        return

    def menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(self, spice, cdm):
        try:
            systemtime_cdm = cdm.get(cdm.CLOCK_CONFIGURATION)
            logging.info("systemtime_cdm before is = %s", systemtime_cdm)

            systemTime = cdm.get(cdm.CLOCK_CONFIGURATION)["systemTime"]
            logging.info("dayName = %s", systemTime)

            # Replacing "T" and "Z" with spaces
            s = systemTime.replace("T", " ").replace("Z", " ")
            logging.info("s = %s", s)

            # Replacing the first two occurrences of "-" with "/"
            date = s.replace("-", "/", 2)
            logging.info("date = %s", date)

            new_string = date.rstrip()
            logging.info("new_string = %s", new_string)

            # Converting the string to datetime object
            datetime_date = datetime.strptime(new_string, "%Y/%m/%d %H:%M:%S")
            logging.info("datetime_date = %s", datetime_date)

            # Printing the day of the week
            dayName = datetime_date.strftime("%A").lower()
            logging.info("day = %s", dayName)

            body = {
                "version": "1.0.0",
                "shutdownPrevention": "none",
                "powerOffScheduleEnabled": "true",
                "powerOffSchedule": [
                    {
                        "scheduleId": 0,
                        "timesOfDay": [
                            {
                                "hourOffset": 10,
                                "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            dayName
                        ]
                    }
                ]
            }

            if dayName in ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
                try:
                    r = cdm.patch_raw(cdm.POWER_CONFIG, body)
                    r = cdm.get_raw(cdm.POWER_CONFIG)
                    logging.info("CDM Value = %s", r.json())
                except Exception as e:
                    logging.info(f"Failed to update power off schedule: {e}")
            else:
                logging.info("None of the Days selected")

        except Exception as e:
            logging.info(f"An error occurred: {e}")

    def set_printerUpdate_doNotCheck_goto_iris_message_screen(self, spice, enterNav=True):
        self.set_printerUpdate_doNotCheck(spice, enterNav)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)

    def goto_menu_settings_bookletSubtray(self, spice):
        """
        Navigates to the Menu > Settings > Print > Booklet Subtray menu.
        """
        self.goto_menu_settings_print_defaultprintoptions(spice)
        cdmvalue= spice.cdm.get(spice.cdm.ENGINE_SERVICECONFIG_ENDPOINT)
        # Check if BookletSubtray screen exists
        try:
            if (cdmvalue["bookletSubTray"] == "true") or (cdmvalue["bookletSubTray"] == "false"):
                self.workflow_common_operations.scroll_to_position_vertical(1, "#defaultPrintOptionsMenuListScrollBar")
                self.workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtray, "#defaultPrintOptionsMenuList", scrollbar_objectname = "#defaultPrintOptionsMenuListScrollBar")
                time.sleep(2)
                self._spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtray).mouse_click()
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_bookletSubtray)
                logging.info("At Booklet Subtray Settings Screen")
            else:
                logging.info("Booklet Subtray is not supported in this device")
        except:
            logging.info("Booklet Subtray is not supported in this device")

    def set_bookletSubtray_onoff(self, spice):
        """
        Sets the bookletSubTray option to ON or OFF using radio buttons.
        """
        self.goto_menu_settings_print_defaultprintoptions(spice)
        cdmvalue= spice.cdm.get(spice.cdm.ENGINE_SERVICECONFIG_ENDPOINT)
        # Check if BookletSubtray screen exists
        try:
            if (cdmvalue["bookletSubTray"] == "true") or (cdmvalue["bookletSubTray"] == "false"):
                self.workflow_common_operations.scroll_to_position_vertical(1, "#defaultPrintOptionsMenuListScrollBar")
                self.workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtray, "#defaultPrintOptionsMenuList", scrollbar_objectname = "#defaultPrintOptionsMenuListScrollBar")
                bookletSubtray_value = self._spice.wait_for(MenuAppWorkflowObjectIds.text_view_bookletSubtray)
                time.sleep(2)
                self._spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtray).mouse_click()
                # Wait for the radio buttons to be present
                on_radio = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtrayON_radioButton)
                off_radio = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_settings_print_defaultprintoptions_bookletSubtrayOFF_radioButton)

                # Click the ON radio button
                turn_on = cdmvalue["bookletSubTray"]
                logging.info(f"Booklet Subtray value is {bookletSubtray_value['text']}")
                logging.info(f"Booklet Subtray is set to {turn_on}")
                if turn_on == "true":
                    if not on_radio["checked"]:
                        on_radio.mouse_click()
                        assert on_radio["checked"] is True
                    else:
                        off_radio.mouse_click()
                        time.sleep(2)
                        assert bookletSubtray_value["text"] == "Off"
                    logging.info("Booklet Subtray set to On")
                else:
                    if not off_radio["checked"]:
                        off_radio.mouse_click()
                        assert off_radio["checked"] is True
                    else:
                        on_radio.mouse_click()
                        time.sleep(2)
                        assert bookletSubtray_value["text"] == "On"
                    logging.info("Booklet Subtray set to Off")
            else:
                logging.info("Booklet Subtray is not supported in this device")
        except:
            logging.info("Booklet Subtray is not supported in this device")

    def wait_for_toast_disappear(self, spice):
        """
        Check for the presence of a toast message in the UI.

        This method waits for the toast message to disappear within a specified timeout.

        Args:
            spice: The UI automation object used to interact with the application.

        Returns:
            None
        """
        # Set timeout of 5 seconds
        wait_until = datetime.now() + timedelta(seconds=5)
        
        # Continue checking until timeout or toast disappears
        while wait_until > datetime.now():
            # Check if toast is visible
            toast_visible = spice.check_item(MenuAppWorkflowObjectIds.view_toast_info_message) != None
            
            # If toast is not visible, exit the loop
            if not toast_visible:
                return
            
        # If we reached here, toast didn't disappear within the timeout
        assert False, "Toast message is still visible after timeout"
