#########################################################################################
# @file      IProSelectKeyboardOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      09-04-2021
# @brief     Interface for all the keyboard common methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class IProSelectKeyboardOperations(object):

    def keyboard_press_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_character(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_text(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_set_text_with_out_dial_action(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_number(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_clear_text(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
