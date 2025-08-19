#########################################################################################
# @file      IStatusCenterUIOperations.py
# @author    Andrew Rose (Andrew.Rose@hp.com)
# @date      Dec 5, 2022
# @brief     Interface for all the Status Center UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys

class IStatusCenterUIOperations(object):
    def goto_sign_in_app(self, action:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def verify_auth(self, expected_result:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def expand(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def collapse(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
