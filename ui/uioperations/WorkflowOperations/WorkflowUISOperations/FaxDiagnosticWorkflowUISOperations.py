
import logging
from time import sleep
import time
from dunetuf.ui.uioperations.WorkflowOperations.FaxDiagnosticWorkflowUICommonOperations import FaxDiagnosticWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
import json

class FaxDiagnosticWorkflowUISOperations(FaxDiagnosticWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations

    #camden, marconihipdl, selene, lotus
    def faxdiagnostics_ringsettings_on(self, spice, udw, enableOption = False):
        logging.info("Goto Ring Settings On")
        pbxRingDetectToggleSwitch = spice.wait_for("#pbxRingDetectSwitch")
        if(pbxRingDetectToggleSwitch ["checked"] != enableOption):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            sleep(1)
            assert pbxRingDetectToggleSwitch ["checked"] == enableOption, "PBX Ring Detect Enable/Disbale failed"
        ringIntervalSpinBox = spice.wait_for("#ringIntervalSpinBox")
        ringIntervalSpinBox.__setitem__('value', "400")
        scrollbar = spice.wait_for("#ringSettingsScrollBar")
        scrollbar.__setitem__("position",0.2)
        sleep(1)
        ringFrequencySpinBox = spice.wait_for("#ringFrequencySpinBox")
        ringFrequencySpinBox.__setitem__('value', "99")
        sleep(2)
        currentElement = spice.wait_for("#doneButton")
        currentElement.mouse_click()
        sleep(2)          

    def single_modem_tone(self,cdm):
        '''
        Navigates to Single modem tone.
        UI Flow is Home->Service->Fax Diagnostic ->Single Modem Tone
        '''
        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_1300Hz)
        currentElement.mouse_click()
        sleep(1)

        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_startstop)
        currentElement.mouse_click()
        sleep(5)

        generateTone = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert generateTone["state"] == "processing", "Modify operation failed"
        sleep(1)

        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_startstop)
        currentElement.mouse_click()
        sleep(2)

        generateTone = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert generateTone["state"] == "idle", "Modify operation failed"

    def verifyfaxmodemmode(self, cdm, state):
        cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert cdm_model
        logging.info(cdm_model)
        if hasattr(cdm_model, 'lastResult'):
            assert cdm_model['lastResult'] == 'success'
        else:
            assert cdm_model['state'] == state        

    def showallfaxlocations(self,cdm,udw):
        '''
        Verifies the show all fax locations button
        UI Flow is Home->Service->Fax Diagnostic ->Show all Fax locations
        '''
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---s screen--: {printerName}')

        def assert_cdm_value_with_ui_value_workflow(showallfax_switch, bool):
            showallfax_switch.mouse_click()
            sleep(1)
            cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
            sleep(1)
            assert cdm_model["showAllFaxLocationsEnabled"] == bool

        showallfax_switch1 = self._spice.query_item("#showAllFaxLocationsTextImage")
        # camden, marconi, selene, moreto, marconihipdl, lotus
        if printerName == "jasper" or printerName == "pearl" or printerName == "morganite":
            showallfax_switch1.mouse_click()
        sleep(1)
        showallfax_switch = self._spice.query_item("#showAllFaxLocationsView")
        assert showallfax_switch
        sleep(2)

        defaultButtonModel_switch = self._spice.wait_for("#defaultButtonModel")
        showAllButtonModel_switch = self._spice.wait_for("#showAllButtonModel")

        # Turn the switch on and off and check cdm values
        if defaultButtonModel_switch["checked"] == True:
            assert_cdm_value_with_ui_value_workflow(defaultButtonModel_switch, "false")
        elif defaultButtonModel_switch["checked"] == False:
            assert_cdm_value_with_ui_value_workflow(defaultButtonModel_switch, "true")

    def servicemenu_faxdiagnosticsmenu_hookoperations(self, cdm, spice, udw):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Service -> Fax DIagnostics -> Hook Operations
        '''
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---small screen--: {printerName}')

        # Wait for view
        current_element = spice.wait_for("#hookOperationsView")
        assert current_element

        # Go off hook to enable hook operations
        current_element = spice.wait_for("#goOffHookButtonModel")
        current_element.mouse_click()

        current_element = spice.wait_for("#doneButton")
        current_element.mouse_click()

        configModel = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)

        # Test onHookEnabled
        assert configModel['onHookEnabled'] == 'false'          #marconihipdl, selene, lotus, camden

        # Test current
        assert configModel['readLineCurrent'].find("mA")

        # Test voltage
        assert configModel['readLineVoltage'].find("Volts")

    def enter_numeric_keyboard_values(self, number, view=FaxAppWorkflowObjectIds.view_keyboard, OK_locator= FaxAppWorkflowObjectIds.keyOK):

        self._spice.wait_for(view)
        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self._spice.wait_for("#key" + num + "PositiveIntegerKeypad")
            key.mouse_click()
        key_Ok  = self._spice.wait_for("#TextView")
        key_Ok.mouse_click()        
        
    def faxdiagnostics_generatedialingtones(self, spice, configuration, dialingtone):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        dialingtone_dict = {
            "Pulse Burst": FaxAppWorkflowObjectIds.diagnostic_dialing_pulseradiobutton,
            "Tone Burst": FaxAppWorkflowObjectIds.diagnostic_dialing_toneradiobutton,
            "Continuous Tone": FaxAppWorkflowObjectIds.diagnostic_dialing_continuoustoneradiobutton
        }
        menu_item_id = dialingtone_dict.get(dialingtone)

        if dialingtone in ["Pulse Burst","Tone Burst","Continuous Tone"]:
            current_button = spice.wait_for(menu_item_id)
            current_button.mouse_click()
            assert spice.wait_for(menu_item_id)["checked"] == True, "Dialing tone is not selected"
        else:
            raise logging.info(f"{dialingtone} is not supported to select")
        
        self.fax_diagnostic_lastdigit(spice, "5", configuration, dialingtone)

    def fax_diagnostic_lastdigit(self, spice, last_digit, configuration, dialingtone):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_scrollbar)
        scrollbar.__setitem__("position",0.2)
        sleep(1)
        lastdigitTextBox = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_lastdigittextbox)
        if (configuration.familyname == "enterprise"):
            lastdigitTextBox.__setitem__('displayText', last_digit)
        else:            
            lastdigitTextBox.mouse_click()
            lastdigitTextBox.__setitem__('displayText', last_digit)
            keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
            keyboard_ok_button.mouse_click()

        # lastdigitTextBox.mouse_click()
        # self.enter_numeric_keyboard_values(last_digit)
        # sleep(1)
        
        if dialingtone == "Continuous Tone":
            sleep(1)
            currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
            assert spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)["enabled"] == True, "Start button is not enabled"
            currentElementStart.mouse_click()
            sleep(1)
            currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
            assert spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)["enabled"] == True, "Start button is not enabled"
            currentElementStart.mouse_click()
        sleep(5)
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_donebutton)
        currentElementdonebutton.mouse_click()        

    def fax_diagnostic_dialingtone_start_verify_constrained_message(self, spice, configuration):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)

        current_button = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_pulseradiobutton)
        current_button.mouse_click()

        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_scrollbar)
        scrollbar.__setitem__("position", 0.2)

        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton, timeout=5)
        currentElementStart.mouse_click()

        # Selected Pulse Burst, clicked start button then verify the constrained message
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        current_button = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_continuoustoneradiobutton)
        current_button.mouse_click()

        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
        currentElementStart.mouse_click()

        # Selected Continuous Tone, last digit is empty, clicked start button then verify the constrained message
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        lastdigitTextBox = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_lastdigittextbox)
        last_digit = '58'
        lastdigitTextBox.mouse_click()
        lastdigitTextBox.__setitem__('displayText', last_digit)
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click()

        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
        currentElementStart.mouse_click()

        # Selected Continuous Tone, last digit is 58, clicked start button then verify the constrained message
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        last_digit = '7'
        lastdigitTextBox.mouse_click()
        lastdigitTextBox.__setitem__('displayText', last_digit)
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click()

        # Selected Continuous Tone, last digit is 7, clicked start button
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton, timeout=5)
        currentElementStart.mouse_click()

        # Click stop button
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton, timeout=5)
        currentElementStart.mouse_click()

        # Click done button
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_donebutton, timeout=5)
        currentElementdonebutton.mouse_click()

    def fax_diagnostic_dialingtone_pulsetone_verify_constrained_message(self, spice, configuration):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)

        current_button = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_toneradiobutton)
        current_button.mouse_click()

        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_scrollbar)
        scrollbar.__setitem__("position", 0.2)

        lastdigitTextBox = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_lastdigittextbox, timeout=5)
        last_digit = '43'
        lastdigitTextBox.mouse_click()
        lastdigitTextBox.__setitem__('displayText', last_digit)
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click()

        # Selected Tone Burst, enter last digit as 43 then verify the constrained message
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        # Click done button
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_donebutton)
        currentElementdonebutton.mouse_click()

    def servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, cdm):
        '''
        Verifies the UI Flow is Menu->Tools->Service->Fax Diagnostic->TranmitSignalLoss
        '''
        view = self._spice.wait_for("#faxTransmitSignalLossView")
        assert view
        logging.info("Fax Diagnostic > Fax Transmit Signal Loss")

        #user input signal level
        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_transmitsignalloss_signal)
        currentElement.mouse_click()
        sleep(2)

        #change range to 5 and register user selection
        keyboard = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_transmitLevelKeyboard)
        assert keyboard
        default = "5"

        keyboard.__setitem__('text', default) 
        
        logging.info("Fax Transmit Signal Loss user input set to 5")
        sleep(2)

        #navigate to proceed button
        fiveButton = self._spice.query_item("#key5PositiveIntegerKeypad").mouse_click()
        okButton = self._spice.query_item("#enterKeyPositiveIntegerKeypad").mouse_click()
        proceedButton = self._spice.wait_for("#proceedButton")
        proceedButton.mouse_click()
        sleep(2)
        logging.info("Fax Transmit Signal Loss is sent to CDM")

        #check that model data matches PATCH value
        cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
        assert int(cdm_model['faxTransmitSignalLoss']) == 5
        logging.info("Fax Transmit Signal Loss is checked with the user input")
        sleep(2)

    def faxdiagnostics_singlemodemtone_v1100(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1100")
        currentElement = spice.wait_for("#tone1100")
        currentElement.mouse_click()
        sleep(2)
        currentElementStart = spice.wait_for("#startStop")
        logging.info("Starting Generate SingleModemTone v1100")
        currentElementStart.mouse_click()
        sleep(5)
        assert spice.wait_for("#startStop")
        logging.info("Done Generate SingleModemTone v1100")
        currentElementStop = spice.wait_for("#startStop")
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for("#DoneButton")
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v1300(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1300")
        currentElement = spice.wait_for("#tone1300")
        currentElement.mouse_click()
        sleep(2)
        currentElementStart = spice.wait_for("#startStop")
        logging.info("Starting Generate SingleModemTone v1300")
        currentElementStart.mouse_click()
        sleep(5)
        assert spice.wait_for("#startStop")
        logging.info("Done Generate SingleModemTone v1300")
        currentElementStop = spice.wait_for("#startStop")
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for("#DoneButton")
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v1800(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1800")
        currentElement = spice.wait_for("#tone1800")
        currentElement.mouse_click()
        sleep(2)
        currentElementStart = spice.wait_for("#startStop")
        logging.info("Starting Generate SingleModemTone v1800")
        currentElementStart.mouse_click()
        sleep(5)
        assert spice.wait_for("#startStop")
        logging.info("Done Generate SingleModemTone v1800")
        currentElementStop = spice.wait_for("#startStop")
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for("#DoneButton")
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v2100(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v2100")
        self.workflow_common_operations.goto_item(
            "#tone2100", "#generateSingleModemTone", select_option = False, scrollbar_objectname = "#generateSingleModemToneScrollBar")
        currentElement = spice.wait_for("#tone2100")
        currentElement.mouse_click()
        sleep(2)
        currentElementStart = spice.wait_for("#startStop")
        logging.info("Starting Generate SingleModemTone v2100")
        currentElementStart.mouse_click()
        sleep(5)
        assert spice.wait_for("#startStop")
        logging.info("Done Generate SingleModemTone v2100")
        currentElementStop = spice.wait_for("#startStop")
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for("#DoneButton")
        currentElementdonebutton.mouse_click() 

    def generate_dial_phone_no(self,cdm,spice,udw):
        logging.info("Fax Diagnostic Generate/Dial phone no!")

        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---small screen--: {printerName}')

        faxNumber = 101
        endpoint = cdm.FAX_MODEM_DIAGNOSTIC_OPERATION
        #Here check the cdm get() of diagnosticOperation. This shows we entered menu with diagnostics turned on
        stateModel = cdm.get_raw(endpoint)
        status = stateModel.status_code
        body = stateModel.json()

        assert status == 200
        if 'state' in body:
            assert body['state'] == 'idle'
        
        #Set dial type
        currentRadioButton = spice.wait_for("#faxDialTypeToneButton")
        currentRadioButton.mouse_click()
        sleep(1)

        #Set FAX No
        FaxNoTextField = spice.wait_for("#phoneNoTextField")
        FaxNoTextField.__setitem__('displayText', faxNumber)
        sleep(2)

        #Click Dial Button
        currentRadioButton = spice.wait_for("#dialButton")
        currentRadioButton.mouse_click()

        spice.wait_until(condition=lambda:'lastResult' in cdm.get(endpoint), timeout=30, delay=3)

        #Check CDM get. 
        stateModel = cdm.get(endpoint)
        assert stateModel
        if 'state' in body:
            assert body['state'] == 'idle'
        
        sleep(5)

        #Click Done Button
        currentRadioButton = spice.wait_for("#DoneButton")
        currentRadioButton.mouse_click()

        logging.info("Fax Diagnostic Generate/Dial phone no completed")

    def servicemenu_faxdiagnostics_faxParameters(self, cdm):
        #This function compares our paramName to the cdm paramName
        def check_view_value_to_cdm(view):
            viewText = view["paramName"]
            assert viewText

            diagnosticData = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)

            sleep(2)

            #Check that country parameter contains data
            assert diagnosticData['countryParameter']
            logging.info(diagnosticData)

            assert diagnosticData['countryParameter']['name'] == viewText

            return viewText 

        view =  self._spice.wait_for("#faxCountryParametersView")

        sleep(2)

        #Change parameters
        assert self._spice.query_item("#spinBox")
        self._spice.query_item("#spinBox")['value'] = 5

        retrieveButton = self._spice.wait_for("#retrieve")
        retrieveButton.mouse_click()

        sleep(2)

        initial_paramName = check_view_value_to_cdm(view)

        sleep(1)

        #Update currentValue to test the Save button
        assert self._spice.query_item("#currentValueTextObj")

        compareCurrentValue = self._spice.query_item("#currentValueTextObj")['inputText']
        updatedCurrentValue = 2

        assert int(compareCurrentValue) != updatedCurrentValue

        #CurrentValue text box to 2
        self._spice.query_item("#currentValueTextObj")['inputText'] = updatedCurrentValue
        self._spice.query_item("#currentValueTextObj")['displayText'] = updatedCurrentValue

        sleep(1)

        compareCurrentValue = self._spice.query_item("#currentValueTextObj")['inputText']
        assert updatedCurrentValue == int(compareCurrentValue)

        sleep(1)        

        #click save
        saveButton = self._spice.wait_for("#faxCountryParamSave")
        saveButton.mouse_click()

        sleep(2)
        self._spice.query_item("#spinBox")['value'] = 4
        retrieveButton = self._spice.wait_for("#retrieve")
        retrieveButton.mouse_click()

        sleep(1)

        compareCurrentValue = self._spice.query_item("#currentValueTextObj")['inputText']
        assert updatedCurrentValue != compareCurrentValue
        sleep(2)

        # Scroll down for the reset button to be visible in UI
        # self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.5, "#faxCountryParametersViewlist1ScrollBar")
       

        compareCurrentValue = self._spice.query_item("#currentValueTextObj")['inputText']

        diagnosticData = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
        assert diagnosticData['countryParameter']
        defaultValue = diagnosticData['countryParameter']['defaultValue']

        assert  int(compareCurrentValue) == int(defaultValue)

        printButton = self._spice.wait_for("#faxCountryParamPrint")
        printButton.mouse_click()

    def servicemenu_faxdiagnostics_generaterandomdata(self, cdm, spice):
        '''
        Verifies the show all fax locations button
        UI Flow is Home->Service->Fax Diagnostic ->Show all Fax locations
        '''
    
        optionslist = [
            ["#v21_300", "#v17_14400","#v17_12000"],
            ["#v29_9600","#v29_7200"],
            ["#v27_4800", "#v27_2400", "#v34_33600"],
            ["#v34_31200", "#v34_28800", "#v34_26400"],
            ["#v34_24000", "#v34_21600"],
            ["#v34_19200", "#v34_16800", "#v34_14400", ],
            ["#v34_12000", "#v34_9600",],
            ["#v34_7200", "#v34_4800", "#v34_2400", ],
            ["#v34_3429", "#v34_3200H", ],
            ["#v34_3200L", "#v34_3000H", "#v34_3000L", ],
            ["#v34_2800H", "#v34_2800L"],
            ["#v34_2743H", "#v34_2743L", "#v34_2400H"],
            ["#v34_2400L"]
        ]

        view = spice.wait_for("#generateRandomDataView")
        assert view

        scroll_value = 0
        for options in optionslist:
            spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(scroll_value, "#generateRandomDataViewScrollBar")            
            for option in options:
                logging.info(f'Click on option: {option}')
                # current_button = spice.query_item("#generateRandomDataViewlist1 " + option)
                current_button = spice.query_item(option)
                sleep(1)
                current_button.mouse_click()
            scroll_value = scroll_value + 0.06

        view = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_randomdata_startdone)
        view.mouse_click()
        sleep(1)

        self.verifyfaxmodemmode(cdm,'processing')
        
        view = spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_randomdata_startdone)
        view.mouse_click()
        sleep(1)

        self.verifyfaxmodemmode(cdm,'idle')

    def diagnostictestview_runfaxtest_start(self, spice):
        logging.info("Starting Run Fax Test")
        assert spice.wait_for(FaxAppWorkflowObjectIds.diagnostictests_menulist_view)
        time.sleep(2)
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.menu_button_diagnostictests_runfaxtest, 
            FaxAppWorkflowObjectIds.diagnostictests_menulist_view,  
            select_option = False,
            scrollbar_objectname = FaxAppWorkflowObjectIds.diagnostictests_menulist_scrollbar)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.button_runfaxtest_start)
        currentElement.mouse_click()
        time.sleep(2)

    def check_diagnostictestview_not_maintenance_mode(self, spice):
        time.sleep(2)
        continuebutton = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_continue_button)
        continuebutton.mouse_click()
        time.sleep(10)
        exiting_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.button_diagnostictests_exiting_maintenancemode_ok)
        exiting_ok_button.mouse_click()

    def check_diagnostictestview_exit_maintenance_mode(self, spice):
        logging.info("Checking Exiting Maintenance Mode")
        diagnostic_test = spice.wait_for(FaxAppWorkflowObjectIds.button_diagnostictests_exiting_maintenancemode_cancel)
        diagnostic_test.mouse_click()
        time.sleep(1)

    def diagnostictestview_cancel_maintenance_mode(self, spice):
        logging.info("Cancel Maintenance Mode")
        assert spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_view)
        time.sleep(1)
        cancel_button = spice.wait_for(MenuAppWorkflowObjectIds.maintenancemode_cancel_button)
        cancel_button.mouse_click()
        time.sleep(1)

    def diagnostictestview_click_other_option(self, spice):
        logging.info("Clicking Other Option")
        assert spice.wait_for(FaxAppWorkflowObjectIds.diagnostictests_menulist_view)
        time.sleep(2)
        other_option = spice.wait_for(FaxAppWorkflowObjectIds.button_diagnostictests_back)
        other_option.mouse_click()
        time.sleep(1)

    def diagnostictestview_click_home(self, spice):
        logging.info("Clicking Home")
        current_screen = spice.wait_for(FaxAppWorkflowObjectIds.diagnostictests_menulist_view)
        spice.wait_until(lambda: current_screen["visible"] == True)
        time.sleep(2)
        home_button = spice.wait_for(FaxAppWorkflowObjectIds.button_diagnostictests_home)
        home_button.mouse_click()
        time.sleep(1)        

    def set_faxdiagnostics_ringsettings_status(self, spice, status_value):
        """
        set faxdiagnostics ringsettings status True/False
        """
        logging.info(f"Set Ring Settings status to {status_value}")
        spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_ringSettings)['position'] = 0

        pbxRingDetectToggleSwitch = spice.wait_for(FaxAppWorkflowObjectIds.pbx_ringdetect_switch)
        if(pbxRingDetectToggleSwitch["checked"] != status_value):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            # wait one second to wait button status change
            time.sleep(1)
            assert pbxRingDetectToggleSwitch["checked"] == status_value, f"PBX Ring Detect status:{status_value} failed"

    def click_save_button_on_faxdiagnostics_ringsettings(self, spice):
        """
        Click save button on faxdiagnostics ringsettings screen.
        """
        save_button = spice.wait_for(FaxAppWorkflowObjectIds.save_button)
        spice.validate_button(save_button)
        save_button.mouse_click()
