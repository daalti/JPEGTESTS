
import logging
from time import sleep
import time
from typing import ClassVar

from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.udw import DuneUnderware


class CopyAppWorkflowUILOperations(CopyAppWorkflowUICommonOperations):

    WAIT_TIMEOUT: ClassVar[float] = 7
    """Default wait timeout (s)."""

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.id_card_copy = spice.idcard_copy_app

    def copy_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "Copy"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.copy_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.copy_button)

    def press_copy_button(self,spice):
        # Press Button "Copy" 
        spice.copy_app.goto(CopyAppWorkflowObjectIds.copy_button)

    def done_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "Done"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.done_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.done_button)

    def press_done_button(self,spice):
        # Press Button "Done"
        spice.copy_app.goto(CopyAppWorkflowObjectIds.done_button)

    def ok_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "ok"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.ok_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.ok_button)

    def press_ok_button(self,spice):
        # Press Button "ok"
        spice.copy_app.goto(CopyAppWorkflowObjectIds.ok_button)

    def eject_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "eject"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.eject_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.eject_button)

    def press_eject_button(self,spice):
        # Press Button "eject"
        spice.copy_app.goto(CopyAppWorkflowObjectIds.eject_button)

    def startscan_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "Start"
        spice.copy_app.wait_until_text_button(CopyAppWorkflowObjectIds.copy_button, CopyAppWorkflowObjectIds.start_button_text, timeout)

    def press_start_button(self,spice):
        # Press button "Start"
        spice.copy_app.goto(CopyAppWorkflowObjectIds.button_startCopy)
    
    def get_insert_page_msg(self,spice, timeout: float = WAIT_TIMEOUT):
        # get "insert page" message 
        obj_text = spice.wait_for(CopyAppWorkflowObjectIds.constraint_string_msg)
        screen_text = obj_text["message"]
        logging.info( "Screen msg:"+ screen_text)
        return screen_text

    def change_color_mode(self,spice,index=0,color_mode={}, timeout: float = WAIT_TIMEOUT):
        # A dictionary {index:color_mode} must be provided
        # See CopyappWorkflowObjectsIds for more details about color options
        scroll_step = 0.1
        try:
            current_button = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_color, timeout)
            current_button.mouse_click()
            current_button = spice.wait_for(color_mode[index], timeout)
            current_button.mouse_click()
        except:
            self.workflow_common_operations.scroll_to_position_vertical(scroll_step, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
            scroll_step =+ scroll_step
        sleep(3)
        
    def change_content_type(self,spice,index=0,content_type={}, timeout: float = WAIT_TIMEOUT):
        # A dictionary {index:content_type} must be provided
        # See CopyappWorkflowObjectsIds for more details about content type options
        scroll_step = 0.1
        try:
            current_button = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_contentType, timeout)
            current_button.mouse_click()
            current_button = spice.wait_for(content_type[index], timeout)
            current_button.mouse_click()
        except:
            self.workflow_common_operations.scroll_to_position_vertical(scroll_step, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
            scroll_step =+ scroll_step
        sleep(3)
        
    def change_quality(self,spice,index=0,quality={}, timeout: float = WAIT_TIMEOUT):
        # A dictionary {index:quality} must be provided
        # See CopyappWorkflowObjectsIds for more details about quality options
        scroll_step = 0.1
        try:
            current_button = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_quality, timeout)
            current_button.mouse_click()
            current_button = spice.wait_for(quality[index], timeout)
            current_button.mouse_click()
        except:
            self.workflow_common_operations.scroll_to_position_vertical(scroll_step, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
            scroll_step =+ scroll_step
        sleep(3)

    def goto_copy(self):
        """
        Purpose: Click on copy App from home screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: None
        """
        current_button = self.get_copy_app()
        current_button.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        logging.info("At Copy Landing Screen")

    def get_copy_app(self):
        """
        Purpose: Click on copy App from home screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param spice: Takes 0 arguments
        :return: copy App
        """
        try:
            # Copied from CopyAppWorkflowUICommonOperations
            self.homemenu.goto_menu(self.spice)
            self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
            copy_app = self.spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy + " MouseArea")
            copy_app.mouse_click()
            # changes made here because the screen is of ButtonTemplate Model. Right Now there is only few options 
            # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        except:
            logging.info("Copy Menu List not available")
        finally:
            return self.spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy_copy + " MouseArea")
    
    def start_copy_from_preview_panel(self, familyname="", adfLoaded = True):
        '''
        Ui Should be in previewpanel
        Click on copy button starts copy
        '''
        self.start_preview()
        time.sleep(2)
        self.verify_preview()
        time.sleep(2)
        self.start_copy_from_secondary_panel(familyname, adfLoaded)
        time.sleep(2)
    
    def verify_preview(self):
        '''
        Ui Should be in previewpanel
        Verif preview
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.fitapge_layout, timeout =9.0)
        self.spice.wait_for(CopyAppWorkflowObjectIds.first_preview_image, timeout =9.0)
    
    def start_copy_from_secondary_panel(self, familyname = "", adfLoaded = True, prompt_for_additional_pages = False):
        '''
        Ui Should be in secondary panel
        Click on copy button starts copy
        '''
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy_preivewpanel)
        self.spice.wait_until(lambda: current_button["enabled"] is True, 20)
        current_button.mouse_click()
        time.sleep(2)
        if familyname == "enterprise":
            try:
                if adfLoaded == False and prompt_for_additional_pages:
                    current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copy_add_page_done)
                    current_button.mouse_click()
            except Exception:
                logging.info("flatbed Add page is not available")

    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        time.sleep(10)
        if (self.spice.query_item(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions)["visible"] == True):
            current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions)
            current_button.mouse_click()
            self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(3)

    def check_spec_on_copy_options_color(self, net, checkoption = "all"):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        if checkoption == "color":
            logging.info("check the string about Color, (color)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            time.sleep(2)
        elif checkoption == "grayscale":
            logging.info("check the string about Color, (Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            time.sleep(2)
        elif checkoption == "all":
            logging.info("check the string about Color, (color, Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            time.sleep(2) 
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.row_combo_copySettings_color)
        current_button.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def check_spec_on_copy_options_auto_color(self, net):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        logging.info("check the string about Color, (Automatic, Color, Grayscale)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_automatic_str_id, CopyAppWorkflowObjectIds.combo_color_option_automatic)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
        #logging.info("verify the back button existed")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copySettings_color)
        current_button.mouse_click()

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
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image)
        logging.info("close content type setting popup")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.row_combo_copySettings_contentType)
        current_button.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 200)

    def check_spec_on_copy_options_quality(self, net):
        """
        Check spec on COPY_OptionsQuality
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsQuality")
        logging.info("check the string about Quality, (Standard, Draft, Best)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_standard_str_id, CopyAppWorkflowObjectIds.combo_quality_option_standard)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_best_str_id, CopyAppWorkflowObjectIds.combo_quality_option_best)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_quality_draft_str_id, CopyAppWorkflowObjectIds.combo_quality_option_draft)
        logging.info("close quality setting popup")
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copySettings_quality)
        current_button.mouse_click()

    def check_spec_copy_options_pages_per_sheet(self, net):
        """
        check spec on copy_OptionsPagesPerSheet
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsPagesPerSheet")
        logging.info("check the string about pages per sheet, (1, 2)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_pagesPerSheet_oneup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_1)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_pagesPerSheet_twoup_str_id, CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2)
        logging.info("close pages per sheet setting popup")
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_pagesPerSheet)
        current_button.mouse_click()

    def check_copy_options_sides_and_select_side(self, net, side = "1_1_sided"):
        """
        check spec on copy_OptionsSides
        @param net:
        @return:
        """
        logging.info("check check on copy_OptionsSides")
        logging.info("check the string about Sides, (1 to 1-Sided, 1 to 2-Sided, 2 to 1-Sided, 2 to 2-Sided)")
        sides_options_dict = {
            "1_1_sided": [CopyAppWorkflowObjectIds.copy_sides_1to1_str_id, f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided}"],
            "1_2_sided": [CopyAppWorkflowObjectIds.copy_sides_1to2_str_id, f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided}"],
            "2_1_sided": [CopyAppWorkflowObjectIds.copy_sides_2to1_str_id, f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided}"],
            "2_2_sided": [CopyAppWorkflowObjectIds.copy_sides_2to2_str_id, f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided}"],
        }
        for side_mode in sides_options_dict.values():
            self.workflow_common_operations.goto_item([side_mode[1], CopyAppWorkflowObjectIds.spiceView], CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list,scrollbar_objectname = CopyAppWorkflowObjectIds.copy_side_scrollbar, select_option=False)
            self.workflow_common_operations.verify_string(net, side_mode[0], side_mode[1])
        logging.info("Click on Copy Side Option")
        copy_side_option = self.sides_options_dict.get(side)
        self.workflow_common_operations.goto_item([copy_side_option, CopyAppWorkflowObjectIds.spiceView], CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list,scrollbar_objectname = CopyAppWorkflowObjectIds.copy_side_scrollbar, select_option=False)
        current_button = self.spice.wait_for(copy_side_option, timeout = 9.0)
        current_button.mouse_click()

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

    def select_copy_quickset_landing(self, quickset_name):
        '''
        This is helper method to select copy quickset
        UI flow Select Copy landing view-> click on quickset
        '''
        logging.info("Select quickset by quickset name")
        quickset_item = self.spice.wait_for(quickset_name)
        quickset_item.mouse_click()
        time.sleep(2)
        assert self.spice.query_item(quickset_name)["checked"]

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
            "1_1_sided": f"{CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list} {CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided}",
            "1_2_sided": f"{CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list} {CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided}",
            "2_1_sided": f"{CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list} {CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided}",
            "2_2_sided": f"{CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list} {CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided}"
        }
        to_select_item = sides_options_dict.get(side_mode)

        current_button = self.spice.query_item(to_select_item)
        assert current_button['visible'] == False

        # Select 1-1sided option
        select_side_option = self.spice.query_item(CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided)
        select_side_option.mouse_click()

    def select_quality_option(self, option):
        '''
        This is helper method to select quality
        UI flow Select QualityList view-> click on any quality
        '''
        self.goto_quality_option()
        time.sleep(3)
        if option == "Standard":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_standard + "")
        elif option == "Best":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_best + "")
        elif option == "Draft":
            current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_quality_option_draft + "")
        else:
            raise Exception(f"Invalid quality type <{option}>")

        current_button.mouse_click( y = current_button["height"] / 2 )
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

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

    def select_color_mode_landing(self, option):
        #colorMode on landing
        self.goto_copy_landing_option_color_screen()
        time.sleep(5)
        if option == "Automatic":
            option = CopyAppWorkflowObjectIds.combo_color_option_automatic + ""
        elif option == "Color":
            option = CopyAppWorkflowObjectIds.combo_color_option_color + ""
        elif option == "Grayscale":
            option = CopyAppWorkflowObjectIds.combo_color_option_grayscale + ""
        else:
            raise Exception(f"Invalid color type <{option}>")

        self.workflow_common_operations.goto_item(option, 
            CopyAppWorkflowObjectIds.view_copySettings_color, 
            scrollbar_objectname=CopyAppWorkflowObjectIds.copy_side_scrollbar,
            select_option=False)
        
        current_button = self.spice.query_item(option)
        current_button.mouse_click()
        time.sleep(1)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout =9.0)

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

    def check_copy_side_constrained(self, net, side_mode:str, constrained_message: str = ""):
        self.goto_sides_option()
        sides_options_dict = {
            "1_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided}",
            "1_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided}",
            "2_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided}",
            "2_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided}",
        }
        to_select_item = sides_options_dict.get(side_mode)
        self.workflow_common_operations.goto_item([to_select_item, CopyAppWorkflowObjectIds.spiceView], CopyAppWorkflowObjectIds.view_copySettings_sides_popup_list,
            scrollbar_objectname = CopyAppWorkflowObjectIds.copy_side_scrollbar, select_option=False)
        current_button = self.spice.query_item(to_select_item + "")  
        current_button.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.constraint_string_msg)

        super().verify_constrained_message(net, constrained_message)
        okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView, timeout = 9.0)

    def goto_preview_panel(self):
        '''
        This is helper method to preview panel settings
        UI flow Landing Page-> click on exapndbutton -> click on previewbutton
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)

        assert self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy, timeout=60.0)
        copy_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_startCopy)["enabled"]
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.button_collapse_secondarypanel, timeout=9.0)
        time.sleep(3)
        copy_expand_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_collapse_secondarypanel)
        copy_expand_button.mouse_click()
        time.sleep(3)

    def goto_preview_panel_after_copy_complete(self):
        '''
        This is a function for UI L size.
        In Common, it is the same as the existing preview entry method, and in L size can only enter the preview by clicking the drop down button.
        '''
        drop_down_button = self.spice.wait_for(CopyAppWorkflowObjectIds.drop_down_button)
        drop_down_button.mouse_click()
        time.sleep(3)
        copy_expand_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_collapse_secondarypanel)
        copy_expand_button.mouse_click()

    def goto_main_panel(self):
        '''
        This is helper method to go to main panel
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        copy_expand_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_expand_secondarypanel)
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

    def go_to_preview_and_come_back_homescreen(self):
        '''
        Ui Should be in preview
        go to preview --> go back home screen
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy, timeout=60.0)

        copy_expand_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_collapse_secondarypanel)
        copy_expand_button.mouse_click()
        time.sleep(3)

        self.spice.wait_for(CopyAppWorkflowObjectIds.preview_panel, timeout=9.0)
        self.spice.wait_for(CopyAppWorkflowObjectIds.button_preview_large, timeout=9.0)
        copy_preview_button = self.spice.query_item(CopyAppWorkflowObjectIds.button_preview_large)
        copy_preview_button.mouse_click()
        time.sleep(3)
        self.spice.goto_homescreen()
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        current_button.mouse_click()

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

    def has_lock_icon(self):
        self.get_copy_app()
        try:
            lock_icon = self.spice.wait_for(CopyAppWorkflowObjectIds.button_menu_copy_copy + " #statusIconRect SpiceLottieImageView")
        except:
            logging.info("Failed to find lock icon")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return True

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
        
    def goto_documentcopy_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> Copy >> Document copy
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyApp + " MouseArea")
        document_copy_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyApp + " MouseArea")
        document_copy_button.mouse_click()

    def goto_idcopy_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> Copy >> idcopy copy
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.button_id_card_copy + " MouseArea")
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_id_card_copy + " MouseArea")
        current_button.mouse_click()

    def goto_copy_options_list_from_idcopy(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from IDCopy screen.
        UI Flow is IDCopy->Options
        '''
		# Wait for Options screen
        currentScreen = self.spice.wait_for(CopyAppWorkflowObjectIds.view_idCopyScreen)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyMoreOptions)
        current_button.mouse_click()
        #assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)
        logging.info("UI: At Options in IDCopy")    

    def goto_copywidget_option_landingview_fromhomescreen(self):
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> copywidget option >> copylanding view
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copy_widgetCardCopyApp_screen)
        copywidget_option_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_widget_gotoCopyApp)
        copywidget_option_button.mouse_click()

    def verify_copy_content_orientation_constrained(self, net, constrained_message: str = ""):
        """
        Go to content orientation option menu and verify that option is cosntrained
        @return:
        """

        logging.info("Go to content orientation option menu")
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView,
                                    CopyAppWorkflowObjectIds.settings_copy_orientation,
                                    scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

        super().verify_constrained_message(net, constrained_message)

        ok_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()