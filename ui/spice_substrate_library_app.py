import sys

# from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowUIXSOperations import MenuAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryAppWorkflowUICommonOperations import SubstrateLibraryAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.SubstrateLibraryAppWorkflowUILOperations import SubstrateLibraryAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.SubstrateLibraryAppWorkflowUIMOperations import SubstrateLibraryAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.SubstrateLibraryAppWorkflowUISOperations import SubstrateLibraryAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.SubstrateLibraryAppWorkflowUIXLOperations import SubstrateLibraryAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.SubstrateLibraryAppWorkflowUIXSOperations import SubstrateLibraryAppWorkflowUIXSOperations
class spice_substrate_library_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        
    def substrateLibraryUI(self):
        if self.uitype == "ProSelect":
            # return SubstrateLibraryProSelectUIOperations(self)
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        if self.uitype in ["Workflow", "Workflow2"]:
            print ("UI Size: " + self.uisize)
            # return SubstrateLibraryAppWorkflowUICommonOperations(self)
            if self.uisize == "XS":
                return SubstrateLibraryAppWorkflowUIXSOperations(self)
            elif self.uisize == "S":
                return SubstrateLibraryAppWorkflowUISOperations(self)
            elif self.uisize == "M":
                return SubstrateLibraryAppWorkflowUIMOperations(self)
            elif self.uisize == "L":
                return SubstrateLibraryAppWorkflowUILOperations(self)  
            elif self.uisize == "XL":
                return SubstrateLibraryAppWorkflowUIXLOperations(self)
            else:
                raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)      
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)