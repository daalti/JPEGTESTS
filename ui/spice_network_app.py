

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''



import logging
import sys
from dunetuf.ui.uioperations.ProSelectOperations.NetworkAppProSelectUIOperations import NetworkAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkAppWorkflowUICommonOperations import NetworkAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.NetworkAppWorkflowUILOperations import NetworkAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.NetworkAppWorkflowUIMOperations import NetworkAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.NetworkAppWorkflowUISOperations import NetworkAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.NetworkAppWorkflowUIXSOperations import NetworkAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.NetworkAppWorkflowUIXLOperations import NetworkAppWorkflowUIXLOperations




class spice_network_app(object):

    def __init__(self, experience, size):
        self._uitype = experience
        self._uisize = size
        self._network_menu_ui_operations = None

    def network_ui(self):
        '''Get the UI size'''
        logging.info("Get UI Size!")
        if self._uisize == "XS":
            logging.info('UI size is XS!')
            return NetworkAppWorkflowUIXSOperations(self)
        elif self._uisize == "S":
            logging.info('UI size is S!')
            return NetworkAppWorkflowUISOperations(self)
        elif self._uisize == "M":
            logging.info('UI size is M!')
            return NetworkAppWorkflowUIMOperations(self)
        elif self._uisize == "L":
            logging.info('UI size is L!')
            return NetworkAppWorkflowUILOperations(self)
        elif self._uisize == "XL":
            logging.info('UI size is XL!')
            return NetworkAppWorkflowUIXLOperations(self)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s', sys._getframe().f_code.co_name)

    @property
    def network(self):
        '''
        Get network object.
        Return:
            Return object for Network operations
        '''
        if self._uitype == "ProSelect":
            logging.info('UI Type is ProSelect!')
            if self._network_menu_ui_operations == None:
                self._network_menu_ui_operations = NetworkAppProSelectUIOperations(self)
            return self._network_menu_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            logging.info('UI Type is Workflow!')
            if self._network_menu_ui_operations == None:
                self._network_menu_ui_operations = self.network_ui()
            return self._network_menu_ui_operations
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s', sys._getframe().f_code.co_name)