#########################################################################################
# @file     CopyAppProSelectUIOperations.py
# @authors  Vinay Kumar M(vinay.kumar.m@hp.com)
# @date     16-03-2021
# @brief    Implementation for all the Copy UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
import requests
import unicodedata
from dunetuf.ui.uioperations.BaseOperations.ICopyAppUIOperations import ICopyAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations

class CopyAppProSelectUIOperations(ICopyAppUIOperations):

    # -------------------------------Function Keywords------------------------ #
    COPY_UUID = "#cedab422-33b3-4638-b6a1-604e54525215"

    COPY_LANDING_VIEW = "#copyLandingView"
    COPY_SETTING_VIEW = "#MenuListcopySettingsPage"
    COPY_SETTING_SIDE_VIEW = "#sidesSettingView"

    NUMBER_OF_COPIES = "#NumberOfCopies"
    COPY_BUTTON = "#CopyButton"
    COPY_OPTION_BUTTON = "#CopyOptionsButton"

    COPY_SETTING_SIDE_MODE_BUTTON = "#copy_sidesButton"
    COPY_SETTING_SIDE_1_TO_1_BUTTON = "#Copy1to1Sided"
    COPY_SETTING_SIDE_1_TO_2_BUTTON = "#Copy1to2Sided"
    COPY_SETTING_SIDE_2_TO_1_BUTTON = "#Copy2to1Sided"
    COPY_SETTING_SIDE_2_TO_2_BUTTON = "#Copy2to2Sided"

    COPY_SETTING_QUALITY_BUTTON = "#copy_qualityButton"
    COPY_SETTING_QUALITY_VIEW = "#MenuSelectionListcopy_quality"
    COPY_SETTING_QUALITY_NORMAL_BUTTON = "#option_normal"
    COPY_SETTING_QUALITY_DRAFT_BUTTON = "#option_draft"
    COPY_SETTING_QUALITY_BEST_BUTTON = "#option_best"

    COPY_SETTING_RESIZE_BUTTON = "#copy_resizeButton"
    COPY_SETTING_RESIZE_VIEW = "#copyResizeSettingView"
    COPY_SETTING_RESIZE_PAGE_LETTER_BUTTON = "#FullPageA4ToLetter"

    COPY_SETTING_COLORMODE_BUTTON = "#copy_colorModeButton"
    COPY_SETTING_COLORMODE_VIEW = "#MenuSelectionListcopy_colorMode"
    COPY_SETTING_COLORMODE_COLOR_BUTTON = "#option_color"
    COPY_SETTING_COLORMODE_GRAYSCALE_BUTTON = "#option_grayscale"

    COPY_SETTING_CONTENTTYPE_BUTTON = "#copy_contentTypeButton"
    COPY_SETTING_CONTENTTYPE_VIEW = "#MenuSelectionListcopy_contentType"
    COPY_SETTING_CONTENTTYPE_MIXED_BUTTON = "#option_mixed"
    COPY_SETTING_CONTENTTYPE_TEXT_BUTTON = "#option_text"
    COPY_SETTING_CONTENTTYPE_PHOTO_BUTTON = "#option_photo"

    COPY_SETTING_ORIGINALSIZE_BUTTON = "#copy_originalSizeButton"
    COPY_SETTING_ORIGINALSIZE_VIEW = "#MenuSelectionListcopy_originalSize"
    COPY_SETTING_ORIGINALSIZE_LEGAL_BUTTON = "#option_na_legal_8_5x14in"
    COPY_SETTING_ORIGINALSIZE_LETTER_BUTTON = "#option_na_letter_8.5x11in"
    COPY_SETTING_ORIGINALSIZE_A4_BUTTON = "#option_iso_a4_210x297mm"

    COPY_SETTING_PAGESPERSHEET_BUTTON = "#copy_pagesPerSheetButton"
    COPY_SETTING_PAGESPERSHEET_VIEW = "#MenuSelectionListcopy_pagesPerSheet"
    COPY_SETTING_PAGESPERSHEET_ONEUP_BUTTON = "#oneUp"
    COPY_SETTING_PAGESPERSHEET_TWOUP_BUTTON = "#twoUp"

    COPY_SETTING_PAPERSELECTION_BUTTON = "#copy_paperSelectionButton"
    COPY_SETTING_PAPERSELECTION_VIEW = "#MenuListcopy_paperSelection"
    COPY_SETTING_PAPERSELECTION_TRAY_BUTTON = "#copy_paperTrayButton"
    COPY_SETTING_PAPERSELECTION_MEDIASIZE_BUTTON = "#copy_mediaSizeButton"
    COPY_SETTING_PAPERSELECTION_PAPERTYPE_BUTTON = "#copy_paperTypeButton"

    COPY_SETTING_PAPERSELECTION_MEDIASIZE_VIEW ="#MenuSelectionListcopy_mediaSize" 
    COPY_SETTING_PAPERSELECTION_MEDIASIZE_A4_BUTTON ="#option_na_legal_8_5x14in"

    COPY_SETTING_PAPERSELECTION_PAPERTYPE_VIEW ="#MenuSelectionListcopy_paperType" 
    COPY_SETTING_PAPERSELECTION_PAPERTYPE_STATIONERY_BUTTON ="#option_stationery"

    COPY_SETTING_PAPERSELECTION_TRAY_VIEW = "#MenuSelectionListcopy_paperTray"
    COPY_SETTING_PAPERSELECTION_TRAY_TAY1_BUTTON = "#option_tray_2"

    COPY_LIGHTER_DARKER_SLIDER = "#copy_exposureMenuSlider"

    COPY_COLLATE_TOGGLE_SWITCH = "#copy_collateToggleMenuSwitch"

    COPY_PAGEFLIPUP_SWITCH = "#copyPageFlipUp"

    COPY_QUICKSET_LIST_VIEW = "#QuickSetListView"
    COPY_QUICKSET_BUTTON = "#QuickSetSelectedButton"
    COPY_QUICKSET_SAVE_BUTTON = "#DefaultSaveButton"
    COPY_QUICKSET_SAVE_OPTION_VIEW = "#QuickSetSaveOptionsView"
    COPY_AS_DEFAULT_BUTTON = "#AsDefault"

    COPY_2_SIDED_PROMPT = "#scanManualDuplexSecondPage"
    COPY_DOCUMENT_BUTTON = "#documentCopyMenuButton"
    COPY_DOCUMENT_LIST_VIEW= "#MenuListcopy"

    COPY_HOME_TITLE_LOCATOR = "#TitleText"
    DEFAULT_AND_QUICK_SETS_LOCATOR = "#CopyQuickSetSelected"
    COPY_QUICKSET_BUTTON = "#QuickSetSelectedButton"

    #options strings and value check
    COPY_SETTING_LIST_HEADER_LOCATOR = "#MenuListcopySettingsPage #Header"
    
    COPY_SETTING_CONTENT_TYPE_VALUE = "#copy_contentTypeMenuNameValue #NameText"
    COPY_SETTING_COLOR_BUTTON_VALUE = "#copy_colorModeMenuNameValue #NameText"
    COPY_SETTING_SIDES_VALUE = "#copyPaperSelection #NameText"
    COPY_SETTING_SIDED_PAGES_UP_STATUS = "#copyPageFlipUp #SpiceSwitch"
    COPY_SETTING_ORIGINAL_SIZE_VALUE = "#copy_originalSizeMenuNameValue #NameText"
    COPY_SETTING_OUTPUT_VALUE = "#copySettingResize #NameText"
    COPY_SETTING_PAPER_SELECTION_VALUE = "#copyPaperSelection #NameText"
    COPY_SETTING_PAGES_SHEET_VALUE = "#copy_pagesPerSheetMenuNameValue #NameText"
    COPY_SETTING_QUALITY_VALUE = "#copy_qualityMenuNameValue #NameText"
    COPY_SETTING_COLLATE_STATUS = "#copy_collateToggleMenuSwitch #SpiceSwitch"
    COMMON_HEADER_LOCATOR = "#RadioButtonListLayout #Header"

    PAPER_SIZE_LOCATOR = "#copy_mediaSizeMenuNameValue"
    PAPER_TYPE_LOCATOR = "#copy_paperTypeMenuNameValue"
    PAPER_TRAY_LOCATOR = "#copy_paperTrayMenuNameValue"
    PAPER_TRAY_HEADER_LOCATOR = "#MenuSelectionListcopy_paperTray #Header"
    TRAY1_LOCATOR = "#option_tray_1"
    TRAY2_LOCATOR = "#option_tray_2"
    TRAY3_LOCATOR = "#option_tray_3"
    AUTOMATIC_LOCATOR = "#option_automatic"

    COPY_SETTING_OUTPUT_SCALE_NONE = "#None"
    COPY_SETTING_OUTPUT_SCALE_CUSTOM = "#Custom"
    COPY_SETTING_OUTPUT_SCALE_FIT_TO_PAGE = "#FitToPage"
    COPY_SETTING_OUTPUT_SCALE_LEGAL_TO_LETTER = "#LegalToLetter"
    COPY_SETTING_OUTPUT_SCALE_LETTER_TO_A4 = "#LetterToA4"

    #output scale custom
    COPY_SETTING_CUSTOM_SETTINGS_VIEW = "#copyCustomSizeKeyboardView"

    #size and tray common locator
    SIZE_OR_TYPE_COMMON_LOCATOR = "#RadioButtonListLayout #SpiceRadioButton SpiceText"

    # --- String id
    DEFAULT_AND_QUICK_SETS_STR_ID = "cDefaultsAndQuickSets"
    COPY_HOME_STR_ID = "cCopy"
    DEFAULT_STR_ID = "cDefault"
    OPTIONS_STR_ID = "cOptions"
    OPTIONS_LIST_HEADER_STR_ID = "cOptions"
    CONTENT_TYPE_STR_ID = "cContentType"
    COLOR_BUTTON_STR_ID = "cColor"
    SIDES_STR_ID = "cSides"
    ORIGINAL_SIZE_STR_ID = "cOriginalSize"
    OUTPUT_STR_ID = "cOutputScale"
    PAPER_SELECTION_STR_ID = "cPaperSelectTitle"
    QUALITY_STR_ID = "cQuality"
    PAGES_PER_SHEET_STR_ID = "cPagesPerSheet"
    CONTENT_TYPE_HEADER_STR_ID = "cContentType"
    CONTENT_TYPE_MIXED_STR_ID = "cMixed"
    CONTENT_TYPE_TEXT_STR_ID = "cText"
    CONTENT_TYPE_PHOTO_STR_ID = "cScanModeGlossy"
    COLOR_COLOR_STR_ID = "cColor"
    COLOR_GRAYSCALE_STR_ID = "cChromaticModeGrayscale"
    SIDED_PAGES_UP_STR_ID = "c2SidedPages"
    COLLATE_STR_ID = "cCollate"
    SIZE_SIZE_STR_ID = "cOriginalSize"

    SIZE_A4_STR_ID = "cMediaSizeIdA4" # "A4 (210x297 mm)"
    SIZE_A5_STR_ID = "cMediaSizeIdA5" # "A5 (148x210 mm)"
    SIZE_A6_STR_ID = "cMediaSizeIdA6" # "A6 (105x148 mm)"
    SIZE_ENVELOP_B5_STR_ID = "cMediaSizeIdB5Envelope" # "Envelope B5 (176x250 mm)"
    SIZE_B6_JIS_STR_ID = "cMediaSizeIdJisB6" # "B6 (JIS) (128x182 mm)"
    SIZE_ENVELOP_C5_STR_ID = "cMediaSizeIdC5Envelope" # "Envelope C5 (162x229 mm)"
    SIZE_ENVELOP_C6_STR_ID = "cMediaSizeIdEnvelopeC6" # "Envelope C6 (114x162 mm)"
    SIZE_ENVELOP_DL_STR_ID = "cMediaSizeIdDLEnvelope" # "Envelope DL (110x220 mm)"
    SIZE_B5_JIS_STR_ID = "cMediaSizeIdJisB5" # "B5 (JIS) (182x257 mm)"
    SIZE_JAPANESE_ENVELOP_CHOU_3_STR_ID= "cMediaSizeIdJChou3Envelope" # "Japanese Envelope Chou #3 (120x235 mm)"
    SIZE_DOUBLE_POSTCARD_JIS_STR_ID = "cMediaSizeIdOfukuHagaki" # Double Postcard (JIS) (148x200 mm)
    SIZE_EXECUTIVE_7_25x10_5_STR_ID = "cMediaSizeIdExecutive" # "Executive (7.25x10.5 in.)"
    SIZE_OFICIO_8_5x13_STR_ID = "cMediaSizeIdOficio" # "Oficio (8.5x13 in.)"
    SIZE_LETTER_8inx10in_STR_ID = "cMediaSizeLetter8x10" # "Letter (8inx10in)"
    SIZE_4x6_in_STR_ID = "cMediaSizeIdFourXSix" # "4x6 in."
    SIZE_5x7_STR_ID = "cMediaSizeIdFiveXSeven" # "5x7 in."
    SIZE_5x8_STR_ID = "cMediaSizeIdFiveXEight" # "5x8 in."
    SIZE_LEGAL_STR_ID = "cMediaSizeIdLegal" # "Legal (8.5x14 in.)"
    SIZE_LETTER_STR_ID = "cMediaSizeIdLetter" # "Letter (8.5x11 in.)"
    SIZE_ENVELOP_10_4_1x9_5_STR_ID = "cMediaSizeIdCOM10Envelope" # "Envelope #10 (4.1x9.5 in.)"
    SIZE_OFICIO_STR_ID = "cMediaSizeIdOficio216x340" # "Oficio (216x340 mm)"
    SIZE_16K_184x260_STR_ID = "cMediaSizeIdSize16K184x260" # "16K (184x260 mm)"
    SIZE_16K_195x270_STR_ID = "cMediaSizeIdSize16k195x270" # "16K (195x270 mm)"
    SIZE_16K_197x273_STR_ID = "cMediaSizeIdSixteenK" # "16K (197x273 mm)"
    SIZE_STATEMENT_8_5x5_5_STR_ID = "cMediaSizeIdStatement" # "Statement (8.5x5.5 in.)"
    SIZE_10_15_STR_ID = "cMediaSizeId10x15cm" #10x15 cm
    SIZE_ENVELOP_MONARCH_STR_ID = "cMediaSizeIdMonarchEnvelope" # Envelope Monarch (3.9x7.5 in.)
    SIZE_POSTCARD_JIS_STR_ID = "cMediaSizeIdHagaki" # Postcard (JIS) (100x148 mm)
    SIZE_DOUBLE_POSTCARD_STR_ID = "cMediaSizeIdOfukuHagaki" # Double Postcard (JIS) (148x200 mm)
    SIZE_CUSTOM_STR_ID = "cCustom" # Custom

    OUTPUT_SCALE_HEADER_STR_ID = "cOutputScale"
    OUTPUT_SCALE_NONE_STR_ID = "cNone"
    OUTPUT_SCALE_FIT_TO_PAGE_STR_ID = "cFitToPage"
    OUTPUT_SCALE_FULL_PAGE_STR_ID = "cFullPageLetter"
    OUTPUT_SCALE_LEGAL_TO_LETTER_STR_ID = "cLegalToLetter"
    OUTPUT_SCALE_LETTER_TO_A4_STR_ID = "cLettertoA4"
    PAPER_SELECTION_HEADER_STR_ID = "cPaperSelectTitle"
    PAPER_SELECTION_PAPER_SIZE_STR_ID = "cMediaSize"
    PAPER_SELECTION_PAPER_TYPE_STR_ID = "cPaperType"
    PAPER_SELECTION_PAPER_TRAY_STR_ID = "cPaperTray"

    PAPER_TYPR_ANY_TYPE_STR_ID = "cMediaTypeIdAnySupportedType"
    PAPER_TYPE_PLAIN_STR_ID = "cMediaTypeIdPlain"
    PAPER_TYPE_ECOFFICIENT_STR_ID = "cMediaTypeIdHPEcoSmartLite" # "HP EcoFFICIENT"
    PAPER_TYPE_HP_MATTE_90g_STR_ID = "cMediaTypeIdHPMatte90gsm" # "HP Matte (90g)"
    PAPER_TYPE_HP_MATTE_105g_STR_ID = "cMediaTypeIdHPMatte105gsm" # "HP Matte (105g)"
    PAPER_TYPE_HP_MATTE_120g_STR_ID = "cMediaTypeIdHPMatte120Gsm" # "HP Matte (120g)"
    PAPER_TYPE_HP_MATTE_200g_STR_ID = "cMediaTypeIdHPMatte200gsm" # "HP Matte (200g)"
    PAPER_TYPE_HP_BROCHURE_MATTE_STR_ID = "cMediaTypeComHpBrochureMatte" # "Hp Brochure Matte"
    PAPER_TYPE_HP_GLOSSY_120g_STR_ID ="cMediaTypeIdHPGlossy130gsm" # "HP Glossy (120g)"
    PAPER_TYPE_HP_GLOSSY_150g_STR_ID = "cMediaTypeIdHPGlossy160gsm" # "HP Glossy (150g)"
    PAPER_TYPE_HP_GLOSSY_200g_STR_ID = "cMediaTypeIdHPGlossy220gsm" # "HP Glossy (200g)"
    PAPER_TYPE_HP_TRIFOLD_GLOSSY_STR_ID = "cMediaTypeIdHPTrifoldBrochureGlossy" # "HP Tri-Fold Glossy (150g)"
    PAPER_TYPE_LIGHT_STR_ID = "cMediaTypeIdPlainLightRecycled" # "Light (60-74g)"
    PAPER_TYPE_INTERMEDIATE_STR_ID = "cMediaTypeIdIntermediate" # "Intermediate (85-95g)"
    PAPER_TYPE_MIDWEIGHT_STR_ID = "cMediaTypeIdMidWeight" # "Mid-Weight (96-110g)"
    PAPER_TYPE_HEAVY_STR_ID = "cMediaTypeIdHeavy" # "Heavy (111-130g)"
    PAPER_TYPE_EXTRA_HEAVY_STR_ID = "cMediaTypeIdExtraHeavy" # "Extra Heavy (131-175g)"
    PAPER_TYPE_CARDSTOCK_STR_ID = "cMediaTypeIdCardstock" # "Cardstock (176-220g)"
    PAPER_TYPE_HEAVY_GLOSSY_STR_ID = "cMediaTypeIdHeavyGlossy" # "Heavy Glossy (111-130g)"
    PAPER_TYPE_EXTRA_HEAVY_GLOSSY_STR_ID = "cMediaTypeIdExtraHeavyGloss" # "Extra Heavy Glossy (131-175g)"
    PAPER_TYPE_CARDSTOCK_GLOSSY_STR_ID = "cMediaTypeIdCardstockGlossy" # "Cardstock Glossy (176-220g)"
    PAPER_TYPE_LABELS_STR_ID = "cMediaTypeIdLabels" # "Labels"
    PAPER_TYPE_LETTERHEAD_STR_ID = "cMediaTypeIdStationeryLetterhead" # "Letterhead"
    PAPER_TYPE_ENVELOP_STR_ID = "cMediaTypeIdEnvelope" # "Envelope"
    PAPER_TYPE_HEAVY_ENVELOP_STR_ID = "cMediaTypeIdHeavyEnvelope" # "Heavy Envelope"
    PAPER_TYPE_PREPRINTED_STR_ID = "cMediaTypeIdStationeryPreprinted" # "Preprinted"
    PAPER_TYPE_COLOREED_STR_ID = "cMediaTypeIdColor" # "Colored"
    PAPER_TYPE_HEAVY_ROUGH_STR_ID = "cMediaTypeIdHeavyRough" # "Heavy Rough"
    PAPER_TYPE_OPAQUE_FILM_STR_ID = "cMediaTypeIdFilmOpaque" # "Opaque Film"
    PAPER_TYPE_TRANSPARENCY_STR_ID = "cMediaTypeIdTransparency" # "Transparency"
    PAPER_TYPE_ROUGH_STR_ID = "cMediaTypeIdRough" # "Rough"
    PAPER_TYPE_RECYCLED_STR_ID = "cMediaTypeIdPlainLightRecycled" # "Recycled"
    PAPER_TYPE_PREPUNCHED_STR_ID = "cMediaTypeIdStationeryPrepunched" # "Prepunched"
    PAPER_TYPE_BOND_STR_ID = "cMediaTypeIdBond" # "Bond"

    TRAY1_STR_ID = ["cTrayN", 1]
    TRAY2_STR_ID = ["cTrayN", 2]
    TRAY3_STR_ID = ["cTrayN", 3]
    AUTOMATIC_STR_ID = "cAutomatic"
    PAGES_SHEET_ONE_STR_ID = "cNumeral1"
    PAGES_SHEET_TWO_STR_ID = "cNumeral2"
    COPY_SETTING_HEADER_STR_ID = "cSides"
    COPY_SIDE_1_TO_1_STR_ID = "c1To1Sided"
    COPY_SIDE_1_TO_2_STR_ID = "c1To2Sided"
    COPY_SIDE_2_TO_1_STR_ID = "c2To1Sided"
    COPY_SIDE_2_TO_2_STR_ID = "c2To2Sided"
    QUALITY_HEADER_STR_ID = "cQuality"
    QUALITY_STANDARD_STR_ID = "cStandard"
    QUALITY_DRAFT_STR_ID = "cDraft"
    QUALITY_BEST_STR_ID = "cBestLabel"

    def __init__(self, spice):
        self.maxtimeout = 60
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.homemenu = MenuAppProSelectUIOperations(spice)
        self.select_keyboard = ProSelectKeyboardOperations(self._spice)

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

    def goto_copy(self):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param _spice: Takes 0 arguments
        :return: None
        """
        currentApp = self.get_copy_app()
        currentApp.mouse_click()
        self._spice.wait_for(self.COPY_LANDING_VIEW, timeout=60)

    def get_copy_app(self):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu
        :param _spice: Takes 0 arguments
        :return: Copy App
        """
        self.goto_menu_mainMenu()
        # move to the Copy app
        startTime = time.time()
        timeSpentWaiting = 0
        currentScreen = self._spice.wait_for("#HomeScreenView")
        while (self._spice.query_item("#CurrentAppText")[
                   "text"] != "Copy" and timeSpentWaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(1)
        assert self._spice.query_item("#CurrentAppText")["text"] == "Copy"
        time.sleep(5)
        return self._spice.wait_for(self.COPY_UUID)

    def ui_select_copy_page(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Copy
        :return: None
        """
        currentScreen = self._spice.wait_for(self.COPY_LANDING_VIEW)
        time.sleep(1)
        while (self._spice.query_item(self.COPY_BUTTON)["activeFocus"] == False):
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self._spice.query_item(self.COPY_BUTTON)["activeFocus"] == True
        currentButton = self._spice.wait_for(self.COPY_BUTTON + " SpiceText")
        currentButton.mouse_click()
        time.sleep(2)
        # self.wait_for_copy_status_toast(net, message="Copying", timeout=60)
        # logging.info(self._spice.wait_for(self.copying_progress))
        # time.sleep(2)
        # self._spice.wait_for(self.COPY_LANDING_VIEW, timeout=100)
        # self._spice.wait_for(self.copy_complete_view, timeout=30)
        # startTime = time.time()
        # timeSpentWaiting = time.time() - startTime
        # while (self._spice.query_item(self.copy_complete_view)["text"] != "Copy complete" and timeSpentWaiting < timeout):
        #     time.sleep(1)
        #     logging.info(self._spice.query_item(self.copy_complete_view)["text"])
        #     timeSpentWaiting = time.time() - startTime

    def ui_copy_set_no_of_pages(self, value):
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

    def wait_for_copy_status_toast(self, net, configuration, message: str = "Copying", no_of_pages=1, timeout=30):
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
    
    def wait_for_copy_job_status_toast_or_modal(self, net, configuration, message: str = "Complete", timeout= 60):
        self.wait_for_copy_status_toast(net,configuration,message,timeout)
    
    def wait_for_copy_status_toast(self, net, configuration, message: str = "Copying", no_of_pages=1, timeout=30):
        """
        Purpose: Wait for the given toast not appears
        NOT IMPLEMENTED
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.dial_common_operations.goto_item(self.COPY_OPTION_BUTTON, self.COPY_LANDING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)
        logging.info("UI: At Options in  Copy Settings")

    def goto_sides_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        self.dial_common_operations.goto_item(self.COPY_SETTING_SIDE_MODE_BUTTON, self.COPY_SETTING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.COPY_SETTING_SIDE_VIEW)

    
    def select_copy_side(self, side_mode:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_sides_option()
        self.dial_common_operations.goto_item(side_mode, self.COPY_SETTING_SIDE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)

    def goto_quality_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        self.dial_common_operations.goto_item(self.COPY_SETTING_QUALITY_BUTTON, self.COPY_SETTING_VIEW)
        # Wait for Options screen
        assert self._spice.wait_for(self.COPY_SETTING_QUALITY_VIEW)

    
    def select_copy_quality(self, quality:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_quality_option()
        self.dial_common_operations.goto_item(quality, self.COPY_SETTING_QUALITY_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)
    
    def select_content_type(self, option):
        #contentType
        self.dial_common_operations.goto_item(self.COPY_SETTING_CONTENTTYPE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_CONTENTTYPE_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_CONTENTTYPE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)

    def select_color_mode(self, option):
        #colorMode
        self.dial_common_operations.goto_item(self.COPY_SETTING_COLORMODE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_COLORMODE_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_COLORMODE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)
    
    def select_original_size(self, option):
        #originalSize
        self.dial_common_operations.goto_item(self.COPY_SETTING_ORIGINALSIZE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_ORIGINALSIZE_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_ORIGINALSIZE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)

    def select_pages_per_sheet_option(self, option):
        #pagesPerSheet
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAGESPERSHEET_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_PAGESPERSHEET_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_PAGESPERSHEET_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)
    
    def select_quality_option(self, option):
        # quality 
        self.dial_common_operations.goto_item(self.COPY_SETTING_QUALITY_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_QUALITY_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_QUALITY_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)

    def select_copy_side(self, option):
        #CopySides
        self.dial_common_operations.goto_item(self.COPY_SETTING_SIDE_MODE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_SIDE_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_SIDE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)
    
    def go_to_paper_selection(self):
        #PaperSelection
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_VIEW)
    
    def select_paper_tray_option(self, selected_option):
        # Paper Tray
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_TRAY_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_TRAY_VIEW, timeout = 9.0)
        self.dial_common_operations.goto_item(selected_option, self.COPY_SETTING_PAPERSELECTION_TRAY_VIEW, 0)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_VIEW, timeout = 9.0)
    
    def select_paper_type_option(self, option):
        # Paper Type
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON, 180)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_VIEW, timeout = 9.0)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_VIEW, timeout = 9.0)

    def select_media_size_option(self, option):
        # # media size
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON, 0)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_VIEW, timeout = 9.0)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_VIEW, 180)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_VIEW, timeout = 9.0)

    def enable_pageflipUp(self):
        self.dial_common_operations.goto_item(self.COPY_PAGEFLIPUP_SWITCH, self.COPY_SETTING_VIEW, 0)

    def change_collate(self):
        # collate 
        self.dial_common_operations.goto_item(self.COPY_COLLATE_TOGGLE_SWITCH, self.COPY_SETTING_VIEW, 180)
    
    def select_resize_option(self, option):

        #resize
        self.dial_common_operations.goto_item(self.COPY_SETTING_RESIZE_BUTTON, self.COPY_SETTING_VIEW, 180)
        assert self._spice.wait_for(self.COPY_SETTING_RESIZE_VIEW)
        self.dial_common_operations.goto_item(option, self.COPY_SETTING_RESIZE_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_VIEW, timeout = 9.0)

    def go_back_to_setting_from_paper_selection(self):
         # BACK TO SETTING
        self.dial_common_operations.back_button_press(self.COPY_SETTING_PAPERSELECTION_VIEW, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60) 


    def select_scan_settings_lighter_darker(self, lighter_darker: int = 1, dial_value=0):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        self.dial_common_operations.goto_item(self.COPY_LIGHTER_DARKER_SLIDER, self.COPY_SETTING_VIEW, dial_value=dial_value, select_option=False)
        assert self._spice.wait_for(self.COPY_LIGHTER_DARKER_SLIDER)
        current_value = self._spice.query_item(self.COPY_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]
        logging.info("Current lighter_darker value is " + current_value)

        assert lighter_darker >= 1 and lighter_darker <= 9 , "Lighter/Darker value is out of range"

        if (lighter_darker != int(current_value)):
            if (lighter_darker > int(current_value)):
                dial_value = 180
            else:
                dial_value = 0

            currentButton = self._spice.query_item(self.COPY_LIGHTER_DARKER_SLIDER)
            currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
            while (int(current_value) != lighter_darker):
                #
                time.sleep(1)
                if (lighter_darker < int(current_value)):
                    currentButton.mouse_wheel(0,0)
                elif (lighter_darker > int(current_value)):
                    currentButton.mouse_wheel(180,180)    
                time.sleep(1)
                current_value = self._spice.query_item(self.COPY_LIGHTER_DARKER_SLIDER + " SpiceText")["text"]

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
        self.dial_common_operations.back_button_press(self.COPY_SETTING_VIEW, self.COPY_LANDING_VIEW, index = 1, timeout_val = 60)   
    
    def back_to_homescreen(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen to Option screen.
        UI Flow is Landing screen->Home screen
        '''
        self.dial_common_operations.back_button_press(self.COPY_LANDING_VIEW, "#HomeScreenView", index = 0, timeout_val = 60)  

    def start_copy(self, dial_value=0):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        self.dial_common_operations.goto_item(self.COPY_BUTTON, self.COPY_LANDING_VIEW, dial_value=dial_value)
    
    def select_copy_2sided_operation(self, operation_type:str):
        '''
        UI should be in Prompt screen.
        Navigates to Side screen starting from Prompt screen.
        UI Flow is Prompt screen->select option
        '''
        assert self._spice.wait_for(self.COPY_2_SIDED_PROMPT, timeout = 9.0)
        self.dial_common_operations.goto_item(self.COPY_2_SIDED_PROMPT, operation_type, 180, False)

        if (self._spice.query_item(operation_type)["activeFocus"] == False):
            copy_prompt = self._spice.wait_for(self.COPY_2_SIDED_PROMPT)
            while (self._spice.query_item(operation_type)["activeFocus"] == False):
                copy_prompt.mouse_wheel(180, 180)
            selected_button = self._spice.query_item(
                operation_type + " SpiceText")
            selected_button.mouse_click()
        else:

            self.dial_common_operations.goto_item(self.COPY_2_SIDED_PROMPT, operation_type, 180, True)
        time.sleep(2)

    def verify_selected_quickset_name(self, net,  stringId):
        '''
        This is helper method to verify selected quickset
        UI flow Landing Page-> Check Copy QuicksetSelected Button
        '''
        assert self._spice.wait_for(self.COPY_LANDING_VIEW)
        assert self._spice.wait_for(self.COPY_QUICKSET_BUTTON)
        self.dial_common_operations.goto_item(self.COPY_QUICKSET_BUTTON, self.COPY_LANDING_VIEW, 180, False)
        assert self._spice.query_item(self.COPY_QUICKSET_BUTTON + " SpiceText")[
            "text"] == LocalizationHelper.get_string_translation(net, stringId)
    
    def save_as_default_copy_ticket(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        self.dial_common_operations.goto_item(self.COPY_QUICKSET_SAVE_BUTTON, self.COPY_LANDING_VIEW, 0, True)
        self.dial_common_operations.goto_item(self.COPY_AS_DEFAULT_BUTTON, self.COPY_QUICKSET_SAVE_OPTION_VIEW, 180, True)
        assert self._spice.wait_for(self.COPY_LANDING_VIEW)
    
    def goto_copy_quickset_view(self):
        '''
        This is helper method to goto copy quickset
        UI flow Select Landing-> click on any quickset button
        '''
        self.dial_common_operations.goto_item(self.COPY_QUICKSET_BUTTON, self.COPY_LANDING_VIEW, 180, True)
        self._spice.wait_for(self.COPY_QUICKSET_LIST_VIEW)

    def select_copy_quickset(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        self._spice.wait_for(quickset_name)
        self.dial_common_operations.goto_item(quickset_name, self.COPY_QUICKSET_LIST_VIEW, 180, True)
        self._spice.wait_for(self.COPY_LANDING_VIEW)
        time.sleep(2)

    def check_copy_home_screen_under_menu_app(self, spice, net):
        excepted_str = spice.common_operations.get_expected_translation_str_by_str_id(net, "cCopy")
        currentScreen = spice.wait_for("#documentCopyMenuButton SpiceText" ,20)
        assert excepted_str == currentScreen["text"],"Failed to find document"
        logging.info("document is shown at copy screen")
    
    def check_copy_default_screen(self,spice,net):
        excepted_str = spice.common_operations.get_expected_translation_str_by_str_id(net, "cDefault")
        currentScreen = spice.wait_for("#QuickSetSelectedButton SpiceText" ,20)
        assert excepted_str == currentScreen["text"],"Failed to find default"
        logging.info("default is shown at copy screen")
    
    def check_copy_delete_quickset_successfully(self, copy_name):
        try:
            copy_quickset_option = self._spice.wait_for(f"#{copy_name}")
            assert not copy_quickset_option, f"Fail to delete quickset <{copy_name}>"
        except TimeoutError:
            logging.info(f"Success to delete quickset <{copy_name}>")

    def check_spec_on_copy_home(self, net):
        """
        check spec on COPY HOME
        @param net:
        @return:
        """
        logging.info("check the str on Home Copy screen")
        time.sleep(2)
        self.dial_common_operations.verify_string(net, self.COPY_HOME_STR_ID, self.COPY_HOME_TITLE_LOCATOR)
        self.dial_common_operations.verify_string(net, self.DEFAULT_AND_QUICK_SETS_STR_ID, self.DEFAULT_AND_QUICK_SETS_LOCATOR)
        self.dial_common_operations.verify_string(net, self.DEFAULT_STR_ID, self.COPY_QUICKSET_BUTTON)
        self.dial_common_operations.verify_string(net, self.OPTIONS_STR_ID, self.COPY_OPTION_BUTTON)
        self.dial_common_operations.verify_string(net, self.COPY_HOME_STR_ID, self.COPY_BUTTON)

    def check_spec_on_copy_options_list(self, net):
        """
        check spec on OPTIONS_LIST
        @param net:
        @return:
        """
        logging.info("check the str on options screen")
        self.dial_common_operations.verify_string(net, self.OPTIONS_LIST_HEADER_STR_ID, self.COPY_SETTING_LIST_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.CONTENT_TYPE_STR_ID, self.COPY_SETTING_CONTENT_TYPE_VALUE)
        self.dial_common_operations.verify_string(net, self.COLOR_BUTTON_STR_ID, self.COPY_SETTING_COLOR_BUTTON_VALUE)
        self.dial_common_operations.verify_string(net, self.SIDES_STR_ID, self.COPY_SETTING_SIDES_VALUE)
        self.dial_common_operations.verify_string(net, self.SIDED_PAGES_UP_STR_ID, self.COPY_SETTING_SIDED_PAGES_UP_STATUS)
        self.dial_common_operations.verify_string(net, self.ORIGINAL_SIZE_STR_ID, self.COPY_SETTING_ORIGINAL_SIZE_VALUE)
        self.dial_common_operations.verify_string(net, self.OUTPUT_STR_ID, self.COPY_SETTING_OUTPUT_VALUE)
        self.dial_common_operations.verify_string(net, self.PAGES_PER_SHEET_STR_ID, self.COPY_SETTING_PAGES_SHEET_VALUE)
        self.dial_common_operations.verify_string(net, self.QUALITY_STR_ID, self.COPY_SETTING_QUALITY_VALUE)
        self.dial_common_operations.verify_string(net, self.COLLATE_STR_ID, self.COPY_SETTING_COLLATE_STATUS)

    def get_copy_pages_per_sheet_options(self):
        """
        Get the pages sheet option
        @return:
        """
        self._spice.wait_for(self.COPY_SETTING_VIEW)
        current_pages_sheet_options = self.dial_common_operations.get_actual_str(self.COPY_SETTING_PAGESPERSHEET_BUTTON)
        logging.info("Current pages sheet settings is: " + current_pages_sheet_options)
        return current_pages_sheet_options

    def goto_copy_pages_per_sheet(self):
        """
        Go to pages per sheet option menu
        @return:
        """
        logging.info("Go to pages per sheet option menu")
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAGESPERSHEET_BUTTON, self.COPY_SETTING_VIEW)
        self._spice.wait_for(self.COPY_SETTING_PAGESPERSHEET_VIEW)

    def check_spec_copy_options_pages_per_sheet(self, net):
        """
        check spec on copy_OptionsPagesPerSheet
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsPagesPerSheet")
        logging.info("check the string about pages per sheet, (1, 2)")
        self.dial_common_operations.verify_string(net, self.PAGES_PER_SHEET_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.PAGES_SHEET_ONE_STR_ID, self.COPY_SETTING_PAGESPERSHEET_ONEUP_BUTTON)
        self.dial_common_operations.verify_string(net, self.PAGES_SHEET_TWO_STR_ID, self.COPY_SETTING_PAGESPERSHEET_TWOUP_BUTTON)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)  

    def check_copy_options_sides_and_select_side(self, net, side = "1_1_sided"):
        """
        check spec on copy_OptionsSides
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsSides")
        logging.info("check the string about Sides, (1 to 1-Sided, 1 to 2-Sided, 2 to 1-Sided, 2 to 2-Sided)")
        self.dial_common_operations.verify_string(net, self.COPY_SETTING_HEADER_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.COPY_SIDE_1_TO_1_STR_ID, self.COPY_SETTING_SIDE_1_TO_1_BUTTON)
        self.dial_common_operations.verify_string(net, self.COPY_SIDE_1_TO_2_STR_ID, self.COPY_SETTING_SIDE_1_TO_2_BUTTON)
        self.dial_common_operations.verify_string(net, self.COPY_SIDE_2_TO_1_STR_ID, self.COPY_SETTING_SIDE_2_TO_1_BUTTON)
        self.dial_common_operations.verify_string(net, self.COPY_SIDE_2_TO_2_STR_ID, self.COPY_SETTING_SIDE_2_TO_2_BUTTON)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)   

    def get_copy_2sided_pages_flip_up_status(self):
        """
        Get the option status of 2 sided pages flip_up
        @return:
        """
        self._spice.wait_for(self.COPY_SETTING_VIEW)
        is_2sided_pages_flip_options_checked = self._spice.query_item(self.COPY_SETTING_SIDED_PAGES_UP_STATUS)["checked"]
        logging.info(f"The current status of 2 sided pages flip_up is <{is_2sided_pages_flip_options_checked}>")
        return is_2sided_pages_flip_options_checked

    def set_copy_2sided_flip_up_options(self, two_sided_options="off"):
        """
        Set the status of 2side flip up option
        @param two_sided_options:str -> on/off
        @return:
        """
        self._spice.wait_for(self.COPY_SETTING_VIEW)
        msg = f"Set 2sided_options to {two_sided_options}"
        logging.info(msg)
        is_2sided_options_checked = self.get_copy_2sided_pages_flip_up_status()

        active_item = self._spice.query_item(self.COPY_SETTING_SIDED_PAGES_UP_STATUS)
        self.dial_common_operations.goto_item(self.COPY_SETTING_SIDED_PAGES_UP_STATUS, self.COPY_SETTING_VIEW, select_option=False)

        if two_sided_options == "off" and is_2sided_options_checked:
            logging.info("need to turn off 2 sided option")
            active_item.mouse_click()
            time.sleep(1)

        if two_sided_options == "on" and not is_2sided_options_checked:
            logging.info("need to turn on 2 sided option")
            active_item.mouse_click()
            time.sleep(1)

        if two_sided_options == "off":
            assert not self.get_copy_2sided_pages_flip_up_status(), f"Failed to set copy_2sided_options: {two_sided_options}"
        else:
            assert self.get_copy_2sided_pages_flip_up_status(), f"Failed to set copy_2sided_options: {two_sided_options}"

    def goto_copy_option_output_scale(self):
        """
        Go to output scale option menu
        @return:
        """
        logging.info("Go to output scale option menu")
        self.dial_common_operations.goto_item(self.COPY_SETTING_RESIZE_BUTTON, self.COPY_SETTING_VIEW)
        self._spice.wait_for(self.COPY_SETTING_RESIZE_VIEW)

    def check_spec_copy_options_output_scale(self, net):
        """
        check spec on copy_OptionsOutputScale
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsOutputScale")
        logging.info("check the string about output scale, (None, Custom 100%, Fit to Page, Full Page/A4 to Letter (91%), Legal to Letter(72%), Letter to A4(94%))")
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_HEADER_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_NONE_STR_ID, self.COPY_SETTING_OUTPUT_SCALE_NONE)
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_FIT_TO_PAGE_STR_ID, self.COPY_SETTING_OUTPUT_SCALE_FIT_TO_PAGE)
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_FULL_PAGE_STR_ID, self.COPY_SETTING_RESIZE_PAGE_LETTER_BUTTON)
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_LEGAL_TO_LETTER_STR_ID, self.COPY_SETTING_OUTPUT_SCALE_LEGAL_TO_LETTER)
        self.dial_common_operations.verify_string(net, self.OUTPUT_SCALE_LETTER_TO_A4_STR_ID, self.COPY_SETTING_OUTPUT_SCALE_LETTER_TO_A4)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)

    def goto_copy_output_scale_custom_menu(self):
        """
        Go to output scale custom option menu
        @return:
        """
        logging.info("Go to output scale custom option menu")
        self.dial_common_operations.goto_item(self.COPY_SETTING_OUTPUT_SCALE_CUSTOM, self.COPY_SETTING_RESIZE_VIEW)
        self._spice.wait_for(self.COPY_SETTING_CUSTOM_SETTINGS_VIEW)

    def set_copy_custom_value_option(self, input_value=0):
        """
        set output scale custom value
        @return:
        """
        logging.info("set output scale custom value")
        excepted_value = 0
        if int(input_value) < 25:
            excepted_value = "Custom 25%"
        elif int(input_value) > 400:
            excepted_value = "Custom 400%"
        else:
            excepted_value = "Custom " + str(input_value)+ "%"
            
        self.select_keyboard.keyboard_set_text_with_out_dial_action(input_string = input_value)
        self._spice.wait_for(self.COPY_SETTING_RESIZE_VIEW)

        current_value = self.get_copy_custom_value_option()
        assert excepted_value == current_value
    
    def get_copy_custom_value_option(self):
        """
        Get the custom value option
        @return:
        """
        self._spice.wait_for(self.COPY_SETTING_RESIZE_VIEW)
        current_custom_value = self.dial_common_operations.get_actual_str(self.COPY_SETTING_OUTPUT_SCALE_CUSTOM)
        logging.info("Current custom value settings is: " + current_custom_value)
        return current_custom_value
    
    def back_to_copy_options_list_view(self, option_mode: str):
        """
        UI should be in the screen where the option content is set.
        Navigates to Option screen
        @param option_mode:
        @return:
        """
        self.dial_common_operations.back_button_press(option_mode, self.COPY_SETTING_VIEW, index=2, timeout_val=60)

    def goto_copy_option_content_type_screen(self):
        """
        Go into option content type screen
        @return:
        """
        self.dial_common_operations.goto_item(self.COPY_SETTING_CONTENTTYPE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_CONTENTTYPE_VIEW)

    def check_spec_on_copy_options_content_type(self, net):
        """
        Check spec on COPY_OptionsContentType
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsContentType")
        logging.info("check the string about Content Type, (Mixed, Text, PhotoGraph)")
        self.dial_common_operations.verify_string(net, self.CONTENT_TYPE_HEADER_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.CONTENT_TYPE_MIXED_STR_ID, self.COPY_SETTING_CONTENTTYPE_MIXED_BUTTON)
        self.dial_common_operations.verify_string(net, self.CONTENT_TYPE_TEXT_STR_ID, self.COPY_SETTING_CONTENTTYPE_TEXT_BUTTON)
        self.dial_common_operations.verify_string(net, self.CONTENT_TYPE_PHOTO_STR_ID, self.COPY_SETTING_CONTENTTYPE_PHOTO_BUTTON)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)

    def goto_copy_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        logging.info("Go to color option menu")
        self.dial_common_operations.goto_item(self.COPY_SETTING_COLORMODE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_COLORMODE_VIEW)

    def check_spec_on_copy_options_color(self, net):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        logging.info("check the string about Color, (color, Grayscale)")
        self.dial_common_operations.verify_string(net, self.COLOR_COLOR_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.COLOR_COLOR_STR_ID, self.COPY_SETTING_COLORMODE_COLOR_BUTTON)
        self.dial_common_operations.verify_string(net, self.COLOR_GRAYSCALE_STR_ID, self.COPY_SETTING_COLORMODE_GRAYSCALE_BUTTON)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)
    
    def goto_quality_option(self):
        """
        Go into quality option screen
        @return:
        """
        logging.info("Go into quality option screen")
        self.dial_common_operations.goto_item(self.COPY_SETTING_QUALITY_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_QUALITY_VIEW)

    def check_spec_on_copy_options_quality(self, net):
        """
        Check spec on COPY_OptionsQuality
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsQuality")
        logging.info("check the string about Quality, (Standard, Draft, Best)")
        self.dial_common_operations.verify_string(net, self.QUALITY_HEADER_STR_ID, self.COMMON_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.QUALITY_STANDARD_STR_ID, self.COPY_SETTING_QUALITY_NORMAL_BUTTON)
        self.dial_common_operations.verify_string(net, self.QUALITY_DRAFT_STR_ID, self.COPY_SETTING_QUALITY_DRAFT_BUTTON)
        self.dial_common_operations.verify_string(net, self.QUALITY_BEST_STR_ID, self.COPY_SETTING_QUALITY_BEST_BUTTON)
        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)

    def goto_copy_option_original_size_screen(self):
        """
        Go to original size screen
        :return:
        """
        #originalSize
        self.dial_common_operations.goto_item(self.COPY_SETTING_ORIGINALSIZE_BUTTON, self.COPY_SETTING_VIEW)
        assert self._spice.wait_for(self.COPY_SETTING_ORIGINALSIZE_VIEW)

    def check_spec_on_common_list_item_values(self, expected_value_list, net, index = 2, locale: str = "en-US"):
        """
        Check spec when a large number of values appear
        @param expected_value_list, net, locale
        @return:
        """
        logging.info("check the string on current screen")
        size_list = []
        index_value = 0
        # only use 180s to find all paper size/type list, and 180s is enough time
        max_time_out = 180
        while max_time_out > 0:
            try:
                size_text = self._spice.query_item("#RadioButtonListLayout #SpiceRadioButton SpiceText", index_value)["text"]
                size_list.append(size_text)
                index_value = index_value + 1
            except Exception as err:
                logging.warning(f"Failed to find the next value and current index_value is {index_value}")
                break
            time.sleep(1)
            max_time_out = max_time_out - 1
        
        logging.info(f"The data of value list is {size_list}")
        
        assert len(expected_value_list) == len(size_list), "Failed to check all list value"

        for str_id in expected_value_list:
            assert self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id, locale) in size_list, "Failed to get strings"

        logging.info("verify the back button existed")
        self.dial_common_operations.back_button_press(self.COMMON_HEADER_LOCATOR, self.COPY_SETTING_VIEW, index = 2, timeout_val = 60)

    def check_spec_on_original_size(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsOriginalSize
        @param expected_value_list, net, locale
        @return:
        """
        logging.info("check spec on the screen of original size")
        self.check_spec_on_common_list_item_values(expected_value_list, net, index = 2, locale = locale)

    def check_spec_on_copy_paper_size(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsPaperSelectionPaperSize
        @param expected_value_list, net, locale
        @return:
        """
        logging.info("check spec on the screen of paper size")
        self.check_spec_on_common_list_item_values(expected_value_list, net, index = 3, locale = locale)

    def check_spec_on_copy_paper_type(self, expected_value_list, net, locale: str = "en-US"):
        """
        Check spec on CopyOptionsPaperSelectionPaperType
        @param expected_value_list, net, locale
        @return:
        """
        logging.info("check spec on the screen of paper type")
        self.check_spec_on_common_list_item_values(expected_value_list, net, index = 3, locale = locale)

    def goto_copy_paper_size_screen(self):
        """
        Go to media size screen
        :return:
        """
        # # media size
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON, 0)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_VIEW, timeout = 9.0)

    def goto_copy_paper_type_screen(self):
        """
        Go to paper type screen
        :return:
        """
        # Paper Type
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON, 180)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_VIEW, timeout = 9.0)

    def goto_copy_paper_tray_screen(self):
        """
        Go to paper tray screen
        :return:
        """
        # Paper Tray
        self.dial_common_operations.goto_item(self.COPY_SETTING_PAPERSELECTION_TRAY_BUTTON, self.COPY_SETTING_PAPERSELECTION_BUTTON)
        assert self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_TRAY_VIEW, timeout = 9.0)

    def check_spec_on_copy_options_paperSelection(self, net):
        """
        Check spec on COPY_OptionsPaperSelection
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsPaperSelection")
        logging.info("check the string about Paper Selection, Paper Size, Paper Type, Paper Tray")
        self.dial_common_operations.verify_string(net, self.PAPER_SELECTION_PAPER_SIZE_STR_ID, self.PAPER_SIZE_LOCATOR)
        self.dial_common_operations.verify_string(net, self.PAPER_SELECTION_PAPER_TYPE_STR_ID, self.PAPER_TYPE_LOCATOR)
        self.dial_common_operations.verify_string(net, self.PAPER_SELECTION_PAPER_TRAY_STR_ID, self.PAPER_TRAY_LOCATOR)
        self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_MEDIASIZE_BUTTON)
        self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_TRAY_BUTTON)
        self._spice.wait_for(self.COPY_SETTING_PAPERSELECTION_PAPERTYPE_BUTTON)

    def check_spec_on_copy_paper_tray(self, net):
        """
        Check spec copy_options_paperSelection_paperTray
        @param net:
        @return:
        """
        logging.info("check the spec on copy_options_paperSelection_paperTray")
        self.dial_common_operations.verify_string(net, self.PAPER_SELECTION_PAPER_TRAY_STR_ID, self.PAPER_TRAY_HEADER_LOCATOR)
        self.dial_common_operations.verify_string(net, self.TRAY1_STR_ID, self.TRAY1_LOCATOR)
        self.dial_common_operations.verify_string(net, self.TRAY2_STR_ID, self.TRAY2_LOCATOR)
        self.dial_common_operations.verify_string(net, self.TRAY3_STR_ID, self.TRAY3_LOCATOR)
        self.dial_common_operations.verify_string(net, self.AUTOMATIC_STR_ID, self.AUTOMATIC_LOCATOR)
