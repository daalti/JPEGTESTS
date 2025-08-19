#########################################################################################
# @file      ISuppliesAppUIOperations.py
# @author    Neha Patel(neha.patel@hp.com)
# @date      27-10-2021
# @brief     Interface for all the Supplies Message Laypout methods
# (c) Copyright HP Inc. 2021. All rights reserved.
###########################################################################################
import sys

class ISuppliesAppUIOperations(object):

    def goto_alert_message_layout_screen(self,timeout=7):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_message_icon_display(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_alert_message(self):
       raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_message(self, expected_title_text):
       raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_supply_icon_display(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_alert_message_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_message_details(self, expected_detail_text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_button(self , button_text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def settings_supplies_verylowbehavior(self, spice, cdm, cartridge = 0):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def settings_supplies_lowwarningthreshold(self, spice, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def settings_supplies_storesupplyusagedata(self, spice, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def settings_supplies_authorizedhpcartridgepolicy(self, spice, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def settings_supplies_cartridgeprotection(self, spice, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ui_shows_validating_state(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_cartridges_ui_alert(self, title, details_key):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)