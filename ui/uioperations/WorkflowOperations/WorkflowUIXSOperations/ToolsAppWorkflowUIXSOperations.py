import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowUICommonOperations import ToolsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowXSObjectIds import MenuAppWorkflowXSObjectIds

class ToolsAppWorkflowUIXSOperations(ToolsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice


    # Service Pin operations
    def servicePin_test(self, udw):
        '''
        Tests the service pin menu.
        Menu->Tools->Service->ServicePinPrompt
        '''  
        SUNSPOT_PIN = "7429"
        BEAM_PIN = "3989"
        DEFAULT_PIN = "08675309"
        ADMIN_PIN = "Pass5742"
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname

        serviceMenu = self._spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service)
        serviceMenu.mouse_click()

        keyboard = self._spice.wait_for(MenuAppWorkflowXSObjectIds.view_serviceKeyboard)
        assert keyboard

        #Enter Admin pin, note default pin is set, we expect admin pin to fail
        keyboard.__setitem__('displayText', ADMIN_PIN) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', ADMIN_PIN)

        time.sleep(2)

        doneButton = self._spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_tools_servce_AuthDone)
        doneButton.mouse_click()

        #Should see access denied
        assert self._spice.wait_for(MenuAppWorkflowXSObjectIds.view_access_denied)

        #click ok button to get out of access denied screen
        self._spice.wait_for("#OK").mouse_click()
        time.sleep(2)

        #Return to service menu
        serviceMenu = self._spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service)
        serviceMenu.mouse_click()

        keyboard = self._spice.wait_for(MenuAppWorkflowXSObjectIds.view_serviceKeyboard)
        assert keyboard

        time.sleep(2)

        if printerName.strip() == 'beam/beamsfp_power' or printerName.strip() == "beamsfp":
            #Enter Default Beam pin
            keyboard.__setitem__('displayText', BEAM_PIN) #just to show the password populated on keyboard
            keyboard.__setitem__('inputText', BEAM_PIN)
        elif printerName.strip() == 'sunspot':
            keyboard.__setitem__('displayText', SUNSPOT_PIN) #just to show the password populated on keyboard
            keyboard.__setitem__('inputText', SUNSPOT_PIN)
        else:
            #Enter Default pin
            keyboard.__setitem__('displayText', DEFAULT_PIN) #just to show the password populated on keyboard
            keyboard.__setitem__('inputText', DEFAULT_PIN)
        time.sleep(2)

        doneButton = self._spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_tools_servce_AuthDone)
        doneButton.mouse_click()

        time.sleep(5)
 
        #In service menu now.
        assert self._spice.wait_for(MenuAppWorkflowXSObjectIds.view_service)
        logging.info("At Service Screen")
        time.sleep(1)
    
    def servicemenu_servicetests_displaytest(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->Service Tests->Display Test
        """
        currentScreen = self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_servicetests_displaytest)
        assert currentScreen

        for x in range(9):
            button = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_servicetests_displaytest_proceed)
            button.mouse_click()

        time.sleep(2)

    def servicemenu_servicetests_keytest(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->Service Tests->Key Test
        """
        keys = ["HOME","BACK","HELP"]

        currentScreen = self._spice.wait_for(MenuAppWorkflowXSObjectIds.view_service_servicetests_keytest)
        assert currentScreen
        
        okButton = self._spice.query_item(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_keytest_ok)
        okButton.mouse_click()
        
        for key in keys:
            logging.info("Verifying Key: %s" % key)
            time.sleep(1) # Give time to see key prompt
            self._spice.udw.mainUiApp.KeyHandler.setKeyPress(key)
        
        time.sleep(1) # Give time to see test passed

        titleTextView = self._spice.wait_for("#textColumn #titleSmallItem")["text"]
        
        assert titleTextView == "Test passed"

        cancelButton = self._spice.query_item(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_keytest_cancel)
        cancelButton.mouse_click()

    def servicemenu_servicetests_faxdiagnostictest(self, cdm, cdmEndPoint, ringInterval, ringFrequency):
        try:
            logging.info("Attempting get() on diagnosticOperation")
            w = cdm.get(cdmEndPoint)
        except:
            assert False, "Failed to GET " + cdmEndPoint

        # Get PBX
        pbxRingDetectToggleSwitch = self._spice.query_item("#pbxRingDetectSwitch")
        if(pbxRingDetectToggleSwitch ["checked"] != True):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            time.sleep(1)
            assert pbxRingDetectToggleSwitch ["checked"] == True, "PBX Ring Detect Enable/Disbale failed"
    
        # # Check original state and set to opposite state
        expectedPbxState = "true"

        # # Get Ring Interval
        assert self._spice.query_item("#ringIntervalSpinBox")
        ringIntervalSpinBox = self._spice.query_item("#ringIntervalSpinBox")
        ringIntervalSpinBox["value"] = ringInterval
        assert self._spice.query_item("#ringIntervalSpinBox")["value"] == ringInterval
    
        # Get Ring Frequency
        assert self._spice.query_item("#ringFrequencySpinBox")
        ringIntervalSpinBox = self._spice.query_item("#ringFrequencySpinBox")
        ringIntervalSpinBox["value"] = ringFrequency
        assert self._spice.query_item("#ringFrequencySpinBox")["value"] == ringFrequency
        
        # Save current settings
        # should be Interval 555, frequency 55, and ring on
        assert self._spice.query_item("#doneButton")
        saveButton = self._spice.query_item("#doneButton")
        time.sleep(0.1)
        saveButton.mouse_click()
        time.sleep(0.1)
        # Should save as ring on
    
        # # Compare and check CDM Endpoint
        try:
            logging.info("Attempting get() on diagnosticOperation")
            w = cdm.get(cdmEndPoint)
        except:
            assert False, "Failed to GET " + cdmEndPoint
    
        assert w["ringSettings"]["pbxRingDetectEnabled"]=='true', "ERROR: PBX state does not match"
    
        # offButton.mouse_click()
        # sleep(0.1)
        # saveButton.mouse_click()
        time.sleep(0.1)
        # # Compare and check CDM Endpoint
        try:
            logging.info("Attempting get() on diagnosticOperation")
            w = cdm.get(cdmEndPoint)
        except:
            assert False, "Failed to GET " + cdmEndPoint
        # assert w["ringSettings"]["pbxRingDetectEnabled"]=='false', "ERROR: PBX state does not match"
        assert w["ringSettings"]["ringInterval"]==ringInterval, "ERROR: Ring interval (" +w["ringSettings"]["ringInterval"]+ ") does not match (" +ringInterval+ ")"
        assert w["ringSettings"]["ringFrequency"]==int(ringFrequency), "ERROR: Ring frequency (" +w["ringSettings"]["ringFrequency"]+ ") does not match (" +ringFrequency+ ")"        

    def servicemenu_faxdiagnosticsmenu_generatedialingtonespulsesmenu(self, cdm, cdmEndPoint, methods):
        currentElement = self._spice.wait_for("#generatePulseToneBurstView")
        assert currentElement

        # Here check the cdm get() of diagnosticOperation.
        # This shows we entered menu with diagnostics turned on
        stateModel = cdm.get(cdmEndPoint)
        assert stateModel
        assert stateModel['state'] == "idle"

        # Select last digits
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        assert self._spice.query_item("#continuousToneButton")
        radiobutton = self._spice.query_item("#continuousToneButton")
        radiobutton.mouse_click()
        self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.5, "#generatePulseToneBurstViewScrollBar")        
        assert self._spice.query_item("#lastDigitsTextObj")
        lastdigitTextBox = self._spice.query_item("#lastDigitsTextObj")
        lastdigitTextBox.mouse_click()
        lastdigitTextBox.__setitem__('displayText', "5")
        okButton = self._spice.query_item("#TextView")
        okButton.mouse_click()
        assert self._spice.query_item("#continuousToneButton")
        radiobutton = self._spice.query_item("#continuousToneButton")
        radiobutton.mouse_click()
        # assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        # self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        # self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0, "#generatePulseToneBurstViewScrollBar")

        assert self._spice.query_item("#startStopButton")
        startStopButton = self._spice.query_item("#startStopButton")

        startStopButton.mouse_click()
        time.sleep(1)
        startStopButton.mouse_click()

        assert self._spice.query_item("#DoneButton")
        doneButton = self._spice.query_item("#DoneButton")
        doneButton.mouse_click() 

        #check test results
        stateModel = cdm.get(cdmEndPoint)
        assert stateModel['lastResult'] == 'success'          

    def test_maintenance_regionreset(self):
        resetButton = self._spice.wait_for("#ResetButton SpiceText")
        resetButton.mouse_click()
        # Wait for the cdm actions to show results in the progress screen
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_regionreset)
        assert self._spice.wait_for("#genericResultView")
        genResultView = self._spice.query_item("#genericResultView")
        assert bool(genResultView.__getitem__("result")) == True
        resultTimer = genResultView.__getitem__("resultTimer")
        assert resultTimer == 10000
        # Go back to the maintenance app home page.
        okButton = self._spice.wait_for("#okResetViewButton")
        okButton.mouse_click()