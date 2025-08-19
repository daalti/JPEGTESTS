
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.TraysAppWorkflowUICommonOperations import TraysAppWorkflowUICommonOperations



class TraysAppWorkflowUIMOperations(TraysAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice

