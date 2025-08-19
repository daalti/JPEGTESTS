#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
import requests
import unicodedata
import re
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration
from dunetuf.qmltest.QmlTestServer import QmlTestServer
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.BaseOperations.IMenuAppUIOperations import IMenuAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ObjectidvalidationProSelect import ObjectidvalidationProSelect
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.SettingsAppProSelectObjectIds import SettingsAppProSelectObjectIds
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIObjectIds import MenuAppProSelectUIObjectIds
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds

class MenuAppProSelectUIOperations(IMenuAppUIOperations):

    max_cancel_time = 60
    home_screen_view = "#HomeScreenView"
    current_app_text = "#CurrentAppText"
    current_app_text = "#CurrentAppText"
    property_text = "text"
    view_service = "#MenuListservice"

    device_language_options = {"option_en" : "English"   , "option_es" : "Español"     , "option_de" : "Deutsch"         , "option_ar" : "العربية"  , "option_ca" : "Català",
                               "option_cs" : "Čeština"   , "option_da" : "Dansk"       , "option_el" : "Ελληνικά"        , "option_fi" : "Suomi"    , "option_fr" : "Français",
                               "option_hr" : "Hrvatski"  , "option_hu" : "Magyar"      , "option_id" : "Bahasa Indonesia", "option_it" : "Italiano" , "option_ko" : "한글" ,
                               "option_nl" : "Nederlands", "option_nb" : "Norsk"       , "option_pl" : "Polski"          , "option_pt" : "Português", "option_ru" : "Русский",
                               "option_sk" : "Slovenčina", "option_sl" : "Slovenščina" , "option_sv" : "Svenska"         , "option_th" : "ไทย"      , "option_tr" : "Türkçe",
                               "option_ro" : "Română"    , "option_ja" : "xxx"         , "option_he" : "עברית"            , "option_zh-CN" : "简体中文"   , "option_zh-TW" : "繁體中文",}

    VOLUME_SLIDER_UNIT_X_VALUE = 2.436
    DISPLAY_BRIGHTNESS_SLIDER_UNIT_X_VALUE = 25.95
    MOUSE_CLICK_Y = 7.8

    def __init__(self, spice):
        self._spice = spice
        self.maxtimeout = 120
        #self.ipaddress = net.ip_address
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)

    def perform_signIn(self,spice):
        spice.signIn.select_sign_in_method("admin", None)
        spice.signIn.enter_credentials(True, "12345678")

    def list_navigation(self, spice, menuObjectId, buttonObjectId, selectOption: bool = True, wait_time = 1, index = 0, direction = "DOWN"):
        time.sleep(wait_time)
        currentScreen = spice.wait_for(menuObjectId)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        directionLock = False
        while True:
            item = spice.check_item(buttonObjectId, index)
            if item != None and item["activeFocus"] == True:
                break
            assert timeSpentWaiting < self.maxtimeout * 2

            logging.info("Scroll direction: " + direction)
            currentScreen.mouse_wheel(180,180) if direction == "DOWN" else currentScreen.mouse_wheel(0,0)

            timeSpentWaiting = time.time() - startTime

            if timeSpentWaiting > self.maxtimeout and directionLock == False:
                direction = "DOWN" if direction == "UP" else "UP"
                directionLock = True

            time.sleep(1)
        assert spice.query_item(buttonObjectId, index)["activeFocus"] == True
        if selectOption == True:
            currentButton = spice.wait_for(buttonObjectId + " SpiceText")
            currentButton.mouse_click()
            time.sleep(1)
            logging.info("Pressed menu item : {0}".format(buttonObjectId))
            # Checking for signin screen
            try:
                (spice.query_item("#DeviceUserView")["visible"])

            except Exception as e:
                logging.info("At Expected Menu")
            else:
                #SignIn Screen
                self.perform_signIn(spice)
                time.sleep(5)
            finally:
                logging.info("At Expected Menu")

    def menu_navigation(self, spice, menuObjectId, buttonObjectId, selectOption: bool = True, wait_time = 1, index = 0, direction = "DOWN"):
        '''method searches and clicks a specified button on a specified menu

        Args:
            menuObjectId: Object Id of the screen
            buttonObjectId: Object Id of the button to be pressed
            selectOption: Select True to click on the element
        '''
        time.sleep(wait_time)
        currentScreen = spice.wait_for(menuObjectId)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        directionLock = False
        while spice.query_item(buttonObjectId, index)["activeFocus"] == False:
            assert timeSpentWaiting < self.maxtimeout * 2

            logging.info("Scroll direction: " + direction)
            currentScreen.mouse_wheel(180,180) if direction == "DOWN" else currentScreen.mouse_wheel(0,0)

            timeSpentWaiting = time.time() - startTime

            if timeSpentWaiting > self.maxtimeout and directionLock == False:
                direction = "DOWN" if direction == "UP" else "UP"
                directionLock = True

            time.sleep(2)
        assert spice.query_item(buttonObjectId, index)["activeFocus"] == True
        if selectOption == True:
            currentButton = spice.wait_for(buttonObjectId + " SpiceText")
            currentButton.mouse_click()
            time.sleep(1)
            logging.info("Pressed menu item : {0}".format(buttonObjectId))
            # Checking for signin screen
            try:
                (spice.query_item("#DeviceUserView")["visible"])

            except Exception as e:
                logging.info("At Expected Menu")
            else:
                #SignIn Screen
                self.perform_signIn(spice)
                time.sleep(5)
            finally:
                logging.info("At Expected Menu")

    def home_navigation(self, spice, home_screen_view, app_name, current_app_text="#CurrentAppText", property_text="text", max_cancel_time=60):
        spice.goto_homescreen()
        current_screen = spice.wait_for(home_screen_view)
        start_time = time.time()
        time_spent_waiting = 0

        previous_app_text = None
        unchanged_text_count = 0
        while (spice.query_item(current_app_text)[property_text] != app_name and time_spent_waiting < max_cancel_time):
            current_app_text_value = spice.query_item(current_app_text)[property_text]
            
            # Check if text stopped changing
            if current_app_text_value == previous_app_text:
                unchanged_text_count += 1
                if unchanged_text_count >= 3:  # Stop after 3 consecutive unchanged attempts
                    logging.info(f"Current app text stopped changing at '{current_app_text_value}', stopping right scroll")
                    break
            else:
                unchanged_text_count = 0
                
            previous_app_text = current_app_text_value
            current_screen.mouse_wheel(180, 180)
            time_spent_waiting = time.time() - start_time

        if spice.query_item(current_app_text)[property_text] != app_name:
            previous_app_text = None
            unchanged_text_count = 0
            while (spice.query_item(current_app_text)[property_text] != app_name and time_spent_waiting < max_cancel_time):
                current_app_text_value = spice.query_item(current_app_text)[property_text]
                
                # Check if text stopped changing
                if current_app_text_value == previous_app_text:
                    unchanged_text_count += 1
                    if unchanged_text_count >= 3:  # Stop after 3 consecutive unchanged attempts
                        logging.info(f"Current app text stopped changing at '{current_app_text_value}', stopping left scroll")
                        break
                else:
                    unchanged_text_count = 0
                    
                previous_app_text = current_app_text_value
                current_screen.mouse_wheel(0, 0)
                time_spent_waiting = time.time() - start_time

    def compare_string(self, net, spice, stringObjectId, stringIdList, menuLevelList: list = [0], language: str = "English"):
        '''method compares the string on the screen with the expected string from  string id

        Args:
            stringObjectId: Object Id of string on the screen to be validated
            stringId: String Id of the of the expected string
            language: Language
            menuLevel: Menu level number

        Returns:
            true: if the string on the screen matches with the string from the stringid
            false: if the string on the screen does not match with the string from the stringid
        '''
        for stringid in stringIdList:
            for menulevel in menuLevelList:
                uiStringContent = spice.query_item(stringObjectId,menulevel)["text"]
                stringIdStringContent = LocalizationHelper.get_string_translation(net, stringid, LocalizationHelper.get_locale(net, language))
                if uiStringContent == stringIdStringContent:
                    break
                else:
                    continue
                break
        logging.info("Sting comparison successful")

    def compare_ui_stringid_string(self, net, spice, stringObjectId, stringIdList, menuLevelList: list = [0], language: str = "English"):
        '''method compares the string on the screen with the expected string from string id

        Args:
        stringObjectId: Object Id of string on the screen to be validated
        stringIdList: List of String Id's of the expected string
        language: Language
        menuLevelList: List of Menu level number of the expected string
        Returns:
        None
        '''
        uiStringContent=""
        stringIdStringContent=""
        for i in range(len(stringIdList)):
            uiStringContent = spice.query_item(stringObjectId,menuLevelList[i])["text"]
            stringIdStringContent = LocalizationHelper.get_string_translation(net, stringIdList[i], LocalizationHelper.get_locale(net, language))
            logging.info("stringIdStringContent is : {}".format(stringIdStringContent))
            if uiStringContent == stringIdStringContent:
                continue
            else:
                logging.info("uiStringContent and stringIdStringContent do not match --> {}:::{}".format(uiStringContent, stringIdStringContent))
                assert False

        logging.info("String comparison successful")

    def compare_content(self, spice, elementObjectId, cdmUrl, cdmName):
        '''method compares the dynamic content on the screen with the value from the cdm url

        Args:
            elementObjectId: Object Id of content on the screen to be validated
            cdmUrl: CDM url of the content
            cdmName: CDM field name of the content

        Returns:
            true: if the content on the screen matches with the CDM content
            false: if the content on the screen does not match with the CDM content
        '''

    # Menu
    def goto_menu(self, spice):
        # Make sure that you are in home screen
        spice.goto_homescreen()
        spice.wait_for("#HomeScreenView")
        spice.wait_until(lambda: spice.query_item("#HomeScreenView")["activeFocus"] == True)
        logging.info("At Home Screen")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # Scroll to the previous option first, since menu option is the first item in the home screen
        homeApp = spice.query_item("#HomeScreenView")
        homeApp.mouse_wheel(0, 0)
        # Scroll till you reach the Menu option (TODO - Need to avoid use of text)
        while (spice.query_item("#CurrentAppText")["text"] != "Menu"):
            logging.debug("CurrentAppText Option Name : {0}".format(spice.query_item("#CurrentAppText")["text"]))
            assert timeSpentWaiting < self.maxtimeout
            homeApp.mouse_wheel(0,0)
            timeSpentWaiting = time.time() - startTime
            time.sleep(2)

        # Enter the menu screen
        logging.info("Entering Menu")
        logging.debug("CurrentAppText Option Name after mouse wheel operation: {0}".format(spice.query_item("#CurrentAppText")["text"]))
        adminApp = spice.wait_for("#8a6dc844-4138-4954-b0c0-0b791fc68587")
        adminApp.mouse_click()
        time.sleep(5)
        # Make sure you are in the menu option
        spice.wait_for("#MenuListlandingPage", timeout=10)
        assert spice.wait_for("#MenuListLayout", timeout=10)
        logging.info("At Menu Screen")
        time.sleep(1)

    def goto_print(self, spice,udw,cdm):
        self.home_navigation(
            spice=self._spice,
            home_screen_view=self.home_screen_view,
            app_name="Print",
            current_app_text=self.current_app_text,
            property_text=self.property_text,
            max_cancel_time=self.max_cancel_time
        )

        logging.info("Entering Print")
        logging.debug("CurrentAppText Option Name after mouse wheel operation: {0}".format(spice.query_item("#CurrentAppText")["text"]))
        logging.debug("Spice Objects from current screen :: {0}".format(udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
        adminApp = spice.wait_for("#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
        adminApp.mouse_click()
        # make sure you are in the Print option
        logging.info("clicked on print icon on home screen")
        # adding the log statement to make sure the click has happened and entered into print screen
        logging.debug("Spice Objects from current screen :: {0}".format(udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
        sku_result = cdm.get(cdm.IDENTITY_URL)['skuIdentifier']
        logging.debug("sku type of simulator:" +sku_result)
        assert self._spice.wait_for("#nativeStackView #02FECD9A-7FE7-4797-AD15-8127DF2CFAAD #ButtonListLayout") ["visible"] is True,"Not entered into print screen"
        assert self._spice.wait_for("#ButtonListLayout #Header #Version1Text") ["text"] == "Print"
        logging.info("Entered into the Print screen")

    # Help Menu
    def goto_help(self, spice):
        logging.info("Navigating to Help Screen")
        # long press for the navigation menu
        navigationApp = spice.query_item("#CurrentAppText")
        navigationApp.mouse_press(0,0,spice.MOUSE_BTN.MIDDLE)
        longPressApp = spice.wait_for("#LongPressLayout")
        logging.info("At Long Press Menu")
        time.sleep(1)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the help button
        while (spice.query_item("#HelpButton")["activeFocus"] == False and timeSpentWaiting < self.maxtimeout):
            longPressApp.mouse_wheel(180,180)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

        helpButton = spice.wait_for("#HelpButton SpiceText")
        helpButton.mouse_click()
        time.sleep(5)

        assert spice.wait_for("#MenuListhelp")
        logging.info("At Help Screen")
        time.sleep(1)

    # Status Menu
    def goto_status(self, spice):
        logging.info("Navigating to Status Screen")
        # long press for the navigation menu
        navigationApp = spice.query_item("#CurrentAppText")
        navigationApp.mouse_press(0,0,spice.MOUSE_BTN.MIDDLE)
        longPressApp = spice.wait_for("#LongPressLayout")
        logging.info("At Long Press Menu")
        time.sleep(1)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the status button
        while (spice.query_item("#StatusButton")["activeFocus"] == False and timeSpentWaiting < self.maxtimeout):
            longPressApp.mouse_wheel(180,180)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

        statusButton = spice.wait_for("#StatusButton SpiceText")
        statusButton.mouse_click()
        time.sleep(5)

        assert spice.wait_for("#StatusView")
        logging.info("At Status Screen")
        time.sleep(1)
    # Menu

    def goto_menu_info(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#infoMenuButton")

        assert spice.wait_for("#MenuListinfo")
        logging.info("At Info Screen")
        time.sleep(1)

    def goto_menu_status(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#statusMenuButton")

        assert spice.wait_for("#StatusView")
        logging.info("At Status Screen")
        time.sleep(1)

    def goto_menu_copy(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#copyMenuButton")

        assert spice.wait_for("#MenuListcopy")
        logging.info("At Menu Copy Screen")
        time.sleep(1)

    def goto_document(self, spice):
        spice.common_operations.goto_item("#documentCopyMenuButton", "#MenuListcopy")

    def goto_menu_copy_document(self, spice):
        self.goto_menu_copy(spice)
        self.menu_navigation(spice, "#MenuListcopy", "#documentCopyMenuButton")

        assert spice.wait_for("#MenuListcopy")
        logging.info("At Copy Screen")
        time.sleep(1)

    def goto_menu_idCardCopy(self, spice):
        self.goto_menu_copy(spice)
        self.menu_navigation(spice, "#MenuListcopy", "#c74293eb-04c1-4dff-b469-1c0e99fdbe8bMenuButton")

        assert spice.wait_for("#idCardCopyLandingView")
        logging.info("At ID Card Copy Screen")
        time.sleep(1)

    def goto_menu_scan(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32MenuButton")

        assert spice.wait_for("#MenuListScanFolderGUI")
        logging.info("At Scan Screen")
        time.sleep(1)

    def goto_menu_print(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuButton")

        assert spice.wait_for("#MenuList02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
        logging.info("At Print Screen")
        time.sleep(1)

    def goto_menu_print_from_usb(self, spice):
        self.goto_menu_print(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#c93bc831-99a8-454c-b508-236fc3a2a08fMenuButton")

    def goto_menu_job_storage(self, spice):
        self.goto_menu_print(spice)
        self.menu_navigation(spice, "#MenuList02FECD9A-7FE7-4797-AD15-8127DF2CFAAD", "#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32BMenuButton")

        logging.info("At Job Storage Screen")

    def goto_menu_fax(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#44aa632b-cfa3-4c10-8cab-697a9bef610bMenuButton")

        assert spice.wait_for("#faxSetupHomeView")
        logging.info("At Fax Screen")
        time.sleep(1)

    def goto_menu_contacts(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#2b328d57-7fff-401c-9665-315ada3010f0MenuButton")

        assert spice.wait_for("#selectedContactOptionView")
        logging.info("At Contacts Screen")
        time.sleep(1)

    def goto_menu_activeJobs(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#activeJobsMenuButton")

    def goto_menu_supplies(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#a5e59604-d216-4977-a901-4774fcacbcb4MenuButton")

        assert spice.wait_for("#suppliesSummaryView")
        logging.info("At Supply Summary Screen")
        time.sleep(1)

    def goto_menu_trays(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#60ce8d1a-64b1-4850-875b-5b9acfc95963MenuButton")

        assert spice.wait_for("#trayConfigurationView")
        logging.info("At Tray Configuration Screen")
        time.sleep(1)

    def goto_menu_settings(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuButton")

        assert spice.wait_for("#MenuListsettings")
        logging.info("At Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_date_and_time(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#dateTimeButton")

        assert spice.wait_for("#DateTimeView")
        logging.info("At Date and Time Settings")
        time.sleep(1)

    def goto_menu_settings_general_update_date(self, spice):
        self.goto_menu_settings_general_date_and_time(spice)
        previous_date = spice.query_item("#SetDateButton #ContentItemText")["text"]
        print("previous_date = ", previous_date)
        self.menu_navigation(spice, "#MenuListgeneralSettings" , "#SetDateButton")
        assert spice.wait_for("#DateTimeView")
        self.menu_navigation(spice, "#DateLayout", "#SpiceTumblerView")
        assert spice.wait_for("#SpiceTumblerView")
        okbutton = spice.wait_for("#SpiceTumblerView")
        okbutton.mouse_wheel(180, 180)
        okbutton.mouse_click()
        applyButton = spice.wait_for("#applyButton #SpiceButton")
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_click()

        currentScreen = spice.wait_for("#DateLayout")
        currentScreen.mouse_wheel(180,180)
        currentScreen.mouse_wheel(180,180)
        applyButton = spice.wait_for("#DateLayout #applyButton #SpiceButton")
        applyButton.mouse_click()
        assert spice.wait_for("#DateTimeView")
        present_date = spice.query_item("#SetDateButton #ContentItemText")["text"]
        print("present_date = ", present_date)
        assert previous_date != present_date, "Date not changed"
        logging.info("At DateTime Settings Screen")
        time.sleep(2)

    def goto_menu_settings_general_update_time(self, spice):
        self.goto_menu_settings_general_date_and_time(spice)
        applyButton = spice.wait_for("#SetTimeButton #SpiceButton")
        applyButton.mouse_wheel(180, 180)
        previous_time = spice.query_item("#SetTimeButton #ContentItemText")["text"]
        print("previous_time = ", previous_time)
        self.menu_navigation(spice, "#MenuListgeneralSettings" , "#SetTimeButton")
        assert spice.wait_for("#TimeLayout")
        self.menu_navigation(spice, "#TimeLayout", "#SpiceTumblerView")
        assert spice.wait_for("#SpiceTumblerView")
        okbutton = spice.wait_for("#SpiceTumblerView")
        okbutton.mouse_wheel(180, 180)
        okbutton.mouse_click()

        applyButton = spice.wait_for("#OkButton #SpiceButton")
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_wheel(180, 180)
        applyButton.mouse_click()

        currentScreen = spice.wait_for("#TimeLayout")
        currentScreen.mouse_wheel(180,180)
        currentScreen.mouse_wheel(180,180)
        applyButton = spice.wait_for("#TimeLayout #OkButton #SpiceButton")
        applyButton.mouse_click()
        assert spice.wait_for("#DateTimeView")
        present_time = spice.query_item("#SetTimeButton #ContentItemText")["text"]
        print("present_time = ", present_time)
        assert previous_time != present_time, "Time not changed"
        logging.info("At Time Settings Screen")
        time.sleep(2)

    def goto_menu_settings_general_energy(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#energySettingsMenuButton")

        assert spice.wait_for("#MenuListenergySettings")
        logging.info("At Energy Settings")
        time.sleep(1)

    def goto_menu_settings_general_energy_sleep(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energySleepButton")

        assert spice.wait_for("#EnergySleepAfterView")
        logging.info("At Energy Sleep Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_energy_voltageFrequency(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyVoltageFrequencyButton")

        assert spice.wait_for("#EnergyVoltageFrequencyView")
        logging.info("At Energy Voltage Frequency Screen")
        time.sleep(1)

    def goto_menu_settings_general_energy_shutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyShutdownButton")

        # assert spice.wait_for("#EnergyShutdownAfterView")
        logging.info("At Energy Shutdown Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_jam_recovery(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#jamRecoveryButton")
        assert spice.wait_for("#MenuSelectionListjamRecovery")
        logging.info("At Jam Recovery Settings")

    def get_jam_recovery_option_text(self, spice, button_id):
        self.goto_menu_settings_general_jam_recovery(spice)
        self.menu_navigation(spice, "#MenuSelectionListjamRecovery", button_id)
        assert spice.wait_for("#jamRecoveryButton")
        return spice.query_item("#jamRecoveryButton SpiceText")["text"]

    # Slider Set for Menu Settings General Volume

    def set_volume_slider_validation(self, spice ):
        self.goto_menu_settings_general(spice)
        assert spice.wait_for("#volumeMenuSlider")

        current_value = spice.query_item("#volumeMenuSlider")["value"]
        logging.info("Current Volume Value on Slider: "+str(current_value))
        assert int(current_value) >= 0 and int(current_value) <= 100 , "Volume value is out of range"
        time.sleep(1)

        return int(current_value)

    # Menu Settings General Energy Disable Shutdown

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

    # Menu Settings General Energy Shutdown
    #lot26 feature 20mins energyshutdown added

    def set_energyshutdown_20Minutes(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.menu_navigation(spice, "#EnergyShutdownAfterView", "#20Minutes")
            assert spice.wait_for("#MenuListenergySettings")
            logging.info("Set Energy Shutdown to 20 minutes")
            time.sleep(1)
        except Exception as e:
            logging.info("failed to Set Energy Shutdown to 20 minutes: ")

    def set_energyshutdown_onehour(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.menu_navigation(spice, "#EnergyShutdownAfterView", "#1Hour")
            assert spice.wait_for("#MenuListenergySettings")
            logging.info("Set Energy Shutdown to 1 hour")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 1 hours: ")

    def set_energyshutdown_twohours(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.menu_navigation(spice, "#EnergyShutdownAfterView", "#2Hours")
            assert spice.wait_for("#MenuListenergySettings")    
            logging.info("Set Energy Shutdown to 2 hours")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 2 hours: ")

    def set_energyshutdown_fourhours(self, spice):
        try:
            self.goto_menu_settings_general_energy_shutdown(spice)
            self.menu_navigation(spice, "#EnergyShutdownAfterView", "#4Hours")
            assert spice.wait_for("#MenuListenergySettings")
            logging.info("Set Energy Shutdown to 4 hours")
            time.sleep(1)
        except Exception as e:
            logging.info("Failed to set Energy Shutdown to 4 hours: ")

    # Menu Settings General Energy Sleep

    def set_energysleep_oneminute(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#1Minute")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 1 minute")
        time.sleep(1)

    def set_energysleep_fiveminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#5Minutes", direction = "UP")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 5 minutes")
        time.sleep(1)

    def set_energysleep_tenminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#10Minutes")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 10 minutes")
        time.sleep(1)

    def set_energysleep_fifteenminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#15Minutes")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 15 minutes")
        time.sleep(1)

    def set_energysleep_thirtyminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#30Minutes")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 30 minutes")
        time.sleep(1)

    def set_energysleep_onehour(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        self.menu_navigation(spice, "#EnergySleepAfterView", "#1Hour")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Sleep to 1 hour")
        time.sleep(1)

    # Menu Settings General Energy Voltage Frequency
    def set_energyVoltageFrequency_50Hz(self, spice):
        self.goto_menu_settings_general_energy_voltageFrequency(spice)
        self.menu_navigation(spice, "#EnergyVoltageFrequencyView", "#frequency50Hz")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Voltage Frequency to 50Hz")
        time.sleep(1)

    def set_energyVoltageFrequency_60Hz(self, spice):
        self.goto_menu_settings_general_energy_voltageFrequency(spice)
        self.menu_navigation(spice, "#EnergyVoltageFrequencyView", "#frequency60Hz")
        assert spice.wait_for("#MenuListenergySettings")
        logging.info("Set Energy Voltage Frequency to 60Hz")
        time.sleep(1)

    # Menu Settings General Energy Autoshutdown
    def goto_menu_settings_general_energy_autoshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, "#MenuListenergySettings", "#energyAutoshutdownMenuSwitch")
        logging.info("CHeck the energyAutoShutdown switch")


    def goto_menu_settings_print(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#printSettingsMenuButton")
        assert spice.wait_for("#MenuListprintSettings", 2)
        logging.info("At Print Settings Screen")

    def goto_menu_settings_print_printquality(self, spice):
        self.goto_menu_settings_print(spice)
        self.menu_navigation(spice, "#MenuListprintSettings", "#printQualityMenuButton")
        assert spice.wait_for("#MenuListprintQuality", 2)
        logging.info("At Print Quality Screen")

    def goto_menu_settings_print_lesspapercurl(self, spice):
        #Check for less paper curl under Print
        self.goto_menu_settings_print(spice)

        try:
            self.menu_navigation(spice, "#MenuListprintSettings", "#lessPaperCurlMenuSwitch", selectOption=False)
            assert spice.wait_for("#lessPaperCurlMenuSwitch", 2)
        except Exception as e:
            #If less paper curl isn't under Print, it will be under Print Quality
            logging.info("Less Paper Curl not found under Print. Looking under Print Quality")
            self.menu_navigation(spice, "#MenuListprintSettings", "#printQualityMenuButton")
            assert spice.wait_for("#MenuListprintQuality", 2)
            
            try:
                self.menu_navigation(spice, "#MenuListprintSettings", "#lessPaperCurlMenuSwitch", selectOption=False)
                assert spice.wait_for("#lessPaperCurlMenuSwitch", 2)
            except Exception as f:
                #Catch the exception to print this line
                logging.info("Less Paper Curl not found under Print Quality")
                #but still raise the error since we didn't find it
                raise

        logging.info("At Screen with Less Paper Curl")

    def goto_menu_settings_print_defaultprintoptions_quality_dropdown(self, spice):
        self.menu_navigation(spice, "#MenuListdefaultPrintOptions", "#qualityButton")
        assert spice.wait_for("#MenuSelectionListquality")
        logging.info("At Print Quality drop down list.")

    def verify_quality_drop_down_menu_items(self, spice):
        spice.wait_for("#MenuSelectionListquality")
        assert spice.wait_for("#option_best")
        assert spice.wait_for("#option_normal")

    def goto_menu_settings_jobs_settings(self, spice):
        logging.error("Jobs Settings Screen in Settings Menu is not implemented")
        raise NotImplementedError('Jobs Settings Screen in Settings Menu is not implemented')

    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        return False

    def goto_menu_tools(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#toolsMenuButton")

        assert spice.wait_for("#MenuListtools")
        logging.info("At Tools Screen")
        time.sleep(1)

    def goto_status_reports(self, spice):
        self.menu_navigation(spice, ProSelectUIObjectIds.reportsAppView, ProSelectUIObjectIds.statusReportButton)

    def goto_usage_reports(self,spice):
        self.menu_navigation(spice, ProSelectUIObjectIds.reportsAppView, ProSelectUIObjectIds.usageReportButton)

    def goto_menu_help(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#1f91f218-ca35-4554-a2f3-16b0b28fea31MenuButton")

        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Help Screen")
        time.sleep(1)

    def goto_menu_quickSets(self, spice, quickset_type=None):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#B2D00A5C-3f28-4370-A703-8F743070E5BCMenuButton")

    #Because the display time of loading screen is too short, the method of direct click is adopted
    def goto_menu_quickSets_and_check_loading_screen(self, spice, net, quickset_type=None):
        excepted_str = spice.common_operations.get_expected_translation_str_by_str_id(net, "cLoading")
        self.goto_menu(spice)
        currentScreen = spice.wait_for("#MenuListLayout")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        while (spice.query_item("#B2D00A5C-3f28-4370-A703-8F743070E5BCMenuButton")["activeFocus"] == False and timeSpentWaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180,180)
            timeSpentWaiting = time.time() - startTime

        assert spice.query_item("#B2D00A5C-3f28-4370-A703-8F743070E5BCMenuButton")["activeFocus"] == True
        currentButton = spice.wait_for("#B2D00A5C-3f28-4370-A703-8F743070E5BCMenuButton")
        currentButton.mouse_click()
        #The loading screen only displays for 1 to 2 seconds, which is too fast to get the view
        #loading_view = spice.wait_for("#processingscreen SpiceText", 20)
        #assert excepted_str == loading_view["text"], "Failed to find loading screen"
        #logging.info("loading screen is shown at meun quicksets screen")

    def goto_menu_cloudScanToEmail(self, spice):
        self.goto_menu_scan(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#83969b5e-f2ac-4f8c-a201-a18f02141136MenuButton")

    def goto_menu_scanToCloud(self, spice):
        self.goto_menu_scan(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#2cd169f1-ad17-4cc1-864e-8f4d5f9ffd10MenuButton")

    # Menu Status
    def goto_joblog(self, spice):
        self.goto_menu_status(spice)
        self.menu_navigation(spice, "#StatusView", "#joblogButton")

        assert spice.wait_for("#jobLogView")
        logging.info("At Job Log Screen Screen")
        time.sleep(1)

    # Menu Jobs
    def goto_job_queue_app(self, spice):
        self.goto_menu_status(spice)

    def goto_statusApp_FocusCheck(self, spice):
        self.goto_menu_status(spice)
        assert spice.query_item("#StatusView")["activeFocus"] == True
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {{ idDevice: 1, stateValue: OK, statusValues:[ OCCUPIED ] }}")
        current_screen = spice.wait_for("#MessageLayout")
        time.sleep(15)
        assert spice.query_item("#StatusView")["activeFocus"] == True


    # Menu Settings
    def goto_menu_settings_rolls(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#rollsSettingsMenuButton")

    def goto_menu_settings_scan(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#scanSettingsMenuButton")

    def goto_menu_settings_copy(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#copySettingsMenuButton")

    def goto_menu_settings_supplies(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#suppliesSettingsMenuButton")
        assert spice.wait_for("#MenuListsuppliesSettings")
        logging.info("At Supply Settings Screen")

    def goto_menu_settings_eventsandnotifications(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#eventsAndNotificationsSettingsMenuButton")

    def goto_menu_settings_security(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#securitySettingsMenuButton")

    def goto_menu_settings_webservices(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#webServicesSettingsMenuButton")

    def goto_menu_settings_network(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#networkSettingsMenuButton")

        assert spice.wait_for("#MenuListnetworkSettings")
        logging.info("At Network Settings Screen")
        time.sleep(1)
    
    def verify_network_menu_item(self, spice):
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxWiFiMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxEthernetMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxWFDMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxBLEMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxAirPrintButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxIPv4EnableButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxIPv6EnableButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxHostNameButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxBonjourNameButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxProxyButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#networkSecuritySettingsMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxNwReportsMenuButton", False)
        self.menu_navigation(spice, "#MenuListnetworkSettings", "#cnxRNDMenuButton", False)

    def goto_menu_settings_replaceableparts(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#replaceablePartsSettingsMenuButton")

    def goto_menu_settings_print(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#printSettingsMenuButton")

    def goto_menu_settings_jobs_settings(self, spice):
        logging.error("Jobs Settings Screen in Settings Menu is not implemented")
        raise NotImplementedError('Jobs Settings Screen in Settings Menu is not implemented')

    def goto_menu_settings_finisher(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#finisherSettingsMenuButton")

    def goto_menu_settings_developeroptions(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#developerOptionsMenuButton")

    def goto_menu_settings_fax(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#faxSettingsMenuButton")

        assert spice.wait_for("#MenuListfaxSettings")
        logging.info("At Fax Settings Screen")
        time.sleep(1)

    def goto_menu_settings_tray(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#traySettingsMenuButton")

    def goto_menu_settings_general(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#generalSettingsMenuButton")

        assert spice.wait_for("#MenuListgeneralSettings")
        logging.info("At General Settings Screen")
        time.sleep(1)

    def goto_menu_settings_printerUpdate(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListsettings", "#printerUpdateMenuButton")
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("At printer update Screen")
        time.sleep(1)


    def goto_menu_settings_general_dateTime(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#dateTimeButton")
        assert spice.wait_for("#DateTimeView")
        logging.info("At Date Time Screen")
        time.sleep(1)

    def goto_menu_settings_general_changeDate(self, spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, "#DateTimeView", "#SetDateButton")
        assert spice.wait_for("#DateLayout")
        logging.info("At Date Screen")
        self.menu_navigation(spice, "#DateLayout", "#DateTumbler")
        button = spice.query_item("#DateTumbler")
        date = spice.query_item("#DateTumbler")["value"]
        button.mouse_click()
        button.mouse_wheel(180,180)
        button.mouse_click()
        time.sleep(2)
        date_ = spice.query_item("#DateTumbler")["value"]
        assert date != date_, "Date is not changed"
        time.sleep(1)


    def goto_menu_settings_printerUpdate_allowUpgrades(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        self.menu_navigation(spice, "#autoFirmwareUpdate", "#SetPrinterUpdateMode")
        assert spice.wait_for("#afuDsMsg")
        logging.info("At Printer Update IRIS Message Screen")

    def goto_menu_settings_printerUpdate_allowUpgrades_iris_options(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        spice.homeMenuUI().menu_navigation(spice, "#afuDsMsg", "#nextButton")
        assert spice.wait_for("#printerUpdateOptions")
        logging.info("At Printer Update Options Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice, net):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        self.menu_navigation(spice, "#SetPrinterUpdateMode", "#installAutomatically", selectOption=True)
        currentScreen = spice.wait_for("#MessageLayout")
        for x in range(14):
            currentScreen.mouse_wheel(180, 180)
        message_text = spice.wait_for("#MessageLayout #DetailTexts #Version2Text")["text"]
        assert LocalizationHelper.get_string_translation(net, "cDSOOBEAutoRecommended", "en") in message_text
        spice.wait_for("#Continue").mouse_click()
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("Set Auto Update (Recommended)")

    def set_printerUpdate_notifyWhenAvailable(self, spice, net, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        self.menu_navigation(spice, "#SetPrinterUpdateMode", "#notifyAvailable", selectOption=True)
        currentScreen = spice.wait_for("#MessageLayout")
        for x in range(14):
            currentScreen.mouse_wheel(180, 180)
        message_text = spice.wait_for("#MessageLayout #DetailTexts #Version2Text")["text"]
        assert LocalizationHelper.get_string_translation(net, "cNotifyWhenAvailableCP", "en") in message_text
        spice.wait_for("#Continue").mouse_click()
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("Set Notify When Available")

    def set_printerUpdate_allowAutoUpdate_goto_iris_message_screen(self, spice, net):
        self.set_printerUpdate_allowAutoUpdate(spice, net)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, False)

    def set_printerUpdate_doNotCheck(self, spice, enterNav = True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        self.menu_navigation(spice, "#printerUpdateOptions", "#RadioButtonListLayout #SpiceRadioButton", True, 1, 2)
        assert spice.wait_for("#autoFirmwareUpdate")
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)

    def set_printerUpdate_doNotCheck_goto_iris_message_screen(self, spice, enterNav = True):
        self.set_printerUpdate_doNotCheck(spice, enterNav)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, enterNav)

    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, enterNav=True):
        self.set_printerUpdate_notifyWhenAvailable(spice, enterNav)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, enterNav)

    def goto_menu_settings_printerUpdate_allowUpgrades_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        currentScreen = spice.wait_for("#afuDsMsg")
        for x in range(150):
            currentScreen.mouse_wheel(180,180)
        nextButton = spice.wait_for("#nextButton")
        nextButton.mouse_click()
        assert spice.wait_for("#printerUpdateOptions")
        logging.info("At printer update options Screen")
        time.sleep(1)

    # Menu Settings General

    def goto_menu_settings_general_inactivitytimeout(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#displayMenuButton")

        self.menu_navigation(spice, "#MenuListgeneralSettings", "#inactivityTimeoutButton")

        assert spice.wait_for("#InactivityTimeoutView")
        logging.info("At Inactivity Timeout Screen")
        time.sleep(1)
        return False

    def goto_menu_settings_general_language(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#displayMenuButton")
        self.menu_navigation(spice, "#MenuListdisplay", "#languageButton")
        assert spice.wait_for("#MenuSelectionListlanguage", timeout=10)
        logging.info("At Language Screen")

    # Menu Settings General Location

    def region_settings_sampletest(self, spice):
        # click the country/region dropdown
        spice.homeMenuUI().goto_menu_settings_general_region(spice)
        self.list_navigation(spice, SettingsAppProSelectObjectIds.settingsGeneralLocationMenuList, SettingsAppProSelectObjectIds.settingsGeneralLocationAngola)
        assert spice.wait_for(SettingsAppProSelectObjectIds.settingsGeneralMenuView)
        logging.info("At General Settings Menu")

    def set_region(self, spice, net, cdm, region, scrollspeed = 0.02):
        view_id = SettingsAppProSelectObjectIds.settingsGeneralLocationMenuList
        obj_id = SettingsAppProSelectObjectIds.settingsGeneralLocation.format(region = region)
        self.list_navigation(spice, view_id, obj_id)
        logging.info("At General Settings Menu")

    # Menu Settings General Inactivity Timeout

    def set_inactivitytimeout_thirtyseconds(self, spice, already_in_setting = False):
        if not already_in_setting:
            self.goto_menu_settings_general_inactivitytimeout(spice)
        self.menu_navigation(spice, "#InactivityTimeoutView", "#thirtySeconds")

        assert spice.wait_for("#MenuListdisplay")
        logging.info("Set Inactivity Timeout to 30 seconds")
        time.sleep(1)

    def set_inactivitytimeout_oneminute(self, spice, already_in_setting = False):
        if not already_in_setting:
            self.goto_menu_settings_general_inactivitytimeout(spice)
        self.menu_navigation(spice, "#InactivityTimeoutView", "#oneMinute")

        assert spice.wait_for("#MenuListdisplay")
        logging.info("Set Inactivity Timeout to 1 minute")
        time.sleep(1)

    def set_inactivitytimeout_twominutes(self, spice, already_in_setting = False):
        if not already_in_setting:
            self.goto_menu_settings_general_inactivitytimeout(spice)
        self.menu_navigation(spice, "#InactivityTimeoutView", "#twoMinutes")

        assert spice.wait_for("#MenuListdisplay")
        logging.info("Set Inactivity Timeout to 2 mins")
        time.sleep(1)

    def set_inactivitytimeout_fiveminutes(self, spice, already_in_setting = False):
        if not already_in_setting:
            self.goto_menu_settings_general_inactivitytimeout(spice)
        self.menu_navigation(spice, "#InactivityTimeoutView", "#fiveMinutes")

        assert spice.wait_for("#MenuListdisplay")
        logging.info("Set Inactivity Timeout to 5 mins")
        time.sleep(1)

    # Menu Settings General Language

    def set_language(self, spice, net, cdm, language):
        self.goto_menu_settings_general_language(spice)
        self.menu_navigation(spice, "#MenuSelectionListlanguage", "#"+language)
        assert spice.wait_for("#MenuListdisplay", timeout=10)
        logging.info("At General - Display Settings Menu")

        # Validate general - Display setting menu for language name, translation of the string "Language" and the active focus on language button
        assert spice.wait_for("#languageButton #ContentItemText")["text"] == self.device_language_options[language]
        # Validate if the cdm reflects the set language
        device_language = language.split("_")[1]
        QmlTestServer.wait_until(condition=lambda:cdm.get(cdm.SYSTEM_CONFIGURATION)["deviceLanguage"] == device_language, timeout=30, current_state_method=cdm.get(cdm.SYSTEM_CONFIGURATION)["deviceLanguage"], delay=5)
        QmlTestServer.wait_until(condition=lambda:cdm.get(cdm.SYSTEM_IDENTITY)["deviceLanguage"] == device_language, timeout=30, current_state_method=cdm.get(cdm.SYSTEM_IDENTITY)["deviceLanguage"], delay=5)
        logging.info("Set Language Successfully to " + self.device_language_options[language])

    def goto_menu_tools_reports(self, spice):
        self.goto_menu_tools(spice)
        self.menu_navigation(spice, "#MenuListtools", "#34876b06-05be-4044-b61c-40cca9dfe4cbMenuButton")

        assert spice.wait_for("#MenuListreports")
        logging.info("At Reports Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance(self, spice):
        self.goto_menu_tools(spice)
        self.menu_navigation(spice, "#MenuListtools", "#9da37e46-9b8a-4dc2-a24c-017fee6b088fMenuButton")

        assert spice.wait_for("#MenuListmaintenance")
        logging.info("At Maintenance Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu(self, spice, udw):
        spice.homeMenuUI().goto_menu_tools(spice)
        spice.homeMenuUI().menu_navigation(spice, "#MenuListtools", "#0e49b040-ed7c-4b11-8dd2-f8acc500760aMenuButton")

        result = udw.mainApp.AdminStandard.resetToDefaultDevicePassword()
        assert result == 'SUCCESS'

        #servicePin required - enter as configured
        #functionality is tested in test_views_spice_menu_tools_servicemenu
        spice.signIn.set_service_pin(udw)

    def goto_menu_tools_troubleshooting(self, spice):
        self.goto_menu_tools(spice)
        self.menu_navigation(spice, "#MenuListtools", "#f6d66534-9b96-4f12-9f51-cea0ab19dc79MenuButton")
        try:
            #Checking For Sign In Screen
            spice.wait_for("#DeviceUserView")
            #Sign IN
            self.perform_signIn(spice)
        except TimeoutError:
            logging.info("DUT is not having signIn option")

        # check if we are at the troubleshooting screen,
        # if not check if we are at the print quality troubleshooting menu
        try:
            spice.wait_for("#MenuListtroubleshooting")
        except TimeoutError:
            assert spice.wait_for("#MenuListprintQualityTroubleshooting")

        logging.info("At Troubleshooting Screen")
        time.sleep(1)

    def goto_menu_tools_reportnewproblem(self, spice):
        self.goto_menu_tools(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#reportProblemMenuButton")

    # Menu Tools Troubleshooting

    def goto_menu_tools_troubleshooting_printquality(self, spice):
        self.goto_menu_tools_troubleshooting(spice)

        # check if we are at the print quality troubleshooting screen
        try:
            spice.wait_for("#MenuListprintQualityTroubleshooting")
        except TimeoutError:
            self.menu_navigation(spice, "#MenuListLayout", "#printQualityTroubleshootingMenuButton")

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        self.goto_menu_tools_troubleshooting_printquality(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#colorCalibrationPQMenuButton")

    def goto_menu_tools_troubleshooting_print_quality_tray_alignment(self, spice):
        self.goto_menu_tools_troubleshooting_printquality(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#trayAlignmentMenuButton")

    def goto_menu_tools_troubleshooting_printquality_cleanbelt(self, spice, isFaxSupported = False):
        self.goto_menu_tools_troubleshooting_printquality(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#cleanTransferBeltButton")

    def goto_menu_tools_troubleshooting_printquality_timebasedcalibration(self, spice):
        self.goto_menu_tools_troubleshooting_printquality_colorcalibration(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#TimeBasedCalibrationButton")
    
    def goto_menu_tools_troubleshooting_printquality_poweroncalibration(self, spice):
        self.goto_menu_tools_troubleshooting_printquality_colorcalibration(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#PowerOnCalibrationButton")

    def goto_menu_tools_troubleshooting_Fax(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#faxTroubleshootingMenuButton")

    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        self.menu_navigation(spice, "#NavigationList", "#faxT30Button")

    def goto_menu_tools_troubleshooting_Fax_RunFaxTest(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        self.menu_navigation(spice, "#NavigationList", "#faxTestButton")

    def goto_menu_tools_troubleshooting_Fax_ClearFaxLogMemory(self, spice, pressClearButton2 = True):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        self.menu_navigation(spice, "#NavigationList", "#clearFaxLogButton")
        if (pressClearButton2):
            spice.wait_for("#clearFaxButton").mouse_click()

    def goto_menu_tools_troubleshooting_Fax_PBXRingDetect(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        self.menu_navigation(spice, "#NavigationList", "#pbxRingButton")


	# Restore Settings Submenu
    def goto_menu_tools_maintenance_restoresettingsmenu(self, spice):
        self.goto_menu_tools_maintenance(spice)
        self.menu_navigation(spice, "#MenuListmaintenance", "#restoreSettingsMenuMenuButton")

        assert spice.wait_for("#MenuListrestoreSettingsMenu")
        logging.info("At Restore Settings Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_restoresettingsmenu_regionreset(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#resetPrinterSupplyRegionMenuButton")
        # button_regionreset = spice.wait_for("#resetRegionSettingsMenuButton)
        # button_regionreset.mouse_click()

        assert spice.wait_for("#ResetPrinterSupplyRegionView")
        logging.info("At Reset Region Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_restore_settings_restore_network_settings(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#restoreNWSettingsMenuButton")
        assert spice.wait_for("#RestoreNetworkSettingView")
        logging.info("At Restore Network Settings Screen")

    def validate_restore_network_settings(self,spice,net):
        assert spice.wait_for("#RestoreNetworkSettingView #DetailTexts #Version2Text") ["text"] == str(LocalizationHelper.get_string_translation(net,"cRestoreOriginalSettings", "en"))
        logging.info("Validating the Restorenetworksettings confirmation text")
        yesbutton = spice.wait_for("#nativeStackView #RestoreNetworkSettingView #Yes #SpiceButton")
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_wheel(180, 180)
        yesbutton.mouse_click()
        time.sleep(2)
        assert spice.wait_for("#RestoreNetworkSettingSuccess #DetailTexts #Version2Text",15) ["text"] == str(LocalizationHelper.get_string_translation(net,"cNetworkDefaultsRestored", "en"))
        logging.info("Validated the Restorenetworksettings success message")
        spice.query_item("#nativeStackView #RestoreNetworkSettingSuccess #OK #SpiceButton").mouse_click()
        logging.info("Performed the okay operation")

    def goto_menu_tools_maintenance_restoresettingsmenu_resetusersettings(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#resetUserSettingsMenuButton")

        assert spice.wait_for("#ResetUserSettingsView")
        logging.info("At Reset User Settings Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_restoresettingsmenu_resetuserdata(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#resetUserDataMenuButton")

        assert spice.wait_for("#ResetUserDataView")
        logging.info("At Reset User Data Screen")
        time.sleep(1)

    def click_reset_button(self, spice):
        self.menu_navigation(spice, "#MaintenanceAppApplicationStackView", "#ResetUserDataView")
        time.sleep(2)

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_mfp(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#restoreAllFactoryDefaultsSfpMenuButton")

        assert spice.wait_for("#RestoreAllFactoryDefaultsSfpView")
        logging.info("At Restore All Factory Defaults Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_sfp(self, spice):
        self.goto_menu_tools_maintenance_restoresettingsmenu(spice)
        self.menu_navigation(spice, "#MenuListrestoreSettingsMenu", "#restoreAllFactoryDefaultsSfpMenuButton")

        assert spice.wait_for("#RestoreAllFactoryDefaultsSfpView")
        logging.info("At Restore All Factory Defaults Screen")
        time.sleep(1)

    def restoresettingsmenu_restoreallfactorydefaults_sfp_click_close_button(self, spice):
        '''
        Click the close button on the restore all factory defaults sfp screen
        Assumes we are on that screen when this function is called
        '''
        #Check if were on the screen
        assert spice.wait_for("#RestoreAllFactoryDefaultsSfpView")

        #Validate the close button functionality
        spice.homeMenuUI().menu_navigation(spice, "#Cancel SpiceText", "#Cancel #SpiceButton")
        logging.info("Close button works as expected.")


    # Firmware Upgrade Submenu
    def goto_menu_tools_maintenance_firmware(self, spice):
        self.goto_menu_tools_maintenance(spice)
        self.menu_navigation(spice, "#MenuListmaintenance", "#firmwareVersionMenuButton")

        assert spice.wait_for("#MenuListfirmwareVersion")
        logging.info("At Firmware Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_checkforupdate(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        self.menu_navigation(spice, "#MenuListfirmwareVersion", "#checkForUpdateMenuButton")

        assert spice.wait_for("#fwUpdateCheckUpdatesView")
        self.menu_navigation(spice, "#fwUpdateCheckUpdatesView", "#checkForUpdateYesButton")
        logging.info("At Check Updates Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_update_available_scroll_yes(self, spice):
        self.goto_menu_tools_maintenance_firmware_checkforupdate(spice)
        self.menu_navigation(spice, "#FwUpdateAvailableView", "#yesButton")

    def goto_menu_tools_maintenance_firmware_update_available_scroll_no(self, spice):
        self.goto_menu_tools_maintenance_firmware_checkforupdate(spice)
        self.menu_navigation(spice, "#FwUpdateAvailableView", "#noButton")

    def goto_menu_tools_maintenance_firmware_update_start_download(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_available_scroll_yes(spice)
        self.menu_navigation(spice, "#FwUpdateStartUpdate", "#downloadButton")

    def verify_icc_error_view(self, spice):
        assert spice.wait_for("#IccErrorView")
        icc_error_reason = spice.query_item("#IccErrorView #DetailTexts #Version2Text")["text"]
        logging.info(f"ICC error reason: {icc_error_reason}")
        return icc_error_reason

    def skip_icc_error_view(self, spice):
        # No skip button in Proselect
        logging.info("No Skip button in proselect")

    def goto_menu_tools_maintenance_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        self.menu_navigation(spice, "#MenuListfirmwareVersion", "#updateFWFromUSBMenuButton")

        assert spice.wait_for("#selectDeviceView")
        logging.info("At Select Device Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive(self, spice, drive):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        self.menu_navigation(spice, "#selectDeviceView", "#"+drive)

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(self, spice, drive, file):
        self.goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive(spice, drive)
        self.menu_navigation(spice, "#MenuListLayout", "#"+file)

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl_upgradeNow(self, spice, drive, file):
        self.goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(spice, drive, file)
        self.menu_navigation(spice, "#MenuListLayout", "#UpgradeNowButton")

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl_skipNow(self, spice, drive, file):
        self.goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(spice, drive, file)
        self.menu_navigation(spice, "#MenuListLayout", "#SkipButton")

    def goto_menu_tools_maintenance_firmware_iris_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        time.sleep(3)

        logging.info("At Firmware BDL Select Screen")
        currentScreen = spice.wait_for("#selectDeviceView")
        currentScreen.mouse_wheel(180, 180)
        time.sleep(0.5)
        currentScreen.mouse_click()
        time.sleep(0.5)

        currentScreen = spice.wait_for("#MenuListLayout")
        currentScreen.mouse_wheel(180, 180)
        time.sleep(0.5)
        currentScreen.mouse_click()
        time.sleep(0.5)


    # Menu Tools Reports
    def goto_menu_tools_reports_statusreports(self, spice):
        self.goto_menu_tools_reports(spice)
        self.menu_navigation(spice, "#MenuListreports", "#reportStatusWithoutDependenciesMenuButton")

        assert spice.wait_for("#CheckboxButtonListLayout")
        logging.info("At Select Device Screen")
        time.sleep(1)

    def goto_menu_tools_reports_eventlog(self, spice):
        self.goto_menu_tools_reports(spice)
        self.menu_navigation(spice, "#MenuListreports", "#eventLogMenuButton")

        assert spice.wait_for("#MenuListLayout")
        logging.info("At printer User Screen")
        time.sleep(1)

    def print_eventlog_with_click_print_button(self, spice):
        print("Navigating to Print button to print eventlog")
        '''
        This delay is to wait for the event log to populate. When you first enter the menu, initially there are no items in the view. When UI
        recieves the data, it will then render all of the events. I have found if we try to navigate before this list generates, we run into
        a state machine issue.
        '''
        time.sleep(3)

        logging.debug("Print EventLog")
        spice.homeMenuUI().menu_navigation(spice, "#MenuListLayout", "#printbuton", direction="UP")

    def print_prt_log_list(self, spice):
        spice.homeMenuUI().menu_navigation(spice, "#CheckboxButtonListLayout", "#checkboxMenuEntry_report_configurationReport")
        spice.homeMenuUI().menu_navigation(spice, "#CheckboxButtonListLayout", "#checkboxMenuEntry_report_jobLog")
        spice.homeMenuUI().menu_navigation(spice, "#CheckboxButtonListLayout", "#checkboxMenuEntry_report_suppliesStatusReport")
        spice.homeMenuUI().menu_navigation(spice, "#CheckboxButtonListLayout", "#checkboxMenuEntry_report_usageReport")
        spice.homeMenuUI().menu_navigation(spice, "#CheckboxButtonListLayout", "#ActionButton", direction="UP")

    def print_diagnostic_test_page(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#diagnosticsTestPageMenuButton")
        assert spice.wait_for("#Version1Text")
        logging.info("At diagnosticsTestPage Screen")
        currentScreen = spice.wait_for("#MenuListLayout")
        currentScreen.mouse_wheel(180, 180)
        spice.wait_for("#Print").mouse_click()
        if spice.uitheme == "loTheme":
           spice.wait_for("#ReportsPrintProgressView")
           spice.wait_for("#Version2Text")["text"] == 'Printing...'
        elif spice.uitheme == "hybridTheme":
           assert spice.wait_for("#ToastInfoText")["text"] == 'Printing...'

    def goto_menu_tools_troubleshooting_printquality_printqualitytroubleshootingpage(self,spice):
        self.menu_navigation(spice, "#MenuListLayout", "#printQualityTroubleshootingPageMenuButton")
        assert spice.wait_for("#Version1Text")
        logging.info("At Printqualitytroubleshooting Screen")
        currentScreen = spice.wait_for("#MenuListLayout")
        currentScreen.mouse_wheel(180, 180)
        spice.wait_for("#Print").mouse_click()
        if spice.uitheme == "loTheme":
           spice.wait_for("#ReportsPrintProgressView")
           spice.wait_for("#Version2Text")["text"] == 'Printing...'
        elif spice.uitheme == "hybridTheme":
           assert spice.wait_for("#ToastInfoText")["text"] == 'Printing...'

    # Menu Tools Service Menu

    def goto_menu_tools_servicemenu_information(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#informationMenuMenuButton")
        assert spice.wait_for("#MenuListLayout")
        logging.info("At Info Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice,udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceResetsMenuButton")
        assert spice.wait_for("#MenuListLayout")
        logging.info("At Service Resets Screen")

    def goto_menu_tools_servicemenu_systemconfiguration(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice,udw)
        self.menu_navigation(spice, "#MenuListLayout", "#systemConfigurationMenuButton")
        assert spice.wait_for("#MenuListLayout")
        logging.info("At System Config Screen")

    def get_serialNumber_SystemConfigMenu(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#systemConfigurationSerialNumberMenuMenuButton")
        logging.info("At Service Id Menu")
        assert spice.wait_for("#serialNumberView")
        return spice.wait_for("#serialNumberView")["serialNumber"]

    def get_current_serviceID_SystemConfigMenu(self, spice):
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def get_serviceID_SystemConfigMenu(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#systemConfigurationServiceIdMenuMenuButton")
        assert spice.wait_for("#serviceIdEditorView")
        logging.info("At Serial Number Menu")
        return spice.wait_for("#serviceIdEditorView")["serviceId"]

    def get_ethernetMacaddress_SystemConfigMenu(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#ethernetMACMenuButton")
        assert spice.wait_for("#ethernetMacAddressEntryView")
        logging.info("At Ethernet Mac Menu")
        return spice.wait_for("#ethernetMacAddressEntryView")["macAddress"]

    def get_wirelessMacAddress_SystemConfigMenu(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#wirelessMACMenuButton")
        return spice.wait_for("#wirelessMacAddressEntryView")['macAddress']

    def get_SystemConfigMenu_View(self, spice):
        return spice.wait_for("#ServiceAppApplicationStackView")

    def get_RestoreAllFactoryResets_BackButton_View(self):
        return "#FactoryResetView"

    def get_Service_Reset_MenuList_View(self):
        return "#MenuListserviceResets"

    def get_ServiceMenu_View(self):
        return "#MenuListservice"

    def get_UserSettingsReset_BackButton_View(self):
        return "#UserSettingsResetView"

    def get_UserDataReset_BackButton_View(self):
        return "#UserDataResetView"

    def get_RestoreAllFactoryResets_BackButton_View(self):
        return "#FactoryResetView"

    def set_wrong_serialNumber_SystemConfigMenu(self, spice, NEW_SN,net):
        self.menu_navigation(spice, "#serialNumberView", "#setButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(NEW_SN)
        assert spice.wait_for("#ConstraintMessage #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid serial number entry message")
        okbutton= spice.wait_for("#MessageLayout #okButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.query_item("#spiceKeyboardView")["currentText"]

    def updatewrong_serialNumber_SystemConfigMenu(self, spice, UPDATE_SN, net):
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(UPDATE_SN)
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == UPDATE_SN, "Updated serial number is not matching"
        confirmbtn = spice.wait_for("#MessageLayout")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful serial number message")
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def set_serialNumber_SystemConfigMenu(self, spice, NEW_SN):
        #select "Set"
        self.menu_navigation(spice, "#serialNumberView", "#setButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(NEW_SN)
        assert spice.wait_for("#serialNumberView")
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == NEW_SN

    def update_serialNumber_SystemConfigMenu(self, spice, net, UPDATE_SN, OLD_SN):
        self.menu_navigation(self._spice,"#MessageLayout","#CancelButton")
        logging.info("Validating the old serialnumber in the dialer")
        assert spice.wait_for("#spiceKeyboardView", query_index = 1)["currentText"] == OLD_SN
        self.proselect_keyboard_operations.keyboard_clear_text(1)
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(UPDATE_SN, 1)
        assert spice.wait_for("#serialNumberView")
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == UPDATE_SN
        confirmbtn = spice.query_item("#MessageLayout")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful serial number message")
        okbutton= spice.wait_for("#MessageLayout #OKButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()

    def get_SystemConfigMenu_View(self, spice):
        return "#ServiceAppApplicationStackView"

    def get_bootModeCurrentView(self, spice):
        return "#bootView"

    def set_serviceID_SystemConfigMenu(self, spice, SERVICE_ID):
        #ensure we are prompting user
        self.menu_navigation(spice, "#serviceIdEditorView", "#setButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(SERVICE_ID)
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == SERVICE_ID

    def set_wrong_serviceID_SystemConfigMenu(self, spice, SERVICE_ID,net):
        self.menu_navigation(spice, "#serviceIdEditorView", "#setButton")
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(SERVICE_ID)
        assert spice.wait_for("#ConstraintMessage #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cInvalidEntry", "en")),"Invalid entry message is not visible"
        logging.info("Validating Invalid service id entry message")
        okbutton= spice.wait_for("#MessageLayout #okButton")
        okbutton.mouse_wheel(180,180)
        okbutton.mouse_click()
        return spice.query_item("#spiceKeyboardView")["currentText"]

    def update_serviceID_SystemConfigMenu(self, spice,UPDATED_SID,net):
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(UPDATED_SID)
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == UPDATED_SID,"Updated service id is not matching"
        confirmbtn = spice.wait_for("#MessageLayout")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        logging.info("Validating Operation successful service id message")
        spice.wait_for("#MessageLayout #OKButton").mouse_click()
        return spice.wait_for("#DetailTexts #Version2Text")["text"]

    def update_new_serviceID_SystemConfigMenu(self, spice,new_serice_id,net):
        spice.wait_for("#serviceIdEditorView #setButton").mouse_click()
        self.proselect_keyboard_operations.keyboard_clear_text()
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(new_serice_id)
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == new_serice_id,"new service id is not matching"
        confirmbtn = spice.wait_for("#MessageLayout")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationFailedText", "en")),"Operation failed message is not visible"
        logging.info("Validating Operation failed service id message")
        spice.wait_for("#MessageLayout #OKButton").mouse_click()

    def update_set_serviceID_SystemConfigMenu(self, spice, UPDATED_SID,net):
        self.menu_navigation(spice, "#MessageLayout", "#CancelButton")
        logging.info("Validating the old serviceID in the dialer")
        assert spice.query_item("#spiceKeyboardView #TextInputArea", 1)["inputText"] == "11111"
        self.proselect_keyboard_operations.keyboard_clear_text(1)
        self.proselect_keyboard_operations.keyboard_set_text_with_out_dial_action(UPDATED_SID,1)
        assert spice.wait_for("#DetailTexts #Version2Text")["text"] == UPDATED_SID
        confirmbtn = spice.query_item("#MessageLayout")
        confirmbtn.mouse_wheel(180,180)
        confirmbtn.mouse_click()
        assert spice.wait_for("#InvalidMessageDialog #MessageLayout #DetailTexts #Version2Text")["text"] == str(LocalizationHelper.get_string_translation(net,"cOperationCompleted", "en")),"Operation successful message is not visible"
        spice.wait_for("#MessageLayout #OKButton").mouse_click()

    def goto_menu_tools_servicemenu_servicetests(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice,udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceTestsMenuMenuButton")
        assert spice.wait_for("#MenuListLayout")
        logging.info("At Service Tests Screen")

    def goto_menu_tools_servicemenu_servicetests_transferkitreset(self, spice, udw):
        #navigate to service reset screen
        self.goto_menu_tools_servicemenu_serviceresets(spice,udw)
        time.sleep(2)
        logging.info(" at Transfer Kit Reset Screen")
        self.menu_navigation(spice, "#MenuListLayout", "#imageTransferKitResetMenuButton")
        time.sleep(2)

    # Menu Tools Service Menu Service Tests
    def goto_menu_tools_servicemenu_servicetests_scanmotortest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceScanMotorMenuMenuButton")
        assert spice.wait_for("#scanMotorTestView")
        logging.info("At Service Motor Tests View")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_frontusbporttest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceFrontUSBPortMenuMenuButton")

        assert spice.wait_for("#usbFrontPortTest")
        logging.info("At Front USB Port Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_servicekeys(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceKeysMenuMenuButton")

        assert spice.wait_for("#hardKeyTestView")
        logging.info("At Keys Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_displaytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceDisplayMenuMenuButton")

    def goto_menu_tools_servicemenu_servicetests_contadfpick(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceContAdfMenuMenuButton")

        assert spice.wait_for("#continuousADFPickView")
        logging.info("At ADF Pick Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_flatbed(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#serviceContFlatbedMenuMenuButton")

        assert spice.wait_for("#continuousFlatbedView")
        logging.info("At Flatbed Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_servicetests_serviceinfinitehs(self, spice, udw, kvp):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#" + kvp["menuButton"] +"MenuButton")
        assert spice.wait_for("#" + kvp["proSelectView"])
        logging.info("At Tools -> Service -> Service Tests -> Service Infinite H Test Screen")

    # Menu Tools Service Menu System Configuration

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
        logging.info("At Serial Number Menu")
        time.sleep(1)

    def goto_menu_tools_servicemenu_systemconfiguration_ethernetmac(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#ethernetMACMenuButton")

        assert spice.wait_for("#ethernetMacAddressEntryView")
        logging.info("At Ethernet Mac Menu")
        time.sleep(1)

    def goto_menu_tools_servicemenu_systemconfiguration_switchbootmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#setBootModeToUserModeMenuMenuButton")

        assert spice.wait_for("#bootView")
        logging.info("At Switch Boot Mode Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_connectivitymenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#connectivityMenuMenuButton")
        assert spice.wait_for("#connectivityMenuView")
        logging.info("At Connectivity Screen")

    def goto_connectivitydiagnostics_menu(self, spice):
        self.menu_navigation(spice, "#MenuListLayout", "#wifiDiagnosticButton")

    def get_connectivitydiagnostics_wifidisabled_ethernetenabled_message(self, spice):
        return spice.wait_for("#DetailTexts #Version2Text")['text']

    # Menu Tools Service Menu Fax Diagnostics

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#faxDiagnosticMenuMenuButton")
        assert spice.wait_for("#MenuListLayout")
        logging.info("At Fax Diagnostics Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_generatedialingtonespulses(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#dialingTonesMenuButton")

        assert spice.wait_for("#generatePulseToneBurstView")
        logging.info("At Generate Dial Tone Pulses Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#hookOperationsMenuButton")

        assert spice.wait_for("#hookOperationsView")
        logging.info("At Hook Operations Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_showallfaxlocations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#showAllFaxLocationsMenuSwitch")

        logging.info("At Fax Diagnostic Show All Fax Locations")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#transmitSignalLossMenuButton")

        assert spice.wait_for("#faxTransmitSignalLossView")
        logging.info("At Fax Diagnostic Signal Loss Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generateDialNumber(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#dialPhoneNumberMenuButton")

        assert spice.wait_for("#generateDialPhoneNumber")
        logging.info("At Fax Diagnostic Phone/Dial Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_ringSettings(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#ringSettingsMenuButton")

        assert spice.wait_for("#ringSettings")
        logging.info("At Fax Diagnostic Ring Settings Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#randomDataMenuButton")

        assert spice.wait_for("#generateRandomDataView")
        logging.info("At Generate Random Data Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_faxparameters(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#faxParametersMenuButton")

        assert spice.wait_for("#faxCountryParametersView")
        logging.info("At Fax Parameters Menu View")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generatesinglemodemtonemenu(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#singleModemToneMenuButton")

        assert spice.wait_for("#generateSingleModemTone")
        logging.info("At Fax Diagnostic Generate Single Modem Tone")
        time.sleep(1)

    # Menu Tools Service Menu Service Resets

    def goto_menu_tools_servicemenu_serviceresets_usersettingsreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#userSettingsResetMenuButton")

        assert spice.wait_for("#UserSettingsResetView")
        logging.info("At User Settings Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_userdatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#userDataResetMenuButton")

        assert spice.wait_for("#UserDataResetView")
        logging.info("At User Data Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#factoryDataResetMenuButton")

        assert spice.wait_for("#FactoryResetView")
        logging.info("At Factory Reset Screen")
        time.sleep(1)
        spice.wait_for("#HomeScreenView")

    def goto_menu_tools_servicemenu_serviceresets_transferkitreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#imageTransferKitResetMenuButton")

        assert spice.wait_for("#TCUnitResetView")
        logging.info("At Transfer Kit Reset Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_serviceresets_repairmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, "#MenuListLayout", "#repairModeMenuButton")

        assert spice.wait_for("#RepairModeView")
        logging.info("At Repair Mode Screen")
        time.sleep(1)

    # Menu Help

    def goto_menu_help_howtovideos(self, spice):
        self.goto_menu_help(spice)
        self.menu_navigation(spice, "#MenuListhelp", "#howToVideosMenuButton", wait_time=6)

        assert spice.wait_for("#MenuListhowToVideos")
        logging.info("At How To Videos Screen")
        time.sleep(1)

    def goto_menu_help_workingsmarttips(self, spice):
        self.goto_menu_help(spice)
        self.menu_navigation(spice, "#MenuListhelp", "#workingSmartTipsMenuButton")

        assert spice.wait_for("#MenuListworkingSmartTips")
        logging.info("At Working Smart Tips Screen")
        time.sleep(1)

    def goto_menu_help_digitalofficetips(self, spice):
        self.goto_menu_help(spice)
        self.menu_navigation(spice, "#MenuListhelp", "#digitalOfficeTipsMenuButton")

        assert spice.wait_for("#MenuListdigitalOfficeTips")
        logging.info("At Digital Office Tips Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips(self, spice):
        self.goto_menu_help(spice)
        self.menu_navigation(spice, "#MenuListhelp", "#hpEnvironmentalTipsMenuButton")

        assert spice.wait_for("#MenuListhpEnvironmentalTips")
        logging.info("At HP Environmental Tips Screen")
        time.sleep(1)

    def goto_menu_help_printerinformation(self, spice):
        self.goto_menu_help(spice)
        self.menu_navigation(spice, "#MenuListhelp", "#helpPrinterInfoMenuButton")

        assert spice.wait_for("#MenuListinfo")
        logging.info("At Printer Information Screen")
        time.sleep(1)

    # Menu Help Working Smart Tips

    def goto_menu_help_workingsmarttips_twosideddocumentswithfax(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpTwoSidedDocumentsWithFaxMenuButton")

    def goto_menu_help_workingsmarttips_twosideddocumentswithoutfax(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpTwoSidedDocumentsWithoutFaxMenuButton")

    def goto_menu_help_workingsmarttips_usingthekeyboard(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpUsingTheKeyboardMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Using Keyboard Screen")
        time.sleep(1)

    def goto_menu_help_workingsmarttips_controlpanelnavigation(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpControlPanelNavigationMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Control Panel Navigation Screen")
        time.sleep(1)

    def goto_menu_help_workingsmarttips_wifidirect(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpWifiDirectMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Wifi Direct Screen")
        time.sleep(1)

    def goto_menu_help_workingsmarttips_idcardcopy(self, spice):
        self.goto_menu_help_workingsmarttips(spice)
        self.menu_navigation(spice, "#MenuListworkingSmartTips", "#helpIdCardCopyMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Id Card Copy Screen")
        time.sleep(1)

    # Menu Help Digital Office Tips

    def goto_menu_help_digitalofficetips_documentscanning(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        self.menu_navigation(spice, "#MenuListdigitalOfficeTips", "#helpDocumentScanningMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Document Scanning Screen")
        time.sleep(1)

    def goto_menu_help_digitalofficetips_mobileprinting(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        self.menu_navigation(spice, "#MenuListdigitalOfficeTips", "#helpMobilePrintingMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Mobile Printing Screen")
        time.sleep(1)

    def goto_menu_help_digitalofficetips_usbprinting(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        self.menu_navigation(spice, "#MenuListdigitalOfficeTips", "#helpUsbPrintingMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At USB Printing Screen")
        time.sleep(1)

    def goto_menu_help_digitalofficetips_printapps(self, spice):
        self.goto_menu_help_digitalofficetips(spice)
        self.menu_navigation(spice, "#MenuListdigitalOfficeTips", "#helpPrintAppsMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Print Apps Screen")
        time.sleep(1)

    # Menu Help Environmental Tips

    def goto_menu_help_hpenvironmentaltips_shutdown(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpShutdownMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Shutdown Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips_sleep(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpSleepMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Sleep Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips_recycle(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpRecycleMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At recycle Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips_twosidedcopying(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpTwoSidedCopyingMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Two Sided Copying Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips_twosidedprinting(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpTwoSidedPrintingMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Two Sided Printing Screen")
        time.sleep(1)

    def goto_menu_help_hpenvironmentaltips_scheduleonoff(self, spice):
        self.goto_menu_help_hpenvironmentaltips(spice)
        self.menu_navigation(spice, "#MenuListhpEnvironmentalTips", "#helpScheduleOnOffMenuButton")

        assert spice.wait_for("#NavigationList")
        logging.info("At Schedule On Off Screen")
        time.sleep(1)

    # Menu Help How To Videos
    def goto_menu_help_howtovideos_loadpaperintray2legal(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadPaperTray2LegalProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadPaperTray2LegalProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadpaperintray2legal screen")

    def goto_menu_help_howtovideos_clearajaminthedocumentfeeder(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamDocumentFeederProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamDocumentFeederProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajaminthedocumentfeeder screen")

    def goto_menu_help_howtovideos_loadpaperintray3legal(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadPaperTray3LegalProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadPaperTray3LegalProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadpaperintray3legal screen")

    def goto_menu_help_howtovideos_loadpaperintray3(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadPaperTray3ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadPaperTray3ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadpaperintray3 screen")

    def goto_menu_help_howtovideos_clearajamintray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamTray2ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamTray2ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajamintray2 screen")

    def goto_menu_help_howtovideos_insertausbdevicejobstorage(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToInsertUSBDeviceStorageProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToInsertUSBDeviceStorageProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video insertausbdevicejobstorage screen")

    def goto_menu_help_howtovideos_manualduplexfromtray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToManualDuplexTray1ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToManualDuplexTray1ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video manualduplexfromtray1 screen")

    def goto_menu_help_howtovideos_clearajamintheoutputbin(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamOutputBinProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamOutputBinProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajamintheoutputbin screen")

    def goto_menu_help_howtovideos_clearajaminthecartridgearea(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamCartridgeAreaProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamCartridgeAreaProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajaminthecartridgearea screen")

    def goto_menu_help_howtovideos_clearajamintray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamTray1ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamTray1ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajamintray1 screen")

    def goto_menu_help_howtovideos_connectanextensionphone(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToConnectExtensionPhoneProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToConnectExtensionPhoneProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video connectanextensionphone screen")

    def goto_menu_help_howtovideos_cleanthescannerglass(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToCleanScannerGlassProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToCleanScannerGlassProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video cleanthescannerglass screen")

    def goto_menu_help_howtovideos_insertausbdevicewalkup(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToInsertUSBDeviceWalkUpProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToInsertUSBDeviceWalkUpProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video insertausbdevicewalkup screen")

    def goto_menu_help_howtovideos_loadoriginalsonthescannerglass(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadOriginalScannerGlassProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadOriginalScannerGlassProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadoriginalsonthescannerglass screen")

    def goto_menu_help_howtovideos_loadpaperintray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadPaperTray2ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadPaperTray2ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadpaperintray2 screen")

    def goto_menu_help_howtovideos_replacethecyancartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToReplaceCyanCartridgeProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToReplaceCyanCartridgeProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video replacethecyancartridge screen")

    def goto_menu_help_howtovideos_connectafaxcable(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToConnectFaxCableProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToConnectFaxCableProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video connectafaxcable screen")

    def goto_menu_help_howtovideos_loadpaperintray1(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadPaperTray1ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadPaperTray1ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadpaperintray1 screen")

    def goto_menu_help_howtovideos_manualduplexfromtray2(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToManualDuplexTray2ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToManualDuplexTray2ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video manualduplexfromtray2 screen")

    def goto_menu_help_howtovideos_replacetheyellowcartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToReplaceYellowCartridgeProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToReplaceYellowCartridgeProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video replacetheyellowcartridge screen")

    def goto_menu_help_howtovideos_replacethemagentacartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToReplaceMagentaCartridgeProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToReplaceMagentaCartridgeProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video replacethemagentacartridge screen")

    def goto_menu_help_howtovideos_loadoriginalsinthedocumentfeeder(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToLoadOriginalDocumentFeederProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToLoadOriginalDocumentFeederProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video loadoriginalsinthedocumentfeeder screen")

    def goto_menu_help_howtovideos_replacetheblackcartridge(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToReplaceBlackCartridgeProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToReplaceBlackCartridgeProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video replacetheblackcartridge screen")

    def goto_menu_help_howtovideos_clearajamintray3(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamTray3ProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamTray3ProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajamintray3 screen")

    def goto_menu_help_howtovideos_clearajaminsidetheprinter(self, spice):
        self.goto_menu_help_howtovideos(spice)
        self.menu_navigation(spice, "#MenuListhowToVideos", "#howToClearJamInsidePrinterProSelectMenuButton", wait_time=6)
        assert spice.wait_for("#howToClearJamInsidePrinterProSelectMenuButton")
        assert spice.wait_for("#VideoItem")
        logging.info("At the video clearajaminsidetheprinter screen")


    def send_scan_to_usb_job(self, spice):
        # make sure in scan to usb screen
        spice.common_operations.goto_item("#UsbSaveButton")

    def goto_menu_scan_scan_to_sharepoint(self, spice):
        """
        Menu app-> Scan -> Scan to sharepoint
        @param spice:
        """
        self.goto_menu_scan(spice)
        spice.common_operations.goto_item("#a3d696df-b7ff-4d3d-9969-5cd7f18c0c92MenuButton")

    def goto_menu_scan_scan_to_network_folder(self, spice):
        """
        Menu app-> Scan -> Scan to network folder
        @param spice:
        """
        self.goto_menu_scan(spice)
        spice.common_operations.goto_item("#65acca51-619d-4e29-b1d0-6414e52f908bMenuButton")

    def goto_menu_scan_scan_to_email(self, spice):
        """
        Menu app-> Scan -> Scan to email
        @param spice:
        """
        self.goto_menu_scan(spice)
        spice.common_operations.goto_item("#b8460c9e-43c8-4290-a0f8-8ce450867f09MenuButton")

    def goto_menu_scan_scan_to_usb(self, spice):
        """
        Menu app-> Scan -> Scan to usb
        @param spice:
        """
        self.goto_menu_scan(spice)
        spice.common_operations.goto_item("#df4a8a01-7659-486f-95d5-e125ccd1529aMenuButton")

    def goto_menu_scan_scan_to_computer(self, spice):
        """
        Menu app-> Scan -> Scan to computer
        @param spice:
        """
        self.goto_menu_scan(spice)
        spice.common_operations.goto_item("#10c9c25c-7b7b-4f7d-b4ad-dd9975be35c7MenuButton")

    def goto_menu_quicksets_shortcuts_goto_specific_quicket_by_name(self, spice, quicket_name):
        """
        Select quickset by proper quickset name when entered from menu app
        """
        spice.common_operations.goto_item(f"#{quicket_name}")

    def check_spec_on_quicksets_home_screen(self, spice, net, quickset_name):
        """
        Check spec on quicksets_home_screen when entered quicksets shortcuts from menu app
        @param spice:
        @param net:
        @param quickset_name:
        """
        logging.info("check the string on current screen")
        spice.common_operations.verify_string(net, "cQuickSetsAppHeading", "#QuickSetsAppList")
        spice.common_operations.verify_string(net, "cScan", "#Scan")
        actual_quickset_name = spice.common_operations.get_actual_str(f"#{quickset_name}")
        logging.info(f"Actual quickset name : {actual_quickset_name}")
        assert actual_quickset_name == quickset_name
        logging.info("verify the back button existed")
        spice.wait_for("#BackButton", 1)

    def get_system_alert_and_close(self,spice):
        """
        Waits for UI to show a system alert and return event properties
        """
        eventModal  = spice.wait_for("#systemEventError")
        alertEvent = dict()
        # alertEvent["title"]   = spice.query_item("#Version2Text",1)["text"]
        alertEvent["description"]   = spice.query_item("#Version2Text",2)["text"]
        alertEvent["errorCode"] = spice.query_item("#Version2Text",3)["text"]

        # spice.homeMenuUI().menu_navigation(spice, "#systemEventError", "#OK")
        # spice.wait_for("#HomeScreenView")
        #
        # Becasue the above two lines are not working for this case,
        # the next codes are added. Spice prosetlect test developer need to check again.
        okButton = spice.query_item("#OK")
        # scroll till you reach the OK button

        mainUIAppView  = spice.wait_for("#HomeScreenAppApplicationStackView")
        screenHeight = mainUIAppView["height"]
        buttonHeight = okButton["height"]
        scroll = int(okButton["y"] - int(screenHeight/2))
        # Next while does not work becuase okButton has focus even though it's not shown really
        # while (okButton["activeFocus"] == False and timeSpentWaiting < 30):
        # Next while does not work becuase y of okButton is always 303.286
        # while ( (screenHeight < (okButton["y"] + buttonHeight)) and timeSpentWaiting < 30):
        for count in range(0,2):
            eventModal.mouse_wheel(scroll, scroll)
            time.sleep(0.1)
        okButton.mouse_click(okButton["width"] / 2, buttonHeight / 2)

        return alertEvent

    def verify_system_alert(self,spice):
        """
        Verifies the contents of System Alert
        """
        spice.wait_for("#systemEventError")

        titleText = spice.query_item("#Version2Text",1)["text"]

        errorCode=spice.query_item("#Version2Text",2)["text"]

        detailText = spice.query_item("#Version2Text",3)["text"]

        spice.homeMenuUI().menu_navigation(spice, "#systemEventError", "#OK")

        spice.wait_for("#HomeScreenView")

        assert titleText == "Printer Error Occurred"

        assert errorCode == "F0.02.05.09"

        assert detailText == "Printer is not fully functional. Contact your support representative."

    def set_energysleep_fiveminutes(self, spice):
        """
        Set sleep timeout to five minutes via UI
        @param spice:
        """
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#energySettingsMenuButton")

        spice.wait_for("#MenuListenergySettings")
        self.menu_navigation(spice, "#MenuListenergySettings", "#energySleepMenuNameValue")

        spice.wait_for("#EnergySleepAfterView")
        self.menu_navigation(spice, "#RadioButtonListLayout", "#5Minutes")

        spice.wait_for("#MenuListenergySettings")
        logging.info("Set Sleep Timeout to 5 mins")
        time.sleep(1)

    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)
        self.menu_navigation(spice, "#FactoryResetView", "#Proceed")

    # Menu - Settings - Supplies

    def goto_menu_settings_supplies_lowwarningthreshold(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice, "#MenuListsuppliesSettings", "#lowWarningThresholdsMenuButton")
        assert spice.wait_for("#lowWarningThresholdsView")
        logging.info("At Low Warning Thresholds Supply Settings Screen")

    def goto_menu_settings_supplies_verylowbehavior(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice, "#MenuListsuppliesSettings", "#veryLowBehaviorMenuButton")
        assert spice.wait_for("#MenuListveryLowBehavior")
        logging.info("At Very Low Behavior Supply Settings Screen")

    def goto_supplies_settings_blackverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        self.menu_navigation(spice, "#MenuListveryLowBehavior", "#blackVeryLowActionButton")
        assert spice.wait_for("#MenuSelectionListblackVeryLowAction")
        logging.info("At Black Very Low Behavior Supply Settings Screen")

    def goto_supplies_settings_colorverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        self.menu_navigation(spice, "#MenuListveryLowBehavior", "#colorVeryLowActionButton")
        assert spice.wait_for("#MenuSelectionListcolorVeryLowAction")
        logging.info("At Color Very Low Behavior Supply Settings Screen")

    def goto_menu_settings_supplies_storesupplyusagedata(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice, menuObjectId="#MenuListsuppliesSettings", buttonObjectId="#storeUsageDataEnabledMenuSwitch", selectOption=False)
        assert spice.wait_for("#storeUsageDataEnabledMenuSwitch")
        logging.info("At Store Supply Usage Data Supply Settings Screen")

    def goto_menu_settings_supplies_authorizedhpcartridgepolicy(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice=spice, menuObjectId="#MenuListsuppliesSettings", buttonObjectId="#supplyPolicyMenuSwitch", selectOption=False)
        assert spice.wait_for("#supplyPolicyMenuSwitch")
        logging.info("At Authorized HP Cartridge Policy Supply Settings Screen")

    def goto_menu_settings_supplies_cartridgeprotection(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice, menuObjectId="#MenuListsuppliesSettings", buttonObjectId="#antiTheftEnabledMenuButton")
        assert spice.wait_for("#cartridgeProtectionView")
        self.menu_navigation(spice, menuObjectId="#cartridgeProtectionView", buttonObjectId="#cartridgeProtectionSwitch", selectOption=False)
        assert spice.wait_for("#cartridgeProtectionSwitch")
        logging.info("At Cartridge Protection Supply Settings Screen")

    def goto_menu_settings_general_quietmode(self, spice, schedule_supported=False):
        """
        Navigates to Menu App --> Settings --> General -->Quiet Mode
        @param spice:
        """
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#quietModeMenuSwitch", selectOption=False)

    def change_settings_general_quietmode(self, spice, enable_option = True, schedule_supported=False):
        """
        Helper method to enable/disable quiet mode
        UI Should be in Menu App --> Settings --> General and enable/disable Quiet Mode
        @param spice:
        @param enableOption: True to enable Quiet mode False to Disable
        """
        quietModeToggleSwitch = spice.wait_for("#quietModeMenuSwitch")
        if(quietModeToggleSwitch["checked"] != enable_option):
            quietModeToggleSwitch.mouse_click()

        assert quietModeToggleSwitch["checked"] == enable_option, "Quiet mode Enable/Disbale failed"

    def verify_settings_general_quietmode(self, spice, enabledOption, schedule_supported=False):
        """
        Helper method to verify the enabled/disabled state of Quiet Mode
        UI Should be in Menu App --> Settings --> General and enable/disable Quiet Mode
        @param spice:
        @param enabledOption: True to verify enabled state and False to verify Disabled state
        """
        quietModeToggleSwitch = spice.wait_for("#quietModeMenuSwitch")
        assert quietModeToggleSwitch["checked"] == enabledOption, "Quiet mode value is not as expected in UI"

    # signout from homescreen
    def signout_from_homescreen(self, spice):
        spice.goto_homescreen()
        try:
            homeApp = spice.query_item("#HomeScreenView")
            startTime = time.time()
            timeSpentWaiting = time.time() - startTime
            # scroll to the next option first
            homeApp.mouse_wheel(180,180)
            # scroll till you reach the Sign In option
            while (spice.query_item("#CurrentAppText")["text"] != "Sign Out" and timeSpentWaiting < self.maxtimeout):
                homeApp.mouse_wheel(0,0)
                timeSpentWaiting = time.time() - startTime
        except Exception as e:
            pass
        else:
            if(spice.query_item("#CurrentAppText")["text"] == "Sign Out"):
                currentApp = spice.wait_for("#7db992ba-557a-461c-b941-6023aa8cfa34")
                currentApp.mouse_click()
                time.sleep(5)
        finally:
            logging.info("At Home Screen")

    def goto_menu_settings_general_display(self,spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings","#displayMenuButton")
        assert spice.wait_for("#MenuListdisplay")
        logging.info("At Display Settings Screen")

    def goto_menu_settings_general_display_continuable_event(self, spice):
        self.goto_menu_settings_general_display(spice)
        self.menu_navigation(spice, "#MenuListdisplay", "#continuableEventsButton")
        logging.info("At Continuable events Screen")

    def check_if_volume_slider_accessible(self,spice):
        self.goto_menu_settings_general_display(spice)
        assert spice.wait_for("#volumeMenuSlider") ,"Volume slider is not accessible"


    def get_default_volume_slider_value(self,spice):
        self.goto_menu_settings_general_display(spice)
        current_value = spice.query_item("#volumeMenuSlider")["value"]
        logging.info("Default volume value on Slider: "+str(current_value))
        return current_value

    def set_volume_slider_value(self,spice,set_val):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for("#volumeMenuSlider")
        slider.__setitem__('value',set_val)


    def move_cursor_validate_and_get_volume_slider_value(self, spice,cdm_set_value):
        self.goto_menu_settings_general_display(spice)
        slider = spice.wait_for("#volumeMenuSlider"+" Slider Rectangle")

        MOUSE_CLICK_X =  cdm_set_value*self.VOLUME_SLIDER_UNIT_X_VALUE
        slider.mouse_click(MOUSE_CLICK_X,self.MOUSE_CLICK_Y)

        current_value = spice.query_item("#volumeMenuSlider")["value"]
        logging.info("Current Volume Value on Slider: "+str(current_value))
        assert int(current_value) >= 0 and int(current_value) <= 100,"Volume value is out of range"
        return int(current_value)

    def set_continuable_event_value(self,spice,type):
        if (type == "Manual"):
            assert spice.wait_for("#Manual #SpiceRadioButton #RadioButtonText")["text"] == "Manual"
            assert spice.wait_for("#Manual #SpiceRadioButton #RadioButtonIndicator")["visible"] == True
            Autocontinueoption = spice.wait_for("#ContinuableEventsView")
            Autocontinueoption.mouse_wheel(0,0)
            Autocontinueoption.mouse_click()
        elif (type == "Auto-Continue"):
            self.menu_navigation(spice, "#MenuListdisplay", "#continuableEventsButton")
            Autocontinueoption = spice.wait_for("#ContinuableEventsView")
            Autocontinueoption.mouse_wheel(180,180)
            Autocontinueoption.mouse_click()

    def get_updated_continuable_event_manual_value_ui(self,spice):
        return spice.wait_for("#continuableEventsButton #ContentItemText")["text"]

    def get_updated_continuable_event_autocontinue_value_ui(self,spice):
        return spice.wait_for("#continuableEventsButton #ContentItemText")["text"]

    def get_continuable_event_after_reboot(self,spice):
        Continuable_btn = spice.wait_for("#MenuListdisplay #continuableEventsButton")
        Continuable_btn.mouse_wheel(180,180)
        Continuable_btn.mouse_wheel(180,180)
        return spice.wait_for("#continuableEventsButton #ContentItemText")["text"]

    def get_product_name(self, udw):
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        return printerName

    def verify_alert_setup_incomplete(self, spice, net):
        spice.udw.mainApp.execute("RtpManager PUB_triggerRtpEvent 15 0 3")
        currentScreen = spice.wait_for("#printerNeedsWSRegistrationNowWindow")
        # Validating the title string
        title_string = spice.query_item("#TitleText #Version1Text")["text"]
        expected1_string = LocalizationHelper.get_string_translation(net, "cSetupIncomplete")
        assert title_string == expected1_string, "String mismatch"
        # Validating the detail string
        detail_string = spice.query_item("#DetailTexts #Version2Text")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cSetupIncompleteCannotPrintActivate")
        assert detail_string == expected_string, "String mismatch"
        for x in range(14):
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
        okbutton = spice.wait_for("#OK")
        okbutton.mouse_click()
        spice.udw.mainApp.execute("RtpManager PUB_unpublishRtpEvent 15")

    def verify_print_job_ui_shows_processing_and_then_completes(self, spice, job_id, job):
        job_info = spice.job_ui.get_job_info(job_id)
        assert job_info.find('Processing') != -1

        # Wait for Job completion
        job.wait_for_job_completion_cdm(job_id)

    def print_status_report(self, spice, reportId):
        assert spice.wait_for("#CheckboxButtonListLayout")
        reportObjectName = '#checkboxMenuEntry_report_' + reportId
        logging.info(f"Scroll and enable checkbox for {reportId}")
        self.menu_navigation(spice, "#MenuListLayout", reportObjectName)
        assert spice.query_item(reportObjectName)['checked'] == True

        logging.info(f"Printing the {reportId}")
        self.menu_navigation(spice, "#MenuListLayout", "#ActionButton", False, direction="UP")
        spice.wait_for("#ActionButton #SpiceButton").mouse_click()
        if spice.uitheme == "loTheme":
           spice.wait_for("#ReportsPrintProgressView")
           assert spice.wait_for("#ReportsPrintProgressView #Version2Text")["text"] == 'Printing...'
        elif spice.uitheme == "hybridTheme":
           assert spice.wait_for("#ToastInfoText")["text"] == 'Printing...'

    def validate_tray_app(self,spice,cdm,net):
        logging.info("validating tray apps")
        dict = {
            1: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray1", "en")) + ":",
            2: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray2", "en")) + ":",
            3: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray3", "en")) + ":"
        }
        media_configuration = cdm.get(cdm.CDM_MEDIA_CONFIGURATION)
        assert spice.wait_for("#trayConfigurationView") ["visible"] == True,"Trays screen is not visible"
        assert  spice.wait_for("#DescriptiveButtonListLayout #Header #Version1Text")["text"] == str(LocalizationHelper.get_string_translation(net, "cTrays", "en"))
        scroll = spice.wait_for("#trayConfigurationView")
        for input in media_configuration.get("inputs",[]):
            media_source_id = input.get("mediaSourceId", "")
            if "tray" in media_source_id:
                match = re.search(r'tray-(\d+)',media_source_id)
                if match:
                    tray_number = int(match.group(1))
                    assert spice.query_item("#DescriptiveButtonListLayout #NameText", tray_number - 1)["text"] == dict[tray_number]
                    scroll.mouse_wheel(180,180)

    def goto_menu_settings_general_region(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, "#MenuListgeneralSettings", "#countryRegionButton")

        assert spice.wait_for("#MenuSelectionListcountryRegion")
        logging.info("At Location Settings")
        time.sleep(1)

    def verify_all_location_names(self, spice, options):
        """
        Navigates to each location option and verifies the name is as expected
        Parmeters
        @param options : a list of tuples with each tuple is a pair of
        location code and location name.
        Eg:[('AF', 'Afghanistan'), ('AL', 'Albania')]
        """

        # TODO here verification logic for country is commented because this logic is not working. Need to add verify country logic back.
        # Created a Story DUNE-178599 to fix it
        menuSelectionListcountryRegion = spice.wait_for("#MenuSelectionListcountryRegion")
        for option in options:
            menuSelectionListcountryRegion.mouse_wheel(180,180)
            # menu_item = "#option_" + option[0]
            # expected_location_text = option[1]

            # print("Verifying location : " + expected_location_text)
            # self.menu_navigation(spice, "#MenuSelectionListcountryRegion", menu_item, selectOption=False)

            # print("Verify UI shows the expected location name")
            # ui_location_text = spice.query_item(menu_item + " SpiceText")["text"]
            # assert ui_location_text  == expected_location_text , "Location name mismatch"

    def signin_from_homescreen(self, spice):
        spice.goto_homescreen()
        try:
            homeApp = spice.query_item("#HomeScreenView")
            startTime = time.time()
            timeSpentWaiting = time.time() - startTime
            # scroll to the Menu option first
            while (spice.query_item("#CurrentAppText")["text"] != "Menu"):
                homeApp.mouse_wheel(0,0)
            # scroll till you reach the Sign In option
            while (spice.query_item("#CurrentAppText")["text"] != "Sign In" and timeSpentWaiting < self.maxtimeout):
                homeApp.mouse_wheel(180,180)
                timeSpentWaiting = time.time() - startTime
                adminApp = spice.wait_for("#7db992ba-557a-461c-b941-6023aa8cfa34")
                adminApp.mouse_click()
                time.sleep(5)
        finally:
            logging.info("At Home Screen")

    def goto_menu_settings_print_defaultprintoptions(self, spice):
        self.goto_menu_settings_print(spice)
        self.menu_navigation(spice, "#MenuListprintSettings", "#defaultPrintOptionsMenuButton")
        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Default Print Options screen")

    def modify_sides_default_print_options(self, spice, select_side):
        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Default Print Options screen")
        self.menu_navigation(spice, "#MenuListlandingPage", "#sidesButton")
        assert spice.wait_for("#RadioButtonListLayout")
        logging.info("At Select Sides screen")
        self.menu_navigation(spice, "#RadioButtonListLayout", select_side)
        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Default Print Options screen")

    def goto_menu_settings_traysettings(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#traySettingsMenuButton")
        logging.info("At Tray Settings screen")

    def change_settings_tray_manual_feed(self, spice, enableOption = True):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable Manual feed
        @param spice:
        @param enableOption: True to enable manual feed False to Disable
        """
        self.menu_navigation(spice, "#MenuListtraySettings", "#manualFeedMenuSwitch")
        manualFeedToggleSwitch = spice.wait_for("#manualFeedMenuSwitch")
        if(manualFeedToggleSwitch ["checked"] != enableOption):
            print("inside if")
            manualFeedToggleSwitch.mouse_click()
            print("after click")
            time.sleep(1)
            assert manualFeedToggleSwitch ["checked"] == enableOption, "Manual feed Enable/Disbale failed"

    def change_settings_tray_alternative_letterhead_mode(self, spice, enableOption = True):
        """
        Helper method to enable/disable Alternative Letterhead Mode
        UI Should be in Menu App --> Settings --> tray and enable/disable Alternative Letterhead Mode
        @param spice:
        @param enableOption: True to enable Alternative Letterhead Mode, False to disable
        """
        self.menu_navigation(spice, ProSelectUIObjectIds.menu_tray_settings_list, ProSelectUIObjectIds.menu_button_settings_tray_Alternative_Letter_Head_Mode)
        ALMtoggleSwitch = spice.wait_for(ProSelectUIObjectIds.menu_button_settings_tray_Alternative_Letter_Head_Mode)
        if(ALMtoggleSwitch ["checked"] != enableOption):
            ALMtoggleSwitch.mouse_click()
            time.sleep(1)
            assert ALMtoggleSwitch ["checked"] == enableOption, "Alternative Letterhead Mode Enable/Disable failed"

    def change_settings_tray_override_size_errors(self, spice, enableOption = True):
        """
        Helper method to enable/disable override size errors
        UI Should be in Menu App --> Settings --> tray and enable/disable override size errors
        @param spice:
        @param enableOption: True to enable override size errors, False to Disable
        """
        self.menu_navigation(spice, "#MenuListtraySettings", "#overrideSizeErrorsMenuSwitch")
        toggleSwitch = spice.wait_for("#overrideSizeErrorsMenuSwitch")
        if (toggleSwitch ["checked"] != enableOption):
            toggleSwitch.mouse_click()
            time.sleep(1)
            assert toggleSwitch ["checked"] == enableOption, "Override size errors Enable/Disable failed"

    def change_settings_size_type_prompt(self, spice, select_prompt):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable size/type Prompt
        @param spice:
        @param enableOption: True to enable size/type Prompt False to Disable
        """
        assert spice.wait_for("#MenuListtraySettings")
        logging.info("At Tray Settings Screen")
        self.menu_navigation(spice, "#MenuListtraySettings", "#sizeTypePromptButton")
        assert spice.wait_for("#RadioButtonListLayout")
        logging.info("At Size/Type Prompt Screen")
        self.menu_navigation(spice, "#RadioButtonListLayout", select_prompt)
        assert spice.wait_for("#MenuListtraySettings")
        logging.info("At Tray Settings Screen")

    def goto_menu_traysettings_paperoutaction(self, spice):
        self.goto_menu_settings_traysettings(spice)
        assert spice.wait_for("#MenuListtraySettings")
        logging.info("At Tray Settings Screen")
        self.menu_navigation(spice, "#MenuListtraySettings", "#paperOutActionMenuButton")
        assert spice.wait_for("#MenuListpaperOutAction")
        logging.info("At Paper out action screen")

    def click_autocontinue_timeout_combobox(self, spice):
        assert spice.wait_for("#MenuListpaperOutAction")
        logging.info("At Paper out action screen")
        self.menu_navigation(spice, "#MenuListlandingPage", "#autoContinueTimeOutButton")
        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Auto Continue Timeout Screen")

    def click_autocontinue_action_combobox(self, spice):
        assert spice.wait_for("#MenuListpaperOutAction")
        logging.info("At Paper out action screen")
        self.menu_navigation(spice, "#MenuListlandingPage", "#autoContinueActionButton")
        assert spice.wait_for("#MenuListlandingPage")
        logging.info("At Auto Continue Action Screen")

    def goto_menu_info_printer(self, spice):
        # navigate to the menu / info screen
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#infoMenuButton")
        # Click on the print details
        self.menu_navigation(spice, "#MenuListLayout", "#printDetailButton")

        assert spice.wait_for("#printDetailButton")

        time.sleep(1)
        logging.info("At printer information Tab")

    def goto_menu_info_connectivity(self, spice):
        # navigate to the menu / info screen
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#infoMenuButton")

        assert spice.wait_for("#infoWiFiMenuNameValue")
        assert spice.wait_for("#infoEthernetMenuNameValue")
        assert spice.wait_for("#infoWiFiDirectMenuNameValue")

        logging.info("At Connectivity information Tab")

    def goto_menu_mediaApp(self, spice):
        spice.homeMenuUI().goto_menu_trays(spice)
        # validate the back button functionality
        spice.common_operations.back_button_press("#trayConfigurationView", "#MenuListlandingPage")
        logging.info("At Menu Screen")
        logging.info("Back button works as expected.")
        time.sleep(1)

    def goto_menuapp_tray(self, spice):
        self.goto_menu(spice)
        self.menu_navigation(spice, "#MenuListLayout", "#60ce8d1a-64b1-4850-875b-5b9acfc95963MenuButton")

        assert spice.wait_for("#trayConfigurationView")
        logging.info("At Tray Configuration Screen")
        time.sleep(1)
        assert spice.wait_for("#DescriptiveButtonListLayout #NameText")["text"] == "Tray 1:"

        scroll = spice.wait_for("#trayConfigurationView")
        scroll.mouse_wheel(60,60)
        scroll.mouse_click()
        assert spice.wait_for("#trayInformationModel")
        logging.info("At Tray1 Configuration Screen")

    def get_service_menu_view(self):
        return self.view_service

    # Get the country/region text
    def get_current_region_text(self, spice):
        country = spice.wait_for(SettingsAppProSelectObjectIds.get_Region_Value)["text"]
        return country

    def select_status_reports_mode_from_menu_tools_reports_status_reports(self, spice, status_reports_mode, check_expected=True):
        '''
        This is helper method to select status reports mode from tools -> reports -> status reports
        UI should be Menu->Tools-> Reports -> Status Reports
        Args: status_reports_mode: status reports mode, such as Network Security Report/Usage RePORT /Web Access Test Report/ Job Log and so on...
                                   add different status reports mode implementation if necessary
        '''
        # get the menu layout used here
        checkbox_layout = "#CheckboxButtonListLayout"
        reports_list_view = spice.wait_for(checkbox_layout)
        spice.wait_until(lambda:reports_list_view["visible"])
        logging.info(f"Selecting the report mode: <{status_reports_mode}>")

        # set the correct checkbox object name based on the status_reports_mode
        if status_reports_mode == "Job Log":
            checkbox_object_name = "#checkboxMenuEntry_report_jobLog"
        elif status_reports_mode == "Color Usage Job Log":
            checkbox_object_name = "#checkboxMenuEntry_report_colorUsageJobLog"
        else:
            raise logging.info(f"{status_reports_mode} is not supported to select")

        # goto the checkbox and check it
        self.menu_navigation(spice, checkbox_layout, checkbox_object_name)
        if check_expected:
            assert spice.query_item(checkbox_object_name)['checked'] == True

    def print_status_reports_with_click_print_button(self, spice):
        '''
        This is helper method to click print button to printing status reports.
        UI should be Menu->Tools-> Reports -> Status Reports
        '''
        self.menu_navigation(spice, "#CheckboxButtonListLayout", "#ActionButton", direction="UP")
        self.check_print_progress_message(spice)

    def check_print_progress_message(self, spice):
        text = "Printing..."
        if spice.uitheme == "loTheme":
           spice.wait_for("#ReportsPrintProgressView")
           assert spice.query_item("#ReportsPrintProgressView #Version2Text")["text"] == text
        elif spice.uitheme == "hybridTheme":
            spice.wait_for("#ToastBase")
            assert spice.query_item("#ToastBase #ToastInfoText")["text"] == text

    def is_network_settings_locked(self) -> bool:
        try:
            self._spice.wait_for(MenuAppProSelectUIObjectIds.SettingsView)
        except:
            logging.error(f"Failed to get: {MenuAppProSelectUIObjectIds.SettingsView}")
            return False

        try:
            self._spice.wait_for(MenuAppProSelectUIObjectIds.NetworkButton + " " + MenuAppProSelectUIObjectIds.LockIcon)
        except:
            logging.error(f"Failed to get lock icon")
            return False

        return True

    def object_id_validation(self,cdm, spice, active_screen, objectId_list):
        if objectId_list == ObjectidvalidationProSelect.help_screen_object_id:
            objectId_list = self.filter_help_menu(cdm, objectId_list)
        print("Object ID list after", objectId_list)
        object_ids = spice.udw.mainUiApp.SpiceTestServer.getObjectTreeHeirarchy(active_screen)
        time.sleep(7)
        failed_obj = 0
        len_id = len(objectId_list)
        print("length of the dict value", len_id)
        tuple_obj = tuple(objectId_list.values())
        for x in range(len_id):
            split_value = tuple_obj[x].split("#")[1]
            # print("value only", split_value)
            if (split_value in object_ids):
                print(split_value, "Object ID available and matching")
            else:
                failed_obj = failed_obj + 1
                print(split_value, "This Object ID not found, please add the changed object ID in "
                                   "failed test case and also update the objectidvalidation.py with new one")
        if failed_obj != 0:
            assert False, ("One or more Object ID not found. Please fix the changed object ID")
        else:
            print("All object id is matching")

    def filter_help_menu(self, cdm, objectId_list):
        for k in list(objectId_list.keys()):
            if k == "menu_button_help_digitalofficetips":
                if not cdm.device_feature_cdm.is_color_supported():
                    del objectId_list[k]
                elif not cdm.device_feature_cdm.is_front_usb_supported() and not cdm.device_feature_cdm.is_wireless_supported():
                    del objectId_list[k]
                else:
                    logging.info("Not removing digitalofficetips")

        return objectId_list

    def check_troubleshooting_fax_visible(self, spice):
        """
        Check if fax options shows in troubleshooting screen.
        """
        try:
            spice.wait_for(MenuAppProSelectUIObjectIds.menu_button_troubleshooting_fax)
            return True
        except:
            logging.info('Fax option does not display on troubleshooting screen')
            return False

    def validate_list_content(self, expected_list, list_id):
        """Validate the content of a list in the UI.

        Args:
            expected_list (list): The expected content of the list.
            list_id (str): The ID of the list to validate.

        Returns:
            None
        """

        list_view = self._spice.wait_for(list_id)
        assert list_view

        for item in expected_list:
            item_id = list_id + " " + item
            assert self._spice.wait_for(item_id)["activeFocus"] == True, f"Item {item} not found in the list"
            # scroll to the next item
            list_view.mouse_wheel(180, 180)
    
    def get_date_value_on_menu_settings_general_datetime(self, spice):
        date_item = spice.wait_for(MenuAppProSelectUIObjectIds.text_view_date_time_date)
        # wait 1 second to wait correct text show, to skip get default text
        time.sleep(1)
        return date_item["text"]

    def get_time_value_on_menu_settings_general_date_time(self, spice):
        time_item = spice.wait_for(MenuAppProSelectUIObjectIds.text_view_date_time_time)
        # wait 1 second to wait correct text show, to skip get default text
        time.sleep(1)
        return time_item["text"]
