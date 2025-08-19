import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.InfoAppWorkflowUICommonOperations import InfoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations

class InfoAppWorkflowUILOperations(InfoAppWorkflowUICommonOperations):

    UI_INFO_APP = "#infoView"
    INFO_GRID_TAB_LAYOUT = "#infoView"
    CLOSE_INFO_CARD_VIEW = "#closeButton"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

        

    def click_on_printer(self):
        self._spice.wait_for(self.UI_INFO_APP)
        info_grid_tab_layout_app = self._spice.query_item(self.INFO_GRID_TAB_LAYOUT)
        info_grid_tab_layout_app["currentIndex"] = "0"
        info_grid_tab_layout_app.mouse_click()
        time.sleep(3)

    def click_on_connectivity(self):
        self._spice.wait_for(self.UI_INFO_APP)
        info_grid_tab_layout_app = self._spice.query_item(self.INFO_GRID_TAB_LAYOUT)
        info_grid_tab_layout_app["currentIndex"] = "1"
        info_grid_tab_layout_app.mouse_click()
        self._spice.wait_for("#infoView")

    def close_card_detail_panel_view(self):
        close_button = self._spice.wait_for(self.CLOSE_INFO_CARD_VIEW)
        close_button.mouse_click()

    def find_wifi_direct_card(self):
        self.workflow_common_operations.scroll_to_position_vertical(0.7, "#connectivityTabLayoutscroll1verticalScroll")
    
    def find_ethernet_card(self):
        self.workflow_common_operations.scroll_to_position_vertical(0.2, "#connectivityTabLayoutscroll1verticalScroll")
