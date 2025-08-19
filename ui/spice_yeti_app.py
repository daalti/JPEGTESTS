'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.YetiAppProSelectUIOperations import YetiAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.YetiAppWorkflowUIXSOperations import \
    YetiAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.YetiAppWorkflowUISOperations import \
    YetiAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.YetiAppWorkflowUIMOperations import \
    YetiAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.YetiAppWorkflowUILOperations import \
    YetiAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.YetiAppWorkflowUIXLOperations import \
    YetiAppWorkflowUIXLOperations


class spice_yeti_app(object):
    uitype = None
    uisize = None

    def __init__(self, experience, size):

        uitype = experience
        uisize = size

    @property
    def yeti(self):
        if self.uitype == "ProSelect":
            return YetiAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return YetiAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return YetiAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return YetiAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return YetiAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return YetiAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)