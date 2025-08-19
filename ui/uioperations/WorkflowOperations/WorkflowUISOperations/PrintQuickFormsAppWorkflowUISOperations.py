import logging
import re
import time
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.PrintQuickFormsAppWorkflowUICommonOperations import PrintQuickFormsAppWorkflowUICommonOperations


QUICKFORMS_MENU_APP = "#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42MenuApp"

class PrintQuickFormsAppWorkflowUISOperations(PrintQuickFormsAppWorkflowUICommonOperations):
    max_cancel_time = 60
    property_current_index = "currentIndex"
    property_active_focus = "activeFocus"
    ALERT_DIALOG_TOAST_WINDOW = "#ToastWindowToastStackView"
    ALERT_TOAST_MESSAGE = "#SpiceToast #ToastRow #infoTextToastMessage"
    ALERT_TOAST_ICON = "#SpiceToast #ToastRow #ToastIconForText"
    NARROW_RULE_MENU = "#quickFormsSelectionOptionnarrow"
    WIDE_RULE_MENU = "#quickFormsSelectionOptionwide"
    CHILD_RULE_MENU = "#quickFormsSelectionOptionchild"
    ONE_EIGHTH_MENU = "#quickFormsSelectionOptiononeeighth"
    FIVE_MM_MENU = "#quickFormsSelectionOptionfivemillimeter"
    CHECKLIST_OPT_1_MENU = "#quickFormsSelectionOption1"
    CHECKLIST_OPT_2_MENU = "#quickFormsSelectionOption2"
    MUSIC_PORTRAIT_MENU = "#quickFormsSelectionOptionportrait"
    MUSIC_LANDSCAPE_MENU = "#quickFormsSelectionOptionlandscape"
    NARROW_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperNarrowRule.json"
    WIDE_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperWideRule.json"
    CHILD_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperChildRule.json"
    ONE_EIGHTH_MENU_ICON = "qrc:/images/Graphics/GraphingPaper1By8in.json"
    FIVE_MM_MENU_ICON = "qrc:/images/Graphics/GraphingPaper5mm.json"
    CHECKLIST_OPT_1_MENU_ICON = "qrc:/images/Graphics/ChecklistPaper1Col.json"
    CHECKLIST_OPT_2_MENU_ICON = "qrc:/images/Graphics/ChecklistPaper2Col.json"
    MUSIC_PORTRAIT_MENU_ICON = "qrc:/images/Graphics/MusicPaperPortrait.json"
    MUSIC_LANDSCAPE_MENU_ICON = "qrc:/images/Graphics/MusicPaperLandscape.json"

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.quickFormRuleType = None

    def goto_print_app(self):
        """
        Purpose: Navigates to Print app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Print app
        :param spice: Takes 0 arguments
        :return: True, if Print app in Homescreen, else False.
        """
        self.goto_mainmenu()

        starttime = time.time()
        timespentwaiting = time.time() - starttime
        currentScreen = self._spice.wait_for("#HomeScreenView")
        while (self._spice.query_item("#CurrentAppText")["text"] != "Print" and timespentwaiting < self.maxtimeout):
            currentScreen.mouse_wheel(180, 180)
            timespentwaiting = time.time() - starttime

        if(self._spice.query_item("#CurrentAppText")["text"] == "Print"):
            currentitem = self._spice.query_item("#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD")
            currentitem.mouse_click()
            return True
        else:
            logging.info("Home Screen does not have ""Print"" app.")
            return False
        
    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def check_toast_information_icon(self):
        alertIcon = self._spice.query_item(self.ALERT_TOAST_ICON)
        #print("icon source=",alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/+loTheme/information_xs.json")

    def check_toast_message(self, text):
        toastMessage = self._spice.query_item(self.ALERT_TOAST_MESSAGE)
        #print("Title message=",str(toastMessage["text"]))
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)
        # Verify toast icon type. Workflow does not support icons on toast popups.
        #self.check_toast_information_icon()

    def check_QF_menu_icon(self, layout, icon_source):
        self._spice.wait_for(layout)
        QF_Icon = self._spice.query_item(layout)
        assert str(QF_Icon["icon"]) == str(icon_source)

    def goto_mainApp_menuApp_printApp_quick_form(self):
        """
        Purpose: Navigates to Quick Forms app screen from any other screen
        Ui Flow: Any screen -> Home Screen -> Menu App -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        self._spice.homeMenuUI().goto_menu_print(self._spice)
        self.goto_quick_forms()

   #Quick Forms Notebook paper
    def detailed_quickForms_notebookPaper_selected(self):
        self.quick_forms_click_button("notebookPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
    
    def detailed_quickForms_notebookPaper_selected_verify_icon(self):
        self.quick_forms_click_button("notebookPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.NARROW_RULE_MENU,self.NARROW_RULE_MENU_ICON)
        self.check_QF_menu_icon(self.WIDE_RULE_MENU,self.WIDE_RULE_MENU_ICON)
        self.check_QF_menu_icon(self.CHILD_RULE_MENU,self.CHILD_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_rule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionnarrow")
        self._spice.wait_for('#SpiceRadioButton')
    
    def detailed_quickForms_notebookPaper_narrowRule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionnarrow")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionsnarrow"

    def detailed_quickForms_notebookPaper_wideRule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionwide")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionswide"

    def detailed_quickForms_notebookPaper_childRule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionchild")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionschild"

    def detailed_quickForms_notebookPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')
    
    def detailed_quickForms_notebookPaper_preview_narrow_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.NARROW_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_wide_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.WIDE_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_child_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHILD_RULE_MENU_ICON)
    
    def detailed_quickForms_notebookPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_notebookPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
        self.quick_forms_click_button("cancelButton")
        self.quick_forms_job_cancel_button(cdm, net, job, locale)

    def detailed_quickForms_notebookPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms graphing paper
    def detailed_quickForms_graphingPaper_selected(self):
        self.quick_forms_click_button("graphingPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
    
    def detailed_quickForms_graphingPaper_selected_verify_icon(self):
        self.quick_forms_click_button("graphingPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.ONE_EIGHTH_MENU,self.ONE_EIGHTH_MENU_ICON)
        self.check_QF_menu_icon(self.FIVE_MM_MENU,self.FIVE_MM_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_rule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptiononeeighth")
        self._spice.wait_for('#SpiceRadioButton')
    
    def detailed_quickForms_graphingPaper_oneEighth_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptiononeeighth")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionsoneeighth"

    def detailed_quickForms_graphingPaper_fiveMillimeter_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionfivemillimeter")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionsfivemillimeter"

    def detailed_quickForms_graphingPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')
    
    def detailed_quickForms_graphingPaper_preview_oneEighth_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.ONE_EIGHTH_MENU_ICON)

    def detailed_quickForms_graphingPaper_preview_fiveMillimeter_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.FIVE_MM_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_graphingPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
        self.quick_forms_click_button("cancelButton")
        self.quick_forms_job_cancel_button(cdm, net, job, locale)

    def detailed_quickForms_graphingPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms checklists
    def detailed_quickForms_checklists_selected(self):
        self.quick_forms_click_button("checklistsSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

    def detailed_quickForms_checklists_selected_verify_icon(self):
        self.quick_forms_click_button("checklistsSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.CHECKLIST_OPT_1_MENU,self.CHECKLIST_OPT_1_MENU_ICON)
        self.check_QF_menu_icon(self.CHECKLIST_OPT_2_MENU,self.CHECKLIST_OPT_2_MENU_ICON)
    
    def detailed_quickForms_checklists_rule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOption1")
        self._spice.wait_for('#SpiceRadioButton')
    
    def detailed_quickForms_checklists_optionButton1_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOption1")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptions1"

    def detailed_quickForms_checklists_optionButton2_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOption2")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptions2"

    def detailed_quickForms_checklists_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')

    def detailed_quickForms_checklists_preview_optionButton1_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHECKLIST_OPT_1_MENU_ICON)

    def detailed_quickForms_checklists_preview_optionButton2_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHECKLIST_OPT_2_MENU_ICON)
    
    def detailed_quickForms_checklists_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_checklists_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
        self.quick_forms_click_button("cancelButton")
        self.quick_forms_job_cancel_button(cdm, net, job, locale)

    def detailed_quickForms_checklists_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms music paper
    def detailed_quickForms_musicPaper_selected(self):
        self.quick_forms_click_button("musicPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

    def detailed_quickForms_musicPaper_selected_verify_icon(self):
        self.quick_forms_click_button("musicPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.MUSIC_PORTRAIT_MENU,self.MUSIC_PORTRAIT_MENU_ICON)
        self.check_QF_menu_icon(self.MUSIC_LANDSCAPE_MENU,self.MUSIC_LANDSCAPE_MENU_ICON)

    def detailed_quickForms_musicPaper_rule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionportrait")
        self._spice.wait_for('#SpiceRadioButton')
    
    def detailed_quickForms_musicPaper_portrait_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionportrait")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionsportrait"

    def detailed_quickForms_musicPaper_landscape_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionlandscape")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionslandscape"

    def detailed_quickForms_musicPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')

    def detailed_quickForms_musicPaper_preview_portrait_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.MUSIC_PORTRAIT_MENU_ICON)

    def detailed_quickForms_musicPaper_preview_landscape_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.MUSIC_LANDSCAPE_MENU_ICON)
    
    def detailed_quickForms_musicPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_musicPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
        self.quick_forms_click_button("cancelButton")
        self.quick_forms_job_cancel_button(cdm, net, job, locale)

    def detailed_quickForms_musicPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()
