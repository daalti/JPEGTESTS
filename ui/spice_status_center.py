import sys

from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowUICommonOperations import StatusCenterWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflow2UICommonOperations import StatusCenterWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.StatusCenterWorkflowUISOperations import StatusCenterWorkflowUISOperations

class spice_status_center(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):
        uitype = experience
        uisize = size

    def status_center(self, cdm):
        if self.uitype == "ProSelect":
            # No status center in ProSelect
            return None
        if self.uitype == "Workflow":
            if self.uisize == "XS":
                return StatusCenterWorkflowUISOperations(self, cdm)
            elif self.uisize == "S":
                return StatusCenterWorkflowUISOperations(self, cdm)
            elif self.uisize == "M":
                return StatusCenterWorkflowUICommonOperations(self, cdm)
            elif self.uisize == "L":
                return StatusCenterWorkflowUICommonOperations(self, cdm)
            elif self.uisize == "XL":
                return StatusCenterWorkflowUICommonOperations(self, cdm)    
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        if self.uitype == "Workflow2":
            if self.uisize == "XS":
                return StatusCenterWorkflow2UICommonOperations(self, cdm)
            elif self.uisize == "S":
                return StatusCenterWorkflow2UICommonOperations(self, cdm)
            elif self.uisize == "M":
                return StatusCenterWorkflow2UICommonOperations(self, cdm)
            elif self.uisize == "L":
                return StatusCenterWorkflow2UICommonOperations(self, cdm)
            elif self.uisize == "XL":
                return StatusCenterWorkflow2UICommonOperations(self, cdm)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)            
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)