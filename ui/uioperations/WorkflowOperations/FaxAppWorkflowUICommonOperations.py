import logging
import time
import sys
from dunetuf.fax.fax import *
from dunetuf.ui.uioperations.BaseOperations.IFaxAppUIOperations import IFaxAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from enum import Enum, unique
from dunetuf.fax.fax import FaxModemType
from dunetuf.network.net import Network
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from datetime import datetime , timedelta

@unique
class FaxCountryRegionOptionForUi(Enum):
    NONE = "cNone" #None
    AR = "cCountryRegionArgentina" # Argentina
    AU = "cCountryRegionAustralia" # Australia
    AT = "cCountryRegionAustria" # Austria
    BY = "cCountryRegionBelarus" # Belarus
    BE = "cCountryRegionBelgium" # Belgium
    BR = "cCountryRegionBrazil" # Brazil
    BG = "cCountryRegionBulgaria" # Bulgaria
    CA = "cCountryRegionCanada" # Canada
    CL = "cCountryRegionChile" # Chile
    CN = "cCountryRegionChina" # China
    HR = "cCountryRegionCroatia" # Croatia
    CZ = "cCountryRegionCzechRepublic" # Czech Republic
    DK = "cCountryRegionDenmark" # Denmark
    EE = "cCountryRegionEstonia" # Estonia
    FI = "cCountryRegionFinland" # Finland
    FR = "cCountryRegionFrance" # France
    DE = "cCountryRegionGermany" # Germany
    GR = "cCountryRegionGreece" # Greece
    HK = "cCountryRegionHongKongSAR" # Hong Kong SAR
    HU = "cCountryRegionHungary" # Hungary
    IS = "cCountryRegionIceland" # Iceland
    IN = "cCountryRegionIndia" # India
    ID = "cCountryRegionIndonesia" # Indonesia
    IE = "cCountryRegionIreland" # Ireland
    IL = "cCountryRegionIsrael" # Israel
    IT = "cCountryRegionItaly" # Italy
    JP = "cCountryRegionJapan" # Japan
    LV = "cCountryRegionLatvia" # Latvia
    LI = "cCountryRegionLiechtenstein" # Liechtenstein
    LT = "cCountryRegionLithuania" # Lithuania
    LU = "cCountryRegionLuxembourg" # Luxembourg
    MY = "cCountryRegionMalaysia" # Malaysia
    MX = "cCountryRegionMexico" # Mexico
    MA = "cCountryRegionMorocco" # Morocco
    NL = "cCountryRegionNetherlands" # Netherlands
    NZ = "cCountryRegionNewZealand" # New Zealand
    NO = "cCountryRegionNorway" # Norway
    PK = "cCountryRegionPakistan" # Pakistan
    PE = "cCountryRegionPeru" # Peru
    PH = "cCountryRegionPhilippines" # Philippines
    PL = "cCountryRegionPoland" # Poland
    PT = "cCountryRegionPortugal" # Portugal
    RO = "cCountryRegionRomania" # Romania
    RU = "cCountryRegionRussia" # Russia
    SG = "cCountryRegionSingapore" # Singapore
    SK = "cCountryRegionSlovakia" # Slovakia
    SI = "cCountryRegionSlovenia" # Slovenia
    ZA = "cCountryRegionSouthAfrica" # South Africa
    ES = "cCountryRegionSpain" # Spain
    LK = "cCountryRegionSriLanka" # Sri Lanka
    SE = "cCountryRegionSweden" # Sweden
    CH = "cCountryRegionSwitzerland" # Switzerland
    TW = "cCountryRegionTaiwan" # Taiwan Region
    TH = "cCountryRegionThailand" # Thailand
    TR = "cCountryRegionTurkey" # Turkey
    UA = "cCountryRegionUkraine" # Ukraine
    GB = "cCountryRegionUnitedKingdom" # United Kingdom
    US = "cCountryRegionUnitedStates" # United States
    VN = "cCountryRegionVietnam" # Vietnam 

