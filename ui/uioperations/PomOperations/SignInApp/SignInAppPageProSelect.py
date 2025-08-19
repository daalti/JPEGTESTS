import logging
import time

from enum import Enum
from .Page import Page
from .LocatorsProSelect import LocatorsProSelect
from .AdminPage import AdminPage
from .SmartCardPage import SmartCardPage
from .WindowsAuthPageProSelect import WindowsAuthPageProSelect
from .LdapPageProSelect import LdapPageProSelect
from .AdminPageProSelect import AdminPageProSelect
from .LdapPage import LdapPage
from .PrinterUserPage import PrinterUserPage
from .PrinterUserPageProSelect import PrinterUserPageProSelect
from .Components.SignInPageVerification import SignInPageVerification

class SignInAppPageProSelect(Page):
    class SignInMethod(str, Enum):
        #ServiceUser = Locators.ServiceUserSignInComboBox
        PrinterUser = "Printer User"
        #Smartcard = Locators.SmartcardSignInComboBox
        Windows = "Windows"
        LDAP = "LDAP"
        Admin = "Device Administrator"

    def __init__(self, spice):
        super().__init__(spice)
        #self.verify = SignInPageVerification(self)
        #self.smartcard = SmartCardPage(self)
        self.windows = WindowsAuthPageProSelect(self)
        self.ldap = LdapPageProSelect(self)
        self.admin = AdminPageProSelect(self)
        self.printer_user = PrinterUserPageProSelect(self)
    
    def change_sign_in_method_to(self, sign_in_method:SignInMethod) -> bool:
        current_sign_in_method = self.get_current_sign_in_method()
        if current_sign_in_method == None: return False
        if current_sign_in_method == sign_in_method:
            logging.debug(f"Already on sign in method: {sign_in_method}")
            return True

        # click Sign In Method button
        if not self.wait_and_click(LocatorsProSelect.SignInMethodButton):
            logging.error("Failed to click \'Sign In Method\' button")
            return False

        # click method type
        return True
    
    def get_current_sign_in_method(self) -> SignInMethod:
        text = self.get_locator_attribute(LocatorsProSelect.SignInMethodText, self.Attribute.Text)

        if text == self.SignInMethod.Windows.value:
            return self.SignInMethod.Windows
        if text == self.SignInMethod.LDAP.value:
            return self.SignInMethod.LDAP
        if text == self.SignInMethod.Admin.value:
            return self.SignInMethod.Admin
        if text == self.SignInMethod.PrinterUser.value:
            return self.SignInMethod.PrinterUser

        return None

    def verify_welcome_user_toast_message(self, username:str, timeout:float = Page.DEFAULT_TIMEOUT) -> bool:
        logging.info("Verifying Welcome User toast message..")

        logging.info("Wait for toast message to populate...")
        text = self.get_locator_attribute(LocatorsProSelect.ToastMessageText, self.Attribute.Text)
        while text == "" and timeout > 0:
            timeout -= 1
            time.sleep(1)
            text = self.get_locator_attribute(LocatorsProSelect.ToastMessageText, self.Attribute.Text)
        
        if text == "": return False
            
        return self.compare_locator_text(LocatorsProSelect.ToastMessageText, f"Welcome, {username}")