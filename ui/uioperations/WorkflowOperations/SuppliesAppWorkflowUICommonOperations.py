import time
import logging
from dunetuf.cdm import CDM
from datetime import datetime
from dunetuf.utility.retry import Retry
from dunetuf.network.net import Network
import dunetuf.metadata as product_metadata
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.BaseOperations.ISuppliesAppUIOperations import ISuppliesAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds


"""CDM - UI Supplies state mapping."""
supplies_state = [
    "ok",
    "inform",
    "warning",
    "error",
]

class SuppliesAppWorkflowUICommonOperations(ISuppliesAppUIOperations):
    
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

    SUPPLIES_ALERT_TITLE_CSTRINGS = {
        "cartridge_low"                         : "cCartridgesLow",
        "genuine_hp_cartridge"                  : "cHPCartridgesInstalled",
        "non_hp_cartridge"                      : "cAlteredClonedCartridgesInstalled",
        "reman_cartridge"                       : "cNonHPRemanufacturedInstalled",
        "used_cartridge"                        : "cUsedOrCounterfeitCartridgesInstalled",
        "reman_used_cartridge"                  : "cUsedCartridgesInstalled",
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
        "missing_micr_cartridge"                : "cInstallMICRCartridge"
        }

    SUPPLIES_ALERT_CONTENT_CSTRINGS = {
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
        "missing_micr_cartridge"                : "cNotMICRCartridge"
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
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        self.maxtimeout = 120
        self.homemenu = self._spice.menu_operations

    def validate_cartridge_details_with_cdm(self, catridgeCdmData, cartridgeInfo):
        """
        Function to validate cartridge details with cdm data
        """
        if( "percentLifeRemaining" in catridgeCdmData):
            assert catridgeCdmData["publicInformation"]["percentLifeDisplay"] == cartridgeInfo["supplyLevel"]
        else:
            print("percentLifeRemaining not exist in" + catridgeCdmData)
        if( "supplyState" in catridgeCdmData["publicInformation"]):
            assert catridgeCdmData["publicInformation"]["supplyState"] == supplies_state[cartridgeInfo["userReportedSeverity"]]
        else:
            print("supplyState not exist in " +catridgeCdmData)

    def verify_cartridge_details_screen_information(self,spice,catridgeCdmData,net): 
        """
        Function to validate cartridge detail page info
        """
        if self._spice.cdm.device_feature_cdm.is_color_supported():
            cartridge = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(0), timeout=10)
            middle_width = round(cartridge["width"] / 2)
            height = round(cartridge["height"] / 2)
            cartridge.mouse_click(middle_width,height)
            time.sleep(3)
            #get cartridge details
            cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info)
        else:
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(0), timeout=10)
            cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(0)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)

        if self._spice.cdm.device_feature_cdm.is_color_supported():
            headerText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
            loc_headerText = LocalizationHelper.get_string_translation(net, "cSupplyCapitalColorEnumerationBlack", 'en-US')
            assert headerText.find(loc_headerText) != -1, "Header Text mismatch"        
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)
            statusText = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
            assert statusText.find("OK") != -1, "Status Text mismatch"
        else:
            spice.wait_for('#rowBlockC #StatusIcon') # Supply color card view is for color printers
            statusText = spice.wait_for('#rowBlockC SpiceText[visible=true]')['text']       

        # Test installed Value
        installedName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed, 0)
        loc_installedName = LocalizationHelper.get_string_translation(net, "cInstalled", 'en-US')
        assert installedName['text'].find(loc_installedName) != -1, "installedName Text mismatch"

        installedValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_value, 0)
       
        cdmInstalledValue = catridgeCdmData["publicInformation"]["selectabilityNumber"]
        #cdm comparasion
        assert installedValue['text'].find(cdmInstalledValue) != -1, "installedValue Text mismatch"
        
        if self._spice.cdm.device_feature_cdm.is_color_supported():
            spice.suppliesapp.close_supply_card_view()
       

    def verify_tcu_details_screen_information(self,spice,net, status): 
        """
        Function to validate tcu page info
        """
        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text)["text"]
        loc_statusText = LocalizationHelper.get_string_translation(net, status, 'en-US')
        assert statusText.find(loc_statusText) != -1, "Status Text mismatch"
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon_1)
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_image_container)

    def set_black_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : SuppliesAppWorkflowUICommonOperationsObjectsIds.stop, "Continue" : SuppliesAppWorkflowUICommonOperationsObjectsIds.continue_, "Prompt to Continue" : SuppliesAppWorkflowUICommonOperationsObjectsIds.prompt}
        spice.wait_for(elementDict[setting]).mouse_click()

    def set_color_very_low_behavior_ui(self, spice, setting):
        elementDict = {"Stop" : SuppliesAppWorkflowUICommonOperationsObjectsIds.stop, "Continue" : SuppliesAppWorkflowUICommonOperationsObjectsIds.continue_, "Print Black" : SuppliesAppWorkflowUICommonOperationsObjectsIds.print_black, "Prompt to Continue" : SuppliesAppWorkflowUICommonOperationsObjectsIds.prompt}
        spice.wait_for(elementDict[setting]).mouse_click()

    def get_black_very_low_behavior_ui(self, spice):
        very_low_behavior = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.black_very_low_action)["text"]
        try: 
            spice.wait_for("#closeButton").mouse_click()
        except:
            pass
        return very_low_behavior

    def get_color_very_low_behavior_ui(self, spice):
        very_low_behavior = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.color_very_low_action)["text"]
        try: 
            spice.wait_for("#closeButton").mouse_click()
        except:
            pass
        return very_low_behavior

    # This method handle only supplies related alert acknowledgment
    def press_alert_button(self, button_id):
        self._spice.wait_for("#AlertFooter")
        button = self._spice.wait_for(button_id)
        self._spice.validate_button(button)
        button.mouse_click()

    # Horizontal scrolling 
    def _scroll_to_position_horizontal(self, spice, position: int, scroll_bar_id = "#horizontalScroll") -> None:
        '''
        Scrolls to the provided position
        Parameters: position to scroll
        spice: the spice object
        position: between 0-1
        '''
        assert (position >= 0 and position <= 1), "Wrong value. Postion can only be between 0 and 1"

        scrollbar = spice.query_item(scroll_bar_id)
        scrollbar.__setitem__("position", str(position))

    # Get color and status from all cartridges
    def get_all_cartridges_color_and_status(self, spice, n_cartridges, expected_color_list, net, cdm, scroll_step=0.06):
        '''
        You must be in Cartridges view screen
        Scrolls left on every iteration
        Parameters: printer cartridge number, ie: sunspot 9
        out: dictionary {color:status}
        spice: the spice object
        '''
        locale = cdm.device_language.get_device_language()
        position = scroll_step
        spice_supplies = {}
        for index in range(n_cartridges):
            base_str = SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card
            cartridge_number = str(index)
            # Get the cartridge object
            cartridge = spice.wait_for(base_str+cartridge_number)
            middle_width = round(cartridge["width"] / 2)
            middle_height = round(cartridge["height"] / 2)
            cartridge.mouse_click(middle_width, middle_height)
            # Get supply color 
            color = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
            # Get supply state
            obj_state = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.obj_state)
            state = obj_state["text"]
            color_id = self.color_translator(expected_color_list, color, net, locale)
            simplified = self.color_converter(color_id)
            spice_supplies[simplified] = self.status_converter(state)
            # Close cartridge card view
            spice.suppliesapp.close_supply_card_view()
            self._scroll_to_position_horizontal(spice,position, SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_scroll_bar)
            position += scroll_step
        return spice_supplies
    
    def get_all_printheads_status(self, spice, n_printheads, scroll_step = 0.05):
        '''
        You must be in printHeads view screen
        Scrolls left on every iteration (if needed)
        Parameters: printer printhead number, ie: sunspot 5
        out: dictionary {color:status}
        spice: the spice object
        '''
        position = scroll_step
        spice_supplies = {}
        for index in range(n_printheads):
            base_str = SuppliesAppWorkflowUICommonOperationsObjectsIds.printhead_card
            printhead_number = str(index)
            # Get the printhead object
            printhead = spice.wait_for(base_str+printhead_number)
            middle_width = round(printhead["width"] / 2)
            middle_height = round(printhead["height"] / 2)
            printhead.mouse_click(middle_width, middle_height)
            # Get supply state
            obj_state = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.obj_state)
            state = obj_state["text"]
            spice_supplies[index] = self.status_converter(state)
            # Close printHead card view
            spice.suppliesapp.close_supply_card_view()
            self._scroll_to_position_horizontal(spice,position, SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_scroll_bar)
            position += scroll_step
        return spice_supplies
    

    def get_printhead_status(self, spice):
        '''
        You must be in printHeads view screen
        Scrolls left on every iteration (if needed)
        Parameters: printer printhead number, ie: sunspot 5
        out: dictionary {color:status}
        spice: the spice object
        '''
        spice_supplies = {}
        base_str = SuppliesAppWorkflowUICommonOperationsObjectsIds.printhead_card
        printhead_number = "0"
        # Get the printhead object
        printhead = spice.wait_for(base_str+printhead_number)
        middle_width = round(printhead["width"] / 2)
        middle_height = round(printhead["height"] / 2)
        printhead.mouse_click(middle_width, middle_height)
        # Get supply state
        obj_state = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.obj_state)
        state = obj_state["text"]
        spice_supplies[0] = self.status_converter(state)
        return spice_supplies
    
    def color_translator(self, expected_color_list, color, net, locale = "en-US"):
        '''
        Function that looks for a color in a list of expected colors regardless of language
        Parameters: expected color list and color
        out: color_id
        '''
        for color_id in expected_color_list:
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

    def get_color_name_from_color_code(self, color_code):
        """
        Function to convert color code to string representation
        :param color_code: Color code (e.g. "K", "C", "M", "Y")
        :return: String representation of the color
        """
        supplyType = {
        "C": "Cyan",
        "M": "Magenta",
        "Y": "Yellow",
        "K": "Black"
        }
        return supplyType.get(color_code, "")

    # Converter between different status nomenclature
    def status_converter(self,status):
        '''
        Simple status translator
        Parameters: status
        out: status 
        '''
        
        converter={
            "Ready" : "ok",
            "OK" : "ok",
            "expiredWarning": "warning",
            "expiredWarrantyWarning": "warning",
            "Printheads Missing": "warning",
            "Printhead Replacement Incomplete": "error"
        }
        if status in converter:
            return converter[status]
        else:
            return status

    def get_cartridge_gas_gauge_details(self, spice, index, is_color_printer=True):
        gas_gauge_details = {}
        if is_color_printer:
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index), timeout=10)
            cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)

            logging.debug("Click cartridge gas gauge card, index :: {0}".format(index))
            cartridge = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index))
            middle_width = round(cartridge["width"] / 2)
            height = round(cartridge["height"] / 2)
            cartridge.mouse_click(middle_width, height)
        else:
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(index), timeout=10)
            cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)

        try:
            spice.get_screenshot(file_name="ui_supply_status_"+str(index)+".png")
        except:
            pass

        try:
            gas_gauge_details["supplylevel"] = cartridgeInfo["supplyLevel"]
        except:
            pass
        try:
            gas_gauge_details["supplystate"] = supplies_state[cartridgeInfo["userReportedSeverity"]]
        except:
            pass
        try:
            gas_gauge_details["selectability_number"] = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_value)['text']
        except:
            pass
        try:
            gas_gauge_details["supplylevelstate"] = spice.wait_for('#rowBlockC SpiceText[visible=true]')['text']
        except:
            pass

        logging.debug("Close cartridge gas gauge card after collecting :: {0}".format(gas_gauge_details))
        if is_color_printer:
            spice.suppliesapp.close_supply_card_view()
        return gas_gauge_details

    def verify_inkCartridge_details_screen_information(self,spice,catridgeCdmData,net): 
        """
        Function to validate cartridge detail page info
        """
        cartridge = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(0))
        middle_width = round(cartridge["width"] / 2)
        height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width,height)
        time.sleep(3)
        #get cartridge details
        cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info)
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)

        headerText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
        loc_headerText = LocalizationHelper.get_string_translation(net, "cSupplyCapitalColorEnumerationBlack", 'en-US')
        assert headerText.find(loc_headerText) != -1, "Header Text mismatch"

        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
        assert statusText.find("OK") != -1, "Status Text mismatch"
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)

        # Test installed 
        installedName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed, 0)
        loc_installedName = LocalizationHelper.get_string_translation(net, "cInstalled", 'en-US')
        assert installedName['text'].find(loc_installedName) != -1, "installedName Text mismatch"

        installedValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_value, 0)
       
        cdmInstalledValue = catridgeCdmData["publicInformation"]["selectabilityNumber"]
        #cdm comparasion
        assert installedValue['text'].find(cdmInstalledValue) != -1, "installed Value  mismatch"  

        # Test installed Date
        installedDate = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_date, 0)
        loc_installedDate = LocalizationHelper.get_string_translation(net, "cInstallationDate", 'en-US')
        assert installedDate['text'].find(loc_installedDate) != -1, "installed Date Text mismatch"

        installedDateValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_date_value, 0)
       
        cdmInstalledDateValue = catridgeCdmData["publicInformation"]["firstInstallDate"]
        #cdm comparasion
        #assert installedDateValue['text'].find(cdmInstalledDateValue) != -1, "installed Date Value mismatch"  

        # Test Manufacturer
        manufacturer = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.manufacturer, 0)
        loc_manufacturer = LocalizationHelper.get_string_translation(net, "cManufacturer", 'en-US')
        assert manufacturer['text'].find(loc_manufacturer) != -1, "Manufacturer Text mismatch"

        manufacturerValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.manufacturer_value, 0)
       
        cdmManufacturerValue= catridgeCdmData["publicInformation"]["brand"]
        #cdm comparasion
        assert manufacturerValue['text'].find(cdmManufacturerValue) != -1, "Manufacturer Value mismatch"  

        # Test Product Name
        #As per defect DUNE-129963 commenting out as product name not applicable for beam
        '''productName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_name, 0)
        loc_productName = LocalizationHelper.get_string_translation(net, "cProductName", 'en-US')
        assert productName['text'].find(loc_productName) != -1, "Product Name Text mismatch"
        productNameValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_name_value, 0)
        cdmProductNameValue = catridgeCdmData["publicInformation"]["orderPartNumber"]
        #cdm comparasion
        assert productNameValue['text'].find(cdmProductNameValue) != -1, "Product Name Value mismatch" '''     

        # Test Product Number
        productNumber = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_number, 0)
        loc_productNumber = LocalizationHelper.get_string_translation(net, "cProductNumber", 'en-US')
        assert productNumber['text'].find(loc_productNumber) != -1, "Product Number Text mismatch"
        productNumberValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_number_value, 0)
        cdmProductNumberValue = catridgeCdmData["publicInformation"]["productNumber"]

        #cdm comparison
        assert productNumberValue['text'].find(cdmProductNumberValue) != -1, "Product Number Value mismatch" 

        # Test Serial Number
        serialNumber = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.serial_number, 0)
        loc_serialNumber = LocalizationHelper.get_string_translation(net, "cSerialNumber", 'en-US')
        assert serialNumber['text'].find(loc_serialNumber) != -1, "Serial Number Text mismatch"

        serialNumberValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.serial_number_value, 0)
       
        cdmSerialNumberValue = catridgeCdmData["publicInformation"]["serialNumber"]
        #cdm comparasion
        assert serialNumberValue['text'].find(cdmSerialNumberValue) != -1, "Serial Number Value mismatch"   

         # Test Supported Cartridges
        supportedCartridges = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supported_cartridges, 0)
        loc_supportedCartridges = LocalizationHelper.get_string_translation(net, "cSupportedCartridges", 'en-US')
        assert supportedCartridges['text'].find(loc_supportedCartridges) != -1, "Supported Cartridges Text mismatch"

        supportedCartridgesValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supported_cartridges_value, 0)
       
        #cdmSupportedCartridgesValue = catridgeCdmData["publicInformation"]["serialNumber"]
        #cdm comparasion
        #assert supportedCartridgesValue['text'].find(cdmSupportedCartridgesValue) != -1, "Supported Cartridges Value mismatch"    
                
        spice.suppliesapp.close_supply_card_view()

    def verify_maintenance_cartridge_details_screen_information(self,spice,net,maintenanceCatridgeCdmData,status): 
        """
        Function to validate maintenance cartridge page info
        """
        #check maintenance cartridge details
        maintenanceCartridge = spice.query_item("#textImageBlock1")
        maintenanceCartridge.mouse_click()
        try:
            #check if replace button is available
            spice.wait_for("#cardExpanded #otherSuppliesFooter #replaceButton")
            statusText = spice.wait_for("#statusBoxBlockC #StatusText")["text"]
            loc_statusText = LocalizationHelper.get_string_translation(net, status,'en-US')
            assert statusText.find(loc_statusText) != -1, "Status Text mismatch"
            spice.wait_for("#statusBoxBlockC  #StatusIcon")

            #Test remaining capacity Text                
            remainingCapacityText = spice.wait_for("#mcCardExpandedRemainingCapacity #NameText")["text"]                      
            loc_remainingCapacityText = LocalizationHelper.get_string_translation(net, "cRemainingCapacity", 'en-US')            
            assert remainingCapacityText.find(loc_remainingCapacityText) != -1, "Remaining capacity Text mismatch"
            #Test remaining capacity Value
            remainingCapacityValue = spice.wait_for("#mcCardExpandedRemainingCapacity #ValueText")
            
            # cdm implementation not ready ,commenting out TBD
            #cdmremainingCapacityValue = maintenanceCatridgeCdmData["publicInformation"]["percentLifeDisplay"]
            #remainingValue = remainingCapacityValue['text'].find(str(cdmremainingCapacityValue))
            #assert int(remainingValue) != -1, "Remaining Capacity value mismatch"  
                             

        finally:
            spice.suppliesapp.close_supply_card_view()

    def verify_status_center_alert_title_and_description(self,spice,loc_title,loc_alert):
        spice.statusCenter_dashboard_expand()
        logging.debug("Verify the status center alert title and description ")
        # Scroll down to alert list.
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        status_title = spice.query_item("#notificationRowAlertTitle #alertStatusCenterText")['text']
        assert loc_title == status_title, "Failed to verify status center alert title"

    def click_status_center_alert_screen(self,spice):
        # Scroll down to alert list.
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        spice.mouse(operation=spice.MOUSE.WHEEL, wheel_y=-100)
        spice.query_item("#notificationRowAlertTitle", 0).mouse_click()

    def verify_ui_cartridge_details(self, cartridge_number, cdm_cartridge_info, position):
        """
        Function to validate UI cartridge details against CDM
        """
        # Click on desired cartridge
        self._scroll_to_position_horizontal(self._spice, position, SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_scroll_bar)
        cartridge = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(cartridge_number))
        middle_width = round(cartridge["width"] / 2)
        middle_height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width, middle_height)
        
        # Get UI cartridge details
        estimated_level_value = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.estimated_level_value)
        manufacturer_value = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.manufacturer_value)
        product_name_value = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_name_value)
        product_number_value = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_number_value)
        serial_number_value = self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.serial_number_value)
        
        # Check UI cartridge details against CDM cartridge info
        assert estimated_level_value["text"] == str(cdm_cartridge_info["percentLifeRemaining"]) + "%*"
        assert manufacturer_value["text"] == cdm_cartridge_info["publicInformation"]["brand"]
        assert product_name_value["text"] == cdm_cartridge_info["publicInformation"]["orderPartNumber"]
        assert product_number_value["text"] == cdm_cartridge_info["publicInformation"]["productNumber"]
        assert serial_number_value["text"] == cdm_cartridge_info["publicInformation"]["serialNumber"]


    def verify_cartridge_status(self, spice, catridgeCdmData, net, status):
        """
        Function to validate cartridge detail page info
        """
        if self._spice.cdm.device_feature_cdm.is_color_supported():
            cartridge = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(0), timeout=10)
            middle_width = round(cartridge["width"] / 2)
            height = round(cartridge["height"] / 2)
            cartridge.mouse_click(middle_width,height)
            # Get cartridge details
            cartridgeInfo = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info)
        else:
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(0), timeout=10)
            cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.mono_cartridge_card + str(0)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)

        self.validate_cartridge_details_with_cdm(catridgeCdmData, cartridgeInfo)
        # Verify cartridge Status
        if self._spice.cdm.device_feature_cdm.is_color_supported():
            spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)
            statusText = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
        else:
            spice.wait_for('#rowBlockC #StatusIcon')
            statusText = spice.wait_for('#rowBlockC SpiceText[visible=true]')['text']
        loc_statusText = LocalizationHelper.get_string_translation(net, status,'en-US')
        assert statusText.find(loc_statusText) != -1, "Status Text mismatch"
        if self._spice.cdm.device_feature_cdm.is_color_supported(): # Supply color card view is for color printers
            self._spice.suppliesapp.close_supply_card_view()

    def verify_directToCartridge_status(self,spice,catridgeCdmData,net,status): 
        """
        Function to validate cartridge detail page info
        """
        cartridge = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.directToCartridge_card + str(0))
        middle_width = round(cartridge["width"] / 2)
        height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width,height)
        time.sleep(3)
        #get cartridge details
        cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info)
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)
        #verify cartridge Status
        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
        loc_statusText = LocalizationHelper.get_string_translation(net, status,'en-US')
        assert statusText.find(loc_statusText) != -1, "Status Text mismatch"
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)
        
        spice.suppliesapp.close_supply_card_view()


    def verify_suppliesWidget_homeScreen(self,spice):
        """
        Function to validate supplies home screen widget
        """
        spice.wait_for("#spiceCartridgesWidget")
        spice.wait_for("#spiceCartridgesWidget #cartridgesCardsList #cartridgeCard_0", timeout = 15.0)
        suppliesWidget = spice.query_item("#HomeScreenView HomeScreenWidgetDock SpiceGridLayout SpiceCard #spiceCartridgesWidget ")
        widgetScrollCont = spice.query_item("#HomeScreenView HomeScreenWidgetDock")
        #move/scroll to supplies widget
        widgetScrollCont["contentX"] = suppliesWidget["x"]
        
        assert spice.check_item("#cartridgeText SpiceText[visible=true]") != None,"cartridgeText is not visible on widget"
        assert spice.check_item("#estimatedLevels SpiceText[visible=true]") != None ,"estimated levels is not visible on widget"
        assert spice.query_item("#cartridgesCardsList")["visible"] == True,"cartridges List is not visible on widget"
        assert spice.query_item("#cartridgesCardsList #cartridgeCard_0")["visible"] == True,"cartridges List is not visible on widget"
        assert spice.query_item("#progressBarCartridgesWidget")["visible"] == False ,"progressBar is visible on widget"
        #click on any cartridge need call code for this
        cartridge = spice.query_item("#cartridgeCard_0")
        middle_width = round(cartridge["width"] / 2)
        height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width,height)

        #check it navigates to supplies app need to call code for this
        assert spice.wait_for("#StatusInfoTemplate")
        widgetScrollCont["contentX"] = 0
        
        # Close cartridge card view
        spice.wait_for("#closeButton").mouse_click()

    def validate_supplies_app(self,spice,cdm,configuration, net):
        logging.info("Validating supplies app screen")
        product_metadata_dict = product_metadata.get_product_metadata(cdm, configuration)
        # print all keys and their values in dictionary
        ConsumableSupport = product_metadata_dict.get('ConsumableSupport', [])
        transfer_kit_supported = 'TransferKit' in ConsumableSupport
        if transfer_kit_supported == True:
            assert spice.wait_for("#Cartridges SpiceText")["visible"] == True,"Cartridges is not visible"
            assert spice.wait_for("#Cartridges SpiceText")["text"] == "Cartridges"
            assert spice.wait_for("#otherSupply SpiceText")["visible"] == True, "Transfer Kit is not visible"
            if spice.uisize == "S" or spice.uisize == "XS":
                assert spice.wait_for("#otherSupply SpiceText")["text"] == str(LocalizationHelper.get_string_translation(net,"cOtherSupplies", "en"))
            else:
                assert spice.wait_for("#otherSupply SpiceText")["text"] == "Transfer Kit"
        else:
            assert spice.wait_for("#Cartridges SpiceText")["visible"] == True,"Cartridges is not visible"
            assert spice.wait_for("#Cartridges SpiceText")["text"] == str(LocalizationHelper.get_string_translation(net,"cCartridges", "en"))

    # Get color code from all cartridges
    def get_all_cartridges_color_and_order(self, spice, n_cartridges, cartridge_color_list, net, cdm,scroll_step=0.05, directToCartridge=False):
        
        locale = cdm.device_language.get_device_language()
        spice_supplies = {}
        for index in range(n_cartridges):
            if (directToCartridge):
                print("directToCartridge")
                base_str = SuppliesAppWorkflowUICommonOperationsObjectsIds.directToCartridge_card
            else:
                print("not directToCartridge")
                base_str = SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card
            cartridge_number = str(index)
            # Get the cartridge object
            cartridge = spice.wait_for(base_str+cartridge_number)
            middle_width = round(cartridge["width"] / 2)
            middle_height = round(cartridge["height"] / 2)
            cartridge.mouse_click(middle_width, middle_height)
            # Get supply color 
            color = spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
            color_id = self.color_translator(cartridge_color_list, color, net, locale)
            simplified = self.color_converter(color_id)
            spice_supplies[simplified]= simplified
            # Close cartridge card view
            spice.suppliesapp.close_supply_card_view()
        return spice_supplies 

    def verify_inkCartridge_details_screen_information_lfp(self,spice,catridgeCdmData,net): 
        """
        Function to validate cartridge detail page info
        """
        cartridge = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(0))
        middle_width = round(cartridge["width"] / 2)
        height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width,height)
        time.sleep(3)
        #get cartridge details
        cartridgeInfo = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info)
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)

        headerText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
        loc_headerText = LocalizationHelper.get_string_translation(net, "cSupplyCapitalColorEnumerationBlack", 'en-US')
        assert headerText.find(loc_headerText) != -1, "Header Text mismatch"

        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
        assert statusText.find("OK") != -1, "Status Text mismatch"
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)

        # Test installed 
        installedName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed, 0)
        loc_installedName = LocalizationHelper.get_string_translation(net, "cInstalled", 'en-US')
        assert installedName['text'].find(loc_installedName) != -1, "installedName Text mismatch"

        installedValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_value, 0)
       
        cdmInstalledValue = catridgeCdmData["publicInformation"]["selectabilityNumber"]
        #cdm comparasion
        assert installedValue['text'].find(cdmInstalledValue) != -1, "installed Value  mismatch"  

        # Test Manufacturer
        manufacturer = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.manufacturer, 0)
        loc_manufacturer = LocalizationHelper.get_string_translation(net, "cManufacturer", 'en-US')
        assert manufacturer['text'].find(loc_manufacturer) != -1, "Manufacturer Text mismatch"

        manufacturerValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.manufacturer_value, 0)
       
        cdmManufacturerValue= catridgeCdmData["publicInformation"]["brand"]
        #cdm comparasion
        assert manufacturerValue['text'].find(cdmManufacturerValue) != -1, "Manufacturer Value mismatch"  

        # Test Product Name
        productName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_name, 0)
        loc_productName = LocalizationHelper.get_string_translation(net, "cProductName", 'en-US')
        assert productName['text'].find(loc_productName) != -1, "Product Name Text mismatch"
        productNameValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_name_value, 0)
        cdmProductNameValue = catridgeCdmData["publicInformation"]["orderPartNumber"]
        #cdm comparasion
        assert productNameValue['text'].find(cdmProductNameValue) != -1, "Product Name Value mismatch"      

        # Test Product Number
        productNumber = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_number, 0)
        loc_productNumber = LocalizationHelper.get_string_translation(net, "cProductNumber", 'en-US')
        assert productNumber['text'].find(loc_productNumber) != -1, "Product Number Text mismatch"
        productNumberValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.product_number_value, 0)
        cdmProductNumberValue = catridgeCdmData["publicInformation"]["productNumber"]

        #cdm comparison
        assert productNumberValue['text'].find(cdmProductNumberValue) != -1, "Product Number Value mismatch" 

        # Test Serial Number
        serialNumber = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.serial_number, 0)
        loc_serialNumber = LocalizationHelper.get_string_translation(net, "cSerialNumber", 'en-US')
        assert serialNumber['text'].find(loc_serialNumber) != -1, "Serial Number Text mismatch"

        serialNumberValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.serial_number_value, 0)
       
        cdmSerialNumberValue = catridgeCdmData["publicInformation"]["serialNumber"]
        #cdm comparasion
        assert serialNumberValue['text'].find(cdmSerialNumberValue) != -1, "Serial Number Value mismatch"

        #Implemented batch ID for sunspot as per DUNE-93030
        BatchID = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.Batch_ID, 0)
        loc_BatchID = LocalizationHelper.get_string_translation(net, "cBatchID", 'en-US')
        assert BatchID['text'].find(loc_BatchID) != -1, "Batch ID Text mismatch"

        batchIDValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.Batch_ID_value, 0)
       
        cdmbatchIDValue = catridgeCdmData["publicInformation"]["batchId"]
        #cdm comparasion
        assert batchIDValue['text'].find(cdmbatchIDValue) != -1, "Batch ID Value mismatch"

        #Validating statuscode only with UI values
        statuscode = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds. status_code, 0)
        loc_statuscode = LocalizationHelper.get_string_translation(net, "cStatusCode", 'en-US')
        assert statuscode['text'].find(loc_statuscode) != -1, "status Code Text mismatch"

        status_code_Value = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds. status_code_Value, 0)
        # comparing UI values
        assert status_code_Value['text'] != -1, "Status code  Value mismatch"

        #Validating warranty only with UI values
        warranty = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds. warranty, 0)
        loc_warranty = LocalizationHelper.get_string_translation(net, "cWarranty", 'en-US')
        assert warranty['text'].find(loc_warranty) != -1, "warranty Text mismatch"

        warranty_Value = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds. warranty_Value, 0)
        
        # comparing UI values
        assert warranty_Value['text'] != -1, "warranty Value mismatch"

        #Validating Expiration date only with UI values
        ExpirationDate = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.Expiration_Date, 0)
        loc_ExpirationDate = LocalizationHelper.get_string_translation(net, "cExpirationDate", 'en-US')
        assert ExpirationDate['text'].find(loc_ExpirationDate) != -1, "ExpirationDate Text mismatch"

        ExpirationDate_Value = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds. Expiration_Date_Value, 0)
        
        # comparing UI values
        assert ExpirationDate_Value['text'] != -1, "ExpirationDate Value mismatch"

        # Test Supported Cartridges
        supportedCartridges = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supported_cartridges, 0)
        loc_supportedCartridges = LocalizationHelper.get_string_translation(net, "cSupportedCartridges", 'en-US')
        assert supportedCartridges['text'].find(loc_supportedCartridges) != -1, "Supported Cartridges Text mismatch"

        # Retrieve CDM values
        cdmSupportedCartridgesValue1 = catridgeCdmData["publicInformation"]["supportedParts"][0]["selectabilityNumber"]
        cdmSupportedCartridgesValue2 = catridgeCdmData["publicInformation"]["supportedParts"][1]["selectabilityNumber"]

        # Get the displayed values from the UI
        supportedCartridgesValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supported_cartridges_value, 0)
        uiValues = supportedCartridgesValue['text'].split(", ")

        # Compare CDM values with UI values
        assert cdmSupportedCartridgesValue1 in uiValues, "Supported Cartridges Value 1 mismatch"
        assert cdmSupportedCartridgesValue2 in uiValues, "Supported Cartridges Value 2 mismatch"
    
        spice.suppliesapp.close_supply_card_view()

    def ui_shows_validating_state(self):
        try:
            return self._spice.wait_for("#progressBarDetail", timeout=30)["text"] == LocalizationHelper.get_string_translation(Network(self._spice.ipaddress), "cValidatingPleaseWait")
        except:
            self._spice.get_screenshot(file_name="supply_validation_status.png")
            cdm = CDM(self._spice.ipaddress)
            logging.exception("AFTER Wait for validating - handling exception.\nalerts:\n{}".format(cdm.get(cdm.ALERTS)['alerts']))
            return False

    def verify_supplies_summary_information_mono(self, spice, cartridgeCdmData, net):
        """
        Validate black supply, ensure color supplies do not appear
        """
        # Verify we are at the 'Cartridges' supply summary
        headerText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_summary_cartridges_header)["text"]
        expectedHeaderText = LocalizationHelper.get_string_translation(net, "cCartridges")
        assert headerText == expectedHeaderText, "Header text mismatch"

        # Validate black cartridge
        cartridgeInfo = spice.query_item("#cartridgeCardView_0 #spiceCartridge")
        assert cartridgeInfo["color"] == cartridgeCdmData["publicInformation"]["supplyColorCode"], "UI and CDM supply color codes don't match"
        self.validate_cartridge_details_with_cdm(cartridgeCdmData, cartridgeInfo)

        # Try to query color cartridge cards, exceptions expected
        colorFound = False
        for index in range(1,4):
            try:
                spice.query_item("#cartridgeCardView_" + str(index))
                colorFound = True
            except:
                logging.info("Success: Color cartridge not found on Mono printer")
            
            assert colorFound == False, "Error: Color cartridge found on Mono printer"

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

    def check_alert_message(self, expected_title_text):
        """
        Test to validate the Title Text
        """
        # Wait for the expected title text to appear
        logging.info("Expected Title text: %s", expected_title_text)
        assert expected_title_text == Retry.until_equal(self.get_alert_message, expected_title_text)

    def check_alert_message_details(self, expected_detail_text):
        """
        Test to validate the a Alert text of alert in status app screen
        """
        # Wait for the expected detail text to appear
        logging.info("Expected Detail text: %s", expected_detail_text)
        assert expected_detail_text == Retry.until_equal(self.get_alert_message_details, expected_detail_text)
    
    def verify_tonerCartridge_details_screen_information(self,spice,catridgeCdmData,protectedCdmData,net): 
        """
        Function to validate cartridge detail page info
        """
        cartridge = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(0))
        middle_width = round(cartridge["width"] / 2)
        height = round(cartridge["height"] / 2)
        cartridge.mouse_click(middle_width,height)
        #get cartridge details
        cartridgeInfo = spice.wait_for((SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_info), timeout=10)
        self.validate_cartridge_details_with_cdm(catridgeCdmData,cartridgeInfo)

        headerText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.header_text_cartridge)["text"]
        loc_headerText = LocalizationHelper.get_string_translation(net, "cSupplyCapitalColorEnumerationBlack", 'en-US')
        assert headerText.find(loc_headerText) != -1, "Header Text mismatch"

        statusText = spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_text_cartridge)["text"]
        assert statusText.find("OK") != -1, "Status Text mismatch"
        spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.status_icon)

        # Test installed 
        installedName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed, 0)
        loc_installedName = LocalizationHelper.get_string_translation(net, "cInstalled", 'en-US')
        assert installedName['text'].find(loc_installedName) != -1, "installedName Text mismatch"

        installedValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.installed_value, 0)
       
        cdmInstalledValue = catridgeCdmData["publicInformation"]["productNumber"]
        #cdm comparasion
        assert installedValue['text'].find(cdmInstalledValue) != -1, "installed Value  mismatch"  

        # Test orderPart 
        orderHPpartName = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.orderHPpart, 0)
        loc_orderHPpartName = LocalizationHelper.get_string_translation(net, "cOrderHpPart", 'en-US')
        assert orderHPpartName['text'].find(loc_orderHPpartName) != -1, "orderHPpartName Text mismatch"

        orderHPpartValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.orderHPpart_value, 0)
       
        cdmOrderHPpartValue = catridgeCdmData["publicInformation"]["orderPartNumber"]
        #cdm comparasion
        assert orderHPpartValue['text'].find(cdmOrderHPpartValue) != -1, "orderHPpart Value  mismatch"  

        # # Test Approximate Pages Remaining
        approximatePagesRemain = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.approximatePagesRemain, 0)
        loc_approximatePagesRemain = LocalizationHelper.get_string_translation(net, "cApproximatePagesRemaining", 'en-US')
        assert approximatePagesRemain['text'].find(loc_approximatePagesRemain) != -1, "approximatePagesRemainName Text mismatch"

        approximatePagesRemainValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.approximatePagesRemain_value, 0)
       
        cdmApproximatePagesRemainValue = str(catridgeCdmData["publicInformation"]["approximatePagesRemainingDisplay"])
        #cdm comparasion
        assert approximatePagesRemainValue['text'].find(cdmApproximatePagesRemainValue) != -1, "approximatePagesRemain Value  mismatch"  

        # # Test Approximate Pages Remaining
        pagesPrinted = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.pagesPrinted, 0)
        loc_pagesPrinted = LocalizationHelper.get_string_translation(net, "cPagesPrintedWithSupply", 'en-US')
        assert pagesPrinted['text'].find(loc_pagesPrinted) != -1, "pagesPrintedName Text mismatch"

        pagesPrintedValue = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.pagesPrinted_value, 0)
        if(len(protectedCdmData[0]["compositeCountsByColorCode"]) < 2):
            cdmPagesPrintedValue = "0"
        else:
            cdmPagesPrintedValue = str(protectedCdmData[0]["lifeValue"]["count"])
        #cdm comparasion
        assert pagesPrintedValue['text'].find(cdmPagesPrintedValue) != -1, "pagesPrinted Value  mismatch"

        spice.suppliesapp.close_supply_card_view()

    def goto_menu_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self.click_on_cartridges()

    def click_on_cartridges(self):
        self._spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_summary)
        supplies_grid_tab_layout_app = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.supplies_summary)
        supplies_grid_tab_layout_app["currentIndex"] = "0"
        supplies_grid_tab_layout_app.mouse_click()

    def close_supply_card_view(self):
        close_button = self._spice.query_item(SuppliesAppWorkflowUICommonOperationsObjectsIds.close_button)
        close_button.mouse_click()