import logging
import time

from dunetuf.ui.uioperations.BaseOperations.IHomeAppUIOperations import IHomeAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowObjectIds import StatusCenterWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.BaseOperations.IFaxAppUIOperations import IFaxAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ContactsAppWorkflowObjectIds import ContactsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowObjectIds import StatusCenterWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class HomeAppWorkflowUICommonOperations(IHomeAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = self._spice.basic_common_operations

    def _scroll_to_position_horizontal(self, position: int) -> None:
        '''
        Scrolls to the provided position
        Parameters:
        spice: the spice object
        position: between 0-1
        '''
        assert (position >= 0 and position <= 1), "Wrong value. Postion can only be between 0 and 1"

        print("Moving scroll to position : " + str(position))
        scrollbar = self._spice.wait_for(HomeAppWorkflowObjectIds.home_dock_hscrollbar)
        scrollbar.__setitem__("position", str(position))

    def goto_home_menu(self):
        self._spice.goto_homescreen()
        self._scroll_to_position_horizontal(0)
        menu_app_button = self._spice.wait_for(HomeAppWorkflowObjectIds.menu_app_button)
        menu_app_button.mouse_click()
        time.sleep(3)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_menu)
        print("At Menu App")

    def goto_home_copy(self):
        self._spice.goto_homescreen()
        time.sleep(5)
        try:
            self.home_navigation(HomeAppWorkflowObjectIds.copy_app_button)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_copy)
            print("At copy App - at ID/Document copy selection screen")
        except:
            self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_only_copy)
            print("At Copy App")

    def goto_home_supplies(self):
        self._spice.goto_homescreen()
        menuApp = self._spice.wait_for(HomeAppWorkflowObjectIds.supplies_app_button)
        menuApp.mouse_click()
        time.sleep(3)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_supplies)
        print("At Supplies App")

    def goto_home_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Home screen -> Print app
        @return:
        """
        self._spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.print_app_button) ["visible"] == True, 'Print is not visible'
        self._spice.wait_for(HomeAppWorkflowObjectIds.print_app_button).mouse_click()
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_print)['text'] == 'Print'
        logging.info("At Print App Screen")

    def goto_home_help_app(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.help_app_button)
        time.sleep(2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_help)['text'] == 'Help'
        print("At Help App")

    def goto_home_supplies_app(self):
        self._spice.goto_homescreen()
        self.home_navigation("#a5e59604-d216-4977-a901-4774fcacbcb4")
        time.sleep(2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_supplies_text)['text'] == 'Supplies'
        print("At Supplies App")

    def goto_home_trays_app(self):
        self._spice.goto_homescreen()
        self.home_navigation("#60ce8d1a-64b1-4850-875b-5b9acfc95963")
        time.sleep(2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_supplies_text)['text'] == 'Trays'
        print("At Trays App")

    def goto_home_jobs_app(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.jobs_app_button)
        time.sleep(2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_jobs_text)['text'] == 'Jobs'
        print("At Jobs App")

    def get_all_button_ids(self):
        button_ids = []
        time.sleep(2) # time for RPC event to propogate
        self._spice.wait_for(HomeAppWorkflowObjectIds.view_homeScreen)
        for i in range(100):    # support a max of 100 buttons
            try:
                button = self._spice.query_item(HomeAppWorkflowObjectIds.all_app_buttons, i)
                button_ids.append(button['objectName'])
            except Exception:
                # All existing buttons have been found
                break
        for i in range(100):    # support a max of 100 buttons
            try:
                button = self._spice.query_item(HomeAppWorkflowObjectIds.all_app_launcher_buttons, i)
                button_ids.append(button['objectName'])
            except Exception:
                # All existing launcher buttons have been found
                break
        return button_ids

    def home_navigation(self, menu_item_id, screen_id= "#hScroll", scrolling_value = 0.1, select_option: bool = True):
        '''
        method searches and clicks a specified button on Home Screen
        Args:
            menu_item_id:pass the Object Id's in the form of string.
            screen_id:Object Id of the screen
            select_option:Select True to click on the element
        Returns:
        '''
        isVisible = False
        step_value = 0
        while (isVisible is False and step_value <= 1):
            try:
                current_screen = self._spice.wait_for(screen_id)
                isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 0)
                while (isVisible is False and step_value <= 1):
                    self.workflow_common_operations.scroll_to_position_horizontal(step_value)
                    time.sleep(2)
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 0)
                    step_value = step_value + scrolling_value

                if select_option is True and isVisible is True:
                    isVisible = self.workflow_common_operations.validateListObjectVisibility(screen_id, menu_item_id, "", 0)
                    if isVisible is True:
                        current_button = self._spice.query_item(menu_item_id + " MouseArea")
                        # Clicking in the mid height of the button to avoid click on header or section
                        current_button_height = current_button["height"]/2
                        current_button.mouse_click(0 , current_button_height)
                        time.sleep(1)
                        logging.info("Clicked Menu item : {0}".format(menu_item_id))
                    else:
                        logging.info("Menu item not found : {0}".format(menu_item_id))

            except Exception as e:
                assert False, f"exception msg is {e}"

    def goto_home_fax(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.fax_app_button)
        time.sleep(2)
        print("At fax App")

    def goto_home_fax_configured_faxsendrecipient_screen(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.fax_app_button)
        time.sleep(2)
        logging.info("At Fax Screen")
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)
        print("At fax App")

    def fax_menu_navigation(self, button_object_id, expected_object_id, select_option: bool = True):
        """
        Purpose: method searches and clicks a specified button on a specified menu under fax settings
        Navigation: NA
        Args:
            button_object_id: Object Id of the button to be pressed
            expected_object_id: Object Id of the expected screen
            select_option: Select True to click on the element
        """

        current_button = self._spice.wait_for(button_object_id + " SpiceText")
        current_button.mouse_click()
        self._spice.wait_for(expected_object_id, 5)
        logging.info("At Expected Menu")

    def  verify_alert_toner_error(self, spice, net):
        # Creating toner error alert message
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction GUIDEDFLOW activateFlow {{flowIdentification:USED_SUPPLY_PROMPT,stateProvider: {subsystem:CARTRIDGES}}}")
        assert spice.wait_for("#usedSupplyPromptWindow")
        current_string = spice.query_item("#alertDetailDescription SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cIndicatedCartridgesUsed")
        assert current_string == expected_string, "String mismatch"
        ok_button = spice.wait_for("#OK")
        ok_button.mouse_click()

    def verify_alert_load_paper(self, spice, net):
        # Creating load paper error alert message
        spice.udw.mainApp.execute("UserPrompt PUB_triggerRequest MediaLoad")
        assert spice.wait_for("#mediaLoadFlowWindow")
        try:
            hide_button = spice.wait_for("#hide")
            hide_button.mouse_click()
            spice.statusCenter_dashboard_expand()
            alert_option = spice.wait_for("#alertStatusCenterText")
            alert_option.mouse_wheel(0, -150)
            time.sleep(5)
            alert_option.mouse_click()
            try:
                okbutton = spice.wait_for("#OK")
                okbutton.mouse_click()
            except:
                hide_button = spice.wait_for("#hide")
                hide_button.mouse_click()
            spice.statusCenter_dashboard_collapse()
        except:
            try: 
                cancelbutton = spice.wait_for("#AlertFooter #Cancel")
            except:
                cancelbutton = spice.wait_for(MenuAppWorkflowObjectIds.cancelButton)
            cancelbutton.mouse_click()
        logging.info("Removing the alert using UDW command")
        udw_cancelalert = 'UserPrompt PUB_cancelRequest'
        logging.info("Executing UDW command: %s", udw_cancelalert)
        spice.udw.mainApp.execute(udw_cancelalert)
        # Close alert app if it is left open
        try:
            alertAppClose = spice.wait_for("#alertAppView #alertAppHeader #closeButton")
            alertAppClose.mouse_click()
        except:
            pass

    def verify_alert_door_open(self, spice, net):
        # Creating door open alert message
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification:DOOR_OPEN,instanceId:1}}")
        assert spice.wait_for("#doorOpen1Window")
        assert spice.wait_for("#alertStatusImage")
        assert spice.wait_for("#alertDetailDescription")
        current_string = spice.wait_for("#alertDetailDescription SpiceText[visible=true]")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cCloseTopCoverContinue")
        assert current_string == expected_string, "String mismatch"
        time.sleep(5)
        try:
            # close_button = spice.query_item("#closeButton")["visible"] == True, 'closeButton is visible'
            close_button = spice.wait_for("#closeButton")["visible"] == True, 'closeButton not visible'
            close_button.mouse_click()
            spice.statusCenter_dashboard_expand()
            alert_option = spice.wait_for("#alertStatusCenterText")
            alert_option.mouse_wheel(0, -150)
            time.sleep(5)
            alert_option.mouse_click()

            # Removing the error using UDW command
            spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:DOOR_OPEN,instanceId:1}}")
            spice.statusCenter_dashboard_collapse()
        except:
            spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:DOOR_OPEN,instanceId:1}}")

    def verify_alert_cartridges_low(self, spice, cdm, configuration):
        color_supported = cdm.device_feature_cdm.is_color_supported()
        dict_supply = {1:'#cartridgeLow1Window', 2:'#cartridgeLow2Window', 3:'#cartridgeLow3Window', 4:"#cartridgeLow4Window"}
        supply_icon = "#alertStatusImage"
        try:
            # Creating cartridge low alert message
            spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
            spice.wait_until(lambda:cdm.alerts.is_alert_present("cartridgeLow"), timeout=20, current_state_method=cdm.alerts.get_alert_list)
            spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
            spice.suppliesapp.press_alert_button("#OK")
            assert True == spice.is_HomeScreen(), "Control panel is not in Home screen"
            logging.debug("Alert cleared successfully")

            spice.statusCenter_dashboard_expand()
            alert_option = spice.wait_for("#alertStatusCenterText")
            alert_option.mouse_wheel(0, -200)
            time.sleep(5)
            alert_option.mouse_click()
            assert spice.wait_for(supply_icon)
            spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
        finally:
            # Removing the error using UDW command
            spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
            spice.statusCenter_dashboard_collapse()

    def has_persistent_header(self) -> bool:
        """
        Persistent Header is only available on Workflow 2 UI

        Args:
            No arguments
        
        Returns:
            bool: False - Workflow will not have persistent header (Only Workflow 2)
        
        Raises:
            None
        """
        return False
    
    def goto_home_usb_drive_folder(self):
        self._spice.goto_homescreen()

        self.home_navigation(HomeAppWorkflowObjectIds.usb_folder_button)
        print("At USB Drive Folder")

        #verify scan apps are visible.
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "USB Drive folder header not visible"
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["text"] == "USB Drive", "USB Drive folder header text not matching"
    
    def is_back_button_visible(self):
        try:
            back_button = self._spice.wait_for(HomeAppWorkflowObjectIds.back_button)
            self._spice.wait_until(lambda: back_button["visible"] == True)
            return True
        except TimeoutError:
            return False

    def is_on_home_screen(self) -> bool:
        # Check if any sign-in related screen exists
        sign_in_stack_view = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.signInStackView, timeout=1)
        if sign_in_stack_view:
            # If the sign-in stack view exists, wait up to 5 seconds for it to not exist
            try:
                self._spice.wait_until(lambda: self._spice.check_item(SignInAppWorkflowObjectIds.signInStackView) == None, 5)
            except:
                return False
        if self._spice.check_item(SignInAppWorkflowObjectIds.signInStackView):
            logging.error("Not on Home Screen. Sign-In view still exists.")
            return False

        status_center = self.workflow_common_operations.get_element(StatusCenterWorkflowObjectIds.status_center_list_view, timeout=5)
        if not status_center:
            logging.error("Failed to get status center on home screen")
            return False

        state = self.workflow_common_operations.get_element_property(status_center, "state")
        if state == "EXPANDED":
            logging.error("Home Screen is not visible. Status Center is expanded.")
            return False
        
        main_app_stack_view = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.view_homeScreen)
        return main_app_stack_view
        
    def click_sign_in_button(self) -> bool:
        """
            Checks if we can sign-in through the home screen sign-in button, if it
            doesn't exist we try to sign-in through status center.
        """
        sign_in_button = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_button)
        if sign_in_button:
            sign_in_button_label = self.workflow_common_operations.get_element(SignInAppWorkflowObjectIds.sign_in_label)
            if not sign_in_button_label: return False
            if self.workflow_common_operations.get_element_property(sign_in_button_label, "text") != "Sign In": return False
            return self.workflow_common_operations.click(sign_in_button)

        status_center = self.workflow_common_operations.get_element(StatusCenterWorkflowObjectIds.status_center_list_view)
        if not status_center: return False
        if self.workflow_common_operations.get_element_property(status_center, "state") == "COLLAPSED":
            if not self.workflow_common_operations.click(status_center): return False
            
        status_center_sign_in_button = self.workflow_common_operations.get_element(StatusCenterWorkflowObjectIds.button_sign_in)
        if not status_center_sign_in_button: return False
        return self.workflow_common_operations.click(status_center_sign_in_button)

    def goto_home_scan_folder(self):
        self._spice.goto_homescreen()
        # Wait until the scan folder button is visible and enabled before clicking
        scan_folder_button = self._spice.wait_for(HomeAppWorkflowObjectIds.scan_folder_button)
        self._spice.validate_button(scan_folder_button)
        self.home_navigation(HomeAppWorkflowObjectIds.scan_folder_button)
        print("At Scan Folder")
        #verify scan apps are visible.
        header = self._spice.wait_for(HomeAppWorkflowObjectIds.header_text)
        self._spice.validate_button(header)
        assert header["text"] == "Scan", "Scan folder header text not matching"	
        
    def is_cancel_button_visible(self):
        try:
            cancel_button = self._spice.wait_for(HomeAppWorkflowObjectIds.cancel_button)
            self._spice.wait_until(lambda: cancel_button["visible"] == True)
            return True
        except TimeoutError:
            return False

    def goto_home_contacts(self):
        self.goto_menu(self._spice)
        #self.spice.wait_for(ContactsAppWorkflowObjectIds.view_contacts)
        self.scroll_position_utilities(ContactsAppWorkflowObjectIds.menu_button_contacts)
        current_button = self._spice.wait_for(ContactsAppWorkflowObjectIds.menu_button_contacts + " MouseArea")
        current_button.mouse_click()

    def scroll_position_utilities(self, menu_item_id, delta = 0, use_bottom_border = True):
        try:
            if use_bottom_border:
                bottom_border = MenuAppWorkflowObjectIds.utilities_section_bottom_border
            else:
                bottom_border = ""
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, menu_item_id , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , bottom_border , delta)
        except Exception:
            if use_bottom_border:
                bottom_border = MenuAppWorkflowObjectIds.empty_section_bottom_border
            else:
                bottom_border = ""
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, menu_item_id , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.empty_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , bottom_border , delta)

    def goto_menu(self, spice):

        # make sure that you are in home screen
        spice.goto_homescreen()

        # Implementation for floating dock implementation for hme screen
        try:
            spice.query_item("#floatingDock")
            logging.info("Printer Having Foating Dock Homescreen")
            self.goto_menu_app_floating_dock(spice)

        except:
            logging.info("Printer Having Regular Homescreen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
            homeApp = spice.query_item(MenuAppWorkflowObjectIds.view_homeScreen)
            spice.wait_until(lambda: homeApp["visible"] == True)
            logging.info("At Home Screen")
            # move the scrollbar firstly.
            self.workflow_common_operations.scroll_to_position_horizontal(0)
            logging.info("Reset horizontal scrollbar")
            time.sleep(2)
            # Printer goes into sleep mode once cdm/ews calls[that execution time is greater than sleep time] in test before UI naviation, for
            # this scenario need to check printer in sleep or not when perform UI navigation
            currentState = int(spice.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
            logging.debug('Printer Sleep status is: %s',currentState)
            if currentState >= 2:
                logging.debug("Waking up printer")
                spice.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
                time.sleep(2)

            # enter the menu screen
            logging.info("Entering Menu")
            adminApp = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp +" MouseArea" )
            # Wait for clickable situation
            spice.wait_until(lambda: adminApp["enabled"] == True)
            spice.wait_until(lambda: adminApp["visible"] == True)
            adminApp.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, timeout = 15.0)
        logging.info("At Menu Screen")
        time.sleep(1)

    def wait_for_home_screen(self) -> bool:
        main_app_stack_view = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.home_app_view)
        try:
            self._spice.wait_until(lambda: main_app_stack_view["activeFocus"] == True)
        except TimeoutError:
            return False
        return True

    def goto_copy_app(self):
        self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)