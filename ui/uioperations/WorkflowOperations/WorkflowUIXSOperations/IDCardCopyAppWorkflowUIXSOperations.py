
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowObjectIds import IDCardCopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations

class IDCardCopyAppWorkflowUIXSOperations(IDCardCopyAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
    
    def check_spec_on_idcopy_screen(self, net):
        """
        According to the document, there is no "Copy" string on ID Card copy button. The purpose of this method is to check the status and visible of the Copy button 
        @param net:
        @return:
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        #self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_button_copy_str_id, IDCardCopyAppWorkflowObjectIds.button_startIDCopy)
        logging.info("verify the startIDCopy button existed")
        button_startIDCopy = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_startIDCopy)
        logging.info("verify the startIDCopy button is visible")
        self.spice.wait_until(lambda: button_startIDCopy["visible"] is True)
