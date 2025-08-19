
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations



class KeyboardWorkflowUIMOperations(WorkflowKeyboardUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        
       