
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.configuration import Configuration
class MenuAppWorkflowUILOperations(MenuAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        #self._spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUILObjectIds = MenuAppWorkflowObjectIds()
        self.MenuAppWorkflowUILObjectIds.menu_button_settings = "#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuApp"
        self.MenuAppWorkflowUILObjectIds.view_menulistLandingpage = "#landingPageMenuAppList"
        self.MenuAppWorkflowUILObjectIds.menu_button_settings_printerUpdateWF = "#printerUpdateSettingsTextImage"
        self.MenuAppWorkflowUILObjectIds.view_printerUpdateWF = "#printerUpdateView" 
        self.MenuAppWorkflowUILObjectIds.view_menuTools = "#toolsMenuAppList"
        self.MenuAppWorkflowUILObjectIds.view_menuSettings = "#settingsMenuListListView"
        self.MenuAppWorkflowUILObjectIds.menu_button_tools = "#toolsMenuApp"
        self.MenuAppWorkflowUILObjectIds.menu_button_tools_maintenance = "##9da37e46-9b8a-4dc2-a24c-017fee6b088fMenuApp"
        self.MenuAppWorkflowUILObjectIds.menu_button_settings_printerUpdateWF_allowUpgrades_next = "#nextButton"
        self.MenuAppWorkflowUILObjectIds.view_printerUpdateWF_iris_radioButtonsView="#radioButtonsViewlist1"
        self.MenuAppWorkflowUILObjectIds.menu_button_settings_printerUpdateWF_allowAutoUpdate = "#autoUpdateRadioButton"
        self.MenuAppWorkflowUILObjectIds.menu_button_settings_printerUpdateWF_notifyWhenAvailable = "#notifyWhenAvailableRadioButton"

    def goto_menu_settings(self, spice, signInRequired = True):
        self.goto_menu(spice)
        time.sleep(1)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUILObjectIds.menu_button_settings + " MouseArea")
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

    # Menu Settings General Energy prevent Shutdown

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown)
        logging.info("Set Energy prevent Shutdown to none(do not disable)")
        time.sleep(1)

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown)
        logging.info("Set Energy prevent Shutdown whenportsareactive)")
        time.sleep(1)

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_print_calibration)
        calibration.mouse_click()
        color_calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_color_calibration)
        color_calibration.mouse_click()

    def goto_menu_tools(self, spice):
        self.goto_menu(spice)
        button = spice.wait_for(self.MenuAppWorkflowUILObjectIds.menu_button_tools+ " MouseArea")
        button.mouse_click()

        assert spice.wait_for(self.MenuAppWorkflowUILObjectIds.view_menuTools)
        logging.info("At Tools Screen")
    
    def goto_menu_tools_servicemenu(self, spice, udw):
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
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
        toolsButton = spice.wait_for(self.MenuAppWorkflowUILObjectIds.menu_button_info + " MouseArea")
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
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        logging.info("At Troubleshooting Screen")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        logging.info("At Troubleshooting Screen")

    def start_color_calibration(self, spice, input_selection_screen = True):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.color_calibration)
        logging.info("Wait for input selection screen")
        if input_selection_screen:
            logging.info("Waits for input selection screen and select Roll")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

    def start_automatic_printhead_alignment(self, spice, input_selection_screen = True):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_alignment_auto_all)
        if input_selection_screen:
            logging.info("Waits for input selection screen and select Roll")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

    def start_printheads_cleaning(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_cleaning)

    def start_calibration(self, spice, calibration):
        align_button = spice.wait_for(calibration + " MouseArea")
        align_button.mouse_click()
        time.sleep(1)
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

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_mediaApp, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage, MenuAppWorkflowObjectIds.utilities_column_name, MenuAppWorkflowObjectIds.landingPage_Content_Item, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)

    def goto_menu_scan_scan_to_network_folder(self, spice):
        """
        Menu app-> Scan -> Scan to network folder
        @param spice: 
        """
        self.goto_menu_scan(spice)
        scan_to_usb_button = spice.wait_for(MenuAppWorkflowObjectIds.button_menu_scan_scan_to_folder)
        scan_to_usb_button.mouse_click()
        folderLandingView = spice.wait_for(MenuAppWorkflowObjectIds.view_folder_screen + " #SpiceBreadcrumb", timeout = 10)
        spice.wait_until(lambda: folderLandingView["visible"]==True, timeout = 25)
        time.sleep(3)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_folder_screen)
        logging.info("At Menu Scan Screen")

    def goto_menu_scan_scan_to_email(self, spice):
        """
        Menu app-> Scan -> Scan to email
        @param spice: 
        """
        self.goto_menu_scan(spice)
        scan_to_email_btn = spice.query_item(MenuAppWorkflowObjectIds.scan_to_email_button + " MouseArea")
        spice.validate_button(scan_to_email_btn)
        scan_to_email_btn.mouse_click()
        email_landing_view = spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view)
        spice.wait_until(lambda: email_landing_view["visible"] == True)
    
    def click_on_input_selection_continue_button(self, spice):
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
        continue_button.mouse_click()
        
    def click_on_input_selection_cancel_button(self, spice):
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_cancel_button)
        cancel_button.mouse_click()
        
    def goto_menu_settings_general_region(self, spice, signInRequired=True):
        self.goto_menu_settings_general(spice, signInRequired=signInRequired)
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
    
    # Menu Settings Energy Sleep 30 minutes. 

    def set_energysleep_thirtyminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        #self.menu_navigation(spice, "#EnergySleepValuelist1", MenuAppWorkflowObjectIds.energy_sleep_30mins, scrollbar_objectname = "#EnergySleepValuelist1ScrollBar")
        self.workflow_common_operations.scroll_to_position_vertical(.3, "#comboBoxScrollBar")
        thirtyMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_30mins)
        thirtyMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 30 minutes")
        time.sleep(1) 

    # Display IRIS Message and radio button

    def goto_menu_settings_printerUpdate_autoUpdateOptions(self, spice):
        self.goto_menu_settings(spice)
        firmware_update = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate)
        firmware_update.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        self.menu_navigation(spice,MenuAppWorkflowObjectIds.view_printerUpdate,MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions,scrollbar_objectname = "#printerUpdateViewScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris)
        logging.info("At Printer Update IRIS Message Screen")

    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.8, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.8, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")
    
    def launch_nozzle_health(self, spice, input_selection_screen=True):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_nozzle_health)
        current_button.mouse_click()
        if input_selection_screen:
            logging.info("Wait for input selection screen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

    def goto_menu_quickSets(self, spice, quickset_type=None):
        """
        Flow -> Home -> Menu -> Quickset item -> Sepecific quickset
        quickset_type:
        1. copy -> Copy
        2. scanToEmail -> Scan to Email
        3. scanToFolder -> Network Folder
        4. scanToSharePoint -> SharePoint
        5. scanToUSB -> Scan to USB
        """
        self.goto_menu(spice)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.quick_set_button , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.utilities_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.utilities_section_bottom_border)
        time.sleep(1)
        spice.query_item(MenuAppWorkflowObjectIds.quick_set_button + " SpiceText[visible=true]").mouse_click()
        #need to wait all quickset display
        time.sleep(2)
        try:
            if quickset_type:
                spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)
                if quickset_type == 'copy':
                    quickset_type = 'copyList'
                elif quickset_type == 'scanToSharePoint':
                    self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)
                    time.sleep(1)

                item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}")
                #SpiceView"
                item.mouse_click()
            else:
                assert spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
        except Exception:
            raise Exception(f"Failed to find item for quickset type: <{quickset_type}>")

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

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        coldResetPaperComboboxObj = "#SettingsComboBox #SettingsSpiceComboBox"
        self.menu_navigation(spice, screen_id = MenuAppWorkflowObjectIds.view_system_configuration, menu_item_id = coldResetPaperComboboxObj, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaper(self, spice, udw):
        coldResetMediaSize_option_A4 = "#coldResetMediaComboA4"
        coldResetMediaSize_option_Letter = "#coldResetMediaComboLetter"   

        self.goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(spice, udw)
        logging.info("At Cold Reset Paper Screen")

        #select opposite media size
        if spice.query_item(coldResetMediaSize_option_Letter)["selected"] is True:
            coldResetMediaSize_original_option = coldResetMediaSize_option_Letter
            current_button = spice.query_item(coldResetMediaSize_option_A4)
            logging.info("Original is Letter and A4 selected and reboot now")
        else:
            coldResetMediaSize_original_option = coldResetMediaSize_option_A4
            current_button = spice.query_item(coldResetMediaSize_option_Letter)
            logging.info("Original is A4 and Letter selected and reboot now")
        assert current_button
        current_button.mouse_click()

        #Wait for homescreen view after 1st reboot
        time.sleep(120)
        self.goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(spice, udw)

        #Check the cold reset paper is changed.
        if spice.query_item(coldResetMediaSize_option_A4)["selected"] is True:
            if(coldResetMediaSize_original_option == coldResetMediaSize_option_A4):
                logging.info("Check: A4 selected : Fail revert original")
            current_button = spice.query_item(coldResetMediaSize_option_Letter)
        else:
            if(coldResetMediaSize_original_option == coldResetMediaSize_option_Letter):
                logging.info("Check: Letter selected : Fail revert original")
            current_button = spice.query_item(coldResetMediaSize_option_A4)
        assert current_button
        current_button.mouse_click()

        #Wait for homescreen view after 2nd reboot for next test
        time.sleep(120)
        self.goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(spice, udw)

        #Check the cold reset paper is the same as the original option.
        if spice.query_item(coldResetMediaSize_option_A4)["selected"] is True:
            if(coldResetMediaSize_original_option != coldResetMediaSize_option_A4):
                logging.info("Check: Original option is not A4 : Fail")
        else:
            if(coldResetMediaSize_original_option != coldResetMediaSize_option_Letter):
                logging.info("Check: Original option is not Letter : Fail")
        logging.info("Cold Reset Paper test ends.")
        spice.wait_for("#HomeScreenView")

    def goto_menu_tools_servicemenu_faxdiagnostics_ringSettings(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_ringsettings, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_ringsettings)
        currentElement.mouse_click()
        # self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_ringsettings, MenuAppWorkflowObjectIds.view_service_faxdiagnostics, update object id of scrollbar)
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_ringsettings)
        logging.info("At RingSettings Screen")
    
    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt)
        else:
            currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxmenudiagnostics)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxregulatorytest)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics, timeout=15)
        logging.info("At Tools -> Service -> Diagnostics ->Fax ->Fax Regulatory Test Screen")
    
    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        time.sleep(1)
        # currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_randomdata)
        # time.sleep(1)
        # currentElement.mouse_click()
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_randomdata, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_randomdata, timeout=15)
        current_button.mouse_click()
        time.sleep(2)
        # assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata)    #not working in Large screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,timeout=15)
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen") 

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_generatedialingtonespulses(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_dialingtones, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = True,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        logging.info("At Generate Dial Tone Pulses Screen")

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics, timeout=15)
        # Scroll up to make Hook Operations Button visible
        # scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        # scrollbar.__setitem__("position",0)
        # # Query Hook Operations
        # time.sleep(2)
        # currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_hookoperations)
        # currentElement.mouse_click()
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_hookoperations, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = True,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(5)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_hookoperations,timeout=15)
        logging.info("At Hook Operations View")               
    
    def goto_menu_tools_servicemenu_faxdiagnostics_generatesinglemodemtonemenu(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_singlemodemtone, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_singlemodemtone)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_singlemodemtone)
    
    def goto_menu_tools_servicemenu_faxdiagnostics_showallfaxlocations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_showalllocations, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_showalllocations)
        time.sleep(2)
        logging.info("At Tools -> Service -> Fax show ALl Location")

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            return False 