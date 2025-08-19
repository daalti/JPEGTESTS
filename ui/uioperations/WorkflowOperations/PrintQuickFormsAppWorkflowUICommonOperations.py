import logging 
import time

from dunetuf.ui.uioperations.BaseOperations.IPrintQuickFormsAppUIOperations import IPrintQuickFormsAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class PrintQuickFormsAppWorkflowUICommonOperations(IPrintQuickFormsAppUIOperations):

    # no of copies
    numberOfCopies_spin_box_layout = "#QuickFormsAppApplicationStackView"
    numberOfCopies_spin_box =  "#QuickFormsAppApplicationStackView #spinbox"
    numberOfCopies_spin_box_preview =  "#spinBoxPreview"
    numberOfCopies_plus_locator = "#upBtn"
    numberOfCopies_minus_locator = "#downBtn"
    numberOfCopies_textArea_locator = "#SpinBoxTextInput"
    LOC_STR_ID_PRINTING = "cPermissionPrintingApp"
    LOC_STR_ID_PRINT_CANCELING = "cJobStateTypeCanceling"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = self._spice.basic_common_operations
        self.homemenu = self._spice.menu_operations
    
    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self._spice.goto_homescreen()
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
        logging.info("At Home Screen")
        # TODO - Need to check the menu app is visible or not
        # check whether the menu is visible on the screen
        menuApp = self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp)
        self._spice.wait_until(lambda: menuApp["visible"] == True)
    
    def goto_mainApp_printApp_quick_forms(self):
        """
        Purpose: Navigates to Quick Forms app screen from any other screen
        Ui Flow: Any screen -> Home Screen -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        self._spice.home_operations.goto_home_print_app()
        self._spice.wait_for(HomeAppWorkflowObjectIds.view_print)
        self.goto_quick_forms()


    def goto_quick_forms(self):
        """
        Purpose: Navigates to Quick Forms app screen from any other screen
        Ui Flow: Any screen -> Home Screen -> Menu App -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        #self.goto_mainmenu()
        self._spice.main_app.goto_quick_forms_app()
    
    def quick_forms_click_button(self, buttonName):
        button = self._spice.wait_for("#" + buttonName)
        button.mouse_click()
    
    def get_value_of_no_of_copies(self, spinBoxObject):
        """
        Get the copy number
        @return: int
        """
        #Wait for Quick forms view is activeFocus = True
        self._spice.main_app.wait_locator_enabled(self.numberOfCopies_spin_box_layout)
        #self._spice.wait_for(self.numberOfCopies_spin_box)
        #current_value = self._spice.query_item(self.numberOfCopies_spin_box)["value"]
        self._spice.wait_for(spinBoxObject)
        current_value = self._spice.query_item(spinBoxObject)["value"]
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        time.sleep(1)
        return current_value

    def set_no_of_copies(self, value, spinBoxObject):
        """
        Selects number of pages in USBPrint_PrintFromUSB screen based on user input
        @param value:
        @return:
        """
        #Wait for Quick forms view is activeFocus = True
        self._spice.main_app.wait_locator_enabled(self.numberOfCopies_spin_box_layout)
        # open expand button to show "Copies"
        expend_button = self._spice.query_item(spinBoxObject + " " + self.numberOfCopies_textArea_locator)
        expend_button.mouse_click(4,4)

        current_value = self.get_value_of_no_of_copies(spinBoxObject)
        dial_value = value - current_value 
        print("Number of copies to be added: ", dial_value)
        if dial_value >= 1:
            self._spice.wait_for(spinBoxObject)
            noCopiesUp = self._spice.query_item(spinBoxObject + " " + self.numberOfCopies_plus_locator)
            for i in range(1, (dial_value + 1)):    #Default value of num of copies is 1. So any increment in copy should be on top of it.
                noCopiesUp.mouse_click(4,4)
                time.sleep(0.1) 
        elif dial_value < 0:
            self._spice.wait_for(spinBoxObject)
            noCopiesUp = self._spice.query_item(spinBoxObject + " " + self.numberOfCopies_minus_locator)
            for i in range(current_value, abs(dial_value), -1):
                noCopiesUp.mouse_click(4,4)
                time.sleep(0.1) 

    def get_value_of_no_of_print_copies(self, default_initValue=0):
        return self.get_value_of_no_of_copies(self.numberOfCopies_spin_box)

    def get_value_of_no_of_preview_copies(self, default_initValue=0):
        return self.get_value_of_no_of_copies(self.numberOfCopies_spin_box_preview)

    def set_no_of_print_copies(self, value):
        self.set_no_of_copies(value, self.numberOfCopies_spin_box)

    def set_no_of_preview_copies(self, value):
        self.set_no_of_copies(value, self.numberOfCopies_spin_box_preview)

    
    def get_loc_string(self, loc_str_id, net, locale):
        loc_msg = LocalizationHelper.get_string_translation(net, loc_str_id, locale)
        logging.info("Localized string: %s", loc_msg)
        return loc_msg 

    def quick_forms_job_cancel_button(self, cdm, net, job, locale):
        #Validate Toast message.
        loc_msg = self.get_loc_string(self.LOC_STR_ID_PRINT_CANCELING, net, locale)
        logging.info("Localized string: %s", loc_msg)
        #self._spice.print_quick_forms.check_toast_message(loc_msg)

        #Validate Quick Form print cancel successfully.
        job_info_url = job.get_current_job_url("print")
        if job_info_url:
            current_job_info = cdm.get(job_info_url)
            jobstate = job.wait_for_job_completion_cdm(str(current_job_info["jobId"]), 300)
            logging.info("Job state: %s", jobstate)
            assert 'cancelled' in jobstate, f"Unexpected job state - {jobstate}."
        else:
            logging.warning("Failed to get cancel job status from job queue, will check it with job history")
        