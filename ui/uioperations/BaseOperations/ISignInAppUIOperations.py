#########################################################################################
# @file      ISignInAppUIOperations.py
# @author    Zachary Goodspeed (zachary.goodspeed@hp.com)
# @date      May 19, 2021
# @brief     Interface for all the Sign In UI navigation methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class ISignInAppUIOperations(object):
    def goto_windows_login(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def goto_sign_in_app(self, action:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def goto_windows_enter_creds(self, user:str, password:str, login:bool = True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    def verify_auth(self, expected_result:str):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def no_user_sign_in(self, net):
        '''
        UI should show Sign In string on home screen when no user login
        Args:
            net
        Return: sign in: True/False
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_admin_signin_page(self, time_out=10):
        """
        Method to wait admin signin screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_admin_signin_page_cancel_button(self):
        """
        Method to click cancel button in admin signin screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def support_sign_in_app_from_fp(self):
        """
        This function is to checek sign in app supported on printer ui or not

        Return: 
              True: sign in app supported on UI
              False: sign in app doesn't supported on UI
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

