

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.InfoAppProSelectUIOperations import InfoAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.InfoAppWorkflowUICommonOperations import InfoAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.InfoAppWorkflowUILOperations import InfoAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.InfoAppWorkflowUIMOperations import InfoAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.InfoAppWorkflowUISOperations import InfoAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.InfoAppWorkflowUIXSOperations import InfoAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.InfoAppWorkflowUIXLOperations import InfoAppWorkflowUIXLOperations


class spice_info_app(object):

    uitype = None
    uisize = None

    def __init__(self, experience, size):
        uitype = experience
        uisize = size
        self._info_ui_operations = None

    def info_ui(self):
        '''Get the UI size'''
        logging.info("Get UI Size!")
        if self.uisize == "XS":
            return InfoAppWorkflowUIXSOperations(self)
        elif self.uisize == "S":
            return InfoAppWorkflowUISOperations(self)
        elif self.uisize == "M":
            return InfoAppWorkflowUIMOperations(self)
        elif self.uisize == "L":
            return InfoAppWorkflowUILOperations(self)
        elif self.uisize == "XL":
            return InfoAppWorkflowUIXLOperations(self)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s', sys._getframe().f_code.co_name)

    @property
    def infoapp(self):
        '''
        Get info object.
        Return:
            Return object for Info operations
        '''
        if self.uitype == "ProSelect":
            if self._info_ui_operations == None:
                self._info_ui_operations = InfoAppProSelectUIOperations(self)
            return self._info_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self._info_ui_operations == None:
                self._info_ui_operations = self.info_ui()
            return self._info_ui_operations
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s', sys._getframe().f_code.co_name)