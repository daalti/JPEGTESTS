import logging
import sys
import time as t
from time import sleep
from enum import Enum
from typing import Dict
from dunetuf.addressBook.addressBook import *
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from dunetuf.ui.uioperations.BaseOperations.IJobStorageAppUIOperations import IJobStorageAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.JobStorageAppWorkflowObjectIds import JobStorageAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.send.common.defaultjoboptions.defaultjoboptionsutils import DefaultJobOptionsUtils, JobType
from dunetuf.send.common.common import Common as ScanCommon
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.configuration import Configuration
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations


class JobStorageAppWorkflowUICommonOperations(IJobStorageAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

        # Scan to job Storage flow operations
        # Navigation from Home screen

    paper_type_option_dict = {
        # dictionary key is element key,value is a list (0:strid  1:itemid(radio) 2:rowid)
        "Any Type": [JobStorageAppWorkflowObjectIds.job_storage_paper_type_any_str_id, JobStorageAppWorkflowObjectIds.radio_paperType_any, JobStorageAppWorkflowObjectIds.row_paper_type_any],
        "Plain": [JobStorageAppWorkflowObjectIds.job_storage_paper_type_plain_str_id, JobStorageAppWorkflowObjectIds.radio_paperType_plain, JobStorageAppWorkflowObjectIds.row_paper_type_plain],

    }
        
    def goto_scan_menu_app(self):
        '''
        Navigates to Scan App from Home screen.
        UI Flow is Home->Scan
        '''
        self.workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.scan_app, MenuAppWorkflowObjectIds.scan_app)

    def goto_send_to_job_storage_from_admin_app(self):
        self.scan_operations.goto_scan_app()

        # Click Scan to Job Storage Button
        button_scan_to_job_storage = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan + " MouseArea")
        self.spice.wait_until(lambda: button_scan_to_job_storage["visible"]==True, timeout=20.0)
        button_scan_to_job_storage.mouse_click()

    def goto_scan_to_job_storage_screen(self):
        '''
        Navigates to Scan then job Storage screen starting from Home screen.
        UI Flow is Scan->job storage(Scan to job storage landing view)
        '''
        self.scan_operations.goto_scan_app()
        sleep(5)
        self.workflow_common_operations.scroll_position(JobStorageAppWorkflowObjectIds.view_scan_screen, JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan,JobStorageAppWorkflowObjectIds.scrollBar_menuscanFolderLanding , JobStorageAppWorkflowObjectIds.scanFolderPage_column_name , JobStorageAppWorkflowObjectIds.scanFolderPage_Content_Item)
        button_scan_to_job_storage = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan + " MouseArea")
        self.spice.wait_until(lambda: button_scan_to_job_storage["visible"]==True)
        button_scan_to_job_storage.mouse_click()
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save,timeout=20.0)
        logging.info("UI: At Scan to job Storage screen")

    def wait_for_scan_to_job_storage_landing_view(self):
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan)
        logging.info("Inside Scan to Job Storage Successful Screen")


    def check_scan_to_job_storage_button(self):
        """
        Purpose: check if scan to job storage under Scan app is visible or not.
        @return: visible
        """
        try:
            self.spice.wait_for(
                JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan)
            visible = True
        except:
            visible = False

        logging.info(
            "[check_scan_job_storage_button] visible={}".format(visible))
        return visible
    
    def goto_scan_to_job_storage_option(self):
        '''
        Navigates to Scan then job Storage screen starting from Home screen.
        UI Flow is Home->Scan->job Storage
        '''
        self.scan_operations.goto_scan_app()
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan + " MouseArea")
        self.spice.wait_until(lambda: current_button["visible"]==True)
        current_button.mouse_click()
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_home_scan)

    def input_job_name_in_landing_view(self, job):
        """
        input for job name  in landing view, UI should in Scan to job storage landing view
        @param: job_name: str
        """
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_name_text)
        current_button.mouse_click()
        keyboard_view = self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        job_name_textbox = self.spice.wait_for(f"{JobStorageAppWorkflowObjectIds.textbox_job_name_field} {JobStorageAppWorkflowObjectIds.textbox_job_name_text}")
        job_name_textbox.__setitem__('displayText', job)
        keyword_ok = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()

    def click_on_pin_text_field(self):
        """
        click on pin text field
        """
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_pin_model)
        current_button.mouse_click()

    def input_pin_in_landing_view(self, pin):
        """
        input for pin  in landing view, UI should in Scan to job storage landing view
        @param: job_name: str
        """
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_pin_model)
        current_button.mouse_click()
        keyboard_view = self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        job_name_textbox = self.spice.wait_for(f"{JobStorageAppWorkflowObjectIds.textbox_job_pin_field} {JobStorageAppWorkflowObjectIds.textbox_job_pin_model}")
        job_name_textbox.__setitem__('displayText', pin)
        keyword_ok = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_enterKeyPositiveIntegerKeypad)
        keyword_ok.mouse_click()

    def input_pin_without_marking_private(self):
        """
        click on  pin text field  in landing view, UI should in Scan to job storage landing view
        """
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_pin_model)
        current_button.mouse_click()
        keyboard_view = self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_common_keyboard)
        self.spice.wait_until(lambda: keyboard_view["visible"] == True)
        job_name_textbox = self.spice.wait_for(f"{JobStorageAppWorkflowObjectIds.textbox_job_pin_field} {JobStorageAppWorkflowObjectIds.textbox_job_pin_model}")
        job_name_textbox.__setitem__('displayText', "1234")
        keyword_ok = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_button)
        keyword_ok.mouse_click()

    def press_save_to_job_storage(self, wait_time=2):
        '''
        UI should be at Scan to job storage landing view.
        Starts save to Scan to job storage.
        '''
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        logging.info("After press save to job Storage")

    def back_to_scan_to_job_storage_from_options_list(self, layer: int = 4):
        '''
        UI should be in Options list.
        Navigates back from Options screen to job Storage landing view.
        '''
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        sleep(5)

    def goto_job_name(self):
        '''
        Navigates to Job Name screen starting from Home screen.
        UI Flow is Home->Scan->job Storage->Job Name->(Alphanumeric Keyboard)
        '''
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.textbox_job_name_field)
        current_button.mouse_click()
        logging.info("UI: At Job Name screen")


    def goto_job_storage_scan_details(self):
        '''
        Navigates to Scan Details screen starting from Home screen.
        UI Flow is Job Storage->Scan To->(Scan Details settings view)
        '''
        self.goto_scan_to_job_storage_screen()
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage + " MouseArea")
        current_button.mouse_click()
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
        logging.info("UI: At Scan details screen in job Storage Settings")


    def goto_options_list_from_scan_to_job_storage_screen(self):
        '''
        UI should be in Scan to Job Storage  screen.
        Navigates to Options screen starting from Scan to Job Storage screen.
        UI Flow is Scan to Job Storage->Options->(Options list)
        '''
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_scan_to_job_storage_options)
        current_button.mouse_click()
        sleep(5)
        # Wait for Options screen
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.menu_list_scan_settings)

    def verify_save_button_constrained(self, net):
        '''
        UI should be at job storage constraint message screen.
        Function will verify the job storage path empty message.
        '''
        message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description} #contentItem", timeout = 9.0)["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        ok_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_button)
        ok_button.mouse_click()

    def verify_save_button_constrained_and_click_ok_if_constrained(self, timeout = 60, confirm: bool = True):
        """
        This method verify the empty constraint message
        Args:
            UI should be in job Storage landing view
        """
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.constraint_message, timeout)

        if(confirm):
            self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_button).mouse_click()

    def select_job_private(self):
        """
        select job private
        """
        current_button = self.spice.wait_for("#scanMakeJobPrivateModel")
        current_button.mouse_click()
        self.spice.wait_until(lambda: current_button["checked"] == True, timeout=10)
        
    def unselect_job_private(self):
        """
        unselect job private
        """
        current_button = self.spice.wait_for("#scanMakeJobPrivateModel")
        current_button.mouse_click()
        self.spice.wait_until(lambda: current_button["checked"] == False, timeout=10)

    def goto_options_list_via_scan_to_job_storage(self):
        '''
        Navigates to Options screen starting from Home screen.
        UI Flow is Home->Scan->job Storage->Options->(Options list)
        '''
        self.goto_scan_to_job_storage_screen()
        self.goto_options_list_from_scan_to_job_storage_screen()
    
    def save_as_default_scan_to_job_storage(self):
        '''
        This is helper method to save deafult settings
        UI flow Landing Page-> click on any save button -> save as deafult
        '''
        # Add sleep time since it takes a while for Save button to be clickable after back from options screen.
        sleep(2)
        save_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_save)
        save_button.mouse_click()
        sleep(3)
        try:
            (self.spice.wait_for(JobStorageAppWorkflowObjectIds.sign_in_combobox)["visible"])
        except Exception as e:
            logging.info("Sign In method screen not found")
        else:
            self.spice.signIn.select_sign_in_method("admin", "user")
            self.spice.signIn.enter_creds(True, "admin", "12345678")
            sleep(3)
        finally:
            self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_save_option_view)
            if (self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_save_as_default)["visible"] == True):
                save_as_default_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.scan_job_storage_save_as_default)
                save_as_default_button.mouse_click()
            ok_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_under_save_option_veiw)
            ok_button.mouse_click()
            self.spice.wait_for(JobStorageAppWorkflowObjectIds.save_as_default_alert_view)
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.save_as_default_alert_save_button)
            current_button.mouse_click()
            sleep(3)
            landing_view =  self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
            self.spice.wait_until(lambda: landing_view["visible"]==True)



    def goto_edge_to_edge_settings_via_scan_to_job_storager(self):
        '''
        Navigates to Edge-to-Edge in job Storage Options starting from Home screen.
        UI Flow is Home->Scan->job Storage->Options->Edge-to-Edge->(Edge-to-Edge toggle :True/False)
        '''
        self.goto_options_list_via_scan_to_job_storage()
        self.scan_operations.goto_edge_to_edge_settings()

    def goto_original_size_settings_via_scan_to_job_storage(self):
        '''
        Navigates to Original Size injobStorage Settings starting from Home screen.
        UI Flow is Home->Scan->jobStorage->Options->Original Size->(Original Size settings screen)
        '''
        self.goto_options_list_via_scan_to_job_storage()
        self.scan_operations.goto_original_size_settings()

    def goto_sides_settings_via_scan_to_job_storage(self):
        '''
        Navigates to Sides in jobStorage Settings screen starting from Home screen.
        UI Flow is Home->Scan->jobStorager->Options->Sides-> (Sides settings screen)
        '''
        self.goto_options_list_via_scan_to_job_storage()
        self.scan_operations.goto_sides_settings()

    

    def back_to_scan_app_from_scan_to_job_storage(self):
        '''
        UI should be in Scan to job Storage landing screen
        UI flow is Scan job Storage landing view -> Scan app landing screen
        '''
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
        back_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing_back_button)
        self.spice.validate_button(back_button)
        back_button.mouse_click()

    def back_to_home_from_scan_to_job_storage(self):
        '''
        UI should be in Scan to job Storage screen
        UI flow is scan home -> main ui
        '''
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
        homeButton = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_home)
        sleep(2)
        homeButton.mouse_click()
        sleep(2)
        # make sure that you are in the home screen
        logging.info("At Home Screen")

    def add_page_pop_up_add_more(self):
        scan_add_page_add_more_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page)
        assert scan_add_page_add_more_button
        scan_add_page_add_more_button.mouse_click()

    def add_page_pop_up_finish(self):
        add_page_done_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_scan_job_storage_add_page_finish)
        add_page_done_button.mouse_click()

    def add_page_pop_up_cancel(self):
        scan_add_page_cancel_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbedduplex_cancel)
        assert scan_add_page_cancel_button
        scan_add_page_cancel_button.mouse_click()
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_no)
        scan_add_page_cancel_page_yes_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_flatbed_duplex_cancel_yes)
        assert scan_add_page_cancel_page_yes_button
        scan_add_page_cancel_page_yes_button.mouse_click()

    def cancel_scan_to_job_storage(self):
        '''
        UI should be at scan progress view.
        Cancel the scan to job Storage job.
        '''
        scan_cancel_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_scan_progress_cancel)
        self.spice.wait_until(lambda: scan_cancel_button["enabled"] == True, 15)
        self.spice.wait_until(lambda: scan_cancel_button["visible"] == True, 15)
        scan_cancel_button.mouse_click()
        sleep(2)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)


    def start_scan_job_storage_job_with_settings(self,scan_options:Dict):
        '''
        Start save to job Storage with scan settings and verify job is success
        UI flow is from Scan to job Storage landing view -> Options list -> Scan settings
        '''
        self.goto_options_list_from_scan_to_job_storage_screen()
        settings = {
            'filetype': scan_options.get('filetype', None),
            'resolution': scan_options.get('resolution', None),
            'filesize': scan_options.get('filesize', None),
            'sides': scan_options.get('sides', None),
            'color': scan_options.get('color', None),
            'size': scan_options.get('size', None),
            'tiffcompression': scan_options.get('tiffcompression', None),
            'orientation': scan_options.get('orientation', None),
            'lighter_darker': scan_options.get('lighter_darker', None),
            'contrast': scan_options.get('contrast', None),
            'sharpness': scan_options.get('sharpness', None),
            'backgroundCleanup': scan_options.get('backgroundCleanup', None)
        }

        if settings['filetype'] != None:
            self.scan_operations.goto_filetype_settings()
            self.scan_operations.set_scan_setting('filetype', settings['filetype'])
        if settings['resolution'] != None:
            self.scan_operations.goto_resolution_settings()
            self.scan_operations.set_scan_settings_resolution(settings['resolution'])
        if settings['filesize'] != None:
            self.scan_operations.goto_filesize_settings()
            self.scan_operations.set_scan_settings_filesize(settings['FileSize'])
        if settings['sides'] != None:
            self.scan_operations.goto_sides_settings()
            self.scan_operations.set_scan_settings_sides(settings['sides'])
        if settings['color'] != None:
            self.scan_operations.goto_color_settings()
            self.scan_operations.set_scan_settings_color(settings['color'])
        if settings['size'] != None:
            self.scan_operations.goto_original_size_settings()
            self.scan_operations.set_scan_settings_original_size(settings['size'])
        if settings['tiffcompression'] != None:
            if settings['color'] == 'color':
                self.scan_operations.goto_tiff_compression_color_settings()
                self.scan_operations.set_scan_setting('tiffcompression_color', settings['tiffcompression'])
            elif settings['color'] == 'blackonly' or settings['color'] == 'grayscale':
                self.scan_operations.goto_tiff_compression_mono_settings()
                self.scan_operations.set_scan_setting('tiffcompression_mono', settings['tiffcompression'])
            else:
                assert False, "Setting not existing"
        if settings['orientation'] != None:
            self.scan_operations.goto_orientation_settings()
            self.scan_operations.set_scan_settings_orientation(orientation=settings['orientation'])
        if settings['lighter_darker'] != None:
            self.scan_operations.goto_lighter_darker_settings()
            self.scan_operations.set_scan_settings_lighter_darker(lighter_darker=settings['lighter_darker'])
        if settings['contrast'] != None:
            self.scan_operations.goto_contrast_settings()
            self.scan_operations.set_scan_settings_contrast(contrast=settings['contrast'])
        if settings['sharpness'] != None:
            self.scan_operations.goto_sharpness_settings()
            self.scan_operations.set_scan_settings_sharpness(sharpness=settings['sharpness'])
        if settings['backgroundCleanup'] != None:
            self.scan_operations.goto_backgroundcleanup_settings()
            self.scan_operations.set_scan_settings_backgroundcleanup(backgroundCleanup=settings['backgroundCleanup'])
        self.back_to_scan_to_job_storage_from_options_list()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save)
        current_button.mouse_click()

    def back_button_press_scan(self, udw, screen_id, layer: int = 0, timeout_val: int = 60):
        '''
        Press back button in specific screen.
        '''

        if (self.spice.wait_for("#BackButton")["visible"] == True):
            # TODO verify the code once the back button is in position
            back_button = self.spice.wait_for("#BackButton")
            back_button.mouse_click()
        else:
            logging.info("Back button is not visible")


    def set_job_name_empty(self):
        '''
        UI should be at alphanumeric keyboard view.
        Function will Clear the file name and press OK.
        '''
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_common_keyboard)
        sleep(3)
        clear_text = self.spice.wait_for(JobStorageAppWorkflowObjectIds.clear_text_filename)
        clear_text.mouse_click()
        sleep(2)
        keyword_ok = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_keyboard_ok)
        keyword_ok.mouse_click()
        sleep(3)
        self.spice.wait_for(ScanAppWorkflowObjectIds.menu_list_scan_settings)


    def verify_jobname_empty_message(self, net):
        '''
        UI should be at  constraint message screen.
        Function will verify the filename empty message.
        '''
        message = self.spice.wait_for(f"{ScanAppWorkflowObjectIds.constraint_description}  #contentItem")["text"]
        logging.info('message %s', message)
        expected_string = LocalizationHelper.get_string_translation(net,'cAllFieldsMarked')
        assert message == expected_string, "The prompt information is not displayed correctly"
        ok_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.ok_button)
        ok_button.mouse_click()


    def wait_for_scan_status_complete(self, net, message: str = "Complete", timeout: int = 60):
        """
        Purpose: Wait for the given toast message to appear in screen and complete if given toast appears
        Args: message: Scanning, Sending, Complete... : str
        """
        if message == "Starting":
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cStarting')
        elif message == "Scanning":
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanning')
        elif message == 'Sending':
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cSending')
        elif message == 'Complete':
           option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cScanSuccessfulMessage')
        elif message == 'preparingToSend':
            option = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cProgressJobQueue')

        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout = 25.0)
        start_time = time()
        while time()-start_time < timeout:
           try:
               self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
               status = self.spice.wait_for(JobStorageAppWorkflowObjectIds.text_toastInfoText, timeout=20.0)["text"]
               logging.info("Current Toast message is : %s" % status)
               self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_systemToastMessagesScreen, timeout=20.0)
           except:
               logging.info("Still finding corresponding status.")
           if option in status:
               break
        if option not in status:
           raise TimeoutError("Required Toast message does not appear within %s " % timeout)


    def wait_mainButton_type(self, state, timeout = 10 ):
        Landing = self.spice.wait_for( JobStorageAppWorkflowObjectIds.view_scan_job_storage_landing , 5 )
        self.spice.wait_until( lambda: Landing["mainButtonType"] == state , timeout )

    def validate_button_control(self):
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_control)

    def wait_and_validate_property_value(self, object, property, state, timeout = 5):
        self.workflow_common_operations.wait_until_property_value( object, property, state, timeout)
        assert object[property] == state


    def press_ok_button_at_read_only_enabled_screen(self):
        """
        This method is to click OK button at the read-only enabled display screen
        :return:
        """
        logging.info("Click ok button to exit Read-Only Enabled display screen")
        ok_button = self.spice.wait_for(f"{JobStorageAppWorkflowObjectIds.constraint_message} {JobStorageAppWorkflowObjectIds.ok_button}")
        ok_button.mouse_click()

    def wait_and_click_on_middle(self, locator: str) -> None:
        """
        Waits for object in clickable state (visible and enabled) and
        it clicks on the middle of the object
        """
        # Validate for object if not exist
        object = self.spice.wait_for(locator)

        # Wait for clickable situation
        self.spice.wait_until(lambda: object["enabled"] == True, 15)
        self.spice.wait_until(lambda: object["visible"] == True, 15)

        # Click on the middle of the object
        middle_width = object["width"] / 2
        middle_height = object["height"] / 2
        object.mouse_click(middle_width, middle_height)


    def wait_for_scan_storage_job_to_complete(self, cdm, udw, net, job, file_type, pages=1, time_out=120):
        """
        wait for scan storage job complete
        @param cdm, udw, job
        @param pages: set it when scan from Glass if scan Multi page
        @param time_out: timeout to wait for job finish
        """
        configuration = Configuration(cdm)
        common_instance = ScanCommon(cdm, udw)
        scan_resource = common_instance.scan_resource()

        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages
        if scan_resource == "Glass":
            try:
                for _ in range(pages-1):
                    scan_add_page_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                    self.spice.validate_button(scan_add_page_button)
                    scan_add_page_button.mouse_click()
                    sleep(2)

                scan_add_page_done_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                logging.info("#finish button found")
                self.spice.validate_button(scan_add_page_done_button)
                scan_add_page_done_button.mouse_click()
            except TimeoutError:
                logging.info("flatbed Add page is not available")
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": "ScanJobStorageApp", "status": "success"}], time_out=300)


    def save_to_job_storage(self, scan_more_pages: bool = False, wait_time=2):
        '''
        UI should be at Scan job storage landing view.
        Starts save to job storage.
        '''
        sleep(7)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save)
        current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save)
        self.spice.wait_until(lambda:current_button["visible"])
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        sleep(wait_time)
        logging.info("After press save to job storage")

    def goto_no_of_copies(self):
        menu_item = [JobStorageAppWorkflowObjectIds.row_spinBox_numberOfCopies, JobStorageAppWorkflowObjectIds.spinBox_numberOfCopies] 
        self.workflow_common_operations.goto_item(menu_item, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar, select_option=False )

    def ui_set_no_of_pages(self, value: int):
        numCopiesElement = self.spice.wait_for(JobStorageAppWorkflowObjectIds.spinBox_numberOfCopies)
        numCopiesElement.__setitem__('value', value)

    def goto_option_color_screen(self):
        """
        Go to color option menu
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        logging.info("Go to color option menu")
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_color, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_color]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_color)  

    def select_color_mode(self, option):
        '''
        Navigates to Side screen starting from setting option to color mode screen.
        UI Flow is setting option->color mode->select color
        '''
        self.goto_option_color_screen()
        if option == "Automatic":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_color_option_automatic)
        elif option == "Color":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_color_option_color)
        elif option == "Grayscale":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_color_option_grayscale)
        elif option == "Black Only":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_color_option_blackonly)
        else:
            raise Exception(f"Invalid color type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0) 

    def goto_quality_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        '''
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_quality, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_quality]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_quality)

    def select_quality_option(self, option):
        # quality
        self.goto_quality_option()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_quality)
        if option == "Standard":
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.combo_quality_option_standard)
        elif option == "Draft":
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.combo_quality_option_draft)
        elif option == "Best":
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.combo_quality_option_best)
        else:
            raise Exception(f"Invalid quality type <{option}>")

        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)

    def goto_option_content_type_screen(self):
        """
        Go into option content type screen
        @return:
        """
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_contentType, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_contentType]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_contentType)

    def select_content_type(self, option):
        #contentType
        self.goto_option_content_type_screen()
        content_options_dict = {
            "Mixed": f"{JobStorageAppWorkflowObjectIds.combo_contentType_option_mixed}",
            "Photograph": f"{JobStorageAppWorkflowObjectIds.combo_contentType_option_photograph}",
            "Text": f"{JobStorageAppWorkflowObjectIds.combo_contentType_option_text}",
            "Lines": f"{JobStorageAppWorkflowObjectIds.combo_contentType_option_linedraw}",
            "Image": f"{JobStorageAppWorkflowObjectIds.combo_contentType_option_image}",
        }
        to_select_item = content_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, JobStorageAppWorkflowObjectIds.view_jobStorageSettings_contentType,
            scrollbar_objectname = JobStorageAppWorkflowObjectIds.standard_sizes_scrollbar, select_option=False)
        current_button = self.spice.query_item(to_select_item + "")
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)
    
    def set_content_orientation_settings(self, orientation_option):
        """
        UI should be on Scan options list screen.
        UI Flow is Orientation-> (Orientation Settings screen).
        """
        self.workflow_common_operations.goto_item([JobStorageAppWorkflowObjectIds.row_object_jobStorage_orientation, JobStorageAppWorkflowObjectIds.settings_jobStorage_orientation],
                                                  JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_orientation_screen)
        if orientation_option == "Portrait":
            orientation_option = JobStorageAppWorkflowObjectIds.orientation_portrait_option
        elif orientation_option == "Landscape":
            orientation_option = JobStorageAppWorkflowObjectIds.orientation_landscape_option
        else:
            raise Exception(f"Invalid orientation type <{orientation_option}>")      
        orientation_option_button = self.spice.wait_for(orientation_option)
        orientation_option_button.mouse_click()
        logging.info("UI: selected orientation option")

    def goto_option_staple(self):
        """
        Go to staple option menu
        @return:
        """
        logging.info("Go to staple option menu")
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, JobStorageAppWorkflowObjectIds.list_jobStorage_staple, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_jobStorage_staple_value)

    def select_staple_option(self, option):

        self.goto_option_staple()

        staple_dict = {
            "leftTwoPoints": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_staple_leftTwoPoints,
                "row_id": JobStorageAppWorkflowObjectIds.row_staple_leftTwoPoints
                },
            "topLeftOnePointAny": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_staple_topLeftOnePointAny,
                "row_id": JobStorageAppWorkflowObjectIds.row_staple_topLeftOnePointAny
                },
        }
        to_select_item = staple_dict.get(option)
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.jobStorage_stapleMenuSelectionList, to_select_item["item_id"], scrollbar_objectname = JobStorageAppWorkflowObjectIds.menu_selection_list_scrollbar,select_option = True)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)

    def go_to_paper_selection(self):
        #PaperSelection
        self.workflow_common_operations.scroll_to_position_vertical(0,  JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        logging.info("Go to paper Selection option menu")
        self.homemenu.menu_navigation(self.spice, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, JobStorageAppWorkflowObjectIds.list_jobStorageSettings_paperSelection, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection)

    def goto_paper_size_screen(self):
        """
        Go to media size screen
        :return:
        """
        screen_id = JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection
        menu_item_id = JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSize
        current_button = self.spice.query_item(screen_id + " " + menu_item_id)
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSize)

    def select_media_size_option(self, option):
        # # media size
        self.go_to_paper_selection()
        self.goto_paper_size_screen()
        paper_size_options_dict = {
            "Match Original Size":JobStorageAppWorkflowObjectIds.row_media_size_any,
            "A2 (420x594 mm)":JobStorageAppWorkflowObjectIds.row_media_size_iso_a2_420x594mm,
            "A3 (297x420 mm)":JobStorageAppWorkflowObjectIds.row_media_size_iso_a3_297x420mm,
            "A4": JobStorageAppWorkflowObjectIds.row_media_size_iso_a4_210x297mm,
            "A4_SEF": JobStorageAppWorkflowObjectIds.row_media_size_rotate_iso_a4_210x297mm,
            "A5": JobStorageAppWorkflowObjectIds.row_media_size_iso_a5_148x210mm,
            "A5_SEF": JobStorageAppWorkflowObjectIds.row_media_size_rotate_iso_a5_148x210mm,
            "A6 (105x148 mm)":JobStorageAppWorkflowObjectIds.row_media_size_iso_a6_105x148mm,
            "Letter": JobStorageAppWorkflowObjectIds.row_media_size_na_letter_8_5x11in,
            "Letter_SEF": JobStorageAppWorkflowObjectIds.row_media_size_rotate_na_letter_8_5x11in,
            "Legal": JobStorageAppWorkflowObjectIds.row_media_size_na_legal_8_5x14in,
            "B5_SEF": JobStorageAppWorkflowObjectIds.row_media_size_rotate_jis_b5_182x257mm,
            "B6 (JIS) (128x182 mm)": JobStorageAppWorkflowObjectIds.row_media_size_jis_b6_128x182mm,
            "Statement (8.5x5.5 in.)": JobStorageAppWorkflowObjectIds.row_media_size_invoice_5_5x8_5in,
            "jis_b5": JobStorageAppWorkflowObjectIds.row_media_size_jis_b5_182x257mm,
            "Executive": JobStorageAppWorkflowObjectIds.row_media_size_executive_7_25x10_5in,
            "oficio_8_5x13": JobStorageAppWorkflowObjectIds.row_media_size_oficio_8_5x13in,
            "Oficio_8_5x13_4": JobStorageAppWorkflowObjectIds.row_media_size_oficio_8_5x13_4in,
            "4x6 in.": JobStorageAppWorkflowObjectIds.row_media_size_index_4x6_4x6in,
            "5x7 in.": JobStorageAppWorkflowObjectIds.row_media_size_index_5x7_5x7in, 
            "5x8 in.": JobStorageAppWorkflowObjectIds.row_media_size_index_5x8_5x8in,
            "Envelope B5 (176x250 mm)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_b5,
            "Envelope Monarch (3.9x7.5 in.)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_monarch,
            "Envelope C5 (162x229 mm)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_c5,
            "Envelope DL (110x220 mm)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_dl,
            "16K (184x260 mm)": JobStorageAppWorkflowObjectIds.row_media_size_16k_184x260,
            "16K (195x270 mm)": JobStorageAppWorkflowObjectIds.row_media_size_16k_195x270,
            "16K (197x273 mm)": JobStorageAppWorkflowObjectIds.row_media_size_16k_197x273,
            "100x150mm": JobStorageAppWorkflowObjectIds.row_media_size_10x15,
            "Double Postcard (JIS) (148x200 mm)": JobStorageAppWorkflowObjectIds.row_media_size_double_postcard_jis_148x200mm,
            "Envelope #10 (4.1x9.5 in.)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_10,
            "Postcard (JIS) (100x148 mm)": JobStorageAppWorkflowObjectIds.row_media_size_postcard_jis_100x148mm,
            "Custom size": JobStorageAppWorkflowObjectIds.row_media_size_custom,
            "Japanese Envelope Chou #3 (120x235 mm)": JobStorageAppWorkflowObjectIds.row_media_size_jpn_chou3_120x235mm,
            "Japanese Envelope Chou #4 (90x205 mm)": JobStorageAppWorkflowObjectIds.row_media_size_jpn_chou4_90x205mm,
            "Envelope C6 (114x162 mm)": JobStorageAppWorkflowObjectIds.row_media_size_envelope_c6,
            "L (89x127 mm)": JobStorageAppWorkflowObjectIds.row_media_size_l_89x127,
            "3x5 in.": JobStorageAppWorkflowObjectIds.row_media_size_index_3x5_3x5in

        }
        to_select_item = paper_size_options_dict.get(option)
        self.workflow_common_operations.goto_item(to_select_item, 
            JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection_paperSize, 
            scrollbar_objectname=JobStorageAppWorkflowObjectIds.jobStorage_papersize_scrollbar,
            select_option=False, scrolling_value = 0.07)        
        current_button = self.spice.wait_for(to_select_item, timeout = 9.0)
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection, timeout = 9.0)

    def go_back_to_setting_from_paper_selection(self):
        self.workflow_common_operations.back_or_close_button_press(f"{JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection} {JobStorageAppWorkflowObjectIds.button_back}", JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView)

    def go_to_more_options(self):
        """
        Go to more options
        """
        option_button =  self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options)
        self.spice.wait_until(lambda: option_button["enabled"] == True, 15)
        self.spice.wait_until(lambda: option_button["visible"] == True, 15)
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options).mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_storage_more_options_view)
        logging.info("UI: At Options list screen")

    def goto_paper_tray_screen(self):
        """
        Go to paper tray screen
        :return:
        """
        # Paper Tray
        screen_id = JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_paperTray, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_paperTray]
        current_button = self.spice.query_item(screen_id + " " + menu_item_id[0] + " " + menu_item_id[1])
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection_paperTray)

    def select_paper_tray_option(self, selected_option):
        # Paper Tray
        self.goto_paper_tray_screen()
        tray_dict = {
            "Automatic" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_auto,
            "Manual feed" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_manual,
            "Tray 1" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_tray1,
            "Tray 2" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_tray2,
            "Tray 3" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_tray3,
            "Tray Alternate" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_alternate,
            "Tray Main" : JobStorageAppWorkflowObjectIds.combo_paperTray_option_main
        }

        to_select_item = tray_dict.get(selected_option)
        self.workflow_common_operations.goto_item(to_select_item, 
            JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection_paperTray, 
            scrollbar_objectname=JobStorageAppWorkflowObjectIds.jobStorage_paperTray_scrollbar,
            select_option=False)        
        current_button = self.spice.wait_for(to_select_item, timeout = 9.0)
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection, timeout = 9.0)

    def goto_paper_type_screen(self):
        """
        Go to paper type screen
        :return:
        """
        screen_id = JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection
        menu_item_id = JobStorageAppWorkflowObjectIds.list_jobStorageSettings_paperType
        current_button = self.spice.query_item(screen_id + " " + menu_item_id)
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection_paperType)

    def select_paper_type_option(self, option):
        # Paper Type
        self.goto_paper_type_screen()
        self.workflow_common_operations.goto_item(self.paper_type_option_dict[option][2], JobStorageAppWorkflowObjectIds.view_jobStorageSettings_paperSelection_paperType, scrollbar_objectname = JobStorageAppWorkflowObjectIds.jobStorage_paperType_scrollbar,scrolling_value=0.05)

    def goto_sharpness_option(self):
        """
        go to contrast option
        """
        logging.info("Go to contrast option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_slider_sharpness, JobStorageAppWorkflowObjectIds.slider_sharpness]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, select_option = False, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar) 
    
    def set_sharpness_setting_value(self, value: int):
        """
        Args:
            value: The sharpness value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView), "Error: Not in All Options view"
        self.goto_sharpness_option()
        sharpness_slider = self.spice.wait_for(JobStorageAppWorkflowObjectIds.slider_sharpness)
        sharpness_slider.__setitem__('value', value)

    def goto_option_punch(self):
        """
        Go to punch option menu
        @return:
        """
        logging.info("Go to punch option menu")
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, JobStorageAppWorkflowObjectIds.list_jobStorageSettings_punch, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_jobStorageSettings_punch_value)

    def select_punch_option(self, option):

        self.goto_option_punch()

        punch_dict = {
            "leftTwoPointDin": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_punch_leftTwoPointDin,
                "row_id": JobStorageAppWorkflowObjectIds.row_punch_leftTwoPointDin
                },
            "rightTwoPointDin": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_punch_rightTwoPointDin,
                "row_id": JobStorageAppWorkflowObjectIds.row_punch_rightTwoPointDin
                },    
        }

        to_select_item = punch_dict.get(option)
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.jobStorage_punchMenuSelectionList, to_select_item["item_id"], scrollbar_objectname = JobStorageAppWorkflowObjectIds.menu_selection_list_scrollbar,select_option = True)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)
    
    def get_collate_status(self):
        """
        Get the option status of collate
        @return:
        """
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView)
        collate_toggle_btn_status = self.spice.query_item(JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_collate)["checked"]
        logging.info(f"The current status of collate is <{collate_toggle_btn_status}>")
        return collate_toggle_btn_status

    def change_collate(self, collate_option="off"):
        """
        Set the status of collate option
        @param collate_option:str -> on/off
        @return:
        """
        logging.info(f"Set collate option to value <{collate_option}>")

        self.workflow_common_operations.goto_item(JobStorageAppWorkflowObjectIds.row_toggle_jobStorageSettings_collate, 
            JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, 
            scrollbar_objectname=JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar,
            select_option=False)        
        
        collate_constraints = self.spice.wait_for(JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_collate)["constrained"]
        collate_toggle_btn = self.spice.wait_for(JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_collate + " MouseArea")
        is_collate_toggle_btn_checked = self.get_collate_status()

        if not collate_constraints == True:
            if collate_option == "off" and is_collate_toggle_btn_checked:
                logging.info("need to turn off collate option")
                collate_toggle_btn.mouse_click()
            elif collate_option == "on" and not is_collate_toggle_btn_checked:
                logging.info("need to turn on collate option")
                collate_toggle_btn.mouse_click()

    def goto_option_fold(self):
        """
        Go to punch option menu
        @return:
        """
        logging.info("Go to punch option menu")
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, JobStorageAppWorkflowObjectIds.list_jobStorage_fold, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_jobStorageSettings_fold_value)

    def select_fold_option(self, option):

        self.goto_option_fold()

        fold_dict = {
            "V-fold": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_fold_Vfold,
                "row_id": JobStorageAppWorkflowObjectIds.row_fold_Vfold
                },
            "C-fold": {
                "item_id": JobStorageAppWorkflowObjectIds.radio_fold_Cfold,
                "row_id": JobStorageAppWorkflowObjectIds.row_fold_Cfold
                },    
        }

        to_select_item = fold_dict.get(option)
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.jobStorage_foldMenuSelectionList, to_select_item["item_id"], scrollbar_objectname = JobStorageAppWorkflowObjectIds.fold_view_scroll_bar,select_option = True)

        btn = self.spice.wait_for(JobStorageAppWorkflowObjectIds.jobStorage_foldMenuSelectionList+" "+JobStorageAppWorkflowObjectIds.button_back, timeout=9.0)
        btn.mouse_click()

        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)

    def set_lighter_darker_option(self,value: int):
        """
        go to lighter darker option
        """
        logging.info("Go to lighter darker option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_slider_lighterDarker, JobStorageAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, select_option = False, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        lighter_Darker_slider = self.spice.wait_for(JobStorageAppWorkflowObjectIds.slider_lighterDarker)
        lighter_Darker_slider.__setitem__('value', value)
    
    def set_contrast_option(self,value: int):
        """
        go to contrast option
        """
        logging.info("Go to contrast option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_slider_contrast, JobStorageAppWorkflowObjectIds.slider_contrast]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, select_option = False, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        contrast_slider = self.spice.wait_for(JobStorageAppWorkflowObjectIds.slider_contrast)
        contrast_slider.__setitem__('value', value)        

    def goto_background_cleanup_option(self):
        """
        go to background cleanup option
        """
        logging.info("Go to background cleanup option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_slider_backGroundCleanup, JobStorageAppWorkflowObjectIds.slider_backGroundCleanup]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, select_option = False, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)

    def set_background_cleanup_setting_value(self, value: int):
        """
        Args:
            value: The background cleanup value to set - ( Range is 1 to 9)
        """
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView), "Error: Not in All Options view"
        self.goto_background_cleanup_option()
        background_cleanup_slider = self.spice.wait_for(JobStorageAppWorkflowObjectIds.slider_backGroundCleanup)
        background_cleanup_slider.__setitem__('value', value)

    def goto_auto_paper_color_removal_option(self):
        """
        go to the auto paper color removal option
        """
        logging.info("Go to auto paper color removal option menu")
        self.workflow_common_operations.scroll_to_position_vertical(0, JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_jobStorageSettings_autoPaperColorRemoval, JobStorageAppWorkflowObjectIds.checkbox_autoPaperColorRemoval]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, select_option = False, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)

    def goto_option_blank_page_suppression(self):
        """
        Go into option blank page suppression
        @return:
        """
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_blankPageSuppression, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_blankPageSuppression]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_blankPageSuppression)

    def select_blank_page_suppression(self, option = "on"):
        self.goto_option_blank_page_suppression()
        if option == "on":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_option_blankPageSuppression_on)
        elif option == "off":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_option_blankPageSuppression_off)
        else:
            raise Exception(f"Invalid option type <{option}>")
        current_button.mouse_click()
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)
    
    def goto_booklet_option(self):
        """
        Go to booklet format option menu
        @return:
        """
        logging.info("Go to booklet option menu")
        self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, 
                                      JobStorageAppWorkflowObjectIds.list_jobStorageSettings_booklet, 
                                      scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_view_jobStorageSettings_booklet)

    def select_booklet_option(self, option):
        """
        Go to booklet option menu and select the option
        @return:
        """
        self.goto_booklet_option()
        if (option == 'bookletFormat'):
            booklet_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.row_booklet_format_option)  
        elif(option == 'bordersOnEachPage'):
            booklet_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.row_borders_on_each_page_option)
        elif(option == 'foldAndStitch'):
            booklet_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.row_booklet_fold_and_stitch_option)
        else:
            booklet_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.row_booklet_fold_and_stitch_custom_option)

        if booklet_button["checked"] is False:
            booklet_button.mouse_click()
            assert booklet_button["checked"] is True
        else:
            booklet_button.mouse_click()
            assert booklet_button["checked"] is False

        back_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_view_jobStorageSettings_booklet +" "+ JobStorageAppWorkflowObjectIds.button_back)
        back_button.mouse_click()

    def goto_pages_per_sheet(self, udw, familyname=""):
        """
        Go to pages per sheet option menu
        @return:
        """
        familyname = self.spice.copy_ui().check_familyname(udw)

        if familyname == "enterprise":
            logging.info("Go to pages per sheet option menu")
            self.homemenu.menu_navigation(self.spice,JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, JobStorageAppWorkflowObjectIds.list_jobStorageSettings_pagesPerSheet, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
            assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_view_jobStorageSettings_pagesPerSheet)
        else:
            logging.info("Go to pages per sheet option menu")
            menu_item_id = [JobStorageAppWorkflowObjectIds.row_combo_jobStorageSettings_pagesPerSheet, JobStorageAppWorkflowObjectIds.combo_jobStorageSettings_pagesPerSheet]
            self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
            assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettings_pagesPerSheet)

    def select_pages_per_sheet_option(self, udw, option):
        #pagesPerSheet
        familyname = self.spice.copy_ui().check_familyname(udw)
        self.goto_pages_per_sheet(udw, familyname)

        if option == "1":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_pagesPerSheet_option_1 + " SpiceText")
            current_button.mouse_click()
        elif option == "2":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_pagesPerSheet_option_2 + " SpiceText")
            current_button.mouse_click()
        elif option == "4_rightThenDown":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_pagesPerSheet_option_4_rightThenDown + " SpiceText")
            current_button.mouse_click()
        elif option == "4_downThenRight":
            current_button = self.spice.query_item(JobStorageAppWorkflowObjectIds.combo_pagesPerSheet_option_4_downThenRight + " SpiceText")
            current_button.mouse_click()

        if familyname == "enterprise":
            back_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.list_view_jobStorageSettings_pagesPerSheet +" "+ JobStorageAppWorkflowObjectIds.button_back)
            back_button.mouse_click()

        assert self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, timeout = 9.0)
    
    def set_output_Bin(self, option):
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_output_destination_comboBox, JobStorageAppWorkflowObjectIds.output_destination_comboBox]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar)
        if option == "OutputBin1":
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.combo_outputBin_option_outputBin1)
        elif option == "OutputBin2":
            current_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.combo_outputBin_option_outputBin2)
        else:
            raise Exception(f"Invalid type <{option}>")

        current_button.mouse_click()

    def get_2_sided_option_status(self):
        """
        Get the option status of collate
        @return:
        """
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView)
        sides_toggle_btn_status = self.spice.query_item(JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_2Sided)["checked"]
        logging.info(f"The current status of collate is <{sides_toggle_btn_status}>")
        return sides_toggle_btn_status

    def set_settings_2sided(self,option):
        menu_item_id = [JobStorageAppWorkflowObjectIds.row_toggle_jobStorageSettings_2Sided, JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_2Sided]
        self.workflow_common_operations.goto_item(menu_item_id, JobStorageAppWorkflowObjectIds.view_jobStorageSettingsView, scrollbar_objectname = JobStorageAppWorkflowObjectIds.job_storage_options_scrollbar, select_option=False)
        is_2Sided_btn_checked = self.get_2_sided_option_status()
        Sided_toggle_btn = self.spice.wait_for(JobStorageAppWorkflowObjectIds.toggle_jobStorageSettings_2Sided + " MouseArea")

        if option == "off" and is_2Sided_btn_checked:
            logging.info("need to turn off 2sided option")
            Sided_toggle_btn.mouse_click()
        elif option == "on" and not is_2Sided_btn_checked:
            logging.info("need to turn on 2Sided option")
            Sided_toggle_btn.mouse_click()  
    
    def set_settings_auto_paper_color_removal(self, auto_paper_color_removal = True):
        '''
        UI should be on auto paper color removal checkbox in Scan settings screen.
        Args:
            auto_paper_color_removal: The auto paper color removal value to set - On / Off
        '''
            
        auto_paper_color_removal_switch_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.checkbox_autoPaperColorRemoval)
        if auto_paper_color_removal == "True":
            if auto_paper_color_removal_switch_button["checked"] is False:
                auto_paper_color_removal_switch_button.mouse_click()
                assert auto_paper_color_removal_switch_button["checked"] is True
              
        else:
            if auto_paper_color_removal_switch_button["checked"] is True:
                auto_paper_color_removal_switch_button.mouse_click()
                assert auto_paper_color_removal_switch_button["checked"] is False
        
        logging.info("auto paper color removal value changed to %s" % auto_paper_color_removal_switch_button)

    def job_storage_general_settings_method(self, job_storage_settings: Dict,udw):
        """
        This method is to set the job storage general settings
        :param job_storage_settings: Dict
        :return:
        """
        settings = {
        'copies': job_storage_settings.get('copies', None),
        'pagesPerSheet': job_storage_settings.get('pagesPerSheet', None),
        '2sided': job_storage_settings.get('2sided', None),
        'colorMode': job_storage_settings.get('colorMode', None),
        'contentType': job_storage_settings.get('contentType', None),
        'quality' : job_storage_settings.get('quality', None),
        'collate' : job_storage_settings.get('collate', None),
        'auto_paper_color_removal' : job_storage_settings.get('auto_paper_color_removal', None),
        'paper_selection': job_storage_settings.get('paper_selection', None),
        'contentOrientation': job_storage_settings.get('contentOrientation', None),
        'staple': job_storage_settings.get('staple', None),
        'sharpness':job_storage_settings.get('sharpness', None),
        'punch': job_storage_settings.get('punch', None),
        'fold': job_storage_settings.get('fold', None),
        'lighter_darker': job_storage_settings.get('lighter_darker', None),
        'contrast': job_storage_settings.get('contrast', None),
        'background_cleanup':job_storage_settings.get('background_cleanup', None),
        'blank_page_suppression': job_storage_settings.get('blank_page_suppression', None),
        'booklet': job_storage_settings.get('booklet', None),
        'outputBin': job_storage_settings.get('outputBin', None)
    }
        try:
            button = self.spice.query_item("#continueButton")
            button.mouse_click()
            self.spice.wait_for('#DetailPanel')
        except:
            logging.info("Continue button not found, trying to print directly")

        self.go_to_more_options()
        if settings['copies']!= None:
            self.ui_set_no_of_pages(settings['copies'])
        if settings['colorMode']!=None:
            self.select_color_mode(settings['colorMode'])
        if settings['quality']!=None:
            self.select_quality_option(settings['quality'])
        if settings['contentType']!=None:
            self.select_content_type(settings['contentType'])
        if settings['contentOrientation']!=None:
            self.set_content_orientation_settings(settings['contentOrientation'])
        if settings['staple']!=None:
            self.select_staple_option(settings['staple'])
        if settings['paper_selection'] != None:
            paper_size = settings['paper_selection'].get('paper_size', None)
            if paper_size:
                self.select_media_size_option(paper_size)
                self.go_back_to_setting_from_paper_selection()
            paper_tray = settings['paper_selection'].get('paper_tray', None)
            if paper_tray:
                self.go_to_paper_selection()
                self.select_paper_tray_option(paper_tray)
                self.go_back_to_setting_from_paper_selection()
            paper_type = settings['paper_selection'].get('paper_type', None)
            if paper_type:
                self.go_to_paper_selection()
                self.select_paper_type_option(paper_type)
                self.go_back_to_setting_from_paper_selection()
        if settings['sharpness'] != None:
                self.set_sharpness_setting_value(settings['sharpness'])
        if settings['punch'] != None:
            self.select_punch_option(settings['punch'])
        if settings['collate'] != None:
            self.change_collate(settings['collate'])
        if settings['fold'] != None:
            self.select_fold_option(settings['fold'])
        if settings['lighter_darker'] != None:
            self.set_lighter_darker_option(settings['lighter_darker'])
        if  settings['contrast'] != None:
            self.set_contrast_option(settings['contrast'])
        if settings['background_cleanup'] != None:
            self.set_background_cleanup_setting_value(settings['background_cleanup'])
        if settings['auto_paper_color_removal'] != None:
            self.goto_auto_paper_color_removal_option()
            self.set_settings_auto_paper_color_removal(settings['auto_paper_color_removal'])
        if settings['blank_page_suppression'] != None:
            self.select_blank_page_suppression(settings['blank_page_suppression'])
        if settings['booklet'] != None:
            self.select_booklet_option(settings['booklet'])
        if settings['pagesPerSheet'] != None:
            self.select_pages_per_sheet_option(udw,settings['pagesPerSheet'])
        if settings['outputBin'] != None:
            self.set_output_Bin(settings['outputBin'])
        if settings['2sided'] != None:
            self.set_settings_2sided(settings['2sided'])     
        
        close_button = self.spice.wait_for(ScanAppWorkflowObjectIds.button_close)
        close_button.mouse_click()
        self.spice.wait_for(JobStorageAppWorkflowObjectIds.job_list_view)
        
    def save_button_not_constrained(self):
        '''
        Checks if the save button in Job Storage is not constrained.
        Returns True if the save button is visible and not constrained, False otherwise.
        This can be used to verify if the user can proceed with saving to job storage.
        '''
        try:
            save_button = self.spice.wait_for(JobStorageAppWorkflowObjectIds.button_job_storage_save, timeout=9.0)
            self.spice.wait_until(lambda: save_button["constrained"] == False, timeout=9.0)
            return True
        except Exception as e:
            logging.info(f"Save button not constrained: {str(e)}")
            return False
        
    
