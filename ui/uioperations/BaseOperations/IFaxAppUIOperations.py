#########################################################################################
# @file     IFaxAppUIOperations.py
# @authors  Vinay Kumar M(vinay.kumar.m@hp.com) Chandrakanth Reddy(chandrakanth.reddy@hp.com)
# @date     26-02-2021
# @brief    Interface for all the Fax UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys
from dunetuf.fax.fax import *


class IFaxAppUIOperations(object):

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app(self):
        """
        Purpose: Navigates to Fax app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Fax app
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_faxsetup_from_notconfigured_screen(self):
        """
        Purpose: Navigates to Basic fax setup screen from fax not configured screen
        Ui Flow: Any screen -> Main menu -> Fax app -> fax not configured screen -> Configure -> Basic Fax Setup
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_homescreen_fax_notconfigured_cancel(self):
        """
        Purpose: Navigates to Home screen from fax not configured screen
        Ui Flow: Any screen -> Main menu -> Fax app -> fax not configured screen -> cancel -> Home
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_disabled_prompt(self):
        """
        Purpose: Navigates to Home screen from fax disabled screen
        Ui Flow: Any screen -> Main menu -> Fax app -> fax disabled screen -> Ok -> Home
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_menu_navigation(self, button_object_id, expected_object_id, select_option: bool = True):
        """
        Purpose: method searches and clicks a specified button on a specified menu under fax settings
        Navigation: NA
        Args:
            button_object_id: Object Id of the button to be pressed
            expected_object_id: Object Id of the screen
            select_option: Select True to click on the element
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Fax Submenus
    def goto_menu_fax_faxsetup(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_fax_faxsetup_Line1(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Line1
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_fax_faxsetup_Line2(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Line2
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_send_settings(self):
        """
        Purpose: Navigates from home menu settings to fax send settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings(self):
        """
        Purpose: Navigates from home menu settings to fax receive settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_send_settings_dialing(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings_faxforward_config(self):
        """
        Purpose: Navigates from home menu settings to fax forward settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Forwarding
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receivesettings_papertray(self):
        """
        Purpose: Navigates from home menu settings to fax receive paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> paper tray
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_faxsetup_headername(self):
        """
        Purpose: Navigates from home menu settings to fax header in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax Header name
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_faxsetup_faxnumber(self):
        """
        Purpose: Navigates from home menu settings to fax number in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_fax_setup(self):
        """
        Purpose: Navigates from home menu fax app to fax setup screen
         Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_navigate_back(self, current_screen, expected_screen):
        """
        Purpose: Navigates one screen back from current screen
        Ui Flow: current screen -> back -> expected screen
        Args: current Screen Id, expected screen Id
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_button_press(self, screen_id, landing_view, timeout_val: int = 10):
        """
        Press back button in specific screen.
        Args:
        screen_id: Screen object id
        timeout_val: Time out for scrolling
        landing_view: Landing screen after pressing back button
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_recipient_screen(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_recipient_screen_with_setup(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Basic Fax Setup -> Fax Recipients screen
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_phone_line_in_use_view(self):
        """
        Go to fax phone line in use screen when hook state is off
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def receive_manual_fax(self,net):
        """
        Perform receive manual fax when hook state is off
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_cancel_button_on_fax_confirmation_screen(self):
        """
        Click cancel button on fax confirmation screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_button_on_atleast_one_recipient_alert_screen(self):  
        """
        Click OK button on Atleast one recipient alert screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_skip_button(self):
        """
        Click skip button in fax app
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_recipient_screen_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_app_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def enter_fax_number_fax_recipient_screen(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_screen(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_without_skip_button(self):
        """
        Purpose: Navigates to Fax app screen 
        Ui Flow: A Fax app ->  fax recipients screen
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_app_fax_setup_phone_line_details(self):
        """
        Purpose: Click Next button on Basic Fax Setup View
        Ui Flow in Main Menu - Fax - Continue - Basic Fax Setup -> Next -> Phoneline details view
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_fax_setup_country_location(self):
        """
        Purpose: Navigates from home screen to Country/Location selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Country/Location Selection view
        Args: None
        """

    def goto_fax_app_fax_setup_dial_type(self):
        """
        Purpose: Navigates from home screen to dial type selection in phoneline screen of fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Next -> Phoneline details view -> dial type
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_fax_options(self):
        """
        Purpose: Navigates to fax options screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_options_fax_settings(self):
        """
        Purpose: Navigates to fax send settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_options_send_settings_fax_dialing(self):
        """
        Purpose: Navigates to fax dialing settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings -> Fax dialing Settings
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # ------------------------------- Function Keywords ----------------------

    def fax_app_enter_fax_number_confirm(self, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number in enter fax number screen and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_set_two_sided_original_value(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Original based on user input
        Args: value: True = 2-Sided Original on, False = 2-Sided Original off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_set_resolution(self, resolution: str):
        """
        Purpose: Selects fax send resolution based on user input in fax options in settings
        Args: resolution: Standard, Fine, Superfine
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_lighter_darker_slider(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_sharpness_slider(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax Sharpness based on user input in fax options in settings
        Args: value: accepts values 1-5: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_contrast_slider(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax Contrast based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_background_cleanup_slider(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax Background cleanup based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_slider_current_value(self, slider_name, value: int = 1):
        """
        Purpose: Get slider values and compare it with specified value
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_job_submission_fax_send(self):
        """
        Purpose: Selects fax send button in fax job submission page
        Args: NA
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_content_type(self, type: str):
        """
        Purpose: Set fax content type based on user input in fax options
        Args: speed: Mixed, Text, Photograph : str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_country(self, country: str = "USA"):
        """
        :param country: USA, UK, Canada and Australia
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_fax_number(self, number):
        """
        Set the value of Fax number based on user input using alphanumeric keyboard
        Args: number: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_header_name(self, name: str):
        """
        Set the value of Fax header name based on user input using alphanumeric keyboard
        Args: name: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_basic_fax_settings_dial_type(self, dial_type: str = "Tone"):
        """
        Purpose: Selects Pulse/Tone dialing type in fax dial settings
        Args: value: Pulse, Tone
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_dialing_prefix(self, prefix):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_settings_set_values(self, options: str, value: bool = False):
        """
        Selects the values of Fax number Confirmation, ErrorCorrectionMode, OverlayFaxHeader and
               Editable Billing Code based on user input
        Args: options: FaxNumberConfirmation, ErrorCorrectionMode, OverlayFaxHeader, EditableBillingCode
        value : True/False : Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_dialing_set_send_speed(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: Slow, Medium, Fast : str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_slider_value(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_settings_dialing_pulse_dialing(self, pulse_dial_type: bool = False):
        """
        Purpose: Enables/Disables Pulse dialing type in fax dialing settings
        Args: value: True = Pulse dialing on, False = Pulse dialing off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_settings_dialing_detect_dialtone(self, pulse_dial_type: bool = False):
        """
        Purpose: Enables/Disables detect  dialing tone in fax dialing settings
        Args: value: True = detect  dialing on, False = detect dialing off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    # ---------Toast/Alerts Validation-------

    def wait_for_fax_job_status_toast(self, message: str = "Success", timeout: int = 10):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: Scanning, Dialing, Faxing, Success... : str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # -------------- Numeric Keyboard ---------------

    def enter_numeric_keyboard_values(self, keyboard_view, fax_number):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # ---------------------- Fax Receive Function cases ----------

    def fax_receive_settings_auto_answer(self, auto_answer: bool = False):
        """
        Purpose: Enables/Disables Auto answer in fax receive settings
        Args: auto_answer: True, False: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_set_ringer_volume(self, value):
        # TODO: @still implementation pending, as volume button object name needs fix
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_receive_settings_set_values(self, options: str, value: bool = False):
        """
        Selects the values of Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes and Fit to Page
        Args: options: Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes, Fit to Page
              value: value : True/False : Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # ---- Fax Forwarding Configuration ----

    def fax_receive_settings_set_fax_forwarding(self, forward, print, fax_number):
        """
        Selects the values of Fax forwarding based on user input like forward, forward+print and fax number
        Args: options: forward, print, fax_number
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # --- Send to Contact ----

    def fax_app_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_send_or_cancel_no_contacts(self, yes_no: str = "No"):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app and enters fax
        number if user selects "Yes" and Cancel fax when user select "No"
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts ->
            If "Yes" Enter fax Num
            If "No" navigated back to fax recipient.
        Args: Yes/No
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_add_remove_recipient(self, add_remove: str):
        """
        Purpose: Navigates from Job Submission screen to fax add/remove recipient in fax app
        Ui Flow: Job Submission -> # of Fax recipients -> Add/Remove
            If "Add" then navigates to Add recipient
            If "Remove" navigated Remove recipient.
        Args: Add/Remove
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_multiple_recipients_using_enter_fax_number(self, fax_number_list):
        """
        Purpose: Enters multiple fax number one after the other and then waits for job submission page
        Args: fax_number_list which is provided on the test case
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_multiple_recipients_send_to_contacts_without_contacts(self, fax_number_list, yes_no: str = "Yes"):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app when 
        there are no contacts created.
        Enters multiple fax number if user selects "Yes" and Cancel fax when user selects "No" 
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts ->
            If "Yes" Enter fax Num
            If "No" navigated back to fax recipient.
        Args: fax_number_list which is provided on the test case and Yes/No
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def create_fax_multiple_contacts(self, cdm, udw, payload_list):
        """
        Purpose: Creates fax contacts (record id's) using the payload list provided on the test case.
        Args: payload_list which is provided on the test case
        Returns: record id list
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_multi_destination_contacts(self, record_id_list):
        """
        Purpose: Selects fax contacts to send to multi destination using addressbook (send to contacts) option 
        Args: record_id_list which is passed on sequentially from create_fax_multiple_contacts keyword.
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def incoming_receive_fax(self, cdm, udw, faxSimIP: str, auto_answer: str="Yes", cancel: str=Cancel.no, waitTime: int=100, stampReceivedFax: str="false", blockedFaxNumber: str="", **payLoad: Dict) -> None:
        """Recieves the fax job

        Args:
            faxSimIP: IP Address of fax simulator
            auto_answer: keep the vaue as "Yes" if the option auto answer is set as On
                         keep the vaue as "No" if the option auto answer is set as Off
            cancel: Possible values are ['no', 'after_init', 'after_start', 'after_create'] 
                    that specifies the post action after starting the fax job.
                    Defaults to 'no'
            waitTime: Timeout in seconds to check for fax job state. Defaults to 60
            stampReceivedFax: Bool indicating received fax is stamped or not. Defaults to false.
        
        Returns:
            None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def receive_fax_trigger(self, cdm, udw, faxSimIP: str, auto_answer: str = "Yes", cancel: str = Cancel.no,
                             waitTime: int = 100,
                             **payLoad: Dict) -> None:
        """Recieves the fax job

        Args:
            faxSimIP: IP Address of fax simulator
            auto_answer: keep the vaue as "Yes" if the option auto answer is set as On
                         keep the vaue as "No" if the option auto answer is set as Off
            cancel: Possible values are ['no', 'after_init', 'after_start', 'after_create']
                    that specifies the post action after starting the fax job.
                    Defaults to 'no'
            waitTime: Timeout in seconds to check for fax job state. Defaults to 60
            
        Returns:
            None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_basic_setup_alert_without_basic_details(self):
        """
        Purpose: Validate the error screen when basic setup details either any Country name,Header name or Fax number
        field empty
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_billingcode_contraint(self,net):
        """
        verify contraint message when billing code is given blank
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def goto_fax_settings_fax_setup_country_location(self):

        """
        Purpose: Navigates from Basic fax setup screen to Country/Location selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Country/Location Selection view
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_recipient_screen_enter_fax_number(self, fax_number):
        """
        Purpose: From fax recipient screen to enter fax number
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: Fax number
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_send_job_submission_from_fax_send_job_options_screen_with_back_button(self):
        """
        Back to send job submission screen from send job options screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_send_job_submission_from_fax_send_job_options_screen_with_close_button(self):
        """
        Back to send job submission screen from send job options screen through close button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_fax_send_settings_from_fax_dialing_screen_with_back_button(self):
        """
        Back to fax send settings screen from fax dialing screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_settings_from_fax_send_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax sending screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_settings_from_fax_settings_screen_with_back_button(self):
        """
        Back to settings screen from fax settings screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def get_max_junk_constraint(self):
        """
        returns the maximum junk block number constraint
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def enter_multiple_fax_number(self, fax_number_list):
        """
        Purpose: Enter Multiple fax number at Fax send to contacts screen
        Args: fax_number_list which is provided on the test case
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_addressbook_local_from_local_select_screen_with_back_button(self):
        """
        Back to Address Book Local screen from local select screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_faxsendtocontacts_from_addressbook_local_screen_with_close_button(self):
        """
        Back to fax send to contacts screen from Address Book Local screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_receive_settings_junk_fax_blocking(self):
        """
        Purpose: Navigates from Fax Receive Settings to Junk Fax Blocking
        Ui Flow: Fax receive Settings -> Junk Fax Blocking
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_receive_settings_with_fax_junk_ok_button(self):
        """
        Purpose: UI should move back to Fax receive settings when click ok button in Junk Fax blocking screen.
        Ui Flow: Junk Fax blocking ->Fax receive settings
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_junk_fax_CallHistory_button(self):
        """
        Purpose: Click Received Call History button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax-> Received Call History 
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_junk_fax_keyboardEntry_button(self):
        """
        Purpose: Click Enter Using Keyboard button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax -> Enter Using Keyboard
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_keyboardEntry_junkfaxblock_cancel_button(self):
        """
        Purpose: Click Enter Using Keyboard button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax->Enter using Keyboard->JunkFax Block screen.Click Cancel 
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_junk_fax_CallHistory_cancel_button(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax->Cancel click. 
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
       
    def click_junk_fax_add_button(self):
        """
        Purpose: Click Add button in Junk Fax blocking screen to input numbers.
        Ui Flow: Junk Fax blocking -> click add button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_blocked_number_add_button(self):
        """
        Purpose: Click Add button in number added existing screen to input numbers.
        Ui Flow: NumberAddedExistingListlist1SpiceListViewView -> click add button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_junk_fax_number_ok_button(self):
        """
        Purpose: Click Ok button in enter junk fax number screen.
        Ui Flow: enter junk fax number screen -> click ok button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_numbers_added_to_junk_list_ok_button(self):
        """
        Purpose: Click Ok button in numbersAddedToJunkList screen.
        Ui Flow: numbersAddedToJunkList screen -> click ok button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_number_already_junk_fax_view(self, net):
        """
        Purpose: Verify 'The number entered is already in the junk fax list' should be displayed
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_already_junk_fax_number_ok_button(self):
        """
        Purpose: Click Ok button in numberAlreadyJunkFaxView screen.
        Ui Flow: numberAlreadyJunkFaxView screen -> click ok button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_junk_fax_number(self, junk_fax_number_list):
        """
        Purpose: Select multiple junk blocking fax numbers one after the other
        Args: junk_fax_number_list which is provided on the test case, e.g.:["0000", "1111", "2222"] or ["123"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_remove_button(self):
        """
        Purpose: Click remove button in number added existing screen to remove numbers which selected.
        Ui Flow: NumberAddedExistingListlist1SpiceListViewView -> click remove button
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_junk_fax_blocking_numbers(self, number_list):
        """
        Purpose: check whether junk fax blocking numbers is reflected in screen.
        Args: number_list: number list needs to be verified, e.g.:["0000", "1111", "2222"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def input_multiple_junk_fax_blocking_numbers(self, junk_fax_number_list):
        """
        Purpose: Enters multiple junk blocking fax number one after the other and then waits for...
        Args: junk_fax_number_list which is provided on the test case, e.g.:["0000", "1111", "2222"] or ["123"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_junk_fax_blocking_number(self, junk_fax_number):
        """
        Purpose: Enters junk blocking fax number. Jut allowed to add only 1 number at a time according to DUNE-89696
        Args: junk_fax_number which is provided on the test case, e.g.:"101"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_home_screen(self):
        """
        Purpose: Navigates to Fax app in home screen
        Ui Flow: Home -> Fax app 
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_home_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_home_fax_app_setup_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_home_enter_fax_number_and_confirm(self, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number in enter fax number screen and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def fax_receive_verify_rings_to_answer(self, value):
        """
        verify the value of rings to answer
        :param value: value of rings to answer
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_options_original_size(self, option: str):
        """
        Select Original Size option from Fax -> Options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_content_orientation(self, orientation_option: str):
        """
        Select Content Orientation option from Fax -> Options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_blank_page_suppression(self, value: str):
        """
        Select Blank Page Suppression option from Fax -> Options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_fax_line_selection(self, size: str):
        """
        Select Fax Line Selection option from Fax -> Options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_line2_notconfigured_constrained(self):
        """
        Click Ok on the fax line2 not configured constrained message
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_dual_line_set_ringer_volume(self, value):
        """
        Purpose: Set ringer volume in fax receive settings
        Args: value: High,Low,Off
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_ringer_volume(self):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> ringer volume
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_rings_to_answer(self,value):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Rings to Answer
        Args: value: 1/2/3/4/5/6
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings_dualline_fax_receive_speed(self):
        """
        Purpose: Navigates from home menu settings to fax receive speed settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Receive Speed -> Dual Line Fax Receive Speed
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_receive_settings_dualline_fax_receive_speed_selection(self, speed: str):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen in dualline
        Args: speed: should be "Slow" or "Medium" or "Fast"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_send_settings_dialing_line2(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing -> Line2
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_settings_set_Line2_errorCorrectionMode(self, value: bool = False):
        '''
        Selects the value of ErrorCorrectionMode
        Args: value: value : True/False : Bool
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_dialing_set_send_speed_line2(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_settings_set_fax_line_selection(self, value: str):
        '''
        Selects the value of ErrorCorrectionMode
        Args: value: str : Auto/Line1/Line2
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_fax_notification(self, value: str):
        """
        Select Fax Notification option from Fax -> Options
        Args: value: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_options_fax_notification_verify_constrained(self, value: str):
        """
        Select Fax Notification option from Fax -> Options and verify the constrained message
        Args: value: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fax_send_settings_fax_notifications_verify_constrained(self, value: str):
        """
        Purpose: Select corresponding option about fax notification in fax send settings and verify the constrained message
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_home_fax_app_setup_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_finish_btn_on_add_page(self):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        Click Finish button on Add Page screen if no more page need scan.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_add_more_btn_on_add_page(self):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        Click Add More button on Add Page screen to scan another page.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_on_add_page_screen(self, net):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        check spec on Add Page Screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_output_tray_closed_is_visible(self):
        """
        Output Tray Closed is shown when generate with UDW command.
        Check the screen is still visible during fax in progress.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_btn_on_output_tray_closed(self):
        """
        Click OK button on Output Tray Closed screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_app_fax_setup_from_basic_fax_setup_with_back_button(self):
        """
        Back to Fax Setup view from Basic Fax Setup view via back button.
        Flow should in Fax App setup -- Basic Fax Setup view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_select_contact_from_search_contact_screen_with_close_button(self):
        """
        Back to select fax contacts screen from Search contact screen through close button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_settings_from_basic_fax_setup_screen_with_back_button(self):
        """
        Back to fax_settings screen from basic_fax_setup screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_home_fax_app_fax_setup_country_location(self):
        """
        UI flow:Home Screen -> Fax App -> Click Continue -> Basic Fax Setup -> Country/Location Selection view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings_fax_receive_speed(self):
        """
        Purpose: Navigates from home menu settings to fax receive speed settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Receive Speed
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_receive_settings_fax_receive_speed_selection(self, speed: str):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen
        Args: speed: should be "slow" or "medium" or "fast"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_send_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Receive Settings to Fax Notifications
        Ui Flow: Fax send Settings -> Fax Notifications
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fax_send_settings_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send settings
        Args:option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fax_send_settings_fax_notifications_include_thumbnail(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send settings and check include thumbnail
        Args:option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fax_receive_settings_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax receive settings
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_receive_settings_view(self, net):
        """
        Check receive settings screen is displayed and verify header text.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_empty_junk_fax_list_view(self, net):
        """
        Check empty junk fax list view is displayed and verify body text.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_fax_settings_from_fax_receive_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax receive settings screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_receive_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Receive Settings to Fax Notifications
        Ui Flow: Fax receive Settings -> Fax Notifications
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_forward_configuration(self):
        """
        Purpose: Navigates from home menu settings to fax forward configuration screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Forward Configuration
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_fax_settings_from_fax_forward_configuration_screen_with_back_button(self):
        """
        Back to fax_settings screen from fax_forward_configuration screen through back button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_reports_list_item(self, net):
        """
        Verify below reports are available.
        Junk Fax Report
        Fax T.30 Trace Report
        Fax Activity Log
        Fax Call Report
        Billing codes report. 
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_reports(self, net, report: str):
        """
        Verify below reports are available.
        Blocked Fax Report
        Fax Trace Report
        Fax Activity Log
        Fax Call Report
        CallerID Report
        Billing codes report
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_settings_fax_dialing_screen(self):
        """
        Purpose: Navigates from fax settings to fax dialing settings screen.
        Ui Flow: Fax Settings -> Fax Send Settings -> Fax Dialing Settings.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_forwarding_configuration_view(self, net):
        """
        Check the fax forwarding configuration view and check the header.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_fax_settings_view(self,net):
        """
        Check fax settings screen is displayed and verify header text.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_setup_view(self,net):
        """"
        Check fax setup screen is displayed and verify header text.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def verify_fax_recipient_view(self,net):
        """
        Check fax recipient screen is displayed and verify header text.
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_receive_fax_junk_fax_number_limit_reached_view_displayed(self):
        """
        To wait for alert displayed when click on add after entering max limited fax number.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_button_on_max_limited_junk_fax_number_screen(self):
        """
        Purpose: Click Ok button in max limited junk fax screen.
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_setup_answering_machine_selection(self, option='Yes', index=8):
        """
        Selects the answering machine option yes or no. Default it is set as Yes.
        Args: options: Yes and No
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_setup_complete_click_ok_button(self):
        """
        Fax setup complete, click on button.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def cancel_fax_setup_wizard_with_click_home_button(self):
        """
        Cancel Fax Setup Wizerd via home button.
        Flow should in Click Home button -- Cancel Setup screen 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_yes_button_on_cancel_setup_screen(self):
        """
        Click Yes button on Cancel Setup screen.
        Flow should in Fax Cancel Setup screen -- Click Yes button 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_set_fax_receive_notification_successfully(self, fax_receive_notification):
        '''
        This is helper method to verify set fax receive notification successfully
        UI should be Menu->Settings->Fax Settings->Fax Receive
        Args: fax_receive_notification: fax receive notification
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_set_fax_send_notification_successfully(self, fax_send_notification):
        '''
        This is helper method to verify set fax send notification successfully
        UI should be Menu->Settings->Fax Settings->Fax Send
        Args: fax_send_notification: fax send notification
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ignore_button_on_incoming_fax(self):
        '''
        Purpose: Click Ignore button on Incoming Fax screen to reject the job.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_accept_button_on_incoming_fax(self):
        '''
        Purpose: Click Accept button on Incoming Fax screen to accept the job.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_set_fax_more_options_successfully(self, net, fax_option, fax_option_item):
        '''
        This is helper method to verify set fax resolution successfully
        UI should be Home->Fax->Fax More Options
        Args: fax_option: Resolution/Content Type
              fax_option_item: "Fine/SuperFine/Standard"/ "Text/Mixed/Photograph
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_ok_btn_on_junk_fax_number_removed(self):
        """
        Click OK button on Junk Fax Number Removed screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_faxsetup_phoneline(self):
        """
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup ->Phone Line Not Connected Screen
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_back_button_press(self):
        """
        Purpose: Press back button to go back the home screen from the fax landing screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_multiple_recipients_send_to_contacts_search_icon(self):
        """
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact -> Serach Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_configured_multiple_recipients_send_to_contacts_search_icon(self):
        """
        Ui Flow: Main Menu -> Fax -> Basic Fax Setup -> Fax Recipients screen -> Sent to Contacts -> local contact -> Serach Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_custom_address_book(self):
        """
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_configured_custom_address_book(self):
        """
        Ui Flow: Main Menu -> Fax -> Fax Setup -> Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_select_custom_address_book(self, custom_address_name):
        """
        Purpose: Navigates from home screen to fax recipient coustom contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook
        Args:custom_address_name: user created custom address book name
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def input_pin_code_for_custom_addressbook(self, pincode):
        """
        Purpose: input pincode for custom addressbook if pincode is set for custom addressbook.
        UI should be in: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook
        Args:pincode: 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_invalid_pin_code_view_and_click_ok_button(self, net):
        """
        Purpose: check invalid pin code view and click ok button 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_submit_button_input_pin_code_view(self):
        """
        Purpose: click submit button when input pin code for custom addressbook
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_contact_search_modal_button(self):
        """
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact/Custom Contact -> Serach Icon -> Serach Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_address_contact_search_and_reset(self):
        """
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact/Custom Contact -> Serach Icon -> Enter Contact->Serach Icon -> Reset
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings_fax_printing_select(self):
        """
        Ui Flow: Main Menu -> Settings -> Fax Setting -> Fax receive setting -> fax printing -> select options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_receive_settings_fax_printing(self):
        """
        Ui Flow: Main Menu -> Settings -> Fax Setting -> Fax receive setting -> fax printing
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_multiple_contacts_from_custom_addressbook(self):
        """
        Ui Flow: Main -> Fax -> Skip -> Contact -> Custom Addressbook
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def input_junk_block_number(self,junk_fax_number_list):
        """
        Purpose: Enters  junk blocking fax number
        Args: junk_fax_number_list which is provided on the test case, e.g.:["123"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def enter_fax_number_alphanumeric(self, fax_number_list):
        """
        Purpose: Enter  fax number at Fax junk blocking using alphanumeric keyboard
        Args: fax_number_list which is provided on the test case
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    
    def enter_fax_number(self, fax_number_list):
        """
        Purpose: Enter  fax number at Fax junk blocking
        Args: fax_number_list which is provided on the test case
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_fax_call_history_addressbook(self):
        """
        Goto fax call history addressbook
        Ui should in fax landing view, UI flow is click Sent to Contacts button -> select Call History
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_multi_fax_contacts_from_call_history(self, fax_contacts_list):
        """
        Selects fax contacts in contacts intergration view
        Ui should in contacts intergration view (Fax -> Skip -> Fax Recipients screen -> click Sent to Contacts button -> select a address book)
        Args: fax_contacts_list
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_multi_callhistory_for_junkfaxblock(self, expected_fax_record_list):
        """
        Check Received call history shows in Blocked Fax screen under Received Call history.
        @param: expected_fax_record_list:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_multi_callhistory_for_junkfaxblock(self, expected_fax_record_list):
        """
        Check specific received call history in Blocked Fax screen under Received Call history.
        @param: expected_fax_record_list:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_fax_call_history_display_in_contacts_list_view(self, expected_fax_record_list):
        """
        Check fax call history record shows in call history contact list view screen.
        @param: expected_fax_record_list:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_spec_no_contacts_in_list(self, net):
        '''
        Check spec no contacts in list when no contacts in contacts list
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, scroll_bar, footer_item_id=None, scroll_height=66):
        """
        Scroll contact/group into center of sceen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items. One more thing, there are 2 screen to show 100 contacts
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                scroll_bar: object name scroll bar 
                footer_item_id: object name for footer view, keep it as None if it does not inculded in scroll view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_clear_activitylogs(self):
        """
        Goto troubleshooting fax and clear fax logs
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_cancel_button_in_select_contacts_view(self):
        """
        Click cancel button in select contacts view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_schedule_cancel_button(self):
        """
        Click on Cancel button in Schedule fax Screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def send_later_enter_numeric_keyboard_values(self):
        """
        Enter Fax number
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_schedule_later_done_button(self):
        """
        Press Done button after setting fax schedule time
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_now_hr_set(self,value):
        """
       Set Hours value in fax schedule screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_send_now_min_set(self,value):
        """
       Set Minits value in fax schedule screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_app_fax_options_schedule_now(self):
        """
        Press Schedule Now in Fax option screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_incoming_fax_alert_visible(self, timeout=9.0):
        '''
        Purpose: check incoming fax alert display or not.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_ldap_address_book(self):
        """
        Purpose: Navigates from home screen to fax recipient ldap contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> ldap addressbook
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_search_button_on_fax_contact_screen(self):
        """
        Click Search button under fax contact screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_search_button_on_fax_contact_search_screen(self):
        """
        Click Search button on fax contact search screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def search_contact_from_contact_address_book(self, search_text):
        """
        Search contact from address book
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_multiple_contacts_from_search_result(self, display_name_list):
        """
        Select multiple contacts from ldap search result
        @param display_name_list: ["display_name1, display_name2"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_select_on_search_result_screen(self):
        """
        Click Select button on search result screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_multiple_contacts_from_ldap_address_book(self, display_name_list, search_text):
        """
        Select multiple contacts from ldap search result
        @param display_name_list: ["display_name1, display_name2"]
        @param search_text: "display_name"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_set_include_cover_page(self, enable_status=True):
        """
        Enable/Disable option include cover page
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_app_verify_include_cover_page_constrained(self):
        """
        Verify include cover page is constrained
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_send_setting_toggle_option_value(self, options: str, value:bool):
        """
        verify the values of fax send settings, UI should be in Menu -> Settings -> Fax Settings -> Fax Send Settings screen.
        Args: options: scanAndFaxMethod, scanAndFaxMethod, errorCorrectionMode, overlayFaxHeader, editableBillingCode
              value: True/False : Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_now_min_value(self):
        """
        Purpose: get schedual now min value
        Ui Flow: fax job Submission screen -> Fax Options->Send Now
        :return: min_value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_now_hr_value(self):
        """
        Purpose: get schedual now hr value
        Ui Flow: fax job Submission screen -> Fax Options->Send Now
        :return: hr_value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_app_click_billing_code_cancel_button(self):
        """
        Purpose: Click cancel button on editable billing code screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_fax_send_settings_dialing_detect_dial_tone_status(self):
        """
        Purpose: get detect dial tone status in fax dialing settings
        @return: dial_tone_state, True = detect dialing on, False = detect dialing off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_dialing_prefix_unavailable(self, net):
        """
        Purpose: Check dialing prefix is unavailable under dialing prefix text
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_receive_get_paper_tray_value(self):
        """
        Purpose:get the paper tray text in fax receive setttings screen.
        @return: ui_setting_string
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_fax_color_option(self):
        """
        Get fax color option
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_fax_color_option(self, color_option, net):
        """
        Set fax color option
        @param color_option grayscale/color
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_cancel_button_on_colorfax_alert_screen(self):
        """
        Click cancel button on Color Fax Alert Screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_button_on_colorfax_alert_screen(self):
        """
        Click ok button on Color Fax Alert Screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def colorfax_alert_ecm_screen_displayed(self, net):
        """
        Color Fax alert ECM screen is displayed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def colorfax_not_supported_screen_displayed(self, net):
        """
        Color Fax not supported screen is displayed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_button_on_color_fax_not_supported_screen(self):
        """
        Click ok button on color fax not supported screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_send_on_colorfax_alert_screen(self):
        """
        Click send button on color fax not supported screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def colorfax_alert_turn_off_scan_and_fax_method_screen_displayed(self, net):
        """
        colorfax alert turn off scan and fax method screen is displayed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_two_sided_original_value_in_landing_view(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Original based on user input in fax landing view
        Args: value: True = 2-Sided Original on, False = 2-Sided Original off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_multiple_reports_print(self, option_list: list):
        """
        Purpose: Navigates to fax report options and prints multiple reports
        Ui Flow: Fax reports -> report options
        @param: option_list: multiple reports want to report, such as: ["Fax trace report", "Fax activity log", "Fax Call Report"]
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_fax_color_option_in_landing_view(self):
        """
        Get fax color option in fax landing view
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_fax_color_option_in_landing_view(self, color_option, net):
        """
        Set fax color option in fax landing view
        @param color_option grayscale/color
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_home_fax_app_and_sign_in(self, authAgent:str, password:str, username = None):
        """
        Purpose: Navigates to Fax app screen from home screen and sign in on Fax app screen.
        Ui Flow: Home -> Fax app -> -> Sign In -> Basic fax setup ->Skip-> fax recipients screen
        :param spice: Takes 0 arguments
        authAgent: The auth agent selected for sign in (OPTIONS: "user", "customUser", "admin", "windows", "ldap")
        password: Sign in password
        username: Sign in username
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def colorfax_alert_scheduled_fax_not_support_color_screen_displayed(self, net):
        """
        colorfax alert scheduled fax not support color screen is displayed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_send_button_on_scheduled_fax_not_support_color_screen(self):
        """
        Click send button on Color Fax Alert scheduled fax not support color Screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_printer_user_screen_for_locked_fax_app_from_menu(self):
        """
	    UI should be on menu screen before calling this method
        Navigate to fax
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_printer_user_screen_for_locked_fax_app_from_home(self):
        """
	    UI should be on home screen before calling this method
        Navigate to fax
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
		
    def has_lock_icon_home(self):
        """
		Check Fax lock icon exist on home screen
		"""
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_fax_locked_view_screen_for_printer_user_from_home(self):
        """
	    UI should be on home screen before calling this method
        Navigate to home screen with printer user and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up
        """		
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
		
    def click_ok_btn_on_fax_locked_view_screen(self):
        """
        Navigate to home screen and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up.
        Click OK button on Locked View screen return to previous screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
		
    def click_cancel_btn_on_printer_user_screen(self):
        """
        Navigate to home screen and disable fax permissions from EWS > Security > Access Control, printer user screen pop up.
        Click Cancel button on Printer User screen return to previous screen.
        """		
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_fax_locked_view_screen_for_printer_user_from_menu(self):
        """
	    UI should be on menu screen before calling this method
        Navigate to menu screen with printer user and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up
        """	
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_search_result_number_in_fax_contacts_list_view(self, expected_result_number):
        """
        Check Search Result numbers shows in contacts list view screen.
        @param:expected_result_number, should be int type 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_contacts_display_name_in_fax_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list: the contacts list should be sorted
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_restricted_alert_string(self, net):
        """
        Purpose: Check restricted alert text.
        Should on the restricted alert screen with ok button
        Args: net
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_store_fax_from_job_storage_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Menu -> Print app -> Job Storage ->Stored Fax
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_store_fax_by_fax_number(self, fax_number, dunestorejob):
        """
        Function to select store fax by fax number
        Ui should be on Stored Faxes screen
        Ui Flow: Select the stored fax job
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_distinctivering_record_verifycallmachine(self):
        """
        verify callmachine screen while recording distinctive ring screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_cancel_distinctivering_record(self):
        """
        cancel distinctive record while callmachine is in progress
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def overwrite_record_distinctiver_ring(self):
        """
        proceeds with overwrite distinctive ring record
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def overwrite_record_distinctive_ringcancel(self):
        """
        cancel record distinctive ring while overwrite
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_distinctivering_verifycallmachinetimeout(self,callmachinetimeoutoption):
        """
        verify timeoutscreen when callmachine failed
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_print_button_on_store_fax_screen(self):
        """
        Function to click print button on Stored Faxes screen
        Ui should be on Stored Faxes screen
        Ui Flow: Click print button
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_delete_button_on_store_fax_screen(self):
        """
        Function to click delete button on Stored Faxes screen
        Ui should be on Stored Faxes screen
        Ui Flow: Click delete button
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_goto_custom_address_book_from_recipient_screen(self):
        """
        Purpose: Navigates from fax recipient to coustom contacts selection screen in fax app and press search Icon
        Ui Flow: Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_contacts_not_present_in_local_address_book(self, payload_list):
        """
        Purpose: Check contacts not present in local address book
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_recipient_screen_remove_existing_contact_enter_fax_number(self, fax_number):
        """
        Purpose: Remove existing contact and enter fax number
        Args: fax_number
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scan_Auto_Detection_Prompt_Select_Media_Size_continue(self, fax_number):
        """
        Select media size in Auto Detection Prompt, press continue button
        Args: value: Media size value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scan_Auto_Detection_Prompt_Select_Media_Size_cancel(self, fax_number):
        """
        Select media size in Auto Detection Prompt, press cancel button and confirm the cancel prompt
        Args: value: Media size value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scan_Auto_Detection_Prompt_Select_Media_Size_cancel_dismiss(self, fax_number):
        """
        Select media size in Auto Detection Prompt, press cancel, No from the cancel prompt
        Args: value: Media size value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_ok_button_on_invalid_or_missing_entries_in_blocked_fax_alert_screen(self):
        """
        Click OK button on invalid or missing entries in blocked fax alert screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_schedule_later_reset_button(self):
        """
        Click Reset button after setting fax schedule time
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_fax_setup_change_country(self):
        """
        Purpose: Navigates from Basic fax setup screen to Country/Location selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Country/Location Selection view
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_setup_select_country(self, country: str = None, fax_mode=FaxModemType.dungeness_bbu_modem.value):
        """
        :param spice: None
        :param country: Indonesia= "ID", Hong Kong S.A.R.="HK", South Korea="KR", Malaysia="MY",Philippines:"PH",Singapore ="SG"
        Sri Lanka = "LK", Thailand="TH", Vietnam ="VN"
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_location_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_faxnumber_headername_previous_button_click(self):
        """
        Purpose:Wait for until Previous button object present
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_setup_add_header_name(self, name: str):
        """
        Set the value of Fax header name based on user input using alphanumeric keyboard
        Args: name: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_setup_add_fax_number(self, number):
        """
        Set the value of Fax number based on user input using alphanumeric keyboard
        Args: number: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_faxnumber_headername_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_constraint_message_faxnumber_headername_not_configured(self):
        """
        Purpose:Verify constraint message when fax number and header name not configured
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_dialing_prefix_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_finish_button(self):
        """
        Purpose:Wait for until finish button object present
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax_faxsetup_enterprise(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_setup_add_dialing_prefix(self, prefix, index_val=0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_cancel_confirmation_from_location(self):
        """
        Purpose:Click on the Cancel button from location and verify cancel confirmation dialog
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_setup_summary(self,expect_text):
        """
        Purpose:Verify values in summary screen
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_fax_options_original_sides_value(self):
        '''
        Get the original sides value
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_fax_options_orininal_sides_non_default_value(self, net):
        '''
        According to current original sides value, set to another value.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def close_fax_options(self):
        '''
        Click close button of Fax Options page
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_fax_receive_settings_auto_answer_status(self, check_status):
        """
        Purpose: check fax receive settings auto answer status
        Args: check_status: True, False: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_send_later_schedule_now(self, net):
        """
        Purpose: navigate to fax options>send later>schedule now
        Args: timeout,minutes
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def fax_send_later_schedule_now_without_faxsetup(self, net):
        """
        Purpose: navigate to fax without faxsetup>options>send later>schedule now
        Args: timeout,minutes
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def fax_dual_fax_set_slider_value(self, slider_name, value: int = 1,line: str = "line1"):
        """
        Purpose: Set slider values based on user input in fax options in settings
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup, Redial On Error, Redial On No Answer, Redial On Busy, Redial Interval
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def fax_send_dualfax_settings_dialing_detect_dialtone(self, detect_dial_tone: bool = False,line: str = "line1"):
        """
        Purpose: Enables/Disables detect dial tone in fax dialing settings
        Args: value: True = detect dialing on, False = detect dialing off: Bool
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
