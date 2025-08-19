#########################################################################################
# @file     FaxAppProSelectUIOperations.py
# @authors Vinay Kumar M(vinay.kumar.m@hp.com) Chandrakanth Reddy(chandrakanth.reddy@hp.com)
# @date     10-03-2021
# @brief    Implementation for all the Fax UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
import requests
import unicodedata
from dunetuf.fax.fax import *
from dunetuf.ui.uioperations.BaseOperations.IFaxAppUIOperations import IFaxAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectKeyboardOperations import ProSelectKeyboardOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper


class FaxAppProSelectUIOperations(IFaxAppUIOperations):
    fax_setup_menu_button = "#faxSetupMenuButton"
    fax_send_menu_button = "#faxSendMenuButton"
    fax_receive_menu_button = "#faxReceiveMenuButton"
    fax_dialing_menu_button = "#faxDialingMenuButton"
    fax_forwarding_menu_button = "#faxForwardingMenuButton"
    fax_receive_tray_button = "#paperTrayMenuButton"
    menu_item_faxid = "#44aa632b-cfa3-4c10-8cab-697a9bef610b"
    basic_fax_setup_fax_header_name_button = "#basicFaxSetupFaxHeaderNameButton"
    enter_fax_header_name_view = "#enterFaxHeaderName"
    basic_fax_setup_faxnumber_button = "#basicFaxSetupFaxNumberButton"
    keyboard_view = "#spiceKeyboardView"

    # Fax App
    Fax_app_setup_home_view = "#faxSetupHomeView"
    fax_setup_skip_button = "#FaxSetupSkipButton"
    fax_setup_continue_button = "#FaxSetupContinueButton"
    basic_fax_setup = "#basicFaxSetup"
    fax_send_recipients_view = "#FaxSendRecipientsView"
    fax_send_to_contacts = "#FaxSendToContacts"
    fax_enter_fax_number = "#FaxEnterFaxNumber"
    FaxSendNoContactsAvailable = "#FaxSendNoContactsAvailable"
    FaxNoListAvailableYesButton = "#FaxNoListAvailableYesButton"
    FaxNoListAvailableNoButton = "#FaxNoListAvailableNoButton"
    fax_number_keyboard = "#faxNumberKeyboard"
    basic_fax_setup_next_button = "#basicFaxSetupNextButton"
    fax_phone_line_details = "#FaxPhoneLineDetails"
    phone_line_details_next_button = "#phoneLineDetailsNextButton"
    basic_fax_setup_country_location_button = "#basicFaxSetupCountryLocationButton"
    fax_select_country_view = "#FaxCountryRegionView"
    dial_type_button = "#dialTypeButton"
    fax_select_dial_type_view = "#faxSelectDialTypeView"
    fax_dial_type_tone_button = "#faxDialTypeToneButton"
    fax_dial_type_pulse_button = "#faxDialTypePulseButton"
    fax_send_job_submission = "#FaxSendJobSubmission"
    back_button = "#BackButton"
    fax_options_button = "#FaxOptionsButton"
    fax_send_options = "#FaxSendOptions"
    fax_send_button = "#FaxSendButton"

    faxcheck_Basic_Fax_setup_View = "#FaxCheckBasicFaxSetupView"
    faxcheck_alert_ok_button = "#OK"
    FaxSetUP_line_share = "#faxSetupLineShare"
    FaxSetup_line_share_YesButton = "#FaxSetUpLineShareYesButton"
    FaxSetup_line_share_NoButton = "#FaxSetUpLineShareNoButton"
    phone_line_Details_NextButton = "#phoneLineDetailsNextButton"
    fax_setup_voice_calls = "#faxSetupVoiceCalls"
    fax_setup_voice_calls_YesButton = "#FaxSetUpVoiceCallsYesButton"
    fax_setup_voice_calls_NoButton = "#FaxSetUpVoiceCallsNoButton"
    fax_setup_distinctive_ring_for_fax = "#faxSetupDistinctiveRingForFax"
    fax_set_up_distinctive_ring_for_fax_yes_button = "#FaxSetUpDistinctiveRingForFaxYesButton"
    fax_set_up_distinctive_ring_for_fax_no_button = "#FaxSetUpDistinctiveRingForFaxNoButton"
    fax_check_basic_fax_setup_view = "#FaxCheckBasicFaxSetupView"
    distinctive_ring_all_standard_rings = "#DistinctiveRingAllStandardRings"
    next = "#Next"
    admin_app_application_stack_view = "#AdminAppApplicationStackView"
    ok_button = "#okButton"

    # -----Add Recipients-----
    fax_add_recipients_button = "#FaxAddRecipientsButton"
    number_of_fax_recipients_button = "#FaxNumberOfRecipientsButton"
    list_of_fax_recipients_view = "#FaxSendRecipientsView"
    add_recipients_button = "#FaxAddRecipients"
    recipient = "#FaxRecipient{8419da52-f886-45cd-9054-ea4d3c6abc15}"

    # -----Remove Recipients-------
    fax_remove_recipient_view = "#faxSendRemoveRecipientView"
    remove_recipient_button = "#FaxSendRecipentsRemoveButton"
    # recipient1 = "#FaxRecipient{8419da52-f886-45cd-9054-ea4d3c6abc15}"
    recipient1 = "#FaxRecipient{13bee3b8-888a-4f52-be2b-65c8773fca29}"
    recipient2 = "#FaxRecipient{a1e37040-f0b4-4934-8c45-a0049ee2c978}"

    # -----Send to Contacts----
    fax_send_to_contacts_screen = "#faxSendToContactsView"
    fax_send_no_contacts_available_view = "#FaxSendNoContactsAvailable"
    fax_no_list_available_yes_button = "#FaxNoListAvailableYesButton"
    fax_no_list_available_no_button = "#FaxNoListAvailableNoButton"
    faxSendToContactsView = "#faxSendToContactsView"
    FaxAddressBookButton = "#FaxAddressBookButton"
    FaxSendToContactDoneButton = "#FaxSendToContactDoneButton"
    # contact1 = "#FaxSendToContactd6d58822-ad7e-4675-9993-af44d652b4bc"  # checked/unchecked
    contact1 = "#FaxSendToContact5ab33747-5d83-45b1-8f04-a29008416983"
    contact2 = "#FaxSendToContact741f5387-f531-4014-8874-e873d34ce1c1"

    # ------ConfirmFaxNumberScreen----
    # confirm_fax_number_view = "#ConfirmFaxNumberView"
    confirm_fax_number_view = "#faxNumberKeyboard"
    # fax_confirm_button = "#FaxConfirmButton"
    fax_confirm_button = "#FaxConfirmButton"
    fax_cancel_button = "#FaxCancelButton"
    version2_text = "#Version2Text"  # Fax Number Confirm Text

    fax_send_two_sided_switch_button = "#FaxSendTowSidedSwitchButton"
    two_sided_original_spice_switch = "#SpiceSwitch"  # property to check - checked(bool) / position(bool)
    fax_resolution_button = "#resolutionButton"
    fax_resolution_spice_text = "#ContentItemText"
    fax_send_resolution_view = "#faxSendResolutionView"
    superfine_button = "#superfineButton"  # Property to check - checked(bool)
    fine_button = "#fineButton"  # Propert to check - checked(bool)
    standard_button = "#standardButton"  # Property to check - checked(bool)

    # ----- Content type Selection ----
    content_type_button = "#contentTypeButton"
    fax_send_content_type_view = "#faxSendContentTypeView"
    mixed_button = "#mixedButton"
    text_button = "#textButton"
    photograph_button = "#glossy"


    lighter_darker_slider_value = "#SliderValue"  # property to use text and input 1-9
    SCAN_LIGHTER_DARKER_MIN = 1
    SCAN_LIGHTER_DARKER_MAX = 9

    lighter_darker_spice_slider = "#FaxSendLighterDarkerSlider"
    LighterDarkerSpiceSlider = "#LighterDarkerSpiceSlider"
    redial_on_error_slider = "#redialOnErrorMenuSlider"
    redial_on_no_answer_slider = "#redialOnNoAnswerMenuSlider"
    redial_on_busy_menu_slider = "#redialOnBusyMenuSlider"
    redial_interval_slider = "#redialIntervalMenuSlider"
    rings_to_answer_slider = "#ringsToAnswerMenuSlider"
    recieve_settings_rings_to_answer_slider = "#RingsToAnswerSlider"

    # ------FaxApplication Send Setting--------#
    fax_app_options_fax_settings_button = "#FaxSettingsButton"
    fax_send_setting_screen = "#NavigationList"
    fax_number_confirmation_menu_switch = "#faxNumberConfirmationMenuSwitch"  # Property to check - checked(bool)
    fax_dialing_menu_button = "#faxDialingMenuButton"
    error_correction_mode_menu_switch = "#errorCorrectionModeMenuSwitch"  # Property to check - checked(bool)
    overlay_fax_header_menu_switch = "#overlayFaxHeaderMenuSwitch"
    # editable_billing_code_menu_switch = "#editableBillingCodeMenuSwitch"
    editable_billing_code_menu_switch = "#billingCodeMenuSwitch"

    # -----Fax Dialling Screen-----
    fax_dialing_screen = "#NavigationList"
    fax_send_speed_menu_name_value = "#faxSendSpeedMenuButton"
    dialing_speed_medium = "#option_medium"
    dialing_speed_slow = "#option_slow"
    dialing_speed_fast = "#option_fast"
    pulse_dialing_mode_menu_switch = "#pulseDialingModeMenuSwitch"
    dialing_prefix_menu_name_value = "#dialingPrefixMenuNameValue"

    # ----faxSendSpeedScreen---
    fax_send_speed_screen = "#MenuSelectionListfaxSendSpeed"
    fax_speed_slow_radio = "#option_slow"
    fax_speed_medium_radio = "#option_medium"
    fax_speed_fast_radio = "#option_fast"

    # -----------Slider values index -------------------
    lighter_darker_slider_val = {"cur": 0, "min": 1, "max": 2}
    redial_on_error_slider_val = {"cur": 3, "min": 4, "max": 5}
    redial_on_no_answer_slider_val = {"cur": 6, "min": 7, "max": 8}
    redial_on_busy_slider_val = {"cur": 9, "min": 10, "max": 11}
    redial_internal_Slider_val = {"cur": 12, "min": 13, "max": 14}

    # ------------ Auto Answer- Fax Receive Settings ----------
    auto_answer_menu_switch = "#autoAnswerMenuSwitch"
    rings_to_answer = "#ringsToAnswerMenuSlider"  # Id need to be added
    ringer_volume_menu_name_value = "#ringerVolumeMenuButton"


    # -----RING VOLUME -------
    menu_selection_list_ringer_volume = "#MenuSelectionListringerVolume"
    ring_volume_high = "#option_high"
    ring_volume_low = "#option_low"
    ring_volume_off = "#option_off"

    #------Distinctive Ring-----
    menu_selection_list_Distinctive_ring = "#faxSetupDistinctiveRingTypeView"
    distinctive_ring_button = "#distinctiveRingMenuButton"

    # ---- Fax Receive Settings ---
    fax_receive_setting_screen = "#MenuListfaxReceive"
    error_correction_menu_switch = "#errorCorrectionMenuSwitch"
    two_sided_printing_menu_switch = "#twoSidedPrintingMenuSwitch"
    stamp_received_faxes_menu_switch = "#stampReceivedFaxesMenuSwitch"
    automatic_reduction_menu_switch = "#automaticReductionMenuSwitch"
    incoming_fax_receive_page = "#faxReceiveState"
    incoming_fax_accept_button = "#AcceptReceiveFax"

    # ---- Fax Forwarding Configuration ----
    fax_forwarding_view = "#MenuListfaxForwarding"
    forward_enabled_menu_switch = "#forwardEnabledMenuSwitch"
    forward_print_enabled_menu_switch = "#forwardPrintEnabledMenuSwitch"
    forward_number_menu_name_value = "#forwardNumberMenuButton"

    fax_forward_number_button = "#[[]]"

    # ---- Fax Country Selection -----
    USA = "#FaxUSARadioButton"
    UK = "#FaxUKRadioButton"
    Canada = "#FaxCanadaRadiobutton"
    Australia = "#FaxAustraliaRadioButton"
    basicFaxSetupCountryLocationButton = "#basicFaxSetupCountryLocationButton"

    # ---- Paper Tray Selection -----
    menu_selection_list_paper_tray = "#MenuSelectionListpaperTray"
    option_tray_1 = "#option_tray_1"
    option_tray_2 = "#option_tray_2"
    option_tray_3 = "#option_tray_3"
    option_automatic = "#option_automatic"

    #------ Tools selection ------
    tools_menu_report_button = "#reportFaxMenuButton"
    tools_menu_print_button = "#printMenuButton"
    fax_activity_log = "#eb9f7652-7021-11eb-9439-0242ac130002"
    fax_trace_report = "#9f6e723c-78fe-477f-a01b-b84adad7f653"
    junk_fax_report = "#969936d0-6e12-45c5-952d-9782882c592a"
    checkbox_button_list_layout = "#CheckboxButtonListLayout"

    def __init__(self, spice):
        self.maxtimeout = 20
        self.spice = spice
        self.homemenu = MenuAppProSelectUIOperations(self.spice)
        self.dial_common_operations = ProSelectCommonOperations(self.spice)
        self.dial_keyboard_operations = ProSelectKeyboardOperations(self.spice)

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        homeApp = self.spice.query_item("#HomeScreenView")
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)
        logging.info("At Home Screen")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the Menu option (TODO - Need to avoid use of text)
        while (self.spice.query_item("#CurrentAppText")[
                   "text"] != "Menu" and timeSpentWaiting < self.maxtimeout):
            homeApp.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

    def goto_fax_app(self):
        """
        Purpose: Navigates to Fax app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Fax app -> Basic fax setup -> fax recipients screen
        :param spice: Takes 0 arguments
        :return: None
        """
        self.goto_mainmenu()
        # move to the Fax app
        startTime = time.time()
        timeSpentWaiting = 0
        current_screen = self.spice.wait_for("#HomeScreenView")
        while (self.spice.query_item("#CurrentAppText")[
                   "text"] != "Fax" and timeSpentWaiting < self.maxtimeout):
            current_screen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(1)
        assert self.spice.query_item("#CurrentAppText")["text"] == "Fax"
        time.sleep(5)
        currentApp = self.spice.wait_for(self.menu_item_faxid)
        currentApp.mouse_click()
        self.spice.wait_for(self.Fax_app_setup_home_view)

    def fax_menu_navigation(self, button_object_id, expected_object_id, select_option: bool = True):
        """
        Purpose: method searches and clicks a specified button on a specified menu under fax settings
        Navigation: NA
        Args:
            button_object_id: Object Id of the button to be pressed
            expected_object_id: Object Id of the screen
            select_option: Select True to click on the element
        """
        time.sleep(1)
        current_screen = self.spice.wait_for(button_object_id)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        time.sleep(1)
        current_button = self.spice.query_item(self.back_button + " SpiceText")
        time.sleep(1)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        while self.spice.query_item(button_object_id)["activeFocus"] == False and timeSpentWaiting < self.maxtimeout:
            current_screen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(0.5)
        time.sleep(1)
        assert self.spice.query_item(button_object_id)["activeFocus"] == True
        time.sleep(5)
        if select_option:
            current_button = self.spice.wait_for(button_object_id + " SpiceText")
            current_button.mouse_click()
            time.sleep(2)
            self.spice.wait_for(expected_object_id)
            logging.info("At Expected Menu")
        time.sleep(1)

    # Menu Fax Submenus
    def goto_menu_fax_faxsetup(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.fax_setup_menu_button)

    def goto_menu_fax_send_settings(self):
        """
        Purpose: Navigates from home menu settings to fax send settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.fax_send_menu_button)

    def goto_menu_fax_receive_settings(self):
        """
        Purpose: Navigates from home menu settings to fax receive settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.fax_receive_menu_button)

    def goto_menu_fax_send_settings_dialing(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.fax_dialing_menu_button)

    def goto_menu_fax_receive_settings_distinctive_ring(self):
        """
        Purpose: Navigates from home menu settings to Distinctive Ring
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> distinctive Ring
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.fax_menu_navigation(self.distinctive_ring_button, self.menu_selection_list_Distinctive_ring)

    def goto_fax_receive_settings_distinctive_ring(self):
        """
        Purpose: Navigates from home fax Receive settings to Distinctive Ring
        Ui Flow: Fax receive Settings -> distinctive Ring
        Args: None
        """
        self.fax_menu_navigation(self.distinctive_ring_button, self.menu_selection_list_Distinctive_ring)

    def goto_menu_fax_receive_settings_faxforward_config(self):
        """
        Purpose: Navigates from home menu settings to fax forward settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Forwarding
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.fax_menu_navigation(self.fax_forwarding_menu_button, self.fax_forwarding_view)

    def goto_menu_fax_receivesettings_papertray(self):
        """
        Purpose: Navigates from home menu settings to fax receive paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> paper tray
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        time.sleep(2)
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.fax_receive_tray_button)

    def goto_menu_fax_faxsetup_headername(self):
        """
        Purpose: Navigates from home menu settings to fax header in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax Header name
        Args: None
        """
        self.goto_menu_fax_faxsetup()
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.basic_fax_setup_fax_header_name_button)
        self.spice.wait_for(self.enter_fax_header_name_view)

    def goto_menu_fax_faxsetup_faxnumber(self):
        """
        Purpose: Navigates from home menu settings to fax number in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax number
        Args: None
        """
        self.goto_menu_fax_faxsetup()
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.basic_fax_setup_faxnumber_button)
        self.spice.wait_for(self.fax_number_keyboard)

    def goto_fax_app_fax_setup(self):
        """
        Purpose: Navigates from home menu fax app to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax Header name
        Args: None
        """
        self.goto_fax_app()
        self.fax_menu_navigation(self.fax_setup_continue_button, self.basic_fax_setup, True)

    def fax_app_navigate_back(self, current_screen, expected_screen):
        """
        Purpose: Navigates one screen back from current screen
        Ui Flow: current screen -> back -> expected screen
        Args: current Screen Id, expected screen Id
        """
        cur_screen = self.spice.wait_for(current_screen)
        for i in range(10):
            cur_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_button = self.spice.wait_for(self.back_button)
        current_button.mouse_click()
        time.sleep(1)
        self.spice.wait_for(expected_screen)

    def back_button_press(self, screen_id, landing_view, timeout_val: int = 10):
        """
        Press back button in specific screen.
        Args:
        screen_id: Screen object id
        timeout_val: Time out for scrolling
        landing_view: Landing screen after pressing back button
        """
        current_screen = self.spice.wait_for(screen_id)
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        while (self.spice.query_item("#BackButton")["activeFocus"] == False and timeSpentWaiting < timeout_val):
            current_screen.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
        time.sleep(1)
        current_button = self.spice.query_item(self.back_button + " SpiceText")

        current_button.mouse_click()
        time.sleep(1)
        assert self.spice.wait_for(landing_view)
        time.sleep(1)

    def goto_fax_app_recipient_screen(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen
        Args: None
        """
        self.goto_fax_app()
        # if "#faxSetupHomeView"
        self.fax_menu_navigation(self.fax_setup_skip_button, self.fax_send_recipients_view)

    def goto_fax_app_recipient_screen_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        Args: None
        """
        self.goto_faxApp_recepientScreen()
        self.fax_menu_navigation(self.FaxSendToContacts, self.faxSendToContactsView)
        current_screen = self.spice.wait_for(self.faxSendToContactsView)
        while (self.spice.query_item(self.contact1 + " SpiceText")["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
        assert self.spice.query_item(self.contact1 + " SpiceText")["activeFocus"] == True
        time.sleep(1)
        state = self.spice.query_item(self.contact1)["checked"]
        logging.info("state : %s" % state)
        current_button = self.spice.wait_for(self.contact1)
        if not state:
            current_button.mouse_click()
            assert not self.spice.query_item(self.contact1)["checked"], "Contact is not checked"
        done_button = self.spice.query_item(self.FaxSendToContactDoneButton + " SpiceText")["activeFocus"]
        while (self.spice.query_item(self.FaxSendToContactDoneButton + " SpiceText")["activeFocus"] == False):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        done_button.mouse_click()
        current_screen = self.spice.wait_for(self.FaxSendJobSubmission)

    def goto_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_recipient_screen()
        self.fax_menu_navigation(self.fax_enter_fax_number, self.fax_number_keyboard)

    def goto_fax_app_fax_setup_phone_line_details(self):
        """
        Purpose: Navigates from home screen to phoneline selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Next -> Phoneline details view
        Args: None
        """
        self.goto_fax_app_fax_setup()
        self.fax_menu_navigation(self.basic_fax_setup_next_button, self.fax_phone_line_details, True)

    def goto_fax_app_fax_setup_country_location(self):
        """
        Purpose: Navigates from home screen to Country/Location selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Country/Location Selection view
        Args: None
        """
        self.goto_fax_app_fax_setup()
        self.fax_menu_navigation(self.basic_fax_setup_country_location_button, self.fax_select_country_view)

    def goto_fax_app_fax_setup_dial_type(self):
        """
        Purpose: Navigates from home screen to dial type selection in phoneline screen of fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Next -> Phoneline details view -> dial type
        Args: None
        """
        self.goto_fax_app_fax_setup_phone_line_details()
        self.fax_menu_navigation(self.dial_type_button, self.fax_select_dial_type_view, True)

    def goto_fax_app_fax_options(self):
        """
        Purpose: Navigates to fax options screen from job submission page
        Ui Flow: fax job Submission screen -> Fax Options
        Args: None
        """
        current_screen = self.spice.wait_for(self.fax_options_button)
        while (self.spice.query_item(self.fax_options_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(1)
        assert self.spice.query_item(self.fax_options_button)["activeFocus"] == True
        current_button = self.spice.wait_for(self.fax_options_button)
        current_button.mouse_click()
        self.spice.wait_for(self.fax_send_options)

    def goto_fax_options_fax_settings(self):
        """
        Purpose: Navigates to fax send settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings
        Args: None
        """
        # current_screen = self.spice.wait_for(self.fax_send_options)
        current_screen = self.spice.wait_for(self.fax_app_options_fax_settings_button)
        while (self.spice.query_item(self.fax_app_options_fax_settings_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.fax_app_options_fax_settings_button)["activeFocus"] == True
        current_button = self.spice.wait_for(self.fax_app_options_fax_settings_button)
        current_button.mouse_click()
        self.spice.wait_for(self.fax_send_setting_screen)
        logging.info("Navigated to Send Settings Screen")

    def goto_fax_options_send_settings_fax_dialing(self):
        """
        Purpose: Navigates to fax dialing settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings -> Fax dialing Settings
        Args: None
        """
        self.goto_fax_options_fax_settings()
        self.fax_menu_navigation(self.fax_dialing_menu_button, self.fax_dialing_screen)

    # ------------------------------- Function Keywords -----------------------

    def fax_app_enter_fax_number_confirm(self, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number in enter fax number screen and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        args = sys.argv[sys.argv.index('faxNumber') + 1]
        # For single send, todo: Tests for multiple send scenario
        fax_number = parse_fax_arguments(args)[0]
        self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_numeric_keyboard_values(fax_number, self.fax_number_keyboard)
        time.sleep(5)
        if confirm_fax_number:
            current_screen = self.spice.wait_for(self.confirm_fax_number_view)
            time.sleep(1)
            # assert self.spice.query_item(self.version2_text + " SpiceText")["text"] == faxnumber
            while (self.spice.query_item(self.fax_confirm_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(1)
            assert self.spice.query_item(self.fax_confirm_button)["activeFocus"] == True
            current_button = self.spice.wait_for(self.fax_confirm_button)
            current_button.mouse_click()
        time.sleep(10)
        self.spice.wait_for(self.fax_send_job_submission)

    def fax_app_set_two_sided_original_value(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Original based on user input
        Args: value: True = 2-Sided Original on, False = 2-Sided Original off: Bool
        """
        current_screen = self.spice.wait_for(self.fax_send_two_sided_switch_button)
        #        while (self.spice.query_item(current_screen + " SpiceText")["text"] != "2-Sided Original"):
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(self.fax_send_two_sided_switch_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.fax_send_two_sided_switch_button)["activeFocus"] == True
        var = self.spice.query_item(self.fax_send_two_sided_switch_button)["checked"]
        logging.info(var)
        current_button = self.spice.wait_for(self.fax_send_two_sided_switch_button)
        if (value == True):
            if (var == False):
                current_button.mouse_click()
                logging.info(
                    "TwoSidedOriginal value is : %s" % self.spice.query_item(self.fax_send_two_sided_switch_button)[
                        "checked"])
            else:
                logging.info("TwoSidedOriginal value is : %s" % var)
        else:
            if (var == True):
                # current_screen.mouse_click()
                current_button.mouse_click()
                logging.info(
                    "TwoSidedOriginal value is : %s" % self.spice.query_item(self.fax_send_two_sided_switch_button)[
                        "checked"])
            else:
                logging.info("TwoSidedOriginal value is : %s" % var)

    def fax_options_set_resolution(self, resolution: str):
        """
        Purpose: Selects fax send resolution based on user input in fax options in settings
        Args: resolution: Standard, Fine, Superfine
        """
        current_screen = self.spice.wait_for(self.fax_resolution_button)
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)

        while (self.spice.query_item(self.fax_resolution_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(1)
        assert self.spice.query_item(self.fax_resolution_button)["activeFocus"] == True
        time.sleep(2)
        current_button = self.spice.wait_for(self.fax_resolution_button)
        current_button.mouse_click()
        current_screen = self.spice.wait_for(self.fax_send_resolution_view)
        time.sleep(4)
        if (resolution == "Standard"):
            while (self.spice.query_item(self.standard_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
            time.sleep(1)
            assert self.spice.query_item(self.standard_button)["activeFocus"] == True
            current_button = self.spice.wait_for(self.standard_button)
            current_button.mouse_click()
            time.sleep(2)
            actual_resolution = self.spice.query_item(self.fax_resolution_button + " SpiceText")["text"]
            logging.info("The Resolution is set to : %s" % actual_resolution)
            assert actual_resolution == resolution, "Resolution is not as expected"

        elif (resolution == "Fine"):
            while (self.spice.query_item(self.fine_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
            time.sleep(1)
            assert self.spice.query_item(self.fine_button)["activeFocus"] == True
            current_button = self.spice.wait_for(self.fine_button)
            current_button.mouse_click()
            time.sleep(2)
            actual_resolution = self.spice.query_item(self.fax_resolution_button + " SpiceText")["text"]
            logging.info("The Resolution is set to : %s" % actual_resolution)
            # assert actual_resolution == resolution, "Resolution is not as expected"

        elif (resolution == "Superfine"):
            while (self.spice.query_item(self.superfine_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
            time.sleep(1)
            assert self.spice.query_item(self.superfine_button)["activeFocus"] == True
            current_button = self.spice.wait_for(self.superfine_button)
            current_button.mouse_click()
            time.sleep(2)
            actual_resolution = self.spice.query_item(self.fax_resolution_button + " SpiceText")["text"]
            logging.info("The Resolution is set to : %s" % actual_resolution)
            # assert actual_resolution == resolution, "Resolution is not as expected"
        else:
            raise ValueError('Value not found')

    def fax_options_lighter_darker_slider(self, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        current_screen = self.spice.wait_for(self.lighter_darker_spice_slider)
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)

        while (self.spice.query_item(self.lighter_darker_spice_slider)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(1)
        assert self.spice.query_item(self.lighter_darker_spice_slider)["activeFocus"] == True
        time.sleep(2)
        # self.set_sliderValue(self.lighter_darker_spice_slider, value)
        self.fax_set_slider_value("Lighter Darker", value)
        logging.info(self.spice.query_item(self.lighter_darker_slider_value + " SpiceText")["text"])

    # ----- Content type Selection ----
    def fax_options_content_type(self, type: str):
        """
        Purpose: Set fax content type based on user input in fax options
        Args: speed: Mixed, Text, Photograph : str
        """
        if type == "Mixed":
            content_type = self.mixed_button
        elif type == "Text":
            content_type = self.text_button
        elif type == "Photograph":
            content_type = self.photograph_button
        # current_screen = self.spice.wait_for(self.content_type_button)
        # for i in range(10):
        #     current_screen.mouse_wheel(0, 0)
        #     time.sleep(0.5)
        # while (self.spice.query_item(self.content_type_button)["activeFocus"] == False):
        #     current_screen.mouse_wheel(180, 180)
        # time.sleep(0.5)
        # assert self.spice.query_item(self.content_type_button)["activeFocus"] == True
        # current_type = self.spice.query_item(self.content_type_button+" SpiceText")
        # current_type.mouse_click()
        self.fax_menu_navigation(self.content_type_button, self.fax_send_content_type_view)

        current_screen = self.spice.wait_for(self.fax_send_content_type_view)
        while (self.spice.query_item(content_type)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(content_type)["activeFocus"] == True
        time.sleep(1)
        currentRadio = self.spice.query_item(content_type+" SpiceText")
        currentRadio.mouse_click()
        self.spice.wait_for(self.fax_send_options)

    def fax_job_submission_fax_send(self):
        """
        Purpose: Selects fax send button in fax job submission page
        Args: NA
        """
        current_screen = self.spice.wait_for(self.fax_send_button)
        while (self.spice.query_item(self.fax_send_button)["activeFocus"] == False):
            current_screen.mouse_wheel(0, 0)
        while (self.spice.query_item(self.fax_send_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(1)
        current_button = self.spice.wait_for(self.fax_send_button + " SpiceText")
        assert self.spice.query_item(self.fax_send_button)["activeFocus"] == True, " Send Button is not Focused "
        current_button.mouse_click()

    def fax_send_settings_set_values(self, options: str, value: bool = False):
        '''
        Selects the values of FaxnumberConfirmation, ErrorCorrectionMode, OverlayFaxHeader and EditableBillingCode based on user input
        Args: options: FaxNumberConfirmation, ErrorCorrectionMode, OverlayFaxHeader, EditableBillingCode
              value: value : True/False : Bool
        '''
        opt = ""
        if options == "faxNumberConfirmation":
            opt = self.fax_number_confirmation_menu_switch
        elif options == "errorCorrectionMode":
            opt = self.error_correction_mode_menu_switch
        elif options == "overlayFaxHeader":
            opt = self.overlay_fax_header_menu_switch
        elif options == "editableBillingCode":
            opt = self.editable_billing_code_menu_switch

        current_screen = self.spice.wait_for(self.fax_send_setting_screen)
        #        while (self.spice.query_item(current_screen + " SpiceText")["text"] != "2-Sided Original"):
        for i in range(6):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(opt)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(opt)["activeFocus"] == True
        var = self.spice.query_item(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt)
        if (value == True):
            if (var == False):
                current_option.mouse_click()

                logging.info(options+" value is : %s" % self.spice.query_item(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info(options+" value is : %s" % self.spice.query_item(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)

    def fax_set_country(self, country: str = None):
        """
        :param spice: None
        :param country: Indonesia= "ID", Hong Kong S.A.R.="HK", South Korea="KR", Malaysia="MY",Philippines:"PH",Singapore ="SG"
        Sri Lanka = "LK", Thailand="TH", Vietnam ="VN"
        :return:
        """
        #self.goto_fax_app_fax_setup_countryLocation()
        #country_id = "#Fax" + country + "Radiobutton"
        country_name = ""
        if country == "ID":
            country_name = "Indonesia"
        elif country == "HK":
            country_name = "Hong Kong S.A.R."
        elif country == "KR":
            country_name = "South Korea"
        elif country == "MY":
            country_name = "Malaysia"
        elif country == "PH":
            country_name = "Philippines"
        elif country == "SG":
            country_name = "Singapore"
        elif country == "LK":
            country_name = "Sri Lanka"
        elif country == "TH":
            country_name = "Thailand"
        elif country == "VN":
            country_name = "Vietnam"
        else:
            raise logging.info(f"Trying to select country name:{country} is not supported to set,"
                               f"Choose proper country name")

        country_id = "#option_" + country
        current_screen = self.spice.wait_for(self.fax_select_country_view)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_button = self.spice.query_item(self.back_button + " SpiceText")
        while (self.spice.query_item(country_id)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(country_id)["activeFocus"] == True
        assert self.spice.query_item(country_id + " SpiceText")["text"] == str(country_name)
        time.sleep(1)
        logging.info(self.spice.query_item(country_id + " SpiceText")["text"])
        current_country = self.spice.wait_for(country_id)
        #self.spice.click()  # mouse_click() not working
        current_country.mouse_click()
        time.sleep(1)
        self.spice.wait_for(self.basic_fax_setup)

    def fax_set_header_name(self, name: str):
        """
        Set the value of Fax header name based on user input using alphanumeric keyboard
        Args: name: str
        """
        self.fax_menu_navigation(self.basic_fax_setup_fax_header_name_button, self.enter_fax_header_name_view, True)
        self.dial_keyboard_operations.keyboard_enter_text(name)
        self.spice.wait_for(self.basic_fax_setup)

    def fax_set_fax_number(self, number):
        """
        Set the value of Fax number based on user input using alphanumeric keyboard
        Args: number: str
        """
        self.spice.wait_for(self.basic_fax_setup)
        self.fax_menu_navigation(self.basic_fax_setup_faxnumber_button, self.keyboard_view, True)
        self.dial_keyboard_operations.keyboard_clear_text()
        self.enter_numeric_keyboard_values(number)
        self.spice.wait_for(self.basic_fax_setup)

    def fax_basic_fax_settings_dial_type(self, dial_type: str = "Tone"):
        """
        Purpose: Selects Pulse/Tone dialing type in fax dial settings
        Args: value: Pulse, Tone
        """
        dial_type_button = "#faxDialType"+dial_type+"Button"
        self.fax_menu_navigation(self.dial_type_button, self.fax_select_dial_type_view)
        current_screen = self.spice.wait_for(self.fax_select_dial_type_view)
        while (self.spice.query_item(dial_type_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(dial_type_button)["activeFocus"] == True
        assert self.spice.query_item(dial_type_button + " SpiceText")["text"] == str(dial_type)
        time.sleep(1)
        current_dial_type = self.spice.query_item(dial_type_button+" SpiceText")
        current_dial_type.mouse_click()
        self.spice.wait_for(self.fax_phone_line_details)
        self.fax_menu_navigation(self.phone_line_Details_NextButton, self.FaxSetup_line_share_NoButton, True)
        current_screen2 = self.spice.wait_for(self.FaxSetUP_line_share)
        for i in range(2):
            current_screen2.mouse_wheel(180, 180)
            time.sleep(0.5)
        current_button = self.spice.wait_for(self.FaxSetup_line_share_NoButton)
        current_button.mouse_click()
        time.sleep(3)


    def fax_dialing_set_send_speed(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: Slow, Medium, Fast : str
        """
        faxSpeed = ""
        faxSpeedRadio = ""
        if speed == "Slow":
            faxSpeedValue = self.dialing_speed_slow
            faxSpeedRadio = self.fax_speed_slow_radio
        elif speed == "Medium":
            faxSpeedValue = self.dialing_speed_medium
            faxSpeedRadio = self.fax_speed_medium_radio
        elif speed == "Fast":
            faxSpeed = self.dialing_speed_fast
            faxSpeedRadio = self.fax_speed_fast_radio
        current_screen = self.spice.wait_for(self.fax_dialing_screen)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        while (self.spice.query_item(self.fax_send_speed_menu_name_value)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(self.fax_send_speed_menu_name_value)["activeFocus"] == True
        currentSpeed = self.spice.wait_for(self.fax_send_speed_menu_name_value)
        currentSpeed.mouse_click()
        time.sleep(5)
        current_screen = self.spice.wait_for(self.fax_send_speed_screen)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_screen.mouse_wheel(0, 0)
        while (self.spice.query_item(faxSpeedRadio)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(faxSpeedRadio)["activeFocus"] == True
        time.sleep(1)
        currentRadio = self.spice.wait_for(faxSpeedRadio)
        currentRadio.mouse_click()
        time.sleep(5)
        self.spice.wait_for(self.fax_dialing_screen)
        # assert self.spice.query_item(self.faxSpeedValue)["activeFocus"] == True
        # ---Validation pending as the object name with space is not accepted.

    def fax_set_dialing_prefix(self, prefix, index_val =0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        self.fax_menu_navigation("#dialingPrefixMenuButton", self.keyboard_view)
        # self.fax_menu_navigation("#[[]]", self.keyboard_view)
        # self.enter_numeric_keyboard_values(prefix, self.keyboard_view)
        self.dial_keyboard_operations.keyboard_clear_text(index_val)
        self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(prefix, index_val)

    def fax_set_slider_value(self, slider_name, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        slide_bar = ""
        slider_min = 0
        slider_max = 0
        if slider_name == "Lighter Darker":
            slide_bar = self.lighter_darker_spice_slider
            slider_min = 1
            slider_max = 9
        elif slider_name == "Redial On Error":
            slide_bar = self.redial_on_error_slider
            slider_min = 0
            slider_max = 9
        elif slider_name == "Redial on No Answer":
            slide_bar = self.redial_on_no_answer_slider
            slider_min = 0
            slider_max = 2
        elif slider_name == "Redial On Busy":
            slide_bar = self.redial_on_busy_menu_slider
            slider_min = 0
            slider_max = 9
        elif slider_name == "Redial Interval":
            slide_bar = self.redial_interval_slider
            slider_min = 1
            slider_max = 5
        elif slider_name == "Number Of Rings":
            slide_bar = self.rings_to_answer_slider
            slider_min = 1
            slider_max = 6
        elif slider_name == "Phone line details Number Of Rings":
            slide_bar = self.recieve_settings_rings_to_answer_slider
            slider_min = 1
            slider_max = 6
            

        current_screen = self.spice.wait_for(slide_bar)
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)

        while (self.spice.query_item(slide_bar)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(1)
        assert self.spice.query_item(slide_bar)["activeFocus"] == True
        time.sleep(2)

        current_value = self.spice.query_item(slide_bar + " SpiceText")["text"]
        logging.info(slider_name + " value is %s" + current_value)
        assert value >= slider_min and value <= slider_max, "Given Slider value does not match"
        if (value != int(current_value)):
            if (value > int(current_value)):
                dial_value = 180
            else:
                dial_value = 0
        current_button = self.spice.query_item(slide_bar + " SpiceText")
        while (int(current_value) != int(value)):
            current_button.mouse_click(button=self.spice.MOUSE_BTN.MIDDLE)
            time.sleep(1)
            current_button.mouse_wheel(dial_value, dial_value)
            time.sleep(1)
            current_value = self.spice.query_item(slide_bar + " SpiceText")["text"]
            logging.info("current slider value is: %s" % current_value)
            current_button.mouse_click(button=self.spice.MOUSE_BTN.MIDDLE)
        time.sleep(1)
        logging.info("Current lighter_darker value is " + current_value)
        assert int(current_value) == value, "Lighter/Darker setting is not successful"

        logging.info(self.spice.query_item(slide_bar + " SpiceText")["text"])

    def fax_send_settings_dialing_pulse_dialing(self, pulse_dial_type: bool = False):
        """
        Purpose: Enables/Disables Pulse dialing type in fax dialing settings
        Args: value: True = Pulse dialing on, False = Pulse dialing off: Bool
        """
        current_screen = self.spice.wait_for(self.fax_dialing_screen)
        #        while (self.spice.query_item(current_screen + " SpiceText")["text"] != "2-Sided Original"):
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(self.pulse_dialing_mode_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.pulse_dialing_mode_menu_switch)["activeFocus"] == True
        state = self.spice.query_item(self.pulse_dialing_mode_menu_switch)["checked"]
        current_button = self.spice.wait_for(self.pulse_dialing_mode_menu_switch + " SpiceText")
        time.sleep(0.5)
        if (pulse_dial_type):
            if (state == False):
                current_button.mouse_click()
                time.sleep(0.5)
                logging.info(
                    "Pulse Dial type value is : %s" % self.spice.query_item(self.pulse_dialing_mode_menu_switch)["checked"])
            else:
                logging.info("Pulse Dial type value is : %s" % state)
        else:
            if (state == True):
                current_button.mouse_click()
                logging.info(
                    "Pulse Dial type value is : %s" % self.spice.query_item(self.pulse_dialing_mode_menu_switch)["checked"])
            else:
                logging.info("Pulse Dial type value is : %s" % state)

    # ---------Toast/Alerts Validation-------

    def wait_for_fax_job_status_toast(self, message: str = "Success", timeout: int = 10):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: Scanning, Dialing, Faxing, Success... : str
        """
        option = ""
        if message == "Scanning":
            option = "Scanning..."
        elif message == "Dialing":
            option = "Dialing..."
        elif message == "Connecting":
            option = "Connecting..."
        elif message == "Faxing":
            option = "Faxing..."
        elif message == "Success":
            option = "Fax sent successfully!"
        elif message == "Receive":
            option = "Fax received successfully!"
        elif message == "Printing":
            option = "Printing fax"
        elif message == "Receiving":
            option = "Receiving page 1"
        elif message == "Canceling":
            option = "Canceling complete"
        elif message == "Processing":
            option = "Processing"

        self.spice.wait_for("#ToastSystemToastStackView", timeout = 15.0)
        for i in range(timeout):
            self.spice.wait_for("#ToastSystemToastStackView", timeout=15.0)
            status = self.spice.query_item("#ToastInfoText")["text"]
            logging.info("Current Toast message is : %s" % status)
            self.spice.wait_for("#ToastSystemToastStackView", timeout=15.0)
            if status == option:
                break
            time.sleep(1)
        if status != option:
            raise TimeoutError("Required Toast message does not appear within %s " % timeout)

    # ---------------------- Fax Receive Function cases ----------

    def fax_receive_settings_auto_answer(self, auto_answer: bool = False):
        """
        Purpose: Enables/Disables Auto answer in fax receive settings
        Args: auto_answer: True, False: Bool
        """
        current_screen = self.spice.wait_for(self.fax_dialing_screen)
        # while (self.spice.query_item(current_screen + " SpiceText")["text"] != "2-Sided Original"):
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(self.auto_answer_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.auto_answer_menu_switch)["activeFocus"] == True
        state = self.spice.query_item(self.auto_answer_menu_switch)["checked"]
        current_button = self.spice.wait_for(self.auto_answer_menu_switch + " SpiceText")
        time.sleep(0.5)
        if (auto_answer):
            if (state == False):
                current_button.mouse_click()
                time.sleep(0.5)
                logging.info(
                    "Pulse Dial type value is : %s" % self.spice.query_item(self.auto_answer_menu_switch)["checked"])
            else:
                logging.info("Pulse Dial type value is : %s" % state)
        else:
            if (state == True):
                current_button.mouse_click()
                logging.info(
                    "Pulse Dial type value is : %s" % self.spice.query_item(self.auto_answer_menu_switch)["checked"])
            else:
                logging.info("Pulse Dial type value is : %s" % state)

    def fax_set_ringer_volume(self, value):
        """
        Purpose: Set ringer volume in fax receive settings
        Args: volue: High,Low,Off
        """
        # # self.fax_menu_navigation("#Low", self.menu_selection_list_ringer_volume)
        val = ""
        if value == "High":
            val = self.ring_volume_high
        elif value == "Low":
            val = self.ring_volume_low
        elif value == "Off":
            val = self.ring_volume_off

        current_screen = self.spice.wait_for(self.ringer_volume_menu_name_value)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        time.sleep(1)
        current_button = self.spice.query_item(self.back_button + " SpiceText")
        time.sleep(1)
        while self.spice.query_item(self.ringer_volume_menu_name_value)["activeFocus"] == False:
            current_screen.mouse_wheel(180, 180)
        assert self.spice.query_item(self.ringer_volume_menu_name_value)["activeFocus"] == True
        # current_button = self.spice.wait_for(self.ring_volume_low)
        current_button = self.spice.wait_for(self.ringer_volume_menu_name_value)
        current_button.mouse_click()
        time.sleep(3)
        current_screen = self.spice.query_item(self.ring_volume_high)
        for i in range(4):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)

        if value == "High":
            while self.spice.query_item(val)["activeFocus"] == False:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(val)["activeFocus"] == True
            current_button = self.spice.wait_for(val)

        elif value == "Low":
            while self.spice.query_item(val)["activeFocus"] == False:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(val)["activeFocus"] == True
            current_button = self.spice.wait_for(val)

        elif value == "Off":
            while self.spice.query_item(val)["activeFocus"] == False:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(val)["activeFocus"] == True
            current_button = self.spice.wait_for(val)

        time.sleep(3)
        current_button.mouse_click()
        # time.sleep(2)
        # self.spice.wait_for(self.menu_selection_list_ringer_volume)

    def fax_receive_settings_set_values(self, options: str, value: bool = False):
        """
        Selects the values of Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes and Fit to Page
        Args: options: Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes, Fit to Page
              value: value : True/False : Bool
        """
        opt = ""
        if options == "Error Correction Mode":
            opt = self.error_correction_menu_switch
        elif options == "2-Sided Fax Printing":
            opt = self.two_sided_printing_menu_switch
        elif options == "Stamp Received Faxes":
            opt = self.stamp_received_faxes_menu_switch
        elif options == "Fit to Page":
            opt = self.automatic_reduction_menu_switch

        current_screen = self.spice.wait_for(self.fax_receive_setting_screen)
        #        while (self.spice.query_item(current_screen + " SpiceText")["text"] != "2-Sided Original"):
        for i in range(6):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(opt)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(opt)["activeFocus"] == True
        var = self.spice.query_item(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt + " SpiceText")
        if (value == True):
            if (var == False):
                current_option.mouse_click()
                logging.info(options+" value is : %s" % self.spice.query_item(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info(options+" value is : %s" % self.spice.query_item(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)

    # ---- Fax Forwarding Configuration ----

    def fax_receive_settings_set_fax_forwarding(self, forward, print, fax_number):
        """
        Selects the values of Fax forwarding based on user input like forward, forward+print and fax number
        Args: options: forward, print, fax_number
        """
        # current_screen = self.spice.wait_for(self.fax_forwarding_view)
        current_screen = self.spice.wait_for(self.forward_enabled_menu_switch)
        for i in range(3):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(self.forward_enabled_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.forward_enabled_menu_switch)["activeFocus"] == True
        var = self.spice.query_item(self.forward_enabled_menu_switch)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(self.forward_enabled_menu_switch)
        if (forward == True):
            if (var == False):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_enabled_menu_switch)["checked"])
                assert self.spice.query_item(self.forward_enabled_menu_switch)["checked"] != var, "Fax forward value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_enabled_menu_switch)["checked"])
                assert self.spice.query_item(self.forward_enabled_menu_switch)[
                           "checked"] != var, "Fax forward and Print value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)

        while (self.spice.query_item(self.forward_print_enabled_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.forward_print_enabled_menu_switch)["activeFocus"] == True
        var = self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(self.forward_print_enabled_menu_switch)
        if (print == True):
            if (var == False):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"])
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"])
            else:
                logging.info("Fax forward value is : %s" % var)

        if forward == True and print == True:
            while (self.spice.query_item(self.forward_number_menu_name_value)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(1)
            assert self.spice.query_item(self.forward_number_menu_name_value)["activeFocus"] == True
            current_option = self.spice.query_item(self.fax_forward_number_button)
            current_option.mouse_click()
            self.enter_numeric_keyboard_values(fax_number)

    # -------------- Numeric Keyboard ---------------

    def enter_numeric_keyboard_values(self, number, view=keyboard_view):
        current_screen = self.spice.wait_for(view)
        while (self.spice.query_item("#Key5")["color"] != "#000000"):
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
        for i in range(len(number)):
            num = number[i]
            logging.info(num)
            if (int(num) != 5):
                if (int(num) < 5) and int(num) != 0:
                    dial_value = 0
                else:
                    dial_value = 180
                while (self.spice.query_item("#Key" + num)["color"] != "#000000"):
                    current_screen.mouse_wheel(dial_value, dial_value)
                    time.sleep(0.5)
            current_screen.mouse_click()
            if (int(num) != 5):
                if (int(num) < 5) and int(num) != 0:
                    dial_value1 = 180
                else:
                    dial_value1 = 0
            while (self.spice.query_item("#Key5")["color"] != "#000000"):
                current_screen.mouse_wheel(dial_value1, dial_value1)
                time.sleep(0.5)

        while (self.spice.query_item("#Key1")["color"] != "#000000"):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)

        # while (self.spice.query_item("#ItemIconDelegatecheckmark")["iconCurrent"] != True):
        while (self.spice.query_item("#ItemIconDelegatecheckmark_xs")["iconCurrent"] != True):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_screen.mouse_click()

    # --- Send to Contact ----

    def fax_app_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        Args: None
        """
        self.goto_fax_app_recepient_screen()
        self.fax_menu_navigation(self.fax_send_to_contacts, self.faxSendToContactsView)
        current_screen = self.spice.wait_for(self.faxSendToContactsView)
        while (self.spice.query_item(self.contact1)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
        assert self.spice.query_item(self.contact1)["activeFocus"] == True
        time.sleep(1)
        # current_button = self.spice.wait_for(self.contact1)
        # current_button.mouse_click()    # Mouse click not working in current screen, hence using self.spice.click
        self.spice.click()
        time.sleep(1)
        logging.info(self.spice.query_item(self.contact1)["checked"])
        assert self.spice.query_item(self.contact1)["checked"] == True, "Contact is not checked"
        time.sleep(0.5)
        while (self.spice.query_item(self.FaxSendToContactDoneButton)["activeFocus"] == False):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        done_button = self.spice.wait_for(self.FaxSendToContactDoneButton + " SpiceText")
        done_button.mouse_click()
        time.sleep(1)
        self.spice.wait_for(self.fax_send_job_submission)

    def fax_app_send_or_cancel_no_contacts(self, yes_no: str = "No"):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app and enters fax
        number if user selects "Yes" and Cancel fax when user select "No"
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts ->
            If "Yes" Enter fax Num
            If "No" navigated back to fax recipient.
        Args: Yes/No
        """
        self.goto_fax_app_recepient_screen()
        self.fax_menu_navigation(self.fax_send_to_contacts, self.fax_send_no_contacts_available_view)
        current_screen = self.spice.wait_for(self.fax_send_no_contacts_available_view)
        if yes_no == "No":
            while (self.spice.query_item(self.fax_no_list_available_no_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(0.5)
            assert self.spice.query_item(self.fax_no_list_available_no_button)["activeFocus"] == True
            no_button = self.spice.wait_for(self.fax_no_list_available_no_button + " SpiceText")
            no_button.mouse_click()
            current_screen = self.spice.wait_for(self.fax_send_recipients_view)
        elif yes_no == "Yes":
            assert self.spice.query_item(self.fax_no_list_available_yes_button)["activeFocus"] == True
            no_button = self.spice.wait_for(self.fax_no_list_available_yes_button + " SpiceText")
            no_button.mouse_click()
            current_screen = self.spice.wait_for(self.fax_number_keyboard)
            args = sys.argv[sys.argv.index('faxNumber') + 1]
            # For single send, todo: Tests for multiple send scenario
            fax_number = parse_fax_arguments(args)[0]
            self.enter_numeric_keyboard_values(self.fax_number_keyboard, fax_number)

    def fax_add_remove_recipient(self, add_remove: str):
        """
        Purpose: Navigates from Job Submission screen to fax add/remove recipient in fax app
        Ui Flow: Job Submission -> # of Fax recipients -> Add/Remove
            If "Add" then navigates to Add recipient
            If "Remove" navigated Remove recipient.
        Args: Add/Remove
        """
        current_screen = self.spice.wait_for(self.fax_send_job_submission)
        while (self.spice.query_item(self.number_of_fax_recipients_button)["activeFocus"] == False):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        assert self.spice.query_item(self.number_of_fax_recipients_button)["activeFocus"] == True
        time.sleep(1)
        recipient_button = self.spice.wait_for(self.number_of_fax_recipients_button + " SpiceText")
        recipient_button.mouse_click()
        current_screen = self.spice.wait_for(self.list_of_fax_recipients_view)
        if add_remove == "Add":
            while (self.spice.query_item(self.add_recipients_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(0.5)
            assert self.spice.query_item(self.add_recipients_button)["activeFocus"] == True
            time.sleep(0.5)
            add_recipient_button = self.spice.wait_for(self.add_recipients_button + " SpiceText")
            add_recipient_button.mouse_click()
            self.spice.wait_for(self.fax_send_recipients_view + " SpiceText")

        current_screen = self.spice.wait_for(self.list_of_fax_recipients_view)
        if add_remove == "Remove":
            while (self.spice.query_item(self.recipient2)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(0.5)
            assert self.spice.query_item(self.recipient2)["activeFocus"] == True
            time.sleep(0.5)
            recipient_button = self.spice.wait_for(self.recipient2 + " SpiceText")
            recipient_button.mouse_click()
            remove_screen = self.spice.wait_for(self.fax_remove_recipient_view + " SpiceText")
            while (self.spice.query_item(self.remove_recipient_button)["activeFocus"] == False):
                remove_screen.mouse_wheel(180, 180)
                time.sleep(0.5)
            assert self.spice.query_item(self.remove_recipient_button)["activeFocus"] == True
            time.sleep(0.5)
            remove_button = self.spice.wait_for(self.remove_recipient_button + " SpiceText")
            remove_button.mouse_click()

    def fax_receive_settings_paper_tray_selection(self, option: str):
        """
        Purpose: Navigates to fax receive setttings screen to select the paper tray.
        Ui Flow: Fax receive settings -> Paper Tray -> Selection
        """
        current_screen = self.spice.query_item(self.menu_selection_list_paper_tray)
        opt = ""
        if option == "Tray1":
            opt = self.option_tray_1
        elif option == "Tray2":
            opt = self.option_tray_2
        elif option == "Tray3":
            opt = self.option_tray_3
        elif option== "Automatic":
            opt = self.option_automatic
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        if option == "Tray1":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        elif option == "Tray2":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        elif option == "Tray3":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        elif option == "Automatic":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        time.sleep(2)
        current_button.mouse_click()

    def fax_app_add_fax_number_confirm(self, fax_number, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_numeric_keyboard_values(fax_number, self.fax_number_keyboard)
        time.sleep(5)
        if confirm_fax_number:
            current_screen = self.spice.wait_for(self.confirm_fax_number_view)
            time.sleep(1)
            while (self.spice.query_item(self.fax_confirm_button)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(1)
            assert self.spice.query_item(self.fax_confirm_button)["activeFocus"] == True
            current_button = self.spice.wait_for(self.fax_confirm_button)
            current_button.mouse_click()
        time.sleep(10)
        self.spice.wait_for(self.fax_send_job_submission)

    def fax_app_enter_fax_number_confirm_cancel(self, fax_number):
        """
        Purpose: Enters fax number in enter fax number screen, confirm and cancel it.
        """
        self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_numeric_keyboard_values(fax_number)
        time.sleep(5)
        assert self.spice.wait_for(self.confirm_fax_number_view)
        current_screen = self.spice.wait_for(self.confirm_fax_number_view)
        time.sleep(1)
        while (self.spice.query_item(self.fax_cancel_button)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.fax_cancel_button)["activeFocus"] == True
        current_button = self.spice.wait_for(self.fax_cancel_button)
        current_button.mouse_click()
        time.sleep(5)
        current_screen = self.spice.wait_for(self.keyboard_view)
        while (self.spice.query_item("#ItemIconDelegateclose_xs")["iconCurrent"] != True):
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
        current_screen.mouse_click()

    def goto_fax_tools_fax_report(self):
        """
        Purpose: Navigates from home menu settings to fax reports
        Ui Flow: Menu -> tools -> Reports -> Fax reports
        Args: None
        """
        self.homemenu.goto_menu_tools_reports(self.spice)
        self.homemenu.menu_navigation(self.spice, "#MenuListLayout", self.tools_menu_report_button)

    def fax_report_print(self, option: str):
        """
        Purpose: Navigates to fax report options and prints
        Ui Flow: Fax reports -> report options
        """
        current_screen = self.spice.query_item(self.checkbox_button_list_layout)
        opt = ""
        if option == "Junk fax report":
            opt = self.junk_fax_report
        elif option == "Fax T.30 Trace Report":
            opt = self.fax_trace_report
        elif option == "Fax activity log":
            opt = self.fax_activity_log
        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        if option == "Junk fax report":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        elif option == "Fax T.30 Trace Report":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        elif option == "Fax activity log":
            while not self.spice.query_item(opt)["activeFocus"]:
                current_screen.mouse_wheel(180, 180)
            assert self.spice.query_item(opt)["activeFocus"] == True
            current_button = self.spice.wait_for(opt)
        time.sleep(2)
        current_button.mouse_click()

        for i in range(5):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        click_print_button = self.spice.wait_for(self.tools_menu_print_button)
        click_print_button.mouse_wheel(180, 180)
        click_print_button.mouse_click()

    def fax_app_multiple_recipients_using_enter_fax_number(self, fax_number_list):
        """
        Purpose: Enters multiple fax number one after the other and then waits for job submission page
        Args: fax_number_list which is provided on the test case
        """
        len_fax_number_list = len(fax_number_list)
        self.goto_fax_app_recipient_screen_enter_fax_number()
        for index, fax_number in enumerate(fax_number_list):
            self.enter_numeric_keyboard_values(fax_number, self.fax_number_keyboard)
            time.sleep(5)
            self.spice.wait_for(self.fax_send_job_submission)
            if index < len_fax_number_list-1:
                self.fax_menu_navigation(self.fax_add_recipients_button, self.fax_send_recipients_view)
                self.fax_menu_navigation(self.fax_enter_fax_number, self.fax_number_keyboard)

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
        len_fax_number_list = len(fax_number_list)
        self.goto_fax_app_recipient_screen()
        for index, fax_number in enumerate(fax_number_list):
            self.fax_menu_navigation(self.fax_send_to_contacts, self.fax_send_no_contacts_available_view)
            current_screen = self.spice.wait_for(self.fax_send_no_contacts_available_view)
            if yes_no == "No":
                while (self.spice.query_item(self.fax_no_list_available_no_button)["activeFocus"] == False):
                    current_screen.mouse_wheel(180, 180)
                    time.sleep(0.5)
                assert self.spice.query_item(self.fax_no_list_available_no_button)["activeFocus"] == True
                no_button = self.spice.wait_for(self.fax_no_list_available_no_button + " SpiceText")
                no_button.mouse_click()
                current_screen = self.spice.wait_for(self.fax_send_recipients_view)
            elif yes_no == "Yes":
                assert self.spice.query_item(self.fax_no_list_available_yes_button)["activeFocus"] == True
                no_button = self.spice.wait_for(self.fax_no_list_available_yes_button + " SpiceText")
                no_button.mouse_click()
                current_screen = self.spice.wait_for(self.fax_number_keyboard)
                self.enter_numeric_keyboard_values(fax_number, self.fax_number_keyboard)
                self.spice.wait_for(self.fax_send_job_submission)

                if index < len_fax_number_list - 1:
                    self.fax_menu_navigation(self.fax_add_recipients_button, self.fax_send_recipients_view)

    def create_fax_multiple_contacts(self, cdm, udw, payload_list):
        """
        Purpose: Creates fax contacts (record id's) using the payload list provided on the test case.
        Args: payload_list which is provided on the test case
        Returns: record id list
        """
        fax = Fax(cdm, udw)
        record_id_list = []
        for payload in payload_list:
            recordId = fax.create_fax_contact(payload)
            record_id_list.append(recordId)
        return record_id_list

    def select_multi_destination_contacts(self, record_id_list):
        """
        Purpose: Selects fax contacts to send to multi destination using addressbook (send to contacts) option
        Args: record_id_list which is passed on sequentially from create_fax_multiple_contacts keyword.
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        """
        self.goto_fax_app_recipient_screen()
        for index, record_id in enumerate(record_id_list):
            self.fax_menu_navigation(self.fax_send_to_contacts, self.faxSendToContactsView)
            contact_object_id = "#FaxSendToContact" + record_id
            current_screen = self.spice.wait_for(self.faxSendToContactsView)
            while (self.spice.query_item(contact_object_id)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(0.5)
            assert self.spice.query_item(contact_object_id)["activeFocus"] == True
            time.sleep(1)
            #self.spice.click()  not working in  self.spice.click, hence using current screen.mouse_click()
            current_screen.mouse_click()
            time.sleep(1)
            logging.info(self.spice.query_item(contact_object_id)["checked"])
            assert self.spice.query_item(contact_object_id)["checked"] == True, "Contact is not checked"
            time.sleep(0.5)
            while (self.spice.query_item(self.FaxSendToContactDoneButton)["activeFocus"] == False):
                current_screen.mouse_wheel(0, 0)
                time.sleep(0.5)
            done_button = self.spice.wait_for(self.FaxSendToContactDoneButton + " SpiceText")
            done_button.mouse_click()
            time.sleep(1)
            self.spice.wait_for(self.fax_send_job_submission)

            if index < len(record_id_list) - 1:
                self.fax_menu_navigation(self.fax_add_recipients_button, self.fax_send_recipients_view)

    def incoming_receive_fax(self, cdm, udw, faxSimIP: str, auto_answer: str = "Yes", cancel: str = Cancel.no,
                             waitTime: int = 100, stampReceivedFax: str = "false", blockedFaxNumber: str = "", faxPrintingSchedule: str ="alwaysPrint",
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
            stampReceivedFax: Bool indicating received fax is stamped or not. Defaults to false.

        Returns:
            None
        """
        fax_instance = Fax(cdm, udw)
        print("fax instance created successfully")
        fax_instance.check_modem_status
        trace_log('========== RECEIVE FAX config setup ==========')
        fax_instance.set_receive_fax_config(stampReceivedFax=stampReceivedFax, faxPrintingSchedule=faxPrintingSchedule)
        if(blockedFaxNumber != ""):
            fax_instance.create_receive_fax_blocked_number(blockedFaxNumber)

        fax_instance.update_receive_fax_ticket(**payLoad)
        trace_log('========== RECEIVE FAX Job Started ==========')
        max_wait_time = waitTime

        # name mangling
        fax_instance._Fax__receive_fax(faxSimIP)

        if auto_answer == "No":
            assert self.spice.wait_for(self.incoming_fax_receive_page, timeout=9.0)
            while (self.spice.query_item(self.incoming_fax_accept_button, 0)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(1)
            assert self.spice.query_item(self.incoming_fax_accept_button, 0)["activeFocus"] == True
            current_button = self.spice.query_item(self.incoming_fax_accept_button, 0)
            current_button.mouse_click()

        job_end_point = fax_instance._Fax__get_job_end_point('receiveFax')
        job_id = re.findall('(?:jobs/)(.*)', job_end_point)[0]
        trace_log('Created Job Id : {}'.format(job_id))

        # TODO:
        # Currently this handles only for cancel after start scenario,
        # Need to find a way to check for created and ready states as job is transitioning to processing states by the time we get the jobid
        if cancel == Cancel.after_init:
            fax_instance._job.check_job_state(job_id, 'ready', max_wait_time)
            fax_instance._job.cancel_job(job_id)

            jobs = self._job.get_job_history()
            job_in_history = [job for job in jobs if job.get('jobId') == job_id]
            assert len(job_in_history) == 0, 'Unexpected job in job history!'

            trace_log('Canceled Job Id : {}'.format(job_id))

        elif cancel == Cancel.after_create:
            fax_instance._job.check_job_state(job_id, 'created', max_wait_time)
            fax_instance._job.cancel_job(job_id)

            jobs = self._job.get_job_history()
            job_in_history = [job for job in jobs if job.get('jobId') == job_id]
            assert len(job_in_history) == 0, 'Unexpected job in job history!'

            trace_log('Canceled Job Id : {}'.format(job_id))

        elif cancel == Cancel.after_start:
            fax_instance._job.check_job_state(job_id, 'processing', max_wait_time)
            fax_instance._job.cancel_job(job_id)
            fax_instance._job.check_job_state(job_id, 'completed', max_wait_time, True)
            trace_log('Canceled Job Id : {}'.format(job_id))
            self.wait_for_fax_job_status_toast("Canceling", 100)

        else:
            fax_instance._job.check_job_state(job_id, 'processing', max_wait_time)
            print('started processing the fax receive job..')
            self.wait_for_fax_job_status_toast("Receive", 90)
            self.wait_for_fax_job_status_toast("Printing", 100)

            if cancel == Cancel.submit_and_exit:  # reusing cancel parameter to submit job and exit without waiting for completion
                trace_log('Submitted fax receive Job with Id: ' + job_id + ' .Track it to completion.')
            else:
                if blockedFaxNumber:
                    print('\n========== RECEIVE FAX blocked fax reset ==========')
                    response = fax_instance._cdm.get(fax_instance._CREATE_BLOCKED_FAX_NUMBER_ENDPOINT)
                    fax_numbers_id = response['blockedNumber'][0]['faxNumbersId']
                    print(fax_numbers_id)
                    # If it is call from blocked number then completion state should be cancelled
                    fax_instance._job.check_job_state(job_id, "completed", max_wait_time, cancel=True)
                    trace_log('Completed Job Id: : {}'.format(job_id))
                    fax_instance.destroy_blocked_fax_number(fax_numbers_id)
                else:
                    fax_instance._job.check_job_state(job_id, 'completed', max_wait_time)
                    trace_log('Completed Job Id : {}'.format(job_id))

            # After receiveFax completion check if forward is configured and validate scanFax
            faxConfig = fax_instance.get_fax_forward_config()
            # false means enabled for now
            if faxConfig["faxForwardEnabled"] == 'true':
                FORWARD_JOB_END_POINT = fax_instance._Fax__get_job_end_point('scanFax')
                # get Job Id from JobEndPoint
                forwardJobid = re.findall('(?:jobs/)(.*)', FORWARD_JOB_END_POINT)[0]
                trace_log('Forward Job Id : {}'.format(forwardJobid))
                # Check for completion state
                fax_instance._job.check_job_state(forwardJobid, "completed", max_wait_time)
                trace_log('Completed Job Id: : {}'.format(forwardJobid))

        trace_log('========== RESET RECEIVE FAX TICKET TO DEFAULT ==========')
        fax_instance.reset_receive_fax_ticket()

        trace_log('========== RECEIVE FAX Job Finished ==========')

    def goto_fax_settings_fax_setup_phone_line_details(self):
        """
        Purpose: Navigates from Basic fax setup screen to phoneline selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Next -> Phoneline details view
        Args: None
        """
        self.spice.wait_for(self.fax_setup_menu_button)
        self.fax_menu_navigation(self.basic_fax_setup_next_button, self.fax_phone_line_details, True)
        # current_screen = self.spice.wait_for(self.FaxSetup_line_share_NoButton)
        # while (self.spice.query_item(self.FaxSetup_line_share_NoButton)["activeFocus"] == False):
        #     current_screen.mouse_wheel(180, 180)
        #     time.sleep(0.5)
        # assert self.spice.query_item(self.FaxSetup_line_share_NoButton)["activeFocus"] == True
        # current_button = self.spice.wait_for(self.FaxSetup_line_share_NoButton + " SpiceText")
        # current_button.mouse_click()
        # time.sleep(3)
        # # self.spice.click()
        # self.spice.wait_for(self.fax_phone_line_details)

    def goto_fax_settings_fax_setup_country_location(self):

        """
        Purpose: Navigates from Basic fax setup screen to Country/Location selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Country/Location Selection view
        Args: None
        """
        self.fax_menu_navigation(self.basic_fax_setup_country_location_button, self.fax_select_country_view)

    def goto_fax_app_recipient_screen_after_set_basic_fax_settings(self):
        """
        Purpose: Navigates to Fax recipients screen without handling basic setup screen from any other screen
        Ui Flow: Any screen -> Main menu -> Fax app ->Fax Recipient screen
        :param spice: Takes 0 arguments
        :return: None
        """
        self.goto_mainmenu()
        # move to the Fax app
        startTime = time.time()
        timeSpentWaiting = 0
        current_screen = self.spice.wait_for("#HomeScreenView")
        while (self.spice.query_item("#CurrentAppText")[
                   "text"] != "Fax" and timeSpentWaiting < self.maxtimeout):
            current_screen.mouse_wheel(180, 180)
            timeSpentWaiting = time.time() - startTime
            time.sleep(1)
        assert self.spice.query_item("#CurrentAppText")["text"] == "Fax"
        time.sleep(5)
        currentApp = self.spice.wait_for(self.menu_item_faxid)
        currentApp.mouse_click()
        self.spice.wait_for(self.fax_send_recipients_view)

    def fax_recipient_screen_enter_fax_number(self, fax_number):
        """
        Purpose: Navigates from fax recipient screen to enter fax number
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: Fax number
        """
        self.spice.wait_for(self.fax_send_recipients_view)
        self.fax_menu_navigation(self.fax_enter_fax_number, self.fax_number_keyboard)
        self.enter_numeric_keyboard_values(fax_number)
        self.spice.wait_for(self.fax_send_job_submission)

    def wait_for_header(self):
        """
        Purpose:Wait for until header object present
        """
        self.spice.wait_for(self.basic_fax_setup_fax_header_name_button)

    def wait_for_basic_fax_setup_fax_number(self):
        """
        Purpose:Wait for until Fax number object present
        :return:
        """
        self.spice.wait_for(self.basic_fax_setup_faxnumber_button)
		
    def wait_for_basic_fax_setup_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        self.spice.wait_for(self.basic_fax_setup_next_button)

    def fax_receieve_set_distinctive_ring(self, distinctive_ring: str = None):
        """
        :param spice: None
        :param distinctive_ring: Single Ring, Double Rings, Triple Rings, Double and Triple Rings,Use Recorded Ring,All Standard Rings,
        Ring Pattern Detection.
        :return:
        """
        distinctive_ring_name = ""
        if distinctive_ring == "Single Ring":
            distinctive_ring_name = "SingleRing"
        elif distinctive_ring == "Double Rings":
            distinctive_ring_name = "DoubleRing"
        elif distinctive_ring == "Triple Rings":
            distinctive_ring_name = "TripleRing"
        elif distinctive_ring == "Double and Triple Rings":
            distinctive_ring_name = "DoubleAndTripleRing"
        elif distinctive_ring == "Use Recorded Ring":
            distinctive_ring_name = "RecordedRingPattern"
        elif distinctive_ring == "All Standard Rings":
            distinctive_ring_name = "AllStandardRings"
        elif distinctive_ring == "Ring Pattern Detection":
            distinctive_ring_name = "StartRecord"
        else:
            raise logging.info(f"Trying to select Distinctive ring:{distinctive_ring} is not supported to set,"
                               f"Choose proper Distinctive ring name")
        distinctive_ring_id = "#option_" + distinctive_ring_name
        current_screen = self.spice.wait_for(self.menu_selection_list_Distinctive_ring)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_button = self.spice.query_item(self.back_button + " SpiceText")
        while (self.spice.query_item(distinctive_ring_id)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
        time.sleep(0.5)
        assert self.spice.query_item(distinctive_ring_id)["activeFocus"] == True
        assert self.spice.query_item(distinctive_ring_id + " SpiceText")["text"] == str(distinctive_ring)
        time.sleep(1)
        logging.info(self.spice.query_item(distinctive_ring_id + " SpiceText")["text"])
        current_distinctive_ring = self.spice.wait_for(distinctive_ring_id)
        #self.spice.click()  # mouse_click() not working
        current_distinctive_ring.mouse_click()
        time.sleep(1)
        current_screen = self.spice.wait_for(self.menu_selection_list_Distinctive_ring)
        for i in range(10):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_button = self.spice.query_item(self.back_button + " SpiceText")
        current_button.mouse_click()
        self.spice.wait_for(self.fax_receive_menu_button)

    def fax_basic_setup_alert_without_basic_details(self):
        """
        Purpose: Validate the error screen when basic setup details either any Country name,Header name or Fax number
        field empty
        :return:
        """
        self.spice.wait_for(self.fax_setup_menu_button)
        self.fax_menu_navigation(self.basic_fax_setup_next_button, self.faxcheck_Basic_Fax_setup_View, True)
        self.spice.wait_for(self.faxcheck_alert_ok_button)
        logging.info("Fax basic details enter alert pop up displayed")

    def fax_app_add_editable_billing_code(self, fax_number, index_val):
        """
        Purpose: Enter editable billing code.
        Args: Index value: Stack 0 or 1
        """
        self.dial_keyboard_operations.keyboard_set_text_with_out_dial_action(fax_number, index_val)

    def fax_delete_prefix_value(self, index_val):
        """
        Purpose: Delete dial Prefix value
        Args: Index value: Stack 0 or 1
        """
        self.fax_menu_navigation("#dialingPrefixMenuButton", self.keyboard_view)
        current_screen = self.spice.wait_for(self.keyboard_view)
        self.dial_keyboard_operations.keyboard_clear_text(index_val)
        time.sleep(1)
        while (self.spice.query_item("#ItemIconDelegatecheckmark_xs", index_val)["iconCurrent"] != True):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_screen.mouse_click()
        time.sleep(3)

    def fax_add_prefix_close(self, prefix, index_value):
        """
        Purpose: Add dial Prefix value and close without saving it.
        Args: Index value: Stack 0 or 1
        """
        self.fax_menu_navigation("#dialingPrefixMenuButton", self.keyboard_view)
        keyboardTextField = self.spice.query_item("#spiceKeyboardView", index_value)
        keyboardTextField["currentText"] = prefix
        current_screen = self.spice.wait_for(self.keyboard_view)
        while (self.spice.query_item("#ItemIconDelegateclose_xs", index_value)["iconCurrent"] != True):
            current_screen.mouse_wheel(0, 0)
            time.sleep(0.5)
        current_screen.mouse_click()

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
        fax_instance = Fax(cdm, udw)
        print("fax instance created successfully")
        fax_instance.check_modem_status
        
        fax_instance.update_receive_fax_ticket(**payLoad)
        trace_log('========== RECEIVE FAX Job Started ==========')
        max_wait_time = waitTime

        # name mangling
        fax_instance._Fax__receive_fax(faxSimIP)

        if auto_answer == "No":
            assert self.spice.wait_for(self.incoming_fax_receive_page, timeout=9.0)
            while (self.spice.query_item(self.incoming_fax_accept_button, 0)["activeFocus"] == False):
                current_screen.mouse_wheel(180, 180)
                time.sleep(1)
            assert self.spice.query_item(self.incoming_fax_accept_button, 0)["activeFocus"] == True
            current_button = self.spice.query_item(self.incoming_fax_accept_button, 0)
            current_button.mouse_click()

        job_end_point = fax_instance._Fax__get_job_end_point('receiveFax')
        job_id = re.findall('(?:jobs/)(.*)', job_end_point)[0]
        trace_log('Created Job Id : {}'.format(job_id))

        # TODO:
        # Currently this handles only for cancel after start scenario,
        # Need to find a way to check for created and ready states as job is transitioning to processing states by the time we get the jobid
        if cancel == Cancel.after_init:
            fax_instance._job.check_job_state(job_id, 'ready', max_wait_time)
            fax_instance._job.cancel_job(job_id)
            fax_instance._job.check_job_state(job_id, 'completed', max_wait_time, True)
            trace_log('Canceled Job Id : {}'.format(job_id))

        elif cancel == Cancel.after_create:
            fax_instance._job.check_job_state(job_id, 'created', max_wait_time)
            fax_instance._job.cancel_job(job_id)
            fax_instance._job.check_job_state(job_id, 'completed', max_wait_time, True)
            trace_log('Canceled Job Id : {}'.format(job_id))

        elif cancel == Cancel.after_start:
            fax_instance._job.check_job_state(job_id, 'processing', max_wait_time)
            fax_instance._job.cancel_job(job_id)
            fax_instance._job.check_job_state(job_id, 'completed', max_wait_time, True)
            trace_log('Canceled Job Id : {}'.format(job_id))
            self.wait_for_fax_job_status_toast("Canceling", 100)

        else:
            fax_instance._job.check_job_state(job_id, 'processing', max_wait_time)
            print('started processing the fax receive job..')

        trace_log('========== RESET RECEIVE FAX TICKET TO DEFAULT ==========')
        fax_instance.reset_receive_fax_ticket()

        trace_log('========== RECEIVE FAX Job Finished ==========')

    def fax_receive_settings_set_fax_forwarding_print_number(self, forward, print, fax_number):
        """
        Selects the values of Fax forwarding based on user input like forward, forward+print and fax number.
        Add fax number with all combination even if fax forward or print is disabled.
        Args: options: forward, print, fax_number
        """
        current_screen = self.spice.wait_for(self.forward_enabled_menu_switch)
        for i in range(3):
            current_screen.mouse_wheel(0, 0)
            time.sleep(1)
        while (self.spice.query_item(self.forward_enabled_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.forward_enabled_menu_switch)["activeFocus"] == True
        var = self.spice.query_item(self.forward_enabled_menu_switch)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(self.forward_enabled_menu_switch)
        if (forward == True):
            if (var == False):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_enabled_menu_switch)["checked"])
                assert self.spice.query_item(self.forward_enabled_menu_switch)["checked"] != var, "Fax forward value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_enabled_menu_switch)["checked"])
                assert self.spice.query_item(self.forward_enabled_menu_switch)[
                           "checked"] != var, "Fax forward and Print value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)

        while (self.spice.query_item(self.forward_print_enabled_menu_switch)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.forward_print_enabled_menu_switch)["activeFocus"] == True
        var = self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(self.forward_print_enabled_menu_switch)
        if (print == True):
            if (var == False):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"])
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click()
                logging.info("Fax forward value is : %s" % self.spice.query_item(self.forward_print_enabled_menu_switch)["checked"])
            else:
                logging.info("Fax forward value is : %s" % var)

        while (self.spice.query_item(self.forward_number_menu_name_value)["activeFocus"] == False):
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
        assert self.spice.query_item(self.forward_number_menu_name_value)["activeFocus"] == True
        current_option = self.spice.query_item(self.fax_forward_number_button)
        current_option.mouse_click()
        time.sleep(5)
        self.dial_keyboard_operations.keyboard_clear_text()
        self.enter_numeric_keyboard_values(fax_number)
        time.sleep(5)

    def fax_setup_phone_line_sharing_selection(self, option='Yes'):
        """
        Selects the phone line option yes or no. Default it is set as Yes.
        Args: options: Yes and No
        """
        self.spice.wait_for(self.fax_phone_line_details)
        self.fax_menu_navigation(self.phone_line_Details_NextButton, self.FaxSetUP_line_share)
        current_screen = self.spice.wait_for(self.FaxSetUP_line_share)
        time.sleep(5)
        if option == 'Yes':
            current_button = self.spice.wait_for(self.FaxSetup_line_share_YesButton)
            assert self.spice.query_item(self.FaxSetup_line_share_YesButton)["activeFocus"] == True
            current_button.mouse_click()
        else:
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
            current_button = self.spice.wait_for(self.FaxSetup_line_share_NoButton)
            assert self.spice.query_item(self.FaxSetup_line_share_NoButton)["activeFocus"] == True
            current_button.mouse_click()

    def fax_setup_voice_call_selection(self, option='Yes'):
        """
        Selects the voice call option yes or no. Default it is set as Yes.
        Args: options: Yes and No
        """
        current_screen = self.spice.wait_for(self.fax_setup_voice_calls)
        time.sleep(5)
        if option == 'Yes':
            current_button = self.spice.wait_for(self.fax_setup_voice_calls_YesButton)
            assert self.spice.query_item(self.fax_setup_voice_calls_YesButton)["activeFocus"] == True
            current_button.mouse_click()
        else:
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
            current_button = self.spice.wait_for(self.fax_setup_voice_calls_NoButton)
            assert self.spice.query_item(self.fax_setup_voice_calls_NoButton)["activeFocus"] == True
            current_button.mouse_click()

    def fax_setup_distinctive_ring_availability(self, net, option='Yes', distinctive_ring = None):
        """
        Selects the distinctive rings option and also Recorded ring is unavailable is handled.
        Args: options: Single Ring, Double Ring, Triple Ring, All standard ring, Ring Pattern Detection, Recorded ring
        """
        current_screen = self.spice.wait_for(self.fax_setup_distinctive_ring_for_fax)
        time.sleep(5)
        if option == 'Yes':
            current_button = self.spice.wait_for(self.fax_set_up_distinctive_ring_for_fax_yes_button)
            assert self.spice.query_item(self.fax_set_up_distinctive_ring_for_fax_yes_button)["activeFocus"] == True
            current_button.mouse_click()
            time.sleep(5)
            current_screen = self.spice.wait_for(self.fax_setup_distinctive_ring_for_fax)
            current_screen.mouse_wheel(180, 180)
            time.sleep(1)
            current_button1 = self.spice.query_item(self.fax_check_basic_fax_setup_view)
            current_button1.mouse_click()
            time.sleep(5)
            if distinctive_ring != 'Use Recorded Ring':
                self.fax_receieve_set_distinctive_ring(distinctive_ring)
                current_screen = self.spice.wait_for(self.fax_setup_distinctive_ring_for_fax)
                while (self.spice.query_item(self.next)["activeFocus"] == False):
                    current_screen.mouse_wheel(180, 180)
                    time.sleep(1)
                assert self.spice.query_item(self.next)["activeFocus"] == True
                current_option = self.spice.query_item(self.next)
                current_option.mouse_click()
            else:
                distinctive_ring_id = "#option_" + "RecordedRingPattern"
                current_screen = self.spice.wait_for(self.menu_selection_list_Distinctive_ring)
                for i in range(10):
                    current_screen.mouse_wheel(0, 0)
                    time.sleep(0.5)
                current_button = self.spice.query_item(self.back_button + " SpiceText")
                while (self.spice.query_item(distinctive_ring_id)["activeFocus"] == False):
                    current_screen.mouse_wheel(180, 180)
                    time.sleep(0.5)
                assert self.spice.query_item(distinctive_ring_id)["activeFocus"] == True
                assert self.spice.query_item(distinctive_ring_id + " SpiceText")["text"] == str(distinctive_ring)
                time.sleep(1)
                logging.info(self.spice.query_item(distinctive_ring_id + " SpiceText")["text"])
                current_distinctive_ring = self.spice.wait_for(distinctive_ring_id)
                current_distinctive_ring.mouse_click()
                time.sleep(2)
                assert self.spice.query_item("#Version1Text", 19)["text"] == \
                       LocalizationHelper.get_string_translation(net, 'cUnavailable')
                assert self.spice.query_item(self.ok_button)["activeFocus"] == True
                current_button = self.spice.query_item(self.ok_button)
                current_button.mouse_click()
        else:
            current_screen.mouse_wheel(180, 180)
            time.sleep(0.5)
            current_button = self.spice.wait_for(self.fax_set_up_distinctive_ring_for_fax_no_button)
            assert self.spice.query_item(self.fax_set_up_distinctive_ring_for_fax_no_button)["activeFocus"] == True
            current_button.mouse_click()


