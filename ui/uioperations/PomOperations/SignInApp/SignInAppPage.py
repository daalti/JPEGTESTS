import logging

from enum import Enum
from .Page import Page
from .Locators import Locators
from .AdminPage import AdminPage
from .SmartCardPage import SmartCardPage
from .WindowsAuthPage import WindowsAuthPage
from .LdapPage import LdapPage
from .PrinterUserPage import PrinterUserPage
from .ServiceUserPage import ServiceUserPage
from .IDCodePage import IDCodePage
from .Components.SignInPageVerification import SignInPageVerification

class SignInAppPage(Page):
    class SignInMethod(str, Enum):
        ServiceUser = Locators.ServiceUserSignInComboBox
        PrinterUser = Locators.PrinterUserSignInComboBox
        Smartcard = Locators.SmartcardSignInComboBox
        Windows = Locators.WindowsSignInComboBox
        IDCode = Locators.IDCodeSignInComboBox
        Admin = Locators.AdminSignInComboBox
        Ldap = Locators.LdapSignInComboBox

    def __init__(self, spice):
        super().__init__(spice)
        self.verify = SignInPageVerification(self)
        self.smartcard = SmartCardPage(self)
        self.windows = WindowsAuthPage(self)
        self.ldap = LdapPage(self)
        self.admin = AdminPage(self)
        self.printer_user = PrinterUserPage(self)
        self.service_user = ServiceUserPage(self)
        self.id_code = IDCodePage(self)

    def get_sign_in_method_view_locator(self, timeout:float = Page.DEFAULT_TIMEOUT) -> str:
        all_sign_in_view_locators = Locators.AllSignInViews
        for view_locator in all_sign_in_view_locators:
            view = self.wait_for_element(view_locator, timeout)
            if view == None: continue
            return view_locator
        logging.error(f"Failed to find current sign in view.\nSearched for all these views: {all_sign_in_view_locators}.\nAre you on the Sign In page?")
        return None

    def get_current_sign_in_method(self) -> SignInMethod:
        view_locator = self.get_sign_in_method_view_locator()
        if view_locator == None: return None
        if not (view_locator in Locators.AllSignInViews): return None

        if view_locator == Locators.SmartcardSignInView:
            return self.SignInMethod.Smartcard
        elif view_locator == Locators.PrinterUserSignInView:
            return self.SignInMethod.PrinterUser
        elif view_locator == Locators.ServiceUserSignInView:
            return self.SignInMethod.ServiceUser
        elif view_locator == Locators.WindowsSignInSingleDomainView or view_locator == Locators.WindowsSignInMultipleDomainsView:
            return self.SignInMethod.Windows
        elif view_locator == Locators.AdminSignInView:
            return self.SignInMethod.Admin
        elif view_locator == Locators.IDCodeSignInView:
            return self.SignInMethod.IDCode
        else:
            return self.SignInMethod.Ldap

    def get_clickable_combobox_locator(self, sign_in_method:SignInMethod) -> str:
        return sign_in_method + " #control"

    def get_combobox_item_suffix_locator(self, sign_in_method:SignInMethod) -> str:
        if sign_in_method == self.SignInMethod.Smartcard:
            return Locators.SmartcardComboBoxItemSuffix
        elif sign_in_method == self.SignInMethod.PrinterUser:
            return Locators.PrinterUserComboBoxItemSuffix
        elif sign_in_method == self.SignInMethod.ServiceUser:
            return Locators.ServiceUserComboBoxItemSuffix
        elif sign_in_method == self.SignInMethod.Windows:
            return Locators.WindowsComboBoxItemSuffix
        elif sign_in_method == self.SignInMethod.Admin:
            return Locators.AdminComboBoxItemSuffix
        elif sign_in_method == self.SignInMethod.IDCode:
            return Locators.IDCodeComboBoxItemSuffix
        else:
            return Locators.LdapComboBoxItemSuffix

    def get_combobox_item_prefix_locator(self, sign_in_method:SignInMethod) -> str:
        if sign_in_method == self.SignInMethod.Smartcard:
            return Locators.SmartcardSignInComboBoxItemPrefix
        elif sign_in_method == self.SignInMethod.PrinterUser:
            return Locators.PrinterUserSignInComboBoxItemPrefix
        elif sign_in_method == self.SignInMethod.ServiceUser:
            return Locators.ServiceUserSignInComboBoxItemPrefix
        elif sign_in_method == self.SignInMethod.Windows:
            return Locators.WindowsSignInComboBoxItemPrefix
        elif sign_in_method == self.SignInMethod.Admin:
            return Locators.AdminSignInComboBoxItemPrefix
        elif sign_in_method == self.SignInMethod.IDCode:
            return Locators.IDCodeSignInComboBoxItemPrefix
        else:
            return Locators.LdapSignInComboBoxItemPrefix

    def get_clickable_combobox_item_locator(self, current_sign_in_method:SignInMethod, select_sign_in_method:SignInMethod) -> str:
        return self.get_combobox_item_prefix_locator(current_sign_in_method) + self.get_combobox_item_suffix_locator(select_sign_in_method) + " #mouseArea"        

    def change_sign_in_method_to(self, sign_in_method:SignInMethod) -> bool:
        current_sign_in_method = self.get_current_sign_in_method()
        if current_sign_in_method == None: return False
        if current_sign_in_method == sign_in_method:
            logging.debug(f"Already on sign in method: {sign_in_method}")
            return True
        clickable_combobox_locator = self.get_clickable_combobox_locator(current_sign_in_method)
        if self.wait_and_click(clickable_combobox_locator) == False:
            logging.error(f"Failed to click \'{clickable_combobox_locator}\' combobox")
            return False

        clickable_item_locator = self.get_clickable_combobox_item_locator(current_sign_in_method, sign_in_method)
        item_locator = self.get_combobox_item_prefix_locator(current_sign_in_method) + self.get_combobox_item_suffix_locator(sign_in_method)
        scroll_area_height = self.get_locator_attribute(current_sign_in_method + Locators.PopupListSuffix, self.Attribute.Height)

        if self.scroll_vertical(Locators.ComboBoxScrollBar, item_locator, scroll_area_height) == False: return False

        if self.wait_and_click(clickable_item_locator) == False:
            logging.error(f"Failed to click \'{clickable_item_locator}\' combobox item")
            return False

        return True

    def click_invalid_sign_in_button(self) -> bool:
        logging.debug("Clicking Invalid Sign In button...")
        # This is the 'Sign In' buttton that is on the 'Invalid Sign In' screen
        return self.wait_and_click(Locators.InvalidSignInButton)

    def click_signing_in_cancel_button(self) -> bool:
        """
            This button pops up extremely quick sometimes after you
            click the 'Sign In' button. Most of the time you sign in
            so fast that you never see this button. If you set the DNS
            to a value that is unresolvable, then the 'Cancel' button
            should appear while it's attempting to sign in.
        """
        logging.debug("Clicking Signing In Cancel button...")
        return self.wait_and_click(Locators.SigningInCancelButton, click_center=False)