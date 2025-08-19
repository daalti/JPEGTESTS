import time
import logging
from dunetuf.ui.uioperations.BaseOperations.IMediaAppUIOperations import IMediaAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.cdm.CdmUnitOfMeasure import CdmUnitOfMeasure
class MediaAppWorkflowUICommonOperations(IMediaAppUIOperations):

    def __init__(self, spice):
        self._spice = spice
        self.maxtimeout = 120
        self.workflow_common_operations = self._spice.basic_common_operations

    def click_on_output_options_tab(self):
        media_grid_tab_layout_app = self._spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_GRID_TAB_LAYOUT)
        media_grid_tab_layout_app["currentIndex"] = "1"
        media_grid_tab_layout_app.mouse_click()

    def click_on_load_button(self):
        load_button = self._spice.wait_for(MediaAppWorkflowObjectIds.LOAD_BUTTON)
        load_button.mouse_click()

    def click_on_unload_button(self):
        unload_button = self._spice.wait_for(MediaAppWorkflowObjectIds.UNLOAD_BUTTON)
        unload_button.mouse_click()

    def click_on_move_and_cut_button(self):
        move_and_cut_button = self._spice.wait_for(MediaAppWorkflowObjectIds.MOVE_AND_CUT_BUTTON)
        move_and_cut_button.mouse_click()
        time.sleep(3)

    def click_on_barcode_button(self):
        barcode_button = self._spice.wait_for(MediaAppWorkflowObjectIds.BARCODE_BUTTON)
        barcode_button.mouse_click()

    def click_on_cut_button(self):
        cut_button = self._spice.wait_for(MediaAppWorkflowObjectIds.CUT_BUTTON_ACTION)
        cut_button.mouse_click()

    def click_on_check_and_continue_button(self):
        self._spice.homeMenuUI().wait_for_visible_enabled_and_click(self._spice, MediaAppWorkflowObjectIds.CONTINUE_ACTION)

    def click_on_load_another_action(self):
        load_another = self._spice.wait_for(MediaAppWorkflowObjectIds.LOAD_ANOTHER_ACTION)
        load_another.mouse_click()

    def click_on_substrate_load_done_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info, timeout = 15)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_ask_media_info_continue, timeout = 15)
        done_button.mouse_click()

    def click_on_sheet_load_done_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_single_sheet_ask_media_info, timeout = 15)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.load_single_sheet_ask_media_info_continue, timeout = 15)
        done_button.mouse_click()

    def click_on_load_tray_ok(self):
        load_tray_ok = self._spice.wait_for(MediaAppWorkflowObjectIds.load_tray_changemedia_ok)
        load_tray_ok.mouse_click()

    def click_on_load_tray_modify(self):
        load_tray_modify = self._spice.wait_for(MediaAppWorkflowObjectIds.load_tray_changemedia_modify)
        load_tray_modify.mouse_click()

    def click_on_load_tray_type_list(self):
        load_tray_modify = self._spice.wait_for(MediaAppWorkflowObjectIds.load_ctray_changemedia_type_list)
        load_tray_modify.mouse_click()

    def click_on_load_tray_family_type_list(self):
        load_tray_modify = self._spice.wait_for(MediaAppWorkflowObjectIds.load_ctray_changemedia_family_type_list)
        load_tray_modify.mouse_click()

    def click_on_load_tray_size_list(self):
        load_tray_modify = self._spice.wait_for(MediaAppWorkflowObjectIds.load_ctray_changemedia_size_list)
        load_tray_modify.mouse_click()

    def click_on_load_tray_done(self):
        load_tray_done = self._spice.wait_for(MediaAppWorkflowObjectIds.load_tray_askMediaInfo_continue)
        load_tray_done.mouse_click()

    def click_on_specific_media_family(self, media_family):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 120
        found = False
        view = self._spice.wait_for("#familyPanelHeader")
        count = 0

        while found == False and (time_spent_waiting < max_timeout):
            try:
                media_family_text = self._spice.wait_for("#familyTextImageBranch" + str(count) + " SpiceText[visible=true]")
                if media_family_text["text"] != media_family:
                    count = count + 1
                    continue
                media_family_text.mouse_click()
                time.sleep(1)
                type_selector = self._spice.wait_for("#typePanelHeader")
                assert type_selector["visible"] == True
                assert type_selector["enabled"] == True
                found = True
            except:
                step = -50*count
                view.mouse_wheel(0, step)
                time_spent_waiting = time.time() - start_time

    def recover_input_card_media_type_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_TYPE_VALUE, timeout=15)
        media_type_value = self._spice.query_item(MediaAppWorkflowObjectIds.MEDIA_TYPE_VALUE, 1)
        return media_type_value["text"]

    def recover_input_card_media_width_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.WIDTH_TYPE_VALUE, timeout=15)
        media_width_value = self._spice.query_item(MediaAppWorkflowObjectIds.WIDTH_TYPE_VALUE, 1)
        return media_width_value["text"]

    def recover_input_card_media_length_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_TYPE_VALUE, timeout=15)
        media_length_value = self._spice.query_item(MediaAppWorkflowObjectIds.LENGTH_TYPE_VALUE, 1)
        return media_length_value["text"]

    def recover_input_card_media_size_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.SIZE_TYPE_VALUE, timeout=15)
        media_size_value = self._spice.query_item(MediaAppWorkflowObjectIds.SIZE_TYPE_VALUE, 1)
        return media_size_value["text"]

    def recover_input_card_media_calibration_status_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.CALIBRATION_STATUS_TYPE_VALUE, timeout=15)
        media_calibration_status_value = self._spice.query_item(MediaAppWorkflowObjectIds.CALIBRATION_STATUS_TYPE_VALUE, 1)
        return media_calibration_status_value["text"]

    def retrieve_input_card_media_right_edge_position_value(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.RIGHT_EDGE_POSITION_VALUE, timeout=15)
        media_right_edge_position_value = self._spice.query_item(MediaAppWorkflowObjectIds.RIGHT_EDGE_POSITION_VALUE, 1)
        return media_right_edge_position_value["text"]

    def click_on_specific_media_size(self, media_size):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 120
        found = False
        view = self._spice.wait_for("#sizePanelHeader")
        count = 0

        time.sleep(2)
        while found == False and (time_spent_waiting < max_timeout):
            try:
                media_text = self._spice.query_item(MediaAppWorkflowObjectIds.TYPE_RADIO_BUTTON.format(count) + " SpiceText[visible=true]")
                if media_text["text"] != media_size:
                    count = count + 1
                    continue
                media_text.mouse_click()
                time.sleep(1)
                try:
                    type_selector = self._spice.wait_for("#sizeSettingsTextImageBranch")
                    assert type_selector["visible"] == True
                    assert type_selector["enabled"] == True
                except:
                    view.mouse_wheel(0,-100)
                    continue
                found = True
            except:
                count = count + 1
                time_spent_waiting = time.time() - start_time

    def set_media_size(self, spice, input_size):
        # Click on the 'Size Modify' selection
        button_media_size_settings = spice.wait_for(MenuAppWorkflowObjectIds.button_media_size_settings)
        button_media_size_settings.mouse_click()
        logging.info("At tray1 media size settings Screen")
        # Wait for the media size list view to be visible
        view_list = spice.wait_for("#mediaSizeListView", timeout=10)
        spice.wait_until(lambda:view_list["visible"])
        scrollbar = spice.wait_for("#mediaSizeListViewScrollBar", timeout=10)
        spice.wait_until(lambda:scrollbar["visible"])
        # Select the input media size value
        self.workflow_common_operations.goto_item(input_size, "#mediaSizeListView", select_option = False, scrollbar_objectname = "#mediaSizeListViewScrollBar")

        media_item = spice.wait_for(input_size)
        media_item.mouse_click()

    def set_media_type(self, spice, input_type, object_type):
        spice.homeMenuUI().goto_menu_trays(spice)
        if spice.uisize == "S" or spice.uisize == "XS":
        # Click on the spice card
            spiceCard = spice.wait_for(MenuAppWorkflowObjectIds.view_menuTray)
            spiceCard.mouse_click()
            # Verify that the Tray1 text is visible on the widget
            assert spice.wait_for(MenuAppWorkflowObjectIds.menu_tray1)["visible"] == True, "Tray 1 Text is not visible on widget"
        # Click on the 'Modify' button
        modify_Button = spice.wait_for(MenuAppWorkflowObjectIds.modify_Button)
        modify_Button.mouse_click()
        logging.info("At tray1 modify Screen")
        
        button_media_type_settings = spice.wait_for(MenuAppWorkflowObjectIds.button_media_type_settings)
        button_media_type_settings.mouse_click()
        logging.info("At tray1 media type settings Screen")
        # Wait for the media type list view to be visible
        view_list = spice.wait_for("#mediaTypeListView", timeout=10)
        spice.wait_until(lambda:view_list["visible"])
        scrollbar = spice.wait_for("#mediaTypeListViewScrollBar", timeout=10)
        spice.wait_until(lambda:scrollbar["visible"])
        # Select the input media type value
        self.workflow_common_operations.goto_item(input_type, "#mediaTypeListView", select_option = False, scrollbar_objectname = "#mediaTypeListViewScrollBar")
        media_item_type = spice.wait_for(object_type)
        if spice.wait_for(object_type, timeout = 15)["checked"] is True:
            logging.info(f"Media type {input_type} is already selected")
            logging.info("Pressing BACK to exit media type selection")
            spice.udw.mainUiApp.KeyHandler.setKeyPress("BACK")
        else:
            media_item_type.mouse_click()


    def goto_media_source_from_media_app(self, spice, cdm, net, source_str: str,  locale: str = "en-US"):
        source_local_str = LocalizationHelper.get_string_translation(net, source_str, locale)
        logging.info(f"goto_media_source: {source_local_str}")
        response = cdm.get(cdm.CDM_MEDIA_CAPABILITIES)
        numberOfTrays = len(response["supportedInputs"])
        index_source = -1
        for i in range(numberOfTrays):
            input_card = spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_INPUT_CARD_TYPE, query_index = i)
            if source_local_str == input_card["text"]:
                index_source = i
                break
        assert index_source >= 0
        spice.homeMenuUI().workflow_common_operations.scroll_to_position_vertical_without_scrollbar(MediaAppWorkflowObjectIds.MEDIA_INPUT_CARD, index_source)

    def check_current_card_values(self, spice, cdm, net, media_type_id_str: str, width_inch_str: str, locale: str = "en-US"):
        logging.info("Checking card values...")
        try:
            assert spice.mediaapp.recover_input_card_media_type_value()                                     \
                    == LocalizationHelper.get_string_translation(net, media_type_id_str, locale),           \
                        f"Expected {LocalizationHelper.get_string_translation(net, media_type_id_str, locale)} loaded, got {spice.mediaapp.recover_input_card_media_type_value()}"
            printer_on_inches = CdmUnitOfMeasure(cdm).get_display_units() == CdmUnitOfMeasure.Units.IMPERIAL
            if printer_on_inches: # we're validating UI in imperial units TODO create another test that does the same but with metric units
                assert spice.mediaapp.recover_input_card_media_width_value() == width_inch_str, \
                        f"Expected {width_inch_str}\" source loaded; got something different: {spice.mediaapp.recover_input_card_media_width_value()}"
            else:
                logging.warning("Printer not on imperial units, skipping inches check...")
        finally:
            # done with the card; close
            try:
                spice.wait_for(MediaAppWorkflowObjectIds.CLOSE_INPUT_CARD).mouse_click()
            except Exception:
                pass

    def click_on_manual_cut_flow_done_button(self, wait_timeout=15):
        self._spice.wait_for(MediaAppWorkflowObjectIds.manual_cut_crop_line_flow_ready_done, timeout = wait_timeout)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.manual_cut_crop_line_flow_ready_done, timeout = wait_timeout)
        done_button.mouse_click()