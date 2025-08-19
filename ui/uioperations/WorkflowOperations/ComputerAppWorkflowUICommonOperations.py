#########################################################################################
# @file      ComputerAppWorkflowUICommonOperations.py
# @author    Payas Kumar (payas.kumar@hp.com)
# @date      09-02-2022
# @brief     Implementation for all the Scan to Computer UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################

from time import sleep
import logging
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.BaseOperations.IComputerAppUIOperations import IComputerAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.ComputerAppWorkflowObjectIds import ComputerAppWorkflowObjectIds

_logger = logging.getLogger(__name__)


class ComputerAppWorkflowUICommonOperations(IComputerAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)

    # Scan to Computer flow operations
    # Navigation from Home screen

    def goto_scan_to_computer(self):
        '''
        Navigates to Scan then Computer screen starting from Home screen.
        UI Flow is Home->Scan->Computer
        '''
        self.scan_operations.goto_scan_app()
        sleep(3)
        self.workflow_common_operations.scroll_position(ComputerAppWorkflowObjectIds.view_scan_screen, ComputerAppWorkflowObjectIds.scan_computer, ComputerAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , ComputerAppWorkflowObjectIds.scanFolderPage_column_name , ComputerAppWorkflowObjectIds.scanFolderPage_Content_Item)
        self.spice.wait_for(ComputerAppWorkflowObjectIds.scan_computer + " MouseArea")
        current_button = self.spice.query_item(ComputerAppWorkflowObjectIds.scan_computer + " MouseArea")
        current_button.mouse_click()  
        logging.info("At Scan to computer App")
        
    def verify_scan_computer_web_setup_ok(self):
        '''
        UI should be at Scan Computer not setup view.
        Verify scan to computer setup using browser by checking for setup screen
        '''
        assert self.spice.wait_for(ComputerAppWorkflowObjectIds.view_scanComputerNotConfigured)
        assert self.spice.wait_for(ComputerAppWorkflowObjectIds.computernotconfigured_button_websetup)
        sleep(2)

    def wait_for_computer_not_configured(self):
        '''
        UI wait for computer not configured
        '''        
        assert self.spice.wait_for(ComputerAppWorkflowObjectIds.view_scanComputerNotConfigured)
        
    def verify_scan_computer_software_setup_ok(self):
        '''
        UI should be at Scan Computer not setup view.
        Verify scan to computer setup using browser by checking for setup screen
        '''        
        assert self.spice.wait_for(ComputerAppWorkflowObjectIds.view_scanComputerNotConfigured)
        assert self.spice.wait_for(ComputerAppWorkflowObjectIds.computernotconfigured_button_softwaresetup)
        sleep(2)