class FaxAppWorkflowUICommonOperations(IFaxAppUIOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.homeoperations = spice.home_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.configuration = Configuration(CDM(self.spice.ipaddress))

    original_size_option_dict = {
        "Any": {
            "item_id": FaxAppWorkflowObjectIds.radio_original_size_any,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_any
            },
        "MIXED_LETTER_LEGAL": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_mixed_letter_legal,
            "row_id": FaxAppWorkflowObjectIds.row_originalSize_mixed_letter_legal
            },
        "MIXED_LETTER_LEDGER": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_mixed_letter_ledger,
            "row_id": FaxAppWorkflowObjectIds.row_originalSize_mixed_letter_ledger
            },
        "MIXED_A4_A3": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_mixed_a4_a3,
            "row_id": FaxAppWorkflowObjectIds.row_originalSize_mixed_a4_a3
            },
        "Letter": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_na_letter_8_5x11in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_na_letter_8_5x11in
            },
        "Letter_SEF": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_rotate_na_letter_8_5x11in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_rotate_na_letter_8_5x11in
            },
        "Legal": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_na_legal_8_5x14in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_na_legal_8_5x14in
            },
        "Executive": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_na_executive_7_dot_25x10_dot_5in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_executive_7_25x10_5in
            },
        "Statement (8.5x5.5 in.)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_invoice_5_5x8_5in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_invoice_5_5x8_5in
            },
        "Ledger": { 
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_tabloid_11x17,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_tabloid_11x17
            },
        "3x5 in": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_3x5in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_3x5in
            },
        "4x6 in.": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_index_4x6_4x6in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_index_4x6_4x6in
            },
        "5x5 in": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_5x5in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_5x5in
            },
        "5x7 in.": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_5x7in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_5x7in
            },
        "5x8 in.": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_index_5x8_5x8in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_index_5x8_5x8in
            },
        "foolscap_8_dot_5x13in": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_na_foolscap_8_dot_5x13in,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_foolscap_8_5x13in
            },
        "Oficio_8_5x13_4": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_oficio_216x340,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_oficio_216x340
            },
        "A3": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_a3,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_a3
            },
        "A4": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_iso_a4_210x297mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_iso_a4_210x297mmn
            },
        "A4_SEF": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_rotate_iso_a4_210x297mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_rotate_iso_a4_210x297mmn
            },
        "A5": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_iso_a5_148x210mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_iso_a5_148x210mm
            },
        "A5_SEF": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_rotate_iso_a5_148x210mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_rotate_iso_a5_148x210mm
            },
        "A6": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_iso_a6_105x148mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_iso_a6_105x148mm
            },
        "RA4": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_iso_ra4_215x305mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_iso_ra4_215x305mmscan_originalSize
            },
        "B4 (JIS) (257x364 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_b4,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_b4
            },
        "B5": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_jis_b5_182x257mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_jis_b5_182x257mm
            },
        "B5_SEF": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_rotate_jis_b5_182x257mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_rotate_jis_b5_182x257mm
            },
        "B6 (JIS) (128x182 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_jis_b6_128x182mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_jis_b6_128x182mm
            },
        "16K (195x270 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_om_16k_195x270mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_16k_195x270
            },
        "16K (184x260 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_16k_184x260,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_16k_184x260
            },
        "16K (197x273 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_16k_197x273,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_16k_197x273
            },
        "Double Postcard (JIS) (148x200 mm)": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_double_postcard_jis_148x200mm,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_double_postcard_jis_148x200mm
            },
        "100x150mm": {
            "item_id": FaxAppWorkflowObjectIds.radio_originalSize_10x15,
            "row_id": FaxAppWorkflowObjectIds.row_original_size_10x15
            }
    }

    original_dict = {
        "Letter": [FaxAppWorkflowObjectIds.fax_mediasize_letter_str_id],
        "Any":[FaxAppWorkflowObjectIds.fax_mediasize_any_str_id]
    }

    content_orientation_option_dict = {
        "portrait": FaxAppWorkflowObjectIds.orientation_portrait_option,
        "landscape": FaxAppWorkflowObjectIds.orientation_landscape_option
    }

    def goto_menu_ringer_volume(self):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> ringer volume
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        ringer_volume = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_ringer_volume)
        ringer_volume.mouse_click()

    def goto_fax_receive_options(self, proprtyId: str = FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive):
        """
        Purpose: Navigates from home menu settings to receive fax two sided printing screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Two Sided Printing
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.goto_item(proprtyId, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        self.spice.wait_for(proprtyId)

    def goto_fax_send_options(self, proprtyId: str = FaxAppWorkflowObjectIds.menuSwitch_pcSendFax):
        """
        Purpose: Navigates from home menu settings to send fax two sided printing screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax send Settings -> Two Sided Printing
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.workflow_common_operations.goto_item(proprtyId, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        self.spice.wait_for(proprtyId)

    def goto_menu_fax_forward_configuration(self):
        """
        Purpose: Navigates from home menu settings to fax forward configuration screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Forward Configuration
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menuText_faxForwarding,scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        fax_forwarding_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list)
        self.spice.wait_until(lambda:fax_forwarding_view["visible"])
        logging.info("At Fax Forward Configuration screen")
        
    def back_to_fax_settings_from_fax_forward_configuration_screen_with_back_button(self):
        """
        Back to fax_settings screen from fax_forward_configuration screen through back button.
        """
        logging.info("Go back to fax_settings screen from fax_forward_configuration screen with back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list} {FaxAppWorkflowObjectIds.button_back}')
        fax_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_menu_fax_settings)
        self.spice.wait_until(lambda:fax_settings_view["visible"])
        logging.info("At Fax Settings screen")

    def back_to_fax_settings_from_basic_fax_setup_screen_with_back_button(self):
        """
        Back to fax_settings screen from basic_fax_setup screen through back button.
        """
        logging.info("Go back to fax_settings screen from basic_fax_setup screen with back button.")
        back_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.button_back}")
        self.spice.wait_until(lambda:back_button["visible"]), f"back button does not exist"
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen, landing_view = FaxAppWorkflowObjectIds.view_faxSettingsScreen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.button_back}')

    def goto_menu_rings_to_answer(self,value):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Rings to Answer
        Args: value: 1/2/3/4/5/6
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        ringsToAnswer = self.spice.wait_for(FaxAppWorkflowObjectIds.spinbox_ringsToAnswer)
        ringsToAnswer.mouse_click()

        current_field = self.spice.wait_for(FaxAppWorkflowObjectIds.spinbox_line2ringsToAnswer)
        self.spice.wait_until(lambda:current_field["visible"]), f"ring to answer spin box does not exist"
        #wait second for default value shows. Otherwise, value will be overwritten by the default value.
        time.sleep(5)
        current_field.__setitem__('value', value)

    def fax_receive_settings_set_rings_to_answer(self,value):

        current_field = self.spice.wait_for(FaxAppWorkflowObjectIds.spinbox_ringsToAnswer)
        self.spice.wait_until(lambda:current_field["visible"]), f"ring to answer spin box does not exist"
        #wait second for default value shows. Otherwise, value will be overwritten by the default value.
        time.sleep(5)
        current_field.__setitem__('value', value)
    
    def fax_receive_settings_dualfax_set_rings_to_answer(self, value, line = "line1"):
        """
        Purpose: Set the rings to answer for dual fax
        :param line: line1/line2
        :return:
        """
        if line == "line1":
            ring_spinbox = (FaxAppWorkflowObjectIds.spinbox_line1ringsToAnswer)
        elif line == "line2":
            ring_spinbox = (FaxAppWorkflowObjectIds.spinbox_line2ringsToAnswer)
        else:
            raise ValueError("Invalid line specified. Use 'line1' or 'line2'.")

        ringer_combobox = self.spice.wait_for(FaxAppWorkflowObjectIds.combobox_ring_to_answer)
        ringer_combobox.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_ringtoanswer_dualfax)
        current_field = self.spice.wait_for(ring_spinbox)
        current_field.__setitem__('value', value)
        logging.info(f"Set rings to answer for {line} to {value}")
        logging.info("navigating back to receive settings screen")
        back_button_id = f"{FaxAppWorkflowObjectIds.view_ringtoanswer_dualfax} {FaxAppWorkflowObjectIds.button_back}"
        back_button = self.spice.wait_for(back_button_id)
        back_button.mouse_click()

    def fax_receive_verify_rings_to_answer(self, value):
        """
        verify the value of rings to answer
        :param value: value of rings to answer, 1/2/3/4/5/6
        :return:
        """
        current_field = self.spice.wait_for(FaxAppWorkflowObjectIds.spinbox_ringsToAnswer)
        actual_value = current_field["value"]
        assert value == actual_value, "value of rings to answer is unexpected"

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
        logging.info("At Home Screen")
        # TODO - Need to check the menu app is visible or not
        # check whether the menu is visible on the screen
        menuApp = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp)
        self.spice.wait_until(lambda: menuApp["visible"] == True)

    def verify_homescreen_fax_notconfigured_cancel(self):
        """
        Purpose: Navigates to Home screen from fax not configured screen
        Ui Flow: Any screen -> Main menu -> Fax app -> fax not configured screen -> Cancel -> Home
        :param spice: Takes 0 arguments
        :return: None
        """

        self.goto_fax_app()
        time.sleep(2)
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.view_faxNotConfiguredAlert)
        logging.info("At Fax not configured Screen")

        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxNotConfCancel)
        current_button.mouse_click()
        assert self.spice.wait_for("#HomeScreenView")

    def verify_fax_disabled_prompt(self):
        """
        Purpose: Navigates to Home screen from fax disabled screen
        Ui Flow: Any screen -> Main menu -> Fax app -> fax disabled screen -> Ok -> Home
        :param spice: Takes 0 arguments
        :return: None
        """
        self.goto_fax_app()
        time.sleep(2)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        logging.info("At Fax not enabled Screen")

        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()
        assert self.spice.wait_for("#HomeScreenView")

    def goto_fax_app(self):
        self.homeoperations.goto_home_fax()

    def fax_menu_navigation(self, button_object_id, expected_object_id, select_option: bool = True):
        """
        Purpose: method searches and clicks a specified button on a specified menu under fax settings
        Navigation: NA
        Args:
            button_object_id: Object Id of the button to be pressed
            expected_object_id: Object Id of the expected screen
            select_option: Select True to click on the element
        """

        try:
            current_button = self.spice.wait_for(button_object_id + " TextArea")
        except Exception as e:
            current_button = self.spice.wait_for(button_object_id + " SpiceText")
        current_button.mouse_click()
        self.spice.wait_for(expected_object_id, 5)
        logging.info("At Expected Menu")

    def fax_app_navigate_back(self, current_screen, expected_screen):
        """
        Purpose: Navigates one screen back from current screen
        Ui Flow: current screen -> back -> expected screen
        Args: current Screen Id, expected screen Id
        """
        cur_screen = self.spice.wait_for(current_screen)
        back_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
        back_button.mouse_click()
        self.spice.wait_for(expected_screen, 2)

    def back_to_fax_app_job_submission_view_from_options_view_with_close_button(self):
        '''
        From options view go back to fax job submission
        UI FLow is fax options view -> send fax view
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_back_close).mouse_click()

    def back_button_press(self, screen_id, landing_view, back_or_close_button, timeout_val: int = 10):
        """
        Press back button in specific screen.
        Args:
        screen_id: Screen object id
        timeout_val: Time out for scrolling
        landing_view: Landing screen after pressing back button
        """
        self.spice.wait_for(screen_id)
        if (self.spice.wait_for(back_or_close_button)["visible"] == True):
            # TODO verify the code once the back button is in position
            back_button = self.spice.wait_for(back_or_close_button)
            back_button.mouse_click()
            self.spice.wait_for(landing_view ,3)
            logging.info("At" +landing_view)

    def back_to_fax_send_job_submission_from_fax_send_job_options_screen_with_back_button(self):
        """
        Back to send job submission screen from send job options screen through back button.
        """
        logging.info("Go back to send job submission screen from fax send option screen with back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_optionsScreen, landing_view = FaxAppWorkflowObjectIds.view_faxSendRecipientScreen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_fax_send_job_submission_from_fax_send_job_options_screen_with_close_button(self):
        """
        Back to send job submission screen from send job options screen through close button.
        """
        logging.info("Go back to send job submission screen from fax send option screen with back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_optionsScreen, landing_view = FaxAppWorkflowObjectIds.view_faxSendRecipientScreen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.button_back_close}')
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def back_to_fax_send_settings_from_fax_dialing_screen_with_back_button(self):
        """
        Back to fax send settings screen from fax dialing screen through back button.
        """
        logging.info("Go back to fax send settings screen from fax dialing screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.fax_dialing_menu_list, landing_view = FaxAppWorkflowObjectIds.fax_send_menu_list, back_or_close_button = f'{FaxAppWorkflowObjectIds.fax_dialing_menu_list} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_fax_settings_from_fax_send_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax sending screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.fax_send_menu_list, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings, back_or_close_button = f'{FaxAppWorkflowObjectIds.fax_send_menu_list} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_fax_settings_from_fax_receive_settings_screen_with_back_button(self):
        """
        Back to fax settings screen from fax receive settings screen through back button.
        """
        logging.info("Go back to fax settings screen from fax receive settings screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, landing_view = FaxAppWorkflowObjectIds.view_menu_fax_settings, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_settings_from_fax_settings_screen_with_back_button(self):
        """
        Back to settings screen from fax settings screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_menu_fax_settings, landing_view = FaxAppWorkflowObjectIds.view_menu_settings_screen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_menu_fax_settings} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_addressbook_local_from_local_select_screen_with_back_button(self):
        """
        Back to Address Book Local screen from local select screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen, landing_view = FaxAppWorkflowObjectIds.view_FaxAddressBookScreen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_faxsendtocontacts_from_addressbook_local_screen_with_close_button(self):
        """
        Back to fax send to contacts screen from Address Book Local screen through back button.
        """
        logging.info("Go back to fax settings screen from fax sending screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_FaxAddressBookScreen, landing_view = FaxAppWorkflowObjectIds.view_faxSendRecipientScreen, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_FaxAddressBookScreen} {FaxAppWorkflowObjectIds.button_back_close_addressBook}')

    def back_to_fax_app_fax_setup_from_basic_fax_setup_with_back_button(self):
        """
        Back to Fax Setup view from Basic Fax Setup view via back button.
        Flow should in Fax App setup -- Basic Fax Setup view
        """
        logging.info("Go back from Basic Fax Setup view")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.menuText_basicFaxSetup, landing_view = FaxAppWorkflowObjectIds.view_fax_setup_checking_screen, back_or_close_button = f'{FaxAppWorkflowObjectIds.menuText_basicFaxSetup} {FaxAppWorkflowObjectIds.button_back}')

    def back_to_select_contact_from_search_contact_screen_with_close_button(self):
        """
        Back to select fax contacts screen from Search contact screen through close button.
        """
        logging.info("Go back to select fax contact screen from search contact screen through close button")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.view_faxSearchContactScreen, landing_view = FaxAppWorkflowObjectIds.view_fax_contacts_integration, back_or_close_button = f'{FaxAppWorkflowObjectIds.view_faxSearchContactScreen} {FaxAppWorkflowObjectIds.button_faxAddressbook_name_cancel}')

    def goto_fax_app_recipient_screen(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen
        Args: None
        """

        self.goto_fax_app()
        self.click_skip_button()
        time.sleep(5)

    def goto_fax_app_recipient_screen_with_setup(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Basic Fax Setup -> Fax Recipients screen
        Args: None
        """
        self.goto_fax_app_screen()
        time.sleep(5)
        
    def goto_fax_phone_line_in_use_view(self):
        """
        Go to fax phone line in use screen when hook state is off
        """

        self.goto_fax_app()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_offhook_phoneline)

    def receive_manual_fax(self,net):
        """
        Perform receive manual fax when hook state is off
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_offhook_phoneline)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_phoneline_button)
        current_button.mouse_click()

        assert self.spice.query_item(FaxAppWorkflowObjectIds.fax_receive_phoneline_button, 0)["enabled"] == False
        self.wait_for_fax_job_status_toast(net,message="Receive")
        time.sleep(10)
        assert self.spice.query_item(FaxAppWorkflowObjectIds.fax_receive_phoneline_button, 0)["enabled"] == True

    def click_cancel_button_on_fax_confirmation_screen(self):
        """
        Click cancel button on fax confirmation screen
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxCancel)
        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def click_ok_button_on_atleast_one_recipient_alert_screen(self):
        """
        Click ok button on Atleast One Recipient Alert Screen
        """
        button_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
        button_ok.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

        logging.info("Click ok button on Atleast One Recipient Alert Screen")

    def click_skip_button(self):
        """
        Click Skip button
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetupSkip)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen, 5)
        logging.info("At Fax send recipient screen Menu")

    def goto_fax_app_recipient_screen_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Sent to Contacts
        Args: None
        """
        self.goto_fax_app()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)

    def fax_app_send_or_cancel_no_contacts(self, yes_no: str = "No"):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app and enters fax
        number if user selects "Yes" and Cancel fax when user select "No"
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts ->
            If "Yes" Enter fax Num
            If "No" navigated back to fax recipient.
        Args: Yes/No
        """
        # Currently for workflow ui doesn't support FaxSend_NoContactsAvailable screen. So cannot test select Yes or no scenario
        #Ajin: Fax Send flow>Enter fax number>Select contacts icon>Select Local address Book>Empty address book display with Cencel and Select button>Implement for Cancel and Select..On Select press, error message>Ok
        self.goto_fax_without_skip_button()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        if yes_no == 'No':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_cancel)
            current_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
            current_button.mouse_click()
            logging.info("verify the error message")
            time.sleep(2)
            error_msg = self.spice.wait_for(FaxAppWorkflowObjectIds.faxAddressbook_select_error_msg + ' SpiceText[visible=true]')["text"]
            assert error_msg == 'Select at least one member to proceed.', 'Error message mismatch'
            logging.info("Then click ok button")
            button_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
            button_ok.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)

    def goto_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_recipient_screen()
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        
        #self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_faxEnterFaxNumber, FaxAppWorkflowObjectIds.faxNumberKeyboard)
   
    def goto_fax_app_screen_enter_fax_number(self):

        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app()
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)

    def enter_fax_number_fax_recipient_screen(self):

        """
        Purpose: Enter fax number in fax recipients
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: None
        """
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
   
    def goto_fax_app_screen(self):
        """
        Purpose: Navigates from home screen to fax recipient selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen
        Args: None
        """
        self.goto_fax_without_skip_button()

    def goto_fax_without_skip_button(self):
        """
        Purpose: Navigates to Fax app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Fax app -> Basic fax setup -> fax recipients screen
        :param spice: Takes 0 arguments
        :return: None
        """

        self.goto_fax_app()
        time.sleep(5)
        logging.info("At Fax Screen")

    def goto_fax_app_fax_setup_phone_line_details(self):
        """
        Purpose: Click Next button on Basic Fax Setup View
        Ui Flow in Main Menu - Fax - Continue - Basic Fax Setup -> Next -> Phoneline details view
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        logging.info("Click next button")
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_basicFaxSetupNext).mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupLineShareScreen)
        logging.info("At Phone Line Share screen")

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
        network_instance = Network(cdm.ipaddress)
        print("fax instance created successfully")
        fax_instance.check_modem_status()
        trace_log('========== RECEIVE FAX config setup ==========')
        fax_instance.set_receive_fax_config(stampReceivedFax=stampReceivedFax, faxPrintingSchedule=faxPrintingSchedule)
        if(blockedFaxNumber != ""):
            fax_instance.create_receive_fax_blocked_number(blockedFaxNumber)

        fax_instance.update_receive_fax_ticket(**payLoad)
        trace_log('========== RECEIVE FAX Job Started ==========')
        max_wait_time = waitTime

        # name mangling
        fax_instance._Fax__receive_fax(faxSimIP)

        if cancel == Cancel.not_answer:
            logging.info("Trigger fax receive job only, user can reject the job by clicking Ignore")
            return

        if auto_answer == "No":
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveStateScreen, timeout=9.0)
            
            self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
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
            self.wait_for_fax_job_status_toast(network_instance,"Fax Cancelled", 100)
        else:
            fax_instance._job.check_job_state(job_id, 'processing', max_wait_time)
            print('started processing the fax receive job..')
            self.wait_for_fax_job_status_toast(network_instance,"Receive", 90)

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
        Ui Flow: Basic Fax Setup screen -> Next -> Phoneline share view
        Args: None
        """
        current_view = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        self.spice.wait_until(lambda:current_view["visible"])
        logging.info("Click next button")
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_basicFaxSetupNext).mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupLineShareScreen)
        logging.info("At Phone Line Share screen")

    def goto_fax_setup_change_country(self):
        """
        Purpose: Navigates from Basic fax setup screen to Country/Location selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Country/Location Selection view
        Args: None
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_setup_country_change_button)
        current_button.mouse_click()

    def fax_setup_select_country(self, country: str = None, fax_mode=FaxModemType.dungeness_bbu_modem.value):
        """
        :param spice: None
        :param country: Indonesia= "ID", Hong Kong S.A.R.="HK", South Korea="KR", Malaysia="MY",Philippines:"PH",Singapore ="SG"
        Sri Lanka = "LK", Thailand="TH", Vietnam ="VN"
        :return:
        """

        country_name = ""
        if country == "ID":
            country_name = "Indonesia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_id
        elif country == "HK":
            country_name = "Hong Kong SAR"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hk
        elif country == "KR":
            country_name = "South Korea"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_kr
        elif country == "MY":
            country_name = "Malaysia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_my
        elif country == "PH":
            country_name = "Philippines"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ph
        elif country == "SG":
            country_name = "Singapore"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sg
        elif country == "LK":
            country_name = "Sri Lanka"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lk
        elif country == "TH":
            country_name = "Thailand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_th
        elif country == "VN":
            country_name = "Vietnam"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_vn
        elif country == "AR":
            country_name = "Argentina"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ar
        elif country == "AU":
            country_name = "Australia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_au
        elif country == "BR":
            country_name = "Brazil"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_br
        elif country == "CA":
            country_name = "Canada"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ca
        elif country == "CL":
            country_name = "Chile"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cl
        elif country == "CN":
            country_name = "China"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cn
        elif country == "IN":
            country_name = "India"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_in
        elif country == "JP":
            country_name = "Japan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_jp
        elif country == "MX":
            country_name = "Mexico"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_mx
        elif country == "NZ":
            country_name = "NewZealand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nz
        elif country == "PK":
            country_name = "Pakistan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pk
        elif country == "PE":
            country_name = "Peru"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pe
        elif country == "TW":
            country_name = "TaiwanRegion"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tw
        elif country == "US":
            country_name = "UnitedStates"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_us
        elif country == "AT":
            country_name = "Austria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_at
        elif country == "BY":
            country_name = "Belarus"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_by
        elif country == "BE":
            country_name = "Belgium"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_be
        elif country == "BG":
            country_name = "Bulgaria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_bg
        elif country == "HR":
            country_name = "Croatia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hr
        elif country == "CZ":
            country_name = "CzechRepublic"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cz
        elif country == "DK":
            country_name = "Denmark"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_dk
        elif country == "EE":
            country_name = "Estonia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ee
        elif country == "FI":
            country_name = "Finland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fi
        elif country == "FR":
            country_name = "France"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fr
        elif country == "DE":
            country_name = "Germany"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_de
        elif country == "GR":
            country_name = "Greece"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gr
        elif country == "HU":
            country_name = "Hungary"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hu
        elif country == "IS":
            country_name = "Iceland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_is
        elif country == "IE":
            country_name = "Ireland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ie
        elif country == "IL":
            country_name = "Israel"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_il
        elif country == "IT":
            country_name = "Italy"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_it
        elif country == "LV":
            country_name = "Latvia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lv
        elif country == "LI":
            country_name = "Liechtenstein"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_li
        elif country == "LT":
            country_name = "Lithuania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lt
        elif country == "LU":
            country_name = "Luxembourg"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lu
        elif country == "MA":
            country_name = "Morocco"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ma
        elif country == "NL":
            country_name = "Netherlands"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nl
        elif country == "NO":
            country_name = "Norway"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_no
        elif country == "PL":
            country_name = "Poland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pl
        elif country == "PT":
            country_name = "Portugal"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pt
        elif country == "RO":
            country_name = "Romania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ro
        elif country == "RU":
            country_name = "Russia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ru
        elif country == "SK":
            country_name = "Slovakia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sk
        elif country == "SI":
            country_name = "Slovenia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_si
        elif country == "ZA":
            country_name = "SouthAfrica"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_za
        elif country == "ES":
            country_name = "Spain"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_es
        elif country == "SE":
            country_name = "Sweden"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_se
        elif country == "CH":
            country_name = "Switzerland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ch
        elif country == "TR":
            country_name = "Turkey"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tr
        elif country == "UA":
            country_name = "Ukraine"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ua
        elif country == "GB":
            country_name = "UnitedKingdom"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gb
        else:
            raise logging.info(f"Trying to select country name:{country} is not supported to set,"
                               f"Choose proper country name")
        logging.info(f"Need to set the country_name to <{country_name}>")
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode])
        self.workflow_common_operations.goto_item(country_region_locator,FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode],select_option=False,scrolling_value=0.01,scrollbar_objectname=FaxAppWorkflowObjectIds.fax_countrylist_scrollbar[fax_mode])
        time.sleep(5)
        country_button = self.spice.wait_for(country_region_locator)
        country_button.mouse_click()
        time.sleep(5)

        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_change_country)
        ok_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.setup_location_view)

    def wait_for_location_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        next_button = self.spice.wait_for(FaxAppWorkflowObjectIds.location_next_button)
        next_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.setup_header_name_view,timeout=15)


    def goto_cancel_confirmation_from_location(self):
        """
        Purpose:Click on the Cancel button from location and verify cancel confirmation dialog
        :return:
        """
        cancel_button = self.spice.wait_for(FaxAppWorkflowObjectIds.location_cancel_button)
        cancel_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.cancel_confirmation_view)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.cancel_confirmation_ok_button)
        ok_button.mouse_click()

    def wait_for_faxnumber_headername_previous_button_click(self):
        """
        Purpose:Wait for until Previous button object present
        :return:
        """
        previous_button = self.spice.wait_for(FaxAppWorkflowObjectIds.faxNumber_previous_button)
        previous_button.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.setup_location_view)


    def fax_setup_add_header_name(self, name: str):
        """
        Set the value of Fax header name based on user input using alphanumeric keyboard
        Args: name: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_header_name_view,timeout=15)
        sleep(1)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupFaxHeaderName, FaxAppWorkflowObjectIds.input_enterFaxHeaderName, True)
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.input_enterFaxHeaderName,timeout=15)
        current_screen.mouse_click()
        current_screen.__setitem__('displayText', name)
        current_screen.mouse_click()
        key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.KeyOK_two)
        key_Ok.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_header_name_view)

    def fax_setup_add_fax_number(self, number):
        """
        Set the value of Fax number based on user input using alphanumeric keyboard
        Args: number: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_faxnumber_view)
        sleep(1)
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #TextInputBox")
        current_screen.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        num_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key123)
        num_button.mouse_click()
        # clear fax number text before input number.
        while self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #Image")["visible"] == True:
            back_space_key_button = self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #Image")
            back_space_key_button.mouse_click()
        self.enter_numeric_keyboard_values(number, OK_locator=FaxAppWorkflowObjectIds.KeyOK_two)
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_faxnumber_view)
        logging.info("Move the scroll bar to top.")

    def wait_for_faxnumber_headername_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        next_button = self.spice.wait_for(FaxAppWorkflowObjectIds.faxNumber_next_button)
        next_button.mouse_click()

    def verify_constraint_message_faxnumber_headername_not_configured(self):
        """
        Purpose:Verify constraint message when fax number and header name not configured
        :return:
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

    def wait_for_dialing_prefix_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        next_button = self.spice.wait_for(FaxAppWorkflowObjectIds.dialing_prefix_next_button)
        next_button.mouse_click()

    def wait_for_finish_button(self):
        """
        Purpose:Wait for until finish button object present
        :return:
        """
        finish_button = self.spice.wait_for(FaxAppWorkflowObjectIds.finish_summary_button)
        finish_button.mouse_click()

    def verify_setup_summary(self, country, expect_faxnumber, expect_hedername, expect_dialingprefix):
        """
        Purpose:Verify values in summary screen
        :return:
        """
        country_name = ""
        if country == "ID":
            country_name = "Indonesia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_id
        elif country == "HK":
            country_name = "Hong Kong SAR"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hk
        elif country == "KR":
            country_name = "South Korea"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_kr
        elif country == "MY":
            country_name = "Malaysia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_my
        elif country == "PH":
            country_name = "Philippines"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ph
        elif country == "SG":
            country_name = "Singapore"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sg
        elif country == "LK":
            country_name = "Sri Lanka"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lk
        elif country == "TH":
            country_name = "Thailand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_th
        elif country == "VN":
            country_name = "Vietnam"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_vn
        elif country == "AR":
            country_name = "Argentina"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ar
        elif country == "AU":
            country_name = "Australia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_au
        elif country == "BR":
            country_name = "Brazil"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_br
        elif country == "CA":
            country_name = "Canada"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ca
        elif country == "CL":
            country_name = "Chile"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cl
        elif country == "CN":
            country_name = "China"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cn
        elif country == "IN":
            country_name = "India"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_in
        elif country == "JP":
            country_name = "Japan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_jp
        elif country == "MX":
            country_name = "Mexico"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_mx
        elif country == "NZ":
            country_name = "NewZealand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nz
        elif country == "PK":
            country_name = "Pakistan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pk
        elif country == "PE":
            country_name = "Peru"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pe
        elif country == "TW":
            country_name = "TaiwanRegion"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tw
        elif country == "US":
            country_name = "UnitedStates"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_us
        elif country == "AT":
            country_name = "Austria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_at
        elif country == "BY":
            country_name = "Belarus"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_by
        elif country == "BE":
            country_name = "Belgium"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_be
        elif country == "BG":
            country_name = "Bulgaria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_bg
        elif country == "HR":
            country_name = "Croatia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hr
        elif country == "CZ":
            country_name = "CzechRepublic"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cz
        elif country == "DK":
            country_name = "Denmark"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_dk
        elif country == "EE":
            country_name = "Estonia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ee
        elif country == "FI":
            country_name = "Finland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fi
        elif country == "FR":
            country_name = "France"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fr
        elif country == "DE":
            country_name = "Germany"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_de
        elif country == "GR":
            country_name = "Greece"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gr
        elif country == "HU":
            country_name = "Hungary"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hu
        elif country == "IS":
            country_name = "Iceland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_is
        elif country == "IE":
            country_name = "Ireland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ie
        elif country == "IL":
            country_name = "Israel"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_il
        elif country == "IT":
            country_name = "Italy"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_it
        elif country == "LV":
            country_name = "Latvia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lv
        elif country == "LI":
            country_name = "Liechtenstein"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_li
        elif country == "LT":
            country_name = "Lithuania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lt
        elif country == "LU":
            country_name = "Luxembourg"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lu
        elif country == "MA":
            country_name = "Morocco"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ma
        elif country == "NL":
            country_name = "Netherlands"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nl
        elif country == "NO":
            country_name = "Norway"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_no
        elif country == "PL":
            country_name = "Poland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pl
        elif country == "PT":
            country_name = "Portugal"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pt
        elif country == "RO":
            country_name = "Romania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ro
        elif country == "RU":
            country_name = "Russia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ru
        elif country == "SK":
            country_name = "Slovakia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sk
        elif country == "SI":
            country_name = "Slovenia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_si
        elif country == "ZA":
            country_name = "SouthAfrica"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_za
        elif country == "ES":
            country_name = "Spain"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_es
        elif country == "SE":
            country_name = "Sweden"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_se
        elif country == "CH":
            country_name = "Switzerland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ch
        elif country == "TR":
            country_name = "Turkey"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tr
        elif country == "UA":
            country_name = "Ukraine"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ua
        elif country == "GB":
            country_name = "United Kingdom"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gb
        else:
            raise logging.info(f"Trying to select country name:{country} is not supported to set,"
                               f"Choose proper country name")
        logging.info(f"Need to set the country_name to <{country_name}>")

        self.spice.wait_for(FaxAppWorkflowObjectIds.location_summary)
        current_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.location_summary} #contentItem")["text"]
        assert country_name == current_text, "Location value is incorrect"

        self.spice.wait_for(FaxAppWorkflowObjectIds.faxnumber_summary)
        current_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.faxnumber_summary} #contentItem")["text"]
        assert expect_faxnumber == current_text, "Fax number value is incorrect"

        self.spice.wait_for(FaxAppWorkflowObjectIds.headername_summary)
        current_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.headername_summary} #contentItem")["text"]
        assert expect_hedername == current_text, "Header Name value is incorrect"

        self.spice.wait_for(FaxAppWorkflowObjectIds.dialing_prefix_summary)
        current_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.dialing_prefix_summary} #contentItem")["text"]
        assert expect_dialingprefix == current_text, "Dialing prefix value is incorrect"

    def goto_menu_fax_faxsetup_enterprise(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.location_LeftPanel)
        location_left_panel = self.spice.wait_for(FaxAppWorkflowObjectIds.location_LeftPanel)
        location_left_panel.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_location_view)

    def goto_fax_settings(self):
        """
        Purpose: Navigates from home menu settings to fax settings screen
        Ui Flow: Menu -> Settings -> Fax Settings
        Args: None
        """
        self.spice.goto_homescreen()
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.view_menu_fax_settings,scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        logging.info("At Fax Settings Screen")
              
    def goto_menu_fax_dualline1_faxsetup_enterprise(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        #self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.location_LeftPanel)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.menuText_FaxSetup)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupMenuLine1)
        current_button.mouse_click()
        location_left_panel = self.spice.wait_for(FaxAppWorkflowObjectIds.location_LeftPanel)
        location_left_panel.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_location_view)

    def goto_faxsetup_from_notconfigured_screen(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Home -> Fax -> Not Configured -> Fax Setup in enterprise
        Args: None
        """

        self.goto_fax_app()
        time.sleep(2)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_faxNotConfiguredAlert, timeout=20)
        assert  self.spice.wait_for(MenuAppWorkflowObjectIds.view_faxNotConfiguredAlert)
        logging.info("At Fax not configured Screen")

        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfigure)
        current_button.mouse_click()
        location_left_panel = self.spice.wait_for(FaxAppWorkflowObjectIds.location_LeftPanel)
        location_left_panel.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_location_view)

    def fax_setup_add_dialing_prefix(self, prefix, index_val=0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_dialing_prefix_view)
        sleep(1)
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.dialing_prefix_TextField)
        # to check if alredy has prefix
        try:
            self.spice.wait_for(f"{FaxAppWorkflowObjectIds.dialing_prefix_TextField} {FaxAppWorkflowObjectIds.item_in_text_field_dialing_prefix}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        
        time.sleep(1)
        self.enter_numeric_keyboard_values(prefix)
        self.spice.wait_for(FaxAppWorkflowObjectIds.setup_dialing_prefix_view)

    def goto_fax_settings_fax_setup_country_location(self, fax_mode=FaxModemType.dungeness_bbu_modem.value):

        """
        Purpose: Navigates from Basic fax setup screen to Country/Location selection screen in fax settings
        Ui Flow: Basic Fax Setup screen -> Country/Location Selection view
        Args: None
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_setup_countryopt)
        current_button.mouse_click()

        
    def goto_fax_app_recipient_screen_after_set_basic_fax_settings(self):
        """
        Purpose: Navigates to Fax recipients screen without handling basic setup screen from any other screen
        Ui Flow: Any screen -> Main menu -> Fax app ->Fax Recipient screen
        :param spice: Takes 0 arguments
        :return: None
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_fax , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item, delta = 0.1)
        current_button = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax + " MouseArea")
        current_button.mouse_click()
        time.sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)


    def goto_fax_app_fax_setup_country_location(self, fax_modem=FaxModemType.dungeness_bbu_modem.value):
        """
        Purpose: Navigates from home screen to Country/Location selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Country/Location Selection view
        Args: None
        """
        self.goto_fax_app_fax_setup()
        if fax_modem == FaxModemType.crawdad_aabrazil.value:
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.basic_setup_country_region, FaxAppWorkflowObjectIds.country_region_popup_list[FaxModemType.crawdad_aabrazil.value])
        elif fax_modem == FaxModemType.dungeness_bbu_modem.value:
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.basic_setup_country_region, FaxAppWorkflowObjectIds.country_region_popup_list[FaxModemType.dungeness_bbu_modem.value])
        elif fax_modem == FaxModemType.dungeness_worldwide_modem.value:
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.basic_setup_country_region, FaxAppWorkflowObjectIds.country_region_popup_list[FaxModemType.dungeness_worldwide_modem.value])
        else:
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.basic_setup_country_region, FaxAppWorkflowObjectIds.country_region_popup_list[FaxModemType.dungeness_bbu_modem.value])

    def goto_fax_app_fax_setup_dial_type(self):
        """
        Purpose: Navigates from home screen to dial type selection in phoneline screen of fax app
        Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup -> Next -> Phoneline details view -> dial type
        Args: None
        """
        pass
        # Cannot get Phoneline details view in WF UI.

    def goto_fax_app_fax_options(self):
        """
        Purpose: Navigates to fax options screen from job submission page
        Ui Flow: fax job Submission screen -> Fax Options
        Args: None
        """
     
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_allOptions)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)

    def get_fax_options_original_sides_value(self):
        '''
        Get the original sides value
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
        current_side_value = self.spice.query_item(f"{FaxAppWorkflowObjectIds.combo_box_2sidedOriginal} {FaxAppWorkflowObjectIds.content_item}")['text']
        logging.info(f"Current original sides value: {current_side_value}")
        return current_side_value

    def set_fax_options_orininal_sides_non_default_value(self, net):
        '''
        According to current original sides value, set to another value.
        '''
        current_side_value = self.get_fax_options_original_sides_value()
        text_1_sides = LocalizationHelper.get_string_translation(net, "c1Sided")
        if current_side_value == text_1_sides:
            self.fax_app_set_two_sided_original_value(value=True)
        else:
            self.fax_app_set_two_sided_original_value(value=False)
    
    def close_fax_options(self):
        '''
        Click close button of Fax Options page
        '''
        logging.info("Close fax options")
        self.spice.fax_ui().back_button_press(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen, FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen, FaxAppWorkflowObjectIds.button_back_close)

    def goto_fax_options_fax_settings(self):
        """
        Purpose: Navigates to fax send settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings
        Args: None
        """
        # There is no Settings section Present for Fax options Settings screen for WF ui

       
        

    def goto_fax_options_send_settings_fax_dialing(self):
        """
        Purpose: Navigates to fax dialing settings screen from job submission page
        Ui Flow: dax job Submission screen -> Fax Options -> Fax send settings -> Fax dialing Settings
        Args: None
        """
        # There is no Settings for Fax dialing Present for Fax options Settings screen for WF ui
        # Use Settings-> Fax Sending Setting -> Fax Dialing for this method
        self.goto_menu_fax_send_settings_dialing()        


    def fax_app_enter_fax_number_confirm(self, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number in enter fax number screen and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        
        self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_numeric_keyboard_values("123")                         # Todo add logic to handle multiple fax numbers

        if confirm_fax_number:
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfirm)
            current_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
            key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
            key_Ok.mouse_click() 
            
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        
        
    def fax_app_set_auto_two_sided_original_value(self, value: str = "Auto"):
        """
        Purpose: Selects Auto, 1-sided, 2-Sided Original based on user input,When Auto is Selected 2-sided is enabled.
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_object_OriginalSides,FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View)
        if value == "Auto":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesAuto_option)
            current_button.mouse_click()
            sleep(2)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesAuto_option)["checked"] == True, "Auto option checked"
            logging.info("TwoSidedOriginal value is : %s" %value)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesDuplex_option)["enabled"] == True, "row_originalSidesDuplex_option is not enabled"
            #assert self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesDuplex_option)["checked"] == True
        elif value == "1-Sided":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesSimplex_option)
            current_button.mouse_click()
            logging.info("TwoSidedOriginal value is : %s" %value)
        elif value == "2-Sided":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesDuplex_option)
            current_button.mouse_click()
            logging.info("TwoSidedOriginal value is : %s" %value)
        back_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View + " " + FaxAppWorkflowObjectIds.backbutton)
        back_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)

    def fax_app_set_auto_two_sided_original_value_check_constraints(self):
        """
        Purpose: Selects Auto, 1-sided, 2-Sided Original based on user input,When Auto is Selected 2-sided is enabled.
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_object_OriginalSides,FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.row_originalSidesSimplex_option)
        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View)
        back_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View + " " + FaxAppWorkflowObjectIds.backbutton)
        back_button.mouse_click()

    def fax_app_set_two_sided_original_value(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Original based on user input
        Args: value: True = 2-Sided Original on, False = 2-Sided Original off: Bool
        """
        # Verify the option 2Sided Original is visible or not
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        if self.configuration.productname in ["citrine","jasper","moonstone","pearl","bell","curie"]:
            self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_object_OriginalSides,FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View)
            if value == True:
                sides = "duplex"
            else:
                sides = "simplex"
            sides_id = FaxAppWorkflowObjectIds.original_sides_custom_dict[sides][1]
            self.workflow_common_operations.goto_item(sides_id, FaxAppWorkflowObjectIds.fax_options_OriginalSides_View,
                                                      scrollbar_objectname=FaxAppWorkflowObjectIds.scrollbar_original_sides_View)
            back_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_options_OriginalSides_View + " " + FaxAppWorkflowObjectIds.backbutton)
            back_button.mouse_click()
        else:
            menu_item_id = [FaxAppWorkflowObjectIds.combo_box_row_2sidedOriginal, FaxAppWorkflowObjectIds.combo_box_2sidedOriginal]
            self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
            original_sided_dict = {
            "1-Sided": FaxAppWorkflowObjectIds.combo_box_options_simplex,
            "2-Sided": FaxAppWorkflowObjectIds.combo_box_options_duplex
            }
            if value == True:
                dic_value = "2-Sided"
                item_select = original_sided_dict.get(dic_value)
                current_button = self.spice.wait_for(item_select)
                current_button.mouse_click()
                logging.info("TwoSidedOriginal value is : %s" %dic_value)
            else:
                dic_value = "1-Sided"
                item_select = original_sided_dict.get(dic_value)
                current_button = self.spice.wait_for(item_select)
                current_button.mouse_click()
                logging.info("TwoSidedOriginal value is : %s" %dic_value)
    
    def fax_app_set_two_sided_scan_format(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Scan format based on user input
        Args: value: True = 2-Sided format flip-style, False = 2-Sided format book-style: Bool
        """
        # Verify the option 2Sided format is visible or not
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        select_format = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_twosided_settings_format)
        select_format.mouse_click()

        if value == False:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_book_style)
            current_button.mouse_click()
        elif value == True:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_flip_style)
            current_button.mouse_click()
        else:
            raise logging.info(f"{select_format} is not supported to select")

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)

    def fax_app_set_two_sided_scan_format_check_constraints(self):
        """
        Purpose: Selects 2-Sided Scan format based on user input
        Args: value: True = 2-Sided format flip-style, False = 2-Sided format book-style: Bool
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        select_format = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_twosided_settings_format)
        select_format.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)

        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(3)
    
    def set_two_sided_original_value_in_landing_view(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Original based on user input in fax landing view
        Args: value: True = 2-Sided Original on, False = 2-Sided Original off: Bool
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen, FaxAppWorkflowObjectIds.combo_box_row_2sidedOriginal, select_option=False, footer_item_id=FaxAppWorkflowObjectIds.footer_view, top_item_id=FaxAppWorkflowObjectIds.fax_option_header_setion)
        two_sided_original_option = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen} {FaxAppWorkflowObjectIds.combo_box_2sidedOriginal}")
        two_sided_original_option.mouse_click()

        original_sided_dict = {
            "1-Sided": FaxAppWorkflowObjectIds.combo_box_options_simplex,
            "2-Sided": FaxAppWorkflowObjectIds.combo_box_options_duplex
        }
        if value == True:
            dic_value = "2-Sided"
            item_select = original_sided_dict.get(dic_value)
            current_button = self.spice.wait_for(item_select)    
            current_button.mouse_click()
            logging.info("TwoSidedOriginal value is : %s" %dic_value)
        else:
            dic_value = "1-Sided"
            item_select = original_sided_dict.get(dic_value)
            current_button = self.spice.wait_for(item_select)    
            current_button.mouse_click()
            logging.info("TwoSidedOriginal value is : %s" %dic_value)
        
    
    def fax_options_set_resolution(self, resolution: str):
        """
        Purpose: Selects fax send resolution based on user input in fax options in settings
        Args: resolution: Standard, Fine, Superfine
        """
        
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        menu_item_id = [FaxAppWorkflowObjectIds.row_object_resolution, FaxAppWorkflowObjectIds.combo_box_resolution ]
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_resolutionListScreen, timeout=9.0)
        resolution_option_dict = {           
            "Standard": FaxAppWorkflowObjectIds.combo_resolution_option_Standrad,            
            "Fine": FaxAppWorkflowObjectIds.combo_resolution_option_Fine,            
            "Superfine": FaxAppWorkflowObjectIds.combo_resolution_option_Superfine           
        }   
        item_select = resolution_option_dict.get(resolution)       
        current_button = self.spice.wait_for(item_select)    
        current_button.mouse_click()
        
    def fax_options_lighter_darker_slider(self, value: int = 1):
        """
        Purpose: Selects fax lighter/Darker based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.slider_lighterDarker)
        while (self.spice.wait_for(FaxAppWorkflowObjectIds.slider_lighterDarker)["visible"] == False):
            current_screen.mouse_wheel(180, -180)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.slider_lighterDarker)["visible"] == True
        # self.set_sliderValue(self.lighter_darker_spice_slider, value)
        self.fax_set_slider_value("Lighter Darker", value)

    def fax_options_sharpness_slider(self, value: int = 1):
        """
        Purpose: Selects fax Sharpness based on user input in fax options in settings
        Args: value: accepts values 1-5: int
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.slider_sharpness)
        while (self.spice.wait_for(FaxAppWorkflowObjectIds.slider_sharpness)["visible"] == False):
            current_screen.mouse_wheel(180, -180)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.slider_sharpness)["visible"] == True
        self.fax_set_slider_value("Sharpness", value)

    def fax_options_contrast_slider(self, value: int = 1):
        """
        Purpose: Selects fax Contrast based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.slider_contrast)
        while (self.spice.wait_for(FaxAppWorkflowObjectIds.slider_contrast)["visible"] == False):
            current_screen.mouse_wheel(180, -180)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.slider_contrast)["visible"] == True
        self.fax_set_slider_value("Contrast", value)

    def fax_options_background_cleanup_slider(self, value: int = 1):
        """
        Purpose: Selects fax Background cleanup based on user input in fax options in settings
        Args: value: accepts values 1-9: int
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.slider_backgroundcleanup)
        while (self.spice.wait_for(FaxAppWorkflowObjectIds.slider_backgroundcleanup)["visible"] == False):
            current_screen.mouse_wheel(180, -180)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.slider_backgroundcleanup)["visible"] == True
        self.fax_set_slider_value("Background Cleanup", value)

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

    def check_content_type_value(self, contentType_option: str, net):
        """
        Check if the selected value is expected
        """
        contentType_Value = self.spice.wait_for(FaxAppWorkflowObjectIds.contentType_Value)
        self.spice.wait_until(lambda: contentType_Value["visible"] == True, timeout = 10.0)
        logging.info("The selected original size is " + contentType_Value['text'])
        expected_string = LocalizationHelper.get_string_translation(net, FaxAppWorkflowObjectIds.content_type_dict.get(contentType_option))
        assert contentType_Value['text'] == expected_string
        return contentType_Value['text']

    def goto_fax_option_original_size_screen(self):
        """
        Go to original size screen in fax options
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=FaxAppWorkflowObjectIds.view_optionsScreen,menu_item_id=FaxAppWorkflowObjectIds.list_faxSettings_originalSize,
            top_item_id=FaxAppWorkflowObjectIds.fax_option_header_section,select_option = True)
        time.sleep(5)
        original_size_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettings_originalSize)
        self.spice.wait_until(lambda: original_size_view["visible"] == True, timeout = 10.0)
        logging.info("at original size list screen")

    def fax_options_original_size(self, option):
        self.goto_fax_option_original_size_screen()
        time.sleep(5)
        to_select_item = self.original_size_option_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=FaxAppWorkflowObjectIds.view_faxSettings_originalSize,
            menu_item_id=to_select_item["row_id"],top_item_id=FaxAppWorkflowObjectIds.fax_option_header_section,select_option = True, scroll_step = 8)

    def check_original_size_option(self, option):
        to_select_item = self.original_size_option_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=FaxAppWorkflowObjectIds.view_faxSettings_originalSize,
            menu_item_id=to_select_item["row_id"],top_item_id=FaxAppWorkflowObjectIds.fax_option_header_section,select_option = False, scroll_step = 8)
        assert self.spice.wait_for(to_select_item["item_id"], timeout = 3.0)

    def fax_options_original_size_verify_constraint_message(self, option):
        self.goto_fax_option_original_size_screen()
        time.sleep(1)
        to_select_item = self.original_size_option_dict.get(option)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=FaxAppWorkflowObjectIds.view_faxSettings_originalSize,
            menu_item_id=to_select_item["row_id"],top_item_id=FaxAppWorkflowObjectIds.fax_option_header_section,select_option = False, scroll_step = 8)

        item = self.spice.wait_for(to_select_item["item_id"], timeout = 3.0)
        item.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

    def close_original_size_screen(self):
        backButton = self.spice.wait_for(FaxAppWorkflowObjectIds.original_size_back_button, timeout=4)
        backButton.mouse_click()

    def check_original_size_value(self, option, net):
        """
        Check if the selected value is expected
        """
        time.sleep(2)
        select_original_size = self.spice.wait_for(FaxAppWorkflowObjectIds.original_size_value)
        self.spice.wait_until(lambda: select_original_size["visible"] == True, timeout = 10.0)
        logging.info("The selected original size is " + select_original_size['text'])
        expected_string = LocalizationHelper.get_string_translation(net, self.original_dict[option][0])
        assert select_original_size['text'] == expected_string
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)

    def fax_options_content_orientation(self, orientation_option: str):
        """
        Select Content Orientation option from Fax -> Options
        Args: orientation_option: informative name for Landscape/Portrait
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        menu_item_id = [FaxAppWorkflowObjectIds.row_object_content_orientation, FaxAppWorkflowObjectIds.settings_content_orientation]
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_settings_orientation_screen, timeout=9.0)
        item_select = self.content_orientation_option_dict.get(orientation_option)
        self.workflow_common_operations.goto_item(item_select, FaxAppWorkflowObjectIds.view_settings_orientation_screen, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxDistinctiveringsOptionListScreen)

    def fax_options_blank_page_suppression(self, value: str):
        """
        Select Blank Page Suppression
        Args: value: Blank Page Suppression On/Off
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        menu_item_id = [FaxAppWorkflowObjectIds.row_object_scan_blank_page_suppression, FaxAppWorkflowObjectIds.combo_scan_blank_page_suppression]
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_can_blank_page_suppression_list, timeout=9.0)
        blank_page_suppression_option_dict = {
            "On": FaxAppWorkflowObjectIds.combo_blank_page_suppression_option_On,
            "Off": FaxAppWorkflowObjectIds.combo_blank_page_suppression_option_Off,
        }
        item_select = blank_page_suppression_option_dict.get(value)
        # scroll_item_into_view doesn't work for menu selection
        self.workflow_common_operations.goto_item(item_select, FaxAppWorkflowObjectIds.view_can_blank_page_suppression_list, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxDistinctiveringsOptionListScreen)

    def fax_options_fax_line_selection(self, size: str):
        """
        Select Fax Line Selection option from Fax -> Options
        Args: size: informationative name for line, Auto/Line1/Line2
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        menu_item_id = [FaxAppWorkflowObjectIds.row_object_fax_line_selection, FaxAppWorkflowObjectIds.combo_fax_line]
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_line_list, timeout=9.0)
        fax_line_option_dict = {
            "Auto": FaxAppWorkflowObjectIds.combo_fax_line_option_auto,
            "Line1": FaxAppWorkflowObjectIds.combo_fax_line_option_line1,
            "Line2": FaxAppWorkflowObjectIds.combo_fax_line_option_line2
        }
        item_select = fax_line_option_dict.get(size)
        # scroll_item_into_view doesn't work for menu selection
        self.workflow_common_operations.goto_item(item_select, FaxAppWorkflowObjectIds.view_fax_line_list, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxDistinctiveringsOptionListScreen)

    def fax_options_fax_notification(self, value: str):
        """
        Select Fax Notification option from Fax -> Options
        Args: value: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])

        self._select_send_fax_notifications(value)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_send_notification)
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        while (self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == False):
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)
            current_button.mouse_click(10,10)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == True, 'Include Thumbnail is not checked'
        time.sleep(1)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        time.sleep(1)

    def fax_options_fax_notification_verify_constrained(self, value: str):
        """
        Select Fax Notification option from Fax -> Options and verify the constrained message
        Args: value: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option, FaxAppWorkflowObjectIds.view_optionsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions )
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])

        self._select_send_fax_notifications(value)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_send_notification)
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        time.sleep(1)
    
    def verify_fax_line2_notconfigured_constrained(self):
        """
        Click Ok on the fax line2 not configured constrained message
        @return:
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

    def fax_set_dialing_prefix(self, prefix, index_val=0):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.workflow_common_operations.scroll_to_position_vertical(0.7, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        # to check if alredy has prefix
        try:
            self.spice.wait_for(f"{FaxAppWorkflowObjectIds.text_field_dialing_prefix} {FaxAppWorkflowObjectIds.item_in_text_field_dialing_prefix}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        
        time.sleep(1)
        self.enter_numeric_keyboard_values(prefix)
        logging.info("Move the scroll bar.")
        self.workflow_common_operations.scroll_to_position_vertical(0.4, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
    
    def fax_set_dualfax_dialing_prefix(self, prefix, index_val=0, line="line1"):
        """
        Purpose: Set dialing prefix based on user input in fax dial settings
        Args: prefix: str
              line: str - "line1" or "line2", defaults to "line1"
        """
        # Set scrollbar based on line parameter
        if line.lower() == "line2":
            scrollbar = (FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2)
        elif line.lower() == "line1":
            scrollbar = (FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1)
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        self.spice.basic_common_operations.scroll_to_position_vertical(0.7, scrollbar_objectname=scrollbar)
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        # to check if alredy has prefix
       
        text_field.mouse_click()
        
        time.sleep(1)
        self.enter_numeric_keyboard_values(prefix)
        logging.info("Move the scroll bar.")
        self.workflow_common_operations.scroll_to_position_vertical(0.4, scrollbar_objectname=scrollbar)

    

    
    def check_dialing_prefix_unavailable(self, net):
        """
        Purpose: Check dialing prefix is unavailable under dialing prefix text
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        ui_body_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.text_field_dialing_prefix} {FaxAppWorkflowObjectIds.help_text_locator}")["text"]
        expect_text = LocalizationHelper.get_string_translation(net, "cUnavailable")
        logging.info(f"under dialing prefix text is: <{ui_body_text}>")
        assert ui_body_text == expect_text, "Check dialing prefix is unavailable failed"

    def fax_set_slider_value(self, slider_name, value: int = 1):
        """
        Purpose: Set slider values based on user input in fax options in settings
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup, Redial On Error, Redial On No Answer, Redial On Busy, Redial Interval
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
        elif slider_name == "Sharpness":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_sharpness
            slide_bar = FaxAppWorkflowObjectIds.slider_sharpness
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 5
        elif slider_name == "Contrast":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_contrast
            slide_bar = FaxAppWorkflowObjectIds.slider_contrast
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 9
        elif slider_name == "Background Cleanup":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_backgroundcleanup
            slide_bar = FaxAppWorkflowObjectIds.slider_backgroundcleanup
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
        self.workflow_common_operations.goto_item( menu_item_id , screen_name,  select_option = False, scrollbar_objectname = scrollbar )
        assert slider_min <= value <= slider_max, 'Value is out of range'
        slider_bar = self.spice.wait_for(slide_bar)
        slider_bar.__setitem__('value', value)
        new_value = self.spice.wait_for(slide_bar)["value"]        
        logging.info("Current Slider value is : %s" % new_value)
    
    def fax_dual_fax_set_slider_value(self, slider_name, value: int = 1,line: str = "line1"):
        """
        Purpose: Set slider values based on user input in fax options in settings
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup, Redial On Error, Redial On No Answer, Redial On Busy, Redial Interval
        """
        if line.lower() == "line2":
            scrollbar_objectid = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2
        elif line.lower() == "line1":
            scrollbar_objectid = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")

        slide_bar = ""
        slide_bar_row = ""
        screen_name = ""
        slider_min = 0
        slider_max = 0
        scrollbar = scrollbar_objectid
        if slider_name == "Redial On Error":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnError
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnError
            screen_name = FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list
            slider_min = 0
            slider_max = 9

        elif slider_name == "Redial on No Answer":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnNoAnswer
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnNoAnswer
            screen_name = FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list
            slider_min = 0
            slider_max = 2
        elif slider_name == "Redial On Busy":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialOnBusy
            slide_bar = FaxAppWorkflowObjectIds.slider_redialOnBusy
            screen_name = FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list
            slider_min = 0
            slider_max = 9
        elif slider_name == "Redial Interval":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_redialInterval
            slide_bar = FaxAppWorkflowObjectIds.slider_redialInterval
            screen_name =  FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list
            slider_min = 1
            slider_max = 5
        else:
            raise ValueError(f"Slider name '{slider_name}' is not supported for dual fax settings.")

        menu_item_id = [slide_bar_row, slide_bar] 
        self.workflow_common_operations.scroll_to_position_vertical(0.1, scrollbar)
        self.workflow_common_operations.goto_item( menu_item_id , screen_name,  select_option = False, scrollbar_objectname = scrollbar )
        assert slider_min <= value <= slider_max, 'Value is out of range'
        slider_bar = self.spice.wait_for(slide_bar)
        slider_bar.__setitem__('value', value)
        new_value = self.spice.wait_for(slide_bar)["value"]        
        logging.info("Current Slider value is : %s" % new_value)

    def verify_slider_current_value(self, slider_name, value: int = 1):
        """
        Purpose: Get slider values and compare it with specified value
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup
        """
        self.fax_get_slider_value(slider_name, value)

    def fax_get_slider_value(self, slider_name, value: int = 1):
        """
        Purpose: Get slider values and compare it with specified value
        Args: value: accepts values 1-9: int
              slider_name: Lighter Darker, Sharpness, Contrast, Background Cleanup
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
        elif slider_name == "Sharpness":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_sharpness
            slide_bar = FaxAppWorkflowObjectIds.slider_sharpness
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 5
        elif slider_name == "Contrast":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_contrast
            slide_bar = FaxAppWorkflowObjectIds.slider_contrast
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 9
        elif slider_name == "Background Cleanup":
            slide_bar_row = FaxAppWorkflowObjectIds.slider_row_backgroundcleanup
            slide_bar = FaxAppWorkflowObjectIds.slider_backgroundcleanup
            screen_name = FaxAppWorkflowObjectIds.view_optionsScreen
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxOptions
            slider_min = 1
            slider_max = 9

        menu_item_id = [slide_bar_row, slide_bar] 
        self.workflow_common_operations.goto_item( menu_item_id , screen_name,  select_option = False, scrollbar_objectname = scrollbar )
        assert slider_min <= value <= slider_max, 'Value is out of range'
        slider_bar = self.spice.wait_for(slide_bar)
        current_value = self.spice.wait_for(slide_bar)["value"]
        logging.info("Current Slider value is : %s" % current_value)
        assert current_value == value, 'Slider value is not matching'

    def wait_for_header(self):
        """
        Purpose:Wait for until header object present
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.input_enterFaxHeaderName)
           
    def wait_for_basic_fax_setup_fax_number(self):
        """
        Purpose:Wait for until Fax number object present
        :return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber)

    def wait_for_basic_fax_setup_next_button(self):
        """
        Purpose:Wait for until Next button object present
        :return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_basicFaxSetupNext)

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
        if distinctive_ring in ["All Standard Rings", "Double and Triple Rings", "Use Recorded Ring"]:
            scrollbar = self.spice.wait_for(FaxAppWorkflowObjectIds.distinctive_ring_menu_list_scrollbar)
            self.spice.wait_until(lambda:scrollbar["visible"]) 
            self.workflow_common_operations.scroll_to_position_vertical(0.3, FaxAppWorkflowObjectIds.distinctive_ring_menu_list_scrollbar)
        time.sleep(5)     
        current_button = self.spice.wait_for(menu_item_id)
        self.spice.wait_until(lambda:current_button["visible"])  
        logging.info(f"Select <{distinctive_ring}> and click the section to save the option")  
        current_button.mouse_click()
        time.sleep(1)

    def fax_distinctivering_record_verifycallmachine(self):
        """
        verify callmachine screen while recording distinctive ring screen
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctivering_callmachine)

    def fax_cancel_distinctivering_record(self):
        """
        cancel distinctive record while callmachine is in progress
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctivering_callmachine)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.distinctive_ring_callmachine_cancel, timeout=20)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_distinctiverecord_cancelscreen)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.distinctiveringrecord_cancelbutton, timeout=20)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctiveRingScreen)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
        current_button.mouse_click()

    def overwrite_record_distinctiver_ring(self):
        """
        proceeds with overwrite distinctive ring record
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_distinctivering_overwrite_proceed, timeout=30)
        current_button.mouse_click()
        self.fax_distinctivering_record_verifycallmachine()

    def overwrite_record_distinctive_ringcancel(self):
        """
        cancel record distinctive ring while overwrite
        """

        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_distinctivering_overwrite_cancel)
        current_button.mouse_click()
        curren_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctiveRingScreen)
        self.spice.wait_until(lambda:curren_view["visible"])
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
        current_button.mouse_click()

    def fax_distinctivering_verifyrecordedring_success(self):
        """
        verify distinctive ring recorded successfully
        """
        self.spice.wait_for("#faxSetupDistinctiveRingRecordComplete", timeout=15.0)
        current_button = self.spice.wait_for("#faxSetupDistinctiveRingRecordCompleteNextButton")
        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
        current_button.mouse_click()

    def fax_distinctivering_verifycallmachinetimeout(self,callmachinetimeoutoption):
        """
        verify timeoutscreen when callmachine failed
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.distinctivering_callmachine_timeoutretry,timeout=130)
        distinctivering_callmachine_dict = {
        "Retry": FaxAppWorkflowObjectIds.distinctivering_callmachine_timeoutretry,
        "Cancel": FaxAppWorkflowObjectIds.distinctivering_callmachine_timeoutcancel
        }
        menu_item_id = distinctivering_callmachine_dict.get(callmachinetimeoutoption)
        if callmachinetimeoutoption in ["Retry"]:
            current_button = self.spice.wait_for(menu_item_id)
            current_button.mouse_click()
            self.fax_distinctivering_record_verifycallmachine()

        if  callmachinetimeoutoption in ["Cancel"]:
            current_button = self.spice.wait_for(menu_item_id)
            current_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctiveRingScreen)
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
            current_button.mouse_click()

    
    def fax_basic_setup_alert_without_basic_details(self):
        """
        Purpose: Validate the error screen when basic setup details either any Country name,Header name or Fax number
        field empty
        :return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_basicFaxSetupNext, FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen, True)
        logging.info("Fax basic details enter alert pop up displayed")
        ok_btn = self.spice.wait_for(FaxAppWorkflowObjectIds.basic_fax_setup_required_ok_button)
        logging.info("Click OK button")
        ok_btn.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)

    def fax_app_add_editable_billing_code(self, fax_number, index_val=None):
        """
        Purpose: Enter editable billing code.
        Args: Index value: Stack 0 or 1 no need for workflow UI
        """
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.test_field_enterBillingCodeTextField)
        text_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_spicekeyboard)
        self.enter_fax_number_alphanumeric(fax_number)
        time.sleep(1)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.billing_code_ok_button)
        ok_button.mouse_click()

    def verify_billingcode_contraint(self,net):
        """
        verify contraint message when billing code is given blank
        """
        time.sleep(3)
        error_msg = self.spice.wait_for(FaxAppWorkflowObjectIds.faxAddressbook_select_error_msg + ' SpiceText[visible=true]')["text"]
        expected_error_msg = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cAllFieldsMarked')
        assert error_msg == expected_error_msg, 'Error message mismatch'
        logging.info("Then click ok button")
        button_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
        button_ok.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.test_field_enterBillingCodeTextField)
    
    def fax_app_click_billing_code_cancel_button(self):
        """
        Purpose: Click cancel button on editable billing code screen
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.billing_code_screen)
        cancel_button = self.spice.wait_for(FaxAppWorkflowObjectIds.billing_code_cancel_button)
        self.spice.validate_button(cancel_button)
        cancel_button.mouse_click()

    def fax_delete_prefix_value(self, index_val):
        """
        Purpose: Delete dial Prefix value
        Args: Index value: Stack 0 or 1
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.6, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        already_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        already_field.mouse_click()
        clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()
        logging.info("Move the scroll bar to top.")
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        logging.info("Delete succesfully")
        # self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)["focus"] = 0
    
    def fax_dual_delete_prefix_value(self, index_val, line="line1"):

        """
        Purpose: Delete dial Prefix value
        Args: Index value: Stack 0 or 1
              line: str - "line1" or "line2", defaults to "line1"
        """
        # Set scrollbar based on line parameter
        if line.lower() == "line2":
            scrollbar = (FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2)
        elif line.lower() == "line1":
            scrollbar = (FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1)
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        
        self.workflow_common_operations.scroll_to_position_vertical(0.7, scrollbar_objectname=scrollbar)
        already_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)
        already_field.mouse_click()
        clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()
        logging.info("Move the scroll bar to top.")
        self.workflow_common_operations.scroll_to_position_vertical(0, scrollbar_objectname=scrollbar)

    def fax_app_verify_dialing_prefix_readonly_value(self,settingsdialPrefix):
        """
        Purpose: verify dialing prefix in fax landing page matching with settings dial prefix value
        Args: settingsdialPrefix: value set in fax settings page
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.dialing_prefix_homepro)
        dPrefix = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.dialing_prefix_homepro} #contentItem")["text"].strip()
        assert dPrefix == settingsdialPrefix, "the value of fax landing dialing prefix value code is not reflected as per settings dialing prefix value," \
                                       "actual value of settings dialing prefix is: in homepro: %s" % settingsdialPrefix

    def fax_app_verify_dialing_prefix_editable_value(self,settingsdialPrefix):
        """
        Purpose: verify dialing prefix in fax landing page matching with settings dial prefix value
        Args: settingsdialPrefix: value set in fax settings page
        """
        faxdialingPrefixNumberTextField = self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxDialingPrefixNumberSendScreen)
        current_value = faxdialingPrefixNumberTextField.__getitem__('displayText')
        logging.info("current_value:"+current_value)

        assert current_value == settingsdialPrefix, "the value of fax landing dialing prefix value code is not reflected as per settings dialing prefix value," \
                                      "actual value of settings dialing prefix is: %s" % settingsdialPrefix


    def fax_app_edit_dialing_prefix_value(self,oldnumber, number):
        """
        Purpose: editing dialPrefix value  in fax landing page
        Args: existing oldnumber value and new value as number
        """
        faxNumberTextField = self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxDialingPrefixNumberSendScreen)
        faxNumberTextField.mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        middle_width = faxNumberTextField["width"] / 2
        middle_height = faxNumberTextField["height"] / 2
        faxNumberTextField.mouse_click(middle_width,middle_height)
        for j in  range(len(oldnumber)):
            num = oldnumber[j]
            logging.info(num)
            key = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
            key.mouse_click()
        logging.info("After key_back_space")

        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self.spice.wait_for(FaxAppWorkflowObjectIds.key_board_keys + num)
            key.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()
        logging.info("Delete succesfully and edited with new number")        

    def fax_add_prefix_close(self, prefix, index_value=0):
        """
        Purpose: Add dial Prefix value and then delete it.
        Args: Index value: Stack 0 or 1
        """
        logging.info("Add prefix")
        self.fax_set_dialing_prefix(prefix, index_value)
        time.sleep(1)
        self.fax_delete_prefix_value(index_value)

    def goto_menu_fax_faxsetup(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.menuText_basicFaxSetup)

    def goto_menu_fax_faxsetup_Line1(self):
        """
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Line1
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.menuText_FaxSetup)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupMenuLine1)
        current_button.mouse_click()
        sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected)["visible"] == True
        sleep(2)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected_ok_button)
        ok_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        
    def goto_menu_fax_faxsetup_Line2(self):
        """
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Line2
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.menuText_FaxSetup)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupMenuLine2)
        current_button.mouse_click()
        sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected)["visible"] == True
        sleep(2)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected_ok_button)
        ok_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        
    def goto_menu_fax_send_settings(self):
        """
        Purpose: Navigates from home menu settings to fax send settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings
        Args: None
        """
        self.spice.goto_homescreen()
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menuText_faxSend,scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)
        logging.info("At Fax Send Settings Screen")

    def goto_menu_fax_send_settings_dialing(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout =5.0)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_menu_list, timeout =8.0)
        logging.info("Wait 8s to wait for all item displayed completely")
        time.sleep(8)

    def goto_menu_fax_send_settings_dialing_prefix_compare_with_fax_landing(self,newDialPrefixVal):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: editing the existing value in fax landing page with a new dial prefix as newDialPrefixVal.
        """
        self.goto_menu_fax_send_settings_dialing()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.text_field_dialing_prefix,
                                                  FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)

        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_dialing_prefix)

        ticket_default_response = self.spice.cdm.get(self.spice.cdm.JOB_TICKET_CONFIGURATION_DEFAULT_SCANFAX)
        dial_prefix = ticket_default_response['dest']['fax']['dialingPrefix']

        logging.info("The value is setting dialing prefix is :"+ dial_prefix)
        # the editted dialingprefix value in fax landing page should not match with the one in settings
        assert dial_prefix != newDialPrefixVal, "the value of dialingPrefix code from fax dialing settings does not match with fax landing page," \
                                       "actual value is: %s" % dial_prefix        

    def goto_menu_fax_send_settings_dialing_line1(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing -> Line1
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen ,5)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()

        line1 = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing_line1)
        line1.mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        logging.info("Wait 8s to wait for all item displayed completely")
        time.sleep(8)
    
    def goto_menu_fax_send_settings_dialing_line2(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing -> Line2
        Args: None
        """
        self.goto_menu_fax_send_settings()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen ,5)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()

        line2 = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing_line2)
        line2.mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        logging.info("Wait 8s to wait for all item displayed completely")
        time.sleep(8)
    
    
    def fax_send_settings_dialing_pulse_dialing(self, dialType: str):
        """
        Purpose: Set dial type based on user input in fax dialing settings
        Args: dialType: should be "pulse" or "tone"
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_pulse_dialing_mode, FaxAppWorkflowObjectIds.button_switch_fax_pulse_dialing_mode]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        select_option = "#ComboBoxOptions" + dialType.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
    
    def fax_send_settings_dualfax_dialing_pulse_dialing(self, dialType: str, line: str = "line1"):
        """
        Purpose: Set dial type based on user input in fax dialing settings
        Args: dialType: should be "pulse" or "tone"
        """
        if line.lower() == "line1":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1
        elif line.lower() == "line2":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        menu_id = [FaxAppWorkflowObjectIds.dual_fax_row_dial_type, FaxAppWorkflowObjectIds.dual_fax_dial_type_combo_box]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list, select_option = False,
                                                  scrollbar_objectname = scrollbar)
        logging.info("Wait for the combo box to be visible and clickable")
        current_elemt = self.spice.wait_for(FaxAppWorkflowObjectIds.dual_fax_dial_type_combo_box)
        self.spice.wait_until(lambda: current_elemt["visible"] == True, timeout=10.0)
        current_elemt.mouse_click()
        select_option = "#ComboBoxOptions" + dialType.lower()
        current_button = self.spice.wait_for(select_option, timeout=10.0)
        current_button.mouse_click()

        

    def fax_send_settings_dialing_detect_dialtone(self, detect_dial_tone: bool = False):
        """
        Purpose: Enables/Disables detect dial tone in fax dialing settings
        Args: value: True = detect dialing on, False = detect dialing off: Bool
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.workflow_common_operations.scroll_to_position_vertical(0.6, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.row_menu_switch_detect_dial_tone_receive)
        state = self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)["checked"]
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive + " SpiceText")
        if (detect_dial_tone):
            if (state == False):
                current_button.mouse_click()
                logging.info(
                    "detect Dial type value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)[
                        "checked"])
            else:
                logging.info("detect Dial type value is : %s" % state)
        else:
            if (state == True):
                current_button.mouse_click()
                logging.info(
                    "detect Dial type value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)[
                        "checked"])
            else:
                logging.info("detect Dial type value is : %s" % state)
        
        self.workflow_common_operations.scroll_to_position_vertical(0.1, FaxAppWorkflowObjectIds.scrollBar_faxDialing)
    
    def fax_send_dualfax_settings_dialing_detect_dialtone(self, detect_dial_tone: bool = False,line: str = "line1"):
        """
        Purpose: Enables/Disables detect dial tone in fax dialing settings
        Args: value: True = detect dialing on, False = detect dialing off: Bool
        """
        if line.lower() == "line1":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1
        elif line.lower() == "line2":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        self.workflow_common_operations.scroll_to_position_vertical(0.6, scrollbar)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.row_menu_switch_detect_dial_tone_receive)
        state = self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)["checked"]
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive + " SpiceText")
        if (detect_dial_tone):
            if (state == False):
                current_button.mouse_click()
                logging.info(
                    "detect Dial type value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)[
                        "checked"])
            else:
                logging.info("detect Dial type value is : %s" % state)
        else:
            if (state == True):
                current_button.mouse_click()
                logging.info(
                    "detect Dial type value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)[
                        "checked"])
            else:
                logging.info("detect Dial type value is : %s" % state)

        self.workflow_common_operations.scroll_to_position_vertical(0.1, scrollbar)

    
    def get_fax_send_settings_dialing_detect_dial_tone_status(self):
        """
        Purpose: get detect dial tone status in fax dialing settings
        @return: dial_tone_state, True = detect dialing on, False = detect dialing off: Bool
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(FaxAppWorkflowObjectIds.view_faxDialingScreen, FaxAppWorkflowObjectIds.row_menu_switch_detect_dial_tone_receive, select_option=False)  
        self.spice.wait_for(FaxAppWorkflowObjectIds.row_menu_switch_detect_dial_tone_receive)
        dial_tone_state = self.spice.wait_for(FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive)["checked"]
        return dial_tone_state

    def fax_job_submission_fax_send(self):
        """
        Purpose: Selects fax send button in fax job submission page
        Args: NA
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSend)
        self.spice.wait_until(lambda:current_button["visible"],timeout=15)
        self.spice.validate_button(current_button)
        current_button.mouse_click()

    def fax_send_settings_set_values(self, options: str, value: bool = False):
        '''
        Selects the values of FaxnumberConfirmation, ErrorCorrectionMode, OverlayFaxHeader and EditableBillingCode based on user input
        Args: options: FaxNumberConfirmation, ErrorCorrectionMode, OverlayFaxHeader, EditableBillingCode
              value: value : True/False : Bool
        '''
        opt = ""
        if options == "scanAndFaxMethod":
            opt = FaxAppWorkflowObjectIds.menuSwitch_scanAndFaxMethod
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_scanAndFaxMethod
        elif options == "faxNumberConfirmation": 
            opt = FaxAppWorkflowObjectIds.menuSwitch_faxNumberConfirmation
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_faxNumberConfirmation
        elif options == "pcSendFax":
            opt = FaxAppWorkflowObjectIds.menuSwitch_pcSendFax
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_pcSendFax
        elif options == "errorCorrectionMode":
            opt = FaxAppWorkflowObjectIds.menuSwitch_errorCorrectionMode
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_errorCorrectionMode
        elif options == "editableBillingCode":
            opt = FaxAppWorkflowObjectIds.menuSwitch_billingCode
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_billingCode

        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        var = self.spice.wait_for(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt)
        if (value == True):
            if (var == False):
                current_option.mouse_click(10,10)

                logging.info(options+" value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
                logging.info(options+" value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(options+" value is : %s" % var)
        # Scroll to list top
        self.workflow_common_operations.scroll_to_position_vertical(position=0, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

    def fax_send_settings_dual_fax_errorCorrectionMode(self, value: bool = False,line="line1"):
        '''
        Selects the value of ErrorCorrectionMode for dual fax
        Args: value: value : True/False : Bool
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)

        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.dual_fax_errorcorrection_mode,FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, 
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.dual_fax_errorcorrection_mode)

        if line.lower() == "line1":
           selection_switch= FaxAppWorkflowObjectIds.dual_fax_errorcorrection_mode_line1
        elif line.lower() == "line2":
            selection_switch= FaxAppWorkflowObjectIds.dual_fax_errorcorrection_mode_line2
        else:
            raise ValueError("Invalid line specified. Use 'line1' or 'line2'.")
        current_option = self.spice.wait_for(selection_switch)
        var = self.spice.wait_for(selection_switch)["checked"]
        if value != var:
            current_option.mouse_click(10,10)
            var = self.spice.wait_for(selection_switch)["checked"]
        logging.info(var)
        if (value == True):
            if (var == False):
                current_option.mouse_click(10,10)
                logging.info("Dual Fax Error Correction Mode value is : %s" % self.spice.wait_for(selection_switch)["checked"])
            else:
                logging.info("Dual Fax Error Correction Mode value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
                logging.info("Dual Fax Error Correction Mode value is : %s" % self.spice.wait_for(selection_switch)["checked"])
            else:
                logging.info("Dual Fax Error Correction Mode value is : %s" % var)
        back_button_id = f"{FaxAppWorkflowObjectIds.view_dual_fax_errorcorrection_mode} {FaxAppWorkflowObjectIds.button_back}"
        back_button = self.spice.wait_for(back_button_id)
        back_button.mouse_click() 

    def fax_send_settings_set_Line2_errorCorrectionMode(self, value: bool = False):
        '''
        Selects the value of ErrorCorrectionMode
        Args: value: value : True/False : Bool
        '''
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout =9.0)

        errorCorrectionMode = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_errorCorrectionMode)
        errorCorrectionMode.mouse_click()

        opt = FaxAppWorkflowObjectIds.menuSwitch_line2_errorCorrectionMode
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_line2_errorCorrectionMode

        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        var = self.spice.wait_for(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt)
        if (value == True):
            if (var == False):
                current_option.mouse_click(10,10)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
        # Scroll to list top
        self.workflow_common_operations.scroll_to_position_vertical(position=0, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

    def fax_send_settings_set_fax_line_selection(self, value: str):
        '''
        Selects the value of ErrorCorrectionMode
        Args: value: str : Auto/Line1/Line2
        '''
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout =9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.8, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

        lineSelection = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_send_fax_line_selection)
        lineSelection.mouse_click()

        select_option = "#ComboBoxOptions" + value.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout =9.0)

        # Scroll to list top
        self.workflow_common_operations.scroll_to_position_vertical(position=0, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

    def verify_fax_send_setting_toggle_option_value(self, options: str, value:bool):
        """
        verify the values of fax send settings, UI should be in Menu -> Settings -> Fax Settings -> Fax Send Settings screen.
        Args: options: scanAndFaxMethod, scanAndFaxMethod, errorCorrectionMode, overlayFaxHeader, editableBillingCode
              value: True/False : Bool
        """
        opt = ""
        if options == "scanAndFaxMethod":
            opt = FaxAppWorkflowObjectIds.menuSwitch_scanAndFaxMethod
        elif options == "faxNumberConfirmation": 
            opt = FaxAppWorkflowObjectIds.menuSwitch_faxNumberConfirmation
        elif options == "pcSendFax":
            opt = FaxAppWorkflowObjectIds.menuSwitch_pcSendFax
        elif options == "errorCorrectionMode":
            opt = FaxAppWorkflowObjectIds.menuSwitch_errorCorrectionMode
        elif options == "editableBillingCode":
            opt = FaxAppWorkflowObjectIds.menuSwitch_billingCode
        else:
            assert False, "setting options not existing"
        
        current_toggle_btn = self.spice.wait_for(opt)
        actual_val = current_toggle_btn["checked"]
        logging.info(f"Get current option <{options}> toggle button is: <{actual_val}>")
        assert actual_val == value, "Fax Send Setting value mismatch."

    def fax_set_country(self, country: str = None, fax_mode=FaxModemType.dungeness_bbu_modem.value):
        """
        :param spice: None
        :param country: Indonesia= "ID", Hong Kong S.A.R.="HK", South Korea="KR", Malaysia="MY",Philippines:"PH",Singapore ="SG"
        Sri Lanka = "LK", Thailand="TH", Vietnam ="VN"
        :return:
        """
        # self.goto_fax_app_fax_setup_countryLocation()
        # country_id = "#Fax" + country + "Radiobutton"
        # the below function just workaround way, need to update it once get corresponding object id
        country_name = ""
        if country == "ID":
            country_name = "Indonesia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_id
        elif country == "HK":
            country_name = "Hong Kong SAR"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hk
        elif country == "KR":
            country_name = "South Korea"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_kr
        elif country == "MY":
            country_name = "Malaysia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_my
        elif country == "PH":
            country_name = "Philippines"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ph
        elif country == "SG":
            country_name = "Singapore"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sg
        elif country == "LK":
            country_name = "Sri Lanka"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lk
        elif country == "TH":
            country_name = "Thailand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_th
        elif country == "VN":
            country_name = "Vietnam"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_vn
        elif country == "AR":
            country_name = "Argentina"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ar
        elif country == "AU":
            country_name = "Australia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_au
        elif country == "BR":
            country_name = "Brazil"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_br
        elif country == "CA":
            country_name = "Canada"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ca
        elif country == "CL":
            country_name = "Chile"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cl
        elif country == "CN":
            country_name = "China"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cn
        elif country == "IN":
            country_name = "India"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_in
        elif country == "JP":
            country_name = "Japan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_jp
        elif country == "MX":
            country_name = "Mexico"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_mx
        elif country == "NZ":
            country_name = "NewZealand"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nz
        elif country == "PK":
            country_name = "Pakistan"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pk
        elif country == "PE":
            country_name = "Peru"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pe
        elif country == "TW":
            country_name = "TaiwanRegion"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tw
        elif country == "US":
            country_name = "UnitedStates"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_us
        elif country == "AT":
            country_name = "Austria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_at
        elif country == "BY":
            country_name = "Belarus"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_by
        elif country == "BE":
            country_name = "Belgium"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_be
        elif country == "BG":
            country_name = "Bulgaria"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_bg
        elif country == "HR":
            country_name = "Croatia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hr
        elif country == "CZ":
            country_name = "CzechRepublic"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_cz
        elif country == "DK":
            country_name = "Denmark"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_dk
        elif country == "EE":
            country_name = "Estonia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ee
        elif country == "FI":
            country_name = "Finland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fi
        elif country == "FR":
            country_name = "France"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_fr
        elif country == "DE":
            country_name = "Germany"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_de
        elif country == "GR":
            country_name = "Greece"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gr
        elif country == "HU":
            country_name = "Hungary"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_hu
        elif country == "IS":
            country_name = "Iceland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_is
        elif country == "IE":
            country_name = "Ireland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ie
        elif country == "IL":
            country_name = "Israel"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_il
        elif country == "IT":
            country_name = "Italy"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_it
        elif country == "LV":
            country_name = "Latvia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lv
        elif country == "LI":
            country_name = "Liechtenstein"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_li
        elif country == "LT":
            country_name = "Lithuania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lt
        elif country == "LU":
            country_name = "Luxembourg"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_lu
        elif country == "MA":
            country_name = "Morocco"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ma
        elif country == "NL":
            country_name = "Netherlands"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_nl
        elif country == "NO":
            country_name = "Norway"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_no
        elif country == "PL":
            country_name = "Poland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pl
        elif country == "PT":
            country_name = "Portugal"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_pt
        elif country == "RO":
            country_name = "Romania"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ro
        elif country == "RU":
            country_name = "Russia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ru
        elif country == "SK":
            country_name = "Slovakia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_sk
        elif country == "SI":
            country_name = "Slovenia"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_si
        elif country == "ZA":
            country_name = "SouthAfrica"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_za
        elif country == "ES":
            country_name = "Spain"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_es
        elif country == "SE":
            country_name = "Sweden"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_se
        elif country == "CH":
            country_name = "Switzerland"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ch
        elif country == "TR":
            country_name = "Turkey"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_tr
        elif country == "UA":
            country_name = "Ukraine"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_ua
        elif country == "GB":
            country_name = "UnitedKingdom"
            country_region_locator = FaxAppWorkflowObjectIds.country_region_gb
        else:
            raise logging.info(f"Trying to select country name:{country} is not supported to set,"
                               f"Choose proper country name")
        logging.info(f"Need to set the country_name to <{country_name}>")
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode])
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_countrylist_scrollbar[fax_mode],timeout=20)
        self.workflow_common_operations.goto_item(country_region_locator,FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode],scrollbar_objectname=FaxAppWorkflowObjectIds.fax_countrylist_scrollbar[fax_mode])
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)

    def fax_set_header_name(self, name: str):
        """
        Set the value of Fax header name based on user input using alphanumeric keyboard
        Args: name: str
        """
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupFaxHeaderName, FaxAppWorkflowObjectIds.input_enterFaxHeaderName, True)
        #self.dial_keyboard_operations.keyboard_enter_text(name)   # TODO Keyboard operations are not implemented for workflow UI
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.input_enterFaxHeaderName)
        current_screen.mouse_click()
        current_screen.__setitem__('displayText', name)
        current_screen.mouse_click()
        key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.KeyOK_two)
        key_Ok.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)

    def fax_set_fax_number(self, number):
        """
        Set the value of Fax number based on user input using alphanumeric keyboard
        Args: number: str
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        sleep(1)
        #self.workflow_common_operations.scroll_to_position_vertical(0.3, FaxAppWorkflowObjectIds.basic_fax_setup_vertical_layout_scrollbar)
        #self.dial_keyboard_operations.keyboard_clear_text() # TODO Keyboard operations are not implemented for workflow UI
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #TextInputBox")
        current_screen.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        num_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key123)
        num_button.mouse_click()
        # clear fax number text before input number.
        while self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #Image")["visible"] == True:
            back_space_key_button = self.spice.wait_for(FaxAppWorkflowObjectIds.input_faxSetupFaxNumber + " #Image")
            back_space_key_button.mouse_click()
        self.enter_numeric_keyboard_values(number, OK_locator=FaxAppWorkflowObjectIds.KeyOK_two)
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        logging.info("Move the scroll bar to top.")


    def remove_fax_number(self):
        """
        Remove the value of Fax number
        """
        # clear fax number text before input number.

        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        while self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen + " #lockImage")["visible"] == True:
            clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
            clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()

    def remove_fax_number_by_backspace(self):
        """
        Remove the value of Fax number by pressing backspace
        """
        # clear fax number text before input number.
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        self.spice.validate_button(clear_button)
        clear_button.mouse_click()
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        self.spice.validate_button(key_ok)
        key_ok.mouse_click()

    def fax_basic_fax_settings_dial_type(self, dial_type: str = "Tone"):
        """
        Purpose: Selects Pulse/Tone dialing type in fax dial settings
        Args: value: Pulse, Tone
        """
        #Cannot find Phone Line Details screen with the flow. Keep dummy code
        pass

    def fax_dialing_set_send_speed(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_send_speed, FaxAppWorkflowObjectIds.button_switch_fax_send_speed]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        select_option = "#ComboBoxOptions" + speed.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
    
    def fax_dialing_dualfax_set_send_speed(self, speed: str,line: str = "line1"):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        if line.lower() == "line1":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1
        elif line.lower() == "line2":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
       
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_send_speed, FaxAppWorkflowObjectIds.button_switch_fax_send_speed]
    
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list, select_option = False,
                                                  scrollbar_objectname = scrollbar)
        logging.info("Wait for the combo box to be visible and clickable")
        current_elem = self.spice.wait_for(FaxAppWorkflowObjectIds.button_switch_fax_send_speed)
        self.spice.wait_until(lambda: current_elem["visible"] == True, timeout=10.0)
        current_elem.mouse_click()
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
            raise ValueError(f"{speed} is not supported to select")
    

    def fax_dialing_set_send_speed_line2(self, speed: str):
        """
        Purpose: Set fax send speed based on user input in fax dialing settings
        Args: speed: should be "slow" or "medium" or "fast"
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_DualfaxDialingScreen)
        send_speed = self.spice.wait_for(FaxAppWorkflowObjectIds.button_switch_fax_send_speed_line2)
        send_speed.mouse_click()

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

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_DualfaxDialingScreen)

    def goto_menu_fax_receive_settings(self):
        """
        Purpose: Navigates from home menu settings to fax receive settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menuText_faxReceive, scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
      
    def goto_menu_fax_receive_settings_distinctive_ring(self):
        """
        Purpose: Navigates from home menu settings to Distinctive Ring
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> distinctive Ring
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_distinctiveRing, FaxAppWorkflowObjectIds.view_distinctiveRingScreen)
    
    def goto_fax_receive_settings_junk_fax_blocking(self):
        """
        Purpose: Navigates from Fax Receive Settings to Junk Fax Blocking
        Ui Flow: Fax receive Settings -> Junk Fax Blocking
        Args: None
        """
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_junk_fax_blocking_settings, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
    
    def goto_fax_receive_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Receive Settings to Fax Notifications
        Ui Flow: Fax receive Settings -> Fax Notifications
        Args: None
        """
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_receive_fax_notifications_settings, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings, select_option=False)
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_fax_notifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_recieve_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])

    def goto_fax_receive_output_bins(self):
        """
        Purpose: Navigates from Fax Receive Settings to Output Bins
        Ui Flow: Fax Receive Settings -> Output Bins
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.outputBinSettingsTextImage, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.outputBinSettingsTextImage)
        #self.spice.wait_until(lambda: self.spice.wait_for(FaxAppWorkflowObjectIds.outputBinSettingsTextImage)["visible"])

    def select_output_bins(self, option):
        """
        Purpose: Select corresponding option about output bins
        Args: option: Output bin 1/Output bin 2/Output bin 3
        """
        logging.info(f"Select output bin option: <{option}>")
        if option == "Output bin 1":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.output_bin1_selected)
            current_option.mouse_click()
        elif option == "Output bin 2":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.output_bin2_selected)
            current_option.mouse_click()
        elif option == "Output bin 3":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.output_bin3_selected)
            current_option.mouse_click()
        elif option == "Automatic":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.output_bin_automatic_selected)
            current_option.mouse_click()
        else:
            raise logging.info(f"{option} is not supported to select")

    def _select_receive_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        logging.info(f"Select fax natification option: <{option}>")
        if option == "Do not notify":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_never)
            current_option.mouse_click()
        elif option == "Notify after job finishes":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_job_completed)
            current_option.mouse_click()
        elif option == "Notify only if job is unsuccessful":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_job_failed)
            current_option.mouse_click()
        else:
            raise logging.info(f"{option} is not supported to select")

    def _select_send_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        logging.info(f"Select fax natification option: <{option}>")
        if option == "Do not notify":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_never)
            current_option.mouse_click()
        elif option == "Notify after job finishes":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_job_completed)
            current_option.mouse_click()
        elif option == "Notify only if job is unsuccessful":
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_option_job_failed)
            current_option.mouse_click()
        else:
            raise logging.info(f"{option} is not supported to select")

    def goto_fax_receive_settings_with_fax_junk_soho_ok_button(self):
        """
        Purpose: UI should move back to Fax receive settings when click ok button in Junk Fax blocking screen.
        Ui Flow: Junk Fax blocking -> Fax receive settings
        Args: None
        """
        junk_fax_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_junk_fax)
        junk_fax_ok_button.mouse_click()
        self.click_junk_fax_keyboardEntry_soho_cancel_button()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
    
    def goto_fax_receive_settings_with_fax_junk_ok_button(self):
        """
        Purpose: UI should move back to Fax receive settings when click ok button in Junk Fax blocking screen.
        Ui Flow: Junk Fax blocking -> Fax receive settings
        Args: None
        """
        self.click_junk_fax_keyboardEntry_cancel_button()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)

    def goto_fax_send_settings_fax_notifications(self):
        """
        Purpose: Navigates from Fax Receive Settings to Fax Notifications
        Ui Flow: Fax send Settings -> Fax Notifications
        Args: None
        """
        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        notifications_option = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_fax_nofifications_combo_box_option)
        notifications_option.mouse_click()
        fax_notifications_box_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)
        self.spice.wait_until(lambda:fax_notifications_box_view["visible"])

    def select_fax_send_settings_fax_notifications_include_thumbnail(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send settings and check include thumbnail
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_send_fax_notifications(option)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_send_notification)
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        while (self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == False):
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)
            current_button.mouse_click(10,10)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == True, 'Include Thumbnail is not checked'
        time.sleep(1)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click()
        fax_send_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_menu_list)
        self.spice.wait_until(lambda:fax_send_settings_view["visible"])

    def select_fax_send_settings_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send settings
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_send_fax_notifications(option)
        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click(10,10)
        fax_send_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_menu_list)
        self.spice.wait_until(lambda:fax_send_settings_view["visible"])

    def select_fax_send_notifications_with_thumbnail(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send screen
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_send_fax_notifications(option)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.3, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_send_notification_view)
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        while (self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == False):
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)
            current_button.mouse_click(10,10)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == True, 'Include Thumbnail is not checked'
        time.sleep(1)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def fax_send_notifications_timeout_screen(self, timeout = "no"):
        """
        Purpose: verify Timeout screen appers on inactivity in fax notification send screen
        Args: option: yes/no
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)
        cancel_button = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_cancel_button)
        self.spice.wait_until(lambda:cancel_button["visible"])
        cancel_button.mouse_click()
        if timeout == "yes":
            time.sleep(5)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_notification_time_out)

    def fax_send_notifications_timeout_screen_select_option(self, option):
        """
        Purpose: verify Timeout screen appers on inactivity in fax notification send screen
        Args: option: yes/no
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_notification_time_out)
        if option == 'yes':
            yes_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_notification_time_out_yes_btn)
            yes_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        else:
            no_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_notification_time_out_no_btn)
            no_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_send_fax_notifications)

    def select_fax_send_settings_fax_notifications_verify_constrained(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax send settings and verify the constrained message
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_send_fax_notifications(option)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_send_notification)
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_done_button)
        doneButton.mouse_click(10,10)
        fax_send_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_menu_list)
        self.spice.wait_until(lambda:fax_send_settings_view["visible"])

    def select_fax_receive_settings_fax_notifications(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax receive settings
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_receive_fax_notifications(option)
        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_receive_done_button)
        doneButton.mouse_click(10,10)
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])

    def select_fax_receive_settings_fax_notifications_include_thumbnail(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax receive settings and check include thumbnail
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_receive_fax_notifications(option)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_receive_notification)               
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.receive_include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        while (self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == False):
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)
            current_button.mouse_click(10,10)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.include_thumbnail_view)["checked"] == True, 'Include Thumbnail is not checked'
        time.sleep(1)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_receive_done_button)
        doneButton.mouse_click()
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])

    def select_fax_receive_settings_fax_notifications_verify_constrained(self, option):
        """
        Purpose: Select corresponding option about fax notification in fax receive settings and verify the constrained message
        Args: option: Do not notify/Notify after job finishes/Notify only if job is unsuccessful
        """
        self._select_receive_fax_notifications(option)

        self.workflow_common_operations.scroll_to_position_vertical(position=0.4, scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_fax_receive_notification)              
        includeThumbnail = self.spice.wait_for(FaxAppWorkflowObjectIds.receive_include_thumbnail)
        includeThumbnail.mouse_click(10,10)
        time.sleep(1)

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

        doneButton = self.spice.wait_for(FaxAppWorkflowObjectIds.notification_receive_done_button)
        doneButton.mouse_click()
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])            

    def verify_fax_receive_settings_view(self, net):
        """
        Check receive settings screen is displayed and verify header text.
        Args: net
        """
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"]==True)
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen} {FaxAppWorkflowObjectIds.menu_text_readcrumb} {FaxAppWorkflowObjectIds.breadcrumb_title_default_text}")["text"]
        expect_text = LocalizationHelper.get_string_translation(net, "cFaxRxSettings")
        assert actual_str == expect_text, f"String checked failed, actual text is <{actual_str}>"

    def verify_empty_junk_fax_list_view(self, net):
        """
        Check empty junk fax list view is displayed and verify body text.
        Args: net
        """
        junk_fax_block_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen)
        self.spice.wait_until(lambda:junk_fax_block_view["visible"])
        # TODO: No specific locator here. 
        expect_text = LocalizationHelper.get_string_translation(net, "cNoFaxList")
        expect_text1 = LocalizationHelper.get_string_translation(net, "cEnableCallerID")
        expected_actual_str=f"{expect_text}\n{expect_text1}"
        actual_str = self.spice.wait_for(FaxAppWorkflowObjectIds.view_junk_block_empty_descr)["text"]

        assert actual_str == expected_actual_str, f"String checked failed, actual text is <{actual_str}>"

    def junk_fax_ok_button_clicked(self):
        """  
        """ 
        junk_fax_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_junk_fax)
        junk_fax_ok_button.mouse_click()        

    def wait_for_receive_fax_junk_fax_number_limit_reached_view_displayed(self):
        """
        To wait for alert displayed when click on add after entering max limited fax number.
        """
        junk_fax_number_limited_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_receive_junk_fax_number_limit_reached_screen)
        self.spice.wait_until(lambda:junk_fax_number_limited_view["visible"])

    def verify_fax_forwarding_configuration_view(self, net):
        """
        Check the fax forwarding configuration view and check the header.
        Args: net
        """
        fax_forwarding_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list)
        self.spice.wait_until(lambda:fax_forwarding_view["visible"])
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_menu_fax_forwarding_list} {FaxAppWorkflowObjectIds.menu_text_readcrumb} {FaxAppWorkflowObjectIds.spice_text_view}", 2)["text"]
        expect_text = LocalizationHelper.get_string_translation(net, "cFaxForwarding")
        assert actual_str == expect_text, f"String checked failed, actual text is <{actual_str}>"

    def verify_fax_reports_menu_list_item(self,net, report, name):
        billing_codes_report_item = self.spice.wait_for(report)
        self.spice.wait_until(lambda:billing_codes_report_item["visible"])
        actual_str = self.spice.wait_for(f"{report} {FaxAppWorkflowObjectIds.checkbox_text}")["text"]
        expect_text = LocalizationHelper.get_string_translation(net, name)
        assert actual_str == expect_text, f"String checked failed, actual text is <{actual_str}>"
        logging.info("<{actual_str}> is available")

    def verify_fax_reports_list_item(self, net):
        """
        Verify below reports are available.
        Junk Fax Report
        Fax T.30 Trace Report
        Fax Activity Log
        Fax Call Report
        Billing codes report.
        Fax Caller ID Report.
        Args: net
        """
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxJunkReport, name ="cBlockedFaxList")
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxTraceReport, name ="cFaxT30TraceReport")
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxActivityLog, name ="cFaxActivity")
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxCallReport, name ="cFaxCallReport")
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxBillingCodesReport, name ="cCfgAppBillingCodesReport")
        self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxCallerIDReport, name ="cCallerIDReport")

    def verify_fax_reports(self,net, report: str):
        """
        Verify the fax reports are available.
        Args: report: str
        """
        if report == "FaxActivityLog":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxActivityLog, name ="cFaxActivity")
        elif report == "FaxCallReport":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxCallReport, name ="cFaxCallReport")
        elif report == "BillingCodesReport":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxBillingCodesReport, name ="cCfgAppBillingCodesReport")
        elif report == "CallerIDReport":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxCallerIDReport, name ="cCallerIDReport")
        elif report == "BlockedFaxlist":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxJunkReport, name ="cBlockedFaxList")
        elif report == "Fax T.30 Trace Report":
            self.verify_fax_reports_menu_list_item(net, report = FaxAppWorkflowObjectIds.menuText_faxTraceReport, name ="cFaxT30TraceReport")
        else:
            raise logging.info(f"{report} is not supported to select")
           
    def verify_fax_settings_view(self,net):
        """
        Check fax settings screen is displayed and verify header text.
        Args: net
        """
        fax_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettingsScreen)
        self.spice.wait_until(lambda:fax_settings_view["visible"]==True)
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxSettingsScreen} {FaxAppWorkflowObjectIds.menu_text_readcrumb} {FaxAppWorkflowObjectIds.breadcrumb_title_default_text}")["text"]
        expect_text = LocalizationHelper.get_string_translation(net, "cFaxAppHeading")
        assert actual_str == expect_text, f"String checked failed, actual text is <{actual_str}>"

    def verify_fax_setup_view(self,net):
        """"
        Check fax setup screen is displayed and verify header text.
        Args: net
        """
        fax_setup_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen)
        self.spice.wait_until(lambda:fax_setup_view["visible"]==True)

        # check header text
        actual_header_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.menu_text_readcrumb} {FaxAppWorkflowObjectIds.spice_text_view}", 2)["text"]
        expect_header_text = LocalizationHelper.get_string_translation(net, "cBasicFaxSetup")
        assert actual_header_str == expect_header_text, f"String checked failed,actual text is<{actual_header_str}>"
        logging.info("At Basic Fax Setup screen")

        # check Country/Region label text
        actual_country_label_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen}  {FaxAppWorkflowObjectIds.item_fax_country_text} {FaxAppWorkflowObjectIds.spice_text_view}")["text"]
        expect_country_label_text = LocalizationHelper.get_string_translation(net, "cCountry") + "*"
        assert actual_country_label_str == expect_country_label_text, f"String checked failed,actual text is<{actual_country_label_str}>"

        # check Country/Region select label
        country_select_label = self.spice.wait_for(FaxAppWorkflowObjectIds.select_fax_country_label)
        self.spice.wait_until(lambda:country_select_label["visible"]==True)
        logging.info("Country/Region is displayed without any error.")

        # check Fax Header Name label text
        actual_header_name_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.input_faxheader_name_view} {FaxAppWorkflowObjectIds.spice_text_view}")["text"]
        expect_header_name_text = LocalizationHelper.get_string_translation(net, "cFaxHeaderName") + "*"
        assert actual_header_name_str == expect_header_name_text, f"String checked failed,actual text is<{actual_header_name_str}>"

        # check Fax Header Name input label
        input_header_name_label = self.spice.wait_for(FaxAppWorkflowObjectIds.input_fax_header_name_label)
        self.spice.wait_until(lambda:input_header_name_label["visible"]==True)
        logging.info("Fax Header Name is displayed without any error.")

        # check Fax Number label text
        actual_header_number_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.input_fax_number_view} {FaxAppWorkflowObjectIds.spice_text_view}")["text"]
        expect_header_number_text = LocalizationHelper.get_string_translation(net, "cFaxNumber") + "*"
        assert actual_header_number_str == expect_header_number_text, f"String checked failed,actual text is<{actual_header_number_str}>"

        # check Fax Number input label
        input_fax_name_label = self.spice.wait_for(FaxAppWorkflowObjectIds.input_fax_number_label)
        self.spice.wait_until(lambda:input_fax_name_label["visible"]==True)
        logging.info("Fax Number is displayed without any error.")

        # check Next button text
        actual_next_button_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxCheckBasicFaxSetupScreen} {FaxAppWorkflowObjectIds.button_faxSetupNext} {FaxAppWorkflowObjectIds.content_item_text}")["text"]
        expect_next_button_text = LocalizationHelper.get_string_translation(net, "cNext")
        # check Next button
        next_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetupNext)
        self.spice.wait_until(lambda:next_button["visible"]==True)
        logging.info("Next button is displayed without any error.")
        
    def verify_fax_recipient_view(self,net):
        """
        Check fax recipient screen is displayed and verify header text.
        Args: net
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        fax_recipient_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.spice.wait_until(lambda:fax_recipient_view["visible"]==True)
        sleep(2)
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_Send_Recipients_View} #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView #SpiceBreadcrumb #textContainer SpiceText")["text"]
        logging.info(f"actual_str1: {actual_str}")

        expect_text = LocalizationHelper.get_string_translation(net, "cFaxAppHeading")
        assert actual_str == expect_text, f"String checked failed, actual text is <{actual_str}>"

    def goto_fax_settings_fax_dialing_screen(self):
        """
        Purpose: Navigates from fax settings to fax dialing settings screen.
        Ui Flow: Fax Settings -> Fax Send Settings -> Fax Dialing Settings.
        """
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menuText_faxSend,scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen ,5)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_menu_list ,5)

    def click_junk_fax_CallHistory_button(self):
        """
        Purpose: Click Received Call History button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax-> Received Call History 
        Args: None
        """
        # self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.receivedCallHistory_button_junk_fax)
        junk_fax_receiveCallHistory_button.mouse_click()
    
    def click_cancel_button_BlockedFax(self):
        """
        Purpose: Click Received Call History button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax-> Received Call History 
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.receivedCallHistory_button_junk_fax)
        junk_fax_receiveCallHistory_button.mouse_click()

    def click_junk_fax_keyboardEntry_button(self):
        """
        Purpose: Click Enter Using Keyboard button in Blocked Fax screen.
        Ui Flow: Fax Receive Settings->Blocked Fax->Enter using Keyboard->JunkFax Block screen.Click Cancel 
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.keyboardEntry_button_junk_fax)
        junk_fax_receiveCallHistory_button.mouse_click()

    def click_junk_fax_CallHistory_cancel_button(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax->Cancel click. 
        Args: None
        """

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.cancel_button_receivedCallHistory)
        junk_fax_receiveCallHistory_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)

    def click_keyboardEntry_junkfaxblock_cancel_button(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->Blocked Fax ->Add->Blocked Fax->Cancel click. 
        Args: None
        """

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_cancel_junkfax)
        junk_fax_receiveCallHistory_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry)
       
    def click_junk_fax_add_button(self):
        """
        Purpose: Click Add button in Junk Fax blocking screen to input numbers.
        Ui Flow: Junk Fax blocking -> click add button
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_junk_fax_blocking_screen)
        junk_fax_add_button = self.spice.wait_for(FaxAppWorkflowObjectIds.add_button_junk_fax)
        junk_fax_add_button.mouse_click()
    
    def click_blocked_number_add_button(self):
        """
        Purpose: Click Add button in number added existing screen to input numbers.
        Ui Flow: NumberAddedExistingListlist1SpiceListViewView -> click add button
        Args: None
        """
        blocked_number_add_button = self.spice.wait_for(FaxAppWorkflowObjectIds.add_button_blocked_number)
        blocked_number_add_button.mouse_click()
    
    def click_junk_fax_number_ok_button(self):
        """
        Purpose: Click Ok button in enter junk fax number screen.
        Ui Flow: enter junk fax number screen -> click ok button
        Args: None
        """
        junk_fax_number_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_junk_fax_number)
        junk_fax_number_ok_button.mouse_click()
    
    def click_numbers_added_to_junk_list_ok_button(self):
        """
        Purpose: Click Ok button in numbersAddedToJunkList screen.
        Ui Flow: numbersAddedToJunkList screen -> click ok button
        Args: None
        """
        junk_fax_number_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_numbers_added_to_junk_list)
        junk_fax_number_ok_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_number_existing_screen)
    
    def check_number_already_junk_fax_view(self, net):
        """
        Purpose: Verify 'The number entered is already in the junk fax list' should be displayed
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_number_already_junk_fax_view)
        ui_body_text = self.spice.wait_for(FaxAppWorkflowObjectIds.body_view_number_already_junk_fax)["text"]
        expect_text = LocalizationHelper.get_string_translation(net, "cEnteredBlockedFax")
        logging.info(f"ui text is: <{ui_body_text}>")
        assert ui_body_text == expect_text, "number already string mismatch"
    
    def click_already_junk_fax_number_ok_button(self):
        """
        Purpose: Click Ok button in numberAlreadyJunkFaxView screen.
        Ui Flow: numberAlreadyJunkFaxView screen -> click ok button
        Args: None
        """
        already_junk_fax_number_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_already_junk_fax_number)
        already_junk_fax_number_ok_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_number_existing_screen)

    def click_ok_button_on_max_limited_junk_fax_number_screen(self):
        """
        Purpose: Click Ok button in max limited junk fax screen.
        Args: None
        """
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_on_max_junk_fax_number_alert)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
        view_number_existing_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_number_existing_screen)
        self.spice.wait_until(lambda:view_number_existing_screen["visible"])
   
    def select_junk_fax_number(self, junk_fax_number_list):
        """
        Purpose: Select multiple junk blocking fax numbers one after the other
        Args: junk_fax_number_list which is provided on the test case, e.g.:["0000", "1111", "2222"] or ["123"]
        """
        for number in junk_fax_number_list:
            number_item = self.spice.wait_for(f"#{number}")
            number_item.mouse_click()

    def selectall_junk_fax_number(self, junk_fax_number_list):
        """
        Purpose: Select multiple junk blocking fax numbers one after the other
        Args: junk_fax_number_list which is provided on the test case, e.g.:["0000", "1111", "2222"] or ["123"]
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.selectAll_checkbox, timeout=15.0)
        check_selectall = self.spice.wait_for(FaxAppWorkflowObjectIds.selectAll_checkbox)
        check_selectall.mouse_click()
        sleep(2)            
    
    def click_remove_button(self):
        """
        Purpose: Click remove button in number added existing screen to remove numbers which selected.
        Ui Flow: NumberAddedExistingListlist1SpiceListViewView -> click remove button
        Args: None
        """
        remove_button = self.spice.wait_for(FaxAppWorkflowObjectIds.remove_button)
        remove_button.mouse_click()

    def check_junk_fax_blocking_numbers(self, number_list):
        """
        Purpose: check whether junk fax blocking numbers is reflected in screen.
        Args: number_list: number list needs to be verified, e.g.:["0000", "1111", "2222"]
        """
        logging.info("check junk fax blocking number added existing screen")
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_junk_fax_blocking_number_existing_screen)
        for number in number_list:
            number_item = self.spice.wait_for(f"#{number}")
        logging.info(f"check junk fax blocking numbers {number_list} success")

    def input_junk_block_number(self,junk_fax_number_list):
        """
        Purpose: Enters  junk blocking fax number 
        Args: junk_fax_number_list which is provided on the test case, e.g.:["123"]
        """
        enter_faxnumber_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number)
        self.spice.wait_until(lambda:enter_faxnumber_view["visible"])
        self.workflow_common_operations.scroll_to_position_vertical(0.8, FaxAppWorkflowObjectIds.blockedFaxScrollBar)
        time.sleep(1)
        junk_fax_number_text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen)
        junk_fax_number_text_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_spicekeyboard)
        self.enter_fax_number_alphanumeric(junk_fax_number_list)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)   
    
    def enter_fax_number_alphanumeric(self,fax_number_list):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of numbers and space
        Args:
          text: number to be entered
        '''        #Populating number keys 
        symbolskey = self.spice.wait_for(FaxAppWorkflowObjectIds.key123)
        symbolskey.mouse_click()
        time.sleep(8)
        for index, fax_number in enumerate(fax_number_list):
            for i in range(len(fax_number)):
                num = fax_number[i]
                logging.info(num)
                key = self.spice.wait_for("#key" + num)
                key.mouse_click()
        key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.KeyOK_two)
        key_Ok.mouse_click()

    def enter_fax_number(self, fax_number_list):
        """
        Purpose: Enter  fax number at Fax junk blocking
        Args: fax_number_list which is provided on the test case
        """
        len_fax_number_list = len(fax_number_list)
        for index, fax_number in enumerate(fax_number_list):
            for i in range(len(fax_number)):
                num = fax_number[i]
                logging.info(num)
                key = self.spice.wait_for("#key" + num)
                key.mouse_click()
        key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_Ok.mouse_click()

    def input_multiple_junk_fax_blocking_numbers(self, junk_fax_number_list):
        """
        Purpose: Enters multiple junk blocking fax number one after the other
        Args: junk_fax_number_list which is provided on the test case, e.g.:["0000", "1111", "2222"] or ["123"]
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number)
        junk_fax_number_text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.enter_junk_fax_number_text_field)
        junk_fax_number_text_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        self.enter_multiple_fax_number(junk_fax_number_list)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)

    def input_junk_fax_blocking_number(self, junk_fax_number):
        """
        Purpose: Enters junk blocking fax number. Jut allowed to add only 1 number at a time according to DUNE-89696
        Args: junk_fax_number which is provided on the test case, e.g.:"101"
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number)
        junk_fax_number_text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.enter_junk_fax_number_text_field)
        junk_fax_number_text_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_spicekeyboard)
        self.enter_fax_number_alphanumeric(junk_fax_number)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)

    def goto_fax_receive_settings_distinctive_ring(self):
        """
        Purpose: Navigates from home fax Receive settings to Distinctive Ring
        Ui Flow: Fax receive Settings -> distinctive Ring
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        # menu_item_id = [FaxAppWorkflowObjectIds.row_object_distinctiveRings,FaxAppWorkflowObjectIds.combo_box_distinctiveRings]
        # self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_distinctive_ring_settings, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_distinctive_ring_settings_select_btn).mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_distinctiveRingScreen)

    def goto_menu_fax_receive_settings_faxforward_config(self):
        """
        Purpose: Navigates from home menu settings to fax forward settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Forwarding
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_faxForwarding, FaxAppWorkflowObjectIds.view_faxForwardingScreen , 5)

    def goto_menu_fax_faxsetup_headername(self):
        """
        Purpose: Navigates from home menu settings to fax header in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax Header name
        Args: None
        """
        self.goto_menu_fax_faxsetup()
        self.homemenu.menu_navigation(self.spice, FaxAppWorkflowObjectIds.view_faxSetupScreen, FaxAppWorkflowObjectIds.button_faxSetupFaxHeaderName)
        self.spice.wait_for(FaxAppWorkflowObjectIds.input_enterFaxHeaderName)
        
    def goto_menu_fax_faxsetup_faxnumber(self):
        """
        Purpose: Navigates from home menu settings to fax number in fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup -> Fax number
        Args: None
        """
        self.goto_menu_fax_faxsetup()
        self.homemenu.menu_navigation(self.spice, FaxAppWorkflowObjectIds.view_faxSetupScreen, FaxAppWorkflowObjectIds.button_faxSetupFaxNumber)
        self.spice.wait_for(FaxAppWorkflowObjectIds.faxNumberKeyboard)

    def goto_fax_app_fax_setup(self):
        """
        Purpose: Navigates from home menu fax app to fax setup screen
         Ui Flow: Main Menu -> Fax -> Continue -> Basic Fax Setup
        Args: None
        """
        logging.info("Go to Menu -> Fax APP")
        self.goto_fax_app()
        try:
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupContinue, FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
            basic_fax_setup_view = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
            self.spice.wait_until(lambda: basic_fax_setup_view["visible"])
        except:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfigure)
            current_button.mouse_click()
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)

    def goto_menu_fax_receivesettings_papertray(self):
        """
        Purpose: Navigates from home menu settings to fax receive paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> paper tray
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.goto_item([FaxAppWorkflowObjectIds.row_object_paper_tray,
                                                   FaxAppWorkflowObjectIds.combo_box_paper_tray],
                                                  FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsPaperTrayScreen)
    
    def goto_menu_fax_receive_settings_fax_receive_speed(self):
        """
        Purpose: Navigates from home menu settings to fax receive speed settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Receive Speed
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.goto_item([FaxAppWorkflowObjectIds.row_object_fax_receive_speed,
                                                   FaxAppWorkflowObjectIds.combo_box_fax_receive_speed],
                                                  FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname=FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        fax_receive_settings_fax_receive_speed_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_settings_fax_receive_speed_screen)
        self.spice.wait_until(lambda:fax_receive_settings_fax_receive_speed_view["visible"])
    
    def fax_receive_settings_dual_fax_receive_speed_selection(self, speed: str, line="line1"):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen
        Args: speed: should be "Slow" or "Medium" or "Fast"
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.receive_speed_combobox_dual_fax)
        combobox = self.spice.wait_for(FaxAppWorkflowObjectIds.receive_speed_combobox_dual_fax)
        combobox.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_receive_dual_fax)
        if line.lower() == "line1":
            speed_combobox = (FaxAppWorkflowObjectIds.receive_speed_line1_combobox)
            current_element = self.spice.wait_for(speed_combobox)
            current_element.mouse_click()
            select_option =self.spice.wait_for(FaxAppWorkflowObjectIds.receive_speed_dual_fax[speed])
            select_option.mouse_click()

        elif line.lower() == "line2":
            speed_combobox = (FaxAppWorkflowObjectIds.receive_speed_line2_combobox)
            current_element = self.spice.wait_for(speed_combobox)
            current_element.mouse_click()
            select_option = self.spice.wait_for(FaxAppWorkflowObjectIds.receive_speed_dual_fax[speed])
            select_option.mouse_click()

        else:
            raise ValueError("Invalid line specified. Use 'line1' or 'line2'.")

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        back_button_id = f"{FaxAppWorkflowObjectIds.view_receive_dual_fax} {FaxAppWorkflowObjectIds.button_back}"
        back_button = self.spice.wait_for(back_button_id)
        back_button.mouse_click() 
    
    
    def fax_receive_settings_fax_receive_speed_selection(self, speed: str):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen
        Args: speed: should be "Slow" or "Medium" or "Fast"
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_receive_settings_fax_receive_speed_screen)
        if speed == "Slow":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_fax_receive_speed_slow)
            current_button.mouse_click()
        elif speed == "Medium":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_fax_receive_speed_medium)
            current_button.mouse_click()
        elif speed == "Fast":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_fax_receive_speed_fast)
            current_button.mouse_click()
        else:
            raise logging.info(f"{speed} is not supported to select")
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        time.sleep(1)

    def goto_menu_fax_receive_settings_dualline_fax_receive_speed(self):
        """
        Purpose: Navigates from home menu settings to fax receive speed settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> Fax Receive Speed -> Dual Line Fax Receive Speed
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        self.workflow_common_operations.scroll_to_position_vertical(0.7, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        fax_receive_speed = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_fax_receive_speed)
        fax_receive_speed.mouse_click()
        fax_receive_settings_fax_receive_speed_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_dualfax_receive_speed_screen)
        self.spice.wait_until(lambda:fax_receive_settings_fax_receive_speed_view["visible"])

    def fax_receive_settings_dualline_fax_receive_speed_selection(self, speed: str):
        """
        Purpose: Set fax receive speed based on Fax Receive Speed screen in dualline
        Args: speed: should be "Slow" or "Medium" or "Fast"
        """
        receive_speed = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_line2_fax_receive_speed)
        receive_speed.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_line2_receive_speed_Screen)
        time.sleep(5)

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
        fax_receive_speed_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_dualfax_receive_speed_screen)
        self.spice.wait_until(lambda:fax_receive_speed_view["visible"])
        time.sleep(1)

        # ---------Toast/Alerts Validation-------
    
    def wait_for_fax_job_status_toast(self,net, message: str = "Success", timeout: int = 60, sec = None, wait_for_toast_dimiss=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        For concurrent feature, if machine support concurrent, this method will verify the toast string
        if not support concurrent, this method will verify the screen str or the screen if is exist.
        Args: message: Scanning, Dialing, Faxing, Success... : str
        """
        job_concurrent_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrent_supported == 'true':
            fax_job_toast_message = ""
            if message == "Scanning":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
            elif message == "Scanning...":
                toast = "..."
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')  
                fax_job_toast_message =(fax_job_toast_message+toast)  
            elif message == "Dialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cDialingMessage')
            elif message == "Connecting":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cConnected')
            elif message == "Faxing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxingMessage')
            elif message == "Success":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxSuccessfulMessage')
            elif message == "Receive":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxReceivedSuccessfully')
            elif message == "Printing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cPrintingFaxMessage')
            elif message == "Receiving":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cReceiving')
            elif message == "Fax received successfully":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxReceivedSuccessfully')
            elif message == "Canceling":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cCancelingCompleteMessage')
            elif message == "Fax Cancelled":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxCanceledMessage')
            elif message == "Fax Cancelled remove originals":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxcanceledBe')
            elif message == "Processing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cJobStateTypeProcessing')
            elif message == "Call blocked":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cCallBlocked')
            elif message == "Printin fax...":
                toast = "..."
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cPrintingFaxMessage')  
                fax_job_toast_message =(fax_job_toast_message+toast) 
            elif message == "Printing complete":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cPrintingCompleteMessage')
            elif message == "Communication problem without redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cCommunicationProblemFaxNotSent')
            elif message == "Fax Reports Printing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cPrinting')    
            elif message == "Communication problem with redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cCommunicationProblem')
            elif message == "No answer without redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cDeliveryStatusTypeNoAnswer')
            elif message == "No answer with redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxResultNoAnswer')
            elif message == "Busy without redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cRecipientBusyFaxNotSent')
            elif message == "Busy with redialing":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cRecipientBusyMessage')
            elif message == "The scheduled fax will be sent at {0:s}":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxSentNameTime')
            elif message == "Redial on No Answer":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cRedialOnNoAnswer')

            elif message == "Incoming fax":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cIncomingFax')
            elif message == "Receive Connecting":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cConnecting')
            elif message == "The fax could not be sent.":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxNotSent')
            elif message == "The fax could not be sent to all the recipients. Try again later.":
                fax_job_toast_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxNotSentAllRecipients')
                
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout = 15.0)
            start_time = time.time()
            toast_status = ""
            while time.time()-start_time < timeout:
                try:
                    self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=3.0)
                    toast_status = self.spice.wait_for(FaxAppWorkflowObjectIds.text_toastInfoText)["text"]
                    logging.info("Current Toast message is : %s" % toast_status)
                    self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=3.0)
                except:
                    logging.info("Still finding corresponding status.")
                logging.info(f"{fax_job_toast_message} in {toast_status} is <{fax_job_toast_message in toast_status}>")
                if fax_job_toast_message in toast_status:
                    break
            if fax_job_toast_message not in toast_status:
                raise TimeoutError("Required Toast message does not appear within %s " % timeout)

            if wait_for_toast_dimiss:
                start_time = time.time()
                toast_status = ""
                while time.time()-start_time < timeout:
                    try:
                        toast_status = self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=4)["text"]
                        logging.info(f"Still corresponding status <{toast_status}> dispay in screen")
                    except Exception as err:
                        logging.info("Toast screen already dismiss")
                        break
        else:
            fax_job_screen_message = ""
            if message == "Dialing":
                fax_job_screen_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cDialingMessage')
            elif message == "Connecting":
                fax_job_screen_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cConnected')
            elif message == "Faxing":
                fax_job_screen_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxingMessage')
            elif message == "Success":
                fax_job_screen_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net,'cFaxSentSuccessfully')
            
            self.spice.wait_for("#wizardProgressRecevieActiveJob", timeout = 15.0)
            start_time = time.time()
            screen_status = ""
            while time.time()-start_time < timeout:
                try:
                    screen_status = self.spice.wait_for("#ActiveJobModalView #ViewColumn SpiceText[visible=true]")["text"]
                    logging.info("Current screen message is : %s" % screen_status)
                except:
                    logging.info("Still finding corresponding status.")
                if fax_job_screen_message in screen_status:
                    break
            if fax_job_screen_message not in screen_status:
                raise TimeoutError("Required screen message does not appear within %s " % timeout)


    def wait_for_non_concurrent_fax_complete_screen(self, timeout=15):
        """
        Purpose: Wait for the fax complete wizard screen appears, the screen only appears on non-concurrent printer.
        Args: timeout:
        @return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_complete_wizard_screen, timeout)
        logging.info("The fax complete wizard screen appears")

    def wait_for_fax_job_status_toast_with_callerID(self, message: str = "Success", timeout: int = 60, sec = None):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        For non concurrent machine, only the string of the incoming status can be obtained. 
        Hence we just verify the callerID and string in incoming state. This method needs to be improved in the future
        Args: message: Scanning, Dialing, Faxing, Success... : str
        """
        job_concurrent_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrent_supported == 'true':
            fax_job_toast_message = ""
            if message == "IncomingFax":
                fax_job_toast_message = "Incoming fax..."
            elif message == "Connecting":
                fax_job_toast_message = "Connecting..."
            elif message == "Receive":
                fax_job_toast_message = "Receiving..."

            self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout = 15.0)
            start_time = time.time()
            toast_status = ""
            while time.time()-start_time < timeout:
                try:
                    self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=15.0)
                    toast_status = self.spice.wait_for(FaxAppWorkflowObjectIds.text_toastInfoText)["text"]
                    logging.info("Current Toast message is : %s" % toast_status)
                    self.spice.wait_for(FaxAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=15.0)
                except:
                    logging.info("Still finding corresponding status.")
                if fax_job_toast_message in toast_status and "101" in toast_status and "FAX SIMULATOR" in toast_status:
                    break
            if fax_job_toast_message not in toast_status:
                raise TimeoutError("Required Toast message does not appear within %s " % timeout)
        else:
            fax_job_screen_message = 'Incoming fax...'
            start_time = time.time()
            current_screen_str = ''
            while time.time()-start_time < timeout:
                try:
                    current_screen_str= self.spice.wait_for('#ProgressColumn #secondaryAreaTextImage SpiceText[visible=true]')['text']
                    logging.info("Current Screen message is : %s" % current_screen_str)
                except:
                    logging.info("Still finding corresponding status.")
                if fax_job_screen_message in current_screen_str and "101" in current_screen_str and "FAX SIMULATOR" in current_screen_str:
                    break
            if fax_job_screen_message not in current_screen_str:
                raise TimeoutError("Required Screen message does not appear within %s " % timeout)

    def fax_receive_settings_auto_answer(self, auto_answer: bool = False):
        """
        Purpose: Enables/Disables Auto answer in fax receive settings
        Args: auto_answer: True, False: Bool
        """
     
        menu_item_id = [FaxAppWorkflowObjectIds.row_menuSwitch_autoAnswer,FaxAppWorkflowObjectIds.menuSwitch_autoAnswer]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        state = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_autoAnswer)["checked"]
        logging.info(state)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_autoAnswer)
    

        if (auto_answer):
            if (state == False):
                current_button.mouse_click()
                logging.info(
                    "Enabling autoAnswer : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_autoAnswer)["checked"])
            else:
                logging.info("AutoAnswer has been enabled already : %s" % state)
        else:
            if (state == True):
                current_button.mouse_click()
                logging.info(
                    "Disabling autoAnswer : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_autoAnswer)["checked"])
            else:
                logging.info("AutoAnswer has been enabled already  : %s" % state)
          
    def check_fax_receive_settings_auto_answer_status(self, check_status):
        """
        Purpose: check fax receive settings auto answer status
        Args: check_status: True, False: Bool
        """
        state = self.spice.query_item(FaxAppWorkflowObjectIds.menuSwitch_autoAnswer)["checked"]
        logging.info(f"fax receive settings auto answer status is: {state}")
        assert state == check_status, "Failed to check fax receive settings auto answer"

    def fax_set_ringer_volume(self, value):
        """
        Purpose: Set ringer volume in fax receive settings
        Args: volue: High,Low,Off
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.combo_box_ringer_volume , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        ringer_volume = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_ringer_volume)
        ringer_volume.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettings_ringer_volume_Screen)
        ringer_volume_id  = self.spice.wait_for(FaxAppWorkflowObjectIds.ringer_volume_dict[value])
        ringer_volume_id.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)

    def fax_dual_line_set_ringer_volume(self, value):
        """
        Purpose: Set ringer volume in fax receive settings
        Args: value: High,Low,Off
        """
        ringer_volume = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_line2_ringer_volume)
        ringer_volume.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_line2_ringer_volume_Screen)
        ringer_volume_id  = self.spice.wait_for(FaxAppWorkflowObjectIds.ringer_volume_dict[value])
        ringer_volume_id.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_ringerVolumeDualLineScreen, timeout =9.0)

    def fax_app_set_originalside_receive_settings(self, value):
        opt = FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_twoSidedPrinting_receive
        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        var = self.spice.wait_for(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt)
        #current_option = self.spice.wait_for(opt + " SpiceText")

        if (value == True):
            if (var == False):
                current_option.mouse_click(5,5)
                logging.info(" value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(" value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(5,5)
                logging.info(" value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(" value is : %s" % var)
        

    def fax_app_set_two_sided_scan_format_receive_settings(self, value: bool = False):
        """
        Purpose: Selects 2-Sided Scan format based on user input
        Args: value: True = 2-Sided format flip-style, False = 2-Sided format book-style: Bool
        """
        # Verify the option 2Sided format is visible or not
        time.sleep(2)
        select_format = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_twosided_settings_format)
        select_format.mouse_click()
        time.sleep(2)

        if value == False:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combobox_twosided_format_bookstyle)
            current_button.mouse_click()
        elif value == True:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.combobox_twosided_format_flipstyle)
            current_button.mouse_click()
        else:
            raise logging.info(f"{select_format} is not supported to select")
        
    def fax_app_set_two_sided_scan_format_faxreceivesettings_check_constraints(self):
        """
        Purpose: Selects 2-Sided Scan format based on user input
        Args: value: True = 2-Sided format flip-style, False = 2-Sided format book-style: Bool
        """
        #constrained_message_string = "This option is available when 2-sided fuctionality is enabled."
        time.sleep(2)
        select_format = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_twosided_settings_format)
        select_format.mouse_click()
        time.sleep(2)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        #textContent = self.spice.wait_for("#constraintDescription #textColumn #contentItem") 
        #assert textContent["text"] == constrained_message_string

        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(3)

    def fax_receive_settings_set_values(self, options: str, value: bool = False):
        """
        Selects the values of Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes and Fit to Page
        Args: options: Error Correction Mode, 2-Sided Fax Printing, Stamp Received Faxes, Fit to Page
              value: value : True/False : Bool
        """
        
        opt = ""
        opt_row = ""

        if options == "Error Correction Mode":
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_errorCorrectionMode_receive
            opt = FaxAppWorkflowObjectIds.menuSwitch_errorCorrection_receive
        elif options == "2-Sided Fax Printing":
            opt = FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_twoSidedPrinting_receive
        elif options == "Stamp Received Faxes":
            opt = FaxAppWorkflowObjectIds.menuSwitch_stampReceivedFaxes_receive
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_stampReceivedFaxes_receive
        elif options == "Fit to Page":
            opt = FaxAppWorkflowObjectIds.menuSwitch_fitToPage_receive
            opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_fitToPage_receive
        elif options == "Detect Dial Tone":
            opt = FaxAppWorkflowObjectIds.menu_switch_detect_dial_tone_receive
            opt_row = FaxAppWorkflowObjectIds.row_menu_switch_detect_dial_tone_receive

        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        var = self.spice.wait_for(opt)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(opt)
        #current_option = self.spice.wait_for(opt + " SpiceText")
        if (value == True):
            if (var == False):
                current_option.mouse_click(5,5)
                logging.info(options + " value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(options + " value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(5,5)
                logging.info(options + " value is : %s" % self.spice.wait_for(opt)["checked"])
            else:
                logging.info(options + " value is : %s" % var)
        
        logging.info("Move the scroll bar to screen top.")
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

    def fax_add_remove_recipient(self, add_remove: str):
        """
        Purpose: Navigates from Job Submission screen to fax add/remove recipient in fax app
        Ui Flow: Job Submission -> # of Fax recipients -> Add/Remove
            If "Add" then navigates to Add recipient
            If "Remove" navigated Remove recipient.
        Args: Add/Remove
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxNumberOfRecipientsButton)["visible"] == True
        recipient_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxNumberOfRecipientsButton + " SpiceText[visible=true]")
        recipient_button.mouse_click()
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        if add_remove == "Add":
            while (self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddRecipients)["visible"] == False):
                current_screen.mouse_wheel(180, -180)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddRecipients)["visible"] == True
            add_recipient_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddRecipients + " SpiceText[visible=true]")
            add_recipient_button.mouse_click()
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        if add_remove == "Remove":
            while (self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_recipient2)["visible"] == False):
                current_screen.mouse_wheel(180, -180)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_recipient2)["visible"] == True
            recipient_button = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_recipient2 + " SpiceText[visible=true]")
            recipient_button.mouse_click()
            remove_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRemoveRecipientScreen + " SpiceText[visible=true]")
            while (self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSendRecipientsRemoveButton)["visible"] == False):
                remove_screen.mouse_wheel(180, -180)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSendRecipientsRemoveButton)["visible"] == True
            remove_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSendRecipientsRemoveButton + " SpiceText[visible=true]")
            remove_button.mouse_click()

    def fax_receive_settings_paper_tray_selection(self, option: str):
        """
        Purpose: Navigates to fax receive setttings screen to select the paper tray.
        Ui Flow: Fax receive settings -> Paper Tray -> Selection
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsPaperTrayScreen)
        paper_tray_id = FaxAppWorkflowObjectIds.paper_tray_dic[option]
        current_button = self.spice.wait_for(paper_tray_id)
        self.spice.wait_until(lambda: current_button["visible"] is True, 20)
        time.sleep(1)
        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout=9.0)
    
    def fax_receive_get_paper_tray_value(self):
        """
        Purpose:get the paper tray text in fax receive setttings screen.
        @return: ui_setting_string
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        ui_setting_string = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.combo_box_paper_tray} SpiceText[visible=true]")["text"]
        return ui_setting_string

    def fax_app_add_fax_number_confirm(self, fax_number, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        self.spice.fax_ui().goto_fax_app_screen_enter_fax_number()

        self.enter_numeric_keyboard_values(fax_number) 
        if confirm_fax_number:
            confirmFaxNumberScreen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
            confirm_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfirm)
            confirm_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    
    def fax_app_add_fax_number_confirm_using_enter_key(self, fax_number, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        self.spice.fax_ui().goto_fax_app_screen_enter_fax_number()

        self.enter_numeric_keyboard_values_using_enter_key(fax_number) 
        if confirm_fax_number:
            confirmFaxNumberScreen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
            confirm_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfirm)
            confirm_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def fax_app_enter_fax_number_confirm_cancel(self, fax_number):
        """
        Purpose: Enters fax number in enter fax number screen, confirm and cancel it.
        """
        self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_numeric_keyboard_values(fax_number)  
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxCancel)
        current_button.mouse_click()
        # assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def goto_fax_tools_fax_report(self):
        """
        Purpose: Navigates from home menu settings to fax reports
        Ui Flow: Menu -> tools -> Reports -> Fax reports
        Args: None
        """
        self.homemenu.goto_menu_tools_reports(self.spice)
        print("Goto Fax tools - Fax reports")
        time.sleep(4)
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxReports)
        #self.homemenu.menu_navigation(self.spice, MenuAppWorkflowObjectIds.view_reports, FaxAppWorkflowObjectIds.menuText_faxReports ,scrollbar_objectname= MenuAppWorkflowObjectIds.scrollbar_menureportspage)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxReports)
        current_button.mouse_click()

    def fax_report_print_constraint_check(self):
        """
        Purpose: Navigates to fax report options and checks the print button constraint
        Ui Flow: Menu -> tools -> Reports -> Fax reports
        Args: None
        """
        click_print_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_printMenu)
        click_print_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
    
    def fax_report_view_constraint_check(self):
        """
        Purpose: Navigates to fax report options and checks the view button constraint
        Ui Flow: Menu -> tools -> Reports -> Fax reports
        Args: None
        """
        click_view_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_viewMenu)
        click_view_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
    
    def fax_report_view(self, option: str):
        """
        Purpose: Navigates to fax report options and views
        Ui Flow: Fax reports -> report options
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_report_list_view)
        opt = ""
        if option == 'Billing Codes Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxBillingCodesReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxBillingCodesReport
        elif option == "Junk fax report":
            opt = FaxAppWorkflowObjectIds.menuText_faxJunkReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxJunkReport
        elif option == "Fax T.30 trace report":
            opt = FaxAppWorkflowObjectIds.menuText_faxTraceReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxTraceReport
        elif option == "Fax activity log":
            opt = FaxAppWorkflowObjectIds.menuText_faxActivityLog
            view_object = FaxAppWorkflowObjectIds.view_object_faxActivityLog
        elif option == 'Fax Call Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxCallReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxCallReport
        elif option == 'Fax CallerID Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxCallerIDReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxCallerIDReport

        self.workflow_common_operations.goto_item(view_object, FaxAppWorkflowObjectIds.fax_report_list_view,select_option = False,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxToolReports)

        report_button = self.spice.wait_for(opt)
        report_button.mouse_click()
        logging.info("Clicked on report view button")
        view_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_viewMenu)
        view_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_reports_pdf)



    def fax_report_print(self, option: str):
        """
        Purpose: Navigates to fax report options and prints
        Ui Flow: Fax reports -> report options
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_report_list_view)
        opt = ""
        if option == 'Billing Codes Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxBillingCodesReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxBillingCodesReport
        elif option == "Junk fax report":
            opt = FaxAppWorkflowObjectIds.menuText_faxJunkReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxJunkReport
        elif option == "Fax T.30 trace report":
            opt = FaxAppWorkflowObjectIds.menuText_faxTraceReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxTraceReport
        elif option == "Fax activity log":
            opt = FaxAppWorkflowObjectIds.menuText_faxActivityLog
            view_object = FaxAppWorkflowObjectIds.view_object_faxActivityLog
        elif option == 'Fax Call Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxCallReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxCallReport
        elif option == 'Fax CallerID Report':
            opt = FaxAppWorkflowObjectIds.menuText_faxCallerIDReport
            view_object = FaxAppWorkflowObjectIds.view_object_faxCallerIDReport

        self.workflow_common_operations.goto_item(view_object, FaxAppWorkflowObjectIds.fax_report_list_view,select_option = False,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxToolReports)


        report_button = self.spice.wait_for(opt)
        report_button.mouse_click()

        click_print_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_printMenu)
        click_print_button.mouse_click()
    

    def fax_multiple_reports_print(self, option_list: list):
        """
        Purpose: Navigates to fax report options and prints multiple reports
        Ui Flow: Fax reports -> report options
        @param: option_list: multiple reports want to report, such as: ["Fax T.30 trace report", "Fax activity log", "Fax Call Report"]
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_report_list_view)
        for index, option in enumerate(option_list):
            opt = ""
            if option == 'Billing Codes Report':
                opt = FaxAppWorkflowObjectIds.menuText_faxBillingCodesReport
                view_object = FaxAppWorkflowObjectIds.view_object_faxBillingCodesReport
            elif option == "Junk fax report":
                opt = FaxAppWorkflowObjectIds.menuText_faxJunkReport
                view_object = FaxAppWorkflowObjectIds.view_object_faxJunkReport
            elif option == "Fax T.30 trace report":
                opt = FaxAppWorkflowObjectIds.menuText_faxTraceReport
                view_object = FaxAppWorkflowObjectIds.view_object_faxTraceReport
            elif option == "Fax activity log":
                opt = FaxAppWorkflowObjectIds.menuText_faxActivityLog
                view_object = FaxAppWorkflowObjectIds.view_object_faxActivityLog
            elif option == 'Fax Call Report':
                opt = FaxAppWorkflowObjectIds.menuText_faxCallReport
                view_object = FaxAppWorkflowObjectIds.view_object_faxCallReport
            elif option == 'Fax CallerID Report':
                opt = FaxAppWorkflowObjectIds.menuText_faxCallerIDReport
                view_object = FaxAppWorkflowObjectIds.view_object_faxCallerIDReport
            
            self.workflow_common_operations.goto_item(view_object, FaxAppWorkflowObjectIds.fax_report_list_view,select_option = False,scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxToolReports)
            self.spice.wait_for(opt).mouse_click()

        click_print_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_printMenu)
        click_print_button.mouse_click()

    def enter_multiple_fax_number(self, fax_number_list):
        """
        Purpose: Enter Multiple fax number at Fax send to contacts screen
        Args: fax_number_list which is provided on the test case
        """
        len_fax_number_list = len(fax_number_list)
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        for index, fax_number in enumerate(fax_number_list):
            for i in range(len(fax_number)):
                num = fax_number[i]
                logging.info(num)
                key = self.spice.wait_for("#key" + num)
                key.mouse_click()
            button_pause = self.spice.wait_for(FaxAppWorkflowObjectIds.enter_key_number_keyboard)
            button_pause.mouse_click()
            if (self.spice.uisize == "XS" or self.spice.uisize == "S" or self.spice.uisize == "L"):
                faxNumberTextField.mouse_click(10)
                time.sleep(1)
            else:
                pass
        

        key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_Ok.mouse_click()

    def fax_app_multiple_recipients_using_enter_fax_number(self, fax_number_list):
        """
        Purpose: Enters multiple fax number one after the other and then waits for job submission page
        Args: fax_number_list which is provided on the test case
        """
        self.spice.fax_ui().goto_fax_app_screen_enter_fax_number()
        #self.goto_fax_app_recipient_screen_enter_fax_number()
        self.enter_multiple_fax_number(fax_number_list)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

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
        self.goto_fax_without_skip_button()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        if yes_no == 'No':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_cancel)
            current_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
            current_button.mouse_click()
            logging.info("verify the error message")
            time.sleep(2)
            error_msg = self.spice.wait_for(FaxAppWorkflowObjectIds.faxAddressbook_select_error_msg + ' SpiceText[visible=true]')["text"]
            assert error_msg == 'Select at least one member to proceed.', 'Error message mismatch'
            logging.info("Then click ok button")
            button_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
            button_ok.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            logging.info("Press the back button")
            self.back_to_addressbook_local_from_local_select_screen_with_back_button()
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
            logging.info("Press the close button")
            self.back_to_faxsendtocontacts_from_addressbook_local_screen_with_close_button()
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
            faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
            faxNumberTextField.mouse_click()
            time.sleep(5)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard,timeout=20)
            self.enter_multiple_fax_number(fax_number_list)

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

    def select_multi_destination_contacts(self, payload_list):
        """
        Purpose: Selects fax contacts to send to multi destination using addressbook (send to contacts) option
        Args: record_id_list which is passed on sequentially from create_fax_multiple_contacts keyword.
        #Need to be replaced later
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts
        """
        self.goto_fax_without_skip_button() 
        self.select_multiple_contacts_from_local_contacts(payload_list)

    def select_multiple_contacts_from_local_contacts(self,payload_list):
        """
        Purpose: Selects fax contacts to send to multi destination using addressbook (send to contacts) option
        UI should be in Fax screen -> Fax Recipients screen -> Sent to Contacts
        UI Flow: Main SendToContacts -> Local -> Select Fax Recipients
        Args: record_id_list which is passed on sequentially from create_fax_multiple_contacts keyword.
        """
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        for payload in payload_list:
            # current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            AddressBook_name = payload['displayName']
            addressBook_name_item = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Row'
            addressBook_name_model = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
            time.sleep(2)
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, addressBook_name_item, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view,scroll_height=50)
            if(self.spice.wait_for(addressBook_name_model)["checked"] == False):
                current_button = self.spice.wait_for(addressBook_name_model, timeout = 10.0)
                current_button.mouse_click()
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def select_multiple_contacts_one_by_one(self, payload):
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        AddressBook_name = payload['displayName']
        addressBook_name_item = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Row'
        addressBook_name_model = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
        time.sleep(2)
        self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, addressBook_name_item, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view,scroll_height=50)
        if(self.spice.wait_for(addressBook_name_model)["checked"] == False):
            current_button = self.spice.wait_for(addressBook_name_model, timeout = 10.0)
            current_button.mouse_click()
        assert self.spice.wait_for(addressBook_name_model)["checked"] == True, 'Contact is not checked'
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()


    def fax_receive_settings_set_fax_forwarding(self, forward, print, fax_number):
        """
        Selects the values of Fax forwarding based on user input like forward, forward+print and fax number
        Args: options: forward, print, fax_number
        """
    
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        var = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        if (forward == True):
            if (var == False):
                current_option.mouse_click(5,5)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(5,5)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward and Print value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        #assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)["visible"] == True
        var = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)
        if (print == True):
            if (var == False):
                current_option.mouse_click(5,5)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)[
                        "checked"])
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(5,5)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)[
                        "checked"])
            else:
                logging.info("Fax forward value is : %s" % var)
        if forward == True and print == True:
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.textField_faxNumberSettings)["visible"] == True
            current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxnumber)
            current_option.mouse_click(5,5)
            self.enter_numeric_keyboard_values(fax_number)    
            
    def enter_numeric_keyboard_values(self, number, view=FaxAppWorkflowObjectIds.view_keyboard, OK_locator= FaxAppWorkflowObjectIds.keyOK):
        self.spice.wait_for(view)
        self.spice.wait_until(lambda: self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)["visible"] == True)
        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self.spice.wait_for("#key" + num)
            key.mouse_click()
        key_Ok  = self.spice.wait_for(OK_locator)
        key_Ok.mouse_click()

              
    def enter_numeric_keyboard_values_using_enter_key(self, number, view=FaxAppWorkflowObjectIds.view_keyboard, OK_locator= FaxAppWorkflowObjectIds.enter_key_number_keyboard):

        current_screen = self.spice.wait_for(view)
        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self.spice.wait_for("#key" + num)
            key.mouse_click()
        key_enter  = self.spice.wait_for(OK_locator)
        key_enter.mouse_click()
    
    def enter_numeric_keyboard_values_using_pause_key(self, number, number2, view=FaxAppWorkflowObjectIds.view_keyboard, OK_locator= FaxAppWorkflowObjectIds.keyOK, pause_key= FaxAppWorkflowObjectIds.KeyPause):
        
        current_screen = self.spice.wait_for(view)
        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self.spice.wait_for("#key" + num)
            key.mouse_click()
        key = self.spice.wait_for("#pause")
        key.mouse_click()
        for j in  range(len(number2)):
            num2 = number2[j]
            logging.info(num2)
            key = self.spice.wait_for("#key" + num2)
            key.mouse_click()
        key_enter  = self.spice.wait_for(OK_locator)
        key_enter.mouse_click()

    def fax_app_send_to_contacts(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app
        Ui Flow: Main Menu -> Fax -> Skip -> Sent to Contacts
        Args: None
        """
        self.goto_fax_app()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)


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
        fax_instance.check_modem_status()

        fax_instance.update_receive_fax_ticket(**payLoad)
        trace_log('========== RECEIVE FAX Job Started ==========')
        max_wait_time = waitTime

        # name mangling
        fax_instance._Fax__receive_fax(faxSimIP)

        if auto_answer == "No":
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveStateScreen, timeout=9.0)

            self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
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
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["visible"] == True
        var = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        if (forward == True):
            if var == False:
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                        "checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                        "checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward and Print value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)["visible"] == True
        var = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)
        if (print == True):
            if (var == False):
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" %
                    self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)[
                        "checked"])
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" %
                    self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForwardAndPrint)[
                        "checked"])
            else:
                logging.info("Fax forward value is : %s" % var)

        text_field = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxnumber} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        # to check if alredy has fax number
        try:
            self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxnumber} {FaxAppWorkflowObjectIds.item_in_textField_enterFaxnumber}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        time.sleep(1)
        self.enter_numeric_keyboard_values(fax_number)
    # Removing Print and Forward enabled features which are not applicable for Enterprise
    def fax_receive_settings_set_fax_forward_print_number(self, forward, fax_number):
        """
        Selects the values of Fax forwarding based on user input like forward, forward+print and fax number.
        Add fax number with all combination even if fax forward or print is disabled.
        Args: options: forward, print, fax_number
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["visible"] == True
        var = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)["checked"]
        logging.info(var)
        current_option = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)
        if (forward == True):
            if var == False:
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                        "checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        else:
            if (var == True):
                current_option.mouse_click(10,10)
                logging.info(
                    "Fax forward value is : %s" % self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                        "checked"])
                assert self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxForward)[
                           "checked"] != var, "Fax forward and Print value is not setting failed"
            else:
                logging.info("Fax forward value is : %s" % var)
        text_field = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxnumber} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        # to check if alredy has fax number
        try:
            self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxnumber} {FaxAppWorkflowObjectIds.item_in_textField_enterFaxnumber}")
            text_field.mouse_click()
        except:
            text_field.mouse_click()
        time.sleep(1)
        self.enter_numeric_keyboard_values(fax_number)


    def fax_setup_phone_line_sharing_selection(self, option='Yes'):
        """
        Selects the phone line option yes or no. Default it is set as Yes.
        Args: options: Yes and No
        """
        current_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupLineShareScreen)
        self.spice.wait_until(lambda:current_view["visible"])
        logging.info("At fax setup phone line sharing selection screen")

        if option == 'Yes':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpLineShareYes)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpLineShareYes)["visible"] == True
            current_button.mouse_click()
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpLineShareNo)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpLineShareNo)["visible"] == True
            current_button.mouse_click()
        time.sleep(1)

    def fax_setup_voice_call_selection(self, option='Yes'):
        """
        Selects the voice call option yes or no. Default it is set as Yes.
        Args: options: Yes and No
        """
    
        logging.info("At fax setup voice call selection screen")

        if option == 'Yes':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpVoiceCallsYes)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpVoiceCallsNo)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()

    def fax_setup_distinctive_ring_availability(self, net, option='Yes', distinctive_ring=None):
        """
        Selects the distinctive rings option and also Recorded ring is unavailable is handled.
        Args: options: Single Ring, Double Ring, Triple Ring, All standard ring, Ring Pattern Detection, Recorded ring
        """
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupDistinctiveRingForFaxScreen)
        self.spice.wait_until(lambda:current_screen["visible"])
        logging.info("At fax setup distinctive ring screen")

        if option == 'Yes':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpDistinctiveRingYes)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()
            if distinctive_ring:
                self.fax_receieve_set_distinctive_ring(distinctive_ring)
                time.sleep(1)
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetUpDistinctiveRingNo)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()
    
    def fax_setup_answering_machine_selection(self, net, option='Yes', index=0, timeout=30):
        """
        Selects the answering machine option yes or no. Default it is set as Yes.
        Args: 
            option: Yes and No
            index:
            timeout:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_setup_answering_machine_screen)
        if option == 'Yes':
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_fax_setup_answering_machine_yes,timeout=15)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()
        else:
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_fax_setup_answering_machine_no)
            self.spice.wait_until(lambda:current_button["visible"])
            time.sleep(1)
            current_button.mouse_click()
    
    
    def fax_setup_complete_click_ok_button(self):
        """
        Fax setup complete, click on button.
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSetupLineShareScreen)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_fax_complete_ok_button)
        self.spice.wait_until(lambda:ok_button["visible"])
        time.sleep(1)
        ok_button.mouse_click()

    def fax_recipient_screen_enter_fax_number(self, fax_number):
        """
        Purpose: From fax recipient screen to enter fax number
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: Fax number
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen, FaxAppWorkflowObjectIds.view_keyboard)
        self.enter_numeric_keyboard_values(fax_number)

    def fax_recipient_screen_enter_fax_number_with_pause(self, fax_num, fax_num2):
        """
        Purpose: From fax recipient screen to enter fax number including pause
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: Fax number + pause+ Fax number 
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen, FaxAppWorkflowObjectIds.view_keyboard)
        self.enter_numeric_keyboard_values_using_pause_key(fax_num, fax_num2)

    def goto_fax_app_home_screen(self):
        """
        Purpose: Navigates to Fax app in home screen
        Ui Flow: Home -> Fax app 
        :return: None
        """
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.2)
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()
        time.sleep(3)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
    
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
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.2)
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()
        time.sleep(2)
        if authAgent in ["admin"]:
            current_sign_type = self.spice.signIn.current_sigin_user_type()
            self.spice.signIn.select_sign_in_method_by_enum(authAgent, current_sign_type)
            self.spice.signIn.enter_credentials(login=True, password=password)
        elif authAgent in ["user", "windows", "ldap"]:
            current_sign_type = self.spice.signIn.current_sigin_user_type()
            self.spice.signIn.select_sign_in_method_by_enum(authAgent, current_sign_type)
            self.spice.signIn.enter_credentials(login=True, password=password, username = username)
        else:
            logging.info("The current user is custom user and does not need to log in.")
        #assert self.spice.wait_for(MenuAppWorkflowObjectIds.view_faxsetuphomeview)
        #self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)
        logging.info("At Fax Screen")
    
    def goto_home_fax_app_setup_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_recipient_screen_with_setup()
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)

    def goto_home_fax_app_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Skip -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_home_screen()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupSkip, FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)

    def goto_home_fax_app_setup_recipient_screen_enter_fax_number(self):
        """
        Purpose: Navigates from home screen to enter fax number in fax recipients
        Ui Flow: Home -> Fax app -> Fax Recipient screen -> Enter Fax number
        Args: None
        """
        self.goto_fax_app_home_screen()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        time.sleep(5)
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)

    def goto_home_fax_app_fax_setup_country_location(self, fax_mode:FaxModemType=FaxModemType.dungeness_bbu_modem):
        """
        UI flow:Home Screen -> Fax App -> Click Continue -> Basic Fax Setup -> Country/Location Selection view
        """
        self.spice.goto_homescreen()
        self.workflow_common_operations.scroll_to_position_horizontal(0.2)
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupContinue, FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        basic_fax_setup_view = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_basicFaxSetup)
        self.spice.wait_until(lambda: basic_fax_setup_view["visible"])
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.basic_setup_country_region, FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode])
        
    def fax_app_home_enter_fax_number_and_confirm(self, confirm_fax_number: bool = False):
        """
        Purpose: Enters fax number in enter fax number screen and Confirm then waits for job submission page
        Args: Confirm fax number: True, False: Bool
        """
        args = sys.argv[sys.argv.index('faxNumber')+1]
        faxNumber = parse_fax_arguments(args)[0]
        self.enter_numeric_keyboard_values(faxNumber)                         

        if confirm_fax_number:
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxConfirmation)
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxConfirm)
            current_button.mouse_click()
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
            key_Ok  = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
            key_Ok.mouse_click() 
            
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def click_finish_btn_on_add_page(self):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        Click Finish button on Add Page screen if no more page need scan.
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_add_page_screen)
        finish_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_finish_on_add_page)
        self.spice.wait_until(lambda: finish_button["visible"] is True)
        time.sleep(1)
        finish_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def click_add_more_btn_on_add_page(self):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        Click Add More button on Add Page screen to scan another page.
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_add_page_screen)
        add_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_add_more_on_add_page)
        add_button.mouse_click()
        time.sleep(2)
    
    def check_spec_on_add_page_screen(self, net):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        check spec on Add Page Screen.
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_add_page_screen, timeout= 30.0)

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)
        expected_title_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cAddAdditionalPages")
        actual_title_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)["text"]
        assert actual_title_str == expected_title_str, "failed to check add page screen title string"

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)
        expected_msg_scanner_glass_and_touch = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cScannerGlassAndTouch")
        #expected_msg_no_pages_to_scan = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cNoPagesToScan")
        expected_description_str = f"{expected_msg_scanner_glass_and_touch}"
        actual_description_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)["text"]
        assert expected_description_str == actual_description_str, "failed to check add page screen description string"

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_add_more_on_add_page)["visible"] == True

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_finish_on_add_page)["visible"] == True
    
    def check_spec_on_add_page_screen_enterprise(self, net):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        check spec on Add Page Screen.
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_add_page_screen)

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)
        expected_title_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "c2SidedOriginal")
        actual_title_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)["text"]
        assert actual_title_str == expected_title_str, "failed to check add page screen title string"

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)
        expected_msg_scanner_glass_and_touch = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cOriginalGlassAddDone")
        #expected_msg_no_pages_to_scan = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cNoPagesToScan")
        expected_description_str = f"{expected_msg_scanner_glass_and_touch}"
        actual_description_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)["text"]
        assert expected_description_str == actual_description_str, "failed to check add page screen description string"

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_add_more_on_add_page)["visible"] == True
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_finish_on_add_page)["visible"] == True
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_cancel_on_add_page)["visible"] == True

        

    def check_spec_on_add_page_flatbed_screen(self, net):
        """
        When do job from flatbed, Add Page screen will show by clicking Send.
        check spec on Add Page Screen.
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_add_page_screen)

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)
        expected_title_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "c2SidedOriginal")
        actual_title_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_title_text_view)["text"]
        assert actual_title_str == expected_title_str, "failed to check add page screen title string"

        self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)
        expected_msg_scanner_glass_and_touch = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cOriginalGlassAddDone")
        #expected_msg_no_pages_to_scan = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cNoPagesToScan")
        expected_description_str = f"{expected_msg_scanner_glass_and_touch}"
        actual_description_str = self.spice.wait_for(FaxAppWorkflowObjectIds.add_page_description_text_view)["text"]
        assert expected_description_str == actual_description_str, "failed to check add page screen description string"

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_add_more_on_add_page)["visible"] == True

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_finish_on_add_page)["visible"] == True
    
    def check_output_tray_closed_is_visible(self):
        """
        Output Tray Closed is shown when generate with UDW command.
        Check the screen is still visible during fax in progress.
        """
        output_tray_closed = self.spice.wait_for(FaxAppWorkflowObjectIds.view_output_tray_closed)
        self.spice.wait_until(lambda: output_tray_closed["visible"] == True)

    def click_ok_btn_on_output_tray_closed(self):
        """
        Click OK button on Output Tray Closed screen.
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_output_tray_closed)

        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.output_tray_closed_footer_ok)
        ok_button.mouse_click()

    """
    * Get the index of the media size.
    * @param mediaSize The media size string.
    * @return The index of the media size.
    """
    def getMediaSizeIndex(self, mediaSize: str):
        stop_loop = 0
        media_size_index = -1
        index = 0
        while((stop_loop == 0)):
            try:
                size_selector = self.spice.wait_for(f"#sizeRadioButton{index} #RadioButtonText")
                size_text = size_selector["text"]
                if size_text == mediaSize:
                    media_size_index = index
                    stop_loop = 1
                index = index + 1
            except Exception as error:
                stop_loop = 0
        assert media_size_index != -1, "Media size not found"
        return media_size_index

    def scan_Auto_Detection_Prompt_Select_Media_Size_continue(self, value: str):
        """
        Select media size in Auto Detection Prompt, press continue button
        Args: value: Media size value
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.scanAutoDetectionPromptConfiguration)

        sizeIndex = self.getMediaSizeIndex(value)
        self.spice.wait_for(f"#sizeRadioButton{sizeIndex}").mouse_click()

        continueButton = self.spice.wait_for(FaxAppWorkflowObjectIds.autoDetection_continueButton)
        continueButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def scan_Auto_Detection_Prompt_Select_Media_Size_cancel(self, value: str):
        """
        Select media size in Auto Detection Prompt, press cancel button and confirm the cancel prompt
        Args: value: Media size value
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.scanAutoDetectionPromptConfiguration)

        sizeIndex = self.getMediaSizeIndex(value)
        self.spice.wait_for(f"#sizeRadioButton{sizeIndex}").mouse_click()

        cancelButton = self.spice.wait_for(FaxAppWorkflowObjectIds.autoDetection_cancelButton)
        self.spice.wait_until(lambda:cancelButton["visible"])
        cancelButton.mouse_click(10,10)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPrompt)
        yesButton = self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPromptYesButton)
        yesButton.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def scan_Auto_Detection_Prompt_Select_Media_Size_cancel_dismiss(self, value: str):
        """
        Select media size in Auto Detection Prompt, press cancel, No from the cancel prompt
        Args: value: Media size value
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.scanAutoDetectionPromptConfiguration)

        sizeIndex = self.getMediaSizeIndex(value)
        self.spice.wait_for(f"#sizeRadioButton{sizeIndex}").mouse_click()

        cancelButton = self.spice.wait_for(FaxAppWorkflowObjectIds.autoDetection_cancelButton)
        self.spice.wait_until(lambda:cancelButton["visible"])
        cancelButton.mouse_click(10,10)

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPrompt)
        noButton = self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPromptNoButton)
        noButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.scanAutoDetectionPromptConfiguration)
        cancelButton = self.spice.wait_for(FaxAppWorkflowObjectIds.autoDetection_cancelButton)
        cancelButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPrompt)
        yesButton = self.spice.wait_for(FaxAppWorkflowObjectIds.flatbedCancelPromptYesButton)
        yesButton.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def verify_supported_country_region_list_display_ui(self, net, expect_country_region, fax_mode=FaxModemType.dungeness_bbu_modem.value):
        '''
        Purpose: Verify actual country/region from ews display as expected
        Args: expect_country_region : printer support country/region  
        '''
        for country in expect_country_region:
            expect_country_region_str = LocalizationHelper.get_string_translation(net, FaxCountryRegionOptionForUi[country].value)
            logging.info(f'The expect country/region string is {expect_country_region_str}')
            item_location =getattr(FaxAppWorkflowObjectIds,f"country_region_{country.lower()}")
            actual_country_region_str = self.workflow_common_operations.get_actual_str(f"{FaxAppWorkflowObjectIds.country_region_popup_list[fax_mode]} {item_location}")
            assert expect_country_region_str == actual_country_region_str, "The country/region is not in supported country/region dict"
        logging.info('The actual country/region display completely and correctly')

    def cancel_fax_setup_wizard_with_click_home_button(self,current_screen = FaxAppWorkflowObjectIds.menuText_basicFaxSetup):
        """
        Cancel Fax Setup Wizerd via home button.
        Flow should in Click Home button -- Cancel Setup screen 
        """
        logging.info("Cancel Fax Setup Wizerd via home button")
        home_button = self.spice.wait_for(f"{current_screen} {FaxAppWorkflowObjectIds.button_home}")
        self.spice.wait_until(lambda:home_button["visible"])
        home_button.mouse_click()
        cancel_setup_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_cancel_setup_screen)
        self.spice.wait_until(lambda:cancel_setup_view["visible"])
        logging.info("At Cancel Setup screen")
    
    def click_yes_button_on_cancel_setup_screen(self):
        """
        Click Yes button on Cancel Setup screen.
        Flow should in Fax Cancel Setup screen -- Click Yes button 
        """
        logging.info("Click Yes button on faxCancelSetup screen")
        yes_button_cancel_setup = self.spice.wait_for(FaxAppWorkflowObjectIds.button_fax_cancel_setup_yes)
        self.spice.wait_until(lambda:yes_button_cancel_setup["visible"])
        yes_button_cancel_setup.mouse_click()
    
    def click_ok_button_on_cancel_setup_screen(self):
        """
        Click OK button on Cancel Setup screen.
        Flow should in Fax Cancel Setup screen -- Click OK button
        """
        logging.info("Click OK button on faxCancelSetup screen")
        ok_button_cancel_setup = self.spice.wait_for(FaxAppWorkflowObjectIds.cancel_confirmation_ok_button)
        self.spice.wait_until(lambda:ok_button_cancel_setup["visible"])
        ok_button_cancel_setup.mouse_click()
    
    def verify_set_fax_receive_notification_successfully(self, fax_receive_notification):
        '''
        This is helper method to verify set fax receive notification successfully
        UI should be Menu->Settings->Fax Settings->Fax Receive
        Args: fax_receive_notification: fax receive notification
        '''
        fax_receive_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen)
        self.spice.wait_until(lambda:fax_receive_settings_view["visible"])

        self.spice.wait_until(lambda:self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_receive_notification_row} {FaxAppWorkflowObjectIds.item_fax_notifications}")["visible"])
        current_fax_receive_notification_option = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_receive_notification_row} {FaxAppWorkflowObjectIds.item_fax_notifications}")["text"]
        assert fax_receive_notification==current_fax_receive_notification_option, "Set fax receive notification failed!!!"

    def verify_set_fax_send_notification_successfully(self, fax_send_notification):
        '''
        This is helper method to verify set fax send notification successfully
        UI should be Menu->Settings->Fax Settings->Fax Send
        Args: fax_send_notification: fax send notification
        '''
        fax_send_settings_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)
        self.spice.wait_until(lambda:fax_send_settings_view["visible"])

        self.spice.wait_until(lambda:self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_send_notification_row} {FaxAppWorkflowObjectIds.item_fax_notifications}")["visible"])
        current_fax_send_notification_option = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_send_notification_row} {FaxAppWorkflowObjectIds.item_fax_notifications}")["text"]
        assert fax_send_notification==current_fax_send_notification_option, "Set fax send notification failed!!!"
  
    def click_ignore_button_on_incoming_fax(self):
        '''
        Purpose: Click Ignore button on Incoming Fax screen to reject the job.
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveStateScreen, timeout=9.0)
        ignore_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxIgnore)
        ignore_button.mouse_click()

    def click_accept_button_on_incoming_fax(self):
        '''
        Purpose: Click Accept button on Incoming Fax screen to accept the job.
        '''
        incoming_fax_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveStateScreen, timeout=9.0)
        
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_incomingFaxAccept)
        current_button.mouse_click()
        

    def is_incoming_fax_alert_visible(self, timeout=9.0):
        '''
        Purpose: check incoming fax alert display or not.
        '''
        try:
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveStateScreen, timeout=9.0)
            return True
        except Exception as err:
            return False

    def verify_set_fax_more_options_successfully(self, net, fax_option, fax_option_item):
        '''
        This is helper method to verify set fax resolution successfully
        UI should be Home->Fax->Fax More Options
        Args: fax_option: Resolution/ContentType
              fax_option_item: "Fine/SuperFine/Standard"/ "Text/Mixed/Photograph" / "Portrait/Landscape"
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_optionsScreen)
        cstring_id = ""
        fax_option_item_id = ""

        if (fax_option.lower() == "resolution"):
            fax_option_item_id = FaxAppWorkflowObjectIds.combo_box_resolution
            cstring_id = FaxAppWorkflowObjectIds.resolution_dict[fax_option_item.lower()][0]
            row_object_id = FaxAppWorkflowObjectIds.row_object_resolution
        elif (fax_option.lower() == "contenttype"):
            fax_option_item_id = FaxAppWorkflowObjectIds.combo_box_contentType
            cstring_id = FaxAppWorkflowObjectIds.content_type_dict[fax_option_item.lower()][0]
            row_object_id = FaxAppWorkflowObjectIds.row_object_contentType
        elif (fax_option.lower() == "contentorientation"):
            fax_option_item_id = FaxAppWorkflowObjectIds.settings_content_orientation
            cstring_id = FaxAppWorkflowObjectIds.content_orientation_dict[fax_option_item.lower()][0]
            row_object_id = FaxAppWorkflowObjectIds.row_object_content_orientation
        else:
            assert False, "Fax option not existing"
        time.sleep(3)
        ui_fax_option_item_string = self.spice.wait_for(f"{row_object_id} {fax_option_item_id} {FaxAppWorkflowObjectIds.content_item}")["text"]
        logging.info(f"Get current option <{fax_option}> is {ui_fax_option_item_string}")
        expected_string = LocalizationHelper.get_string_translation(net, cstring_id)
        assert ui_fax_option_item_string == expected_string, f"Setting value <{ui_fax_option_item_string}> mismatch"
    
    def click_ok_btn_on_junk_fax_number_removed(self):
        """
        Click OK button on Junk Fax Number Removed screen.
        """
        junk_fax_number_removed = self.spice.wait_for(FaxAppWorkflowObjectIds.view_junk_fax_number_removed)
        self.spice.wait_until(lambda: junk_fax_number_removed["visible"] == True)

        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_junk_fax_number_removed)
        ok_button.mouse_click()

    def goto_menu_fax_faxsetup_phoneline(self):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup ->Phone Line Not Connected Screen
        Args: None
        """
        self.homemenu.goto_menu_settings_fax(self.spice)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSetupMenuButton)
        current_button.mouse_click()
        sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected)["visible"] == True
        sleep(2)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected_ok_button)
        ok_button.mouse_click()

    def goto_menu_dualfax_faxsetup_phoneline(self,line="line1"):
        """
        Purpose: Navigates from home menu settings to fax setup screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Setup ->Phone Line Not Connected Screen
        Args: None
        """
        if line.lower() == "line2":
            lineselection = (FaxAppWorkflowObjectIds.view_faxSetupMenuLine2)
            
        elif line.lower() == "line1":
            lineselection = (FaxAppWorkflowObjectIds.view_faxSetupMenuLine1)
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.homemenu.goto_menu_settings_fax(self.spice)

        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxSetupMenuButton, FaxAppWorkflowObjectIds.menuText_FaxSetup)
        current_button = self.spice.wait_for(lineselection)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected)
        #self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected)["visible"] == True
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_phoneline_not_connected_ok_button)
        ok_button.mouse_click()

    def fax_back_button_press(self):
        """
        Purpose: Press back button to go back the home screen from the fax landing screen
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_back)
        current_button.mouse_click()
    def fax_multiple_recipients_send_to_contacts_search_icon(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app for search contact in local address
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact -> Serach Icon
        """
        #self.goto_fax_app_recipient_screen()
        self.goto_fax_app_recipient_screen_with_setup()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        sleep(2)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.search_icon)
        current_button.mouse_click()

    def fax_configured_multiple_recipients_send_to_contacts_search_icon(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app for search contact in local address
        Ui Flow: Main Menu -> Fax -> Basic Fax Setup -> Fax Recipients screen -> Sent to Contacts -> local contact -> Serach Icon
        """
        self.goto_fax_app_recipient_screen_with_setup()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        sleep(2)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.search_icon)
        current_button.mouse_click()
    
    def fax_clear_activitylogs(self):
        """
        Goto troubleshooting fax and clear fax logs
        """
        currentScreen = self.spice.wait_for(FaxAppWorkflowObjectIds.troubleshooting_fax_view_screen)
        assert currentScreen

        # validate clear button
        currentElement = self.spice.wait_for(FaxAppWorkflowObjectIds.troubleshooting_fax_clearlogs_clear_button)
        currentElement.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.troubleshooting_fax_toastwindow)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.troubleshooting_fax_toastinfo)["text"] == "Success"

    def fax_custom_address_book(self):
        """
        Purpose: Navigates from home screen to fax recipient coustom contacts selection screen in fax app and press search Icon
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        self.goto_fax_app_recipient_screen()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_custom, FaxAppWorkflowObjectIds.view_FaxcustomSelectScreen)
        sleep(2)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.search_icon)
        current_button.mouse_click()

    def fax_configured_custom_address_book(self):
        """
        Purpose: Navigates from home screen to fax recipient coustom contacts selection screen in fax app and press search Icon
        Ui Flow: Main Menu -> Fax -> Basic Fax Setup -> Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        self.goto_fax_app_recipient_screen_with_setup()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_custom, FaxAppWorkflowObjectIds.view_FaxcustomSelectScreen)
        sleep(2)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.search_icon)
        current_button.mouse_click()

    def fax_multiple_recipients_send_to_contacts_custom_contact(self,payload_list):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen in fax app when
        there are no contacts created.
        Enters multiple fax number if user selects "Yes" and Cancel fax when user selects "No"
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts ->
            If "Yes" Enter fax Num
            If "No" navigated back to fax recipient.
        Args: fax_number_list which is provided on the test case and Yes/No
        """
        for payload in payload_list:
            AddressBook_name = payload["displayName"]
            addressBook_name_locator = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
            time.sleep(2)
            if (self.spice.wait_for(addressBook_name_locator)["checked"] == False):
                self.spice.wait_for(addressBook_name_locator, timeout = 10.0)
                checkbox_contact = self.spice.wait_for(addressBook_name_locator)
                checkbox_contact.mouse_click()
                assert self.spice.wait_for(addressBook_name_locator)["checked"] == True, 'Contact is not checked'
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def fax_select_custom_address_book(self, custom_address_name):
        """
        Purpose: Navigates from home screen to fax recipient coustom contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook
        Args:custom_address_name: user created custom address book name
        """
        self.goto_fax_without_skip_button()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        custom_address_local = "#addressbook_" + custom_address_name + " #SpiceRadioButton"
        custom_address_button = self.spice.wait_for(custom_address_local)
        custom_address_button.mouse_click()

    def select_ldap_address_book(self):
        """
        Purpose: Navigates from home screen to fax recipient ldap contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> ldap addressbook
        """
        self.goto_fax_without_skip_button()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        ldap_address_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_ldap)
        self.spice.wait_until(lambda: ldap_address_button['visible'])
        time.sleep(1)
        ldap_address_button.mouse_click()

    def input_pin_code_for_custom_addressbook(self, pincode):
        """
        Purpose: input pincode for custom addressbook if pincode is set for custom addressbook.
        UI should be in: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> custom addressbook
        Args:pincode: 
        """
        pin_code_editor = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_access_code)
        pin_code_editor.mouse_click()
        pin_code_editor.__setitem__('displayText', pincode)

        keyboard_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.press_key_ok)
        keyboard_ok_button.mouse_click()
    
    def check_invalid_pin_code_view_and_click_ok_button(self, net):
        """
        Purpose: check invalid pin code view and click ok button 
        """
        self.spice.common_operations.verify_string(net, "cRetryPassword", FaxAppWorkflowObjectIds.alert_description, isSpiceText=True)

        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_alert_description)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()
    
    def click_submit_button_input_pin_code_view(self):
        """
        Purpose: click submit button when input pin code for custom addressbook
        """
        pin_code_submit_button = self.spice.wait_for(FaxAppWorkflowObjectIds.press_access_code_done)
        self.spice.validate_button(pin_code_submit_button)
        pin_code_submit_button.mouse_click()

    def fax_contact_search_modal_button(self):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact/Custom Contact -> Serach Icon -> Serach Icon
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_contact_search_model_button)
        current_button.mouse_click()
        sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.faxAddressbook_select_error_msg)["visible"] == True
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
        current_button.mouse_click()

    def fax_address_contact_search_and_reset(self,name=str):
        """
        Purpose: Navigates from home screen to fax recipient contacts selection screen
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts -> local contact/Custom Contact -> Serach Icon -> Enter Contact->Serach Icon -> Reset
        """
        logging.info("At expected fax recipient contacts selection view")
        self.search_contact_from_contact_address_book(name)
        time.sleep(2)
        # Todo change reset button object id
        reset_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_contact_reset_button)
        reset_button.mouse_click()
        time.sleep(2)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contacts_integration)
    
    def goto_fax_call_history_addressbook(self):
        """
        Goto fax call history addressbook
        Ui should in fax landing view, UI flow is click Sent to Contacts button -> select Call History
        """
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_fax_addressbook_call_history, FaxAppWorkflowObjectIds.view_FaxcustomSelectScreen)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contacts_integration)
    
    def click_cancel_button_in_select_contacts_view(self):
        """
        Click cancel button in select contacts view
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contacts_integration)
        current_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_FaxcustomSelectScreen} {FaxAppWorkflowObjectIds.button_faxAddressbook_name_cancel}")
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
    
    def select_multi_fax_contacts_from_call_history(self, fax_contacts_list):
        """
        Selects fax contacts in contacts intergration view
        Ui should in contacts intergration view (Fax -> Skip -> Fax Recipients screen -> click Sent to Contacts button -> select a address book)
        Args: fax_contacts_list
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        for fax_number in fax_contacts_list:
            fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
            time.sleep(2)
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view)
            current_button = self.spice.wait_for(fax_contact_model)
            current_button.mouse_click()
        
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def select_multi_fax_contacts_from_call_history_with_same_contacts(self, fax_contacts_list):
        """
        Selects fax contacts in contacts intergration view, fax contacts with same contacts
        Ui should in contacts intergration view (Fax -> Skip -> Fax Recipients screen -> click Sent to Contacts button -> select a address book)
        Args: fax_contacts_list
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        duplicate_number_list = list(set([x for x in fax_contacts_list if fax_contacts_list.count(x) > 1]))
        no_duplicate_number_list= list(set(fax_contacts_list))
        for fax_number in no_duplicate_number_list:
            fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
            time.sleep(2)
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view)
            current_button = self.spice.wait_for(fax_contact_model)
            current_button.mouse_click()
            time.sleep(1)
            assert current_button["checked"] == True, f"Failed to select contacts: <{fax_number}>"

        if len(duplicate_number_list)!= 0:
            for fax_number in duplicate_number_list:
                fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
                fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
                time.sleep(2)
                current_button = self.spice.query_item(fax_contact_model, 1)
                current_button.mouse_click()
                time.sleep(1)
                while current_button["checked"] != True:
                    height = self.spice.query_item(fax_contact_row)["height"]
                    view_content_y = self.spice.query_item(FaxAppWorkflowObjectIds.view_fax_contact_list_view)["contentY"]
                    self.spice.query_item(FaxAppWorkflowObjectIds.view_fax_contact_list_view)["contentY"] = view_content_y + height
                    current_button = self.spice.query_item(fax_contact_model, 1)
                    current_button.mouse_click()

                assert current_button["checked"] == True, f"Failed to select contacts: <{fax_number}>"

        select_button = self.spice.query_item(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def select_multi_callhistory_for_junkfaxblock(self, expected_fax_record_list):
        """
        Check Received call history shows in Blocked Fax screen under Received Call history.
        @param: expected_fax_record_list:
        @return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_ReceivedCallHistoryScreen)
        # Wait all contacts load completed
      
        for fax_number in expected_fax_record_list:
            fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
            time.sleep(2)
            """
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_received_callhistory_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_receivedcallhistory_list_view)
            """
            current_button = self.spice.wait_for(fax_contact_model)
            current_button.mouse_click()
        
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_receivedCallHistory_add_select)
        select_button.mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_soho_screen)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_soho_junk_fax_number)
        ok_button.mouse_click()
        self.click_numbers_added_to_junk_list_ok_button()

        logging.info(f"Check contacts name list {expected_fax_record_list} success")

    def check_multi_callhistory_for_junkfaxblock(self, expected_fax_record_list):
        """
        Check specific received call history in Blocked Fax screen under Received Call history.
        @param: expected_fax_record_list:
        @return: True, False
        """
        try:
            self.spice.wait_for(FaxAppWorkflowObjectIds.view_ReceivedCallHistoryScreen)
        except Exception as e:
            logging.info(f"view_ReceivedCallHistoryScreen not visible. Exception is {e}")
            return False

        # Wait all contacts load completed
      
        for fax_number in expected_fax_record_list:
            fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
            time.sleep(2)
            """
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_received_callhistory_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_receivedcallhistory_list_view)
            """
            current_button = self.spice.wait_for(fax_contact_model)
            logging.info(f"-found: {fax_contact_row}")
            logging.info(f"-found: {fax_contact_model}")
            logging.info(f"-found: {current_button}")
        logging.info(f"Check received call history for junfaxblock {expected_fax_record_list} success")
        if current_button:
            return True
        else:
            return False 

    def select_multi_callhistory_to_check_max_limit_of_BlockedFax(self, expected_fax_record_list):
        """
        Check Received call history shows in Blocked Fax screen under Received Call history.
        @param: expected_fax_record_list:
        @return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_ReceivedCallHistoryScreen)
        # Wait all contacts load completed
      
        for fax_number in expected_fax_record_list: 
            fax_contact_model = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Model'
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + fax_number + 'Row'
            time.sleep(3)
            """
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_received_callhistory_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_receivedcallhistory_list_view)
            """

            current_button = self.spice.wait_for(fax_contact_model)
            current_button.mouse_click()

        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_receivedCallHistory_add_select)
        select_button.mouse_click()

        logging.info(f"Check contacts name list {expected_fax_record_list} success")
                    
    def check_fax_call_history_display_in_contacts_list_view(self, expected_fax_record_list):
        """
        Check fax call history record showss in call history contact list view screen.
        @param: expected_fax_record_list:
        @return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
        # Wait all contacts load completed
        sleep(2)

        for contacts_name in expected_fax_record_list:
            fax_contact_row = FaxAppWorkflowObjectIds.addressbook_name_common + contacts_name + 'Row'
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, fax_contact_row, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view)
            self.spice.wait_for(fax_contact_row)
            logging.info(f"-found: {fax_contact_row}")
        
        logging.info(f"Check contacts name list {expected_fax_record_list} success")
    
    def check_spec_no_contacts_in_list(self, net):
        '''
        Check spec no contacts in list when no contacts in contacts list
        '''
        logging.info("Check spec no contacts in list when no contacts in contacts list")
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contact_list_view)
        actual_text = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.text_view_empty_record} {FaxAppWorkflowObjectIds.spice_text_view}")["text"]
        expected_text = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, "cNoContactsInList")
        assert actual_text == expected_text, "Failed to check spec no contacts in list"

    def goto_menu_fax_receive_settings_fax_printing_select(self, option):
        #colorMode on landing
        self.goto_menu_fax_receive_settings_fax_printing()
        time.sleep(5)
        if option == "Always Print":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_always_print)
        elif option == "Store and Print":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_store_and_print)
        elif option == "Always Store":
            current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_printing_option_screen_alwaysstore_radiobutton)
        else:
            raise Exception(f"Invalid fax printing type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)

    def goto_menu_fax_receive_settings_fax_printing(self):
        self.goto_menu_fax_receive_settings()
        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(0.7, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        fax_printing = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_option)
        fax_printing.mouse_click()
    
    def get_fax_receive_settings_fax_printing_value(self):
        """
        Get fax receive setting fax printing text
        UI should in menu fax receive setting screen.
        @return: fax_print_value
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettingsScreen)
        time.sleep(5)
        self.workflow_common_operations.scroll_vertical_row_item_into_view(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_option, select_option=False)
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_option)

        fax_print_value = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_receive_fax_printing_options} {FaxAppWorkflowObjectIds.content_item}")["text"]

        return fax_print_value
    
    def check_fax_receive_settings_fax_printing_value(self, expected_value):
        """
        Check fax receive setting fax printing text
        @param: expected_value, "Always Print"/"Store and Print"
        """
        get_text = self.get_fax_receive_settings_fax_printing_value()

        assert get_text == expected_value, "Error - check fax printing value failed"

    def select_multiple_contacts_from_custom_addressbook(self,payload_list):
        AddressBook_name = payload_list['displayName']
        addressBook_name_locator = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
        time.sleep(2)
        while (self.spice.wait_for(addressBook_name_locator)["checked"] == False):
            current_button = self.spice.wait_for(addressBook_name_locator + ' MouseArea')
            self.spice.wait_until(lambda: current_button["visible"] == True)
            current_button.mouse_click()
            assert self.spice.wait_for(addressBook_name_locator)["checked"] == True, 'Contact is not checked'
        select_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxAddressbook_name_select)
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def has_lock_icon(self):
        # Must be on Menu page
        try:
            lock_icon = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax + " #statusIconRect SpiceLottieImageView")
        except:
            logging.info("Failed to find lock icon")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return True
    
    def scroll_contact_or_group_item_into_view(self, screen_id, row_item_id, scroll_bar, footer_item_id=None, scroll_height=66, top_item_id=None):
        """
        Scroll contact/group into center of sceen that the user could click it/select it and no need to always from the first item, then could get the item quickly when
        have lots of items. One more thing, there are 2 screen to show 100 contacts
        @param: screen_id: object name for screen that contains all list item
                row_item_id: object name for row
                scroll_bar: object name scroll bar 
                footer_item_id: object name for footer view, keep it as None if it does not inculded in scroll view
        """
        logging.info(f"Try to scroll <{row_item_id}> into view of screen <{row_item_id}>")
        current_screen = self.spice.wait_for(screen_id)
        at_y_end = False
        is_visible = False
        while(is_visible is False and at_y_end is False):
            try:
                is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id, top_item_id=top_item_id)
                while (is_visible is False and at_y_end is False):
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, scroll_height)
                    is_visible = self.workflow_common_operations.validate_list_object_is_in_vertical_screen_view(screen_id, row_item_id, footer_item_id, top_item_id=top_item_id)
                    at_y_end = current_screen["atYEnd"]
            except Exception as err:
                logging.info(f"exception msg {err}")
                if str(err).find("Query selection returned no items") != -1:
                    self.workflow_common_operations.scroll_screen_via_height(screen_id, scroll_height)
                    at_y_end = current_screen["atYEnd"]
                else:
                    raise Exception(err)

        logging.info(f"The item <{row_item_id}> is in screen view <{screen_id}> now: <{is_visible}>")

        return is_visible

    def goto_fax_app_fax_options_schedule_now(self):
        """
        Purpose: Navigates to fax options screen from job submission page
        Ui Flow: fax job Submission screen -> Fax Options->Send Now
        Args: None
        """
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_optionsScreen, FaxAppWorkflowObjectIds.fax_schedule_view, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxOptions)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_schedule_screen_view)
    
    def fax_send_now_min_set(self, value):
        """
        Purpose: Sets the scheduled minute value for sending a fax job
        Ui Flow: fax job Submission screen -> Fax Options->Send Now -> Adding minute value
        :return: None
        """
        time.sleep(10)
        min_set = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_now_set_min_value)
        min_set.__setitem__('value', value)

    def fax_send_now_hr_set(self, value):
        """
        Purpose: Sets the hour value for scheduled fax sending
        Ui Flow: fax job Submission screen -> Fax Options->Send Now -> Set hour value
        :return: None
        """
        time.sleep(10)
        min_set = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_now_set_hr_value)
        min_set.__setitem__('value', value)
    
    def get_now_min_value(self):
        """
        Purpose: get schedual now min value
        Ui Flow: fax job Submission screen -> Fax Options->Send Now
        :return: min_value
        """
        time.sleep(3)
        min_set_input = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_send_now_set_min_value} {FaxAppWorkflowObjectIds.fax_send_now_text_input}")
        min_value = min_set_input["text"]
        return min_value

    def get_now_hr_value(self):
        """
        Purpose: get schedual now hr value
        Ui Flow: fax job Submission screen -> Fax Options->Send Now
        :return: hr_value
        """
        time.sleep(3)
        hr_set_input = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_send_now_set_hr_value} {FaxAppWorkflowObjectIds.fax_send_now_text_input}")
        hr_value = hr_set_input["text"]
        return hr_value

    def fax_schedule_later_done_button(self):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: fax job Submission screen -> Fax Options->Send Now -> Adding Min values- > Done
        :return: None
        """
        Press_done = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_schedule_done)
        Press_done.mouse_click()

    def fax_schedule_later_reset_button(self):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: fax job Submission screen -> Fax Options->Send Now -> Adding Min values- > reset
        :return: None
        """
        Press_done = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_schedule_reset)
        Press_done.mouse_click()

    def send_later_enter_numeric_keyboard_values(self, number, OK_locator= FaxAppWorkflowObjectIds.keyOK):
        faxNumberTextField = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen} {FaxAppWorkflowObjectIds.textField_mouse_area}")
        faxNumberTextField.mouse_click(10)
        time.sleep(5)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        for i in  range(len(number)):
            num = number[i]
            logging.info(num)
            key = self.spice.wait_for(FaxAppWorkflowObjectIds.key_board_keys + num)
            key.mouse_click()
        key_Ok  = self.spice.wait_for(OK_locator)
        key_Ok.mouse_click()

    def fax_schedule_cancel_button(self):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: fax job Submission screen -> Fax Options->Send Now -> Cancel
        :return: None
        """
        Press_cancel = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_send_cancel)
        Press_cancel.mouse_click()
    
    def click_search_button_on_fax_contact_screen(self):
        """
        Click Search button under fax contact screen
        """
        logging.info("Click Search button under fax contact screen")
        search_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_fax_contacts_integration} {FaxAppWorkflowObjectIds.search_icon}")
        self.spice.wait_until(lambda:search_button['visible'])
        time.sleep(1)
        search_button.mouse_click()

    def click_search_button_on_fax_contact_search_screen(self):
        """
        Click Search button on fax contact search screen
        """
        logging.info("Click Search button on fax contact search screen")
        search_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_fax_contacts_integration} {FaxAppWorkflowObjectIds.search_icon}")
        self.spice.wait_until(lambda:search_button['visible'])
        time.sleep(1)
        search_button.mouse_click()

    def search_contact_from_contact_address_book(self, search_text):
        """
        Search contact from address book
        """
        logging.info("Search contact from address book")
        text_input_box = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_fax_contacts_integration} {FaxAppWorkflowObjectIds.fax_contact_search_text_input_box}")
        self.spice.wait_until(lambda: text_input_box["visible"])
        time.sleep(1)
        text_input_box.mouse_click()
        time.sleep(1)
        search_input_view = self.spice.wait_for(FaxAppWorkflowObjectIds.text_field_search_input)
        search_input_view.__setitem__('displayText', search_text)
        time.sleep(1)
        self.spice.wait_for(FaxAppWorkflowObjectIds.key_hide_keyboard).mouse_click()
        search_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_search)
        self.spice.validate_button(search_button)
        search_button.mouse_click()
        logging.info("Wait search result to load")
        time.sleep(3)

    def select_multiple_contacts_from_search_result(self, display_name_list):
        """
        Select multiple contacts from ldap search result
        @param display_name_list: ["display_name1, display_name2"]
        """
        logging.info("Select multiple contacts from ldap search result")
        display_name_list = sorted(display_name_list)
        for item in display_name_list:
            logging.info(f"Select multiple contacts from ldap search result <{item}>")
            row_item = f"#checkBox_{item}Row"
            is_visible = self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, row_item, None, footer_item_id = None, top_item_id = FaxAppWorkflowObjectIds.search_result_section)
            assert is_visible, f"{row_item} is not in the view of screen and could be selected"
            check_box_button = self.spice.wait_for(f"#checkBox_{item}Model")
            check_box_button.mouse_click()
            self.spice.wait_until(lambda:check_box_button["checked"])
    
    def click_select_on_search_result_screen(self):
        """
        Click Select button on search result screen
        """
        logging.info("Click Select button on ldap search result screen")
        select_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_fax_contacts_integration} {FaxAppWorkflowObjectIds.button_faxAddressbook_name_select}")
        select_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)

    def select_multiple_contacts_from_ldap_address_book(self, display_name_list, search_text):
        """
        Select multiple contacts from ldap search result
        @param display_name_list: ["display_name1, display_name2"]
        @param search_text: "display_name"
        """
        self.select_ldap_address_book()
        self.click_search_button_on_fax_contact_screen()
        self.search_contact_from_contact_address_book(search_text)
        time.sleep(10)
        self.select_multiple_contacts_from_search_result(display_name_list)
        self.click_select_on_search_result_screen()

    def fax_app_set_include_cover_page(self, enable_status=True):
        """
        Enable/Disable option include cover page
        """
        is_visible = self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_optionsScreen, FaxAppWorkflowObjectIds.switch_includecoverpage_row, None, top_item_id=FaxAppWorkflowObjectIds.fax_option_header_setion)
        assert is_visible, "Cannot Enable/Disable option include cover page since it does not show in view of screen that could click"

        include_cover_page_button = self.spice.wait_for(FaxAppWorkflowObjectIds.switch_includecoverpage_button)
        current_status = include_cover_page_button["checked"]
        logging.info(f"Current status is <{current_status}>")

        if enable_status:
            if current_status:
                logging.info(f"No need to update its status since it is already in <{current_status}>")
            else:
                include_cover_page_button.mouse_click(10,10)
                self.spice.wait_until(lambda: include_cover_page_button["checked"])
                time.sleep(2)
        else:
            if current_status:
                include_cover_page_button.mouse_click(10,10)
                self.spice.wait_until(lambda: not include_cover_page_button["checked"])
                time.sleep(2)
            else:
                logging.info(f"No need to update its status since it is already in <{current_status}>")
        logging.info(f'Current status is <{include_cover_page_button["checked"]}>')
        assert include_cover_page_button["checked"] == enable_status, "Failed to update include_cover_page"
    
    def fax_app_verify_include_cover_page_constrained(self,):
        """
        Verify include cover page is constrained
        """
        is_visible = self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_optionsScreen, FaxAppWorkflowObjectIds.switch_includecoverpage_row, None, top_item_id=FaxAppWorkflowObjectIds.fax_option_header_setion)
        assert is_visible, "Cannot Enable/Disable option include cover page since it does not show in view of screen that could click"

        include_cover_page_button = self.spice.wait_for(FaxAppWorkflowObjectIds.switch_includecoverpage_button)
        include_cover_page_button.mouse_click(10,10)

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message, timeout = 2.0)
        okButton = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(2)

    def get_fax_color_option(self):
        """
        Get fax color option
        """
        color_option = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item}")
        self.spice.wait_until(lambda: color_option["visible"])
        time.sleep(2)
        value =  self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item} {FaxAppWorkflowObjectIds.content_item}")["text"]
        logging.info(f"The value of color_option_button is <{value}>")
        return value
    
    def set_fax_color_option(self, color_option, net):
        """
        Set fax color option
        @param color_option grayscale/color
        """
        current_value = self.get_fax_color_option()
        color_dict = {
            "grayscale": "cChromaticModeGrayscale",
            "color": "cColor"
        }

        if current_value == LocalizationHelper.get_string_translation(net, color_dict[color_option]):
            logging.info(f"No need to change fax color option, since current value is already <{current_value}>")
            return 
        else:
            if "grayscale" == color_option:
                option_object = FaxAppWorkflowObjectIds.fax_options_grayscale
            else:
                option_object = FaxAppWorkflowObjectIds.fax_options_color
        
        self.workflow_common_operations.scroll_vertical_row_item_into_view(FaxAppWorkflowObjectIds.view_optionsScreen, FaxAppWorkflowObjectIds.fax_colormodesettingscomboBox_row, select_option=False, top_item_id=FaxAppWorkflowObjectIds.fax_option_header_setion)
        color_option_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_optionsScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item}")
        color_option_button.mouse_click()

        option_item = self.spice.wait_for(option_object)
        self.spice.wait_until(lambda: option_item["visible"])
        time.sleep(2)
        option_item.mouse_click()
        current_value = self.get_fax_color_option()
        assert current_value == LocalizationHelper.get_string_translation(net, color_dict[color_option]), "Failed to Set fax color option"
        logging.info(f"Success to Set fax color option to <{color_option}>")
    

    def get_fax_color_option_in_landing_view(self):
        """
        Get fax color option in fax landing view
        """
        color_option = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item}")
        self.spice.wait_until(lambda: color_option["visible"])
        time.sleep(2)
        value =  self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item} {FaxAppWorkflowObjectIds.content_item}")["text"]
        logging.info(f"The value of color_option_button is <{value}>")
        return value
    
    def set_fax_color_option_in_landing_view(self, color_option, net):
        """
        Set fax color option in fax landing view
        @param color_option grayscale/color
        """
        current_value = self.get_fax_color_option_in_landing_view()
        color_dict = {
            "grayscale": "cChromaticModeGrayscale",
            "color": "cColor"
        }

        if current_value == LocalizationHelper.get_string_translation(net, color_dict[color_option]):
            logging.info(f"No need to change fax color option, since current value is already <{current_value}>")
            return 
        else:
            if "grayscale" == color_option:
                option_object = FaxAppWorkflowObjectIds.fax_options_grayscale
            else:
                option_object = FaxAppWorkflowObjectIds.fax_options_color
        
        self.workflow_common_operations.scroll_vertical_row_item_into_view(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen, FaxAppWorkflowObjectIds.fax_colormodesettingscomboBox_row, select_option=False, footer_item_id=FaxAppWorkflowObjectIds.footer_view, top_item_id=FaxAppWorkflowObjectIds.fax_option_header_setion)
        color_option_button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen} {FaxAppWorkflowObjectIds.fax_scan_colormodecomboBox_item}")
        color_option_button.mouse_click()

        option_item = self.spice.wait_for(option_object)
        self.spice.wait_until(lambda: option_item["visible"])
        time.sleep(2)
        option_item.mouse_click()
        current_value = self.get_fax_color_option_in_landing_view()
        assert current_value == LocalizationHelper.get_string_translation(net, color_dict[color_option]), "Failed to Set fax color option"
        logging.info(f"Success to Set fax color option to <{color_option}> in landing view")

    def click_cancel_button_on_colorfax_alert_screen(self):
        """
        Click cancel button on Color Fax Alert Screen
        """
        button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_color_mode_alert} {FaxAppWorkflowObjectIds.button_color_cancel_mode_alert}")
        time.sleep(2)
        button.mouse_click()

        logging.info("Click cancel button on Color Fax Alert Screen")

    def click_ok_button_on_colorfax_alert_screen(self):
        """
        Click ok button on Color Fax Alert Screen
        """
        button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_color_mode_alert} {FaxAppWorkflowObjectIds.ok_button_color_mode_alert}")
        button.mouse_click()

        logging.info("Click ok button on Color Fax Alert Screen")
    
    def colorfax_alert_ecm_screen_displayed(self, net):
        """
        Color Fax alert ECM screen is displayed
        """
        screen = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.alert_content}")
        time.sleep(2)
        expected_str = LocalizationHelper.get_string_translation(net, "cSendColorFaxECMOn")
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.alert_content} #contentItem")["text"]
        assert actual_str == expected_str, f"Failed to check Color Fax alert ECM screen is displayed expected_str is <{expected_str}>, actual is <{actual_str}>"

    def colorfax_not_supported_screen_displayed(self, net):
        """
        Color Fax not supported screen is displayed
        """
        assert self.spice.wait_for(f"{FaxAppWorkflowObjectIds.color_fax_not_supported_body}", timeout = 40)
        time.sleep(2)
        expected_str = LocalizationHelper.get_string_translation(net, "cColorFaxNotSupported")
        actual_str = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.color_fax_not_supported_body}")["text"]
        assert actual_str == expected_str, f"Failed to checkColor Fax not supported screen is displayed expected_str is <{expected_str}>, actual is <{actual_str}>"
        logging.info("Color Fax not supported screen is displayed")


    def click_ok_button_on_color_fax_not_supported_screen(self):
        """
        Click ok button on color fax not supported screen
        """
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_on_color_fax_not_supported)
        time.sleep(2)
        ok_button.mouse_click()
        logging.info("Click ok button on color fax not supported screen")

    def click_send_on_colorfax_alert_screen(self):

        """
        Click send button on Color Fax Alert Screen
        """
        self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_color_mode_alert} {FaxAppWorkflowObjectIds.send_button_color_mode_alert}")
        current_button=self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_color_mode_alert} {FaxAppWorkflowObjectIds.send_button_color_mode_alert}")
        current_button.mouse_click()
        logging.info("Click ok button on Color Fax Alert Screen")

    def colorfax_alert_turn_off_scan_and_fax_method_screen_displayed(self, net):
        """
        colorfax alert turn off scan and fax method screen is displayed
        """
        screen = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.alert_content}")
        self.spice.wait_until(lambda: screen["visible"])
        time.sleep(2)
        expected_body_str = LocalizationHelper.get_string_translation(net, "cTurnOffScanFaxMethod")
        actual_body_str = self.spice.wait_for(FaxAppWorkflowObjectIds.alert_content + " #contentItem")["text"]
        assert expected_body_str == actual_body_str, f"Failed to check colorfax alert turn off scan and fax method screen is displayed expected_body_str is <{expected_body_str}>, actual_body_str is <{actual_body_str}>"

    def colorfax_alert_scheduled_fax_not_support_color_screen_displayed(self, net):
        """
        colorfax alert scheduled fax not support color screen is displayed
        """
        screen = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.alert_content}")
        self.spice.wait_until(lambda: screen["visible"])
        time.sleep(2)
        expected_body_str = LocalizationHelper.get_string_translation(net, "cScheduledFaxGrayscale")
        actual_body_str = self.spice.wait_for(FaxAppWorkflowObjectIds.alert_content+ " #contentItem")["text"]
        assert expected_body_str == actual_body_str, f"Failed to check colorfax alert scheduled fax not support color screen is displayed expected_body_str is <{expected_body_str}>, actual_body_str is <{actual_body_str}>"

    def click_send_button_on_scheduled_fax_not_support_color_screen(self):
        """
        Click send button on Color Fax Alert scheduled fax not support color Screen
        """
        button = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.fax_color_mode_alert} {FaxAppWorkflowObjectIds.send_button_color_mode_alert}")
        button.mouse_click()

        logging.info("Click send button on Color Fax Alert scheduled fax not support color Screen")

    def verify_printer_user_screen_for_locked_fax_app_from_menu(self):
        """
	    UI should be on menu screen before calling this method
        Navigate to Menu -> Fax with Guest and disable fax permissions from EWS > Security > Access Control, check printer user screen pop up
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage)
        fax_app = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax + " MouseArea")
        fax_app.mouse_click()

        self.spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
        logging.info("At Printer User Screen")

    def verify_printer_user_screen_for_locked_fax_app_from_home(self):
        """
	    UI should be on home screen before calling this method
        Navigate to Home -> Fax with Guest and disable fax permissions from EWS > Security > Access Control, check printer user screen pop up
        """
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()

        self.spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
        logging.info("At Printer User Screen")
		
    def has_lock_icon_home(self):
        """
	    UI should be on home screen before calling this method
        Navigate to Home with Guest and disable fax permissions from EWS > Security > Access Control, check fax lock icon display
        """
        try:
            if self.spice.uitype != "Workflow2":
                self.workflow_common_operations.scroll_to_position_horizontal(0.2)
                lock_icon = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " #statusIconRect SpiceLottieImageView")
            else :
                self.spice.home_operations.home_navigation(FaxAppWorkflowObjectIds.fax_app_home,select_option=False)
                lock_icon = self.spice.wait_for(FaxAppWorkflowObjectIds.home_swipe_view +" "+ FaxAppWorkflowObjectIds.fax_app_home + " #statusIconRect SpiceLottieImageView")

        except:
            logging.info("Failed to find lock icon")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return True

    def verify_lock_icon(self, propertyId: str, on_click: str = None):
        """
        Verify lock icon is on
        @param objectId: object id of a particular option with respect to the objectId passed
        """
        lock_icon_validator = self.spice.wait_for(propertyId, timeout=15.0)
        assert lock_icon_validator["visible"] == True, f"For {propertyId} lock icon is not visible"
        assert lock_icon_validator["locked"] == True, f"For {propertyId} is not locked"

        lock_icon_validator.mouse_click(5, 5)

        if on_click != None:
            # If on_click is provided, it means we need to click on the lock icon
            # and verify the expected behavior after clicking.
            self.spice.wait_for(on_click, timeout=15.0)
            assert self.spice.wait_for(on_click)["visible"] == True, f"Expected screen {on_click} is not visible after clicking lock icon"

    def verify_restricted_access_message_and_click_on_ok_button(self):
        """
        Verify restricted access message and click on OK button
        """
        restricted_access_message = self.spice.wait_for(FaxAppWorkflowObjectIds.restricted_access_alert_message, timeout = 15.0)
        assert restricted_access_message["visible"] is True, "Restricted access message is not visible"
        logging.info("Restricted access message is visible")
        
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.restricted_access_alert_message_ok_button, timeout = 15.0)
        ok_button.mouse_click()
        logging.info("Clicked on OK button on restricted access message")

    def verify_fax_locked_view_screen_for_printer_user_from_home(self, net):
        """
	    UI should be on home screen before calling this method
        Navigate to home screen with printer user and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up
        """
        fax_app = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home + " MouseArea")
        fax_app.mouse_click()
        self.verify_restricted_alert_string(net)
        assert self.spice.signIn.verifyPermissionEnforced(expected = False) is True, "Unexpected screen"
        logging.info("At Fax Locked View Screen")

    def verify_fax_locked_view_screen_for_printer_user_from_menu(self, net):
        """
	    UI should be on menu screen before calling this method
        Navigate to menu screen with printer user and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.1, MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage)
        fax_app = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_fax + " MouseArea")
        fax_app.mouse_click()
        self.verify_restricted_alert_string(net)
        assert self.spice.signIn.verifyPermissionEnforced(expected = False) is True, "Unexpected screen"
        logging.info("At Fax Locked View Screen")

    def click_ok_btn_on_fax_locked_view_screen(self):
        """
        Navigate to home screen and disable fax permissions from EWS > Security > Access Control, fax locked view screen pop up.
        Click OK button on Locked View screen return to previous screen.
        """
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.view_fax_locked)
        ok_button = self.spice.wait_for(MenuAppWorkflowObjectIds.view_fax_locked_ok_button)
        self.spice.wait_until(lambda: ok_button["visible"] is True)
        time.sleep(1)
        ok_button.mouse_click()

    def click_cancel_btn_on_printer_user_screen(self):
        """
        Navigate to home screen and disable fax permissions from EWS > Security > Access Control, printer user screen pop up.
        Click Cancel button on Printer User screen return to previous screen.
        """
        assert self.spice.wait_for(MenuAppWorkflowObjectIds.login_user_view)
        cancel_button = self.spice.wait_for(MenuAppWorkflowObjectIds.signin_cancel)
        self.spice.wait_until(lambda: cancel_button["visible"] is True)
        time.sleep(1)
        cancel_button.mouse_click()

    def check_search_result_number_in_fax_contacts_list_view(self, expected_result_number):
        """
        Check Search Result numbers shows in contacts list view screen.
        @param:expected_result_number, should be int type 
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contacts_integration)
        result_number_view = self.spice.wait_for(f"{FaxAppWorkflowObjectIds.search_result_section} {FaxAppWorkflowObjectIds.spice_text_view}")
        self.spice.wait_until(lambda:result_number_view["visible"])
        result_message = result_number_view["text"]
        assert expected_result_number == int(result_message), "Search result numbers is error"
        logging.info("check search result number success")
    
    def check_contacts_display_name_in_fax_contacts_list_view(self, expected_contact_list):
        """
        Check expect contacts shows in contact list view screen.
        @param:expected_contact_list: the contacts list should be sorted
        @return:
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_contacts_integration)
        time.sleep(3)

        for display_name in expected_contact_list:
            item_object_name = f"#checkBox_{display_name}Row"
            self.scroll_contact_or_group_item_into_view(FaxAppWorkflowObjectIds.view_fax_contact_list_view, item_object_name, None, footer_item_id = None, top_item_id = FaxAppWorkflowObjectIds.search_result_section)
            self.spice.wait_for(item_object_name)
            logging.info(f"-found:{display_name}")
        
        logging.info(f"Check contacts name list {expected_contact_list} success")
        self.workflow_common_operations.scroll_to_position_vertical(0, FaxAppWorkflowObjectIds.scrollbar_fax_contact_list_view)

    def verify_restricted_alert_string(self, net):
        """
        Purpose: Check restricted alert text.
        Should on the restricted alert screen with ok button
        Args: net
        """
        self.spice.wait_for("#noAccessView")
        expected_str = LocalizationHelper.get_string_translation(net, "cItemRestricted")
        actual_str = self.spice.wait_for("#noAccessView #alertDetailDescription #contentItem")["text"]
        logging.info(f"verify_restricted_alert_string actual_str <{actual_str}> and expected_str <{expected_str}>")
        assert expected_str == actual_str, f"Failed to check restricted alert is displayed. expected _str is <{expected_str}>, actual_str is <{actual_str}>"

    def goto_store_fax_from_job_storage_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Menu -> Print app -> Job Storage ->Stored Fax
        @return:
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        print_app = self.spice.wait_for(MenuAppWorkflowObjectIds.view_menuPrint)
        #self.spice.validate_button(print_app)
        print_app.mouse_click()
        self.spice.wait_for(MenuAppWorkflowObjectIds.menu_print_list)
        logging.info("At Print App")

        job_storage = self.spice.wait_for(MenuAppWorkflowObjectIds.job_storage)
        self.spice.validate_button(job_storage)
        job_storage.mouse_click()

        self.spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)
        logging.info("At Job Storage App")

        stored_faxes = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_stored_item)
        self.spice.validate_button(stored_faxes)
        stored_faxes.mouse_click()
        time.sleep(2)

    def goto_menu_jobStorage(self, spice):
        self.homemenu.goto_menu(self.spice)

        is_job_storage_available_in_menu = False
        try:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menulistLandingpage, MenuAppWorkflowObjectIds.menu_button_jobStorage , MenuAppWorkflowObjectIds.scrollbar_menulistlandingpage ,MenuAppWorkflowObjectIds.app_column_name , MenuAppWorkflowObjectIds.landingPage_Content_Item , MenuAppWorkflowObjectIds.app_section_bottom_border)
            current_button = self.spice.wait_for(MenuAppWorkflowObjectIds.job_storage + " MouseArea")
            current_button.mouse_click()
            time.sleep(1)
            is_job_storage_available_in_menu = True
        except Exception as e:
            # If the print app is not found in the main screen, go directly to job storage.
            logging.info("Print app not found in Main Menu, trying to access job storage app directly")

        # If the job storage app is not available in the main menu, go to the print app and access the job storage app from there.
        if not is_job_storage_available_in_menu:
            self.homemenu.goto_menu_print(self.spice)
            current_button = self.spice.wait_for(MenuAppWorkflowObjectIds.job_storage + " MouseArea")
            current_button.mouse_click()

        assert self.spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)

        logging.info("At Menu Job Storage Screen")
        time.sleep(1)
        stored_faxes = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_stored_item)
        stored_faxes.mouse_click()

    def select_store_fax_by_fax_number(self, fax_number, dunestorejob):
        """
        Function to select store fax by fax number
        Ui should be on Stored Faxes screen
        Ui Flow: Select the stored fax job
        @return:
        """
        storejobs = dunestorejob.get_all()
        total_fax_job = []
        for storejob in storejobs:
            if storejob['jobType'] == 'receiveFax':
                total_fax_job.append(storejob)

        self.spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)

        try:
            for index in range(len(total_fax_job)*2):
                title_info = self.spice.query_item("#jobListView #panelsStack #joblistspiceListView #textColumn SpiceText[visible=true]", index)
                if title_info['text'] == fax_number:
                    logging.info("Select the store fax job")
                    check_box = self.spice.query_item("#jobListView #panelsStack #joblistspiceListView #CheckBoxView", index)
                    check_box.mouse_click()
                    time.sleep(2)
                    assert check_box['checked'] == True, 'Failed to select the store fax!'
        except Exception:
            raise Exception("Failed to find the Store Fax job by fax number!")
        
        time.sleep(3)

    def verify_store_fax_by_fax_number(self,fax_number,dunestorejob):

        """
        Function to verify store fax by fax number
        Ui should be on Stored Faxes screen
        Ui Flow: verify the stored fax job
        @return:
        """
        storejobs = dunestorejob.get_all()
        total_fax_job = []
        for storejob in storejobs:
            if storejob['jobType'] == 'receiveFax':
                total_fax_job.append(storejob)

        self.spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)

        try:
            for index in range(len(total_fax_job)*2):
                title_info = self.spice.query_item("#jobListView #panelsStack #joblistspiceListView #textColumn SpiceText[visible=true]", index)
                if title_info['text'] == fax_number:
                    logging.info("verified the store fax job")
                    time.sleep(2)
        except Exception:
            raise Exception("Failed to find the Store Fax job by fax number!")
        
        time.sleep(3)
        back_button = self.spice.wait_for(FaxAppWorkflowObjectIds.backbutton)
        back_button.mouse_click()


    

    
    def click_print_button_on_store_fax_screen(self):
        """
        Function to click print button on Stored Faxes screen
        Ui should be on Stored Faxes screen
        Ui Flow: Click print button
        @return:
        """
        print_button = self.spice.wait_for("#printButton")
        self.spice.validate_button(print_button)
        print_button.mouse_click()
        
    def click_delete_button_on_store_fax_screen(self):
        """
        Function to click delete button on Stored Faxes screen
        Ui should be on Stored Faxes screen
        Ui Flow: Click delete button
        @return:
        """
        delete_button = self.spice.wait_for("#deleteButton")
        self.spice.validate_button(delete_button)
        delete_button.mouse_click()
    
    def fax_goto_custom_address_book_from_recipient_screen(self):
        """
        Purpose: Navigates from fax recipient to coustom contacts selection screen in fax app and press search Icon
        Ui Flow: Fax Recipients screen -> Sent to Contacts -> custom addressbook -> Search Icon
        """
        #self.goto_fax_app_recipient_screen()
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_custom, FaxAppWorkflowObjectIds.view_FaxcustomSelectScreen)
        sleep(2)
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.search_icon)
        current_button.mouse_click()

    def check_fax_app(self):
        isFaxAppEnabled = False

        try:
            self.goto_fax_app()
            isFaxAppEnabled = True
        except Exception as e:
            logging.info("Fax App is Disabled")

        logging.info("check_fax_app ={}".format(isFaxAppEnabled))
        
        return isFaxAppEnabled

    def check_fax_send_button(self):
        """
        Purpose: check if fax send under fax app is visible or not.
        @return: visible
        """
        try:
            self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSend)
            visible = True
        except:
            visible = False

        logging.info(
            "[check_fax_send_button] visible={}".format(visible))
        return visible

    def wait_fax_send_button_status(self, expect_status):
        """
        Purpose: wait fax send status under fax app is same with expected.
        @return: expect_status: True/False
        """
        send_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSend)
        self.spice.wait_button_status(send_button, expect_status)

    def check_fax_receive_feature(self, spice, udw, cdm, net, sys):
        isFaxReceiveEnabled = True

        try:
            logging.info("goto Menu>Settings>Fax settings>Receive Settings, enable auto answer")
            spice.fax_ui().goto_menu_fax_receive_settings()
            spice.fax_ui().fax_receive_settings_auto_answer(True)
            faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
            logging.info("Receive Fax job..")
            Fax(cdm, udw).receive_fax(faxSimIp, cancel=Cancel.trigger_receive_and_exit)
            logging.info("Incoming Fax in progress")
            spice.fax_ui().wait_for_fax_job_status_toast(net,"Incoming fax")
            logging.info("Fax should automatically connect without clicking on Accept button")
            spice.fax_ui().wait_for_fax_job_status_toast(net,"Receive Connecting")
            spice.fax_ui().wait_for_fax_job_status_toast(net,"Receiving")
            logging.info("Receive Incoming fax job from remote device to DUT and when fax is in progress navigate to Scan icon")
            spice.fax_ui().wait_for_fax_job_status_toast(net,message="Fax received successfully", timeout=20, wait_for_toast_dimiss=True)
            spice.goto_homescreen()

            isFaxReceiveEnabled = True
        except Exception as e:
            logging.info("Fax Receive is Disabled")
            isFaxReceiveEnabled = False


        logging.info("check_fax_receive_feature ={}".format(isFaxReceiveEnabled))

        return isFaxReceiveEnabled        

    def check_fax_receive_disable_feature(self, spice, udw, cdm):

        isFaxReceiveEnabled = True

        try:
            status = Fax(cdm, udw).is_fax_receive_enabled()
            isFaxReceiveEnabled = status
        except Exception as e:
            logging.info("except:::Fax Receive is Enabled") 

        logging.info("check_fax_receive_disable_feature ={}".format(isFaxReceiveEnabled))                          
        
        return isFaxReceiveEnabled
    
    def disable_fax_forward(self, spice, cdm, udw):
        fax_forward_uri = "cdm/fax/v1/faxForwardConfiguration"

        try:
            spice.fax_ui().goto_menu_fax_forward_configuration()
            spice.fax_ui().fax_receive_settings_set_fax_forwarding(False, False, None)
            ticket_default_response = cdm.get(fax_forward_uri)
            logging.info(ticket_default_response)
            faxForwardEnabled = ticket_default_response["faxForwardEnabled"]
            assert faxForwardEnabled == 'false', "the  value of faxforward is set from ui is not " \
                                            "reflected in cdm, actual value is: %s" % faxForwardEnabled   
        finally:
            spice.goto_homescreen()

    def get_ipp_protocol(self):
        ipp_protocols = ["ipp"]
        return ipp_protocols[random.randint(0, len(ipp_protocols) - 1)]            

    def execute_ipp_airfax_command(self, printer_ip, ipp_dat_file, ipp_print_file, ipp_print_server_file):

        # send ipp test files
        ipp_tool_exe = "/opt/ippeveselfcert/ipptool"
        ipp_uri = self.get_ipp_protocol() + "://" + printer_ip + "/ipp/faxout "

        # TODO do we need to consider these parameters IPv4|IPv6
        # TODO -E TLS options?
        ipp_command = []
        ipp_command = ipp_tool_exe + " -vt " + ipp_uri + " -f " + ipp_print_file + " " + ipp_dat_file

        print("IPP Command: {0}".format(ipp_command))
    
        process = subprocess.Popen(ipp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        print("Standard Output: {0}".format(output[0]))
        print("Standard Error: {0}".format(output[1]))

        print("process.returncode: {0}".format(process.returncode))

        return process.returncode

    def check_maximum_contacts_screen(self):
        """
        Purpose: Check maximum contacts screen
        Ui Flow: Fax Recipients screen -> Add Contacts -> Maximum Contacts screen
        """
        current_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_faxSend)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()

        maximum_contact_view = self.spice.wait_for(FaxAppWorkflowObjectIds.maximum_contacts_screen)
        sleep(2)
        self.spice.wait_until(FaxAppWorkflowObjectIds.maximum_contact_view)["visible"] == True
        sleep(2)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.maximum_contacts_screen_ok_button)
        ok_button.mouse_click()

    def verify_prepreview_screen_string_adf(self,udw,net, locale: str = "en"):
        udw.mainApp.ScanMedia.unloadMedia("ADF")#flatbed
        flatbed_ui_string =self.spice.wait_for(FaxAppWorkflowObjectIds.pre_preview_layout +" "+ FaxAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        flatbed_expected_string = str(LocalizationHelper.get_string_translation(net, ["cLoadingOriginalDocument", str(LocalizationHelper.get_string_translation(net, "cSend", locale))], locale))+ "\n" + str(LocalizationHelper.get_string_translation(net, "cPreviewUnavailable", locale))
        assert flatbed_ui_string == flatbed_expected_string, "String mismatch"
        udw.mainApp.ScanMedia.loadMedia("ADF")#Adf
        sleep(2)
        adf_ui_string = self.spice.wait_for(FaxAppWorkflowObjectIds.pre_preview_layout +" "+ FaxAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        adf_expected_string = str(LocalizationHelper.get_string_translation(net, ["cOriginalDetectedSend", str(LocalizationHelper.get_string_translation(net, "cSend", locale))], locale)) + "\n" + str(LocalizationHelper.get_string_translation(net, "cPreviewUnavailable", locale))
        assert adf_ui_string == adf_expected_string, "String mismatch"
        
    def get_max_junk_constraint(self,cdm):
        """
        returns the maximum junk block number constraint
        """
        ENDPOINT = "cdm/faxReceive/v1/blockedNumbers/constraints"
        response = cdm.get_raw(ENDPOINT)
        assert response.status_code==200, 'Unexpected response'
        r_historyStats = response.json()
        data = r_historyStats
        for validator in data['validators']:
         if 'maxSize' in validator:
           blocknum_max = validator['maxSize']['value']
        return blocknum_max
    
    def click_junk_fax_keyboardEntry_cancel_button(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->'Using Keyboard' Screen->Cancel click. 
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)
        junk_fax_receiveCallHistory_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_cancel_junkfax)
        junk_fax_receiveCallHistory_button.mouse_click()

    def goto_blocked_fax_screen(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->'Blocked Fax' UI->Click 'Add' button
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_number_existing_screen)
        self.click_blocked_number_add_button()

    def check_contacts_not_present_in_local_address_book(self, payload_list):
        """
        Ui Flow: Main Menu -> Fax -> Skip -> Fax Recipients screen -> Sent to Contacts >> Local Address Book
        """
        self.goto_fax_without_skip_button()
        for payload in payload_list:
            status = False
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.menuText_FaxSendToContacts, FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
            self.fax_menu_navigation(FaxAppWorkflowObjectIds.button_faxAddressbook_local, FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxLocalSelectScreen)
            AddressBook_name = payload['displayName']
            addressBook_name_locator = FaxAppWorkflowObjectIds.addressbook_name_common+AddressBook_name+'Model'
            time.sleep(2)
            try:
                self.spice.wait_for(addressBook_name_locator)
                status = True
            except:
                pass
            self.back_to_addressbook_local_from_local_select_screen_with_back_button()
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_FaxAddressBookScreen)
            self.back_to_faxsendtocontacts_from_addressbook_local_screen_with_close_button()
            assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendJobSubmissionScreen)
            if status:
                logging.info(f"{payload['displayName']} is found in local address book which is not expected")
                assert not status, f'contact - {payload["displayName"]} is visible in local address book'
            else:
                logging.info(f"{payload['displayName']} not found in local address book as expected")

    def fax_recipient_screen_remove_existing_contact_enter_fax_number(self, fax_number):
        """
        Purpose: From fax recipient screen to enter fax number
        Ui Flow: Fax Recipient screen -> Enter Fax number
        Args: Fax number
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)
        self.fax_menu_navigation(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen, FaxAppWorkflowObjectIds.view_keyboard)
        current_screen = self.spice.wait_for(FaxAppWorkflowObjectIds.view_keyboard)
        key_back  = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
        key_back.mouse_click()
        logging.info("cleared the existing fax number")
        self.enter_numeric_keyboard_values(fax_number)

    def click_ok_button_on_invalid_or_missing_entries_in_blocked_fax_alert_screen(self):
        """
        Click ok button on Invalid or Missing Entries Alert Screen
        """
        button_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.button_error_msg_ok)
        button_ok.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)

        logging.info("Click ok button on invalid or missing entries alert screen")

    def fax_send_settings_set_fax_send_header_values(self, header: str):
        """
        Purpose: Set fax send header based on user input in fax send settings
        Args: header: should be "prepend" or "overlay"
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_menuComboBox_overLayFaxHeader, FaxAppWorkflowObjectIds.menuComboBox_overLayFaxHeader]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)
        select_option = "#ComboBoxOptions" + header.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)   

    def goto_menu_fax_send_settings_send_header(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings
        Args: None
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_menuComboBox_overLayFaxHeader, FaxAppWorkflowObjectIds.menuComboBox_overLayFaxHeader]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)                    
    def fax_dialing_set_line_monitor_volume(self, volume: str):
        """
        Purpose: Set fax line monitor volume based on user input in fax dialing settings
        Args: volume: should be "low" or "medium" or "high" or "off"
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_line_monitor_volume, FaxAppWorkflowObjectIds.button_switch_fax_line_monitor_volume]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.view_faxDialingScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)
        select_option = "#ComboBoxOptions" + volume.lower()
        current_button = self.spice.wait_for(select_option)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
    
    def fax_dialing_dualfax_set_line_monitor_volume(self, volume: str,line: str = "line1"):
        """
        Purpose: Set fax line monitor volume based on user input in fax dialing settings
        Args: volume: should be "low" or "medium" or "high" or "off"
        """
        if line.lower() == "line1":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line1
        elif line.lower() == "line2":
            scrollbar = FaxAppWorkflowObjectIds.scrollBar_faxdialing_line2
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)
        menu_id = [FaxAppWorkflowObjectIds.row_switch_fax_line_monitor_volume, FaxAppWorkflowObjectIds.button_switch_fax_line_monitor_volume]
        self.workflow_common_operations.goto_item(menu_id, FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list,select_option = False,
                                                  scrollbar_objectname = scrollbar)
        logging.info("Wait for the combo box to be visible and clickable")
        current_elemt = self.spice.wait_for(FaxAppWorkflowObjectIds.button_switch_fax_line_monitor_volume)
        self.spice.wait_until(lambda: current_elemt["visible"] == True, timeout=10.0)
        current_elemt.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.line_monitor_combo_list)
        ringer_volume_dict = {
        "Low": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_low,
        "High": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_high,
        "Off": FaxAppWorkflowObjectIds.combo_box_fax_send_line_monitor_volume_off
        }
        menu_item_id = ringer_volume_dict.get(volume)
        self.workflow_common_operations.goto_item(menu_item_id, FaxAppWorkflowObjectIds.line_monitor_combo_list, scrollbar_objectname = FaxAppWorkflowObjectIds.ringer_volume_scrollbar )
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list)


    def goto_menu_fax_send_settings_dialing_line_monitor_volume(self):
        """
        Purpose: Navigates from home menu settings to fax Dialing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Dialing
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxDialingScreen)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_switch_fax_line_monitor_volume , FaxAppWorkflowObjectIds.view_faxDialingScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxDialing)

    def click_junk_fax_keyboardEntry_soho_cancel_button(self):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->'Add Blocked Fax Numbers' Screen->Cancel click. 
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_soho_screen)
        junk_fax_soho_screen_button = self.spice.wait_for(FaxAppWorkflowObjectIds.cancel_button_soho_junk_fax_number)
        junk_fax_soho_screen_button.mouse_click()        

    def click_junk_fax_keyboardEntry_soho_screen_to_input_number(self,junk_fax_number_list):
        """
        Purpose: Click Cancel button in Blocked Fax Screen.
        Ui Flow: Fax Receive Settings->Blocked Fax Numbers->'Add Blocked Fax Numbers' Screen->click on Textfield. 
        Args: None
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_soho_screen)
        junk_fax_number_text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.enter_junk_fax_number_text_field)
        junk_fax_number_text_field.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_spicekeyboard)
        self.enter_fax_number_alphanumeric(junk_fax_number_list)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_soho_screen)

    def remove_blockedfax_number_by_backspace(self, junk_fax_number_list):
        """
        Remove the value of Blocked Fax number by pressing backspace
        """
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_soho_screen)
        object = self.spice.wait_for(FaxAppWorkflowObjectIds.enter_junk_fax_number_text_field)
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)
        # clear blocked fax number text before input number.
        text_length = len(junk_fax_number_list)        
        for i in range(text_length):
            clear_button = self.spice.wait_for(FaxAppWorkflowObjectIds.key_back_space)
            clear_button.mouse_click()
            time.sleep(1)
        key_ok = self.spice.wait_for(FaxAppWorkflowObjectIds.keyOK)
        key_ok.mouse_click()               

    def click_junk_fax_number_soho_ok_button(self):
        """
        Purpose: Click Ok button in enter junk fax number screen.
        Ui Flow: enter junk fax number soho screen -> click ok button
        Args: None
        """
        junk_fax_number_soho_ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_soho_junk_fax_number)
        junk_fax_number_soho_ok_button.mouse_click()

    def click_lastsender_add_button(self):
        """
        Purpose: Click Add button in Last Sender screen
        Ui Flow: Fax Recipient screen -> Last Sender -> Add button
        Args: None
        """
        enter_faxnumber_view = self.spice.wait_for(FaxAppWorkflowObjectIds.view_enter_junk_fax_number_screen)
        last_sender_add_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_add_last_sender)
        last_sender_add_button.mouse_click()
        self.spice.wait_until(lambda:enter_faxnumber_view["visible"])
        self.workflow_common_operations.scroll_to_position_vertical(0.8, FaxAppWorkflowObjectIds.blockedFaxScrollBar)
        time.sleep(1)

    def save_lastsender_value_into_textfield(self, last_sender):
        """
        Purpose: Save last sender value into text field
        Ui Flow: Fax Recipient screen -> Last Sender -> Add button -> Save last sender value
        Args: last_sender
        """
        # Save the value in a text field
        text_field = self.spice.wait_for(FaxAppWorkflowObjectIds.textField_enterFaxNumberSendScreen)
        text_field.__setitem__('displayText', last_sender)        

    def goto_menu_settings_Fax_clearFaxActivityLog(self, spice):
        '''
        Clears the Fax Activity Logs submitted through
        Menu --> Settings --> Fax --> Clear Fax Activity Log --> Clear
        '''
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menu_button_fax_settings_clearFaxLogs,
         scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        spice.wait_for(FaxAppWorkflowObjectIds.menu_button_fax_settings_clearLogs).mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_settings_clearfax_log)
        self.spice.wait_for(FaxAppWorkflowObjectIds.menu_button_fax_settings_clearLogs_clear).mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_settings_toast_window)
        assert self.spice.query_item(FaxAppWorkflowObjectIds.view_settings_fax_toastinfo)["text"] == "Success"

    def goto_menu_settings_Fax_cancelClearFaxActivityLog(self, spice):
        '''
        Cancel the Fax Activity Logs submitted through
        Menu --> Settings --> Fax --> Clear Fax Activity Log --> Cancel
        '''
        self.homemenu.goto_menu_settings_fax(self.spice)
        self.homemenu.menu_navigation(self.spice, FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menu_button_fax_settings_clearFaxLogs,
         scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        spice.wait_for(FaxAppWorkflowObjectIds.menu_button_fax_settings_clearLogs).mouse_click()

        self.spice.wait_for(FaxAppWorkflowObjectIds.view_fax_settings_clearfax_log)
        self.spice.wait_for(FaxAppWorkflowObjectIds.menu_button_fax_settings_clearLogs_cancel).mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettingsScreen)
    
    def fax_send_later_schedule_now(self,net,minutes: int = 2, timeout: int = 120):
        '''
        Purpose: Schedule a fax to be sent now
        fax>fax options>schedule now>set time>done>enter fax number>send
        '''
        self.goto_fax_app_recipient_screen_with_setup()
        self.goto_fax_app_fax_options()
        self.goto_fax_app_fax_options_schedule_now()
        self.goto_fax_app_fax_options()
        self.goto_fax_app_fax_options_schedule_now()
        self.fax_send_later_schedule(net,minutes,timeout)
    
    def fax_send_later_schedule_now_without_faxsetup(self,net,minutes: int = 2, timeout: int = 120):
        '''
        Purpose: Schedule a fax to be sent now
        fax>fax options>schedule now>set time>done>enter fax number>send
        '''
        self.goto_fax_app_recipient_screen()
        self.goto_fax_app_fax_options()
        self.goto_fax_app_fax_options_schedule_now()
        self.fax_send_later_schedule(net,minutes,timeout)
    
    def fax_send_later_schedule(self, net, minutes: int = 2, timeout: int = 120):
        '''
        Purpose: Schedule a fax to be sent later by adding specified minutes to current UI time
        Ui Flow: fax>fax options>schedule now>set time>done>enter fax number>send
        
        Args:
            net: Network object for localization
            minutes: Number of minutes to add to current time (default: 2)
            timeout: Timeout for waiting for job status toast (default: 120)
        '''
        try:
            # Get current time values from UI to ensure synchronization with UI state
            current_min = int(self.get_now_min_value())
            current_hr = int(self.get_now_hr_value())
            
            # Calculate new time with proper rollover handling
            total_minutes = current_min + minutes
            new_hr = (current_hr + (total_minutes // 60)) % 24  # Handle minute and hour rollover
            new_min = total_minutes % 60
            
            # Convert to strings for UI
            hr_string, min_string = str(new_hr), str(new_min)
            
            # Critical: Set hour first when it changes to avoid UI timing issues
            if new_hr != current_hr:
                self.fax_send_now_hr_set(hr_string)
            self.fax_send_now_min_set(min_string)
            
            # Complete the scheduling process
            self.fax_schedule_later_done_button()
            self.send_later_enter_numeric_keyboard_values('101')
            self.fax_job_submission_fax_send()
            
            # Wait for confirmation with formatted time message
            expected_message = f"The scheduled fax will be sent at {hr_string}:{min_string}"
            self.wait_for_fax_job_status_toast(net, message=expected_message, timeout=timeout)
            
            logging.info(f"Successfully scheduled fax for {hr_string}:{min_string}")
            
        except Exception as e:
            # Handle any other unexpected errors
            logging.error(f"Unexpected error during fax scheduling: {e}")
            raise

    def is_on_basic_fax_setup_screen(self) -> bool:
        return self.spice.wait_for(FaxAppWorkflowObjectIds.fax_basic_setup_view)

    def verify_adf_add_page_prompt(self):
        """
        Verify current screen is ADF add page Prompt
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.adfAddPagePrompt, timeout=10)

    def adf_add_page_prompt_start_job(self):
        """
        On ADF add page Prompt, press start button
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.adfAddPagePrompt)

        startButton = self.spice.wait_for(FaxAppWorkflowObjectIds.adfAddPage_start)
        startButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def adf_add_page_prompt_cancel_job(self):
        """
        On ADF add page Prompt, press cancel button
        """
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.adfAddPagePrompt)

        cancelButton = self.spice.wait_for(FaxAppWorkflowObjectIds.adfAddPage_cancel)
        cancelButton.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendRecipientScreen)

    def is_fax_app_on_the_home_screen(self):
        exist = True
        try:
            if(self.spice.wait_for(FaxAppWorkflowObjectIds.fax_app_home)["visible"] == True):
                exist = True
        except:
            logging.info("Fax app is not on the home screen")
            exist = False
        return exist

    def goto_preview_panel(self):
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View)
        fax_collapse_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_expand_secondarypanel, timeout=9.0)
        fax_collapse_button.mouse_click()

    def goto_main_panel(self):
        fax_expand_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_collapse_secondarypanel)
        self.spice.wait_until(lambda: fax_expand_button["enabled"] == True, timeout = 15.0)
        fax_expand_button.mouse_click()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View, timeout=15.0)

    def start_preview(self):
        self.spice.wait_for(FaxAppWorkflowObjectIds.button_preview)
        fax_preview_button = self.spice.wait_for(FaxAppWorkflowObjectIds.button_preview)
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

    def verify_preview_layout_header(self):
        self.spice.wait_for(FaxAppWorkflowObjectIds.preview_header)
        self.spice.wait_for(FaxAppWorkflowObjectIds.preview_header_moreOptions)
        moreOptions = self.spice.query_item(FaxAppWorkflowObjectIds.preview_header_moreOptions)
        assert moreOptions["visible"] == True, "More Options is not visible"
        moreOptions.mouse_click()

    def verify_preview_magnification_options(self):
        zoomout_button = self.spice.query_item(FaxAppWorkflowObjectIds.zoomOut_button)
        zoomout_button.mouse_click()

        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_constraint_message)
        ok_button = self.spice.wait_for(FaxAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()

        self.verify_preview_layout_header()
        zoomIn_button = self.spice.query_item(FaxAppWorkflowObjectIds.zoomIn_button)
        zoomIn_button.mouse_click()

        self.verify_preview_layout_header()
        fitHeightButton = self.spice.query_item(FaxAppWorkflowObjectIds.fitHeightButton)
        fitHeightButton.mouse_click()

        self.verify_preview_layout_header()
        fitWidthButton = self.spice.query_item(FaxAppWorkflowObjectIds.fitWidthButton)
        fitWidthButton.mouse_click()

    def wait_and_click_preview_n(self, preview_index ):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_index = preview_index-1
        thumbnail_objectname = FaxAppWorkflowObjectIds.preview_image_without_index + str(preview_index)
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.fitpage_layout, timeout=15.0)
        fitpage_layout = self.spice.wait_for(FaxAppWorkflowObjectIds.fitpage_layout, timeout=15.0)
        self.spice.wait_until(lambda: fitpage_layout["isPreviewImageAvailable"] == True)
        thumbnail_object = self.spice.wait_for(thumbnail_objectname, timeout=15.0)
        thumbnail_object.mouse_click()
    
    def back_to_fax_send_settings_from_dual_fax_dialing_screen_with_back_button(self):
        """
        Back to fax send settings screen from fax dialing screen through back button.
        """
        logging.info("Go back to fax send settings screen from fax dialing screen through back button.")
        self.back_button_press(screen_id = FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list, landing_view = FaxAppWorkflowObjectIds.fax_send_menu_list, back_or_close_button = f'{FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list} {FaxAppWorkflowObjectIds.button_back}')
    
    def goto_fax_settings_fax_dualfax_dialing_screen(self, line: str = "line1"):
        """
        Purpose: Navigates from fax settings to fax dialing settings screen.
        Ui Flow: Fax Settings -> Fax Send Settings -> Fax Dialing Settings.
        """
        if line.lower() == "line2":
            line_button = FaxAppWorkflowObjectIds.menuText_faxDialing_line2
        elif line.lower() == "line1":
            line_button = FaxAppWorkflowObjectIds.menuText_faxDialing_line1
        else:
            raise ValueError("Invalid line parameter. Use 'line1' or 'line2'.")
        self.homemenu.menu_navigation(self.spice,FaxAppWorkflowObjectIds.view_faxSettingsScreen, FaxAppWorkflowObjectIds.menuText_faxSend,scrollbar_objectname= FaxAppWorkflowObjectIds.scrollBar_faxSettings)
        self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen ,5)
        logging.info("Click the Fax Dialing field")
        fax_dialing_field = self.spice.wait_for(FaxAppWorkflowObjectIds.menuText_faxDialing + " MouseArea")
        fax_dialing_field.mouse_click()
        line_selection = self.spice.wait_for(line_button)
        line_selection.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_dialing_line2_menu_list ,5)

    def wait_for_preview_window(self):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_window_objectname = FaxAppWorkflowObjectIds.previewWindow
        assert self.spice.wait_for(preview_window_objectname)

    def back_from_preview(self):
        '''
        Ui Should be in previewpanel
        Press back button
        '''
        self.spice.wait_for(FaxAppWorkflowObjectIds.preview_back_button)
        current_button = self.spice.query_item(FaxAppWorkflowObjectIds.preview_back_button)
        current_button.mouse_click()
        self.spice.wait_for(FaxAppWorkflowObjectIds.fax_Send_Recipients_View)

    def verify_prepreview_screen_string(self, udw, net):
        current_string_id = self.spice.query_item(FaxAppWorkflowObjectIds.prepreview_layout +" "+ FaxAppWorkflowObjectIds.pre_preview_content +" #contentItem")["text"]
        assert current_string_id != "", "Error: String ID Not found"
        expected_string_id = self.spice.common_operations.get_expected_translation_str_by_str_id(net,FaxAppWorkflowObjectIds.prepreview_enabled_string_id)
        assert expected_string_id != "", "Error: String ID Not not trnaslated"
        assert current_string_id == expected_string_id, f"Error: String mismatch {current_string_id} != {expected_string_id}"
    
       #rec settings

    def goto_stamped_received_faxes(self):
        """
        Purpose: Navigates from home menu settings to ringer volume screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax receive Settings -> ringer volume
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout =9.0)
        opt = FaxAppWorkflowObjectIds.menuSwitch_stampReceivedFaxes_receive
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_stampReceivedFaxes_receive
        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        stamp_rec = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_stampReceivedFaxes_receive)
        stamp_rec.mouse_click()

    def goto_paper_tray_settings(self):
        """
        Purpose: Navigates from home menu settings to paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Paper Tray Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.4, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        paper_tray = self.spice.wait_for(FaxAppWorkflowObjectIds.row_object_paper_tray)
        paper_tray.mouse_click()

    def goto_fit_to_page_settings(self):
        """
        Purpose: Navigates from home menu settings to fit to page settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fit to Page Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        opt = FaxAppWorkflowObjectIds.spiceSwitch_fitToPage_receive
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_fitToPage_receive
        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        fit_to_page = self.spice.wait_for(FaxAppWorkflowObjectIds.spiceSwitch_fitToPage_receive)

    def goto_2sided_printing(self):
        """
        Purpose: Navigates from home menu settings to 2-sided printing settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> 2-Sided Printing Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        opt = FaxAppWorkflowObjectIds.menuSwitch_twoSidedPrinting_receive
        opt_row = FaxAppWorkflowObjectIds.row_menuSwitch_twoSidedPrinting_receive
        menu_item_id = [opt_row,opt]
        self.workflow_common_operations.goto_item( menu_item_id , FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,  select_option = False, scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)
        two_sided_printing = self.spice.wait_for(FaxAppWorkflowObjectIds.spiceSwitch_twoSidedPrinting_receive)
        two_sided_printing.mouse_click()

    def goto_fax_printing_options(self):
        """
        Purpose: Navigates from home menu settings to fax printing options screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Printing Options
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_option, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        fax_printing_options = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_setting_fax_printing_option)
        fax_printing_options.mouse_click()

    def goto_junk_fax_blocking(self):
        """
        Purpose: Navigates from home menu settings to junk fax blocking screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Junk Fax Blocking
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_junk_fax_blocking_settings, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        junk_fax_blocking = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_junk_fax_blocking_settings)
        junk_fax_blocking.mouse_click()

    def goto_fax_rec_notification(self):
        """
        Purpose: Navigates from home menu settings to fax receive notification screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Receive Notification
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.fax_receive_fax_notifications_combo_box_option, FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)


        fax_rec_notification = self.spice.wait_for(FaxAppWorkflowObjectIds.fax_receive_fax_notifications_combo_box_option)
        fax_rec_notification.mouse_click()

    def goto_paper_tray(self):
        """
        Purpose: Navigates from home menu settings to paper tray settings screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Paper Tray Settings
        Args: None
        """
        self.goto_menu_fax_receive_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxReceiveSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.4, FaxAppWorkflowObjectIds.scrollBar_faxReceiveSettings)

        paper_tray = self.spice.wait_for(FaxAppWorkflowObjectIds.combo_box_paper_tray)
        paper_tray.mouse_click(5,5)


    # send settings

    def goto_fax_num_confirmation(self):
        """
        Purpose: Navigates from home menu settings to fax number confirmation screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Number Confirmation
        Args: None
        """
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.menuSwitch_faxNumberConfirmation, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

        fax_num_confirmation = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_faxNumberConfirmation)
        fax_num_confirmation.mouse_click()
    
    def goto_ipp_fax_send(self):
        """
        Purpose: Navigates from home menu settings to IPP Fax Send screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> IPP Fax Send
        Args: None
        """
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_menuSwitch_pcSendFax, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

        ipp_fax_send = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_pcSendFax)
        ipp_fax_send.mouse_click()

    def goto_ecm(self):
        """
        Purpose: Navigates from home menu settings to ECM screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> ECM
        Args: None
        """
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

        ecm = self.spice.wait_for(FaxAppWorkflowObjectIds.menuSwitch_errorCorrectionMode)
        ecm.mouse_click()

    def goto_fax_header(self):
        """
        Purpose: Navigates from home menu settings to Fax Header screen
        Ui Flow: Menu -> Settings -> Fax Settings -> Fax Send Settings -> Fax Header
        Args: None
        """
        self.goto_menu_fax_send_settings()
        assert self.spice.wait_for(FaxAppWorkflowObjectIds.view_faxSendSettingsScreen, timeout = 9.0)
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.row_menuComboBox_overLayFaxHeader, FaxAppWorkflowObjectIds.view_faxSendSettingsScreen,
                                                  scrollbar_objectname = FaxAppWorkflowObjectIds.scrollBar_faxSendSettings)

        fax_header = self.spice.wait_for(FaxAppWorkflowObjectIds.menuComboBox_overLayFaxHeader)
        fax_header.mouse_click()

