import logging 
import time

from dunetuf.ui.uioperations.BaseOperations.IPrintAppUIOperations import IPintAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintAppWorkflowObjectIds import PrintAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds

class PrintAppWorkflowUICommonOperations(IPintAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations

    def set_print_quality_settings_cleaning_page_autocalibration(self, spice, cleaning_pages_settings):
        """
        Set the number of cleaning pages   
        """
        spice.wait_for(PrintAppWorkflowObjectIds.cleaning_pages_combobox_screen, timeout=15)
        self.workflow_common_operations.goto_item(cleaning_pages_settings,
            PrintAppWorkflowObjectIds.cleaning_pages_combobox_screen,
            scrollbar_objectname = PrintAppWorkflowObjectIds.cleaning_pages_combobox_scroll_bar)
        cleaning_pages = spice.wait_for(MenuAppWorkflowObjectIds.cleaningPage_combobox, timeout=15)

    def goto_clean_smear(self, spice):
        """
        Go to clean smear screen
        """
        spice.wait_for(PrintAppWorkflowObjectIds.clean_smear, timeout=30)
        spice.wait_for(PrintAppWorkflowObjectIds.clean_smear).mouse_click()
        assert spice.wait_for(PrintAppWorkflowObjectIds.view_clean_smear, timeout=30)

    def goto_pen_align_auto(self, spice):
        """
        Go to pen align auto screen
        """
        spice.wait_for(MenuAppWorkflowObjectIds.ph_alignement, timeout=30)
        spice.wait_for(MenuAppWorkflowObjectIds.ph_alignement).mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button, timeout=30)

    def goto_line_feed_calibration(self, spice):
        """
        Go to line feed calibration screen
        """
        current_button = spice.wait_for(MenuAppWorkflowObjectIds.paper_advance_calibration_button, timeout = 30)
        current_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.calibration_start_button, timeout = 30)

    def goto_quality_and_speed(self, spice):
        """
        Select the quality and speed combo box on default print options
        """
        view_defaultprintoptions = spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=10)
        spice.wait_until(lambda:view_defaultprintoptions["visible"])
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=10)
        self.workflow_common_operations.goto_item([MenuAppWorkflowObjectIds.print_default_options_quality_screen, PrintAppWorkflowObjectIds.quality_speed_settings],
        MenuAppWorkflowObjectIds.view_defaultprintoptions, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_print_default_print_options)
        combo_box_view = spice.wait_for(PrintAppWorkflowObjectIds.view_quality_combobox)
        spice.wait_until(lambda:combo_box_view["visible"])

    def set_quality_and_speed_settings(self, spice, setting_value):
        """
        Set the quality and speed settings on default print options
        Setting_value:Draft/Normal/Best
        """
        setting_id = ""
        if (setting_value == "draft"):
            setting_id = PrintAppWorkflowObjectIds.quality_speed_dict['draft']
        elif (setting_value == "normal"):
            setting_id = PrintAppWorkflowObjectIds.quality_speed_dict['normal']
        elif (setting_value == "best"):
            setting_id = PrintAppWorkflowObjectIds.quality_speed_dict['best']
        else:
            assert False, "Setting not existing"
        #Click on the setting value
        quality_speed_settings_button = spice.wait_for(setting_id, timeout=20)
        quality_speed_settings_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=20)

    def set_sides_settings_on_default_print_options(self, spice, setting_value):
        """
        Set the sides settings on default print options
        Setting_value:1-sided/2-sided
        """
        setting_id = ""
        if (setting_value.lower() == "1-sided"):
            setting_id = PrintAppWorkflowObjectIds.sides_dict['1-sided']
        elif (setting_value.lower() == "2-sided"):
            setting_id = PrintAppWorkflowObjectIds.sides_dict['2-sided']
        else:
            assert False, "Setting not existing"
        #Click on the setting value
        sides_settings_button = spice.wait_for(setting_id, timeout=20)
        sides_settings_button.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=20)

    def goto_defaultprintoptions_sides(self, spice):
        """
        Select the sides combo box on default print options
        """
        view_defaultprintoptions = spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=10)
        spice.wait_until(lambda:view_defaultprintoptions["visible"])
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_defaultprintoptions, timeout=10)
        self.workflow_common_operations.goto_item([PrintAppWorkflowObjectIds.row_object_sides, MenuAppWorkflowObjectIds.menu_button_settings_print_defaultprintoptions_sides],
        MenuAppWorkflowObjectIds.view_defaultprintoptions, scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_print_default_print_options)
        combo_box_view = spice.wait_for(PrintAppWorkflowObjectIds.view_combo_box_sides)
        spice.wait_until(lambda:combo_box_view["visible"])

    def goto_color_calibration(self, spice):
        """
        Navigate to the Color Calibration screen in the print Quality
        """
        #scroll and click on Color Calibration
        self.workflow_common_operations.goto_item(MenuAppWorkflowObjectIds.menu_button_troubleshooting_color_calibration,PrintAppWorkflowObjectIds.view_printquality_screen,
            scrollbar_objectname=MenuAppWorkflowObjectIds.scrollbar_tools_troubleshooting_printquality)
        
    

        

    
    
