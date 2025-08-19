import logging
import time
from dunetuf.ui.uioperations.BaseOperations.ITraysAppUIOperations import ITraysAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.TraysAppWorkflowObjectIds import TraysAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.configuration import Configuration

class TraysAppWorkflowUICommonOperations(ITraysAppUIOperations):

    def __init__(self, spice):
        self.TraysAppWorkflowObjectIds = TraysAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.maxtimeout = 120
        self._spice = spice

    def goto_tray1(self):
        '''
        Navigates to Tray1 from Home Screen
        UI Flow is Home->Menu->Trays->Tray1
        '''
        self._spice.homeMenuUI().goto_menu_trays(self._spice)
        tray1QueryIndex = 0
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_tray, query_index = tray1QueryIndex).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_details)

    def goto_tray2(self):
        '''
        Navigates to Tray2 from Home Screen
        UI Flow is Home->Menu->Trays->Tray2
        '''
        self._spice.homeMenuUI().goto_menu_trays(self._spice)
        tray2QueryIndex = 1
        self.workflow_common_operations.scroll_to_position_vertical(0.3,"#verticalScroll")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_tray, query_index = tray2QueryIndex).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_details)

    def goto_modifyTray(self):
        '''
        Navigates to TrayX Paper Size and Type
        UI Should be in the specific Tray screen
        '''
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_modify_in_tray_detail).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_configuration)

    def modify_tray_size_letter(self):
        print("Click on Media Size Option")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_size_settings).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_size_selection)

        print("Click on Paper Size Letter")
        paperSizeLetterBtn = WorkflowUICommonOperations(self._spice)
        paperSizeLetterBtn.goto_item(menu_item_id = TraysAppWorkflowObjectIds.letter_size, screen_id ="#mediaSizeListView", select_option = True,scrollbar_objectname = "#mediaSizeListViewScrollBar")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_size_settings)

    def modify_tray_type_plain(self):
        print("Click on Media Type Option")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_type_settings).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_type_selection)

        print("Click on Paper Type Plain")
        paperTypePlainBtn = WorkflowUICommonOperations(self._spice)
        paperTypePlainBtn.goto_item(menu_item_id = TraysAppWorkflowObjectIds.plain_type, screen_id ="#mediaTypeListView", select_option = True,scrollbar_objectname = "#mediaTypeListViewScrollBar")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_type_settings)

    def finish_modifyTray(self):
        print("Click Done to finish modifying Paper Size and Type")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_done).mouse_click()

    def verify_tray_media_size_string_a5_and_a5_rotated(self):
        '''
        Verify tray media sizes a5 and a5 rotated have the expected string
        UI Should be in the specific Tray screen
        '''
        print("Click on modify Button")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_modify_in_tray_detail).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_configuration)

        print("Click on Media Size Option")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_size_settings).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_size_selection)

        print("verify a5 paper size has no junk charecters")
        a5radioButton = self._spice.wait_for(TraysAppWorkflowObjectIds.radio_button_a5)
        assert a5radioButton["text"] == "A5 (148x210 mm)" , "Mismatch observed in A5 media size"

        print("verify a5 rotated paper size has no junk charecters")
        a5rotatedradioButton = self._spice.wait_for(TraysAppWorkflowObjectIds.radio_buttom_a5_rotated)
        assert a5rotatedradioButton["text"] == "A5 ▭ (148x210 mm)", "Mismatch observed in A5 rotated media size"

        print("Navigate back to the previous screen")
        self._spice.query_item(TraysAppWorkflowObjectIds.button_tray_configuration_back).mouse_click()
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_configuration)
        if self._spice.uisize == "XS":
            self._spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")

        print("Navigate back to the Trays Screen")
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_cancel).mouse_click()
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_menuTrays)

    def goto_tray_modify_screen(self):
        # # Click on the 'Modify' button
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_modify_in_tray_detail).mouse_click(10,10)
        time.sleep(3)
        logging.info("At tray1 modify Screen")
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_tray_configuration)

    def goto_tray_media_size_settings_screen(self):
        # Click on the 'Size Modify' selection
        self._spice.wait_for(TraysAppWorkflowObjectIds.button_media_size_settings).mouse_click()
        logging.info("At tray1 media size settings Screen")
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_size_selection)

    def verify_custom_media_size(self):
        self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_size_selection)
        self.workflow_common_operations.goto_item(TraysAppWorkflowObjectIds.radio_custom, "#panelsStack #mediaSizeListView", select_option= False, scrolling_value=1, scrollbar_objectname="#panelsStack #mediaSizeListViewScrollBar")
        assert self._spice.wait_for(TraysAppWorkflowObjectIds.radio_custom)

    def goto_custom_media_size(self):
        time.sleep(2)
        self._spice.wait_for(TraysAppWorkflowObjectIds.view_media_size_selection)
        self.workflow_common_operations.goto_item(TraysAppWorkflowObjectIds.radio_custom, "#panelsStack #mediaSizeListView", select_option= False, scrolling_value=1, scrollbar_objectname="#panelsStack #mediaSizeListViewScrollBar")
        time.sleep(2)
        self._spice.wait_for(TraysAppWorkflowObjectIds.radio_custom).mouse_click()

    def enter_value_numkeypad(self, value, unit):
        """
        Purpose: Input number in x or y diemesion area
        return: None
        """
        digits = [int(digit) for digit in str(value)]
        for i in digits:
            self._spice.wait_for(f"#key{i}PositiveIntegerKeypad").mouse_click() if unit == "mm" else self._spice.wait_for(f"#key{i}PositiveDecimalKeypad").mouse_click()
            time.sleep(1)
        self._spice.wait_for("#enterKeyPositiveIntegerKeypad").mouse_click() if unit == "mm" else self._spice.wait_for("#enterKeyPositiveDecimalKeypad").mouse_click()

    def setRange_custom_media_size(self, unit, value_x, value_y):
        # Unit
        self._spice.wait_for("#SettingsComboBox #SettingsSpiceComboBox").mouse_click()
        time.sleep(2)
        if unit=="mm":
            self._spice.wait_for("#SettingsSpiceComboBoxpopupList #comboListMillimeter").mouse_click()
        elif unit == 'inch':
            self._spice.wait_for("#SettingsSpiceComboBoxpopupList #comboListInches").mouse_click()
        time.sleep(2)
        btn = self._spice.wait_for("#SettingsSpinBox #xDimexsionSpinBox #SpinBoxTextInput")
        btn.mouse_click()
        time.sleep(2)
        self.enter_value_numkeypad(value_x, unit)
        btn = self._spice.wait_for("#SettingsSpinBox #yDimexsionSpinBox #SpinBoxTextInput")
        time.sleep(2)
        btn.mouse_click()
        time.sleep(2)
        self.enter_value_numkeypad(value_y, unit)

    def setValue_custom_media_size(self):
        self._spice.wait_for(TraysAppWorkflowObjectIds.custom_done_button).mouse_click()

    def verify_custom_media_size_value(self, unit, value_x, value_y):
        # verify changed values
        time.sleep(2)
        result = self._spice.wait_for(TraysAppWorkflowObjectIds.radio_custom_value)['text']
        if unit=="mm":
            value_x = "{:d}".format(round(value_x, 0))
            value_y = "{:d}".format(round(value_y, 0))
            ref = f"({value_x}x{value_y} mm)"
        elif unit == 'inch':
            value_x = "{:.2f}".format(round(value_x, 0))
            value_y = "{:.2f}".format(round(value_y, 0))
            ref = f"({value_x}x{value_y} in.)"
        assert result == ref, "Not matched"





