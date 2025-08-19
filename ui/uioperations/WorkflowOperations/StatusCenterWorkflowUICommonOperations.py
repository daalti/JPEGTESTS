#########################################################################################
# @file      StatusCenterWorkflowUIOperations.py
# @author    Andrew Rose (Andrew.Rose@hp.com)
# @date      Dec 5, 2022
# @brief     Implementation of Status Center Workflow UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
"""
Implementation Sign In Workflow UI navigation methods
"""
import logging
from time import sleep
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.BaseOperations.IStatusCenterUIOperations import IStatusCenterUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowObjectIds import StatusCenterWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
import time

class StatusCenterWorkflowUICommonOperations(IStatusCenterUIOperations):
    """
    SignInAppWorkflowUIOperations module for Workflow Operations on SignInApp
    """
    def __init__(self, spice, cdm):
        self.maxtimeout = 100
        self.spice = spice
        self.cdm = cdm
        self.workflow_common_operations = spice.basic_common_operations
        self.workflow_sign_in_common_operations = SignInAppWorkflowUIOperations(self.spice)

    def goto_sign_in_app(self, action:str, SignIn:bool = True):
        '''
        UI should be on home screen before calling this method
        Navigate to Sign In via Status Center

        Navigation: Home Screen > Status Center

        Arguments:
            action (string): either "Sign In" or "Sign Out"
        '''
        # logging.info("Check if we are on the home screen...")
        # assert self.spice.is_HomeScreen(),\
        #     logging.error(f"Not on home screen. Make sure you are on the home screen before calling \"goto_sign_in_app\"")

        # Not expand status center if currently is visible
        if not self.is_status_center_visible():
            logging.info("Expand Status Center")
            self.expand()

        if not SignIn: return
        sign_in_button = self.get_sign_in_button(action)

        logging.info(f"Sign In button: {sign_in_button}")
        assert sign_in_button != None, logging.error(f"Sign In button does not match what was requested")

        sign_in_button.mouse_click()

    def get_sign_in_button(self, action:str):
        '''
        UI should be on Status Center before calling this method
        Get button on Status Center that either says "Sign In" or "Sign Out"

        Navigation: Stays on current page

        Arguments:
            action (string): either "Sign In" or "Sign Out"
        '''

        if action == "Sign In":
            button_name = StatusCenterWorkflowObjectIds.button_sign_in
        elif action == "Sign Out":
            button_name = StatusCenterWorkflowObjectIds.button_sign_out
        else:
            return

        button_name += " MouseArea" # Make sure to get the MouseArea which is the clickable part of the button

        try:
            button = self.spice.wait_for(button_name, timeout=25.0)
            logging.info(f"Wait for {button_name} button to be visible and clickable before performing mouse click.")
            self.spice.validate_button(button)
        except QmlItemNotFoundError:
            assert False, logging.error("Failed to find the Sign In/Out button.")
        
        return button

    def expand(self):
        '''
        UI can be on any page before calling this method
        Click Status Center drop down bar from the top of the screen to expand

        Navigation: Current Page > Status Center

        Arguments:
            None
        '''
        self.spice.statusCenter_dashboard_expand()
        logging.info("Waiting for Status Center to expand...")
        list_view = self.spice.wait_for(StatusCenterWorkflowObjectIds.status_center_list_view)
        self.spice.wait_until(lambda: list_view["visible"] == True)

    def is_status_center_visible(self):
        '''
        UI can be on any page before calling this method
        Check if Status Center is visible

        Navigation: Stays on current page

        Arguments:
            wait_until_visible: bool to advise that check to wait until is not true and return directly current state, default is True
        '''
        list_view = self.workflow_common_operations.get_element(StatusCenterWorkflowObjectIds.status_center_list_view)
        if not list_view:
            logging.debug("Status Center list view not found.")
            return False
        isVisible = self.workflow_common_operations.get_element_property(list_view, 'visible')

        return isVisible

    def collapse(self):
        '''
        UI should be on the expanded Status Center page
        Click Status Center drop down bar from the bottom of the screen to collapse
        
        Navigation: Status Center > Last Active Page

        Arguments:
            None
        '''
        self.spice.statusCenter_dashboard_collapse()
        list_view = self.spice.wait_for(StatusCenterWorkflowObjectIds.status_center_list_view)
        logging.debug(f"collapse - 'list_view['active']'={list_view['active']}")
        self.spice.wait_until(lambda: list_view["active"] == False, 5)

    def compare_homescreen_and_status_center_sign_in_buttons(self, spice):
        """
            Compares two sign in buttons to see if they both are "Sign In" buttons or "Sign Out" buttons
            Returns True if they are the same and False otherwise
        """
        homescreen_sign_in_button_text = spice.query_item(SignInAppWorkflowObjectIds.menu_item_signinid + " SpiceText")["text"]
        spice.status_center.expand()
        status_center_sign_in_button_text = self.get_sign_in_button_text()
        spice.status_center.collapse()

        return homescreen_sign_in_button_text == status_center_sign_in_button_text

    def get_sign_in_button_text(self):
        """
            Get the text of the sign in button on the status center

            Navigation: Stays on current page if status center is visible, expand status center if no

            Arguments:
                None

            Returns:
                string: "Sign In" or "Sign Out"
        """

        is_previously_expanded = self.is_status_center_visible()
        current_value = None

        if not is_previously_expanded:
            logging.info("Expand Status Center")
            self.expand()
            """
            There is no good way to wait for the status center to expand. The 'state', 'visible', and 'active' properties instantly change when the status center is expanded despite it not being fully expanded.
            This is why the sleep is used.
            """
            time.sleep(3)
            assert (is_previously_expanded := self.is_status_center_visible()), logging.error("Failed to expand status center")

        # Try to get "Sign In" button
        try:
            self.spice.query_item(StatusCenterWorkflowObjectIds.button_sign_in)
            current_value = "Sign In"
        except (QmlItemNotFoundError, TimeoutError):
            # If you can't get "Sign In" button, then try to get "Sign Out" button
            try:
                self.spice.query_item(StatusCenterWorkflowObjectIds.button_sign_out)
                current_value = "Sign Out"
            except (QmlItemNotFoundError, TimeoutError):
                pass
        logging.debug(f"get_sign_in_button_text - 'is_previously_expanded'={is_previously_expanded}")
        logging.debug(f"get_sign_in_button_text - 'current_value'={current_value}")
        if is_previously_expanded:
            logging.info("Collapse Status Center")
            self.collapse()
            assert not self.is_status_center_visible(), logging.error("Failed to collapse status center")

        return current_value

    def wait_for_warning_prompt(self, confirm:bool, timeout:int=10, checkHomeScreen:bool=True):
        """
            confirm:bool - True = click Yes, False = click No
        """
        # Wait for warning prompt
        confirm_sign_out_view = self.spice.wait_for("#confirmSignOutView", timeout=timeout)
        assert confirm_sign_out_view, logging.error("Failed to find status center sign out warning prompt")

        sign_out_message = 'cBySigningOut'
        proceed_prompt_message = 'cWantProceed'
        endpoint = "/hp/device/localization/localize.json"

        response = self.cdm.post_raw(endpoint, {'language':'en-US', 'stringIds':[sign_out_message, proceed_prompt_message]})
        assert response.status_code == 200, logging.error("Failed to get localization string")

        try:
            sign_out_message_string = response.json()['StringIds'][sign_out_message]
            proceed_prompt_message_string = response.json()['StringIds'][proceed_prompt_message]
        except KeyError:
            raise ValueError("Failed to get string messages or locale en-US does not exist.")

        sign_out_screen_message = self.spice.wait_for("#confirmSignOutView #confirmSignOutContent #signingOutSpiceText", timeout=timeout)['text']
        proceed_prompt_screen_message = self.spice.wait_for("#confirmSignOutView #confirmSignOutContent #wantProceedSpiceText", timeout=timeout)['text']
        assert sign_out_message_string == sign_out_screen_message, logging.error("Sign out message on the screen does not match expected sign out message string.")
        assert proceed_prompt_message_string == proceed_prompt_screen_message, logging.error("Proceed message on the screen does not match expected proceed message string.")

        if confirm:
            logging.info("Getting Sign-Out Yes Button")
            button = self.spice.wait_for("#confirmSignOutYesButton #ButtonControl", timeout=timeout)
        else:
            button = self.spice.wait_for("#confirmSignOutNoButton #ButtonControl", timeout=timeout)

        button.mouse_click()

        if confirm:
            # Status Center will automatically collapse
            list_view = self.spice.wait_for(StatusCenterWorkflowObjectIds.status_center_list_view)
            self.spice.wait_until(lambda: list_view["active"] == False, 15)

        if checkHomeScreen:
            # Status Center will automatically navigate back to home screen
            home_screen = self.spice.wait_for("#HomeScreenView")
            sleep(5)
            assert self.spice.is_HomeScreen(), logging.error("Failed to navigate back to home screen after signing out")

    def is_signed_in(self) -> bool:
        try:
            self.get_sign_in_button("Sign In")
            return False
        except:
            # Check Sign Out
            pass
        try:
            self.get_sign_in_button("Sign Out")
            return True
        except:
            return False
        
    def get_status_center(self):
        return self.workflow_common_operations.get_element(StatusCenterWorkflowObjectIds.status_center_list_view, 1)
    
    def check_scan_release_button_visible(self):
        '''Method to check if scan release button is visible

        Returns:
            bool: True if scan release button is visible, False otherwise
        '''
        if not self.is_status_center_visible():
            self.expand()
        
        try:
            self.spice.wait_for(StatusCenterWorkflowObjectIds.scan_release_page_dashboard)
            eject_button = True
        except:
            eject_button = False
        
        return eject_button

    def click_scan_release_button(self):
        '''
        Method to perform a click in release scan page in status center dashboard.
        
        if status center is not visible, method will expand previous click button
        
        '''
        if not self.is_status_center_visible():
            self.expand()

        self.spice.main_app.wait_and_click_on_middle(StatusCenterWorkflowObjectIds.scan_release_page_dashboard)
            