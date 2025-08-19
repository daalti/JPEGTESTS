import time

from dunetuf.ui.uioperations.BaseOperations.IFirmwareUpdateAppUIOperations import IFirmwareUpdateAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class FirmwareUpdateAppWorkflowUIMOperations(IFirmwareUpdateAppUIOperations):

       def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
