import logging
import time
from random import randrange

from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperations import SuppliesAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration


class SuppliesAppWorkflowUISOperations(SuppliesAppWorkflowUICommonOperations):

    UI_SUPPLIES_APP = "#suppliesSummaryView"
    SUPPLIES_GRID_TAB_LAYOUT = "#suppliesSummaryView"
    SUPPLIES_REPLACEMENT_BUTTON = "#suppliesReplacementButton"
    CLOSE_SUPPLY_CARD_VIEW = "#closeButton"
    #Alert ObjectIds
    ALERT_DIALOG_WINDOW= "#bodyLayout"
    INDEX = 0
    ALERT_BUTTON = "AlertModel #FooterView #FooterViewRight #ContentItem SpiceText"
    ALERT_IMAGE_ICON = "#imageObject"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage"
    TRANSFER_KEY_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_ALERT_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_ALERT_DETAIL_ID_ENTERPRISE = "#alertDetailDescription1 #textColumn #contentItem"
    COMMON_TITLE_ID = "#titleObject"
    PROMPT_TITLE_ID = "#promptAgain #titleObject"
    PROMPT_TITLE_ID_COLOR = "#promptAgain #titleObject"
    COMMON_ALERT_DETAIL_IDX = 0
    COMMON_TITLE_SCREEN_ID = 0
    TRANSFER_KEY_DETAIL_IDX = 0
    COMMON_TITLE_IDX = 0
    REAR_DOOR_OPEN_TITLE_ID = "#doorOpen3Window #titleObject"
    REAR_DOOR_OPEN_DETAIL_ID = "#doorOpen3Window #alertDetailDescription #contentItem"
    JAM_CARTRIDGE_DOOR_TITLE_ID = "#jamAutoNavWindow #titleObject"
    JAM_CARTRIDGE_DOOR_DETAIL_ID = "#jamAutoNavWindow #alertDetailDescription #contentItem"
    CARTRIDGE_DOOR_OPEN_TITLE_ID = "#doorOpen2Window #titleObject"
    CARTRIDGE_DOOR_OPEN_DETAIL_ID = "#doorOpen2Window #alertDetailDescription #contentItem"
    TRAY1_OVERFILLED_TITLE_ID = "#trayOverfilled1Window #titleObject"
    TRAY1_OVERFILLED_DETAIL_ID = "#trayOverfilled1Window #alertDetailDescription #contentItem"
    TRAY2_OVERFILLED_TITLE_ID = "#trayOverfilled2Window #titleObject"
    TRAY2_OVERFILLED_DETAIL_ID = "#trayOverfilled2Window #alertDetailDescription #contentItem"
    TRAY3_OVERFILLED_TITLE_ID = "#trayOverfilled3Window #titleObject"
    TRAY3_OVERFILLED_DETAIL_ID = "#trayOverfilled3Window #alertDetailDescription #contentItem"
    COMMON_ALERT_TEXT_ID = "#titleObject"
    COMMON_ALERT_TEXT_IDX = 0
    COMMON_STATUS_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_STATUS_DETAIL_IDX = 0
    COMMON_STATUS_TITLE = "#notificationRowAlertTitle #alertStatusCenterText" 
    COMMON_STATUS_TITLE_IDX = 0
    ALERT_BTN =  "#Hide"
    ALERT_BUTTON_ENTERPRISE = "#SuppliesFlowModuleAlert #FooterView #FooterViewRight #ContentItem SpiceText"
    ALERT_IMAGE_ENTERPRISE = "#gridLayout #gridLayoutView #gridLayout #imageContainer"


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
            "cartridge_very_low_stop"               : "cReplaceVeryLowCartridge" if is_enterprise else "cCartridgesVeryLow",
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
            "protected_cartridge"                   : "cProtectedCartridgeInstall" if is_enterprise else "cHPProtectedCartridgesInstalled",
            "non_hp_chip"                           : "cNonHPChipDetected",
            "alienation_detection"                  : "cAlignmentErrorTitle",
            "long_life_consumable_low"              : "cTransferKitReplaceSoon",
            "long_life_consumable_very_low"         : "cTransferKitReplaceNow",
            "cartridge_very_low_prompt_title"       : "cPromptAgain",  # This is for the prompt that appears after choosing a VL continue option
            "cartridge_very_low_continue_title"     : "cContinueOptions",  # This is for the prompt that appears after acknowledging the VL prompt
            "micr_cartridge_low"                    : "cReplaceMICRCartridge",
            "non_micr_cartridge"                    : "cInstallMICRCartridge",
            "missing_micr_cartridge"                : "cInstallMICRCartridge",
            "cartridge_beyond_very_low_continue"    : "cBeyondVeryLow",
            "cartridge_beyond_very_low_prompt"      : "cBeyondVeryLow",
            "cartridge_beyond_very_low_warning"     : "cBeyondVeryLow"
            }

        self.SUPPLIES_ALERT_CONTENT_CSTRINGS = {
            "cartridge_low"                         : "cIndicatedCartridgesLowReplacementsRecycle" if is_enterprise else "cIndicatedCartridgesLow",
            "cartridge_low_stop"                    : "cSupplyIndicatesLowStop",
            "cartridge_very_low_continue"           : "cVeryLowIndicatedCartridge" if is_enterprise else "cCartridgesVeryLowContinue",  # Enterprise should also have cActualSupplyLife cConsiderHavingReplacementVeryLow cSupplyDoesNotNeedReplacePQ, followed by recommended cartridges info
            "cartridge_very_low_print_black"        : "cPrinterConfiguredPrintBlackShort",  # Not defined in Enterprise SMS yet
            "cartridge_very_low_prompt"             : "cVeryLowIndicatedCartridge" if is_enterprise else "cCartridgesVeryLowPrompt",  # Enterprise has additional strings too
            "cartridge_very_low_stop"               : "cVeryLowIndicatedCartridge" if is_enterprise else "cCartridgesConfiguredStopVeryLow",  # Enterprise has additional strings too
            "genuine_hp_cartridge"                  : "cOriginalHPCartridgesInstalled",
            "non_hp_cartridge"                      : "cDetectedNoGuaranteeChip",
            "reman_cartridge"                       : "cNonHPRemanufacturedCartridgesInstalled",  # Not defined in Enterprise SMS yet
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails",
            "used_cartridge"                        : "cIndicatedCartridgeUsedCounterfeit" if is_enterprise else "cIndicatedCartridgesUsed",
            "used_or_refilled"                      : "cCartridgesRefilledDepleted" if is_enterprise else "cCartridgesRefilledRemanufactured",
            "incompatible_cartridge"                : "cIndicatedSupportedCartridge" if is_enterprise else "cIndicatedIncompatibleCartridges",
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
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails",
            "cartridge_beyond_very_low_continue"    : "cCartridgesVeryLowPrompt",
            "cartridge_beyond_very_low_prompt"      : "cCartridgesPromptVeryLow",
            "cartridge_beyond_very_low_warning"     : "cCartridgesVeryLowContinue"
            }

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

    def click_on_other_supplies(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "2"
        middle_width = supplies_grid_tab_layout_app["width"] / 2
        height = supplies_grid_tab_layout_app["height"] * 3/4
        supplies_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def click_on_tcu(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "1"
        middle_width = supplies_grid_tab_layout_app["width"] / 2
        height = supplies_grid_tab_layout_app["height"] / 2
        supplies_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def click_replace_button(self):
        supplies_replace_button = self._spice.wait_for(self.SUPPLIES_REPLACEMENT_BUTTON) 
        supplies_replace_button.mouse_click()

    def close_supply_card_view(self):
        self._spice.query_item(self.CLOSE_SUPPLY_CARD_VIEW).mouse_click()
        time.sleep(3)

    def goto_menu_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self.click_on_cartridges()

    def goto_menu_supplies_tcu_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self.click_on_tcu()

    def verify_supplies_transferkit_reset(self, spice, udw):
        #navigate to service reset screen
        self.homemenu.goto_menu_tools_servicemenu_serviceresets(spice,udw)
        time.sleep(2)
        logging.info(" at Transfer Kit Reset Screen")
        self.homemenu.menu_navigation(spice, "#serviceResetsMenuList", "#imageTransferKitResetMenuButton")
        time.sleep(2)

    def verify_supplies_transferkit_reset_OK(self, spice, udw):
        #Transferkit reset
        resetButton = spice.query_item("#TransferResetButton")
        resetButton.mouse_click()
        time.sleep(2)

    def verify_supplies_transferkit_reset_Cancel(self, spice, udw):
        #tansferkit cancel
        cancelButton = spice.query_item("#CancelButton")
        cancelButton.mouse_click()
        time.sleep(2)


    def set_cartridge_very_low_behavior_ui (self, spice, object_id, cartridge, property_object_id):
        """
        Configures Cartridge very low behavior property through UI.
        """
        spice.query_item(object_id,cartridge).mouse_click()
        spice.wait_for(property_object_id).mouse_click()
        # wait for 1 sec to reflect the change in cdm.
        time.sleep(1)

    def validate_cartridge_very_low_behavior_with_cdm(self, cdm, type, property):
        """
        Verifies the Cartridge very low behavior property set through UI from CDM
        """
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        assert result[type +'VeryLowAction'] == property, type +" Cartridge - Very Low Behavior is not set to " + property

    def settings_supplies_verylowbehavior(self, spice, cdm, cartridge = 0):
        """
        Verifies different Black and Color cartridge properties for very low behavior.
        """

        object_id = MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_black
        cartridge_type = "black"
        if cartridge == 1:
            object_id = MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_color
            cartridge_type = "color"

        # Check stop property
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_stop)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm,cartridge_type, "stop")
        
        # Check continue property
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_continue)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm,cartridge_type, "continue")
        
        # Check prompt property
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_prompt)
        self.validate_cartridge_very_low_behavior_with_cdm(cdm,cartridge_type, "prompt")
        
        # check printBlack property if it is color cartridge
        if cartridge == 1:
            self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_printblack)
            self.validate_cartridge_very_low_behavior_with_cdm(cdm,cartridge_type, "printBlack")

        # Return to default setting
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_continue)

        # Verify back button
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, "#SettingsSpiceComboBoxpopupverticalLayout " + MenuAppWorkflowObjectIds.button_back)

    def settings_supplies_lowwarningthreshold(self, spice, cdm):
        """
        Verifies low warning threshold sliding bars.
        """
        set_value = randrange(10,50) 
        for index in range(4): 
            slider_bar = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_slidebar + str(index))
            current_value = slider_bar["value"]
            logging.info("Current Value on Slider: "+ str(current_value))
            slider_bar.__setitem__('value', set_value)
            slider_bar = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_slidebar + str(index))
            current_value = slider_bar["value"]
            assert current_value == set_value

        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        for index in range(4):
            assert set_value == result["lowThresholdsPerSupply"][index]["threshold"], "Low value Threshold for UI and CDM are not same"

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

    def set_supplies_uiitem_validate_with_cdm (self,spice, cdm, view_id, object_id, key, value):
        """
        Clicks on given supplies UI item and validates it with cdm.
        """
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        logging.info("Supplies values in cdm Before Clicking the UI item" + key)
        logging.info(result)
        ## menu_navigation is not working for few menu items such as cartridge protection, Authorized HP
        ## cartridge policy (DUNE-77021). Using wait_for() to click on the object.
        #self.homemenu.menu_navigation(spice, view_id, object_id, scrollbar_objectname = view_id + "ScrollBar")
        spice.wait_for(object_id).mouse_click()
        #Wait for 2 secs to update value in the cdm.
        time.sleep(2)
        logging.info("Supplies values in cdm After clicking the UI item" + key)
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        logging.info(result)
        assert result[key] == value, "UI and CMD value doesn't match for "+ key

    def settings_supplies_authorizedhpcartridgepolicy(self, spice, cdm):
        """
        Verifies supplies Authorized HP cartridge policy is disabled/enabled.
        """
        
        ## Added Manual scroll to make Authorized HP Cartridge policy visible as menu_navigation scroll
        ## is not working (DUNE-77021)
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies+"ScrollBar")
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        values = ["genuineHp","any"]
        if result["supplyPolicy"] == "genuineHp":
            values.reverse()
        
        # Validate Authorized HP Cartridge policy switch button
        for value in values:
            self.set_supplies_uiitem_validate_with_cdm (spice, 
                                                 cdm, 
                                                 MenuAppWorkflowObjectIds.view_settings_supplies,
                                                 MenuAppWorkflowObjectIds.menu_button_settings_supplies_supplypolicy,
                                                 "supplyPolicy", 
                                                 value)


    def settings_supplies_storesupplyusagedata(self, spice, cdm):
        """
        Verifies supplies Store Supply Usage Data is disabled/enabled.
        """

        values = ["true","false"]
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        if result["storeUsageDataEnabled"] == "true":
            values.reverse()
        
        # Validate Store supply Usage switch button
        for value in values:
            self.set_supplies_uiitem_validate_with_cdm (spice, 
                                                 cdm, 
                                                 MenuAppWorkflowObjectIds.view_settings_supplies,
                                                 MenuAppWorkflowObjectIds.menu_button_settings_supplies_storedatausage,
                                                 "storeUsageDataEnabled", 
                                                 value)
       
    def settings_supplies_cartridgeprotection(self, spice, cdm):
        """
        Verifies cartridge protection is disabled/enabled.
        """
        values = ["true","false"]
        result = cdm.get_raw(cdm.SUPPLIES_CONFIG_PUBLIC).json()
        if result["antiTheftEnabled"] == "true":
            values.reverse()
       # Validate Cartridge protection switch button
        for value in values:
            self.set_supplies_uiitem_validate_with_cdm (spice, 
                                                 cdm, 
                                                 MenuAppWorkflowObjectIds.view_settings_supplies_cartridgeprotection,
                                                 MenuAppWorkflowObjectIds.menu_button_settings_supplies_cartridgeprotection,
                                                 "antiTheftEnabled", 
                                                 value)

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

    def check_alert_icon_display(self):
        """Check Error Icon
        """
        alertIcon = self._spice.query_item(self.ALERT_IMAGE_ICON)
        self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/ErrorFill.json")

    def check_alert_supply_icon_display_enterprise(self):
        """
        Test to validate the Supplies Icon
        """
        supplyIcon = self._spice.query_item(self.ALERT_IMAGE_ENTERPRISE)
        logging.info("Check Supplies Icon visibility")
       
        icon_display = supplyIcon["visible"]
        # Check Icon Visibility
        assert supplyIcon["visible"] is True, 'Supplies Icon not visible'
        logging.info(f"Verified icon visible is :{icon_display}")
        
    def check_warning_icon_display(self):
        alertIcon = self._spice.query_item(self.ALERT_IMAGE_ICON)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/WarningFill.json")

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

    def _get_alert_window_and_index(self):
        """Helper method to get alert window name and index
        
        Returns:
            tuple: (alert_window_name, index) where alert_window_name is the name of the 
                  active alert window (or empty string if not found), and index is the 
                  active focus index (or 0 if not found)
        """
        alert_window_name = ""
        index = 0
        logging.info("Collecting the active alert window name or index of active alert")
        
        # Try to find the active window name from the supplies_spice_window list
        for spice_alert in self.supplies_spice_window:
            try:
                if self._spice.query_item("#{0}".format(spice_alert))['activeFocus']:
                    alert_window_name = "#{0} ".format(spice_alert)
                    logging.info("Active alert window name: {0}".format(alert_window_name))
                    break
            except:
                pass
        
        # If window name not found, try to get the active focus index
        if alert_window_name == "":
            index = self.get_alert_active_focus_index()
            
        return alert_window_name, index
        
    def get_alert_message(self):
        """Get the Title Text of the alert
        
        Returns:
            str: The title text of the active alert, or empty string if not found
        """
        alert_window_name, index = self._get_alert_window_and_index()
        
        try:
            actual_title_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #titleObject".format(alert_window_name), index)["text"]
        except:
            logging.info("Could not get alert title text")
            actual_title_text = ""
        return actual_title_text

    def get_alert_button_text(self):
        """Get the Alert button text
        
        Returns:
            str: The text of the alert button
        
        Raises:
            Exception: If button text can't be retrieved
        """
        alert_window_name, index = self._get_alert_window_and_index()

        button_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #FooterView #FooterViewRight #ContentItem SpiceText".format(alert_window_name), index)["text"]
        return button_text

    def get_alert_message_details(self):
        """Get the detail text of the alert
        
        Returns:
            str: The detail text of the active alert, or empty string if not found
        """
        alert_window_name, index = self._get_alert_window_and_index()
        actual_detail_text = ""
        try:
            actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #alertDetailDescription #contentItem".format(alert_window_name), index)["text"]
        except:
            try:
                actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #alertDetailDescription1 #contentItem".format(alert_window_name), index)["text"]
            except:
                actual_detail_text = ""
        return actual_detail_text

    def get_alert_message_event_code(self):
        """Get the Event code of the alert in status app screen
        
        Returns:
            str: The event code text of the active alert
        """
        alert_window_name, index = self._get_alert_window_and_index()
        event_code_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #statusBox #StatusText".format(alert_window_name), index)["text"]
        logging.info("Event code is: %s", event_code_text) 
        return event_code_text

    def check_alert_prompt_title_text(self, prompt_text, object_id, index=0):
        """
        Test to validate the Prompt Title Text
        """
        logging.info("Check Prompt Title text")
        self._spice.wait_for(object_id)
        promptText = self._spice.query_item(object_id,index)["text"]
        logging.info("Verified prompt again Title text: %s", promptText)
        assert promptText == prompt_text, 'incorrect prompt again title text'

    def check_alert_continue_option_title_text(self,continue_text):
        """
        Test to validate the Continue Option Title Text
        """
        logging.info("Check Continue Option Title text")
        self._spice.wait_for("#continueOptions #titleObject")
        assert self._spice.wait_for("#continueOptions #titleObject")["text"] ==  continue_text, 'Title text incorrect'
        logging.info("Verified Title text: %s ", continue_text)

    def check_alert_continue_options_and_select_print_color_option(self):
        """
        Test to validate the Continue Option buttons and Selecting the print in color option.
        """
        assert self._spice.wait_for("#permissionPrintBlack")["visible"] is True, 'Button not visible'
        assert self._spice.wait_for("#permissionPrintColor")["visible"] is True, 'Button not visible'
        logging.info("Selecting the print in color option")
        self._spice.wait_for("#permissionPrintColor").mouse_click()

    def check_alert_continue_options_and_select_print_black_option(self):
        """
        Test to validate the Continue Option buttons and Selecting the print in black option.
        """
        assert self._spice.wait_for("#permissionPrintBlack")["visible"] is True, 'Button not visible'
        assert self._spice.wait_for("#permissionPrintColor")["visible"] is True, 'Button not visible'
        logging.info("Selecting the print in color option")
        self._spice.wait_for("#permissionPrintBlack").mouse_click()

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

    def check_transfer_kit_alert_detail_text(self,detail_text):
        """
        Test to validate the Alert text
        """
        assert self._spice.query_item(self.ALERT_DETAIL)["text"] == detail_text ,'Detail text incorrect'

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

    def check_alert_button_enterprise(self, button_text):
        """
        Test to validate the Button Text
        """
        btn_display = self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE)["visible"]
        logging.info("Check button visible or not")
        assert self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE)["visible"] is True, 'Button not visible'
        logging.info(f"Verified {button_text} button visible is :{btn_display}")

        logging.info("Check button enable or not")
        btn_enable = self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE)["enabled"]
        assert self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE)["enabled"] is True, 'Button is disable'
        logging.info(f"Verified {button_text} button enable is :{btn_enable}")

        buttonText = self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE)["text"]
        logging.info("Check button Text")

        assert buttonText == button_text, "Button text incorrect"
        logging.info(f"Verified {button_text} Button Text: {buttonText}")

        logging.info(f"Press the button")
        alert_button = self._spice.query_item(self.ALERT_BUTTON_ENTERPRISE) 
        self._spice.wait_for(self.ALERT_BUTTON_ENTERPRISE)
        alert_button.mouse_click()

    def goto_menu_supplies_othersupplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        time.sleep(4)
        self.click_on_other_supplies()

    def verify_supplies_summary_information(self,spice,catridgeCdmData,index,net):
        """
        Function to validate supplies summary info
        """
        subTitleText = spice.query_item("#cartridgeTabHeader #subtitleObject")
        loc_subTitleText = LocalizationHelper.get_string_translation(net, "cEstimatedLevelsPlural", 'en-US')
        assert subTitleText['text'].find(loc_subTitleText) != -1, "subTitleText Text mismatch"

        spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index))
        cartridgeInfo = spice.query_item( SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card +str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)
        self.validate_cartridge_details_with_cdm(catridgeCdmData, cartridgeInfo)

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
            middle_width  = statusCenterDash["width"] / 2
            middle_height = statusCenterDash["height"] / 2
            status_app = _spice.query_item("#notificationRowChevron")
            status_app.mouse_click()
            statusCenterDash.mouse_click(middle_width, middle_height)
            time.sleep(3)

    def menu_navigation_statusapp_navigateBackToHome(self, _spice):
        """
        Navigates back to homescreen from the status app
        """
        BackToHome = _spice.query_item("#footer #footerRectangle")
        BackToHome.mouse_click()

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

    def goto_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self._spice.home.workflow_common_operations.scroll_to_position_horizontal(0)
        self._spice.home.goto_home_supplies_app()
        self._spice.wait_for("#Cartridges", timeout=10).mouse_click()
