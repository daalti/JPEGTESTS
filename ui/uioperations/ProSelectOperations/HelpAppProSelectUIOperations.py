import time
from dunetuf.ui.uioperations.BaseOperations.IHelpAppUIOperations import IHelpAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
import logging

class HelpAppProSelectUIOperations(IHelpAppUIOperations):
    # -------------------------------Function Keywords------------------------ #
    max_cancel_time = 60
    property_text = "text"
    home_screen_view = "#HomeScreenView"
    current_app_text = "#CurrentAppText"
    help_folder_guid = "#1f91f218-ca35-4554-a2f3-16b0b28fea31"

    def __init__(self, spice):
        """
        HelpAppUIOperations class to initialize help app options operations.
        @param spice:
        """
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)

    def goto_help_app(self):
        """
        Function to navigate to Help app on home screen
        Ui Flow: Any screen -> Home screen -> Help app
        @return:
        """
        # Use the existing home_navigation method instead of manual scrolling
        self.home_menu_dial_operations.home_navigation(
            spice=self._spice,
            home_screen_view=self.home_screen_view,
            app_name="Help",
            current_app_text=self.current_app_text,
            property_text=self.property_text,
            max_cancel_time=self.max_cancel_time
        )

        assert self._spice.query_item(self.current_app_text)[self.property_text] == "Help"

        current_item = self._spice.wait_for(self.help_folder_guid)
        current_item.mouse_click()