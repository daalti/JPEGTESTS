
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxDiagnosticWorkflowUICommonOperations import FaxDiagnosticWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM

class FaxAppWorkflowUISOperations(FaxAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.homeoperations = spice.home_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))


