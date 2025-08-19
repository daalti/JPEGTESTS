#########################################################################################
# @file      FaxDiagnosticProSelectUIOperations.py
# @author    Praveen
# @date      28-11-2021
# @brief     Interface for all the Fax Diagnostics methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################

from time import sleep
import logging

from dunetuf.ui.uioperations.BaseOperations.IFaxDiagnosticUIOperations import IFaxDiagnosticUIOperations

_logger = logging.getLogger(__name__)


class FaxDiagnosticProSelectUIOperations(IFaxDiagnosticUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    # Single Modem Tone flow operations

    def single_modem_tone(self,cdm):
        '''
        Navigates to Single modem tone.
        UI Flow is Home->Service->Fax Diagnostic ->Single Modem Tone
        '''
        sleep(2)
        currentElement = self._spice.wait_for("#generateSingleModemTone")
        assert currentElement

        while (self._spice.query_item("#tone1800")["activeFocus"] == False):
            currentElement.mouse_wheel(180,180)
            sleep(0.2)
        currentElement.mouse_click()
        sleep(0.2)
        assert self._spice.query_item("#tone1800")["checked"] == True, "tone1800 item is not checked"

        currentElement.mouse_wheel(180,180)
        if (self._spice.query_item("#startButton")["activeFocus"] == True):
            currentElement.mouse_click()
            sleep(0.2)

        currentElement.mouse_wheel(180,180)
        
        if (self._spice.query_item("#doneButton")["activeFocus"] == True):
            currentElement.mouse_click()
            sleep(0.2)

        generateTone = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert generateTone["lastResult"] == "success", "Modify operation failed"


    def showallfaxlocations(self,cdm):
        '''
        Verifies the show all fax locations button
        UI Flow is Home->Service->Fax Diagnostic ->Show all Fax locations
        '''

        switch = self._spice.query_item("#showAllFaxLocationsMenuSwitch")
        assert switch["activeFocus"] == True

        state = switch["checked"]
        switch.mouse_click()

        sleep(0.2)

        cdmModel = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
        assert cdmModel["showAllFaxLocationsEnabled"] != state

    def servicemenu_faxdiagnosticsmenu_hookoperations(self, cdm):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Service -> Fax DIagnostics -> Hook Operations
        '''
        # Wait for view
        currentElement = self._spice.wait_for("#hookOperationsView")
        assert currentElement
        currentElement.mouse_wheel(180,180)
        currentElement.mouse_click()
        sleep(5)

        # Test Line Voltage Value
        voltage = self._spice.query_item("#ValueText", 1)
        assert voltage
        assert voltage['text'].find("Volts")

        # Test Line Current Value
        current = self._spice.query_item("#ValueText", 2)
        assert current
        assert current['text'].find("mA")
        currentElement.mouse_wheel(180,180)
        currentElement.mouse_wheel(180,180)

        # Test Refresh Button
        assert self._spice.query_item("#refreshButtonModel")
        currentElement.mouse_click()
        sleep(0.2)
        # Voltage
        voltage = self._spice.query_item("#ValueText", 1)
        assert voltage
        assert voltage['text'].find("Volts")
        # Current
        current = self._spice.query_item("#ValueText", 2)
        assert current
        assert current['text'].find("mA")

        # Scroll Back to Go Off Hook Button
        while(self._spice.query_item("#goOnOffHookButtonModel")['activeFocus'] != True):
            currentElement.mouse_wheel(0,0)
            sleep(0.2)
        currentElement.mouse_click()

        # Test Go Off Hook Button
        assert self._spice.query_item("#goOnOffHookButtonModel")
        currentElement.mouse_click()
        sleep(5)

        configModel = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
        assert configModel
        assert configModel['onHookEnabled'] == 'true'

        # Test Done Button
        while(self._spice.query_item("#doneButtonModel")['activeFocus'] != True):
            currentElement.mouse_wheel(180,180)
            sleep(0.2)
        currentElement.mouse_click()

    def generate_dial_phone_no(self,cdm):
        faxNumber = 5555555
        endpoint = cdm.FAX_MODEM_DIAGNOSTIC_OPERATION
        #Here check the cdm get() of diagnosticOperation. This shows we entered menu with diagnostics turned on
        stateModel = cdm.get(endpoint)
        assert stateModel
        assert stateModel['state'] == 'idle'

        logging.info("Fax Diagnostic CDM Good!")

        #Set Faxnumber. Navigate to keyboard
        currentScreen = self._spice.wait_for("#generateDialPhoneNumber")
        currentScreen.mouse_wheel(180, 180)
        assert self._spice.query_item("#keyboardButton")
        currentScreen.mouse_click()

        currentScreen = self._spice.wait_for("#spiceKeyboardView")        
        currentScreen.__setitem__('currentText', faxNumber)
        sleep(1)

        while (self._spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
            currentScreen.mouse_wheel(0,0)
            sleep(0.2)
        currentScreen.mouse_click()

        #Set Dial type. Navigate to Dial Type Menu
        currentScreen = self._spice.wait_for("#generateDialPhoneNumber")
        sleep(1)
        currentScreen.mouse_wheel(180, 180)
        sleep(1)
        assert self._spice.query_item("#DialTypeButton")
        currentScreen.mouse_click()

        currentScreen = self._spice.wait_for("#faxSelectDialTypeView")
        sleep(1)
        currentScreen.mouse_wheel(180,180)
        sleep(0.5)
        currentScreen.mouse_click()

        currentScreen = self._spice.wait_for("#generateDialPhoneNumber")  
        sleep(1)      
        while(self._spice.query_item("#DialFaxNumberButton")['activeFocus'] != True):
            currentScreen.mouse_wheel(180,180)
            sleep(0.2)

    def servicemenu_faxdiagnostics_faxParameters(self, cdm):
        def check_view_value_to_cdm(view):
            view_text = view['paramName']
            assert view_text

            diagnosticData = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
            assert diagnosticData
            assert diagnosticData['countryParameter']['name'] == view_text

            return view_text

        view = spice.wait_for("#faxCountryParametersView")

        #check default is populated
        default_value = check_view_value_to_cdm(view)

        #move to single range input component
        view.mouse_wheel(180,180)
        spinner =  spice.query_item('#SpiceTumblerView')
        assert spinner['activeFocus'] is True

        #spinner value  property bound to paramValue
        view.mouse_click()
        view['paramNumber'] = 5
        #trigger update
        view.mouse_click()

        time.sleep(1)

        #check that it changed
        assert default_value != check_view_value_to_cdm(view)

        #TODO: when support for reset operation and value change are implemented
        # extend this test to cover the functionality
        # UI already contains logic for this (needs to be turned on)


    def servicemenu_faxdiagnostics_generaterandomdata(self, cdm):
        '''
        Verifies the show all fax locations button
        UI Flow is Home->Service->Fax Diagnostic ->Show all Fax locations
        '''
    
        options = ["#v17_14400","#v17_12000","#v29_9600","#v29_7200","#v27_4800","#v27_2400","#v34_33600","#v34_31200","#v34_28800"]

         # Wait for view
        view = self._spice.wait_for("#generateRandomDataView")
        assert view

        for option in options:
            while(self._spice.query_item(option)['activeFocus'] != True):
                view.mouse_wheel(180,180)
                sleep(0.5)
        
        while(self._spice.query_item("#startButton")['activeFocus'] != True):
            view.mouse_wheel(180,180)
            sleep(0.5)

        view.mouse_click()

        sleep(1)

        cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert cdm_model
        if hasattr(cdm_model, 'lastResult'):
            assert cdm_model['lastResult'] == 'success'
        else:
            assert cdm_model['state'] == 'processing' 

        while(self._spice.query_item("#doneButton")['activeFocus'] != True):
            view.mouse_wheel(180,180)
            sleep(0.2)
        sleep(1)
        view.mouse_click()

    def servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, cdm):
        '''
        Verifies the UI Flow is Menu->Tools->Service->Fax Diagnostic->TranmitSignalLoss
        '''
        view = self._spice.wait_for("#faxTransmitSignalLossView")
        assert view

        #proceed button has focus - navigate to range spinner
        view.mouse_wheel(0, 0)

        #toggle range focus
        view.mouse_click()

        #change range to 5
        for _ in range(5):
            view.mouse_wheel(180,180)
            sleep(0.25)

        #register user selection
        view.mouse_click()

        #navigate to proceed button
        view.mouse_wheel(180,180)

        #allow ui to apply changes to cdm
        view.mouse_click()
        sleep(0.2)

        #check that model data matches PATCH value
        cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
        assert int(cdm_model['faxTransmitSignalLoss']) == 5
        sleep(1)
