#########################################################################################
# @file      FirmwareUpdateAppWorkflowUICommonOperations.py
# @author    Neha
# @date      4-02-2022
# @brief     Interface for all the Fax Diagnostics methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################

from time import sleep
import logging

from dunetuf.ui.uioperations.BaseOperations.IFirmwareUpdateAppUIOperations import IFirmwareUpdateAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

_logger = logging.getLogger(__name__)


class FirmwareUpdateAppWorkflowUICommonOperations(IFirmwareUpdateAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

