
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.OOBEAppWorkflowUICommonOperations import OOBEAppWorkflowUICommonOperations


class OOBEAppWorkflowUIXLOperations(OOBEAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        super().__init__(self.spice)
