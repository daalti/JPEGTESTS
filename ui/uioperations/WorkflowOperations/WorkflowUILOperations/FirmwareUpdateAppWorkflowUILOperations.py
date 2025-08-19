import time
import logging

from dunetuf.ui.uioperations.BaseOperations.IFirmwareUpdateAppUIOperations import IFirmwareUpdateAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds

class FirmwareUpdateAppWorkflowUILOperations(IFirmwareUpdateAppUIOperations):

    PRINTER_UPDATE_RADIO_BUTTON_VIEW = "#radioButtonsViewlist1"
    PRINTER_UPDATE_RADIO_BUTTON_VALUE = PRINTER_UPDATE_RADIO_BUTTON_VIEW+" #SpiceRadioButton"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    def validate_printerUpdate_firmwareUpdate_doNotCheckForUpdates_option_isNotPresent(self):
        text_to_check = "do not check for updates"
        radio_button_count = self._spice.query_item(self.PRINTER_UPDATE_RADIO_BUTTON_VIEW)['count']
        for textNum in range(radio_button_count):
            actual_string = str(self._spice.query_item(self.PRINTER_UPDATE_RADIO_BUTTON_VALUE,textNum)['text']).lower()
            if(actual_string != text_to_check):
                    logging.info("Text did not match: "+ actual_string +" was found, expected text: "+text_to_check)
            assert actual_string != text_to_check, "Do Not Check For Updates option should not exist"
        current_button = self._spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
        current_button.mouse_click()