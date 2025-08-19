import logging
import time

from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations


class ProSelectUICommonLoOperations(ProSelectCommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice

    