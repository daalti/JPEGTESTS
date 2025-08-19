
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflow2UICommonOperations import MenuAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.configuration import Configuration
class MenuAppWorkflow2UILOperations(MenuAppWorkflow2UICommonOperations):

    def __init__(self, spice):        
        super().__init__(spice)
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = Workflow2UICommonOperations(spice)
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

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_print_calibration)
        calibration.mouse_click()
        color_calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_color_calibration)
        color_calibration.mouse_click()

    def goto_menu_settings_print_printquality(self, spice):
        self.goto_menu_settings_print(spice)
        printquality_button= spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_printquality, 2)
        printquality_button.mouse_click()
        logging.info("At Print Quality Screen")
        
    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)

        # Click on Proceed Button
        proceedButton = spice.query_item("#SpiceView SpiceView SpiceText[visible=true]", 0)
        assert proceedButton["text"] == "Proceed", "Could not find Proceed Button"
        proceedButton.mouse_click()

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

    def set_inactivitytimeout_fiveminutes(self, spice):
        isEnterPriseProduct = self.goto_menu_settings_general_inactivitytimeout(spice)
        if isEnterPriseProduct:
            self.setInactivityTimeoutForEnterprise(spice,300)
        else:
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_inactivity_timeout_settings, MenuAppWorkflowObjectIds.inactivity_timeout_5mins)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("Set Inactivity Timeout to 5 mins")
        time.sleep(1)

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        self.workflow_common_operations.goto_menu_app_floating_dock(spice)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_mediaApp, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage, MenuAppWorkflowObjectIds.utilities_column_name, MenuAppWorkflowObjectIds.landingPage_Content_Item, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)

        logging.info("Go to menu app from floating dock")

        # Validate for object if not exist
        object = spice.wait_for(MenuAppWorkflowObjectIds.menu_app_button_floating_dock)

        # Wait for clickable situation
        spice.wait_until(lambda: object["enabled"] == True, 15)
        spice.wait_until(lambda: object["visible"] == True, 15)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)

    def click_on_input_selection_continue_button(self, spice):
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
        continue_button.mouse_click()
        
    def click_on_input_selection_cancel_button(self, spice):
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_cancel_button)
        cancel_button.mouse_click()
        
    def goto_menu_settings_general_region(self, spice, signInRequired=True):
        self.goto_menu_settings_general(spice, signInRequired=signInRequired)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_region_wf , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general)
        login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
        restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
        if login_view and login_view["visible"]:
            logging.info("Login view is displayed as expected")
            current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
            current_button.mouse_click()
        elif restricted_view and restricted_view["visible"]:
                logging.info("Restricted view is displayed as expected")
                current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
                current_button.mouse_click()
        else:
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
    
    def set_printerUpdate_doNotCheck_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        donotcheckButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotCheck)
        donotcheckButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set DoNot Check to true")
        time.sleep(1)
    
    def set_printerUpdate_allowAutoUpdate_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        autoUpdateButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate)
        autoUpdateButton.mouse_click()
        saveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save)
        saveButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        self.match_privacy_notice_content(spice,True)
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_ok)
        ok_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")
        time.sleep(1)

    def set_printerUpdate_notifyWhenAvailable_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        notifyButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable)
        notifyButton.mouse_click()
        saveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save)
        saveButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        self.match_privacy_notice_content(spice,False)
        ok_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_ok)
        ok_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)
    
    def launch_nozzle_health(self, spice, input_selection_screen=True):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_nozzle_health)
        current_button.mouse_click()
        if input_selection_screen:
            logging.info("Wait for input selection screen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

    def goto_menu(self, spice):
        self.homeApp_workflow2_common_operations.goto_home_menu()
        print("At Menu App")

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
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
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
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_randomdata)
        currentElement.mouse_click()
        # assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata)    #not working in Large screen
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,timeout=20)
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen")

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_generatedialingtonespulses(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_dialingtones, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False,
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_dialingtones)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView,timeout=20)
        logging.info("At Generate Dial Tone Pulses Screen")

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
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
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_hookoperations)
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