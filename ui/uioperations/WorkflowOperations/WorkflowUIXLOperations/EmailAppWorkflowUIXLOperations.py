from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowUICommonOperations import EmailAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.scan.ScanAction import ScanAction

import logging
import time


class EmailAppWorkflowUIXLOperations(EmailAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations

    def complete_email_send(self, cdm, udw, job, scan_more_pages: bool = False, dial_value: int = 180, wait_time=5, need_to_wait_email_landing_view=True,first = True, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        scan_action = ScanAction().set_udw(udw).set_cdm(cdm)
        new_number_of_jobs_to_check = len(job.get_newjobs()) + 1

        # In case of concurrent jobs, if media is loaded, start should be called, but if media is not loaded, load media will start job automatically
        if(scan_action.is_media_loaded()):
            if first:
                self.email_send(wait_time,need_to_wait_email_landing_view)
            else:
                self.email_start_send(wait_time, need_to_wait_email_landing_view)
        else:
            scan_action.load_media()
            self.spice.scan_settings.wait_for_preview_n(1)
            # Non concurrent jobs need to start job explicitly
            if job.job_concurrency_supported == "false":
                if first:
                    self.email_send(wait_time,need_to_wait_email_landing_view)
                else:
                    self.email_start_send(wait_time, need_to_wait_email_landing_view)
            
        job_ticket = job.get_job_details("scanEmail")
        file_type = job_ticket["pipelineOptions"]["sendFileAttributes"]["fileType"]
        self.wait_for_scan_email_job_to_complete(cdm, udw, job, file_type, number_of_jobs_to_check=new_number_of_jobs_to_check, button=button, wait_for_preview=wait_for_preview)

    def start_scan_email_job_with_settings(self, job, cdm, udw, name: str, recordId, scan_options: dict, scan_more_pages: bool = False):
        '''
        Start scan to email with scan settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        cdm -> cdm instance
        udw -> udw instance
        name -> is the name provided in the display_name field while creating email profile
        scan_options = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'orientation': 'portrait',
            'lighter_darker': 1,
            'contrast': 1
        }
        '''
        self.select_options_scan_email(cdm, udw, name, recordId, scan_options)
        assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 9.0)
        self.complete_email_send(cdm,udw,job,scan_more_pages)

    def wait_for_scan_email_job_to_complete(self, cdm, udw, job, file_type, pages=1, time_out=120,scan_emulation=None, number_of_jobs_to_check=1, button=ScanAppWorkflowObjectIds.send_button, wait_for_preview=True, adf_loaded=False):
        """
        wait for scan email job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        """
        common_instance = ScanCommon(cdm, udw)
        completed_jobs_expected_in_row = []
        if scan_emulation==None:
            scan_resource = common_instance.scan_resource()
        else:
            scan_resource= self.get_scan_resource_used(udw,scan_emulation) 
        logging.info("Scan resource used in UIXL: %s", scan_resource)   
        for i in range(number_of_jobs_to_check):
            completed_jobs_expected_in_row.append({"type": "scanEmail", "status": "success"})

        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages(type = "email")

        if scan_resource == "Glass": 
            try:
                for _ in range(pages-1):
                    scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                    self.spice.validate_button(scan_add_page_button)
                    scan_add_page_button.mouse_click()
                    time.sleep(2)

                scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                logging.info("#finish button found")
                self.spice.validate_button(scan_add_page_done_button)
                scan_add_page_done_button.mouse_click()
            except TimeoutError:
                logging.info("flatbed Add page is not available")
        elif scan_resource == "MDF":
            for i in range(pages-1):
                logging.info("Wait for page %s", i)
                if i < pages - 1:
                    logging.info("Loading media %s", i)
                    udw.mainApp.ScanMedia.loadMedia("MDF")

            # Wait for preview
            if wait_for_preview:
                self.spice.scan_settings.wait_for_preview_n(pages,15)

            scan_send_button = self.spice.wait_for(button)
            self.spice.wait_until(lambda: scan_send_button["visible"], 10)
            self.spice.wait_until(lambda: scan_send_button["enabled"], 10)
            scan_send_button.mouse_click()
            self.spice.scan_settings.mdf_add_page_alert_done()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completed_jobs_expected_in_row, time_out)

    def email_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=2, need_to_wait_email_landing_view=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        
        isExpanded = self.is_landing_expanded()
        if isExpanded:
            self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_start_main_panel, timeout = 20.0)
            self.spice.email.wait_and_click_on_middle(EmailAppWorkflowObjectIds.button_email_start_main_panel)
        else:
            self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_start, timeout = 20.0)
            self.spice.email.wait_and_click_on_middle(EmailAppWorkflowObjectIds.button_email_start)

        time.sleep(wait_time)

        if need_to_wait_email_landing_view:
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        logging.info("Inside Email Details Screen")               

        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()

    def verify_error_msg_email_send_without_recipient(self, net):
        '''
        From email landing view click on send button and check for error prompt
        UI Flow is email landing view -> send -> error prompt
        '''
        self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_start, timeout = 20.0)
        send_button = self.spice.query_item(EmailAppWorkflowObjectIds.button_email_start)
        
        self.wait_and_validate_property_value(send_button, "visible", True, 10)
        self.wait_and_validate_property_value(send_button, "enabled", True, 10)
        self.wait_and_validate_property_value(send_button, "constrained", True, 10)
        send_button.mouse_click()

        self.spice.wait_for(EmailAppWorkflowObjectIds.message_email_error_alert, timeout = 20.0)
        send_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_enter_pin_wrong_ok)
        send_button.mouse_click()


    def email_start_send(self, scan_more_pages: bool = False, dial_value: int = 180, wait_time=2, need_to_wait_email_landing_view=True):
        '''
        From email details screen navigate to email send successfully screen
        UI Flow is select email details -> email send success
        '''
        
        isExpanded = self.is_landing_expanded()
        if isExpanded:
            current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send_main_panel, timeout = 20.0)
        else:
            current_button = self.spice.wait_for(EmailAppWorkflowObjectIds.button_email_send, timeout = 20.0)

        self.spice.wait_until(lambda: current_button["visible"], 20.0)
        self.spice.wait_until(lambda: current_button["enabled"], 20.0)
        current_button.mouse_click()
        time.sleep(wait_time)
        if need_to_wait_email_landing_view:
            assert self.spice.wait_for(EmailAppWorkflowObjectIds.view_email_landing_view, timeout = 20.0)
        logging.info("Inside Email Details Screen")               

        common_instance = ScanCommon(self.spice.cdm, self.spice.udw)
        if common_instance.should_prompt_for_additional_pages(scan_more_pages, "email"):
            self.scan_operations.flatbed_scan_more_pages()            

    def back_to_back_email_jobs(self, scan_resource, cdm, udw, job, scan_emulation, times=1,send_instance=None):
        """
        Back to back email jobs
        """
        for i in range(times):
            logging.info(f"Starting email job iteration {i+1} of {times}")
            if scan_resource == "MDF":
                scan_emulation.media.load_media('MDF', 1)
            else:
                scan_emulation.media.load_media('ADF', 1)
            if i == 0:
                logging.info("First email job, calling complete_email_send with first=True")
                self.complete_email_send(cdm, udw, job, first=True)
            else:
                logging.info("Subsequent email job, calling complete_email_send with first=False")
                self.spice.scan_settings.wait_for_preview_n(1)
                self.complete_email_send(cdm, udw, job, first=False)
            job.wait_for_no_active_jobs()
            logging.info("Waiting for email send landing view")
            self.spice.email.wait_for_email_send_landing_view()
            if send_instance:
                logging.info("Waiting for corresponding scanner status with CDM")
                send_instance.wait_for_corresponding_scanner_status_with_cdm(timeout=30)
            logging.info(f"Completed email job iteration {i+1} of {times}")
