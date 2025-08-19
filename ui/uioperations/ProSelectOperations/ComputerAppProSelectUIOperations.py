#########################################################################################
# @file      ComputerAppProSelectUIOperations.py
# @author    Mangesh Patil (mangesh.patil1@hp.com)
# @date      22-06-2021
# @brief     Implementation for all the Scan to Computer UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################

from time import sleep
import logging
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.BaseOperations.IComputerAppUIOperations import IComputerAppUIOperations

_logger = logging.getLogger(__name__)


class ComputerAppProSelectUIOperations(IComputerAppUIOperations):

    SCAN_COMPUTER = "#10c9c25c-7b7b-4f7d-b4ad-dd9975be35c7"

    SCAN_COMPUTER_NOT_CONFIGURED_VIEW = "#eSCLNotConfiguredView"
    SCAN_COMPUTER_SETUP_WITH_SOFTWARE_BUTTON = "#setupWithSoftwareButton"
    SCAN_COMPUTER_SETUP_WITH_WEB_BUTTON = "#setupWithWebButton"

    SCAN_COMPUTER_SETUP_VIEW = "#eSCLSetupInfoView"
    SCAN_COMPUTER_SETUP_OK_BUTTON = "#okayButton"
    SCAN_COMPUTER_SETUP_PRINT_BUTTON = "printButton"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.scan_operations = ScanAppProSelectUIOperations(self._spice)

    # Scan to Computer flow operations
    # Navigation from Home screen

    def goto_scan_to_computer(self):
        '''
        Navigates to Scan then Computer screen starting from Home screen.
        UI Flow is Home->Scan->Computer
        '''
        self.scan_operations.goto_scan_app()
        self.dial_common_operations.goto_item(self.SCAN_COMPUTER, "#ButtonListLayout")
        
    def verify_scan_computer_web_setup_ok(self):
        '''
        UI should be at Scan Computer not setup view.
        Verify scan to computer setup using browser by checking for setup screen
        '''
        assert self._spice.wait_for(self.SCAN_COMPUTER_NOT_CONFIGURED_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_COMPUTER_SETUP_WITH_WEB_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_COMPUTER_SETUP_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_COMPUTER_SETUP_OK_BUTTON, "#ButtonListLayout")
        sleep(2)
        
    def verify_scan_computer_software_setup_ok(self):
        '''
        UI should be at Scan Computer not setup view.
        Verify scan to computer setup using browser by checking for setup screen
        '''        
        assert self._spice.wait_for(self.SCAN_COMPUTER_NOT_CONFIGURED_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_COMPUTER_SETUP_WITH_SOFTWARE_BUTTON, "#ButtonListLayout")
        assert self._spice.wait_for(self.SCAN_COMPUTER_SETUP_VIEW)
        self.dial_common_operations.goto_item(self.SCAN_COMPUTER_SETUP_OK_BUTTON, "#ButtonListLayout")
        sleep(2)