import time
import logging

from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowObjectIds import IDCardCopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations


class IDCardCopyAppWorkflowUISOperations(IDCardCopyAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.IDCardCopyAppWorkflowObjectIds = IDCardCopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

    def set_copy_settings(self, cdm):
        self.goto_copy_options_list()

        #contentorientation
        # TODO Uncomment this once the orientation for IdcardCopy is implemented
        # menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_orientation, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_orientation]
        # self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        # assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_orientation)
        # self.spice.wait_for(f"{IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_landscape} {IDCardCopyAppWorkflowObjectIds.text_view}").mouse_click()
        # assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)

        #colorMode
        if cdm.device_feature_cdm.is_color_supported(): 
            menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idCopySettings_color, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color]
            self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
            assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_color)
            self.spice.wait_for(f"{IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_color} {IDCardCopyAppWorkflowObjectIds.text_view}").mouse_click()
            assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)

        #Paper tray
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_paperTray, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_paperTray)
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray1).mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)

        #lighter darker
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_slider_lighterDarker, IDCardCopyAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        self.set_scan_settings_lighter_darker(8)

        # quality
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_quality, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_quality]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_quality)
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_draft).mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)