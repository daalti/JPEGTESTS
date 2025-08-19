import sys


class IIDCardCopyAppUIOperation(object):

    def goto_menu_mainMenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param _spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_idcopy(self):
        """
        Purpose: Navigates to Copy app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Copy app
        :param _spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ui_select_idcopy_page(self):
        """
        Purpose: Selects Copy option in copy screen and waits for copy successful screen
        Ui Flow: Copy screen -> Copy
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def ui_idcopy_set_no_of_pages(self, value):
        """
        Purpose: Selects number of pages in copy screen based on user input
        Ui Flow: Copy screen -> Set number of pages
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_copying_toast(self, message: str = "Copying", no_of_pages=1, timeout=30):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        Args: message: Copying : str
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_copy_options_list(self):
        '''
        UI should be in Copy Landing screen.
        Navigates to Options screen starting from Copy screen.
        UI Flow is Copy->Options->(Options list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sides_option(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_copy_side(self, side_mode: str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_quality_option(self, dial_value=180):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen.
        UI Flow is CopyOptions->(Side list)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_copy_quality(self, quality: str):
        '''
        UI should be in Landing view screen.
        Navigates to Side screen starting from Landing to side mode screen.
        UI Flow is Landing->option->side mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_copy_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_scan_settings_lighter_darker(self, lighter_darker: int = 1):
        '''
        UI should be on lighter_darker slider in Scan settings screen.
        Args:
            lighter_darker: The lighter_darker value to set - ( Range is 1 to 9)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_landing_view(self):
        '''
        UI should be in Option screen.
        Navigates to Side screen starting from Option screen to landing screen.
        UI Flow is Option screen->Landing screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_homescreen(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen to Option screen.
        UI Flow is Landing screen->Home screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_copy(self):
        '''
        UI should be in Landing screen.
        Navigates to Side screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_screen(self, net):
        """
        check spec on ID Copy Screen
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def start_id_copy(self, dial_value=180, timeout=60):
        '''
        UI should be in ID Copy Landing Screen.
        Navigates to screen starting from Landing screen.
        UI Flow is click on copy button
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_first_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_idcopy_first_continue_button(self, timeout=60):
        """
        click first continue button
        @param:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_second_screen(self, net):
        """
        check spec on page prompt
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_idcopy_second_continue_button(self):
        """
        click second continue button
        @param:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def wait_for_idcopy_complete(self, net, timeout=120):
        """
        Purpose: Wait for the given toast message to appear in screen and success if given toast appears
        :param net:
        :param timeout:
        :return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_idcopy(self, spice):
        """
        navigate screen: home_menu -> menu -> copy -> id card copy
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def back_to_copy_home_screen_from_idcopy(self):
        '''
        UI should be in ID Copy screen from menu
        Navigates to menu_copy screen starting from ID Copy landing screen to copy home screen
        UI Flow is ID Copy Landing screen -> copy home screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_options_screen(self, net):
        """
        check spec on ID Copy Options screen
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_idcopy_option_color_screen(self):
        """
        Go to ID Card Copy -> Options -> Color screen
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_option_color_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Color screen
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_idcopy_color_options(self, net, idcopy_color_options="Color", locale: str = "en-US"):
        """
        Set idcopy color option
        @param net:
        @param idcopy color_options: str -> Color/Grayscale
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_idcopy_color_options(self):
        """
        Get the idcopy color option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_idcopy_options_paper_tray(self):
        """
        go to the options -> paper tray
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_option_paper_tray(self, net):
        """
        Check spec on ID Card Copy -> Options -> Paper Tray
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_idcopy_paper_tray_options(self, net, idcopy_paper_tray_options="Automatic", locale: str = "en-US"):
        """
        Set idcopy paper tray option
        @param net:
        @param idcopy paperTray_options: str -> Tray 1/Tray 2/Tray 3/Automatic
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_idcopy_paper_tray_options(self):
        """
        Get the idcopy paper tray option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_option_quality_screen(self, net):
        """
        Check spec on ID Card Copy -> Options -> Quality screen
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_idcopy_quality_options(self, net, idcopy_quality_options="Standard", locale: str = "en-US"):
        """
        Set idcopy quality option
        @param net:
        @param idcopy_quality_options: str -> Standard/Draft/Best
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_idcopy_quality_options(self):
        """
        Get idcopy quality option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_idcopy_lighter_or_darker_options(self):
        """
        go to the lighter or darker
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_idcopy_option_orientation_screen(self):
        """
        Go to orientation option menu
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_idcopy_options_orientation(self, net):
        """
        Check spec on IDCopy_Orientaion_Options
        @param net:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_idcopy_orientation_options(self, net, orientation_options="Portrait", locale: str = "en-US"):
        """
        Set the orientation option
        @param net:
        @param orientaion_options: str -> Landscape/Portrait
        @param locale:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_idcopy_orientation_options(self):
        """
        Get the orientation option
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_idcopy_cancel_on_second_screen(self):
        """
        click cancel button on second screen
        @param:
        @return:
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
