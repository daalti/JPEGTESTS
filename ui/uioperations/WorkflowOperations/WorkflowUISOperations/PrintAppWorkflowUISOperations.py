import logging
import re
from dunetuf.ui.uioperations.WorkflowOperations.PrintAppWorkflowUICommonOperations import PrintAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class PrintAppWorkflowUISOperations(PrintAppWorkflowUICommonOperations):
    max_cancel_time = 60
    property_current_index = "currentIndex"
    property_active_focus = "activeFocus"
    spice_tumbler_view = "#SpiceTumblerView"
    ALERT_DIALOG_TOAST_WINDOW = "#ToastWindowToastStackView" 
    ALERT_TOAST_MESSAGE = "#ToastBase #ToastRow #ToastInfoText"
    ALERT_TOAST_ICON = "#ToastBase #ToastRow #ToastIconForText"
    BUTTON_LIST_LAYOUT = "ButtonListLayout"
    MENU_LIST_LAYOUT = "MenuListLayout"
    ALERT_OPTIONS_BUTTON = "#CollapseButton"
    ALERT_OPTIONS_CANCEL_BUTTON = "#cancelBtn"
    ALERT_NO_WIDTH_TEXT = "#alertDetailDescription"
    ALERT_IMAGE_ICON = "#MessageLayout #MessageIcon"
    ALERT_TOAST_ICON_INFO = "#ToastBase #ToastIconForText"
    
    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
      
        self.LESS_PAPER_CURL_STR_ID = "cLessPaperCurl"
        self.LESS_PAPER_CURL = "#lessPaperCurlWFMenuSwitch"
        self.LESS_PAPER_CURL_VIEW = "#printQualityMenuList"
        self.TONER_DENSITY = "#tonerDensityMenuSlider"
        self.TONER_DENSITY_VIEW = "#printQualityMenuList"
        self.LESS_PAPER_CURL_BTN_TXT_ID = "#lessPaperCurlWFSettingsSwitch #contentItem"
        self.CLEAN_BELT = "cCleanBeltOption"
        self.CLEAN_BELT_BTN_ID = "#CleanBelt"
        self.ALERT_TOAST_MESSAGE_CLEAN_BELT = "#ToastWindowToastStackView #ToastRow #infoTextToastMessage"
        self.workflow_common_operations = spice.basic_common_operations

    def check_less_paper_curl_btn_text(self, net):
        """Check toogle text"""        
        exp_less_paper_curl_btn_txt = LocalizationHelper.get_string_translation(net, self.LESS_PAPER_CURL_STR_ID)
        act_less_paper_curl_btn_txt = self._spice.query_item(self.LESS_PAPER_CURL_BTN_TXT_ID)['text']
        assert act_less_paper_curl_btn_txt == exp_less_paper_curl_btn_txt, "Incorrect button text"

    def verify_cleanbelt_label_visibility(self, net):
        exp_clean_belt_btn_txt = LocalizationHelper.get_string_translation(net, self.CLEAN_BELT)
        act_clean_belt_btn_txt = self._spice.wait_for(self.CLEAN_BELT_BTN_ID+" #textColumn SpiceText[visible=true]")["text"]
        assert act_clean_belt_btn_txt == exp_clean_belt_btn_txt, "Incorrect button text"

    def get_toner_density_slider_value(self):
        '''
        Ui Should be in print quality panel
        Get toner density slider value
        '''
        self._spice.wait_for(self.TONER_DENSITY_VIEW,60)
        self._spice.wait_for(self.TONER_DENSITY)
        current_element = self._spice.wait_for(self.TONER_DENSITY,60)
        print(current_element.__getitem__('value'))
        return current_element.__getitem__('value')

    def set_toner_density_slider_value(self, value):
        '''
        Ui Should be in print quality panel
        Set toner density slider value
        '''
        self._spice.wait_for(self.TONER_DENSITY_VIEW)
        slider = self._spice.wait_for(self.TONER_DENSITY)
        slider.__setitem__('value', value)

    def get_less_paper_curl_toggle_state(self):
        """Get Less Paper Curl button state"""
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        logging.info("Default state : %s", less_paper_curl_toggled_state)
        if less_paper_curl_toggled_state:
            return 'true'
        else:
            return 'false'

    def cancel_print_no_width(self):
        """Click Less Paper Curl slider"""
        self._spice.wait_for(self.ALERT_OPTIONS_BUTTON, timeout = 9.0).mouse_click()
        self._spice.wait_for(self.ALERT_OPTIONS_CANCEL_BUTTON).mouse_click()

    def click_less_paper_curl_toggle(self):
        """Click Less Paper Curl slider"""
        self._spice.query_item(self.LESS_PAPER_CURL).mouse_click()
       
    def check_less_paper_curl_toggle(self):
        """UI should be off Less Paper Curl settings."""
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        assert not less_paper_curl_toggled_state,"Default setting of Less Paper Curl should be disable"

        self._spice.query_item(self.LESS_PAPER_CURL).mouse_click()
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        assert less_paper_curl_toggled_state, "Less Paper Curl Enable failed"

        self._spice.query_item(self.LESS_PAPER_CURL).mouse_click()
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        assert not less_paper_curl_toggled_state, "Less Paper Curl Disable failed"

    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def verify_clean_belt_toast_message(self, text):
        self.wait_for_alert_dialog_toast_window()
        toastMessage = self._spice.query_item(self.ALERT_TOAST_MESSAGE_CLEAN_BELT)
        #print("Title message=",str(toastMessage["text"]))
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)
        # Verify toast icon type. Workflow does not support icons on toast popups.
        #self.check_toast_information_icon()

    def check_toast_information_icon(self):
        alertIcon = self._spice.query_item(self.ALERT_TOAST_ICON_INFO)
        #print("icon source=",alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/+loTheme/information_xs.json")