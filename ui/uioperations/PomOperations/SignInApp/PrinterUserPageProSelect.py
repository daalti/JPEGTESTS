import logging
import time

from .LocatorsProSelect import LocatorsProSelect
from .Components.TextField import TextField

"""
    Must be on Sign In page to used this class.
"""

class PrinterUserPageProSelect():
    def __init__(self, page):
        self.__page = page
        self.__keyboard_character_list = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",",
            "-", ".", "/", ":", "[", "]", "\\", "^", "_", "`", ";", "<", "=", ">", "?", "@",
            "{", "|", "}", "~", "SPACE", "OK", "CLOSE", "BACKSPACE", "SHIFT", "NUMBERS"
        ]
        
    
    def __enter_each_character(self, text:str) -> bool:
        current_index = 0
        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        for character in text:
            if character.isupper():
                desired_index = self.__keyboard_character_list.index("SHIFT")
                difference = desired_index - current_index
                if difference > 0:
                    if not self.__page.scroll_right_increment(tumbler, difference): return False
                    current_index = desired_index
                elif difference < 0:
                    if not self.__page.scroll_left_increment(tumbler, abs(difference)): return False
                    current_index = desired_index
                if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False
                character = character.lower()
            desired_index = self.__keyboard_character_list.index(character)
            difference = desired_index - current_index
            if difference > 0:
                if not self.__page.scroll_right_increment(tumbler, difference): return False
                current_index = desired_index
            elif difference < 0:
                if not self.__page.scroll_left_increment(tumbler, abs(difference)): return False
                current_index = desired_index
            
            if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False
        return True

    def select_method(self) -> bool:
        """
            Selects 'Printer User' as sign in method
        """
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.PrinterUser) == False:
            logging.error("Failed to switch to Printer User sign in method")
            return False
        
        return True

    def enter_username(self, username:str) -> bool:
        printer_user_view = self.__page.wait_for_element(LocatorsProSelect.PrinterUserView)
        self.__page.scroll_right_increment(printer_user_view, 1)

        if not self.__page.wait_and_click(LocatorsProSelect.PrinterUserNameButton):
            logging.error("Failed to click User Name field")
            return False
        
        if not self.__enter_each_character(username):
            logging.error(f"Failed to enter \'{username}\' each character in username field")
            return False
        last_character_index = self.__keyboard_character_list.index(username[-1])
        difference = self.__keyboard_character_list.index("OK") - last_character_index

        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)

        if difference > 0:
            if not self.__page.scroll_right_increment(tumbler, difference): return False
        elif difference < 0:
            if not self.__page.scroll_left_increment(tumbler, abs(difference)): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(printer_user_view, 6): return False

        return True
    
    def enter_password(self, password:str) -> bool:
        printer_user_view = self.__page.wait_for_element(LocatorsProSelect.PrinterUserView)
        self.__page.scroll_right_increment(printer_user_view, 2)

        if not self.__page.wait_and_click(LocatorsProSelect.PrinterUserPasswordButton):
            logging.error("Failed to click Password field")
            return False

        tumbler = self.__page.wait_for_element(LocatorsProSelect.TumblerView)
        
        """
            NOTE: When you enter the Printer User Password view, you are put on the
                  numeric keyboard. We want to start on the alphabetical keyboard, so
                  we move to the "abc" button and click before proceeding.
        """
        if not self.__page.scroll_left_increment(tumbler, 1): return False
        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False
        if not self.__enter_each_character(password):
            logging.error(f"Failed to enter \'{password}\' each character in password field")
            return False
        last_character_index = self.__keyboard_character_list.index(password[-1])
        difference = self.__keyboard_character_list.index("OK") - last_character_index
        
        if difference > 0:
            if not self.__page.scroll_right_increment(tumbler, difference): return False
        elif difference < 0:
            if not self.__page.scroll_left_increment(tumbler, abs(difference)): return False

        if not self.__page.wait_and_click(LocatorsProSelect.KeyboardButton): return False

        if not self.__page.scroll_left_increment(printer_user_view, 7): return False

        return True

    def click_sign_in_button(self) -> bool:
        ldap_view = self.__page.wait_for_element(LocatorsProSelect.PrinterUserView)
        if not self.__page.scroll_right_increment(ldap_view, 3): return False

        if not self.__page.wait_and_click(LocatorsProSelect.PrinterUserSignInOkButton): return False

        return True
    
    def confirm_username_proceed_page(self, proceed:bool = True) -> bool:
        if proceed:
            button_locator = LocatorsProSelect.ConfrimOkButton
        else:
            button_locator = LocatorsProSelect.ConfirmCancelButton

        confirmation_message_view = self.__page.wait_for_element(LocatorsProSelect.ConfirmView)
        if not self.__page.scroll_right_increment(confirmation_message_view, 1): return False

        return self.__page.wait_and_click(button_locator)