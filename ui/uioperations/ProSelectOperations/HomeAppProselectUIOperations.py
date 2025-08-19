#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  sys
import logging
import time
import requests
import unicodedata

from dunetuf.ui.uioperations.BaseOperations.IHomeAppUIOperations import IHomeAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.CopyAppProSelectUIOperations import CopyAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.PrintFromUsbAppProSelectUIOperations import PrintFromUsbAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.HelpAppProSelectUIOperations import HelpAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class HomeAppProSelectUIOperations(IHomeAppUIOperations):
    MAX_WAIT_TIMEOUT_FOR_HOMESCREEN_VISIBILITY = 3
    MAX_WAIT_TIMEOUT_FOR_HOMESCREEN_ACTIVE_FOCUS = 3

    def __init__(self, spice):
        self._spice = spice
        self.homemenu = MenuAppProSelectUIOperations(self._spice)
        self.homecopy = CopyAppProSelectUIOperations(self._spice)
        self.printapp = PrintFromUsbAppProSelectUIOperations(self._spice)
        self.helpapp = HelpAppProSelectUIOperations(self._spice)
        self.maxtimeout = 120
        self.current_app_text = "#CurrentAppText"
        self.property_text = "text"
        self.proselect_common_operations = ProSelectCommonOperations(spice)

    def home_scroll_max_left(self) -> bool:
        """
            Scrolls all the way to the left on the home screen.
        """
        home_app = self.proselect_common_operations.get_element(ProSelectUIObjectIds.homeScreenView)
        if not home_app: return False
        if not self.proselect_common_operations.get_element_property(home_app, "activeFocus"): return False

        current_app_text = self.proselect_common_operations.get_element(ProSelectUIObjectIds.CurrentAppText)
        if not current_app_text: return False
        text = self.proselect_common_operations.get_element_property(current_app_text, "text")
        timeout = 0
        while (text != "Menu" and timeout < ProSelectCommonOperations.DEFAULT_WAIT_TIME_SECONDS):
            home_app.mouse_wheel(0,0)
            text = self.proselect_common_operations.get_element_property(current_app_text, "text")
            time.sleep(1)
            timeout += 1

        return text == "Menu"

    def goto_home_menu(self):
        self.homemenu.goto_menu(self._spice)
        print("At Menu App")

    def goto_home_copy(self):
        self.homecopy.goto_copy()
        print("At Copy App")

    def goto_home_print_app(self):
        self.homemenu.goto_print(self._spice,self._spice.udw,self._spice.cdm)
        logging.info("At Print App")

    def goto_home_help_app(self):
        self.helpapp.goto_help_app()
        logging.info("At Help App")

    def goto_home_supplies_app(self):
        self.homemenu.home_navigation(self._spice,app_name="Supplies",home_screen_view="#HomeScreenView")
        assert self._spice.query_item(self.current_app_text)[self.property_text] == "Supplies"
        current_item = self._spice.wait_for("#a5e59604-d216-4977-a901-4774fcacbcb4 MouseArea")
        current_item.mouse_click()
        logging.info("At Supplies App")

    def goto_home_trays_app(self):
        """
        Function to navigate to Supplies app on home screen
        Ui Flow: Any screen -> Home screen -> Trays app
        @return:
        """
        self.homemenu.home_navigation(self._spice,app_name="Trays",home_screen_view="#HomeScreenView")
        assert self._spice.query_item(self.current_app_text)[self.property_text] == "Trays"
        current_item = self._spice.wait_for("#60ce8d1a-64b1-4850-875b-5b9acfc95963 MouseArea")
        current_item.mouse_click()

    def verify_alert_toner_error(self, spice, net):
        # Creating toner error alert message
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction GUIDEDFLOW activateFlow {{flowIdentification:USED_SUPPLY_PROMPT,stateProvider: {subsystem:CARTRIDGES}}}")
        assert spice.wait_for("#usedSupplyPromptWindow")
        # current_string = spice.query_item("#alertDetailDescription SpiceText[visible=true]")["text"]
        spice.wait_for("#DetailTexts")
        current_string = spice.query_item("#DetailTexts SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cIndicatedCartridgesUsed")
        assert current_string == expected_string, "String mismatch"
        scroll = spice.wait_for("#OK")
        for i in range(0, 1500, 150):
            scroll.mouse_wheel(i, i+150)
        scroll.mouse_click()

    def goto_status_menu(self):
        self.homemenu.goto_status(self._spice)
        print("At Status Screen")

    def verify_alert_load_paper(self, spice, net):
        # Creating load paper error alert message
        spice.udw.mainApp.execute("UserPrompt PUB_triggerRequest MediaLoad")
        assert spice.wait_for("#mediaLoadFlowWindow")
        cancel_button = spice.wait_for(ProSelectUIObjectIds.cancel_button)
        cancel_button.mouse_click()

    def is_on_home_screen(self) -> bool:
        home_screen_view = self.proselect_common_operations.get_element(ProSelectUIObjectIds.homeScreenView)
        if not home_screen_view: return False
        wait_timeout = self.MAX_WAIT_TIMEOUT_FOR_HOMESCREEN_VISIBILITY
        while not self.proselect_common_operations.get_element_property(home_screen_view, "visible") and wait_timeout > 0:
            wait_timeout -= 1
            time.sleep(1)
        wait_timeout = self.MAX_WAIT_TIMEOUT_FOR_HOMESCREEN_ACTIVE_FOCUS
        while not self.proselect_common_operations.get_element_property(home_screen_view, "activeFocus") and wait_timeout > 0:
            wait_timeout -= 1
            time.sleep(1)
        return True

    def click_sign_in_button(self) -> bool:
        home_app = self.proselect_common_operations.get_element(ProSelectUIObjectIds.homeScreenView)
        if not home_app: return False
        if not self.proselect_common_operations.get_element_property(home_app, "activeFocus"): return False

        if not self.home_scroll_max_left(): return False

        current_app_text = self.proselect_common_operations.get_element(ProSelectUIObjectIds.CurrentAppText)
        if not current_app_text: return False
        text = self.proselect_common_operations.get_element_property(current_app_text, "text")
        timeout = 0
        while (text != "Sign In" and timeout < ProSelectCommonOperations.DEFAULT_WAIT_TIME_SECONDS):
            home_app.mouse_wheel(180,0)
            text = self.proselect_common_operations.get_element_property(current_app_text, "text")
            time.sleep(1)
            timeout += 1
        if text != "Sign In": return False

        sign_in_button = self.proselect_common_operations.get_element(ProSelectUIObjectIds.HomeSignInButton)
        if not sign_in_button: return False

        return self.proselect_common_operations.click(sign_in_button)

    def verify_alert_cartridges_low(self, spice, cdm, configuration):
        color_supported = cdm.device_feature_cdm.is_color_supported()
        dict_supply = {1:'#cartridgeLow1Window', 2:'#cartridgeLow2Window', 3:'#cartridgeLow3Window', 4:"#cartridgeLow4Window"}
        supply_icon = "#alertStatusImage"
        try:
            # Creating cartridge low alert message
            if color_supported:
                for n in dict_supply:
                    spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification: 'CARTRIDGE_LOW',instanceId: " + str(n) + "}}")
            else:
                spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
            spice.wait_until(lambda:cdm.alerts.is_alert_present("cartridgeLow"), timeout=20, current_state_method=cdm.alerts.get_alert_list)
            spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
            spice.suppliesapp.press_alert_button("#OK")
            assert True == spice.is_HomeScreen(), "Control panel is not in Home screen"
            logging.debug("Alert cleared successfully")
        finally:
            # Removing the error using UDW command
            if color_supported:
                for n in dict_supply:
                    spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification: 'CARTRIDGE_LOW',instanceId: " + str(n) + "}}")
            else:
                spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
            spice.statusCenter_dashboard_collapse()

    def has_persistent_header(self) -> bool:
        """
        Persistent Header is only available on Workflow 2 UI

        Args:
            No arguments
        
        Returns:
            bool: False - Workflow will not have persistent header (Only Workflow 2)
        
        Raises:
            None
        """
        return False   

    def goto_home_usb_drive_folder(self):
        # make sure that you are in home screen
        self.homemenu.home_navigation(
            spice=self._spice,
            home_screen_view="#HomeScreenView",
            app_name="USB Drive",
            current_app_text=self.current_app_text,
            property_text=self.property_text,
            max_cancel_time=self.maxtimeout
        )
        logging.info("Entering USB")
        logging.debug("CurrentAppText Option Name after mouse wheel operation: {0}".format(self._spice.query_item("#CurrentAppText")["text"]))
        logging.debug("Spice Objects from current screen :: {0}".format(self._spice.udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
        adminApp = self._spice.wait_for("#USBDriveFolderGUID")
        adminApp.mouse_click()
        # make sure you are in the USB Drive option
        logging.info("clicked on usb icon on home screen")
        # adding the log statement to make sure the click has happened and entered into print screen
        logging.debug("Spice Objects from current screen :: {0}".format(self._spice.udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
        sku_result = self._spice.cdm.get(self._spice.cdm.IDENTITY_URL)['skuIdentifier']
        logging.debug("sku type of simulator:" +sku_result)
        assert self._spice.wait_for("#nativeStackView #USBDriveFolderGUID #ButtonListLayout") ["visible"] is True,"Not entered into usb drive screen"
        assert self._spice.wait_for("#ButtonListLayout #Header #Version1Text") ["text"] == "USB Drive"
        logging.info("Entered into the USB Drive screen")

