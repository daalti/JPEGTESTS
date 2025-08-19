
import logging
import time

from dunetuf.fax.fax import *
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.WorkflowUICommonXSOperations import WorkflowUICommonXSOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM

class FaxAppWorkflowUIXSOperations(FaxAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = WorkflowUICommonXSOperations(self.spice)
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    def goto_fax_app_home_screen(self):
        """
        Purpose: Navigates to Fax app in home screen
        Ui Flow: Home -> Fax app 
        :return: None
        """
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.4)
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()
        time.sleep(3)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)


    def goto_fax_receive_settings_junk_fax_blocking(self):
            """
            Purpose: Navigates from Fax Receive Settings to Junk Fax Blocking
            Ui Flow: Fax receive Settings -> Junk Fax Blocking
            Args: None
            """
            self.workflow_common_operations.goto_item_for_vertical_menu(FaxAppWorkflowObjectIds.fax_junk_fax_blocking_settings, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings, scrolling_value=0.05)

    def fax_set_slider_value(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        slide_bar = ""
        slide_bar_row = ""
        screen_name = ""
        scrollbar = ""
        slider_min = 0
        slider_max = 0
        if slider_name == "Lighter Darker":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_lighterDarker
            slide_bar = FaxAppWorkflowObjectIds.slider_lighterDarker
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 9
        elif slider_name == "Redial On Error":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnError
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnError
            screen_name = FaxAppWorkflowObjectIds.view_faxDialingScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxDialing
            slider_min = 0
            slider_max = 9
        elif slider_name == "Redial on No Answer":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnNoAnswer
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnNoAnswer
            screen_name = FaxAppWorkflowObjectIds.view_faxDialingScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxDialing
            slider_min = 0
            slider_max = 2
        elif slider_name == "Redial On Busy":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnBusy
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnBusy
            screen_name = FaxAppWorkflowObjectIds.view_faxDialingScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxDialing
            slider_min = 0
            slider_max = 9
        elif slider_name == "Redial Interval":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialInterval
            slide_bar = FaxAppWorkflowObjectIds.slider_redialInterval
            screen_name =  FaxAppWorkflowObjectIds.view_faxDialingScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxDialing
            slider_min = 1
            slider_max = 5

        menu_item_id = [slide_bar_row, slide_bar] 
        self.workflow_common_operations.goto_item_for_vertical_menu(menu_item_id[0], screen_name, scrollbar_objectname = scrollbar, scrolling_value=0.05, select_option=False)
        current_button = self.spice.query_item(f"{screen_name} {slide_bar_row} {slide_bar}")
        current_button.mouse_click()
        time.sleep(3)
        logging.info("At Expected Menu")

        assert slider_min <= value <= slider_max, 'Value is out of range'
        slider_bar = self.spice.query_item(slide_bar)
        slider_bar.__setitem__('value', value)
        new_value = self.spice.query_item(slide_bar)["value"]        
        logging.info("Current Slider value is : %s" % new_value)

    def fax_dialing_set_send_speed(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        assert self.spice.query_item(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_send_speed, FaxAppWorkflowObjectIds.button_switch_fax_send_speed]
        self.workflow_common_operations.goto_item_for_vertical_menu(menu_id[0], FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing, scrolling_value=0.05, select_option=False)
        select_speed = self.spice.query_item(f"{FaxAppWorkflowObjectIds.view_faxDialingScreen} {FaxAppWorkflowObjectIds.row_switch_fax_send_speed} {FaxAppWorkflowObjectIds.button_switch_fax_send_speed}")
        select_speed.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_send_speed_option)
        
        select_option = "#ComboBoxOptions" + speed.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
    
    def goto_menu_fax_receivesettings_papertray(self):
        """
        Purpose: Navigates from home menu settings to fax receive paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> paper tray
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.goto_item_for_vertical_menu(FaxAppWorkflowObjectIds.row_object_paper_tray, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings, scrolling_value=0.05, select_option=False)
        tray_item = self.spice.query_item(f"{FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen} {FaxAppWorkflowObjectIds.row_object_paper_tray} {FaxAppWorkflowObjectIds.combo_box_paper_tray}")
        tray_item.mouse_click()
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsPaperTrayScreen)
        self.spice.wait_until(lambda:current_screen["visible"])
        logging.info("At Expected Menu")
        time.sleep(3)
        
    def fax_set_ringer_volume(self, value):
        """
        Purpose: Set ringer volume in fax receive settings
        Args: volue: High,Low,Off
        """
        menu_id = [FaxAppWorkflowObjectIds.row_object_ringer_volume, FaxAppWorkflowObjectIds.combo_box_ringer_volume]
        self.workflow_common_operations.goto_item_for_vertical_menu(menu_id[0], FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                                    FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings, 
                                                                    scrolling_value=0.05, select_option=False)
        select_ring_volume = self.spice.query_item(f"{FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen}\
                                                     {FaxAppWorkflowObjectIds.row_object_ringer_volume}\
                                                     {FaxAppWorkflowObjectIds.combo_box_ringer_volume}")
        select_ring_volume.mouse_click()
        
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettings_ringer_volume_Screen)
        select_option = "#ComboBoxOptions" + value.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout=9.0)

    def goto_home_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_home_screen()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        #self.workflow_common_operations.goto_item_for_vertical_menu(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen, scrollbar_objectname=FaxAppWorkflowObjectIds.progress_panel_vertical_layout_scrollbar, scrolling_value=0.05)
        time.sleep(5)
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click()
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)

    def fax_receieve_set_distinctive_ring(self, distinctive_ring: str = None):
        """
        :param spice: None
        :param distinctive_ring: Single Ring, Double Rings, Triple Rings, Double and Triple Rings,Use Recorded Ring,All Standard Rings,
        Ring Pattern Detection.
        :return:
        """
        
        curren_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctiveRingScreen)
        self.spice.wait_until(lambda:curren_view["visible"])
        logging.info("At fax receieve set distinctive ring screen")       
        distinctive_ring_option_dict = {            
            "Single Ring": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_single_ring,            
            "Double Rings": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_double_ring,            
            "Triple Rings": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_triple_ring,
            "Double and Triple Rings": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_double_and_triple_ring,
            "Use Recorded Ring": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_use_recorded_ring,
            "All Standard Rings": FaxAppWorkflowObjectIds.distinctive_ring_menu_item_all_standard_rings,
            "Record Ring Pattern":FaxAppWorkflowObjectIds.distinctive_ring_menu_item_start_record
        }        
        menu_item_id = distinctive_ring_option_dict.get(distinctive_ring)  
        if distinctive_ring in ["All Standard Rings", "Double and Triple Rings", "Triple Rings"]:
            self.workflow_common_operations.scroll_to_position_vertical(0.5, FaxAppWorkflowObjectIds.distinctive_ring_menu_list_scrollbar)
        time.sleep(5)     
        current_button = self.spice.query_item(menu_item_id)
        self.spice.wait_until(lambda:current_button["visible"])  
        logging.info(f"Select <{distinctive_ring}> and click the section to save the option")  
        current_button.mouse_click()
        time.sleep(1)


    def goto_menu_fax_receive_settings_fax_receive_speed(self):
        """
        Purpose: Navigates from home menu settings to fax receive speed settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Receive Speed
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        menu_id = [FaxAppWorkflowObjectIds.row_object_fax_receive_speed, FaxAppWorkflowObjectIds.combo_box_fax_receive_speed]
        self.workflow_common_operations.goto_item_for_vertical_menu(menu_id[0], FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                                    FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings, 
                                                                    scrolling_value=0.05)
        fax_receive_speed = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_fax_receive_speed)
        fax_receive_speed.mouse_click()
        fax_receive_settings_fax_receive_speed_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_settings_fax_receive_speed_screen)
        self.spice.wait_until(lambda:fax_receive_settings_fax_receive_speed_view["visible"])

    def cancel_fax_setup_wizard_with_click_home_button(self):
            """
            Cancel Fax Setup Wizerd via home button for XS size screen machine.
            For XS size screen machine, there is no HOME button on UI screen. hence use command to go home. 
            Flow should in Click Home button -- Cancel Setup screen 
            """
            logging.info("Cancel Fax Setup Wizerd via home button")
            self.spice.goto_homescreen()
            cancel_setup_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_cancel_setup_screen)
            self.spice.wait_until(lambda:cancel_setup_view["visible"])
            logging.info("At Cancel Setup screen")

    def back_button_press(self, screen_id, landing_view, timeout_val: int = 10):
        """
        Press back button for XS screen by sending command via udw.
        Args:
        screen_id: Screen object id
        timeout_val: Time out for scrolling
        landing_view: Landing screen after pressing back button
        """
        self.spice.wait_for(screen_id)
        # For XS size machine, back button is not in the UI. Should press back button by sending command via udw.
        self.spice.common_operations.click_back_button()
        self.spice.wait_for(landing_view ,3)
        logging.info("At" +landing_view)

    def back_to_fax_settings_from_fax_forward_configuration_screen_with_back_button(self):
        """
        Back to fax_settings screen from fax_forward_configuration screen through back button.
        """
        logging.info("Go back to fax_settings screen from fax_forward_configuration screen with back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings)
        fax_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_menu_fax_settings)
        self.spice.wait_until(lambda:fax_settings_view["visible"])
        logging.info("At Fax Settings screen")
    
    def back_to_fax_settings_from_fax_send_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax sending screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.fax_send_menu_list, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings)
    
    def back_to_fax_send_settings_from_fax_dialing_screen_with_back_button(self):
        """
        Back to fax send settings screen from fax dialing screen through back button.
        """
        logging.info("Go back to fax send settings screen from fax dialing screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.fax_dialing_menu_list, landing_view = FaxAppWorkflowObjectIds.fax_send_menu_list)

    def back_to_fax_settings_from_basic_fax_setup_screen_with_back_button(self):
        """
        Back to fax_settings screen from basic_fax_setup screen through back button.
        """
        logging.info("Go back to fax_settings screen from basic_fax_setup screen with back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen, landing_view = FaxAppWorkflowObjectIds.view_faxSettingsScreen)

    def back_to_addressbook_local_from_local_select_screen_with_back_button(self):
        """
        Back to Address Book Local screen from local select screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen, landing_view = FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
    
    def back_to_faxsendtocontacts_from_addressbook_local_screen_with_close_button(self):
        """
        Back to fax send to contacts screen from Address Book Local screen through close button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through close button.")
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        close_button = self.spice.wait_for(f'{FaxAppWorkflowObjectIds.view_FaxAddressBookScreen} {FaxAppWorkflowObjectIds.button_back_close_addressBook}')
        if close_button["visible"] == True:
            close_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen ,3)
            logging.info("At" + FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def goto_fax_send_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Send Settings to Fax Notifications for XS size screen
        Ui Flow: Fax send Settings -> Fax Notifications
        Args: None
        """
        self.workflow_common_operations.scroll_to_position_vertical(position=0.6, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])

    def back_to_fax_send_job_submission_from_fax_send_job_options_screen_with_close_button(self):
        """
        Purpose: Navigates from Fax Send Settings to Fax Notifications for XS size screen
        Ui Flow: Fax send Settings -> Fax Notifications
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        close_button = self.spice.wait_for(f'{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.button_back_close}')
        if close_button["visible"] == True:
            close_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen ,3)
            logging.info("At" + FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def back_to_fax_settings_from_fax_receive_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax receive settings screen through back button.
        """
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_menu_fax_settings ,3)

    def goto_fax_receive_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Receive Settings to Fax Notifications for XS size screen
        Ui Flow: Fax receive Settings -> Fax Notifications
        Args: None
        """
        self.workflow_common_operations.scroll_to_position_vertical(position=0.6, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_fax_notifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_recieve_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])        
