
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflow2UICommonOperations import MenuAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations


class MenuAppWorkflow2UIXLOperations(MenuAppWorkflow2UICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.workflow_common_operations = Workflow2UICommonOperations(spice)
        self.MenuAppWorkflowUIXLObjectIds = MenuAppWorkflowObjectIds()
        self.MenuAppWorkflowUIXLObjectIds.menu_button_settings = "#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuApp"
        self.MenuAppWorkflowUIXLObjectIds.view_menulistLandingpage = "#landingPageMenuAppList"
        self.MenuAppWorkflowUIXLObjectIds.view_menuTools = "#toolsMenuAppList"
        self.MenuAppWorkflowUIXLObjectIds.view_menuSettings = "#settingsMenuListListView"
        self.MenuAppWorkflowUIXLObjectIds.menu_button_tools = "#toolsMenuApp"
        self.MenuAppWorkflowUIXLObjectIds.menu_button_tools_maintenance = "#9da37e46-9b8a-4dc2-a24c-017fee6b088fMenuApp"

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

    def goto_menu_settings_output_destinations_folder(self, spice):
        #self.goto_menu_settings(spice)
        output_destinations_folder = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations_folder + " MouseArea")
        output_destinations_folder.mouse_click()
        logging.info("At Folder Settings Screen")

    def goto_menu_settings_output_destinations_folder_custom_folding_styles(self, spice):
        #self.goto_menu_settings(spice)
        output_destinations_folder_custom_folding_styles = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations_folder_custom_folding_styles + " MouseArea")
        output_destinations_folder_custom_folding_styles.mouse_click()
        logging.info("At Custom Folding Styles Settings Screen")

    def set_energysleep_fifteenminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        fifteenMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_15mins)
        fifteenMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 15 minutes")
        time.sleep(1)
    
    def set_energysleep_thirtyminutes(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        thirtyMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_30mins)
        thirtyMinutesButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 30 minutes")
        time.sleep(1)
    
    def set_energysleep_onehour(self, spice):
        self.goto_menu_settings_general_energy_sleep(spice)
        oneHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_1hour)
        oneHourButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Sleep to 1 hour")
        time.sleep(1)

    def set_energyshutdown_fourhours(self, spice):
        self.goto_menu_settings_general_energy_shutdown(spice)
        fourHourButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_shutdown_4hours)
        fourHourButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("Set Energy Shutdown to 4 hours")
        time.sleep(1)

    def goto_menu_fax(self, spice):
        logging.info("fax menuApp isnt available in jupiter")
        #empty function to avoid executing the same function in CommonOperations.

    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)

        # Click on Proceed Button
        proceedButton = spice.query_item("#SpiceView SpiceView SpiceText[visible=true]", 0)
        assert proceedButton["text"] == "Proceed", "Could not find Proceed Button"
        proceedButton.mouse_click()
    
        status_center_service_stack_view = spice.check_item(MenuAppWorkflowObjectIds.view_troubleshooting)
        if status_center_service_stack_view != None:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_menu_list)
        logging.info("At Troubleshooting Screen")
    
    def start_scanner_calibration(self, spice, scan_action, udw,net, locale, last_view, last_object, cancel_action:bool=False, skip_action:bool=True):
        """
        Executes the calibration process.
        Parameters:
        - spice: Spice fixture.
        - scan_action: The instance of the ScanAction used for scan actions.
        - udw: The UDW fixture.
        - cancel_action: A boolean indicating whether to cancel the calibration process. Default is False.
        - skip_action: A boolean indicating whether to skip the scan process. Default is True.
        """
        spice.homeMenuUI().goto_menu_tools_maintenance(spice)
        scan_tab_button = spice.wait_for(MenuAppWorkflowObjectIds.view_maintenance_userMaintenance_button)
        scan_tab_button.mouse_click()
        assert spice.wait_for("#SettingsButton")

        scanner_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.enter_calibration_button)
        scanner_calibration_button.mouse_click()

        start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.start_calibration_button)
        start_calibration_button.mouse_click()

        scan_service = spice.wait_for("#ScanService")

        isMDF = "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower()

        # Checks if there is a page loaded
        if  isMDF and not scan_action.is_media_loaded("MDF"):
            assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_load_sheet_view)
            Control.validate_result(scan_action.load_media("MDF"))

        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_in_progress_view)

        if cancel_action:
            # Cancel the calibration.
            spice.main_app.wait_locator_visible(MenuAppWorkflowObjectIds.calibration_in_progress_cancel_button)
            start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_in_progress_cancel_button)
            # Calibration takes a bit to start and enable the cancelling.
            spice.wait_until(lambda: start_calibration_button["enabled"] == True, 20)
            start_calibration_button.mouse_click()

            # Wait for the cancel dialog to appear and confirm.
            assert spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_dialog)
            start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_dialog_confirm_button)
            start_calibration_button.mouse_click()
        else:
            spice.wait_for(last_view, 20)

        last_button = spice.wait_for(last_object)
        last_button.mouse_click()


    def start_color_calibration(self, spice, input_selection_screen = True ):
        
        self.start_calibration(spice, MenuAppWorkflowObjectIds.color_calibration)
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
        self.goto_printheads_cleaning(spice)
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view)
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()
    
    def start_full_calibration(self, spice, allowed_calibrations, input_selection_screen=True):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.full_calibration)
        
        # Validate allowed calibrations for the currently loaded media
        for calibration in allowed_calibrations:
            spice.wait_for(calibration)
        
        if input_selection_screen:
            logging.info("Wait for input selection screen")
            # Select roll on input selection screen
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()
                
        # Click on "Continue" button
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.full_calibration_continue_button)
        continue_button.mouse_click()
    
    def start_calibration(self, spice, calibration):
        align_button = spice.wait_for(calibration + " MouseArea", timeout = 10)
        align_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view)
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        self.workflow_common_operations.goto_menu_app_floating_dock(spice)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_mediaApp, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage, MenuAppWorkflowObjectIds.utilities_column_name, MenuAppWorkflowObjectIds.landingPage_Content_Item, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)
    
    def click_on_input_selection_continue_button(self, spice):
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
        continue_button.mouse_click()
    
    def click_on_input_selection_cancel_button(self, spice):
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_cancel_button)
        cancel_button.mouse_click()

    def goto_calibration(self, spice, calibration, index = ""):

        align_button = spice.wait_for(calibration + " #printCardContent")
        align_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view)

    def goto_menu_settings_printerUpdate(self, spice):
        self.goto_menu_settings(spice)
        firmware_update = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate)
        firmware_update.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("At Printer Update WF Screen")
    
    def goto_menu_settings_printerUpdate_autoUpdateOptions(self, spice):
        self.goto_menu_settings(spice)
        firmware_update = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate)
        firmware_update.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        firmware_update_autoupdateoptions = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions)
        firmware_update_autoupdateoptions.mouse_click()
        time.sleep(2)
        # Check if Sign-in screen exists
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except:
            logging.info("No Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
            time.sleep(5)
        finally:
            logging.info("At Printer Update IRIS Message Screen")

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris)
    
    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def set_printerUpdate_allowAutoUpdate_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        autoUpdateButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate)
        autoUpdateButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")
        time.sleep(1)

    def set_printerUpdate_notifyWhenAvailable_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        notifyButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable)
        notifyButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1)

    def set_printerUpdate_doNotCheck_navigation(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(spice)
        donotcheckButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotCheck)
        donotcheckButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set DoNot Check to true")
        time.sleep(1)

    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        settingsButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        settingsButton.mouse_click()
        settingsButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable + " MouseArea")
        settingsButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set userConfirmationEnabled to true")
        time.sleep(1) 

    def launch_nozzle_health(self, spice, input_selection_screen=True):
        self.goto_menu_tools_troubleshooting_more_options(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_more_options_nozzle_health, timeout = 10)
        current_button.mouse_click()
        if input_selection_screen:
            logging.info("Wait for input selection screen")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

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

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            return False