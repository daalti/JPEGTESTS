
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM

class FaxAppWorkflowUILOperations(FaxAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.homeoperations = spice.home_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def fax_receive_settings_paper_tray_selection(self, option: str):
        """
        Purpose: Navigates to fax receive setttings screen to select the paper tray.
        Ui Flow: Fax receive settings -> Paper Tray -> Selection
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsPaperTrayScreen)
        paper_tray_id = FaxAppWorkflowObjectIds.paper_tray_dic_enterprise[option]
        self.workflow_common_operations.goto_item(  paper_tray_id, FaxAppWorkflowObjectIds.view_faxReceiveSettingsPaperTrayScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.ringer_volume_scrollbar)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout=9.0)
    
    def fax_dialing_set_send_speed(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        assert self.spice.query_item(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_send_speed, FaxAppWorkflowObjectIds.button_switch_fax_send_speed]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        if speed == "Slow":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_send_speed_slow)
            current_button.mouse_click()
        elif speed == "Medium":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_send_speed_medium)
            current_button.mouse_click()
        elif speed == "Fast":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_send_speed_fast)
            current_button.mouse_click()
        else:
            raise logging.info(f"{speed} is not supported to select")
        #select_option = "#ComboBoxOptions" + speed.lower()
        #current_button = self.spice.wait_for(select_option)
        #current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen) 
    
    def fax_receive_settings_fax_receive_speed_selection(self, speed: str):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen
        Args: speed: should be "Slow" or "Medium" or "Fast"
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_settings_fax_receive_speed_screen)
        if speed == "Slow":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_receive_speed_slow)
            current_button.mouse_click()
        elif speed == "Medium":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_receive_speed_medium)
            current_button.mouse_click()
        elif speed == "Fast":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_dualfax_receive_speed_fast)
            current_button.mouse_click()
        else:
            raise logging.info(f"{speed} is not supported to select")
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        time.sleep(1)
   
    def wait_and_click_on_middle(self, locator: str) -> None:
        """
        Waits for object in clickable state (visible and enabled) and
        it clicks on the middle of the object
        """
        # Validate for object if not exist
        object = self.spice.wait_for(locator)

        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True, 15)
        self.spice.wait_until(lambda: object["visible"] == True, 15)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)
    
    def fax_options_content_type(self, type: str):
        """
        Purpose: Set fax content type based on user input in fax options
        Args: speed: Mixed, Text, Photograph : str
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        menu_item_id = [FaxAppWorkflowObjectIds.row_object_contentType, FaxAppWorkflowObjectIds.combo_box_contentType]
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_contentTypeListScreen, timeout=9.0)
        resolution_option_dict = {           
            "Mixed": FaxAppWorkflowObjectIds.combo_contentTYpe_option_mixed,            
            "Photograph": FaxAppWorkflowObjectIds.combo_contentTYpe_option_photograph,            
            "Text": FaxAppWorkflowObjectIds.combo_contentTYpe_option_text,
            "Undefined": FaxAppWorkflowObjectIds.combo_contentTYpe_option_undefined,
            "Automatic": FaxAppWorkflowObjectIds.combo_contentTYpe_option_automatic,
            "Image": FaxAppWorkflowObjectIds.combo_contentTYpe_option_image
        }        
        item_select = resolution_option_dict.get(type)
        self.workflow_common_operations.goto_item(item_select, FaxAppWorkflowObjectIds.view_contentTypeListScreen, scrollbar_objectname=FaxAppWorkflowObjectIds.combo_box_contentType_scrollbar) 
    
    def fax_dialing_set_line_monitor_volume(self, volume: str):
        """
        Purpose: Set fax line monitor volume based on user input in fax dialing settings
        Args: volume: should be "low" or "medium" or "high" or "off"
        """
        assert self.spice.query_item(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_line_monitor_volume, FaxAppWorkflowObjectIds.button_switch_fax_line_monitor_volume]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        self.spice.wait_for(FaxAppWorkflowObjectIds.line_monitor_combo_list)
        ringer_volume_dict = {
        "Low": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_low,
        "High": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_high,
        "Off": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_off
        }
        menu_item_id = ringer_volume_dict.get(volume)
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.line_monitor_combo_list, scrollbar_objectname = FaxAppWorkflowObjectIds.ringer_volume_scrollbar )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)

    def fax_job_submission_fax_send(self):
        """
        Purpose:  Verifies send button enable status and selects fax send button in fax job submission page
        Args: NA
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSend)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        time.sleep(2)
        assert self.spice.query_item(FaxAppWorkflowObjectIds.button_faxSend, 0)["enabled"] == True
        current_button.mouse_click(10,10)
        time.sleep(2)
   
    def fax_set_dialing_prefix(self, prefix, index_val=0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.spice.basic_common_operations.scroll_to_position_vertical(0.7, scrollbar_objectname="#faxDialingMenuListScrollBar")
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        # to check if alredy has prefix
        try:
            self.spice.query_item(f"{FaxAppWorkflowObjectIds.text_field_dialing_prefix} {FaxAppWorkflowObjectIds.item_in_text_field_dialing_prefix}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        
        time.sleep(1)
        self.enter_numeric_keyboard_values(prefix)
        logging.info("Move the scroll bar.")
        self.workflow_common_operations.scroll_to_position_vertical(0.4, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
    
    def fax_delete_prefix_value(self, index_val):
        """
        Purpose: Delete dial Prefix value
        Args: Index value: Stack 0 or 1
        """
        assert  self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.spice.basic_common_operations.scroll_to_position_vertical(0.7, scrollbar_objectname="#faxDialingMenuListScrollBar")
        already_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        already_field.mouse_click()
        clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK, timeout=5)
        key_ok.mouse_click()
        logging.info("Move the scroll bar to top.")
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        logging.info("Delete succesfully")
        # self.spice.query_item(FaxAppWorkflowObjectIds.text_field_dialing_prefix)["focus"] = 0

    def goto_preview_panel(self):
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View)
        fax_collapse_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_collapse_secondarypanel, timeout=9.0)
        fax_collapse_button.mouse_click()

    def goto_main_panel(self):
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View)
        fax_expand_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_expand_secondarypanel)
        fax_expand_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View)

    def start_preview(self):
        self.spice.wait_for(FaxAppWorkflowObjectIds.preview_panel, timeout=9.0)
        fax_preview_button = self.spice.query_item(FaxAppWorkflowObjectIds.button_preview_large)
        fax_preview_button.mouse_click()

    def verify_preview(self):
        self.spice.wait_for(FaxAppWorkflowObjectIds.fitpage_layout, timeout =15.0)
        self.spice.wait_for(FaxAppWorkflowObjectIds.first_preview_image, timeout =15.0)

    def click_on_inactivity_timeout_prompt_continue_button(self):
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.preview_cancel_job_warning_prompt, timeout=15.0), "Not at Inactivity Timeout Prompt"
        logging.info("At Inactivity Timeout Prompt")
        continue_button = self.spice.wait_for(FaxAppWorkflowObjectIds.preview_cancel_job_warning_prompt_primary_button)
        continue_button.mouse_click()

    def click_on_inactivity_timeout_prompt_cancel_button(self):
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.preview_cancel_job_warning_prompt, timeout=15.0), "Not at Inactivity Timeout Prompt"
        logging.info("At Inactivity Timeout Prompt")
        cancel_button = self.spice.wait_for(FaxAppWorkflowObjectIds.preview_cancel_job_warning_prompt_secondary_button)
        cancel_button.mouse_click()

    def goto_2sided_printing(self):
        """
        Purpose: Navigates from home menu settings to 2-sided printing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> 2-Sided Printing Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        two_sided_printing = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive)
        two_sided_printing.mouse_click()

    def goto_fit_to_page_settings(self):
        """
        Purpose: Navigates from home menu settings to fit to page settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fit to Page Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        opt = FaxAppWorkflowObjectIds.menuSwitch_fitToPage_receive
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_fitToPage_receive
        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        fit_to_page = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_fitToPage_receive)
        fit_to_page.mouse_click()

    def goto_stamped_received_faxes(self):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> ringer volume
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.menuSwitch_stampReceivedFaxes_receive, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        stamp_rec = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_stampReceivedFaxes_receive)
        stamp_rec.mouse_click()

