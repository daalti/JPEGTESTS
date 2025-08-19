import re
import logging
import time

from dunetuf.ui.uioperations.ProSelectOperations.PrintQuickFormsAppProSelectUIOperations import PrintQuickFormsAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import ProSelectHybridKeyboardOperations

class PrintQuickFormsAppProSelectUIHybridOperations(PrintQuickFormsAppProSelectUIOperations):

    ALERT_DIALOG_TOAST_WINDOW = "#ToastSystemToastStackView"

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.proselect_keyboard_hybrid_operations = ProSelectHybridKeyboardOperations(self._spice)

    def check_toast_information_icon(self):
        alertIcon = self._spice.query_item(self.ALERT_TOAST_ICON)
        #print("icon source=",alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/+hybridTheme/information_xs.json")

    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def check_toast_message(self, text):
        toastMessage = self._spice.wait_for("#ToastInfoText")
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)