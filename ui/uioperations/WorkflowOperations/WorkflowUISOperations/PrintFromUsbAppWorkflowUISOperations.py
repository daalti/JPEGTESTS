from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowUICommonOperations import PrintFromUsbAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
import dunetuf.metadata as product_metadata
import logging
import time


class PrintFromUsbAppWorkflowUISOperations(PrintFromUsbAppWorkflowUICommonOperations):
    def __init__(self, spice):
        """
        PrintFromUsbAppUISOperations class to initialize print from usb options operations.
        @param spice:
        """
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.dial_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

        self.home_screen_view = PrintFromUsbAppWorkflowObjectIds.home_screen_view
        self.print_usb_app_view = PrintFromUsbAppWorkflowObjectIds.print_usb_app_view
        self.options_view = PrintFromUsbAppWorkflowObjectIds.options_view
        self.print_settings_view = PrintFromUsbAppWorkflowObjectIds.continue_button_locator
        self.paper_selection_settings_view = PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor
        self.select_file_view = PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view
        self.print_usb_no_content_ok_button = PrintFromUsbAppWorkflowObjectIds.print_usb_no_content_ok_button
        self.print_from_usb_button_locator = PrintFromUsbAppWorkflowObjectIds.print_from_usb_button_locator
        self.Print_from_usb_button_home_locator = PrintFromUsbAppWorkflowObjectIds.print_from_usb 

    def start_print(self, dial_value=0):
        """
        UI should be in USBPrint_PrintFromUSB.
        Navigates to Side screen starting from USBPrint_PrintFromUSB.
        UI Flow is click on print button
        On the XS/S screen, click the continue button - print button.
        @param dial_value:
        @return:
        """
        time.sleep(3) # make sure can click print button
        # sometimes cannot click print button
        button_locator = PrintFromUsbAppWorkflowObjectIds.continue_button_locator

        if (self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)["visible"] == True):
            button_locator = PrintFromUsbAppWorkflowObjectIds.continue_button_locator
        elif (self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.footer_detail_print_button_locator)["visible"] == True):
            button_locator = PrintFromUsbAppWorkflowObjectIds.footer_detail_print_button_locator

        for _ in range(5):
            self.spice.wait_for(button_locator).mouse_wheel(0, 0)

        self.workflow_common_operations.goto_item_navigation(button_locator, PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)

        if (button_locator == PrintFromUsbAppWorkflowObjectIds.continue_button_locator):
            self.start_print()

        logging.info("Click the print button to start printing")

    def check_spec_on_usb_print_print_from_usb(self, net):
        """
        check spec on Continue_PrintFromUSB
        The XS/S screen has a continue button instead of a print button.
        @param net:
        @return:
        """
        logging.info("check the str on Continue_PrintFromUSB screen")

        logging.info("check the string for Continue button")
        self.workflow_common_operations.verify_string(net, PrintFromUsbAppWorkflowObjectIds.continue_button_str_id, PrintFromUsbAppWorkflowObjectIds.continue_button_locator)

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
        
    def goto_options_menu(self):
        expend_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)
        expend_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator) # representative item in the expected view.
        time.sleep(1)
        scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.detail_panel_layout_scrollbar
        scrollbar_size = self.spice.query_item(scrollbar_objectname)["size"]
        self.workflow_common_operations.scroll_to_position_vertical(1 - scrollbar_size, scrollbar_objectname)
        mode_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_button_locator)
        mode_button.mouse_click()
        time.sleep(1)

    def set_no_of_copies(self, value):
        """
        Selects number of pages in USBPrint_PrintFromUSB screen based on user input
        @param value:
        @return:
        """
        # open continue button to show "Copies"
        continue_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)
        continue_button.mouse_click()

        numCopiesElement = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)
        numCopiesElement.__setitem__('value', value)

    def get_value_of_no_of_copies(self):
        """
        Get the copy number
        @return: int
        """
        expend_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)
        expend_button.mouse_click()

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)
        current_value = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator)["value"]
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        expend_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.back_button)
        expend_button.mouse_click()
        time.sleep(1)
        return current_value

    def goto_interactive_summary(self):
        continue_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)
        continue_button.mouse_click()
        wait_pages = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.numberOfCopies_locator) # representative item in the expected view.
        self.spice.wait_until(lambda: wait_pages["visible"] == True, 20)

    def check_quickset(self, title):
        continue_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)
        continue_button.mouse_click()
        time.sleep(1)
        
        quicksetItem = self.spice.wait_for(f"#{title}")
        quicksetItem.mouse_click()
        
        assert quicksetItem["focus"] == True, "select quickset failed"

    def collapse_print_setting(self):
        """
        Collapse print setting
        @return:
        """
        back_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.back_button)
        back_button.mouse_click()
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)

    def press_back_button_from_folder_view(self, screen_id, landing_view, index):
        if (self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.continue_button_locator)["visible"] != True):
            current_button= self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.back_button, 1)
            current_button.mouse_click()
        current_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.back_button, 1)
        current_button.mouse_click()

    def validate_print_app(self, udw, net, cdm, configuration, usbdevice):
        product_metadata_dict = product_metadata.get_product_metadata(cdm, configuration)
        device_functions = product_metadata_dict.get('DeviceFunction', [])
        jobstorage = 'JobStorage' in device_functions
        assert self.spice.wait_for("#c93bc831-99a8-454c-b508-236fc3a2a08f" + " #labelText",10)["text"] == str(LocalizationHelper.get_string_translation(net,"cRetrieveFromUSB", "en"))
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_from_usb) ["visible"] is True, 'Print from USB icon is not visible'
        assert self.spice.wait_for("#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42" + " #labelText",10)["text"] == str(LocalizationHelper.get_string_translation(net,"cQuickForms", "en"))
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.quick_forms_app) ["visible"] is True, 'QuickForms icon is not visible'
        if jobstorage == True:
            assert self.spice.wait_for("#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B" + " #labelText",10)["text"] == str(LocalizationHelper.get_string_translation(net,"cOpenFromDeviceMemory", "en"))
            assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.job_storage) ["visible"] is True, 'Job Storage icon is not visible'
