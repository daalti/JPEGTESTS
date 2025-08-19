#########################################################################################
# @file      IInfoAppProSelectUIOperations.py
# @author    Daniel Fernandez Charro (daniel.fernandez.charro@hp.com)
# @date      21-03-2022
# @brief     Interface for all the Info UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys

class IInfoAppUIOperations(object):

    def goto_info_app(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
