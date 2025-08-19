import logging
from dunetuf.ui.uioperations.WorkflowOperations.PrintQuickFormsAppWorkflowUICommonOperations import PrintQuickFormsAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class PrintQuickFormsAppWorkflowUIMOperations(PrintQuickFormsAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120