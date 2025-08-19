import sys
import logging
import time

from dunetuf.ui.uioperations.BaseOperations.IJobUIOperations import IJobUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowObjectIds import JobAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromNetworkAppWorkflowObjectIds import PrintFromNetworkAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds


class JobAppWorkflowUICommonOperations(IJobUIOperations):
    """JobAppWorkflowUICommonOperations class to initialize job workflow operations."""

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    def goto_created_job(self, job_id):
        # Check that the job is in "In Progress" section
        self.goto_job(job_id)
        assert self.spice.wait_for(JobAppWorkflowObjectIds.cancel_button, 10)

    def cancel_selected_job(self, curing = False, supported_concurrency = 'true'):
        '''
        Cancel a job from the job details view.
        '''
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_button, 10)
        cancel_button.mouse_click()

        # Confirm cancel job
        if curing == False:
            if supported_concurrency == 'true':
               cancel_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_confirmation_button, 10)
               cancel_button_confirm.mouse_click()
            else:
               cancel_button_confirm_unconcurrency = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_confirmation_unconcurrency_button, 10)
               cancel_button_confirm_unconcurrency.mouse_click()
    
        else:
                cancel_print_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_only_print_button, 10)
                cancel_print_button.mouse_click()
                cancel_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_yes_button, 10)
                cancel_button_confirm.mouse_click()

    def cancel_job_while_curing(self):
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_button, 10)
        cancel_button.mouse_click()
            
        # Confirm cancel curing job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_curing_job, 10)
        cancel_button.mouse_click()
    
    def release_selected_job(self):
        '''
        Release a job from the job details view.
        '''
        # Release job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.release_button, 10)
        cancel_button.mouse_click()
    
    def get_job_info(self, job_id, index=0):
        """Retrieves job information for a specified job ID.
        Waits for the job to be found in the job list and retrieves its job name.
        Args:
            job_id (str): The unique identifier of the job to retrieve information for.
        Returns:
            str: The job name/information retrieved from the UI element.
        Raises:
            TimeoutError: If the job information is not found within the timeout period.
        """
        start_time = time.time()
        max_timeout = 180
        found = False
        job_info = None
        while time.time() - start_time < max_timeout:
            try:
                job_info = self.spice.wait_for("#JOB_" + job_id + " #jobListElementTextBlock", timeout=5)["jobName"]
                if job_info:
                    found = True
                    return job_info
                    break
            except:
                time.sleep(1)
        if not found:
            raise TimeoutError(f"Job info not found within {max_timeout}s timeout.")

    def recover_job_status(self):
        '''
        Recover the job status text inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_status_text)["text"]

    def is_job_status_expected(self, net):
        '''
        Check if the job status is the expected successful / completed value
        '''
        return self.recover_job_status() == LocalizationHelper.get_string_translation(net, "cJobStateTypeCompleted", 'en-US')

    def recover_job_status_type(self):
        '''
        Recover the type of job status inside the job details view.

        For available types see SpiceStatusBox.Status
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_status_box)["status"]

    def print_job_status_description_text(self):
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_status_description_text)["text"]

    def recover_job_remaining_time(self):
        '''
        Recover the job time to finish inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_remaining_time)["text"]

    def recover_job_substrate_tpye(self):
        '''
        Recover the job media type name inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_substrate_type)["text"]

    def recover_job_media_tpye(self):
        '''
        Recover the job media type name inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_media_type)["text"]
    
    def recover_job_substrate_tpye(self):
        '''
        Recover the job substrate type name inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_substrate_type)["text"]
    
    def recover_job_media_source(self):
        '''
        Recover the job media source text inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_media_source)["text"]
    
    def wait_for_job_state(self , _job_ui, state, timeout=120) -> str:
        """Wait for the job state (uses UI).

        Args:
            jo_UI: job_ui of the job to wait for
            state: expected job state
            timeout: timeout in seconds to wait for job completion

        Returns:
            jobstate string

        Raises:
            TimeoutError if no new jobs are found within ``timeout`` seconds
        """
        jobstate, start_time = '', time.time()
        while time.time() < start_time + timeout:
            time.sleep(2)
            jobstate = _job_ui.recover_job_status()
            if state == jobstate:
                return jobstate
        raise TimeoutError(f'Job did not complete within {timeout}s timeout. Job State: {jobstate}.')

    def recover_job_start_time(self):
        '''
        Recover the job start time value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_start_time)["text"]
    
    def recover_job_output_size(self):
        '''
        Recover the output size value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_output_size)["text"]

    def recover_job_user_name(self):
        '''
        Recover the job user name value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_user_name)["text"]
    
    def recover_job_file_name(self):
        '''
        Recover the job file name value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_file_name)["text"]
    
    def recover_job_file_type(self):
        '''
        Recover the job file type value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_file_type)["text"]
    
    def recover_job_completion_time(self):
        '''
        Recover the job completion time value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_completion_time)["text"]
    
    def recover_job_margins(self):
        '''
        Recover the job margins value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_margins)["text"]
    
    def recover_job_destination(self):
        '''
        Recover the job destination value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_destination)["text"]
    
    def recover_job_output_destination(self):
        '''
        Recover the job output destination value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_output_destination)["text"]
    
    def recover_job_original_size(self):
        '''
        Recover the job original size value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_original_size)["text"]
    
    def recover_job_original_sides(self):
        '''
        Recover the job original size value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_original_sides)["text"]
    
    def recover_job_resolution(self):
        '''
        Recover the job status text inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_resolution)["text"]
    
    def recover_job_output_sides(self):
        '''
        Recover the job status text inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_output_sides)["text"]
    
    def recover_job_color_mode(self):
        '''
        Recover the job color mode text inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_color_mode)["text"]
    
    def recover_job_copies(self):
        '''
        Recover the job copies value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_copies)["text"]

    def recover_job_type(self):
        '''
        Recover the job type value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_type)["text"]
    
    def recover_job_fax_destination(self):
        '''
        Recover the destination value of fax job
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_fax_destination)["text"]
    
    def recover_job_scanned_pages(self):
        '''
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_details_scanned_pages)["text"]
    
    def recover_job_total_pages(self):
        '''
        Recover the job total page value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_total_pages)["text"]

    def recover_job_pages(self):
        '''
        Recover the job page count value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_pages)["text"]
    
    def recover_job_saved_pages(self):
        '''
        Recover the job saved page count value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_saved_pages)["text"]

    def recover_job_quality(self):
        '''
        Recover the job quality value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_quality)["text"]

    def recover_job_completion_text(self):
        '''
        Recover the job completion text value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_completion_text)["text"]

    def recover_job_collate(self):
        '''
        Recover the job collate value inside the job details view.
        '''
        return self.spice.wait_for(JobAppWorkflowObjectIds.job_collate)["text"]

    def goto_job(self, job_id):
        '''
        Go to a job inside job queue list.
        Args:
            job_id: ID of the job to open
        '''
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 180
        found = False
        view = self.spice.wait_for(JobAppWorkflowObjectIds.job_list_view)
        
        while found == False and (time_spent_waiting < max_timeout):    
            try:
                job_item_id = (JobAppWorkflowObjectIds.job_id).format(job_id)
                self.workflow_common_operations.goto_item(job_item_id, JobAppWorkflowObjectIds.job_list_view, scrollbar_objectname = JobAppWorkflowObjectIds.job_widget_scroll_bar, select_option=False)
                job_ui = self.spice.wait_for((JobAppWorkflowObjectIds.job_ui).format(job_id), 10)
                job_ui.mouse_click()
                time.sleep(2)
                job_view = self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
                assert job_view["visible"] == True
                found = True
            except:
                time_spent_waiting = time.time() - start_time
        assert found
    
    def goto_created_job_through_job_widget(self, job_id):
        # Check that the job is in "In Progress" section
        self.goto_job_through_job_widget(job_id)
        assert self.spice.wait_for(JobAppWorkflowObjectIds.cancel_button, 10)
        
    
    def goto_job_through_job_widget(self, job_id):
        '''
        Go to a job inside job queue list.
        Args:
            job_id: ID of the job to open
        '''
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 180
        found = False
        scroll_step = 0
        self.spice.wait_for(JobAppWorkflowObjectIds.job_widget_list_view)
        
        while found == False and (time_spent_waiting < max_timeout):    
            try:
                job_ui = self.spice.wait_for((JobAppWorkflowObjectIds.job_widget_ui).format(job_id), 10)
                job_ui.mouse_click()
                time.sleep(2)
                job_view = self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
                assert job_view["visible"] == True
                found = True
            except:
                scroll_step = scroll_step + 0.1
                self.workflow_common_operations.scroll_to_position_vertical(scroll_step, JobAppWorkflowObjectIds.job_widget_scroll_bar)
                time_spent_waiting = time.time() - start_time
        assert found

    def goto_old_jobs(self):
        '''
        Go to the old jobs screen.

        The "View older jobs" button is shown as a row at the end of the job list, so we have to scroll down until we find it.
        After that we can click on it and wait for the old jobs list to be visible.
        '''
        self.spice.wait_for(JobAppWorkflowObjectIds.job_app_list_view)
        self.workflow_common_operations.goto_item(JobAppWorkflowObjectIds.view_older_jobs_button, JobAppWorkflowObjectIds.job_app_list_view, scrollbar_objectname = JobAppWorkflowObjectIds.job_app_scroll_bar, scrolling_value=0.2, select_option=False)
        self.spice.wait_for(JobAppWorkflowObjectIds.view_older_jobs_button).mouse_click()
        self.spice.wait_for(JobAppWorkflowObjectIds.older_jobs_list)

    def goto_old_job(self, job_id):
        '''
        Go to an old job.

        Scroll down until we find the job in the old jobs list.
        '''
        job = JobAppWorkflowObjectIds.older_job_ui.format(job_id)

        self.spice.wait_for(JobAppWorkflowObjectIds.older_jobs_list)
        self.spice.wait_for(JobAppWorkflowObjectIds.older_jobs_scroll_bar)
        self.workflow_common_operations.goto_item(job, JobAppWorkflowObjectIds.older_jobs_list, scrollbar_objectname = JobAppWorkflowObjectIds.older_jobs_scroll_bar, scrolling_value=0.2, select_option=False)


    def reprint_job(self, net, copies=1):
        '''
        Reprint a job from the job details view.
        '''
        #Make sure we are on the correct view
        self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
        # Check reprint button
        reprint_button_text = self.spice.wait_for(JobAppWorkflowObjectIds.reprint_button_text)
        assert reprint_button_text["text"] == LocalizationHelper.get_string_translation(net, "cReprint", 'en-US')
        # Go to reprint screen
        reprint_button = self.spice.wait_for(JobAppWorkflowObjectIds.reprint_button)
        reprint_button.mouse_click()
        time.sleep(2)
        
        # Set number of copies
        reprint_spin = self.spice.wait_for(JobAppWorkflowObjectIds.reprint_spin)
        reprint_spin["value"] = copies
        
        # Check print button
        reprint_button_confirm_text = self.spice.wait_for(JobAppWorkflowObjectIds.reprint_confirmation_button_text)
        assert reprint_button_confirm_text["text"] == LocalizationHelper.get_string_translation(net, "cPrint", 'en-US')
        # Reprint job
        reprint_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.reprint_confirmation_button)
        reprint_button_confirm.mouse_click()
        time.sleep(2)

    def delete_job(self, net):
        '''
        Delete a job from the job details view.
        '''
        #Make sure we are on the correct view
        self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
        # Check delete button
        delete_button_text = self.spice.wait_for(JobAppWorkflowObjectIds.delete_button_text)
        assert delete_button_text["text"] == LocalizationHelper.get_string_translation(net, "cDeleteJob", 'en-US')

        delete_button = self.spice.wait_for(JobAppWorkflowObjectIds.delete_button)
        delete_button.mouse_click()
        time.sleep(2)

        # Check delete button
        delete_button_confirm_text = self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button_text)
        assert delete_button_confirm_text["text"] == LocalizationHelper.get_string_translation(net, "cDelete", 'en-US')

        # Delete job        
        delete_button_confirm = self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button)
        delete_button_confirm.mouse_click()
        time.sleep(2)

    def cancel_job_through_critical_buttons_bar(self):
        '''
        Cancel a job from the critical buttons bar.
        '''
        # EXPANDABLE CBB: cancel job is the most prioritary buttons: always visible
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_cancel_button)
        cancel_button.mouse_click()

        # Cancel printing only
        cancel_printing_only = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_only_print_button)
        cancel_printing_only.mouse_click()
        
        # Click on "Confirm" button
        confirm_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_yes_button)
        confirm_button.mouse_click()

    def pause_resume_toggle_job_through_critical_buttons_bar(self):
        '''
        Pause or resume (toggle) a job from the critical buttons bar.
        '''
        # EXPANDABLE CBB: pause button is in expandabale CBB gridview
        expandable_button_bar = self.spice.wait_for("#CBB_PANEL")
        if expandable_button_bar["expandableMode"]: #CBB expandableMode==true
            expandable_button_bar_button = self.spice.wait_for("#CBB_BUTTON_EXPANDER")
            expandable_button_bar_button.mouse_click() #Click on CBB button
            time.sleep(0.5) #CBB expand animation 

        # Pause or resume jobs (toggle button)
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_pause_button)
        cancel_button.mouse_click()
        time.sleep(2)

    def click_on_print_job_anyway(self):
        '''
        Click on "Print anyway" button.
        '''
        # Display more options
        more_options_button = self.spice.wait_for(JobAppWorkflowObjectIds.more_options_button)
        more_options_button.mouse_click()
        
        # Print anyway
        print_anyway_button = self.spice.wait_for(JobAppWorkflowObjectIds.print_anyway_button)
        print_anyway_button.mouse_click()

    def click_on_print_job_anyway_directly(self):
        '''
        Click on "Print anyway" button.
        '''
        # Print anyway
        print_anyway_button = self.spice.wait_for(JobAppWorkflowObjectIds.print_anyway_button)
        print_anyway_button.mouse_click()

    def click_on_print_job_anyway_job_details(self):
        '''
        Click on "Print anyway" button in job details view.
        '''
        try:
            # Click on "Options"
            options_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_details_options_button)
            options_button.mouse_click()
        except:
            logging.info("Options button not available")
        
        # Print anyway
        print_anyway_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_details_printanyway_button)
        print_anyway_button.mouse_click()

    def click_on_load_media_job_details(self):
        '''
        Click on "Load media" button in job details view.
        '''
        try:
            # Click on "Options"
            options_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_details_options_button)
            options_button.mouse_click()
        except:
            logging.info("Options button not available")
        
        # Load media
        load_media_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_details_load_button)
        load_media_button.mouse_click()

    def click_on_ok_options_not_available_option_screen(self):
        '''
        Click on "OK" button in job option not available view.
        '''
        # OK
        ok_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_details_load_option_not_available_ok_button)
        ok_button.mouse_click()

    def verify_mismatch_alert(self, net, locale, title, string_id, time_out=60):
        '''Method to verify that a mismatch alert is currently in front of stack view

        Args:
            net (lib): Dune Tuf Library
            locale (lib): Dune Tuf Library
            title (str): string with expect title category
            string_id (str): string id expected in screen
        '''
        hold_screen = self.spice.wait_for(title, timeout=time_out)
        assert str(hold_screen['text']) == str(LocalizationHelper.get_string_translation(net, string_id, locale))

    def mismatch_alert_hold_job(self):
        '''
        On the mismatch alert, click on hold job button
        '''

        button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_hold_button, timeout=15)
        button.mouse_click()

    def mismatch_alert_cancel_job(self):
        '''
        On the mismatch alert, click on cancel job button
        '''

        button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_cancel_button)
        button.mouse_click()

    def mismatch_alert_load_media_job(self):
        '''
        On the mismatch alert, click on load media button
        '''

        button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_load_button)
        button.mouse_click()

    def mismatch_alert_printanyway_job(self):
        '''
        On the mismatch alert, click on print anyway button
        '''

        button = self.spice.wait_for(JobAppWorkflowObjectIds.mismatch_printanyway_button)
        button.mouse_click()

    def get_print_settings_values(self):
        '''
        Get the values from the curing temperature and vacuum spins in settings on the fly
        '''
        return [self.spice.wait_for(JobAppWorkflowObjectIds.curing_temperature_spinbox)["value"], self.spice.wait_for(JobAppWorkflowObjectIds.vacuum_spinbox)["value"]]

    def expand_cbb(self):
        '''
        Expand Critical Buttons Bar
        '''
        expandable_button_bar = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_panel)
        if expandable_button_bar["expandableMode"] == True:
            expandable_button_bar_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_expander)
            expandable_button_bar_button.mouse_click()
            time.sleep(0.5) # CBB expand animation

    def hide_cbb(self):
        expandable_button_bar_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_expander)
        expandable_button_bar_button.mouse_click()
        time.sleep(0.5) # CBB hide animation

    def access_print_settings_through_critical_buttons_bar(self):
        '''
        Expand CBB and click on "Print settings" button
        '''
        self.spice.job_ui.expand_cbb()
        print_settings_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_print_settings_button)
        assert print_settings_button["enabled"] == True,"Print Settings button is disabled"
        print_settings_button.mouse_click()
        current_screen = self.spice.wait_for(JobAppWorkflowObjectIds.print_settings_screen, 60)
        return current_screen

    def dual_cancel_job_through_critical_buttons_bar(self):
        '''
        Cancel both printing and curing from the critical buttons bar.
        '''
        # EXPANDABLE CBB: cancel job is the most prioritary buttons: always visible
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_cancel_button)
        cancel_button.mouse_click()      

        # Click on "Cancel Printing and Curing" button
        cancel_both_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_both_button)
        cancel_both_button.mouse_click()

        # Click on "Confirm" button
        confirm_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_yes_button)
        confirm_button.mouse_click()

    def cancel_curing_through_critical_buttons_bar(self):
        '''
        Cancel curing from the critical buttons bar.
        '''
        # EXPANDABLE CBB: cancel job is the most prioritary buttons: always visible
        # Cancel job
        cancel_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_cancel_button)
        cancel_button.mouse_click()      

        # Click on cancel curing button
        cancel_both_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_curing_job)
        cancel_both_button.mouse_click()

    def statusCenter_open_job_alert(self):
        """
        Performs a mouse_click on the job alert
        """
        self.spice.statusCenter_dashboard_expand()
        jobButton = self.spice.wait_for(JobAppWorkflowObjectIds.notification_center_job_notification)
        jobButton.mouse_click()

    def warm_up_through_critical_buttons_bar(self):
        # EXPANDABLE CBB: warm-up button is in expandabale CBB gridview
        self.spice.job_ui.expand_cbb()
        warm_up_button = self.spice.wait_for(JobAppWorkflowObjectIds.critical_buttons_bar_warm_up_button)
        assert warm_up_button["enabled"] == True, "Warm up button is disabled"
        middle_width = round(warm_up_button["width"] / 2)
        middle_height = round(warm_up_button["height"] / 2)
        warm_up_button.mouse_click(middle_width, middle_height)    

    def cancel_all_jobs(self):
        """
        Cancel all jobs from job queue app
        """
        more_actions_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_button)
        more_actions_button.mouse_click()
        cancel_all_jobs_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_all_jobs_button)
        cancel_all_jobs_button.mouse_click()
        yes_button = self.spice.wait_for(JobAppWorkflowObjectIds.cancel_all_yes_button)
        yes_button.mouse_click()

    def has_lock_icon(self):
        """
        Starting from Home Screen
        """
        self.spice.main_app.scroll_to_find(self.spice.main_app.locators.job_queue_app_button)
        job_app_lock_icon_id = JobAppWorkflowObjectIds.job_app + " #statusIconRect SpiceLottieImageView"
        
        try:
            lock_icon = self.spice.wait_for(job_app_lock_icon_id, 15)
        except:
            logging.info("Failed to find lock icon for Job App")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return lock_icon["visible"] == True

    # Jobs settings

    def goto_menu_jobs_settings(self):
        """
        Helper function to display JobHistoryMoreActionsMenu
        """
        # Click more action "..." button in job history
        more_actions_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_button)
        more_actions_button.mouse_click()
        time.sleep(4)

        # Click Settings button
        jobs_settings_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_jobs_settings_button)
        jobs_settings_button.mouse_click()
        time.sleep(3)

    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        """
        Helper method to indicate if the job settings button in JobHistoryMoreActionsMenu is shown
        UI Should be in Settings menu
        @param spice:
        """
        # Click more action "..." button in job history
        try:
            more_actions_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_button)
        except Exception:
            logging.info("Item '%s' NOT found", JobAppWorkflowObjectIds.job_history_more_actions_button)
            return False

        if not more_actions_button['visible']:
            return False

        more_actions_button.mouse_click()

        time.sleep(4)

        # Click Settings button
        jobs_settings_button = self.spice.query_item(JobAppWorkflowObjectIds.job_history_more_actions_jobs_settings_button)
        is_jobs_settings_menu_shown = jobs_settings_button['visible']

        # Close the screen if close button is found
        try:
            close_button = self.spice.query_item(JobAppWorkflowObjectIds.job_history_jobs_settings_close_button)
            close_button.mouse_click()
        except Exception:
            logging.info('Close button not found')

        time.sleep(2)

        return is_jobs_settings_menu_shown

    def scroll_job_settings_view(self, spice, position:float):
        """
        Helper method to scroll the job settings scroll bar to the indicated position.
        @param spice:
        @param Position: scroll position. Range: [0, 1]
        """
        assert position >= 0.0 and position <= 1.0
        scrollbar = spice.wait_for(JobAppWorkflowObjectIds.job_history_jobs_settings_view_list + "ScrollBar")
        scroll_position = (1.0 - scrollbar["visualSize"]) * position
        scrollbar.__setitem__("position", str(scroll_position))
        spice.wait_until(lambda:abs(scrollbar["position"] - scroll_position) <= 0.01)


    def goto_job_recovery_mode_options(self, spice):
        """
        Helper method to display the menu to select the job recovery policy.
        UI Should be in Jobs Settings menu
        @param spice:
        """
        job_recovery_policy_combo_box = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        job_recovery_policy_combo_box.mouse_click()
        spice.wait_until(lambda:spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode_options_view)["visible"] == True)


    def is_visible_hide_deleted_jobs(self, spice) -> bool:
        """
        Helper method to indicate if hideDeletedJobs is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            hide_deleted_jobs_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
            return hide_deleted_jobs_switch['visible']
        except TimeoutError:
            return False

    def get_hide_deleted_jobs(self, spice) -> bool:
        """
        Helper method to return if hideDeletedJobs is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        hide_deleted_jobs_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        assert hide_deleted_jobs_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        return hide_deleted_jobs_switch["checked"]

    def set_hide_deleted_jobs(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable hideDeletedJobs
        UI Should be in Jobs Settings menu
        @param spice: 
        @param enable: True to enable HoldJob mode False to Disable
        """
        hide_deleted_jobs_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)
        assert hide_deleted_jobs_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_hide_deleted_jobs)

        old_enable = hide_deleted_jobs_switch["checked"]
        if old_enable != enable:
            self.scroll_job_settings_view(spice, 0.0)
            hide_deleted_jobs_switch.mouse_click(x=2, y=2)
            spice.wait_until(lambda:hide_deleted_jobs_switch["checked"] == enable)

        return old_enable


    def is_visible_cancel_jobs_on_hold_delay(self, spice) -> bool:
        """
        Helper method to indicate if cancelJobsOnHoldDelay is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            cancel_jobs_on_hold_spinbox = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
            return cancel_jobs_on_hold_spinbox['visible']
        except TimeoutError:
            return False

    def get_cancel_jobs_on_hold_delay(self, spice) -> int:
        """
        Helper method to return the value of cancelJobsOnHoldDelay
        UI Should be in Jobs Settings menu
        @param spice:
        """
        cancel_jobs_on_hold_spinbox = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        assert cancel_jobs_on_hold_spinbox["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        return cancel_jobs_on_hold_spinbox['value']

    def set_cancel_jobs_on_hold_delay(self, spice, value:int, expected_value:int = None) -> int:
        """
        Helper method to set the new value cancelJobsOnHoldDelay
        UI Should be in Jobs Settings menu
        @param spice: 
        @param enable: True to enable HoldJob mode False to Disable
        """
        cancel_jobs_on_hold_spinbox = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)
        assert cancel_jobs_on_hold_spinbox["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_cancel_jobs_on_hold)

        old_value = cancel_jobs_on_hold_spinbox['value']
        if old_value != value:
            self.scroll_job_settings_view(spice, 0.25)
            cancel_jobs_on_hold_spinbox.__setitem__("value", value)
            spice.wait_until(lambda:cancel_jobs_on_hold_spinbox["value"] == (value if expected_value is None else expected_value))

        return old_value


    def is_visible_job_queue_recovery_mode(self, spice) -> bool:
        """
        Helper method to indicate if jobQueueRecoveryMode is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            job_recovery_policy_combo_box = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
            return job_recovery_policy_combo_box['visible']
        except TimeoutError:
            return False

    def get_job_queue_recovery_mode(self, spice) -> int:
        """
        Helper method to return the current value of jobQueueRecoveryMode
        UI Should be in Jobs Settings menu
        @param spice:
        """
        job_recovery_policy_combo_box = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        assert job_recovery_policy_combo_box["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        return job_recovery_policy_combo_box['currentIndex']
    
    def verify_job_recovery_policy_index(self, spice, index):
        job_recovery_policy_combo_box = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        spice.wait_until(lambda:job_recovery_policy_combo_box["currentIndex"] == index)

    def set_job_queue_recovery_mode(self, spice, value:str) -> int:
        """
        Helper method to set the new value to jobQueueRecoveryMode
        UI Should be in Jobs Settings menu
        @param spice: 
        @param enable: True to enable HoldJob mode False to Disable
        """
        job_recovery_policy_combo_box = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        assert job_recovery_policy_combo_box["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode)

        #self.scroll_job_settings_view(spice, 0.50)
        self.goto_job_recovery_mode_options(spice)

        if value == "putOnHold":
            index = 0
            current_button = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode_put_on_hold)
        elif value == "cancel":
            index = 1
            current_button = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode_cancel)
        else:
            raise Exception(f"Invalid job queue recovery mode <{value}>")

        job_recovery_policy_combo_box_settings = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_job_recovery_mode_settings)
        old_value = job_recovery_policy_combo_box_settings['currentIndex']
        current_button.mouse_click()
        self.verify_job_recovery_policy_index(spice, index)

        return old_value


    def is_visible_job_on_hold_for_manual_release(self, spice) -> bool:
        """
        Helper method to indicate if holdJobForManualRelease is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            jobs_for_manual_release_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
            return jobs_for_manual_release_switch['visible']
        except TimeoutError:
            return False

    def get_job_on_hold_for_manual_release(self, spice) -> bool:
        """
        Helper method to return if holdJobForManualRelease is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        jobs_for_manual_release_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        assert jobs_for_manual_release_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        return jobs_for_manual_release_switch["checked"]

    def set_job_on_hold_for_manual_release(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable holdJobForManualRelease
        UI Should be in Jobs Settings menu
        @param spice: 
        @param enable: True to enable HoldJob mode False to Disable
        """
        jobs_for_manual_release_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)
        assert jobs_for_manual_release_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_hold_jobs_for_manual_release)

        old_enable = jobs_for_manual_release_switch["checked"]
        if old_enable != enable:
            self.scroll_job_settings_view(spice, 0.75)
            jobs_for_manual_release_switch.mouse_click(x=2, y=2)
            spice.wait_until(lambda:jobs_for_manual_release_switch["checked"] == enable)

        return old_enable


    def is_visible_reprint_resend_jobs_enabled(self, spice) -> bool:
        """
        Helper method to indicate if reprintResendJobsEnabled control is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            reprint_resend_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
            return reprint_resend_jobs_enabled_switch['visible']
        except TimeoutError:
            return False

    def get_reprint_resend_jobs_enabled(self, spice) -> bool:
        """
        Helper method to return if reprintResendJobsEnabled is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        reprint_resend_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        assert reprint_resend_jobs_enabled_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        return reprint_resend_jobs_enabled_switch["checked"]

    def set_reprint_resend_jobs_enabled(self, spice, enable:bool, confirm_disabled:bool = False) -> bool:
        """
        Helper method to enable/disable reprintResendJobsEnabled
        UI Should be in Jobs Settings menu
        @param spice: 
        @param enable: True to enable HoldJob mode False to Disable
        """
        reprint_resend_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)
        assert reprint_resend_jobs_enabled_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled)

        old_enable = reprint_resend_jobs_enabled_switch["checked"]
        if old_enable != enable:
            self.scroll_job_settings_view(spice, 1.0)
            reprint_resend_jobs_enabled_switch.mouse_click(x=2, y=2)

            # Answer confirmation dialog if the setting is disabled
            if (enable == False):
                confirmation_dialog = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog)
                spice.wait_until(lambda: confirmation_dialog["visible"] == True, 5)

                button_name = JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog_yes_button \
                    if confirm_disabled else JobAppWorkflowObjectIds.jobs_settings_reprint_resend_jobs_enabled_confirmation_dialog_no_button

                confirmation_dialog = spice.query_item(button_name)
                confirmation_dialog.mouse_click()

                time.sleep(2)

                control_enabled = not confirm_disabled
            else:
                control_enabled = True

            spice.wait_until(lambda:reprint_resend_jobs_enabled_switch["checked"] == control_enabled)

        return old_enable

    def is_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        """
        Helper method to indicate if promoteToInterruptPrintJob control is visible
        UI Should be in Jobs Settings menu
        @param spice:
        """
        try:
            promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
            return promote_to_interrupt_print_jobs_enabled_switch['visible']
        except TimeoutError:
            return False

    def get_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        """
        Helper method to return if promoteToInterruptPrintJob is enabled
        UI Should be in Jobs Settings menu
        @param spice:
        """
        promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
        assert promote_to_interrupt_print_jobs_enabled_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)
        return promote_to_interrupt_print_jobs_enabled_switch["checked"]

    def set_visible_promote_to_interrupt_print_job_enabled(self, spice, enable:bool) -> bool:
        """
        Helper method to enable/disable promoteToInterruptPrintJob
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable promote to interrupt print job False to Disable
        """
        promote_to_interrupt_print_jobs_enabled_switch = spice.wait_for(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled, 5)
        assert promote_to_interrupt_print_jobs_enabled_switch["visible"], "{0} is not visible.".format(JobAppWorkflowObjectIds.jobs_settings_promote_to_interrupt_print_jobs_enabled)

        old_enable = promote_to_interrupt_print_jobs_enabled_switch["checked"]

        if old_enable != enable:
            self.scroll_job_settings_view(spice, 1.0)
            promote_to_interrupt_print_jobs_enabled_switch.mouse_click(x=2,y=2)
            spice.wait_until(lambda:promote_to_interrupt_print_jobs_enabled_switch["checked"] == enable, 15)
            return enable
        
        return old_enable

    def get_job_status_from_status_center(self):
        """
        Purpose: From FPUI, expand status center, get the current job status.
        """
        self.spice.statusCenter_dashboard_expand()
        time.sleep(1)
        status = self.spice.wait_for("#notificationRowDescription #jobStatusCenterText")["text"]
        logging.info(f"The current job status is {status}")
        time.sleep(5)

        self.spice.statusCenter_dashboard_collapse()
        return status

    def goto_job_app_object(self,object_id,parameter):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 180
        found = False
        scroll_step = 0
        
        while found == False and (time_spent_waiting < max_timeout):    
            try:
                job_view = self.spice.wait_for(object_id)
                assert job_view[parameter] == True
                found = True
            except:
                scroll_step = scroll_step + 0.1
                self.workflow_common_operations.scroll_to_position_vertical(scroll_step, JobAppWorkflowObjectIds.job_widget_scroll_bar)
                time_spent_waiting = time.time() - start_time
        assert found
    
    def validate_job_app(self,spice, net):
        logging.info("validating the jobs")
        self.goto_job_app_object(JobAppWorkflowObjectIds.job_app_in_progress_text, "visible")
        assert spice.wait_for(JobAppWorkflowObjectIds.job_app_in_progress_text)["text"] == str(LocalizationHelper.get_string_translation(net,"cInProgressCap", "en"))
        self.goto_job_app_object(JobAppWorkflowObjectIds.job_app_up_next_text, "visible")
        assert spice.wait_for(JobAppWorkflowObjectIds.job_app_up_next_text)["text"] == str(LocalizationHelper.get_string_translation(net,"cUpcomingCap", "en"))
        self.goto_job_app_object(JobAppWorkflowObjectIds.job_app_history_text, "visible")
        assert spice.wait_for(JobAppWorkflowObjectIds.job_app_history_text)["text"] == str(LocalizationHelper.get_string_translation(net,"cHistoryCap", "en"))

    def goto_print_from_jobStorage(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        print_app = self.spice.wait_for(HomeAppWorkflowObjectIds.print_app_button)
        print_app.mouse_click()
        logging.info("At Print App")
        job_storage = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.job_storage)
        job_storage.mouse_click()
        self.spice.wait_for("#JobStorageAppApplicationStackView")
        logging.info("At Job Storage App")

    def goto_menu_jobs_delete_all_jobs_history(self):
        """
        Function to navigate to JobHistoryMoreActionsMenu and click on Delete All Jobs
        Ui Flow: Any screen -> JobHistoryMoreActionsMenu -> Delete All Jobs in History > Confirm and Delete
        @return:
        """
        # Click more action "..." button in job history
        more_actions_button = self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_button)
        more_actions_button.mouse_click()
        assert self.spice.wait_for(JobAppWorkflowObjectIds.delete_all_jobs_button, timeout=30)
        more_actions_button = self.spice.wait_for(JobAppWorkflowObjectIds.delete_all_jobs_button)
        more_actions_button.mouse_click()
        assert self.spice.wait_for(JobAppWorkflowObjectIds.delete_all_jobs_confirmation_button)
        self.spice.wait_for(JobAppWorkflowObjectIds.delete_all_jobs_confirmation_button).mouse_click()
        assert self.spice.wait_for(JobAppWorkflowObjectIds.job_history_more_actions_button, timeout=30)

    def delete_job_ui(self, net):
        '''
        Delete a job from the job details view.
        '''
        #Make sure we are on the correct view
        self.spice.wait_for(JobAppWorkflowObjectIds.job_view)
        #Click on the delete button
        self.spice.wait_for(JobAppWorkflowObjectIds.delete_button).mouse_click()
        assert self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button)
        self.spice.wait_for(JobAppWorkflowObjectIds.delete_confirmation_button).mouse_click()
        job_view = self.spice.wait_for(JobAppWorkflowObjectIds.job_view, timeout=40)
        self.spice.wait_until(lambda:job_view["visible"])
        assert self.spice.wait_for(JobAppWorkflowObjectIds.job_view, timeout=10)
    
    def dismiss_jobapp_exit_Modal(self, pause_job=True):
        '''
        UI should come from scan progress view and be in the modal alert of canceling current job.
        Cancels (or not) the job.
        '''

        self.spice.wait_for("#jobsModalExit")
        if pause_job:
            stay_paused_button = self.spice.wait_for("#stayPausedButton")
            self.spice.validate_button(stay_paused_button)
            stay_paused_button.mouse_click()
        else:
            resume_all_button = self.spice.wait_for("#resumeAllButton")
            self.spice.validate_button(resume_all_button)
            resume_all_button.mouse_click()

    def job_app_exit_with_paused_job(self):
        '''
        UI should be in a Job app with a job paused.
        Dismiss the modal, keeping it paused and goes to the homescreen.
        '''
        home_button = self.spice.wait_for("#HomeButton")
        home_button.mouse_click()

        self.dismiss_jobapp_exit_Modal(pause_job=True)
