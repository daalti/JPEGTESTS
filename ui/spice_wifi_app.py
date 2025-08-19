import logging
import sys
from dunetuf.ui.uioperations.ProSelectOperations.WifiAppProSelectUIOperations import WifiAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WifiAppWorkflowUIXSOperations import WifiAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.WifiAppWorkflowUILOperations import WifiAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.WifiAppWorkflowUIMOperations import WifiAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.WifiAppWorkflowUIXLOperations import WifiAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WifiAppWorkflowUISOperations import WifiAppWorkflowUISOperations

class spice_wifi_app(object):

    def __init__(self, experience, size):
        self._uitype = experience
        self._uisize = size
        self._wifi_menu_ui_operations = None

    def network_wifi_ui(self):
        '''Get the UI size'''
        logging.info("Get UI Size!")
        if self._uisize == "XS":
            return WifiAppWorkflowUIXSOperations(self)
        elif self._uisize == "S":
            return WifiAppWorkflowUISOperations(self)
        elif self._uisize == "M":
            return WifiAppWorkflowUIMOperations(self)
        elif self._uisize == "L":
            return WifiAppWorkflowUILOperations(self)
        elif self._uisize == "XL":
            return WifiAppWorkflowUIXLOperations(self)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s', sys._getframe().f_code.co_name)


    @property
    def network_wifi(self):
        '''
        evenGet wifi navigation methods
        '''
        if self.uitype == "ProSelect":
            if self._wifi_menu_ui_operations == None:
                self._wifi_menu_ui_operations = WifiAppProSelectUIOperations(self)
            return self._wifi_menu_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self._wifi_menu_ui_operations == None:
                self._wifi_menu_ui_operations = self.network_wifi_ui()
            return self._wifi_menu_ui_operations
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s',sys._getframe().f_code.co_name)















