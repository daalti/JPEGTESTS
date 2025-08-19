
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxDiagnosticWorkflowUICommonOperations import FaxDiagnosticWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration
class FaxDiagnosticWorkflowUIXSOperations(FaxDiagnosticWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations

    def servicemenu_faxdiagnosticsmenu_hookoperations(self, cdm, spice, udw):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Service -> Fax DIagnostics -> Hook Operations
        '''
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---extra small screen--: {printerName}')

        # Wait for view
        current_element = spice.wait_for("#hookOperationsView")
        assert current_element

        # Go off hook to enable hook operations
        current_element = spice.wait_for("#goOffHookButtonModel")
        current_element.mouse_click()

        configModel = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)

        # Test onHookEnabled        
        assert configModel['onHookEnabled'] == 'false'      #moreto, marconi

        # Test current
        assert configModel['readLineCurrent'].find("mA")

        # Test voltage
        assert configModel['readLineVoltage'].find("Volts")

    #moreto, marconi
    def faxdiagnostics_ringsettings_on(self, spice, udw, enableOption = False):
        logging.info("Goto Ring Settings On")
        pbxRingDetectToggleSwitch = spice.wait_for("#pbxRingDetectSwitch")
        if(pbxRingDetectToggleSwitch ["checked"] != enableOption):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            time.sleep(1)
            assert pbxRingDetectToggleSwitch ["checked"] == enableOption, "PBX Ring Detect Enable/Disbale failed"
        ringIntervalSpinBox = spice.wait_for("#ringIntervalSpinBox")
        ringIntervalSpinBox.__setitem__('value', "400")
        scrollbar = spice.wait_for("#ringSettingsScrollBar")
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)
        ringFrequencySpinBox = spice.wait_for("#ringFrequencySpinBox")
        ringFrequencySpinBox.__setitem__('value', "99")
        time.sleep(2)
        currentElement = spice.wait_for("#doneButton")
        currentElement.mouse_click()
        time.sleep(2)          