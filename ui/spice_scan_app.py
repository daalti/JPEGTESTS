'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''
import logging
import sys



from dunetuf.ui.uioperations.ProSelectOperations.ScanAppProSelectUIOperations import ScanAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ComputerAppProSelectUIOperations import ComputerAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ContactsAppProSelectUIOperations import ContactsAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.SharePointAppProSelectUIOperations import SharePointAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.UsbScanAppProSelectUIOperations import UsbScanAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.NetworkFolderAppProSelectUIOperations import NetworkFolderAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.ScanAppWorkflowUIXSOperations import ScanAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ScanAppWorkflowUISOperations import ScanAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ScanAppWorkflowUIMOperations import ScanAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ScanAppWorkflowUILOperations import ScanAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.ScanAppWorkflowUIXLOperations import ScanAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.UsbScanAppWorkflowUIXSOperations import UsbScanAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.UsbScanAppWorkflowUISOperations import UsbScanAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.UsbScanAppWorkflowUIMOperations import UsbScanAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.UsbScanAppWorkflowUILOperations import UsbScanAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.UsbScanAppWorkflowUIXLOperations import UsbScanAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.ProSelectOperations.EmailAppProSelectUIOperations import EmailAppProSelectUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.EmailAppWorkflowUIXSOperations import EmailAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.EmailAppWorkflowUISOperations import EmailAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.EmailAppWorkflowUIMOperations import EmailAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.EmailAppWorkflowUILOperations import EmailAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.EmailAppWorkflowUIXLOperations import EmailAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.NetworkFolderAppWorkflowUILOperations import NetworkFolderAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.NetworkFolderAppWorkflowUIMOperations import NetworkFolderAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.NetworkFolderAppWorkflowUISOperations import NetworkFolderAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.NetworkFolderAppWorkflowUIXSOperations import NetworkFolderAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.NetworkFolderAppWorkflowUIXLOperations import NetworkFolderAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.SharePointAppWorkflowUILOperations import SharePointAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.SharePointAppWorkflowUIMOperations import SharePointAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.SharePointAppWorkflowUISOperations import SharePointAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.SharePointAppWorkflowUIXSOperations import SharePointAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.SharePointAppWorkflowUIXLOperations import SharePointAppWorkflowUIXLOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.JobStorageAppWorkflowUISOperations import JobStorageAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.JobStorageAppWorkflowUILOperations import JobStorageAppWorkflowUILOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.ComputerAppWorkflowUIXSOperations import ComputerAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ComputerAppWorkflowUISOperations import ComputerAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ComputerAppWorkflowUIMOperations import ComputerAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ComputerAppWorkflowUILOperations import ComputerAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.ComputerAppWorkflowUIXLOperations import ComputerAppWorkflowUIXLOperations

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.HpBuildAppWorkflowUIXSOperations import HpBuildAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.HpBuildAppWorkflowUISOperations import HpBuildAppWorkflowUISOperations



