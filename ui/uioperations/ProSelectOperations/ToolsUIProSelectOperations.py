#########################################################################################
# @file      ToolsUIProSelectOperations.py
# @author    Srinivas
# @date      27-01-2022
# @brief     Interface for all the Fax Diagnostics methods.
#            Interface for service pin methods.
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################

import random
from time import sleep
import logging
import re
import time
from dunetuf.ui.uioperations.BaseOperations.IToolsUIOperations import IToolsUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import ProSelectHybridKeyboardOperations

_logger = logging.getLogger(__name__)


class ToolsUIProSelectOperations(IToolsUIOperations):

    ALERT_TOAST_MESSAGE = "#ToastSystemToastStackView #ToastBase #ToastRowItem #ToastInfoText"
    LOC_STR_ID_PRINTING = "cPermissionPrintingApp"
    LOC_STR_ID_CANCELED = "cPrintCanceled"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    # Service Pin operations
    def servicePin_test(self, udw):
        '''
        Tests the service pin menu.
        Menu->Tools->Service->ServicePinPrompt
        '''    
        DEFAULT_PIN = "08675309"
        ADMIN_PIN = "Pass5742"
        self.proselect_UI_Hybrid_operations= ProSelectHybridKeyboardOperations(self._spice)

        self.udw = udw
        self._uiTheme = self.udw.mainUiApp.ApplicationEngine.getTheme()

        self._spice.homeMenuUI().menu_navigation(self._spice, "#MenuListtools", "#0e49b040-ed7c-4b11-8dd2-f8acc500760aMenuButton")
        
        if self._uiTheme == "hybridTheme":
            keyboardTextField = self._spice.wait_for("#hybridKeyboardTextInputArea")
            keyboardTextField["inputText"] = ADMIN_PIN
            self.proselect_UI_Hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)
            self._spice.wait_for("#accessDeniedMessage")

            self._spice.homeMenuUI().menu_navigation(self._spice, "#MenuListtools", "#0e49b040-ed7c-4b11-8dd2-f8acc500760aMenuButton")
            keyboardTextField = self._spice.wait_for("#hybridKeyboardTextInputArea")
            keyboardTextField["inputText"] = DEFAULT_PIN
            self.proselect_UI_Hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)

        else:
            keyboard =  self._spice.wait_for("#spiceKeyboardView")
            assert keyboard

            keyboard.__setitem__('currentText', ADMIN_PIN)
            while (self._spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
                keyboard.mouse_wheel(0,0)
                sleep(1)
            keyboard.mouse_click()

            assert self._spice.wait_for("#accessDeniedMessage")
            toolsScreen = self._spice.query_item("#MenuListtools")
            self._spice.wait_until(lambda: toolsScreen["enabled"] == True, 20)
            self._spice.wait_for("#0e49b040-ed7c-4b11-8dd2-f8acc500760aMenuButton").mouse_click()

            keyboard =  self._spice.wait_for("#spiceKeyboardView")
            assert keyboard

            sleep(1)
            keyboard.__setitem__('currentText', DEFAULT_PIN)
            sleep(1)

            while (self._spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
                keyboard.mouse_wheel(0,0)
                sleep(1)
            keyboard.mouse_click()

        assert self._spice.wait_for("#MenuListLayout")
        logging.info("At Service Screen")
        sleep(1)

    # Single Modem Tone flow operations

    def troubleshoot_fax_runFaxTest(self):
        '''
        Checks the runFax test messages submitted thorugh
        Menu->Tools->Troubleshooting->Fax->Run Fax Test
        '''
        assert self._spice.wait_for("#ToastSystemToastStackView")
        assert self._spice.query_item("#ToastInfoText")["text"] == "Processing"
    
    def troubleshoot_fax_PBXRingDetect(self, cdm):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Troubleshooting -> Fax -> PBX Ring Detect
        '''
        def assert_pbx_ring_detect_proselect(current_element, bool):
            current_element.mouse_wheel(180,180)
            current_element.mouse_click()
            current_element = self._spice.wait_for("#faxTroubleshootingMenuButton")
            current_element.mouse_click()
            cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
            sleep(0.25)
            assert cdm_model['ringSettings']['pbxRingDetectEnabled'] == bool

        current_element = self._spice.wait_for("#pbxRingDetectView")
        assert current_element

        # validate on button
        assert_pbx_ring_detect_proselect(current_element, "true")
            
        # validate off button
        current_element.mouse_wheel(180,180)
        sleep(0.25)
        assert_pbx_ring_detect_proselect(current_element, "false")

        # validate back button
        sleep(0.25)
        current_element.mouse_click()
        current_element = self._spice.wait_for("#faxTroubleshootingMenuButton")
        assert current_element

    def troubleshoot_fax_clearFaxMemoryLog(self):
        '''
        Clears the Fax Memory Logs submitted throuhj
        Menu -> Tools -> Troubleshooting -> Fax -> Clear Fax Log/Memory
        '''
        currentElement = self._spice.wait_for("#clearFaxLogMemoryView")
        assert currentElement

        # validate clear button
        for i in range(2):
            currentElement.mouse_wheel(180,180)
            sleep(0.2)

        currentElement.mouse_click()
        assert self._spice.wait_for("#ToastSystemToastStackView")
        assert self._spice.query_item("#ToastInfoText")["text"] == "Success"
        sleep(3.5)

        # validate cancel button
        currentElement.mouse_wheel(180,180)
        currentElement.mouse_click()
        currentElement = self._spice.wait_for("#faxTroubleshootingMenuButton")
        assert currentElement

        # validate back button
        currentElement.mouse_click()
        currentElement.mouse_click()
        currentElement = self._spice.wait_for("#faxTroubleshootingMenuButton")
        assert currentElement

    def troubleshoot_fax_faxT30RepMode(self, cdm):
        '''
        Test Navigation and Functionality of Menu->Tools->Troubleshooting->Fax->Fax T.30 Rep Mode
        '''
        faxT30 = cdm.get(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT)
        setVal = faxT30['analogFaxOperation']['t30ReportMode']
        currentElement = self._spice.wait_for("#MenuSelectionListfaxT30RepMode")
        assert currentElement

        #ui_string = spice.query_item("#RadioButtonListLayout",0)["text"]
        currentElement.mouse_wheel(180,180)
        currentElement.mouse_click()

        sleep(1)
        generateTone = cdm.get(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT)
        assert generateTone['analogFaxOperation']['t30ReportMode'] != setVal, "Modify operation failed"

    def troubleshooting_print_quality_image_registration(self, cdm, tray):
        currentElement = self._spice.query_item("#BackButton #SpiceButton")
        currentElement.mouse_click()

    def servicemenu_servicetests_continuousflatbedtest(self,net):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service tests-> Continous Flat bed test
        """
        view = self._spice.wait_for("#continuousFlatbedView")

        view.mouse_wheel(180,180)
        assert self._spice.query_item("#proceedButton")["activeFocus"] is True
        proceed_button = self._spice.wait_for("#proceedButton SpiceText")

        proceed_button.mouse_click()
        # validate the ToastSystem layout with Procession message
        assert self._spice.wait_for("#ToastBase")
        processmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeProcessing")
        assert processmsg in self._spice.query_item("#ToastBase #ToastRowItem #ToastInfoText")["text"]
        sleep(3.5)

        view.mouse_wheel(180,180)
        assert self._spice.query_item("#dismissButton")["activeFocus"] is True
        dismiss_button = self._spice.wait_for("#dismissButton SpiceText")

        dismiss_button.mouse_click()
        # validate the ToastSystem layout with Cancel Procession message
        assert self._spice.wait_for("#ToastBase")
        assert "Canceling" in self._spice.query_item("#ToastBase #ToastRowItem #ToastInfoText")["text"]
        sleep(3.5)

    def servicemenu_servicetests_displaytest(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service tests-> Display test
        """
        self._spice.wait_for("#displayTest")

        #start the test
        for x in range(10):
            currentElement = self._spice.wait_for("#proceedButton SpiceText")
            if currentElement["text"] != "Cancel":
                currentElement.mouse_click()
            else:
                break
        # Check if the Test passed
        titleText = self._spice.wait_for("#TitleText SpiceText")
        assert titleText['text'] == "Test passed", "Test Passed Message is not found in Title Text"
        currentElement.mouse_click()

    def servicemenu_servicetests_continuousadfpicktest(self,net):
        """
        Test Navigation and Functionality of Menu -> Tools -> Engineering Menu -> Service Menu -> Service Tests -> Continuous ADF Pick Test
        """
        view = self._spice.wait_for("#continuousADFPickView")

        view.mouse_wheel(180,180)
        assert self._spice.query_item("#proceedButton")["activeFocus"] is True
        proceed_button = self._spice.wait_for("#proceedButton SpiceText")

        proceed_button.mouse_click()
        # validate the ToastSystem layout with Procession message
        assert self._spice.wait_for("#ToastBase")
        processmsg = self._spice.common_operations.get_expected_translation_str_by_str_id(net, "cJobStateTypeProcessing")
        assert processmsg in self._spice.query_item("#ToastBase #ToastRowItem #ToastInfoText")["text"]

        sleep(3.5)

        view.mouse_wheel(180,180)
        assert self._spice.query_item("#dismissButton")["activeFocus"] is True
        dismiss_button = self._spice.wait_for("#dismissButton SpiceText")

        dismiss_button.mouse_click()
        # validate the ToastSystem layout with Cancel Procession message
        assert self._spice.wait_for("#ToastBase")
        assert "Canceling" in self._spice.query_item("#ToastBase #ToastRowItem #ToastInfoText")["text"]
        sleep(3.5)

    def servicemenu_servicetests_scanmotortest(self):
        """
        Test Navigation and Functionality of Menu -> Tools -> Engineering Menu -> Service Menu -> Service Tests -> Scan Motor Test
        """
        view = self._spice.wait_for("#scanMotorTestView")

        while(self._spice.query_item("#startButton")['activeFocus'] != True):
            view.mouse_wheel(180, 180)
            sleep(0.5)

        button = self._spice.wait_for("#startButton")

        for count in range(5): #0-4
            view = self._spice.query_item("#scanMotorTestView")
            assert count == view['cycleCount']
            button.mouse_click()
            sleep(1)

        #5
        view = self._spice.query_item("#scanMotorTestView")
        assert 5 == view['cycleCount']

    def servicemenu_faxdiagnosticsmenu_generatedialingtonespulsesmenu(self, cdm, cdmEndPoint, methods):
        currentElement = self._spice.wait_for("#generatePulseToneBurstView")
        assert currentElement
        # Here check the cdm get() of diagnosticOperation.
        # This shows we entered menu with diagnostics turned on
        stateModel = cdm.get(cdmEndPoint)
        assert stateModel
        assert stateModel['state'] == "idle"
        for method in methods:  
            while (self._spice.query_item("#valueInputButton")["activeFocus"] == False):
                currentElement.mouse_wheel(180, 180)
                sleep(0.2)
            currentElement.mouse_click()
            
            keyboard = self._spice.wait_for("#spiceKeyboardView")
            keyboard.__setitem__('currentText', 1)
            while (self._spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
                keyboard.mouse_wheel(0,0)
                sleep(0.2)
            keyboard.mouse_click()
            while (self._spice.query_item("#startStopButton")["activeFocus"] == False):
                currentElement.mouse_wheel(180, 180)
                sleep(0.2)
            # Start Button Click
            currentElement.mouse_click()
            sleep(0.2)
            
            #Stop button click
            currentElement.mouse_click()
            #check test results
            stateModel = cdm.get(cdmEndPoint)
            assert stateModel['lastResult'] == 'success'
            while (self._spice.query_item(method)["activeFocus"] == False):
                currentElement.mouse_wheel(0, 0)
                sleep(0.2)
            currentElement.mouse_click()

    def servicemenu_servicetests_frontusbporttest(self, udw):
        """
        Test to validate Service Tests, Front Usb Port
        """
        REAR_USB = 2
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

        def assertToastMessage(msg):
            self._spice.wait_for("#ToastBase")
            assert msg in self._spice.query_item("#ToastBase #ToastRowItem #ToastInfoText")['text']
            sleep(3.5)

        view = self._spice.wait_for("#usbFrontPortTest")

        #locate proceed button
        while(self._spice.query_item("#proceedButton")['activeFocus'] != True):
            view.mouse_wheel(180,180)
            sleep(0.5)

        proceedButton = self._spice.wait_for("#proceedButton SpiceText")

        # #
        # # Test front device - front/rear present
        # #
        addDevice("front", "front_folder", FRONT_USB, False)
        print("Front device inserted. Initiating Front Test...")
        proceedButton.mouse_click()
        assertToastMessage("USB Device Connected")
        print("Front Test Successful. Front device found and triggers success message.")

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
        proceedButton.mouse_click()
        assertToastMessage("Cannot read the USB device")
        print("No Devices Test Successful.")

        print("Testing Complete. Returning to HomeScreen.")
    
    def servicemenu_servicetests_faxdiagnostictest(self, cdm, cdmEndPoint, ringInterval, ringFrequency):
        try:
            logging.info("Attempting get() on diagnosticOperation")
            w = cdm.get(cdmEndPoint)
        except:
            assert False, "Failed to GET " + cdmEndPoint
        # Navigate to Ring Interval
        currentScreen = self._spice.wait_for("#ringSettings")
        currentScreen.mouse_wheel(180, 180)
        sleep(0.2)
        assert self._spice.query_item("#ringIntervalButton SpiceText")
        currentScreen.__setitem__('ringInterval', ringInterval)

        # Navigate to Ring Frequency
        currentScreen.mouse_wheel(180, 180)
        sleep(0.2)
        assert self._spice.query_item("#ringFrequencyButton SpiceText")
        
        currentScreen.__setitem__('ringFrequency', ringFrequency)

        # Navigate to PBX
        currentScreen.mouse_wheel(180, 180)
        sleep(0.2)
        assert self._spice.query_item("#ringPBXButton SpiceText")
        currentScreen.mouse_click()
        currentScreen = self._spice.wait_for("#setPBXDetectView")

        # Set dial to True
        currentScreen.mouse_wheel(180, 180)
        sleep(1)
        assert self._spice.query_item("#pbxEnabled")        

        # Check original state and set to opposite state
        expectedPbxState = "true"

        if w["ringSettings"]["pbxRingDetectEnabled"] == "true":
            logging.info("Selecting False, move Dial")
            expectedPbxState = "false"
            currentScreen.mouse_wheel(180, 180)
            sleep(0.2)
        else:
            logging.info("Selecting True, dont move Dial")

        currentScreen.mouse_click()
        currentScreen = self._spice.wait_for("#ringSettings")
        sleep(1)

        # Set ring settings
        currentScreen.mouse_wheel(180, 180)
        sleep(1)

        currentScreen.mouse_click()
        sleep(1)

        # Compare and check CDM Endpoint
        try:
            logging.info("Attempting get() on diagnosticOperation")
            w = cdm.get(cdmEndPoint)
        except:
            assert False, "Failed to GET " + cdmEndPoint

        assert w["ringSettings"]["pbxRingDetectEnabled"]==expectedPbxState, "ERROR: PBX state does not match"
        assert w["ringSettings"]["ringInterval"]==ringInterval, "ERROR: Ring interval (" +w["ringSettings"]["ringInterval"]+ ") does not match (" +ringInterval+ ")"
        assert w["ringSettings"]["ringFrequency"]==int(ringFrequency), "ERROR: Ring frequency (" +w["ringSettings"]["ringFrequency"]+ ") does not match (" +ringFrequency+ ")"

    def test_maintenance_regionreset(self):
        # self._spice.homeMenuUI().menu_navigation(self._spice, "#ResetPrinterSupplyRegionView", "#ResetButton")
        buttonObjectId = "#ResetButton"
        direction = "DOWN"
        index = 0
        currentScreen = self._spice.wait_for("#ResetPrinterSupplyRegionView")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        while self._spice.query_item(buttonObjectId, index)["activeFocus"] == False:
            assert timeSpentWaiting < self.maxtimeout
            if direction == "DOWN":
                logging.info("scrolling down")
                currentScreen.mouse_wheel(180,180)
            else:
                logging.info("scrolling up")
                currentScreen.mouse_wheel(0,0)
            timeSpentWaiting = time.time() - startTime
            # Reduce the time spent searching to stay within the overall test timeout
            if timeSpentWaiting > self.maxtimeout / 10.0:
                # Haven't found it yet.  Try scrolling up instead
                direction = "UP"
            logging.info("Time spent waiting is {}/{}".format(timeSpentWaiting, self.maxtimeout))

        # Wait for the cdm actions to show results in the progress screen
        sleep(2)

    def servicemenu_serviceresets_transferkitreset(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service resets-> transfer kit reset
        """
        currentScreen = self._spice.wait_for("#TCUnitResetView")
        assert currentScreen

        #locate reset button
        while(self._spice.query_item("#resetButton")['activeFocus'] != True):
            currentScreen.mouse_wheel(180,180)
            sleep(1)

        # validating Reset Button
        currentElement = self._spice.wait_for("#resetButton SpiceText")
        assert currentElement
        currentElement.mouse_click()
        logging.info("Reset button works as expected.")
        sleep(2)

    def check_toast_message(self, text):
        toastMessage = self._spice.query_item(self.ALERT_TOAST_MESSAGE)
        #print("Title message=",str(toastMessage["text"]))
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)

    def get_loc_string(self, loc_str_id, net, locale):
        loc_msg = LocalizationHelper.get_string_translation(net, loc_str_id, locale)
        logging.info("Localized string: %s", loc_msg)
        return loc_msg 

    # helper function to check if job is in jobQueue
    def check_jobmanager_queue(self, name):
        jobQueueResponse = self._spice.cdm.get(self._spice.cdm.JOB_QUEUE_ENDPOINT)
        jobQueue = jobQueueResponse.get('jobList')
        logging.info("Job Queue size <%d>", len(jobQueue))
        for job in jobQueue:
            if job["jobName"] == name:
                return True

        return False

    def servicemenu_servicetests_serviceinfinitehs(self, kvp, cdm, job, net, locale):
        """
        Test functionality of Menu->Tools->Service->service tests-> service infinite hs
        """
        INFINITEHS_STRING_ID = "#ServiceAppApplicationStackView #nativeStackView"
        self.dial_common_operations = ProSelectCommonOperations(self._spice)

        loc_msg = self.get_loc_string(self.LOC_STR_ID_PRINTING, net, locale)
        logging.info("Localized string: %s", loc_msg)

        # validate infinite h service print button
        self.dial_common_operations.goto_item("#" + kvp["testStart"], "#" + kvp["proSelectView"])
        #Validate Toast message.
        self.check_toast_message(loc_msg)
        sleep(5)
        if kvp["view"] == "serviceInfiniteHs":
            assert self.check_jobmanager_queue("Infinite H's (Black Only)")
        else:
            assert self.check_jobmanager_queue("Infinite H's (Color)")
        
        loc_msg = self.get_loc_string(self.LOC_STR_ID_CANCELED, net, locale)
        logging.info("Localized string: %s", loc_msg)
        view = self._spice.wait_for(INFINITEHS_STRING_ID + " " + "#" + kvp["proSelectView"])
        while(self._spice.query_item("#MessageLayout " + "#" + kvp["testCancel"])['visible'] != True):
            view.mouse_wheel(180, 180)
            sleep(0.5)
        # validate infinite h service cancel button
        self.dial_common_operations.goto_item("#" + kvp["testCancel"], "#" + kvp["proSelectView"])
        #Validate Toast message.
        self.check_toast_message(loc_msg)

        #Validate H page print cancel successfully.
        job_info_url = job.get_current_job_url("print")
        if job_info_url:
            current_job_info = cdm.get(job_info_url)
            jobstate = job.wait_for_job_completion_cdm(str(current_job_info["jobId"]), 300)
            logging.info("Job state: %s", jobstate)
            assert 'cancelled' in jobstate, f"Unexpected job state - {jobstate}."
            
        else:
            logging.warning("Failed to get cancel job status from job queue, will check it with job history")

    def perform_region_reset(self):
        self._spice.homeMenuUI().menu_navigation(self._spice, "#ResetPrinterSupplyRegionView", "#ResetButton")

    def validate_tools_reports_event_log(self,spice,qml,eventName,descText,validate):
        eventRow = self._spice.wait_for("#49.01.04 #SpiceButton")
        eventRow.mouse_click()
        eventDetails = self._spice.wait_for("#eventLogInfoView #ValueText")
        assert descText == qml.query_item("#descriptionNode #ValueText")["text"]
        print("TEST value:{}, {}".format(eventRow["text"], eventDetails))

    def validate_user_activity_fw_update(self, spice):
        # Wait for screen asking if should check for update
        current_screen = spice.wait_for("#checkForUpdateYesButton",30)
        # Click yes for check for update
        current_screen.mouse_click()

        #Printer check for the update if available
        not_avbl = spice.wait_for("#fwupdateNotAvailableOk", 120)
        # Click OK
        not_avbl.mouse_click()

        # Wait to get back to maintenance screen
        current_screen = spice.wait_for("#MenuListtools",30)