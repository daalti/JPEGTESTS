import sys
from typing import Dict

class IJobStorageAppUIOperations(object):

    def goto_scan_to_job_storage_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_job_storage_scan_details(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_options_list_from_scan_to_job_storage_screen(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_scan_to_job_storage_from_options_list(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_home_from_scan_to_job_storage(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def save_to_scan_to_job_storage_and_verify(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_save_to_job_storage(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def cancel_scan_to_job_storage(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_job_to_job_storage(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_scan_cancel_job_storage(self, abId, recordId):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def save_as_default_job_storage_ticket(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_job_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_jobName_empty_message(self, net):
        '''
        UI should be at storage landingview.
        Function will verify the filename empty message.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def wait_for_scan_to_job_storage_job_to_complete(self, cdm, udw, job, file_type, pages=1, time_out=90):
        """
        wait for scan storage job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def back_to_scan_app_from_scan_to_job_storage(self):
        '''
        UI should be in Scan to Network storage landing screen
        UI flow is Scan storage landing view -> Scan app landing screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
