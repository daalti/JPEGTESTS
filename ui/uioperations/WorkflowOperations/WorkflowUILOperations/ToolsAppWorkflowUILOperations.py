
from time import sleep
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowUICommonOperations import ToolsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds



class ToolsAppWorkflowUILOperations(ToolsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        
    def test_maintenance_regionreset(self):
        resetButton = self._spice.wait_for("#ResetButton SpiceText")
        resetButton.mouse_click()
        # Wait for the cdm actions to show results in the progress screen
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_restoreSettings_regionreset)
        assert self._spice.wait_for("#genericResultView")
        genResultView = self._spice.query_item("#genericResultView")
        assert bool(genResultView.__getitem__("result")) == True
        resultTimer = genResultView.__getitem__("timerResult")
        assert resultTimer == 10000
        # Go back to the maintenance app home page.
        okButton = self._spice.wait_for("#okResetViewButton")
        okButton.mouse_click()

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