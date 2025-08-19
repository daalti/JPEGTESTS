'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys



from dunetuf.ui.uioperations.ProSelectOperations.CopyAppProSelectUIOperations import CopyAppProSelectUIOperations
from dunetuf.ui.uioperations.PomOperations.CopyApp.CopyAppPage import CopyAppPage
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.CopyAppWorkflowUIXSOperations import CopyAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.CopyAppWorkflowUISOperations import CopyAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.CopyAppWorkflowUIMOperations import CopyAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.CopyAppWorkflowUILOperations import CopyAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.CopyAppWorkflowUIXLOperations import CopyAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.CopyAppWorkflow2UIXSOperations import CopyAppWorkflow2UIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.CopyAppWorkflow2UISOperations import CopyAppWorkflow2UISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.CopyAppWorkflow2UIMOperations import CopyAppWorkflow2UIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.CopyAppWorkflow2UILOperations import CopyAppWorkflow2UILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.CopyAppWorkflow2UIXLOperations import CopyAppWorkflow2UIXLOperations

class spice_copy_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._copyAppPage = None



    def copy_ui(self):
        if self.uitype == "ProSelect":
            return CopyAppProSelectUIOperations(self)
        if self.uitype in ["Workflow"]:
            if self.uisize == "XS":
                return CopyAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return CopyAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return CopyAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return CopyAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return CopyAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        elif self.uitype in ["Workflow2"]:
            if self.uisize == "XS":
                return CopyAppWorkflow2UIXSOperations(self)
            elif self.uisize == "S":
                return CopyAppWorkflow2UISOperations(self)
            elif self.uisize == "M":
                return CopyAppWorkflow2UIMOperations(self)
            elif self.uisize == "L":
                return CopyAppWorkflow2UILOperations(self)
            elif self.uisize == "XL":
                return CopyAppWorkflow2UIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
           
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def copy_app(self):
        '''  Get copy app '''
        if self.uitype == "ProSelect":
            if self._copyAppPage == None:
                self._copyAppPage = CopyAppProSelectUIOperations(self)
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self._copyAppPage == None:
                self._copyAppPage = self.copy_ui(self)
        else:
            if self._copyAppPage == None:
                self._copyAppPage = CopyAppPage(self)
        return self._copyAppPage