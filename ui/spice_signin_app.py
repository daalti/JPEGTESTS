'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.SignInAppProSelectUIOperations import SignInAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.SignInAppWorkflowUIXSOperations import SignInAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.SigninAppProSelectUIHybridOperations import SigninAppProSelectUIHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflow2UICommonOperations import SignInAppWorkflow2UIOperations

class spice_signin_app(object):
    uitype = None
    uisize = None
    def __init__(self, experience, size):
        uitype = experience
        uisize = size
        self._signin_ui_operations = None


    def signin_ui(self):
        if self.uitype == "ProSelect":
            if self.uitheme == "loTheme":
                return SignInAppProSelectUIOperations(self)
            elif self.uitheme == "hybridTheme":
                return SigninAppProSelectUIHybridOperations(self)
        elif self.uitype == "Workflow":
            return SignInAppWorkflowUIOperations(self)
        elif self.uitype == "Workflow2":
            return SignInAppWorkflow2UIOperations(self)
        raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def signIn(self):
        '''
        Get Sign In methods
        '''
        if self.uitype == "ProSelect":
            print ("UI Theme: " + self.uitheme)
            if self.uitheme == "loTheme":
                if self._signin_ui_operations == None:
                    self._signin_ui_operations = SignInAppProSelectUIOperations(self)
                return self._signin_ui_operations
            elif self.uitheme == "hybridTheme":
                if self._signin_ui_operations == None:
                    self._signin_ui_operations = SigninAppProSelectUIHybridOperations(self)
                return self._signin_ui_operations
        elif self.uitype == "Workflow":
            if self._signin_ui_operations == None:
                if self.uisize == "XS":
                    self._signin_ui_operations = SignInAppWorkflowUIXSOperations(self)
                else:
                    self._signin_ui_operations = SignInAppWorkflowUIOperations(self)
            return self._signin_ui_operations
        elif self.uitype == "Workflow2":
            if self._signin_ui_operations == None:
                self._signin_ui_operations = SignInAppWorkflow2UIOperations(self)
            return self._signin_ui_operations
        raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    
    