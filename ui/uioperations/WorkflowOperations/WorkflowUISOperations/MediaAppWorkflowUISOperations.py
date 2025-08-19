import re
import time
import logging
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MoveAndCutWorkflowObjectIds import MoveAndCutWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowUICommonOperations import MediaAppWorkflowUICommonOperations
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM
class MediaAppWorkflowUISOperations(MediaAppWorkflowUICommonOperations):
    TUR_BUTTON = "#deactivateTakeUpReelButton"
    RELEASE_SUBSTRATE_BUTTON = "#releaseSubstrateButton"
    ALERT_DIALOG_WINDOW_TYPE1 = "#AlertModelView"
    ALERT_DIALOG_WINDOW_TYPE2 = "#AlertModelView"
    ALERT_DIALOG_WINDOW_TYPE3 = "#AlertDetails1"
    ALERT_DIALOG_WINDOW_TYPE4 = "#nativeStackView"
    ALERT_DIALOG_TOAST_WINDOW = "#SpiceToast"
    ALERT_TITLE_TEXT = "#titleObject"
    ALERT_DETAIL_DESCRIPTION = "#contentItem"
    ALERT_DETAIL_DESCRIPTION_PART1 = "#AlertModelView #TitleText #TitleTextHeaderView"
    ALERT_DETAIL_DESCRIPTION_PART2 = "#AlertModelView #alertDetailDescription #contentItem"
    ALERT_DETAIL_DESCRIPTION_CUSTOM = "#AlertModelView #alertDetailDescription #contentItem"
    ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL = " #alertDetailDescription #contentItem"
    ALERT_TOAST_MESSAGE = "#infoTextToastMessage"
    ALERT_IMAGE_ICON = "#imageObject"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage SpiceLottieImageView"
    ALERT_LOAD_MEDIA_VERIFY_FLOW = "#statusCenterServiceStackView"

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        configuration = Configuration(CDM(spice.ipaddress))
        is_enterprise = configuration.familyname == 'enterprise'

        self.MEDIA_ALERT_TITLE_CSTRINGS =  { 
        "standard_bin_full"               : "cStandardBinParam" if is_enterprise else "cOutputBinFullHeader",
        "bin_full"                      : "cVariableBinFull" if is_enterprise else None} # Note: homePro doesn't report binfull string alone.
        
        self.MEDIA_ALERT_CONTENT_CSTRINGS = {
        "standard_bin_full"               : "cRemoveAllPaperFromBin" if is_enterprise else "cOutputBinRemovePaper"
        }
        

    def click_on_substrate_source(self):
        substrate_source = self._spice.wait_for(MediaAppWorkflowObjectIds.SUBSTRATE_SOURCE)
        substrate_source.mouse_click()
        time.sleep(3)

    def click_on_output_options(self):
        output_options_tab = self._spice.wait_for(MediaAppWorkflowObjectIds.OUTPUT_OPTIONS)
        output_options_tab.mouse_click()
        time.sleep(3)

    def click_on_substrate_widget(self):
        substrate_widget = self._spice.wait_for(MediaAppWorkflowObjectIds.SUBSTRATE_WIDGET)
        substrate_widget.mouse_click()

    def click_on_widget_load_unload_button(self):
        load_unload_button = self._spice.wait_for(MediaAppWorkflowObjectIds.WIDGET_LOAD_UNLOAD_BUTTON)
        load_unload_button.mouse_click()

    def click_on_tur_button(self):
        tur_button = self._spice.wait_for(self.TUR_BUTTON)
        tur_button.mouse_click()

    def click_on_release_substrate_button(self):
        release_substrate_button = self._spice.wait_for(self.RELEASE_SUBSTRATE_BUTTON)
        release_substrate_button.mouse_click()

    def click_on_resuming_load_ok_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_resuming_load_info, timeout = 15)
        ok_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_resuming_load_info_continue, timeout = 15)
        ok_button.mouse_click()

    def click_on_select_media_type_button(self):
        time.sleep(5)
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info, timeout = 15)
        type_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.TYPE_SETTINGS, timeout = 15)
        type_selector.mouse_click()

    def click_on_substrate_load_cancel_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info, timeout = 15)
        cancel_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_cancel, timeout = 15)
        cancel_button.mouse_click()

    def click_on_media_load_cancel_msg_no_button(self): 
        no_action = self._spice.wait_for(MediaAppWorkflowObjectIds.CANCEL_MEDIA_LOAD_NO_BUTTON, timeout = 10)
        no_action.mouse_click()

    def click_on_media_load_cancel_msg_yes_button(self): 
        yes_action = self._spice.wait_for(MediaAppWorkflowObjectIds.CANCEL_MEDIA_LOAD_YES_BUTTON, timeout = 10)
        yes_action.mouse_click()

    def click_on_media_length_option(self):
        length_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_SETTINGS, timeout = 15)
        length_selector.mouse_click()
    
    def click_on_media_width_option(self):
        width_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.WIDTH_SETTINGS, timeout = 15)
        width_selector.mouse_click()

    def click_on_media_loading_options(self):
        # Scroll to the bottom of the view to find the desired option
        currentView = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info)
        currentView.mouse_wheel(0, -120)
        loading_options_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.LOADING_OPTIONS_SETTINGS, timeout = 15)
        loading_options_selector.mouse_click()
        self._spice.wait_for(MediaAppWorkflowObjectIds.loading_options_header)

    def select_manual_loading_method(self):
        loading_options_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.LOADING_METHOD_SETTINGS, timeout = 15)
        loading_options_selector.mouse_click()
        loading_options_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.LOADING_METHOD_RADIO_BUTTON.format(1), timeout = 15)
        loading_options_selector.mouse_click()

    def increase_skew(self, times):
        for i in range(times):
            increase_button = self._spice.wait_for(MediaAppWorkflowObjectIds.SKEW_SPINBOX)
            width = increase_button["width"]
            middle_height = increase_button["height"] / 2
            increase_button.mouse_click(width, middle_height)

    def decrease_skew(self, times):
        for i in range(times):
            increase_button = self._spice.wait_for(MediaAppWorkflowObjectIds.SKEW_SPINBOX)
            increase_button.mouse_click()

    def increase_right_edge_position_value(self, times):
        increase_button = self._spice.wait_for(MediaAppWorkflowObjectIds.RIGHT_EDGE_POSITION_SPINBOX_INCREASE_BUTTON)
        for i in range(times):
            increase_button.mouse_click()

    def decrease_right_edge_position_value(self, times):
        decrease_button = self._spice.wait_for(MediaAppWorkflowObjectIds.RIGHT_EDGE_POSITION_SPINBOX_DECREASE_BUTTON)
        for i in range(times):
            decrease_button.mouse_click()

    def click_on_media_length_radio_button(self, media_length_number):
        length_button = self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_RADIO_BUTTON.format(media_length_number), timeout = 10)
        length_button.mouse_click()

    def click_on_set_width_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_error_lateral_media_edge_not_found, timeout = 15)
        set_width_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_error_lateral_media_edge_not_found_continue, timeout = 15)
        set_width_button.mouse_click()

    def click_on_roll_width_done_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_roll_width, timeout = 15)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_roll_width_continue, timeout = 15)
        done_button.mouse_click()

    def click_on_roll_width_cancel_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_roll_width, timeout = 15)
        cancel_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_roll_width_cancel, timeout = 15)
        cancel_button.mouse_click()

    def click_on_skew_handling_continue_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_skew_handling_correcting_manually, timeout = 30)
        continue_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_skew_handling_correcting_manually_continue, timeout = 15)
        continue_button.mouse_click()

    def click_on_load_manual_feed_continue_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_manual_feed, timeout=15)
        continue_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_manual_feed_continue, timeout=15)
        continue_button.mouse_click()

    def click_on_load_manual_feed_with_accessory_continue_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_manual_feed_with_accessory, timeout=15)
        continue_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_manual_feed_with_accessory_continue, timeout=15)
        continue_button.mouse_click()

    def click_on_remove_loading_accessory_continue_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_remove_loading_accessory, timeout=15)
        continue_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_remove_loading_accessory_continue, timeout=15)
        continue_button.mouse_click()

    def click_on_move_media_to_cut_line_continue_button(self):
        self._spice.wait_for(MoveAndCutWorkflowObjectIds.view_move_and_cut_media_flow_ready_move_front_edge_to_cut_line)
        continue_button = self._spice.wait_for(MoveAndCutWorkflowObjectIds.move_and_cut_ready_move_front_edge_to_cut_line_continue_button) 
        continue_button.mouse_click()

    def click_on_move_media_to_roll_continue_button(self):
        self._spice.wait_for(MoveAndCutWorkflowObjectIds.view_move_and_cut_media_flow_ready_move_front_edge_to_roll)
        continue_button = self._spice.wait_for(MoveAndCutWorkflowObjectIds.move_and_cut_ready_move_front_edge_to_roll_continue_button) 
        continue_button.mouse_click()

    def click_on_more_options_button(self):
        more_option_button = self._spice.wait_for(MediaAppWorkflowObjectIds.MORE_OPTIONS_BUTTON)
        more_option_button.mouse_click()

    def click_on_modify_button(self):
        time.sleep(5)
        modify_button = self._spice.wait_for(MediaAppWorkflowObjectIds.MODIFY_BUTTON)
        assert modify_button["visible"] == True
        middle_width  = modify_button["width"]/2
        middle_height = modify_button["height"]/2
        modify_button.mouse_click(middle_width, middle_height)

    def click_on_modify_media_type_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration, timeout = 30)
        type_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.TYPE_SETTINGS, timeout = 15)
        type_selector.mouse_click()

    def click_on_modify_load_done_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration, timeout = 15)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration_done, timeout = 15)
        done_button.mouse_click()

    def click_on_media_type_radio_button(self, media_type_number):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 180
        found = False
        view = self._spice.wait_for("#typePanelHeader")

        while found == False & (time_spent_waiting < max_timeout):    
            try:
                media_type = self._spice.wait_for(MediaAppWorkflowObjectIds.TYPE_RADIO_BUTTON.format(media_type_number))
                media_type.mouse_click()
                time.sleep(2)
                type_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.TYPE_SETTINGS)
                assert type_selector["visible"] == True
                found = True
            except:
                view.mouse_wheel(0,-50)
                time_spent_waiting = time.time() - start_time

    def click_on_specific_media_type(self, media_name):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 120
        found = False
        view = self._spice.wait_for("#typePanelHeader")
        count = 0

        time.sleep(2)
        while found == False and (time_spent_waiting < max_timeout):   
            try:
                media_text = self._spice.query_item(MediaAppWorkflowObjectIds.TYPE_RADIO_BUTTON.format(count) + " SpiceText[visible=true]")
                if media_text["text"] != media_name:
                    count = count + 1
                    continue
                media_text.mouse_click()
                time.sleep(1)
                try:
                    type_selector = self._spice.wait_for("#typeSettingsTextImageBranch")
                    assert type_selector["visible"] == True
                    assert type_selector["enabled"] == True
                except:
                    view.mouse_wheel(0,-100)
                    continue
                found = True
            except:
                count = count + 1
                time_spent_waiting = time.time() - start_time

    def click_on_finish_load_ok_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_finished, timeout = 15)
        ok_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_finished_continue, timeout = 15)
        ok_button.mouse_click()
    
    def skip_substrate_load_recommendation(self):
        try:
            self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_load_recomendation_curing)
            skip_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_load_recomendation_curing_skip)
            skip_button.mouse_click()
        except:
            self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_load_recommendation_tur)
            skip_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_load_recommendation_tur_skip)
            skip_button.mouse_click()

    def wait_for_alert_dialog_window_type1(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE1), "Device not showing alert dialog."

    def wait_for_alert_dialog_window_type2(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE2), "Device not showing alert dialog."

    def wait_for_alert_dialog_window_type3(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
    
    def wait_for_alert_dialog_window_type4(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."

    def wait_for_alert_dialog_window(self, alert_type):
        if alert_type == "itbMissing":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type == "mediaMismatchSizeFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."
        if alert_type =="mediaLoadFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."
        if alert_type == "mediaMismatchTypeFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."
        if alert_type =="noFuser":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."
        if alert_type =="rearDoorOpenStatus":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE4), "Device not showing alert dialog."
        if alert_type =="shippingLockStatus":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."

    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def get_mediaLoadVerifyFlow_message(self, net, locale, PaperType, Size):
         self._spice.mediaapp.check_alert_message(LocalizationHelper.get_string_translation(net, ["cLoadPaperTray1", 1], locale)) #cLoadPaperTray1, Load Paper Tray 1
         loc_msg = LocalizationHelper.get_string_translation(net, ["cOOPwithOKtoUse", Size, PaperType, 1], locale)
         return loc_msg

    def get_alertMediaLoadFlow_message(self, net, locale, PaperType, Size):
        self._spice.mediaapp.check_alert_message(LocalizationHelper.get_string_translation(net, "cLoadPaperTitle", 'en-US'))
        loc_msg = LocalizationHelper.get_string_translation(net, [ "cOOPwithOKtoUse", PaperType, Size, 1], locale)
        return loc_msg

    def get_alertMediaMismatchFlow_message(self, net, locale, PaperType, Size):
        self._spice.mediaapp.check_alert_message(LocalizationHelper.get_string_translation(net, "cPaperSizeProblem", locale))
        loc_msg = LocalizationHelper.get_string_translation(net, [ "cUnexpectedSizeProblem", 1, PaperType, Size], locale)
        return loc_msg

    def wait_for_alert_window_dialogue_window_type(self):
        self._spice.mediaapp.wait_for_alert_dialog_window_type4()

    def get_alert_message(self):
        alertMessage = self._spice.wait_for(self.ALERT_TITLE_TEXT)
        return str(alertMessage["text"])

    def check_alert_message(self, text):
        alertMessage = self.get_alert_message()
        assert alertMessage == str(text)

    def get_alert_message_details(self):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        return str(alertMessageDetails["text"])

    def check_alert_message_details(self, text):
        alertMessageDetails = self.get_alert_message_details()
        assert alertMessageDetails == str(text)
    
    def verify_trayoverfilled_alert_screen(self ):
        alert_icon = self._spice.wait_for(MediaAppWorkflowObjectIds.alert_icon)
        try:
            assert str(alert_icon["source"]) == str("qrc:/images/Status/ErrorFill.json")
        except:
            assert str(alert_icon["source"]) == str("qrc:/images/Status/WarningFill.json")


    def check_sizeType_alert_message_details(self, loc_msg1, loc_msg2):
        alertMessageDetails1 = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_PART1)
        alertMessageDetails2 = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_PART2)
        time.sleep(20)
        assert str(alertMessageDetails1["text"]) == str(loc_msg1)
        assert str(alertMessageDetails2["text"]) == str(loc_msg2)

    def check_custom_alert_message_details(self, text):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        assert str(alertMessageDetails["text"]) == str(text)

    def check_custom_path_alert_message_details(self, path, text):
        alertMessageDetails = self._spice.wait_for( path + self.ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL )
        assert str(alertMessageDetails["text"]) == str(text)

    def validate_mediaMismatchTypeFlow_alert_message_details(self, net, locale):
        loc_msg = LocalizationHelper.get_string_translation(net, ["cPaperDetectedTrayMismatch", "Heavy (111-130g)", "A4 (210x297 mm)", 1, "Plain", "A4 (210x297 mm)"], locale)
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        assert str(alertMessageDetails["text"]) == str(loc_msg)        

    def check_toast_message(self, text):
        toastMessage = self._spice.wait_for(self.ALERT_TOAST_MESSAGE)
        assert str(toastMessage['text']) == str(text)

    def validate_sizeType_alert_title_and_message_details(self, net, locale, Size, PaperType):
        self.wait_for_alert_dialog_window_type2() 
        #cConfirmLoadedPaper,Confirm Loaded Paper
        loc_msgHeader = LocalizationHelper.get_string_translation(net, "cConfirmLoadedPaper", locale)
        self.check_alert_message(loc_msgHeader)
        #cTrayNColonTypeSizeLabel,"Tray %1$d: %2$s, %3$s"``
        loc_msg1 = LocalizationHelper.get_string_translation(net, "cTrayNColonTypeSizeLabel", locale)
        loc_msg1 = loc_msg1.replace("%1$d", "{}").replace("%2$s", "{}").replace("%3$s", "{}").format(2, PaperType, Size)
        self.check_alert_message_details(loc_msg1)
        #cChangeSizeTypeModify,"To change size or type, select ""Modify"".
        loc_msg2 = LocalizationHelper.get_string_translation(net, "cChangeSizeTypeTouchModify", locale)
        assert loc_msg2 == self._spice.query_item("#contentItem", query_index=1)["text"]
        #cAcceptTouchOK ,"To accept, select ""OK""."
        loc_msg3 = LocalizationHelper.get_string_translation(net, "cAcceptTouchOK", locale)
        assert loc_msg3 == self._spice.query_item("#contentItem", query_index=2)["text"]
        

    def validate_alert_dialogue(self):
        self.wait_for_alert_dialog_window_type4()

    def validate_alert_dialogue_outputBinFull(self):
        self.wait_for_alert_dialog_window_type4()

    def validate_trayOverfilled_icon(self):
        self.check_warning_icon() # trayOverFill alert is showing warning icon for Ulysses and error for Selene.

    def check_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/Status/ErrorFill.json")

    def check_image_status_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/Status/Error.json")

    def check_stateDecorator_image_status_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/StateDecorator/images/Error.json")

    def check_custom_error_icon(self):
        alertIcon = self._spice.wait_for("#AlertDetails1 #SpiceView")
        assert str(alertIcon["source"]) == str("qrc:/images/Glyph/MoreOptionsCircle.json")

    def check_warning_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/Status/WarningFill.json")

    def check_informative_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/StateDecorator/images/Informative.json")

    def check_details_icon(self, image):
        detailsIcon = self._spice.wait_for(self.ALERT_IMAGE_DETAILS_ICON)
        assert str(detailsIcon["source"]) == str(image)

    def goto_skew_acceptance_setting(self, net, locale: str = "en"):
        # Go to media app
        self._spice.homeMenuUI().goto_media_app_floating_dock(self._spice)

        # Click on Substrate source
        self.click_on_substrate_source()

        # Click on Load button
        self.click_on_load_button()

        # Click Resume button on 'Resume Substrate Load' screen
        self.click_on_resuming_load_ok_button()

        # Check substrate load screen
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info, timeout = 15)
        header_title = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_title)
        assert str(LocalizationHelper.get_string_translation(net, "cLoadPaper", locale)) == str(header_title["text"])

        # Click on media loading options
        self.click_on_media_loading_options()

    def exit_loading_options_screen_and_cancel_load(self):
        # Exit "Loading options" screen
        self._spice.wait_for(MediaAppWorkflowObjectIds.loading_options_header)
        back_button = self._spice.wait_for("#BackButton")
        middle_width  = back_button["width"] / 2
        middle_height = back_button["height"] / 2
        back_button.mouse_click(middle_width, middle_height)

        # Click "Done" on substrate load screen
        self.click_on_substrate_load_done_button()

        # Click on "Set Width" button
        self.click_on_set_width_button()

        # Click "Cancel" on roll width screen
        self.click_on_roll_width_cancel_button()

        # Confirm paper load cancelation
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_cancel)
        yes_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_cancel_yes_button)
        yes_button.mouse_click()

    def click_resume_on_risk_paper_jam_screen(self):
        '''
        Click "Resume" on Risk of Paper Jam screen
        '''
        self._spice.wait_for(MediaAppWorkflowObjectIds.risk_of_paper_jam)
        resume_button = self._spice.wait_for(MediaAppWorkflowObjectIds.risk_of_paper_jam_resume)
        resume_button.mouse_click()

    def set_media_length_button(self, media_length):
        '''
        Set media length button
        '''
        length_text_input = self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_TEXT_INPUT)
        length_text_input.mouse_click()
        length_text_input["text"] = int(media_length)
        enter_key = self._spice.wait_for(MediaAppWorkflowObjectIds.ENTER_KEY_DECIMAL_PAD)
        enter_key.mouse_click()

    def set_media_width_button(self, media_width):
        '''
        Set media width button
        '''
        width_text_input = self._spice.wait_for(MediaAppWorkflowObjectIds.WIDTH_TEXT_INPUT)
        width_text_input.mouse_click()
        width_text_input["text"] = int(media_width)
        enter_key = self._spice.wait_for(MediaAppWorkflowObjectIds.ENTER_KEY_INTEGER_PAD)
        enter_key.mouse_click()

    def set_media_width_value(self, media_width_value):
        '''
        Set media width value
        '''
        self._spice.mediaapp.workflow_common_operations.scroll_to_position_vertical_without_scrollbar(MediaAppWorkflowObjectIds.WIDTH_SETTINGS)
        self._spice.mediaapp.click_on_media_width_option()
        self._spice.mediaapp.set_media_width_button(media_width_value)   
        self._spice.common_operations.click_on_back_button() 
