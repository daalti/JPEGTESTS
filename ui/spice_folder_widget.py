'''Note :This class is used for switching between UI type and size. No implementation to be added here.'''

import logging
import sys

from dunetuf.ui.uioperations.WorkflowOperations.FolderWidgetWorkflowUICommonOperations import FolderWidgetWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.FolderWidgetWorkflowUISOperations import FolderWidgetWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.FolderWidgetWorkflowUIXLOperations import FolderWidgetWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIMOperations.FolderWidgetWorkflowUIMOperations import FolderWidgetWorkflowUIMOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.FolderWidgetWorkflowUILOperations import FolderWidgetWorkflowUILOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.FolderWidgetWorkflowUIXSOperations import FolderWidgetWorkflowUIXSOperations


class spice_folder_widget(object):

    uitype = None
    uisize = None
    
    def __init__(self, experience, size):

        uitype = experience
        uisize = size
        self._folder_widget_ui_operations = None


    def folderwidget_ui(self):
        return FolderWidgetWorkflowUIOperations(self)
        #raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)


    @property
    def folder_widget(self):
        '''
        Get Folder Widget methods
        '''
        self.uitype == "Workflow" ##{PR114945} TODO what is this syntax?
        if self.uisize == "XS":
            if self._folder_widget_ui_operations == None:
                self._folder_widget_ui_operations = FolderWidgetWorkflowUIXSOperations(self)
        elif self.uisize == "S":
            if self._folder_widget_ui_operations == None:
                self._folder_widget_ui_operations = FolderWidgetWorkflowUISOperations(self)
        elif self.uisize == "M":
            if self._folder_widget_ui_operations == None:
                self._folder_widget_ui_operations = FolderWidgetWorkflowUIMOperations(self)
        elif self.uisize == "L":
            if self._folder_widget_ui_operations == None:
                self._folder_widget_ui_operations = FolderWidgetWorkflowUILOperations(self)
        elif self.uisize == "XL":
            if self._folder_widget_ui_operations == None:
                self._folder_widget_ui_operations = FolderWidgetWorkflowUIXLOperations(self)
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)
        return self._folder_widget_ui_operations
        #raise NotImplementedError('Unimplemented method for workflow UI %s' % sys._getframe().f_code.co_name)
