import time
import logging
import sys
from time import sleep
from dunetuf.ui.uioperations.BaseOperations.IPrintFromMyhomeAppUIOperations import IPrintFromMyhomeAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromMyhomeAppWorkflowObjectIds import PrintFromMyhomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class PrintFromMyhomeAppWorkflowUICommonOperations(IPrintFromMyhomeAppUIOperations):

    output_scale_standard_sizes_dict = {
        "a0": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a0,
        "a1": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a1,
        "a2": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a2,
        "a3": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a3,
        "a4": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a4,
        "b1": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b1,
        "b2": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b2,
        "b3": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b3,
        "b4": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b4,
        "letter": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_letter,
        "ledger": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ledger,
        "ansi_c": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_c,
        "ansi_d": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_d,
        "ansi_e": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_e,
        "arch_a": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_a,
        "arch_b": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_b,
        "arch_c": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_c,
        "arch_d": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_d,
        "arch_e": PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_e
    }

    def __init__(self, spice):
        """
        PrintFromMyhomeAppUIOperations class to initialize print from myhome options operations.
        @param spice:
        """
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.dial_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        print_app = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_app)
        print_app.mouse_click()
        logging.info("At Print App")

    def check_joblog_from_ui(self, expected_list=[{"index": 2, "expect_value_list": ["Print from My Home Folder", "Success"]}], jobs=None):
        """
        Check the job log from print ui under status menu
        @param expected_list:
        @return:
        """
        logging.info("Check the job log from UI")
        self.spice.goto_homescreen()
        self.homemenu.goto_joblog(self.spice)

        if (jobs == None):
            assert len(expected_list) == 1, "expected_list should be 1"
        else:
            logging.info("Check the job log from cdm")
            time_out = 300
            while len(jobs.get_job_history()) == 0 and time_out:
                time.sleep(1)
                time_out = time_out - 1

            logging.info(f"Check jobs {jobs.get_job_history()}")
            assert len(jobs.get_job_history()) == len(expected_list), "Failed to get all job log"

        for i, item in enumerate(expected_list):
            logging.info(f"Check index {i} and value is {item}")
            if (jobs == None):
                current_job = self.spice.wait_for("#jobListElementTextBlock")
                job_name = current_job["jobName"]
                current_job.mouse_click()
                time.sleep(3)
                job_result = "Success" if self.spice.job_ui.recover_job_status_type() == 0 else "Fail"
            else:
                self.spice.wait_for("#JOB_" + jobs.get_job_history()[i]["jobId"])
                job_name = self.spice.query_item("#JOB_" + jobs.get_job_history()[i]["jobId"] + " #jobListElementTextBlock")["jobName"]
                job_result = "Success" if self.spice.query_item("#JOB_" + jobs.get_job_history()[i]["jobId"] + " #jobListElementTextBlock #gridLayoutView")["completed"] else "Fail"
            logging.info(f"Check job_name {job_name} and job_result is {job_result}")
            assert job_name in item.get("expect_value_list")
            assert job_result in item.get("expect_value_list")

    def check_job_log_from_cdm(self, job, completion_state_list=["success"], time_out=300):
        """
        Check the job from cdm
        make sure invoke function job.bookmark_jobs() before performing a job
        @param job:
        @param completion_state_list:[success, cancelled]
        @param time_out:
        @return:
        """
        logging.info("check the job log from cdm")
        while len(job.get_newjobs()) == 0 and time_out:
            time.sleep(1)
            time_out = time_out - 1

        assert len(job.get_newjobs()) == len(completion_state_list), "Failed to get all job log"

        for i, completion_state in enumerate(completion_state_list):
            logging.info(f"The index {i}，value is {completion_state}")
            actual_status = job.wait_for_job_completion_cdm(job.get_newjobs()[i]["jobId"])
            assert actual_status == completion_state, f"Job status is not correct, expected status should be <{completion_state}>, actual status is <{actual_status}>"

    def goto_print_from_myhome(self):
        """
        Purpose: navigate to Print from Myhome under Print app.
        Ui Flow: Home_Print -> Print from Myhome app(ERROR_MESSAGE/ADDRESSBOOK_STATE/NO_Myhome_FOLDER_CONFIGURED)
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome)
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromMyhome 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        current_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome)
        current_button.mouse_click()

    def check_visible_print_from_myhome(self):
        """
        Purpose: check if Print from Myhome under Print app is visible or not.
        @return: isVisible
        """
        logging.info("[check_visible_print_from_myhome]")
        isVisible = False
        try:
            self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome)
            isVisible = True
        except:
            isVisible = False

        logging.info("[check_visible_print_from_myhome] isVisible={}".format(isVisible))
        return isVisible

    def check_visible_print_from_myhome(self):
        """
        Purpose: check if Print from My Home Folder under Print app is visible or not.
        @return: isVisible
        """
        logging.info("[check_visible_print_from_myhome]")
        isVisible = False
        try:
            self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.icon_print_from_myhome)
            isVisible = True
        except:
            isVisible = False

        logging.info("[check_visible_print_from_myhome] isVisible={}".format(isVisible))
        return isVisible

    def check_spec_on_myhome_print_print_from_myhome_home(self, net, header_text = ""):
        """
        check spec on FOLDER_STRUCTURE of Print From Myhome app.
        @param net:
        @return:
        """
        logging.info("check the FOLDER_STRUCTURE of Print from Myhome")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_landing_view  + " MouseArea", timeout = 120.0)
        logging.info("check the header string of Print from Myhome")
        assert self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_landing_view_header + " #SpiceBreadcrumb #BreadcrumbView #textContainer SpiceText")["text"] == header_text

    def check_spec_on_myhome_print_print_from_myhome(self, net):
        """
        check spec on print button of the FOLDER_STRUCTURE
        @param net:
        @return:
        """
        logging.info("check the string for Print button of the FOLDER_STRUCTURE")

        button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_main
        
        if (self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.expand_button_locator)["visible"] == True):
            button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_main
        elif (self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.collapse_button_locator)["visible"] == True):
            button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_detail

        self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.print_button_str_id, button_locator)

    def goto_options_menu(self):
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator) # representative item in the expected view.
        time.sleep(1)
        self.workflow_common_operations.scroll_to_position_vertical(0.2, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.detail_panel_layout_scrollbar)
        mode_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.options_button_locator)
        mode_button.mouse_click()
        time.sleep(1)

    def close_option_mode(self):
        """
        Close print mode
        @return:
        """
        logging.info("Close print mode")
        close_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.close_option_button_locator)
        close_button.mouse_click()
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator)  # representative item in the expected view.
        time.sleep(1)
    
    def collapse_print_setting(self):
        """
        Collapse print setting
        @return:
        """
        collapse_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.collapse_button_locator)
        collapse_button.mouse_click()
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_landing_view)

    def check_spec_on_usb_print_options(self, net, two_sided=None,color=None, quality=None, paper_selection=None, collate=None):
        """
        Check spec on USBPrint_Options
        @param net:
        @param two_sided:str -> on/off
        @param color:str
        @param quality:str
        @param paper_seleection:dict
        @param collate:str -> on/off
        @return:
        """
        # paper_selection optional parameters
        paper_selection_key_list = ["paper_size", "paper_type", "paper_tray"]
        logging.info("check static spec(Options, 2-Sided, Color, Quality, Paper Selection) on usb print options page")

        wait_pages = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        self.spice.wait_until(lambda: wait_pages["visible"] is True, 20)
        time.sleep(3)
        logging.info(f"paper_selection is {paper_selection}")

        if(two_sided):
            logging.info("check 2sided options spec")
            assert ("on" if self.get_copy_2sided_options_status() else "off") == two_sided
        if(collate):
            logging.info("check collate status spec")
            assert ("on" if self.get_collate_options_status() else "off") == collate
        if(color):
            logging.info("check color options spec")
            self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.option_color_str_id, PrintFromMyhomeAppWorkflowObjectIds.option_color_menu_loctor)
            assert self.get_color_options() == color
        if(quality):
            logging.info("check quality otpions spec")
            self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.option_quality_str_id, PrintFromMyhomeAppWorkflowObjectIds.option_quality_menu_loctor)
            assert self.get_quality_options() == quality
        if(paper_selection['paper_size'] and paper_selection['paper_type'] and paper_selection['paper_tray']):
            self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.option_paperSelection_str_id, PrintFromMyhomeAppWorkflowObjectIds.option_paperSelection_menu_loctor)
            paper_selection_options_list = self.get_paper_selection_options().split(", ")

            actual_paper_selection_dict = dict(zip(paper_selection_key_list,paper_selection_options_list))

            for key, val in paper_selection.items():
                logging.info(f"check paper selection option: {key}")
                assert actual_paper_selection_dict[key.lower()] == val

    def get_copy_2sided_options_status(self):
        """
        Get the option status of 2sided setting
        @return:
        """

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        current_sides_option = self.workflow_common_operations.get_actual_str(PrintFromMyhomeAppWorkflowObjectIds.option_two_sided_button_locator)

        if(current_sides_option == "Select Any"):
            time.sleep(1)
            current_sides_option = self.workflow_common_operations.get_actual_str(PrintFromMyhomeAppWorkflowObjectIds.option_two_sided_button_locator)

        logging.info("Current side settings is: " + current_sides_option)
        if(current_sides_option == "1-Sided"):
            return False
        else:
            return True
        
    def get_collate_options_status(self):
        """
        Get collate option status
        @return:
        """
        logging.info("Get collate option status")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        time.sleep(1)
        is_collate_options_checked = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.options_collate_menu_switch)[PrintFromMyhomeAppWorkflowObjectIds.property_checked]
        logging.info(f"Current collate option is: {is_collate_options_checked}")
        return is_collate_options_checked
    
    def get_quality_options(self):
        """
        Get quality option
        @return:
        """
        logging.info("Get the quality option")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        current_quality_option = self.workflow_common_operations.get_actual_str(PrintFromMyhomeAppWorkflowObjectIds.option_quality_button_locator)
        logging.info("Current quality settings is: " + current_quality_option)
        return current_quality_option
    
    def set_color_options(self, net, color_options="color", locale: str = "en-US"):
        """
        Set the color option
        @param net:
        @param color_options: str -> color/auto/grayscale
        @param locale:
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        color_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_color_button_locator)
        color_item.mouse_click()
        time.sleep(1)

        if color_options == "color":
            gray_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_color_set_color)
            gray_item.mouse_click()
            time.sleep(1)

        if color_options == "grayscale":
            gray_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_color_set_grayscale)
            gray_item.mouse_click()
            time.sleep(1)

        if color_options == "auto":
            gray_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_color_set_auto)
            gray_item.mouse_click()
            time.sleep(1)
    
    def get_color_options(self):
        """
        Get the color option
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        current_color_option = self.workflow_common_operations.get_actual_str(PrintFromMyhomeAppWorkflowObjectIds.option_color_button_locator)
        logging.info("Current color settings is: " + current_color_option)
        return current_color_option

    def goto_color_options_menu(self):
        """
        Go to color option menu
        @return:
        """
        logging.info("Go to color option menu")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_color_menu_loctor)
    
    def get_paper_selection_options(self):
        """
        Get paper selection option
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        current_paper_selection_option = self.get_actual_str_of_value(PrintFromMyhomeAppWorkflowObjectIds.option_paperSelection_menu_loctor)
        logging.info("Current paperSelection settings is: " + current_paper_selection_option)
        return current_paper_selection_option
    
    def get_print_margins_options(self):
        """
        Get print margins option
        @return:
        """
        logging.info("Get the print margins option")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        logging.info(f"To get actual str of " + PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_button_locator)
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_button_locator)

        self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_button_locator + " #contentItem")

        current_print_margins_option = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_button_locator + " #contentItem")["text"]
        logging.info("Current print margins settings is: " + current_print_margins_option)
        return current_print_margins_option
    
    def set_print_margins_options(self, net, print_margins_options="clip_from_contents"):
        """
        Set print margins option
        @param net:
        @param print_margins_options:str -> clip_from_contents/add_to_contents/oversize
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_menu_loctor, PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_button_locator]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromMyhomeAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.options_view_scrollbar )
        time.sleep(1)

        if print_margins_options == "clip_from_contents":
            clip_from_contents_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_set_clip_from_contents)
            clip_from_contents_item.mouse_click()
            time.sleep(1)

        elif print_margins_options == "add_to_contents":
            add_to_contents_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_set_add_to_contents)
            add_to_contents_item.mouse_click()
            time.sleep(1)

        elif print_margins_options == "oversize":
            oversize_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_set_oversize)
            oversize_item.mouse_click()
            time.sleep(1)

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

    def check_spec_on_usb_print_options_print_margins(self, net, print_margins=None):
        """
        Check spec on Print Margins in Print myhome option
        @param net:
        @param print_margins:str -> clip_from_contents/add_to_contents/oversize
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        #self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.print_margins_str_id, PrintFromMyhomeAppWorkflowObjectIds.option_print_margins_menu_loctor)

        if(print_margins):
            logging.info("check print margins options spec")
            assert self.get_print_margins_options() == print_margins
    
    def get_output_scale_options(self):
        """
        Get output scale option
        @return:
        """
        logging.info("Get the output scale option")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        logging.info(f"To get actual str of " + PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_button_locator)
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_button_locator)
        self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_button_locator + " #contentItem")
        current_output_scale_option = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_button_locator + " #contentItem")["text"]
        logging.info("Current output scale settings is: " + current_output_scale_option)
        return current_output_scale_option
    
    def set_output_scale_options(self, net, configuration, output_scale_options="none", detail_option=None):
        """
        Set print output scale option
        @param net:
        @param output_scale_options:str -> none/custom/loaded_paper/standard_sizes
        @param detail_option:
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_menu_loctor]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromMyhomeAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.options_view_scrollbar )

        self.homemenu.menu_navigation(self.spice,PrintFromMyhomeAppWorkflowObjectIds.view_optionView, PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_menu_loctor, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.options_view_scrollbar)
        
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_none)

        if output_scale_options == "none":
            none_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_none)
            none_item.mouse_click()

        elif output_scale_options == "custom":
            custom_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom)
            custom_item.mouse_click()
            if detail_option:
                custom_value = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom_spin_box)["value"] - detail_option
                if custom_value > 0:
                    custom_down = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom_spin_box + " " + PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom_spin_box_minus_locator)
                    for i in range(0, custom_value):
                        custom_down.mouse_click()
                        time.sleep(0.1)
                else:
                    custom_up = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom_spin_box + " " + PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_custom_spin_box_plus_locator)
                    for i in range(0, abs(custom_value)):
                        custom_up.mouse_click()
                        time.sleep(0.1)

        elif output_scale_options == "loaded_paper":
            loaded_paper_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper)
            loaded_paper_item.mouse_click()
            if detail_option:
                detail_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail)
                detail_item.mouse_click()
                if configuration.productname == "jupiter" :
                    self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll1)

                    if detail_option == "roll1":
                        roll_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll1)
                        roll_item.mouse_click()
                    elif detail_option == "roll2":
                        tray_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll2)
                        tray_item.mouse_click()
                    
                elif configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
                    self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll)
                
                    if detail_option == "roll":
                        roll_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll)
                        roll_item.mouse_click()
                    elif detail_option == "tray":
                        tray_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_tray)
                        tray_item.mouse_click()

        elif output_scale_options == "standard_sizes":
            standard_sizes_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes)
            standard_sizes_item.mouse_click()
            if detail_option:
                detail_item = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail)
                detail_item.mouse_click()
                self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a0)
                detail_option_id = self.output_scale_standard_sizes_dict.get(detail_option)

                self.workflow_common_operations.goto_item(detail_option_id, PrintFromMyhomeAppWorkflowObjectIds.standard_sizes_optionView, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.standard_sizes_scrollbar)

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.option_output_scale_view + " #BackButton").mouse_click()
        next_view = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        self.spice.wait_until(lambda: next_view["visible"] == True, 20)

    def check_spec_on_myhome_print_options_output_scale(self, net, output_scale=None):
        """
        Check spec on Output Scale in print myhome option
        @param net:
        @param output_scale:str -> none/...
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.options_view)
        time.sleep(1)

        if(output_scale):
            logging.info("check output scale options spec")
            assert self.get_output_scale_options() == output_scale

    def check_spec_on_print_from_myhome_not_configuration_view(self, net):
        """
        Check Print from Myhome not configuration view.
        @param net:
        @return:
        """
        logging.info("Check spec on Print from Myhome not configured view")

        logging.info("verify the modal messages")
        self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.myhome_not_configure_message_str_id, PrintFromMyhomeAppWorkflowObjectIds.myhome_not_configure_message)

        logging.info("verify the ok button messages")
        self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.myhome_not_configure_ok_button_str_id, PrintFromMyhomeAppWorkflowObjectIds.myhome_not_configure_ok_button)

    def select_print_from_myhome_not_configuration_ok_button(self):
        """
        Select Print from Myhome not configuration ok button
        @param:
        @return:
        """
        logging.info("Press the Ok button")
        ok_button = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.myhome_not_configure_ok_button)
        ok_button.mouse_click()

    def wait_for_connecting_screen(self):
        """
        wait for connecting screen
        @return:
        """
        logging.info("check the connecting view screen")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.connecting_progress_locator)

    def select_print_file_or_folder_by_name(self, name: str, dial_value: int = 180):
        """
        UI should be in FOLDER_STRUCTURE of print from Myhome.
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        logging.info("Wait_For print_myhome_folder_landing_view")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_landing_view  + " MouseArea", timeout = 60.0)
        logging.info("Wait_For  print_myhome_folder_grid_view")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view + " MouseArea")
        
        logging.info("Wait_For name")
        self.spice.wait_for("#"+name, timeout = 20.0)

        ##move scrollbar to postion 0
        scrollbar = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view_verticalscroll)
        scrollbar.__setitem__("position", "0")
        
        rowObjectY = self.spice.query_item(f"#{name}")["y"]
        if (rowObjectY != 0):
            assert self.spice.query_item( PrintFromMyhomeAppWorkflowObjectIds.view_print_myhome_folder_grid_view)["contentHeight"] != 0
            contentHeight = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.view_print_myhome_folder_grid_view)["contentHeight"]
            stepValue = rowObjectY / contentHeight
            self.workflow_common_operations.scroll_to_position_vertical(stepValue, scrollbar_objectname = PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view_verticalscroll)
        
        logging.info("goto_item_navigation")
        self.workflow_common_operations.goto_item_navigation(f"#{name}", PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view)

    def get_value_of_no_of_copies(self):
        """
        Get the copy number
        @return: int
        """
        expend_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator)
        current_value = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator)["value"]
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        expend_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.collapse_button_locator)
        expend_button.mouse_click()
        time.sleep(1)
        return current_value

    def set_no_of_copies(self, value):
        """
        Set number of pages in detail panel of Print Myhome app 
        @param value:
        @return:
        """
        # open expand buttor to show "Copies"
        expend_button = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator)
        numCopiesElement = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.numberOfCopies_locator)
        numCopiesElement.__setitem__('value', value)

    def start_print(self):
        """
        UI should be in FOLDER_STRUCTURE of print from Myhome.
        Navigates to Side screen starting from FOLDER_STRUCTURE.
        UI Flow is click on print button
        @return:
        """
        time.sleep(3) # make sure can click print button
        # sometimes cannot click print button
        button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_main
        
        if (self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.expand_button_locator)["visible"] == True):
            button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_main
        elif (self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.collapse_button_locator)["visible"] == True):
            button_locator = PrintFromMyhomeAppWorkflowObjectIds.print_button_locator_footer_detail

        for _ in range(5):
            self.spice.wait_for(button_locator).mouse_wheel(0, 0)
        
        self.workflow_common_operations.goto_item_navigation(button_locator, PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_landing_view)
        logging.info("Click the print button to start printing")

    def wait_for_downloading_screen(self):
        """
        wait for downloading screen
        @return:
        """
        logging.info("check the downloading view screen")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_locator)

    def wait_for_downloading_screen_completed(self):
        """
        wait for downloading screen completed
        @return:
        """
        logging.info("wait the downloading view screen completed")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_locator)

        num = 0
        while num < 95:
            progressBarDetail = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_locator + " " + PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_bar + " #progressBarDetail")
            str_progressBarDetail = str(progressBarDetail["text"])
            loc_percent = str_progressBarDetail.find('%', 0)
            num_str = str_progressBarDetail[0:loc_percent]
            num = int(str(num_str))

        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_locator)

    def press_cancel_button_from_downloading_screen(self):
        """
        press for downloading screen completed
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.downloading_progress_locator)

        cancel_button = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.downloading_cancel_button)
        cancel_button.mouse_click()

    def wait_for_print_status_toast(self, net, message: str = "complete", timeout=60, specific_str_checked=False):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: str, starting /printing /complete/canceled
              timeout:
              specific_str_checked: 1. True, strings containing special characters should equal to toast message/False, just need to judge that the string is included in the toast message.
                                    2. Just to check the corresponding status, please using with False/Need to check its screen expected str, please using True
        @return:
        """
        status = False

        if message == "starting":
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintFromMyhomeAppWorkflowObjectIds.toast_message_starting)
            print_toast_specific_message = print_toast_message_from_id + "..."
        elif message == 'printing':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintFromMyhomeAppWorkflowObjectIds.toast_message_printing)
            print_toast_specific_message = print_toast_message_from_id + "..."
        elif message == 'complete':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintFromMyhomeAppWorkflowObjectIds.toast_message_completed)
            print_toast_specific_message= print_toast_message_from_id
        elif message == 'canceled':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintFromMyhomeAppWorkflowObjectIds.toast_message_canceled)
            print_toast_specific_message= print_toast_message_from_id

        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                toast_message = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.toast_message_text)["text"]
                logging.info("Current Toast message is : %s" % toast_message)
                
            except:
                logging.info("Still finding corresponding status.")
            if specific_str_checked:
                if print_toast_specific_message == toast_message:
                    status = True
                    break
            else:
                if print_toast_message_from_id in toast_message:
                    status = True
                    break

        if not status:
            raise Exception(f"Timeout to find print status <{message}>")
        

    def press_back_button(self, index = 1):
        assert self.spice.query_item("#BackButton", index)["visible"] == True
        self.spice.query_item("#BackButton", index).mouse_click()

    def goto_sort_filter_search_options_menu(self):
        """
        Go to sort filter search options menu.
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_app_view)
        more_options_btn = self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_more_options_button)
        more_options_btn.mouse_click()

    def select_sort_filter_search_option(self, option:str):
        """
        Select corresponding option
        @param:option sort/filter/search
        @return:
        """
        options_dict = {
            "sort": PrintFromMyhomeAppWorkflowObjectIds.option_sort,
            "filter": PrintFromMyhomeAppWorkflowObjectIds.option_filter,
            "search": PrintFromMyhomeAppWorkflowObjectIds.option_search
        }
        selected_opt = self.spice.wait_for(options_dict[option])
        selected_opt.mouse_click()
        time.sleep(2)

    def select_specific_filter_option(self, option:str):
        """
        Select filter option in filter screen.
        @param:option all_file_types/jpeg/png/tiff/pdf/ppt/doc/ps
        @return:
        """
        filter_options_dict = {
            "all_file_types": PrintFromMyhomeAppWorkflowObjectIds.filter_option_all_file_type,
            "jpeg": PrintFromMyhomeAppWorkflowObjectIds.filter_option_jpeg,
            "tiff": PrintFromMyhomeAppWorkflowObjectIds.filter_option_tiff,
            "pdf":PrintFromMyhomeAppWorkflowObjectIds.filter_option_pdf,
            "ppt":PrintFromMyhomeAppWorkflowObjectIds.filter_option_ppt,
            "doc":PrintFromMyhomeAppWorkflowObjectIds.filter_option_doc,
            "ps":PrintFromMyhomeAppWorkflowObjectIds.filter_option_ps
        }
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_filter_view)
        # update method to scroll_item_into_view while scroll_item_into_view method merge into 24s branch.
        # self.scroll_item_into_view(PrintFromUsbAppWorkflowObjectIds.filter_list_view, PrintFromUsbAppWorkflowObjectIds.filter_list_view_scroll_bar, filter_options_dict[option], shifting=True)
        
        filter_item = self.spice.wait_for(filter_options_dict[option] + " " + PrintFromMyhomeAppWorkflowObjectIds.button_radio_button)
        filter_item.mouse_click()

    def click_save_button_on_filter_screen(self):
        """
        Click save button in filter screen.
        @return:
        """
        save_button = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.save_button_filter_screen)
        save_button.mouse_click()

    def check_file_names_in_folder_list_view(self, expected_file_list):
        """
        Check expect files shows in folder list view screen.
        @param:expected_file_list:
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view)
        time.sleep(2)
        scrollbar = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view_verticalscroll)
        scrollbarSize = scrollbar['size']
        scrollPosition = 0
        scrollbar["position"] = scrollPosition

        time.sleep(1)
        not_found_file_list = []
        for file_name in expected_file_list:
            try:
                self.spice.wait_for(f"#{file_name}", timeout=0.2)
                logging.info(f"-found:{file_name}")
            except:
                not_found_file_list.append(file_name)

        #scroll down to find files
        while scrollPosition + 0.5 * scrollbarSize < 1:
            scrollPosition = scrollPosition + 0.5 * scrollbarSize
            self.workflow_common_operations.scroll_to_position_vertical(scrollPosition, PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view_verticalscroll)
            time.sleep(2)    
            for file_name in not_found_file_list[:]:
                try:
                    self.spice.wait_for(f"#{file_name}", timeout=0.2)
                    logging.info(f"-found:{file_name}")
                    not_found_file_list.remove(file_name)
                except:
                    logging.info(f"not found: {file_name}, will find next scroll")

        assert len(not_found_file_list) == 0 , "not found files"
        logging.info(f"Check file name list {expected_file_list} success")
    
    def check_search_result_number_in_folder_list_view(self, expected_file_list):
        """
        Check Search Result numbers shows in folder list view screen.
        @param:expected_file_list: 
        @return:
        """
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.print_myhome_folder_grid_view)
        result_message = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.search_result_message_locator, 15)["text"]
        result_number = result_message.split("+")[0]
        assert len(expected_file_list) == int(result_number), "Search result numbers is error"

    def input_search_text_in_search_screen(self, search_text):
        """
        Input search text in search screen.
        @param:search_text: str
        @return:
        """
        logging.info("wait for Search screen")
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.view_print_myhome_search_view)
        search_input_view = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.search_text_field_locator)
        search_input_view.mouse_click()
        search_input_view.__setitem__('displayText', search_text)
        self.spice.query_item(PrintFromMyhomeAppWorkflowObjectIds.ok_button_keyboard).mouse_click()

    def click_search_button_in_search_screen(self):
        """
        Click search button in search screen.
        @return:
        """
        search_button = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.search_button_locator)
        search_button.mouse_click()

    def select_specific_sort_option(self, option:str):
        """
        Select sort option
        @param:option AtoZ/ZtoA/OldToNew/NewToOld
        @return:
        """
        sort_options_dict = {
            "AtoZ": PrintFromMyhomeAppWorkflowObjectIds.sort_option_a_to_z,
            "ZtoA": PrintFromMyhomeAppWorkflowObjectIds.sort_option_z_to_a,
            "OldToNew": PrintFromMyhomeAppWorkflowObjectIds.sort_option_old_to_new,
            "NewToOld":PrintFromMyhomeAppWorkflowObjectIds.sort_option_new_to_old,
        }
        # update method to scroll_item_into_view while scroll_item_into_view method merge into 24s branch.
        # self.scroll_item_into_view("#sortList", "#sortListScrollBar", sort_options_dict[option], shifting=True)
        
        #if option == "OldToNew" or option == "NewToOld":
        #    self.workflow_common_operations.scroll_to_position_vertical(0.4, "#sortListScrollBar")
        
        sort_button = self.spice.wait_for(sort_options_dict[option] + " " + PrintFromMyhomeAppWorkflowObjectIds.button_radio_button)
        sort_button.mouse_click()
    
    def click_save_button_on_sort_screen(self):
        """
        Click save button in sort screen.
        @return:
        """
        save_button = self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.save_button_sort_screen)
        save_button.mouse_click()

    def check_cartridge_very_low_screen(self, net, locale: str = "en-US"):
        self.workflow_common_operations.verify_string(net, PrintFromMyhomeAppWorkflowObjectIds.cartridge_very_low_str_id, PrintFromMyhomeAppWorkflowObjectIds.cartridge_very_low_locator, locale, isSpiceText=True)
    
    def select_quickset(self, quick_name):
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.detail_panel_layout)
        quickset_button = self.spice.wait_for("#" + quick_name)
        quickset_button.mouse_click()

    def verify_selected_quickset(self, quick_name):
        self.spice.wait_for(PrintFromMyhomeAppWorkflowObjectIds.detail_panel_layout)
        assert self.spice.query_item("#" + quick_name)["checked"] == True
