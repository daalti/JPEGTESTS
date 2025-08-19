import logging
import time
from random import randrange

from dunetuf.ui.uioperations.WorkflowOperations.InfoAppWorkflowUICommonOperations import InfoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations



class InfoAppWorkflowUISOperations(InfoAppWorkflowUICommonOperations):

    HOME_SCREEN_VIEW = "#HomeScreenView"
    HOME_BUTTON = "#HomeButton"
    INFO_ID = "#697749ba-b6ea-11eb-80d0-9ffe5c5f1620MenuApp"
    UI_INFO_APP = "#infoView"
    INFO_GRID_TAB_LAYOUT = "#infoView"
    CONNECTIVITY_GRID_TAB_LAYOUT = "#connectivityTabLayout"
    WIFI_DIRECT_CARD_OBJECT = "#wifiDirectCardInTab"
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
        middle_width = info_grid_tab_layout_app["width"] / 2
        height = info_grid_tab_layout_app["height"] / 4
        info_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def connectivityGetHostname(self):
        '''
        Recover the hostname value inside the connectivity details view.
        '''
        return self._spice.wait_for(self.hostname_name)["text"]

    def connectivityGetIP(self):
        '''
        Recover the IP value inside the connectivity details view.
        '''
        return self._spice.wait_for(self.Ip_adress)["text"]

    def connectivityGetIPv6(self):
        '''
        Recover the IPv6 value inside the connectivity details view.
        '''
        return self._spice.wait_for(self.Ipv6_adress_state)["text"]

    def connectivityGetMAC(self):
        '''
        Recover the MAC value inside the connectivity details view.
        '''
        return self._spice.wait_for(self.MAC_adress_eth0)["text"]

    def click_on_connectivity(self):
        self._spice.wait_for(self.UI_INFO_APP)
        info_grid_tab_layout_app = self._spice.query_item(self.INFO_GRID_TAB_LAYOUT)
        info_grid_tab_layout_app["currentIndex"] = "1"
        middle_width = info_grid_tab_layout_app["width"] / 2
        height = info_grid_tab_layout_app["height"] / 2
        info_grid_tab_layout_app.mouse_click(middle_width, height)
        time.sleep(3)

    def find_wifi_direct_card(self):
        self.workflow_common_operations.scroll_to_position_vertical(0.7, "#connectivityTabLayoutscroll1verticalScroll")

    def find_ethernet_card(self):
        self.workflow_common_operations.scroll_to_position_vertical(0.2, "#connectivityTabLayoutscroll1verticalScroll")
        
    def close_card_detail_panel_view(self):
        close_button = self._spice.wait_for(self.CLOSE_INFO_CARD_VIEW)
        close_button.mouse_click()

    def goto_sign_in(self):
        is_authentication_supported = True
        try:
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
        except Exception as message:
            logging.debug("Sign_in not supported %s", message)
            is_authentication_supported = False
        finally:
            return is_authentication_supported
