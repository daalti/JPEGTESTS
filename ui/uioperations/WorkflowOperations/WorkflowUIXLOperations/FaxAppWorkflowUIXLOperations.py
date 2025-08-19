
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations

class FaxAppWorkflowUIXLOperations(FaxAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.homeoperations = spice.home_operations

