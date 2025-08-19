
import logging
import time
from random import randrange

from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperations import SuppliesAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds


class SuppliesAppWorkflowUILOperations(SuppliesAppWorkflowUICommonOperations):
    
    UI_SUPPLIES_APP = "#suppliesSummaryView"
    SUPPLIES_GRID_TAB_LAYOUT = "#suppliesSummaryView"
    SUPPLIES_REPLACEMENT_BUTTON = "#suppliesReplacementButton"
    CLOSE_SUPPLY_CARD_VIEW = "#closeButton"
    #Alert ObjectIds
    ALERT_DIALOG_WINDOW= "#bodyLayout"
    ALERT_BUTTON = "#AlertModelView #FooterView #FooterViewRight #ContentItem SpiceText"
    ALERT_IMAGE_ICON = "#imageObject"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage"
    COMMON_ALERT_DETAIL_ID = "#alertDetailDescription #contentItem"
    TRANSFER_KEY_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_TITLE_ID = "#titleObject"
    COMMON_ALERT_DETAIL_IDX = 0
    TRANSFER_KEY_DETAIL_IDX = 0
    COMMON_TITLE_IDX = 0
    COMMON_ALERT_TEXT_ID = "#titleObject"
    COMMON_ALERT_TEXT_IDX = 0
    COMMON_STATUS_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_ALERT_DETAIL_ID_ENTERPRISE = "#alertDetailDescription1 #textColumn #contentItem"
    COMMON_STATUS_DETAIL_IDX = 0
    COMMON_STATUS_TITLE = "#notificationRowAlertTitle #alertStatusCenterText" 
    COMMON_STATUS_TITLE_IDX = 0
    ALERT_BTN = "#Hide"
    ALERT_BUTTON_ENTERPRISE = "#SuppliesFlowModuleAlert #FooterView #FooterViewRight #ContentItem SpiceText"
    PROMPT_TITLE_ID = "#promptAgain #titleObject"    
    ALERT_IMAGE_ENTERPRISE = "#gridLayout #gridLayoutView #gridLayout #imageContainer"    

    SUPPLIES_ALERT_TITLE_CSTRINGS = {
        "protected_cartridge"                   : "cHPProtectedCartridges",
        "unauthorized_cartridge"                : "cUnauthorizedCartridgesInstalled",
        "non_hp_cartridge"                      : "cAlteredClonedCartridgesInstalled",
        "cartridge_very_low_continue"           : "cCartridgesVeryLow",
        "cartridge_very_low_print_black"        : "cCartridgesVeryLow",
        "cartridge_very_low_prompt"             : "cCartridgesVeryLow",
        "cartridge_very_low_stop"               : "cCartridgesVeryLow",
        "genuine_hp_cartridge"                  : "cHPCartridgesInstalled"
        }

    SUPPLIES_ALERT_CONTENT_CSTRINGS = {
        "cartridge_wrong_slot"                  : "cWrongSlotRemoveReinsert",
        "missing_elabel"                        : "cCartridgesUsedRefilled",
        "genuine_hp_cartridge"                  : "cOriginalHPCartridgesInstalled",
        "non_hp_cartridge"                      : "cDetectedNoGuaranteeChip",
        "used_cartridge"                        : "cIndicatedCartridgesUsed",
        "missing_cartridge"                     : "cMissingCartridgesShort",
        "memory_error"                          : "cCartridgesNotCommunicating",
        "unauthorized_cartridge"                : "cUnauthorizedAdminConfigured",
        "protected_cartridge"                   : "cCartridgeProtectionAntiTheft",
        "incompatible_cartridge"                : "cIndicatedIncompatibleCartridges",
        "long_life_consumable_very_low"         : "cScheduleTransferKitReplaceNow",
        "long_life_consumable_low"              : "cScheduleTransferKitReplaceSoon",
        "cartridge_low"                         : "cIndicatedCartridgesLow",
        "cartridge_very_low_continue"           : "cVeryLowIndicatedCartridge",
        "cartridge_very_low_stop"               : "cCartridgesConfiguredStopVeryLow",
        "cartridge_very_low_printing_black"     : "cCartridgeVeryLowPrintingBlack",
        "cartridge_refilled_remanufactured"     : "cCartridgeRefilledRemanufactured",
        "non_hp_chip"                           : "cDSFailedNonHPChip",
        "printer_failure"                       : "cPrinterFailureLarge",
        "cartridge_very_low_prompt"             : "cCartridgesVeryLowPrompt"
        }

    supplies_spice_window = ["genuineHPSupplyFlowWindow",
                            "nonHPSupplyFlowWindow",
                            "usedSupplyPromptWindow",
                            "blackSupplyVeryLowFlowWindow",
                            "colorSupplyVeryLowFlowWindow",
                            "longLifeConsumableLowWindow",
                            "longLifeConsumableVeryLowWindow",
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
                            ]

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def click_on_cartridges(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "0"
        supplies_grid_tab_layout_app.mouse_click()
        time.sleep(3)

    def click_on_printheads(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "1"
        supplies_grid_tab_layout_app.mouse_click()
        time.sleep(3)
        
    def click_replace_button(self):
        self._spice.wait_for(self.SUPPLIES_REPLACEMENT_BUTTON)
        supplies_replace_button = self._spice.query_item(self.SUPPLIES_REPLACEMENT_BUTTON) 
        time.sleep(10)
        supplies_replace_button.mouse_click()
        
    def close_supply_card_view(self):
        close_button = self._spice.query_item(self.CLOSE_SUPPLY_CARD_VIEW)
        close_button.mouse_click()
        time.sleep(3)

    # Vertical Scrolling Cartridges window
    def _scroll_to_position_vertical(self, spice, position, scrollbar_objectname="#cartridgesCardsViewScrollverticalScroll") -> None:
        '''
        Scrolls to the provided position
        Parameters: position to scroll
        spice: the spice object
        position: between 0-1
        '''
        assert (position >= 0 and position <= 1.1), "Wrong value. Postion can only be between 0 and 1"
        scrollbar = spice.query_item(scrollbar_objectname)
        scrollbar.__setitem__("position", str(position))

    # Vertical Scrolling printHeads window
    def _scroll_to_position_vertical_printheads(self, spice, position, scrollbar_objectname="#printheadsCardsViewScrollverticalScroll") -> None:
        '''
        Scrolls to the provided position
        Parameters: position to scroll
        spice: the spice object
        position: between 0-1
        '''
        assert (position >= 0 and position <= 1.1), "Wrong value. Postion can only be between 0 and 1"
        scrollbar = spice.query_item(scrollbar_objectname)
        scrollbar.__setitem__("position", str(position))

    # Get color and status from all cartridges in Cartridge window
    def get_all_cartridges_status_from_card_views(self, spice, n_cartridges, scroll_step=0.1):
        '''
        Scrolls down on every iteration
        You must be in Supplies view screen
        Parameters: printer cartridge number, ie: Jupiter 4
        out: dictionary {index:status}
        spice: the spice object
        '''
        position = scroll_step
        spice_supplies = {}
        for index in range(n_cartridges):
            base_str = "#cartridgeCardView_"
            cartridge_number = str(index)
            # Get the cartridge object
            cartridge = spice.query_item(base_str+cartridge_number)
            spice.common_operations.click_button_on_middle(cartridge)
            time.sleep(3)
            # Get supply state
            obj_state = spice.wait_for("#rowBlockC #statusBoxBlockC SpiceText[visible=true]")
            state = obj_state["text"]
            spice_supplies[index] = spice.suppliesapp.status_converter(state)
            # Close cartridge card view
            self._scroll_to_position_vertical(spice,position)
            spice.suppliesapp.close_supply_card_view()
            position += scroll_step
        return spice_supplies

    # Get status from all printHeads in printHead window
    def get_all_printheads_status(self, spice, n_printheads, selected_space = "main", scroll_step = 0.0 ):
        '''
        You must be in printHeads view screen
        Scrolls down on every iteration (if needed)
        Parameters: printer printhead count, ie: Jupiter 8
        Parameters: data origin window (main/not main=right panel)
        out: dictionary {index:status}, index starts on 0
        spice: the spice object
        '''
        position = scroll_step
        spice_supplies = {}
        base_str = "#printheadCardView_"
        if selected_space == "main":
            base_str = "#printheadCard_"
        for index in range(n_printheads):
            printhead_number = str(index)
            # Get the printhead object
            printhead = spice.query_item(base_str+printhead_number)
            if selected_space == "main":
                printhead.mouse_click()
            else:
                spice.common_operations.click_button_on_middle(printhead) 
            time.sleep(2)
            # Get supply state
            obj_state = spice.wait_for("#rowBlockC #statusBoxBlockC SpiceText[visible=true]")
            state = obj_state["text"]
            spice_supplies[index] = self.status_converter(state)
            # Close printHead card view
            spice.suppliesapp.close_supply_card_view()
            self._scroll_to_position_vertical_printheads(spice,position)
            position += scroll_step
        return spice_supplies

    def click_on_tcu(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "1"
        middle_width = supplies_grid_tab_layout_app["width"] / 2
        height = supplies_grid_tab_layout_app["height"] / 2
        supplies_grid_tab_layout_app.mouse_click(middle_width, height)
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

        # set to default
        self.set_cartridge_very_low_behavior_ui (spice, object_id, cartridge, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_continue)

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
        viewObject = spice.wait_for(object_id)

        # Wait for clickable situation
        spice.wait_until(lambda: viewObject["enabled"] == True, 15)
        spice.wait_until(lambda: viewObject["visible"] == True, 15)

        # Click on the middle of the object
        middle_width = viewObject["width"] / 2
        middle_height = viewObject["height"] / 2
        viewObject.mouse_click(middle_width, middle_height)

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
        scrollbar.__setitem__("position",0.1)
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

    def check_warning_icon_display(self):
        alertIcon = self._spice.query_item(self.ALERT_IMAGE_ICON)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/WarningFill.json")

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

        logging.info(f"Press the button")
        alert_button = self._spice.query_item(self.ALERT_BUTTON) 
        self._spice.wait_for(self.ALERT_BUTTON)
        alert_button.mouse_click()

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
    
    def verify_supplies_summary_information(self,spice,catridgeCdmData,index,net):
        """
        Function to validate supplies summary info
        """
        spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index))
        cartridgeInfo = spice.query_item( SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card +str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)
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

    def check_alert_prompt_title_text(self, prompt_text, object_id, index=0):
        """
        Test to validate the Prompt Title Text
        """
        logging.info("Check Prompt Title text")
        self._spice.wait_for(object_id)
        promptText = self._spice.query_item(object_id,index)["text"]
        logging.info("Verified prompt again Title text: %s", promptText)
        assert promptText == prompt_text, 'incorrect prompt again title text'

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
        try:
            actual_title_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #titleObject".format(alert_window_name), index)["text"]
        except:
            actual_title_text = ""
        return actual_title_text

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
            try:
                actual_detail_text = self._spice.query_item("{0}#SuppliesFlowModuleAlert #alertDetailDescription1 #contentItem".format(alert_window_name), index)["text"]
            except:
                actual_detail_text = ""
        return actual_detail_text

