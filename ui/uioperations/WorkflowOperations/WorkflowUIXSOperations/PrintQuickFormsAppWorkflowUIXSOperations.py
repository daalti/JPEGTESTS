import logging
import re
from dunetuf.ui.uioperations.WorkflowOperations.PrintQuickFormsAppWorkflowUICommonOperations import PrintQuickFormsAppWorkflowUICommonOperations

class PrintQuickFormsAppWorkflowUIXSOperations(PrintQuickFormsAppWorkflowUICommonOperations):

    ALERT_DIALOG_TOAST_WINDOW = "#ToastWindowToastStackView"
    ALERT_TOAST_MESSAGE = "#SpiceToast #ToastRow #infoTextToastMessage"
    NARROW_RULE_MENU = "#quickFormsSelectionOptionnarrow"
    WIDE_RULE_MENU = "#quickFormsSelectionOptionwide"
    CHILD_RULE_MENU = "#quickFormsSelectionOptionchild"
    ONE_EIGHTH_MENU = "#quickFormsSelectionOptiononeeighth"
    FIVE_MM_MENU = "#quickFormsSelectionOptionfivemillimeter"
    CHECKLIST_OPT_1_MENU = "#quickFormsSelectionOption1"
    CHECKLIST_OPT_2_MENU = "#quickFormsSelectionOption2"
    CHECKLIST_OPT_1_MENU_ICON = "qrc:/images/Graphics/ChecklistPaper1Col.json"
    CHECKLIST_OPT_2_MENU_ICON = "qrc:/images/Graphics/ChecklistPaper2Col.json"
    ONE_EIGHTH_MENU_ICON = "qrc:/images/Graphics/GraphingPaper1By8in.json"
    FIVE_MM_MENU_ICON = "qrc:/images/Graphics/GraphingPaper5mm.json"
    MUSIC_PORTRAIT_MENU = "#quickFormsSelectionOptionportrait"
    MUSIC_LANDSCAPE_MENU = "#quickFormsSelectionOptionlandscape"
    MUSIC_PORTRAIT_MENU_ICON = "qrc:/images/Graphics/MusicPaperPortrait.json"
    MUSIC_LANDSCAPE_MENU_ICON = "qrc:/images/Graphics/MusicPaperLandscape.json"
    DROP_DOWN_BUTTON = "#dropDownButton"
    CLOSE_BUTTON = "#closeButton"
    CHECKLIST_OPT_1_MENU = "#quickFormsSelectionOption1"
    CHECKLIST_OPT_2_MENU = "#quickFormsSelectionOption2"
    NARROW_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperNarrowRule.json"
    WIDE_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperWideRule.json"
    CHILD_RULE_MENU_ICON = "qrc:/images/Graphics/NotebookPaperChildRule.json"

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        self.quickFormRuleType = None

    def goto_mainApp_menuApp_printApp_quick_form(self):
        self._spice.homeMenuUI().goto_menu_print(self._spice)
        self.goto_quick_forms()
    
    def get_value_of_no_of_preview_copies(self, default_initValue=0):
        self._spice.query_item(self.DROP_DOWN_BUTTON).mouse_click()
        copy_value = self.get_value_of_no_of_copies(self.numberOfCopies_spin_box_preview)
        self._spice.query_item(self.CLOSE_BUTTON).mouse_click()
        return copy_value

    def set_no_of_preview_copies(self, value):
        self._spice.query_item(self.DROP_DOWN_BUTTON).mouse_click()
        self.set_no_of_copies(value, self.numberOfCopies_spin_box_preview)
        self._spice.query_item(self.CLOSE_BUTTON).mouse_click()
    
    def detailed_quickForms_checklists_preview_optionButton1_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHECKLIST_OPT_1_MENU_ICON)
    
    def detailed_quickForms_checklists_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_checklists_preview_optionButton2_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHECKLIST_OPT_2_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_selected_verify_icon(self):
        self.quick_forms_click_button("graphingPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.ONE_EIGHTH_MENU,self.ONE_EIGHTH_MENU_ICON)
        self.check_QF_menu_icon(self.FIVE_MM_MENU,self.FIVE_MM_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_preview_fiveMillimeter_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.FIVE_MM_MENU_ICON)
    
    def detailed_quickForms_graphingPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')
    
    def detailed_quickForms_graphingPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_graphingPaper_preview_oneEighth_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.ONE_EIGHTH_MENU_ICON)
    
    def detailed_quickForms_musicPaper_selected_verify_icon(self):
        self.quick_forms_click_button("musicPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.MUSIC_PORTRAIT_MENU,self.MUSIC_PORTRAIT_MENU_ICON)
        self.check_QF_menu_icon(self.MUSIC_LANDSCAPE_MENU,self.MUSIC_LANDSCAPE_MENU_ICON)


    def detailed_quickForms_notebookPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
    
    def detailed_quickForms_notebookPaper_previewCancel_selected(self, cdm, net, job, locale):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()
        self.quick_forms_click_button("cancelButton")
        self.quick_forms_job_cancel_button(cdm, net, job, locale)
    
    def detailed_quickForms_notebookPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')
    
    def detailed_quickForms_checklists_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')
    
    def check_QF_menu_icon(self, layout, icon_source):
        self._spice.wait_for(layout)
        QF_Icon = self._spice.query_item(layout)
        assert str(QF_Icon["icon"]) == str(icon_source)
    
    def detailed_quickForms_checklists_selected_verify_icon(self):
        self.quick_forms_click_button("checklistsSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.CHECKLIST_OPT_1_MENU,self.CHECKLIST_OPT_1_MENU_ICON)
        self.check_QF_menu_icon(self.CHECKLIST_OPT_2_MENU,self.CHECKLIST_OPT_2_MENU_ICON)

    #Quick Forms checklists
    def detailed_quickForms_checklists_selected(self):
        self.quick_forms_click_button("checklistsSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

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

    def detailed_quickForms_checklists_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def check_toast_message(self, text):
        toastMessage = self._spice.query_item(self.ALERT_TOAST_MESSAGE)
        toastMessage = re.sub("[...]", "", str(toastMessage["text"]))
        assert toastMessage == str(text)

    #Quick Forms Notebook paper
    def detailed_quickForms_notebookPaper_selected(self):
        self.quick_forms_click_button("notebookPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

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
    def detailed_quickForms_notebookPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms graphing paper
    def detailed_quickForms_graphingPaper_selected(self):
        self.quick_forms_click_button("graphingPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

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

    def detailed_quickForms_graphingPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    #Quick Forms music paper
    def detailed_quickForms_musicPaper_selected(self):
        self.quick_forms_click_button("musicPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')

    def detailed_quickForms_musicPaper_rule_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionportrait")
        self._spice.wait_for('#SpiceRadioButton')

    def detailed_quickForms_musicPaper_landscape_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionlandscape")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionslandscape"

    def detailed_quickForms_musicPaper_print_selected(self):
        self.quick_forms_click_button("printButton")
        self.wait_for_alert_dialog_toast_window()

    def detailed_quickForms_musicPaper_portrait_selected(self):
        self.quick_forms_click_button("quickFormsSelectionOptionportrait")
        self._spice.wait_for('#SpiceRadioButton')
        self.quickFormRuleType = "quickFormsSelectionOptionsportrait"

    def detailed_quickForms_musicPaper_preview_selected(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self._spice.wait_for('#quickFormsPreviewPage')

    def detailed_quickForms_musicPaper_previewPrint_selected(self):
        self.quick_forms_click_button("printPreviewButton")
        self.wait_for_alert_dialog_toast_window()

    def detailed_quickForms_musicPaper_preview_landscape_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.MUSIC_LANDSCAPE_MENU_ICON)

    def detailed_quickForms_notebookPaper_selected_verify_icon(self):
        self.quick_forms_click_button("notebookPaperSettingsTextImage")
        self._spice.wait_for('#quickFormsListViewlist1')
        self.check_QF_menu_icon(self.NARROW_RULE_MENU,self.NARROW_RULE_MENU_ICON)
        self.check_QF_menu_icon(self.WIDE_RULE_MENU,self.WIDE_RULE_MENU_ICON)
        self.check_QF_menu_icon(self.CHILD_RULE_MENU,self.CHILD_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_child_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.CHILD_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_narrow_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.NARROW_RULE_MENU_ICON)

    def detailed_quickForms_notebookPaper_preview_wide_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.WIDE_RULE_MENU_ICON)

    def detailed_quickForms_musicPaper_preview_portrait_selected_verify_icon(self):
        previewButton = self._spice.wait_for("#quickFormsListView #quickFormsListViewverticalLayout #" + self.quickFormRuleType + " " + "#previewButton")
        previewButton.mouse_click()
        self.check_QF_menu_icon('#quickFormsPreviewPage', self.MUSIC_PORTRAIT_MENU_ICON)
