
import logging
import time
from datetime import datetime
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from selenium.common.exceptions import TimeoutException



class MenuAppWorkflowUIXLOperations(MenuAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUIXLObjectIds = MenuAppWorkflowObjectIds()
        self.MenuAppWorkflowUIXLObjectIds.menu_button_settings = "#3dfe6950-5cf9-41c2-a3b2-6154868ab45dMenuApp"
        self.MenuAppWorkflowUIXLObjectIds.view_menulistLandingpage = "#landingPageMenuAppList"
        self.MenuAppWorkflowUIXLObjectIds.view_menuTools = "#toolsMenuAppList"
        self.MenuAppWorkflowUIXLObjectIds.view_menuSettings = "#settingsMenuListListView"
        self.MenuAppWorkflowUIXLObjectIds.menu_button_tools = "#toolsMenuApp"
        self.MenuAppWorkflowUIXLObjectIds.menu_button_tools_maintenance = "#9da37e46-9b8a-4dc2-a24c-017fee6b088fMenuApp"

    def goto_menu_settings(self, spice, signInRequired = True):
        self.goto_menu(spice)
        settingsButton = spice.wait_for(self.MenuAppWorkflowUIXLObjectIds.menu_button_settings + " MouseArea")
        settingsButton.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        logging.info("At Settings Screen")

    def goto_menu_settings_output_destinations(self, spice):
        self.goto_menu_settings(spice)
        #Sleep added to avoid misclicking the correct menu entry due to a flickering in the Settigns menu list, seen in 2-DuneHeadHead execution since Kernel update to 6.1. DUNE-225846
        time.sleep(5)
        output_destinations = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations + " MouseArea")
        if not output_destinations["visible"] or not output_destinations["enabled"]:
            spice.wait_until(lambda: output_destinations["visible"] == True and output_destinations["enabled"] == True)
        output_destinations.mouse_click()
        logging.info("At Output Destinations Settings Screen")

    def click_on_horizontal_cutter(self, spice):
        self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button, MenuAppWorkflowObjectIds.view_menu_settings_output_destinations)
        horizontal_cutter_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button)
        time.sleep(2)
        logging.info("Horizontal cutter switch status: {}".format(horizontal_cutter_switch_button["checked"]))

    def goto_menu_settings_output_destinations_folder(self, spice):
        #self.goto_menu_settings(spice)
        output_destinations_folder = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations_folder + " MouseArea", 30)
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
        try:
            self.goto_menu_settings_general_energy_sleep(spice)
            self.workflow_common_operations.scroll_to_position_vertical(.3, "#comboBoxScrollBar")
            thirtyMinutesButton = spice.wait_for(MenuAppWorkflowObjectIds.energy_sleep_30mins)
            thirtyMinutesButton.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
            logging.info("Set Energy Sleep to 30 minutes")
        except Exception as e:
            logging.info(f"Failed to set Energy Sleep to 30 minutes: {e}")
            return  #Exit
        finally:
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

    # Menu Settings General Energy prevent Shutdown

    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        assert spice.wait_for("#energycheckbox #CheckBoxView")
        logging.info("Set Energy prevent Shutdown to when ports are active")
        return spice.query_item("#energycheckbox #CheckBoxView")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        logging.info("Set Energy prevent Shutdown to none(do not disable)")
        time.sleep(1)

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        logging.info("Set Energy prevent Shutdown to when ports are active")
        time.sleep(1)

    def goto_menu_tools(self, spice):
        self.goto_menu(spice)

        toolsButton = spice.wait_for(self.MenuAppWorkflowUIXLObjectIds.menu_button_tools + " MouseArea")
        toolsButton.mouse_click()

        assert spice.wait_for(self.MenuAppWorkflowUIXLObjectIds.view_menuTools)
        logging.info("At Tools Screen")

    def goto_menu_tools_maintenance(self,spice):
        self.goto_menu_tools(spice)
        maintenanceButton = spice.wait_for(self.MenuAppWorkflowUIXLObjectIds.menu_button_tools_maintenance + " MouseArea")
        maintenanceButton.mouse_click()

        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings)
        logging.info("At Maintenance Screen")

    def goto_menu_fax(self, spice):
        logging.info("fax menuApp isnt available in jupiter")
        #empty function to avoid executing the same function in CommonOperations.

    def perform_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets_factorydatareset(spice, udw)

        # Click on Proceed Button
        proceedButton = spice.query_item("#SpiceView SpiceView SpiceText[visible=true]", 0)
        assert proceedButton["text"] == "Proceed", "Could not find Proceed Button"
        proceedButton.mouse_click()

    def goto_menu_tools_troubleshooting(self, spice):
        self.goto_menu_tools(spice)
        time.sleep(1)
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

        if input_selection_screen:
            logging.info("Wait for input selection screen")
            # Select roll on input selection screen
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()

        # Validate allowed calibrations for the currently loaded media
        for calibration in allowed_calibrations:
            spice.wait_for(calibration)

        # Click on "Continue" button
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.full_calibration_continue_button)
        continue_button.mouse_click()

    def start_media_advance_calibration(self, spice, cal_mode = "auto", multi_inputs = True):

        "Starts a media advance calibration in the specified mode.(auto/manual)."

        logging.info("Starting Media Advance Calibration - CalType : {0}".format(cal_mode))
        advance_cal = spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_calibration_option, timeout = 15)
        advance_cal.mouse_click()

        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view, 10)
        # Sleep for 1 second to allow the calibration cards to load
        time.sleep(1)
        card_1 = spice.query_item(MenuAppWorkflowObjectIds.paper_advance_calibration_card,0)
        card_2 = spice.query_item(MenuAppWorkflowObjectIds.paper_advance_calibration_card,1)
        card_1_cal_type = int(card_1["calibrationType"])
        card_2_cal_type = int(card_2["calibrationType"])

        if  card_1_cal_type == 32 and card_2_cal_type == 62:
                manual_advance = card_1
                automatic_advance = card_2
        elif card_1_cal_type == 62 and card_2_cal_type == 32:
                manual_advance = card_2
                automatic_advance = card_1
        else :
            assert False , "No Media Advance Calibration Type found"

        if cal_mode == "manual":
                logging.info("Starting Manual Advance Calibration")
                manual_advance.mouse_click()
        elif cal_mode == "auto":
                logging.info("Starting Automatic Advance Calibration")
                automatic_advance.mouse_click()
        else:
            assert False, "Invalid Calibration Mode"

        #Start Calibration
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button,timeout=10)
        start_button.mouse_click()
        if multi_inputs :
            print("Waiting for Source Input Selection Screen")
            #Select source Roll & Continue
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            spice.homeMenuUI().click_on_input_selection_continue_button(spice)

    def start_calibration(self, spice, calibration):
        align_button = spice.wait_for(calibration + " MouseArea", timeout = 10)
        align_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view,timeout = 10)
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
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
        #grid 2x2, 5 elements
        if calibration == MenuAppWorkflowObjectIds.full_calibration: # element number 5
            spice.wait_for(MenuAppWorkflowObjectIds.calibration_scrollbar)
            spice.basic_common_operations.scroll_to_position_vertical(1, MenuAppWorkflowObjectIds.calibration_scrollbar)
            #After moving the scroll, it seems a 1-second sleep is necessary, since, without the timer, sometimes the mouse_click() doesn't have an effect
        time.sleep(1)
        align_button = spice.wait_for(calibration + " #printCardContent")
        #wait for clickable situation
        if not align_button["visible"] or not align_button["enabled"]:
            spice.wait_until(lambda: align_button["visible"] == True and align_button["enabled"] == True)
        align_button.mouse_click()
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

    def menu_settings_General_Datetime_SystemtimeChange (self, spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        try:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        
            logging.info("At Time Settings Screen")
            #Setting the Hour to 9
            try:
                spice.wait_for("#Hour #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At spinbox keyboard")
                    spice.wait_for("#key9PositiveIntegerKeypad").mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
                    pass
            except Exception as e:
                print(f"An unexpected error occurred hour not found: {e}")
                pass
                
            #Setting the Minutes to 0
            try:
                spice.wait_for("#Minute #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At the spinbox keyboard")
                    spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
                    pass
            except Exception as e:
                print(f"An unexpected error occurred minute not found: {e}")
                pass
            try:
                applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
                applyButton.mouse_click()
            except Exception as e:
                print(f"An unexpected error occurred minute not found: {e}")
                pass
        except AssertionError:
            logging.info("Could not find the keyboard view")
            spice.goto_homescreen()
        finally:
            spice.goto_homescreen()
            
    def energy_scheduleOff_set_time_day_after_schedule(self, spice, cdm, net):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOff_2infoBlockRow #contentItem")["text"]
            if schedule_set_not != "Not Set":
                print("Schedule is already set")
                spice.goto_homescreen()
                return
            
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
            if not spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen):
                logging.info("Failed to find the schedule off screen")
                spice.goto_homescreen()
                return

            steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView, "Failed to select days option"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday, "Failed to select Sunday"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_nextButton, "Failed to click next button"),
                (MenuAppWorkflowObjectIds.view_energySettings_scheduleOnHoursView, "Failed to set hour"),
            ]

            for step, error_message in steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.info(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return

            # Setting the Hour to 10
            try:
                spice.wait_for("#timeSettingsListView #Hour #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At spinbox keyboard")
                spice.wait_for("#key1PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()
            except Exception as e:
                logging.info(f"Failed to set hour to 10: {e}")
                spice.goto_homescreen()
                return

            # Setting the Minute to 0
            try:
                spice.wait_for("#timeSettingsListView #Minute #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At the spinbox keyboard")
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()
            except Exception as e:
                logging.info(f"Failed to set minute to 0: {e}")
                spice.goto_homescreen()
                return

            final_steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_doneButton, "Failed to click done button"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_saveButton, "Failed to click save button"),
            ]

            for step, error_message in final_steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.info(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return
        
            self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)
            self.menu_settings_General_Datetime_SystemtimeChange_10Hr03min(spice, net)

            clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
            clock_data = clock.json()
            print("CDM Value After SystemTime change = ", clock_data)
            system_time = clock_data['systemTime']
            time_part = system_time.split('T')[1]
            hour_minute = time_part.split(':')[0:2]
            updated_System_time = ":".join(hour_minute)
            assert updated_System_time == "10:03", f"Expected '10:03' but got {updated_System_time}"
            print(updated_System_time)
        except Exception as e:
            logging.info(f"Failed to verify schedule off {e}")
            return

    def energy_scheduleOff_set_time_day_before_schedule(self, spice, cdm, net):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        try:
            schedule_set_not = spice.wait_for("#SchOff_2infoBlockRow #contentItem")["text"]
            if schedule_set_not != "Not Set":
                print("Schedule is already set")
                spice.goto_homescreen()
                return
            
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
            if not spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen):
                logging.info("Failed to find the schedule off screen")
                spice.goto_homescreen()
                return

            steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView, "Failed to select days option"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday, "Failed to select Sunday"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_nextButton, "Failed to click next button"),
                (MenuAppWorkflowObjectIds.view_energySettings_scheduleOnHoursView, "Failed to set hour"),
            ]

            for step, error_message in steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.info(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return

            # Setting the Hour to 10
            try:
                spice.wait_for("#timeSettingsListView #Hour #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At spinbox keyboard")
                spice.wait_for("#key1PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()
            except Exception as e:
                logging.info(f"Failed to set hour to 10: {e}")
                spice.goto_homescreen()
                return

            # Setting the Minute to 0
            try:
                spice.wait_for("#timeSettingsListView #Minute #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At the spinbox keyboard")
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()
            except Exception as e:
                logging.info(f"Failed to set minute to 0: {e}")
                spice.goto_homescreen()
                return

            final_steps = [
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_doneButton, "Failed to click done button"),
                (MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_saveButton, "Failed to click save button"),
            ]

            for step, error_message in final_steps:
                try:
                    element = spice.wait_for(step)
                    element.mouse_click()
                except Exception as e:
                    logging.info(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return
                
            self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)
            self.menu_settings_General_Datetime_SystemtimeChange_9Hr57min(spice, net)

            clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
            clock_data = clock.json()
            print("CDM Value Before SystemTime change = ", clock_data)
            system_time = clock_data['systemTime']
            time_part = system_time.split('T')[1]
            hour_minute = time_part.split(':')[0:2]
            updated_System_time = ":".join(hour_minute)
            assert updated_System_time == "09:57", f"Expected '09:57' but got {updated_System_time}"
            print(updated_System_time)
        except Exception as e:
            logging.info(f"Failed to verify schedule off {e}")
            return

    def menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(self, spice, cdm):
        try:
            systemtime_cdm = cdm.get(cdm.CLOCK_CONFIGURATION)
            print("systemtime_cdm before is = ", systemtime_cdm)

            systemTime = cdm.get(cdm.CLOCK_CONFIGURATION)["systemTime"]
            print("dayName = ", systemTime)

            # Replacing "T" and "Z" with spaces
            s = systemTime.replace("T", " ").replace("Z", " ")
            print("s =", s)

            # Replacing the first two occurrences of "-" with "/"
            date = s.replace("-", "/", 2)
            print("date =", date)

            new_string = date.rstrip()
            print("new_string =", new_string)

            # Converting the string to datetime object
            datetime_date = datetime.strptime(new_string, "%Y/%m/%d %H:%M:%S")
            print("datetime_date =", datetime_date)

            # Printing the day of the week
            dayName = datetime_date.strftime("%A").lower()
            print("day =", dayName)

            configuration_endpoint = cdm.POWER_CONFIG
            body = {
                "version": "1.0.0",
                "shutdownPrevention": "none",
                "powerOffScheduleEnabled": "true",
                "powerOffSchedule": [
                    {
                        "scheduleId": 0,
                        "timesOfDay": [
                            {
                                "hourOffset": 10,
                                "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            dayName
                        ]
                    }
                ]
            }

            if dayName in ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
                try:
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ", r.json())
                except Exception as e:
                    logging.info(f"Failed to update power off schedule: {e}")
            else:
                logging.info("None of the Days selected")

        except Exception as e:
            logging.info(f"An error occurred: {e}")

    def menu_settings_General_Datetime_SystemtimeChange_9Hr57min(self, spice, net):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        
        try:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
            logging.info("At Time Settings Screen")

            # SystemTime Setting the Hour to 9
            try:
                spice.wait_for("#Hour #SpinBoxTextFieldMouseArea").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info("Failed to find the spinbox keyboard")
                logging.info("At spinbox keyboard")
                spice.wait_for("#key9PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()  # click ok button
            except Exception as e:
                logging.info(f"Failed to set hour to 9: {e}")
                spice.goto_homescreen()
                return

            # SystemTime Setting the Minutes to 57
            try:
                spice.wait_for("#Minute #SpinBoxTextFieldMouseArea").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info("Failed to find the spinbox keyboard")
                logging.info("At the spinbox keyboard")
                spice.wait_for("#key5PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#key7PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()  # click ok button
            except Exception as e:
                logging.info(f"Failed to set minutes to 57: {e}")
                spice.goto_homescreen()
                return

            try:
                applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
                applyButton.mouse_click()
            except Exception as e:
                logging.info(f"Failed to click apply button: {e}")
                spice.goto_homescreen()
                return

        except AssertionError:
            logging.info("Could not find the dateTime time view")
            spice.goto_homescreen()
        except Exception as e:
            logging.info(f"An unexpected error occurred: {e}")
            spice.goto_homescreen()
        finally:
            spice.goto_homescreen()

    def menu_settings_General_Datetime_SystemtimeChange_10Hr03min(self, spice, net):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        try:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
            logging.info("At Time Settings Screen")

            # SystemTime Setting the Hour to 10
            try:
                spice.wait_for("#Hour #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info("Failed to find the spinbox keyboard")
                logging.info("At spinbox keyboard")
                spice.wait_for("#key1PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()  # click ok button
            except Exception as e:
                logging.info(f"Failed to set hour to 10: {e}")
                spice.goto_homescreen()
                return

            # SystemTime Setting the Minutes to 03
            try:
                spice.wait_for("#Minute #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info("Failed to find the spinbox keyboard")
                logging.info("At the spinbox keyboard")
                spice.wait_for("#key0PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#key3PositiveIntegerKeypad").mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()  # click ok button
            except Exception as e:
                logging.info(f"Failed to set minutes to 03: {e}")
                spice.goto_homescreen()
                return

            try:
                applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
                applyButton.mouse_click()
            except Exception as e:
                logging.info(f"Failed to click apply button: {e}")
                spice.goto_homescreen()
                return

        except Exception as e:
            logging.info(f"An unexpected error occurred: {e}")
            spice.goto_homescreen()
        finally:
            spice.goto_homescreen()

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            return False
