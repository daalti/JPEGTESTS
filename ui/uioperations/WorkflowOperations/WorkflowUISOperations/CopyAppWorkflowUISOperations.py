
import logging
import time
from typing import ClassVar

from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowUICommonOperations import IDCardCopyAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper


class CopyAppWorkflowUISOperations(CopyAppWorkflowUICommonOperations):

    WAIT_TIMEOUT = CopyAppWorkflowUICommonOperations.WAIT_TIMEOUT

    sides_options_locked_dict = {
        "1_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_1_sided_radio_button}",
        "1_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_1_2_sided_radio_button}",
        "2_1_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_1_sided_radio_button}",
        "2_2_sided": f"{CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided_radio_button}",
    }
    
    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.id_card_copy = IDCardCopyAppWorkflowUICommonOperations(self.spice)

    def copy_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "Copy"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.copy_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.copy_button)

    def press_copy_button(self,spice):
        # Press Button "Copy" 
        spice.copy_app.goto(CopyAppWorkflowObjectIds.copy_button)

    def goto_copy_from_copyapp_at_home_screen(self,scroll=True):
        """
        Purpose: Navigates to Copy app screen by clicking copy icon on Home screen
        Ui Flow: Any screen -> Home screen -> Copy app
        :param scroll: Boolean, indicates whether we want to scroll right to find 
                       the Copy app before clicking
        :param spice : Takes 0 arguments
        :return: None
        """
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0)
        time.sleep(1)
        # 
        try:
            copy_icon = self.spice.wait_for(CopyAppWorkflowObjectIds.copyFolder_home_screen + " MouseArea", 3)
            # First enter the copyFolder on the home screen -- id: '#copy'
            logging.info("Entering Copy folder from Home screen since for Product supoort ID card copy should click '#copy' firstly")
            copy_icon.mouse_click()
            # Then open the copy app itself
        except:
            logging.info("The current product could not support ID Card Copy App")
            self.workflow_common_operations.scroll_to_position_horizontal(0)

        logging.info("Launching Copy App")
        copy_icon = self.spice.wait_for(CopyAppWorkflowObjectIds.button_copyApp + " MouseArea")
        copy_icon.mouse_click()
        copy_home = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        self.spice.wait_until(lambda: copy_home["visible"] == True)
        logging.info("At Copy Landing Screen")

    def validate_add_page_media_sizes(self, cdm):
        """
        Purpose: Validate the media sizes available in Add Page prompt screen
        @return:
        """
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_add_page_prompt_view)
        logging.info("At AddPage prompt with original media sizes screen")

        scroll_bar_step_value = 0.04
        add_page_prompt_media_sizes_list = self.get_add_page_media_sizes_list_from_cdm(cdm)

        self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, CopyAppWorkflowObjectIds.add_page_prompt_scroll_bar)

        for media in add_page_prompt_media_sizes_list:
            scroll_bar_step_value = scroll_bar_step_value + 0.05

            media_size_id_radio_button = self.spice.wait_for(f"{CopyAppWorkflowObjectIds.add_page_content_id} " + media)

            self.spice.wait_until(lambda: media_size_id_radio_button["visible"] == True, timeout = 10.0)
            assert media_size_id_radio_button
            media_size_id_radio_button.mouse_click()

            # scroll to next media size
            self.workflow_common_operations.scroll_to_position_vertical(scroll_bar_step_value, CopyAppWorkflowObjectIds.add_page_prompt_scroll_bar)

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

    def wait_for_copy_status_toast(self, net, configuration, message: str = "Complete", timeout= 60, wait_for_toast_dismiss=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, Starting... -> Scanning... -> Copying... -> Copying complete
        """
        copy_toast_message=""
        toast_status=""
        if message == "Starting":
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
        elif message == 'Scanning':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
        elif message == 'Copying':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopying')
        elif message == 'Complete':
            if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
                copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyingCompleteMessage')
            else:
                copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyComplete')
        elif message == 'Cancel':
            copy_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cCopyCanceledMessage')
        elif message == 'Canceling':
            copy_toast_message= self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cJobStateTypeCanceling')
        elif message == 'SomeSettingsChangedBetweenPages':
            copy_toast_message= self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cNewSettingsScan')
        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                self.spice.wait_for(CopyAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=15.0)
                toast_status = self.spice.query_item(CopyAppWorkflowObjectIds.text_toastInfoText)["text"]
                logging.info("Current Toast message is : %s" % toast_status)
                self.spice.wait_for(CopyAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=15.0)
            except:
                logging.info("Still finding corresponding status.")
            if copy_toast_message in toast_status:
                break
        if copy_toast_message not in toast_status:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)
    
        if wait_for_toast_dismiss:
                start_time = time.time()
                toast_status = ""
                while time.time()-start_time < timeout:
                    try:
                        toast_status = self.spice.wait_for(CopyAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=2)["text"]
                        logging.info(f"Still corresponding status <{toast_status}> dispay in screen")
                    except Exception as err:
                        logging.info("Toast screen already dismiss")
                        break

    def validate_preview_in_preview_panel(self):
        self.goto_preview_panel()
        #Wait for generated thumbnail
        self.spice.scan_settings.wait_for_preview_n(1)

    def click_on_preview_button_in_preview_panel(self):
        self.goto_preview_panel()
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_button)
        self.spice.wait_until(lambda: current_button['enabled'] == True, 10.0)
        preview_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_preview)
        assert preview_button
        self.spice.wait_until(lambda: preview_button['visible'] == True, 10.0)
        preview_button.mouse_click()
    
    def start_copy_after_preview(self):
        # For small screen preview go to secondary panel
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy_mainpanel)
        self.spice.wait_until(lambda: current_button['enabled'] == True, 10.0)
        current_button.mouse_click()

    def click_on_main_action_button_in_detail_panel(self):
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.copy_button)
        self.spice.wait_until(lambda: current_button['enabled'] == True, 10.0)
        current_button.mouse_click()

    # def verify_copy_pages_per_sheet_constrained(self, udw):
        # """
        # Go to pages per sheet option menu and verify that option is cosntrained
        # @return:
        # """
        # self.goto_copy_pages_per_sheet(udw)
        # logging.info("Go to pages per sheet option menu")
        # current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_pagesPerSheet_option_2 + " SpiceText[visible=true]")
        # current_button.mouse_click()
        # menu_item_id = [CopyAppWorkflowObjectIds.row_combo_copySettings_pagesPerSheet, CopyAppWorkflowObjectIds.combo_copySettings_pagesPerSheet]
        # self.workflow_common_operations.goto_item(menu_item_id, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        # 
        # assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)
# 
        # okButton = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        # okButton.mouse_click()
        # time.sleep(3)
        # self.workflow_common_operations.back_or_close_button_press(f"{CopyAppWorkflowObjectIds.view_copySettings_pagesPerSheetpopup} {CopyAppWorkflowObjectIds.button_back}", CopyAppWorkflowObjectIds.view_copySettingsView)


    def verify_copy_content_orientation_constrained(self, net , constrained_message: str = ""):
        """
        Go to content orientation option menu and verify that option is cosntrained
        @return:
        """

        logging.info("Go to content orientation option menu")
        self.homemenu.menu_navigation(self.spice,CopyAppWorkflowObjectIds.view_copySettingsView,
                                    CopyAppWorkflowObjectIds.row_object_copy_orientation,
                                    scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_constraint_message)

        super().verify_constrained_message(net, constrained_message)

        ok_button = self.spice.wait_for(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()

    def wait_for_copy_completion_window_and_click_ok(self, spice, net):
        """
        Wait until the copy job window appears and click on the OK button.
        """
        expected_text = LocalizationHelper.get_string_translation(net, "cCopyCompleteMessage")
        spice.wait_until(lambda: spice.wait_for(CopyAppWorkflowObjectIds.copy_active_job_modal_text_locator)["text"] == expected_text, 120)
        spice.wait_for(CopyAppWorkflowObjectIds.copy_wizard_completion_active_job_modal_ok_button).mouse_click()

    def goto_copy_options_list_from_preview(self):
        '''
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        self.goto_main_panel_from_preview()
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions, timeout = 10)
        assert setting_view
        self.spice.wait_until(lambda: setting_view["enabled"] == True, timeout = 15.0)
        self.spice.wait_until(lambda: setting_view["visible"] == True, timeout = 15.0)

        assert setting_view["enabled"] == True
        assert setting_view["visible"] == True
        setting_view.mouse_click()
        self.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettingsView)
        time.sleep(3) 

    def goto_main_panel_from_preview(self):

        copy_expand_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_collapse_secondarypanel)
        self.spice.wait_until(lambda: copy_expand_button["enabled"] == True, timeout = 15.0)
        copy_expand_button.mouse_click()   
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)    
    
    def verify_locked(self, current_item) -> bool:
        """
        Return True if the item has its 'locked' or 'locked_' property set.
        """
        # prefer "locked", fall back to "locked_"
        if current_item["locked"] == True:
            return True
        else:
            return False
        
    
    def check_sides_property_locked(self, side_mode:str) -> bool:
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to side mode screen.
        UI Flow is setting option->side mode->select side
        '''
        self.goto_sides_option()
        to_select_item = self.sides_options_locked_dict.get(side_mode)
        current_button = self.spice.wait_for(to_select_item)
        locked = self.verify_locked(current_button)
        select_side_option = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_sides_option_2_2_sided)
        select_side_option.mouse_click()
        return locked

    def select_sides_option(self, side_mode):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to side mode screen.
        UI Flow is setting option->side mode->select side
        '''
        to_select_item = self.sides_options_locked_dict.get(side_mode)
        current_button = self.spice.wait_for(to_select_item)
        current_button.mouse_click()
        