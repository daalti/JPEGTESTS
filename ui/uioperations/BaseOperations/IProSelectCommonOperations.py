#########################################################################################
# @file      IProSelectCommonOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      20-10-2020
# @brief     Interface for all the UI dial methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys

class IProSelectCommonOperations(object):

    def goto_item(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_button_press(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_help_content(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sub_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_ethernet_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_or_close_button_press(self, close_or_back_button, landing_view):
        '''
        Press back/close button in specific screen.
        Args:
          close_or_back_button: close/back button object name
          landing_view: Landing screen after pressing back button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def scroll_to(self, view_locator:str, item_locator:str, timeout:float = 30) -> bool:
        """Scrolls horizontally within a view until a specific item gets focus.

        Args:
            view_locator (str): The locator for the scrollable view container.
            item_locator (str): The locator for the target item to scroll to.
            timeout (float, optional): Maximum time to wait while scrolling. Defaults to 30.

        Returns:
            bool: True if the item is found and focused, False otherwise.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