class spice_scan_app(object):

    uitype = None
    uisize = None

    def __init__(self, experience, size):
        logging.info("spice_scan_app %s,%s", self.uitype, self.uisize)
        uitype = experience
        uisize = size
        self._scan_options_ui_operations = None
        self._scan_computer_ui_operations = None
        self._scan_sharepoint_ui_operations = None
        self._scan_usb_ui_operations = None
        self._scan_network_folder_ui_operations = None
        self._scan_job_storage_ui_operations = None
        self._scan_email_ui_operations = None
        self._scan_hpbuild_ui_operations = None

    @property
    def scan_settings(self):
        '''
        #Get Scan settings navigation methods
        '''
        if self.uitype == "ProSelect":
            if self._scan_options_ui_operations == None:
                self._scan_options_ui_operations = ScanAppProSelectUIOperations(self)
            return self._scan_options_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_options_ui_operations == None:
                    self._scan_options_ui_operations = ScanAppWorkflowUIXSOperations(self)
                return self._scan_options_ui_operations
            elif self.uisize == "S":
                if self._scan_options_ui_operations == None:
                    self._scan_options_ui_operations = ScanAppWorkflowUISOperations(self)
                return self._scan_options_ui_operations
            elif self.uisize == "M":
                if self._scan_options_ui_operations == None:
                    self._scan_options_ui_operations = ScanAppWorkflowUIMOperations(self)
                return self._scan_options_ui_operations
            elif self.uisize == "L":
                if self._scan_options_ui_operations == None:
                    self._scan_options_ui_operations = ScanAppWorkflowUILOperations(self)
                return self._scan_options_ui_operations
            elif self.uisize == "XL":
                if self._scan_options_ui_operations == None:
                    self._scan_options_ui_operations = ScanAppWorkflowUIXLOperations(self)
                return self._scan_options_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def scan_computer(self):
        '''
        Get Scan to computer navigation methods
        '''
        if self.uitype == "ProSelect":
            if self._scan_computer_ui_operations == None:
                self._scan_computer_ui_operations = ComputerAppProSelectUIOperations(self)
            return self._scan_computer_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_computer_ui_operations == None:
                    self._scan_computer_ui_operations = ComputerAppWorkflowUIXSOperations(self)
                return self._scan_computer_ui_operations
            elif self.uisize == "S":
                if self._scan_computer_ui_operations == None:
                    self._scan_computer_ui_operations = ComputerAppWorkflowUISOperations(self)
                return self._scan_computer_ui_operations
            elif self.uisize == "M":
                if self._scan_computer_ui_operations == None:
                    self._scan_computer_ui_operations = ComputerAppWorkflowUIMOperations(self)
                return self._scan_computer_ui_operations
            elif self.uisize == "L":
                if self._scan_computer_ui_operations == None:
                    self._scan_computer_ui_operations = ComputerAppWorkflowUILOperations(self)
                return self._scan_computer_ui_operations
            elif self.uisize == "XL":
                if self._scan_computer_ui_operations == None:
                    self._scan_computer_ui_operations = ComputerAppWorkflowUIXLOperations(self)
                return self._scan_computer_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def sharepoint(self):
        '''
        Get Sharepointr Scan navigation methods
        '''
        if self.uitype == "ProSelect":
            if self._scan_sharepoint_ui_operations == None:
                self._scan_sharepoint_ui_operations = SharePointAppProSelectUIOperations(self)
            return self._scan_sharepoint_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_sharepoint_ui_operations == None:
                    self._scan_sharepoint_ui_operations = SharePointAppWorkflowUIXSOperations(self)
                return self._scan_sharepoint_ui_operations
            elif self.uisize == "S":
                if self._scan_sharepoint_ui_operations == None:
                    self._scan_sharepoint_ui_operations = SharePointAppWorkflowUISOperations(self)
                return self._scan_sharepoint_ui_operations
            elif self.uisize == "M":
                if self._scan_sharepoint_ui_operations == None:
                    self._scan_sharepoint_ui_operations = SharePointAppWorkflowUIMOperations(self)
                return self._scan_sharepoint_ui_operations
            elif self.uisize == "L":
                if self._scan_sharepoint_ui_operations == None:
                    self._scan_sharepoint_ui_operations = SharePointAppWorkflowUILOperations(self)
                return self._scan_sharepoint_ui_operations
            elif self.uisize == "XL":
                if self._scan_sharepoint_ui_operations == None:
                    self._scan_sharepoint_ui_operations = SharePointAppWorkflowUIXLOperations(self)
                return self._scan_sharepoint_ui_operations  
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def usb_scan(self):
        '''
        Get USB Scan navigation methods
        '''
        if self.uitype == "ProSelect":
            if self._scan_usb_ui_operations == None:
                self._scan_usb_ui_operations = UsbScanAppProSelectUIOperations(self)
            return self._scan_usb_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_usb_ui_operations == None:
                    self._scan_usb_ui_operations = UsbScanAppWorkflowUIXSOperations(self)
                return self._scan_usb_ui_operations
            elif self.uisize == "S":
                if self._scan_usb_ui_operations == None:
                    self._scan_usb_ui_operations = UsbScanAppWorkflowUISOperations(self)
                return self._scan_usb_ui_operations
            elif self.uisize == "M":
                if self._scan_usb_ui_operations == None:
                    self._scan_usb_ui_operations = UsbScanAppWorkflowUIMOperations(self)
                return self._scan_usb_ui_operations
            elif self.uisize == "L":
                if self._scan_usb_ui_operations == None:
                    self._scan_usb_ui_operations = UsbScanAppWorkflowUILOperations(self)
                return self._scan_usb_ui_operations
            elif self.uisize == "XL":
                if self._scan_usb_ui_operations == None:
                    self._scan_usb_ui_operations = UsbScanAppWorkflowUIXLOperations(self)
                return self._scan_usb_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def scan_job_storage(self):
        '''
        Get  Scan to JobStorage navigation methods
        '''

        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "S":
                if self._scan_job_storage_ui_operations == None:
                    self._scan_job_storage_ui_operations = JobStorageAppWorkflowUISOperations(self)
                return self._scan_job_storage_ui_operations
            elif self.uisize == "L":
                if self._scan_job_storage_ui_operations == None:
                    self._scan_job_storage_ui_operations = JobStorageAppWorkflowUILOperations(self)
                return self._scan_job_storage_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def network_folder(self):
        '''
        Get Network Folder Scan navigation methods
        '''

        if self.uitype == "ProSelect":
            if self._scan_network_folder_ui_operations == None:
                self._scan_network_folder_ui_operations = NetworkFolderAppProSelectUIOperations(self)
            return self._scan_network_folder_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_network_folder_ui_operations == None:
                    self._scan_network_folder_ui_operations = NetworkFolderAppWorkflowUIXSOperations(self)
                return self._scan_network_folder_ui_operations
            elif self.uisize == "S":
                if self._scan_network_folder_ui_operations == None:
                    self._scan_network_folder_ui_operations = NetworkFolderAppWorkflowUISOperations(self)
                return self._scan_network_folder_ui_operations
            elif self.uisize == "M":
                if self._scan_network_folder_ui_operations == None:
                    self._scan_network_folder_ui_operations = NetworkFolderAppWorkflowUIMOperations(self)
                return self._scan_network_folder_ui_operations
            elif self.uisize == "L":
                if self._scan_network_folder_ui_operations == None:
                    self._scan_network_folder_ui_operations = NetworkFolderAppWorkflowUILOperations(self)
                return self._scan_network_folder_ui_operations
            elif self.uisize == "XL":
                if self._scan_network_folder_ui_operations == None:
                    self._scan_network_folder_ui_operations = NetworkFolderAppWorkflowUIXLOperations(self)
                return self._scan_network_folder_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)

    @property
    def email(self):
        '''
        Get Email Scan methods
        '''
        if self.uitype == "ProSelect":
            if self._scan_email_ui_operations == None:
                self._scan_email_ui_operations = EmailAppProSelectUIOperations(self)
            return self._scan_email_ui_operations
        if self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._scan_email_ui_operations == None:
                    self._scan_email_ui_operations = EmailAppWorkflowUIXSOperations(self)
                return self._scan_email_ui_operations
            elif self.uisize == "S":
                if self._scan_email_ui_operations == None:
                    self._scan_email_ui_operations = EmailAppWorkflowUISOperations(self)
                return self._scan_email_ui_operations
            elif self.uisize == "M":
                if self._scan_email_ui_operations == None:
                    self._scan_email_ui_operations = EmailAppWorkflowUIMOperations(self)
                return self._scan_email_ui_operations
            elif self.uisize == "L":
                if self._scan_email_ui_operations == None:
                    self._scan_email_ui_operations = EmailAppWorkflowUILOperations(self)
                return self._scan_email_ui_operations
            elif self.uisize == "XL":
                if self._scan_email_ui_operations == None:
                    self._scan_email_ui_operations = EmailAppWorkflowUIXLOperations(self)
                return self._scan_email_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
        
    @property
    def hpbuild(self):
        '''
        Get HpBuild Scan methods
        '''
        if self.uitype == "Workflow":
            if self.uisize == "XS":
                if self._scan_hpbuild_ui_operations == None:
                    self._scan_hpbuild_ui_operations = HpBuildAppWorkflowUIXSOperations(self)
                return self._scan_hpbuild_ui_operations
            elif self.uisize == "S":
                if self._scan_hpbuild_ui_operations == None:
                    self._scan_hpbuild_ui_operations = HpBuildAppWorkflowUISOperations(self)
                return self._scan_hpbuild_ui_operations
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        else:
            raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
