#########################################################################################
# @file      ToolsAppWorkflowUICommonOperations.py
# @author    Srinivas
# @date      27-01-2022
# @brief     Interface for all the Fax Diagnostics methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################

from time import sleep
import logging
import random

from dunetuf.ui.uioperations.BaseOperations.IToolsUIOperations import IToolsUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ToolsAppWorkflowObjectIds import ToolsAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper

_logger = logging.getLogger(__name__)

class ToolsAppWorkflowUICommonOperations(IToolsUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice

    def maintenancemenu_restoresettings_check_visibility_of_restore_button_under_restoreallfactorydefaults(self):
        """
        Check Restore button is displayed under screen Restore All Factory Defaults
        """
        logging.info("Check Restore button is displayed under screen Restore All Factory Defaults")
        self._spice.wait_for(ToolsAppWorkflowObjectIds.restore_all_factory_defaults_view)
        restore_button = self._spice.wait_for(ToolsAppWorkflowObjectIds.restore_button_under_restore_all_factory_defaults_view)
        self._spice.wait_until(lambda: restore_button["visible"] is True)

    def maintenancemenu_restoresettings_check_visibility_of_cancel_button_under_restoreallfactorydefaults(self):
        """
        Check Cancel button is displayed under screen Restore All Factory Defaults
        """
        logging.info("Check Cancel button is displayed under screen Restore All Factory Defaults")
        self._spice.wait_for(ToolsAppWorkflowObjectIds.restore_all_factory_defaults_view)
        cancel_button = self._spice.wait_for(ToolsAppWorkflowObjectIds.cancel_button_under_restore_all_factory_defaults_view)
        self._spice.wait_until(lambda: cancel_button["visible"] is True)

    def maintenancemenu_restoresettings_click_cancel_button_under_restoreallfactorydefaults(self):
        """
        Click Cancel button to back to previous screen
        """
        logging.info("Click Cancel button to back to previous screen")
        self._spice.wait_for(ToolsAppWorkflowObjectIds.restore_all_factory_defaults_view)
        cancel_button = self._spice.wait_for(ToolsAppWorkflowObjectIds.cancel_button_under_restore_all_factory_defaults_view)
        self._spice.wait_until(lambda: cancel_button["visible"] is True)
        cancel_button.mouse_click()
        restore_settings_menu_view = self._spice.wait_for(ToolsAppWorkflowObjectIds.restore_settings_menu_view)
        self._spice.wait_until(lambda: restore_settings_menu_view["visible"] is True)

    def validate_tools_reports_event_log(self,spice,qml,eventName,descText,validate):
        
        main_object_name = "#eventLogViewlist1"
        # Take the scroll bar object from the list and pass it
        scroll_bar_name = "#eventLogViewlist1ScrollBar"
        if validate:
            logging.debug("Event log will be validated in detail")
            spice.homeMenuUI().navigate_through_pagination(spice, scroll_bar_name,main_object_name,eventName, False)
            eventLogDetailsObj = self._spice.wait_for(eventName)
            eventLogDetailsObj.mouse_click()

            # Scroll down to info.
            self._spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical(0.2, "#DetailInfoverticalLayoutScrollBar")
            eventDetails = self._spice.wait_for("#eventLogDetailInfo #errorCode")
            assert descText == qml.query_item("#description #ValueText")["text"]
        else:
            logging.debug("Event log will not be validated in detail")
            object_name = spice.homeMenuUI().navigate_through_pagination(spice, scroll_bar_name,main_object_name,eventName, False)
    
    def validate_user_activity_fw_update(self, spice):
        # Wait for screen asking if should check for update
        current_screen = spice.wait_for("#fwUpCheckUpdate",30)
        # Click yes for check for update
        current_screen.mouse_click()

        #Printer check for the update if available
        # not_avbl = spice.wait_for("#fwupdateNotAvailableOk", 120)
        # not_avbl.mouse_click()

        # Wait to get back to maintenance screen
        current_screen = spice.wait_for("#fwUpCheckUpdate",60)
    
    def verify_toast_message(self, message):
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window)
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo,10)["text"] == message

    def check_tray_alignment_apply(self, cdm, tray):
        card_id = MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality_image_registration_tray

        # If we have more than one tray, we need to add the tray number to the card_id
        # for this test tray 1 will work as the test tray.
        if (tray.get_supported_tray_count() > 1):
            card_id += "1"

        # Randomly generate the new tray alignment values
        new_tray_values = []
        for i in range(4):
            if i%2 == 0:
                new_tray_values.append(random.randrange(-20,21,1)*0.25)
            else:
                new_tray_values.append(random.randrange(-20,7,1)*0.25)

        # Navigate to Tray alignment menu
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality_image_registration).mouse_click()
        self._spice.wait_for(card_id).mouse_click()

        # Set the Front and Back vertical and horizontal  shift values
        tray_objects = []
        tray_original_values = []
        spin_box_ids = ["#spinBoxfrontSideHorizontalShift", "#spinBoxfrontSideVerticalShift", "#spinBoxbackSideHorizontalShift", "#spinBoxbackSideVerticalShift"]
        for i in range(4):
            tray_obj = self._spice.wait_for(spin_box_ids[i])
            tray_objects.append(tray_obj)
            tray_original_values.append(tray_obj.__getitem__("value"))
            tray_obj.__setitem__("value", new_tray_values[i])

        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_apply).mouse_click()
        # Wait for new tray alignment values to reflect in CDM.
        sleep(2)
        # Get the values from CDM
        media_configuration = cdm.get_raw(cdm.CDM_MEDIA_CONFIGURATION).json()
        # Verify the new tray alignment values
        assert media_configuration["inputs"][0]["frontSideHorizontalShift"] == new_tray_values[0] , "frontSideHorizontalShift new Value is not updated"
        assert media_configuration["inputs"][0]["frontSideVerticalShift"] == new_tray_values[1] , "frontSideVerticalShift new Value is not updated"
        assert media_configuration["inputs"][0]["backSideHorizontalShift"] == new_tray_values[2] , "backSideHorizontalShift new Value is not updated"
        assert media_configuration["inputs"][0]["backSideVerticalShift"] == new_tray_values[3] , "backSideVerticalShift new Value is not updated"

        # Set the values back to original values
        self._spice.wait_for(card_id).mouse_click()
        sleep(1)
        for i in range(4):
            tray_objects[i].__setitem__("value",tray_original_values[i])
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_apply).mouse_click()
        # Get the values from CDM
        media_configuration = cdm.get_raw(cdm.CDM_MEDIA_CONFIGURATION).json()
        # Verify the original tray alignment values
        assert media_configuration["inputs"][0]["frontSideHorizontalShift"] == tray_original_values[0] , "frontSideHorizontalShift new Value is not updated"
        assert media_configuration["inputs"][0]["frontSideVerticalShift"] == tray_original_values[1] , "frontSideVerticalShift new Value is not updated"
        assert media_configuration["inputs"][0]["backSideHorizontalShift"] == tray_original_values[2] , "backSideHorizontalShift new Value is not updated"
        assert media_configuration["inputs"][0]["backSideVerticalShift"] == tray_original_values[3] , "backSideVerticalShift new Value is not updated"

        logging.debug("Verify toast window message")
        self._spice.wait_for(MenuAppWorkflowObjectIds.view_toast_window,10)
        assert self._spice.wait_for(MenuAppWorkflowObjectIds.view_troubleshooting_fax_toastinfo,10)["text"] == "Tray values saved"
        self._spice.query_item("#HomeButton #ButtonControl")
        sleep(2)

    def check_tray_alignment_menu(self, tray, button_id):
        card_id = MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality_image_registration_tray

        # If we have more than one tray, we need to add the tray number to the card_id
        # for this test tray 1 will work as the test tray.
        if (tray.get_supported_tray_count() > 1):
            card_id += "1"

        # Navigate to Tray alignment menu.
        self._spice.wait_for(card_id).mouse_click()
        self._spice.wait_for(button_id).mouse_click()

    def troubleshooting_print_quality_image_registration(self, cdm, tray):
        # Verify Apply Button.
        self.check_tray_alignment_apply(cdm, tray)

        # Verify closeButton in Tray alignment menu.
        self.check_tray_alignment_menu(tray, MenuAppWorkflowObjectIds.menu_button_close)

        # Verify printButton in Tray alignment menu.
        self.check_tray_alignment_menu(tray, MenuAppWorkflowObjectIds.menu_button_print_button)
        self.verify_toast_message("Printing...")

        # Close the menu.
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_close).mouse_click()

    def validate_image_registration_limits(self, tray, net):
        card_id = MenuAppWorkflowObjectIds.menu_button_troubleshooting_print_quality_image_registration_tray

        # If we have more than one tray, we need to add the tray number to the card_id
        # for this test tray 1 will work as the test tray.
        if (tray.get_supported_tray_count() > 1):
            card_id += "1"

        # Navigate to Tray alignment menu
        self._spice.wait_for(card_id).mouse_click()

        # Array of sections
        sections = [ 
            {
                "id": ToolsAppWorkflowObjectIds.front_horizontal_shift_section, 
                "title": "cConfigAppPQX1Shift",
                "spin_box": ToolsAppWorkflowObjectIds.front_horizontal_shift_spin_box,
                "min": "-5.00",
                "max": "5.00",
                "required": True
            },
            {
                "id": ToolsAppWorkflowObjectIds.front_vertical_shift_section,
                "title": "cTrayY1Shift",
                "spin_box": ToolsAppWorkflowObjectIds.front_vertical_shift_spin_box,
                "min": "-5.00",
                "max": "1.50",
                "required": True
            },
            {
                "id": ToolsAppWorkflowObjectIds.back_horizontal_shift_section,
                "title": "cConfigAppPQX2Shift",
                "spin_box": ToolsAppWorkflowObjectIds.back_horizontal_shift_spin_box,
                "min": "-5.00",
                "max": "5.00",
                "required": False
            },
            {
                "id": ToolsAppWorkflowObjectIds.back_vertical_shift_section,
                "title": "cTrayY2Shift",
                "spin_box": ToolsAppWorkflowObjectIds.back_vertical_shift_spin_box,
                "min": "-5.00",
                "max": "1.50",
                "required": False
            }
        ]

        # Validate each section has the correct title and range
        for section in sections:
            title_id = section["id"] + " " + ToolsAppWorkflowObjectIds.text_view
            spin_box_text_id = section["spin_box"] + " " + ToolsAppWorkflowObjectIds.text_view
            expected_spin_box_range_text = "mm (" + section["min"] + " to " + section["max"] + ")"

            # Check if the section exists, if its optional and not found, continue
            try:
                assert self._spice.wait_for(section["id"])
            except:
                if section["required"]:
                    title = str(LocalizationHelper.get_string_translation(net, section["title"]))
                    assert False, "Section " + title + " not found"
                else:
                    continue

            # Validate that the section has the correct title
            assert self._spice.wait_for(title_id)["text"] == LocalizationHelper.get_string_translation(net, section["title"])
            # Validate that the spin box has the correct range
            assert self._spice.wait_for(spin_box_text_id)["text"] == expected_spin_box_range_text

        # Close the menu
        self._spice.wait_for(MenuAppWorkflowObjectIds.menu_button_close).mouse_click()