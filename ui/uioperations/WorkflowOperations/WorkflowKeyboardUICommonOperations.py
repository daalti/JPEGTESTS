
import  sys
import time
import logging

#TODO:Import keyboard
from dunetuf.ui.uioperations.BaseOperations.IWorkflowKeyboardUICommonOperations import IWorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowUICommonOperations import FaxAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.cdm import CDM


_logger = logging.getLogger(__name__)

alpha_numeric_keys = {
  "a": "1", "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
  "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23,
  "x": 24, "y": 25, "z": 26, "0": 27, "1": 28, "2": 29, "3": 30, "4": 31, "5": 32, "6": 33, "7": 34, 
  "8": 35, "9": 36,"!" : 37,"\"":38, "#": 39, "$": 40, "%": 41 ,"&": 42 , "'": 43, "(": 44 ,")": 45, 
  "*": 46,"+":47 , ",": 48 , "-": 49 ,".": 50, "/": 51,":": 52, "[": 53,"]":54,"\\":55,"^": 56 ,"_":57, 
  "`": 58,";": 59,"<": 60, "=": 61, ">": 62, "?": 63, "@": 64 , "{": 65, "|": 66 ,"}": 67, "~": 68
    }

special_char_keys ={
    "@":"#keyAt", "#":"#keyNumberSign", "%":"#keyPercent", "&":"#keyAmpersand", "*":"#keyAsterisk", "-":"#keyMinus",
    "+":"#keyPlus", "(":"#keyParentLeft", ")":"#keyParentRight", "!":"#keyExclam", "<":"#keyLess", ">":"#keyGreater",
    "'":"#keyApostrophe", ":":"#keyColon", ";":"#keySemicolon", "?":"#keyQuestion", "{":"#keyBraceLeft", "/":"#keySlash", 
    "~":"#keyAsciiTilde", "`":"#keyAgrave", "|":"#keyBar", ".":"#keyDot", "√":"#keySquareroot", "÷":"#keyDivision",
    "×":"#keyMultiply", "½":"#keyOnehalf", "{":"#keyBraceLeft", "}":"#keyBraceRight", "$":"#keyDollar", "€":"#keyEuro",
    "£":"#keyPound", "¢":"#keyCent", "¥": "#keyYen", "=":"#keyEqual", "§":"#keySection", "[":"#keyBracketLeft",
    "]":"#keyBracketRight", "_":"#keyUnderScore", "™":"#keyTradeMark", "®":"#keyRegisterMark", "«":"#keyGuillemotleft",
    "»":"#keyGuillemotright", "^": "#keyAsciiCircum" , "." :"#keyPeriod", "," : "#keyComma"
}
 
icon_keys = {
    "spacebar": 69, "done": 70, "backspace": 71, "language": 72, "shift_off": 73, "symbols": 74, "alphabet": 75, "numeric": 76, 
}

