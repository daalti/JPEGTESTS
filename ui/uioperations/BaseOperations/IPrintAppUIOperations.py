#########################################################################################
# @file      IPintAppUIOperations.py
# @author    Neha Patel (neha.patel@hp.com)
# @date      07-09-2020
# @brief     Interface for all the Settings-Print-Print Quality navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys

class IPintAppUIOperations(object):

    def check_less_paper_curl_btn_text(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_cleanbelt_label_visibility(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def is_less_paper_curl_toggle_btn_checked(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_less_paper_curl_toggle(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_less_paper_curl_toggle(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_clean_belt_toast_message(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    