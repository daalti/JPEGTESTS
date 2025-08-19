'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.IDCardCopyAppProSelectUIOperations import IDCardCopyAppProSelectUIOperations
from dunetuf.ui.uioperations.PomOperations.CopyApp.CopyAppPage import CopyAppPage
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.IDCardCopyAppWorkflowUIXSOperations import IDCardCopyAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.IDCardCopyAppWorkflowUISOperations import IDCardCopyAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.IDCardCopyAppWorkflowUIMOperations import IDCardCopyAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.IDCardCopyAppWorkflowUILOperations import IDCardCopyAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.IDCardCopyAppWorkflowUIXLOperations import IDCardCopyAppWorkflowUIXLOperations

class spice_copy_idcard_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._idcopyAppPage = None


    @property
    def idcard_copy_app(self):
        '''  Get ID Card copy app '''
        if self.uitype == "ProSelect":
            if self._idcopyAppPage == None:
                self._idcopyAppPage = IDCardCopyAppProSelectUIOperations(self)
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                return IDCardCopyAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return IDCardCopyAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return IDCardCopyAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return IDCardCopyAppWorkflowUILOperations(self)
            elif self.uisize == "XL":
                return IDCardCopyAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            if self._idcopyAppPage == None:
                self._idcopyAppPage = CopyAppPage(self)
        return self._idcopyAppPage
