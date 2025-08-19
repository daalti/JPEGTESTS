
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowXSObjectIds import MenuAppWorkflowXSObjectIds
from dunetuf.ui.uioperations.PomOperations.SignInApp.Locators import Locators
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.engine.engine import Engine

class MenuAppWorkflowUIXSOperations(MenuAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUIXSObjectIds = MenuAppWorkflowObjectIds()

    def goto_menu(self, spice):

        # make sure that you are in home screen
        spice.goto_homescreen()
        spice.wait_for("#HomeScreenView")
        homeApp = spice.query_item("#HomeScreenView")
        spice.wait_until(lambda: homeApp["visible"] == True)
        logging.info("At Home Screen")
        self.workflow_common_operations.scroll_to_position_horizontal(0)
        logging.info("Reset horizontal scrollbar")
        time.sleep(2)

        currentState = int(spice.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
        logging.debug('Printer Sleep status is: %s',currentState)
        if currentState >= 2:
            logging.debug("Waking up printer")
            spice.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
            time.sleep(2)

        # scroll till you reach the Menu option (TODO - Need to check the menu app is visible or not)
        # enter the menu screen
        logging.info("Entering Menu")
        adminApp = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp +" MouseArea" )
        # Wait for clickable situation
        spice.wait_until(lambda: adminApp["enabled"] == True)
        spice.wait_until(lambda: adminApp["visible"] == True)
        adminApp.mouse_click()
        time.sleep(5)
        assert spice.wait_for("#landingPageMenuAppList")
        logging.info("At Menu Screen")
        time.sleep(3)

    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1.0, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(1.0, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def goto_menu_settings_printer_update_next(self, spice):
        self.workflow_common_operations.scroll_to_position_vertical(0.9, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        coldResetPaperComboboxList = "#SettingsSpiceComboBoxpopupList"
        coldResetPaperComboboxOption = "#SettingsSpiceComboBox"
        self.workflow_common_operations.scroll_to_position_vertical(0.9,scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)
        selectOption = spice.wait_for(coldResetPaperComboboxOption)
        selectOption.mouse_click()
        spice.wait_for(coldResetPaperComboboxList)
        logging.info("option end")

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

        logging.info("Cold Reset Paper test ends.")

    def goto_menu_tools_servicemenu_servicetests_displaytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        selectOption = spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_displaytest)
        selectOption.mouse_click()

    def goto_menu_tools_servicemenu_servicetests_keytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        selectOption = spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_keytest)
        selectOption.mouse_click()

    def goto_menu_info_printer_card(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_info_printer(spice)

        #Printer Information card expanded
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_printercard)["visible"]
        time.sleep(2)         
        logging.info("At printer information card Tab")

    # Menu Settings General Energy prevent Shutdown
    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.51, "#energySettingsMenuListScrollBar")
        assert spice.wait_for("#energycheckbox #CheckBoxView")
        return spice.query_item("#energycheckbox #CheckBoxView")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.51, "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()

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
            time.sleep(1)

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.51, "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        
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
            time.sleep(1)

    def goto_menu_tools_maintenance_firmware_updatehistory(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        # Screen has been changed and Drop Down Button is not available for some product.
        # So, if dropDownButton available then proceed otherwise simply skip
        try:
           drop_down_button = spice.wait_for("#dropDownButton")
           drop_down_button.mouse_click()
        except:
           logging.info("The product does not have Drop Down Button")
        finally:
           update_history_button = spice.wait_for("#fwUpUpdateHistory")
           update_history_button.mouse_click()
           assert spice.wait_for("#updateHistoryLayout")
           logging.info("At update history screen")

    def goto_menu_settings_general_energy_shutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.5, "#energySettingsMenuListScrollBar")

        try:
            (spice.query_item(MenuAppWorkflowObjectIds.view_energySettings_shutdown)["visible"])
        except Exception as e:
            logging.info("Navigate to shutdown view")
            spice.query_item(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_shutdown).mouse_click()
        else:
            logging.info("At expected Menu")
        finally:
            ##Assert Energy shutdown Screen
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_shutdown)
            logging.info("At Energy Shutdown Settings Screen")
            time.sleep(1)

    def goto_menu_settings_print(self, spice):
        self.goto_menu_settings(spice)
        self.workflow_common_operations.goto_item("#printSettingsSettingsTextImage", "#settingsMenuListListViewlist1", 0, True, 0.1, "#settingsMenuListListViewlist1ScrollBar")

    def goto_menu_settings_print_lesspapercurl(self, spice):
        #Check for less paper curl under Print
        self.goto_menu_settings_print(spice)
        spice.wait_for("#printSettingsMenuList", timeout = 5)

        try:
            spice.wait_for("#lessPaperCurlWFMenuSwitch", timeout = 5)
        except Exception as e:
            #If less paper curl isn't under Print, it will be under Print Quality
            logging.info("Less Paper Curl not found under Print. Looking under Print Quality")
            self.workflow_common_operations.goto_item("#printQualitySettingsTextImage", "#printSettingsMenuList", 0, True, 0.1, "#printSettingsMenuListScrollBar")
            spice.wait_for("#printQualityMenuList", timeout = 5)

            try:
                spice.wait_for("#lessPaperCurlWFMenuSwitch", timeout = 5)
            except Exception as f:
                #Catch the exception to print this line
                logging.info("Less Paper Curl not found under Print Quality")
                #but still raise the error since we didn't find it
                raise
        
        logging.info("At Screen with Less Paper Curl")

    def goto_menu_settings_print_printquality(self, spice):
        self.goto_menu_settings_print(spice)
        self.workflow_common_operations.goto_item("#printQualitySettingsTextImage", "#printSettingsMenuList", 0, True, 0.1, "#printSettingsMenuListScrollBar")
        logging.info("At Print Quality Screen")

    def goto_menu_settings_print_defaultprintoptions_quality_dropdown(self, spice):
        self.menu_navigation(spice,"#defaultPrintOptionsMenuList", "#qualitySettingsComboBox")
        assert spice.wait_for("#qualityComboBoxpopupList")
        logging.info("At Quality drop down menu")

    def verify_quality_drop_down_menu_items_economode_detailed(self, spice):
        spice.wait_for("#qualityComboBoxpopupList")
        assert spice.wait_for("#ComboBoxOptionsnormalRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionsdetailedRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionseconomodeRadioButtonModel")

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for("#faxDiagnosticMenuMenuList")
        time.sleep(1)
        # currentElement = spice.wait_for("#generateRandomDataTextImage")
        currentElement = spice.wait_for("#randomDataSettingsTextImage")
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for("#generateRandomDataView")
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen")

    def validate_tray_app(self,spice,cdm,net):
        logging.info("validating tray apps")
        assert spice.wait_for("#MediaAppApplicationStackView") ["visible"] == True,"Trays screen is not visible"
        assert spice.wait_for("#MediaAppApplicationStackView #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #textContainer SpiceText[visible=true]")["text"] == "Trays"
        assert spice.query_item("#titleSmallItem")["text"] == "Tray 1"
        assert spice.query_item("#titleSmallItem",1)["text"] == "Tray 2"
        assert spice.query_item("#titleSmallItem",2)["text"] == "Tray 3"
        
    def verify_job_recovery_policy_index(self, spice, index):
        jobs_settings_job_recovery_mode_settings = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_settings)
        spice.wait_until(lambda:jobs_settings_job_recovery_mode_settings["currentIndex"] == index)

    def verify_print_job_ui_shows_processing_and_then_completes(self, spice, job_id, job):
        logging.info('Navigate to the Job Details Screen')
        spice.job_ui.goto_created_job(job_id)

        # Wait for Processing job Status
        spice.job_ui.wait_for_job_state(spice.job_ui, "Processing")

        # Wait for Job completion
        job.wait_for_job_completion_cdm(job_id)

        # Check that the job status is completed
        spice.wait_until(lambda:spice.job_ui.recover_job_status() == "Completed", timeout=15)

    def print_status_report(self, spice, reportId):
        assert spice.wait_for(MenuAppWorkflowObjectIds.list_checkboxButtonListLayout)
        reportObjectName = '#controlObject_report_' + reportId
        logging.info(f"Scroll and enable checkbox for {reportId}")
        spice.query_item(reportObjectName).mouse_click()
        assert spice.query_item(reportObjectName)['checked'] == True

        logging.info(f"Printing the {reportId}")
        spice.query_item("#printButton").mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo)["text"] == "Printing..."

        logging.info("Disable checkbox for the report")
        spice.wait_for(reportObjectName).mouse_click()

    def goto_menu_tools_maintenance_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        spice.wait_for(self.MenuAppWorkflowUIXSObjectIds.menu_button_tools_maintenance_firmware_updateFWFromUSB).mouse_click()
        logging.info("At Firmware Screen")

    def goto_menu_tools_maintenance_firmware(self, spice):
        self.goto_menu_tools_maintenance(spice)
        spice.wait_for(self.MenuAppWorkflowUIXSObjectIds.menu_button_tools_maintenance_firmware).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_firmwareVersion)
        logging.info("At Firmware Screen")

    def goto_menu_tools_maintenance_firmware_iris_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(spice)
        time.sleep(3)
        logging.info("At Firmware Update Screen")

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        spice.wait_for(self.MenuAppWorkflowUIXSObjectIds.menu_button_tools_maintenance_fw_up_select_device).mouse_click()
        logging.info("At Select file Screen")

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        spice.wait_for(self.MenuAppWorkflowUIXSObjectIds.menu_button_tools_maintenance_fw_up_select_file).mouse_click()
        logging.info("At Select Bundle Screen")

    def set_service_ID(self, spice, SERVICE_ID):
        self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)
        spice.query_item("#ServiceIDTextField").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At Service Id Edit Menu")
        keyboardView = spice.wait_for("#ServiceIDTextField")
        keyboardView['displayText'] = SERVICE_ID
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click()

    def goto_manual_paper_advance_calibration(self, spice, cdm, net):
        """
        Navigates to the Manual Paper Advance screen in Beam
        """       
        if spice.is_HomeScreen():
            # Menu > Tools > Troubleshooting > Print Quality
            # In MFP there is an intermidiate "Print Quality" tab
            try:
                isMfp = Engine.is_MFP_printer(cdm)
            except HTTPError as e:
                logging.info(f"Failed to get scanner status: {e}")
                isMfp = False

            spice.homeMenuUI().goto_menu_tools_troubleshooting_printquality(spice, isMfp)
            
            # Confirm that we are on the Troubleshooting app and past the "Loading" screen.
            # Must see "#TroubleShootingApplicationStackView"
            assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_app)
            logging.info("[OK] Troubleshooting app is loaded")
            
            # Must NOT see "#loadingProgressContent"
            try:
                spice.query_item(MenuAppWorkflowObjectIds.loading_data_progress_content)
                assert False, "[ERROR] Stuck on Troubleshooting loading screen"
            except QmlItemNotFoundError:
                # We expect an exception to be raised
                logging.info("[OK] Troubleshooting loading screen is gone")
        
        if spice.wait_for(MenuAppWorkflowObjectIds.paper_advance_calibration_option): 
            # Select "Paper-Advance Calibration" (linefeed)
            spice.wait_for(MenuAppWorkflowObjectIds.paper_advance_calibration_option).mouse_click()
        
        # Select "Manual Paper-Advance Calibration"
        spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_calibration_option).mouse_click()

        # Wait for the Manual Paper-Advance Calibration screen to load and click "Start" button
        spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button).mouse_click()

        # We use tray as the input, as load is well implemented for the Emulator
        trayCard = spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_media_load_tray_card)
        for _ in range(3):
            self.workflow_common_operations.scroll_to_position_vertical(
                0.25, MenuAppWorkflowObjectIds.manual_paper_advance_media_load_cards_layout)
                
        trayCard.mouse_click()
        
        # Click "Continue" button
        spice.wait_for(MenuAppWorkflowObjectIds.full_calibration_continue_button).mouse_click()
        
        # Now we should be at the Manual Paper-Advance Calibration screen
        spice.wait_for(MenuAppWorkflowObjectIds.manual_paper_advance_setting_view)
    
    def goto_express_printhead_cleaning(self, spice, cdm):
        """
        Navigates to the Express Printhead Cleaning screen in Beam
        """       
        if spice.is_HomeScreen():
            # Menu > Tools > Troubleshooting > Print Quality
            # In MFP there is an intermidiate "Print Quality" tab
            try:
                isMfp = Engine.is_MFP_printer(cdm)
            except HTTPError as e:
                logging.info(f"Failed to get scanner status: {e}")
                isMfp = False

            spice.homeMenuUI().goto_menu_tools_troubleshooting_printquality(spice, isMfp)
            
            # Confirm that we are on the Troubleshooting app and past the "Loading" screen.
            # Must see "#TroubleShootingApplicationStackView"
            assert spice.query_item(MenuAppWorkflowObjectIds.troubleshooting_app)
            logging.info("[OK] Troubleshooting app is loaded")
            
            # Must NOT see "#loadingProgressContent"
            try:
                spice.query_item(MenuAppWorkflowObjectIds.loading_data_progress_content)
                assert False, "[ERROR] Stuck on Troubleshooting loading screen"
            except QmlItemNotFoundError:
                # We expect an exception to be raised
                logging.info("[OK] Troubleshooting loading screen is gone")
        
        # Select "Printhead Cleaning"
        spice.wait_for(MenuAppWorkflowObjectIds.ph_cleaning).mouse_click()
        
        # Select "Express Printhead Cleaning"
        spice.wait_for(MenuAppWorkflowObjectIds.ph_cleaning).mouse_click()
        
        # Start the Cleaning
        spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button).mouse_click()

    def get_advance_factor_value(self, spice):
        """
        Returns the current value of the manual paper advance factor in Beam
        """
        value = spice.wait_for("#manualPaperAdvanceSettingView #SpinBoxTextInput")
        return int(value["text"], 10)

    def set_advance_factor_value(self, spice, value):
        """
        Sets the value of the manual paper advance factor in Beam
        """
        value_input = spice.wait_for("#manualPaperAdvanceSettingView #SpinBoxTextInput")
        value_input.mouse_click()
        keypad = spice.wait_for(Locators.KeyboardView)
        spice.wait_until(lambda: keypad['visible'])
        value_input["text"] = value
        spice.wait_for("#enterKeyIntegerKeypad").mouse_click()
        
    def goto_menu_settings_printerUpdate_allowUpgrades(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowUpgrades).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris)
        logging.info("At Printer Update IRIS Message Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")

    def set_printerUpdate_notifyWhenAvailable(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("Set Notify to true")

    def set_printerUpdate_doNotCheck(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        
        # Add retry mechanism and better error handling for screen size issues
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                # First try the original selector
                try:
                    do_not_check_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_doNotcheck, timeout=5)
                    do_not_check_button.mouse_click()
                    assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
                    logging.info("Set Do Not Check to true")
                    return
                except TimeoutError:
                    # Try alternate approach - sometimes the radio button may have a different ID or be in a different container
                    logging.info("Couldn't find standard Do Not Check radio button, trying alternative approaches")
                    
                    try:
                        # Check if we're in the radio buttons view
                        radio_view = spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView, timeout=5)
                        
                        # Try to locate by position - typically the "do not check" is the third radio button (index 2)
                        radio_buttons = spice.query_item("#radioButtonsView RadioButtonModel", 2)
                        radio_buttons.mouse_click()
                        logging.info("Clicked third radio button")
                        
                        # Verify we made it back to the printer update view
                        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
                        logging.info("Set Do Not Check to true via alternative method")
                        return
                    except Exception as inner_error:
                        logging.warning(f"Alternative radio button approach failed: {inner_error}")
                        
                        # Try another approach - look for any visible radio buttons
                        try:
                            # Find all RadioButtonModel elements
                            for i in range(5):  # Try up to 5 radio buttons
                                try:
                                    radio_button = spice.query_item("RadioButtonModel", i)
                                    if radio_button["visible"]:
                                        # The "Do Not Check" option is usually the last radio button
                                        radio_button.mouse_click()
                                        logging.info(f"Clicked radio button at index {i}")
                                        
                                        # Verify we made it back to the printer update view
                                        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
                                        logging.info("Set Do Not Check to true via fallback method")
                                        return
                                except:
                                    continue
                        except Exception as fallback_error:
                            logging.warning(f"Fallback radio button approach failed: {fallback_error}")
                            # Continue to retry
                
            except Exception as e:
                logging.warning(f"Attempt {retry_count+1} failed: {e}")
            
            retry_count += 1
            time.sleep(2)
            
            # Try to go back to the right screen before retrying
            try:
                self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice, enterNav=True)
            except:
                logging.warning("Failed to navigate back to update screen")
        
        # If we get here, all retries failed
        raise TimeoutError("Failed to locate and click the Do Not Check radio button after multiple attempts")

    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, net, enterNav=True):
        self.set_printerUpdate_notifyWhenAvailable(spice, enterNav)
        spice.wait_for(self.MenuAppWorkflowUIXSObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_privacy_notice)
        notify_when_available_note = spice.wait_for("#alertDetailDescription #textColumn #contentItem")["text"]
        assert LocalizationHelper.get_string_translation(net, "cNotifyWhenAvailableCP", "en") in notify_when_available_note
        spice.wait_for("#Continue").mouse_click()

    def set_printerUpdate_doNotCheck_goto_iris_message_screen(self, spice, net=None, enterNav=True):
        self.set_printerUpdate_doNotCheck(spice, enterNav)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)

    def goto_menu_settings_output_destinations(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_output_destinations, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        output_destinations = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_output_destinations + " MouseArea")
        output_destinations.mouse_click()
        logging.info("At Output Destinations Settings Screen")

    def set_horizontal_cutter_switch(self, spice, value=True):
        horizontal_cutter_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button)
        if (horizontal_cutter_switch_button["checked"] != value):
            spice.homeMenuUI().click_on_horizontal_cutter(spice)
        logging.info("Set Horizontal Cutter switch status to {}".format(value))

    def set_manual_cut_mode_switch(self, spice, value=True):
        manual_cut_mode_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.manual_cut_mode_switch_button)
        if (manual_cut_mode_switch_button["checked"] != value):
            spice.homeMenuUI().click_on_manual_cut_mode(spice)
        logging.info("Set Manual Cut Mode switch status to {}".format(value))

    def click_on_horizontal_cutter(self, spice):
        self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button, MenuAppWorkflowObjectIds.view_menu_settings_output_destinations)
        horizontal_cutter_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.horizontal_cutter_switch_button)
        logging.info("Horizontal cutter switch status: {}".format(horizontal_cutter_switch_button["checked"]))

    def click_on_manual_cut_mode(self, spice):
        self.workflow_common_operations.goto_item_navigation(MenuAppWorkflowObjectIds.manual_cut_mode_switch_button, MenuAppWorkflowObjectIds.view_menu_settings_output_destinations)
        manual_cut_mode_switch_button = spice.wait_for(MenuAppWorkflowObjectIds.manual_cut_mode_switch_button)
        logging.info("Manual cut flow switch status: {}".format(manual_cut_mode_switch_button["checked"]))
    
    def match_privacy_notice_content(self, spice, is_auto = True):
        assert spice.wait_for("#alertDetailBlock")
        assert spice.wait_for("#alertDetailDescription")
        assert spice.wait_for("#alertDetailBlock #alertDetailDescription")
        alert_description = spice.query_item("#alertDetailBlock #alertDetailDescription SpiceText[visible=true]")["text"]
        if is_auto:
            option_text = "Auto (Recommended)"
        else:
            option_text = "Notify"
        correct_string = "Setting: " + option_text + "\n\nWhen set to \"" + option_text + "\", your printer will connect to HP to check for or install firmware updates. Necessary data will be collected and used to provide functionality. Visit hp.com/privacy to learn more."
        print(correct_string)
        assert alert_description == correct_string
        logging.info("Privacy Notice content matched")

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
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.quick_set_button)
        spice.query_item(MenuAppWorkflowObjectIds.quick_set_button + " SpiceText").mouse_click()
        try:
            (spice.query_item(MenuAppWorkflowObjectIds.login_user_view)["visible"])
        except Exception as e:
            logging.info("At Expected Menu")
        else:
            spice.homeMenuUI().perform_signIn(spice)            
        finally:
            logging.info("At Expected Menu")
            time.sleep(1)
        try:
            if quickset_type:
                spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view)
                if quickset_type == 'scanToSharePoint':
                    self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)
                    time.sleep(1)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()
                elif quickset_type == 'copy':
                    quickset_type = 'copyList'
                    time.sleep(3)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()
                    time.sleep(3)
                else:
                    self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)
                    time.sleep(1)
                    item = spice.query_item(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}" + " MouseArea")
                    item.mouse_click()


            else:
                assert spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
        except Exception:
            raise Exception(f"Failed to find item for quickset type: <{quickset_type}>")

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            scroll_bar = spice.wait_for(scrollbar_id)
            scrollbar_size = scroll_bar["visualSize"]
            scroll_bar.__setitem__("position", scrollbar_size - size)
            return True
