#########################################################################################
# @file     IDCardCopyAppProSelectUIOperations.py
# @authors  Shubham Khandelwal (shubham.khandelwal@hp.com)
# @date     23-08-2021
# @brief    Implementation for all the Copy UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IIDCardCopyAppUIOperation import IIDCardCopyAppUIOperation
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class IDCardCopyAppProSelectUIOperations(IIDCardCopyAppUIOperation):

    # -------------------------------Function Keywords------------------------ #
    IDCARD_COPY_UUID = "#c74293eb-04c1-4dff-b469-1c0e99fdbe8b"

    IDCARD_COPY_LANDING_VIEW = "#idCardCopyLandingView"
    IDCARD_COPY_SETTING_VIEW = "#MenuListidcopySettingsPage"

    NUMBER_OF_COPIES = "#NumberOfCopies"
    IDCARD_COPY_BUTTON = "#IDCardCopyButton"
    IDCARD_COPY_OPTION_BUTTON = "#IDCardCopyOptionsButton"


    IDCARD_COPY_SETTING_QUALITY_BUTTON = "#idcopy_qualityButton"
    IDCARD_COPY_SETTING_QUALITY_VIEW = "#MenuSelectionListidcopy_quality"
    IDCARD_COPY_SETTING_QUALITY_NORMAL_BUTTON = "#option_normal"
    IDCARD_COPY_SETTING_QUALITY_DRAFT_BUTTON = "#option_draft"
    IDCARD_COPY_SETTING_QUALITY_BEST_BUTTON = "#option_best"

    IDCARD_COPY_SETTING_COLORMODE_BUTTON = "#idcopy_colorModeButton"
    IDCARD_COPY_SETTING_COLORMODE_VIEW = "#MenuSelectionListidcopy_colorMode"
    IDCARD_COPY_SETTING_COLORMODE_COLOR_BUTTON = "#option_color"
    IDCARD_COPY_SETTING_COLORMODE_GRAYSCALE_BUTTON = "#option_grayscale"

    IDCARD_COPY_SETTING_CONTENTORIENTATION_BUTTON = "#idcopy_contentOrientationButton"
    IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW = "#MenuSelectionListidcopy_contentOrientation"
    IDCARD_COPY_SETTING_CONTENTORIENTATION_LANDSCAPE_BUTTON = "#option_landscape"
    IDCARD_COPY_SETTING_CONTENTORIENTATION_POTRAIT_BUTTON = "#option_portrait"

    IDCARD_COPY_SETTING__TRAY_BUTTON = "#idcopy_paperTrayButton"

    IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW = "#MenuSelectionListidcopy_paperTray"
    IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY1_BUTTON = "#option_tray-1"
    IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY2_BUTTON = "#option_tray-2"
    IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY3_BUTTON = "#option_tray-3"
    IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY_AUTO_BUTTON = "#option_auto"

    IDCARD_COPY_LIGHTER_DARKER_SLIDER = "#idcopy_exposureMenuSlider"

    IDCARD_COPY_START_SCREEN= "#idCardCopyStartingView"
    IDCARD_COPY_START_SCREEN_CONTINUE_BUTTON = "#idCardContinueButton"
    IDCARD_COPY_PROMPT_VIEW = "#scanManualDuplexSecondSide"
    IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON = "#Continue"
    IDCARD_COPY_PROMPT_VIEW_CANCEL_BUTTON = "#CopyCancelButton"

    IDCARD_COPY_TITLE_LOCATOR = "#LandingLayoutView #TitleText"
    COMMON_BACK_LOCATOR = "#BackButton"
    IDCARD_COPY_FACE_DOWN_HEADER = "#MessageLayout #TitleText"
    IDCARD_COPY_FACE_DOWN_BODY = "#MessageLayout #DetailTexts"

    IDCARD_COPY_OPTIONS_HEADER = "#MenuListidcopySettingsPage #Header"
    IDCARD_COPY_QUALITY_TITLE = "#idcopy_qualityMenuNameValue"
    IDCARD_COPY_ORIENTATION_TITLE = "#idcopy_contentOrientationMenuNameValue"

    IDCARD_COPY_COLOR_HEADER = "#RadioButtonListLayout  #Header"
    IDCARD_COPY_PAPERTRAY_HEADER = "#RadioButtonListLayout #Header"
    IDCARD_COPY_QUALITY_HEADER = "#RadioButtonListLayout #Header"
    IDCARD_COPY_ORIENTATION_HEADER = "#RadioButtonListLayout #Header"

    """String id"""
    IDCARD_COPY_STR_ID = "cIDCardCopyApp"
    IDCARD_COPY_BUTTON_STR_ID = "cCopy"

    IDCARD_COPY_OPTIONS_HEADER_STR_ID = "cOptions"
    IDCARD_COPY_FACE_DOWN_BODY_STR_ID = "cPlaceCardOnGlass"
    IDCARD_COPY_FLIP_BODY_STR_ID = "cFlipIDCard"
    IDCARD_COPY_COLOR_STR_ID = "cColor"
    IDCARD_COPY_PAPERTRAY_HEADER_STR_ID = "cPaperTray"
    IDCARD_COPY_PAPERTRAY_TITLE = "#idcopy_paperTrayMenuNameValue"
    IDCARD_COPY_QUALITY_HEADER_STR_ID = "cQuality"
    IDCARD_COPY_ORIENTATION_TITLE_STR_ID = "cOrientation"
    IDCARD_COPY_COLOR_GRAYSCALE_STR_ID = "cChromaticModeGrayscale"
    IDCARD_COPY_PAPERTRAY_TRAY1_STR_ID = ["cTrayN", 1]
    IDCARD_COPY_PAPERTRAY_TRAY2_STR_ID = ["cTrayN", 2]
    IDCARD_COPY_PAPERTRAY_TRAY3_STR_ID = ["cTrayN", 3]
    IDCARD_COPY_PAPERTRAY_AUTOMATIC_STR_ID = "cAutomatic"
    IDCARD_COPY_QUALITY_STANDARD_STR_ID = "cStandard"
    IDCARD_COPY_QUALITY_BEST_STR_ID = "cBestLabel"
    IDCARD_COPY_QUALITY_DRAFT_STR_ID = "cDraft"
    IDCARD_COPY_ORIENTATION_LANDSCAPE_STR_ID = "cLandscape"
    IDCARD_COPY_ORIENTATION_PORTRAIT_STR_ID = "cPortrait"

    def __init__(self, spice):
        self.maxtimeout = 60
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.homemenu = MenuAppProSelectUIOperations(spice)

    def goto_menu_mainMenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param _spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self._spice.goto_homescreen()
        homeApp = self._spice.query_item("#HomeScreenView")
        self._spice.wait_until(lambda: homeApp["activeFocus"] == True)
        logging.info("At Home Screen")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the Menu option (TODO - Need to avoid use of text)
        while (self._spice.query_item("#CurrentAppText")[
                   "text"] != "Menu" and timeSpentWaiting < self.maxtimeout):
            homeApp.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

    def goto_idcopy(self):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param _spice: Takes 0 arguments
        :return: None
        """
        self.goto_menu_mainMenu()
        # move to the Copy app
        startTime = time.time()
        timeSpentWaiting = 0
        currentScreen = self._spice.wait_for("#HomeScreenView")
        while (self._spice.query_item("#CurrentAppText")[
                   "text"] != "ID Card Copy" and timeSpentWaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(1)
        assert self._spice.query_item("#CurrentAppText")["text"] == "ID Card Copy"
        time.sleep(5)
        currentApp = self._spice.wait_for(self.IDCARD_COPY_UUID)
        currentApp.mouse_click()
        self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW, timeout=60)

    def ui_select_idcopy_page(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Copy
        :return: None
        """
        currentScreen = self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW)
        time.sleep(1)
        while (self._spice.query_item(self.IDCARD_COPY_BUTTON)["activeFocus"] == False):
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self._spice.query_item(self.IDCARD_COPY_BUTTON)["activeFocus"] == True
        currentButton = self._spice.wait_for(self.IDCARD_COPY_BUTTON + " SpiceText")
        currentButton.mouse_click()
        time.sleep(2)
        # self.wait_for_copying_toast(message="Copying", timeout=60)
        # logging.info(self._spice.wait_for(self.copying_progress))
        # time.sleep(2)
        # self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW, timeout=100)
        # self._spice.wait_for(self.copy_complete_view, timeout=30)
        # startTime = time.time()
        # timeSpentWaiting = time.time() - startTime
        # while (self._spice.query_item(self.copy_complete_view)["text"] != "Copy complete" and timeSpentWaiting < timeout):
        #     time.sleep(1)
        #     logging.info(self._spice.query_item(self.copy_complete_view)["text"])
        #     timeSpentWaiting = time.time() - startTime

    def ui_idcopy_set_no_of_pages(self, value):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: Copy screen -> Set number of pages
        :return: None
        """
        dial_value = 0
        currentScreen = self._spice.wait_for(self.NUMBER_OF_COPIES)
        for i in range(5):
            currentScreen.mouse_wheel(0, 0)
            time.sleep(1)

        while (self._spice.query_item(self.NUMBER_OF_COPIES)["activeFocus"] == False):
            currentScreen.mouse_wheel(180, 180)
        time.sleep(1)
        assert self._spice.query_item(self.NUMBER_OF_COPIES)["activeFocus"] == True
        time.sleep(2)

        current_value = self._spice.query_item(self.NUMBER_OF_COPIES)["value"]
        logging.info("Number of Copies value is: %s" % current_value)
        if (value != int(current_value)):
            if (value > int(current_value)):
                dial_value = 180

        currentButton = self._spice.wait_for(self.NUMBER_OF_COPIES)
        while (int(current_value) != int(value)):
            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
            time.sleep(1)
            currentButton.mouse_wheel(dial_value, dial_value)
            time.sleep(1)
            current_value = self._spice.query_item(self.NUMBER_OF_COPIES)["value"]
            logging.info("Number of Copies value is %s" % current_value)
            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
        time.sleep(1)
        assert int(current_value) == value, "Number of Copies setting is not successful"

    # ---------Toast/Alerts Validation-------

    def wait_for_copying_toast(self, message: str = "Copying", no_of_pages=1, timeout=30):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: Copying : str
        """
        option = ""
        status = ""
        if message == "Copying":
            option = "Copying 1/1"

        self._spice.wait_for("#ToastSystemToastStackView")
        time.sleep(timeout)
        # for i in range(timeout):
        #     status = self._spice.query_item("#ToastInfoText")["text"]
        #     logging.info("Current Toast message is : %s" % status)
        #     if status == option:
        #         break
        #     time.sleep(1)
        # if status != option:
        #     raise TimeoutError("Required Toast message does not appear within %s " % timeout)


    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.dial_common_operations.goto_item(self.IDCARD_COPY_OPTION_BUTTON, self.IDCARD_COPY_LANDING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)
        logging.info("UI: At Options in  Copy Settings")

    def goto_sides_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_SIDE_MODE_BUTTON, self.IDCARD_COPY_SETTING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_SIDE_VIEW)


    def select_copy_side(self, side_mode:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_sides_option()
        self.dial_common_operations.goto_item(side_mode, self.IDCARD_COPY_SETTING_SIDE_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

    def goto_quality_option(self, dial_value=180):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_QUALITY_BUTTON, self.IDCARD_COPY_SETTING_VIEW, dial_value=dial_value)
        # Wait for Options screen
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_QUALITY_VIEW)


    def select_copy_quality(self, quality:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_quality_option()
        self.dial_common_operations.goto_item(quality, self.IDCARD_COPY_SETTING_QUALITY_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

    def set_copy_settings(self):
        self.goto_copy_options_list()

        #contentorientation
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_CONTENTORIENTATION_BUTTON, self.IDCARD_COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW)
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_CONTENTORIENTATION_LANDSCAPE_BUTTON, self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW, 0)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

        #colorMode
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_COLORMODE_BUTTON, self.IDCARD_COPY_SETTING_VIEW, 0)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_COLORMODE_VIEW)
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_COLORMODE_COLOR_BUTTON, self.IDCARD_COPY_SETTING_COLORMODE_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

        #Paper tray
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING__TRAY_BUTTON, self.IDCARD_COPY_SETTING_VIEW, 180)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW)
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY1_BUTTON, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW, 0)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

        #lighter darker
        self.dial_common_operations.goto_item(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER, self.IDCARD_COPY_SETTING_VIEW, 180, False)
        self.set_scan_settings_lighter_darker(8)


        # quality
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_QUALITY_BUTTON, self.IDCARD_COPY_SETTING_VIEW, 0)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_QUALITY_VIEW)
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_QUALITY_DRAFT_BUTTON, self.IDCARD_COPY_SETTING_QUALITY_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout = 9.0)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        assert self._spice.wait_for(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER)
        current_value = self._spice.query_item(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]
        logging.info("Current lighter_darker value is " + current_value)

        assert lighter_darker >= 1 and lighter_darker <= 9 , "Lighter/Darker value is out of range"

        if (lighter_darker != int(current_value)):
            if (lighter_darker > int(current_value)):
                dial_value = 180
            else:
                dial_value = 0

            currentButton = self._spice.query_item(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER)
            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
            while (int(current_value) != lighter_darker):
                #
                time.sleep(1)
                if (lighter_darker < int(current_value)):
                    currentButton.mouse_wheel(0,0)
                elif (lighter_darker > int(current_value)):
                    currentButton.mouse_wheel(180,180)
                time.sleep(1)
                current_value = self._spice.query_item(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]

            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
            time.sleep(1)
            logging.info("Current lighter_darker value is " + current_value)

        assert int(current_value) == lighter_darker, "Lighter/Darker setting is not successful"

    def back_to_landing_view(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen to landing screen.
        UI Flow is Option screen->Landing screen
        '''
        self.dial_common_operations.back_button_press(self.IDCARD_COPY_SETTING_VIEW, self.IDCARD_COPY_LANDING_VIEW, index = 1, timeout_val = 60)

    def back_to_homescreen(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen to Option screen.
        UI Flow is Landing screen->Home screen
        '''
        self.dial_common_operations.back_button_press(self.IDCARD_COPY_LANDING_VIEW, "#HomeScreenView", index = 0, timeout_val = 60)

    def start_copy(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        self.dial_common_operations.goto_item(self.IDCARD_COPY_BUTTON, self.IDCARD_COPY_LANDING_VIEW, 0)

        self.dial_common_operations.goto_item(self.IDCARD_COPY_START_SCREEN_CONTINUE_BUTTON, self.IDCARD_COPY_START_SCREEN, 180)

        assert self._spice.wait_for(self.IDCARD_COPY_PROMPT_VIEW, timeout =15.0)

        self.dial_common_operations.goto_item(self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON, self.IDCARD_COPY_PROMPT_VIEW, 180, False)

        if (self._spice.query_item(self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON)["activeFocus"] == False):
            copy_prompt = self._spice.wait_for(self.IDCARD_COPY_PROMPT_VIEW)
            while (self._spice.query_item(self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON)["activeFocus"] == False):
                copy_prompt.mouse_wheel(180, 180)
            selected_button = self._spice.query_item(
                self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON + " SpiceText")
            selected_button.mouse_click()
        else:

            self.dial_common_operations.goto_item(self.IDCARD_COPY_PROMPT_VIEW, self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON, 180, True)

        time.sleep(3)

    def check_spec_on_idcopy_screen(self, net):
        """
        check spec on ID Copy Screen
        @param net:
        @return:
        """
        logging.info("check the str on ID Card Copy screen")
        self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_STR_ID, self.IDCARD_COPY_TITLE_LOCATOR)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_BUTTON_STR_ID, self.IDCARD_COPY_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_OPTIONS_HEADER_STR_ID, self.IDCARD_COPY_OPTION_BUTTON)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 1)

    def start_id_copy(self, dial_value=180, timeout=60):
        '''
        UI should be in ID Copy Landing Screen.
        Navigates to screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        self.dial_common_operations.goto_item(self.IDCARD_COPY_BUTTON, self.IDCARD_COPY_LANDING_VIEW, dial_value)

    def check_spec_on_idcopy_first_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        logging.info("check on first screen page prompt")
        self._spice.wait_for(self.IDCARD_COPY_START_SCREEN)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_STR_ID, self.IDCARD_COPY_FACE_DOWN_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_FACE_DOWN_BODY_STR_ID, self.IDCARD_COPY_FACE_DOWN_BODY)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 1)

    def select_idcopy_first_continue_button(self, timeout=60):
        """
        click first continue button
        # todo: need to update when the HMDE-285 is fixed
        @param:
        @return:
        """
        logging.info("click continue button")
        self.dial_common_operations.goto_item(
            self.IDCARD_COPY_START_SCREEN_CONTINUE_BUTTON,
            self.IDCARD_COPY_START_SCREEN
        )
        time.sleep(2)
        copy_process_find = False

        for i in range(timeout):
            time.sleep(1)
            try:
                toast_message = self._spice.query_item("#ToastInfoText")["text"]
            except:
                toast_message = "Does not capture the status"
            logging.info(f"current message is: <{toast_message}>")
            if toast_message.strip().startswith("Copying"):
                logging.info("Find Copying")
                copy_process_find = True
                break

        if not copy_process_find:
            raise Exception("Timeout to find Copying")

    def check_spec_on_idcopy_second_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        logging.info("check on second screen page prompt")
        self._spice.wait_for(self.IDCARD_COPY_PROMPT_VIEW, timeout=60)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_STR_ID, self.IDCARD_COPY_FACE_DOWN_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_FLIP_BODY_STR_ID, self.IDCARD_COPY_FACE_DOWN_BODY)

    def select_idcopy_second_continue_button(self):
        """
        click second continue button
        @param:
        @return:
        """
        logging.info("click second continue button")

        current_button = self._spice.wait_for(self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON, 10)
        # scroll to bottom first, if not script cannot click continue button sometimes
        for _ in range(5):
            time.sleep(1)
            current_button.mouse_wheel(180, 180)

        self.dial_common_operations.goto_item(self.IDCARD_COPY_PROMPT_VIEW_CONTINUE_BUTTON, self.IDCARD_COPY_PROMPT_VIEW, dial_value=0)
        self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW)

    def click_idcopy_cancel_on_second_screen(self):
        """
        click cancel button on second screen
        @param:
        @return:
        """
        logging.info("click cancel button")

        current_button = self._spice.wait_for(self.IDCARD_COPY_PROMPT_VIEW_CANCEL_BUTTON, 10)
        # scroll to bottom first, if not script cannot click cancel button sometimes
        for _ in range(5):
            time.sleep(1)
            current_button.mouse_wheel(180, 180)

        self.dial_common_operations.goto_item(self.IDCARD_COPY_PROMPT_VIEW_CANCEL_BUTTON, self.IDCARD_COPY_PROMPT_VIEW, dial_value=0)
        self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW)

    def wait_for_idcopy_complete(self, net, timeout=120):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        :param net:
        :param timeout:
        :return:
        """
        self._spice.wait_for("#ToastSystemToastStackView")
        complete_message = self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id="cCopyCompleteMessage")
        copy_process_find = False
        for i in range(timeout):
            time.sleep(1)
            try:
                current_status = self._spice.query_item("#ToastInfoText")["text"]
            except:
                current_status = "Does capture the status"
            logging.info("Current status is: " + current_status)
            if current_status == complete_message:
                logging.info("copy complete!")
                copy_process_find = True
                break

        if not copy_process_find:
            raise Exception("Copy complete doesn`t appear within %s" % timeout)

    def goto_menu_idcopy(self, spice):
        """
        navigate screen: home_menu -> menu -> copy -> id card copy
        @return:
        """
        self.homemenu.goto_menu(spice)
        self.homemenu.menu_navigation(spice, "#MenuListlandingPage", "#copyMenuButton")
        assert self._spice.wait_for("#MenuListcopy")
        self.homemenu.menu_navigation(spice, "#MenuListcopy", "#c74293eb-04c1-4dff-b469-1c0e99fdbe8bMenuButton")
        assert self._spice.wait_for(self.IDCARD_COPY_LANDING_VIEW)
        logging.info("At ID Card Copy Landing Screen")
        time.sleep(1)

    def back_to_copy_home_screen_from_idcopy(self):
        '''
        UI should be in ID Copy screen from menu
        Navigates to menu_copy screen starting from ID Copy landing screen to copy home screen
        UI Flow is ID Copy Landing screen -> copy home screen
        '''
        self.dial_common_operations.back_button_press("#idCardCopyLandingView", "#MenuListcopy", index=2, timeout_val=60)

    def check_spec_on_idcopy_options_screen(self, net):
        """
        check spec on ID Copy Options screen
        @param net:
        @return:
        """
        
        logging.info("check the items on ID Card Copy Options screen")
        setting_view = self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW, timeout=60)
        self._spice.wait_until(lambda: setting_view["visible"] == True, timeout = 10.0)
        header = self._spice.wait_for(self.IDCARD_COPY_OPTIONS_HEADER)
        self._spice.wait_until(lambda: header["visible"] == True, timeout = 10.0)
        assert header
        # Have to delay some time so that the script can get the correct value. we notice that the value is changed from Button to color quickly on printer.
        # eg: will get wrong str 'Button' if not delay, will get correct value 'Color' if add time.sleep
        # ->The actual str of oject name: #idcopy_colorModeButton is: Button if not add time.sleep
        time.sleep(2)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_OPTIONS_HEADER_STR_ID, self.IDCARD_COPY_OPTIONS_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_COLOR_STR_ID, self.IDCARD_COPY_SETTING_COLORMODE_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_HEADER_STR_ID, self.IDCARD_COPY_PAPERTRAY_TITLE)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_QUALITY_HEADER_STR_ID, self.IDCARD_COPY_QUALITY_TITLE)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_ORIENTATION_TITLE_STR_ID, self.IDCARD_COPY_ORIENTATION_TITLE)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 1)

    def goto_idcopy_option_color_screen(self):
        """
        Go to ID Card Copy -> Options -> Color screen
        @return:
        """
        logging.info("Go to ID Card Copy -> Options -> Color screen")
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_COLORMODE_BUTTON, self.IDCARD_COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_COLORMODE_VIEW)

    def check_spec_on_idcopy_option_color_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Color screen
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Color screen")
        self._spice.wait_for(self.IDCARD_COPY_SETTING_COLORMODE_VIEW, timeout=60)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_COLOR_STR_ID, self.IDCARD_COPY_COLOR_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_COLOR_STR_ID, self.IDCARD_COPY_SETTING_COLORMODE_COLOR_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_COLOR_GRAYSCALE_STR_ID, self.IDCARD_COPY_SETTING_COLORMODE_GRAYSCALE_BUTTON)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 2)

    def set_idcopy_color_options(self, net, idcopy_color_options="Color", locale: str = "en-US"):
        """
        Set idcopy color option
        @param net:
        @param idcopy color_options: str -> Color/Grayscale
        @param locale:
        @return:
        """
        logging.info("Set the idcopy color option to: " + idcopy_color_options)

        idcopy_color_options_dict = {
            "Color": self.IDCARD_COPY_SETTING_COLORMODE_COLOR_BUTTON,
            "Grayscale": self.IDCARD_COPY_SETTING_COLORMODE_GRAYSCALE_BUTTON
        }

        str_id_dict = {
            "Color": self.IDCARD_COPY_COLOR_STR_ID,
            "Grayscale": self.IDCARD_COPY_COLOR_GRAYSCALE_STR_ID
        }

        to_select_item = idcopy_color_options_dict.get(idcopy_color_options)
        str_id = str_id_dict.get(idcopy_color_options)

        for i in range(3):
            self._spice.wait_for(self.IDCARD_COPY_SETTING_COLORMODE_VIEW).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.IDCARD_COPY_SETTING_COLORMODE_VIEW)
        time.sleep(1)
        current_idcopy_color_options = self.get_idcopy_color_options()

        assert current_idcopy_color_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id, locale), f"failed to set color options {idcopy_color_options}"

    def get_idcopy_color_options(self):
        """
        Get the idcopy color option
        @return:
        """
        self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW)
        current_idcopy_color_option = self.dial_common_operations.get_actual_str(self.IDCARD_COPY_SETTING_COLORMODE_BUTTON)
        logging.info("Current idcopy Color settings is: " + current_idcopy_color_option)
        return current_idcopy_color_option

    def goto_idcopy_options_paper_tray(self):
        """
        go to the options -> paper tray
        """
        logging.info("Go to paper tray screen")
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING__TRAY_BUTTON, self.IDCARD_COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW)

    def check_spec_on_idcopy_option_paper_tray(self, net):
        """
        Check spec on ID Card Copy -> Options -> Paper Tray
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Paper Tray")
        self._spice.wait_for(self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_HEADER_STR_ID, self.IDCARD_COPY_PAPERTRAY_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_TRAY1_STR_ID, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY1_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_TRAY2_STR_ID, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY2_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_TRAY3_STR_ID, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY3_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_PAPERTRAY_AUTOMATIC_STR_ID, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY_AUTO_BUTTON)
        logging.info("verify the back button existed")
        self._spice.wait_for(self.COMMON_BACK_LOCATOR, 2)

    def set_idcopy_paper_tray_options(self, net, idcopy_paper_tray_options="Automatic", locale: str = "en-US"):
        """
        Set idcopy paper tray option
        @param net:
        @param idcopy paperTray_options: str -> Tray 1/Tray 2/Tray 3/Automatic
        @param locale:
        @return:
        """
        logging.info("Set the idcopy paper tray option to: " + idcopy_paper_tray_options)

        idcopy_paper_tray_options_dict = {
            "Tray 1": self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY1_BUTTON,
            "Tray 2": self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY2_BUTTON,
            "Tray 3": self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY3_BUTTON,
            "Automatic": self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_TAY_AUTO_BUTTON
        }

        str_id_dict = {
            "Tray 1": self.IDCARD_COPY_PAPERTRAY_TRAY1_STR_ID,
            "Tray 2": self.IDCARD_COPY_PAPERTRAY_TRAY2_STR_ID,
            "Tray 3": self.IDCARD_COPY_PAPERTRAY_TRAY3_STR_ID,
            "Automatic": self.IDCARD_COPY_PAPERTRAY_AUTOMATIC_STR_ID
        }

        to_select_item = idcopy_paper_tray_options_dict.get(idcopy_paper_tray_options)
        str_id = str_id_dict.get(idcopy_paper_tray_options)
        for i in range(5):
            self._spice.wait_for(self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.IDCARD_COPY_SETTING_PAPERSELECTION_TRAY_VIEW)
        time.sleep(1)
        current_idcopy_paper_tray_options = self.get_idcopy_paper_tray_options()

        assert current_idcopy_paper_tray_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id, locale), f"failed to set paper tray options {idcopy_paper_tray_options}"

    def get_idcopy_paper_tray_options(self):
        """
        Get the idcopy paper tray option
        @return:
        """
        self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW)
        current_tray_options = self.dial_common_operations.get_actual_str(self.IDCARD_COPY_SETTING__TRAY_BUTTON)
        logging.info("Current paper tray settings is: " + current_tray_options)
        return current_tray_options

    def check_spec_on_idcopy_option_quality_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Quality screen
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Quality screen")
        self._spice.wait_for(self.IDCARD_COPY_SETTING_QUALITY_VIEW, timeout=60)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_QUALITY_HEADER_STR_ID, self.IDCARD_COPY_QUALITY_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_QUALITY_STANDARD_STR_ID, self.IDCARD_COPY_SETTING_QUALITY_NORMAL_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_QUALITY_BEST_STR_ID, self.IDCARD_COPY_SETTING_QUALITY_BEST_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_QUALITY_DRAFT_STR_ID, self.IDCARD_COPY_SETTING_QUALITY_DRAFT_BUTTON)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 2)

    def set_idcopy_quality_options(self, net, idcopy_quality_options="Standard", locale: str = "en-US"):
        """
        Set idcopy quality option
        @param net:
        @param idcopy_quality_options: str -> Standard/Draft/Best
        @param locale:
        @return:
        """
        logging.info("Set the quality option to: " + idcopy_quality_options)

        idcopy_quality_options_dict = {
            "Standard": self.IDCARD_COPY_SETTING_QUALITY_NORMAL_BUTTON,
            "Draft": self.IDCARD_COPY_SETTING_QUALITY_DRAFT_BUTTON,
            "Best": self.IDCARD_COPY_SETTING_QUALITY_BEST_BUTTON
        }

        str_id_dict = {
            "Standard": self.IDCARD_COPY_QUALITY_STANDARD_STR_ID,
            "Draft": self.IDCARD_COPY_QUALITY_DRAFT_STR_ID,
            "Best": self.IDCARD_COPY_QUALITY_BEST_STR_ID
        }

        to_select_item = idcopy_quality_options_dict.get(idcopy_quality_options)
        str_id = str_id_dict.get(idcopy_quality_options)

        for i in range(3):
            self._spice.wait_for(self.IDCARD_COPY_SETTING_QUALITY_VIEW).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.IDCARD_COPY_SETTING_QUALITY_VIEW)
        time.sleep(1)
        current_idcopy_quality_options = self.get_idcopy_quality_options()

        assert current_idcopy_quality_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id, locale), f"failed to set quality options {idcopy_quality_options}"

    def get_idcopy_quality_options(self):
        """
        Get idcopy quality option
        @return:
        """
        self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW)
        current_idcopy_quality_option = self.dial_common_operations.get_actual_str(self.IDCARD_COPY_SETTING_QUALITY_BUTTON)
        logging.info("Current idcopy quality settings is: " + current_idcopy_quality_option)
        return current_idcopy_quality_option

    def goto_idcopy_lighter_or_darker_options(self):
        """
        go to the lighter or darker
        """
        logging.info("Go to lighter or darker option menu")
        self.dial_common_operations.goto_item(self.IDCARD_COPY_LIGHTER_DARKER_SLIDER, self.IDCARD_COPY_SETTING_VIEW, 180, False)

    def goto_idcopy_option_orientation_screen(self):
        """
        Go to orientation option menu
        @return:
        """
        logging.info("Go to orientation option menu")
        self.dial_common_operations.goto_item(self.IDCARD_COPY_SETTING_CONTENTORIENTATION_BUTTON, self.IDCARD_COPY_SETTING_VIEW)
        self._spice.wait_for(self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW)

    def check_spec_on_idcopy_options_orientation(self, net):
        """
        Check spec on IDCopy_Orientaion_Options
        @param net:
        @return:
        """
        logging.info("check the spec on IDCopy_Orientaion_Options")
        logging.info("check the string about Orientation, (Landscape, Portrait)")
        self._spice.wait_for(self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_ORIENTATION_TITLE_STR_ID, self.IDCARD_COPY_ORIENTATION_HEADER)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_ORIENTATION_LANDSCAPE_STR_ID, self.IDCARD_COPY_SETTING_CONTENTORIENTATION_LANDSCAPE_BUTTON)
        self.dial_common_operations.verify_string(net, self.IDCARD_COPY_ORIENTATION_PORTRAIT_STR_ID, self.IDCARD_COPY_SETTING_CONTENTORIENTATION_POTRAIT_BUTTON)
        logging.info("verify the back button existed")
        assert self._spice.wait_for(self.COMMON_BACK_LOCATOR, 2)

    def set_idcopy_orientation_options(self, net, orientation_options="Portrait", locale: str = "en-US"):
        """
        Set the orientation option
        @param net:
        @param orientaion_options: str -> Landscape/Portrait
        @param locale:
        @return:
        """
        logging.info("Set the orientation option to: " + orientation_options)

        orientation_options_dict = {
            "Landscape": self.IDCARD_COPY_SETTING_CONTENTORIENTATION_LANDSCAPE_BUTTON,
            "Portrait": self.IDCARD_COPY_SETTING_CONTENTORIENTATION_POTRAIT_BUTTON
        }

        str_id_dict = {
            "Landscape": self.IDCARD_COPY_ORIENTATION_LANDSCAPE_STR_ID,
            "Portrait": self.IDCARD_COPY_ORIENTATION_PORTRAIT_STR_ID
        }

        to_select_item = orientation_options_dict.get(orientation_options)
        str_id = str_id_dict.get(orientation_options)

        for i in range(3):
            self._spice.wait_for(self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.IDCARD_COPY_SETTING_CONTENTOREINTATION_VIEW)
        time.sleep(1)
        current_orientation_options = self.get_idcopy_orientation_options()

        assert current_orientation_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id, locale), f"failed to set orientation options {orientation_options}"

    def get_idcopy_orientation_options(self):
        """
        Get the orientation option
        @return:
        """
        self._spice.wait_for(self.IDCARD_COPY_SETTING_VIEW)
        current_orientation_option = self.dial_common_operations.get_actual_str(self.IDCARD_COPY_SETTING_CONTENTORIENTATION_BUTTON)
        logging.info("Current orientation settings is: " + current_orientation_option)
        return current_orientation_option
