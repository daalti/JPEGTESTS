from enum import Enum

class Display():
    class InactivityTimeout(str, Enum):
        Timeout30Seconds = "30 Seconds"
        Timeout1Minute = "1 Minute"
        Timeout2Minutes = "2 Minutes"
        Timeout5Minutes = "5 Minutes"

    @staticmethod
    def inactivity_timeout_to_float(inactivity_timeout:InactivityTimeout) -> float:
        if inactivity_timeout == Display.InactivityTimeout.Timeout30Seconds:
            return 30
        if inactivity_timeout == Display.InactivityTimeout.Timeout1Minute:
            return 60
        if inactivity_timeout == Display.InactivityTimeout.Timeout2Minutes:
            return 120
        if inactivity_timeout == Display.InactivityTimeout.Timeout5Minutes:
            return 300
        return 0

    @staticmethod
    def inactivity_timeout_string_to_element_locator(inactivity_timeout:InactivityTimeout) -> str:
        if inactivity_timeout == Display.InactivityTimeout.Timeout30Seconds:
            return "#thirtySeconds"
        if inactivity_timeout == Display.InactivityTimeout.Timeout1Minute:
            return "#oneMinute"
        if inactivity_timeout == Display.InactivityTimeout.Timeout2Minutes:
            return "#twoMinutes"
        if inactivity_timeout == Display.InactivityTimeout.Timeout5Minutes:
            return "#fiveMinutes"
        return "NO LOCATOR"

    def select(self) -> bool:
        # Clicks the Display button
        return False

    def select_inactivity_timeout(self, inactivity_timeout:InactivityTimeout) -> bool:
        # Click the inactivity timeout and select a timeout
        return False

    def click_inactivity_timeout(self) -> bool:
        # Click the inactivity timeout, but dont' select anything(it might be a buttno or combobox)
        return False
    