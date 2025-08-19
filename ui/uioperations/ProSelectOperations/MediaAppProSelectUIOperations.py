#########################################################################################
# @file      MediaAppProSelectUIOperations.py
# @author    Carlos Criado (carlos.criado@hp.com)
# @date      25-11-2021
# @brief     Implementation for all the Media UI methods
# (c) Copyright HP Inc. 2021. All rights reserved.
#########################################################################################

import re
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.BaseOperations.IMediaAppUIOperations import IMediaAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds
import logging 

class MediaAppProSelectUIOperations(IMediaAppUIOperations):
    ALERT_DIALOG_WINDOW_TYPE1 = "#AlertDetails1"
    ALERT_DIALOG_WINDOW_TYPE2 = "#SpiceStackView"
    ALERT_DIALOG_WINDOW_TYPE3 = "#nativeStackView"
    ALERT_DIALOG_TOAST_WINDOW = "#ToastSystemToastStackView"
    ALERT_TITLE_TEXT = "#MessageLayout #TitleText #Version1Text"
    ALERT_TITLE_TEXT_CUSTOM = "#MessageLayout #TitleText #Version1Text"
    ALERT_DETAIL_DESCRIPTION = "#MessageLayout #DetailTexts #Version2Text"
    ALERT_DETAIL_DESCRIPTION_PART1 = "#alertModalView #alertDetailDescription #titleBigItem"
    ALERT_DETAIL_DESCRIPTION_PART2 = "#alertModalView #alertShortDescription #titleSmallItem"
    ALERT_DETAIL_DESCRIPTION_CUSTOM = "#MessageLayout #DetailTexts #Version2Text"
    ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL = " #DetailTexts #Version2Text"
    ALERT_TOAST_MESSAGE = "#ToastBase #ToastInfoText"
    ALERT_IMAGE_ICON = "#MessageLayout #MessageIcon"
    ALERT_TOAST_ICON = "#ToastBase #ToastIconForText"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage SpiceLottieImageView"
    ALERT_LOAD_MEDIA_VERIFY_FLOW = "#mediaLoadVerifyFlowWindow"

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        
        self.MEDIA_ALERT_TITLE_CSTRINGS =  {"standard_bin_full" : "cOutputBinFullHeader" }
        self.MEDIA_ALERT_CONTENT_CSTRINGS = {"standard_bin_full" : "cOutputBinRemovePaper"}

    def wait_for_alert_dialog_window_type1(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE1), "Device not showing alert dialog."

    def wait_for_alert_dialog_window_type2(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE2), "Device not showing alert dialog."

    def wait_for_alert_dialog_window_type3(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
    
    def get_mediaLoadVerifyFlow_message(self, net, locale, PaperType, Size):
        loc_msg = LocalizationHelper.get_string_translation(net, ["cOOPwithOKtoUse", PaperType, Size, 1], locale)
        return loc_msg

    def get_alertMediaLoadFlow_message(self, net, locale, PaperType, Size):
        self._spice.mediaapp.check_alert_message(LocalizationHelper.get_string_translation(net, "cLoadPaperTitle", locale))
        loc_msg = LocalizationHelper.get_string_translation(net, ["cOOPwithOKtoUseMedia", PaperType, Size, 1], locale)
        return loc_msg
    
    def get_alertMediaMismatchFlow_message(self, net, locale, PaperType, Size):
        self._spice.mediaapp.check_alert_message_type1(LocalizationHelper.get_string_translation(net, "cPaperSizeProblem", locale))
        loc_msg = LocalizationHelper.get_string_translation(net, ["cUnexpectedSizeProblem", 1, PaperType, Size], locale)
        return loc_msg

    def wait_for_alert_dialog_window(self, alert_type):
        if alert_type == "itbMissing":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type == "mediaMismatchSizeFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type == "mediaLoadFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type == "mediaMismatchTypeFlow":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type =="noFuser":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type =="rearDoorOpenStatus":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."
        if alert_type =="shippingLockStatus":
            assert self._spice.wait_for(self.ALERT_DIALOG_WINDOW_TYPE3), "Device not showing alert dialog."

    def wait_for_alert_dialog_toast_window(self):
        assert self._spice.wait_for(self.ALERT_DIALOG_TOAST_WINDOW), "Device not showing toast alert message."

    def wait_for_alert_window_dialogue_window_type(self):
        self.wait_for_alert_dialog_window_type1()
    
    def verify_trayoverfilled_alert_screen(self ):
        alert_icon = self._spice.wait_for(MediaAppWorkflowObjectIds.alert_tray_overfilled)
        

    def get_alert_message(self):
        alertMessage = self._spice.wait_for(self.ALERT_TITLE_TEXT)
        return str(alertMessage["text"])

    def check_alert_message(self, text):
        alertMessage = self.get_alert_message()
        assert alertMessage == str(text)

    def check_alert_message_type1(self, text):
        alertMessage = self._spice.wait_for(self.ALERT_TITLE_TEXT_CUSTOM)
        assert str(alertMessage["text"]) == str(text)

    def get_alert_message_details(self):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        return str(alertMessageDetails["text"])

    def check_alert_message_details(self, text):
        alertMessageDetails = self.get_alert_message_details()
        assert alertMessageDetails == str(text)

    def check_sizeType_alert_message_details(self, text):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_CUSTOM)
        assert str(alertMessageDetails["text"]) == str(text)

    def check_custom_alert_message_details(self, text):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_CUSTOM)
        assert str(alertMessageDetails["text"]) == str(text)

    def check_custom_path_alert_message_details(self, path, text):
        alertMessageDetails = self._spice.wait_for( path + self.ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL )
        assert str(alertMessageDetails["text"]) == str(text)

    def validate_mediaMismatchTypeFlow_alert_message_details(self, net, locale):
        loc_msg = LocalizationHelper.get_string_translation(net, ["cPaperDetectedMismatch", "Heavy (111-130g)", "A4 (210x297 mm)", "Plain", "A4 (210x297 mm)"], locale)
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        assert str(alertMessageDetails["text"]) == str(loc_msg)

    def check_toast_message(self, text):
        toastMessage = self._spice.wait_for(self.ALERT_TOAST_MESSAGE)
        assert str(toastMessage["text"]) == str(text), "Failed to match the toast message."
        # Verify toast icon type. Workflow code does not have this following piece of code implemented as toast icon is missing in workflow.
        self.check_toast_warning_icon()

    def validate_sizeType_alert_title_and_message_details(self, net, locale, Size, PaperType):
        #cDidYouChangePaper,Did you change the paper?
        #cSizeTypeChangeMulti,"Tray %1$d: %2$s, %3$s\nTo change size or type, select ""Modify"".\nTo accept, select ""OK""."
        loc_msgHeader = LocalizationHelper.get_string_translation(net, "cDidYouChangePaper", locale)
        loc_msg1 = LocalizationHelper.get_string_translation(net, ["cSizeTypeChangeMulti", 2, Size, PaperType], locale)
        self.check_alert_message_type1(loc_msgHeader)
        self.check_sizeType_alert_message_details(loc_msg1)

    def validate_alert_dialogue(self):
        self.wait_for_alert_dialog_window_type3()

    def validate_trayOverfilled_icon(self):
        self.check_custom_error_icon() 

    def check_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/error_xs.json")

    def check_image_status_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/error_xs.json")

    def check_stateDecorator_image_status_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/error_xs.json")

    def check_custom_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/error_xs.json")

    def check_warning_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/images/+loTheme/warning_xs.json")

    def check_informative_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["icon"]) == str("qrc:/StateDecorator/images/Informative.json")

    def check_toast_warning_icon(self):
        # Verify toast icon type. Workflow code does not have this following piece of code implemented as toast icon is missing in workflow.
        alertIcon = self._spice.wait_for(self.ALERT_TOAST_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/+loTheme/warning_xs.json")

    def check_details_icon(self, image):
        detailsIcon = self._spice.wait_for(self.ALERT_IMAGE_DETAILS_ICON)
        assert str(detailsIcon["icon"]) == str(image)
