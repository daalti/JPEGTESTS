import logging

from ..Page import Page
from ..Locators import Locators
from .Verification import Verification

class SmartCardPageVerification():
    def __init__(self, page:Page) -> None:
        self.__verification = Verification(page)
        self.__page = page

    def __get_constraint_error_page_text(self) -> str:
        if self.__verification.verify(Locators.ConstraintMessageErrorPageTextView, verify_active_focus=False) == False: return False
        return self.__page.get_locator_attribute(Locators.ConstraintMessageErrorPageTextView, self.__page.Attribute.Text)
        
    def on_page(self) -> bool:
        logging.debug("Verifying we are on Smartcard Sign In page...")
        return self.__verification.verify(Locators.SmartcardSignInView)

    def on_smartcard_problem_page(self) -> bool:
        logging.debug("Verifying Smartcard Problem page")
        return self.__verification.verify(Locators.SmartcardProblemView, verify_active_focus=False)

    def on_no_smartcard_reader_detected_page(self) -> bool:
        logging.debug("Verifying No Smartcard Reader Detected page")
        text = self.__get_constraint_error_page_text()
        if text == None: return False
        return text == Locators.SmartcardErrorPageNoReaderMessage

    def on_no_smartcard_detected_page(self) -> bool:
        logging.debug("Verifying No Smartcard Detected page")
        text = self.__get_constraint_error_page_text()
        if text == None: return False
        return text == Locators.SmartcardErrorPageNoSmartcardMessage

    def on_multiple_readers_attached_page(self) -> bool:
        logging.debug("Verifying Multiple Readers Attached page")
        text = self.__get_constraint_error_page_text()
        if text == None: return False
        return text == Locators.SmartcardErrorPageMultipleReadersMessage

    def on_smartcard_locked_page(self) -> bool:
        logging.debug("Verifying Smartcard Locked page")
        return self.__verification.verify(Locators.SmartcardLockedView, verify_active_focus=False)

    def smartcard_inserted_toast_message(self) -> bool:
        logging.debug("Verifying Smartcard Inserted Toast Message appears")
        return self.__page.compare_locator_text(Locators.ToastMessageText, Locators.SmartcardDetectedToastMessage)

    def smartcard_reader_inserted_toast_message(self) -> bool:
        logging.debug("Verifying Smartcard Inserted Toast Message appears")
        return self.__page.compare_locator_text(Locators.ToastMessageText, Locators.SmartcardReaderDetectedToastMessage)

    def connect_reader_constraint_message(self) -> bool:
        logging.debug("Verifying Connect Reader Constraint Message appears")
        return self.__page.compare_locator_text(Locators.SmartcardConstraintTextFieldText, Locators.SmartcardConstraintNoReaderMessage)
        
    def no_smartcard_inserted_constraint_message(self) -> bool:
        logging.debug("Verifying No Smartcard Inserted Constraint Message appears")
        return self.__page.compare_locator_text(Locators.SmartcardConstraintTextField, Locators.SmartcardConstraintNoCardInsertedMessage)