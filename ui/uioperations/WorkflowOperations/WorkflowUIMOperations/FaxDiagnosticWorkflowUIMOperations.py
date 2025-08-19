
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxDiagnosticWorkflowUICommonOperations import FaxDiagnosticWorkflowUICommonOperations




class FaxDiagnosticWorkflowUIMOperations(FaxDiagnosticWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120


