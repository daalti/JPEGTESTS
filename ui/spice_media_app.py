'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.MediaAppProSelectUIOperations import MediaAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.MediaAppWorkflowUISOperations import MediaAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MediaAppWorkflowUIXSOperations import MediaAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.MediaAppWorkflowUIMOperations import MediaAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.MediaAppWorkflowUILOperations import MediaAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MediaAppWorkflowUIXLOperations import MediaAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.MediaAppHybridUIOperations import MediaAppHybridUIOperations

class spice_media_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._media_ui_operations = None

    @property
    def mediaapp(self):
        '''
        Get UI media methods
        '''
        if self.uitype == "ProSelect":
            if self.uitheme == "hybridTheme":
                self._media_ui_operations = MediaAppHybridUIOperations(self)
            if self._media_ui_operations == None:
                self._media_ui_operations = MediaAppProSelectUIOperations(self)
            return self._media_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._media_ui_operations == None:
                    self._media_ui_operations = MediaAppWorkflowUIXSOperations(self)
                return self._media_ui_operations

            elif self.uisize == "S":
                if self._media_ui_operations == None:
                    self._media_ui_operations = MediaAppWorkflowUISOperations(self)
                return self._media_ui_operations

            elif self.uisize == "M":
                if self._media_ui_operations == None:
                    self._media_ui_operations = MediaAppWorkflowUIMOperations(self)
                return self._media_ui_operations
                          
            elif self.uisize == "L":
                if self._media_ui_operations == None:
                    self._media_ui_operations = MediaAppWorkflowUILOperations(self)
                return self._media_ui_operations 
                
            elif self.uisize == "XL":
                if self._media_ui_operations == None:
                    self._media_ui_operations = MediaAppWorkflowUIXLOperations(self)
                return self._media_ui_operations 
            else: 
                raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
