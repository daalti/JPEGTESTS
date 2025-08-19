import time
from dunetuf.ui.uioperations.BaseOperations.IPrintFromUsbAppUIOperations import IPrintFromUsbAppUIOperations
from dunetuf.ui.uioperations.ProSelectOperations.ProSelectCommonOperations import ProSelectCommonOperations
from dunetuf.ui.uioperations.ProSelectOperations.MenuAppProSelectUIOperations import MenuAppProSelectUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
import logging
import dunetuf.metadata as product_metadata

class PrintFromUsbAppProSelectUIOperations(IPrintFromUsbAppUIOperations):
    # -------------------------------Function Keywords------------------------ #
    max_cancel_time = 60
    common_header = "#Header"
    common_back_loctor = "#BackButton"
    property_text = "text"
    property_value = "value"
    property_current_index = "currentIndex"
    property_active_focus = "activeFocus"
    property_count = "count"
    property_checked = "checked"
    spice_text_view = " SpiceText"
    home_screen_view = "#HomeScreenView"
    current_app_text = "#CurrentAppText"
    print_folder_guid = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAAD"
    usb_drive_app = "#USBDriveFolderGUID"

    # -----Home_Print
    print_from_usb_button_locator = "#c93bc831-99a8-454c-b508-236fc3a2a08f"

    # -----USBPrint_PrintFromUSBHome
    select_file_view = "#selectFileView"
    header_print_from_usb_locator = "#PrintSelectedDirectory"
    header_print_from_usb_str_id = "cRetrieveFromUSB"

    # -----USBPrint_PrintFromUSB
    print_settings_view = "#printSettingsView"
    print_select_settings_view="#printSelectSettingsView"
    spice_tumbler_view = "#SpiceTumblerView"
    print_button_locator = "#PrintButton"
    print_button_str_id = "cPrint"
    options_button_locator = "#OptionsButton"
    options_button_str_id = "cOptions"

    # -----usb_defect
    usb_no_file_str_id = "cUnableToFindFilesFolders"
    usb_defect_str_id = "cInsertUSBStorage"
    usb_defect_locator = "#DetailTexts"
    usb_defect_header_str_id = "cNoUSBInserted"
    usb_defect_header_locator = "#TitleText"
    print_usb_no_content_ok_button = "#printUsbNoContentOkButton"
    usb_cancel_button_str_id = "cCancel"
    usb_ok_button_str_id = "cOKButton"
    usb_cancel_button_locator = "#usbNoFrontDeviceCancelButton"

    usb_disconnected_button_locator = "#disconnectedUSBOkBtn"

    # ----Printing
    printing_view = "#printingView"
    printing_cancel_button = "#SystemProgressButton"
    select_printing_file_button = "#selectFileView #SpiceButton"

    # ---Print Done
    print_done_view = "#printDoneView"

    # ---USBPrint_Options
    menu_switch_2sided_str_id = "cPlexDuplex"
    options_view = "#MenuListprintUSBSettingsPage"
    options_header = "#MenuListprintUSBSettingsPage #Header"
    options_two_sided_menu_switch = "#printFromUSB_twoSidedMenuSwitch"

    option_color_menu_loctor = "#printFromUSB_colorMenuNameValue #NameText"
    option_color_button_loctor = "#printFromUSB_colorButton"

    print_usb_app_view = "#PrintUsbAppApplicationStackView"

    # collate_options
    options_collate_menu_switch = "#printFromUSB_collateMenuSwitch"

    # ---color option setting
    color_settings_view = "#MenuSelectionListprintFromUSB_color"
    color_settings_header_locator = "#MenuSelectionListprintFromUSB_color #Header"
    color_black_only_locator = "#monochrome"
    color_color_locator = "#option_color"
    color_color_str_id = "cColor"
    color_auto_detect_locator = "#option_autoDetect"
    color_auto_detect_str_id = "cAutomatic"
    color_grayscale_locator = "#option_grayscale"
    color_grayscale_str_id = "cChromaticModeGrayscale"

    # ---quality option setting
    quality_settings_view = "#MenuSelectionListprintFromUSB_quality"
    quality_settings_header_locator = "#MenuSelectionListprintFromUSB_quality #Header"

    quality_quality_str_id = "cQuality"
    quality_best_only_locator = "#option_best"
    quality_best_only_str_id = "cBestLabel"
    # quality_quality_locator = "#quality"
    quality_standard_locator = "#option_normal"
    quality_standard_str_id = "cStandard"

    # quality_options
    option_quality_menu_loctor = "#printFromUSB_qualityMenuNameValue #NameText"
    option_quality_button_loctor = "#printFromUSB_qualityButton"

    # paperselection
    paperSelection_str_id = "cPaperSelectTitle"
    option_paperSelection_menu_loctor= "#printPaperSelectionView #NameText"
    option_paperSelection_button_locator = "#printFromUSB_paperSelectionButton"
    paperSelection_settings_view = "#MenuListprintFromUSB_paperSelection"
    paperSelection_settings_header_locator = "#MenuListprintFromUSB_paperSelection #Header"

    # papertype
    option_paperType_menu_locator = "#printFromUSB_paperTypeMenuNameValue"
    option_paperType_button_locator = "#printFromUSB_paperTypeButton"
    paperType_settings_view = "#MenuSelectionListprintFromUSB_paperType"

    paperType_str_id = "cPaperType"
    paperType_locator = "#RadioButtonListLayout"
    paperType_plain_str_id = "cMediaTypeIdPlain"
    paperType_plain_locator = "#option_stationery"
    paperType_custom_str_id = "cMediaSizeCustom"
    paperType_custom_locator = "#option_custom"
    paperType_bond_locator = "#option_bond"
    paperType_any_type_locator = "#option_any"

    #paper_tray_options
    paper_tray1_str_id = ""
    paper_tray1_locator = "#option_tray-1"
    paper_tray2_str_id = ""
    paper_tray2_locator = "#option_tray-2"
    paper_tray3_str_id = ""
    paper_tray3_locator = "#option_tray-3"

    # paper_selection_options
    option_paper_selection_button_loctor = "#printFromUSB_paperSelectionButton"
    paper_selection_settings_view = "#MenuListprintFromUSB_paperSelection"
    option_paper_size_button_loctor = "#printFromUSB_paperSizeButton"
    option_paper_tray_button_loctor = "#printFromUSB_paperTrayButton"
    paper_size_settings_view = "#MenuSelectionListprintFromUSB_paperSize"
    paper_tray_settings_view ="#MenuSelectionListprintFromUSB_paperTray"

    # error_screen
    load_paper_error_view = "#mediaLoadFlow"
    media_mismatch_type_view = "#mediaMismatchTypeFlow"
    media_mismatch_size_view = "#mediaMismatchSizeFlow"
    ok_button_loctor = "#OK"
    cartridge_very_low_locator = "#MessageLayout #TitleText"
    cartridge_very_low_str_id = "cCartridgesVeryLow"

    paper_size_dict_str_id = {
        "custom": "cCustom",
        "a4_210x297_mm": "cMediaSizeIdA4",
        "letter_8_5x11_in": "cMediaSizeIdLetter"
    }

    paper_size_dict = {
        "envelope_a2": "#option_a2Envelope",
        "custom": "#option_custom",
        "a0": "#option_iso_a0_841x1189mm",
        "a1": "#option_iso_a1_594x841mm",
        "a2": "#option_iso_a2_420x594mm",
        "a3_297x420_mm": "#option_iso_a3_297x420mm",
        "a4_210x297_mm": "#option_iso_a4_210x297mm",
        "a5_148x210_mm": "#option_iso_a5_148x210mm",
        "a6_105x148_mm": "#option_iso_a6_105x148mm",
        "b2": "#option_iso_b2_500x707mm",
        "b3": "#option_iso_b3_353x500mm",
        "b4_jis_257x364mm": "#option_iso_b4_250x253mm",
        "envelop_b5_176x250mm": "#option_iso_b5_176x250mm",
        "envelope_c5_162x229mm": "#option_iso_c5_162x229mm",
        "envelope_c6_114x162mm": "#option_iso_c6_114_162mm",
        "envelope_dl_110x220mm": "#option_iso_dl_110x220",
        "b5_jis_182x257mm": "#option_jis_b5_182x257mm",
        "b6_jis_128x182mm": "#option_jis_b6_128x182mm",
        "japanese_envelope_chou_#3_120x235mm": "#option_jpn_chou3_120x235mm",
        "postcard_jis_100x148mm": "#option_jpn_hagaki_100x148mm",
        "double_postcard_jis_148x200mm": "#option_jpn_oufuku_148x200mm",
        "execuitive_7_25x10_5_in": "#option_na_executive_7_25x10_5in",
        "oficio_8_5x13_in": "#option_na_foolscap_8_5x13in",
        "letter_8inx10in": "#option_na_govt_letter_8x10in",
        "3x5_in": "#option_na_index_3x5_3x5in",
        "4x6_in": "#option_na_index_4x6_4x6in",
        "5x7_in": "#option_na_index_5x7_5x7in",
        "5x8_in": "#option_na_index_5x8_5x8in",
        "ledger_11x17_in": "#option_na_ledger_11x17in",
        "legal_8_5x14_in": "#option_na_legal_8_5x14in",
        "letter_8_5x11_in": "#option_na_letter_8.5x11in",
        "envelope_monarch_3_9x7_5_in": "#option_na_monarch_3_87x7_5in",
        "envelope_#10_4_1x9_5_in": "#option_na_number_10_4_125x9_5in",
        "oficio_216x340_mm": "#option_na_oficio_8_5x13_4in",
        "10x15cm": "#option_om_small_photo_100x150mm",
        "16k_184x260mm": "#option_prc_16k_184x260mm",
        "16k_195x270mm": "#option_prc_16k_195x270mm",
        "16k_197x273mm": "#option_roc_16k_7_75x10_75in"
    }

    def __init__(self, spice):
        """
        PrintFromUsbAppUIOperations class to initialize print from usb options operations.
        @param spice:
        """
        self._spice = spice
        self.dial_common_operations = ProSelectCommonOperations(self._spice)
        self.home_menu_dial_operations = MenuAppProSelectUIOperations(self._spice)

    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.home_menu_dial_operations.home_navigation(
            spice=self._spice,
            home_screen_view=self.home_screen_view,
            app_name="Print",
            current_app_text=self.current_app_text,
            property_text=self.property_text,
            max_cancel_time=self.max_cancel_time
        )

        if self.home_menu_dial_operations.get_product_name(self._spice.udw) == "zelus":
            assert self._spice.query_item(self.current_app_text)[self.property_text] != "Print", "Print icon is visible"
        else:
            assert self._spice.query_item(self.current_app_text)[self.property_text] == "Print"
            current_item = self._spice.query_item(self.print_folder_guid)
            current_item.mouse_click()
            logging.info("clicked on print icon on home screen")
            assert self._spice.wait_for("#nativeStackView #02FECD9A-7FE7-4797-AD15-8127DF2CFAAD #ButtonListLayout") ["visible"] is True,"Not entered into print screen"
            assert self._spice.wait_for("#ButtonListLayout #Header #Version1Text") ["text"] == "Print"
            logging.info("Entered into the Print screen")

    def check_joblog_from_ui(self, expected_list=[{"index": 2, "expect_value_list": ["Print from USB", "Success"]}]):
        """
        Check the job log from print ui under status menu
        @param expected_list:
        @return:
        """
        logging.info("Check the job log from UI")
        self._spice.print_from_usb.home_menu_dial_operations.goto_joblog(self._spice)

        for i, item in enumerate(expected_list):
            logging.info(f"Check index {i} and value is {item}")
            self._spice.wait_for("#jobLogView #SpiceButton", item.get("index"))
            actual_text = self._spice.query_item("#jobLogView #SpiceButton SpiceText", item.get("index"))["text"]

            for j in item.get("expect_value_list"):
                assert j in actual_text

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
        self._spice.homeMenuUI().menu_navigation(self._spice, "#ButtonListLayout", self.print_from_usb_button_locator)
        # todo: Global_Processing Screen is not shown currently, Loading screen is not yet implemented, hence its not shown in UI.

    def check_visible_print_from_usb(self):
        """
        Purpose: check if Print from USB under Print app is visible or not.
        Ui Flow: Home_Print -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return: isVisible
        """
        logging.info("[check_visible_print_from_usb]")
        isVisible = self._spice.homeMenuUI().check_menu_visible(self._spice, "#ButtonListLayout", self.print_from_usb_button_locator)
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
        self.dial_common_operations.verify_string(net, self.header_print_from_usb_str_id,
                                                  self.header_print_from_usb_locator)
        # todo: search/filter feature is not yet implemented.

    def select_print_file_or_folder_by_name(self, name: str, dial_value: int = 180):
        """
        UI should be in USBPrint_PrintFromUSBHome.
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        self.dial_common_operations.goto_item(f"#{name}", self.select_file_view, dial_value=dial_value)

    def check_spec_on_usb_print_print_from_usb(self, net):
        """
        check spec on USBPrint_PrintFromUSB
        @param net:
        @return:
        """
        logging.info("check the str on USBPrint_PrintFromUSB screen")

        logging.info("check the string for Print button")
        self.dial_common_operations.verify_string(net, self.print_button_str_id, self.print_button_locator)

        logging.info("check the string for Options button")
        self.dial_common_operations.verify_string(net, self.options_button_str_id, self.options_button_locator)

        # todo: Defaults and Quick Sets/Preview is not shown on screen, not implement

    def get_value_of_no_of_copies(self):
        """
        Get the copy number
        @return: int
        """
        current_value = self._spice.query_item(self.spice_tumbler_view)[self.property_current_index] + 1
        msg = f"Number of Copies value is: {current_value}"
        logging.info(msg)
        return current_value

    def set_no_of_copies(self, value):
        """
        Selects number of pages in USBPrint_PrintFromUSB screen based on user input
        @param value:
        @return:
        """
        dial_value = 0
        currentScreen = self._spice.wait_for(self.spice_tumbler_view)
        for i in range(5):
            currentScreen.mouse_wheel(0, 0)
            time.sleep(1)

        starttime = time.time()
        times_pent_waiting = 0

        while (self._spice.query_item(self.spice_tumbler_view)[
                   self.property_active_focus] == False and times_pent_waiting < self.max_cancel_time * 2):
            currentScreen.mouse_wheel(180, 180)
            times_pent_waiting = time.time() - starttime

        time.sleep(1)
        assert self._spice.query_item(self.spice_tumbler_view)[self.property_active_focus] == True

        current_value = self.get_value_of_no_of_copies()

        if (value != int(current_value)):
            if (value > int(current_value)):
                dial_value = 180

        currentButton = self._spice.wait_for(self.spice_tumbler_view)

        starttime = time.time()
        times_pent_waiting = 0

        currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)

        while (int(current_value) != int(value) and times_pent_waiting < self.max_cancel_time * (
        4 if value < 40 else 7)):
            time.sleep(1)
            currentButton.mouse_wheel(dial_value, dial_value)
            time.sleep(0.5)
            current_value = self.get_value_of_no_of_copies()
            times_pent_waiting = time.time() - starttime

        currentButton.mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
        time.sleep(1)
        assert int(current_value) == value, "Number of Copies setting is not successful"

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
        for _ in range(5):
            self._spice.wait_for(self.print_button_locator).mouse_wheel(0, 0)
        
        self.dial_common_operations.goto_item(self.print_button_locator, self.print_settings_view)
        logging.info("Click the print button to start printing")

    def wait_for_print_started_screen_displayed(self, timeout=60):
        """
        Wait for print started screen displayed
        @param timeout
        @return:
        """
        status = False

        for i in range(timeout):
            time.sleep(1)
            try:
                toast_message = self._spice.wait_for("#ToastInfoText")["text"]
            except:
                toast_message = "Does not capture the status"

            logging.info(f"current message is: <{toast_message}>")
            if "start" in toast_message.strip().lower():
                logging.info("start status")
                status = True
                break

        if not status:
            raise Exception("Timeout to find start status")

    def check_spec_on_usb_print_file(self, net):
        # todo: need to add method, currently not implement:DUNE-63181
        pass

    def wait_for_print_complete_successfully(self, net, timeout=300):
        """
        Wait for print job complete
        @param time_out:
        @return:
        """
        # todo: need to update this function after Job Status Toast Messages implement, at present using self.get_current_job_status("usbPrint") to check job complete
        # self._spice.wait_for(self.print_done_view, time_out)
        # start_obj = "#ToastInfoText"
        # self._spice.wait_for(start_obj, 10)

        job_info_url = self.get_current_job_url("usbPrint")

        if job_info_url:
            current_job_status = self.get_current_job_status(job_info_url)

            while current_job_status != "completed" and timeout > 0:
                time_out = timeout - 1
                time.sleep(1)
                current_job_status = self.get_current_job_status(job_info_url)

            assert current_job_status == "completed", f"Print job is not complete in time {timeout}"
            logging.info("print job finished")
        else:
            logging.warning("Failed to get job status from job queue, will check it with job history")

    def wait_for_print_status(self, net, job, message:str = "complete", timeout=300, specific_str_checked=False):
        if message == "complete":
            self.wait_for_print_complete_successfully(net, timeout)
        else:
            raise Exception("wait for print status: \"{}\" Not implement yet for ProSelect".format(message))
        
    def goto_options_menu(self):
        """
        Go to options menu
        @return:
        """
        logging.info("Go to options menu")
        self.dial_common_operations.goto_item(self.options_button_locator, self.print_settings_view)

    def check_spec_on_usb_print_options(self, net, two_sided=None,color=None, quality=None, 
                                        paper_selection=None, collate=None):
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
        self.dial_common_operations.verify_string(net, self.options_button_str_id, self.options_header)
        self.dial_common_operations.verify_string(net, self.quality_quality_str_id,self.option_quality_menu_loctor)
        self.dial_common_operations.verify_string(net, self.color_color_str_id,self.option_color_menu_loctor)
        # "cPlexDuplex is not a valid String id"
        # self.dial_common_operations.verify_string(net, self.menu_switch_2sided_str_id, self.options_two_sided_menu_switch)
        self.dial_common_operations.verify_string(net, self.paperSelection_str_id, self.option_paperSelection_menu_loctor)
        logging.info("verify the back button existed")
        self._spice.wait_for(self.common_back_loctor, 3)

        if(two_sided):
            logging.info("check 2sided options spec")
            assert ("on" if self.get_copy_2sided_options_status() else "off") == two_sided
        if(collate):
            logging.info("check collate status spec")
            assert ("on" if self.get_collate_options_status() else "off") == collate
        if(color):
            logging.info("check color options spec")
            assert self.get_color_options() == color
        if(quality):
            logging.info("check quality otpions spec")
            assert self.get_quality_options() == quality
        if(paper_selection):
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
        self._spice.wait_for(self.options_view)
        is_2sided_options_checked = self._spice.query_item(self.options_two_sided_menu_switch)[self.property_checked]
        return is_2sided_options_checked

    def set_copy_2sided_options(self, two_sided_options="off"):
        """
        Set the status of 2side option
        @param two_sided_options:str -> on/off
        @return:
        """
        self._spice.wait_for(self.options_view)
        msg = f"Set 2sided_options to {two_sided_options}"
        logging.info(msg)
        is_2sided_options_checked = self.get_copy_2sided_options_status()

        active_item = self._spice.query_item(self.options_two_sided_menu_switch)
        self.dial_common_operations.goto_item(self.options_two_sided_menu_switch, self.options_view,
                                              select_option=False)

        if two_sided_options == "off" and is_2sided_options_checked:
            logging.info("need to turn off 2 sided option")
            active_item.mouse_click()
            time.sleep(1)

        if two_sided_options == "on" and not is_2sided_options_checked:
            logging.info("need to turn on 2 sided option")
            active_item.mouse_click()
            time.sleep(1)

        if two_sided_options == "off":
            assert not self.get_copy_2sided_options_status(), f"Failed to set copy_2sided_options: {two_sided_options}"
        else:
            assert self.get_copy_2sided_options_status(), f"Failed to set copy_2sided_options: {two_sided_options}"

    def get_color_options(self):
        """
        Get the color option
        @return:
        """
        self._spice.wait_for(self.options_view)
        current_color_option = self.dial_common_operations.get_actual_str(self.option_color_button_loctor)
        logging.info("Current color settings is: " + current_color_option)
        return current_color_option

    def goto_color_options_menu(self):
        """
        Go to color option menu
        @return:
        """
        logging.info("Go to color option menu")
        self.dial_common_operations.goto_item(self.option_color_button_loctor, self.options_view)
        self._spice.wait_for(self.color_settings_view)

    def check_spec_on_usb_print_options_color(self, net):
        """
        Check spec on USBPrint_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on USBPrint_OptionsColor")
        logging.info("check the string about Color, (Automatic, color, Grayscale)")
        self.dial_common_operations.verify_string(net, self.color_color_str_id, self.color_settings_header_locator)
        self.dial_common_operations.verify_string(net, self.color_color_str_id, self.color_color_locator)
        self.dial_common_operations.verify_string(net, self.color_auto_detect_str_id, self.color_auto_detect_locator)
        self.dial_common_operations.verify_string(net, self.color_grayscale_str_id, self.color_grayscale_locator)
        logging.info("verify the back button existed")
        self._spice.wait_for(self.common_back_loctor, 4)

    def set_color_options(self, net, color_options="color", locale: str = "en-US"):
        """
        Set the color option
        @param net:
        @param color_options: str -> color/auto/grayscale
        @param locale:
        @return:
        """
        logging.info("Set the color option to: " + color_options)

        color_options_dict = {
            "color": self.color_color_locator,
            "auto": self.color_auto_detect_locator,
            "grayscale": self.color_grayscale_locator
        }

        str_id_dict = {
            "color": self.color_color_str_id,
            "auto": self.color_auto_detect_str_id,
            "grayscale": self.color_grayscale_str_id
        }

        to_select_item = color_options_dict.get(color_options)
        str_id = str_id_dict.get(color_options)

        for i in range(5):
            self._spice.wait_for(self.color_settings_view).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.color_settings_view)
        time.sleep(1)
        current_color_options = self.get_color_options()

        assert current_color_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net, str_id,
                                                                                                           locale), f"failed to set color options {color_options}"

    def get_collate_options_status(self):
        """
        Get collate option status
        @return:
        """
        logging.info("Get collate option status")
        self._spice.wait_for(self.options_view)
        time.sleep(1)
        is_collate_options_checked = self._spice.query_item(self.options_collate_menu_switch)[self.property_checked]
        logging.info(f"Current collate option is: {is_collate_options_checked}")
        return is_collate_options_checked

    def set_collate_options(self, collate_options="off"):
        """
        Set collate option
        @param collate_options:str -> on/off
        @return:
        """
        logging.info(f"Set Collate_options to {collate_options}")
        self._spice.wait_for(self.options_view)
        collate_options_checked = self.get_collate_options_status()

        active_item = self._spice.query_item(self.options_collate_menu_switch)
        self.dial_common_operations.goto_item(self.options_collate_menu_switch, self.options_view, select_option=False)

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
        self._spice.wait_for(self.options_view)
        current_quality_option = self.dial_common_operations.get_actual_str(self.option_quality_button_loctor)
        logging.info("Current quality settings is: " + current_quality_option)
        return current_quality_option

    def goto_quality_options_menu(self):
        """
        Go to quality option menu
        @return:
        """
        logging.info("Go to quality option menu")
        self.dial_common_operations.goto_item(self.option_quality_button_loctor, self.options_view)
        self._spice.wait_for(self.quality_settings_view)

    def check_spec_usb_print_options_quality(self, net):
        """
        check spec on USBPrint_OptionsQuality
        @param net:
        @return:
        """
        logging.info("check check on USBPrint_OptionsQuality")
        logging.info("check the string about quality, (Best, Draft, Standard)")
        self.dial_common_operations.verify_string(net, self.quality_quality_str_id,
                                                  self.quality_settings_header_locator)
        self.dial_common_operations.verify_string(net, self.quality_best_only_str_id, self.quality_best_only_locator)
        self.dial_common_operations.verify_string(net, self.quality_standard_str_id, self.quality_standard_locator)
        logging.info("verify the back button existed")
        self._spice.wait_for(self.common_back_loctor, 4)

    def set_quality_options(self, net, quality_options="standard", locale: str = "en-US"):
        """
        Set quality option
        @param net:
        @param quality_options:str -> best/standard/draft
        @param locale:
        @return:
        """
        logging.info("Set the quality option to: " + quality_options)
        self.dial_common_operations.goto_item(self.option_quality_button_loctor, self.options_view)

        quality_options_dict = {
            "best": self.quality_best_only_locator,
            "standard": self.quality_standard_locator
        }

        str_id_dict = {
            "best": self.quality_best_only_str_id,
            "standard": self.quality_standard_str_id
        }

        to_select_item = quality_options_dict.get(quality_options)
        str_id = str_id_dict.get(quality_options)

        for i in range(3):
            self._spice.wait_for(self.quality_settings_view).mouse_wheel(0, 0)
            time.sleep(1)

        self.dial_common_operations.goto_item(to_select_item, self.quality_settings_view)

        time.sleep(1)
        current_quality_options = self.get_quality_options()

        assert current_quality_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net,
                                                                                                             str_id,
                                                                                                             locale), f"failed to set color options {quality_options}"

    def get_paper_selection_options(self):
        """
        Get paper selection option
        @return:
        """
        self._spice.wait_for(self.options_view)
        current_paperSelection_option = self.dial_common_operations.get_actual_str(
            self.option_paperSelection_button_locator)
        logging.info("Current paperSelection settings is: " + current_paperSelection_option)
        return current_paperSelection_option

    def get_paper_type_options(self):
        """
        Get paper type option
        @return:
        """
        self._spice.wait_for(self.options_view)
        current_paperType_option = self.dial_common_operations.get_actual_str(self.option_paperType_button_locator)
        logging.info("Current paper type settings is: " + current_paperType_option)
        return current_paperType_option

    def goto_usb_print_options_paper_type(self):
        """
        Go to USBPrint_OptionsPaperType from USBPrint_OptionsPaperSelection screen
        @return:
        """
        logging.info("Go to paper type option menu")
        self.dial_common_operations.goto_item(self.option_paperType_button_locator, self.options_view)
        self._spice.wait_for(self.paperType_settings_view)

    def check_spec_usb_print_options_paper_type(self, net):
        """
        Check spec on USBPrint_OptionsPaperType
        @param net:
        @return:
        """
        logging.info("check the spec on USBPrint_OptionsPaperType")
        logging.info("check the string for paperType options")
        logging.info("check the string about paperType, (Plain, Custom)")
        self.dial_common_operations.verify_string(net, self.paperType_str_id, self.paperType_locator)
        self.dial_common_operations.verify_string(net, self.paperType_plain_str_id, self.paperType_plain_locator)
        self.dial_common_operations.verify_string(net, self.paperType_custom_str_id, self.paperType_custom_locator)
        # todo: back button?
        # logging.info("verify the back button existed")
        # self._spice.wait_for("#BackButton", 4)

    def set_paper_type_options(self, net, paperType_options="Plain", locale: str = "en-US"):
        """
        Set paper type option
        @param net:
        @param paperType_options: str -> Plain/Custom
        @param locale:
        @return:
        """
        # todo:need to update function
        logging.info("Set the paperType option to: " + paperType_options)
        self.scroll_to_back_button(screen_id=self.paperSelection_settings_view, index=4)
        self.dial_common_operations.goto_item(self.option_paperType_button_locator, self.paperSelection_settings_view)

        paperType_options_dict = {
            "Plain": self.paperType_plain_locator,
            "Custom": self.paperType_custom_locator,
            "Prepunched": "#prepunched"
        }

        str_id_dict = {
            "Plain": self.paperType_plain_str_id,
            "Custom": self.paperType_custom_str_id,
        }

        to_select_item = paperType_options_dict.get(paperType_options)
        str_id = str_id_dict.get(paperType_options)

        self.scroll_to_back_button(screen_id=self.paperType_settings_view, index=5)

        self.dial_common_operations.goto_item(to_select_item, self.paperType_settings_view)

        # todo Need related String IDs for check

        #time.sleep(10)
        #current_paperType_options = self.get_paper_type_options()

        # assert current_paperType_options == self.dial_common_operations.get_expected_translation_str_by_str_id(net,
        #                                                                                                        str_id,
        #                                                                                                        locale), f"failed to set paperType options {paperType_options}"

    def goto_usb_print_options_paper_selection(self):
        """
        Goto USBPrint_OptionsPaperSelection from USBPrint_Options
        @return:
        """
        logging.info("Goto USBPrint_OptionsPaperSelection from USBPrint_Options")
        self.dial_common_operations.goto_item(self.option_paper_selection_button_loctor, self.options_view)
        self._spice.wait_for(self.paper_selection_settings_view)

    def goto_usb_print_options_paper_size(self):
        """
        Go to USBPrint_OptionsPaperSize from SBPrint_OptionsPaperSelection screen
        @return:
        """
        logging.info("Go to USBPrint_OptionsPaperSize from SBPrint_OptionsPaperSelection screen")
        self.dial_common_operations.goto_item(self.option_paper_size_button_loctor, self.paper_selection_settings_view)
        view = self._spice.wait_for(self.paper_size_settings_view)
        self._spice.wait_until(lambda: view['visible'] is True, 20)
        time.sleep(5)

    def set_paper_size_options(self, paper_size_options="a4_210x297_mm"):
        """
        Set paper size
        @param paper_size_options:
        @return:
        """
        self.scroll_to_back_button(screen_id=self.paper_size_settings_view, index=5)

        to_select_item = self.paper_size_dict.get(paper_size_options)

        self.dial_common_operations.goto_item(to_select_item, self.paper_size_settings_view)
    
    def check_spec_scan_to_usb_global_insert_usb(self, net):
        """
        Check ScanToUSB_GlobalInsertUSB
        @param net:
        @return:
        """
        logging.info("Check spec on ScanToUSB_GlobalInsertUSB")
        logging.info("verify the header messages")
        self.dial_common_operations.verify_string(net, self.usb_defect_header_str_id, self.usb_defect_header_locator)

        logging.info("verify the body messages")
        self.dial_common_operations.verify_string(net, self.usb_defect_str_id, self.usb_defect_locator)

        logging.info("verify the  cancel button messages")
        self.dial_common_operations.verify_string(net, self.usb_cancel_button_str_id, self.usb_cancel_button_locator)

    def select_scan_to_usb_global_insert_usb_cancel_button(self):
        """
        Select ScanToUSB_GlobalInsertUSB cancel button
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        self._spice.query_item(self.usb_cancel_button_locator).mouse_click()
        self._spice.wait_for(self.print_from_usb_button_locator)

    def check_usb_print_disconnected_message_button(self):
        """
        Check if PrintFromUSB disconnected message and button are visible
        @param:
        @return:
        """
        logging.info("Press the Cancel button")
        self._spice.query_item(self.usb_disconnected_button_locator).mouse_click()
        self._spice.wait_for(self.usb_disconnected_button_locator)

    def check_spec_usb_print_no_file_found(self, net):
        """
        Check spec USBPrint_NoFileFound
        @param net:
        @return:
        """
        logging.info("check the spec on USBPrint_NoFileFound")
        self.dial_common_operations.verify_string(net, self.usb_no_file_str_id, self.usb_defect_locator)
        self.dial_common_operations.verify_string(net, self.usb_ok_button_str_id, self.print_usb_no_content_ok_button)

    def cancel_current_print_job_by_click_cancel_button(self):
        """
        Click cancel button during printing process
        @return:
        """
        logging.info("Click cancel button during printing process")
        self._spice.query_item(self.printing_cancel_button).mouse_click(button=self._spice.MOUSE_BTN.MIDDLE)
    
    def select_print_file_or_folder_by_property_text(self, file_name, timeout_val=300):
        """
        Select file or folder by property text
        @param file_name:
        @return
        """
        self.scroll_to_back_button(screen_id=self.select_file_view, index=1)
        count = 0
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        find = False
        while time_spent_waiting < timeout_val:
            try:
                current_button = self._spice.query_item(self.select_printing_file_button, count)
                if current_button["text"] == file_name and current_button["activeFocus"]:
                    self._spice.query_item(self.select_printing_file_button, count).mouse_click()
                    time.sleep(2)
                    find = True
                    break
                else:
                    self._spice.query_item(self.select_printing_file_button).mouse_wheel(180, 180)
            except Exception as err:
                logging.info(str(err))
            
            count = count + 1
        
        if not find:
            raise Exception(f"Failed to select file or folder by property text: {file_name}")
            
    def scroll_to_back_button(self, screen_id, index: int = 0, timeout_val: int = 120):
        """
        scroll_to_back_button
        @param screen_id:
        @param index:
        @param timeout_val:
        @return:
        """
        current_screen = self._spice.wait_for(screen_id)
        self._spice.wait_until(lambda: current_screen["visible"] is True, 10)
        # so many item need to loading
        time.sleep(3)
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        while (self._spice.query_item(self.common_back_loctor, index)[self.property_active_focus] is False and time_spent_waiting < timeout_val):
            current_screen.mouse_wheel(0, 0)
            time_spent_waiting = time.time() - start_time
        time.sleep(1)

        assert self._spice.query_item(self.common_back_loctor, index)[self.property_active_focus], "Back button is not in focus"
    

    def wait_for_print_cancel_successfully(self, time_out=300):
        """
        Wait for print job complete
        @param time_out:
        @return:
        """
        flag = False

        while time_out and not flag :
            time.sleep(1)
            time_out = time_out - 1
            try:
                self._spice.query_item(self.printing_view)
            except:
                flag = True
            
        if not flag:
            raise Exception("Timeout to wait job cancel")
        
        self._spice.wait_for(self.print_settings_view)
            
    def goto_usb_print_options_paper_tray(self):
        """
        Go to USBPrint_OptionsPaperTray from USBPrint_OptionsPaperSelection screen
        @return:
        """
        logging.info("Go to USBPrint_OptionsPaperTray from USBPrint_OptionsPaperSelection screen")
        self.dial_common_operations.goto_item(self.option_paper_tray_button_loctor, self.paper_selection_settings_view)
        self._spice.wait_for(self.paper_tray_settings_view)

    def set_paper_tray_options(self, net, paper_tray_options="tray1"):
        """
        Set paper tray
        @param tray_options:
        @return:
        """
        logging.info("Set the paper_tray option to: " + paper_tray_options)
        paper_tray_dict = {
            "tray1": self.paper_tray1_locator,
            "tray2": self.paper_tray2_locator,
            "tray3": self.paper_tray3_locator,
        }
        for i in range(len(paper_tray_dict)):
            self._spice.wait_for(self.paper_tray_settings_view).mouse_wheel(0, 0)
            time.sleep(1)

        to_select_item = paper_tray_dict.get(paper_tray_options)

        self.dial_common_operations.goto_item(to_select_item, self.paper_tray_settings_view)

    def get_current_job_url(self, current_job_type):
        # todo: need to move this function into job.py since this function in other branch and wait for merge into default
        logging.info("To get the current active print job status from CDM")
        job_queue = self._spice.cdm.get(self._spice.cdm.JOB_QUEUE_ENDPOINT)
        job_list = job_queue.get("jobList")
        job_info_url = None
        
        get_job_queue_time_out = 20
        while len(job_list) == 0 and get_job_queue_time_out > 0:
            get_job_queue_time_out = get_job_queue_time_out - 1
            time.sleep(1)
            job_queue = self._spice.cdm.get(self._spice.cdm.JOB_QUEUE_ENDPOINT)
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
        current_job_info = self._spice.cdm.get(job_info_url)
        logging.info(f'Current job id is {current_job_info["jobId"]}, status is: {current_job_info["state"]}')
        return current_job_info["state"]

    def check_cartridge_very_low_screen(self, net, locale: str = "en-US"):
        self.dial_common_operations.verify_string(net, self.cartridge_very_low_str_id, self.cartridge_very_low_locator, locale)

    def go_back_to_print_from_options(self):
        self.dial_common_operations.back_button_press(self.options_view, self.print_settings_view, 3)

    def go_back_to_options_from_paper_selection(self):
        self.dial_common_operations.back_button_press(self.paper_selection_settings_view, self.options_view, 4)

    def press_back_button_from_folder_view(self, screen_id, landing_view, index):
        self.dial_common_operations.back_button_press(screen_id, landing_view, index)

    def validate_print_app(self, udw, net, cdm, configuration, usbdevice):
        product_metadata_dict = product_metadata.get_product_metadata(cdm, configuration)

        try:
            print_from_usb = 'PrintFromUsb' in product_metadata_dict['DeviceFunction']
        except:
            print_from_usb = False

        try:
            print_from_job_storage = 'JobStorage' in product_metadata_dict['DeviceFunction']
        except:
            print_from_job_storage = False

        currentElement = self._spice.wait_for("#ButtonListLayout")

        if (print_from_usb == True):
            assert self._spice.wait_for("#c93bc831-99a8-454c-b508-236fc3a2a08f #SpiceButton #ContentItemText")["text"] == str(LocalizationHelper.get_string_translation(net,"cRetrieveFromUSB", "en"))
            assert self._spice.wait_for("#c93bc831-99a8-454c-b508-236fc3a2a08f",20) ["visible"] is True, 'Print from USB icon is not visible'
            currentElement.mouse_wheel(180,180)

        if (print_from_job_storage == True):
            assert self._spice.wait_for("#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B #SpiceButton #ContentItemText")["text"] == str(LocalizationHelper.get_string_translation(net,"cOpenFromDeviceMemory", "en"))
            assert self._spice.wait_for("#86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B") ["visible"] is True, 'Job Storage icon is not visible'
            currentElement.mouse_wheel(180,180)

        assert self._spice.wait_for("#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42 #SpiceButton #ContentItemText")["text"] == str(LocalizationHelper.get_string_translation(net,"cQuickForms", "en"))
        assert self._spice.wait_for("#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42") ["visible"] is True, 'Quick Forms icon is not visible'

    def navigate_homescreen(self, navigate_to_app, button):
        self._spice.goto_homescreen()
        current_screen = self._spice.wait_for(self.home_screen_view)
        starttime = time.time()
        time_spent_waiting = 0

        while (self._spice.query_item(self.current_app_text)[
                   self.property_text] != navigate_to_app and time_spent_waiting < self.max_cancel_time):
            current_screen.mouse_wheel(180, 180)
            time_spent_waiting = time.time() - starttime

        app = self._spice.wait_for(button)
        app.mouse_click()

    def home_print_from_usb_has_lock_icon(self):
        """
        Starting from Home Screen
        """
        self.navigate_homescreen("Print", self.print_folder_guid)
        print_from_usb_lock_icon_id = self.print_from_usb_button_locator + " #ContentItem SpiceImage"
        lock_icon = self._spice.wait_for(print_from_usb_lock_icon_id)

        return lock_icon["width"] > 0

    def usb_print_from_usb_has_lock_icon(self):
        """
        Starting from Home Screen
        """
        #Check other places for lock icon where print from usb is located
        self.home_print_from_usb_has_lock_icon()
        
        self.navigate_homescreen("USB Drive", self.usb_drive_app)
        print_from_usb_lock_icon_id = self.print_from_usb_button_locator + " #ContentItem SpiceImage"
        lock_icon = self._spice.wait_for(print_from_usb_lock_icon_id)

        return lock_icon["width"] > 0

    def has_lock_icon(self):
        """
        Starting from Home Screen
        """
        #Check other places for lock icon where print from usb is located
        self.usb_print_from_usb_has_lock_icon()

        self.home_menu_dial_operations.goto_menu_print(self._spice)
        print_from_usb_lock_icon_id = self.print_from_usb_button_locator + "MenuButton #ContentItem SpiceImage"
        lock_icon = self._spice.wait_for(print_from_usb_lock_icon_id)

        return lock_icon["width"] > 0

    def validate_print_app_cancel(self):
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView")
        self.dial_common_operations.goto_item("#test1.pdf",screen_id="#PrintUsbAppApplicationStackView")
        time.sleep(2)
        self.dial_common_operations.goto_item("#PrintButton",screen_id="#printSettingsView",dial_value=0)
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView #PrintUsbProgressView #Cancel")["visible"] == True
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView #Dismiss")["visible"] == True
        self._spice.query_item("#PrintUsbAppApplicationStackView #PrintUsbProgressView #Cancel").mouse_click()
        assert self._spice.wait_for("#ToastInfoText")["text"] == "Canceling"
        time.sleep(3)
        self.dial_common_operations.goto_item("#test1.pdf",screen_id="#PrintUsbAppApplicationStackView")
        self.dial_common_operations.goto_item("#PrintButton",screen_id="#printSettingsView",dial_value=0)
        Dismiss = self._spice.wait_for("#PrintUsbAppApplicationStackView #Dismiss")
        Dismiss.mouse_wheel(180,180)
        Dismiss.mouse_click()

    def validate_print_app_multiple_job_cancel(self):
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView")
        self.dial_common_operations.goto_item("#test2.pdf",screen_id="#PrintUsbAppApplicationStackView")
        time.sleep(2)
        self.dial_common_operations.goto_item("#PrintButton",screen_id="#printSettingsView",dial_value=0)
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView #PrintUsbProgressView #Cancel")["visible"] == True
        assert self._spice.wait_for("#PrintUsbAppApplicationStackView #Dismiss")["visible"] == True
        Dismiss = self._spice.wait_for("#PrintUsbAppApplicationStackView #Dismiss")
        Dismiss.mouse_wheel(180,180)
        Dismiss.mouse_click()
        backbutton = self._spice.wait_for("#PrintUsbAppApplicationStackView")
        backbutton.mouse_wheel(0,0)
        backbutton.mouse_wheel(0,0)
        backbutton.mouse_wheel(0,0)
        backbutton.mouse_wheel(0,0)
        backbutton.mouse_wheel(0,0)
        backbutton.mouse_wheel(0,0)
        self._spice.wait_for("#BackButton SpiceText").mouse_click()
        self.dial_common_operations.goto_item("#test1.pdf",screen_id="#PrintUsbAppApplicationStackView")
        self.dial_common_operations.goto_item("#PrintButton",screen_id="#printSettingsView",dial_value=0)
        self._spice.query_item("#PrintUsbAppApplicationStackView #PrintUsbProgressView #Cancel").mouse_click()
        assert self._spice.wait_for("#StatusView")["visible"] == True
        self._spice.wait_for("#StatusView").mouse_click()
        self._spice.wait_for("#Cancel").mouse_click()
