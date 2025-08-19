
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperations import SuppliesAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.SuppliesAppWorkflowUICommonOperationsObjectsIds import SuppliesAppWorkflowUICommonOperationsObjectsIds


class SuppliesAppWorkflowUIXLOperations(SuppliesAppWorkflowUICommonOperations):
    
    UI_SUPPLIES_APP = "#suppliesSummaryView"
    SUPPLIES_GRID_TAB_LAYOUT = "#suppliesSummaryView"
    SUPPLIES_REPLACEMENT_BUTTON = "#suppliesReplacementButton"
    CLOSE_SUPPLY_CARD_VIEW = "#closeButton"
    ACTION_NEEDED_PINTHEAD_RENPLACEMENT = "#acceptAction"
    REPLACE_CARRIDGE_NEEDED_PINTHEAD_RENPLACEMENT = "#continueAction"
    CALIBRATION_OK_BUTTON = "#calibrationFlow_finishedSuccess #continueAction"
    DETAILS_PRINTHEADS_STATUS = "#DetailInfo #rowBlockC #statusBoxBlockC SpiceText[visible=true]"
    PH_REPLACEMENT_WAIT_DOOR_OPEN = "#printheadReplacementFlow_waitForDoorOpen"
    PH_REPLACEMENT_WAIT_DOOR_OPEN_ANIMATION = "#printheadReplacementFlow_waitForDoorOpen #VideoLayout #VideoItem"
    PH_REPLACEMENT_PH_INSERTED = "#printheadReplacementFlow_printheadInserted"
    PH_REPLACEMENT_WAIT_DOOR_CLOSED = "#printheadReplacementFlow_waitForDoorClose"
    PH_REPLACEMENT_WAIT_DOOR_CLOSED_ANIMATION = "#printheadReplacementFlow_waitForDoorClose #VideoLayout #VideoItem"
    APA_CALIBRATION_PREPARING_TO_PRINT = "#calibrationFlow_preparingToPrint"
    APA_CALIBRATION_PRINTING = "#calibrationFlow_printingPattern"
    APA_CALIBRATION_FINISHED_SUCCESS = "#calibrationFlow_finishedSuccess"
    ALERT_IMAGE_ICON = "#imageObject"
    COMMON_ALERT_TEXT_ID = "#titleObject"
    COMMON_ALERT_TEXT_IDX = 0
    COMMON_STATUS_DETAIL_ID = "#alertDetailDescription #contentItem"
    COMMON_STATUS_DETAIL_IDX = 0
    COMMON_STATUS_TITLE = "#notificationRowAlertTitle #alertStatusCenterText" 
    COMMON_STATUS_TITLE_IDX = 0
    ALERT_BTN = "#ButtonControl #Background"
    ALERT_BTN1 = "#ButtonControl #Background"

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
    
    def click_on_maintenance_cartridge(self):
        self._spice.wait_for(self.UI_SUPPLIES_APP)
        supplies_grid_tab_layout_app = self._spice.query_item(self.SUPPLIES_GRID_TAB_LAYOUT)
        supplies_grid_tab_layout_app["currentIndex"] = "2"
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

    def click_cartrigdge_replacement_needed(self):
        self._spice.wait_for(self.ACTION_NEEDED_PINTHEAD_RENPLACEMENT).mouse_click()
        self._spice.wait_for(self.REPLACE_CARRIDGE_NEEDED_PINTHEAD_RENPLACEMENT).mouse_click()

    # Verticall Scrolling Cartridges window
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

    # Verticall Scrolling printHeads window
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
            obj_state = spice.wait_for("#block2 #rowBlockC #StatusText")
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
            obj_state = spice.wait_for(self.DETAILS_PRINTHEADS_STATUS)
            assert obj_state["visible"] == True
            state = obj_state["text"]
            spice_supplies[index] = self.status_converter(state)
            # Close printHead card view
            time.sleep(2)
            spice.suppliesapp.close_supply_card_view()
            self._scroll_to_position_vertical_printheads(spice,position)
            position += scroll_step
        return spice_supplies
    
    def goto_menu_supplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self.click_on_cartridges()

    def goto_menu_supplies_othersupplies_summary(self):
        """
        Navigates to supplies summary page
        """
        self.homemenu.goto_menu_supplies(self._spice)
        self.click_on_maintenance_cartridge()
    
    def verify_supplies_summary_information(self,spice,catridgeCdmData,index,net):
        """
        Function to validate supplies summary info
        """
        spice.wait_for(SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card + str(index))
        cartridgeInfo = spice.query_item( SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge_card +str(index)+ SuppliesAppWorkflowUICommonOperationsObjectsIds.cartridge)
        self.validate_cartridge_details_with_cdm(catridgeCdmData, cartridgeInfo)

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

            statusCenterDash.mouse_click(middle_width, middle_height)
            time.sleep(3)

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