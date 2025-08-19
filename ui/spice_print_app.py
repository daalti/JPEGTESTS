'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import sys
from dunetuf.ui.uioperations.ProSelectOperations.PrintFromUsbAppProSelectUIOperations import PrintFromUsbAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.PrintFromUsbAppWorkflowUIXSOperations import PrintFromUsbAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.PrintFromUsbAppWorkflowUISOperations import PrintFromUsbAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.PrintFromUsbAppWorkflowUIMOperations import PrintFromUsbAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.PrintFromUsbAppWorkflowUILOperations import PrintFromUsbAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.PrintFromUsbAppWorkflowUIXLOperations import PrintFromUsbAppWorkflowUIXLOperations

from dunetuf.ui.uioperations.ProSelectOperations.PrintAppProSelectUIOperations import PrintAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.PrintAppWorkflowUISOperations import PrintAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.PrintAppWorkflowUIXSOperations import PrintAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.PrintAppWorkflowUIMOperations import PrintAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.PrintAppWorkflowUILOperations import PrintAppWorkflowUILOperations

from dunetuf.ui.uioperations.ProSelectOperations.PrintQuickFormsAppProSelectUIOperations import PrintQuickFormsAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.PrintQuickFormsAppProSelectUIHybridOperations import PrintQuickFormsAppProSelectUIHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.PrintQuickFormsAppWorkflowUISOperations import PrintQuickFormsAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.PrintQuickFormsAppWorkflowUIXSOperations import PrintQuickFormsAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.PrintQuickFormsAppWorkflowUIMOperations import PrintQuickFormsAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.PrintQuickFormsAppWorkflowUILOperations import PrintQuickFormsAppWorkflowUILOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.PrintFromNetworkAppWorkflowUIXLOperations import PrintFromNetworkAppWorkflowUIXLOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.PrintPhotoAppWorkflowUIXSOperations import PrintPhotoAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.PrintPhotoAppWorkflowUISOperations import PrintPhotoAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintPhotoAppWorkflowUICommonOperations import PrintPhotoAppWorkflowUICommonOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.PrintFromMyhomeAppWorkflowUIXLOperations import PrintFromMyhomeAppWorkflowUIXLOperations


class spice_print_app(object):

    uitype = None
    uisize = None

    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._print_from_usb_ui_operations = None
        self.print_quality_ui_operations = None
        self.print_quick_forms_ui_operations = None
        self.print_from_network_ui_operations = None
        self.print_from_myhome_ui_operations = None
        self._print_from_photo_ui_operations = None

    @property
    def print_from_myhome(self):
        # Get print from myhome navigation methods
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XL":
                if self.print_from_myhome_ui_operations == None:
                    self.print_from_myhome_ui_operations = PrintFromMyhomeAppWorkflowUIXLOperations(self)
                return self.print_from_myhome_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def print_from_network(self):

        # Get print from network navigation methods
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XL":
                if self.print_from_network_ui_operations == None:
                    self.print_from_network_ui_operations = PrintFromNetworkAppWorkflowUIXLOperations(self)
                return self.print_from_network_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def print_from_usb(self):

        # Get print from usb navigation methods

        if self.uitype == "ProSelect":
            if self._print_from_usb_ui_operations == None:
                self._print_from_usb_ui_operations = PrintFromUsbAppProSelectUIOperations(self)
            return self._print_from_usb_ui_operations

        if self.uitype in ["Workflow","Workflow2"]:
            if self.uisize == "XS":
                if self._print_from_usb_ui_operations == None:
                    self._print_from_usb_ui_operations = PrintFromUsbAppWorkflowUIXSOperations(self)
                return self._print_from_usb_ui_operations
            elif self.uisize == "S":
                if self._print_from_usb_ui_operations == None:
                    self._print_from_usb_ui_operations = PrintFromUsbAppWorkflowUISOperations(self)
                return self._print_from_usb_ui_operations
            elif self.uisize == "M":
                if self._print_from_usb_ui_operations == None:
                    self._print_from_usb_ui_operations = PrintFromUsbAppWorkflowUIMOperations(self)
                return self._print_from_usb_ui_operations
            elif self.uisize == "L":
                if self._print_from_usb_ui_operations == None:
                    self._print_from_usb_ui_operations = PrintFromUsbAppWorkflowUILOperations(self)
                return self._print_from_usb_ui_operations
            elif self.uisize == "XL":
                if self._print_from_usb_ui_operations == None:
                    self._print_from_usb_ui_operations = PrintFromUsbAppWorkflowUIXLOperations(self)
                return self._print_from_usb_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def print_photo_from_usb(self):

        # Get print from usb navigation methods

        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._print_from_photo_ui_operations == None:
                    self._print_from_photo_ui_operations = PrintPhotoAppWorkflowUICommonOperations(self)
                return self._print_from_photo_ui_operations
            elif self.uisize == "S":
                if self._print_from_photo_ui_operations == None:
                    self._print_from_photo_ui_operations = PrintPhotoAppWorkflowUISOperations(self)
                return self._print_from_photo_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
    
    
    @property
    def print_quality(self):

        # Get print methods

        if self.uitype == "ProSelect":
            if self.print_quality_ui_operations == None:
                self.print_quality_ui_operations = PrintAppProSelectUIOperations(self)
            return self.print_quality_ui_operations

        if self.uitype in ["Workflow", "Workflow2"]:
          
            if self.uisize == "XS":
                if self.print_quality_ui_operations == None:
                    self.print_quality_ui_operations = PrintAppWorkflowUIXSOperations(self)
                return self.print_quality_ui_operations
            elif self.uisize == "S":
                if self.print_quality_ui_operations == None:
                    self.print_quality_ui_operations = PrintAppWorkflowUISOperations(self)
                return self.print_quality_ui_operations
            elif self.uisize == "M":
                if self.print_quality_ui_operations == None:
                    self.print_quality_ui_operations = PrintAppWorkflowUIMOperations(self)
                return self.print_quality_ui_operations
            elif self.uisize == "L":
                if self.print_quality_ui_operations == None:
                    self.print_quality_ui_operations = PrintAppWorkflowUILOperations(self)
                return self.print_quality_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def print_quick_forms(self):
        #Get print from Quick Forms

        if self.uitype == "ProSelect":
            print ("UI Theme: " + self.uitheme)
            if self.uitheme == "loTheme":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppProSelectUIOperations(self)
                return self.print_quick_forms_ui_operations
            elif self.uitheme == "hybridTheme":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppProSelectUIHybridOperations(self)
                return self.print_quick_forms_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)   
        if self.uitype in ["Workflow", "Workflow2"]:
          
            if self.uisize == "XS":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppWorkflowUIXSOperations(self)
                return self.print_quick_forms_ui_operations
            elif self.uisize == "S":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppWorkflowUISOperations(self)
                return self.print_quick_forms_ui_operations
            elif self.uisize == "M":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppWorkflowUIMOperations(self)
                return self.print_quick_forms_ui_operations
            elif self.uisize == "L":
                if self.print_quick_forms_ui_operations == None:
                    self.print_quick_forms_ui_operations = PrintQuickFormsAppWorkflowUILOperations(self)
                return self.print_quick_forms_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
