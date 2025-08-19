
import logging
import time
from datetime import datetime
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflow2UICommonOperations import MenuAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.network.net import Network
from dunetuf.configuration import Configuration

class MenuAppWorkflow2UISOperations(MenuAppWorkflow2UICommonOperations):
    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = Workflow2UICommonOperations(spice)
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()
        super().__init__(spice)
        
    def goto_menu_settings_printerUpdate(self, spice):
        logging.info("Navigating to Settings Menu")
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate,scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate)
        logging.info("At Printer Update WF Screen")

    def goto_menu_settings_printerUpdate_allowUpgrades(self, spice, enterNav = True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate(spice)
        upgradeButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_allowUpgrades)
        upgradeButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate_iris)
        logging.info("At Printer Update IRIS Message Screen")
   
    def goto_menu_settings_printerUpdate_allowUpgrades_iris_options(self, spice, enterNav = True):
        if(enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.8, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_allowUpgrades_next, timeout = 15)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def set_printerUpdate_allowAutoUpdate(self, spice):
        self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        autoUpdateButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_allowAutoUpdate)
        autoUpdateButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate)
        logging.info("Set autoUpdateEnabled to true")
       
    def set_printerUpdate_notifyWhenAvailable(self, spice, enterNav = True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        notifyButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_notifyWhenAvailable)
        notifyButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate, timeout = 0.9)
        logging.info("Set Notify to true")
       
    def set_printerUpdate_doNotCheck(self, spice, enterNav = True):
        if (enterNav):
            self.goto_menu_settings_printerUpdate_allowUpgrades_iris_options(spice)
        doNotCheckButton = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_settings_printerUpdate_doNotcheck)
        doNotCheckButton.mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_printerUpdate,timeout = 0.9)
        logging.info("Set Do Not Check to true")

    def set_printerUpdate_allowAutoUpdate_goto_iris_message_screen(self, spice, net):
        self.set_printerUpdate_allowAutoUpdate(spice)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, False)
       
    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, net, enterNav=True):
        self.set_printerUpdate_notifyWhenAvailable(spice, enterNav)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, enterNav)
       
    def set_printerUpdate_doNotCheck_goto_iris_message_screen(self, spice, enterNav = True):
        self.set_printerUpdate_doNotCheck(spice, enterNav)
        self.goto_menu_settings_printerUpdate_allowUpgrades(spice, enterNav)
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
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax_menu).mouse_click()
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
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_t30_repmode_menu)
        #assert spice.wait_for("#SpiceView")
        logging.info("At Troubleshooting -> FAX Screen")
    
    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode(self, spice):
        self.goto_menu_tools_troubleshooting_Fax(spice)
        spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_t30_repmode_menu).mouse_click()
        assert spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_t30_repmode_menu)
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
        time.sleep(1)
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        if self.product_family == 'enterprise':
            currentElement = spice.query_item(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_alt)
        else:
            currentElement = spice.query_item(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics)
        time.sleep(1)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxmenudiagnostics)
        time.sleep(1)
        currentElement.mouse_click()
        currentElement = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxregulatorytest)
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(1)
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
                                 self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets_alt,
                                 scrollbar_objectname=self.MenuAppWorkflowUISObjectIds.scrollbar_serviceMenu)
        else:
            self.menu_navigation(spice,
                                 self.MenuAppWorkflowUISObjectIds.view_service,
                                 self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets,
                                 scrollbar_objectname=self.MenuAppWorkflowUISObjectIds.scrollbar_serviceMenu)
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
        time.sleep(1)
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
        self.workflow_common_operations.goto_menu_app_floating_dock(spice)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_mediaApp, use_bottom_border=False, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_mediaApp)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_media_app)

    def goto_job_queue_app_floating_dock(self, spice):
        logging.info("Going to job queue app from menu app")
        self.workflow_common_operations.goto_menu_app_floating_dock(spice)
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage, 10)
        self.scroll_position_utilities(MenuAppWorkflowObjectIds.menu_button_jobApp, use_bottom_border=False, delta = 0.1)
        spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.menu_button_jobApp+" MouseArea")
        time.sleep(1)
        spice.wait_for(MenuAppWorkflowObjectIds.ui_job_queue_app)

    def goto_supplies_app_floating_dock(self, spice):
        logging.info("Going to media app from menu app")
        self.workflow_common_operations.goto_menu_app_floating_dock(spice)
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
        self.menu_navigation(spice, 
                             MenuAppWorkflowObjectIds.view_menuSettings,
                             MenuAppWorkflowObjectIds.menu_button_settings_jobs_settings + " MouseArea",
                             scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_jobs_settings)
        logging.info("At Jobs Settings Screen")
    
    # User needs to be at Troubleshoting Screen
    def goto_printhead_alignment(self, spice):
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.ph_alignement + " MouseArea")
        current_button.mouse_click()
        time.sleep(1)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_printheads)
        logging.info("At Printhead Alignment Screen")
    
    def start_color_calibration(self, spice):
        self.start_calibration(spice, MenuAppWorkflowObjectIds.color_calibration)

    def start_automatic_printhead_alignment(self, spice, printheads=MenuAppWorkflowObjectIds.ph_alignment_colors):
        self.goto_printhead_alignment(spice)
        self.start_calibration(spice, MenuAppWorkflowObjectIds.ph_alignement, index = "0")
        
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
        while calibration_type["visible"] == False:
            calibration_type = spice.query_item(calibration, i)
            i += 1
        calibration_type.mouse_click()
        time.sleep(2)
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_view + index)
        time.sleep(1)
    
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
        assert spice.wait_for("#MediaAppApplicationStackView") ["visible"] == True,"Trays screen is not visible"
        assert spice.wait_for("#MediaAppApplicationStackView #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #textContainer SpiceText[visible=true]")["text"] == "Trays"
        assert spice.query_item("#titleSmallItem")["text"] == "Tray 1"
        assert spice.query_item("#titleSmallItem",1)["text"] == "Tray 2"
        assert spice.query_item("#titleSmallItem",2)["text"] == "Tray 3"
        
    def goto_menu_settings_general_energy(self, spice):
        self.goto_menu_settings(spice)
        current_button1 = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general + " MouseArea")
        current_button1.mouse_click()

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings)
        logging.info("At Energy Settings Screen")
        
    def goto_menu_settings_general_energy_inactivity_shutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(.45, "#energySettingsMenuListScrollBar")
        logging.info("At Energy Settings Screen")
        
    def goto_menu_settings_general_display_inactivity_timeout(self, spice):
        self.goto_menu_settings(spice)
        current_button1 = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general + " MouseArea")
        current_button1.mouse_click()

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_display + " MouseArea")
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
        
    # Menu Settings General Energy prevent Shutdown
    def goto_menu_settings_general_energy_preventshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(.45, "#energySettingsMenuListScrollBar")
        assert spice.wait_for("#energycheckbox #CheckBoxView")
        return spice.query_item("#energycheckbox #CheckBoxView")

    def set_energypreventshutdown_donotdisable(self, spice):
        self.goto_menu_settings_general_energy(spice)
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(.45, "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()

    def set_energypreventshutdown_whenportsareactive(self, spice):
        self.goto_menu_settings_general_energy(spice)
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(.45, "#energySettingsMenuListScrollBar")

        current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_preventShutdown + " MouseArea")
        current_button.mouse_click()
        
    def goto_menu_settings_general_energy_autoshutdown(self, spice):
        self.goto_menu_settings_general_energy(spice)
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(.35, "#energySettingsMenuListScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_autoshutdown)        

    def test_core_power_ui_menu_settings_General_Datetime_SystemtimeChange (self, spice):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        logging.info("At Time Settings Screen")
        #SystemTime settings 
        #Setting the Hour to 9
        spice.query_item("#Hour #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At spinbox keyboard")
        spice.query_item("#key9PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        #Setting the Minutes to 0
        spice.query_item("#Minute #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At the spinbox keyboard")
        spice.query_item("#key0PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()

        spice.goto_homescreen() 

    def menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_after(self,spice,cdm):
        self.test_core_power_ui_menu_settings_General_Datetime_SystemtimeChange(spice)                  #setting the datetime to 9:00am
        self.goto_menu_settings_general_energy_scheduleOff_set_time_day(spice)                        #setting the schedule to 10:00am
        systemtime_cdm = cdm.get(cdm.CLOCK_CONFIGURATION)
        print("systemtime_cdm before is = ", systemtime_cdm)

        systemTime = cdm.get(cdm.CLOCK_CONFIGURATION)["systemTime"]
        print("dayName = ",systemTime)

        # Replacing "T" and "Z" with spaces
        s = systemTime.replace("T", " ").replace("Z", " ")
        print("s =", s)

        # Replacing the first two occurrences of "-" with "/"
        date = s.replace("-", "/", 2)
        print("date =", date)

        new_string = date.rstrip()
        print("new_string =",new_string)

        # Converting the string to datetime object
        datetime_date = datetime.strptime(new_string, "%Y/%m/%d %H:%M:%S")
        print("datetime_date =", datetime_date)

        # Printing the day of the week
        dayName =  datetime_date.strftime("%A")
        print("day =", dayName)  
        configuration_endpoint = "/cdm/power/v1/configuration"
        if dayName == "Sunday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "sunday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Monday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "monday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Tuesday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "tuesday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Wednesday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "wednesday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Thursday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "thursday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Friday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "friday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Saturday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "saturday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())
        else:
            logging.info("None of the Days selected")
        time.sleep(1)  

    def menu_settings_General_Energy_SystemtimeChange_ScheduleOFF_Before(self,spice,cdm):
        self.test_core_power_ui_menu_settings_General_Datetime_SystemtimeChange(spice)                  #setting the datetime to 9:00am

        systemtime_cdm = cdm.get(cdm.CLOCK_CONFIGURATION)
        print("systemtime_cdm before is = ", systemtime_cdm)

        systemTime = cdm.get(cdm.CLOCK_CONFIGURATION)["systemTime"]
        print("dayName = ",systemTime)

        # Replacing "T" and "Z" with spaces
        s = systemTime.replace("T", " ").replace("Z", " ")
        print("s =", s)

        # Replacing the first two occurrences of "-" with "/"
        date = s.replace("-", "/", 2)
        print("date =", date)

        new_string = date.rstrip()
        print("new_string =",new_string)

        # Converting the string to datetime object
        datetime_date = datetime.strptime(new_string, "%Y/%m/%d %H:%M:%S")
        print("datetime_date =", datetime_date)

        # Printing the day of the week
        dayName =  datetime_date.strftime("%A")
        print("day =", dayName)  
        configuration_endpoint = "/cdm/power/v1/configuration"
        if dayName == "Sunday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "sunday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Monday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "monday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Tuesday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "tuesday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Wednesday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "wednesday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Thursday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "thursday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Friday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "friday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())

        elif dayName == "Saturday":
                    body = {
                        "version" : "1.0.0",
                        "shutdownPrevention" : "none",
                        "powerOffScheduleEnabled": "true",
                        "powerOffSchedule": {
                        "timesOfDay": [
                            {
                            "hourOffset": 10,
                            "minuteOffset": 0
                            }
                        ],
                        "daysOfWeek": [
                            "saturday"
                        ]
                        }
                    }
                    r = cdm.patch_raw(configuration_endpoint, body)
                    r = cdm.get_raw(configuration_endpoint)
                    print("CDM Value = ",r.json())
        else:
            logging.info("None of the Days selected")
        time.sleep(1)  

    
    def goto_menu_settings_general_energy_scheduleOff_set_time_day(self,spice):
        self.goto_menu_settings_general_energy_scheduleOnOff_screen(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_energySettings_scheduleOnOffScreen, MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleTurnOffscreen)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOffScreen)

        DaysOption = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView)
        DaysOption.mouse_click()

        Sunday = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_Sunday)
        Sunday.mouse_click()

        NextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_nextButton)
        NextButton.mouse_click()

        hourset = spice.wait_for(MenuAppWorkflowObjectIds.view_energySettings_scheduleOnHoursView)
        hourset.mouse_click()

        #Setting the Hour to 10
        spice.query_item("#timeSettingsListView #Hour #spinbox #SpinBoxTextInput").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At spinbox keyboard")
        spice.query_item("#key1PositiveIntegerKeypad").mouse_click()
        spice.query_item("#key0PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        #Setting the Minute to 0
        spice.query_item("#timeSettingsListView #Minute #spinbox #SpinBoxTextInput").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At the spinbox keyboard")
        spice.query_item("#key0PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        DoneButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_doneButton)
        DoneButton.mouse_click()
        SaveButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleONOFF_scheduleDaysView_saveButton)
        SaveButton.mouse_click()


    def test_core_power_ui_menu_settings_General_Datetime_SystemtimeChange_9Hr57min (self, spice, net):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        logging.info("At Time Settings Screen")

        #SystemTime Setting the Hour to 9
        spice.query_item("#Hour #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At spinbox keyboard")
        spice.query_item("#key9PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        #SystemTime Setting the Minutes to 57
        spice.query_item("#Minute #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At the spinbox keyboard")
        spice.query_item("#key5PositiveIntegerKeypad").mouse_click()
        spice.query_item("#key7PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()

        # spice.goto_homescreen()
        time.sleep(180)
        #pinging to check the system is shutdown
        ping_status = net.is_pingable(net.ip_address)
        print("ping_status =",ping_status)
        print("ip_address =",net.ip_address)
        assert ping_status == True, "Ping Failed for the IP"

    def test_core_power_ui_menu_settings_General_Datetime_SystemtimeChange_10Hr03min (self, spice, net):
        self.goto_menu_settings_general_dateTime(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_dateTime, MenuAppWorkflowObjectIds.dateTime_time)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_dateTime_time)
        logging.info("At Time Settings Screen")

        #SystemTime Setting the Hour to 10
        spice.query_item("#Hour #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At spinbox keyboard")
        spice.query_item("#key1PositiveIntegerKeypad").mouse_click()
        spice.query_item("#key0PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        #SystemTime Setting the Minutes to 03
        spice.query_item("#Minute #SpinBoxTextFieldMouseArea").mouse_click()
        assert spice.wait_for("#spiceKeyboardView")
        logging.info("At the spinbox keyboard")
        spice.query_item("#key0PositiveIntegerKeypad").mouse_click()
        spice.query_item("#key3PositiveIntegerKeypad").mouse_click()
        spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click() #click ok button

        applyButton = spice.wait_for(MenuAppWorkflowObjectIds.time_applyButton)
        applyButton.mouse_click()

        time.sleep(180)
        #pinging to check the system is shutdown
        ping_status = net.is_pingable(net.ip_address)
        print("ping_status =",ping_status)
        print("ip_address =",net.ip_address)
        assert ping_status == True, "Ping Failed for the IP"
    
    def set_mismatch_actions_pause_and_ask(self, spice):
        mismatch_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_pause_and_ask)
        mismatch_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)
    
    def set_mismatch_actions_hold_and_continue(self, spice):
        hold_and_continue_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_mismatch_actions_hold_job)
        hold_and_continue_button.mouse_click()
        spice.wait_for(MenuAppWorkflowObjectIds.view_mismatchActions)

    def goto_menu_info_printer_card(self, spice):
        """
        Navigate to the INFO Application -> Printer Info -> Info Card Tab
        """
        logging.info("Navigating to Info App -> Printer Info -> Info Card Tab")
        self.goto_menu_info_printer(spice)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo_printercard)["visible"]
        logging.info("At Info App -> Printer Info Card Tab")

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            scroll_bar = spice.wait_for(scrollbar_id)
            scrollbar_size = scroll_bar["visualSize"]
            scroll_bar.__setitem__("position", scrollbar_size - size)
            return True