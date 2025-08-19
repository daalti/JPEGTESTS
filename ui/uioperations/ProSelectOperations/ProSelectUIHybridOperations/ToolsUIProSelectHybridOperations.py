#########################################################################################
# @file      ToolsUIProSelectHybridOperations.py
# @author
# @date
# @brief     Interface for all the Fax Diagnostics methods.
#            Interface for service pin methods.
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################

from time import sleep
import logging

from dunetuf.ui.uioperations.ProSelectOperations.ToolsUIProSelectOperations import ToolsUIProSelectOperations

_logger = logging.getLogger(__name__)


class ToolsUIProSelectHybridOperations(ToolsUIProSelectOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    def servicemenu_servicetests_keytest(self):
        """
        Test Navigation and Functionality of Menu->Tools->Service->service tests-> key test
        """
        keys = ["BACK","HOME","CANCEL","ENTER","UP","RIGHT","LEFT","DOWN"]
        self._spice.wait_for("#testKeysView #Version1Text")
        startbtn = self._spice.query_item("#testStart SpiceText")
        startbtn.mouse_click()
        for key in keys:
            logging.info("Verifying Key: %s" % key)
            startbtn._server.udw.mainUiApp.KeyHandler.setKeyPress(key)
            assert "Passed" in self._spice.wait_for("#ToastBase #ToastRowItem #ToastInfoText")["text"], "%s: Key Didn't Work" % key
            # Wait for Toast message to clear.
            sleep(3)