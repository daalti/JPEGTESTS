
import logging
from time import sleep
from typing import ClassVar

from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowUICommonOperations import CopyAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations

import dunetuf.common.commonActions as CommonActions
from dunetuf.localization.LocalizationHelper import LocalizationHelper

class CopyAppWorkflowUIXLOperations(CopyAppWorkflowUICommonOperations):

    WAIT_TIMEOUT: ClassVar[float] = 7
    """Default wait timeout (s)."""

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)

    def copy_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        is_landing_expanded = self.is_landing_expanded(spice)

        if(is_landing_expanded):
            spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.button_startCopy_mainpanel, timeout)
            spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.button_startCopy_mainpanel)
        else:
            spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.copy_button, timeout)
            spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.copy_button)

    def wait_for_copy_landing_view(self):
        '''
        Method to wait for copy landing view plenty prepared to work
        '''
        copy_landing = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        self.are_quicksets_visible(self.spice)

        # Check settings is enable and visible
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen + " " + CopyAppWorkflowObjectIds.button_copyMoreOptions, timeout = 10)
        assert setting_view
        self.spice.wait_until(lambda: setting_view["enabled"], timeout = 15.0)
        self.spice.wait_until(lambda: setting_view["visible"], timeout = 15.0)
        logging.info("Inside Copy Successful Screen")

    def wait_for_copy_landing_view_from_widget_or_one_touch_quickset(self):
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        logging.info("Inside Copy Successful Screen")

    def wait_and_click_done_button_of_main_panel(self, spice, cdm, timeout: float = WAIT_TIMEOUT):
        """
        Waits and clicks until main button of copy app is DONE. Useful for sync waiting until acquisition finishes.
        So, timeout can be increased depending of size of acquired plot size.
        Pay attention: this function is only valid when landing is expanded (main_panel),
        because if collapsed main button has different objectname
        """
        expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, self.spice.copy_app.locators.done_string_id_button)
        self.spice.copy_app.wait_until_text_button(CopyAppWorkflowObjectIds.button_startCopy_mainpanel, expected_copy_text_button)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy_mainpanel)
        current_button.mouse_click()

    def wait_and_click_copy_button_of_main_panel(self, spice, cdm, timeout: float = WAIT_TIMEOUT):
        """
        Waits and clicks until main button of copy app is COPY. Useful for sync waiting until acquisition finishes.
        So, timeout can be increased depending of size of acquired plot size.
        Pay attention: this function is only valid when landing is expanded (main_panel),
        because if collapsed main button has different objectname
        """
        expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, self.spice.copy_app.locators.copy_string_id_button)
        self.spice.copy_app.wait_until_text_button(CopyAppWorkflowObjectIds.button_startCopy_mainpanel, expected_copy_text_button)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy_mainpanel)
        current_button.mouse_click()

    def is_landing_expanded(self, spice ):
        """
        Return if copy landing sceen is expanded, only preview visible in main panel and detail panel with settings is not shown
        """
        copyLanding = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        return copyLanding["isSecondaryCollapsed"]
    
    def wait_for_landing_is_expanded(self):
        """
        Waits for copy landing sceen is expanded condition, only preview visible in main panel and detail panel with settings is not shown
        """
        copyLanding = self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen)
        self.spice.wait_until(lambda: copyLanding["isSecondaryCollapsed"], timeout = 10.0)

    def are_quicksets_visible(self, spice):
        """
        Return if quicksets are visibles in copy app screen
        """
        areQuicksetsVisibles = False
        isLandingExpanded = self.is_landing_expanded(spice)

        if (isLandingExpanded):
            areQuicksetsVisibles = False #if expanded quickset_selection_view does not exist
        else:
            qsList = self.spice.wait_for(CopyAppWorkflowObjectIds.quickset_selection_view)
            areQuicksetsVisibles = qsList["visible"]

        return areQuicksetsVisibles

    def press_copy_button(self,spice):
        # Press Button "Copy" 
        spice.copy_app.goto(CopyAppWorkflowObjectIds.copy_button)

    def ok_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "ok"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.ok_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.ok_button)

    def press_ok_button(self,spice):
        # Press Button "ok"
        self.ok_button_present(spice)
        spice.copy_app.goto(CopyAppWorkflowObjectIds.ok_button)

    def press_options_detail_panel(self):
        # Press Button option details
        options_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_openSettings_option)
        self.spice.wait_until(lambda: options_button["enabled"], timeout = 15.0)
        self.spice.wait_until(lambda: options_button["visible"], timeout = 15.0)
        options_button.mouse_click()

    def set_detailed_options_resolution(self, value):
        # Change the resolution
        resolution_comboBox = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_resolution_option)
        self.spice.wait_until(lambda: resolution_comboBox["enabled"], timeout = 15.0)
        self.spice.wait_until(lambda: resolution_comboBox["visible"], timeout = 15.0)
        resolution_comboBox.mouse_click()
        option_object_name=""

        if value == "200Dpi":
            option_object_name=CopyAppWorkflowObjectIds.setings_resolution_option_200
        elif value == "300Dpi":
            option_object_name=CopyAppWorkflowObjectIds.setings_resolution_option_300
        elif value == "600Dpi":
            option_object_name=CopyAppWorkflowObjectIds.setings_resolution_option_600

        assert option_object_name != "", "The resolution is not valid"
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.setings_resolution_option_list,
            menu_item_id=option_object_name, top_item_id=CopyAppWorkflowObjectIds.setings_resolution_option)

        select_resolution = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_resolution_option +' #contentItem')
        logging.info("The selected resolution is " + select_resolution['text'])
    
    def set_detailed_original_media(self, value):
        """
        UI should be on copy options list screen.
        UI Flow is copy original paper type-> (copy original paper type settings screen).
        """
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_originalPaper_option)
        current_button.mouse_click()
        option_object_name=""
        
        if value == "white":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_white
        elif value == "photo":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_photo
        elif value == "translucent":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_translucent
        elif value == "old" or value == "oldRecycled":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_oldRecycled
        elif value == "blueprint":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_blueprints
        elif value == "ammonia_old_blueprint" or value == "darkBlueprints":
            option_object_name=CopyAppWorkflowObjectIds.setings_originalPaper_option_darkBlueprints
        
        assert option_object_name != "", "The original paper type is not valid"
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.setings_originalPaper_option_list,
            menu_item_id=option_object_name)

        select_original_paper_type = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_originalPaper_option +' #contentItem')
        logging.info("The selected original paper type is " + select_original_paper_type['text'])

    def goto_original_paper_type_settings(self):
        """
        UI should be on copy options list screen.
        UI Flow is copy original paper type-> (copy original paper type settings screen).
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.row_copy_original_paper_type,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At original paper type settings")

    
    def change_options_color_mode(self):
        # Open color combobox
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_color_option)
        current_button.mouse_click()
        
    def change_options_original_media(self):
        # Open color combobox
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_originalPaper_option)
        current_button.mouse_click()
    
    def set_auto_release_mode(self, auto_release_mode = True):
        # set auto release
        self.workflow_common_operations.scroll_to_position_vertical(0.1, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_autoRelease_option + ' MouseArea')
        self.spice.wait_until(lambda: current_button["visible"] == True, timeout = 10.0)
        actual_state = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_autoRelease_option)["checked"]
        if auto_release_mode != actual_state:
            current_button.mouse_click()
        else:
            logging.info(f"Current long original state is {auto_release_mode}")

    def close_options_detail_panel(self):
        # Press Button option details
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_close_option)
        if not current_button["visible"] or not current_button["enabled"]:
            self.spice.wait_until(lambda: current_button["visible"] == True and current_button["enabled"] == True, timeout = 10.0)
        current_button.mouse_click()

    def set_scan_speed_mode(self):
        # set scan speed
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.setings_scanSpeed_option)
        current_button.mouse_click()

    def eject_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "eject"
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.eject_button, timeout)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.eject_button)

    def press_eject_button(self,spice):
        # Press button eject
        spice.copy_app.goto(CopyAppWorkflowObjectIds.eject_button)

    def startscan_button_present(self,spice, timeout: float = WAIT_TIMEOUT):
        # Check Button "Start"
        spice.copy_app.wait_until_text_button(CopyAppWorkflowObjectIds.copy_button, CopyAppWorkflowObjectIds.start_button_text, timeout)
    
    def press_start_button(self,spice):
        # Press button "Start"
        spice.copy_app.goto(CopyAppWorkflowObjectIds.button_startCopy)
        
    def change_content_type(self,spice,index=0,content_type={}, timeout: float = WAIT_TIMEOUT):
        # A dictionary {index:content_type} must be provided
        # See CopyappWorkflowObjectsIds for more details about content type options
        scroll_step = 0.1
        try:
            current_button = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_contentType, timeout)
            current_button.mouse_click()
            current_button = spice.wait_for(content_type[index], timeout)
            current_button.mouse_click()
        except:
            self.workflow_common_operations.scroll_to_position_vertical(scroll_step, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
            scroll_step =+ scroll_step
        sleep(3)
        
    def change_quality(self,spice,index=0,quality={}, timeout: float = WAIT_TIMEOUT):
        # A dictionary {index:quality} must be provided
        # See CopyappWorkflowObjectsIds for more details about quality options
        scroll_step = 0.1
        try:
            current_button = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_quality, timeout)
            current_button.mouse_click()
            current_button = spice.wait_for(quality[index], timeout)
            current_button.mouse_click()
        except:
            self.workflow_common_operations.scroll_to_position_vertical(scroll_step, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
            scroll_step =+ scroll_step
        sleep(3)

    def has_lock_icon(self):
        self.spice.goto_homescreen()
        home_screen_copy_app_lock_icon_id = CopyAppWorkflowObjectIds.button_copyApp + " #statusIconRect SpiceLottieImageView"

        try:
            lock_icon = self.spice.wait_for(home_screen_copy_app_lock_icon_id)
        except:
            logging.info("Failed to find lock icon")
            return False
        self.spice.wait_until(lambda: lock_icon["visible"] == True, 15)
        return True

    def get_copy_app(self):
        self.spice.goto_homescreen()
        
        copy_app_id = CopyAppWorkflowObjectIds.button_copyApp + " MouseArea"
        return self.spice.wait_for(copy_app_id)

    def set_blueprint_invert_toggle(self, blueprint_invert):
        """
        toggle invert blueprint settings switch
        Args: blueprint_invert: bool True or False
        """
        setting_view = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_invert_blueprint)
        self.spice.wait_until(lambda: setting_view["visible"] == True, timeout = 10.0)

        actual_state = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_invert_blueprint)["checked"]
        if blueprint_invert != actual_state:
            blueprint_invert_button = self.spice.wait_for(CopyAppWorkflowObjectIds.toggle_button_invert_blueprint + " MouseArea")
            blueprint_invert_button.mouse_click()
            sleep(3)
        else:
            logging.info(f"Current invert blueprint state is {blueprint_invert}")
    
    def goto_black_enhancements_settings(self):
        """
        UI should be on copy options list screen.
        Go to Black Enhancement and settings
        """
        self.workflow_common_operations.scroll_vertical_row_item_into_view(screen_id=CopyAppWorkflowObjectIds.view_copySettingsView,menu_item_id=CopyAppWorkflowObjectIds.row_black_enhancements,top_item_id=CopyAppWorkflowObjectIds.copy_option_header_section,select_option = False)
        
        logging.info("UI: At copy black enhancements settings")
    
    def set_black_enhancements_settings(self, black_enhancements = None):
        """
        UI should be on copy options list screen.
        """
        black_enhancements_view = self.spice.wait_for(CopyAppWorkflowObjectIds.row_black_enhancements_textinput)
        self.spice.wait_until(lambda: black_enhancements_view["visible"] == True, timeout = 8.0)

        black_enhancements_view.__setitem__('value', black_enhancements)

    def goto_select_setting_with_payload_and_back_landing_view(self, udw, net, settings:dict, copy_path=None):
        '''
        This method is used to setting the copy settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        settings = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'lighter_Darker': 1
        }
        '''

        if copy_path is not None:
            logging.info("copy from Menu Copy app settings page")
            if copy_path=='MenuCopyDocumnetSettingsPage':
                logging.info("copy from Menu Copy app settings page")
                self.goto_copy()
                self.goto_copy_options_list()
            elif copy_path=='WidgetCopyPage':
                self.goto_copywidget_option_landingview_fromhomescreen()
                self.goto_copy_options_list()
            elif copy_path=='CopyLandingPage':
                copy_button = self.get_copy_app()
                copy_button.mouse_click()
                self.goto_copy_options_list()
            elif copy_path=='IDCardMenuPage':
                self.id_card_copy.goto_idcopy()
                self.goto_copy_options_list_from_idcopy()
            elif copy_path=='IDCardLandingPage':
                self.goto_home_screen_at_copy_app()
                self.goto_idcopy_fromhomescreen()
                self.goto_copy_options_list_from_idcopy()
        else:
            logging.info("Copy App is opened, going directly to option list")
            self.goto_copy_options_list()

        def check_settings_exist(settings, key):
            ''' Method to check if key exit in setting an It has value set
            Args:
                settings (dict): Copy Ticket dict settings
                key (string): name of setting expected to exist in dictionary
            Returns:
                boolean: true if setting exist, false if no
            '''
            return key in settings and settings[key] is not None

        if check_settings_exist(settings,'colorMode'):
            if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
                self.id_card_copy.goto_idcopy_option_color_screen()
                logging.info('settings clor :%s', settings['colorMode'])
                self.id_card_copy.set_idcopy_color_options(net,idcopy_color_options=settings['colorMode'])
            else:
                self.select_color_mode(settings['colorMode'])

        if check_settings_exist(settings,'contentType'):
            self.select_content_type(settings['contentType'])
        if check_settings_exist(settings,'originalPaperType'):
            # self.goto_original_paper_type_settings()  # XL don't need to move in options to find original paper type setting, is in first visual
            self.set_detailed_original_media(settings['originalPaperType'])
        if check_settings_exist(settings,'copies'):
            self.ui_copy_set_no_of_pages(settings['copies'])
        if check_settings_exist(settings,'sides'):
            self.select_copy_side(settings['sides'])
        if check_settings_exist(settings,'pagesPerSheet'):
            self.select_pages_per_sheet_option(udw, settings['pagesPerSheet'])
        if check_settings_exist(settings,'lighter_darker'):
            if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
                self.id_card_copy.goto_idcopy_lighter_or_darker_options()
                self.id_card_copy.set_scan_settings_lighter_darker(settings['lighter_darker'])
            else:
                self.select_scan_settings_lighter_darker(settings['lighter_darker'])
        if check_settings_exist(settings,'size'):
            self.select_original_size(settings['size'])
        if check_settings_exist(settings,'quality'):
            if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
                self.id_card_copy.goto_quality_option()
                self.id_card_copy.set_idcopy_quality_options(net, idcopy_quality_options=settings['quality'])
            else:
                self.select_quality_option(settings['quality'])
        if check_settings_exist(settings,'tray'):
            if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
                self.id_card_copy.goto_idcopy_options_paper_tray()
                self.id_card_copy.set_idcopy_paper_tray_options(net, idcopy_paper_tray_options= settings['tray'])
            else:
                self.select_paper_tray_option(settings['tray'])
        if check_settings_exist(settings,'outputScale'):
            self.goto_copy_option_output_scale()
            self.set_output_scale_options(net, output_scale_options= settings['outputScale'], detail_option= settings['outputScaleDetailOption'])
            self.back_to_copy_options_list_view("Back_to_options_list")
        if check_settings_exist(settings,'collate'):
            self.change_collate(settings['collate'])
        if check_settings_exist(settings,'long_original'):
            self.goto_long_plot_settings_toggle(settings['long_original'])
        if check_settings_exist(settings,'resolution'):
            self.set_detailed_options_resolution(settings['resolution'])
        if check_settings_exist(settings,'blueprint_invert'):
            self.set_blueprint_invert_toggle(settings['blueprint_invert'])
        if check_settings_exist(settings,'auto_release_original'):
            self.set_auto_release_mode(settings['auto_release_original'])
        if check_settings_exist(settings,'black_enhancements'):
            self.goto_black_enhancements_settings()
            self.set_black_enhancements_settings(settings['black_enhancements'])
        # if settings['detailed_background_removal'] in settings:
            # self.select_detailed_background_removal_settings(settings['detailed_background_removal'])

        sleep(3)
        logging.info("Go back Copy Landing screen")
        if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
            self.id_card_copy.back_to_landing_view()
        else:
            self.back_to_landing_view()
    
    def copy_job_ticket_general_method(self,loadmedia:str, copy_path, copy_settings: dict, udw, net, print_emulation=None, familyname="",scan_emulation=None):
        '''
        This method is used to setting the copy settings and verify job is success
        UI flow is from Home screen.
        e.g.:
        settings = {
            'filetype': 'pdf',
            'resolution': e75dpi,
            'filesize': 'highest',
            'sides': 'duplex'',
            'color': 'color',
            'size': 'letter',
            'lighter_Darker': 1
        }
        '''

        settings = {
                'inputMediaSize': copy_settings.get('inputMediaSize', None),
                'copies': copy_settings.get('copies', None),
                'pagesPerSheet': copy_settings.get('pagesPerSheet', None),
                'sides': copy_settings.get('sides', None),
                'outputScale': copy_settings.get('outputScale', None),
                'outputScaleDetailOption': copy_settings.get('outputScaleDetailOption', None),
                'colorMode': copy_settings.get('colorMode', None),
                'contentType': copy_settings.get('contentType', None),
                'lighter_darker': copy_settings.get('lighter_darker', None),
                'size': copy_settings.get('size', None),
                'quality' : copy_settings.get('quality', None),
                'tray' : copy_settings.get('tray', None),
                'collate' : copy_settings.get('collate', None),
                'long_original':copy_settings.get('long_original', None),
                'resolution':copy_settings.get('resolution', None),
                'blueprint_invert': copy_settings.get('blueprint_invert', None),
                'originalPaperType': copy_settings.get('originalPaperType', None),
                'auto_release_original': copy_settings.get('auto_release_original', None),
                'black_enhancements':copy_settings.get('black_enhancements', None),
                'detailed_background_removal': copy_settings.get('detailed_background_removal', None)
            }

        logging.info("load media")
        if loadmedia!=None:
            if loadmedia == 'ADF':
                logging.info("load ADF")
                udw.mainApp.ScanMedia.loadMedia("ADF")
                
            elif loadmedia == 'ADF_PROMPT':
                logging.info("Unload ADF")
                udw.mainApp.ScanMedia.unloadMedia("ADF")

            elif loadmedia =='Flatbed':
                logging.info("Unload ADF OR LOAD Flatbed")
                udw.mainApp.ScanMedia.unloadMedia("ADF")

            elif loadmedia =='MDF':
                logging.info("Unload MDF")
                udw.mainApp.ScanMedia.loadMedia("MDF")
            else:
                assert False, "No media loaded"

        self.goto_select_setting_with_payload_and_back_landing_view(udw, net, settings,copy_path)
        
        logging.info("Start a copy job")
        if copy_path in ['IDCardMenuPage', 'IDCardLandingPage']:
            self.id_card_copy.start_copy()
        else:
            self.start_copy()
            if loadmedia == 'MDF':
                sleep(1)
                self.done_button_present(self.spice, timeout = 15)
                self.press_done_button(self.spice)
        sleep(6)

    def wait_for_acquisition_finished_and_for_copy_button_enabled(self, copy_instance, timeout = 30, expanded = False, wait_time=1,raise_exception_when_processing=False):
        """
            Waits for the scanner acquisition to finish and check copy button is enabled. 
        """
        self.wait_for_acquisition_finished(copy_instance, timeout, wait_time, raise_exception_when_processing)

        # Wait until the copy button is enabled
        if expanded:
            self.spice.main_app.wait_locator_enabled(self.spice.copy_app.locators.copy_button_expanded)
        else:
            self.spice.main_app.wait_locator_enabled(self.spice.copy_app.locators.copy_button)

    def wait_for_acquisition_finished(self, copy_instance, timeout = 30, wait_time=1,raise_exception_when_processing=False):
        """
            Waits for the scanner acquisition to finish. 
        """
        # Make sure scanning is processing
        copy_instance.wait_for_corresponding_scanner_status_with_cdm("Processing", timeout, raise_exception_when_processing, wait_time)

        self.wait_for_scanner_ready(copy_instance, timeout, wait_time)

    def wait_for_scanner_ready(self, copy_instance, timeout = 30, wait_time = 0):
        """
            Waits for the scanner to be ready (idle state). 
        """
        # Make sure scanning is done
        copy_instance.wait_for_corresponding_scanner_status_with_cdm("Idle", timeout, wait_time)

    def wait_main_button_to_start_copy(self, cdm, is_visible:bool=True, is_enabled:bool=True, is_constrained:bool=False, max_timeout:float=10.0):
        '''Method that will wait for start button

        Args:
            cdm (lib): duneTuf library
            is_visible (bool, optional): Check if button is visible. Defaults to True.
            is_enabled (bool, optional): Check if button is enabled. Defaults to True.
            is_constrained (bool, optional): Check if button is contrained. Defaults to False.
            max_timeout (float, optional): max time to wait for any state be in excpected value. Defaults to 10.0.
        '''
        
        # Get translated button string id in device language
        expected_start_text_button = CommonActions.get_translated_text_in_device_language(cdm, self.spice.copy_app.locators.start_string_id_button)
        
        # Wait for the text of the main button to become Start
        self.spice.copy_app.wait_until_text_button(self.spice.copy_app.locators.copy_button, expected_start_text_button)
        current_button = self.spice.wait_for(self.spice.copy_app.locators.copy_button)
        self.spice.wait_until(lambda: current_button["visible"]     == is_visible,      timeout = max_timeout)
        self.spice.wait_until(lambda: current_button["enabled"]     == is_enabled,      timeout = max_timeout)
        self.spice.wait_until(lambda: current_button["constrained"] == is_constrained,  timeout = max_timeout)

    def wait_main_button_to_finish_copy(self, cdm, is_visible:bool=True, is_enabled:bool=True, is_constrained:bool=False, max_timeout:float=10.0, is_done_button=False):
        '''Method that will wait for copy button

        Args:
            cdm (lib): duneTuf library
            is_visible (bool, optional): Check if button is visible. Defaults to True.
            is_enabled (bool, optional): Check if button is enabled. Defaults to True.
            is_constrained (bool, optional): Check if button is contrained. Defaults to False.
            max_timeout (float, optional): max time to wait for any state be in excpected value. Defaults to 10.0.
        '''
        # Get translated button string id in device language
        if(is_done_button):
            expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, self.spice.copy_app.locators.done_string_id_button)
        else:
            expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, self.spice.copy_app.locators.copy_string_id_button)

        # Wait for the text of the main button to become Copy
        self.spice.copy_app.wait_until_text_button(self.spice.copy_app.locators.copy_button, expected_copy_text_button)
        current_button = self.spice.wait_for(self.spice.copy_app.locators.copy_button)
        self.spice.wait_until(lambda: current_button["visible"]     == is_visible,      timeout = max_timeout)
        self.spice.wait_until(lambda: current_button["enabled"]     == is_enabled,      timeout = max_timeout)
        self.spice.wait_until(lambda: current_button["constrained"] == is_constrained,  timeout = max_timeout)

    def start_copy_from_preview_panel(self):
        '''
        Ui Should be in previewpanel
        Click on copy button starts copy
        '''
        self.start_preview()
        sleep(2)
        self.verify_preview()
        sleep(2)
        self.start_copy_from_secondary_panel()
        sleep(2)
    
    
    def start_preview(self):
        '''
        Ui Should be in previewpanel
        Click on preview button starts preview
        '''
        self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy)
        copy_expand_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy)
        self.workflow_common_operations.click_button_on_middle(copy_expand_button)
    
    def verify_preview(self):
        '''
        Ui Should be in previewpanel
        Verif preview
        '''
        assert self.spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, timeout = 9.0), "Current screen is not at copy landing view"
        self.spice.wait_for(CopyAppWorkflowObjectIds.fitapge_layout, timeout =9.0)
        self.spice.wait_for(CopyAppWorkflowObjectIds.first_preview_image, timeout =9.0)
    
    def start_copy_from_secondary_panel(self):
        '''
        Ui Should be in secondary panel
        Click on copy button starts copy
        '''
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.button_startCopy_preivewpanel)
        current_button.mouse_click()
        sleep(2)
    
    def check_spec_on_copy_options_color(self, net, checkoption = "all"):
        """
        Check spec on COPY_OptionsColor
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsColor")
        if checkoption == "color":
            logging.info("check the string about Color, (color)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            sleep(2)
        elif checkoption == "grayscale":
            logging.info("check the string about Color, (Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            sleep(2)
        elif checkoption == "all":
            logging.info("check the string about Color, (color, Grayscale)")
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_str_id, CopyAppWorkflowObjectIds.combo_color_option_color)
            self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_color_grayScale_str_id, CopyAppWorkflowObjectIds.combo_color_option_grayscale)
            sleep(2) 
        current_button = self.spice.query_item(CopyAppWorkflowObjectIds.combo_copySettings_color)
        current_button.mouse_click()
    
    def check_spec_on_copy_options_content_type(self, net, configuration):
        """
        Check spec on COPY_OptionsContentType
        @param net:
        @return:
        """
        logging.info("check the spec on COPY_OptionsContentType")
        logging.info("check the string about Content Type, (Mixed, Lines, Image)")
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_lines_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_linedraw)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_image_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_image)
        self.workflow_common_operations.verify_string(net, CopyAppWorkflowObjectIds.copy_contentType_mixed_str_id, CopyAppWorkflowObjectIds.combo_contentType_option_mixed)
        current_button = self.spice.wait_for(CopyAppWorkflowObjectIds.combo_contentType_option_linedraw)
        current_button.mouse_click()

    def increase_copyApp_num_copies(self, num_increment=1):
        """
        Clicks on the upBtn on the Copy Widget to increment the number of copies in the number_of_copies spinBox
        Note: It has the same ObjectName as the Copy Widget. Must be on Copy App for this to work in the Copy App.
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.4, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
        incrementCopiesElement = self.spice.wait_for(
           CopyAppWorkflowObjectIds.spinBox_numberOfCopies_plus)
        
        for i in range(0, num_increment):
            incrementCopiesElement.mouse_click()
        self.workflow_common_operations.scroll_to_position_vertical(0.1, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)

    def decrease_copyApp_num_copies(self, num_decrement=1):
        """
        Clicks on the downBtn inside the Copy App to increment the number of copies in the number_of_copies spinBox
        Note: It has the same ObjectName as the Copy Widget. Must be on Copy App for this to work in the Copy App.
        """
        self.workflow_common_operations.scroll_to_position_vertical(0.4, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)
        decrementCopiesElement = self.spice.wait_for(
            CopyAppWorkflowObjectIds.spinBox_numberOfCopies_minus)
        for i in range(0, num_decrement):
            decrementCopiesElement.mouse_click(4,4)
        self.workflow_common_operations.scroll_to_position_vertical(0.1, CopyAppWorkflowObjectIds.vertical_layout_scrollbar)

    def wait_and_validate_copy_complete_toast(self, spice, net):
        """
        Wait until the copy complete toast appears.
        """
        spice.common_operations.compare_alert_toast_message(net, "cCopyComplete", timeout = 120)