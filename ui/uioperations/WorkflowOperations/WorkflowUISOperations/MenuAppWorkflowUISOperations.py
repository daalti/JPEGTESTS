import logging
import time
from datetime import datetime
import re
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from requests.exceptions import HTTPError
from dunetuf.engine.engine import Engine
from dunetuf.configuration import Configuration

positive_integer_key_pad_map = {
    0: "#key0PositiveIntegerKeypad",
    1: "#key1PositiveIntegerKeypad",
    2: "#key2PositiveIntegerKeypad",
    3: "#key3PositiveIntegerKeypad",
    4: "#key4PositiveIntegerKeypad",
    5: "#key5PositiveIntegerKeypad",
    6: "#key6PositiveIntegerKeypad",
    7: "#key7PositiveIntegerKeypad",
    8: "#key8PositiveIntegerKeypad",
    9: "#key9PositiveIntegerKeypad",
}

class MenuAppWorkflowUISOperations(MenuAppWorkflowUICommonOperations):
    def __init__(self, spice):
        super().__init__(spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()

    def goto_menu_settings_printerUpdate(self, spice):
        logging.info("Navigating to Settings Menu")
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate,scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("At Printer Update WF Screen")

    def goto_menu_settings_cloudConnection(self, spice):
        logging.info("Navigating to Settings Menu")
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_cloudConnection, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_cloudConnection)
        logging.info("At HP Cloud Connection Screen")

    def goto_menu_settings_general_display(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display)
        self.workflow_common_operations.scroll_to_position_vertical(0.2, "#displayMenuListScrollBar")

    def goto_menu_settings_general_energy_inactivity_shutdown(self, spice):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_energy)
        self.workflow_common_operations.scroll_to_position_vertical(0.2, "#energySettingsMenuListScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("At Energy Settings Screen")
        time.sleep(1)

    def goto_menu_settings_printerUpdate_allowUpgrades(self, spice, enterNav=True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_allowUpgrades).mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate_iris)
        logging.info("At Printer Update IRIS Message Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        
        # Add retry mechanism and better error handling for screen size issues
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                # First try the original selector
                try:
                    auto_update_button = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate, timeout=5)
                    auto_update_button.mouse_click()
                    assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                    logging.info("Set autoUpdateEnabled to true")
                    return
                except TimeoutError:
                    # Try alternate approach - sometimes the radio button may have a different ID or be in a different container
                    logging.info("Couldn't find standard auto update radio button, trying alternative approaches")
                    
                    try:
                        # Check if we're in the radio buttons view
                        radio_view = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate_iris_radioButtonsView, timeout=5)
                        
                        # Try to locate by position - typically the auto update is the first radio button (index 0)
                        radio_buttons = spice.query_item("#radioButtonsView RadioButtonModel", 0)
                        radio_buttons.mouse_click()
                        logging.info("Clicked first radio button")
                        
                        # Verify we made it back to the printer update view
                        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                        logging.info("Set autoUpdateEnabled to true via alternative method")
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
                                        # The "Auto Update" option is usually the first radio button
                                        radio_button.mouse_click()
                                        logging.info(f"Clicked radio button at index {i}")
                                        
                                        # Verify we made it back to the printer update view
                                        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                                        logging.info("Set autoUpdateEnabled to true via fallback method")
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
        raise TimeoutError("Failed to locate and click the auto update radio button after multiple attempts")
       
    def set_printerUpdate_notifyWhenAvailable(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        
        # Add retry mechanism and better error handling for screen size issues
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                # First try the original selector
                try:
                    notify_when_available_button = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable, timeout=5)
                    notify_when_available_button.mouse_click()
                    assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                    logging.info("Set Notify to true")
                    return
                except TimeoutError:
                    # Try alternate approach - sometimes the radio button may have a different ID or be in a different container
                    logging.info("Couldn't find standard notify radio button, trying alternative approaches")
                    
                    try:
                        # Check if we're in the radio buttons view
                        radio_view = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate_iris_radioButtonsView, timeout=5)
                        
                        # Try to locate by position - typically the notify when available is the second radio button (index 1)
                        radio_buttons = spice.query_item("#radioButtonsView RadioButtonModel", 1)
                        radio_buttons.mouse_click()
                        logging.info("Clicked second radio button")
                        
                        # Verify we made it back to the printer update view
                        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                        logging.info("Set Notify to true via alternative method")
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
                                        # The "Notify When Available" option is usually the second radio button
                                        if i == 1:  # Use index 1 for the second radio button
                                            radio_button.mouse_click()
                                            logging.info(f"Clicked radio button at index {i}")
                                            
                                            # Verify we made it back to the printer update view
                                            assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
                                            logging.info("Set Notify to true via fallback method")
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
        raise TimeoutError("Failed to locate and click the notify when available radio button after multiple attempts")
       
    def set_printerUpdate_doNotCheck(self, spice, enterNav=True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_doNotcheck).mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
        logging.info("Set Do Not Check to true")

    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, net, enterNav=True):
        self.set_printerUpdate_notifyWhenAvailable(spice, enterNav)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_privacy_notice)
        notify_when_available_note = spice.wait_for("#alertDetailDescription #textColumn #contentItem")["text"]
        assert LocalizationHelper.get_string_translation(net, "cNotifyWhenAvailableCP", "en") in notify_when_available_note
        spice.wait_for("#Continue").mouse_click()

    def set_printerUpdate_doNotCheck_goto_iris_message_screen(self, spice, enterNav=True):
        self.set_printerUpdate_doNotCheck(spice, enterNav)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerupdate_save).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)

    def goto_menu_supplies_printheads(self, spice):
        self.goto_menu_supplies(spice)
        self.menu_navigation(spice, self.MenuAppWorkflowUISObjectIds.view_suppliesSummary, "#printHeadsSettingsButton")
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_suppliesSummary)
        logging.info("At Supply Summary Screen")
        time.sleep(1)

    def goto_menu_tools_troubleshooting_printquality(self, spice, isFaxSupported = True):
        self.goto_menu_tools_troubleshooting(spice)
        if isFaxSupported == True :
            spice.wait_for("#printQualityTabModel").mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_printheads)
        assert spice.wait_for("#PrintQualityMenuOptions")
        logging.info ("At Troubleshooting -> Print Quality")

    def goto_menu_settings_print_defaultprintoptions_quality_dropdown(self, spice):
        self.menu_navigation(spice,"#defaultPrintOptionsMenuList", "#qualitySettingsComboBox")
        assert spice.wait_for("#qualityComboBoxpopupList")
        logging.info("At Quality drop down menu")

    def verify_quality_drop_down_menu_items(self, spice):
        spice.wait_for("#qualityComboBoxpopupList")
        assert spice.wait_for("#ComboBoxOptionsbestRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionsnormalRadioButtonModel")

    def verify_quality_drop_down_menu_items_economode_detailed(self, spice):
        spice.wait_for("#qualityComboBoxpopupList")
        assert spice.wait_for("#ComboBoxOptionsnormalRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionsdetailedRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionseconomodeRadioButtonModel")


    def goto_menu_copy_document(self, spice):
        self.goto_menu_copy(spice)
        self.menu_navigation(spice, "#copyMenuAppList", "#documentCopyMenuButton")

        assert spice.wait_for("#MenuListcopy")
        logging.info("At Copy Screen")

    def goto_menu_copy_document_defaultoptions(self, spice):
        #Already in copy document menu (navigate to default options panel)
        spice.wait_for("MenuListcopy")
        detailsButton = spice.wait_for("#optionsDetailPanelButton").click()
        assert spice.wait_for("#copySettingsPage_")
        logging.info("At Copy Document Settings Screen")

    def verify_copy_defaultoptions(self, spice):
        spice.wait_for("#copySettingsPage_")
        assert spice.wait_for("#ComboBoxOptionsnormalImageContainer")
        assert spice.wait_for("#ComboBoxOptionsdraftRadioButtonModel")
        assert spice.wait_for("#ComboBoxOptionsBest")

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.troubleshooting_printQuality_menu_options)
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_printquality)
        scrollbar.__setitem__("position", 0.3)
        assert spice.query_item(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_color_calibration)["visible"] == True
        color_calibration = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_color_calibration)
        color_calibration.mouse_click()

    def goto_menu_tools_troubleshooting_printquality_cleanbelt(self, spice, isFaxSupported = True):
        self.goto_menu_tools_troubleshooting_printquality(spice, isFaxSupported)
        spice.wait_for("#troubleShootingTabLayout")
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_printquality_cleanbelt).mouse_click()  
                  
    def goto_menu_tools_troubleshooting_Fax(self, spice):
        self.goto_menu_tools_troubleshooting(spice)
        faxButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_option)
        faxButton.mouse_click()
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
        #self.menu_navigation(spice, qml, self.MenuAppWorkflowUISObjectIds.view_troubleshooting, self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax)
        #assert spice.wait_for("#SpiceView")
        logging.info("At Troubleshooting -> FAX Screen")
    
    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax_faxT30)
        currentElement.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax_faxT30)
        logging.info("At Troubleshooting -> FAX Screen -> faxT30Button")

    def goto_menu_tools_troubleshooting_Fax_RunFaxTest(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax_runFaxTest)
        currentElement.mouse_click()

    def goto_menu_tools_troubleshooting_Fax_PBXRingDetect(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        ## Further Navigation is not required for PBX Ring Detect in workflow.

    def goto_menu_tools_troubleshooting_Fax_JBIG_Compression(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)

    def change_troubleshooting_Fax_JBIG_Compression(self, spice, enableOption = False):
        '''
        Navigate to Menu -> Tools -> Troubleshooting -> Fax -> JBIG Compression
        '''
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_troubleshooting_fax, MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_jbig, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_fax)
        jbig_switch = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_jbig_switch)
        if(jbig_switch ["checked"] != enableOption):
            jbig_switch.mouse_click(10,10)
            time.sleep(1)
            assert jbig_switch ["checked"] == enableOption, "JBIG Compression Enable/Disbale failed"

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        logging.debug("Spice Objects from current screen :: {0}".format(udw.mainUiApp.execute("SpiceTestServer PUB_getObjectTreeHeirarchy top")))
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt).mouse_click()
        else:
            spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics).mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxmenudiagnostics).mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxregulatorytest).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics)
        logging.info("At Tools -> Service -> Diagnostics ->Fax ->Fax Regulatory Test Screen")

    def goto_menu_tools_servicemenu_faxdiagnostics_showallfaxlocations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_showalllocations, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_showalllocations)
        currentElement.mouse_click()
        time.sleep(2)
        logging.info("At Tools -> Service -> Fax show ALl Location")

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
        # Scroll up to make Hook Operations Button visible
        scrollbar = spice.wait_for(self.MenuAppWorkflowUISObjectIds.scrollbar_tools_service_faxdiagnostics)
        scrollbar.__setitem__("position",0)
        # Query Hook Operations
        time.sleep(2)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_hookoperations)
        currentElement.mouse_click()
        time.sleep(2)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_hookoperations)
        # assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_hookoperations)
        logging.info("At Hook Operations View")        

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
        ## TODO: Menu Navigation for few objects is not working due to validateListObjectVisibility() issues so
        ##       scroll down by 0.3 to make transmitsignalloss button visible.
        scrollbar = spice.wait_for(self.MenuAppWorkflowUISObjectIds.scrollbar_tools_service_faxdiagnostics)
        scrollbar.__setitem__("position",0.3)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_transmitsignalloss)
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(1)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_transmitsignalloss)
        logging.info("At Fax Diagnostic Transmit Signal Loss Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generatesinglemodemtonemenu(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)        
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
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
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_singlemodemtone,timeout=15)
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_generateDialNumber(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_generate_dial_phone_no, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        time.sleep(2)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_generate_dial_phone_no)
        time.sleep(1)
        currentElement.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_dial_phone_number)
        logging.info("At Fax Diagnostic Generate/Dial Phone No Screen")
        time.sleep(1)

    def goto_menu_tools_servicemenu_faxdiagnostics_faxparameters(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
        self.workflow_common_operations.goto_item(
            MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_faxparameters, 
            MenuAppWorkflowObjectIds.view_service_faxdiagnostics,  
            select_option = False, 
            scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_service_faxdiagnostics)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_faxparameters)
        time.sleep(2)
        currentElement.mouse_click()
        logging.info("At Fax Parameters Screen with Password")
        self.goto_menu_tools_servicemenu_faxdiagnostics_faxparameters_password(spice)

    def goto_menu_tools_servicemenu_faxdiagnostics_faxparameters_password(self, spice):
        password = "qsxokm"
        passwordTextField = spice.wait_for(self.MenuAppWorkflowUISObjectIds.faxdiagnostics_faxparamters_password_textfield)
        passwordTextField.mouse_click()
        passwordTextField.__setitem__('displayText', password)
        passwordTextField.__setitem__('inputText', password)
        key_Ok = spice.wait_for(self.MenuAppWorkflowUISObjectIds.KeyOK_two) 
        key_Ok.mouse_click()
        time.sleep(2)

        if len(password) > 0:            
            nextButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.faxdiagnostics_faxparamters_next_button)
            nextButton.mouse_click()

        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_faxcountryparameters)
        logging.info("At Fax Country Parameters Screen")            

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics)
        time.sleep(1)
        currentElement = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_randomdata)
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_faxdiagnostics_generaterandomdata)
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen")

    # Firmware Upgrade Submenu
    def goto_menu_tools_maintenance_firmware(self, spice):
        self.goto_menu_tools_maintenance(spice)
        time.sleep(2)
        menu_button_tools_maintenance_firmware = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_maintenance_firmware)
        menu_button_tools_maintenance_firmware.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_firmwareVersion)
        logging.info("At Firmware Screen")
        time.sleep(1)
    
    def goto_menu_tools_maintenance_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware(spice)
        time.sleep(2)
        fWup_fromUSB_button= spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_maintenance_firmware_updateFWFromUSB)
        fWup_fromUSB_button.mouse_click()
        logging.info("At Firmware Screen")
        time.sleep(1) 

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        fw_up_select_device = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_maintenance_fw_up_select_device)
        fw_up_select_device.mouse_click()
        logging.info("At Select file Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb(spice)
        fw_up_select_file = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_maintenance_fw_up_select_file)
        fw_up_select_file.mouse_click()
        logging.info("At Select Bundle Screen")
        time.sleep(1)

    def goto_menu_tools_maintenance_firmware_iris_firmware_update_from_usb(self, spice):
        self.goto_menu_tools_maintenance_firmware_update_from_usb_selectDrive_selectBdl(spice)
        time.sleep(3)
        logging.info("At Firmware Update Screen")     

    def goto_menu_tools_servicemenu_serviceresets(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            self.menu_navigation(spice, 
                                self.MenuAppWorkflowUISObjectIds.view_service,
                                self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets_alt)
        else:
            self.menu_navigation(spice, 
                                self.MenuAppWorkflowUISObjectIds.view_service,
                                self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_serviceresets)
        logging.info("At Tools -> Service -> Service Resets Screen")

    def goto_menu_tools_servicemenu_serviceresets_transferkitreset(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice,
                             self.MenuAppWorkflowUISObjectIds.view_service_serviceresets,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets_transferkitreset)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_serviceresets_transferkitreset)
        logging.info("At Tools -> Service -> Service Resets -> Transfer Kit Reset Screen")

    def goto_menu_tools_servicemenu_serviceresets_repairmode(self, spice, udw):
        self.goto_menu_tools_servicemenu_serviceresets(spice, udw)
        self.menu_navigation(spice, 
                             self.MenuAppWorkflowUISObjectIds.view_service_serviceresets,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets_repairmode,
                             scrollbar_objectname = self.MenuAppWorkflowUISObjectIds.scrollbar_tools_service_serviceresets)
        current_button = spice.wait_for("#repairModeSettingsButton")
        current_button_height = current_button["height"]/2
        current_button_width = current_button["width"]-20
        current_button.mouse_click(current_button_width , current_button_height)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_serviceresets_repairmode)
        logging.info("At Tools -> Service -> Service Resets -> Repair Mode")

    def goto_menu_tools_servicemenu_servicetests_flatbed(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, 
                             self.MenuAppWorkflowUISObjectIds.view_service_servicetests,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousflatbed)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_continuousflatbed)
        logging.info("At Tools -> Service -> Service Tests -> Continuous Flat Bed Screen")       

    def goto_menu_tools_servicemenu_servicetests_displaytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice, 
                             self.MenuAppWorkflowUISObjectIds.view_service_servicetests,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_displaytest)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_displaytest)
        logging.info("At Tools -> Service -> Service Tests -> Display Test Screen")

    def goto_menu_tools_servicemenu_servicetests_contadfpick(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice,
                             self.MenuAppWorkflowUISObjectIds.view_service_servicetests,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousadfpick)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_continuousadfpick)
        logging.info("At Tools -> Service -> Service Tests -> Continuous ADF Pick Screen")

 
    def goto_menu_tools_servicemenu_servicetests_scanmotortest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        self.menu_navigation(spice,
                             self.MenuAppWorkflowUISObjectIds.view_service_servicetests,
                             self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_scanmotor)
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_scanmotor)
        logging.info("At Tools -> Service -> Service Tests -> Scan Motor Screen")

    def goto_menu_tools_servicemenu_servicetests_frontusbporttest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        # Scroll down to make Walk-up USB Port Test visible
        currentScreen = spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests)
        ## TODO: Menu Navigation for few objects is not working due to validateListObjectVisibility() issues so
        ##       scroll down by 0.6 to make Walk-up USB Port Test button visible.
        scrollbar = spice.wait_for(self.MenuAppWorkflowUISObjectIds.scrollbar_tools_service_servicetests)
        scrollbar.__setitem__("position",0.6)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_frontusbporttest).mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_usbfrontporttest)
        logging.info("At Tools -> Service -> Service Tests -> Walk-up USB Port Test Screen")

    def goto_menu_tools_servicemenu_servicetests_serviceinfinitehs(self, spice, udw, kvp):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        scrollbar = spice.wait_for(MenuAppWorkflowObjectIds.scrollbar_tools_service_servicetests)
        # menu_navigation() method requires update to scroll functionality. Using __setitem__ to statictically 
        # scroll to menu node
        scrollbar.__setitem__("position",0.3)
        spice.wait_for("#" + kvp["menuButton"] +"MenuButton")
        spice.wait_for("#" + kvp["menuButton"] +"MenuButton").mouse_click()
        assert spice.wait_for("#" + kvp["view"])
        logging.info("At Tools -> Service -> Service Tests -> Service Infinite H Test Screen")

    def goto_menu_tools_troubleshooting_calibrations(self, spice):
        """ Go to the troubleshooting calibrations menu inside Menu App
            from home view.
        """
        self.goto_menu_tools(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_troubleshooting , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        logging.info("At Calibrations screen")

    def goto_media_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_mediaApp, use_bottom_border=False, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)

    def goto_menu_job_queue_app(self, spice):
        self.goto_menu(spice)
        time.sleep(1)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_jobApp)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_jobApp + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.job_list_view)
        logging.info("At Menu Job queue Screen")
        time.sleep(1)


    def goto_job_queue_app_floating_dock(self, spice):
        logging.info("Going to job queue app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_jobApp, use_bottom_border=False, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_jobApp+" MouseArea")
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_job_queue_app)

    def goto_supplies_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        spice.main_app.goto_menu_app_floating_dock()
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_supplies, use_bottom_border=False, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_supplies+" MouseArea")
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_supplies_app)

    def goto_menu_settings_supplies(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, 
                             MenuAppWorkflowObjectIds.view_menuSettings,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Supply Settings Screen")
   
    def goto_menu_settings_print_printquality(self, spice):
        self.goto_menu_settings_print(spice)
        printquality_button= spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_print_printquality, 2)
        printquality_button.mouse_click()
        logging.info("At Print Quality Screen")
   
    def goto_menu_settings_jobs_settings(self, spice):
        self.goto_menu_settings(spice)
        time.sleep(1)
        self.workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        job_settings_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings)
        job_settings_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_jobs_settings)
        logging.info("At Jobs Settings Screen")

    def goto_menu_tools_troubleshooting(self, spice):

        spice.homeMenuUI().goto_menu(spice)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_tools, use_bottom_border=False, delta = 0.1)
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools + " MouseArea")
        current_button.mouse_click()
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
    
    # User needs to be at Troubleshoting Screen
    def goto_printhead_alignment(self, spice):
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.ph_alignement + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_printheads)
        logging.info("At Printhead Alignment Screen")
    
    def start_color_calibration(self, spice, input_selection_screen=True):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.color_calibration)

    def start_automatic_printhead_alignment(self, spice, printheads=MenuAppWorkflowObjectIds.ph_alignment_colors, input_selection_screen = True):
        self.goto_printhead_alignment(spice)
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_alignement, index = "0")
        if input_selection_screen:
            logging.info("Waits for input selection screen and select Roll")
            spice.wait_for(MenuAppWorkflowObjectIds.view_calibration_input_selection_screen, timeout = 10)
            continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
            continue_button.mouse_click()
        
    def start_manual_printhead_alignment(self, spice):
        self.goto_printhead_alignment(spice)
        self.start_calibration(spice, MenuAppWorkflowObjectIds.manual_ph_alignment, index = "1")
        
    def start_printheads_cleaning(self, spice):
        self.goto_printheads_cleaning(spice)
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_cleaning, index = "0")

    def start_printheads_hard_cleaning(self, spice):
        self.goto_printheads_cleaning(spice)
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_hard_cleaning, index = "1")

    def start_scanner_calibration(self, spice, scan_action, udw, net, locale, last_view, last_object, cancel_action:bool=False, skip_action:bool=True):
        """
        Executes the calibration process.
        Parameters:
        - spice: Spice fixture.
        - scan_action: The instance of the ScanAction used for scan actions.
        - udw: The UDW fixture.
        - cancel_action: A boolean indicating whether to cancel the calibration process. Default is False.
        - skip_action: A boolean indicating whether to skip the scan process. Default is True.
        last_view, last_object should be used to check the last objects. For S products, the last object is always success. 
        """
        spice.homeMenuUI().goto_menu_tools_troubleshooting(spice)
        scan_tab_button = spice.wait_for(MenuAppWorkflowObjectIds.scan_tab)
        scan_tab_button.mouse_click()

        start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.start_calibration_button)
        start_calibration_button.mouse_click()

        scan_service = spice.wait_for("#ScanService")

        spice.wait_for(MenuAppWorkflowObjectIds.calibration_plot)


        if (skip_action):
            #skipping the scanning part of the plot
            start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_skip_scanning_printed_plot)
            start_calibration_button.mouse_click()
        else:
            spice.wait_for("#printButton").mouse_click()
            calibration_title = spice.wait_for(MenuAppWorkflowObjectIds.calibration_title_header, 360) ["text"]
            logging.info(str(LocalizationHelper.get_string_translation(net, "cScannerCalibrationTab", locale)))
            assert calibration_title == str(LocalizationHelper.get_string_translation(net, "cScannerCalibrationTab", locale))

            #Scan plot already printed
            spice.wait_for(MenuAppWorkflowObjectIds.calibration_plot_successfully_printed_continue_button, 40).mouse_click()
            successful_calibration = spice.wait_for("#SpiceHeaderVar1 #SpiceHeaderVar1HeaderView #leftBlockObject SpiceText[visible=true]", 360) ["text"]
            logging.info(str(LocalizationHelper.get_string_translation(net, "cSuccessfullyPrinted", locale)))
            assert successful_calibration == str(LocalizationHelper.get_string_translation(net, "cSuccessfullyPrinted", locale))

            #Lets follow the copy flow to finish the calibration
            spice.wait_for(MenuAppWorkflowObjectIds.calibration_plot_successfully_printed_continue_button).mouse_click() #to continue
            #Lets continue from Copy screen
            spice.wait_for(MenuAppWorkflowObjectIds.calibration_plot_successfully_printed_continue_button, 20).mouse_click() #to continue

        isMDF = "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower()

        # Checks if there is a page loaded
        if  isMDF and not scan_action.is_media_loaded("MDF"):
            assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_load_sheet_view)
            Control.validate_result(scan_action.load_media("MDF"))

        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_in_progress_view)

        if cancel_action:
            # Cancel the calibration.
            start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_in_progress_cancel_button, 30)
            # Calibration takes a bit to start and enable the cancelling.
            spice.wait_until(lambda: start_calibration_button["enabled"] == True, 20)
            start_calibration_button.mouse_click()

            # Wait for the cancel dialog to appear and confirm.
            #assert spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_dialog)
            start_calibration_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_dialog_confirm_button)
            start_calibration_button.mouse_click()

        else:
            #Successful calibration screen
            scanner_calibration = spice.wait_for(MenuAppWorkflowObjectIds.calibration_success_view + " #wizardCompletionTexts SpiceText[objectName=titleSmallItem]", 60)["text"]
            assert scanner_calibration == str(LocalizationHelper.get_string_translation(net, "cScanCalibrationCompleted", locale))

        #Calibration finished lets confirm
        logging.info("Ok button")
        logging.info(MenuAppWorkflowObjectIds.calibration_success_footer_button)
        ok_button = spice.wait_for("#scanCalibSuccess #scanCalibSuccessFooter #scanCalibSuccessConfirmYes")
        spice.wait_until(lambda: ok_button["visible"] == True)
        spice.wait_for("#scanCalibSuccess #scanCalibSuccessFooter #scanCalibSuccessConfirmYes").mouse_click()
        spice.wait_for("#scanCalibSuccess #scanCalibSuccessFooter #scanCalibSuccessConfirmYes").mouse_click()

    def goto_calibration(self, spice, calibration, index = ""):
        if calibration == MenuAppWorkflowObjectIds.ph_alignement or calibration == MenuAppWorkflowObjectIds.manual_ph_alignment:
            self.goto_printhead_alignment(spice)

        if calibration == MenuAppWorkflowObjectIds.ph_cleaning or calibration == MenuAppWorkflowObjectIds.ph_hard_cleaning:
            self.goto_printheads_cleaning(spice)

        self.select_calibration(spice, calibration, index)
        
    def select_calibration(self, spice, calibration, index = ""):
        calibration_type = spice.wait_for(calibration)
        # There are some calibrations with the same objectnames on both screens,
        # there are no way to tell them apart via objectNames, so we use the index for it
        i = 0
        time.sleep(1)
        while calibration_type["visible"] == False:
            calibration_type = spice.query_item(calibration, i)
            i += 1
        calibration_type.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view + index)
    
    def start_calibration(self, spice, calibration, index = ""):
        self.select_calibration(spice, calibration + " MouseArea", index)
        
        start_button = spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button)
        start_button.mouse_click()
        time.sleep(1)

    def goto_menu_tools_troubleshooting_printquality_printqualitytroubleshootingpage(self, spice):
        spice.wait_for(MenuAppWorkflowObjectIds.tools_menu_print_quality_troubleshooting_page).mouse_click()
        # Validating the Toast Message
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo)["text"] == "Printing..."

    def goto_menu_info_printer_card(self, spice):
        #navigate to the menu /info/printer screen
        self.goto_menu_info_printer(spice)

        #Printer Information card expanded
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_printercard)["visible"]
        time.sleep(2)         
        logging.info("At printer information card Tab")

    def print_diagnostic_test_page(self, spice):
        assert spice.wait_for(MenuAppWorkflowObjectIds.diagnostic_print)["visible"] == True
        spice.wait_for(MenuAppWorkflowObjectIds.diagnostic_print).mouse_click()
        # Validating the Toast Message
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert spice.query_item(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo)["text"] == "Printing..."
        
    
    def click_on_input_selection_continue_button(self, spice):
        continue_button = spice.wait_for(MenuAppWorkflowObjectIds.input_selection_continue_button)
        continue_button.mouse_click() 

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
    
    def cancel_calibration_flow(self, spice, curing=False):
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration, timeout=30)
        cancel_button.mouse_click()
        if curing:
            cancel_print_and_curing_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_print_and_curing)
            cancel_print_and_curing_button.mouse_click()
        else:
            cancel_only_printing_button = spice.wait_for(MenuAppWorkflowObjectIds.cancel_calibration_print_only)
            cancel_only_printing_button.mouse_click()
        confirm_button = spice.wait_for(MenuAppWorkflowObjectIds.confirm_cancel_calibration)
        confirm_button.mouse_click()

    def validate_tray_app(self,spice,cdm,net):
        logging.info("validating tray apps")
        dict = {
            1: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray1", "en")),
            2: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray2", "en")),
            3: str(LocalizationHelper.get_string_translation(net, "cMediaInputIdTray3", "en"))
        }
        request = cdm.get_raw(cdm.CDM_MEDIA_CONFIGURATION)
        assert request.status_code == 200
        media_configuration = request.json()
        assert spice.wait_for("#MediaAppApplicationStackView") ["visible"] == True,"Trays screen is not visible"
        assert spice.wait_for("#MediaAppApplicationStackView #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #textContainer SpiceText[visible=true]")["text"] == "Trays"
        for input in media_configuration.get("inputs",[]):
            media_source_id = input.get("mediaSourceId", "")
            if "tray" in media_source_id:
                match = re.search(r'tray-(\d+)',media_source_id)
                if match:
                    tray_number = int(match.group(1))
                    assert spice.query_item("#titleSmallItem", tray_number - 1)["text"] == dict[tray_number]

    # Menu Settings General Energy prevent Shutdown
    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.35, "#energySettingsMenuListScrollBar")
        assert spice.wait_for("#energycheckbox #CheckBoxView")
        return spice.query_item("#energycheckbox #CheckBoxView")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        self.workflow_common_operations.scroll_to_position_vertical(.35, "#energySettingsMenuListScrollBar")

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
        self.workflow_common_operations.scroll_to_position_vertical(.35, "#energySettingsMenuListScrollBar")

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
    
    def menu_settings_General_Datetime_SystemtimeChange (self, spice):
        #set system time as 9 hours and 0 minute
        self.menu_settings_General_Datetime_SetSystemTime(spice,9,0)

    def find_positive_integer_key_pad(self,number):
        key_value = positive_integer_key_pad_map[number]
        return(key_value)

    def menu_settings_General_Datetime_SetSystemTime (self, spice, given_hour, given_minute):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time, scrollbar_objectname=MenuAppWorkflowObjectIds.dateTime_scrollbar)
        try:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
            logging.info("At Time Settings Screen")
            try:
                spice.wait_for("#Hour #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At spinbox keyboard")
                    for digit in str(given_hour):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for Hour Spin Box: {e}")
            try:
                spice.wait_for("#Minute #SpinBoxTextInput").mouse_click()
                try:
                    assert spice.wait_for("#spiceKeyboardView")
                    logging.info("At the spinbox keyboard")

                    for digit in str(given_minute):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                    spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button
                except AssertionError:
                    logging.info("Could not find the keyboard view")
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for Minute Spin Box: {e}")
            try:
                applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
                applyButton.mouse_click()
            except Exception as e:
                logging.warning(f"Exception occurred while waiting for time apply button: {e}")
        except AssertionError:
            logging.info("Could not find the keyboard view")
        finally:
            spice.goto_homescreen()
            
    def energy_scheduleOff_set_time_day_after_schedule(self, spice, cdm, net):
        setschedhour=10
        setschedminute=0
        setsyshouraftersched=10
        setsysminuteaftersched=3

        self.menu_settings_general_energy_scheduleOnOff_setdayandtime(spice,"schedule off",setschedhour,setschedminute)
        self.validate_poweroff_scheduled_data(cdm,setschedhour,setschedminute)
        self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)

        self.menu_settings_General_Datetime_SetSystemTime(spice, setsyshouraftersched, setsysminuteaftersched)

        clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
        clock_data = clock.json()
        system_time = clock_data['systemTime']
        time_part = system_time.split('T')[1]
        hour_minute = time_part.split(':')[0:2]
        hour = int(hour_minute[0])
        minute = int (hour_minute[1])

        assert(hour==setsyshouraftersched)
        assert(minute==setsysminuteaftersched)
        return

    def menu_settings_general_energy_scheduleOnOff_setdayandtime(self,spice,given_screen,given_hour,given_minute):
        spice.homeMenuUI().goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        spice.homeMenuUI().goto_schedule_on_or_off_screen(spice, given_screen)

        logging.info("Set schedule on date and time")
        try:
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
                    logging.warning(f"{error_message}: {e}")
                    spice.goto_homescreen()
                    return
            try:
                spice.wait_for("#timeSettingsListView #Hour #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.warning("Failed to find the spinbox keyboard:")
                logging.info("At spinbox keyboard")
                for digit in str(given_hour):
                    spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
                spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click()

            except Exception as e:
                logging.info(f"Failed to set hour: {e}")
                spice.goto_homescreen()
                return

            try:
                spice.wait_for("#timeSettingsListView #Minute #spinbox #SpinBoxTextInput").mouse_click()
                if not spice.wait_for("#spiceKeyboardView"):
                    logging.info(f"Failed to find the spinbox keyboard: {e}")
                logging.info("At the spinbox keyboard")
                for digit in str(given_minute):
                        spice.wait_for(self.find_positive_integer_key_pad(int(digit))).mouse_click()
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
        except Exception as e:
            logging.info(f"Failed to verify schedule off {e}")
            return

    def validate_poweroff_scheduled_data(self,cdm,sethour,setminute):
        cdmPowerData = cdm.get_raw(cdm.POWER_CONFIG)
        logging.info(cdmPowerData.json())
        statusGet = cdmPowerData.status_code
        assert statusGet == 200, "status=%d" % statusGet

        # Validate powerOffScheduleEnabled as True
        assert(cdmPowerData.json()["powerOffScheduleEnabled"] == "true")

        # Validate poweroff schedule data
        hourOffset=0
        minuteOffset=0

        powerOffSchedule = cdmPowerData.json().get("powerOffSchedule", [])
        for schedule in powerOffSchedule:
            timesOfDay = schedule.get("timesOfDay", [])
            for time in timesOfDay:
                hourOffset = time.get("hourOffset")
                minuteOffset = time.get("minuteOffset")

        assert(hourOffset == sethour)
        assert(minuteOffset == setminute)
        return

    def energy_scheduleOff_set_time_day_before_schedule(self, spice, cdm, net):
        setschedhour=10
        setschedminute=0
        setsyshourbeforesched=9
        setsysminutebeforesched=57

        self.menu_settings_general_energy_scheduleOnOff_setdayandtime(spice,"schedule off",setschedhour,setschedminute)
        self.validate_poweroff_scheduled_data(cdm,setschedhour,setschedminute)
        self.menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(spice, cdm)

        self.menu_settings_General_Datetime_SetSystemTime(spice, setsyshourbeforesched, setsysminutebeforesched)

        clock = cdm.get_raw(cdm.CLOCK_CONFIGURATION)
        clock_data = clock.json()
        system_time = clock_data['systemTime']
        time_part = system_time.split('T')[1]
        hour_minute = time_part.split(':')[0:2]
        hour = int(hour_minute[0])
        minute = int (hour_minute[1])

        assert(hour==setsyshourbeforesched)
        assert(minute==setsysminutebeforesched)
        return

    def menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_setScheduledays(self, spice, cdm):
        try:
            systemtime_cdm = cdm.get(cdm.CLOCK_CONFIGURATION)
            logging.info("systemtime_cdm before is = %s", systemtime_cdm)

            systemTime = cdm.get(cdm.CLOCK_CONFIGURATION)["systemTime"]
            logging.info("dayName = %s", systemTime)

            # Replacing "T" and "Z" with spaces
            s = systemTime.replace("T", " ").replace("Z", " ")
            logging.info("s = %s", s)

            # Replacing the first two occurrences of "-" with "/"
            date = s.replace("-", "/", 2)
            logging.info("date = %s", date)

            new_string = date.rstrip()
            logging.info("new_string = %s", new_string)

            # Converting the string to datetime object
            datetime_date = datetime.strptime(new_string, "%Y/%m/%d %H:%M:%S")
            logging.info("datetime_date = %s", datetime_date)

            # Printing the day of the week
            dayName = datetime_date.strftime("%A").lower()
            logging.info("day = %s", dayName)

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
                    r = cdm.patch_raw(cdm.POWER_CONFIG, body)
                    r = cdm.get_raw(cdm.POWER_CONFIG)
                    logging.info("CDM Value = %s", r.json())
                except Exception as e:
                    logging.info(f"Failed to update power off schedule: {e}")
            else:
                logging.info("None of the Days selected")

        except Exception as e:
            logging.info(f"An error occurred: {e}")

    def set_mismatch_actions_pause_and_ask(self, spice):
        mismatch_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_pause_and_ask)
        mismatch_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)
    
    def set_mismatch_actions_hold_and_continue(self, spice):
        hold_and_continue_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_hold_job)
        hold_and_continue_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)
        
    def verify_job_recovery_policy_index(self, spice, index):
        jobs_settings_job_recovery_mode_settings = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_settings)
        spice.wait_until(lambda:jobs_settings_job_recovery_mode_settings["currentIndex"] == index)

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
            time.sleep(2)
            assert spice.query_item(MenuAppWorkflowObjectIds.troubleshooting_app)
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
        time.sleep(1)
        value_input["text"] = value
        spice.wait_for("#enterKeyIntegerKeypad").mouse_click()

    def goto_menu_tools_troubleshooting_scanner_calibration(self, spice):
        spice.homeMenuUI().goto_menu_tools_troubleshooting(spice)
        scan_tab_button = spice.wait_for(MenuAppWorkflowObjectIds.scan_tab)
        assert scan_tab_button, "Scanner Calibration button is not visible"
        scan_tab_button.mouse_click()
        logging.info ("Clicked on Scanner Calibration button")
        logging.info ("At Troubleshooting -> Scanner Calibration")


    def go_to_scanner_calibration_start_screen(self, spice):
        """
        Navigates to the screen in which there is a button to print the Scanner Calibration Plot
        """       
        # Menu > Tools > Troubleshooting > Scanner Calibration
        spice.homeMenuUI().goto_menu_tools_troubleshooting_scanner_calibration(spice)

        # Click "Start" button
        spice.wait_for(MenuAppWorkflowObjectIds.start_calibration_button).mouse_click()

    def go_to_scanner_calibration_check_screen(self, spice):
        """
        Navigates to the screen in which there is a button to print the Scanner Diagnostic Plot
        """       
        # Menu > Tools > Troubleshooting > Scanner Calibration
        spice.homeMenuUI().goto_menu_tools_troubleshooting_scanner_calibration(spice)

        # Click "Check" button
        spice.wait_for(MenuAppWorkflowObjectIds.check_calibration_button).mouse_click()

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
        time.sleep(2)
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
