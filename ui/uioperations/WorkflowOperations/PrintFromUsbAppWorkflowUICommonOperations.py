import time
from dunetuf.ui.uioperations.BaseOperations.IPrintFromUsbAppUIOperations import IPrintFromUsbAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
import logging
import sys
from dunetuf.cdm import CDM

class PrintFromUsbAppWorkflowUICommonOperations(IPrintFromUsbAppUIOperations):

    paper_size_dict_str_id = {
        "custom": "cCustom",
        "a4_210x297_mm": "cMediaSizeIdA4",
        "iso_a4_210x297mm" : "cMediaSizeIdA4",
        "letter_8_5x11_in": "cMediaSizeIdLetter"
    }

    paper_type_dict_str_id = {
        "plain": "cMediaTypeIdPlain"
    }

    paper_tray_dict_str_id = {
        "automatic": "cAutomatic",
        "tray": "cTray",
        "tray1": "cMediaInputIdTray1",
        "tray2": "cMediaInputIdTray2",
        "tray3": "cMediaInputIdTray3"
    }

    paper_size_dict = {
        "envelope_a2": "#MenuValuea2Envelope",
        "custom": "#customprintFromUSB_paperSize",
        "a0": "#MenuValueiso_a0_841x1189mm",
        "a1": "#MenuValueiso_a1_594x841mm",
        "a2": "#MenuValueiso_a2_420x594mm",
        "a3_297x420_mm": "#MenuValueiso_a3_297x420mm",
        "a4_210x297_mm": "#iso_a4_210x297mmprintFromUSB_paperSize",
        "iso_a4_210x297mm":"#iso_a4_210x297mmprintFromUSB_paperSize",
        "a5_148x210_mm": "#iso_a5_148x210mmprintFromUSB_paperSize",
        "a6_105x148_mm": "#iso_a6_105x148mmprintFromUSB_paperSize",
        "b2": "#MenuValueiso_b2_500x707mm",
        "b3": "#MenuValueiso_b3_353x500mm",
        "b4_jis_257x364mm": "#MenuValueiso_b4_250x253mm",
        "envelop_b5_176x250mm": "#iso_b5_176x250mmprintFromUSB_paperSize",
        "envelope_c5_162x229mm": "#iso_c5_162x229mmprintFromUSB_paperSize",
        "envelope_c6_114x162mm": "#MenuValueiso_c6_114_162mm",
        "envelope_dl_110x220mm": "#iso_dl_110x220mmprintFromUSB_paperSize",
        "b5_jis_182x257mm": "#jis_b5_182x257mmprintFromUSB_paperSize",
        "b6_jis_128x182mm": "#jis_b6_128x182mmprintFromUSB_paperSize",
        "japanese_envelope_chou_#3_120x235mm": "#MenuValuejpn_chou3_120x235mm",
        "postcard_jis_100x148mm": "#jpn_hagaki_100x148mmprintFromUSB_paperSize",
        "double_postcard_jis_148x200mm": "#jpn_oufuku_148x200mmprintFromUSB_paperSize",
        "execuitive_7_25x10_5_in": "#na_executive_7_dot_25x10_dot_5inprintFromUSB_paperSize",
        "oficio_8_5x13_in": "#na_foolscap_8_dot_5x13inprintFromUSB_paperSize",
        "letter_8inx10in": "#MenuValuena_govt_letter_8x10in",
        "3x5_in": "#MenuValuena_index_3x5_3x5in",
        "4x6_in": "#na_index_dash_4x6_4x6inprintFromUSB_paperSize",
        "5x7_in": "#MenuValuena_index_5x7_5x7in",
        "5x8_in": "#na_index_dash_5x8_5x8inprintFromUSB_paperSize",
        "ledger_11x17_in": "#MenuValuena_ledger_11x17in",
        "legal_8_5x14_in": "#na_legal_8_dot_5x14inprintFromUSB_paperSize",
        "letter_8_5x11_in": "#na_letter_8_dot_5x11inprintFromUSB_paperSize",  
        "envelope_monarch_3_9x7_5_in": "#na_monarch_3_dot_875x7_dot_5inprintFromUSB_paperSize",
        "envelope_#10_4_1x9_5_in": "#na_number_dash_10_4_dot_125x9_dot_5inprintFromUSB_paperSize",
        "oficio_216x340_mm": "#na_oficio_8_dot_5x13_dot_4inprintFromUSB_paperSize",
        "10x15cm": "#om_small_dash_photo_100x150mmprintFromUSB_paperSize",
        "16k_184x260mm": "#om_16k_184x260mmprintFromUSB_paperSize",
        "16k_195x270mm": "#om_16k_195x270mmprintFromUSB_paperSize",
        "16k_197x273mm": "#roc_16k_7_dot_75x10_dot_75inprintFromUSB_paperSize"
    }

    paper_tray_dict = {
        "tray1": "#MenuValuetray_dash_1",
        "tray2": "#MenuValuetray_dash_2",
        "tray3": "#MenuValuetray_dash_3",
        "automatic": "#auto_printFromUSB_paperTray",
        "tray": "#mainprintFromUSB_paperTray",
        "sheet": "#topprintFromUSB_paperTray",
        "roll1": "#ComboBoxOptionsroll_dash_1",
        "roll2": "#ComboBoxOptionsroll_dash_2",
        "roll": "#ComboBoxOptionsmain_dash_roll",
    }

    paper_type_dict = {
        "plain": "#stationeryprintFromUSB_paperType",
        "custom": "#customprintFromUSB_paperType",
        "label": "#labelsprintFromUSB_paperType",
        "envelope": "#envelopeprintFromUSB_paperType",
        "prepunched": "#prepunchedprintFromUSB_paperType",
        "UserType10": "#com_dot_hp_dot_usertype_dash_10_paperType"
    }

    def __init__(self, spice):
        """
        PrintFromUsbAppUIOperations class to initialize print from usb options operations.
        @param spice:
        """
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.dial_common_operations = spice.basic_common_operations
        self.homemenu =  spice.menu_operations

        self.print_usb_app_view = PrintFromUsbAppWorkflowObjectIds.print_usb_app_view
        self.options_view = PrintFromUsbAppWorkflowObjectIds.options_view
        self.print_settings_view = PrintFromUsbAppWorkflowObjectIds.print_button_locator
        self.paper_selection_settings_view = PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor
        self.select_file_view = PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view
    
    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.goto_home_print_app()
        logging.info("At Print App")
    
    def goto_home_print_app(self):
        """
        Function to navigate to Print app on home screen 
        Ui Flow: Home screen->menu -> Print app
        @return:
        """
        self.spice.home_operations.goto_home_print_app()
        self.spice.wait_for(HomeAppWorkflowObjectIds.view_print)
        
        assert self.spice.wait_for(HomeAppWorkflowObjectIds.view_print)['text'] == 'Print'
        logging.info("At Print App Screen")
    
    def goto_print_app_from_menu(self):
        """
        Function to navigate to Print app on home screen from menu
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.spice.home_operations.goto_home_menu()
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        scan_app = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_app)
        scan_app.mouse_click()
        logging.info("At Print from Usb App")
    


    def check_joblog_from_ui(self, expected_list=[{"index": 2, "expect_value_list": ["Print from USB", "Success"]}], jobs=None):
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
                current_job = self.spice.wait_for("#JobQueueAppApplicationStackView #jobListElementTextBlock")
                job_name = current_job["jobName"]
                time.sleep(3)
                scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.job_status_scrollbar)
                scrollbar.__setitem__("position",0.4)
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

    def goto_print_from_usb(self):
        """
        Purpose: navigate to Print from USB under Print app.
        Ui Flow: Home_Print -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromUsb 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        #self.workflow_common_operations.scroll_position(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb , PrintFromUsbAppWorkflowObjectIds.scrollBar_printFolderPage , PrintFromUsbAppWorkflowObjectIds.printFolderPage_column_name  , PrintFromUsbAppWorkflowObjectIds.printFolderPage_Content_Item)
        current_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
        current_button.mouse_click()
        # Wait for usb drive screen
        # self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, timeout=9.0) #TBD
    
    def goto_print_from_usb_menu(self):
        """
        Purpose: navigate to Print from USB under Print app.
        Ui Flow: Home_Print -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb + " MouseArea")
        current_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb + " MouseArea")
        current_button.mouse_click()
    
    def check_visible_print_from_usb(self):
        """
        Purpose: check if Print from USB under Print app is visible or not.
        Ui Flow: Home_Print -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return: isVisible
        """
        logging.info("[check_visible_print_from_usb]")
        isVisible = False
        try:
            self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_from_usb)
            isVisible = True
        except:
            isVisible = False

        logging.info("[check_visible_print_from_usb] isVisible={}".format(isVisible))
        return isVisible

    def check_spec_on_usb_print_print_from_usb_home(self, net):
        """
        check spec on USBPrint_PrintFromUSBHome
        @param net:
        @return:
        """
        logging.info("check the str on USBPrint_PrintFromUSBHome screen")

        logging.info("check the string for Print from USB")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.header_print_from_usb_str_id,
                                                  PrintFromUsbAppWorkflowObjectIds.print_from_usb)
        # todo: search/filter feature is not yet implemented.

    def check_spec_on_usb_print_print_from_usb_homescreen(self, net):
        """
        check spec on USBPrint_PrintFromUSBHome
        @param net:
        @return:
        """
        logging.info("check the str on USBPrint_PrintFromUSBHome screen")

        logging.info("check the string for Print from USB")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.header_print_from_usb_str_id,
                                                  PrintFromUsbAppWorkflowObjectIds.print_from_usb)

    def validateListObjectVisibility(self, listView, targetItem):        
        rowObjectY = targetItem["y"]
        rowObjectHeight = targetItem["height"]
        contentYOfListObj = listView["contentY"]
        heightOfListObj = listView["height"]
        return (rowObjectY >= contentYOfListObj and rowObjectY <= heightOfListObj + contentYOfListObj - rowObjectHeight)
    
    def find_print_file_or_folder_by_name(self, file_name: str):
        """
        find expect file shows in folder list view screen.
        @param:file_name:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        listView = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_usb_folder_list_view)
        try:
            targetItem = self.spice.wait_for(f"#{file_name}", timeout=0.2)
            isVisible = self.validateListObjectVisibility(listView, targetItem)
            if isVisible:
                return
        except:
            logging.info("search failed: try to scroll")

        time.sleep(3)
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
        scrollbarSize = scrollbar['size']
        scrollPosition = 0
        scrollbar["position"] = scrollPosition
        #scroll down to find files
        
        while scrollPosition + 0.5 * scrollbarSize < 1:
            try:
                targetItem = self.spice.wait_for(f"#{file_name}", timeout=0.2)
                isVisible = self.validateListObjectVisibility(listView, targetItem)
                if isVisible:
                    return
                logging.info("expected file is not in screen")
            except:
                logging.info("search failed: try to scroll")
            scrollPosition = scrollPosition + 0.5 * scrollbarSize
            scrollbar["position"] = scrollPosition
        assert self.spice.wait_for(f"#{file_name}", timeout=20), "search failed"
        
    def select_print_file_or_folder_by_name(self, name: str, dial_value: int = 180):
        """
        UI should be in USBPrint_PrintFromUSBHome.
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view, timeout = 20.0)
        logging.info("Wait_For  print_usb_folder_list_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        logging.info("Wait_For name")
        self.find_print_file_or_folder_by_name(name)
        
        logging.info("goto_item_navigation")
        self.spice.query_item(f"#{name}").mouse_click()
    
    def check_print_file_is_selected(self, name:str):
        """
        check print file is selected since select print file by name
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        logging.info("Wait For file name")
        self.spice.wait_for(f"#{name}")
        assert self.spice.query_item(f"#{name}")["focus"] == True, "select print file or folder failed"
        
    def check_spec_on_usb_print_print_from_usb(self, net):
        """
        check spec on USBPrint_PrintFromUSB
        @param net:
        @return:
        """
        logging.info("check the str on USBPrint_PrintFromUSB screen")

        logging.info("check the string for Print button")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.print_button_str_id, PrintFromUsbAppWorkflowObjectIds.print_button_locator)

        #logging.info("check the string for Options button")
        #self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.options_button_str_id, PrintFromUsbAppWorkflowObjectIds.options_button_locator)
        
    def get_value_of_no_of_copies(self):
        """
        Get the copy number
        @return: int
        """
        expend_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)
        current_value = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)["value"]
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        expend_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.collapse_button_locator)
        expend_button.mouse_click()
        time.sleep(1)
        return current_value

    def set_no_of_copies(self, value):
        """
        Selects number of pages in USBPrint_PrintFromUSB screen based on user input
        @param value:
        @return:
        """
        # open expand buttor to show "Copies"
        expend_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()

        numCopiesElement = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)
        numCopiesElement.__setitem__('value', value)

    def start_print(self, dial_value=0):
        """
        UI should be in USBPrint_PrintFromUSB.
        Navigates to Side screen starting from USBPrint_PrintFromUSB.
        UI Flow is click on print button
        @param dial_value:
        @return:
        """
        time.sleep(3) # make sure can click print button
        # sometimes cannot click print button
        button_locator = PrintFromUsbAppWorkflowObjectIds.print_button_locator
        
        if (self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)["visible"] == True):
            button_locator = PrintFromUsbAppWorkflowObjectIds.print_button_locator
        elif (self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.collapse_button_locator)["visible"] == True):
            button_locator = PrintFromUsbAppWorkflowObjectIds.footer_detail_print_button_locator

        for _ in range(5):
            self.spice.wait_for(button_locator).mouse_wheel(0, 0)
        
        self.workflow_common_operations.goto_item_navigation(button_locator, PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)
        logging.info("Click the print button to start printing")

    def wait_for_print_status(self, net, job, message: str = "complete", timeout=300, specific_str_checked=False):
        if job.job_concurrency_supported == "true":
            self.wait_for_print_status_toast(net, message, timeout, specific_str_checked)
        else:
            self.wait_for_print_status_modal(net, message, timeout)

    def wait_for_print_status_toast(self, net, message: str = "complete", timeout=300, specific_str_checked=False, wait_for_toast_dismiss=False):
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
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
            print_toast_specific_message = print_toast_message_from_id + "..."
        elif message == 'printing':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cPermissionPrintingApp')
            print_toast_specific_message = print_toast_message_from_id + "..."
        elif message == 'complete':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cPrintingCompleteMessage')
            print_toast_specific_message= print_toast_message_from_id
        elif message == 'canceled':
            print_toast_message_from_id = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cPrintCanceled')
            print_toast_specific_message= print_toast_message_from_id

        start_time = time.time()
        while time.time()-start_time < timeout:
            try:
                toast_message = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.toast_message_text + "")["text"]
                logging.info("Current Toast message is : %s" % toast_message)
                
            except:
                logging.info("Still finding corresponding status.")
                toast_message = "Did not catch"
            if specific_str_checked:
                if print_toast_specific_message == toast_message:
                    status = True
                    break
            else:
                if print_toast_message_from_id in toast_message:
                    status = True
                    break

        if not status:
            raise Exception(f"Timeout <{timeout}> to find print status <{message}>")

        if wait_for_toast_dismiss:
            start_time = time.time()
            while time.time()-start_time < timeout:
                try:
                    toast_message = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.toast_message_text + "")["text"]
                    logging.info(f"Still corresponding toast message <{toast_message}> display in screen")
                except Exception as err:
                    logging.info("Toast screen already dismiss")
                    break

    def wait_for_print_status_modal(self, net, message: str = "complete", timeout=300):
        """
        Purpose: Wait for the given modal message to appear in screen and success if given modal appears
        Args: message: str, printing / Print successfully
              timeout
        @return:
        """
        if message == "starting":
            click_ok_button = False
            targetViewType = "jobModalProgress"
        elif message == "printing":
            click_ok_button = False
            targetViewType = "jobModalProgress"
        elif message == "complete":
            click_ok_button = True
            targetViewType = "jobModalCompletion"
        elif message == "canceled":
            click_ok_button = True
            targetViewType = "jobModalCompletion"

        started = time.time()
        while True:
            if time.time() - started > timeout:
                raise TimeoutError(
                    "Status matching '{}' not found within {:.2f}s".format(
                        targetViewType, timeout
                    )
                )
            
            if targetViewType == "jobModalCompletion":
                if (self.spice.wait_for("#ActiveJobModalView #okButton")["visible"] == True):
                    break
            elif targetViewType == self.spice.wait_for("#ActiveJobModalView")["viewType"]:
                break
            else:
                time.sleep(0.1)
        
        if click_ok_button:
            ok_button = self.spice.query_item("#okButton")
            ok_button.mouse_click()

    def check_spec_on_usb_print_file(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def goto_options_menu(self):
        expend_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator) # representative item in the expected view.
        time.sleep(1)
        scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.detail_panel_layout_scrollbar
        scrollbar_size = self.spice.query_item(scrollbar_objectname)["size"]
        self.workflow_common_operations.scroll_to_position_vertical(1 - scrollbar_size, scrollbar_objectname)
        mode_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_button_locator)
        mode_button.mouse_click()
        time.sleep(1)

    def goto_interactive_summary(self):
        expend_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()
        wait_pages = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator) # representative item in the expected view.
        self.spice.wait_until(lambda: wait_pages["visible"] == True, 20)

    def check_quickset(self, title):
        expend_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.expand_button_locator)
        expend_button.mouse_click()
        time.sleep(1)
        
        quicksetItem = self.spice.wait_for(f"#{title}")
        quicksetItem.mouse_click()
        
        assert quicksetItem["focus"] == True, "select quickset failed"

    def goto_expand_screen_to_options_menu(self):
        detail_panel_layout = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.detail_panel_layout)
        detail_panel_layout.mouse_wheel(0,-360)
        mode_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_button_locator)
        mode_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

    def close_print_mode(self):
        """
        Close print mode
        @return:
        """
        logging.info("Close print mode")
        close_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.close_print_mode_button_locator)
        close_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)  # representative item in the expected view.
        time.sleep(1)

    def collapse_print_setting(self):
        """
        Collapse print setting
        @return:
        """
        collapse_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.collapse_button_locator)
        collapse_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)

    def check_color_supported(self, cdm):
        """
        Check color supported
        @return:
        """
        CDM_ENDPOINT = cdm.JOB_TICKET_CAPABILITIES_ENDPOINT

        logging.info("[check_color_supported] START")
        cdm_get_response = cdm.get(CDM_ENDPOINT)
        logging.info(cdm_get_response)
        is_supported = False
        try:
            if "true" == cdm_get_response["print"]["colorModeSupported"]:
                is_supported = True
                logging.info("[check_color_supported] color is supported")
            else:
                logging.info("[check_color_supported] Need to skip this test - color is not supported.")
        except:
            logging.info("[check_color_supported] Need to skip this test - [except]color is not supported.")
        logging.info("[check_color_supported] END")
        return is_supported
    
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

        wait_pages = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        self.spice.wait_until(lambda: wait_pages["visible"] is True, 20)
        time.sleep(3)

        if(two_sided):
            logging.info("check 2sided options spec")
            assert ("on" if self.get_copy_2sided_options_status() else "off") == two_sided
        if(collate):
            logging.info("check collate status spec")
            assert ("on" if self.get_collate_options_status() else "off") == collate
        if(self.check_color_supported(self.spice.cdm)):            
          if(color):
            logging.info("check color options spec")
            self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.color_color_str_id, PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_color_menu_loctor)
            assert self.get_color_options() == color
        if(quality):
            logging.info("check quality otpions spec")
            self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.quality_quality_str_id, PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_quality_menu_loctor)
            assert self.get_quality_options() == quality
        if(paper_selection):
            self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.paperSelection_str_id, PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor)
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

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_sides_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view+ " " + PrintFromUsbAppWorkflowObjectIds.option_two_sided_button_locator)

        if(current_sides_option == "Select Any"):
            time.sleep(1)
            current_sides_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view+ " " + PrintFromUsbAppWorkflowObjectIds.option_two_sided_button_locator)

        logging.info("Current side settings is: " + current_sides_option)
        if(current_sides_option == "1-Sided"):
            return False
        else:
            return True

    def set_copy_2sided_options(self, two_sided_options="off"):
        """
        Set the status of 2side option
        @param two_sided_options:str -> on/off
        @return:
        """

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        msg = f"Set 2sided_options to {two_sided_options}"
        logging.info(msg)

        time.sleep(5)
        self.workflow_common_operations.scroll_to_position_vertical(position=0, scrollbar_objectname='#printSelectSettingsViewlist1ScrollBar')
        time.sleep(1)

        option_view = PrintFromUsbAppWorkflowObjectIds.options_view
        select_item = PrintFromUsbAppWorkflowObjectIds.option_two_sided_button_locator
        active_item = self.spice.query_item(option_view + " " + select_item)
        active_item.mouse_click()
        time.sleep(1)

        if two_sided_options == "off":
            logging.info("need to turn off 2 sided option")
            duplex_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_two_sided_set_simplex)
            duplex_item.mouse_click()
            time.sleep(1)

        if two_sided_options == "on":
            logging.info("need to turn on 2 sided option")
            simplex_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_two_sided_set_duplex)
            simplex_item.mouse_click()
            time.sleep(1)

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        if two_sided_options == "off":
            assert not self.get_copy_2sided_options_status(), f"Failed to set copy_2sided_options: {two_sided_options}"
        else:
            assert self.get_copy_2sided_options_status(), f"Failed to set copy_2sided_options: {two_sided_options}"
        


    def get_color_options(self):
        """
        Get the color option
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_color_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_color_button_locator)
        logging.info("Current color settings is: " + current_color_option)
        return current_color_option

    def goto_color_options_menu(self):
        """
        Go to color option menu
        @return:
        """
        logging.info("Go to color option menu")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_color_menu_loctor)

    def check_spec_on_usb_print_options_color(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_color_options(self, net, color_options="color", locale: str = "en-US"):
        """
        Set the color option
        @param net:
        @param color_options: str -> color/auto/grayscale
        @param locale:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        time.sleep(10)
        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.option_color_menu_loctor, PrintFromUsbAppWorkflowObjectIds.option_color_button_locator ]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )
        
        #color_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_color_button_locator)
        time.sleep(5)
        #color_item.mouse_click()
        time.sleep(5)

        if color_options == "color":
            gray_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_color_set_color)
            gray_item.mouse_click()
            time.sleep(1)

        if color_options == "grayscale":
            gray_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_color_set_grayscale)
            gray_item.mouse_click()
            time.sleep(1)


        if color_options == "auto":
            gray_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_color_set_auto)
            gray_item.mouse_click()
            time.sleep(1)

    def get_collate_options_status(self):
        """
        Get collate option status
        @return:
        """
        logging.info("Get collate option status")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        time.sleep(1)
        is_collate_options_checked = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch)[PrintFromUsbAppWorkflowObjectIds.property_checked]
        logging.info(f"Current collate option is: {is_collate_options_checked}")
        return is_collate_options_checked

    def set_collate_options(self, collate_options="off"):
        """
        Set collate option
        @param collate_options:str -> on/off
        @return:
        """
        logging.info(f"Set Collate_options to {collate_options}")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.options_collate_setting_switch, PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch ]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )
        collate_options_checked = self.get_collate_options_status()

        active_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch)
        # self.workflow_common_operations.goto_item_navigation(PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch, PrintFromUsbAppWorkflowObjectIds.options_view, select_option=False)

        if collate_options == "off" and collate_options_checked:
            logging.info("need to turn off collate option")
            active_item.mouse_click()
            time.sleep(1)

        if collate_options == "on" and not collate_options_checked:
            logging.info("need to turn on collate option")
            active_item.mouse_click()
            time.sleep(1)

        if collate_options == "off":
            assert not self.get_collate_options_status(), f"Failed to set collate to {collate_options}"
        else:
            assert self.get_collate_options_status(), f"Failed to set collate to {collate_options}"

    def get_quality_options(self):
        """
        Get quality option
        @return:
        """
        logging.info("Get the quality option")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_quality_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view + " " +PrintFromUsbAppWorkflowObjectIds.option_quality_button_locator+" SpiceText[visible=true]", isSpiceText=True)
        logging.info("Current quality settings is: " + current_quality_option)
        return current_quality_option

    def goto_quality_options_menu(self):
        """
        Go to quality menu
        @return:
        """
        logging.info("Go to quality menu")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_quality_menu_loctor)

    def check_spec_usb_print_options_quality(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_quality_options(self, net, quality_options="standard", locale: str = "en-US"):
        """
        Set quality option
        @param net:
        @param quality_options:str -> best/standard/draft
        @param locale:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.option_quality_menu_loctor, PrintFromUsbAppWorkflowObjectIds.option_quality_button_locator]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname=PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar)
        time.sleep(1)

        if quality_options == "standard" or quality_options == "normal":
            normal_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_quality_set_normal)
            normal_item.mouse_click()
            time.sleep(1)

        if quality_options == "best":
            best_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_quality_set_best)
            best_item.mouse_click()
            time.sleep(1)

        if quality_options == "draft":
            best_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_quality_set_draft)
            best_item.mouse_click()
            time.sleep(1)

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
    
    def set_page_order_options(self, page_order_options="first_page_on_top"):
        """
        Set the page order option
        @param page_order_options: str -> first_page_on_top/last_page_on_top
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        
        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.options_page_order_menu_locator, PrintFromUsbAppWorkflowObjectIds.options_page_order_button_locator]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar)

        if page_order_options == "first_page_on_top":
            first_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_first_page_on_top)
            first_on_top_item.mouse_click()
            time.sleep(1)

        if page_order_options == "last_page_on_top":
            last_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_last_page_on_top)
            last_on_top_item.mouse_click()
            time.sleep(1)
    
    def set_rotation_options(self, rotation_options="auto"):
        """
        Set the rotation option
        @param rotation_options: str -> auto/0_degrees/90_degrees/180_degrees/270_degrees
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        
        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.options_rotation_menu_locator, PrintFromUsbAppWorkflowObjectIds.options_rotation_button_locator]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar)

        if rotation_options == "auto":
            first_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_rotation_auto)
            first_on_top_item.mouse_click()
            time.sleep(1)

        if rotation_options == "0_degrees":
            last_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_rotation_0_degrees)
            last_on_top_item.mouse_click()
            time.sleep(1)
        
        if rotation_options == "90_degrees":
            last_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_rotation_90_degrees)
            last_on_top_item.mouse_click()
            time.sleep(1)
        
        if rotation_options == "180_degrees":
            last_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_rotation_180_degrees)
            last_on_top_item.mouse_click()
            time.sleep(1)
        
        if rotation_options == "270_degrees":
            last_on_top_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_rotation_270_degrees)
            last_on_top_item.mouse_click()
            time.sleep(1)
	
    def get_actual_str_of_value(self, object_name):
        """
        Get actual string of value about menu from object name.
        This function gets the string of value if there is both a title and a value, such as paper selection in the options.
        @return:
        """
        logging.info(f"To get actual str of value of{object_name}")
        item = self.spice.wait_for(object_name)
        self.spice.wait_until(lambda: item["visible"] is True, 20)
        actual_str = self.spice.query_item(object_name + " SpiceText[visible=true]", 1)["text"]
        logging.info(f"The actual str of value of oject name: {object_name} is: {actual_str}")
        return actual_str

    def get_paper_selection_options(self):
        """
        Get paper selection option
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_paperSelection_option = self.get_actual_str_of_value(PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor)
        logging.info("Current paperSelection settings is: " + current_paperSelection_option)
        return current_paperSelection_option

    def get_paper_type_options(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_usb_print_options_paper_type(self):
        """
        Go to USBPrint_OptionsPaperType from USBPrint_OptionsPaperSelection screen
        @return:
        """
        logging.info("Go to USBPrint_OptionsPaperSize from USBPrint_OptionsPaperSelection screen")
        self.workflow_common_operations.goto_item_navigation(PrintFromUsbAppWorkflowObjectIds.option_paperType_menu_locator, PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection)
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperType)

    def check_spec_usb_print_options_paper_type(self, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_paper_type_options(self, net, paper_type_options="label", locale: str = "en-US"):
        """
        Set paper type
        @param paper_type_options:
        @return:
        """
        logging.info("Set Papertype")
        to_select_item = self.paper_type_dict.get(paper_type_options)
        #self.spice.common_operations.scroll_item_into_view(PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperType, PrintFromUsbAppWorkflowObjectIds.paper_type_list_view_scroll_bar,to_select_item)
        logging.info("wait for focus on")
        time.sleep(2)
        self.workflow_common_operations.goto_item(to_select_item, PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperType, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.paper_type_list_view_scroll_bar)

    def goto_usb_print_options_paper_selection(self):
        """
        Goto USBPrint_OptionsPaperSelection from USBPrint_Options
        @return:
        """
        logging.info("Goto USBPrint_OptionsPaperSelection from USBPrint_Options")
        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor, PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor ]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )
        active_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor)
        active_item.mouse_click()
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection)

    def goto_usb_print_options_paper_size(self):
        """
        Go to USBPrint_OptionsPaperSize from USBPrint_OptionsPaperSelection screen
        @return:
        """
        logging.info("Go to USBPrint_OptionsPaperSize from USBPrint_OptionsPaperSelection screen")
        self.workflow_common_operations.goto_item_navigation(PrintFromUsbAppWorkflowObjectIds.option_paperSize_menu_locator, PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection)
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperSize)

    def set_paper_size_options(self, paper_size_options="a4_210x297_mm"):
        """
        Set paper size
        @param paper_size_options:
        @return:
        """
        logging.info("Set Papersize")
        to_select_item = self.paper_size_dict.get(paper_size_options)
        #self.spice.common_operations.scroll_item_into_view(PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperSize, PrintFromUsbAppWorkflowObjectIds.paper_size_list_view_scroll_bar,to_select_item)
        logging.info("wait for focus on")
        time.sleep(2)
        self.workflow_common_operations.goto_item(to_select_item, PrintFromUsbAppWorkflowObjectIds.view_option_paperSelection_paperSize, scrolling_value=0.05, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.paper_size_list_view_scroll_bar)

    def get_print_margins_options(self):
        """
        Get print margins option
        @return:
        """
        logging.info("Get the print margins option")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_print_margins_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_margins_button_locator+" SpiceText[visible=true]", isSpiceText=True)
        logging.info("Current print margins settings is: " + current_print_margins_option)
        return current_print_margins_option

    def set_print_margins_options(self, net, print_margins_options="clip_from_contents"):
        """
        Set print margins option
        @param net:
        @param print_margins_options:str -> clip_from_contents/add_to_contents/oversize
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.option_print_margins_menu_loctor]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )

        margins_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_margins_button_locator)
        margins_item.mouse_click()
        time.sleep(1)

        if print_margins_options == "clip_from_contents":
            clip_from_contents_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_print_margins_set_clip_from_contents)
            clip_from_contents_item.mouse_click()
            time.sleep(1)

        elif print_margins_options == "add_to_contents":
            add_to_contents_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_print_margins_set_add_to_contents)
            add_to_contents_item.mouse_click()
            time.sleep(1)
        
        elif print_margins_options == "oversize":
            oversize_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_print_margins_set_oversize)
            oversize_item.mouse_click()
            time.sleep(1)

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

    def check_spec_on_usb_print_options_print_margins(self, net, print_margins=None):
        """
        Check spec on Print Margins in USBPrint_Options
        @param net:
        @param print_margins:str -> clip_from_contents/add_to_contents
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.print_margins_str_id, PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_margins_menu_loctor)

        if(print_margins):
            logging.info("check print margins options spec")
            assert self.get_print_margins_options() == print_margins

    def set_print_defaultOutputDestination(self, net, defaultOutputDestination="stacker"):
        """
        Set print margins option
        @param net:
        @param defaultOutputDestination:str -> stacker/folder
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_menu_locator]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )

        margins_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_button_locator)
        margins_item.mouse_click()
        time.sleep(1)

        if defaultOutputDestination == "stacker":
            clip_from_contents_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_set_stacker)
            clip_from_contents_item.mouse_click()
            time.sleep(1)

        elif defaultOutputDestination == "folder":
            add_to_contents_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_set_folder)
            add_to_contents_item.mouse_click()
            time.sleep(1)

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

    def get_print_defaultOutputDestination_options(self):
        """
        Get print margins option
        @return:
        """
        logging.info("Get the print margins option")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        current_print_defaultOutputDestination_option = self.workflow_common_operations.get_actual_str(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_button_locator)
        logging.info("Current print defaultOutputDestination settings is: " + current_print_defaultOutputDestination_option)
        return current_print_defaultOutputDestination_option
    
    def check_spec_on_usb_print_options_print_defaultOutputDestination(self, net, print_defaultOutputDestination=None):
        """
        Check spec on Print defaultOutputDestination in USBPrint_Options
        @param net:
        @param print_defaultOutputDestination:str -> Stacker/Folder
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.print_defaultOutputDestination_str_id, PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_defaultOutputDestination_menu_locator)

        if(print_defaultOutputDestination):
            logging.info("PONS check print defaultOutputDestination options spec" + self.get_print_defaultOutputDestination_options())
            logging.info("PONS check print defaultOutputDestination options spec" + print_defaultOutputDestination)
            assert self.get_print_defaultOutputDestination_options() == print_defaultOutputDestination

    def check_spec_on_usb_print_options_print_defaultFoldingStyle(self, net, print_folder_constrained_mode=True):
        """
        Check spec on Print defaultFoldingStyle in USBPrint_Options
        @param net:
        @param print_folder_constrained_mode:bool
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        folder_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_view + " " + PrintFromUsbAppWorkflowObjectIds.option_print_defaultFoldingStyle_button_locator)
        if(print_folder_constrained_mode):
            assert folder_item["constrained"] == True, "Button is not constrained"
        else:
            assert folder_item["constrained"] == False, "Button is constrained"
        
    def get_output_scale_options(self):
        """
        Get output scale option
        @return:
        """
        logging.info("Get the output scale option")
        logging.info(f"To get actual str of " + PrintFromUsbAppWorkflowObjectIds.option_output_scale_button_locator)
        
        target_item = PrintFromUsbAppWorkflowObjectIds.option_output_scale_button_locator
        item = self.spice.wait_for(target_item)
        current_output_scale_option = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_button_locator + " #contentItem")["text"]
        logging.info("Current output scale settings is: " + current_output_scale_option)
        return current_output_scale_option

    def set_output_scale_options(self, net, output_scale_options="none", detail_option=None, check_radio_btn=0, setting_page_id='Alloptions'):
        """
        Set print output scale option
        @param net:
        @param output_scale_options:str -> none/custom/loaded_paper/standard_sizes
        @param detail_option:
        @return:
        """
        setting_page_dict = {
            'Alloptions' : PrintFromUsbAppWorkflowObjectIds.options_view,
            'interactive_summary' : PrintFromUsbAppWorkflowObjectIds.detail_panel_layout
        }

        setting_page_scrollbar_dict = {
            'Alloptions' : PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar,
            'interactive_summary' : PrintFromUsbAppWorkflowObjectIds.detail_panel_layout_scrollbar
        }

        setting_page = setting_page_dict[setting_page_id]
        setting_page_scrollbar = setting_page_scrollbar_dict[setting_page_id]

        self.spice.wait_for(setting_page)
        
        if setting_page_id == 'Alloptions':
            menu_item_id = PrintFromUsbAppWorkflowObjectIds.option_output_scale_button_locator
            self.workflow_common_operations.goto_item(menu_item_id, setting_page, scrollbar_objectname = setting_page_scrollbar )
        else:
            scrollbar = self.spice.query_item(setting_page_scrollbar)
            scrollbar['position'] = 0.2

        output_scale_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_menu_loctor)
        output_scale_item.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_none)

        if check_radio_btn:
            none_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_none)
            none_item.mouse_click()

        if output_scale_options == "none":
            none_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_none)
            none_item.mouse_click()

        elif output_scale_options == "custom":
            if check_radio_btn == 0:
                custom_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom)
                custom_item.mouse_click()
            if detail_option:
                customValue = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom_spin_box)["value"] - detail_option
                if customValue > 0:
                    customDown = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom_spin_box + " " + PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom_spin_box_minus_locator)
                    for i in range(0, customValue):
                        customDown.mouse_click()
                        time.sleep(0.1)
                else:
                    customUp = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom_spin_box + " " + PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom_spin_box_plus_locator)
                    for i in range(0, abs(customValue)):
                        customUp.mouse_click()
                        time.sleep(0.1)

                if check_radio_btn:         
                    custom_size_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_custom)
                    assert custom_size_item["checked"] == True

        elif output_scale_options == "loaded_paper":
            if check_radio_btn == 0:
                loaded_paper_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper)
                loaded_paper_item.mouse_click()
            if detail_option:
                detail_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail)
                detail_item.mouse_click()
                if detail_option == "roll-1":
                    self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll1)
                    roll_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll1)
                    roll_item.mouse_click()
                elif detail_option == "roll-2":
                    self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll2)
                    roll_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll2)
                    roll_item.mouse_click()
                elif detail_option == "tray":
                    self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_tray)
                    tray_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_tray)
                    tray_item.mouse_click()

                if check_radio_btn:
                    loaded_paper_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_loaded_paper)
                    assert loaded_paper_item["checked"] == True

        elif output_scale_options == "standard_sizes":
            if check_radio_btn == 0:
                standard_sizes_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes)
                standard_sizes_item.mouse_click()
            if detail_option:
                detail_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail)
                detail_item.mouse_click()
                self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a0)
                detail_option_dict = {
                    "a0": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a0,
                    "a1": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a1,
                    "a2": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a2,
                    "a3": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a3,
                    "a4": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_a4,
                    "b1": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b1,
                    "b2": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b2,
                    "b3": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b3,
                    "b4": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_b4,
                    "letter": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_letter,
                    "ledger": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ledger,
                    "ansi_c": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_c,
                    "ansi_d": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_d,
                    "ansi_e": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_ansi_e,
                    "arch_a": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_a,
                    "arch_b": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_b,
                    "arch_c": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_c,
                    "arch_d": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_d,
                    "arch_e": PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes_detail_arch_e
                }
                detail_option_id = detail_option_dict.get(detail_option)
                self.workflow_common_operations.goto_item(detail_option_id, PrintFromUsbAppWorkflowObjectIds.standard_sizes_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.standard_sizes_scrollbar)
                
                if check_radio_btn:
                    standard_sizes_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_output_scale_set_standard_sizes)
                    assert standard_sizes_item["checked"] == True
        
        if setting_page_id == 'Alloptions':
            back_button = PrintFromUsbAppWorkflowObjectIds.option_output_scale_view + " #BackButton"
        else:
            back_button = "#closeButton"
        self.spice.query_item(back_button).mouse_click()
        self.spice.wait_for(setting_page)

    def check_spec_on_usb_print_options_output_scale(self, net, output_scale=None, setting_page_id='Alloptions'):
        """
        Check spec on Output Scale in USBPrint_Options
        @param net:
        @param output_scale:str -> none/...
        @return:
        """
        setting_page_dict = {
            'Alloptions' : PrintFromUsbAppWorkflowObjectIds.options_view,
            'interactive_summary' : PrintFromUsbAppWorkflowObjectIds.detail_panel_layout
        }
        setting_page = setting_page_dict[setting_page_id]

        self.spice.wait_for(setting_page)
        
        time.sleep(1)
        target_item = setting_page + " " + PrintFromUsbAppWorkflowObjectIds.option_output_scale_menu_loctor
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.output_scale_str_id, target_item)

        if(output_scale):
            logging.info("check output scale options spec")
            assert self.get_output_scale_options() == output_scale

    def check_spec_scan_to_usb_global_insert_usb(self, net):
        """
        Check ScanToUSB_GlobalInsertUSB
        @param net:
        @return:
        """
        logging.info("Check spec on ScanToUSB_GlobalInsertUSB")
        logging.info("verify the header messages")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.usb_defect_header_str_id, PrintFromUsbAppWorkflowObjectIds.usb_defect_header)

        #logging.info("verify the body messages")
        #self.dial_common_operations.verify_string(net, self.usb_defect_str_id, self.usb_defect_locator)

        logging.info("verify the  cancel button messages")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.usb_cancel_button_str_id, PrintFromUsbAppWorkflowObjectIds.usb_cancel_button)

    def select_scan_to_usb_global_insert_usb_cancel_button(self):
        """
        Select ScanToUSB_GlobalInsertUSB cancel button
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        scan_app = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.usb_cancel_button)
        scan_app.mouse_click()

    def check_usb_print_disconnected_message_button(self):
        """
        Check if PrintFromUSB disconnected message and button are visible
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        scan_app = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.usb_disconnected_button)
        scan_app.mouse_click()

    def check_spec_usb_print_no_file_found(self, net):
        """
        Check spec USBPrint_NoFileFound
        @param net:
        @return:
        """
        logging.info("check the spec on USBPrint_NoFileFound")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.usb_no_file_str_id, PrintFromUsbAppWorkflowObjectIds.usb_defect_locator)
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.usb_ok_button_str_id, PrintFromUsbAppWorkflowObjectIds.print_usb_no_content_ok_button)

    def cancel_current_print_job_by_click_cancel_button(self, udw):
        """
        Click cancel button to cancel current print job
        @return:
        """
        ui_size = udw.mainUiApp.ControlPanel.getBreakPoint()
        job_concurrent_supported = self.spice.cdm.get(self.spice.cdm.JOB_CAPABILITIES_ENDPOINT).get('jobConcurrencySupported')
        if job_concurrent_supported == 'true':
            self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view, timeout = 9.0)
            try:
                cancel_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_cancel_job_button_footer_locator, timeout = 5.0)
                self.spice.wait_until(lambda: cancel_button["visible"] == True)
                cancel_button.mouse_click()
            except Exception:
                cancel_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_cancel_job_button_locator)
                cancel_button.mouse_click()
        else:
            cancel_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_cancel_button_locator)
            cancel_button.mouse_click()
            cancel_confirm_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_cancel_confirm_button_locator, timeout = 9.0)
            cancel_confirm_button.mouse_click()

    def get_index_from_file_name(self, file_name, timeout_val=300):
        """
        Get print file or folder by file_name
        @param name:
        @return: index of file_name 
        """
        start_time = time.time()
       
        searched_name = ''
        count = 0
        while time.time() < start_time + timeout_val:
            current_button = self.spice.query_item("#printUsbFolderLandingView SpiceText[visible=true]", count)
            searched_name = current_button['text']
            if searched_name == file_name:
                logging.info("Get index success")
                return count
            count += 1


    def select_print_file_or_folder_by_property_text(self, file_name, timeout_val=300):
        """
        Select print file or folder by property text
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)
        logging.info("Wait_For  print_usb_folder_list_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        logging.info("goto_item print_usb_folder_list_view")
        # This is a workaround for only test_printfromusb_ui_filename_special_characters (hello@#$%^&world)
        time.sleep(5)
        count = self.get_index_from_file_name(file_name)
        current_button = self.spice.query_item("#printUsbFolderLandingView SpiceText[visible=true]", count)
        current_button.mouse_click()

    def scroll_to_back_button(self, screen_id, index: int = 0, timeout_val: int = 120):
        #Do nothing
        return None

    def goto_usb_print_options_paper_tray(self):
        """
        Go to Paper Tray menu
        @return:
        """
        logging.info("Go to Paper Tray menu")
        paperTraySetting = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_paperTray_menu_locator)
        paperTraySetting.mouse_click()
        time.sleep(1)

    def set_paper_tray_options(self, net, paper_tray_options="tray1"):
        """
        Set paper tray, UI in Paper Tray menu
        @param tray_options:
        @return:
        """
        logging.info("Set the paper_tray option to: " + paper_tray_options)

        to_select_item = self.paper_tray_dict.get(paper_tray_options)
        self.spice.wait_for(to_select_item)

        traySetting = self.spice.query_item(to_select_item)
        traySetting.mouse_click()
        time.sleep(1)

    def get_current_job_url(self, current_job_type):
        # todo: need to move this function into job.py since this function in other branch and wait for merge into default
        logging.info("To get the current active print job status from CDM")
        job_queue = self.spice.cdm.get(self.spice.cdm.JOB_QUEUE_ENDPOINT)
        job_list = job_queue.get("jobList")
        job_info_url = None
        
        get_job_queue_time_out = 20
        while len(job_list) == 0 and get_job_queue_time_out > 0:
            get_job_queue_time_out = get_job_queue_time_out - 1
            time.sleep(1)
            job_queue = self.spice.cdm.get(self.spice.cdm.JOB_QUEUE_ENDPOINT)
            job_list = job_queue.get("jobList")

        logging.info("job_queue is: " + str(job_queue))

        for job_item in job_list:
            if job_info_url:
                break

            job_type = job_item.get("jobType")

            if job_type == current_job_type:
                links = job_item.get("links")

                for link_item in links:
                    rel = link_item.get("rel")
                    if rel == "job":
                        job_info_url = link_item.get("href")
                        break

        if job_info_url:
            return job_info_url
        
        logging.warning(f"Failed to get job_info_url in job list: {job_list}")

        return None

    def get_current_job_status(self, job_info_url):
        res = self.spice.cdm.get_raw(job_info_url, timeout=10)
        res.raise_for_status()
        current_job_info = res.json()
        logging.info(f'Current job id is {current_job_info["jobId"]}, status is: {current_job_info["state"]}')
        return current_job_info["state"]

    def check_cartridge_very_low_screen(self, net, locale: str = "en-US"):
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.cartridge_very_low_str_id, PrintFromUsbAppWorkflowObjectIds.cartridge_very_low_locator, locale, isSpiceText=True)

    def go_back_to_print_from_options(self):
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_optionView, timeout = 3.0)
        try:
            close_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_button_close)
            close_button.mouse_click()
            time.sleep(1)
        except:
            self.workflow_common_operations.back_button_press(self.options_view, self.print_settings_view, 4)
            assert self.spice.query_item("#BackButton", 4)["visible"] == True
            self.spice.query_item("#BackButton", 4).mouse_click()
    
    def go_back_to_options_from_paper_selection(self):
        time.sleep(1)
        assert self.spice.query_item("#printFromUSB_paperSelectionMenuList #BackButton")["visible"] == True
        self.spice.query_item("#printFromUSB_paperSelectionMenuList #BackButton").mouse_click()
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_optionView, timeout = 9.0)
    
    def press_back_button_from_folder_view(self, screen_id, landing_view, index):
        current_button = self.spice.wait_for("#BackButton", 1)
        current_button.mouse_click()

    def press_back_button(self, index = 1):
        current_button = self.spice.wait_for("#BackButton", index)
        current_button.mouse_click()
    
    def wait_for_load_paper_error_view(self):
        """
        Wait for load paper error view
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_load_paper_error_view, timeout = 500)

    def click_ok_button_load_paper_error_view(self):
        """
        Click ok button in load paper error view
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_load_paper_error_view, timeout = 9.0)
        ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_load_paper_error_view)
        ok_button.mouse_click()
    
    def click_cancel_button_load_paper_error_view(self):
        """
        Click cancel button in load paper error view
        @return:
        """
        cancel_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.cancel_button_load_paper_error_view,timeout=30)
        cancel_button.mouse_click()
    
    def wait_for_media_mismatch_type_view(self):
        """
        Wait for media mismatch type view
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_type, timeout = 500)

    def is_media_mismatch_type_view_dismiss(self):
        """
        Check media mismatch type view is dismiss or not
        @return:
        """
        try:
            self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_type)
            return False
        except:
            return True
        
    def is_media_mismatch_size_view_dismiss(self):
        """
        Check media mismatch size view is dismiss or not
        @return:
        """
        try:
            self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_size)
            return False
        except:
            return True
        
    def is_confirm_loaded_paper_view_dismiss(self):
        """
        Check "confirm loaded paper" view is dismiss or not
        @return:
        """
        try:
            self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_confirm_loaded_paper)
            return False
        except:
            return True

    def click_ok_button_media_mismatch_type_view(self):
        """
        Click ok button in media mismatch type view
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_type, timeout = 9.0)
        ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_media_mismatch_type)
        ok_button.mouse_click()

    def wait_for_media_mismatch_size_view(self):
        """
        Wait for media mismatch size view
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_size, timeout = 500)

    def click_ok_button_media_mismatch_size_view(self, configuration):
        """
        Click ok button in media mismatch size view
        @param tray:main/tray-1, ok button id is different for main tray and tray-1
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_media_mismatch_size, timeout = 9.0)
        if configuration.productname in ["selene", "euthenia", "camden", "dagger", "busch", "bowie", "katana"]:
            ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_media_mismatch_size)
        elif configuration.productname in ["eddington", "elion", "marconi/marconisfpdl", "marconi/marconihipdl", "marconi/marconipdl", "marconi/marconihi", "marconi/marconi", "marconi/marconisf", "moreto", "moretohi"]:
            ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_media_mismatch_size_for_mm)
        else:
            ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_media_mismatch_size)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def check_folder_name_in_usb_folder_list_screen(self, folder_name):
        """
        Check folder name on printUsbFolderListView screen.
        @param folder_name:
        @return:
        """
        logging.info("Check folder name on printUsbFolderListView screen")
        title_text = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_header_view_folder_title_locator,query_index = 32767)["text"]
        assert folder_name == title_text, f"Folder name is error, expected folder name should be <{folder_name}>, actual folder name is <{title_text}>"

    def goto_sort_filter_search_options_menu(self):
        """
        Go to sort filter search options menu.
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_app_view)
        
        logging.info("Go to top to find sort filter search options menu")
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
        
        logging.info("The scroll positon of Homepro models need to set position 0 twice.")
        time.sleep(2)
        try :
            while scrollbar["position"] != 0 :
                scrollbar["position"] = 0
        except Exception as e:
            logging.info(e)
            pass
        

    def select_sort_filter_search_option(self, option:str):
        """
        Select corresponding option
        @param:option sort/filter/search
        @return:
        """
        options_dict = {
            "sort": PrintFromUsbAppWorkflowObjectIds.option_sort,
            "filter": PrintFromUsbAppWorkflowObjectIds.option_filter,
            "search": PrintFromUsbAppWorkflowObjectIds.option_search
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
            "all_file_types": PrintFromUsbAppWorkflowObjectIds.filter_option_all_file_type,
            "jpeg": PrintFromUsbAppWorkflowObjectIds.filter_option_jpeg,
            "tiff": PrintFromUsbAppWorkflowObjectIds.filter_option_tiff,
            "pdf":PrintFromUsbAppWorkflowObjectIds.filter_option_pdf,
            "ppt":PrintFromUsbAppWorkflowObjectIds.filter_option_ppt,
            "doc":PrintFromUsbAppWorkflowObjectIds.filter_option_doc,
            "ps":PrintFromUsbAppWorkflowObjectIds.filter_option_ps
        }
        self.spice.wait_for(filter_options_dict[option])
        # update method to scroll_item_into_view while scroll_item_into_view method merge into 24s branch.
        # self.scroll_item_into_view(PrintFromUsbAppWorkflowObjectIds.filter_list_view, PrintFromUsbAppWorkflowObjectIds.filter_list_view_scroll_bar, filter_options_dict[option], shifting=True)
        self.spice.wait_for(f"{filter_options_dict[option]}").mouse_click()
    
    def click_save_button_on_filter_screen(self):
        """
        Click save button in filter screen.
        @return:
        """
        save_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.save_button_filter_screen)
        save_button.mouse_click()
        
    def check_file_names_in_folder_list_view(self, expected_file_list):
        """
        Check expect files shows in folder list view screen.
        @param:expected_file_list:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        time.sleep(2)
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
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
            self.workflow_common_operations.scroll_to_position_vertical(scrollPosition, PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
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
        time.sleep(5)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        result_message = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.search_result_message_locator, 15)["text"]
        result_number = result_message.split("+")[0]
        assert len(expected_file_list) == int(result_number), "Search result numbers is error"
    
    def input_search_text_in_search_screen(self, search_text):
        """
        Input search text in search screen.
        @param:search_text: str
        @return:
        """
        logging.info("wait for Search screen")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_usb_search_view)
        search_input_view = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.search_text_field_locator)
        search_input_view.mouse_click()
        search_input_view.__setitem__('displayText', search_text)
        self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.ok_button_keyboard).mouse_click()
    
    def click_search_button_in_search_screen(self):
        """
        Click search button in search screen.
        @return:
        """
        search_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.search_button_locator)
        self.spice.validate_button(search_button)
        search_button.mouse_click(10,10)
    
    def check_search_constrained_screen(self, net):
        """
        Check search constrained screen should be displayed correctly.
        """
        expected_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintFromUsbAppWorkflowObjectIds.search_file_folder_str_id)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_app_view+" "+PrintFromUsbAppWorkflowObjectIds.view_constraint_message)
        logging.info("check 'Type a file name in the text field to search.' shows in search constrained screen")
        constrain_message = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.text_view_constraint_message)["text"]
        assert constrain_message == expected_str, "Failed to check search constrained message"

    def click_ok_button_on_search_constrained_screen(self):
        """
        click OK button on search constrained screen.
        """
        ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_app_view+" "+PrintFromUsbAppWorkflowObjectIds.view_constraint_message+" "+PrintFromUsbAppWorkflowObjectIds.ok_button_constrained_message)
        self.spice.validate_button(ok_button)
        ok_button.mouse_click()

    def click_cancel_button_on_search_screen(self):
        """
        click Cancel button on search screen.
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_usb_search_view+" "+PrintFromUsbAppWorkflowObjectIds.button_on_search_screen)
        cancel_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.view_print_usb_search_view+" "+PrintFromUsbAppWorkflowObjectIds.button_on_search_screen,1)
        self.spice.validate_button(cancel_button)
        cancel_button.mouse_click()
    
    def wait_for_reading_usb_screen(self):
        """
        wait for reading usb screen
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.reading_usb_progress_locator)
    
    def select_specific_sort_option(self, option:str):
        """
        Select sort option
        @param:option AtoZ/ZtoA/OldToNew/NewToOld
        @return:
        """
        sort_options_dict = {
            "AtoZ": PrintFromUsbAppWorkflowObjectIds.sort_option_a_to_z,
            "ZtoA": PrintFromUsbAppWorkflowObjectIds.sort_option_z_to_a,
            "OldToNew": PrintFromUsbAppWorkflowObjectIds.sort_option_old_to_new,
            "NewToOld":PrintFromUsbAppWorkflowObjectIds.sort_option_new_to_old,
        }
        # update method to scroll_item_into_view while scroll_item_into_view method merge into 24s branch.
        # self.scroll_item_into_view("#sortList", "#sortListScrollBar", sort_options_dict[option], shifting=True)
        if option == "OldToNew" or option == "NewToOld":
            scrollbar_size = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.sort_option_scrollbar)
            self.workflow_common_operations.scroll_to_position_vertical(1- scrollbar_size["size"], PrintFromUsbAppWorkflowObjectIds.sort_option_scrollbar)
        
        self.spice.wait_for(f"{sort_options_dict[option]} #SpiceRadioButton").mouse_click()
    
    def click_save_button_on_sort_screen(self):
        """
        Click save button in sort screen.
        @return:
        """
        save_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.save_button_sort_screen)
        save_button.mouse_click()
    
    def get_sorted_file_name_list(self, expect_all_file_list):
        """
        Get file name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_all_file_list: 
        @return:file_name_list
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view)
        logging.info("(get_sorted_file_name_list)wait for sorted files load completed")
        time.sleep(10)
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
        scrollbarSize = scrollbar['size']
        scrollPosition = 0
        scrollbar["position"] = scrollPosition

        time.sleep(1)
        file_name_to_y_list = []       
        not_found_file_list = []

        for file_name in expect_all_file_list:
            try:
                self.spice.wait_for(f"#{file_name}", timeout=0.2)
                y_coordinate = self.spice.query_item(f"#{file_name}")["y"]
                file_name_to_y_list.append({
                    "file_name": file_name,
                    "y_coordinate": y_coordinate
                })
                logging.info(f"(get_sorted_file_name_list) -found without scroll:{file_name}, {y_coordinate}")
            except:
                not_found_file_list.append(file_name)

        #scroll down to find files
        while scrollPosition + 0.5 * scrollbarSize < 1:
            scrollPosition = scrollPosition + 0.5 * scrollbarSize
            self.workflow_common_operations.scroll_to_position_vertical(scrollPosition, PrintFromUsbAppWorkflowObjectIds.print_usb_folder_list_view_scroll)
            time.sleep(2)    
            for file_name in not_found_file_list[:]:
                try:
                    self.spice.wait_for(f"#{file_name}", timeout=0.2)
                    not_found_file_list.remove(file_name)
                    y_coordinate = self.spice.query_item(f"#{file_name}")["y"]
                    file_name_to_y_list.append({
                            "file_name": file_name,
                            "y_coordinate": y_coordinate
                    })
                    logging.info(f"(get_sorted_file_name_list) -found:{file_name}, {y_coordinate}")
                except:
                    logging.info(f"(get_sorted_file_name_list) not found: {file_name}, will find next scroll")

        logging.info(f"(get_sorted_file_name_list) sorted list by y coordinate")
        file_name_to_y_list.sort(key = lambda item: item["y_coordinate"])
        logging.info("(get_sorted_file_name_list) get file name list sorted by y coordinate")
        file_name_list = [i["file_name"] for i in file_name_to_y_list]
        logging.info(f"(get_sorted_file_name_list) file name list after sorted by y coordinate is <{file_name_list}>")
        return file_name_list

    def select_usb_partition(self, usb_partition):
        """
        Purpose: Select partition from select usb view.
        Ui Flow: USBPrint_SelectUsbView -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return:
        """
        self.spice.wait_for(usb_partition)
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromUsb 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        #self.workflow_common_operations.scroll_position(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb , PrintFromUsbAppWorkflowObjectIds.scrollBar_printFolderPage , PrintFromUsbAppWorkflowObjectIds.printFolderPage_column_name  , PrintFromUsbAppWorkflowObjectIds.printFolderPage_Content_Item)
        current_button = self.spice.query_item(usb_partition)
        current_button.mouse_click()
        # Wait for usb drive screen
        # self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, timeout=9.0) #TBD

    def goto_usb_print_options_paper_source(self):
        """
        Goto USBPrint_OptionsPaperSource from USBPrint_Options
        @return:
        """
        logging.info("Go to paper source menu")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_paper_source_menu_loctor)

    def set_paper_source_options(self, net, paper_source_options="roll1"):
        """
        Set paper source, UI in Paper Source menu
        @param tray_options:
        @return:
        """
        logging.info("Set the paper_source_options option to: " + paper_source_options)

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)
        time.sleep(1)
        if (paper_source_options=="roll") :
            self.workflow_common_operations.scroll_to_position_vertical(position=0.9, scrollbar_objectname=PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar)
            time.sleep(1)
        paper_source_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view+" "+PrintFromUsbAppWorkflowObjectIds.option_paper_source_button_locator)
        paper_source_item.mouse_click()
        time.sleep(1)

        to_select_item = self.paper_tray_dict.get(paper_source_options)

        roll_item = self.spice.wait_for(to_select_item)
        roll_item.mouse_click()
        time.sleep(1)

    def get_expected_paper_selection_options(self, net, paper_size=None, paper_type=None, paper_tray=None):
        """
        Purpose: This method is get the paper selection string via string id.
        param:
        paper_size: string type. eg: 'letter_8_5x11_in', 'a4_210x297_mm'
        paper_type: string type. eg: 'plain'
        paper_tray: string type. eg: 'tray1', 'tray2'
        return: dic
        """

        paper_selection_dict = {}
        if paper_size:
            paper_size_str_id = self.paper_size_dict_str_id.get(paper_size)
            paper_size_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, paper_size_str_id)
            paper_selection_dict["paper_size"] = paper_size_str
        
        if paper_type:
            paper_type_str_id = self.paper_type_dict_str_id.get(paper_type)
            paper_type_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, paper_type_str_id)
            paper_selection_dict["paper_type"] = paper_type_str

        if paper_tray:
            paper_tray_str_id = self.paper_tray_dict_str_id.get(paper_tray)
            paper_tray_str = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, paper_tray_str_id)
            paper_selection_dict["paper_tray"] = paper_tray_str

        
        return paper_selection_dict
    
    def verify_collate_constrained(self):
        """
        Go to collate option menu and verify that option is cosntrained
        @return:
        """
        logging.info("Go to collate option menu")
        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.options_collate_setting_switch, PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch ]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )
        
        active_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch + " MouseArea")
        active_item.mouse_click()
        
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_constraint_message)

        okButton = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        time.sleep(1)

    def select_preview_button(self, name: str):
        """
        select preview button to preview image
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view, timeout = 20.0)
        logging.info("Wait_For name")
        self.find_print_file_or_folder_by_name(name)

        logging.info("select preview")
        preview_button = self.spice.query_item(f"#{name} {PrintFromUsbAppWorkflowObjectIds.print_usb_folder_preview_button}")
        preview_button.mouse_click()

    def wait_for_preview_layout(self):
        """
        wait until preview layout displayed
        @param name:
        @return:
        """
        logging.info("Wait_For preview_layout")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.preview_screen_for_small, timeout = 40.0)

    def validate_preview_layout_header(self):
        """
        validate preview layout header
        @param name:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.preview_screen_for_large)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.preview_screen_header)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.preview_screen_header_moreOptions)

    def check_no_preview_button(self, name: str):
        """
        check preview button is not visible
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view, timeout = 20.0)
        logging.info("Wait_For name")
        self.find_print_file_or_folder_by_name(name)

        logging.info("check preview visible is false")
        assert (self.spice.query_item(f"#{name} {PrintFromUsbAppWorkflowObjectIds.print_usb_folder_preview_button}")["visible"] == False)

    def come_back_from_preview_screen(self):
        """
        select the Back button to exit the preview screen
        @return: None
        """
        back_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.preview_screen_header_backButton)
        assert back_button["visible"] == True
        back_button.mouse_click()

    def verify_constraint_message_view(self, net):
        """
        verify the constraint message view
        @param net:
        @return:
        """
        option_item = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.option_two_sided_menu_loctor)
        option_item.mouse_click()
        logging.info("Wait for the constraint message view pops up and verify the view")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.view_constraint_message_str_id, PrintFromUsbAppWorkflowObjectIds.view_constraint_message_content)
        logging.info("Verify the Constraint Message view successfully")

        logging.info("Clear this Constraint Message view")
        ok_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()

    def scroll_to_bottom(self, scroll_area_grid_layout):
        """
        Incrementally scroll to the bottom of the page to find the folder.
        :param usb_select_folder_layout: The layout of the USB folder selection screen.
        :return: True if the folder is found while scrolling, False otherwise.
        """
        pos = 0.05
        scroll_area = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.scroll_area_grid_layout_vertical_layout)
        while not self.page_indicator_in_viewing_area():
            scroll_area["position"] = pos
            pos += 0.05
            
    def page_indicator_in_viewing_area(self):
        """
        Check if the page indicator is in the viewing area.
        :return: True if the page indicator is in the viewing area, False otherwise.
        """
        grid_layout = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.scroll_area_grid_layout)
        page_indicator = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.page_indicator_loader)
        isIn = page_indicator["y"] >= grid_layout["height"] and grid_layout["contentY"] + grid_layout["height"] >= page_indicator["y"] + page_indicator["height"]
        return isIn
    
    def get_page_items(self, page: int, total_items: int = 120, items_per_page: int = 30, folders_prefix_name: str =""):
        """Helper function to calculate first and last items for a given page"""
        start_idx = (page - 1) * items_per_page + 1
        end_idx = min(page * items_per_page, total_items)
        folder_start= f"{folders_prefix_name}{start_idx:03d}" 
        folder_end= f"{folders_prefix_name}{end_idx:03d}" 
        return (folder_start, folder_end)
            
    def pagination_navigation_with_folder_order(self, folders_prefix_name: str, total_folders: int, max_items_per_page: int):
        """
        Test case to verify pagination navigation and folder visibility with folder order consideration.

        This function navigates through the USB folder selection screen, verifying folder visibility on 
        different pages (second page, last page, previous page, and first page). It dynamically calculates 
        folder IDs and ensures that folders are visible on the expected pages.
        
        :param folders_prefix_name: Prefix name for the folder IDs.
        :param total_folders: Total number of folders available.
        """
        logging.info("Starting pagination navigation test with folder order consideration.")

        # Wait for the USB folder layout and page indicator to load
        scroll_area_grid_layout = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.scroll_area_grid_layout)
        self.spice.wait_until(lambda: scroll_area_grid_layout["visible"] == True)
        page_indicator = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.page_indicator)
        self.spice.wait_until(lambda: page_indicator["visible"] == True)
        num_of_pages = page_indicator["count"]

        # Helper function to verify folder visibility
        def verify_folder_visibility(page: int, page_description: str):
            first, last = self.get_page_items(page, total_folders, max_items_per_page, folders_prefix_name)
            logging.debug(f"Verifying folder visibility on {page_description}: {first} and {last}")
            first_item = self.spice.wait_for(f"#{first}", timeout=50)
            self.spice.wait_until(lambda: first_item["visible"] is True, 50)
            last_item = self.spice.wait_for(f"#{last}", timeout=50) 
            self.spice.wait_until(lambda: last_item["visible"] is True, 50)

        # Step 1: Navigate to the second page and verify folder visibility
        logging.info("Navigating to the second page and verifying folder visibility.")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view)

        verify_folder_visibility(1, "first page")

        self.scroll_to_bottom(scroll_area_grid_layout)
        next_page_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.button_next_page)
        self.spice.validate_button(next_page_button)
        next_page_button.mouse_click()

        if not scroll_area_grid_layout["atYEnd"]:
            self.scroll_to_bottom(scroll_area_grid_layout)

        verify_folder_visibility(2, "second page")

        # Step 2: Navigate to the last page and verify folder visibility
        logging.info("Navigating to the last page and verifying folder visibility.")
        
        last_page_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.page_indicator_mouse_area + str(num_of_pages - 1))
        self.spice.validate_button(last_page_button)
        last_page_button.mouse_click()

        if not scroll_area_grid_layout["atYEnd"]:
            self.scroll_to_bottom(scroll_area_grid_layout)
        verify_folder_visibility(num_of_pages, "last page")

        # Step 3: Navigate to the previous page and verify folder visibility
        logging.info("Navigating to the previous page and verifying folder visibility.")
        previous_page_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.button_previous_page)
        self.spice.validate_button(previous_page_button)
        previous_page_button.mouse_click()

        if not scroll_area_grid_layout["atYEnd"]:
            self.scroll_to_bottom(scroll_area_grid_layout)
        verify_folder_visibility(num_of_pages-1, "Previous page")

        # Step 4: Navigate back to the first page and verify folder visibility
        logging.info("Navigating back to the first page and verifying folder visibility.")
        first_page_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.frist_page_indicator_mouse_area)
        self.spice.validate_button(first_page_button)
        first_page_button.mouse_click()
        if not scroll_area_grid_layout["atYEnd"]:
            self.scroll_to_bottom(scroll_area_grid_layout)

        verify_folder_visibility(1, "first page")
        logging.info("Pagination navigation test with folder order consideration completed successfully.")
