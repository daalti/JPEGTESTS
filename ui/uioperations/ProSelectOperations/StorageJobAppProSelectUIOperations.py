import sys
import logging
import time

from dunetuf.ui.uioperations.BaseOperations.IStorageJobAppUIOperations import IStorageJobAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectHybridKeyboardOperations import KeyboardType, ProSelectHybridKeyboardOperations

JOBSTORAGE_BUTTON = "#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B"

class StorageJobAppProSelectUIOperations(IStorageJobAppUIOperations):
    """StorageJobUIProSelectOperations class to initialize StorageJob options operations."""
    def __init__(self, spice):
        self.maxtimeout = 60
        self.spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self.spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self.spice)
        self.proselect_UI_Hybrid_operations= ProSelectHybridKeyboardOperations(self.spice )

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self.spice.goto_homescreen()
        homeApp = self.spice.query_item("#HomeScreenView")
        self.spice.wait_until(lambda: homeApp["activeFocus"] == True)
        logging.info("At Home Screen")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the Menu option (TODO - Need to avoid use of text)
        while (self.spice.query_item("#CurrentAppText")[
                   "text"] != "Menu" and timeSpentWaiting < self.maxtimeout):
            homeApp.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

    def goto_print_app(self):
        """
        Purpose: Navigates to Print app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Print app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.goto_mainmenu()

        starttime = time.time()
        timespentwaiting = time.time() - starttime
        currentScreen = self.spice.wait_for("#HomeScreenView")
        while (self.spice.query_item("#CurrentAppText")["text"] != "Print" and timespentwaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180, 180)
            timespentwaiting = time.time() - starttime

        assert self.spice.query_item("#CurrentAppText")["text"] == "Print"

        currentitem = self.spice.query_item("#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
        currentitem.mouse_click()

    def goto_job_storage(self):
        """
        Purpose: Navigates to Job Storage app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Print app -> Job Storage app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.goto_print_app()
        self.spice.homeMenuUI().menu_navigation(self.spice, "#ButtonListLayout", JOBSTORAGE_BUTTON)

    def job_storage_click_button(self, buttonName):
        self.spice.wait_for("#" + buttonName)
        self.spice.homeMenuUI().menu_navigation(self.spice, "#ButtonListLayout", "#" + buttonName)
    
    def click_jobStorageFormatUsbSuccessful_okButton(self, dunestorejob):
        dunestorejob.alert_action('jobStorageFormatUsbSuccessful', 'ok')
    
    def click_jobStorageFormatUsb_continueButton(self):
        self.spice.homeMenuUI().menu_navigation(self.spice, '#jobStorageFormatUsb', '#Continue')
    
    def select_storageJob(self, userName, fileName=None):
        self.job_storage_click_button(userName)
        self.spice.query_item("#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B #ContentItemText").mouse_click()

    def print_storeJob_selected(self):
        self.spice.wait_for("#printButton").mouse_click()

    def delete_storeJob_selected(self):
        self.job_storage_click_button("deleteButton")
        self.spice.wait_for("#deleteConfirmationView")
        self.job_storage_click_button("confirmationDeleteButton")
        self.spice.wait_for("#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
    
    def detailed_storeJob_selected(self):
        self.job_storage_click_button("jobDetailsButton")
        self.spice.wait_for('#jobDetailsView')

    def has_lock_icon(self):
        """
        Starting from Home Screen
        """
        self.home_menu_dial_operations.goto_menu_print(self.spice)
        job_app_lock_icon_id = "#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32BMenuButton #ContentItem SpiceImage"
        current_screen = self.spice.wait_for("#MenuList02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
        current_screen.mouse_wheel(180, 180)
        lock_icon = self.spice.wait_for(job_app_lock_icon_id)

        return lock_icon["width"] > 0

    def unlock_storeJob_selected(self, pin):
        if(self.spice.uitheme == "hybridTheme") :
            keyboard = self.spice.wait_for("#pinPasswordKeyboard")
            self.spice.keyBoard.keyboard_enter_text(pin)
            self.proselect_UI_Hybrid_operations.keyboard_press_icon_ok_button("#SpiceKeyBoardbutton_en", 0, 0)

        else :
            keyboard = self.spice.wait_for("#spiceKeyboardView")
            current_position = 0
            for i in range(len(pin)):
                new_position = int(pin[i])
                if (new_position >= current_position) and (new_position - current_position <= 9):
                    dial_value = 180 # dial right
                else:
                    dial_value = 0 # dial left
                while current_position != new_position:
                    keyboard.mouse_wheel(dial_value, dial_value)
                    time.sleep(1)
                    if dial_value:
                        current_position += 1
                    else:
                        current_position -= 1
                keyboard.mouse_click()
