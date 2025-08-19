'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.SuppliesUIProSelectOperations import SuppliesUIProSelectOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.SuppliesUIProSelectHybridOperations import SuppliesUIProSelectHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.SuppliesAppWorkflowUISOperations import SuppliesAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.SuppliesAppWorkflowUIXSOperations import SuppliesAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.SuppliesAppWorkflowUIMOperations import SuppliesAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.SuppliesAppWorkflowUILOperations import SuppliesAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.SuppliesAppWorkflowUIXLOperations import SuppliesAppWorkflowUIXLOperations

class spice_supplies_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._supplies_ui_operations = None

    @property
    def suppliesapp(self):
        '''
        Get supplies methods
        '''
        if self.uitype == "ProSelect":
            if self._supplies_ui_operations == None:
                if self.uitheme == "hybridTheme":
                    self._supplies_ui_operations = SuppliesUIProSelectHybridOperations(self)
                else:
                    self._supplies_ui_operations = SuppliesUIProSelectOperations(self)
            return self._supplies_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._supplies_ui_operations == None:
                    self._supplies_ui_operations = SuppliesAppWorkflowUIXSOperations(self)
                return self._supplies_ui_operations

            elif self.uisize == "S":
                if self._supplies_ui_operations == None:
                    self._supplies_ui_operations = SuppliesAppWorkflowUISOperations(self)
                return self._supplies_ui_operations

            elif self.uisize == "M":
                if self._supplies_ui_operations == None:
                    self._supplies_ui_operations = SuppliesAppWorkflowUIMOperations(self)
                return self._supplies_ui_operations
                          
            elif self.uisize == "L":
                if self._supplies_ui_operations == None:
                    self._supplies_ui_operations = SuppliesAppWorkflowUILOperations(self)
                return self._supplies_ui_operations
            elif self.uisize == "XL":
                if self._supplies_ui_operations == None:
                    self._supplies_ui_operations = SuppliesAppWorkflowUIXLOperations(self)
                return self._supplies_ui_operations 
            else: 
                raise NotImplementedError('Unimplemented method %s.' % sys._getframe().f_code.co_name + ' uisize reported: %s' % self.uisize)

        else:
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
