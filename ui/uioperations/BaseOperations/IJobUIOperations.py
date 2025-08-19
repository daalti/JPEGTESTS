import sys

class IJobUIOperations(object):
    def goto_created_job(self, job_id):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_selected_job(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_job_info(self, job_id, index=0):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def recover_job_status(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def recover_job_status_type(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_job(self, job_id):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_old_jobs(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def reprint_job(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Jobs settings

    def goto_menu_jobs_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_visible_hide_deleted_jobs(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_hide_deleted_jobs(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_hide_deleted_jobs(self, spice, value:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_cancel_jobs_on_hold_delay(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_cancel_jobs_on_hold_delay(self, spice) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_cancel_jobs_on_hold_delay(self, spice, value:int) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_job_queue_recovery_mode(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_job_queue_recovery_mode(self, spice) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_job_queue_recovery_mode(self, spice, value:str) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_job_on_hold_for_manual_release(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_job_on_hold_for_manual_release(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_job_on_hold_for_manual_release(self, spice, enable:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_reprint_resend_jobs_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_reprint_resend_jobs_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_reprint_resend_jobs_enabled(self, spice, enable:bool, confirm_disabled:bool = False) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_visible_promote_to_interrupt_print_job_enabled(self, spice, enable:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_job_status_from_status_center(self):
        """
        Purpose: From FPUI, expand status center, get the current job status.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def recover_job_fax_destination(self):
        '''
        Recover the destination value of fax job
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def recover_job_scanned_pages(self):
        '''
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def recover_job_original_sides(self):
        '''
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def recover_job_resolution(self):
        '''
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def recover_job_output_sides(self):
        '''
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)