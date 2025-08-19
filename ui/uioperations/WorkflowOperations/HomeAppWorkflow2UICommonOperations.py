import logging
import time

from dunetuf.ui.uioperations.BaseOperations.IHomeAppUIOperations import IHomeAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.ui.uioperations.BaseOperations.IFaxAppUIOperations import IFaxAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowObjectIds import QuicksetsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflow2UICommonOperations import SignInAppWorkflow2UIOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.cdm import CDM

class HomeAppWorkflow2UICommonOperations(HomeAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.workflow_common_operations = Workflow2UICommonOperations(self._spice)

    def goto_home_menu(self):
        self._spice.goto_homescreen()
        time.sleep(5)
        self._spice.udw.mainUiApp.ApplicationEngine.launchApp("AdminApp")
        time.sleep(2)

        print("At Menu App")

    def goto_home_copy(self):
        self._spice.goto_homescreen()
        time.sleep(5)
        try:
            self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_only_copy)
            print("At copy App - at ID/Document copy selection screen")
        except:
            self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_only_copy)
            print("At Copy App")


    def goto_home_copy_in_folder(self):
        self._spice.goto_homescreen()
        time.sleep(5)
        try:
            self.home_navigation(HomeAppWorkflowObjectIds.copy_app_button)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_copy)
            print("At copy App - at ID/Document copy selection screen")
        except:
            self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp, HomeAppWorkflowObjectIds.home_folder_view)
            time.sleep(2)
            assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_only_copy)
            print("At Copy App")

    def goto_home_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Home screen -> Print app
        @return:
        """
        self.home_navigation(HomeAppWorkflowObjectIds.print_app_button)
        time.sleep(2)
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_print)['text'] == 'Print'
        logging.info("At Print App Screen")

    def goto_home_settings_app(self, spice):
        """
        Function to navigate to Settings app on home screen
        UI Flow: Home screen -> Settings app
        """
        spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.view_menuSettings)

        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_settings_text)['text'] == 'Settings'
        print("At Settings App")

    def home_navigation(self, menu_item_id, screen_id= "#homeScreenSwipeView", scrolling_value = 0.1, select_option: bool = True):
        '''
        method searches and clicks a specified button on Home Screen
        Args:
            menu_item_id:pass the Object Id's in the form of string.
            screen_id:Object Id of the screen
            select_option:Select True to click on the element
        Returns:
        '''
        isVisible = False
        index = 0
        menu_item_id = menu_item_id.replace("MouseArea","")
        current_screen = self._spice.wait_for(screen_id)
        self._spice.query_item(screen_id)["currentIndex"] = 0
        while (isVisible is False):
            try:
                isVisible = self.workflow_common_operations.validateObjectVisibility(screen_id, menu_item_id, "", 0)
                logging.info("item visible:{0}".format(isVisible))
                if isVisible is False:
                    index = index + 1
                    maxPages = self._spice.query_item(screen_id)["count"]
                    while (isVisible is False and index < maxPages):
                        self.workflow_common_operations.scroll_to_home_page(screen_id, index)
                        isVisible = self.workflow_common_operations.validateObjectVisibility(screen_id, menu_item_id, "", 0)
                        index = index + 1

                if isVisible is True:
                    if select_option is True:
                        locator = menu_item_id if menu_item_id.find("#launcherButton") != -1 else menu_item_id + " #launcherButton"
                        current_button = self._spice.wait_for(locator)
                        logging.info("Before rearrangement X: {0}, Y: {1}".format(current_button["x"], current_button["y"]))
                        # Wait a brief moment for any rearrangement to complete
                        time.sleep(0.5)
                        current_button = self._spice.wait_for(locator)
                        logging.info("After rearrangement X: {0}, Y: {1}".format(current_button["x"], current_button["y"]))
                        current_button_height = current_button["height"]/2
                        current_button.mouse_click(0 , current_button_height)
                        time.sleep(1)
                        logging.info("Clicked Home item : {0}".format(menu_item_id))
                    else:
                        logging.info("Home item found : {0}".format(menu_item_id))
                else:
                    raise Exception("Home item not found : {0}".format(menu_item_id))

            except Exception as e:
                assert False, f"exception msg is {e}"

    def signin_from_homescreen(self,spice):
        spice.signIn.select_universal_sign_in_from_home()

    def perform_signIn(self,spice):
        spice.signIn.select_sign_in_method("admin", "user")
        spice.signIn.enter_credentials(True, "12345678")

    # signout from homescreen
    def signout_from_homescreen(self, spice):
        spice.goto_homescreen()
        try:
            spice.signIn.select_universal_sign_out_from_home()
            spice.signIn.cleanup( "success")
        except Exception as e:
            pass
        finally:
            logging.info("At Home Screen")

    def goto_home_scan_folder(self):
        self._spice.goto_homescreen()
        time.sleep(5)

        self.home_navigation(HomeAppWorkflowObjectIds.scan_folder_button)
        time.sleep(2)
        print("At Scan Folder")

        #verify scan apps are visible.
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "Scan folder header not visible"
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.header_text)["text"] == "Scan", "Scan folder header text not matching"

    def goto_home_menu_folder(self):
        self._spice.goto_homescreen()
        time.sleep(5)
        self._spice.udw.mainUiApp.ApplicationEngine.launchApp("AdminApp")
        time.sleep(2)
        print("At Menu Folder")

        #verify scan apps are visible.
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "Scan folder header not visible"
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["text"] == "Menu", "Scan folder header text not matching"

    def goto_home_print_folder(self):
        self._spice.goto_homescreen()
        time.sleep(5)

        self.home_navigation(HomeAppWorkflowObjectIds.print_folder_button)
        time.sleep(2)
        print("At Print Folder")

        #verify scan apps are visible.
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "Print folder header not visible"
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["text"] == "Print", "Print folder header text not matching"


    def goto_home_usb_drive_folder(self):
        self._spice.goto_homescreen()
        time.sleep(5)

        self.home_navigation(HomeAppWorkflowObjectIds.usb_folder_button)
        time.sleep(2)
        print("At USB Drive Folder")

        #verify scan apps are visible.
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "USB Drive folder header not visible"
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["text"] == "USB Drive", "USB Drive folder header text not matching"


    def goto_home_jobs_apps(self):
        self._spice.goto_homescreen()
        time.sleep(5)

        self.home_navigation(HomeAppWorkflowObjectIds.jobs_app_button)
        time.sleep(2)
        print("At Jobs App")

        #verify scan apps are visible.
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["visible"] == True, "Jobs app header not visible"
        assert self._spice.query_item(HomeAppWorkflowObjectIds.header_text)["text"] == "Jobs", "Jobs app header text not matching"

    def goto_homescreen(self) -> None:
        """
        Scrolls to the home page
        Parameters:
            -> spice: the spice object
        """

        self._spice.goto_homescreen()
        # Get the homescreen swipeview object
        home_swipe_view = self._spice.query_item(HomeAppWorkflowObjectIds.home_swipe_view)
        home_swipe_view["currentIndex"] = 0
        time.sleep(2)

    def check_homeScreen_footer_state (self):
        """
        Method to verify the footer state of the home screen.

        Returns:
        bool: The current state of the footer (True if enabled, False if disabled).
        """

        isFooterAvailable = False

        try:
            homeScreen = self._spice.wait_for(HomeAppWorkflowObjectIds.view_homeScreen)
            isFooterAvailable = homeScreen["isHomeScreenFooterAvailable"]
            logging.info("Home Screen Footer is in Enabled State")
        except:
            logging.info("Home Screen Footer is in Disabled State")

        logging.info("Footer State: {0}".format(isFooterAvailable))
        return isFooterAvailable

    def  verify_alert_toner_error(self, spice, net):
        # Creating toner error alert message
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction GUIDEDFLOW activateFlow {{flowIdentification:USED_SUPPLY_PROMPT,stateProvider: {subsystem:CARTRIDGES}}}")
        assert spice.wait_for("#usedSupplyPromptWindow")
        current_string = []
        alert_id= ["alertDetailDescription","alertDetailDescription1"]
        string_ids= ["cIndicatedCartridgesUsed","cIndicatedCartridgeUsedCounterfeit"]

        self.cdm = CDM(self.spice.ipaddress, timeout=5.0)

        alert_response = self.cdm.get_raw(self.cdm.ALERTS)
        alert_response_body = alert_response.json()
        # check other ioref ussed for toner error alert
        for i in range(len(alert_response_body['alerts'])):
            if alert_response_body['alerts'][i]['category'] == "usedSupplyPrompt":
                if alert_response_body['alerts'][i]['stringId'] == 80034:
                   print("hpMfp Model") 
                   string_ids= ["cCartridgesRefilledDepleted", "cRecommendedHpCartridges"]
                   break

        for alert in alert_id:
            try:
                string = spice.query_item("#"+alert+" SpiceText[visible=true]")["text"]
                current_string.append(str(string))
            except:
                logging.info("AlertDetailDescription window not found")
        expected_string = []
        for string in string_ids:
            string = LocalizationHelper.get_string_translation(net, string)
            expected_string.append(str(string))         
        assert any(string in current_string for string in expected_string), "No expected string found in current string"
        ok_button = spice.wait_for("#OK")
        ok_button.mouse_click()

    def verify_alert_load_paper(self, spice, net):
        # Creating load paper error alert message
        spice.udw.mainApp.execute("UserPrompt PUB_triggerRequest MediaLoad")
        assert spice.wait_for("#mediaLoadFlowWindow")
        hide_button = spice.wait_for("#hide")
        hide_button.mouse_click()
        spice.statusCenter_dashboard_expand()
        alertButton = spice.wait_for(MenuAppWorkflowObjectIds.alert_button)
        spice.wait_until(lambda: alertButton["visible"] == True)
        alertButton.mouse_click()
        spice.wait_for("#alertAppView #alertAppHeader")
        spice.wait_for("#alertAppView #alert0")
        alert0 = spice.wait_for("#alertAppView #alert0")
        alert0.mouse_click()
        try:
            okbutton = spice.wait_for("#OK")
            okbutton.mouse_click()
        except:
            try:
                hide_button = spice.wait_for("#hide")
                hide_button.mouse_click()
            except:
                logging.warning("Neither OK nor hide button was found.")
        spice.statusCenter_dashboard_collapse()
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
        expected_string = LocalizationHelper.get_string_translation(net, "cAllDoorsCoversClosed")
        assert current_string == expected_string, "String mismatch"
        time.sleep(5)
        close_button = spice.wait_for("#closeButton")
        close_button.mouse_click()
        spice.status_center.click_alert_in_alert_app(0)
        # Removing the error using UDW command
        spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:DOOR_OPEN,instanceId:1}}")


    def verify_alert_cartridges_low(self, spice, cdm, configuration):
        color_supported = cdm.device_feature_cdm.is_color_supported()
        is_enterprise = configuration.familyname == 'enterprise'
        dict_supply = {2:'#cartridgeLow2Window', 1:'#cartridgeLow1Window', 3:'#cartridgeLow3Window', 4:"#cartridgeLow4Window"}
        supply_icon = "#alertStatusImage"
        if is_enterprise:
            supply_icon = "#columnforText1 #imageContainer"
        try:
            # Creating cartridges low alert message
            if color_supported:
                for n in dict_supply:
                    spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification: 'CARTRIDGE_LOW',instanceId: " + str(n) + "}}")
                    #Enterprise will generate multiple alerts
                    if is_enterprise:
                        assert spice.wait_for(dict_supply[n], timeout=15) 
                    else:
                        assert spice.wait_for(dict_supply[2], timeout=15)
                    spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
                    spice.wait_for("#OK").mouse_click()
            else:
                spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
                time.sleep(3)
                assert spice.wait_for(dict_supply[1])
                spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
                spice.wait_for("#OK").mouse_click()
            spice.status_center.click_alert_in_alert_app("0")
            if color_supported:
                assert spice.wait_for(dict_supply[2], timeout=15)
            else:
                assert spice.wait_for(dict_supply[1], timeout=15)
            assert spice.wait_for(supply_icon)  
            spice.suppliesapp.verify_cartridges_ui_alert('cCartridgesLow', 'cartridge_low')
        finally:
            # Removing the error using UDW command
            if color_supported:
                for n in dict_supply:
                    spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification: 'CARTRIDGE_LOW',instanceId: " + str(n) + "}}")
            else:
                spice.udw.mainApp.execute("EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification: 'CARTRIDGE_LOW',instanceId: 1}}")
            spice.statusCenter_dashboard_collapse()

    
    
    def verify_language_change_objectname_check(self, spice, cdm, objName):
        #This method checks if the language change is affecting object names of quick actions
        try: 
            #Check StatusButtonSignInAction
            spice.wait_for(objName)
            signInButton = spice.query_item(objName)
            spice.wait_until(lambda: signInButton["visible"] == True)

            #Change language to Spanish
            resultLanguage = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION_ENDPOINT, {"deviceLanguage":'es'})
            assert resultLanguage.status_code == 204 , "CDM patch command failed, status=%d" % resultLanguage.status_code

            #Check StatusButtonSignInAction
            spice.wait_for(objName)
            signInButton = spice.query_item(objName)
            spice.wait_until(lambda: signInButton["visible"] == True)

        finally:
            #Reset language to English
            resultLanguage = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION_ENDPOINT, {"deviceLanguage":'en'})

            assert resultLanguage.status_code == 204 , "CDM patch command failed, status=%d" % resultLanguage.status_code
    
    def is_on_home_screen(self) -> bool:
        persistent_header = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_header, timeout=5)
        if not persistent_header: return False
        logging.debug("is_on_home_screen: Persistent header found.")

        main_app_stack_view = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.home_app_view, timeout=5)

        if not main_app_stack_view: return False
        logging.debug("is_on_home_screen: Home App found.")

        is_visible = self.workflow_common_operations.get_element_property(main_app_stack_view, "activeFocus")
        if not is_visible:
            logging.debug("is_on_home_screen: Home App did not have activeFocus.")
        return is_visible

    def goto_home_fax(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.fax_app_button)

        print("At Fax app")

    def goto_home_tools(self):
        print("goto home tools - Navigating to tools app via home")
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.tools_app_button)

        print("At Tools app")
        
    def goto_home_mediaApp(self):
        self._spice.goto_homescreen()
        self.home_navigation("#60ce8d1a-64b1-4850-875b-5b9acfc95963")
        print("At Media App")

    def goto_home_contacts(self):
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.contact_app_button)

        assert self._spice.wait_for(HomeAppWorkflowObjectIds.contact_app_landing_view)
        print("At Contacts App")

    
    def has_persistent_header(self) -> bool:
        """
        Persistent Header is only available on Workflow 2 UI

        Args:
            No arguments
        
        Returns:
            bool: True - Workflow 2 will have persistent header
        
        Raises:
            None
        """
        return True

    def get_sign_in_initial(self) -> str:
        """
        Get the user's sign-in initials from the sign-in button in the persistent header

        Args:
            No arguments
        
        Returns:
            str: The user's initials string
        
        Raises:
            TimeoutError: If the sign-in button's 'showSignIn' property value is False after 10 seconds
        """
        sign_in_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_sign_in_button)
        self._spice.wait_until(lambda: sign_in_button['showSignIn'] == False, timeout=10)
        sign_in_initial = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_sign_in_button + " SpiceText")
        return self.workflow_common_operations.get_element_property(sign_in_initial, "text")
    
    def is_persistent_header_signed_in(self) -> bool:
        """
        Check if a user is signed in by checking the persistent header sign-in button

        Args:
            No arguments
        
        Returns:
            bool: True if the sign-in button 'showSignIn' property is False, False otherwise
        
        Raises:
            None
        """
        sign_in_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_sign_in_button, timeout=15)
        return not self.workflow_common_operations.get_element_property(sign_in_button, "showSignIn")
    
    def click_sign_in_button(self) -> bool:
        """
        Click the sign-in button in the persistent header

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' on the sign-in button was performed, False otherwise
        
        Raises:
            None
        """
        logging.info("Click sign-in button in Persistent Header from Home page")
        persistent_header_sign_in_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_sign_in_button)
        return self.workflow_common_operations.click(persistent_header_sign_in_button, click_center=False)
    
    def click_sign_out_button(self) -> bool:
        """
        Click the sign-out button in the persistent header

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' on the sign-out button was performed, False otherwise
        
        Raises:
            None
        """
        logging.info("Click sign-out button in Persistent Header from Home page")
        persistent_header_sign_in_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.persistent_sign_in_button)
        self._spice.wait_until(lambda: persistent_header_sign_in_button.is_enabled(), timeout=Workflow2UICommonOperations.DEFAULT_WAIT_TIME_SECONDS)
        return self.workflow_common_operations.click(persistent_header_sign_in_button, click_center=False)

    def goto_home_quicksetapp_landing_view(self, quickset_type):
        """
        Printer Home screen -> Menu -> Quicksets app -> Corresponding app
        @param quickset_type: email/sharepoint/usb/folder/copy
        """
        logging.info(f"goto_quicksetapp_landing_view and quickset_type is <{quickset_type}>")
        self._spice.goto_homescreen()
        self.home_navigation(HomeAppWorkflowObjectIds.home_quickset_button)
        #need to wait to load login display
        time.sleep(2)
        try:
            self._spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"]
            logging.info("At Sign-in Screen")
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            logging.info("perform sign-in")
            #Sign-In and authenticate
            self.perform_signIn(self._spice)
            response = self._spice.signIn.verify_auth("success")
            assert response == True
            #need to wait till succesful toast disappears
            time.sleep(2)
        finally:
            logging.info("signed in")
        
        if quickset_type:
            self._spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)
            menu_list_screen = self._spice.wait_for(QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view)
            self._spice.wait_until(lambda: menu_list_screen["visible"])
            if quickset_type == 'sharepoint':
                time.sleep(1)
                if not menu_list_screen["atYEnd"]:
                    logging.info(f"need to scroll to screen bottom")
                    max_y = menu_list_screen["contentHeight"] - menu_list_screen["height"]
                    menu_list_screen["contentY"] = menu_list_screen["originY"] + max_y
                    time.sleep(2)

            if quickset_type == "copy":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.copy_item}"
            elif quickset_type == "email":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_email_item}"
            elif quickset_type == "sharepoint":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_sharepoint_item}"
            elif quickset_type == "usb":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_usb_item}"
            elif quickset_type == "folder":
                item_object = f"{QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view} {QuicksetsAppWorkflowObjectIds.scan_to_folder_item}"

            if quickset_type == 'copy':
                item = self._spice.wait_for(item_object)
                if not self._spice.query_item(item_object)["visible"]:
                    item = self._spice.query_item(item_object, 2)
            else:
                item = self._spice.wait_for(f"{item_object} MouseArea")
            item = self._spice.wait_for(f"{item_object} MouseArea")
            item.mouse_click()
            logging.info(f"At quicksetapp_landing_view and quickset_type is <{quickset_type}>")
        else:
            self._spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
            logging.info(f"No corresponding quickset app")
 
    def goto_home_trays_app(self):
        self._spice.goto_homescreen()
        self.home_navigation("#60ce8d1a-64b1-4850-875b-5b9acfc95963")
        assert self._spice.wait_for(HomeAppWorkflowObjectIds.view_supplies_text,timeout = 5)['text'] == 'Trays'
        print("At Trays App")
    
    def click_copy_app(self) -> bool:
        """
        Click the Copy app from the home page on a Workflow 2 UI device

        Args:
            No arguments
        
        Returns:
            bool: True if the 'click' was perfomred, False otherwise
        
        Raises:
            None
        """
        copy_app_button = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.button_copyApp + " MouseArea")
        return self.workflow_common_operations.click(copy_app_button)

    def on_home_screen(self) -> bool:
        main_app_stack_view = self.workflow_common_operations.get_element(HomeAppWorkflowObjectIds.home_app_view)
        if not self.workflow_common_operations.get_element_property(main_app_stack_view, "activeFocus"):
            logging.error("Not on home screen. Something is in front of the home screen.")
            return False
        return True
    
    def goto_copy_app(self):
        self.home_navigation(HomeAppWorkflowObjectIds.button_copyApp)

