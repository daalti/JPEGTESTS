import logging
import re
import time
from time import sleep
from dunetuf.ui.uioperations.BaseOperations.IPrintQuickFormsAppUIOperations import IPrintQuickFormsAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

QUICKFORMS_BUTTON = "#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42"
QUICKFORMS_MENU_BUTTON = "#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42MenuButton"

class PrintQuickFormsAppProSelectUIOperations(IPrintQuickFormsAppUIOperations):
    max_cancel_time = 60
    property_current_index = "currentIndex"
    property_active_focus = "activeFocus"
    tumbler_listLayout = "#MenuListLayout"
    tumbler_preview = "#quickFormsPreview"
    spice_tumbler_view = "#SpiceTumblerView"
    ALERT_DIALOG_TOAST_WINDOW = "#ReportsPrintProgressView"
    ALERT_TOAST_ICON = "#SpiceProgressIndicator"
    BUTTON_LIST_LAYOUT = "ButtonListLayout"
    MENU_LIST_LAYOUT = "MenuListLayout"
    MENU_LIST_GRID_LAYOUT = "02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuAppListGridLayout"
    LOC_STR_ID_PRINTING = "cPermissionPrintingApp"
    LOC_STR_ID_PRINT_CANCELING = "cJobStateTypeCanceling"
    NARROW_RULE_MENU_ICON = "notebook_paper_narrow_rule_m"
    WIDE_RULE_MENU_ICON = "notebook_paper_wide_m"
    CHILD_RULE_MENU_ICON = "notebook_paper_child_rule_m"
    ONE_EIGHTH_MENU_ICON = "graphing_paper_1by8in_m"
    FIVE_MM_MENU_ICON = "graphing_paper_5mm_m"
    CHECKLIST_OPT_1_MENU_ICON = "checklist_paper_1col_m"
    CHECKLIST_OPT_2_MENU_ICON = "checklist_paper_2col_m"
    MUSIC_PORTRAIT_MENU_ICON = "music_paper_portrait_m"
    MUSIC_LANDSCAPE_MENU_ICON = "music_paper_landscape_m"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.QUICK_FORMS_LAYOUT = "ButtonListLayout"
    
    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        # make sure that you are in home screen
        self._spice.goto_homescreen()
        homeApp = self._spice.query_item("#HomeScreenView")
        self._spice.wait_until(lambda: homeApp["activeFocus"] == True)
        logging.info("At Home Screen")
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        # scroll till you reach the Menu option (TODO - Need to avoid use of text)
        while (self._spice.query_item("#CurrentAppText")[
                   "text"] != "Menu" and timeSpentWaiting < self.maxtimeout):
            homeApp.mouse_wheel(0, 0)
            timeSpentWaiting = time.time() - startTime
        time.sleep(2)

    def goto_print_app(self):
        """
        Purpose: Navigates to Print app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Print app
        :param spice: Takes 0 arguments
        :return: True if finds "Print" button on Homescreen else return False.
        """
        self.goto_mainmenu()

        starttime = time.time()
        timespentwaiting = time.time() - starttime
        currentScreen = self._spice.wait_for("#HomeScreenView")
        while (self._spice.query_item("#CurrentAppText")["text"] != "Print" and timespentwaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180, 180)
            timespentwaiting = time.time() - starttime

        if (self._spice.query_item("#CurrentAppText")["text"] == "Print"):
            currentitem = self._spice.query_item("#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
            currentitem.mouse_click()
            return True
        else:
            # No "Print" button on Homescreen.
            return False
        
    def quick_forms_click_button(self, buttonType, buttonName):
        self._spice.wait_for("#" + buttonName)
        self._spice.homeMenuUI().menu_navigation(self._spice, "#" + buttonType, "#" + buttonName)
    
    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def check_toast_information_icon(self):
        assert self._spice.query_item(self.ALERT_TOAST_ICON)

    def check_toast_message(self, text):
        toastMessage = self._spice.wait_for("#ProcessingLayout #Version2Text")
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)
        
        # Verify toast icon type. 
        self.check_toast_information_icon()

    def get_value_of_no_of_copies(self, tumbler_view, default_initValue=0):
        """
        Get the copy number
        @return: int
        """
        current_value = self._spice.query_item(tumbler_view + " " + self.spice_tumbler_view)[self.property_current_index] + default_initValue
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        return current_value
    
    def set_no_of_copies(self, value, tumbler_view):
        """
        Selects number of pages in Quick Forms screen based on user input
        @param value:
        @return:
        """
        dial_value = 0
        currentScreen = self._spice.wait_for(tumbler_view + " " + self.spice_tumbler_view)
        for i in range(5):
            currentScreen.mouse_wheel(0, 0)
            time.sleep(1)

        starttime = time.time()
        times_pent_waiting = 0

        while (self._spice.query_item(tumbler_view + " " + self.spice_tumbler_view)[
                   self.property_active_focus] == False and times_pent_waiting < self.max_cancel_time * 2):
            currentScreen.mouse_wheel(180, 180)
            times_pent_waiting = time.time() - starttime

        time.sleep(1)
        assert self._spice.query_item(tumbler_view + " " + self.spice_tumbler_view)[self.property_active_focus] == True

        current_value = self.get_value_of_no_of_copies(tumbler_view, 1) # Default initial value of tumbler_view is 1.

        if (value != int(current_value)):
            if (value > int(current_value)):
                dial_value = 180

        currentButton = self._spice.wait_for(tumbler_view + " " + self.spice_tumbler_view)

        starttime = time.time()
        times_pent_waiting = 0

        currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)

        while (int(current_value) != int(value) and times_pent_waiting < self.max_cancel_time * (
        4 if value < 40 else 7)):
            time.sleep(1)
            currentButton.mouse_wheel(dial_value, dial_value)
            time.sleep(0.5)
            current_value = self.get_value_of_no_of_copies(tumbler_view, 1)   # Default initial value of tumbler_view is 1.
            times_pent_waiting = time.time() - starttime

        currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
        time.sleep(1)
        assert int(current_value) == value, "Number of Copies setting is not successful"
    
    def get_value_of_no_of_print_copies(self, default_initValue=1):
        return self.get_value_of_no_of_copies(self.tumbler_listLayout, default_initValue)

    def get_value_of_no_of_preview_copies(self, default_initValue=1):
        return self.get_value_of_no_of_copies(self.tumbler_preview, default_initValue)

    def set_no_of_print_copies(self, value):
        self.set_no_of_copies(value, self.tumbler_listLayout)

    def set_no_of_preview_copies(self, value):
        self.set_no_of_copies(value, self.tumbler_preview)
    
    def get_loc_string(self, loc_str_id, net, locale):
        loc_msg = LocalizationHelper.get_string_translation(net, loc_str_id, locale)
        logging.info("Localized string: %s", loc_msg)
        return loc_msg     

    def check_QF_menu_icon(self, layout, icon_source):
        self._spice.wait_for(layout)
        QF_Icon = self._spice.query_item(layout)
        assert str(QF_Icon["icon"]) == str(icon_source)

    def goto_mainApp_printApp_quick_forms(self):
        """
        Purpose: Navigates to Quick Forms app screen from any other screen
        Ui Flow: Any screen -> Home Screen -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        if not self.goto_print_app():
            #If above method goto_print_app method return False, means there is no "Print" app in Homescreen, then redirect the Quick forms call to Menu->Print app.
            self.QUICK_FORMS_LAYOUT = self.MENU_LIST_LAYOUT
            self._spice.homeMenuUI().goto_menu_print(self._spice)
            self._spice.homeMenuUI().menu_navigation(self._spice, "#" + self.QUICK_FORMS_LAYOUT, QUICKFORMS_MENU_BUTTON)
        else:
            self.QUICK_FORMS_LAYOUT = self.BUTTON_LIST_LAYOUT
            self._spice.homeMenuUI().menu_navigation(self._spice, "#" + self.QUICK_FORMS_LAYOUT, QUICKFORMS_BUTTON)
        self._spice.wait_for('#QuickFormsAppApplicationStackView')

    
    def goto_mainApp_menuApp_printApp_quick_form(self):
        """
        Purpose: Navigates to Quick Forms app screen from any other screen
        Ui Flow: Any screen -> Home Screen -> Menu App -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        self.QUICK_FORMS_LAYOUT = self.MENU_LIST_LAYOUT
        self._spice.homeMenuUI().goto_menu_print(self._spice)
        self._spice.homeMenuUI().menu_navigation(self._spice, "#" + self.QUICK_FORMS_LAYOUT, QUICKFORMS_MENU_BUTTON)
        self._spice.wait_for('#QuickFormsAppApplicationStackView')
   
   #Quick Forms Notebook paper
    def detailed_quickForms_notebookPaper_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "notebookPaperMenuButton")
        self._spice.wait_for('#quickFormsListView')
    
    def detailed_quickForms_notebookPaper_selected_verify_icon(self):
        self.detailed_quickForms_notebookPaper_selected()

    def detailed_quickForms_notebookPaper_rule_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "selectionButton")
        self._spice.wait_for('#RadioButtonListLayout')
    
    def detailed_quickForms_notebookPaper_narrowRule_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonnarrow")
        self._spice.wait_for('#MenuListLayout')

    def detailed_quickForms_notebookPaper_wideRule_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonwide")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_notebookPaper_childRule_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonchild")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_notebookPaper_preview_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self._spice.wait_for('#quickFormsPreview')

    def detailed_quickForms_notebookPaper_preview_narrow_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.NARROW_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_wide_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.WIDE_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_child_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.CHILD_RULE_MENU_ICON)
    
    def detailed_quickForms_notebookPaper_previewPrint_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Print")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_notebookPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Cancel")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_notebookPaper_print_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms graphing paper
    def detailed_quickForms_graphingPaper_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "graphingPaperMenuButton")
        self._spice.wait_for('#quickFormsListView')
    
    def detailed_quickForms_graphingPaper_selected_verify_icon(self):
        self.detailed_quickForms_graphingPaper_selected()

    def detailed_quickForms_graphingPaper_rule_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "selectionButton")
        self._spice.wait_for('#RadioButtonListLayout')
    
    def detailed_quickForms_graphingPaper_oneEighth_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtononeeighth")
        self._spice.wait_for('#MenuListLayout')

    def detailed_quickForms_graphingPaper_fiveMillimeter_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonfivemillimeter")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_graphingPaper_preview_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self._spice.wait_for('#quickFormsPreview')

    def detailed_quickForms_graphingPaper_preview_oneEighth_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.ONE_EIGHTH_MENU_ICON)

    def detailed_quickForms_graphingPaper_preview_fiveMillimeter_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.FIVE_MM_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_previewPrint_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Print")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_graphingPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Cancel")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_graphingPaper_print_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms checklists
    def detailed_quickForms_checklists_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "checklistsMenuButton")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_checklists_selected_verify_icon(self):
        self.detailed_quickForms_checklists_selected()
    
    def detailed_quickForms_checklists_rule_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "selectionButton")
        self._spice.wait_for('#RadioButtonListLayout')
    
    def detailed_quickForms_checklists_optionButton1_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButton1")
        self._spice.wait_for('#MenuListLayout')

    def detailed_quickForms_checklists_optionButton2_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButton2")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_checklists_preview_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self._spice.wait_for('#quickFormsPreview')

    def detailed_quickForms_checklists_preview_optionButton1_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.CHECKLIST_OPT_1_MENU_ICON)

    def detailed_quickForms_checklists_preview_optionButton2_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.CHECKLIST_OPT_2_MENU_ICON)
    
    def detailed_quickForms_checklists_previewPrint_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Print")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_checklists_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Cancel")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_checklists_print_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms music paper
    def detailed_quickForms_musicPaper_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "musicPaperMenuButton")
        self._spice.wait_for('#quickFormsListView')
    
    def detailed_quickForms_musicPaper_selected_verify_icon(self):
        self.detailed_quickForms_musicPaper_selected()

    def detailed_quickForms_musicPaper_rule_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "selectionButton")
        self._spice.wait_for('#RadioButtonListLayout')
    
    def detailed_quickForms_musicPaper_portrait_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonportrait")
        self._spice.wait_for('#MenuListLayout')

    def detailed_quickForms_musicPaper_landscape_selected(self):
        self.quick_forms_click_button("RadioButtonListLayout", "QuickFormsOptionButtonlandscape")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_musicPaper_preview_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self._spice.wait_for('#quickFormsPreview')

    def detailed_quickForms_musicPaper_preview_portrait_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.MUSIC_PORTRAIT_MENU_ICON)

    def detailed_quickForms_musicPaper_preview_landscape_selected_verify_icon(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "previewButton")
        self.check_QF_menu_icon('#quickFormsPreview', self.MUSIC_LANDSCAPE_MENU_ICON)
    
    def detailed_quickForms_musicPaper_previewPrint_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Print")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_musicPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "Cancel")
        self._spice.wait_for('#quickFormsListView')

    def detailed_quickForms_musicPaper_print_selected(self):
        self.quick_forms_click_button(self.QUICK_FORMS_LAYOUT, "printButton")
        self.wait_for_alert_dialog_toast_window()