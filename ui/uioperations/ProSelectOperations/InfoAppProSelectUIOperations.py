#########################################################################################
# @file      InfoAppProSelectUIOperations.py
# @author    Daniel Fernandez Charro (daniel.fernandez.charro@hp.com)
# @date      21-03-2022
# @brief     Implementation Info UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
from email.policy import default
import  sys
import time
import logging
import pytest
from dunetuf.ui.uioperations.BaseOperations.IInfoAppUIOperations import IInfoAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

_logger = logging.getLogger(__name__)


class InfoAppProSelectUIOperations(IInfoAppUIOperations):
    def __init__(self, spice):
        self._spice = spice
        self.proselect_common_operations = ProSelectCommonOperations(self._spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)
        self.proselect_keyboard_operations = ProSelectKeyboardOperations(self._spice)
          