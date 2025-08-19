#########################################################################################
# @file      ProSelectHybridKeyboardOperations.py
# @author    Joe Hillard (joe.hillard@hp.com)
# @date      03-03-2023
# @brief     All operations related to keyboard on UI 
# (c) Copyright HP Inc. 2023. All rights reserved.
###########################################################################################
import  sys
import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IProSelectKeyboardOperations import IProSelectKeyboardOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectUIObjectIds import ProSelectUIObjectIds
from enum import Enum

_logger = logging.getLogger(__name__)


layouts = [
    [ 
    { "q": 0, "w": 1, "e": 2, "r": 3, "t": 4, "y": 5, "u": 6, "i": 7, "o": 8, "p": 9, "ba": 10 },
    { "a": 0, "s": 1, "d": 2, "f": 3, "g": 4, "h": 5, "j": 6, "k": 7, "l": 8, "_": 9, ".": 10 },
    { "caps": 0, "z": 1, "x": 2, "c": 3, "v": 4, "b": 5, "n": 6, "m": 7, "-": 8, "@": 9 },
    { "12?": 0, ".com": 1, "sp": 2, "sh1": 3, "sh2": 4, "en": 5 }
    ],

    [
    { "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "0": 9, "ba": 10 },
    { "!": 0, "/": 1, ":": 2, ";": 3, "(": 4, ")": 5, "$": 6, "&": 7, "`": 8, "-": 9, "~": 10 },
    { "#+=": 0, "'": 1, "|": 2, "?": 3, "_": 4, ",": 5, ".": 6, "@": 7  },
    { "abc": 0, ".com": 1, "sp": 2, "sh1": 3, "sh2": 4, "en": 5 }
    ],

    [
    { "[": 0, "]": 1, "{": 2, "}": 3, "#": 4, "%": 5, "^": 6, "*": 7, "+": 8, "=": 9, "ba": 10 },
    { "!": 0, "\\": 1, ":": 2, "<": 3, ">": 4, "¥": 5, "£": 6, "€": 7, "`": 8, "-": 9, "~": 10 },
    { "12?": 0, "'": 1, "|": 2, "?": 3, "_": 4, ",": 5, ".": 6, "@": 7 },
    { "abc": 0, ".com": 1, "sp": 2, "sh1": 3, "sh2": 4, "en": 5 }
    ]
]

icon_coords = {
    "#SpiceKeyBoardbutton_en" : { "row": 3, "pos": 5 },
    "#SpiceKeyBoardbutton_ba" : { "row": 0, "pos": 10 },
    "#SpiceKeyBoardbutton_caps": { "row": 2, "pos": 0 },
    "#SpiceKeyBoardbutton_sp": { "row": 3, "pos": 2 },
    "#SpiceKeyBoardbutton_sh1": { "row": 3, "pos": 3 },
    "#SpiceKeyBoardbutton_sh2": { "row": 3, "pos": 4 }
}

class KeyboardType:
    ALPHABET = 0
    NUMERIC = 1
    SYMBOLIC = 2

keyboardInputObject = "#hybridKeyboardTextInputArea"

class ProSelectHybridKeyboardOperations(IProSelectKeyboardOperations):

    current_row = 0
    current_pos = 0
    current_keyboard_type = KeyboardType.ALPHABET

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        self.proselect_common_operations = ProSelectCommonOperations(spice)
        self.reset()


    def reset(self):
        ProSelectHybridKeyboardOperations.current_row = 0
        ProSelectHybridKeyboardOperations.current_pos = 0
        ProSelectHybridKeyboardOperations.current_keyboard_type = KeyboardType.ALPHABET


    def go_to_row(self, dest_row):
        """
        UI should be at hybrid keyboard view.
        Move the focused key to the specified row.
        """
        keyboard = self._spice.wait_for("#spiceKeyboardHybridView")
        assert keyboard

        _logger.debug("current row is %i" % ProSelectHybridKeyboardOperations.current_row)
        cur_row = ProSelectHybridKeyboardOperations.current_row
        if (cur_row == dest_row):
            return
        while (cur_row != dest_row):
            if dest_row > cur_row:
                keyboard.keypad_down()
                cur_row += 1
            else:
                keyboard.keypad_up()
                cur_row -= 1
        
        ProSelectHybridKeyboardOperations.current_row = cur_row


    def go_to_pos(self, dest_pos):
        """
        UI should be at the hybrid keyboard view.
        Move the focused key to the specified position in the row.
        """
        keyboard = self._spice.wait_for("#spiceKeyboardHybridView");
        assert keyboard

        _logger.debug("current pos is %i" % ProSelectHybridKeyboardOperations.current_pos)
        cur_pos = ProSelectHybridKeyboardOperations.current_pos
        if (cur_pos == dest_pos):
            return
        while (cur_pos != dest_pos):
            if dest_pos > cur_pos:
                keyboard.keypad_right()
                cur_pos += 1
            else:
                keyboard.keypad_left()
                cur_pos -= 1
        
        ProSelectHybridKeyboardOperations.current_pos = cur_pos


    def goto(self, character):
        dest_row = 0
        dest_pos = -1
        for row in layouts[ProSelectHybridKeyboardOperations.current_keyboard_type]:
            if character in row:
                dest_pos = row[character]
                break
            dest_row += 1
        
        assert dest_pos >= 0, "Unable to find location of key %s in layouts map" % character
        self.go_to_row(dest_row)
        self.go_to_pos(dest_pos)
                

    def keyboard_press_icon(self, object_id, index_value = 0, dial_val:int = 180, return_home = True):
        '''
        UI should be at alphabetic keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Space, Left and Right Arrows)
        '''
        assert self._spice.wait_for("#spiceKeyboardHybridView")
        key = self._spice.wait_for(object_id)

        self.go_to_row(icon_coords[object_id]["row"])
        self.go_to_pos(icon_coords[object_id]["pos"])
        key.mouse_click()
        if (return_home):
            self.go_to_pos(0)
            self.go_to_row(0)

    def keyboard_press_icon_ok_button(self, object_id, index_value = 0, dial_val:int = 180):
        '''
        UI should be at alphabetic keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Space, Left and Right Arrows)
        '''
        assert self._spice.wait_for("#spiceKeyboardHybridView")
        key = self._spice.wait_for(object_id)

        self.go_to_row(icon_coords[object_id]["row"])
        self.go_to_pos(icon_coords[object_id]["pos"])
        key.mouse_click()
        
        

    def change_layout(self, layout_type):
        switched = False

        if layout_type == KeyboardType.ALPHABET:
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.ALPHABET:
                key = self._spice.wait_for("#SpiceKeyBoardbutton_abc")
                self.goto("abc")
                key.mouse_click()
                self.go_to_pos(0)
                switched = True

        elif layout_type == KeyboardType.NUMERIC:
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.NUMERIC:
                key = self._spice.wait_for("#SpiceKeyBoardbutton_12?")
                self.goto("12?")
                key.mouse_click()
                self.go_to_pos(0)
                switched = True

        elif layout_type == KeyboardType.SYMBOLIC:
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.SYMBOLIC:
                if ProSelectHybridKeyboardOperations.current_keyboard_type == KeyboardType.ALPHABET:
                    key = self._spice.wait_for("#SpiceKeyBoardbutton_12?")
                    self.goto("12?")
                    key.mouse_click()
                    self.go_to_pos(0)
                    ProSelectHybridKeyboardOperations.current_row = 0
                    ProSelectHybridKeyboardOperations.current_pos = 0
                    ProSelectHybridKeyboardOperations.current_keyboard_type = KeyboardType.NUMERIC

                key = self._spice.wait_for("#SpiceKeyBoardbutton_#+=")
                self.goto("#+=")
                key.mouse_click()
                self.go_to_pos(0)
                switched = True

        else:
            logging.error("Invalid layout type specified")

        if switched:
            ProSelectHybridKeyboardOperations.current_row = 0
            ProSelectHybridKeyboardOperations.current_pos = 0
            ProSelectHybridKeyboardOperations.current_keyboard_type = layout_type


    def keyboard_enter_character(self, character, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press alphabets, numbers or special characters in alphanumeric keyboard
        Args:
          character: character to be entered
          dial_val: Direction for dialing
        '''
        assert self._spice.wait_for("#spiceKeyboardHybridView")

        #To check whther the key board layout has alphabets
        if character.isalpha():
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.ALPHABET:
                self.change_layout(KeyboardType.ALPHABET)

            if character.islower():
                if self._spice.query_item("#spiceKeyboardHybridView")["capsLock"] == True:
                    self.keyboard_press_icon("#SpiceKeyBoardbutton_caps") 
                
                key = self._spice.wait_for("#SpiceKeyBoardbutton_" + character)
                self.goto(character)
                key.mouse_click()
                self.go_to_pos(0)
                self.go_to_row(0)

            elif character.isupper():
                if self._spice.query_item("#spiceKeyboardHybridView")["capsLock"] == False:
                    self.keyboard_press_icon("#SpiceKeyBoardbutton_caps") 
                key = self._spice.wait_for("#SpiceKeyBoardbutton_" + character.lower())
                self.goto(character.lower())
                key.mouse_click()
                self.go_to_pos(0)
                self.go_to_row(0)

        # To enter numeric  values
        elif character.isnumeric():
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.NUMERIC:
                self.change_layout(KeyboardType.NUMERIC)
            key = self._spice.wait_for("#SpiceKeyBoardbutton_" + character)
            self.goto(character)
            key.mouse_click()
            self.go_to_pos(0)
            self.go_to_row(0)

        # To enter space    
        elif character == " ":    
            self.keyboard_press_icon("#SpiceKeyBoardbutton_sp")

        # To enter symbols  
        else:
            if ProSelectHybridKeyboardOperations.current_keyboard_type != KeyboardType.SYMBOLIC:
                self.change_layout(KeyboardType.SYMBOLIC)
            key = self._spice.wait_for("#SpiceKeyBoardbutton_" + character)
            self.goto(character)
            key.mouse_click()
            self.go_to_pos(0)
            self.go_to_row(0)


    def keyboard_enter_text(self, text:str, check: bool = True):
        '''
        UI should be at the keyboard view
        Enter text which consists of alphabets, numbers, special charecters and space text
        Args:
          text: text to be entered
        '''
    
        self.keyboard_clear_text()

        for character in text:
            self.keyboard_enter_character(character)
        

    def keyboard_set_text_with_out_dial_action(self, input_string, index_value=0):
        '''
        UI should be at keyboard view
        input_string text which consists of alphabets, numbers, special charecters and space text
        without manual action. It will directly set value to keyboard 
        
        Args:
          input_string: text to be entered
        '''
        keyboardTextField = self._spice.wait_for("#hybridKeyboardTextInputArea")
        keyboardTextField["inputText"] = input_string
        keyboardTextField["cursorPosition"] = len(input_string)


    def keyboard_clear_text(self, index_value=0):
        '''
        Method to clear text box
        UI should be on keyboard view before calling this method
        '''
        text_input_area = self.proselect_common_operations.get_element(ProSelectUIObjectIds.HybridKeyboardTextInputArea)
        if not text_input_area:
            logging.error(f"Failed to get Hybrid Keyboard Text Input Area: {ProSelectUIObjectIds.HybridKeyboardTextInputArea}")
            return
        current_text_length = len(self.proselect_common_operations.get_element_property(text_input_area, "inputText"))
        if current_text_length == 0: return

        for i in range(current_text_length):
            self.keyboard_press_icon(ProSelectUIObjectIds.HybridKeyboardBackspaceButton, bool(i != current_text_length - 1))
            
        assert len(self.proselect_common_operations.get_element_property(text_input_area, "inputText")) == 0
