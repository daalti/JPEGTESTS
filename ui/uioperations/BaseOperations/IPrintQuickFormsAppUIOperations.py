#########################################################################################
# @file      IPrintQuickFormsAppUIOperations.py
# @author    Biju Thomas (bthomas@hp.com)
# @date      09-28-2022
# @brief     Interface for Quick Forms UI navigation methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys

class IPrintQuickFormsAppUIOperations(object):

    def goto_mainApp_printApp_quick_forms(self):
            """
            Purpose: Navigates to Quick Form app screen from any other screen
            Ui Flow: Any screen -> Main menu -> Print app -> Quick Forms app
            :param spice: Takes 0 arguments
            :return: None
            """
            raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_mainApp_menuApp_printApp_quick_form(self):
        """
        Purpose: Navigates to Quick Form app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Menu App -> Print app -> Quick Forms app
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_value_of_no_of_print_copies(self, default_initValue=0):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_value_of_no_of_preview_copies(self, default_initValue=0):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_no_of_print_copies(self, value):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_no_of_preview_copies(self, value):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_toast_message(self, text):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_print_complete_successfully(self, time_out=300):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_loc_string(self, loc_str_id, net, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def quick_forms_job_cancel_button(self, cdm, net, job, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    #Quick Forms Notebook paper
    def detailed_quickForms_notebookPaper_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_notebookPaper_rule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_narrowRule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_wideRule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_childRule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_preview_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_notebookPaper_preview_narrow_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_preview_wide_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_preview_child_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_previewPrint_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_previewCancel_selected(self, cdm, net, job, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_notebookPaper_print_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    #Quick Forms graphing paper
    def detailed_quickForms_graphingPaper_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_graphingPaper_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_rule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_oneEighth_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_fiveMillimeter_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_preview_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_graphingPaper_preview_oneEighth_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_preview_fiveMillimeter_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_previewPrint_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_previewCancel_selected(self, cdm, net, job, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_graphingPaper_print_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    #Quick Forms checklists
    def detailed_quickForms_checklists_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_checklists_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_rule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_optionButton1_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_optionButton2_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_preview_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_checklists_preview_optionButton1_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_preview_optionButton2_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_previewPrint_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_previewCancel_selected(self, cdm, net, job, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_checklists_print_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    #Quick Forms music paper
    def detailed_quickForms_musicPaper_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_musicPaper_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_rule_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_portrait_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_landscape_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_preview_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_quickForms_musicPaper_preview_portrait_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_preview_landscape_selected_verify_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_previewPrint_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def detailed_quickForms_musicPaper_previewCancel_selected(self, cdm, net, job, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def detailed_quickForms_musicPaper_print_selected(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)