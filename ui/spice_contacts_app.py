

'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.ProSelectOperations.ContactsAppProSelectUIOperations import ContactsAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.ContactsAppWorkflowUIXSOperations import ContactsAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ContactsAppWorkflowUISOperations import ContactsAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ContactsAppWorkflowUIMOperations import ContactsAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ContactsAppWorkflowUILOperations import ContactsAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.ContactsAppWorkflowUIXLOperations import ContactsAppWorkflowUIXLOperations

class spice_contacts_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):
        uitype = experience
        uisize = size
        self._scan_contacts_ui_operations = None
        
    @property
    def contacts(self):
        if self.uitype == "ProSelect":
            if self._scan_contacts_ui_operations == None:
                self._scan_contacts_ui_operations = ContactsAppProSelectUIOperations(self)
            return self._scan_contacts_ui_operations
            
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_contacts_ui_operations == None:
                    self._scan_contacts_ui_operations = ContactsAppWorkflowUIXSOperations(self)
                return self._scan_contacts_ui_operations
            elif self.uisize == "S":
                if self._scan_contacts_ui_operations == None:
                    self._scan_contacts_ui_operations = ContactsAppWorkflowUISOperations(self)
                return self._scan_contacts_ui_operations
            elif self.uisize == "M":
                if self._scan_contacts_ui_operations == None:
                    self._scan_contacts_ui_operations = ContactsAppWorkflowUIMOperations(self)
                return self._scan_contacts_ui_operations
            elif self.uisize == "L":
                if self._scan_contacts_ui_operations == None:
                    self._scan_contacts_ui_operations = ContactsAppWorkflowUILOperations(self)
                return self._scan_contacts_ui_operations
            elif self.uisize == "XL":
                if self._scan_contacts_ui_operations == None:
                    self._scan_contacts_ui_operations = ContactsAppWorkflowUIXLOperations(self)
                return self._scan_contacts_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
