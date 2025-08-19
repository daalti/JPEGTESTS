#########################################################################################
# @file     ITraysAppUIOperations.py
# @authors  Mohammed Haris (mohammed.haris@hp.com)
# @date     01-06-2023
# @brief    Interface for all the Trays UI navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class ITraysAppUIOperations(object):

    def goto_tray1(self):
        '''
        Navigates to Tray1 from Home Screen
        UI Flow is Home->Menu->Trays->Tray1
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_tray2(self):
        '''
        Navigates to Tray2 from Home Screen
        UI Flow is Home->Menu->Trays->Tray1
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_tray_media_size_string_a5_and_a5_rotated(self):
        '''
        Verify tray media sizes a5 and a5 rotated have the expected string
        UI Should be in the specific Tray screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_modifyTray(self):
        '''
        ProSelect and Workflow have different design implementations resulting
        in Workflow requiring an extra step to modify its paper size and type.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def finish_modifyTray(self):
        '''
        ProSelect and Workflow have different design implementations resulting
        in Workflow requiring an extra step to modify its paper size and type.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def modify_tray_size_letter(self):
        '''
        Modify tray size to letter
        UI Should be in the specific Tray screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def modify_tray_type_plain(self):
        '''
        Modify tray type to plain
        UI Should be in the specific Tray screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

