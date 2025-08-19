import logging
import time
import sys
import logging
from dunetuf.ui.uioperations.BaseOperations.IStorageJobAppUIOperations import IStorageJobAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowKeyboardUICommonOperations import WorkflowKeyboardUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowObjectIds import JobStorageAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.StorageJobAppWorkflowObjectIds import StorageJobAppWorkflowObjectIds

class StorageJobAppWorkflowUICommonOperations(IStorageJobAppUIOperations):
    """StorageJobAppWorkflowUICommonOperations class to initialize StorageJob workflow operations."""

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.workflow_keyboard_operations = WorkflowKeyboardUICommonOperations(self.spice)

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        self.homemenu.goto_menu(self.spice)

    def goto_job_storage(self):
        """
        Purpose: Navigates to Job Storage app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Job Storage app
        :param spice: Takes 0 arguments
        :return: None
        """
        found_job_storage = False
        menu_job_storage = False
        try:
            self.spice.main_app.goto_job_storage_app()
            found_job_storage = True
        
        except Exception as e:
            # If the print app is not found in the main screen, go directly to job storage.
            logging.info("Job Storage app not found, trying to access job storage app through print app")

        if not found_job_storage:
            try:
                print_app = self.spice.wait_for(HomeAppWorkflowObjectIds.print_app_button)
                print_app.mouse_click()
                logging.info("At Print App")
                job_storage = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.job_storage)
                job_storage.mouse_click()
                self.spice.wait_for("#JobStorageAppApplicationStackView")
                logging.info("At Job Storage App")
                menu_job_storage = True

            except Exception as e:
                logging.error("Job Storage app not found")
            
            if not menu_job_storage:
                self.spice.homeMenuUI().goto_menu_jobStorage(self.spice)
           
    def select_job_from_storage(self, jobName, query_index=0):
        max_attempts = 10
        scroll_position = 0.0
        scroll_increment = 0.1
        scroll_bar = StorageJobAppWorkflowObjectIds.job_list_view_scrollbar
        job_object_name = "#" + jobName
        for attempt in range(max_attempts):
            try:
                isVisible = self.validate_list_object_visibility_by_id(
                    StorageJobAppWorkflowObjectIds.job_list_spice_listView,
                    StorageJobAppWorkflowObjectIds.job_list_spice_row_element_prefix + jobName,
                    timeout=5
                )
                if not isVisible:
                    raise Exception(f"Job '{jobName}' not visible at scroll position {scroll_position}")
                    
                storejob = self.spice.wait_for(job_object_name, 5, query_index=query_index)
                storejob.mouse_click()
                logging.info(f"Found and clicked job '{jobName}' at scroll position {scroll_position}")
                return
            except Exception as e:
                logging.info(f"Job '{jobName}' not found at scroll position {scroll_position}, scrolling...")
                scroll_position += scroll_increment
                if scroll_position > 1.0:
                    scroll_position = 1.0
                
                self.workflow_common_operations.scroll_to_position_vertical(
                    scroll_position, 
                    scrollbar_objectname=StorageJobAppWorkflowObjectIds.job_list_view_scrollbar
                )
                
                if scroll_position >= 1.0:
                    break
        
        # Final attempt with longer timeout
        try:
            storejob = self.spice.wait_for(job_object_name, 10, query_index=query_index)
            storejob.mouse_click()
            logging.info(f"Found job '{jobName}' on final attempt")
        except Exception as e:
            logging.error(f"Failed to find job '{jobName}' after scrolling through the list")
            raise Exception(f"Job '{jobName}' not found in storage list")

    def job_storage_click_button(self, buttonName, query_index=0):
        button = self.spice.wait_for("#" + buttonName, 30, query_index=query_index)
        button.mouse_click()

    def select_first_locked_job(self, dunestorejob):
        storeJobs = dunestorejob.get_all()
        logging.info(f"No of store jobs are: {len(storeJobs)}")
        assert len(storeJobs) > 0, 'No stored jobs found!'

        firstJob = storeJobs[0]
        logging.info(f"Selecting first store job: {firstJob}")
        storedJobId = firstJob.get('jobId')
        self.job_storage_click_button(storedJobId)

    def click_jobStorageFormatUsbSuccessful_okButton(self, dunestorejob):
        self.job_storage_click_button("okButton")
    
    def click_jobStorageFormatUsb_continueButton(self):
        self.job_storage_click_button("Continue")
    
    def click_jobStorageFormatUsb_cancelButton(self):
        self.job_storage_click_button("Cancel")
    
    def select_storageJob(self, userName, fileName):
        self.job_storage_click_button(userName)
        jobList_checkBox = self.spice.wait_for("#" + fileName)
        jobList_checkBox.mouse_click()

    def select_job(self, fileName):
        """
        Selects a job from the job storage by its file name.
        :param fileName: The name of the job file to select.
        """
        jobList_checkBox = self.spice.wait_for("#" + fileName)
        jobList_checkBox.mouse_click()

    def unlock_stored_job(self, userName):
        """
        Clicks on the unlock button for the stored jobs of a specific user.
        :param userName: The name of the user whose stored jobs are to be unlocked.
        """
        self.job_storage_click_button(userName)
        unlock_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.unlock_button)
        unlock_button.mouse_click()

    def print_storeJob_selected(self):
        query_index = 0
        try:
            self.job_storage_click_button("continueButton")
            self.spice.wait_for('#DetailPanel')
            # If we are in the detail panel, we need to click the "second" print button
            # because the one in the main panel has index=0 but is not clickable.
            query_index = 1
        except:
            logging.info("Continue button not found, trying to print directly")    
        self.job_storage_click_button("printButton",query_index)
    
    def delete_storeJob_selected(self):
        self.job_storage_click_button("deleteButton")

    def detailed_storeJob_selected(self):
        self.job_storage_click_button("expandButton")
        self.spice.wait_for('#DetailPanel')

    def unlock_storeJob_selected(self, pin):
        self.spice.storejob.job_storage_click_button("unlockButton")
        field = self.spice.wait_for("#pinField", 10)
        field.mouse_click()
    
        self.workflow_keyboard_operations.numeric_keyboard_enter_number(pin, "#pinField", "FullKeypad")

        self.spice.storejob.job_storage_click_button("doneButton")

    def unlock_storeJob_encrypted_selected(self, pin):
        field = self.spice.wait_for("#passwordField", 10)
        field.mouse_click()
    
        self.workflow_keyboard_operations.keyboard_enter_text(pin, "#passwordField")
        
        self.spice.storejob.job_storage_click_button("doneButton")
    
    def click_on_copies_plus_button(self):
        plus_button = self.spice.wait_for("#jobStorage_numberOfCopiesMenuSpinBox #spinBoxItem #upButtonContainer #upBtn")
        assert plus_button, "Plus button not found"
        plus_button.mouse_click()

    def delete_all_store_jobs(self, dunestorejob):
        """
        Select all the store jobs in print from job storage app
        """
        storeJobs = dunestorejob.get_all()
        logging.info(f"No of store jobs are: {len(storeJobs)}")
        assert len(storeJobs) > 0, 'No stored jobs found!'
        
        for storeJob in storeJobs:
            logging.info(f"Deleting store job: {storeJob}")
            storedJobId = storeJob.get('jobId')
            self.job_storage_click_button(storedJobId)
        
        self.delete_storeJob_selected()

    def click_on_settings_notification_row_and_verify_constraint_message(self, job_names: list):
        """
        click on notification in interative summary and verify the constraint message with job names
        :param job_names: list of job names to verify in the constraint message
        """
        self.spice.wait_for(StorageJobAppWorkflowObjectIds.row_jobStorage_notification_constraint)
        self.spice.wait_for(StorageJobAppWorkflowObjectIds.row_jobStorage_notification_constraint).mouse_click()
        self.spice.wait_for(StorageJobAppWorkflowObjectIds.view_constraint_message)
        assert self.spice.wait_for(StorageJobAppWorkflowObjectIds.constraintDescription)

        text_content = self.spice.wait_for(StorageJobAppWorkflowObjectIds.constraintDescriptionText)
        lines = [line for line in text_content["text"].split("\n") if line.strip()]
        assert lines[1:] == job_names
        logging.info("Constraint message verified successfully")
        ok_button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.ok_button_constrained_message)
        ok_button.mouse_click()
        
    def back_to_folder_selection_view_from_job_listview(self):
        """
        navigate back to folder selection view from job list view
        """
        logging.info("Navigated back to folder selection from job list view")
        close_button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_list_view + StorageJobAppWorkflowObjectIds.back_button)
        close_button.mouse_click()

    def goto_number_of_copies(self):
        """
        Go to number of copies menu
        """
        menu_item = [StorageJobAppWorkflowObjectIds.row_spinBox_numberOfCopies, StorageJobAppWorkflowObjectIds.spinBox_numberOfCopies] 
        self.workflow_common_operations.goto_item(menu_item, StorageJobAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = StorageJobAppWorkflowObjectIds.job_storage_options_scrollbar, select_option=False )

    def set_number_of_copies(self, value: int):
        """
        Set the number of copies in the spin box
        """
        num_copies_element = self.spice.wait_for(StorageJobAppWorkflowObjectIds.spinBox_numberOfCopies)
        num_copies_element.__setitem__('value', value)
    
    def get_number_of_copies(self):
        """
        Get the number of copies from the spin box
        """
        num_copies_element = self.spice.wait_for(StorageJobAppWorkflowObjectIds.spinBox_numberOfCopies)
        value = num_copies_element.__getitem__('value')
        return value

    def set_number_of_copies_in_settings_view(self, value: int):
        """
        Set the number of copies in the settings view spin box
        """
        num_copies_element = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options_view +" " + StorageJobAppWorkflowObjectIds.spinBox_numberOfCopies)
        num_copies_element.__setitem__('value', value)
    
    def get_number_of_copies_in_settings_view(self):
        """
        Get the number of copies from the settings view spin box
        """
        num_copies_element = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options_view+ " "+ StorageJobAppWorkflowObjectIds.spinBox_numberOfCopies)
        value = num_copies_element.__getitem__('value')
        return value
        
    def goto_more_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, StorageJobAppWorkflowObjectIds.job_storage_options_scrollbar)
        logging.info("Go to color option menu")
        menu_item_id = [StorageJobAppWorkflowObjectIds.row_combo_copySettings_color, StorageJobAppWorkflowObjectIds.combo_copySettings_color]
        self.workflow_common_operations.goto_item(menu_item_id, StorageJobAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = StorageJobAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(StorageJobAppWorkflowObjectIds.view_copySettings_color)  

    def select_color_mode(self, option):
        '''
        UI should be in copy Settings view screen.
        Navigates to Side screen starting from setting option to color mode screen.
        UI Flow is setting option->color mode->select color
        '''
        self.goto_copy_option_color_screen()
        if option == "Automatic":
            current_button = self.spice.query_item(StorageJobAppWorkflowObjectIds.combo_color_option_automatic)
        elif option == "Color":
            current_button = self.spice.query_item(StorageJobAppWorkflowObjectIds.combo_color_option_color)
        elif option == "Grayscale":
            current_button = self.spice.query_item(StorageJobAppWorkflowObjectIds.combo_color_option_grayscale)
        elif option == "Black Only":
            current_button = self.spice.query_item(StorageJobAppWorkflowObjectIds.combo_color_option_blackonly)
        else:
            raise Exception(f"Invalid color type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(StorageJobAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0) 

    def is_more_options_visible(self, timeout=10):
        more_options_button_visible = False
        navigated_to_detail_panel = False

        try:
            more_options_button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options, timeout=timeout)
            more_options_button_visible = more_options_button["visible"]
        except Exception:
            pass

        if not more_options_button_visible:
            try:
                logging.info("Checking if we are in detail panel")
                try:
                    detail_panel = self.spice.wait_for(StorageJobAppWorkflowObjectIds.detail_panel, timeout=timeout)
                    if detail_panel["visible"] == False:
                        raise Exception("Detail panel not visible")
                except Exception:
                    logging.info("Not in detail panel, moving to detail panel")
                    self.detailed_storeJob_selected()
                    navigated_to_detail_panel = True

                more_options_button_detail = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options_detail, timeout=timeout)
                more_options_button_visible = more_options_button_detail["visible"]
            except Exception:
                pass
        if navigated_to_detail_panel:
           self.close_detail_panel()
        return more_options_button_visible

    def go_to_more_options(self):
        """
        Go to more options
        """
        try:
            button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options)
            if not button["visible"]:
                raise Exception("job_storage_more_options not visible")
            button.mouse_click()
        except Exception as e:
            logging.info("job_storage_more_options not found, trying to enter through detail panel")
            button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.job_storage_more_options_detail)
            if not button["visible"]:
                raise Exception("job_storage_more_options_detail not visible")
            button.mouse_click()
        logging.info("UI: At Options list screen")

    def close_detail_panel(self):
        if (self.spice.uisize == "XS" or self.spice.uisize == "S"):
            self.spice.wait_for(StorageJobAppWorkflowObjectIds.detail_panel +" " + StorageJobAppWorkflowObjectIds.back_button).mouse_click()
        else :
            self.spice.wait_for(StorageJobAppWorkflowObjectIds.collapse_button).mouse_click()
        time.sleep(1)
    
    def validate_list_object_visibility_by_id(self, list_view_id, target_item_id, timeout=5):
        """
        Validates if a target item is visible within a list view by querying the elements using their object IDs.
        
        :param list_view_id: Object ID of the list view container
        :param target_item_id: Object ID of the target item to check visibility for
        :param timeout: Timeout for waiting for elements (default: 5 seconds)
        :return: True if the target item is visible, False otherwise
        """
        try:
            # Query the list view element
            list_view_element = self.spice.wait_for(list_view_id, timeout)
            if not list_view_element:
                logging.warning(f"List view element with ID '{list_view_id}' not found")
                return False
            
            # Query the target item element
            target_item_element = self.spice.wait_for(target_item_id, timeout)
            if not target_item_element:
                logging.warning(f"Target item element with ID '{target_item_id}' not found")
                return False
            
            # Extract properties from the queried elements
            row_object_y = target_item_element["y"]
            row_object_height = target_item_element["height"]
            content_y_of_list_obj = list_view_element["contentY"]
            height_of_list_obj = list_view_element["height"]
            
            # Perform visibility calculation
            is_visible = (row_object_y >= content_y_of_list_obj and 
                         row_object_y <= height_of_list_obj + content_y_of_list_obj - row_object_height)
            
            logging.info(f"Visibility check for '{target_item_id}': {is_visible}")
            logging.debug(f"Target Y: {row_object_y}, Target Height: {row_object_height}")
            logging.debug(f"List Content Y: {content_y_of_list_obj}, List Height: {height_of_list_obj}")
            
            return is_visible
            
        except Exception as e:
            logging.error(f"Error checking visibility for '{target_item_id}' in '{list_view_id}': {str(e)}")
            return False

    def back_to_listView_from_detailPanel(self):
        """
        Navigate back to list view from detail panel
        """
        if (self.spice.uisize == "XS" or self.spice.uisize == "S"):
            back_button = self.spice.wait_for(StorageJobAppWorkflowObjectIds.detail_panel +" "+ StorageJobAppWorkflowObjectIds.back_button)
            back_button.mouse_click()
