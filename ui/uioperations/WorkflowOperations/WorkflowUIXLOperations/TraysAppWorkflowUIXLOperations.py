
import logging
from time import sleep


from dunetuf.ui.uioperations.WorkflowOperations.TraysAppWorkflowUICommonOperations import TraysAppWorkflowUICommonOperations


class TraysAppWorkflowUIXLOperations(TraysAppWorkflowUICommonOperations):

 
    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    