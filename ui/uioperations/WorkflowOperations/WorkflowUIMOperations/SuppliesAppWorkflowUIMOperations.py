import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperations import SuppliesAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration

class SuppliesAppWorkflowUIMOperations(SuppliesAppWorkflowUICommonOperations):
    
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
            "missing_micr_cartridge"                : "cInstallMICRCartridge"
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
            "reman_used_cartridge"                  : "cUsedCartridgesInstalledDetails"
            }

    def get_alert_active_focus_index(self):
        index = 0
        for idx in [0,1,2,3]:
            try:
                active_index = self._spice.query_item(MenuAppWorkflowObjectIds.alert_view, idx)['activeFocus']
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

    def get_alert_message_details(self):
        """Get the detail text of the alert

        Returns:
            str: The detail text of the active alert, or empty string if not found
        """
        alert_window_name, index = self._get_alert_window_and_index()
        actual_detail_text = ""
        try:
            actual_detail_text = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_detail_description), index)["text"]
        except:
            try:
                actual_detail_text = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_detail_description1), index)["text"]
            except:
                actual_detail_text = ""
        return actual_detail_text
    
    # validate Supplies Alerts                                            
    def goto_alert_message_layout_screen(self,timeout=35):
        """At Message layout screen
        """
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.alert_dialog_window,timeout=timeout), "Device not showing toast alert message."

    def check_alert_informative_icon_display(self):
        """Check Informative Icon
        """
        alertIcon = self._spice.query_item(MenuAppWorkflowObjectIds.alert_image_icon)
        self._spice.wait_for(MenuAppWorkflowObjectIds.alert_image_icon)
        assert alertIcon["visible"] is True, 'Icon not visible'
        assert str(alertIcon["source"]) == str("qrc:/images/Status/InformativeFill.json")
    
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

    def check_alert_prompt_title_text(self, title_text, object_id, index = 0):
        """
        Test to validate the Alert Prompt Title Text
        """
        logging.info("Check Alert Prompt Title text")
        # wait for 2 sec to read Title .
        time.sleep(2)
        titleText = self._spice.query_item(object_id, index)["text"]
        logging.info("Verified alert prompt Title text: %s ", titleText)
        assert titleText == title_text, 'incorrect Alert Prompt Title text'

    def get_alert_message(self):
        """Get the Title Text of the alert

        Returns:
            str: The title text of the active alert, or empty string if not found
        """
        alert_window_name, index = self._get_alert_window_and_index()

        try:
            actual_title_text = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_title_object), index)["text"]
        except:
            logging.info("Could not get alert title text")
            actual_title_text = ""
        return actual_title_text

    def get_alert_message_event_code(self):
        """Get the Event code of the alert in status app screen

        Returns:
            str: The event code text of the active alert
        """
        alert_window_name, index = self._get_alert_window_and_index()
        event_code_text = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_status_box), index)["text"]
        logging.info("Event code is: %s", event_code_text)
        return event_code_text


    def check_alert_icon_display(self):
        """
        Test to validate the Alert Icon display
        """
        alertIcon = self._spice.query_item(MenuAppWorkflowObjectIds.alert_image_icon)
        self._spice.wait_for(MenuAppWorkflowObjectIds.alert_image_icon)
        assert alertIcon["visible"] is True, 'Alert Icon not visible'
        logging.info("Verified alert icon is visible")

    def check_alert_supply_icon_display(self):
        """
        Test to validate the Supplies Icon
        """
        supplyIcon = self._spice.query_item(MenuAppWorkflowObjectIds.alert_image_icon)
        logging.info("Check Supplies Icon visibility")
       
        icon_display = supplyIcon["visible"]
        # Check Icon Visibility
        assert supplyIcon["visible"] is True, 'Supplies Icon not visible'
        logging.info(f"Verified icon visible is :{icon_display}")

    def check_alert_supply_icon_display_enterprise(self):
        """
        Test to validate the Supplies Icon for Enterprise
        """
        supplyIcon = self._spice.query_item(MenuAppWorkflowObjectIds.enterprise_supply_icon)
        logging.info("Check Supplies Icon visibility for Enterprise")
       
        icon_display = supplyIcon["visible"]
        # Check Icon Visibility
        assert supplyIcon["visible"] is True, 'Supplies Icon not visible'
        logging.info(f"Verified icon visible is :{icon_display}")

    def check_alert_statusapp_detail_text(self, detail_text, object_id, index):
        """
        Test to validate the Alert detail text in statusapp screen
        """
        alert_window_name, active_index = self._get_alert_window_and_index()
        try:
            alertText = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_detail_description), active_index)["text"]
        except:
            try:
                alertText = self._spice.query_item("{0}{1} {2}".format(alert_window_name, MenuAppWorkflowObjectIds.supplies_flow_module_alert, MenuAppWorkflowObjectIds.alert_detail_description1), active_index)["text"]
            except:
                # Fallback to the original method if window-based approach fails
                alertText = self._spice.query_item(object_id, index)["text"]
        
        logging.info("Verified statusapp actual detail text: %s" , alertText)
        logging.info("Verified statusapp expected detail text: %s" , detail_text)
        assert alertText == detail_text ,'incorrect Detail text in status app'

    def check_alert_button(self, button_text):
        self.check_alert_button_enterprise(button_text)

    def check_alert_button_enterprise(self, button_text):
        """
        Test to validate the Button Text for Enterprise
        """
        btn_display = self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise)["visible"]
        logging.info("Check button visible or not")
        assert self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise)["visible"] is True, 'Button not visible'
        logging.info(f"Verified {button_text} button visible is :{btn_display}")

        logging.info("Check button enable or not")
        btn_enable = self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise)["enabled"]
        assert self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise)["enabled"] is True, 'Button is disable'
        logging.info(f"Verified {button_text} button enable is :{btn_enable}")

        buttonText = self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise)["text"]
        logging.info("Check button Text")

        assert buttonText == button_text, "Button text incorrect"
        logging.info(f"Verified {button_text} Button Text: {buttonText}")

        logging.info(f"Press the button")
        alert_button = self._spice.query_item(MenuAppWorkflowObjectIds.alert_button_enterprise) 
        self._spice.wait_for(MenuAppWorkflowObjectIds.alert_button_enterprise)
        alert_button.mouse_click()