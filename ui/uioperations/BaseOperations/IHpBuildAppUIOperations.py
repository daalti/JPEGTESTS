#########################################################################################
# @file      IHpBuildAppUIOperations.py
# @author    Shubham Khandelwal (shubham.khandelwal@hp.com)
# @date      12-06-2025
# @brief     Interface for all the Scan to HpBuild UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class IHpBuildAppUIOperations(object):

    def goto_scan_to_hpbuild(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)