
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.YetiAppWorkflowUICommonOperations import YetiAppWorkflowUICommonOperations


class YetiAppWorkflowUILOperations(YetiAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        self.maxtimeout = 120