import logging
import time
from random import randrange

from dunetuf.ui.uioperations.ProSelectOperations.SuppliesUIProSelectOperations import SuppliesUIProSelectOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class SuppliesUIProSelectHybridOperations(SuppliesUIProSelectOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

        self.SUPPLIES_ALERT_TITLE_CSTRINGS = {
            "cartridge_low"                         : "cCartridgesLow",
            "genuine_hp_cartridge"                  : "cHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cAlteredClonedCartridgesInstalled",
            "reman_cartridge"                       : "cNonHPRemanufacturedInstalled",
            "used_cartridge"                        : "cUsedOrCounterfeitCartridgesInstalled",
            "used_or_refilled"                      : "cUsedRefilledCartridgesDetected",
            "incompatible_cartridge"                : "cIncompatibleCartridges",
            "cartridge_wrong_slot"                  : "cCartridgesWrongSlot",
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
            "cartridge_beyond_very_low_continue"    : "cCartridgesVeryLowPrompt",
            "cartridge_beyond_very_low_prompt"      : "cCartridgesPromptVeryLow",
            "cartridge_beyond_very_low_warning"     : "cCartridgesVeryLowContinue"
            }

    def set_very_low_behavior_ui(self, spice, cartridge, setting):
        if cartridge == 0:
            self.set_black_very_low_behavior_ui(spice, setting)
        else:
            self.set_color_very_low_behavior_ui(spice, setting)

    def set_black_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : "#stop", "Continue" : "#continue_", "Prompt to Continue" : "#prompt"}
        spice.common_operations.goto_item(elementDict[setting], "#MenuSelectionListblackVeryLowAction")

    def set_color_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : "#stop", "Continue" : "#continue_", "Print Black" : "#printBlack", "Prompt to Continue" : "#prompt"}
        spice.common_operations.goto_item(elementDict[setting], "#MenuSelectionListcolorVeryLowAction")

    def validate_cartridge_very_low_behavior_with_cdm(self, cdm, type, property):
        """
        Verifies the cartridge 'Very Low Behavior' setting changed through UI is reflected in CDM
        """
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        assert result[type +'VeryLowAction'] == property, type +" Cartridge - Very Low Behavior is not set to " + property

    def check_alert_icon_display(self):
         """Check Error Icon
         """
         alertIcon = self._spice.query_item(self.message_icon)
         self._spice.wait_for(self.message_icon)
         assert alertIcon["visible"] is True, 'Icon hybrid not visible'
         assert str(alertIcon["icon"]) == str("qrc:/images/+hybridTheme/error_xs.json")

    def check_alert_informative_icon_display(self):
         """Check Informative Icon
         """
         alertIcon = self._spice.query_item(self.message_icon)
         self._spice.wait_for(self.message_icon)
         assert alertIcon["visible"] is True, 'Icon not visible'
         assert str(alertIcon["icon"]) == str("qrc:/images/+hybridTheme/information_xs.json")

    def settings_supplies_verylowbehavior(self, spice, cdm, cartridge = 0):
        """
        Verifies the different black or color cartridge settings for 'Very Low Behavior'
        """
        cartridge_type = "black" if cartridge == 0 else "color"

        # Check 'Stop' setting
        self.set_very_low_behavior_ui(spice, cartridge, "Stop")
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "stop")

        # Check 'Continue' setting
        self.set_very_low_behavior_ui(spice, cartridge, "Continue")
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "continue")

        # Check 'Prompt to Continue' setting
        self.set_very_low_behavior_ui(spice, cartridge, "Prompt to Continue")
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "prompt")

        # Check 'Print Black' setting if cartridge is color
        if cartridge_type == "color":
            self.set_very_low_behavior_ui(spice, cartridge, "Print Black")
            self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "printBlack")

        # Return to default setting
        self.set_very_low_behavior_ui(spice, cartridge, "Continue")

    def settings_supplies_lowwarningthreshold_mono(self, spice, cdm):
        """
        Verifies black cartridge 'Low Warning Threshold' slider and absence of color sliders
        """
        # Color cartridges are slider[0-2] and black is always slider3
        # Try to access color sliders first, exception expected
        for index in range(3):
            color_found = False
            try:
                slider_bar = spice.wait_for("#slider" + str(index))
                color_found = True
            except:
                logging.info("Success: Color slider not found on Mono printer")
            assert color_found == False, "Error: Color slider found on Mono printer"

        # Test black slider
        slider_bar = spice.wait_for("#slider" + str(3))

        initial_value = slider_bar["value"]
        random_value = randrange(10,50)
        while initial_value == random_value:
            random_value = randrange(10,50)
            logging.info("Re-rolled random value to: " + str(random_value))

        slider_bar.__setitem__('value', random_value)
        assert slider_bar["value"] == random_value, "Error: Slider value did not update"

        # Give CDM some time to update the value
        time.sleep(1)

        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        # Black cartridge is index 0
        assert random_value == result["lowThresholdsPerSupply"][0]["threshold"], "Error: 'Low Warning Threshold' values from UI and CDM are not equal"
        # Return slider to initial value
        slider_bar.__setitem__('value', initial_value)

    def verify_supplies_summary_information_mono(self, spice, cartridgeCdmData, net):
        """
        Validate black supply, ensure color supplies do not appear
        """
        # Verify we are at the supplies summary
        headerText = spice.query_item("#suppliesSummary #levelsApproximatelText #Version2Text")["text"]
        expectedHeaderText = LocalizationHelper.get_string_translation(net, "cEstimatedLevelsPlural")
        assert headerText == expectedHeaderText, "Header text mismatch"

        # Validate black cartridge
        cartridge = spice.query_item("#gauge0")
        cartridgeColor = spice.query_item("#gauge0 #suppliesGauge #ContentItem #ContentItemText")["text"]
        assert cartridgeColor == cartridgeCdmData["publicInformation"]["supplyColorCode"], "UI and CDM supply color codes don't match"
        self.validate_cartridge_details_with_cdm(cartridgeCdmData, cartridge)

        # Try to query color cartridge gauges, exceptions expected
        colorFound = False
        for index in range(1,4):
            try:
                spice.query_item("#gauge" + str(index))
                colorFound = True
            except:
                logging.info("Success: Color gauge not found on Mono printer")
            assert colorFound == False, "Error: Color gauge found on Mono printer"