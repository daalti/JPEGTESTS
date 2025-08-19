
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations

class CopyAppWorkflowUIMOperations(CopyAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.CopyAppWorkflowObjectIds = CopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.id_card_copy = IDCardCopyAppWorkflowUICommonOperations(self.spice)

    def goto_preview_panel(self):
        '''
        This is helper method to preview panel settings
        UI flow Landing Page-> click on exapndbutton -> click on previewbutton
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        copy_expand_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_collapse_secondarypanel, timeout=9.0)
        copy_expand_button.mouse_click()
        time.sleep(3)
        
    def start_preview(self):
        '''
        Ui Should be in previewpanel
        Click on preview button starts preview
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.preview_panel, timeout=9.0)
        copy_expand_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_preview_large)
        copy_expand_button.mouse_click()

    def verify_preview(self):
        '''
        Ui Should be in previewpanel
        Verif preview
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.fitapge_layout, timeout =9.0)
        self.spice.wait_for(CopyAppWorkflowObjectIds.first_preview_image, timeout =9.0)

    def check_preview_button_visible(self):
        '''
        Ui Should be in previewpanel
        Check preview button visibility
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.preview_panel)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.preview_panel)

        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_preview_large)
        assert current_button["visible"] == True
        time.sleep(2)

    def goto_main_panel(self):
        '''
        This is helper method to go to main panel
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        copy_expand_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_expand_secondarypanel)
        copy_expand_button.mouse_click()
        time.sleep(3)
    
    def select_color_mode(self, option):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to color mode screen.
        UI Flow is setting option->color mode->select color
        '''
        self.goto_copy_option_color_screen()
        time.sleep(5)
        if option == "Automatic":
            option = CopyAppWorkflowObjectIds.combo_color_option_automatic + ""
        elif option == "Color":
            option = CopyAppWorkflowObjectIds.combo_color_option_color + ""
        elif option == "Grayscale":
            option = CopyAppWorkflowObjectIds.combo_color_option_grayscale
        else:
            raise Exception(f"Invalid color type <{option}>")
        
        self.workflow_common_operations.goto_item(option, 
            CopyAppWorkflowObjectIds.view_copySettings_color, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_side_scrollbar,
            select_option=False)
        
        current_button = self.spice.query_item(option)
        current_button.mouse_click()
        time.sleep(1)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def select_paper_tray_option(self, selected_option):
        # Paper Tray
        #self.go_to_paper_selection()
        self.goto_copy_paper_tray_screen()
        time.sleep(2)
        tray_options_dict = {
            "Tray 1": CopyAppWorkflowObjectIds.combo_paperTray_option_tray1,
            "Tray 2": CopyAppWorkflowObjectIds.combo_paperTray_option_tray2,
            "Tray 3": CopyAppWorkflowObjectIds.combo_paperTray_option_tray3,
            "Tray 4": CopyAppWorkflowObjectIds.combo_paperTray_option_tray4,
            "Tray 5": CopyAppWorkflowObjectIds.combo_paperTray_option_tray5,
            "Tray 6": CopyAppWorkflowObjectIds.combo_paperTray_option_tray6,
            "Tray Alternate": CopyAppWorkflowObjectIds.combo_paperTray_option_alternate,
            "Tray Main": CopyAppWorkflowObjectIds.combo_paperTray_option_main,
            "Manual feed": CopyAppWorkflowObjectIds.combo_paperTray_option_manual
        }
        if selected_option == "Tray 1" or selected_option == "Tray 2" or selected_option == "Tray 3" or selected_option == "Tray Alternate" or selected_option == "Tray Main" or selected_option == "Manual feed":
            to_select_item = tray_options_dict.get(selected_option)
            self.workflow_common_operations.goto_item(to_select_item,"#copy_paperSourceComboBoxpopupList",scrollbar_objectname="#comboBoxScrollBar",select_option=False)
            current_button = self.spice.query_item(to_select_item)
        else:
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_paperTray_option_auto)
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection, timeout = 9.0)
        
    def select_copy_side(self, side_mode:str):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to side mode screen.
        UI Flow is setting option->side mode->select side
        '''
        #self.goto_copy_options_list()
        self.goto_sides_option()
        time.sleep(2)
        sides_options_dict = {
            "1_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided}",
            "1_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided}",
            "2_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided}",
            "2_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided}",
        }
        to_select_item = sides_options_dict.get(side_mode)
        if side_mode == "1_1_sided":
            current_button = self.spice.query_item(to_select_item + "")
        else:
            self.workflow_common_operations.goto_item([to_select_item, CopyAppWorkflowObjectIds.spiceView], CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list,
                scrollbar_objectname = CopyAppWorkflowObjectIds.copy_side_scrollbar, select_option=False)
            current_button = self.spice.query_item(to_select_item + "")
        current_button.mouse_click()
        time.sleep(3)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)
        
    def check_copy_options_sides_and_select_side(self, net, side = "1_1_sided"):
        """
        check spec on copy_OptionsSides
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsSides")
        logging.info("check the string about Sides, (1 to 1-Sided, 1 to 2-Sided, 2 to 1-Sided, 2 to 2-Sided)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_1to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_1to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_2to1_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_sides_2to2_str_id, CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided)
        logging.info("close sides setting popup")
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_sides)
        current_button.mouse_click()

    def goto_copy_quickset_view(self):
        '''
        This is helper method to goto copy quickset view list
        '''
        if not self.is_quickset_existing():
            return 

        view_all_btn = self.spice.wait_for(CopyAppWorkflowObjectIds.view_all_locator)
        
        isEntered = False
        step_value = 0
        while (isEntered is False and step_value <= 1):
            try:
                self.workflow_common_operations.scroll_to_position_vertical(step_value, CopyAppWorkflowObjectIds.qs_scroll_horizontal_bar)
                time.sleep(5)
                view_all_btn.mouse_click()
                self.spice.wait_for(CopyAppWorkflowObjectIds.quickset_list_box,timeout=0.9)
                isEntered = self.spice.query_item(CopyAppWorkflowObjectIds.quickset_list_box)["visible"]
                
            except Exception as e:
                logging.info("exception msg %s", e)
                if str(e).find("Item matching '" + CopyAppWorkflowObjectIds.quickset_list_box + "' not found") != -1:
                    step_value = step_value + 0.1
                    pass

    def select_copy_quickset(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select QuicksetList view-> click on any quickset
        '''
        time.sleep(7)
        if quickset_name == CopyAppWorkflowObjectIds.default_quickset_button:
            # for workflow, default quickset will not displayed in quickset list view, have to select it on copy home screen
            self.spice.query_item(CopyAppWorkflowObjectIds.close_button_under_quick_sets_view).mouse_click()
            time.sleep(2)
            assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
            default_quickset_item = self.spice.query_item(quickset_name)
            default_quickset_item.mouse_click()
            time.sleep(3)
            assert self.spice.query_item(quickset_name)["checked"]
            return

        logging.info("Select quickset by quickset name")
        quickset_item = self.spice.wait_for(CopyAppWorkflowObjectIds.quickset_list_box + " " + quickset_name)
        quickset_item.mouse_click()
        time.sleep(7)
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)

    def check_copy_side_not_visible(self, side_mode:str):
        '''
        UI should be in Settings option view screen.
        Navigates to Side screen starting from Option to side mode screen.
        check is option available or not
        UI Flow is Landing->option->side mode
        '''
        self.goto_sides_option()
        time.sleep(2)
        sides_options_dict = {
            "1_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided} {CopyAppWorkflowObjectIds.text_view}",
            "1_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided} {CopyAppWorkflowObjectIds.text_view}",
            "2_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided} {CopyAppWorkflowObjectIds.text_view}",
            "2_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided} {CopyAppWorkflowObjectIds.text_view}",
        }
        to_select_item = sides_options_dict.get(side_mode)

        current_button = self.spice.query_item(to_select_item)
        assert current_button["visible"] == False
        side_view_close_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copySettings_sides)
        side_view_close_button.mouse_click()

        # Select 1-1sided option
        select_side_option = self.spice.query_item(CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided)
        select_side_option.mouse_click()

    def set_copy_custom_value_option(self, input_value=0):
        """
        set output scale custom value
        @return:
        """
        time.sleep(2)
        logging.info("set output scale custom value")
        custom_Element = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.spinbox_copySettings_outputScale_custom} {CopyAppWorkflowObjectIds.spinBox_numberOfCopies_textArea}")
        custom_Element.mouse_click()
        time.sleep(2)
        custom_Element["text"] = input_value
        try:
            ok_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
            time.sleep(2)
            ok_button.mouse_click()
            time.sleep(2)
        except  TimeoutError:
            logging.info('keypad is not displayed')

    def set_copy_2sided_flip_up_options(self, two_sided_options="off"):
        """
        Set the status of 2side flip up option
        @param two_sided_options:str -> on/off
        @return:
        """
        msg = f"Set 2sided_options to {two_sided_options}"
        logging.info(msg)

        menu_item_id = [CopyAppWorkflowObjectIds.row_toggle_copySettings_pageFlipup, CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp ]
        self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, select_option=False )
        active_item = self.spice.query_item(CopyAppWorkflowObjectIds.toggle_copySettings_pageFlipUp + " MouseArea")
        is_2sided_options_checked = self.get_copy_2sided_pages_flip_up_status()

        if two_sided_options == "off" and is_2sided_options_checked:
            logging.info("need to turn off 2 sided option")
            active_item.mouse_click()

        if two_sided_options == "on" and not is_2sided_options_checked:
            logging.info("need to turn on 2 sided option")
            active_item.mouse_click()

    def check_spec_on_copy_options_content_type(self, net, configuration):
        """
        Check spec on COPY_OptionsContentType
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsContentType")
        logging.info("check the string about Content Type, (Mixed, Text, PhotoGraph)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_text_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_text)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_photo_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_photograph)
        self.workflow_common_operations.goto_item(CopyAppWorkflowObjectIds.combo_contentType_option_mixed, CopyAppWorkflowObjectIds.view_copySettings_contentType, 
        scrollbar_objectname = CopyAppWorkflowObjectIds.standard_sizes_scrollbar, select_option=False)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
        self.workflow_common_operations.goto_item(CopyAppWorkflowObjectIds.combo_contentType_option_image, CopyAppWorkflowObjectIds.view_copySettings_contentType, 
        scrollbar_objectname = CopyAppWorkflowObjectIds.standard_sizes_scrollbar, select_option=False)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image)
        logging.info("close content type setting popup")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copySettings_contentType)
        current_button.mouse_click()
