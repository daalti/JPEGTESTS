import logging
import time

from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.BaseOperations.IIDCardCopyAppUIOperation import IIDCardCopyAppUIOperation
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowObjectIds import IDCardCopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations

class IDCardCopyAppWorkflowUICommonOperations(IIDCardCopyAppUIOperation):

    def __init__(self, spice):
        self.spice = spice
        self.IDCardCopyAppWorkflowObjectIds = IDCardCopyAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations
        self.maxtimeout = 120
        
    def goto_menu_mainMenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        self.spice.goto_homescreen()
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_homeScreen)
        logging.info("At Home Screen")
        # TODO - Need to check the menu app is visible or not
        # check whether the menu is visible on the screen
        menuApp = self.spice.wait_for(MenuAppWorkflowObjectIds.menu_button_menuApp)
        self.spice.wait_until(lambda: menuApp["visible"] == True)

    def goto_home_screen_at_copy_app(self):
        """
        Purpose: Navigates to Home screen -> Copy app
        Ui Flow: Any screen -> Home screen -> Copy app
        :param spice : Takes 0 arguments
        :return: None
        """
        self.spice.scroll_home_left(1)
        time.sleep(3)
        copy_icon = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_copyhome + " MouseArea")
        copy_icon.mouse_click()
        time.sleep(3)

    def goto_idcopy(self):
        """
        Purpose: Navigates to IDCopy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> IDCopy app
        :param spice: Takes 0 arguments
        :return: None
        """
        #self.goto_menu_mainMenu()
        #idCopyApp = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idcopyApp + " MouseArea")
        #idCopyApp.mouse_click()
        #self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        self.goto_menu_idcopy(self.spice)
    
    def check_cartridge_error_is_shown(self):
        """
        Purpose: Check cartridge error is shown
        :param spice: Takes 0 arguments
        :return: None
        """
        button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.button_startIDCopy)
        button.mouse_click()
        assert self.spice.wait_for("#cartridgeMissing1Window")
        assert self.spice.wait_for("#alertStatusImage")
        self.spice.suppliesapp.press_alert_button("#Hide")

    def goto_idcopy_fromhomescreen(self):

        self.spice.goto_homescreen()
        copy_app_exist = self.is_copy_app_on_the_home_screen()
        if(copy_app_exist == True):
            self.goto_home_screen_at_copy_app()
            current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idcopyApp + " MouseArea")
            current_button.mouse_click()
        else:
            self.workflow_common_operations.scroll_to_position_horizontal(0.5)
            current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idcopyApp + " MouseArea")
            current_button.mouse_click()



    def ui_select_idcopy_page(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: IDCopyLanding screen -> IDCopy Start screen
        """
        self.workflow_common_operations.goto_item(IDCardCopyAppWorkflowObjectIds.button_startIDCopy, IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyStart_screen, timeout = 9.0)

    def wait_for_copying_toast(self, message: str = "Copying", no_of_pages=1, timeout=30):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: Copying : str
        """
        option = ""
        status = ""
        if message == "Copying":
            option = "Copying 1/1"

        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_systemToastMessagesScreen)
        time.sleep(timeout)

    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from IDCopy screen.
        UI Flow is IDCopy->Options
        '''
		# Wait for Options screen
        currentScreen = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopyMoreOptions)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)
        logging.info("UI: At Options in IDCopy")

    def goto_quality_option(self, dial_value=180):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is IDCopyOptions->(Quality list)
        '''
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_quality, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_quality]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_quality, timeout = 9.0)

    def select_copy_quality(self, quality:str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        self.goto_copy_options_list()
        self.goto_quality_option()
        idcopy_quality_options_dict = {
            "Standard": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_standard,
            "Draft": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_draft,
            "Best": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_best
        }
        to_select_item = idcopy_quality_options_dict.get(quality)
        current_button = self.spice.query_item(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

    def set_copy_settings(self, cdm):
        self.goto_copy_options_list()

        #contentorientation
        # TODO Uncomment this once the orientation for IdcardCopy is implemented
        # menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_orientation, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_orientation]
        # self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        # assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_orientation)
        # current_button = self.spice.query_item(f"{IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_landscape} {IDCardCopyAppWorkflowObjectIds.text_view}")
        # current_button.mouse_click()
        # assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

        #colorMode
        if cdm.device_feature_cdm.is_color_supported(): 
            menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idCopySettings_color, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color]
            self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
            assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_color)
            current_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_color)
            current_button.mouse_click()
            assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

        #Paper tray
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_paperTray, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_paperTray)
        current_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray2)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

        #lighter darker
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_slider_lighterDarker, IDCardCopyAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        self.set_scan_settings_lighter_darker(8)

    def start_copy(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        self.start_id_copy()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyStart_screen, timeout =30.0)
        first_continue = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopy_continue)
        first_continue.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopy_secondSide_screen, timeout =15.0)
        second_continue = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopy_done)
        second_continue.mouse_click()
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        time.sleep(10)

    def start_id_copy(self, dial_value=180, timeout=60):
        '''
        UI should be in ID Copy Landing Screen.
        Navigates to screen starting from Landing screen.
		'''
        currentScreen = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        start_time = time.time()
        enabled = False
        while time.time()-start_time < timeout:
                try:
                    enabled = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_startIDCopy)["enabled"]
                except:
                    toast_message = "Does not capture the status"
                if enabled:
                    logging.info("Copy Is enabled")
                    break
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_startIDCopy)
        current_button.mouse_click()

    def select_idcopy_first_continue_button(self, timeout=60, concurent=True):
        """
        click first continue button
        # todo: need to update when the HMDE-285 is fixed
        @param:
        @return:
        """
        logging.info("click continue button")
        currentScreen = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyStart_screen)
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopy_continue)
        current_button.mouse_click()
        copy_process_find = False
        start_time = time.time()
        if concurent:
            while time.time()-start_time < timeout:
                try:
                    toast_message = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.text_toastInfoText)["text"]
                except:
                    toast_message = "Does not capture the status"
                logging.info(f"current message is: <{toast_message}>")
                if toast_message.strip().startswith("Starting") or toast_message.strip().startswith("Scanning"):
                    logging.info("Find Copying")
                    copy_process_find = True
                    break

            if not copy_process_find:
                raise Exception("Timeout to find Copying")

    def select_idcopy_second_continue_button(self):
        """
        click second continue button
        @param:
        @return:
        """
        logging.info("click second continue button")

        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopy_secondSide_screen, timeout =15.0)
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopy_done)
        current_button.mouse_click()
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)

    def click_idcopy_cancel_on_second_screen(self):
        """
        click cancel button on second screen
        @param:
        @return:
        """
        logging.info("click cancel button")

        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopy_secondSide_screen, timeout =15.0)
        current_button = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_idCopy_second_cancel)
        current_button.mouse_click()
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)

    def wait_for_idcopy_complete(self, net, timeout=120):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        :param net:
        :param timeout:
        :return:
        """
        #Only Starting Toast implemented
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_systemToastMessagesScreen)
        complete_message = self.workflow_common_operations.get_expected_translation_str_by_str_id(net, str_id="cCopyCompleteMessage")
        copy_process_find = False
        for i in range(timeout):
            try:
                current_status = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.text_toastInfoText)["text"]
            except:
                current_status = "Does capture the status"
            logging.info("Current status is: " + current_status)
            if current_status == complete_message:
                logging.info("copy complete!")
                copy_process_find = True
                break

        if not copy_process_find:
            raise Exception("Copy complete doesn`t appear within %s" % timeout)
        """

    def goto_idcopy_option_color_screen(self):
        """
        Go to ID Card Copy -> Options -> Color screen
        @return:
        """
        logging.info("Go to ID Card Copy -> Options -> Color screen")
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idCopySettings_color, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_color)

    def goto_idcopy_lighter_or_darker_options(self):
        """
        go to the lighter or darker
        """
        logging.info("Go to lighter or darker option menu")
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_slider_lighterDarker, IDCardCopyAppWorkflowObjectIds.slider_lighterDarker]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)

    def goto_idcopy_option_orientation_screen(self):
        """
        Go to orientation option menu
        @return:
        """
        logging.info("Go to orientation option menu")
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_orientation, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_orientation]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_orientation)

    def back_to_landing_view(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen to landing screen.
        UI Flow is Option screen->Landing screen
        '''
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)
        current_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.idCardCopy_options_closeButton)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)

    def back_to_homescreen(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen to Option screen.
        UI Flow is Landing screen->Home screen
        '''
        self.workflow_common_operations.back_button_press(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen, MenuAppWorkflowObjectIds.view_homeScreen)

    def set_idcopy_color_options(self, net, idcopy_color_options="Color", locale: str = "en-US"):
        """
        Set idcopy color option
        @param net:
        @param idcopy color_options: str -> Color/Grayscale
        @param locale:
        @return:
        """
        logging.info("Set the idcopy color option to: " + idcopy_color_options)

        idcopy_color_options_dict = {
            "Color": f"{IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_color} {IDCardCopyAppWorkflowObjectIds.text_view}",
            "Grayscale": f"{IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_grayscale} {IDCardCopyAppWorkflowObjectIds.text_view}"
        }
        to_select_item = idcopy_color_options_dict.get(idcopy_color_options)
        current_button = self.spice.wait_for(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

    def set_idcopy_paper_tray_options(self, net, idcopy_paper_tray_options="Automatic", locale: str = "en-US"):
        """
        Set idcopy paper tray option
        @param net:
        @param idcopy paperTray_options: str -> Tray 1/Tray 2/Tray 3/Automatic
        @param locale:
        @return:
        """
        logging.info("Set the idcopy paper tray option to: " + idcopy_paper_tray_options)

        idcopy_paper_tray_options_dict = {
            "Tray 1": IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray1,
            "Tray 2": IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray2,
            "Tray 3": IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray3,
            "Automatic": IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_auto
        }
        to_select_item = idcopy_paper_tray_options_dict.get(idcopy_paper_tray_options)
        self.workflow_common_operations.goto_item(to_select_item,"#copy_paperSourceComboBoxpopupList",scrollbar_objectname="#comboBoxScrollBar",select_option=False)
        current_button = self.spice.query_item(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

    def set_idcopy_quality_options(self, net, idcopy_quality_options="Standard", locale: str = "en-US"):
        """
        Set idcopy quality option
        @param net:
        @param idcopy_quality_options: str -> Standard/Draft/Best
        @param locale:
        @return:
        """
        logging.info("Set the quality option to: " + idcopy_quality_options)

        idcopy_quality_options_dict = {
            "Standard": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_standard,
            "Draft": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_draft,
            "Best": IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_best
        }
        to_select_item = idcopy_quality_options_dict.get(idcopy_quality_options)
        current_button = self.spice.wait_for(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

    def set_idcopy_orientation_options(self, net, orientation_options="Portrait", locale: str = "en-US"):
        """
        Set the orientation option
        @param net:
        @param orientaion_options: str -> Landscape/Portrait
        @param locale:
        @return:
        """
        logging.info("Set the orientation option to: " + orientation_options)

        orientation_options_dict = {
            "Landscape": f"{IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_landscape} {IDCardCopyAppWorkflowObjectIds.text_view}",
            "Portrait": f"{IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_portrait} {IDCardCopyAppWorkflowObjectIds.text_view}"
        }
        to_select_item = orientation_options_dict.get(orientation_options)
        current_button = self.spice.query_item(to_select_item)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)

    def get_idcopy_color_options(self):
        """
        Get the idcopy color option
        @return:
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)
        current_idcopy_color_option = self.workflow_common_operations.get_actual_str(IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color)
        logging.info("Current idcopy Color settings is: " + current_idcopy_color_option)
        return current_idcopy_color_option

    def get_idcopy_paper_tray_options(self):
        """
        Get the idcopy paper tray option
        @return:
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)
        current_tray_options = self.workflow_common_operations.get_actual_str(IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray)
        logging.info("Current paper tray settings is: " + current_tray_options)
        return current_tray_options

    def get_idcopy_quality_options(self):
        """
        Get idcopy quality option
        @return:
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)
        current_idcopy_quality_option = self.workflow_common_operations.get_actual_str(IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_quality)
        logging.info("Current idcopy quality settings is: " + current_idcopy_quality_option)
        return current_idcopy_quality_option

    def get_idcopy_orientation_options(self):
        """
        Get the orientation option
        @return:
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView)
        current_orientation_option = self.workflow_common_operations.get_actual_str(IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_orientation)
        logging.info("Current orientation settings is: " + current_orientation_option)
        return current_orientation_option

    def goto_idcopy_options_paper_tray(self):
        """
        go to the options -> paper tray
        """
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 6)
        logging.info("Go to paper tray screen")
        menu_item_id = [IDCardCopyAppWorkflowObjectIds.row_combo_idcopySettings_paperTray, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray]
        self.workflow_common_operations.goto_item(menu_item_id, IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, scrollbar_objectname = IDCardCopyAppWorkflowObjectIds.idCardCopy_options_scrollbar)
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_paperTray)
        time.sleep(2)

    def check_spec_on_idcopy_screen(self, net):
        """
        check spec on ID Copy Screen
        @param net:
        @return:
        """
        logging.info("check the str on ID Card Copy screen")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_button_copy_str_id, IDCardCopyAppWorkflowObjectIds.button_startIDCopy)
        logging.info("verify the home* button existed")
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_home, 1)

    def check_spec_on_idcopy_first_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        logging.info("check on first screen page prompt")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyStart_screen)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_firstScreen_body_str_id, IDCardCopyAppWorkflowObjectIds.idCardCopy_firstScreen_alert_body)

    def check_spec_on_idcopy_second_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        logging.info("check on second screen page prompt")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopy_secondSide_screen, timeout=60)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_secondScreen_body_str_id, IDCardCopyAppWorkflowObjectIds.idCardCopy_secondScreen_alert_body)

    def ui_idcopy_set_no_of_pages(self, value):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: Copy screen -> Set number of pages
        :return: None
        """
        time.sleep(10)
        numCopiesElement = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.spinBox_idCopy_numberOfCopies)
        numCopiesElement.__setitem__('value', value)

    def goto_menu_idcopy(self, spice):
        """
        navigate screen: home_menu -> menu -> copy -> id card copy
        @return:
        """
        self.homemenu.goto_menu(spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage)
        copy_app = self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_menu_copy)
        copy_app.mouse_click()
         # changes made here because the screen is of ButtonTemplate Model. Right Now there is only few options 
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code
        
        #self.workflow_common_operations.scroll_position(IDCardCopyAppWorkflowObjectIds.view_menu_copy_screen, IDCardCopyAppWorkflowObjectIds.button_menu_idCopy , IDCardCopyAppWorkflowObjectIds.scrollBar_menucopyFolderLanding , IDCardCopyAppWorkflowObjectIds.copyFolderPage_column_name , IDCardCopyAppWorkflowObjectIds.copyFolderPage_Content_Item)
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_menu_idCopy)
        current_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.button_menu_idCopy)
        current_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopyScreen)
        logging.info("At ID Card Copy Landing Screen")

    def back_to_copy_home_screen_from_idcopy(self):
        '''
        UI should be in ID Copy screen from menu
        Navigates to menu_copy screen starting from ID Copy landing screen to copy home screen
        UI Flow is ID Copy Landing screen -> copy home screen
        '''
        back_button = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.button_back, 1)
        back_button.mouse_click()
        assert self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_menu_copy_screen, timeout=60)

    def check_spec_on_idcopy_option_color_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Color screen
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Color screen")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_color, timeout=60)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_color_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_color)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_color_grayScale_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_color_grayscale)

    def check_spec_on_idcopy_option_paper_tray(self, net):
        """
        Check spec on ID Card Copy -> Options -> Paper Tray
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Paper Tray")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_paperTray, timeout=60)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_paperTray_tray1_str_id, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray1)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_paperTray_tray2_str_id, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray2)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_paperTray_tray3_str_id, IDCardCopyAppWorkflowObjectIds.combo_idcopySettings_paperTray_tray3)

    def check_spec_on_idcopy_option_quality_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Quality screen
        @param net:
        @return:
        """
        logging.info("Check spec on ID Card Copy -> Options -> Quality screen")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_quality, timeout=60)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_quality_standard_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_standard)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_quality_best_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_best)
        self.workflow_common_operations.verify_string(net, IDCardCopyAppWorkflowObjectIds.idCardCopy_quality_draft_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopySettings_quality_draft)

    def check_spec_on_idcopy_options_orientation(self, net):
        """
        Check spec on IDCopy_Orientaion_Options
        @param net:
        @return:
        """
        logging.info("check the spec on IDCopy_Orientaion_Options")
        logging.info("check the string about Orientation, (Landscape, Portrait)")
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettings_orientation, timeout=60)
        self.workflow_common_operations.verify_string(net,IDCardCopyAppWorkflowObjectIds.idCardCopy_orientation_landscape_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_landscape)
        self.workflow_common_operations.verify_string(net,IDCardCopyAppWorkflowObjectIds.idCardCopy_orientation_portrait_str_id, IDCardCopyAppWorkflowObjectIds.combo_idCopy_orientation_portrait)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        current_value = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.slider_lighterDarker)["value"]
        logging.info("Current lighter_darker value is %s" % current_value)
        current_element = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.slider_lighterDarker)
        current_element.__setitem__('value', lighter_darker)
        current_value = self.spice.query_item(IDCardCopyAppWorkflowObjectIds.slider_lighterDarker)["value"]
        logging.info("lighter_darker value changed to %s" % current_value)

    def check_spec_on_idcopy_options_screen(self, net):
        """
        check spec on ID Copy Options screen
        @param net:
        @return:
        """

        logging.info("check the items on ID Card Copy Options screen")
        #TODO: String verification in Options screen
        self.spice.wait_for(IDCardCopyAppWorkflowObjectIds.view_idCopySettingsView, timeout = 9.0)
    
    def is_copy_app_on_the_home_screen(self):
        exist = True
        try:
            if(self.spice.query_item(IDCardCopyAppWorkflowObjectIds.button_copyhome)["visible"] == True):
                exist = True
        except:
            logging.info("There is Document Copy on the Home screen, not the Copy app.")
            exist = False
        return exist