
import logging
import time
import sys
from dunetuf.fax.fax import *
from dunetuf.ui.uioperations.BaseOperations.IFaxDiagnosticUIOperations import IFaxDiagnosticUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.power.power import Power, ActivityMode
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.configuration import Configuration

fax_modem_uri = "cdm/faxModem/v1/configuration"
fax_receive_uri = "cdm/faxReceive/v1/configuration"
fax_resource_uri = "cdm/jobTicket/v1/configuration/defaults/receiveFax"
fax_forward_uri = "cdm/fax/v1/faxForwardConfiguration"

class FaxDiagnosticWorkflowUICommonOperations(IFaxDiagnosticUIOperations):

    def __init__(self, spice):
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.maxtimeout = 120
        self._spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuAppWorkflowUISObjectIds = MenuAppWorkflowObjectIds()

    def single_modem_tone(self, cdm):
        '''
        Navigates to Single modem tone.
        UI Flow is Home->Service->Fax Diagnostic ->Single Modem Tone
        '''
        logging.info("Start writing the common operations")
        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_1300Hz)
        currentElement.mouse_click()
        time.sleep(1)

        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_startstop)
        currentElement.mouse_click()
        time.sleep(5)

        generateTone = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert generateTone["state"] == "processing", "Modify operation failed"
        time.sleep(1)

        currentElement = self._spice.wait_for(self.MenuAppWorkflowUISObjectIds.menu_button_service_faxdiagnostics_singlemodemtone_startstop)
        currentElement.mouse_click()
        time.sleep(2)

        generateTone = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert generateTone["state"] == "idle", "Modify operation failed"

    def servicemenu_faxdiagnosticsmenu_hookoperations(self, cdm, spice, udw):
        '''
        Test Navigation and Functionality of Menu -> Tools -> Service -> Fax DIagnostics -> Hook Operations
        '''
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---common screen--: {printerName}')

        # Wait for view
        current_element = spice.wait_for("#hookOperationsView")
        assert current_element

        # Go off hook to enable hook operations
        current_element = spice.wait_for("#goOffHookButtonModel")
        current_element.mouse_click()

        configModel = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)

        # Test onHookEnabled
        # moretohi, marconi, marconihipdl, lotus, selene => true
        if printerName == "camden" or printerName == "jasper" or printerName == "pearl" or printerName == "morganite" or printerName == "selene":            
            assert configModel['onHookEnabled'] == 'false'
        else:
            assert configModel['onHookEnabled'] == 'true'

        # Test current
        assert configModel['readLineCurrent'].find("mA")

        # Test voltage
        assert configModel['readLineVoltage'].find("Volts")        
        
    def faxdiagnostics_onhook_refresh(self, spice, udw):
        currentScreen = spice.wait_for(FaxAppWorkflowObjectIds.go_on_hook)
        logging.info("Go On Hook Operations View")
        # Query On Hook Operations
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.go_on_hook)
        currentElement.mouse_click()
        logging.info("Starting refresh")
        currentElementhomeButton = spice.wait_for(FaxAppWorkflowObjectIds.refresh_button)
        currentElementhomeButton.mouse_click()
        time.sleep(2)
        logging.info("Go On Hook Operations View")

    def faxdiagnostics_offhook_refresh(self, spice, udw):
        #self.goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(spice, udw)
        currentScreen = spice.wait_for(FaxAppWorkflowObjectIds.go_off_hook)
        logging.info("Go Off Hook Operations View")
        # Query On Hook Operations
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.go_off_hook)
        currentElement.mouse_click()
        currentElementhomeButton = spice.wait_for(FaxAppWorkflowObjectIds.refresh_button)
        currentElementhomeButton.mouse_click()
        logging.info("Starting refresh")
        time.sleep(2)
        logging.info("Go Off Hook Operations View")
        spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service_faxdiagnostics_hookoperations)
        currentElementhomeButton = spice.wait_for(FaxAppWorkflowObjectIds.button_home)
        currentElementhomeButton.mouse_click()

    def verifyfaxmodemmode(self, cdm, state):
        cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_OPERATION)
        assert cdm_model
        logging.info(cdm_model)
        if hasattr(cdm_model, 'lastResult'):
            assert cdm_model['lastResult'] == 'success'
        else:
            assert cdm_model['state'] == state        

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
                # current_button = self._spice.query_item("#generateRandomDataViewlist1 " + option)
                current_button = spice.query_item(option)
                sleep(1)
                current_button.mouse_click()
            scroll_value = scroll_value + 0.06

        view = spice.wait_for("#startStopButton")
        view.mouse_click()
        sleep(1)

        self.verifyfaxmodemmode(cdm,'processing')
        
        view = spice.wait_for("#startStopButton")
        view.mouse_click()
        sleep(1)

        self.verifyfaxmodemmode(cdm,'idle')        

    def generate_dial_phone_no(self,cdm,spice,udw):
        logging.info("Fax Diagnostic Generate/Dial phone no!")

        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---common screen--: {printerName}')

        faxNumber = 101
        endpoint = cdm.FAX_MODEM_DIAGNOSTIC_OPERATION
        #Here check the cdm get() of diagnosticOperation. This shows we entered menu with diagnostics turned on
        stateModel = cdm.get(endpoint)
        logging.info(stateModel)
        assert stateModel
        assert stateModel['state'] == 'idle'
        
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

        #Check CDM get. 
        stateModel = cdm.get(endpoint)
        assert stateModel
        assert stateModel['state'] == 'idle'        #For moreto, marconi

        sleep(5)

        #Click Done Button
        currentRadioButton = spice.wait_for("#DoneButton")
        currentRadioButton.mouse_click()

        logging.info("Fax Diagnostic Generate/Dial phone no completed")        

    def faxdiagnostics_randomdata_v21300(self, spice, udw):
        logging.info("Go to Generate Random Data v.21.300")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v21300, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v21300)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.21.300")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.21.300")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v17_14400(self, spice, udw):
        logging.info("Go to Generate Random Data v.17 14.4K")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v1714400, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v1714400)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.17 14.4K")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.17 14.4K")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v17_12000(self, spice, udw):
        logging.info("Go to Generate Random Data v.17 12.0K")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v1712000, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v1712000)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.17 12.0K")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.17 12.0K")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v29_9600(self, spice, udw):
        logging.info("Go to Generate Random Data v.29 9600")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v299600, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v299600)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.29 9600")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.29 9600")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v29_7200(self, spice, udw):
        logging.info("Go to Generate Random Data v.29 9600")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v297200, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v297200)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.29 9600")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.29 9600")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v27_4800(self, spice, udw):
        logging.info("Go to Generate Random Data v.27 4800")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v274800, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v274800)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.27 4800")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.27 4800")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v27_2400(self, spice, udw):
        logging.info("Go to Generate Random Data v.27 2400")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v272400, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v272400)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.27 2400")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.27 2400")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_33600(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 33600")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v3433600, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3433600)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 33600")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 33600")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_31200(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 31200")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v3431200, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3431200)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 31200")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 31200")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_28800(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 28800")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.radioButton_v3428800, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3428800)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 28800")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 28800")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()        

    def faxdiagnostics_randomdata_v34_26400(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 264000")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.26)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3426400)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 264000")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 264000")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_24000(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 24000")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.28)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3424000)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 24000")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 24000")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_21600(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 21600")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.3)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3421600)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 21600")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 21600")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_19200(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 19200")
        # self.workflow_common_operations.goto_item(
        #     FaxAppWorkflowObjectIds.radioButton_v3421600, 
        #     FaxAppWorkflowObjectIds.view_service_faxdiagnostics_generaterandomdata,  
        #     select_option = False, 
        #     scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.33)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3419200)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 19200")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 19200")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_16800(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 16800")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.36)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3416800)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 16800")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 16800")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_14400(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 14400")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.4)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3414400)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 14400")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 14400")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_12000(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 12000")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.43)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v3412000)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 12000")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 12000")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v34_9600(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 9600")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.46)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v349600)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 9600")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 9600")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v347200(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 7200")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.5)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v347200)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 7200")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 7200")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v344800(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 4800")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.53)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v344800)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 4800")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 4800")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342400(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2400")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.56)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342400)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2400")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2400")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v343429(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 3429")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.6)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v343429)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 3429")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 3429")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v343200H(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 3200H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.63)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v343200H)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 3200H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 3200H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v343200L(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 3200L")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.66)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v343200L)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 3200L")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 3200L")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v343000H(self, spice, udw):       
        logging.info("Go to Generate Random Data v.34 3000H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.7)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v343000H)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 3000H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 3000H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v343000L(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 3000L")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.73)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v343000L)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 3000L")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 3000L")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342800H(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2800H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.76)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342800H)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2800H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2800H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342800L(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2800L")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.8)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342800L)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2800L")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2800L")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342743H(self, spice, udw):        
        logging.info("Go to Generate Random Data v.34 2743H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.83)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342743H)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2743H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2743H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342743L(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2743L")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.86)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342743L)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2743L")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2743L")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342400H(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2400H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.9)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342400H)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2400H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2400H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_randomdata_v342400L(self, spice, udw):
        logging.info("Go to Generate Random Data v.34 2400H")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_generateRandomData)
        scrollbar.__setitem__("position",0.9)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.radioButton_v342400L)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Starting Generate Random Data v.34 2400H")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        logging.info("Done Generate Random Data v.34 2400H")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.startstopbutton)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.donebutton)
        currentElementdonebutton.mouse_click()

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
        else:
            raise logging.info(f"{dialingtone} is not supported to select")
        
        self.fax_diagnostic_lastdigit(spice, "5", configuration, dialingtone)

    def fax_diagnostic_lastdigit(self, spice, last_digit, configuration, dialingtone):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_scrollbar)
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)
        lastdigitTextBox = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_lastdigittextbox)
        if (configuration.familyname == "enterprise"):
            lastdigitTextBox.__setitem__('displayText', last_digit)
        else:            
            lastdigitTextBox.mouse_click()
            lastdigitTextBox.__setitem__('displayText', last_digit)
            okButton = self._spice.query_item("#TextView")
            okButton.mouse_click()

        # lastdigitTextBox.mouse_click()
        # self.enter_numeric_keyboard_values(last_digit)
        # time.sleep(1)

        if dialingtone == "Continuous Tone":
            time.sleep(1)
            currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
            currentElementStart.mouse_click()
            time.sleep(1)
            currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_startbutton)
            currentElementStart.mouse_click()
        time.sleep(5)
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_donebutton)
        currentElementdonebutton.mouse_click()

    def fax_diagnostic_dialingtone_start_verify_constrained_message(self, spice, configuration):
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_faxdiagnostics_generatePulseToneBurstView)

        current_button = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_pulseradiobutton)
        current_button.mouse_click()

        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_scrollbar)
        scrollbar.__setitem__("position", 0.3)

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
        okButton = self._spice.query_item("#TextView")
        okButton.mouse_click()
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
        okButton = self._spice.query_item("#TextView")
        okButton.mouse_click()
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
        scrollbar.__setitem__("position", 0.3)
        time.sleep(1)

        lastdigitTextBox = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_lastdigittextbox)
        last_digit = '43'
        lastdigitTextBox.mouse_click()
        lastdigitTextBox.__setitem__('displayText', last_digit)
        okButton = self._spice.query_item("#TextView")
        okButton.mouse_click()
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click()

        # Selected Tone Burst, enter last digit as 43 then verify the constrained message
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()

        # Click done button
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_dialing_donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_generatedialphonenumber_tone(self, spice, udw):
        #currentScreen = spice.wait_for(FaxAppWorkflowObjectIds.tone_button)
        logging.info("Go to Generate/Dial Phone Number Tone")
        # Query On Generate/Dial Phone Number Tone
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone_button)
        currentElement.mouse_click()
        logging.info("Entering Fax Number")
        time.sleep(1)
        faxTextBox = spice.wait_for(FaxAppWorkflowObjectIds.fax_number_text)
        faxTextBox.mouse_click()
        faxTextBox.__setitem__('displayText', "101") 
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click()
        time.sleep(2) 
        currentElementDial = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_phonenumber_dailbutton)
        currentElementDial.mouse_click()
        time.sleep(5)
        currentElementDial = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_phonenumber_donebutton)
        currentElementDial.mouse_click()

    def faxdiagnostics_generatedialphonenumber_pulse(self, spice, udw):
        #currentScreen = spice.wait_for(FaxAppWorkflowObjectIds.pulse_button)
        logging.info("Go to Generate/Dial Phone Number Pulse")
        # Query On Generate/Dial Phone Number Tone
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.pulse_button)
        currentElement.mouse_click()
        logging.info("Entering Fax Number")
        time.sleep(1)
        faxTextBox = spice.wait_for(FaxAppWorkflowObjectIds.fax_number_text)
        faxTextBox.mouse_click()
        faxTextBox.__setitem__('displayText', "101")
        keyboard_ok_button = spice.wait_for(FaxAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyboard_ok_button.mouse_click() 

        time.sleep(2)
        currentElementDial = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_phonenumber_dailbutton)
        currentElementDial.mouse_click()
        time.sleep(5)
        currentElementDial = spice.wait_for(FaxAppWorkflowObjectIds.diagnostic_phonenumber_donebutton)
        currentElementDial.mouse_click()

    def faxdiagnostics_generatesinglemodemtone_1100(self, spice, udw):
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone1100)
        currentElement.mouse_click()
        logging.info("clicking on tone 1100")
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button, timeout=10)
        currentElementStart.mouse_click()
        time.sleep(2)
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElementStop.mouse_click()
        time.sleep(2)
        currentElementhomeButton = spice.wait_for(FaxAppWorkflowObjectIds.button_home)
        currentElementhomeButton.mouse_click()

    def faxdiagnostics_generatesinglemodemtone_1800(self, spice, udw):
        self.homemenu.menu_navigation(self._spice,FaxAppWorkflowObjectIds.view_optionsScreen, FaxAppWorkflowObjectIds.fax_schedule_view, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
        logging.info("Go to Generate Single Modem Tone 1800")
        #Query on Generate Single Modem Tone 1800
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone1800)
        currentElement.mouse_click()
        logging.info("clicking on tone 1800")
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElement.mouse_click()
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElement.mouse_click()
        currentElementhomeButton = spice.wait_for(FaxAppWorkflowObjectIds.button_home)
        currentElementhomeButton.mouse_click()

    def faxdiagnostics_faxtransmitsignal_loss(self, spice, udw):
        logging.info("Fax transmit signal loss")
        #currentElement = spice.wait_for(FaxAppWorkflowObjectIds.up_button)
        #currentElement.mouse_click()
        signalLossTextBox = spice.wait_for(FaxAppWorkflowObjectIds.signal_level)
        signalLossTextBox.__setitem__('value', "11")
        time.sleep(2)
        logging.info("Clicking on Proceed Button")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.proceed_button)
        currentElement.mouse_click()
        time.sleep(2)

    def faxdiagnostics_ringsettings_on(self, spice, udw, enableOption = False):
        logging.info("Goto Ring Settings On")
        pbxRingDetectToggleSwitch = spice.wait_for(FaxAppWorkflowObjectIds.pbx_ringdetect_switch)
        if(pbxRingDetectToggleSwitch ["checked"] != enableOption):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            time.sleep(1)
            assert pbxRingDetectToggleSwitch ["checked"] == enableOption, "PBX Ring Detect Enable/Disbale failed"
        ringIntervalSpinBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_interval_spinbox)
        ringIntervalSpinBox.__setitem__('value', "400")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_ringSettings)
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)
        ringFrequencySpinBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_frequency_spinbox)
        ringFrequencySpinBox.__setitem__('value', "99")
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.save_button)
        currentElement.mouse_click()
        time.sleep(2)


    def faxdiagnostics_ringsettings_off(self, spice, udw, enableOption = False):
        logging.info("Goto Ring Settings Off")
        pbxRingDetectToggleSwitch = spice.wait_for(FaxAppWorkflowObjectIds.pbx_ringdetect_switch)
        if(pbxRingDetectToggleSwitch ["checked"] != enableOption):
            pbxRingDetectToggleSwitch.mouse_click(10,10)
            time.sleep(1)
            assert pbxRingDetectToggleSwitch ["checked"] == enableOption, "PBX Ring Detect Enable/Disbale failed"
        time.sleep(1)            
        ringIntervalSpinBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_interval_spinbox)
        ringIntervalSpinBox.__setitem__('value', "400")
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_ringSettings)
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)
        ringFrequencySpinBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_frequency_spinbox)
        ringFrequencySpinBox.__setitem__('value', "99")
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.save_button)
        currentElement.mouse_click()
        time.sleep(2)

    def faxdiagnostics_ringsettings_set_frequency(self, spice, udw, frequency_value):
        time.sleep(2)
        logging.info("updating the Ring frequency value")
        ringFrequencyTextBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_frequency_spinbox)
        ringFrequencyTextBox.__setitem__('value', frequency_value)
        time.sleep(2)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.save_button)
        currentElement.mouse_click()        
        time.sleep(2)  

    def faxdiagnostics_ringsettings_get_frequency(self, spice, udw):
        time.sleep(2)
        #getting the ring frequency value from the spinbox
        ringFrequencyTextBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_frequency_spinbox)
        item_value = ringFrequencyTextBox.__getitem__('value')
        time.sleep(2)
        return item_value

    def faxdiagnostics_ringsettings_set_interval(self, spice, udw, interval_value):
        time.sleep(2)
        logging.info("updating the Ring interval value")
        ringIntervalTextBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_interval_spinbox)
        ringIntervalTextBox.__setitem__('value', interval_value)
        time.sleep(2)
        scrollbar = spice.wait_for(FaxAppWorkflowObjectIds.scrollBar_ringSettings)
        scrollbar.__setitem__("position",0.2)
        time.sleep(1)

    def faxdiagnostics_ringsettings_get_interval(self, spice, udw):
        time.sleep(2)
        #getting the ring interval value from the spinbox
        ringIntervalTextBox = spice.wait_for(FaxAppWorkflowObjectIds.ring_interval_spinbox)
        item_value = ringIntervalTextBox.__getitem__('value')
        time.sleep(2)
        return item_value
    
    def faxdiagnostics_faxSpeedSelection_v29speed9600(self, spice, udw):
        logging.info("Goto V29 9600 off")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.v29speed_9600)
        currentElement.mouse_click()
        time.sleep(2)

    def faxdiagnostics_faxSpeedSelection_v29speed7200(self, spice, udw):
        logging.info("Goto V29 7200 on")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.v29speed_7200)
        currentElement.mouse_click()
        time.sleep(2)

    def faxdiagnostics_get_faxSpeedSelection(self, spice, udw):
        state = spice.wait_for(FaxAppWorkflowObjectIds.v29speed_7200)
        time.sleep(2)
        if(state["checked"]==True):
            return True
        else:
            return False
        
    def fax_receivejob_after_v29_speed_selection(self, spice, setup_fax_using_cdm, cdm, udw):
        time.sleep(1)
        try:
            default_fax_receive_ticket = cdm.get(fax_receive_uri)
            spice.fax_ui().goto_menu_fax_receive_settings()
            #spice.fax_ui().fax_set_slider_value("Number Of Rings", 3) # Rings to answer is not a slider but a spin box for WF UI
            spice.fax_ui().fax_receive_settings_set_rings_to_answer("3")
            spice.fax_ui().fax_receive_settings_set_values("2-Sided Fax Printing", True)
            spice.fax_ui().fax_receive_settings_set_values("Fit to Page", True)

            # incoming receive fax alert trigger and validation
            faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
            trace_log('faxSimIp - {}'.format(faxSimIp))
            spice.fax_ui().incoming_receive_fax(cdm, udw, faxSimIp, "Yes")

            # wait for toast invisible.
            time.sleep(30)
        finally:
            spice.goto_homescreen()
            cdm.put(fax_resource_uri, default_fax_receive_ticket)

    def fax_dualfax_receivejob_after_v29_speed_selection(self, spice, setup_fax_using_cdm, cdm, udw):
        try:
            default_fax_receive_ticket = cdm.get(fax_receive_uri)
            spice.fax_ui().goto_menu_fax_receive_settings()
            #spice.fax_ui().fax_set_slider_value("Number Of Rings", 3) # Rings to answer is not a slider but a spin box for WF UI
            spice.fax_ui().fax_receive_settings_dualfax_set_rings_to_answer("3")
            spice.fax_ui().fax_receive_settings_set_values("2-Sided Fax Printing", True)
            spice.fax_ui().fax_receive_settings_set_values("Fit to Page", True)

            # incoming receive fax alert trigger and validation
            faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
            trace_log('faxSimIp - {}'.format(faxSimIp))
            spice.fax_ui().incoming_receive_fax(cdm, udw, faxSimIp, "Yes")

        finally:
            spice.goto_homescreen()

    def faxdiagnostics_singlemodemtone_v1100(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1100")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone1100)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Starting Generate SingleModemTone v1100")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Done Generate SingleModemTone v1100")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.single_modem_tone_donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v1300(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1300")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone1300)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Starting Generate SingleModemTone v1300")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Done Generate SingleModemTone v1300")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.single_modem_tone_donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v1800(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v1800")
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone1800)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Starting Generate SingleModemTone v1800")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Done Generate SingleModemTone v1800")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.single_modem_tone_donebutton)
        currentElementdonebutton.mouse_click()

    def faxdiagnostics_singlemodemtone_v2100(self, spice, udw):
        logging.info("Go to Generate SingleModemTone v2100")
        self.workflow_common_operations.goto_item(
            FaxAppWorkflowObjectIds.tone2100, 
            FaxAppWorkflowObjectIds.view_service_faxdiagnostics_singlemodemtone,  
            select_option = False, 
            scrollbar_objectname = FaxAppWorkflowObjectIds.scrollbar_single_modem_tone)
        currentElement = spice.wait_for(FaxAppWorkflowObjectIds.tone2100)
        currentElement.mouse_click()
        time.sleep(2)
        currentElementStart = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Starting Generate SingleModemTone v2100")
        currentElementStart.mouse_click()
        time.sleep(5)
        assert spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        logging.info("Done Generate SingleModemTone v2100")
        currentElementStop = spice.wait_for(FaxAppWorkflowObjectIds.generate_start_button)
        currentElementStop.mouse_click()
        currentElementdonebutton = spice.wait_for(FaxAppWorkflowObjectIds.single_modem_tone_donebutton)
        currentElementdonebutton.mouse_click()

    def showallfaxlocations(self,cdm,udw):
        '''
        Verifies the show all fax locations button
        UI Flow is Home->Service->Fax Diagnostic ->Show all Fax locations
        '''
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname
        logging.info(f'printerName---common screen--: {printerName}')

        def assert_cdm_value_with_ui_value_workflow(showallfax_switch, bool):
            showallfax_switch.mouse_click()
            time.sleep(1)
            cdm_model = cdm.get(cdm.FAX_MODEM_DIAGNOSTIC_CONFIGURATION)
            time.sleep(1)
            assert cdm_model["showAllFaxLocationsEnabled"] == bool

        showallfax_switch1 = self._spice.query_item("#showAllFaxLocationsTextImage")        
        # camden, marconi, selene, moreto, marconihipdl, lotus
        if printerName == "jasper" or printerName ==  "pearl" or printerName == "morganite":
            showallfax_switch1.mouse_click()
        time.sleep(1)
        showallfax_switch = self._spice.query_item("#showAllFaxLocationsView")
        assert showallfax_switch
        time.sleep(2)

        defaultButtonModel_switch = self._spice.wait_for("#defaultButtonModel")
        showAllButtonModel_switch = self._spice.wait_for("#showAllButtonModel")

        # Turn the switch on and off and check cdm values
        if defaultButtonModel_switch["checked"] == True:
            assert_cdm_value_with_ui_value_workflow(defaultButtonModel_switch, "false")
        elif defaultButtonModel_switch["checked"] == False:
            assert_cdm_value_with_ui_value_workflow(defaultButtonModel_switch, "true")                                   

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
        other_option = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_print_quality)
        other_option.mouse_click()
        time.sleep(1)

    def diagnostictestview_click_home(self, spice):
        logging.info("Clicking Home")
        assert spice.wait_for(FaxAppWorkflowObjectIds.diagnostictests_menulist_view)
        time.sleep(2)
        home_button = spice.wait_for(FaxAppWorkflowObjectIds.button_diagnostictests_home)
        home_button.mouse_click()
        time.sleep(1)

