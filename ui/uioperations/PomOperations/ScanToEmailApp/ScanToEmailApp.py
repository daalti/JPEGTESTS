from .Locators import Locators
from ..SignInApp.Page import Page
from ..SignInApp.Components.Button import Button
from ..SignInApp.Components.TextField import TextField

import logging
import time

class ScanToEmailApp(Page):
    
    def __init__(self, spice) -> None:
        super(ScanToEmailApp, self).__init__(spice)
        self.search_text_field = TextField(self, Locators.LDAPSearchTextField)
    
    def select_profile(self, cdm, profile_name:str) -> bool:
        """
        The selectable email server profile UI elements are named "smtpServer[SERVER_ID]".
        We need to get the list of smtp servers and search for the server name that matches the given "profile_name".
        Once we find the smtp server name, we save the server ID and now we can navigate to the correct profile in the UI.
        """
        response = cdm.email_servers.get_servers()
        if response.status_code != 200: return False

        server_id = ""

        servers = response.json()["servers"]
        for server in servers:
            if server["name"] == profile_name:
                server_id = server["smtpServerId"]
                break
        
        if server_id == "": return False

        scroll_bar = Locators.SelectEmailProfileScrollBar
        scroll_to = Locators.SelectEmailProfilePrefix + server_id
        height = self.get_locator_attribute(scroll_to, self.Attribute.Height)
        scroll_height = 2 * height

        if not self.scroll_vertical(scroll_bar, scroll_to, scroll_height): return False
        if not self.wait_and_click(scroll_to + " #mouseArea"): return False

        return True

    def click_to_address_book(self) -> bool:
        return self.wait_and_click(Locators.EmailToFieldAddressBookButton)
    
    def click_email_send_button(self) -> bool:
        return self.wait_and_click("#emailLandingView #GenericStructureView #DetailPanelverticalLayout #scanAppFooter #FooterViewRight #sendButtonDetailRightBlock #ButtonControl")
    
    def select_ldap_address_book(self) -> bool:
        return self.wait_and_click(Locators.LDAPAddressBook)
    
    def ldap_address_book_search(self, search:str) -> bool:
        if not self.wait_and_click(Locators.LDAPHeaderSearchButton): return False
        if not self.search_text_field.enter(search): return False
        if not self.wait_and_click(Locators.LDAPTextFieldSearchButton): return False
        return True
    
    def ldap_address_book_select_user(self, user:str) -> bool:
        if not self.wait_and_click(Locators.LDAPAddressBookSearchResultItem.format(user), check_enabled=False): return False
        return True

    def ldap_address_book_click_select(self) -> bool:
        return self.wait_and_click(Locators.LDAPAddressBookSelectButton)