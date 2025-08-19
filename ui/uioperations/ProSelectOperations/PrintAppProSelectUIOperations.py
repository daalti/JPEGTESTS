import logging
from time import sleep
from dunetuf.ui.uioperations.BaseOperations.IPrintAppUIOperations import IPintAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class PrintAppProSelectUIOperations(IPintAppUIOperations):
    ALERT_DIALOG_TOAST_WINDOW = "#ToastSystemToastStackView"
    ALERT_TOAST_MESSAGE_CLEAN_BELT = "#ToastBase #ToastRow #ToastInfoText"
    ALERT_IMAGE_ICON = "#MessageLayout #MessageIcon"
    ALERT_TOAST_ICON = "#ToastBase #ToastIconForText"

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        self.LESS_PAPER_CURL = "#lessPaperCurlMenuSwitch"
        self.LESS_PAPER_CURL_STR_ID = "cLessPaperCurl"
        self.CLEAN_BELT = "cCleanBeltOption"
        self.LESS_PAPER_CURL_BTN_TXT_ID = "#lessPaperCurlMenuSwitch #SwitchText"
        self.TONER_DENSITY = "#tonerDensityMenuSlider"
        self.TONER_DENSITY_VIEW = "#MenuListprintQuality"

    def check_less_paper_curl_btn_text(self, net):
        """Check toogle text"""
        exp_less_paper_curl_btn_txt = LocalizationHelper.get_string_translation(net, self.LESS_PAPER_CURL_STR_ID)
        act_less_paper_curl_btn_txt = self._spice.query_item(self.LESS_PAPER_CURL_BTN_TXT_ID)['text']
        assert act_less_paper_curl_btn_txt == exp_less_paper_curl_btn_txt, "Incorrect button text"

    def verify_cleanbelt_label_visibility(self, net):
        exp_clean_belt_btn_txt = LocalizationHelper.get_string_translation(net, self.CLEAN_BELT)
        act_clean_belt_btn_txt = self._spice.query_item("#cleanTransferBeltButton" + " SpiceText")["text"]
        assert act_clean_belt_btn_txt == exp_clean_belt_btn_txt, "Incorrect button text"

    def get_toner_density_slider_value(self):
        '''
        Ui Should be in print quality panel
        Get toner density slider value
        '''
        self._spice.wait_for(self.TONER_DENSITY_VIEW)
        self._spice.wait_for(self.TONER_DENSITY)
        current_element = self._spice.query_item(self.TONER_DENSITY)
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
        """Get Less Paper Curl button status"""
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        logging.info("Default state : %s", less_paper_curl_toggled_state)
        if less_paper_curl_toggled_state:
            return 'true'
        else:
            return 'false'

    def click_less_paper_curl_toggle(self):
        """Click Less Paper Curl slider"""
        currentElement = self._spice.query_item("#lessPaperCurlMenuSwitch")
        # navigate to toggle button
        while (self._spice.query_item("#lessPaperCurlMenuSwitch")["activeFocus"] == False):
            currentElement.mouse_wheel(180,180)
            sleep(0.2)
        currentElement.mouse_click()
        
    def check_less_paper_curl_toggle(self):
        """check Less Paper Curl by turning On/OFF """
        currentElement = self._spice.wait_for(self.LESS_PAPER_CURL, timeout = 9.0)
        assert currentElement
        # navigate to toggle button
        while (self._spice.query_item(self.LESS_PAPER_CURL)["activeFocus"] == False):
            currentElement.mouse_wheel(180,180)
            sleep(0.2)
        # toggle starts false(less paper curl is on), switch to true(less paper curl is off)
        currentElement.mouse_click()
        sleep(0.2)
        assert self._spice.query_item(self.LESS_PAPER_CURL)["checked"] == True, "Less Paper Curl is OFF"

        # toggle back to false
        if (self._spice.query_item(self.LESS_PAPER_CURL)["activeFocus"] == True):
            currentElement.mouse_click()
            sleep(0.2)
        assert self._spice.query_item(self.LESS_PAPER_CURL)["checked"] == False, "Less Paper Curl is ON"
    
    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def verify_clean_belt_toast_message(self, text):
        self.wait_for_alert_dialog_toast_window()
        toastMessage = self._spice.wait_for(self.ALERT_TOAST_MESSAGE_CLEAN_BELT)
        assert str(toastMessage["text"]) == str(text), "Failed to match the toast message."
        # Verify toast icon type. Workflow code does not have this following piece of code implemented as toast icon is missing in workflow.
        self.check_toast_information_icon()
    
    def check_toast_information_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_TOAST_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/+loTheme/information_xs.json")
