import sys
import logging
import time

from dunetuf.power.power import Power
from dunetuf.cdm import CDM
from dunetuf.ui.uioperations.WorkflowOperations.OOBEAppWorkflowUICommonOperations import OOBEAppWorkflowUICommonOperations


class OOBEAppWorkflowUISOperations(OOBEAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        super().__init__(self.spice)
        