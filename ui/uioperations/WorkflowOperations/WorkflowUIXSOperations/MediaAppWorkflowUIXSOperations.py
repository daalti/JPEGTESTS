
import logging
import time

from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowUICommonOperations import MediaAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds

class MediaAppWorkflowUIXSOperations(MediaAppWorkflowUICommonOperations):
    ALERT_DETAIL_DESCRIPTION_PART1 = "#alertModalView #alertDetailDescription #titleBigItem"
    ALERT_DETAIL_DESCRIPTION_PART2 = "#alertModalView #alertShortDescription #titleSmallItem"
    ALERT_DETAIL_DESCRIPTION = "#contentItem"
    ALERT_DIALOG_WINDOW_TYPE1 = "#AlertModelView"
    ALERT_DIALOG_WINDOW_TYPE2 = "#alertModalView"
    ALERT_DIALOG_WINDOW_TYPE3 = "#AlertDetails1"
    ALERT_DIALOG_WINDOW_TYPE4 = "#nativeStackView"
    ALERT_TITLE_TEXT = "#titleObject"
    ALERT_IMAGE_ICON = "#imageObject"
    ALERT_DIALOG_TOAST_WINDOW = "#SpiceToast"
    ALERT_DETAIL_DESCRIPTION_CUSTOM = "#AlertModelView #alertDetailDescription #contentItem"
    ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL = " #alertDetailDescription #contentItem"
    ALERT_TOAST_MESSAGE = "#infoTextToastMessage"
    ALERT_IMAGE_DETAILS_ICON = "#alertStatusImage SpiceLottieImageView"
    ALERT_LOAD_MEDIA_VERIFY_FLOW = "#statusCenterServiceStackView"

    alert_window = ["badOptionalCassetteConnection1Window"]

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def get_alert_message(self):
        alertMessage = self._spice.wait_for(self.ALERT_TITLE_TEXT)
        return str(alertMessage["text"])

    def get_alert_active_focus_index(self):
        index = 0
        for idx in [0,1,2,3]:
            try:
                active_index = self._spice.query_item("#AlertModelView", idx)['activeFocus']
                if active_index:
                    index = idx
                    break
            except:
                logging.info("Alert index not found")
        return index

    def get_alert_message_details(self):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        return str(alertMessageDetails["text"])

    def check_alert_message(self, text):
        alertMessage = self.get_alert_message()
        assert alertMessage == str(text)

    def check_alert_message_details(self, text):
        alertMessageDetails = self.get_alert_message_details()
        assert alertMessageDetails == str(text)

    def check_error_icon(self):
        alertIcon = self._spice.wait_for(self.ALERT_IMAGE_ICON)
        assert str(alertIcon["source"]) == str("qrc:/images/Status/ErrorFill.json")

    def check_custom_alert_message_details(self, text):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        assert str(alertMessageDetails["text"]) == str(text)

    def wait_for_alert_window_dialogue_window_type(self):
        self._spice.mediaapp.wait_for_alert_dialog_window_type4()

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

    def check_sizeType_alert_message_details(self, loc_msg1, loc_msg2):
        alertMessageDetails1 = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_PART1)
        alertMessageDetails2 = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION_PART2)
        assert str(alertMessageDetails1["text"]) == str(loc_msg1)
        assert str(alertMessageDetails2["text"]) == str(loc_msg2)

    def validate_sizeType_alert_title_and_message_details(self, net, locale, Size, PaperType):
        self.wait_for_alert_dialog_window_type4() 
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

    def check_custom_path_alert_message_details(self, path, text):
        alertMessageDetails = self._spice.wait_for( path + self.ALERT_DETAIL_DESCRIPTION_CUSTOM_PARTIAL )
        assert str(alertMessageDetails["text"]) == str(text)

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


    def check_toast_message(self, text):
        toastMessage = self._spice.wait_for(self.ALERT_TOAST_MESSAGE)
        assert str(toastMessage['text']) == str(text)