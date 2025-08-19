#########################################################################################
# @file      IFirmwareUpdateAppUIOperations.py
# @author    Neha Patel(neha.patel@hp.com)
# @date      05-02-2022
# @brief     Interface for all the Firmware Update methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys

class IFirmwareUpdateAppUIOperations(object):

    def check_update_from_usb_iris_Disclaimer_message_layout(self,net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_firmware_update_yes_btn_text(self,net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_firmware_update_no_btn_text(self,net):
       raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_on_fw_update_cnf_yes_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_on_fw_update_cnf_no_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def validate_printerUpdate_firmwareUpdate_irisDisclaimer_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_home_button(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
