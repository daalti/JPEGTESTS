'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUILoOperations.ProSelectUICommonLoOperations import ProSelectUICommonLoOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.ProSelectUICommonHybridOperations import ProSelectUICommonHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WorkflowUICommonSOperations import WorkflowUICommonSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.WorkflowUICommonMOperations import WorkflowUICommonMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.WorkflowUICommonLOperations import WorkflowUICommonLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.WorkflowUICommonXLOperations import WorkflowUICommonXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflow2UICommonOperations import MenuAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowUICommonOperations import HomeAppWorkflowUICommonOperations

class spice_common_operations(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):
        uitype = experience
        uisize = size

        self._ui_common_operations = None
        self._ui_basic_common_operations = None
        self._ui_menu_operations = None
        self._ui_home_operations = None

    @property
    def home_operations(self):
        '''
        Get Common methods by workflow flavour
        '''
        if self.uitype == "Workflow":
            if self._ui_home_operations == None:
                self._ui_home_operations = HomeAppWorkflowUICommonOperations(self)
            return self._ui_home_operations
        elif self.uitype == "Workflow2":
            if self._ui_home_operations == None:
                self._ui_home_operations = HomeAppWorkflow2UICommonOperations(self)
            return self._ui_home_operations
        else: 
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    @property
    def menu_operations(self):
        '''
        Get Common methods by workflow flavour
        '''
        if self.uitype == "Workflow":
            if self._ui_menu_operations == None:
                self._ui_menu_operations = MenuAppWorkflowUICommonOperations(self)
            return self._ui_menu_operations
        elif self.uitype == "Workflow2":
            if self._ui_menu_operations == None:
                self._ui_menu_operations = MenuAppWorkflow2UICommonOperations(self)
            return self._ui_menu_operations
        else: 
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    @property
    def basic_common_operations(self):
        '''
        Get Common methods by workflow flavour
        '''
        if self.uitype == "Workflow":
            if self._ui_basic_common_operations == None:
                self._ui_basic_common_operations = WorkflowUICommonOperations(self)
            return self._ui_basic_common_operations
        elif self.uitype == "Workflow2":
            if self._ui_basic_common_operations == None:
                self._ui_basic_common_operations = Workflow2UICommonOperations(self)
            return self._ui_basic_common_operations
        else: 
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    @property
    def common_operations(self):
        '''
        Get Common methods
        '''
        if self.uitype == "ProSelect":
            print ("UI Theme: " + self.uitheme)
            if self.uitheme == "loTheme":
                self._ui_common_operations = ProSelectUICommonLoOperations(self)
                return self._ui_common_operations
            elif self.uitheme == "hybridTheme":
                self._ui_common_operations = ProSelectUICommonHybridOperations(self)
                return self._ui_common_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name) 

        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._ui_common_operations == None:
                    self._ui_common_operations = WorkflowUICommonXSOperations(self)
                return self._ui_common_operations

            elif self.uisize == "S":
                if self._ui_common_operations == None:
                    self._ui_common_operations = WorkflowUICommonSOperations(self)
                return self._ui_common_operations

            elif self.uisize == "M":
                if self._ui_common_operations == None:
                    self._ui_common_operations = WorkflowUICommonMOperations(self)
                return self._ui_common_operations
                          
            elif self.uisize == "L":
                if self._ui_common_operations == None:
                    self._ui_common_operations = WorkflowUICommonLOperations(self)
                return self._ui_common_operations 
            elif self.uisize == "XL":
                if self._ui_common_operations == None:
                    self._ui_common_operations = WorkflowUICommonXLOperations(self)
                return self._ui_common_operations 
            else: 
                raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
