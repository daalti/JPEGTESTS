#########################################################################################
# @file      IHelpAppUIOperations.py
# @author    Dylan Leman (dylan.leman@hp.com)
# @date      2-1-2023
# @brief     Interface for all the Help App UI navigation methods
# (c) Copyright HP Inc. 2023. All rights reserved.
###########################################################################################
import sys

class IHelpAppUIOperations(object):

    def goto_help_app(self):
        """
        Function to navigate to Help app on home screen
        Ui Flow: Any screen -> Home screen -> Help app
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)