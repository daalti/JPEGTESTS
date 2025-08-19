import time
import logging
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowUICommonOperations import MediaAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds


class MediaAppWorkflowUIXLOperations(MediaAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def click_on_load_button(self):
        load_button = self._spice.wait_for(MediaAppWorkflowObjectIds.LOAD_BUTTON_INPUT_CARD)
        load_button.mouse_click()
        self._spice.wait_for(MediaAppWorkflowObjectIds.load_roll_wait_drawer_open)

    def click_on_unload_button(self):
        unload_button = self._spice.wait_for(MediaAppWorkflowObjectIds.UNLOAD_BUTTON_INPUT_CARD)
        unload_button.mouse_click()

    def click_on_jam_how_to_fix_button(self):
        how_to_fix = self._spice.wait_for(MediaAppWorkflowObjectIds.JAM_HOW_TO_FIX_BUTTON)
        how_to_fix.mouse_click()

    def click_on_modify_button(self):
        modify_button = self._spice.wait_for(MediaAppWorkflowObjectIds.MODIFY_BUTTON)
        modify_button.mouse_click()

    def click_on_modify_media_type_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration, timeout = 30)
        type_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.TYPE_SETTINGS, timeout = 15)
        type_selector.mouse_click()

    def click_on_modify_load_done_button(self):
        self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration, timeout = 15)
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.roll_and_sheet_load_configuration_done, timeout = 15)
        done_button.mouse_click()

    def click_on_done_button(self):
        done_button = self._spice.wait_for(MediaAppWorkflowObjectIds.DONE_BUTTON)
        done_button.mouse_click()

    def click_on_batch_load_details_input_card_content(self): 
        input_card = self._spice.wait_for(MediaAppWorkflowObjectIds.BATCH_LOAD_DETAILS_INPUT_CARD_CONTENT)
        input_card.mouse_click()

    def click_on_media_length_option(self):
        type_selector = self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_SETTINGS, timeout = 15)
        type_selector.mouse_click()

    def click_on_media_length_radio_button(self, media_type_number):
        length_button = self._spice.wait_for(MediaAppWorkflowObjectIds.LENGTH_RADIO_BUTTON.format(media_type_number), timeout = 10)
        length_button.mouse_click()

    def click_on_media_input_card(self, roll):
        input_card = self._spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_INPUT_CARD, timeout = 15, query_index = roll)
        middle_width = input_card["width"] / 2
        middle_height = input_card["height"] / 2
        input_card.mouse_click(middle_width, middle_height)

    def click_on_close_media_input_card(self):
        close_input_card = self._spice.wait_for(MediaAppWorkflowObjectIds.CLOSE_INPUT_CARD)
        close_input_card.mouse_click()

    def click_on_media_load_cancel_button(self): 
        cancel_button = self._spice.wait_for(MediaAppWorkflowObjectIds.CANCEL_MEDIA_LOAD_BUTTON, timeout = 10)
        cancel_button.mouse_click()

    def click_on_media_load_cancel_msg_no_button(self): 
        no_action = self._spice.wait_for(MediaAppWorkflowObjectIds.CANCEL_MEDIA_LOAD_NO_BUTTON, timeout = 10)
        no_action.mouse_click()

    def click_on_media_load_cancel_msg_yes_button(self): 
        yes_action = self._spice.wait_for(MediaAppWorkflowObjectIds.CANCEL_MEDIA_LOAD_YES_BUTTON, timeout = 10)
        yes_action.mouse_click()

    def select_roll_card_in_load_media_from_mismatch_out_of_media_alert(self):
        # Select roll 1
        self._spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_GRID_TAB_LAYOUT)
        roll_1_card = self._spice.wait_for(MediaAppWorkflowObjectIds.ROLL_CARD)
        roll_1_card.mouse_click()

        # Click continue button
        continue_button = self._spice.wait_for(MediaAppWorkflowObjectIds.MEDIA_GRID_CONTINUE_BUTTON)
        continue_button.mouse_click()

    def click_on_specific_media_type(self, media_name):
        start_time = time.time()
        time_spent_waiting = time.time() - start_time
        max_timeout = 120
        found = False
        count = 0
        
        while found == False and (time_spent_waiting < max_timeout):   
            try:
                media_text = self._spice.query_item(MediaAppWorkflowObjectIds.TYPE_RADIO_BUTTON.format(count) + " SpiceText[visible=true]")
                if media_text["text"] != media_name:
                    count = count + 1
                    continue
                media_text.mouse_click()
                found = True
            except:
                count = count + 1
                time_spent_waiting = time.time() - start_time
