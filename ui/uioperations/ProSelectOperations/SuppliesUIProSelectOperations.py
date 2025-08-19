#########################################################################################
# @file      SuppliesUIProSelectOperations.py
# @author    Neha Patel(neha.patel@hp.com)
# @date      27-10-2021
# @brief     Implementation for all the Supplies Message Layout operations
# (c) Copyright HP Inc. 2021. All rights reserved.
###########################################################################################
import time
import logging
from dunetuf.cdm import CDM
from datetime import datetime
from dunetuf.network.net import Network
import dunetuf.metadata as product_metadata
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.BaseOperations.ISuppliesAppUIOperations import ISuppliesAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds
from dunetuf.utility.retry import Retry
from dunetuf.configuration import Configuration
class SuppliesUIProSelectOperations(ISuppliesAppUIOperations):
    
    def __init__(self, spice):
        self.maxtimeout = 10
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.homemenu = MenuAppProSelectUIOperations(self._spice)
        configuration = Configuration(CDM(self._spice.ipaddress))
        is_enterprise = configuration.familyname == 'enterprise'

        self.SUPPLIES_ALERT_TITLE_CSTRINGS = {
            "cartridge_low"                         : "cCartridgesLow",
            "genuine_hp_cartridge"                  : "cHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cAlteredClonedCartridgesInstalled",
            "reman_cartridge"                       : "cNonHPRemanufacturedInstalled",
            "used_cartridge"                        : "cUsedOrCounterfeitCartridgesInstalled",
            "reman_used_cartridge"                  : "cUsedCartridgesInstalled",
            "used_or_refilled"                      : "cUsedRefilledCartridgesDetected",
            "incompatible_cartridge"                : "cIncompatibleCartridges",
            "cartridge_wrong_slot"                  : "cCartridgeWrongSlot" if is_enterprise else "cCartridgesWrongSlot",
            "missing_cartridge"                     : "cCartridgesMissingTitle",
            "memory_error"                          : "cProblemCartridge",
            "missing_elabel"                        : "cCartridgeMemoryMissing",
            "unauthorized_cartridge"                : "cUnauthorizedCartridgesInstalled",
            "protected_cartridge"                   : "cHPProtectedCartridgesInstalled",
            "non_hp_chip"                           : "cNonHPChipDetected",
            "alienation_detection"                  : "cAlignmentErrorTitle",
            "cartridge_very_low_prompt"             : "cCartridgesVeryLow",
            "cartridge_very_low_stop"               : "cCartridgesVeryLow",
            "cartridge_very_low_continue"           : "cCartridgesVeryLow",
            "cartridge_very_low_print_black"        : "cCartridgesVeryLow",
            "long_life_consumable_low"              : "cTransferKitReplaceSoon",
            "long_life_consumable_very_low"         : "cTransferKitReplaceNow",
            "cartridge_very_low_prompt_title"       : "cPromptAgain",
            "cartridge_very_low_continue_title"     : "cContinueOptions",
            "micr_cartridge_low"                    : "cReplaceMICRCartridge",
            "non_micr_cartridge"                    : "cInstallMICRCartridge",
            "missing_micr_cartridge"                : "cInstallMICRCartridge",
            "cartridge_beyond_very_low_continue"    : "cBeyondVeryLow",
            "cartridge_beyond_very_low_prompt"      : "cBeyondVeryLow",
            "cartridge_beyond_very_low_warning"     : "cBeyondVeryLow"
            }

        self.SUPPLIES_ALERT_CONTENT_CSTRINGS = {
            "cartridge_low"                         : "cIndicatedCartridgesLow",
            "cartridge_very_low_continue"           : "cCartridgesVeryLowContinue",
            "cartridge_very_low_print_black"        : "cPrinterConfiguredPrintBlackShort",
            "cartridge_very_low_prompt"             : "cCartridgesVeryLowPrompt",
            "cartridge_very_low_stop"               : "cCartridgesConfiguredStopVeryLow",
            "genuine_hp_cartridge"                  : "cOriginalHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cDetectedNoGuaranteeChip",
            "reman_cartridge"                       : "cNonHPRemanufacturedCartridgesInstalled",
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails",
            "used_cartridge"                        : "cIndicatedCartridgesUsed",
            "used_or_refilled"                      : "cCartridgesRefilledRemanufactured",
            "incompatible_cartridge"                : "cIndicatedIncompatibleCartridges",
            "cartridge_wrong_slot"                  : "cWrongSlotRemoveReinsert",
            "missing_cartridge"                     : "cMissingSupplies",
            "memory_error"                          : "cCartridgesNotCommunicating",
            "missing_elabel"                        : "cMissingElabel",
            "unauthorized_cartridge"                : "cUnauthorizedAdminConfigured",
            "protected_cartridge"                   : "cCartridgeProtectionAntiTheft",
            "non_hp_chip"                           : "cDSFailedNonHPChip",
            "alienation_detection"                  : "cAlignmentErrorReplaceCartridgesPersists",
            "long_life_consumable_low"              : "cScheduleTransferKitReplaceSoon",
            "long_life_consumable_very_low"         : "cScheduleTransferKitReplaceNow",
            "printer_failure"                       : "cPrinterFailureLarge",
            "micr_cartridge_low"                    : "cReplaceMICRCartridgeDetails",
            "non_micr_cartridge"                    : "cNotMICRCartridge",
            "missing_micr_cartridge"                : "cNotMICRCartridge",
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails",
            "missing_micr_cartridge"                : "cNotMICRCartridge",
            "cartridge_beyond_very_low_continue"    : "cCartridgesVeryLowPrompt",
            "cartridge_beyond_very_low_prompt"      : "cCartridgesPromptVeryLow",
            "cartridge_beyond_very_low_warning"     : "cCartridgesVeryLowContinue"
            }

    message_layout = "#MessageLayout"
    message_icon = "#MessageIcon"
    supplies_icon = "#DetailIcons"
    TRANSFER_KEY_DETAIL_ID = "#Version1Text"
    COMMON_ALERT_DETAIL_ID = "#Version2Text"
    COMMON_TITLE_ID = "#Version1Text"
    PROMPT_TITLE_ID = "#RadioButtonListLayout #Header #Version1Text"
    PROMPT_TITLE_ID_COLOR = "#RadioButtonListLayout #Header #Version1Text"
    ALERT_BUTTON = "#HideButton"
    COMMON_TITLE_SCREEN_ID = 0
    COMMON_ALERT_DETAIL_IDX = 3
    TRANSFER_KEY_DETAIL_IDX = 2
    COMMON_TITLE_IDX = 1
    REAR_DOOR_OPEN_TITLE_ID = "#doorOpen3Window #TitleText #Version1Text"
    REAR_DOOR_OPEN_DETAIL_ID = "#doorOpen3Window #DetailTexts #Version2Text"
    COMMON_ALERT_TEXT_ID = "#Version1Text"
    COMMON_ALERT_TEXT_IDX = 2
    COMMON_STATUS_DETAIL_ID = "#Version2Text"
    COMMON_STATUS_DETAIL_IDX = 4
    COMMON_STATUS_TITLE = "#Spicebutton"
    COMMON_STATUS_TITLE_IDX = 11
    ALERT_BTN = "#Hide"
    ALERT_BTN1 = "#HideButton"
    JAM_CARTRIDGE_DOOR_TITLE_ID = "#jamAutoNavWindow #TitleText #Version1Text"
    JAM_CARTRIDGE_DOOR_DETAIL_ID = "#jamAutoNavWindow #DetailTexts #Version2Text"
    CARTRIDGE_DOOR_OPEN_TITLE_ID = "#doorOpen2Window #TitleText #Version1Text"
    CARTRIDGE_DOOR_OPEN_DETAIL_ID = "#doorOpen2Window #DetailTexts #Version2Text"
    TRAY1_OVERFILLED_TITLE_ID = "#trayOverfilled1Window #TitleText #Version1Text"
    TRAY1_OVERFILLED_DETAIL_ID = "#trayOverfilled1Window #DetailTexts #Version2Text"
    TRAY2_OVERFILLED_TITLE_ID = "#trayOverfilled2Window #TitleText #Version1Text"
    TRAY2_OVERFILLED_DETAIL_ID = "#trayOverfilled2Window #DetailTexts #Version2Text"
    TRAY3_OVERFILLED_TITLE_ID = "#trayOverfilled3Window #TitleText #Version1Text"
    TRAY3_OVERFILLED_DETAIL_ID = "#trayOverfilled3Window #DetailTexts #Version2Text"


    supplies_spice_window = ["genuineHPSupplyFlowWindow",
                            "nonHPSupplyFlowWindow",
                            "usedSupplyPromptWindow",
                            "blackSupplyVeryLowFlowWindow",
                            "colorSupplyVeryLowFlowWindow",
                            "longLifeConsumableLowWindow",
                            "longLifeConsumableVeryLowWindow",
                            "cartridgeBeyondVeryLowFlowWindow",
                            "cartridgeBeyondVeryLowPromptFlowWindow",
                            "cartridgeLowStop1Window",
                            "cartridgeLowWindow",
                            "cartridgeLow1Window",
                            "cartridgeLow2Window",
                            "cartridgeLow3Window",
                            "cartridgeLow4Window",
                            "cartridgeVeryLowContinueWindow",
                            "cartridgeVeryLowContinue1Window",
                            "cartridgeVeryLowContinue2Window",
                            "cartridgeVeryLowContinue3Window",
                            "cartridgeVeryLowContinue4Window",
                            "cartridgeVeryLowPrintingBlackOnlyWindow",
                            "cartridgeVeryLowPrintingBlackOnly1Window",
                            "cartridgeVeryLowPrintingBlackOnly2Window",
                            "cartridgeVeryLowPrintingBlackOnly3Window",
                            "cartridgeVeryLowPrintingBlackOnly4Window",
                            "cartridgeVeryLowStopWindow",
                            "cartridgeVeryLowStop1Window",
                            "cartridgeVeryLowStop2Window",
                            "cartridgeVeryLowStop3Window",
                            "cartridgeVeryLowStop4Window",
                            "incompatibleCartridgeWindow",
                            "incompatibleCartridge1Window",
                            "incompatibleCartridge2Window",
                            "incompatibleCartridge3Window",
                            "incompatibleCartridge4Window",
                            "cartridgeMemoryMissingWindow",
                            "cartridgeMemoryMissing1Window",
                            "cartridgeMemoryMissing2Window",
                            "cartridgeMemoryMissing3Window",
                            "cartridgeMemoryMissing4Window",
                            "cartridgeWrongSlotWindow",
                            "cartridgeWrongSlot1Window",
                            "cartridgeWrongSlot2Window",
                            "cartridgeWrongSlot3Window",
                            "cartridgeWrongSlot4Window",
                            "cartridgeMissingWindow",
                            "cartridgeMissing1Window",
                            "cartridgeMissing2Window",
                            "cartridgeMissing3Window",
                            "cartridgeMissing4Window",
                            "cartridgeMemoryErrorWindow",
                            "cartridgeMemoryError1Window",
                            "cartridgeMemoryError2Window",
                            "cartridgeMemoryError3Window",
                            "cartridgeMemoryError4Window",
                            "cartridgeUnauthorizedWindow",
                            "cartridgeUnauthorized1Window",
                            "cartridgeUnauthorized2Window",
                            "cartridgeUnauthorized3Window",
                            "cartridgeUnauthorized4Window",
                            "antiTheftEnabledSupplyErrorWindow",
                            "antiTheftEnabledSupplyError1Window",
                            "antiTheftEnabledSupplyError2Window",
                            "antiTheftEnabledSupplyError3Window",
                            "antiTheftEnabledSupplyError4Window",
                            "cartridgeDynamicIntegrityViolationErrorWindow",
                            "cartridgeDynamicIntegrityViolationError1Window",
                            "cartridgeDynamicIntegrityViolationError2Window",
                            "cartridgeDynamicIntegrityViolationError3Window",
                            "cartridgeDynamicIntegrityViolationError4Window",
                            "cartridgeAlienationDetectionErrorWindow",
                            "cartridgeAlienationDetectionError1Window",
                            "cartridgeAlienationDetectionError2Window",
                            "cartridgeAlienationDetectionError3Window",
                            "cartridgeAlienationDetectionError4Window",
                            "cartridgeRefilledFlowWindow",
                            "cartridgeRefilledFlow1Window",
                            "cartridgeRefilledFlow2Window",
                            "cartridgeRefilledFlow3Window",
                            "cartridgeRefilledFlow4Window",
                            "cartridgeBeyondVeryLowWindow",
                            "cartridgeBeyondVeryLow1Window",
                            "cartridgeBeyondVeryLow2Window",
                            "cartridgeBeyondVeryLow3Window",
                            "cartridgeBeyondVeryLow4Window"
                            ]

    def goto_alert_message_layout_screen(self,timeout=7):
        """At Message layout screen
        """
        self._spice.wait_for(self.message_layout,timeout=timeout)

    def goto_statusapp(self, spice):
        #go to status app
        spice.homeMenuUI().goto_status(spice)
        time.sleep(2)

    def menu_navigation_statusapp(self, spice):
        #go to menu navigation
        spice.homeMenuUI().menu_navigation(spice, "#StatusView", "#AlertsList")
        time.sleep(2)

    def check_alert_icon_display(self):
        """Check Error Icon
        """
        alertIcon = self._spice.query_item(self.message_icon)
        self._spice.wait_for(self.message_icon)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/error_xs.json")

    def check_warning_icon_display(self):
        alertIcon = self._spice.query_item(self.message_icon)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/warning_xs.json")

    def get_alert_active_focus_index(self, alert_name="#SuppliesFlowModuleAlert"):
        index = 0
        for idx in [0,1,2,3]:
            try:
                active_index = self._spice.query_item(alert_name, idx)['activeFocus']
                if active_index:
                    index = idx
                    break
            except:
                logging.info("Alert index not found")
        logging.info("Index of the active alert {0} is : {1}".format(alert_name, index))
        return index

    def get_alert_message(self):
        """
        Get the Title Text
        """
        alert_window_name = ""
        index = 0
        logging.info("Collect the Active alert window name or index of active alert.")
        for spice_alert in  self.supplies_spice_window:
            try:
                if self._spice.query_item("#{0}".format(spice_alert))['activeFocus']:
                    alert_window_name = "#{0} ".format(spice_alert)
                    logging.info("Active alert window name : {0}".format(alert_window_name))
                    break
            except:
                pass
        if alert_window_name == "":
            index = self.get_alert_active_focus_index()
        actual_title_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #TitleText #Version1Text".format(alert_window_name), index)["text"]
        return actual_title_text
    
    def check_alert_message(self, expected_title_text):
        """
        Test to validate the Title Text
        """
        logging.info("Expected title text : %s", expected_title_text)   
        assert expected_title_text == Retry.until_equal(self.get_alert_message, expected_title_text)

    def check_alert_prompt_title_text(self, prompt_text, object_id, index=0):
        """
        Test to validate the Prompt Title Text
        """
        logging.info("Check Prompt Title text")
        time.sleep(2)
        self._spice.wait_for(object_id)
        currentPromptText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified prompt again Title text: %s ", currentPromptText)
        assert currentPromptText == prompt_text, 'incorrect prompt again title text'

    def check_very_low_prompt_again_screen(self):
        """
        Test to validate the Prompt Again mandatory button and Selecting the prompt option..
        """
        assert self._spice.wait_for("#NeverStop #RadioButtonText") ["visible"] is True, 'Icon not visible'
        assert self._spice.wait_for("#NeverStop #SpiceRadioButton") ["checked"] == True
        logging.info("Selecting the prompt option")
        self._spice.wait_for("#RadioButtonListLayout").mouse_wheel(180,180)
        logging.info("Selecting the prompt option")
        self._spice.wait_for("#100PagesToStop #SpiceRadioButton").mouse_click()

    def check_very_low_alert_prompt_again_options(self):
        """
        Test to validate the Prompt buttons Text and button click.
        """
        prompt_options_list = ["#NeverStop #RadioButtonText","#100PagesToStop #SpiceRadioButton","#200PagesToStop #SpiceRadioButton","#300PagesToStop #SpiceRadioButton","#400PagesToStop #SpiceRadioButton"]
        for prompt_option in prompt_options_list:
            self._spice.wait_for("#RadioButtonListLayout").mouse_wheel(180,180)
            self._spice.wait_for(prompt_option)
            assert self._spice.wait_for(prompt_option)["visible"] is True, 'Icon not visible'
        assert self._spice.wait_for("#NeverStop #SpiceRadioButton") ["checked"] == True
        logging.info("Selecting the prompt option")
        self._spice.wait_for("#400PagesToStop #SpiceRadioButton").mouse_click()

    def check_alert_continue_option_title_text(self,continue_text):
        """
        Test to validate the Continue Option Title Text
        """
        logging.info("Check Continue Option Title text")
        time.sleep(2)
        self._spice.wait_for("#colorSupplyVeryLowFlow #Header #Version1Text",3)
        assert self._spice.wait_for("#colorSupplyVeryLowFlow #Header #Version1Text",3)["text"] ==  continue_text, 'Title text incorrect'
        logging.info("Verified Title text: %s ", continue_text)

    def check_alert_continue_options_and_select_print_color_option(self):
        """
        Test to validate the Continue Option buttons and Selecting the print in color option.
        """
        assert self._spice.wait_for("#permissionPrintBlack #SpiceButton")["visible"] is True, 'Button not visible'
        assert self._spice.wait_for("#permissionPrintColor #SpiceButton")["visible"] is True, 'Button not visible'
        logging.info("Selecting the print in color option")
        menuObject = self._spice.wait_for("#MessageLayout")
        menuObject.mouse_wheel(0,360)
        self._spice.wait_for("#permissionPrintColor #SpiceButton").mouse_click()

    def check_alert_continue_options_and_select_print_black_option(self):
        """
        Test to validate the Continue Option buttons and Selecting the print in black option.
        """
        assert self._spice.wait_for("#permissionPrintBlack #SpiceButton")["visible"] is True, 'Button not visible'
        assert self._spice.wait_for("#permissionPrintColor #SpiceButton")["visible"] is True, 'Button not visible'
        logging.info("Selecting the print in black option")
        self._spice.wait_for("#permissionPrintBlack #SpiceButton").mouse_click()

    def check_alert_statusapp_title_text(self, title_text, object_id, index):
        """
        Test to validate the a Title Text of alert in statusapp screen
        """
        logging.info("Check Title text of statusapp screen")
        titleText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified statusapp Title text: %s ", titleText)
        assert titleText == title_text, 'incorrect Title text in status app'

    def check_alert_informative_icon_display(self):
        """Check Informative Icon
        """
        alertIcon = self._spice.query_item(self.message_icon)
        self._spice.wait_for(self.message_icon)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/information_xs.json")

    def check_alert_supply_icon_display(self):
        """
        Test to validate the Supplies Icon
        """
        supplyIcon = self._spice.query_item(self.supplies_icon)
        logging.info("Check Supplies Icon visibility")
        icon_display = supplyIcon["visible"]
        # Check Icon Visibility
        assert supplyIcon["visible"] is True, 'Supplies Icon not visible'
        logging.info(f"Verified icon visible is :{icon_display}")

    def get_alert_message_details(self):
        """
        Get the Alert text
        """
        alert_window_name = ""
        index = 0
        logging.info("Collect the Active alert window name or index of active alert.")
        for spice_alert in  self.supplies_spice_window:
            try:
                if self._spice.query_item("#{0}".format(spice_alert))['activeFocus']:
                    alert_window_name = "#{0} ".format(spice_alert)
                    logging.info("Active alert window name : {0}".format(alert_window_name))
                    break
            except:
                pass
        if alert_window_name == "":
            index = self.get_alert_active_focus_index()
        actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #DetailTexts #Version2Text".format(alert_window_name), index)["text"]
        return actual_detail_text
    
    def check_alert_message_details(self, expected_detail_text):
        """
        Test to validate the Alert text
        """
        logging.info("Expected Detail text : %s", expected_detail_text)
        assert expected_detail_text == Retry.until_equal(self.get_alert_message_details, expected_detail_text)

    def get_alert_button_text(self):
        """
        Get the Alert button text
        """
        alert_window_name = ""
        index = 0
        logging.info("Collect the Active alert window name or index of active alert.")
        for spice_alert in  self.supplies_spice_window:
            try:
                if self._spice.query_item("#{0}".format(spice_alert))['activeFocus']:
                    alert_window_name = "#{0} ".format(spice_alert)
                    logging.info("Active alert window name : {0}".format(alert_window_name))
                    break
            except:
                pass
        if alert_window_name == "":
            index = self.get_alert_active_focus_index()

        button_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #SpiceButton".format(alert_window_name), index)["text"]
        return button_text

    def check_alert_statusapp_detail_text(self, detail_text, object_id, index):
        """
        Test to validate the a Alert text of alert in statusapp screen
        """
        alertText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified statusapp Detail text: %s" , alertText)
        assert alertText == detail_text ,'incorrect Detail text in status app'

    def check_alert_button(self, button_text):
        """
        Test to validate the Button Text (only for simulator)
        """
        btn_ele = self._spice.query_item("#SpiceButton")
        btn_display = self._spice.query_item("#SpiceButton")["visible"]
        logging.info("Check button visible or not")
        assert self._spice.query_item("#SpiceButton")["visible"] is True, 'Button not visible'
        logging.info(f"Verified {button_text} button visible is :{btn_display}")

        logging.info("Check button enable or not")
        btn_enable = self._spice.query_item("#SpiceButton")["enabled"]
        assert self._spice.query_item("#SpiceButton")["enabled"] is True, 'Button is disable'
        logging.info(f"Verified {button_text} button enable is :{btn_enable}")

        buttonText = self._spice.query_item("#SpiceButton")["text"]
        logging.info("Check button Text")

        assert buttonText == button_text, "Button text incorrect"
        logging.info(f"Verified {button_text} Button Text: {buttonText}")
        
        # press button
        logging.info("Press the button")
        self._spice.wait_for("#SpiceButton")
        btn_ele.mouse_click()

    # This method handle only supplies related alert acknowledgment
    def press_alert_button(self, button_id):
        # Scroll to end of the active screen by assuming alert button is available at the end of the screen on dial display.
        # Due to UI design limitation activeFocus and visible properties will be always True even when button is not present in the active screen
        # Refer Bug DUNE-68368
        self._spice.wait_for(query_selector="#SuppliesFlowModuleAlert", timeout=30)
        alert_window_name = ""
        index = 0
        logging.info("Collect the Active alert window name or index of active alert.")
        for spice_alert in  self.supplies_spice_window:
            try:
                if self._spice.query_item("#{0}".format(spice_alert))['activeFocus']:
                    alert_window_name = "#{0} ".format(spice_alert)
                    logging.info("Active alert window name : {0}".format(alert_window_name))
                    break
            except:
                pass
        if alert_window_name == "":
            index = self.get_alert_active_focus_index()
        else:
            index = self.get_alert_active_focus_index(alert_name="{0}#SuppliesFlowModuleAlert".format(alert_window_name))
        currentScreen = self._spice.query_item("{0}#SuppliesFlowModuleAlert".format(alert_window_name), index)
        i = 0
        while i < 20:
            currentScreen.mouse_wheel(180, 180)
            time.sleep(1)
            i = i + 1
        self._spice.query_item("{0}#SuppliesFlowModuleAlert {1}".format(alert_window_name, button_id), index).mouse_click()
        time.sleep(2)

    def goto_menu_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)

    def goto_menu_supplies_tcu_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)

    def verify_tcu_details_screen_information(self,spice,net,status): 
        """
        Function to validate tcu page info
        """
        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.statustext)["text"]
        loc_statusText = LocalizationHelper.get_string_translation(net, status, 'en-US')
        assert statusText.find(loc_statusText) != -1, "Status Text mismatch" 

    def verify_supplies_summary_information(self,spice,catridgeCdmData,index,net):
        """
        Function to validate supplies summary info
        """
        spice.wait_for("#gauge"+ str(index))
        cartridgeInfo = spice.query_item("#gauge"+ str(index))
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)

    def verify_supplies_transferkit_reset(self, spice, udw):
        #navigate to service reset screen
        spice.homeMenuUI().goto_menu_tools_servicemenu_serviceresets(spice, udw)
        time.sleep(2)

        logging.info(" at Transfer Kit Reset Screen")
        spice.homeMenuUI().menu_navigation(spice, "#serviceTestsMenuMenuButton", "#imageTransferKitResetMenuButton")
        time.sleep(2)

    def verify_supplies_transferkit_reset_OK(self, spice, udw):
        #navigate to tansferkit reset
        spice.homeMenuUI().menu_navigation(spice,"#MessageLayout", "#resetButton")
        time.sleep(2)

    def verify_supplies_transferkit_reset_Cancel(self, spice, udw):
        #navigate to tansferkit cancel
        spice.homeMenuUI().menu_navigation(spice,"#MessageLayout", "#Cancel")
        time.sleep(2)

    def verify_cartridge_details_screen_information(self,spice,catridgeCdmData,net):
        """
        Function to validate cartridge detail page info
        """
        spice.homeMenuUI().menu_navigation(spice, "#suppliesSummaryView", "#gauge0")
        spice.wait_for("#supplyCartridgeInformationView")

        spice.wait_for("#gauge0")
        spice.wait_for("#statusDetail")
        spice.wait_for("#installedCartridge")
        spice.wait_for("#printDetails")

        # obtain gauge details from details screen
        suppliesGauge = spice.query_item("#gauge0")
        #validate cartridge details obtained from the detailed screen with cdm data
        self.validate_cartridge_details_with_cdm(catridgeCdmData,suppliesGauge)

    def validate_cartridge_details_with_cdm(self,catridgeCdmData,suppliesGauge):
        """
        Function to validate cartridge details with cdm data
        """
        if( "percentLifeRemaining" in catridgeCdmData):
            assert catridgeCdmData["publicInformation"]["percentLifeDisplay"] == suppliesGauge["suppliesLevel"]
        else:
            print("percentLifeRemaining not exist in tonerCartridge0")

        if( "supplyState" in catridgeCdmData["publicInformation"]):
            assert catridgeCdmData["publicInformation"]["supplyState"] == supplies_state[suppliesGauge["suppliesState"]]
        else:
           print("supplyState not exist in tonerCartridge0")

        if( "levelState" in catridgeCdmData["publicInformation"]):
            assert catridgeCdmData["publicInformation"]["levelState"] == supplies_level_state[suppliesGauge["suppliesLevelState"]]
        else:
           print("levelstate not exist in tonerCartridge0")

    def set_black_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : "#stop", "Continue" : "#continue_", "Prompt to Continue" : "#prompt"}
        spice.common_operations.goto_item(elementDict[setting], "#MenuSelectionListblackVeryLowAction")

    def set_color_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : "#stop", "Continue" : "#continue_", "Print Black" : "#printBlack", "Prompt to Continue" : "#prompt"}
        spice.common_operations.goto_item(elementDict[setting], "#MenuSelectionListcolorVeryLowAction")

    def get_black_very_low_behavior_ui(self, spice):
        return spice.wait_for("#blackVeryLowActionButton SpiceText", 10)["text"]

    def get_color_very_low_behavior_ui(self, spice):
        return spice.wait_for("#colorVeryLowActionButton SpiceText", 10)["text"]

    def close_supply_card_view(self):
        if self._spice.uitheme == "hybridTheme":
            logging.info("Using Keyhandler UDW command for BACK Button: Hybrid UI")
            self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")
        else:
            self._spice.query_item("#BackButton", 1).mouse_click()
        time.sleep(2)

    def get_cartridge_gas_gauge_details(self, spice, index, is_color_printer=True):
        gas_gauge_details = {}
        spice.wait_for("#gauge"+ str(index))
        cartridgeInfo = spice.query_item("#gauge"+ str(index))

        logging.debug("Click cartridge gas gauge, index :: {0}".format(index))
        spice.homeMenuUI().menu_navigation(spice, "#suppliesSummaryView", "#gauge" + str(index))

        try:
            spice.get_screenshot(file_name="ui_supply_status_"+str(index)+".png")
        except:
            pass

        try:
            gas_gauge_details["supplylevel"] = cartridgeInfo["suppliesLevel"]
        except:
            pass
        try:
            gas_gauge_details["supplystate"] = supplies_state[cartridgeInfo["suppliesState"]]
        except:
            pass
        try:
            gas_gauge_details["selectability_number"] = spice.wait_for('#installedCartridge #ValueText')['text']
        except:
            pass
        try:
            gas_gauge_details["supplylevelstate"] = spice.wait_for("#statusDetail #ContentItemText")['text']
        except:
            pass

        logging.debug("Close cartridge gas gauge card after collecting :: {0}".format(gas_gauge_details))
        self.close_supply_card_view()
        return gas_gauge_details

    def verify_status_center_alert_title_and_description(self,spice,loc_title,loc_alert):
        logging.info("Expand the status center dashboard")
        self.goto_statusapp(spice)
        logging.debug("Verify the status center alert title")
        self.check_alert_statusapp_title_text(loc_title,"#SpiceButton",2)
        #Note: Notification description is not applicable for ProSelect

    def click_status_center_alert_screen(self, spice):
        self.menu_navigation_statusapp(spice)

    def set_very_low_alert_prompt_options(self,prompt_option):
        """
        Select very low alert prompt option
        """
        prompt_options_list = {"NeverStop" : "#NeverStop #SpiceRadioButton",
                               "100Pages"  : "#100PagesToStop #SpiceRadioButton",
                               "200Pages"  : "#200PagesToStop #SpiceRadioButton",
                               "300Pages"  : "#300PagesToStop #SpiceRadioButton",
                               "400Pages"  : "#400PagesToStop #SpiceRadioButton"}

        logging.info("Selecting the prompt option")
        self._spice.wait_for(prompt_options_list[prompt_option]).mouse_click()

    def validate_supplies_app(self,spice,cdm,configuration,net):
        logging.info("Validating supplies app screen")
        assert self._spice.wait_for("#suppliesSummaryView")
        product_metadata_dict = product_metadata.get_product_metadata(cdm, configuration)
        transfer_kit_supported = 'TransferKit' in product_metadata_dict['ConsumableSupport']
        if (spice.uitheme == "loTheme" and transfer_kit_supported == True):
            assert self._spice.wait_for("#SuppliesAppApplicationStackView #suppliesSummaryView #suppliesSummary #levelsApproximatelText #Version2Text ")["text"] == str(LocalizationHelper.get_string_translation(net,"cEstimatedLevelsPlural", "en"))
            scrollbtn = self._spice.wait_for("#SuppliesAppApplicationStackView #suppliesSummaryView #suppliesSummary")
            scrollbtn.mouse_wheel(180,180)
            scrollbtn.mouse_wheel(180,180)
            scrollbtn.mouse_wheel(180,180)
            scrollbtn.mouse_wheel(180,180)
            assert self._spice.wait_for("#SuppliesAppApplicationStackView #suppliesSummaryView #suppliesSummary #tcuImageText #statusText")["text"] == 'Transfer Kit'
        else:
            assert self._spice.wait_for("#SuppliesAppApplicationStackView #suppliesSummaryView #suppliesSummary #levelsApproximatelText #Version2Text ")["text"] == str(LocalizationHelper.get_string_translation(net,"cEstimatedLevelsPlural", "en"))

    def goto_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self._spice.home.goto_home_supplies_app()
    
    def ui_shows_validating_state(self):
        try:
            return self._spice.wait_for("#waitingForSupplyAssessmentWindow #Version2Text", timeout=30)["text"] == LocalizationHelper.get_string_translation(Network(self._spice.ipaddress), "cValidatingPleaseWait")
        except:
            self._spice.get_screenshot(file_name="supply_validation_status.png")
            cdm = CDM(self._spice.ipaddress)
            logging.exception("AFTER Wait for validating - handling exception.\nalerts:\n{}".format(cdm.get(cdm.ALERTS)['alerts']))
            return False
    
    def verify_cartridges_ui_alert(self, title, details_key):
        net = Network(self._spice.ipaddress)
        self._spice.wait_ready()
        logging.debug("Verify Current UI state")
        loc_title = LocalizationHelper.get_string_translation(net, title, 'en-US')
        logging.info(f"loc_title: {loc_title}")
        loc_details = LocalizationHelper.get_string_translation(net, self.SUPPLIES_ALERT_CONTENT_CSTRINGS[details_key],'en-US')
        logging.info(f"loc_details: {loc_details}")
        try:
            logging.debug("Spice Objects from current screen :: {0}".format(self._spice.udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._spice.get_screenshot(file_name="supply_ui_alert"+str(timestamp)+".png")
        except:
            pass
        self.check_alert_message(loc_title)
        self.check_alert_message_details(loc_details)


"""CDM - UI Supplies state mapping."""
supplies_state = [
    "ok",
    "inform",
    "warning",
    "error"
]

"""CDM - UI Supplies level state mapping."""
supplies_level_state = [
    "ok",
    "low",
    "veryLow",
    "veryVeryLow",
    "depleted"
]
