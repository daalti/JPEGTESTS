from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowUICommonOperations import ScanAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from enum import Enum
import logging
import time


class ScanAppWorkflowUIXLOperations(ScanAppWorkflowUICommonOperations):
    class CropSizeValues(Enum):
        DO_NOT_CROP = "doNotCrop"
        CUSTOM = "custom"

    class CropOrientationValues(Enum):
        LANDSCAPE = "landscape"
        PORTRAIT = "portrait"

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.homemenu = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations
        self.scan_operations = ScanAppWorkflowUICommonOperations(self.spice)


    def wait_for_preview_n(self, preview_index, timeout=10):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_index = preview_index-1 #[0..n]

        thumbnail_objectname = ScanAppWorkflowObjectIds.preview_image_without_index + str(preview_index) # "#image_0" 
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout)
        self.spice.wait_for(thumbnail_objectname, timeout)
        time.sleep(2) # Wait needed so that preview image object is fully loaded and clickable, not enought with just the previous wait_for

    def click_on_edit_button(self):
        '''
        Ui Should be in previewpanel
        Click on edit button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_button, timeout=15)
        time.sleep(5)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_button)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        time.sleep(10)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)
    
    def click_on_brightness_button(self):
        '''
        Ui Should be in preview edit panel
        Click on brightness button
        '''
        time.sleep(10)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_button, timeout=15)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_brightness_button)
        current_button.mouse_click()
        time.sleep(15)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_screen, timeout=15)

    def click_on_contrast_button(self):
        '''
        Ui Should be in preview edit panel
        Click on contrast button
        '''
        time.sleep(10)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_contrast_button, timeout=15)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_contrast_button)
        current_button.mouse_click()
        time.sleep(15)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_contrast_screen, timeout=15)

    def click_on_crop_button(self):
        '''
        Ui Should be in preview edit panel
        Click on crop button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_crop_button)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    
    def click_on_brightness_slider(self, brightness_value):
        '''
        Ui Should be in brightness panel
        Click on brightness slider
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_slider, timeout=15)
        current_element = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_brightness_slider)
        current_element.__setitem__('value', brightness_value)
        time.sleep(15)

    def click_on_contrast_slider(self, contrast_value):
        '''
        Ui Should be in contrast panel
        Click on contrast slider
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_contrast_slider, timeout=15)
        current_element = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_contrast_slider)
        current_element.__setitem__('value', contrast_value)
        time.sleep(15)

    def click_on_edit_operation_done_button(self):
        '''
        Ui Should be in brightness or contrast panel
        Click on brightness or contrast done button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_operation_done_button, timeout=15)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_operation_done_button)
        self.spice.wait_until_constrained(current_button, False)
        current_button.mouse_click()
        time.sleep(10)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)
    
    def click_on_edit_operation_cancel_button(self):
        '''
        Ui Should be in brightness or contrast panel
        Click on brightness or contrast cancel button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preivew_edit_operation_cancel_button, timeout=15)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preivew_edit_operation_cancel_button)
        current_button.mouse_click()
        time.sleep(10)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)

    def click_edit_operation_reset_button(self):
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_operation_reset_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_operation_reset_button)
        current_button.mouse_click()
        time.sleep(1)

    def click_on_edit_done_button(self):
        '''
        Ui Should be in preview edit panel
        Click on edit done button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen, timeout=15)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_done_button, timeout=15)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_done_button)
        self.spice.validate_button(current_button)
        self.spice.wait_until_constrained(current_button, False)
        current_button.mouse_click()
        time.sleep(10)
    
    def click_on_edit_cancel_button(self):
        '''
        Ui Should be in preview edit panel
        Click on edit cancel button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_screen)
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_cancel_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_cancel_button)
        self.spice.validate_button(current_button)
        self.spice.wait_until_constrained(current_button, False)
        current_button.mouse_click()
        time.sleep(5)
    
    def perform_brightness_edit(self, brightness_value):
        '''
        Ui Should be in previewpanel
        Perform brightness edit
        '''
        self.click_on_edit_button()
        self.click_on_brightness_button()
        self.click_on_brightness_slider(brightness_value)
        self.click_on_edit_operation_done_button()
        self.click_on_edit_done_button()

    def perform_contrast_edit(self, contrast_value):
        '''
        Ui Should be in previewpanel
        Perform contrast edit
        '''
        self.click_on_edit_button()
        self.click_on_contrast_button()
        self.click_on_contrast_slider(contrast_value)
        self.click_on_edit_operation_done_button()
        self.click_on_edit_done_button()

    def goto_crop_view_from_edit_scren(self):
        '''
        Ui Should be in edit screen.
        Go to crop edit view.
        '''
        # Wait until the buttons to navigate are not constrained.
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_cancel_button)
        self.spice.validate_button(current_button)
        self.spice.wait_until_constrained(current_button, False)
        self.click_on_crop_button()

    def goto_crop_view(self):
        '''
        Ui Should be in previewpanel
        Go to crop edit view.
        '''
        self.click_on_edit_button()
        self.goto_crop_view_from_edit_scren()

    def goto_landing_from_crop_view(self):
        '''
        Ui Should be in crop view.
        Go back to copy landing.
        '''
        self.click_on_edit_operation_done_button()
        self.click_on_edit_done_button()

    def wait_and_click_preview_n(self, preview_index ):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_index = preview_index-1 #[0..n]

        thumbnail_objectname = ScanAppWorkflowObjectIds.preview_image_without_index + str(preview_index) # "#image_0" 
        assert self.spice.wait_for(ScanAppWorkflowObjectIds.fitpage_layout, timeout =9.0)
        thubmnail_object = self.spice.wait_for(thumbnail_objectname + " MouseArea", timeout =9.0)
        thubmnail_object.mouse_click()

    def wait_for_preview_window(self):
        '''
        Ui Should be in previewpanel
        Verify preview is shown
        '''
        preview_window_objectname = ScanAppWorkflowObjectIds.previewWindow
        assert self.spice.wait_for(preview_window_objectname, timeout =9.0)

    def back_from_preview(self):
        '''
        Ui Should be in previewpanel
        Press back button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.preview_back_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.preview_back_button)
        current_button.mouse_click()

    def mdf_add_page_alert_done(self):
        """
        XL does not have an alert. We wait to finish the page.
        to send the scan job.
        :return: None
        """
        logging.info("XL does not have alert page")

    def goto_usb_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to USB.
        """
        #self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        self.workflow_common_operations.scroll_position(ScanAppWorkflowObjectIds.view_scan_app_landing, ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan, ScanAppWorkflowObjectIds.scroll_bar_scan_app_home , ScanAppWorkflowObjectIds.scan_app_home_column_name , ScanAppWorkflowObjectIds.scan_app_home_landingPage_Content_Item)
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_to_usb_from_home_scan +" MouseArea")
        button.mouse_click()
        logging.info("At Scan to USB screen")

    def goto_folder_from_scanapp_at_home_screen(self):
        """
        UI should be on Scan app screen from home.
        UI Flow is Scan app -> Scan to Network Folder.
        """
        self.spice.wait_for(ScanAppWorkflowObjectIds.view_scan_app_landing)
        folder_button = self.spice.wait_for(ScanAppWorkflowObjectIds.scan_network_folder_from_home_scan + " MouseArea")
        self.workflow_common_operations.click_button_on_middle(folder_button)
        logging.info("At scan to folder screen")

    def get_brightness_slider_value(self):
            '''
            Ui Should be in brightness panel
            Get brightness slider value
            '''
            self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_brightness_slider)
            current_element = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_brightness_slider)
            return current_element.__getitem__('value')

    def get_contrast_slider_value(self):
            '''
            Ui Should be in contrast panel
            Get contrast slider value
            '''
            self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_contrast_slider)
            current_element = self.spice.query_item(ScanAppWorkflowObjectIds.preview_edit_contrast_slider)
            return current_element.__getitem__('value')


    # ---- Crop Edit Operations ----
    def wait_crop_available(self):
        button = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_operation_done_button)
        self.spice.validate_button(button)
        self.spice.wait_until_constrained(button, False)
        # We need to wait a bit so that all signals finish processing after the preview is loaded.
        # and the models and ui are all conherent.
        time.sleep(1)

    def get_crop_spinbox_width(self):
        width_spinbox_model = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_width_spinbox)
        self.spice.validate_button(width_spinbox_model)
        return int(width_spinbox_model["value"])

    def get_crop_spinbox_height(self):
        height_spinbox_model = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_height_spinbox)
        self.spice.validate_button(height_spinbox_model)
        return int(height_spinbox_model["value"])

    def get_crop_ratio(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
        return crop_object["cropAspectRatio"]

    def get_crop_checkbox_proportions(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_proportion_checkbox)
        self.spice.validate_button(crop_object)
        return crop_object["checked"]

    def get_crop_width_height(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
        return (crop_object["cropInputValueWidth"], crop_object["cropInputValueHeight"])

    def get_crop_topleft_corner_position(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_grid_crop)
        return (crop_object['x'], crop_object['y'])

    def get_crop_bottomright_corner_position(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_br_handler)
        return (crop_object['x'], crop_object['y'])

    def get_crop_center_marker_position(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_center_marker)
        return (crop_object['x'], crop_object['y'])

    def get_crop_combobox_size_value(self):
        crop_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_size_combobox_row)
        self.spice.validate_button(crop_cb)
        if crop_cb['currentIndex'] == 0:
            return self.CropSizeValues.DO_NOT_CROP
        else:
            return self.CropSizeValues.CUSTOM

    def get_crop_combobox_orientation_value(self):
        crop_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_orientation_combobox_row)
        self.spice.validate_button(crop_cb)
        if crop_cb['currentIndex'] == 0:
            return self.CropOrientationValues.LANDSCAPE
        else:
            return self.CropOrientationValues.PORTRAIT
        
    def set_crop_spinbox_width(self, value):
        width_spinbox_model = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_width_spinbox)
        self.spice.wait_until_constrained(width_spinbox_model, False)
        width_spinbox_model["value"] = int(value)

    def set_crop_spinbox_height(self, value):
        height_spinbox_model = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_height_spinbox)
        self.spice.wait_until_constrained(height_spinbox_model, False)
        height_spinbox_model["value"] = int(value)

    def toggle_crop_checkbox_proportions(self):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_proportion_checkbox)
        self.spice.wait_until_constrained(crop_object, False)
        crop_object.mouse_click()

    def set_crop_gridcrop_topleft_corner_position(self, value):
        crop_object = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_grid_crop)
        crop_object["x"] = int(value[0])
        crop_object["y"] = int(value[1])

    def select_crop_combobox_size_value(self, value):
        crop_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_size_combobox)
        self.spice.wait_until_constrained(crop_cb, False)
        crop_cb.mouse_click()
        if value == self.CropSizeValues.CUSTOM:
            crop_custom = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_size_custom)
            crop_custom.mouse_click()
        elif value == self.CropSizeValues.DO_NOT_CROP:
            crop_not = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_size_doNotCrop)
            crop_not.mouse_click()

    def select_crop_combobox_orientation_value(self, value):
        orient_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_orientation_combobox)
        self.spice.wait_until_constrained(orient_cb, False)
        orient_cb.mouse_click()
        if value == self.CropOrientationValues.LANDSCAPE:
            land_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_orientation_landscape)
            land_cb.mouse_click()
        elif value == self.CropOrientationValues.PORTRAIT:
            port_cb = self.spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_orientation_portrait)
            port_cb.mouse_click()

    def goto_long_original_settings(self, dial_val: int = 180):
        """
        UI should be on Scan options list screen.
        UI Flow is Long original-> (Long original settings screen).
        """
        logging.debug("UI: In XL, Long Original is visible in screen so not need to go to setting")  

    def perform_dimiss_page(self):
        """
        UI should be on Scan app screen from home.
        Perform a discard of the focused page
        """
        self.click_on_discard_footer_button()
        self.click_on_discard_confirmation_button()

    def click_on_discard_footer_button(self):
        '''
        UI should be on Scan app screen from home.
        Click on discard footer button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.discard_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.discard_button)
        self.spice.validate_button(current_button)
        current_button.mouse_click()
        self.spice.wait_for(ScanAppWorkflowObjectIds.discard_confirmation_screen)

    def click_on_discard_confirmation_button(self):
        '''
        UI should be on Discard page confirmation screen.
        Click on discard button
        '''
        self.spice.wait_for(ScanAppWorkflowObjectIds.discard_confirmation_button)
        current_button = self.spice.query_item(ScanAppWorkflowObjectIds.discard_confirmation_button)
        self.spice.validate_button(current_button)
        current_button.mouse_click()