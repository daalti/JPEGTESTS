#########################################################################################
# @file      IComputerAppUIOperations.py
# @author    Mangesh Patil (mangesh.patil1@hp.com)
# @date      21-06-2021
# @brief     Interface for all the Scan to Computer UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys


class IComputerAppUIOperations(object):

    def goto_scan_to_computer(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_scan_computer_web_setup_ok(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_scan_computer_software_setup_ok(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_computer_not_configured(self):
        '''
        UI wait for computer not configured
        '''        
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)