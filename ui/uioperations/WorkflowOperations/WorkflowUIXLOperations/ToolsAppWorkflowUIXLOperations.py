import logging
from time import sleep
import json

from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowUICommonOperations import ToolsAppWorkflowUICommonOperations
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations



class ToolsAppWorkflowUIXLOperations(ToolsAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.workflow_common_operations = spice.basic_common_operations
        self.maxtimeout = 120
        self._spice = spice

     # Service Pin operations
    def servicePin_test(self, udw):
        '''
        Tests the service pin menu.
        Menu->Tools->Service->ServicePinPrompt
        '''  
        BEAM_PIN = "3989"
        DEFAULT_PIN = "08675309"
        ADMIN_PIN = "Pass5742"
        self.udw = udw
        self.cdm = CDM(self.udw.get_target_ip(), timeout=5.0)
        self.configuration = Configuration(self.cdm)
        printerName = self.configuration.productname

        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_service , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
        current_button = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service + " MouseArea")
        current_button.mouse_click()

        keyboard = self._spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard

        #Enter Admin pin, note default pin is set, we expect admin pin to fail
        keyboard.__setitem__('displayText', ADMIN_PIN) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', ADMIN_PIN)

        doneButton = self._spice.wait_for(MenuAppWorkflowObjectIds.view_service_sign_in_button)
        doneButton.mouse_click()

        #Should see access denied
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_access_denied)

        #click ok button to get out of access denied screen
        self._spice.wait_for("#servicePromptFooter #ButtonControl").mouse_click()

        #Return to service menu
        serviceMenu = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_service)
        serviceMenu.mouse_click()

        keyboard = self._spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard

        if printerName.strip() == "beamsfp" or printerName.strip() == 'jupiter':
            #Enter Default Beam pin
            keyboard.__setitem__('displayText', BEAM_PIN) #just to show the password populated on keyboard
            keyboard.__setitem__('inputText', BEAM_PIN)
        else:
            #Enter Default pin
            keyboard.__setitem__('displayText', DEFAULT_PIN) #just to show the password populated on keyboard
            keyboard.__setitem__('inputText', DEFAULT_PIN)

        doneButton = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_tools_servce_AuthDone)
        doneButton.mouse_click()
 
        #In service menu now.
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_service)
        logging.info("At Service Screen")
        sleep(1)