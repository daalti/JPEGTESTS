
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class MenuAppWorkflowUIMOperations(MenuAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        #self._spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUIMObjectIds = MenuAppWorkflowObjectIds()
        self.MenuAppWorkflowUIMObjectIds.menu_button_settings = "#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuApp"
        self.MenuAppWorkflowUIMObjectIds.view_menulistLandingpage = "#landingPageMenuAppList"
        self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF = "#printerUpdateSettingsTextImage"
        self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF = "#printerUpdateView" 
        self.MenuAppWorkflowUIMObjectIds.view_menuTools = "#toolsMenuAppList"
        self.MenuAppWorkflowUIMObjectIds.view_menuSettings = "#settingsMenuListListView"
        self.MenuAppWorkflowUIMObjectIds.menu_button_tools = "#toolsMenuApp"
        self.MenuAppWorkflowUIMObjectIds.menu_button_tools_maintenance = "##9da37e46-9b8a-4dc2-a24c-017fee6b088fMenuApp"
        self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_allowUpgrades_next = "#nextButton"
        self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF_iris_radioButtonsView="#radioButtonsViewlist1"
        self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_allowAutoUpdate = "#autoUpdateRadioButton"
        self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_notifyWhenAvailable = "#notifyWhenAvailableRadioButton"

    def goto_menu_settings(self, spice, signInRequired = True):
        self.goto_menu(spice)
        time.sleep(1)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings + " MouseArea")
        settingsButton.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        logging.info("At Settings Screen")

    def goto_menu_settings_output_destinations(self, spice):
        self.goto_menu_settings(spice)
        output_destinations = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations + " MouseArea")
        output_destinations.mouse_click()
        logging.info("At Output Destinations Settings Screen")

    def click_on_horizontal_cutter(self, spice):
        self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button, MenuAppWorkflowObjectIds.view_menu_settings_output_destinations)
        horizontal_cutter_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button)
        time.sleep(2)
        logging.info("Horizontal cutter switch status: {}".format(horizontal_cutter_switch_button["checked"]))

    def goto_menu_settings_printerUpdate(self, spice):
        self.goto_menu_settings(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF + " MouseArea")
        settingsButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        logging.info("At Printer Update WF Screen")

    def set_printerUpdate_allowAutoUpdate_goto_iris_message_screen(self, spice):
        self.set_printerUpdate_allowAutoUpdate(spice)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, False)

    def goto_menu_settings_printerUpdate_allowUpgrades_iris_options(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_allowUpgrades_next)
        settingsButton.mouse_click()
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_notifyWhenAvailable + " MouseArea")
        settingsButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)    

    def goto_menu_settings_printerUpdate_allowUpgrades_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_allowUpgrades_next)
        settingsButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_radio(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_allowAutoUpdate + " MouseArea")
        settingsButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF)
        logging.info("Set autoUpdateEnabled to true")
        time.sleep(1)

    def set_printerUpdate_notifyWhenAvailable(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_radio(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_settings_printerUpdateWF_notifyWhenAvailable + " MouseArea")
        settingsButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUIMObjectIds.view_printerUpdateWF)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_print_calibration)
        calibration.mouse_click()
        color_calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_color_calibration)
        color_calibration.mouse_click()

    def goto_menu_tools(self, spice):
        self.goto_menu(spice)
        button = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_tools+ " MouseArea")
        button.mouse_click()

        assert spice.wait_for(self.MenuAppWorkflowUIMObjectIds.view_menuTools)
        logging.info("At Tools Screen")
    
    def goto_menu_tools_servicemenu(self, spice, udw):
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_service , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        keyboard = spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard

        result = udw.mainApp.AdminStandard.resetToDefaultDevicePassword()
        assert result == 'SUCCESS'

        defaultPin = udw.mainApp.AdminStandard.getDefaultDevicePassword()
        assert len(defaultPin) > 0
        defaultPin = "12345678"

        keyboard.__setitem__('displayText', defaultPin) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', defaultPin)

        time.sleep(2)

        doneButton = spice.wait_for(MenuAppWorkflowObjectIds.view_service_sign_in_button)
        doneButton.mouse_click()

        time.sleep(5)        

        #In service menu now.
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service)
        logging.info("At Service Screen")
        time.sleep(1)

    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)

        # Click on Proceed Button
        proceedButton = spice.query_item("#SpiceView SpiceView SpiceText[visible=true]", 0)
        assert proceedButton["text"] == "Proceed", "Could not find Proceed Button"
        proceedButton.mouse_click()

    def goto_menu_info(self, spice):
        self.goto_menu(spice)
        toolsButton = spice.wait_for(self.MenuAppWorkflowUIMObjectIds.menu_button_info + " MouseArea")
        toolsButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo)
        logging.info("At Info Screen")

    def goto_menu_tools_maintenance(self,spice):
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_tools_maintenance , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_maintenance + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings)
        logging.info("At Maintenance Screen")

    def goto_menu_tools_troubleshooting(self, spice):
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_troubleshooting , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("user signed in")
        status_center_service_stack_view = spice.check_item(MenuAppWorkflowObjectIds.view_troubleshooting)
        if status_center_service_stack_view != None:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_menu_list)
        logging.info("At Troubleshooting Screen")

    def start_color_calibration(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.color_calibration)

    def start_automatic_printhead_alignment(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_alignement)

    def start_printheads_cleaning(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_cleaning)

    def start_calibration(self, spice, calibration):
        align_button = spice.wait_for(calibration + " MouseArea")
        align_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view)
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()

    def goto_menu_tools_reports(self, spice):
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_reports , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_reports + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_reports)
        logging.info("At Reports Screen")

    def set_inactivitytimeout_fiveminutes(self, spice):
        isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)
        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,300)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_inactivity_timeout_settings, MenuAppWorkflowObjectIds.inactivity_timeout_5mins)
        
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("Set Inactivity Timeout to 5 mins")
        time.sleep(1)

    def goto_menu_help(self, spice):
        self.goto_menu(spice)        
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp)
        logging.info("At help Screen")

    def goto_menu_help_hpenvironmentaltips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)        
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_hpenvironmentaltips)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_hpEnvironmentalTips)
        logging.info("At how to videos screen")

    def goto_menu_help_workingsmarttips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)        
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_workingsmarttips)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_workingSmartTips)

    def goto_menu_help_digitalofficetips(self, spice):
        self.goto_menu_help(spice)
        time.sleep(1)        
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_help_digitalofficetips)
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp_digitalOfficeTips)
        logging.info("At how to videos screen")

    def goto_document(self, spice):
        """
        Go to Copy Home by click Copy item on Menu Copy Screen
        """
        spice.wait_for(MenuAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")
        current_button = spice.query_item(MenuAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_copyScreen)

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_mediaApp, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage, MenuAppWorkflowObjectIds.utilities_column_name, MenuAppWorkflowObjectIds.landingPage_Content_Item, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)

    def goto_menu_settings_general_region(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_region_wf , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_country_region_wf)
        logging.info("At country/Region setting Screen")
        time.sleep(1)

    def region_settings_sampletest(self, spice):
        # click the country/region dropdown
        spice.homeMenuUI().goto_menu_settings_general_region(spice)
        time.sleep(10)
        self.menu_navigation_radiobutton(spice, MenuAppWorkflowObjectIds.view_settings_country_region_wf, "#AOcountryRegionWF", "#MenuValueAO", scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_countryregion_wf)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Menu")
        time.sleep(2)

    def goto_menu(self, spice):

        # make sure that you are in home screen
        spice.goto_homescreen()

        # Implementation for floating dock implementation for hme screen
        try: 
            spice.query_item("#floatingDock")
            print ("Printer Having Foating Dock Homescreen")
            self.goto_menu_app_floating_dock(spice)

        except:
            print ("Printer Having Regular Homescreen")
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
            time.sleep(5)

            # in some cases "#landingPageMenuAppList" is not viewed during execution
            while True:
                if spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, timeout = 9.0):
                    break
                else :
                    adminApp.mouse_click()
                    continue

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, timeout = 9.0)
        logging.info("At Menu Screen")
        time.sleep(3)

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            scroll_bar = spice.wait_for(scrollbar_id)
            scrollbar_size = scroll_bar["visualSize"]
            scroll_bar.__setitem__("position", scrollbar_size - size)
            return True