import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.InfoAppWorkflowUICommonOperations import InfoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MenuAppWorkflowUIXLOperations import MenuAppWorkflowUIXLOperations

class InfoAppWorkflowUIXLOperations(InfoAppWorkflowUICommonOperations):

    UI_INFO_APP = "#infoView"
    INFO_GRID_TAB_LAYOUT = "#infoView"
    CLOSE_INFO_CARD_VIEW = "#closeButton"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.home_menu_workflow_xl_operations = MenuAppWorkflowUIXLOperations(self._spice)

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
        time.sleep(3)
    
    def close_card_detail_panel_view(self):
        close_button = self._spice.wait_for(self.CLOSE_INFO_CARD_VIEW)
        close_button.mouse_click()

    def goto_sign_in(self):
        admin_textfield = self._spice.wait_for("#userSignInComboBox")
        admin_textfield.mouse_click()

        select_admin = self._spice.wait_for("#userSignInComboBoxItem_admin")
        select_admin.mouse_click()

        password_textfield = self._spice.wait_for("#adminPasswordInputField")
        password_textfield.__setitem__('displayText', "12345678")

        signin_button = self._spice.wait_for("#adminSignInButton")
        signin_button.mouse_click()

        # Sleep while the welcome message is displayed
        time.sleep(5)
        