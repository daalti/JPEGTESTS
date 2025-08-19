import logging
from dunetuf.ui.uioperations.WorkflowOperations.PrintAppWorkflowUICommonOperations import PrintAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class PrintAppWorkflowUIMOperations(PrintAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
       