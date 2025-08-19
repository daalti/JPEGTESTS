import logging

from .Locators import Locators
from .Components.TextComboBox import TextComboBox
from .Components.TextField import TextField
from .Components.Button import Button
from .Components.SmartCardPageVerification import SmartCardPageVerification

"""
    Must be on Sign In page to used this class.
"""

class SmartCardPage():
    def __init__(self, page):
        self.__page = page
        self.__pin_field = TextField(page, Locators.SmartcardPinInputField)
        self.__domain_combo_box = TextComboBox(page, Locators.SmartcardDomainComboBox, Locators.ComboBoxScrollBar, Locators.SmartcardDomainTextField)
        self.__domain_text_field = TextField(page, Locators.SmartCardDomainTextField)
        self.__smartcard_problem_ok_button = Button(page, Locators.SmartcardProblemOkButton)
        self.__constraint_error_page_ok_button = Button(page, Locators.ConstraintMessageErrorPageOkButton)
        self.__multiple_readers_attached_ok_button = Button(page, Locators.MultipleReadersAttachedOkButton)
        self.__smartcard_locked_ok_button = Button(page, Locators.SmartcardLockedOkButton)
        self.__cancel_button = Button(page, Locators.SmartcardCancelButton)
        self.__sign_in_button = Button(page, Locators.SmartcardSignInButton)
        self.__keyboard_ok_button = Button(page, Locators.KeyboardEnterTextView)
        self.__keypad_ok_button = Button(page, Locators.KeypadEnterTextView)
        self.verify = SmartCardPageVerification(page)

    def select_method(self) -> bool:
        """
            Selects 'Smartcard' as sign in method
        """
        if self.verify.on_page() == True:
            logging.debug("Already on Smartcard Sign In page")
            return True
        
        # Switch to smartcard sign in view
        if self.__page.change_sign_in_method_to(self.__page.SignInMethod.Smartcard) == False:
            logging.error("Failed to switch to Smartcard sign in method")
            return False

        return self.verify.on_page()

    def get_current_domain_text(self) -> str:
        logging.info("Getting current domain text...")
        domain = self.__domain_text_field.get_text()
        if domain == '':
            domain = self.__domain_combo_box.get_selected_text()
        if domain == None:
            logging.error("Failed to get current domain text")
        return domain
    
    def get_pin_input_display_text(self) -> str:
        return self.__pin_field.get_display_text()

    def select_domain(self, domain:str) -> bool:
        domainText = self.get_current_domain_text()
        logging.info(f"Current Domain: {domainText}")
        if domain != domainText:
            if self.__domain_combo_box.select_item(domain) == False:
                logging.error(f"Failed to select domain \'{domain}\'")
                return False
        return True

    def enter_pin(self, pin:str) -> bool:
        logging.debug(f"Entering pin for smartcard: {pin}...")
        if self.__pin_field.enter(pin) == False:
            logging.error(f"Failed to enter pin \'{pin}\' into pin field \'{self.__pin_field.locator}\'")
            return False
        logging.debug(f"Successfully entered pin: {pin}")
        return True

    def is_numeric_keypad(self) -> bool:
        """
            Smartcard on-screen keyboard can be
            alphabetical or numeric depending on
            if 'numericOnlyKeypad' is true or false.

            'numericOnlyKeypad' = True -> Keypad
            'numericOnlyKeypad' = False -> Alphabetical Keyboard
        """
        logging.debug("Checking on-screen keyboard type...")
        if self.__page.wait_for_element(Locators.KeyboardView) == None:
            logging.error("Keyboard is not currently active. Is the keyboard on screen?")
            return False
        if self.__page.wait_for_element(Locators.KeypadEnterTextView) == None:
            logging.error("Failed to find Keypad")
            return False
        if self.__page.get_locator_attribute(Locators.KeypadEnterTextView, self.__page.Attribute.Visible) == False:
            logging.error("Keypad is invisible")
            return False
        return True

    def is_alphabetical_keyboard(self) -> bool:
        logging.debug("Checking on-screen keyboard type...")
        if self.__page.wait_for_element(Locators.KeyboardView) == None:
            logging.error("Keyboard is not currently active. Is the keyboard on screen?")
            return False
        if self.__page.wait_for_element(Locators.KeyboardEnterTextView) == None:
            logging.error("Failed to find Keyboard")
            return False
        if self.__page.get_locator_attribute(Locators.KeyboardEnterTextView, self.__page.Attribute.Visible) == False:
            logging.error("Keyboard is invisible")
            return False
        return True
    
    def is_pin_input_revealed(self) -> bool:
        echo_mode = self.__page.get_locator_attribute(Locators.SmartcardPinInputField, self.__page.Attribute.EchoMode)
        logging.info(f"Echo Mode: {echo_mode}")
        # 0 = password revealed, 2 = password hidden
        return echo_mode == 0
    
    def has_pin_reveal_icon(self) -> bool:
        return self.__page.wait_for_element(Locators.SmartcardPinInputRevealIconButton) != None
    
    def has_pin_input_error(self) -> bool:
        logging.debug("Checking if pin input field has an error (indicated by a red border)...")
        error_value = self.__page.get_locator_attribute(Locators.SmartcardPinInputFieldContainer, self.__page.Attribute.Error)
        return error_value

    def click_pin_input_field(self) -> bool:
        """
            Clicks the PIN input field only so
            the keyboard pops up
        """
        logging.debug("Clicking PIN input field...")
        return self.__pin_field.click()
    
    def click_pin_input_reveal_icon(self) -> bool:
        return self.__page.wait_and_click(Locators.SmartcardPinInputRevealIconButton)
        
    def click_sign_in_button(self) -> bool:
        logging.debug("Clicking Smartcard Sign In button...")
        return self.__sign_in_button.click()

    def click_cancel_button(self) -> bool:
        logging.debug("Clicking Smartcard Cancel button...")
        return self.__cancel_button.click()

    def click_keyboard_ok_button(self) -> bool:
        """
            Clicks the on-screen keyboard OK button,
            if keyboard is showing. (This is for the
            keyboard, not the keypad).
        """
        logging.debug("Clicking Keyboard Ok button...")
        return self.__keyboard_ok_button.click()

    def click_keypad_ok_button(self) -> bool:
        logging.debug("Clicking Keypad Ok button...")
        return self.__keypad_ok_button.click()

    def click_smartcard_problem_ok_button(self) -> bool:
        logging.debug("Clicking Smartcard Problem Ok button...")
        return self.__smartcard_problem_ok_button.click()

    def click_smartcard_error_page_ok_button(self) -> bool:
        logging.debug("Clicking Smartcard Error Page Ok button...")
        return self.__constraint_error_page_ok_button.click()

    def click_smartcard_multiple_readers_attached_ok_button(self) -> bool:
        logging.debug("Clicking Multiple Readers Attached OK button...")
        return self.__multiple_readers_attached_ok_button.click()

    def click_smartcard_locked_ok_button(self) -> bool:
        logging.debug("Clicking Smartcard Locked OK button...")
        return self.__smartcard_locked_ok_button.click()