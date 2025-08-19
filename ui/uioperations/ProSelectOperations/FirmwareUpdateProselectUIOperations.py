import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IFirmwareUpdateAppUIOperations import IFirmwareUpdateAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class FirmwareUpdateProselectUIOperations(IFirmwareUpdateAppUIOperations):


     # Function objectIds 
     MENU_LIST_LAYOUT = "#MenuListLayout"
     FW_UPDATE_MSG_VIEW = "#MessageLayout"
     FW_UPDATE_MSG_CF_YES_BUTTON = "#UpgradeNowButton #SpiceButton"
     FW_UPDATE_MSG_CF_NO_BUTTON = "#SkipButton #SpiceButton"
     PRINTER_UPDATE_RADIO_BUTTON_VIEW = "#RadioButtonListLayout"

     # options strings and value check
     FW_UPDATE_MSG_VALUE = "#DetailTexts SpiceText"
     FW_UPDATE_USB_CF_YES_VALUE = "#UpgradeNowButton #ContentItem SpiceText"
     FW_UPDATE_USB_CF_NO_VALUE = "#SkipButton #ContentItem SpiceText"
     FW_UPDATE_STATUS_VALUE = "#FwUpdateStatus #SpiceView"
     PRINTER_UPDATE_RADIO_BUTTON_VALUE = PRINTER_UPDATE_RADIO_BUTTON_VIEW+" #SpiceRadioButton"

     # String id
     FIRMWARE_UPDATE_STR_ID =  "cAFirmwareUpdate"
     VISIT_WEBSITE_STR_ID = "cVisitCompanyWebsite"
     CF_FIRMWARE_UPDATE_STR_ID = "cConfirmFirmwareUpdate"
     FW_UPDATE_USB_CF_YES_STR_ID = "cYes"
     FW_UPDATE_MSG_CF_NO_STR_ID = "cNo" 
     FW_UPDATE_PREPARING_UPDATE = "#PreparingUpdate"
     FW_UPDATE_STATUS =  "#FwUpdateStatus"
     PRINTER_FW_UPDATE_STR_ID = "cDSOOBEUpdateChip"

     def __init__(self, spice):
          self.maxtimeout = 10
          self._spice =  spice
          self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)
     # Firmware Update iris screen validation
     def check_update_from_usb_iris_Disclaimer_message_layout(self, net):
          """
          Test to validate the Firmware update 'IRIS Declaimer message'
          """
          act_firmwareUpdate_string = LocalizationHelper.get_string_translation(net, self.FIRMWARE_UPDATE_STR_ID)
          act_visitCompWebsite_string = LocalizationHelper.get_string_translation(net, self.VISIT_WEBSITE_STR_ID)
          act_confFirmUpdate_string = LocalizationHelper.get_string_translation(net, self.CF_FIRMWARE_UPDATE_STR_ID)

          act_final_string = act_firmwareUpdate_string +' \n' + act_visitCompWebsite_string + ' \n' + act_confFirmUpdate_string

          self._spice.wait_for(self.FW_UPDATE_MSG_VIEW)
          firmwareUpdate_string = self._spice.query_item(self.FW_UPDATE_MSG_VALUE)['text']
            
            
          assert firmwareUpdate_string == act_final_string, "error string on the screen"
            
            
     def check_firmware_update_yes_btn_text(self, net):
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
          exp_fw_up_CfmNo_btn_txt = self._spice.query_item(self.FW_UPDATE_USB_CF_NO_VALUE)['text']
          act_fw_up_CfmNo_btn_txt = LocalizationHelper.get_string_translation(net, self.FW_UPDATE_MSG_CF_NO_STR_ID)

          assert exp_fw_up_CfmNo_btn_txt == act_fw_up_CfmNo_btn_txt, "error string on the screen"
             
     def click_on_fw_update_cnf_yes_button(self, net):
          """
          Click 'Firmware Update Confirm Yes' button
          """
          currentScreen = self._spice.wait_for(self.MENU_LIST_LAYOUT)
          currentScreen.mouse_wheel(180, 180)
          time.sleep(1)
          currentScreen.mouse_click()
          time.sleep(1)
         
          fw_up_CfmYes_button = self._spice.query_item(self.FW_UPDATE_MSG_CF_YES_BUTTON)
          time.sleep(1)
          fw_up_CfmYes_button.mouse_click()
        
            
     def click_on_fw_update_cnf_no_button(self):
          """
          Click Firmware Update Confirm No' button
          """
          self.home_menu_dial_operations.menu_navigation(self._spice, self.FW_UPDATE_MSG_VIEW, self.FW_UPDATE_MSG_CF_NO_BUTTON)
         
     def validate_printerUpdate_firmwareUpdate_irisDisclaimer_message(self, net):
          """
          Test to validate the printer update > firmware update 'IRIS Disclaimer message'
          """
          actual_string = expected_string = ""
          expected_string = expected_string + LocalizationHelper.get_string_translation(net, self.PRINTER_FW_UPDATE_STR_ID)
          actual_string = actual_string + self._spice.query_item(self.FW_UPDATE_MSG_VALUE,0)['text']
          logging.info("Actual Disclaimer Message - "+actual_string)
          logging.info("Expected Disclaimer Message - "+expected_string)
          assert actual_string != "" and expected_string != "", "incorrect disclaimer message"   
          assert expected_string == actual_string, "incorrect disclaimer message"
        
     def validate_printerUpdate_firmwareUpdate_doNotCheckForUpdates_option_isNotPresent(self):
          text_to_check = "do not check for updates"
          radio_button_count = 2
          for textNum in range(radio_button_count):
               actual_string = str(self._spice.query_item(self.PRINTER_UPDATE_RADIO_BUTTON_VALUE,textNum)['text']).lower()
               if(actual_string != text_to_check):
                    logging.info("Text did not match: "+ actual_string +" was found, expected text: "+text_to_check)
               assert actual_string != text_to_check, "Do Not Check For Updates option should not exist"