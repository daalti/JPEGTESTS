import logging
import sys


from dunetuf.ui.uioperations.ProSelectOperations.ToolsUIProSelectOperations import ToolsUIProSelectOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIHybridOperations.ToolsUIProSelectHybridOperations import ToolsUIProSelectHybridOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ToolsAppWorkflowUISOperations import ToolsAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.ToolsAppWorkflowUIXSOperations import ToolsAppWorkflowUIXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.ToolsAppWorkflowUIMOperations import ToolsAppWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.ToolsAppWorkflowUILOperations import ToolsAppWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.ToolsAppWorkflowUIXLOperations import ToolsAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ToolsAppWorkflow2UISOperations import ToolsAppWorkflow2UISOperations

class spice_tools_app(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._tools_ui_operations = None

    @property
    def toolsapp(self):
        '''
        Get tools methods
        '''
        if self.uitype == "ProSelect":
            if self._tools_ui_operations == None:
                if self.uitheme == "hybridTheme":
                    self._tools_ui_operations = ToolsUIProSelectHybridOperations(self)
                else:
                    self._tools_ui_operations = ToolsUIProSelectOperations(self)
            return self._tools_ui_operations
        elif self.uitype in ["Workflow", "Workflow2"]:
            if self.uisize == "XS":
                if self._tools_ui_operations == None:
                    self._tools_ui_operations = ToolsAppWorkflowUIXSOperations(self)
                return self._tools_ui_operations

            elif self.uisize == "S":
                if self._tools_ui_operations == None:
                    if self.uitype == "Workflow2":
                        self._tools_ui_operations = ToolsAppWorkflow2UISOperations(self)
                    else:
                        self._tools_ui_operations = ToolsAppWorkflowUISOperations(self)
                return self._tools_ui_operations

            elif self.uisize == "M":
                if self._tools_ui_operations == None:
                    self._tools_ui_operations = ToolsAppWorkflowUIMOperations(self)
                return self._tools_ui_operations
                          
            elif self.uisize == "L":
                if self._tools_ui_operations == None:
                    self._tools_ui_operations = ToolsAppWorkflowUILOperations(self)
                return self._tools_ui_operations

            elif self.uisize == "XL":
                if self._tools_ui_operations == None:
                    self._tools_ui_operations = ToolsAppWorkflowUIXLOperations(self)
                return self._tools_ui_operations

            else: 
                raise NotImplementedError('Unimplemented method %s.' % sys._getframe().f_code.co_name + ' uisize reported: %s' % self.uisize)

        else:
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
