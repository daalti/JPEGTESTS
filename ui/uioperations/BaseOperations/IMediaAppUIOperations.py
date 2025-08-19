#########################################################################################
# @file      IMediaAppUIOperations.py
# @author    Carlos Criado (carlos.criado@hp.com)
# @date      25-11-2021
# @brief     Implementation for all the Media UI methods
# (c) Copyright HP Inc. 2021. All rights reserved.
#########################################################################################

import sys

class IMediaAppUIOperations(object):

    def goto_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_alert_dialog_window_type1(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_alert_dialog_window_type2(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_alert_dialog_window_type3(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_alert_dialog_window(self, alert_type):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_alert_dialog_toast_window(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_alert_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_message(self, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_alert_message_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_alert_message_details(self, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_custom_alert_message_details(self, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_custom_path_alert_message_details(self, path, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def validate_mediaMismatchTypeFlow_alert_message_details(self, net, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_toast_message(self, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def validate_sizeType_alert_title_and_message_details(self, net, locale, Size, PaperType):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def validate_trayOverfilled_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_error_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_image_status_error_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_custom_error_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_warning_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_informative_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_details_icon(self, image):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_stateDecorator_image_status_error_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
