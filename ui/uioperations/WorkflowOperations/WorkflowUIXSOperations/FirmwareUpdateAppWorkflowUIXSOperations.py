import logging
import time
from dunetuf.ui.uioperations.BaseOperations.IFirmwareUpdateAppUIOperations import IFirmwareUpdateAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class FirmwareUpdateAppWorkflowUIXSOperations(IFirmwareUpdateAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    # Function objectIds
    FW_UPDATE_MSG_VIEW = "#bodyLayout"
    FW_UPDATE_MSG_CF_YES_BUTTON = "#fwupdateAvailableConfirmYes"
    FW_UPDATE_MSG_CF_NO_BUTTON = "#fwUpCheckUpdate"

    # options strings and value check
    FW_UPDATE_MSG_VALUE = "#fwupdateAvailableManualCheckContent #contentItem"
    FW_UPDATE_USB_CF_YES_VALUE = "#fwupdateAvailableConfirmYes #ContentItem SpiceText"
    FW_UPDATE_USB_CF_NO__VALUE = "#fwupdateAvailableConfirmNo #ContentItem SpiceText"

    # String id
    FIRMWARE_UPDATE_STR_ID =  "cDSUpdateChip"
    FW_UPDATE_USB_CF_YES_STR_ID = "cYes"
    FW_UPDATE_MSG_CF_NO_STR_ID = "cNo"

    def check_update_from_usb_iris_Disclaimer_message_layout(self, net):
        """
        Test to validate the Firmware update 'IRIS Declaimer message'
        """
        act_firmware_update_string = LocalizationHelper.get_string_translation(net, self.FIRMWARE_UPDATE_STR_ID)
        self._spice.wait_for(self.FW_UPDATE_MSG_VIEW)
        exp_firmware_update_string = self._spice.query_item(self.FW_UPDATE_MSG_VALUE)['text']

        logging.info("verify disclaimer message")
        assert act_firmware_update_string != "" and exp_firmware_update_string != "", "incorrect disclaimer message"
        assert act_firmware_update_string == exp_firmware_update_string, "incorrect disclaimer message"
        scrollbar = self._spice.wait_for("#fwupdateAvailable #verticalScroll")
        scrollbar.__setitem__("position",0.7)

    def check_firmware_update_yes_btn_text(self,net):
        """
        Test to validate the Firmware update 'Yes' button text
        """
        exp_fw_up_CfmYes_btn_txt = self._spice.query_item(self.FW_UPDATE_USB_CF_YES_VALUE)["text"]
        act_fw_up_CfmYes_btn_txt = LocalizationHelper.get_string_translation(net, self.FW_UPDATE_USB_CF_YES_STR_ID)
        assert exp_fw_up_CfmYes_btn_txt == act_fw_up_CfmYes_btn_txt, "error string on the screen"

    def check_firmware_update_no_btn_text(self, net):
        """
        Test to validate the Firmware update 'No' button text
        """
        exp_fw_up_CfmNo_btn_txt = self._spice.query_item(self.FW_UPDATE_USB_CF_NO__VALUE)['text']
        act_fw_up_CfmNo_btn_txt = LocalizationHelper.get_string_translation(net, self.FW_UPDATE_MSG_CF_NO_STR_ID)
        assert exp_fw_up_CfmNo_btn_txt == act_fw_up_CfmNo_btn_txt, "error string on the screen"

    def click_on_fw_update_cnf_yes_button(self):
        """
        Click 'Firmware Update Confirm Yes' button
        """
        fw_up_CfmYes_button = self._spice.query_item(self.FW_UPDATE_USB_CF_YES_VALUE)
        time.sleep(2)
        fw_up_CfmYes_button.mouse_click()

    def click_on_fw_update_cnf_no_button(self):
        """
        Click Firmware Update Confirm No' button
        """
        fw_up_CfmNo_button = self._spice.query_item(self.FW_UPDATE_USB_CF_NO__VALUE)
        time.sleep(2)
        fw_up_CfmNo_button.mouse_click()
