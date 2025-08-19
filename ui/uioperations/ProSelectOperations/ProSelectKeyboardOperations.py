#########################################################################################
# @file      ProSelectKeyboardOperations.py
# @author    Leena D Murdeshwar (leena-d.murdeshwar@hp.com)
# @date      09-04-2021
# @brief     All operations related to keyboard on UI 
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import  sys
import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IProSelectKeyboardOperations import IProSelectKeyboardOperations

_logger = logging.getLogger(__name__)

alpha_numeric_keys = {
  "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
  "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23,
  "x": 24, "y": 25, "z": 26, "0": 27, "1": 28, "2": 29, "3": 30, "4": 31, "5": 32, "6": 33, "7": 34, 
  "8": 35, "9": 36,"!" : 37,"\"":38, "#": 39, "$": 40, "%": 41 ,"&": 42 , "'": 43, "(": 44 ,")": 45, 
  "*": 46,"+":47 , ",": 48 , "-": 49 ,".": 50, "/": 51,":": 52, "[": 53,"]":54,"\\":55,"^": 56 ,"_":57, 
  "`": 58,";": 59,"<": 60, "=": 61, ">": 62, "?": 63, "@": 64 , "{": 65, "|": 66 ,"}": 67, "~": 68
    }

icon_keys = {
    "spacebar": 69, "done": 70, "backspace": 71, "language": 72, "shift_off": 73, "symbols": 74, "alphabet": 75, "numeric": 76, 
}

icon_coords = {
    "#SpiceKeyBoardbutton_en" : { "row": 3, "pos": 5 },
    "#SpiceKeyBoardbutton_ba" : { "row": 0, "pos": 10 },
    "#SpiceKeyBoardbutton_caps": { "row": 2, "pos": 0 },
    "#SpiceKeyBoardbutton_sp": { "row": 3, "pos": 2 },
    "#SpiceKeyBoardbutton_sh1": { "row": 3, "pos": 3 },
    "#SpiceKeyBoardbutton_sh2": { "row": 3, "pos": 4 }
}

keyboardInputObject = "#TextInputArea"