class WorkflowKeyboardUICommonOperations(IWorkflowKeyboardUICommonOperations):

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        #self.faxoperations = FaxAppWorkflowUICommonOperations(self._spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.MenuApp_Workflow_UI_Common_Operations = spice.menu_operations

    def keyboard_press_icon(self, object_id, index_value = 0, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press special icons in alphanumeric keyboard
        Args:
          object_id: Object id of the icon (Done, Backspace, Shift, Numerics, Close, Language, Alphabet, Symbols, Space)
          dial_val: Direction for dialing
        '''
        assert self._spice.wait_for("#spiceKeyboardView")
        key = self._spice.wait_for(object_id)
        key.mouse_click()     
        time.sleep(0.5)

    def keyboard_enter_character(self, character, dial_val:int = 180):
        '''
        UI should be at alphanumeric keyboard view
        Press alphabets, numbers or special characters in alphanumeric keyboard
        Args:
          character: character to be entered
          dial_val: Direction for dialing
        '''
        assert self._spice.wait_for("#spiceKeyboardView")
        #To check whther the key board layout has alphabets
        if character.isalpha():
            if self._spice.wait_for("#symbolModeKey")["displayText"] == "ABC" or self._spice.wait_for("#symbolModeKey")["displayText"] == "abc":
                self.keyboard_press_icon("#symbolModeKey")
            if character.islower():
                if self._spice.wait_for("#keyShift")["uppercased"] == True:
                    self.keyboard_press_icon("#keyShift") 
                character = character.upper()    # Object names of keys are with Uppercase letters hence converting character to upper 
                key = self._spice.wait_for("#key" + character)
                key.mouse_click()
            elif character.isupper():
                if self._spice.wait_for("#keyShift")["uppercased"] == False:
                    self.keyboard_press_icon("#keyShift") 
                key = self._spice.wait_for("#key" + character)
                key.mouse_click()
        # To enter Numeric values
        elif character.isnumeric():
            if self._spice.wait_for("#symbolModeKey")["displayText"] == "&123":
                self.keyboard_press_icon("#symbolModeKey")
            key = self._spice.wait_for("#key" + character)
            key.mouse_click()
        # To enter space    
        elif character == " ":    
            self.keyboard_press_icon("#spaceKey")
        # To enter Special Characters  
        else:
            if self._spice.wait_for("#symbolModeKey")["displayText"] == "&123":
                self.keyboard_press_icon("#symbolModeKey")
            try:    
                key = self._spice.wait_for(special_char_keys[character] ,5)
                key.mouse_click() 
            except Exception as e:
                self.keyboard_press_icon("#key1By21")
                key = self._spice.wait_for(special_char_keys[character], 5)
                key.mouse_click()
                try:
                    self.keyboard_press_icon("#key2By21")
                except:
                    self.keyboard_press_icon("#key1By21")

            
                
            
    def keyboard_enter_text(self, text:str, textfield_objectid, check: bool = True,append = False):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of alphabets, numbers, special charecters and space text
        Args:
          text: text to be entered
          textfield_objectid: text filed objectId
          append : True or false,  if true the text will be entered without clearing the field and wont save the text

        '''
       
        # Delete pre-existing text, if any'''
        if append == False:
            self.keyboard_clear_text(textfield_objectid)
        time.sleep(1)
        for new_char in text:
            self.keyboard_enter_character(new_char)
        #To save the text entered 
        if self._spice.query_item("#symbolModeKey")["displayText"] == "ABC":
            self.keyboard_press_icon("#symbolModeKey")
        if append == False:
            key_Ok  = self._spice.query_item("#enterKey1")
            key_Ok.mouse_click()

           
    def keyboard_set_text_with_out_dial_action(self, input_string, textfield_objectid, index_value=0):
        '''
        UI should be at keyboard view
        input_string text which consists of alphabets, numbers, special charecters and space text
        without dial action. directly set value to keyboard 
        This method is preferred if you are not testing keyboard dialing. It will save lot of time
        Args:
          input_string: text to be entered
          textfield_objectid: object id of the textfield
        '''
        # clear the textfield if not empty
        key = self._spice.wait_for(textfield_objectid)
        key.mouse_click()
        key.__setitem__('displayText', input_string)
        #key["currentText"] = input_string
        # Press ok key to save the text
        key_Ok  = self._spice.query_item("#enterKey1")
        key_Ok.mouse_click()
        #self.keyboard_press_icon("#ItemIconDelegatecheckmark_xs",index_value, 0)

    def keyboard_enter_number(self, text:str):
        '''
        UI should be at alphanumeric keyboard view
        Enter text which consists of numbers and space
        Args:
          text: number to be entered
        '''
        #Populating number keys 
        symbolskey = self._spice.query_item("#symbolModeKey")
        symbolskey.mouse_click()
        for i in  range(len(text)):
            num = text[i]
            logging.info(num)
            key = self._spice.wait_for("#key" + num)
            key.mouse_click()
        key_Ok  = self._spice.wait_for("#enterKey1")
        key_Ok.mouse_click()

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

    def keyboard_clear_text(self, textfield_objectid, index_value=0):
        '''
        Method to clear text box
        UI should be on keyboard view before calling this method
        Args:
           textfield_objectid: Object name of the textfield
        '''
        is_icon = False
        # Delete pre-existing text, if any
        text_length = len(self._spice.query_item(textfield_objectid, index_value)["inputText"])
        if(text_length > 0):
            for i in range(text_length+1):
                self.keyboard_press_icon("#keyRight")
            time.sleep(1)    
        if (text_length > 0):
            for i in range(text_length):
                self.keyboard_press_icon("#backspaceKey", index_value, dial_val = 0)
            is_icon = True
            time.sleep(1)
        assert len(self._spice.query_item(textfield_objectid, index_value)["inputText"]) == 0 , "Textfield is not empty"

    def numeric_keyboard_clear_values(self, textfield_objectid, keypadType, index_value=0):
        '''
        Method to clear text box
        UI should be on numeric keyboard view before calling this method
        Args:
           textfield_objectid: Object name of the textfield
        '''
        is_icon = False
        # Delete pre-existing text, if any
        time.sleep(2)
        clear_text = self._spice.query_item("#ClearMouseArea")
        clear_text.mouse_click()
        time.sleep(2)
        text_length = len(self._spice.query_item(textfield_objectid, index_value)["inputText"])
        if (text_length > 0):
            for i in range(text_length):
                self.keyboard_press_icon("#backspaceKey" + keypadType, index_value, dial_val = 0)
            is_icon = True
            time.sleep(1)
        assert len(self._spice.query_item(textfield_objectid, index_value)["inputText"]) == 0 , "Textfield is not empty"
    
    def numeric_keyboard_enter_value(self,character, keypadType):
        '''
        Method to enter single numeric value 
        UI Should be on numeric keyboard view before calling this method
        Args:
           character : The number or the dot to be enterd 
        ''' 
        if character.isnumeric():
            key = self._spice.wait_for("#key" + character + keypadType)
            key.mouse_click()
        elif character == ".":
            if(keypadType in set(["MacKeypad", "FullKeypad", "PositiveDecimalKeypad"])):
                key = self._spice.wait_for("#keyCommaOrPeriod" + keypadType)
                key.mouse_click() 

    def numeric_keyboard_enter_number(self, number:str, textfield_objectid, keypadType, check: bool = True):
        '''
        Method to enter  numeric values 
        UI Should be on numeric keyboard view before calling this method
        Args:
           number : The number to be entered 
           textfield_objectid : Object name of the text field
        ''' 
        # Delete pre-existing text, if any'''
       
        self.numeric_keyboard_clear_values(textfield_objectid, keypadType)
        time.sleep(1)
        for num in number:
            self.numeric_keyboard_enter_value(num, keypadType)
        #To save the number entered 
        key_Ok  = self._spice.query_item("#enterKey" + keypadType)
        key_Ok.mouse_click()


    def navigate_to_fax_header(self):
        '''
        Method to navigate to the Alphanumeric keyboard to enter fax header name
        '''
        #self.faxoperations.goto_menu_fax_faxsetup()
        self.workflow_common_operations.goto_item(FaxAppWorkflowObjectIds.input_enterFaxHeaderName, "#basicFaxSetupverticalLayout",scrollbar_objectname = "#basicFaxSetupverticalLayout")
       
        
    def select_keyboard_layout(self, cdm):
        #TODO Keyboard layout feature is not yet implemented will continue after implementing story https://hp-jira.external.hp.com/browse/DUNE-64491
        constraint_endpoint = "cdm/controlPanel/v1/configuration/constraints"
        tkt_response = cdm.get(constraint_endpoint)
        validators = tkt_response["validators"]
        print(validators)
        payload =  {"options": [
        {
          "sValue": "azerty"
        }
        ]
        }
        response = cdm.patch_raw("cdm/controlPanel/v1/configuration", payload )

        print(response)

    def navigate_to_proxy_settings_screen(self):
        self.MenuApp_Workflow_UI_Common_Operations.goto_menu_settings_network(self._spice)
        time.sleep(3)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.network_settings_menu_view, NetworkFolderAppWorkflowObjectIds.proxy_settings_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.network_settings_menu_scroll)
        try:  
            (spice.query_item("#ComponentBlockRow")["visible"])  
        except Exception as e:
            pass
        else:
            self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.proxy_settings_menu_view, NetworkFolderAppWorkflowObjectIds.proxy_toggle_button)
        finally:
            logging.info("At Menu ProxySetting")
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.proxy_settings_menu_view, NetworkFolderAppWorkflowObjectIds.proxy_port_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.proxy_settings_menu_scroll)
        time.sleep(3)

    def navigate_to_manual_IPv4_settings_screen(self):
        self.MenuApp_Workflow_UI_Common_Operations.goto_menu_settings_network(self._spice)
        time.sleep(2)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.network_settings_menu_view, NetworkFolderAppWorkflowObjectIds.cnxEthernet_settings_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.network_settings_menu_scroll)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.cnxEthernet_settings_menu_view, NetworkFolderAppWorkflowObjectIds.Ethernet_settings_IPv4_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.Ethernet_settings_menu_scroll)
        time.sleep(2)
        #changing IpWarning Ok pop up button
        key_Ok = self._spice.query_item(NetworkFolderAppWorkflowObjectIds.IPv4_warning_ok_button)
        key_Ok.mouse_click()
        time.sleep(1)

    def navigate_to_manual_ip_settings_screen(self):
        self.navigate_to_manual_IPv4_settings_screen()
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.IPv4_settings_menu_view, NetworkFolderAppWorkflowObjectIds.IPv4_configuration_DHCP_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.IPv4_settings_menu_scroll)
        manual_dropdown = self._spice.query_item(NetworkFolderAppWorkflowObjectIds.IPv4_manual_dropdown_option)
        manual_dropdown.mouse_click()
        time.sleep(1)
        #Select manual pop up button
        manual_Button = self._spice.query_item(NetworkFolderAppWorkflowObjectIds.IPv4_manual_button)
        manual_Button.mouse_click()
        time.sleep(1)
        # assert self._spice.wait_for("#spiceKeyboardView")
        logging.info("At Menu Manual IP Settings")

    def goto_ip_address_screen(self):
        self.navigate_to_manual_ip_settings_screen()
        time.sleep(2)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_view, NetworkFolderAppWorkflowObjectIds.Ipaddress_text_field_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_scroll)
        logging.info("At Menu Manual IP address keypad")
    
    def goto_subnet_mask_screen(self):
        self.navigate_to_manual_ip_settings_screen()
        time.sleep(2)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_view, NetworkFolderAppWorkflowObjectIds.subnetmask_text_field_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_scroll)
        logging.info("At Menu Manua subnet mask keypad")

    def goto_gate_way_screen(self):
        self.navigate_to_manual_ip_settings_screen()
        time.sleep(2)
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_view, NetworkFolderAppWorkflowObjectIds.gateway_text_field_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.manual_IP_settings_menu_scroll)
        logging.info("At Menu Gate way keypad")

    def goto_DNS_screen(self):
        self.navigate_to_manual_IPv4_settings_screen()
        logging.info("At Menu IPv4 screen")
        self.MenuApp_Workflow_UI_Common_Operations.menu_navigation(self._spice, NetworkFolderAppWorkflowObjectIds.IPv4_settings_menu_view, NetworkFolderAppWorkflowObjectIds.primary_DNS_option, scrollbar_objectname = NetworkFolderAppWorkflowObjectIds.IPv4_settings_menu_scroll)
        logging.info("Primary DNS keypad")
        
    def keyboard_enter_alphanumeric_text(self, text, textfield_objectid, index_value=0, dial_val: int = 180, append = False):
        is_icon = False
        # Delete pre-existing text, if any
        clear_text = self._spice.query_item(textfield_objectid + " #ClearMouseArea")
        clear_text.mouse_click()
        time.sleep(1)
        if not append:
            for character in text:
                if character in text:
                    if character.isalpha():
                        if self._spice.query_item("#symbolModeKey")["displayText"] == "ABC":
                            self.keyboard_press_icon("#symbolModeKey")
                        if character.islower():
                            if self._spice.query_item("#keyShift")["uppercased"] == True:
                                self.keyboard_press_icon("#keyShift")
                            character = character.upper()
                            key = self._spice.wait_for("#key" + character)
                            key.mouse_click()
                        elif character.isupper():
                            if self._spice.query_item("#keyShift")["uppercased"] == False:
                                self.keyboard_press_icon("#keyShift")
                            key = self._spice.wait_for("#key" + character)
                            key.mouse_click()
                    elif character.isnumeric():
                        if self._spice.query_item("#symbolModeKey")["displayText"] == "&123":
                            self.keyboard_press_icon("#symbolModeKey")
                        key = self._spice.wait_for("#key" + character)
                        key.mouse_click()
                    elif character == " ":
                        self.keyboard_press_icon("#spaceKey")
                    else:
                        if self._spice.query_item("#symbolModeKey")["displayText"] == "&123":
                            self.keyboard_press_icon("#symbolModeKey")
                        try:
                            key = self._spice.wait_for(special_char_keys[character], 5)
                            key.mouse_click()
                        except Exception as e:
                            self.keyboard_press_icon("#key1By21")
                            key = self._spice.wait_for(special_char_keys[character], 5)
                            key.mouse_click()
                            self.keyboard_press_icon("#key2By21")
            key_Ok  = self._spice.query_item("#enterKey1")
            key_Ok.mouse_click()

    def keyboard_empty_text(self, textfield_objectid, index_value=0):
        textfield = self._spice.query_item(textfield_objectid, index_value)
        text_length = len(textfield["inputText"])
        logging.info("Text length is %s %s", text_length, textfield["cursorPosition"]) 
        textfield.__setitem__('displayText', "")
        time.sleep(1)
        assert len(self._spice.query_item(textfield_objectid, index_value)["inputText"]) == 0 , "Textfield is not empty"

    def keyboard_enter_textfield(self, text: str):
        for new_char in text:
            self.keyboard_enter_character(new_char)
        # To save the text entered
        if self._spice.wait_for("#symbolModeKey")["displayText"] == "ABC":
            self.keyboard_press_icon("#symbolModeKey")
        key_Ok = self._spice.wait_for("#enterKey1")
        key_Ok.mouse_click()
