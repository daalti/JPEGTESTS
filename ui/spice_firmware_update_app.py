

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.FirmwareUpdateProselectUIOperations import FirmwareUpdateProselectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.FirmwareUpdateAppWorkflowUIXSOperations import FirmwareUpdateAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.FirmwareUpdateAppWorkflowUISOperations import FirmwareUpdateAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.FirmwareUpdateAppWorkflowUIMOperations import FirmwareUpdateAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.FirmwareUpdateAppWorkflowUILOperations import FirmwareUpdateAppWorkflowUILOperations

class spice_firmware_update_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._firmware_ui_operations = None

    @property
    def fw_update_app(self):
        '''
        Get Firmware Update methods
        '''
        if self.uitype == "ProSelect":
            if self._firmware_ui_operations == None:
                self._firmware_ui_operations = FirmwareUpdateProselectUIOperations(self)
            return self._firmware_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._firmware_ui_operations == None:
                    self._firmware_ui_operations = FirmwareUpdateAppWorkflowUIXSOperations(self)
                return self._firmware_ui_operations

            elif self.uisize == "S":
                if self._firmware_ui_operations == None:
                    self._firmware_ui_operations = FirmwareUpdateAppWorkflowUISOperations(self)
                return self._firmware_ui_operations

            elif self.uisize == "M":
                if self._firmware_ui_operations == None:
                    self._firmware_ui_operations = FirmwareUpdateAppWorkflowUIMOperations(self)
                return self._firmware_ui_operations
                          
            elif self.uisize == "L":
                if self._firmware_ui_operations == None:
                    self._firmware_ui_operations = FirmwareUpdateAppWorkflowUILOperations(self)
                return self._firmware_ui_operations 
            else: 
                raise NotImplementedError('Unimplemented method %s.' % sys._getframe().f_code.co_name + ' uisize reported: %s' % self.uisize)

        else:
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)