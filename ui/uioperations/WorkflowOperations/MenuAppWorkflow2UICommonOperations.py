
import logging
import time
import json
from datetime import datetime, timezone
from dunetuf.ews.pom.quick_sets.quicksets_enum import QuickSetStartOption
from dunetuf.send.email.email import Email
from dunetuf.ui.uioperations.BaseOperations.IMenuAppUIOperations import IMenuAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.FaxAppWorkflowObjectIds import FaxAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.EmailAppWorkflowObjectIds import EmailAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.SharePointAppWorkflowObjectIds import SharePointAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
from dunetuf.copy.copy import Copy
from dunetuf.qmltest.QmlTestServer import QmlTestServerError
from dunetuf.ui.uioperations.WorkflowOperations.objectidvalidation import objectidvalidation
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.PomOperations.MainApp import Locators

# menuappworkflowuioperation
class MenuAppWorkflow2UICommonOperations(MenuAppWorkflowUICommonOperations):


    device_language_options = {"option_en" : "English"   , "option_es" : "Español"     , "option_de" : "Deutsch"         , "option_ar" : "العربية"  , "option_ca" : "Català",
                               "option_cs" : "Čeština"   , "option_da" : "Dansk"       , "option_el" : "Ελληνικά"        , "option_fi" : "Suomi"    , "option_fr" : "Français",
                               "option_hr" : "Hrvatski"  , "option_hu" : "Magyar"      , "option_id" : "Bahasa Indonesia", "option_it" : "Italiano" , "option_ko" : "한글" ,
                               "option_nl" : "Nederlands", "option_nb" : "Norsk"       , "option_pl" : "Polski"          , "option_pt" : "Português", "option_ru" : "Русский",
                               "option_sk" : "Slovenčina", "option_sl" : "Slovenščina" , "option_sv" : "Svenska"         , "option_th" : "ไทย"      , "option_tr" : "Türkçe",
                               "option_ro" : "Română"    , "option_ja" : "xxx"         , "option_he" : "עברית"            , "option_zh-CN" : "[[]]"   , "option_zh-TW" : "[[]]", "option_bg" : "bulgarian",}

    country_code_iso = {"Argentina" : "AR"   , "United States" : "US", "None": "None"}

    device_language = { "option_en" : "en"    , "option_es" : "es"    , "option_de" : "de"    , "option_ar" : "ar"    , "option_ca" : "ca",
                        "option_cs" : "cs"    , "option_da" : "da"    , "option_el" : "el"    , "option_fi" : "fi"    , "option_fr" : "fr",
                        "option_hr" : "hr"    , "option_hu" : "hu"    , "option_id" : "id"    , "option_it" : "it"    , "option_ko" : "ko" ,
                        "option_nl" : "nl"    , "option_nb" : "nb"    , "option_pl" : "pl"    , "option_pt" : "pt"    , "option_ru" : "ru",
                        "option_sk" : "sk"    , "option_sl" : "sl"    , "option_sv" : "sv"    , "option_th" : "th"     , "option_tr" : "tr",
                        "option_ro" : "ro"    , "option_ja" : "ja"    , "option_he" : "he"    , "option_zh-CN" : "zh_dash_CN"   , "option_zh-TW" : "zh_dash_TW", "option_bg" : "bg",}

    inactivity_shutdown_options_dict = {
        "20 Minutes": [MenuAppWorkflowObjectIds.twenty_minutes_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_20mins],
        "1 Hour": [MenuAppWorkflowObjectIds.one_hour_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_1hrs],
        "2 Hours": [MenuAppWorkflowObjectIds.two_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_2hrs],
        "3 Hours": [MenuAppWorkflowObjectIds.three_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_3hrs],
        "4 Hours": [MenuAppWorkflowObjectIds.four_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_4hrs],
        "5 Hours": [MenuAppWorkflowObjectIds.five_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_5hrs],
        "6 Hours": [MenuAppWorkflowObjectIds.six_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_6hrs],
        "7 Hours": [MenuAppWorkflowObjectIds.seven_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_7hrs],
        "8 Hours": [MenuAppWorkflowObjectIds.eight_hours_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_8hrs],
        "Never": [MenuAppWorkflowObjectIds.never_str_id, MenuAppWorkflowObjectIds.inactivity_shutdown_never]
    }

    jam_recovery_textimage_map = {
        "#auto_": "cAutomatic",
        "#off": "cOff",
        "#on": "cOn"
    }

    VOLUME_SLIDER_UNIT_X_VALUE = 2.436
    DISPLAY_BRIGHTNESS_SLIDER_UNIT_X_VALUE = 25.95
    MOUSE_CLICK_Y = 7.8

    def __init__(self, spice):
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.maxtimeout = 120
        self.workflow_common_operations = Workflow2UICommonOperations(spice)
        self.homeApp_workflow2_common_operations = HomeAppWorkflow2UICommonOperations(spice)        
        self._spice = spice
        self.is_menu_enabled = False

    def goto_menu(self, spice):
        self.homeApp_workflow2_common_operations.goto_home_menu()
        print("At Menu App")

    def goto_menu_settings(self, spice, signInRequired = True):
        """
        Navigate to the Settings Application
        """

        if self.is_menu_navigation(spice):
            logging.info("Navigating to Settings App via Menu")
            super().goto_menu_settings(spice)
        else:
            logging.info("Navigating to Settings App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.settings_app_button)
            """If the user not having the permission to access the settings, 
            it will show the login view or restricted view"""
            login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
            restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
            if (not signInRequired) and login_view and login_view["visible"]:
                logging.info("Login view is displayed as expected for guest if the icon is locked")
                current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
                current_button.mouse_click()
            elif (not signInRequired) and restricted_view and restricted_view["visible"]:
                logging.info("Restricted view is displayed as expected")
                current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
                current_button.mouse_click()
            else:
                assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuSettings)
        logging.info("At Settings App")    

    def goto_menu_settings_general(self, spice, signInRequired = True):
        self.goto_menu_settings(spice, signInRequired)
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar", signInRequired = signInRequired)
        
        """If the user not having the permission to access the general settings, 
        it will show the login view or restricted view"""
        login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
        restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
        if login_view and login_view["visible"]:
            logging.info("Login view is displayed as expected")
            current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
            current_button.mouse_click()
        elif restricted_view and restricted_view["visible"]:
            logging.info("Restricted view is displayed as expected")
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
            current_button.mouse_click()
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Screen")
        time.sleep(1)


    def goto_menu_settings_general_display(self, spice, signInRequired = True):
        self.goto_menu_settings(spice, signInRequired)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Screen")
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar", signInRequired=signInRequired)
        
        """If the user not having the permission to access the display settings, 
        it will show the login view or restricted view"""
        login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
        restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
        if login_view and login_view["visible"]:
            logging.info("Login view is displayed as expected")
            current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
            current_button.mouse_click()
        elif restricted_view and restricted_view["visible"]:
            logging.info("Restricted view is displayed as expected")
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
            current_button.mouse_click()
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("At display Settings Screen")
        time.sleep(1)

    def goto_menu_settings_general_region(self, spice, signInRequired=True):
        self.goto_menu_settings_general(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_region , scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menu_settings_general, signInRequired=signInRequired)
        
        """If the user not having the permission to access the location settings, 
        it will show the login view or restricted view"""
        login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
        restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
        if login_view and login_view["visible"]:
            logging.info("Login view is displayed as expected")
            current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
            current_button.mouse_click()
        elif restricted_view and restricted_view["visible"]:
            logging.info("Restricted view is displayed as expected")
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
            current_button.mouse_click()
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_country_region, timeout=50)
        logging.info("At country/Region setting Screen")
        time.sleep(1) 
       
    def goto_joblog(self, spice):
        self.homeApp_workflow2_common_operations.goto_home_jobs_app()
        logging.info("At Job Log Screen Screen")
        time.sleep(1)

    def goto_menu_settings_fax(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, FaxAppWorkflowObjectIds.button_menuFaxSettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(FaxAppWorkflowObjectIds.view_faxSettingsScreen, 10)
        logging.info("At Fax Settings Screen")
    
    def goto_menu_settings_image_preview(self, spice):
        self.goto_menu_settings(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, CopyAppWorkflowObjectIds.button_menupreviewSettings, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_menusettingspage)
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_previewScreen, 10)
        logging.info("At Image Preview Screen")

    def goto_menu_settings_supplies_lowbehavior(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_settings_supplies, MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_behavior)
        assert spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_supplies_low_behavior_black)
        logging.info("At Low Behavior Supply Settings Screen")

    def test_views_spice_menu_settings_General_Energy_ScheduleON_DaysHourssettingview(self, spice):
        self.test_views_spice_menu_settings_General_Energy_ScheduleON_DaysHours_Sch(spice)
        ToggleButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleON_scheduleDaysView_toggleButton)
        ToggleButton.mouse_click()
        logging.info("At schedule turn On hours list Screen")
        time.sleep(1)

    def test_views_spice_menu_settings_General_Energy_ScheduleOFF_DaysHourssettingview(self, spice):
        self.test_views_spice_menu_settings_General_Energy_ScheduleOFF_DaysHours_Sch(spice)
        ToggleButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_energy_scheduleOFF_scheduleDaysView_toggleButton)
        ToggleButton.mouse_click()
        logging.info("At schedule turn On hours list Screen")
        time.sleep(1)

    def set_job_queue_recovery_mode(self, spice, value:str) -> int:
        """
        Helper method to set the new value to jobQueueRecoveryMode
        UI Should be in Jobs Settings menu
        @param spice:
        @param enable: True to enable HoldJob mode False to Disable
        """
        job_recovery_policy_combo_box = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)
        assert job_recovery_policy_combo_box["visible"], "{0} is not visible.".format(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode)

        self.scroll_job_settings_view(spice, 0.50)
        self.goto_job_recovery_mode_options(spice)

        if value == "putOnHold":
            index = 0
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_put_on_hold)
        elif value == "cancel":
            index = 1
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.jobs_settings_job_recovery_mode_cancel)
        else:
            raise Exception(f"Invalid job queue recovery mode <{value}>")

        old_value = job_recovery_policy_combo_box['currentIndex']
        current_button.mouse_click()
        spice.wait_until(lambda:job_recovery_policy_combo_box["currentIndex"] == index)

        return old_value

    def signin_from_homescreen(self,spice):
        spice.signIn.goto_universal_sign_in("Sign In")

    # signout from homescreen
    def signout_from_homescreen(self, spice):
        spice.goto_homescreen()
        try:
            spice.signIn.goto_universal_sign_in("Sign Out")
        except Exception as e:
            pass                
        finally:
            logging.info("At Home Screen")

    def verify_alert_setup_incomplete(self, spice, net):
        # Creating setup incomplete alert message using UDW command
        spice.udw.mainApp.execute("RtpManager PUB_triggerRtpEvent 15 0 3")
        assert spice.wait_for("#printerNeedsWSRegistrationNowWindow")
        current_string = spice.query_item("#alertDetailDescription #contentItem")["text"]
        expected_string = LocalizationHelper.get_string_translation(net, "cSetupIncompleteCannotPrintActivate")
        assert current_string == expected_string, "String mismatch"
        okbutton = spice.wait_for("#OK")
        okbutton.mouse_click()
        alertButton = spice.query_item("#HomeScreenView #persistentHeader #headerVar2RightContainer #alertButton")
        spice.wait_until(lambda: alertButton["visible"] == True)
        alertButton.mouse_click()
        spice.wait_for("#alertAppView #alertAppHeader")
        spice.wait_for("#alertAppView #alert0")
        alert0 = spice.query_item("#alertAppView #alert0")
        alert0.mouse_click()
        spice.udw.mainApp.execute("RtpManager PUB_unpublishRtpEvent 15")

    def status_center_ipaddress_validation(self, spice, net):
        #{PR114945} TODO Add the code here once IP adress added
        pass

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice, udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        currentElement = spice.wait_for("#diagnosticsMenuSettingsButton")
        currentElement.mouse_click()
        currentElement = spice.wait_for("#faxMenuSettingsTextImage")
        currentElement.mouse_click()
        currentElement = spice.wait_for("#faxDiagnosticMenuSettingsTextImage")
        currentElement.mouse_click()
        assert spice.wait_for("#faxDiagnosticMenuMenuList")
        logging.info("At Tools -> Service -> Diagnostics ->Fax ->Fax Regulatory Test Screen")

    def goto_menu_tools_servicemenu_adjustment(self,spice,udw):
        self.goto_menu_tools_servicemenu(spice, udw)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_service, MenuAppWorkflowObjectIds.menu_button_service_adjustment,
                             scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_serviceMenu)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service_adjustment)

    def goto_menu_tools_troubleshooting(self, spice):
        self.goto_menu_tools(spice)
        obj_home_folder_view = spice.check_item(MenuAppWorkflowObjectIds.home_folder_view)
        if obj_home_folder_view != None:
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.troubleshooting_app_button, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        else:
            self.workflow_common_operations.scroll_position(MenuAppWorkflowObjectIds.view_menuTools, MenuAppWorkflowObjectIds.menu_button_troubleshooting , MenuAppWorkflowObjectIds.scrollbar_menutoolspage ,MenuAppWorkflowObjectIds.tools_column_name , MenuAppWorkflowObjectIds.tools_Content_Item)
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting + " MouseArea")
            current_button.mouse_click()
        try:
            (spice.wait_for(MenuAppWorkflowObjectIds.login_user_view,30)["visible"])
        except:
            logging.info("DUT doesn't have a Sign-in Screen")
        else:
            #Sign-In and authenticate user
            self.perform_signIn(spice)
        finally:
            logging.info("user signed in")
        if obj_home_folder_view != None:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleShooting_enterprise)
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_menu_list,30)
        logging.info("At Troubleshooting Screen")

    """
    Navigates to the Menu Print screen.
    """
    def goto_menu_print(self, spice):
        if self.is_menu_navigation(spice):
            super().goto_menu_print(spice)
        else:
            self._spice.home_operations.goto_home_print_app()
            self._spice.wait_for(HomeAppWorkflowObjectIds.view_print)

    """
    Navigates to the Menu Job Storage screen.
    """
    def goto_menu_jobStorage(self, spice):
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Job Storage via Menu")
            super().goto_menu_jobStorage(spice)
        else:
            logging.info("Navigating to Job Storage via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.job_storage)
            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)
        logging.info("At Job Storage Screen")

    """
    Navigate to the Job Application
    """
    def goto_menu_jobs(self, spice):
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Job App via Menu")
            super().goto_job_queue_app(spice)
        else:
            logging.info("Navigating to Job App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.job_app)
            assert spice.wait_for(MenuAppWorkflowObjectIds.job_app_view)
        logging.info("At Job App")

    def is_menu_available(self):
        """
        Checks if the Menu functionality is currently applicable for the given context.

        :param spice: The instance used for operations.
        :return: True if the Menu is applicable, False otherwise.
        """
        return self.is_menu_enabled
    
    def goto_menu_mediaApp(self,spice):
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Media App via Menu")
            super().goto_menu_mediaApp(spice)
        else:
            logging.info("Navigating to Media App via Home Screen")
            self.homeApp_workflow2_common_operations.goto_home_mediaApp()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuTray)

    def is_menu_navigation(self, spice):
        """
        Navigates through the Menu if applicable. 

        If the Menu is applicable, it triggers the `goto_menu` functionality. Otherwise, it skips menu navigation.

        :param spice: The instance used for operations.
        :return: True if navigation via menu was performed, False otherwise.
        """        
        if self.is_menu_available():
            logging.info("Menu is Applicable")
            self.goto_menu(spice)
            return True
        logging.info("Menu is not Applicable")
        return False

    def goto_menu_help(self, spice):
        """
        Navigate to the HELP Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Help App via Menu")
            super().goto_menu_help(spice)
        else:
            logging.info("Navigating to Help App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.help_app_button)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuHelp)
        logging.info("At Help App")

    def goto_menu_quickSets(self, spice, quickset_type=None):
        """
        Navigate to the QuickSets Application
        """
        signed_in = False
        if self.is_menu_navigation(spice):
            logging.info("Navigating to QuickSets App via Menu")
            super().goto_menu_quickSets(spice, quickset_type)
        else:
            logging.info("Navigating to QuickSets App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.quicksets_app_button)

            try:
                assert spice.wait_for(MenuAppWorkflowObjectIds.login_user_view, timeout=50.0)["visible"]
                logging.info("Authentication screen found while navigating to QuickSets App")
                self.perform_signIn(spice)
                # wait for toast message to disappear because toast can hide the quickset view
                spice.wait_until(lambda: spice.check_item(MenuAppWorkflowObjectIds.view_toast_window) == None, 50.0)
                logging.info("User signed in")
                signed_in = True
            except:
                logging.info("No Authentication screen found while navigating to QuickSets App")

            try:
                if quickset_type:
                    assert spice.wait_for(MenuAppWorkflowObjectIds.quick_set_view, timeout=50.0)
                    logging.info("At QuickSets App")

                    if quickset_type == 'copy':
                        quickset_type = 'copyList'
                    else:
                        self.workflow_common_operations.scroll_to_position_vertical(0.15, MenuAppWorkflowObjectIds.scrollbar_quicksts_list)

                    quickset_item = spice.wait_for(f"{MenuAppWorkflowObjectIds.quick_set_view} #{quickset_type}")
                    logging.info(f"Quickset item found: {quickset_item}")
                    quickset_item.mouse_click()
                else:
                    logging.info("No quickset type provided; loading default loading quickset view.")
                    assert spice.wait_for(MenuAppWorkflowObjectIds.no_quickset_view_menu_quickset)
            except Exception as e:
                raise Exception(f"Failed to find quickset-item of quickset-type: <{quickset_type}>")
        return signed_in

    def goto_menu_info(self, spice):
        """
        Navigate to the INFO Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Info App via Menu")
            super().goto_menu_info(spice)
        else:
            logging.info("Navigating to Info App via Home Screen")
            spice.goto_homescreen()
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.info_app_button)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuInfo)
        logging.info("At Info App")


    def goto_menu_scan(self, spice):
        """
        Navigate to the SCAN Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Scan App via Menu")
            super().goto_menu_scan(spice)
        else:
            logging.info("Navigating to Scan App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.scan_app)
            assert spice.wait_for(MenuAppWorkflowObjectIds.home_folder_view)
        logging.info("At Scan App")

    def goto_menu_scan_scan_to_email(self, spice):
        """
        Navigate to the SCAN Application -> Scan to Email
        """
        logging.info("Navigating to Scan App -> Scan to Email")
        self.goto_menu_scan(spice)
        spice.wait_for(MenuAppWorkflowObjectIds.home_folder_view)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.scan_to_email_app,
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_scan_to_email)
        logging.info("At Scan App -> Scan to Email Screen")

    def goto_menu_scan_scan_to_network_folder(self, spice):
        """
        Navigate to the SCAN Application -> Scan to Network Folder
        """
        logging.info("Navigating to Scan App -> Scan to Network Folder")
        self.goto_menu_scan(spice)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.scan_to_network_folder_app, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_folder_screen)
        logging.info("At Scan App -> Scan to Network Folder Screen")

    def goto_menu_scan_scan_to_usb(self, spice):
        """
        Navigate to the SCAN Application -> Scan to USB
        """
        logging.info("Navigating to Scan App -> Scan to USB")
        self.goto_menu_scan(spice)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.scan_to_usb_app, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_scan_to_usb)
        logging.info("At Scan App -> Scan to USB Screen")
        
    def goto_menu_tools(self, spice):
        """
        Navigate to the tools Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to tools App via Menu")
            super().goto_menu_tools(spice)
        else:
            logging.info("Navigating to tools App via Home Screen")
            spice.goto_homescreen()
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.tools_app_button)
            logging.info("At tools Screen")

    def goto_menu_contacts(self, spice):
        """
        Navigate to the Contacts Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Contacts App via Menu")
            super().goto_menu_contacts(spice)
        else:
            logging.info("Navigating to Contacts App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.contact_app_button)
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuContacts)
        logging.info("At Contacts App")
        
    def goto_menu_tools_reports(self, spice):
        self.goto_menu_tools(spice)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.reports_app_button, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_reports)
        logging.info("At tools App-> Reports Screen")
        
    def goto_menu_tools_maintenance(self, spice):
        self.goto_menu_tools(spice)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.maintenance_app_button, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_maintenanceSettings)
        logging.info("At tools App-> Maintenance Screen")

    def goto_menu_tools_servicemenu(self, spice, udw):
        prod_config = Configuration(spice.cdm)
        self.product_family = prod_config.familyname
        self.goto_menu_tools(spice)
        self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.service_app_button, 
                                                                 MenuAppWorkflowObjectIds.home_folder_view)
        keyboard = spice.wait_for(MenuAppWorkflowObjectIds.view_serviceKeyboard)
        assert keyboard

        json_path = "/code/dunetuf/dunetuf/ui/uioperations/WorkflowOperations/ServicePins.json"
        with open(json_path) as json_file:
            service_pins = json.load(json_file)
        product_pin = service_pins.get(Configuration(CDM(udw.get_target_ip(), timeout=5.0)).productname.strip(), "12345678")

        keyboard.__setitem__('displayText', product_pin) #just to show the password populated on keyboard
        keyboard.__setitem__('inputText', product_pin)

        doneButton = spice.wait_for(MenuAppWorkflowObjectIds.view_service_sign_in_button)
        doneButton.mouse_click()
        #In service menu now.
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_service)
        logging.info("At Service Screen")

    def goto_menu_copy(self, spice):
        """
        Navigate to the COPY Application
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to Copy App via Menu")
            super().goto_menu_copy(spice)
        else:
            logging.info("Navigating to Copy App via Home Screen")
            self.homeApp_workflow2_common_operations.goto_home_copy()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_copyScreen)
        logging.info("At Copy App")
    
    def goto_menu_settings_general_display(self, spice, signInRequired = True):
        self.goto_menu_settings(spice, signInRequired)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_menuSettings, MenuAppWorkflowObjectIds.menu_button_settings_general,scrollbar_objectname = MenuAppWorkflowObjectIds.view_menuSettings+"ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_generalSettings)
        logging.info("At General Settings Screen")
        time.sleep(1)
        self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_generalSettings, MenuAppWorkflowObjectIds.menu_button_settings_general_display,scrollbar_objectname = MenuAppWorkflowObjectIds.view_generalSettings+"ScrollBar", signInRequired=signInRequired)
        
        """If the user not having the permission to access the display settings, 
        it will show the login view or restricted view"""
        login_view = spice.check_item(MenuAppWorkflowObjectIds.login_user_view)
        restricted_view = spice.check_item(MenuAppWorkflowObjectIds.restricted_access_view)
        if login_view and login_view["visible"]:
            logging.info("Login view is displayed as expected")
            current_button = spice.wait_for(SignInAppWorkflowObjectIds.printerUserCancelButtonControl)
            current_button.mouse_click()
        elif restricted_view and restricted_view["visible"]:
            logging.info("Restricted view is displayed as expected")
            current_button = spice.wait_for(MenuAppWorkflowObjectIds.restricted_access_ok_button)
            current_button.mouse_click()
        else:
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
        logging.info("At display Settings Screen")
        time.sleep(1)

    def goto_menu_trays(self,spice):
       if self.is_menu_navigation(spice):
          logging.info("Navigating to tray App via Menu")
          super().goto_menu_trays(spice)
       else:
           logging.info("Navigating to Tray App via Home Screen")
           self.homeApp_workflow2_common_operations.goto_home_trays_app()
           assert spice.wait_for(MenuAppWorkflowObjectIds.view_menuTray)

    def goto_menu_settings_supplies_resetsupplies(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                             MenuAppWorkflowObjectIds.view_settings_supplies,
                             MenuAppWorkflowObjectIds.menu_button_settings_supplies_resetsupplies,
                             scrollbar_objectname=MenuAppWorkflowObjectIds.view_settings_supplies + "ScrollBar")
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_settings_supplies)
        logging.info("At Reset Supplies Screen")

    def goto_home_settings_supplies(self, spice):
        """ Navigate to Supplies settings from Home screen """
        self._spice.home.goto_home_settings_app(spice)
        screen_id = "#settingsMenuListListView" 
        assert self._spice.wait_for(screen_id) 
        self.scroll_to_list_item(
                self._spice,
                MenuAppWorkflowObjectIds.view_menuSettings,  # listName 
                MenuAppWorkflowObjectIds.menu_button_settings_supplies,  # rowName
                MenuAppWorkflowObjectIds.scrollbar_menusettingspage)  # scrollbarName
        current_button = self._spice.wait_for("#suppliesSettingsSettingsTextImage" + " MouseArea")
        current_button.mouse_click()

    def goto_menu_settings_supplies_verylowbehavior(self, spice):
        self.goto_menu_settings_supplies(spice)
        self.menu_navigation(spice,
                MenuAppWorkflowObjectIds.view_settings_supplies,
                "#veryLowBehavior_WFSettingsTextImage",
                scrollbar_objectname = "#suppliesSettingsMenuListScrollBar")
        assert self._spice.wait_for("#veryLowBehavior_WFSettingsTextImage")
        logging.info("At Very Low Behavior Supply Settings Screen")

    def goto_supplies_settings_blackverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        spice.wait_for("#blackVeryLowAction_WFMenuComboBox").mouse_click()
        logging.info("At Very Low Behavior - Black Supply Settings Screen")

    def goto_supplies_settings_colorverylowbehavior(self, spice):
        self.goto_menu_settings_supplies_verylowbehavior(spice)
        spice.wait_for("#colorVeryLowAction_WFMenuComboBox").mouse_click()
        logging.info("At Very Low Behavior - Color Supply Settings Screen")

    def change_supply_usage_data(self, enable_option = False):
        """ Enable/Disable Supply Usage Data """
        self.scroll_to_list_item(
                self._spice,
                "#suppliesSettingsMenuList",  # listName 
                "#storeUsageDataEnabledSettingsSwitch",  # rowName
                "#suppliesSettingsMenuListScrollBar")  # scrollbarName        
        supply_usage_status = self._spice.wait_for("#storeUsageDataEnabledMenuSwitch")        
        if supply_usage_status["checked"] == enable_option:
            logging.info(f"Supply usage data is already set to {enable_option}")
        else:
            logging.info(supply_usage_status["checked"])
            supply_usage_status.mouse_click()
            is_clicked = self._spice.wait_for("#storeUsageDataEnabledMenuSwitch")
            assert is_clicked["checked"] == enable_option, "Supply usage data Enable/Disbale failed"

    def get_supply_usage_data_status(self):
        """ Get store Supply Usage Data status """
        self.scroll_to_list_item(
                self._spice,
                "#suppliesSettingsMenuList",  # listName 
                "#storeUsageDataEnabledSettingsSwitch",  # rowName
                "#suppliesSettingsMenuListScrollBar")  # scrollbarName        
        supply_usage_status = self._spice.wait_for("#storeUsageDataEnabledMenuSwitch") 
        return supply_usage_status["checked"]

    def goto_menu_settings_supplies_storesupplyusagedata(self, spice):
        """ Navigate to Store Supply Usage Data """
        self._spice.home.goto_home_settings_app(spice)
        screen_id = "#settingsMenuListListView" 
        assert self._spice.wait_for(screen_id) 
        self.scroll_to_list_item(
                self._spice,
                MenuAppWorkflowObjectIds.view_menuSettings,  # listName 
                MenuAppWorkflowObjectIds.menu_button_settings_supplies,  # rowName
                MenuAppWorkflowObjectIds.scrollbar_menusettingspage)  # scrollbarName
        current_button = self._spice.wait_for("#suppliesSettingsSettingsTextImage" + " MouseArea")
        current_button.mouse_click()
        #Go to Store Supply Usage Data
        self.scroll_to_list_item(
                self._spice,
                "#suppliesSettingsMenuList",  # listName 
                "#storeUsageDataEnabledSettingsSwitch",  # rowName
                "#suppliesSettingsMenuListScrollBar")  # scrollbarName        
        assert self._spice.wait_for("#storeUsageDataEnabledMenuSwitch") 
    
    def goto_menu_supplies(self, spice):
        """
        Navigate to the menu supplies
        """
        if self.is_menu_navigation(spice):
            logging.info("Navigating to supplies App via menu") 
            super().goto_menu_supplies(spice)
        else:
            logging.info("Navigating to Supplies App via Home Screen")
            self.homeApp_workflow2_common_operations.home_navigation(MenuAppWorkflowObjectIds.supplies_app_button)
            assert self._spice.wait_for(MenuAppWorkflowObjectIds.ui_supplies_app)
            
        logging.info("At Supplies App")
    
    def goto_menu_settings_general_display_inactivity_timeout(self, spice):
        try:
            self.goto_menu_settings(spice)
            current_button1 = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general + " MouseArea")
            current_button1.mouse_click()

            current_button = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_general_display + " MouseArea")
            current_button.mouse_click()
            assert spice.wait_for(MenuAppWorkflowObjectIds.view_display_Settings)
            self.menu_navigation(spice, MenuAppWorkflowObjectIds.view_display_Settings, MenuAppWorkflowObjectIds.menu_button_settings_general_inactivity_timeout, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_display_settings)
        except Exception as e:
            logging.info("Inactivity Timeout is not available in the current screen")
            raise e

    def is_scan_digital_setting_locked(self, spice):
        """
        Check if the scan digital setting is locked
        """
        button = spice.wait_for(EmailAppWorkflowObjectIds.button_menuEmailSettings)
        return button["locked"] == True
    
    def select_digital_send_setting(self, spice):
        """
        Select the digital send setting from the dropdown
        """
        button = spice.wait_for(EmailAppWorkflowObjectIds.button_menuEmailSettings)
        spice.wait_until(lambda: button["visible"] == True)
        spice.wait_until(lambda: button["enabled"] == True)
        button.mouse_click()

    def is_email_setup_locked(self, spice):
        """
        Check if the email setup is locked
        """
        button = spice.wait_for(EmailAppWorkflowObjectIds.button_emailSetupMenuButton)
        return button["locked"] == True

    def select_email_setup(self, spice):
        """
        Select the email setup from the dropdown
        """
        button = spice.wait_for(EmailAppWorkflowObjectIds.button_emailSetupMenuButton)
        spice.wait_until(lambda: button["visible"] == True)
        spice.wait_until(lambda: button["enabled"] == True)
        button.mouse_click()
