import time
import sys
import logging
from dunetuf.scp import SCP
from dunetuf.ui.uioperations.BaseOperations.IPrintPhotoUsbAppUIOperations import IPrintPhotoUsbAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.PrintPhotoAppWorkflowObjectIds import PrintPhotoAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui import spice
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

class PrintPhotoAppWorkflowUICommonOperations(IPrintPhotoUsbAppUIOperations):
    
    
    def __init__(self, spice):
        """
        PrintPhotoAppUIOperations class to initialize print photo options operations.
        @param spice:
        """
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        
        
        
        
    def goto_print_photo_app(self):
        """
        Function to navigate to Inside of Print Photo app in Print App
        Ui Flow: Any screen -> Home screen -> Print app -> Print Photos
        @return:
        """
        print_photo_app = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.icon_print_photo_app)
        print_photo_app.mouse_click()
        logging.info("At Print Photo App")        
        
        
        
    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        photo_app = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.print_app)
        photo_app.mouse_click()
        logging.info("At Print App")
        
        
        
        
    def exit_no_usb_inserted_screen(self):
        """
        Click cancel button to exit no usb inserted screen
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_usb_inserted, timeout = 9.0)
        cancel_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.usb_photo_cancel_button)
        cancel_button.mouse_click()
        
        
        
        
    def no_file_found_OK(self):
        
        """
        Click OK button to exit 'noFileFoundUsbPhoto' screen
        @return:
        """
                
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_file_or_folder_found_screen, timeout = 9.0)
        ok_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_file_or_folder_found_screen_OK_button)
        ok_button.mouse_click()
        
        
        
        
    def select_files_from_list_after_usb_inserted(self, name: str, int = 180):
        
        """
       Selects file inside print photo
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.files_after_usb_inserted, timeout = 9.0)
        logging.info("Wait_For photo_print_usb_folder_landing_view")
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_landing_view, timeout = 20.0)
        logging.info("Wait_For  photo_print_usb_folder_list_view")
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        logging.info("Wait_For name")
        time.sleep(3)
        self.find_print_photo_file_or_folder_by_name(name)
        time.sleep(3)
        logging.info("goto_item_navigation")
        self.workflow_common_operations.goto_item_navigation(f"#{name}", PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        
        
        
        
    def find_print_photo_file_or_folder_by_name(self, file_name: str):
        """
        find expect file shows in folder list view screen.
        @param:file_name:
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        
        try:
            self.spice.wait_for(f"#{file_name}", timeout=20)
            return
        except:
            logging.info("search failed: try to scroll")

        time.sleep(3)
        scrollbar = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view_scroll)
        scrollbarSize = scrollbar['size']
        scrollPosition = 0
        scrollbar["position"] = scrollPosition
        #scroll down to find files
        
        while scrollPosition + 0.5 * scrollbarSize < 1:
            scrollPosition = scrollPosition + 0.5 * scrollbarSize
            scrollbar["position"] = scrollPosition
            try:
                targetItem = self.spice.wait_for(f"#{file_name}", timeout=0.5)
                listView = self.spice.query_item(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
                
                rowObjectY = targetItem["y"]
                rowObjectHeight = targetItem["height"]
                contentYOfListObj = listView["contentY"]
                heightOfListObj = listView["height"]
                
                if (rowObjectY >= contentYOfListObj and rowObjectY <= heightOfListObj + contentYOfListObj - rowObjectHeight):
                    return
                logging.info("expected file is not in screen")
            except:
                logging.info("search failed: try to scroll")
        assert self.spice.wait_for(f"#{file_name}", timeout=20), "search failed"  
        
        
        
        
    def start_photo_print(self):
        """
        UI should be in Print Photo App
        Selects the file inside Print Photo App
        UI Flow is click on print button
        @return:
        """
        time.sleep(3) # make sure can click print button          # sometimes cannot click print button
        button_locator = PrintPhotoAppWorkflowObjectIds.photo_print_button_locator
        if (self.spice.query_item(PrintPhotoAppWorkflowObjectIds.expand_button_locator)["visible"] == True):
            button_locator = PrintPhotoAppWorkflowObjectIds.photo_print_button_locator
        elif (self.spice.query_item(PrintPhotoAppWorkflowObjectIds.collapse_button_locator)["visible"] == True):
            button_locator = PrintPhotoAppWorkflowObjectIds.footer_detail_photo_print_button_locator

        for _ in range(5):
            self.spice.wait_for(button_locator).mouse_wheel(0, 0)
        
        self.workflow_common_operations.goto_item_navigation(button_locator, PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        logging.info("Click the print button to start printing")
                
       # print_button = self.spice.wait_for(button_locator)
        #print_button.mouse_click()
        logging.info("Divya-Print button clicked")
    
        
        
        
        
    def wait_for_photo_print_status(self, net, job, message: str, timeout=60, specific_str_checked=False):
        
        """
        Waits for print job to be completed
        @return:
        """
        
        if job.job_concurrency_supported == "true":
            self.wait_for_photo_print_status_toast(net, message, timeout, specific_str_checked)
        else:
            self.wait_for_print_status_modal(net, message, timeout)
            
            
            
            
    def wait_for_photo_print_status_modal(self, net, message: str, timeout=120):
        """
        Purpose: Wait for the given modal message to appear in screen and success if given modal appears
        Args: message: str, printing / Print successfully
              timeout
        @return:
        """
        if message == "printing":
            self.spice.wait_for("#wizardProgressActiveJobPrinting", timeout)
        elif message == "complete":
            self.spice.wait_for("#wizardCompletionActiveJob", timeout)
            ok_button = self.spice.query_item("#okButton")
            ok_button.mouse_click()
        elif message == "canceled":
            self.spice.wait_for*("#cancellingJob", timeout)

    
    def wait_for_print_status_modal(self, net, message: str = "complete", timeout=60):
        """
        Purpose: Wait for the given modal message to appear in screen and success if given modal appears
        Args: message: str, printing / Print successfully
              timeout
        @return:
        """
        view_content = ""
        if message == "starting":
            click_ok_button = False
            targetViewType = "jobModalProgress"
        elif message == "printing":
            click_ok_button = False
            targetViewType = "jobModalProgress"
        elif message == "complete":
            click_ok_button = True
            targetViewType = "jobModalCompletion"
            view_content = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintPhotoAppWorkflowObjectIds.print_job_completed_str_id).replace("%1$s", "Photo")
        elif message == "canceled":
            click_ok_button = True
            targetViewType = "jobModalCompletion"
            view_content = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, PrintPhotoAppWorkflowObjectIds.print_job_canceled_str_id).replace("%1$s", "Photo")

        started = time.time()
        while True:
            if time.time() - started > timeout:
                raise TimeoutError(
                    "Status matching '{}' not found within {:.2f}s".format(
                        targetViewType, timeout
                    )
                )

            if targetViewType == self.spice.wait_for("#ActiveJobModalView")["viewType"]:
                break
            elif view_content == self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.active_print_job_view)["text"]:
                break
            else:
                time.sleep(0.1)
        
        if click_ok_button:
            ok_button = self.spice.query_item("#okButton")
            logging.info("clicking OK button")
            ok_button.mouse_click()
            
            
            
    
    def wait_for_photo_print_status_toast(self, net, message: str, timeout=60, specific_str_checked=False):
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

        for i in range(time_out*2):
            time.sleep(0.5)
            try:
                toast_message = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.toast_message_text)["text"]
            except:
                toast_message = "Does not capture the status"

            logging.info(f"current message is: <{toast_message}>")
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
        
        
        
        
    def validate_photo_header(self, net, message: str = "Print Photos", timeout=60):
        if message == "Print Photos":
           self.spice.wait_for("#printPhotoUsbFolderLandingViewHeader", timeout)        
           
           
           
    def validate_photo_files_selected(self, net, message: str = "Selected", timeout=60):
        if message == "Selected":
           self.spice.wait_for("#selectedobj", timeout)
    
    
    def validate_photo_printButton(self, net, message: str = "Print", timeout=60):
        
        button_locator = PrintPhotoAppWorkflowObjectIds.photo_print_button_locator
        '''
        if (self.spice.query_item(PrintPhotoAppWorkflowObjectIds.expand_button_locator)["visible"] == True):
            button_locator = PrintPhotoAppWorkflowObjectIds.photo_print_button_locator
        elif (self.spice.query_item(PrintPhotoAppWorkflowObjectIds.collapse_button_locator)["visible"] == True):
            button_locator = PrintPhotoAppWorkflowObjectIds.footer_detail_photo_print_button_locator '''

        for _ in range(5):
            self.spice.wait_for(button_locator).mouse_wheel(0, 0)
        
    
    def photo_print_job_cancel_while_printing(self):
        self.start_photo_print()
        cancel_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_cancel_job_button_locator)
        cancel_button.mouse_click()
        
    def validate_fileNotSelected_screen(self):
        #self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_file_selected_screen, 60)
        ok_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_file_selected_screen_ok_button, 60)
        ok_button.mouse_click()
        
    def validate_toggleButton_nextScreen(self):
        toggle_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.expand_button_locator, 60)
        toggle_button.mouse_click()    
        
    def validate_number_of_copies(self):
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.number_of_copies, 60)
    
    def validate_layout(self):   
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.layout_menu_locator, 60)
        
    def validate_paper_type(self):   
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.paper_type, 60)

        
    def select_more_options(self):
        option_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_sort_ellipse)
        option_button.mouse_click()
    
    def select_search_option(self):
        self.spice.wait_for("#mainSection")
        search_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_search_option)
        search_button.mouse_click()
        
    def enter_file_name(self, message: str):
        keyboard = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_field)
        keyboard.__setitem__('displayText', message)
        keyboard.__setitem__('inputText', message)
        
    def selecting_search(self):
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_search_view, 60)
        search_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_button)
        search_button.mouse_click()  
        
    def check_search_result_number_in_folder_list_view(self, expected_file_list):
        """
        Check Search Result numbers shows in folder list view screen.
        @param:expected_file_list: 
        @return:
        """
        time.sleep(3) # Wait for 3 seconds for the result refresh to complete
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_results_reset_screen)
        result_number = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_result_message_locator)["text"]
        assert len(expected_file_list) == int(result_number), "Search result numbers is error"       
        
    def reset_after_search(self):
        reset_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.search_results_reset_screen)
        reset_button.mouse_click()
        
    def select_sort_option(self):
        self.spice.wait_for("#mainSection")
        time.sleep(3)
        sort_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_sort_screen_landing)
        sort_button.mouse_click()        
        self.spice.wait_for("#sortLayoutPhoto")
        
    
    
    def select_specific_sort_option(self, option:str):
        """
        Select sort option
        @param:option AtoZ/ZtoA/OldToNew/NewToOld
        @return:
        """
        sort_options_dict = {
            "AtoZ": PrintPhotoAppWorkflowObjectIds.sort_option_a_to_z,
            "ZtoA": PrintPhotoAppWorkflowObjectIds.sort_option_z_to_a,
            "OldToNew": PrintPhotoAppWorkflowObjectIds.sort_option_old_to_new,
            "NewToOld":PrintPhotoAppWorkflowObjectIds.sort_option_new_to_old,
        }
        
        
        if option == "OldToNew" or option == "NewToOld":
            # self.workflow_common_operations.scroll_to_position_vertical(0.4, "#sortListScrollBar")
            # sortListScrollBar cannot scroll with scroll_to_position_vertical function as the size of sortListScrollBar is always 1.
            scrollbar = self.spice.wait_for("#sortListScrollBar")
            scrollbar.__setitem__("position", str(0.4))
        
        self.spice.wait_for(f"{sort_options_dict[option]} #SpiceRadioButton").mouse_click()
        
        
    
    def click_save_button_on_sort_screen(self):
        """
        Click save button in sort screen.
        @return:
        """
        save_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.save_button_sort_screen)
        save_button.mouse_click()
        
           
    def get_sorted_file_name_list(self, expect_all_file_list):
        """
        Get file name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_all_file_list: 
        @return:file_name_list
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        logging.info("(get_sorted_file_name_list)wait for sorted files load completed")
        time.sleep(10)
        file_name_to_y_list = []
        not_found_file_list = []

        for file_name in expect_all_file_list:
            try:
                self.spice.wait_for(f"#{file_name}", 0.2)
                y_coordinate = self.spice.query_item(f"#{file_name}")["y"]
                file_name_to_y_list.append({
                    "file_name": file_name,
                    "y_coordinate": y_coordinate
                })
                logging.info(f"(get_sorted_file_name_list) -found without scroll:{file_name}, {y_coordinate}")
            except:
                not_found_file_list.append(file_name)



        #scroll down and up to find files
        for i in range(2):
            if i%2 == 0:
                scrolldownnum = 1
            else:
                scrolldownnum = 9
            
            while len(not_found_file_list) > 0 and scrolldownnum < 10 and scrolldownnum >0:
                logging.info(f"(get_sorted_file_name_list) not found file name list : try to find them after scroll- {not_found_file_list} ")
                try:
                    pos = round(0.1 * scrolldownnum, 1)
                    logging.info(f"(get_sorted_file_name_list) -found scrolldownnum={scrolldownnum}, i= {i}, pos= {pos}")
                    self.workflow_common_operations.scroll_to_position_vertical(pos, PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view_scroll)
                except:
                    logging.info("(get_sorted_file_name_list) set possion failed: try again")

                for file_name in not_found_file_list:
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

                if (i%2 == 0):
                    scrolldownnum +=1
                else:
                    scrolldownnum -=1

        logging.info(f"(get_sorted_file_name_list) sorted list by y coordinate")
        file_name_to_y_list.sort(key = lambda item: item["y_coordinate"])
        logging.info("(get_sorted_file_name_list) get file name list sorted by y coordinate")
        file_name_list = [i["file_name"] for i in file_name_to_y_list]
        logging.info(f"(get_sorted_file_name_list) file name list after sorted by y coordinate is <{file_name_list}>")
        return file_name_list
    
    
    def cancelling_print_job(self):
        """
        Click cancel button to cancel current print job
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_landing_view, timeout = 9.0)
        cancel_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.cancel_print_job_button)
        cancel_button.mouse_click()
        
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


    def launch_print_job_no_file_selected(self):
        ok_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.no_file_selected_screen_ok_button, 60)
        ok_button.mouse_click()
        
        
        
        
    def set_no_of_copies(self, value):
        """
        Selects number of pages in USBPrint_printphoto screen based on user input
        @param value:
        @return:
        """
        # open expand buttor to show "Copies"
        expend_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.expand_button_locator, 60)
        expend_button.mouse_click()

        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.number_of_copies)
        numCopiesElement = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.number_of_copies)
        numCopiesElement.__setitem__('value', value)
    
    def set_number_of_copies_job(self, value):
        self.set_no_of_copies(value, PrintPhotoAppWorkflowObjectIds.numberOfCopies_spin_box)
        
        
    def select_usb_partition(self, usb_partition):
     
        self.spice.wait_for(usb_partition)
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromUsb 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        #self.workflow_common_operations.scroll_position(PrintPhotoAppWorkflowObjectIds.view_print_from_usb_landing, PrintPhotoAppWorkflowObjectIds.icon_print_from_usb , PrintPhotoAppWorkflowObjectIds.scrollBar_printFolderPage , PrintPhotoAppWorkflowObjectIds.printFolderPage_column_name  , PrintPhotoAppWorkflowObjectIds.printFolderPage_Content_Item)
        current_button = self.spice.query_item(usb_partition)
        current_button.mouse_click()
        
    def check_file_names_in_folder_list_view(self, expected_file_list):
        """
        Check expect files shows in folder list view screen.
        @param:expected_file_list:
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        time.sleep(2)
        scrollbar = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view_scroll)
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
            self.workflow_common_operations.scroll_to_position_vertical(scrollPosition, PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view_scroll)
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
        
    def press_back_button(self, index = 1):
        assert self.spice.query_item("#BackButton", index)["visible"] == True
        self.spice.query_item("#BackButton", index).mouse_click()
        
    def check_spec_scan_to_usb_global_insert_usb(self, net):
        """
        Check ScanToUSB_GlobalInsertUSB
        @param net:
        @return:
        """
        logging.info("Check spec on ScanToUSB_GlobalInsertUSB")
        logging.info("verify the header messages")
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.usb_defect_header_str_id, PrintPhotoAppWorkflowObjectIds.no_usb_inserted)

        logging.info("verify the  cancel button messages")
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.usb_cancel_button_str_id, PrintPhotoAppWorkflowObjectIds.usb_photo_cancel_button)
        
    def check_spec_usb_print_no_file_found(self, net):
        """
        Check spec USBPrint_NoFileFound
        @param net:
        @return:
        """
        logging.info("check the spec on USBPrint_NoFileFound")
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.usb_no_file_str_id, PrintPhotoAppWorkflowObjectIds.usb_defect_locator)
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.usb_ok_button_str_id, PrintPhotoAppWorkflowObjectIds.no_file_or_folder_found_screen_OK_button)

    def check_spec_on_usb_print_print_from_usb(self, net):
        """
        check spec on USBPrint_printphoto
        @param net:
        @return:
        """
        logging.info("check the str on USBPrint_printphoto screen")

        logging.info("check the string for Print button")
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.print_button_str_id, PrintPhotoAppWorkflowObjectIds.photo_print_button_locator)
        
    def check_spec_on_photo_print_home(self, net):
        """
        check spec on USBPrint_printphotoHome
        @param net:
        @return:
         """
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.header_print_photos_str_id,
                                                      PrintPhotoAppWorkflowObjectIds.icon_print_photo_app)


    def check_usb_print_disconnected_message_button(self):
        """
        Check if printphoto disconnected message and button are visible
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        disconnected = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.usb_disconnected_button)
        disconnected.mouse_click()


    def check_usb_print_disconnected_message_button(self):
        """
        Check if printphoto disconnected message and button are visible
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        disconnected = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.usb_disconnected_button)
        disconnected.mouse_click()
        
    def check_joblog_from_ui(self, expected_list=[{"index": 2, "expect_value_list": ["Print Photos", "Success"]}], jobs=None):
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
                current_job = self.spice.wait_for("#JobQueueAppApplicationStackView #jobListElementTextBlock SpiceText")
                current_job.mouse_click()
                job_name = current_job["jobName"]
                time.sleep(3)
                job_result = "Success" if self.spice.job_ui.recover_job_status_type() == 0 else "Fail"
            else:
                self.spice.wait_for("#JOB_" + jobs.get_job_history()[i]["jobId"])
                job_name = self.spice.query_item("#JOB_" + jobs.get_job_history()[i]["jobId"] + " #jobListElementTextBlock")["jobName"]
                job_result = "Success" if self.spice.query_item("#JOB_" + jobs.get_job_history()[i]["jobId"] + " #jobListElementTextBlock #gridLayoutView")["completed"] else "Fail"
            logging.info(f"Check job_name {job_name} and job_result is {job_result}")
            assert job_name in item.get("expect_value_list")
            assert job_result in item.get("expect_value_list")
            
    def check_cartridge_very_low_screen(self, net, locale: str = "en-US"):
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.cartridge_very_low_str_id, PrintPhotoAppWorkflowObjectIds.cartridge_very_low_locator, locale, isSpiceText=True)
        
    def collapse_print_setting(self):
        """
        Collapse print setting
        @return:
        """
        collapse_button = self.spice.query_item(PrintPhotoAppWorkflowObjectIds.collapse_button_locator)
        collapse_button.mouse_click()
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_landing_view)
        
        
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
        
    def set_layout_options(self, net, layout_options="layout4X6Inches", locale: str = "en-US"):
        """
        Set the layout option
        @param net:
        @param layout_options: str -> layout/layout4X6Inches
        @param locale:
        @return:
        """

        layout_option_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.option_layout_button_locator)
        layout_option_button.mouse_click()


        if layout_options == "layout4X6Inches":
            gray_item = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.option_layout_set_4X6)
            gray_item.mouse_click()
            time.sleep(1)

        if layout_options == "layout5X7Inches":
            gray_item = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.option_layout_set_5X7)
            gray_item.mouse_click()
            time.sleep(1)

        if layout_options == "layoutLetter8Dot5X11Inches":
            gray_item = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.option_layout_set_8Dot5X11)
            gray_item.mouse_click()
            time.sleep(1)
            
    def goto_paper_options_menu(self):
        """
        Go to color option menu
        @return:
        """

        toggle_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.expand_button_locator, 60)
        toggle_button.mouse_click() 
        logging.info("Go to paper type option menu")
        self.workflow_common_operations.goto_item_navigation(PrintPhotoAppWorkflowObjectIds.option_paperType_menu_locator, PrintPhotoAppWorkflowObjectIds.view_option_paperSelection)
        time.sleep(5)


    def select_paper_type(self, paper_type_option ="otherMatteInkjetPaper", locale: str = "en-US"):
        
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.view_option_paperSelection_paperType, 60)

        if paper_type_option == "otherMatteInkjetPaper":
            item = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.option_other_matte_inkjet_paper, 60)
            item.mouse_click()
            time.sleep(5)

    def paper_mismatch_bypass(self):
        self.start_photo_print()
       # self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.media_mismatch_screen, 60)
       # print = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.media_mismatch_screen_print_bttn, 60)
        #print.mouse_click()
        

    def select_scan_to_usb_global_insert_usb_cancel_button(self):
        """
        Select ScanToUSB_GlobalInsertUSB cancel button
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        cancel_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.usb_photo_cancel_button)
        cancel_button.mouse_click()    


    def check_spec_on_photo_from_usb_home(self, net):
        """
        check spec on USBPrint_PrintFromUSBHome
        @param net:
        @return:
        """
        logging.info("check the str on Print Photos screen")

        logging.info("check the string for Print Photos")
        self.workflow_common_operations.verify_string(net, PrintPhotoAppWorkflowObjectIds.header_print_photos_str_id,
                                                  PrintPhotoAppWorkflowObjectIds.icon_print_photo_app)
        
    def goto_layout_options_menu(self):
        """
        Go to layout option menu
        @return:
        """

        toggle_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.expand_button_locator, 60)
        toggle_button.mouse_click() 
        logging.info("Go to layout option menu")
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.layout_menu_locator)
        
    def wait_for_reading_usb_screen(self):
        """
        wait for reading usb screen
        @return:
        """
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.reading_progess)

    def upload_multiple_file_to_usb_with_file_name(usbdevice, multiple_file_name, folder_path):
        logging.info("Put multiple file to usb with file name")
        upload_list = []
        original_file_list = list(map((lambda x:x.split("=")[0]), multiple_file_name.split("&")))
        file_list = map(lambda x:x.split("=")[1], multiple_file_name.split("&"))
        for i, file_name in enumerate(file_list):
            upload_list.append(file_name)
            logging.info(f"Upload index {i} file name {file_name} into path {folder_path} org file {original_file_list[i]}")
            usbdevice.upload_with_file_name(file_name, folder_path, original_file_list[i])
            time.sleep(1)

        return original_file_list

    def upload_with_file_name(self, file, path, target_file_name):
        """Copy specified file from system_test_binaries to specific USB device path."""
        file_path = get_system_test_binaries_path(file)
        drive_path = f'{path}/{target_file_name}'

        logging.info('Uploading file to USB drive: %s', drive_path)
        scp = SCP(self._cdm.ipaddress)
        scp.upload(file_path, drive_path)

        return drive_path

    def check_no_entries_found(self, net):
        '''
        Check no entries found spec when not search files
        '''
        logging.info("Check no entries found spec when not search files")
        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view)
        actual_text = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.text_view_empty_files)["text"]
        expected_text = self.spice.common_operations.get_expected_translation_str_by_str_id(net, "cNoEntriesFound")
        assert actual_text == expected_text, "Failed to check no entries found spec when not search files"

    def go_back_to_print_photos_from_option_list(self):
        """
        Click Back button on Print Photo Option list page
        """
        back_button = self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.back_button_option_list, timeout = 3.0)
        self.spice.validate_button(back_button)
        back_button.mouse_click()

        self.spice.wait_for(PrintPhotoAppWorkflowObjectIds.photo_print_usb_folder_list_view, timeout = 3.0)
