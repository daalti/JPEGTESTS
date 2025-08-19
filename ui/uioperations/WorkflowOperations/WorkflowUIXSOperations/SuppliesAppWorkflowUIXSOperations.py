import time
import logging
from random import randrange
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperations import SuppliesAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds

class SuppliesAppWorkflowUIXSOperations(SuppliesAppWorkflowUICommonOperations):

    ALERT_IMAGE_ICON = "#imageObject"
    COMMON_ALERT_TEXT_ID = "#titleObject"
    COMMON_ALERT_TEXT_IDX = 0
    COMMON_STATUS_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_STATUS_DETAIL_IDX = 0
    COMMON_STATUS_TITLE = "#notificationRowAlertTitle #alertStatusCenterText" 
    COMMON_STATUS_TITLE_IDX = 0
    #ALERT_BTN = "#ButtonControl #Background"
    ALERT_BTN = "#Hide"
    ALERT_BTN1 = "#ButtonControl #Background"
    UI_SUPPLIES_APP = "#suppliesSummaryView"
    SUPPLIES_GRID_TAB_LAYOUT = "#suppliesSummaryView"
    CLOSE_SUPPLY_CARD_VIEW = "#closeButton"
    #Alert ObjectIds
    ALERT_DIALOG_WINDOW= "#bodyLayout"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage"
    PROMPT_TITLE_ID = "#promptAgain #titleObject"
    COMMON_TITLE_IDX = 0
    COMMON_ALERT_DETAIL_IDX = 0
    COMMON_TITLE_ID = "#titleObject"
    COMMON_ALERT_DETAIL_ID = "#alertDetailDescription #contentItem"
    ALERT_BUTTON = "AlertModel #FooterView #FooterViewRight #ContentItem SpiceText"
    JAM_CARTRIDGE_DOOR_TITLE_ID = "#jamAutoNavWindow #titleObject"
    JAM_CARTRIDGE_DOOR_DETAIL_ID = "#jamAutoNavWindow #alertDetailDescription #contentItem"
    REAR_DOOR_OPEN_TITLE_ID = "#doorOpen3Window #titleObject"
    REAR_DOOR_OPEN_DETAIL_ID = "#doorOpen3Window #alertDetailDescription #contentItem"
    CARTRIDGE_DOOR_OPEN_TITLE_ID = "#doorOpen2Window #titleObject"
    CARTRIDGE_DOOR_OPEN_DETAIL_ID = "#doorOpen2Window #alertDetailDescription #contentItem"
    TRAY1_OVERFILLED_TITLE_ID = "#trayOverfilled1Window #titleObject"
    TRAY1_OVERFILLED_DETAIL_ID = "#trayOverfilled1Window #alertDetailDescription #contentItem"
    TRAY2_OVERFILLED_TITLE_ID = "#trayOverfilled2Window #titleObject"
    TRAY2_OVERFILLED_DETAIL_ID = "#trayOverfilled2Window #alertDetailDescription #contentItem"
    TRAY3_OVERFILLED_TITLE_ID = "#trayOverfilled3Window #titleObject"
    TRAY3_OVERFILLED_DETAIL_ID = "#trayOverfilled3Window #alertDetailDescription #contentItem"

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

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        configuration = Configuration(CDM(self._spice.ipaddress))
        is_enterprise = configuration.familyname == 'enterprise'

        self.SUPPLIES_ALERT_TITLE_CSTRINGS = {
            "cartridge_low"                         : "cCartridgesLow",
            "cartridge_low_stop"                    : "cSupplyReplace",
            "cartridge_very_low_continue"           : "cCartridgesVeryLow",
            "cartridge_very_low_print_black"        : "cCartridgesVeryLow",
            "cartridge_very_low_prompt"             : "cCartridgesVeryLow",
            "cartridge_very_low_stop"               : "cSupplyReplace" if is_enterprise else "cCartridgesVeryLow",
            "genuine_hp_cartridge"                  : "cHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cAlteredClonedCartridgesInstalled",
            "reman_cartridge"                       : "cNonHPRemanufacturedInstalled",
            "used_cartridge"                        : "cUsedOrCounterfeitCartridgesInstalled",
            "used_or_refilled"                      : "cUsedRefilledDetected" if is_enterprise else "cUsedRefilledCartridgesDetected",
            "incompatible_cartridge"                : "cIncompatibleCartridges",
            "cartridge_wrong_slot"                  : "cCartridgeWrongSlot" if is_enterprise else "cCartridgesWrongSlot",
            "missing_cartridge"                     : "cCartridgesMissingTitle",
            "memory_error"                          : "cProblemCartridge",
            "missing_elabel"                        : "cCartridgeMemoryMissing",
            "unauthorized_cartridge"                : "cUnauthorizedCartridgesInstalled",
            "protected_cartridge"                   : "cProtectedCartridgeInstall" if is_enterprise else "cHPProtectedCartridgesInstalled",
            "non_hp_chip"                           : "cNonHPChipDetected",
            "alienation_detection"                  : "cAlignmentErrorTitle",
            "long_life_consumable_low"              : "cTransferKitReplaceSoon",
            "long_life_consumable_very_low"         : "cTransferKitReplaceNow",
            "cartridge_very_low_prompt_title"       : "cPromptAgain",  # This is for the prompt that appears after choosing a VL continue option
            "cartridge_very_low_continue_title"     : "cContinueOptions", # This is for the prompt that appears after acknowledging the VL prompt
            "micr_cartridge_low"                    : "cReplaceMICRCartridge",
            "non_micr_cartridge"                    : "cInstallMICRCartridge",
            "missing_micr_cartridge"                : "cInstallMICRCartridge",
            "cartridge_beyond_very_low_continue"    : "cBeyondVeryLow",
            "cartridge_beyond_very_low_prompt"      : "cBeyondVeryLow",
            "cartridge_beyond_very_low_warning"     : "cBeyondVeryLow"
            }



        self.SUPPLIES_ALERT_CONTENT_CSTRINGS = {
            "cartridge_low"                         : "cConsiderHavingReplacementLow" if is_enterprise else "cIndicatedCartridgesLow",
            "cartridge_low_stop"                    : "cSupplyIndicatesLowStop",
            "cartridge_very_low_continue"           : "cVeryLowIndicatedCartridge" if is_enterprise else "cCartridgesVeryLowContinue",  # Enterprise should also have cActualSupplyLife cConsiderHavingReplacementVeryLow cSupplyDoesNotNeedReplacePQ, followed by recommended cartridges info
            "cartridge_very_low_print_black"        : "cPrinterConfiguredPrintBlackShort",  # Not defined in Enterprise SMS yet
            "cartridge_very_low_prompt"             : "cSupplyIndicatesVeryLow" if is_enterprise else "cCartridgesVeryLowPrompt",  # Enterprise has additional strings too
            "cartridge_very_low_stop"               : "cSupplyIndicatesVeryLow" if is_enterprise else "cCartridgesConfiguredStopVeryLow",  # Enterprise has additional strings too
            "genuine_hp_cartridge"                  : "cOriginalHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cDetectedNoGuaranteeChip",
            "reman_cartridge"                       : "cNonHPRemanufacturedCartridgesInstalled",  # Not defined in Enterprise SMS yet
            "used_cartridge"                        : "cIndicatedCartridgesUsedCounterfeit" if is_enterprise else "cIndicatedCartridgesUsed",
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails",
            "used_or_refilled"                      : "NOT DEFINED YET IN ENTERPRISE SMS" if is_enterprise else "cCartridgesRefilledRemanufactured",
            "incompatible_cartridge"                : "cIndicatedIncompatibleCartridges",  # Enterprise SMS doesn't provide the string id for this
            "cartridge_wrong_slot"                  : "cWrongPositionHelp" if is_enterprise else "cWrongSlotRemoveReinsert",
            "missing_cartridge"                     : "cSupplyMissingOrNotSeated" if is_enterprise else "cMissingSupplies",
            "memory_error"                          : "cIndicatedSupplies" if is_enterprise else "cCartridgesNotCommunicating",
            "missing_elabel"                        : "cUnableToReadCartridge" if is_enterprise else "cMissingElabel",
            "unauthorized_cartridge"                : "cUnauthorizedCartridgeHelp" if is_enterprise else "cUnauthorizedAdminConfigured",
            "protected_cartridge"                   : "cCartridgeOnlyUsedInInitalProtectedProduct" if is_enterprise else "cCartridgeProtectionAntiTheft",
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

    # validate Supplies Alerts
    def goto_alert_message_layout_screen(self,timeout=15):
        """At Message layout screen
        """
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW,timeout=timeout), "Device not showing toast alert message."

    def check_alert_informative_icon_display(self):
        """Check Informative Icon
        """
        alertIcon = self._spice.query_item(self.ALERT_IMAGE_ICON)
        self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/InformativeFill.json")

    def check_alert_supply_icon_display(self):
        """
        Test to validate the Supplies Icon
        """
        supplyIcon = self._spice.query_item(self.ALERT_IMAGE_DETAILS_ICON)
        logging.info("Check Supplies Icon visibility")

        icon_display = supplyIcon["visible"]
        # Check Icon Visibility
        assert supplyIcon["visible"] is True, 'Supplies Icon not visible'
        logging.info(f"Verified icon visible is :{icon_display}")

    def check_alert_button(self, button_text):
        """
        Test to validate the Button Text
        """
        btn_display = self._spice.query_item(self.ALERT_BUTTON)["visible"]
        logging.info("Check button visible or not")
        assert self._spice.query_item(self.ALERT_BUTTON)["visible"] is True, 'Button not visible'
        logging.info(f"Verified {button_text} button visible is :{btn_display}")

        logging.info("Check button enable or not")
        btn_enable = self._spice.query_item(self.ALERT_BUTTON)["enabled"]
        assert self._spice.query_item(self.ALERT_BUTTON)["enabled"] is True, 'Button is disable'
        logging.info(f"Verified {button_text} button enable is :{btn_enable}")

        buttonText = self._spice.query_item(self.ALERT_BUTTON)["text"]
        logging.info("Check button Text")

        assert buttonText == button_text, "Button text incorrect"
        logging.info(f"Verified {button_text} Button Text: {buttonText}")

    def goto_statusapp(self,_spice):
        """
        Performs a mouse_click on status center dashboard
        to expand it when collapsed
        """
        statusCenter = self._spice.wait_for("NotificationCenterView")

        if statusCenter["state"] != "EXPANDED":
            statusCenterDash = self._spice.wait_for("NotificationCenterView #footer #footerRectangle")

            middle_width  = statusCenterDash["width"] / 2
            middle_height = statusCenterDash["height"] / 2

            statusCenterDash.mouse_click(middle_width, middle_height)
            time.sleep(3)

    def menu_navigation_statusapp(self, _spice):
        """
        Performs a mouse_click on status center dashboard
        to collapse it when expanded
        """
        statusCenter = self._spice.wait_for("NotificationCenterView")

        if statusCenter["state"] != "COLLAPSED":
            statusCenterDash = self._spice.wait_for("NotificationCenterView #footer #footerRectangle")
    
            # Scroll down to alert list.
            self._spice.mouse(operation=self._spice.MOUSE.WHEEL, wheel_y=-200)
            self._spice.query_item("#notificationRowAlertTitle", 0).mouse_click()
            time.sleep(3)

    def menu_navigation_statusapp_navigateBackToHome(self, _spice):
        """
        Navigates back to homescreen from the status app
        """

        BackToHome = _spice.query_item("#footer #footerRectangle")
        BackToHome.mouse_click()

    def check_alert_statusapp_title_text(self, title_text, object_id, index):
        """
        Test to validate the a Title Text of alert in statusapp screen
        """
        logging.info("Check Title text of statusapp screen")
        # wait for 2 sec to read Title .
        time.sleep(2)
        titleText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified statusapp Title text: %s ", titleText)
        assert titleText == title_text, 'incorrect Title text in status app'

    def check_alert_statusapp_detail_text(self, detail_text, object_id, index):
        """
        Test to validate the a Alert text of alert in statusapp screen
        """
        alertText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified statusapp actual detail text: %s" , alertText)
        logging.info("Verified statusapp expected detail text: %s" , detail_text)
        assert alertText == detail_text ,'incorrect Detail text in status app'

    def check_alert_icon_display(self):
        """Check Error Icon
        """
        alertIcon = self._spice.query_item(self.ALERT_IMAGE_ICON)
        self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/ErrorFill.json")

    def click_on_cartridges(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "0"
        middle_width = supplies_grid_tab_layout_app["width"] / 2
        height = supplies_grid_tab_layout_app["height"] / 4
        supplies_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def click_on_printheads(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "1"
        middle_width = supplies_grid_tab_layout_app["width"] / 2
        height = supplies_grid_tab_layout_app["height"] / 2
        supplies_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def close_supply_card_view(self):
        self._spice.query_item(self.CLOSE_SUPPLY_CARD_VIEW).mouse_click()
        time.sleep(3)
    
    def color_translator(self, cartridge_color_list, color, net, locale = "en-US"):
        '''
        Function that looks for a color in a list of expected colors regardless of language
        Parameters: expected color list and color
        out: color_id
        '''
        for color_id in cartridge_color_list:
            if color ==  LocalizationHelper.get_string_translation(net, color_id, locale):
                return color_id

    def color_converter(self, color_id):
        '''
        Simple color convertor
        Parameters: color identifier
        out: simplified standard color name
        '''
        converter = {
            "cColorBlack"         : "K",
            "cColorCyan"          : "C",
            "cColorMagenta"       : "M",
            "cColorYellow"        : "Y",
            "cLightCyan"          : "lc",
            "cLightMagenta"       : "lm",
            "cOptimizer"          : "OP",
            "cOvercoat"           : "OC",
            "cColorWhite"         : "W",
            "cTriColor"           : "CMY"
        }
        return converter[color_id]

    def goto_menu_supplies_summary(self):
        """
        Navigates to 'Cartridges' supply summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self._spice.wait_for("#Cartridges").mouse_click()

    def goto_menu_directCartridgesView(self):
        """
        Navigates to 'Cartridges' supply page
        """
        self.homemenu.goto_menu_directCartridgesView(self._spice)
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_supplies).mouse_click()
        
    def verify_direct_supplies_information(self,spice,catridgeCdmData,index,net):
        """
        Function to validate direct to supplies info
        """
        spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.directToCartridge_card + str(index))
        cartridgeInfo = spice.query_item( SuppliesAppWorkflowUICommonOperationsObjectsIds.directToCartridge_card +str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)
        self.validate_cartridge_details_with_cdm(catridgeCdmData, cartridgeInfo)

    def goto_menu_supplies_clicked(self,net):
        """
        Navigates to supplies summary page
        """
        cartridges = "#Cartridges"
        self.homemenu.goto_menu_supplies(self._spice)
        assert self._spice.wait_for(cartridges)
        current_string = self._spice.query_item("#Cartridges SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cInkCartridges")
        assert current_string == expected_string, "String mismatch"

    def goto_menu_supplies_clicked_LFP(self,net):
        """
        Navigates to supplies summary page
        """
        cartridges = "#Cartridges"
        self.homemenu.goto_menu_supplies(self._spice)
        assert self._spice.wait_for(cartridges)
        current_string = self._spice.query_item("#Cartridges SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cCartridges")
        assert current_string == expected_string, "String mismatch"

    def set_cartridge_very_low_behavior_ui (self, spice, object_id, cartridge, property_object_id):
        """
        Sets the cartridge 'Very Low Behavior' setting through UI
        """
        spice.query_item(object_id,cartridge).mouse_click()
        spice.wait_for(property_object_id).mouse_click()
        # Wait for 1 sec to reflect the change in CDM.
        time.sleep(1)

    def validate_cartridge_very_low_behavior_with_cdm(self, cdm, type, property):
        """
        Verifies the cartridge 'Very Low Behavior' setting changed through UI is reflected in CDM
        """
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        assert result[type +'VeryLowAction'] == property, type +" Cartridge - Very Low Behavior is not set to " + property

    def settings_supplies_verylowbehavior(self, spice, cdm, cartridge = 0):
        """
        Verifies the different black or color cartridge settings for 'Very Low Behavior'
        """
        object_id = (
            SuppliesAppWorkflowUICommonOperationsObjectsIds.black_very_low_action if cartridge == 0
            else SuppliesAppWorkflowUICommonOperationsObjectsIds.color_very_low_action)

        cartridge_type = "black" if cartridge == 0 else "color"

        # Check 'Stop' setting
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, SuppliesAppWorkflowUICommonOperationsObjectsIds.stop)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "stop")

        # Check 'Continue' setting
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, SuppliesAppWorkflowUICommonOperationsObjectsIds.continue_)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "continue")

        # Check 'Prompt to Continue' setting
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, SuppliesAppWorkflowUICommonOperationsObjectsIds.prompt)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "prompt")

        # Check 'Print Black' setting if cartridge is color
        if cartridge_type == "color":
            self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, SuppliesAppWorkflowUICommonOperationsObjectsIds.print_black)
            self.validate_cartridge_very_low_behavior_with_cdm(cdm, cartridge_type, "printBlack")

        # Return to default setting
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, SuppliesAppWorkflowUICommonOperationsObjectsIds.continue_)

    def settings_supplies_lowwarningthreshold_mono(self, spice, cdm):
        """
        Verifies black cartridge 'Low Warning Threshold' slider and absence of color sliders
        """
        # Color cartridges are slider[0-2] and black is always slider3
        # Try to access color sliders first, exception expected
        for index in range(3):
            color_found = False
            try:
                slider_bar = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_slidebar + str(index))
                color_found = True
            except:
                logging.info("Success: Color slider not found on Mono printer")
            assert color_found == False, "Error: Color slider found on Mono printer"

        # Test black slider
        slider_bar = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_slidebar + str(3))

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

    def get_alert_active_focus_index(self):
        index = 0
        for idx in [0,1,2,3]:
            try:
                active_index = self._spice.query_item("#AlertModelView", idx)['activeFocus']
                if active_index:
                    index = idx
                    break
            except:
                logging.info("Alert index not found")
        return index

    def get_alert_message(self):
        """
        Get the Title Text of the alert
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
        actual_title_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #titleObject".format(alert_window_name), index)["text"]
        return actual_title_text

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

        button_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #FooterView #FooterViewRight #ContentItem SpiceText".format(alert_window_name), index)["text"]
        return button_text

    def get_alert_message_details(self):
        """
        Test to validate the a Alert text of alert in status app screen
        """
        alert_window_name = ""
        actual_detail_text = ""
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
        try:
            actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #alertDetailDescription #contentItem".format(alert_window_name), index)["text"]
        except:
            actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #alertDetailDescription1 #contentItem".format(alert_window_name), index)["text"]
        return actual_detail_text

    def goto_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self._spice.home.workflow_common_operations.scroll_to_position_horizontal(0)
        self._spice.home.goto_home_supplies_app()
        self._spice.wait_for("#Cartridges", timeout=10).mouse_click()
    
    def check_alert_prompt_title_text(self, prompt_text, object_id, index=0):
        """
        Test to validate the Prompt Title Text
        """
        logging.info("Check Prompt Title text")
        self._spice.wait_for(object_id)
        promptText = self._spice.query_item(object_id,index)["text"]
        logging.info("Verified prompt again Title text: %s", promptText)
        assert promptText == prompt_text, 'incorrect prompt again title text'
    
    def check_very_low_prompt_again_screen(self):
        """
        Test to validate the Prompt Again mandatory button and Selecting the prompt option..
        """
        assert self._spice.wait_for("#NeverStop #RadioButtonText") ["visible"] is True, 'Icon not visible'
        assert self._spice.wait_for("#NeverStop #SpiceRadioButton") ["checked"] == True
        logging.info("Selecting the prompt option")
        self._spice.wait_for("#100PagesToStop #SpiceRadioButton").mouse_click()
    
    def check_very_low_alert_prompt_again_options(self):
        """
        Test to validate the Prompt buttons Text and button click.
        """
        prompt_options_list = ["#NeverStop #RadioButtonText","#100PagesToStop #SpiceRadioButton","#200PagesToStop #SpiceRadioButton","#300PagesToStop #SpiceRadioButton","#400PagesToStop #SpiceRadioButton"]
        for prompt_option in prompt_options_list:
            self._spice.wait_for(prompt_option)
            assert self._spice.wait_for(prompt_option)["visible"] is True, 'Icon not visible'
        assert self._spice.wait_for("#NeverStop #SpiceRadioButton") ["checked"] == True
        logging.info("Selecting the prompt option")
        self._spice.wait_for("#100PagesToStop #SpiceRadioButton").mouse_click()