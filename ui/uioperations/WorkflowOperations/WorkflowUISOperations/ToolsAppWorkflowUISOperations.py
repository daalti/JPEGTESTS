import logging
from time import sleep

from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowUICommonOperations import ToolsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.qmltest.QmlTestServer import QmlTestServer



class ToolsAppWorkflowUISOperations(ToolsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()


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

        serviceMenu = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service)
        serviceMenu.mouse_click()

        keyboard = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_serviceKeyboard)
        assert keyboard

        #Enter Admin pin, note default pin is set, we expect admin pin to fail
        keyboard.__setitem__('displayText', ADMIN_PIN) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', ADMIN_PIN)

        sleep(2)

        doneButton = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_servce_AuthDone)
        doneButton.mouse_click()

        #Should see access denied
        assert self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_access_denied)

        #click ok button to get out of access denied screen
        self._spice.wait_for("#OK").mouse_click()
        sleep(2)

        #Return to service menu
        serviceMenu = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service)
        serviceMenu.mouse_click()

        keyboard = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_serviceKeyboard)
        assert keyboard

        sleep(2)

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
        sleep(2)

        doneButton = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_tools_servce_AuthDone)
        doneButton.mouse_click()

        sleep(5)
 
        #In service menu now.
        assert self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service)
        logging.info("At Service Screen")
        sleep(1)

    # Single Modem Tone flow operations

    def troubleshoot_fax_runFaxTest(self):
        '''
        Checks the runFax test messages submitted thorugh
        Menu->Tools->Troubleshooting->Fax->Run Fax Test
        '''
        self.verify_toast_message("Printing...")

    def troubleshoot_fax_PBXRingDetect(self, cdm):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Troubleshooting -> Fax -> PBX Ring Detect
        '''
        def assert_cdm_value_with_ui_value_workflow(pbx_switch, bool):
            pbx_switch.mouse_click()
            sleep(2)
            cdm_model = cdm.get(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT)
            sleep(1)
            assert cdm_model['analogFaxReceiveSettings']['pbxRingDetectEnabled'] == bool

        pbx_switch = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_torubleshooting_fax_pbx)
        assert pbx_switch
        self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.3, MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_fax)
        sleep(2)
        # Turn the switch on and off and check cdm values
        if pbx_switch["checked"] == True:
            assert_cdm_value_with_ui_value_workflow(pbx_switch, "false")
        elif pbx_switch["checked"] == False:
            assert_cdm_value_with_ui_value_workflow(pbx_switch, "true")

    def setValue_and_save(self,buttonId,index,cdm):
        if index > 3:
            Scroling_btn = self._spice.wait_for("#faxT30RepModelist1ScrollBar")
            Scroling_btn.__setitem__("position",index*0.1)
        self._spice.wait_for(buttonId).mouse_click()
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_faxT30_save).mouse_click()
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax)

        faxT30 = cdm.get(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT)
        return faxT30['analogFaxOperation']['t30ReportMode']

    def troubleshoot_fax_faxT30RepMode(self, cdm):
        '''
        Test Navigation and Functionality of Menu->Tools->Troubleshooting->Fax->Fax T.30 Rep Mode
        '''
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode)
        sleep(2)
        element_list=[ ["#faxT30NeverAutoPrint","never"], ["#faxT30PrintAfterEveryFax","always"], ["#faxT30PrintAfterFaxSend","allSendJobs"], ["#faxT30PrintAfterFaxReceive","allReceiveJobs"], ["#faxT30PrintAfterFaxSendErrors","sendErrorsOnly"], ["#faxT30PrintAfterFaxReceiveErrors","receiveErrorsOnly"], ["#faxT30PrintAfterAnyFaxError","allErrors"]]
        index=1
        for element in element_list:
            assert self.setValue_and_save(element[0],index,cdm)==element[1],"Set operation failed"
            index +=1
            sleep(1)
            if element[0] != element_list[-1][0]:
                self._spice.wait_for (MenuAppWorkflowObjectIds.menu_button_troubleshooting_fax_faxT30).mouse_click()
                sleep(2)
                self._spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_t30_repmode)

    def troubleshoot_fax_clearFaxMemoryLog(self):
        '''
        Clears the Fax Memory Logs submitted through
        Menu -> Tools -> Troubleshooting -> Fax -> Clear Fax Log/Memory
        '''
        # validate clear button
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_clearfax_log)
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_torubleshooting_fax_clearLogs_clearbutton2).mouse_click()
        assert self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_toast_window)
        assert self._spice.query_item(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_toastinfo)["text"] == "Success"

        # validate cancel button
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax)
        self._spice.wait_for (self.MenuAppWorkflowUISObjectIds.menu_button_troubleshooting_fax_clearLogs).mouse_click()
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_torubleshooting_fax_clearLogs_cancel).mouse_click()
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax)

    def servicemenu_servicetests_continuousflatbedtest(self,net):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service tests-> Continous Flat bed test
        """
        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_continuousflatbed)
        assert currentScreen

        button = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousflatbed_proceed)
        button.mouse_click()

        processmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeProcessing")
        assert processmsg in self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_toastinfo,15)["text"]

        cancelmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeCanceling")
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousflatbed_dismiss).mouse_click()

        QmlTestServer.wait_until(lambda: cancelmsg in self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_toastinfo,15)["text"],timeout=15)

    def servicemenu_servicetests_displaytest(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service tests-> Display test
        """
        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_displaytest)
        assert currentScreen

        for x in range(9):
            button = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_displaytest_proceed)
            button.mouse_click()

        sleep(2)

    def servicemenu_servicetests_continuousadfpicktest(self,net):
        """
        Test Navigation and Functionality of Menu -> Tools -> Engineering Menu -> Service Menu -> Service Tests -> Continuous ADF Pick Test
        """
        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_continuousadfpick)
        assert currentScreen

        button = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousadfpick_proceed)
        button.mouse_click()

        processmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeProcessing")
        assert processmsg in self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_toastinfo,10)["text"]

        cancelmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeCanceling")
        self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_continuousadfpick_dismiss).mouse_click()

        QmlTestServer.wait_until(lambda: cancelmsg in self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_troubleshooting_fax_toastinfo,10)["text"],timeout=15)

    def servicemenu_servicetests_scanmotortest(self):
        """
        Test Navigation and Functionality of Menu -> Tools -> Engineering Menu -> Service Menu -> Service Tests -> Scan Motor Test
        """

        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_scanmotor)
        assert currentScreen

        button = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_scanmotor_start)

        for count in range(5): #0-4
            view = self._spice.query_item(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_scanmotor)
            assert count == view['cycleCount']
            button.mouse_click()
            sleep(1)

        #5
        view = self._spice.query_item(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_scanmotor)
        assert 5 == view['cycleCount']
        ## Workaround for goto_homescreen() not going to Home Menu.
        self._spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)
    
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
            sleep(1)
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
        sleep(0.1)
        saveButton.mouse_click()
        sleep(0.1)
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
        sleep(0.1)
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

        assert self._spice.query_item("#startStopButton")
        startStopButton = self._spice.query_item("#startStopButton")

        startStopButton.mouse_click()
        sleep(1)
        startStopButton.mouse_click()

        assert self._spice.query_item("#DoneButton")
        doneButton = self._spice.query_item("#DoneButton")
        doneButton.mouse_click() 

        #check test results
        stateModel = cdm.get(cdmEndPoint)
        assert stateModel['lastResult'] == 'success'               

    def servicemenu_servicetests_frontusbporttest(self, udw):
        """
        Test Navigation and Functionality of Menu -> Tools -> Service Menu -> Service Tests -> Walk-Up USB Port Test
        """
        FRONT_USB = 1

        def addDevice(name, volume, loc, is_paired):
            try:
                udw.mainApp.UsbHostMgr.addMockStorageDevice(name, volume, loc, is_paired)
            except:
                assert False, "Failed to convert addMockDevice "+name+" to boolean. response: " + str(result) 

        def removeDevice(name):
            try:
                udw.mainApp.UsbHostMgr.removeMockStorageDevice(name)
            except:
                assert False, "Failed to convert removeMockStorage"+name+" to boolean. response: " + str(result)
 
        result = udw.mainApp.UsbHostMgr.numStorageDevices()
        try:
            res = int(result)
        except Exception:
            assert False, "numStorageDevices failed to convert response to int. response: " + str(result)

        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_servicetests_usbfrontporttest)
        assert currentScreen

        button = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_servicetests_frontusbporttest_start)
        button.mouse_click()
        
        self.verify_toast_message("Cannot read the USB device. The device might be corrupt.")

        # Wait for toast dismiss
        sleep(3.75)

        logging.info("No Devices Test Successful.")

        #
        # Test front device - front/rear present
        #
        addDevice("front", "front_folder", FRONT_USB, False)

        logging.info("Front device inserted. Initiating Front Test...")  
      
        button.mouse_click()  

        self.verify_toast_message("USB Device Connected")

        logging.info("Front Test Successful. Front device found and triggers success message.")

        # #
        # #Test No Device present
        # #
        print("Removing Device...")
        removeDevice("front")

        result = udw.mainApp.UsbHostMgr.numStorageDevices()
        try:
            res = int(result)
        except Exception:
            assert False, "numStorageDevices failed to convert response to int. response: " + str(result)
        assert res == 0, "Removing devices Failed. "+str(res)+" devices remain."

        print("Devices removed successfully. Initiating No Devices Test...")
        logging.info("Testing Complete. Returning to HomeScreen.")

    def servicemenu_servicetests_serviceinfinitehs(self, kvp, cdm, job, net, locale):
        """
        Test functionality of Menu->Tools->Service->service tests-> service infinite hs
        """

        def query_job(jobName):
            job_manager = self._spice.cdm.get(self._spice.cdm.JOB_QUEUE_ENDPOINT)
            job_list = job_manager.get('jobList')
            ret = []

            for job in job_list:
                if job["jobName"] == jobName:
                    ret.append(job["state"])
            
            return ret
        
        def validate_job_state(list = [], name = ""):
            response = query_job(name)
            timeout_counter = 10
            
            while timeout_counter > 0:

                for state in response:
                    logging.info("State: " + state)
                    if state in list:
                        return True 

                sleep(1)
                timeout_counter = timeout_counter - 1
                response = query_job(name)


            return False
        
        def validate_button(label, click = False, msg = ""):
            button = self._spice.wait_for(label)

            assert button

            if click:
                button.mouse_click()

            if msg != "":
                self.verify_toast_message(msg)

        processing_states = ["created","ready","processing","initializeProcessing"]
        canceled_states = ["cancelProcessing", "completed", "ready", ""]
        
        view_element = self._spice.wait_for("#" + kvp["view"])
        self._spice.validate_button(view_element)

        # validate print button
        validate_button(label = "#" + kvp["startButton"], click = True, msg = "Printing...")

        # cdm response
        assert validate_job_state(processing_states, kvp["report"])

        # validate cancel button
        validate_button(label = "#" + kvp["cancelButton"], click = True, msg = "Print canceled")
        
        # cdm response
        assert validate_job_state(canceled_states, kvp["report"]) or len(query_job(kvp["report"])) == 0

        # wait for toast to dismiss
        sleep(5)
        
        # return Home
        validate_button(label = "#HomeButton SpiceText", click = True)


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

    def servicemenu_serviceresets_transferkitreset(self):
        """
        Test Navigation and Functionality of Menu -> Tools -> Engineering Menu -> Service Menu -> Service Resets -> Transfer Kit Reset
        """

        currentScreen = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.view_service_serviceresets_transferkitreset)
        assert currentScreen
        logging.info("Transfer Kit Reset screen in Service Resets")
        sleep(2)

        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_serviceresets_transferkitreset_transferresetbutton)
        assert currentElement
        logging.info("Reset button working in Transfer Kit Reset screen")
        sleep(2)

        ## Workaround for goto_homescreen() not going to Home Menu.
        logging.info("Testing Complete. Returning to HomeScreen.")
        self._spice.wait_for("#HomeButton SpiceText").mouse_click(0,6)

    def perform_region_reset(self):
        resetButton = self._spice.query_item("#ResetButton")
        resetButton.mouse_click()