class ProSelectKeyboardOperations(IProSelectKeyboardOperations):

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice

    def keyboard_press_icon(self, object_id, index_value = 0, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Numerics, Close, Language, Alphabet, Symbols, Space)
          dial_val: Direction for dialing
        '''
        current_screen = self._spice.wait_for("#spiceKeyboardView")

        while True:
            try:
                self._spice.query_item(object_id)["iconCurrent"]
                while (self._spice.query_item(object_id, index_value)["iconCurrent"] != True):
                    current_screen.mouse_wheel(dial_val, dial_val)
                    time.sleep(0.5)
                current_screen.mouse_click()
                break
            except:
                current_screen.mouse_wheel(dial_val, dial_val)
                time.sleep(0.5)
                pass

        time.sleep(0.5)

    def keyboard_enter_character(self, character, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press alphabets, numbers or special characters in alphanumeric keyboard
        Args:
          character: character to be entered
          dial_val: Direction for dialing
        '''
        current_screen = self._spice.wait_for("#spiceKeyboardView")

        while True:
            try:
                self._spice.query_item("#Key" + character)
                while (self._spice.query_item("#Key" + character)["color"] != "#000000"):
                    current_screen.mouse_wheel(dial_val, dial_val)
                    time.sleep(0.5)
                current_screen.mouse_click()
                break

            except:
                current_screen.mouse_wheel(dial_val, dial_val)
                time.sleep(0.5)
                pass

        time.sleep(0.5)

    def keyboard_enter_text(self, text:str, check: bool = True):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of alphabets, numbers, special charecters and space text
        Args:
          text: text to be entered
        '''
        current_position = alpha_numeric_keys['a']
        is_icon = False
        # Delete pre-existing text, if any
        text_length = len(self._spice.wait_for("#TextInputArea")["inputText"])
        if (text_length > 0):
            for i in range(text_length):
                self.keyboard_press_icon("#ItemIconDelegatebackspace_xs", dial_val = 0)
            current_position = icon_keys['backspace']
            is_icon = True
            time.sleep(1)

        assert len(self._spice.query_item("#TextInputArea")["inputText"]) == 0 #Empty

        time.sleep(1)
        for i in range(len(text)):
            new_char = text[i]
            if new_char.isalpha() and new_char.isupper():
                # Press Shift key to get upper case characters
                if is_icon == True: #navigate from icon
                    if (icon_keys['shift_off'] < current_position): #and (current_position < alpha_numeric_keys["7"]):
                        dial_value = 0 # dial left
                    else:
                        dial_value = 180 # dial right
                else:# navigate from non-icon
                    # alpha_numeric_keys['9'] is approx. middle value in the dial keyboard
                    if (current_position < alpha_numeric_keys['9']):
                        dial_value = 0
                    else:
                        dial_value = 180

                self.keyboard_press_icon("#ItemIconDelegateshift_off_xs", dial_value)
                current_position = icon_keys['shift_off']

                # Character in object id is always lower case
                new_char = new_char.lower()
                new_position = alpha_numeric_keys[new_char]
                if (new_position >= alpha_numeric_keys['9']):
                    dial_value = 0
                else:
                    dial_value = 180
                self.keyboard_enter_character(new_char, dial_value)
                current_position = new_position
                is_icon = False

            elif new_char == " ":# Space
                if (current_position < alpha_numeric_keys['9']):
                    dial_value = 0
                else:
                    dial_value = 180
                self.keyboard_press_icon("#ItemIconDelegatespacebar_xs", dial_value)
                current_position = icon_keys['spacebar']
                is_icon == True

            else:
                # Enter lower case alphabets, special characters and numbers
                new_position = alpha_numeric_keys[new_char]
                # alpha_numeric_keys['9'] is approx. middle value in the dial keyboard
                if (new_position >= current_position) and ((new_position - current_position) < alpha_numeric_keys['9']):
                    dial_value = 180 # dial right
                else:
                    dial_value = 0 # dial left
                self.keyboard_enter_character(new_char, dial_value)
                current_position = new_position

        if (check == True):
            if (len(text) > 0): # Check for text to be entered is not empty
                text_entry = self._spice.query_item("#TextInputArea")["inputText"]
                if text_entry != text:
                    self.keyboard_press_icon("#ItemIconDelegateclose_xs", dial_val = 0)
                assert text_entry == text
                          
        # Press done key
        if (current_position < alpha_numeric_keys['9']):
            dial_value = 0
        else:
            dial_value = 180
        self.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", dial_value)

    def keyboard_set_text_with_out_dial_action(self, input_string, index_value=0):
        '''
        UI should be at keyboard view
        input_string text which consists of alphabets, numbers, special charecters and space text
        without dial action. directly set value to keyboard 
        This method is preferred if you are not testing keyboard dialing. It will save lot of time
        Args:
          input_string: text to be entered
        '''
        keyboardTextField = self._spice.wait_for("#spiceKeyboardView", timeout=5, query_index=index_value)
        keyboardTextField["currentText"] = input_string
        
        # Press done key
        self.keyboard_press_icon("#ItemIconDelegatecheckmark_xs",index_value, 0)
    
    def keyboard_press_icon_ok_button(self, object_id, index_value = 0, dial_val:int = 180):
        '''
        UI should be at alphabetic keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Space, Left and Right Arrows)
        '''
        assert self._spice.wait_for("#spiceKeyboardView")
        key = self._spice.wait_for(object_id)

        self.go_to_row(icon_coords[object_id]["row"])
        self.go_to_pos(icon_coords[object_id]["pos"])
        key.mouse_click()

    def keyboard_enter_number(self, text:str):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of numbers and space
        Args:
          text: number to be entered
        '''
        #clear text entered
        keyboardTextField = self._spice.query_item("#spiceKeyboardView")
        keyboardTextField["currentText"] = ""

        self.keyboard_press_icon("#ItemIconDelegatenumerics", 0)
        current_position = alpha_numeric_keys['0']
        is_icon = True
        time.sleep(1)
        for i in range(len(text)):
            new_char = text[i]
            new_position = alpha_numeric_keys[new_char]
            if (new_position >= current_position) and ((new_position - current_position) < alpha_numeric_keys['!']):
                dial_value = 180 # dial right
            else:
                dial_value = 0 # dial left
            self.keyboard_enter_character(new_char, dial_value)
            current_position = new_position
        
        if (len(text) > 0): # Check for text to be entered is not empty
            text_entry = self._spice.query_item("#TextInputArea")["inputText"]
            assert text_entry == text
            # Press done key
            if (current_position < alpha_numeric_keys['!']):
                dial_value = 0
            else:
                dial_value = 180
            self.keyboard_press_icon("#ItemIconDelegatecheckmark", dial_value)

    def keyboard_enter_pin(self, text):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of numbers and space
        Args:
          text: number to be entered
        '''
        #clear text entered
        keyboardTextField = self._spice.query_item("#spiceKeyboardView")
        keyboardTextField["currentText"] = ""

        current_position = alpha_numeric_keys['0']
        #is_icon = True
        time.sleep(1)
        for i in range(len(text)):
            new_char = text[i]
            new_position = alpha_numeric_keys[new_char]
            if (new_position >= current_position) and ((new_position - current_position) < alpha_numeric_keys['!']):
                dial_value = 180 # dial right
            else:
                dial_value = 0 # dial left
            self.keyboard_enter_character(new_char, dial_value)
        if (len(text) > 0): # Check for text to be entered is not empty
            text_entry = self._spice.query_item("#TextInputArea")["inputText"]
            assert text_entry == text
            # Press done key
            if (current_position < alpha_numeric_keys['!']):
                dial_value = 0
            else:
                dial_value = 180
            self.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", dial_value)

    def keyboard_enter_password(self, text):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of numbers and space
        Args:
          text: number to be entered
        '''
        #clear text entered
        keyboardTextField = self._spice.query_item("#spiceKeyboardView")
        keyboardTextField["currentText"] = ""

        current_position = alpha_numeric_keys['0']
        #is_icon = True
        time.sleep(1)
        for i in range(len(text)):
            new_char = text[i]
            new_position = alpha_numeric_keys[new_char]
            if (new_position >= current_position) and ((new_position - current_position) < alpha_numeric_keys['!']):
                dial_value = 180 # dial right
            else:
                dial_value = 0 # dial left
            self.keyboard_enter_character(new_char, dial_value)
        if (len(text) > 0): # Check for text to be entered is not empty
            text_entry = self._spice.query_item("#TextInputArea")["inputText"]
            assert text_entry == text
            # Press done key
            if (current_position < alpha_numeric_keys['!']):
                dial_value = 0
            else:
                dial_value = 180
            self.keyboard_press_icon("#ItemIconDelegatecheckmark_xs", dial_value)

    def keyboard_clear_text(self, index_value = 0):
        '''
        Method to clear text box
        UI should be on keyboard view before calling this method
        '''
        keyboard = self._spice.wait_for("#spiceKeyboardView", query_index = index_value)
        keyboard['currentText'] = ""

        assert len(self._spice.query_item("#TextInputArea", index_value)["inputText"]) == 0 #Empty
        