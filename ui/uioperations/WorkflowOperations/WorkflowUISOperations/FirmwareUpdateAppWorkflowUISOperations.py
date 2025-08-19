import time
import logging

from dunetuf.ui.uioperations.WorkflowOperations.FirmwareUpdateAppWorkflowUICommonOperations import IFirmwareUpdateAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

class FirmwareUpdateAppWorkflowUISOperations(IFirmwareUpdateAppUIOperations):

        # Function objectIds 
        FW_UPDATE_MSG_VIEW = "#bodyLayout"
        FW_UPDATE_MSG_CF_YES_BUTTON = "#fwupdateAvailableConfirmYes"
        FW_UPDATE_MSG_CF_NO_BUTTON = "#fwUpCheckUpdate"
        FW_UPDATE_PREPARING_UPDATE = "#progressBarDetail"
        FW_UPDATE_STATUS =  "#alertDetailDescription"
        PRINTER_UPDATE_RADIO_BUTTON_VIEW = "#radioButtonsViewlist1"

        # options strings and value check
        FW_UPDATE_MSG_VALUE = "#fwupdateAvailableManualCheckContent #contentItem"
        PRINTER_UPDATE_MSG_VALUE = "#irisMessage #irisMessageverticalLayout SpiceText"
        FW_UPDATE_USB_CF_YES_VALUE = "#fwupdateAvailableConfirmYes #ContentItem SpiceText"
        FW_UPDATE_USB_CF_NO__VALUE = "#fwupdateAvailableConfirmNo #ContentItem SpiceText"
        FW_UPDATE_STATUS_VALUE = "#alertDetailDescription SpiceText"
        PRINTER_UPDATE_RADIO_BUTTON_VALUE = PRINTER_UPDATE_RADIO_BUTTON_VIEW+" #SpiceRadioButton"

        # String id
        FIRMWARE_UPDATE_STR_ID =  "cDSUpdateChip"
        VISIT_WEBSITE_STR_ID = "cVisitCompanyWebsite"
        CF_FIRMWARE_UPDATE_STR_ID = "cConfirmFirmwareUpdate"
        FW_UPDATE_USB_CF_YES_STR_ID = "cYes"
        FW_UPDATE_MSG_CF_NO_STR_ID = "cNo"
        PRINTER_FW_UPDATE_STR_ID_List = ["cFirmwareUpdatesSecurity", "cPrinterDynamicSecurity", "cVisitCompanyWebsite", "cYourChoices", "cInstallNewUpdates", "cCheckUpdateNotify","cDoNotCheck", "cDSOOBESelectNext"]
        FWUPDATEUSBAPPAPPLICATIONVIEW = "#FwUpdateUSBAppApplicationStackView"
        HOME_BUTTON = "#HomeButton"

        def __init__(self, spice):
            self.maxtimeout = 10
            self._spice =  spice
                   
        # Firmware Update iris screen validation
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
            scrollbar.__setitem__("position",0.5)
                   
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

        def validate_printerUpdate_firmwareUpdate_irisDisclaimer_message(self, net):
            """
            Test to validate the printer update > firmware update 'IRIS Disclaimer message'
            """
            actual_string = expected_string = ""
            for id in self.PRINTER_FW_UPDATE_STR_ID_List:
                expected_string = expected_string + LocalizationHelper.get_string_translation(net, id)
            for textNum in range(3,19):
                actual_string = actual_string + self._spice.query_item(self.PRINTER_UPDATE_MSG_VALUE,textNum)['text']
            logging.info("Actual Disclaimer Message - "+actual_string)
            logging.info("Expected Disclaimer Message - "+expected_string)
            assert actual_string != "" and expected_string != "", "incorrect disclaimer message"   
            assert actual_string == expected_string , "incorrect disclaimer message"
        
        def validate_printerUpdate_firmwareUpdate_doNotCheckForUpdates_option_isNotPresent(self):
            text_to_check = "do not check for updates"
            radio_button_count = self._spice.query_item(self.PRINTER_UPDATE_RADIO_BUTTON_VIEW)['count']
            for textNum in range(radio_button_count):
                actual_string = str(self._spice.query_item(self.PRINTER_UPDATE_RADIO_BUTTON_VALUE,textNum)['text']).lower()
                if(actual_string != text_to_check):
                        logging.info("Text did not match: "+ actual_string +" was found, expected text: "+text_to_check)
                assert actual_string != text_to_check, "Do Not Check For Updates option should not exist"

        def click_home_button(self):
            """
            Click Home button to go back to Home screen. spice.goto_homescreen() doesn't work, then we create separate function here
            """
            logging.info("Go bck to Home screen by clicking Home button")
            current_view = self._spice.wait_for(self.FWUPDATEUSBAPPAPPLICATIONVIEW)
            self._spice.wait_until(lambda: current_view['visible'] is True)
            time.sleep(2)
            self._spice.wait_for(f"{self.FWUPDATEUSBAPPAPPLICATIONVIEW} {self.HOME_BUTTON}").mouse_click()
            time.sleep(2)
