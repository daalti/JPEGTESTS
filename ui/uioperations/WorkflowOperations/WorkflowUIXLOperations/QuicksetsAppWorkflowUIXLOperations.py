from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowUICommonOperations import QuicksetsAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.WorkflowUICommonXLOperations import WorkflowUICommonXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.MenuAppWorkflowUIXLOperations import MenuAppWorkflowUIXLOperations
from dunetuf.ui.uioperations.WorkflowOperations.QuicksetsAppWorkflowObjectIds import QuicksetsAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.configuration import Configuration
from dunetuf.send.common.common import Common as ScanCommon
import logging, time

class QuicksetsAppWorkflowUIXLOperations(QuicksetsAppWorkflowUICommonOperations):
    
    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.workflow_common_operations = WorkflowUICommonXLOperations(self._spice)
        self.homemenu = MenuAppWorkflowUIXLOperations(self._spice)
    
    def select_quickset_from_menu_quicksetapp(self, quickset_name, quickset_type, start_option="user presses start", ana_sign_in_payload=None, pin=None, already_on_landing_view=False):
        """
        Select quickset by name at correspoding scan app landing veiw under quickset app
        @param quickset_name:
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param start_option:"user presses start"/"start automatically"
        @param pin, pin for quickset if set this option
        @param ana_sign_in_payload: some printer support sigin feature and should provide authorization when folder/sharepoint sign-in method is "Use credentials of the user currently signed in"
                                    > Please set it to None if you already sign in from Home screen/Don't handle ana sign in with this function
                                    > payload format {"admin":{"password":"12345678"}}/{"printer_user":{"username":"xxxx", "password":"xxx"}}/{"ldap":{"username":"xxxx", "password":"xxx"}}/{"windows":{"username":"xxxx", "password":"xxx"}}
        @param already_on_landing_view, will go to quicksetapp landing view from Home screen if False, could set it True if printer already on quicksetapp landing view
        @return:
        """
        assert quickset_type in ["email", "sharepoint", "usb", "folder", "copy"], "Please create quickser with quickset_type <email/sharepoint/usb/folder/copy>"
        assert start_option in ["user presses start", "start automatically"], 'Please take start_option from one of <"user presses start"/"start automatically">'

        if quickset_type == "email":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.email_landing_view
        elif quickset_type == "sharepoint":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.sharepoint_landing_view
        elif quickset_type == "usb":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.usb_landing_view
        elif quickset_type == "folder":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.folder_landing_view
        elif quickset_type == "copy":
            corresponding_app_landing_view_object = QuicksetsAppWorkflowObjectIds.copy_landing_view

        if not already_on_landing_view:
            self.goto_quicksetapp_landing_view(quickset_type)
        
        quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.quicksets_landing_page_view} #{quickset_name} MouseArea")
        self._spice.wait_until(lambda: quickset_item["visible"])
        time.sleep(1)
        quickset_item.mouse_click()
        logging.info(f"Success to select <{quickset_name}>")

        if ana_sign_in_payload and pin:
            raise Exception("Please don't provide ana_sign_in_payload and pin value at the same time, please just take one of them")

        if pin:
            if quickset_type == "folder":
                self._spice.network_folder.enter_quickset_pin(pin)
            elif quickset_type == "sharepoint":
                self._spice.sharepoint.enter_quickset_pin(pin)

        if ana_sign_in_payload:
            self._handle_ana_sign_in(ana_sign_in_payload, quickset_name, quickset_type, start_option)
            self.select_quickset_from_menu_quicksetapp(quickset_name, quickset_type, start_option=start_option, already_on_landing_view=True)
        
        if start_option == "user presses start":
            logging.info(f"The printer is in screen <{corresponding_app_landing_view_object}>")
            corresponding_app_landing_screen = self._spice.wait_for(corresponding_app_landing_view_object)
            self._spice.wait_until(lambda: corresponding_app_landing_screen["visible"])
            time.sleep(2)
            assert self.is_quickset_selected(quickset_name, quickset_type), f"The quickset <{quickset_name}> is not in selected status"

        elif start_option == "start automatically":
            logging.info(f"The quickset job <{quickset_name}> start automatically")

    def is_quickset_selected(self, quickset_name, quickset_type):
        """
        To check if quickset is selectded or not
        @param quickset_type: email/sharepoint/usb/folder
        @param quickset_name: should provide name when qs type is sharepoint
        @return:
        """
        is_selected = False

        if quickset_type == "email":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.email_landing_view} #{quickset_name}")
        elif quickset_type == "sharepoint":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.sharepoint_landing_view} #{quickset_name}")
        elif quickset_type == "usb":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.usb_landing_view} #{quickset_name}")
        elif quickset_type == "folder":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.folder_landing_view} #{quickset_name}")
        elif quickset_type == "copy":
            quickset_item = self._spice.wait_for(f"{QuicksetsAppWorkflowObjectIds.copy_landing_view} #{quickset_name}")

        is_selected = quickset_item["checked"]
        logging.info(f"The <{quickset_name}> is selected <{is_selected}>")
        return is_selected



    def perform_quickset_job_from_menu_quicksetapp(self,net, job, ews_quicksets_app, quickset_type, payload, ana_sign_in_payload=None, pin=None, pages=1, time_out=90, pdf_encryption_code=None):
        """
        Home screen -> Menu -> Quicksets app
        1. Create Corresponding quickset app from EWS - just set setting set in payload
        2. Check Corresponding quickset app setting via UI - just check setting set in payload
        3. Check Corresponding quickset app setting via CDM - just check setting set in payload
        4. Home screen -> Menu -> Quicksets app -> Corresponding app - > perform quickset job
        5. Wait for job complete
        @param net
        @param job
        @param ews_quicksets_app
        @param quickset_type:email/sharepoint/usb/folder/copy
        @param payload: please refer to structure from quickset_base_payload, scan_common_setting_payload and quickset_email_payload/quickset_sharepoint_payload/quickset_folder_payload from dunetuf.ews.copy_scan_ews_option_dict
        @param ana_sign_in_payload: some printer support sign in feature and should provide authorization when folder/sharepoint sign-in method is "Use credentials of the user currently signed in"
                                    > Please set it to None if you already sign in from Home screen/Don't handle ana sign in with this function
                                    > payload format {"admin":{"password":"12345678"}}/{"printer_user":{"username":"xxxx", "password":"xxx"}}/{"ldap":{"username":"xxxx", "password":"xxx"}}/{"windows":{"username":"xxxx", "password":"xxx"}} 
        @param pin: pin for quickset if set this option
        @param pages: set it when scan from Glass if scan Multi page 
        @param time_out: timeout to wait for job finish
        @param pdf_encryption_code: should provide code when pdf encryption is enabled 
        """
        logging.info(f"Perform quickset job from menu quicksetapp <{quickset_type}> <{payload}>")

        start_option = payload.get("start_option", None)
        wait_for_landing = True
        quickset_name = payload["name"]

        logging.info(f'create {quickset_type} quickset {payload["name"]} with ews')
        ews_quicksets_app.create_common_quicksets(quickset_type, payload)

        logging.info(f"check {quickset_type} quickset option value with UI")  
        short_cut_id = ews_quicksets_app.csc.get_shortcut_id(payload["name"])
        self.compare_ui_copy_scan_settings_with_created_quickset(net, quickset_type, payload, job=job, id=short_cut_id,  pin=pin, already_on_setting_screen=False)

        if quickset_type == "copy":
            self._spice.goto_homescreen()
    
        logging.info(f"check {quickset_type} quickset payload with cdm")
        ews_quicksets_app.csc.compare_cdm_copy_scan_settings_with_created_quickset(quickset_type, payload)

        self.select_quickset_from_menu_quicksetapp(quickset_name, quickset_type, start_option=start_option, ana_sign_in_payload=ana_sign_in_payload, pin=pin, already_on_landing_view=False)
        
        if start_option == "user presses start":
            self.start_quickset_job(quickset_type)
        
        elif start_option == "start automatically":
            logging.info(f"The quickset job <{quickset_name}> start automatically")
            wait_for_landing = False

        if quickset_type == "copy":
            self.media_mismatch_size_flow(net)
            self.wait_for_copy_quickset_job_to_complete(net, job, sides=payload.get("sides"), time_out=time_out)
        else:
            if pdf_encryption_code:
                self._handle_pdf_encryption_code(pdf_encryption_code)

            self.wait_for_scan_quickset_job_to_complete(net, job, quickset_type=quickset_type, pages=pages, time_out=time_out, wait_for_landing = wait_for_landing)



    def wait_for_scan_quickset_job_to_complete(self, net, job, quickset_type, pages=1, time_out=90, final_job_status="success", wait_for_landing: bool = True, is_expanded:bool = False):
        """
        @param quickset_type quickset_type:email/sharepoint/usb/folder
        """
        configuration = Configuration(self._spice.cdm)
        common_instance = ScanCommon(self._spice.cdm, self._spice.udw)
        scan_resource = common_instance.scan_resource()
        #prompt_for_additional_pages = common_instance.get_prompt_for_additional_pages(type = quickset_type)

        if scan_resource == "Glass": 
            try:
                for _ in range(pages-1):
                    scan_add_page_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page, timeout = 40.0)
                    self._spice.validate_button(scan_add_page_button)
                    scan_add_page_button.mouse_click()
                    time.sleep(2)

                scan_add_page_done_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_scan_add_page_done)
                logging.info("#finish button found")
                self._spice.validate_button(scan_add_page_done_button)
                scan_add_page_done_button.mouse_click()
            except TimeoutError:
                logging.info("flatbed Add page is not available")
        elif scan_resource == "MDF":
            if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
                # todo: need to add multiple page scene when bug DUNE-147017 fixed.
                self._spice.scan_settings.mdf_add_page_alert_done()
            elif configuration.productname == "jupiter" :
                for _ in range(pages-1):
                    is_expanded = self.is_landing_expanded(quickset_type)
                    if is_expanded:
                        self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_main_right_block, time_out)
                    else:
                        self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_detail_right_block, time_out)
                    self._spice.udw.mainApp.ScanMedia.loadMedia("MDF")
                
                #self.start_quickset_job(quickset_type, wait_for_landing)
                self._spice.scan_settings.wait_for_preview_n(1)
                
                if self.is_landing_expanded(quickset_type):
                    scan_done_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_main_right_block, time_out)
                else:
                    scan_done_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_detail_right_block, time_out)
                    assert scan_done_button

                self._spice.wait_until(lambda: scan_done_button["enabled"])
                scan_done_button.mouse_click()

        if quickset_type == "email":
            job_type = "scanEmail"
        elif quickset_type == "sharepoint":
            job_type = "scanSharePoint"
        elif quickset_type == "usb":
            job_type = "scanUsb"
        elif quickset_type == "folder":
            job_type = "scanNetworkFolder"
        
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm([{"type": job_type, "status": final_job_status}])
        # wait for status dismiss
        time.sleep(7)

    def back_to_back_jobs(self, net,folder_setting, ana_sign_in_payload, number_of_jobs=2):
        for job_index in range(number_of_jobs):
            self._spice.udw.mainApp.ScanMedia.loadMedia("MDF")
            self._spice.quickset_ui.select_quickset_from_menu_quicksetapp(
                folder_setting["name"], 
                "folder", 
                start_option=folder_setting["start_option"], 
                ana_sign_in_payload=ana_sign_in_payload if job_index == 0 else None
            )
            self._spice.wait_for(ScanAppWorkflowObjectIds.view_scan_network_folder_landing, timeout=10.0)
            self._spice.scan_settings.wait_for_preview_n(1, timeout=20)
            if job_index == 0:
                self._spice.scan_settings.wait_for_preview_window()
                self._spice.scan_settings.verify_preview_layout_header()
                back_button = self._spice.wait_for(ScanAppWorkflowObjectIds.back_button, timeout=10.0,query_index = 3)
                back_button.mouse_click()
            send_button = self._spice.wait_for(ScanAppWorkflowObjectIds.button_send_main_right_block, timeout=20.0)
            self._spice.validate_button(send_button)
            self._spice.wait_until(lambda: not send_button["constrained"])
            send_button.mouse_click()
            self._spice.wait_for(QuicksetsAppWorkflowObjectIds.quickset_menu_list_screen_view, timeout=10.0)
            home_button = self._spice.wait_for("#HomeButton")
            home_button.mouse_click()