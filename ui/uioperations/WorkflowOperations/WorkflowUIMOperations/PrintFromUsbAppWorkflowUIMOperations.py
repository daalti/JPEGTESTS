from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowUICommonOperations import PrintFromUsbAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
import logging
import time

class PrintFromUsbAppWorkflowUIMOperations(PrintFromUsbAppWorkflowUICommonOperations):
    def __init__(self, spice):
        """
        PrintFromUsbAppUIMOperations class to initialize print from usb options operations.
        @param spice:
        """
        self.maxtimeout = 120
        self.spice = spice
        self.workflow_common_operations = spice.basic_common_operations
        self.dial_common_operations = spice.basic_common_operations
        self.homemenu = spice.menu_operations

        self.home_screen_view = PrintFromUsbAppWorkflowObjectIds.home_screen_view
        self.options_view = PrintFromUsbAppWorkflowObjectIds.options_view
        self.print_settings_view = PrintFromUsbAppWorkflowObjectIds.print_button_locator
        self.paper_selection_settings_view = PrintFromUsbAppWorkflowObjectIds.option_paperSelection_menu_loctor
        self.select_file_view = PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view
        self.print_usb_no_content_ok_button = PrintFromUsbAppWorkflowObjectIds.print_usb_no_content_ok_button
        self.print_from_usb_button_locator = PrintFromUsbAppWorkflowObjectIds.print_from_usb_button_locator

    def goto_print_app(self):
        """
        Function to navigate to Print app on home screen
        Ui Flow: Any screen -> Home screen -> Print app
        @return:
        """
        self.homemenu.goto_menu(self.spice)
        self.spice.wait_for(MenuAppWorkflowObjectIds.view_menulistLandingpage + " MouseArea")
        scan_app = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_app + " MouseArea")
        scan_app.mouse_click()
        logging.info("At Print from Usb App")

    def goto_print_from_usb(self):
        """
        Purpose: navigate to Print from USB under Print app.
        Ui Flow: Home_Print -> USBPrint_NoFileFound/USBPrint_PrintFromUSBHome
        @return:
        """
        print_usb_app = self.spice.check_item(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
        if print_usb_app != None:
            current_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
            current_button.mouse_click()
        else:
            self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb + " MouseArea")
            current_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb + " MouseArea")
            current_button.mouse_click()

        #self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
        # changes made here because the screen is of ButtonTemplate Model. Right Now there is only 1 options- PrintFromUsb
        # So scrollbar isnt needed. If in future the scollbar needs to be used uncomment the below code

        #self.workflow_common_operations.scroll_position(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, PrintFromUsbAppWorkflowObjectIds.icon_print_from_usb , PrintFromUsbAppWorkflowObjectIds.scrollBar_printFolderPage , PrintFromUsbAppWorkflowObjectIds.printFolderPage_column_name  , PrintFromUsbAppWorkflowObjectIds.printFolderPage_Content_Item)
        #current_button = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.print_from_usb + " MouseArea")
        #current_button.mouse_click()
        # Wait for usb drive screen
        # self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_from_usb_landing, timeout=9.0) #TBD

    def go_back_to_options_from_paper_selection(self):
        time.sleep(1)
        assert self.spice.query_item("#printFromUSB_paperSelectionMenuList #BackButton")["visible"] == True
        self.spice.query_item("#printFromUSB_paperSelectionMenuList #BackButton").mouse_click()
        assert self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_optionView, timeout = 9.0)

    def find_print_file_or_folder_by_name(self, file_name: str):
        """
        find expect file shows in folder list view screen.
        @param:file_name:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view)
        listView = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.view_print_usb_folder_grid_view)
        try:
            targetItem = self.spice.wait_for(f"#{file_name}", timeout=0.2)
            isVisible = self.validateListObjectVisibility(listView, targetItem)
            if isVisible:
                return
        except:
            logging.info("search failed: try to scroll")

        time.sleep(3)
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view_verticalscroll)
        scrollbarSize = scrollbar['size']
        scrollPosition = 0
        scrollbar["position"] = scrollPosition
        #scroll down to find files

        while scrollPosition + 0.5 * scrollbarSize < 1:
            try:
                targetItem = self.spice.wait_for(f"#{file_name}", timeout=0.2)
                isVisible = self.validateListObjectVisibility(listView, targetItem)
                if isVisible:
                    return
                logging.info("expected file is not in screen")
            except:
                logging.info("search failed: try to scroll")
            scrollPosition = scrollPosition + 0.5 * scrollbarSize
            scrollbar["position"] = scrollPosition
        assert self.spice.wait_for(f"#{file_name}", timeout=20), "search failed"
    
    def select_print_file_or_folder_by_name(self, name: str, dial_value: int = 180):
        """
        UI should be in USBPrint_PrintFromUSBHome.
        This function cannot be used for localization file name
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view  + " MouseArea", timeout = 60.0)
        logging.info("Wait_For  print_usb_folder_list_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view + " MouseArea")

        logging.info("Wait_For name")
        self.spice.wait_for("#"+name, timeout = 20.0)

        #move scrollbar to postion 0
        scrollbar = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view_verticalscroll)
        scrollbar.__setitem__("position", "0")

        rowObjectY = self.spice.query_item(f"#{name}")["y"]
        if (rowObjectY != 0):
            assert self.spice.query_item( PrintFromUsbAppWorkflowObjectIds.view_print_usb_folder_grid_view)["contentHeight"] != 0
            contentHeight = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.view_print_usb_folder_grid_view)["contentHeight"]
            stepValue = rowObjectY / contentHeight
            self.workflow_common_operations.scroll_to_position_vertical(stepValue, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view_verticalscroll)

        logging.info("goto_item_navigation")
        self.spice.query_item(f"#{name}").mouse_click()    

    def get_sorted_file_name_list(self, expect_all_file_list):
        """
        Get file name list sorted by y coordinate from Gammaray tool, from Gammaray tool we can know that the file will ordered by its attribute Y
        @param:expect_all_file_list:
        @return:file_name_list
        """
        wait_pages = self.spice.wait_for(f"#{expect_all_file_list[0]}",timeout = 20)
        self.spice.wait_until(lambda: wait_pages["visible"] is True, 60)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view,timeout = 20)
        logging.info("wait for sorted files load completed")
        time.sleep(3)
        file_name_to_list = []
        for file_name in expect_all_file_list:
            self.spice.wait_for(f"#{file_name}")
            x_coordinate = self.spice.query_item(f"#{file_name}")["x"]
            y_coordinate = self.spice.query_item(f"#{file_name}")["y"]
            file_name_to_list.append({
                "file_name": file_name,
                "x_coordinate": x_coordinate,
                "y_coordinate": y_coordinate
            })

        logging.info(f"sorted list by y coordinate")
        file_name_to_list.sort(key = lambda item: (item["y_coordinate"],item["x_coordinate"]))
        logging.info("get file name list sorted by y coordinate")
        file_name_list = [i["file_name"] for i in file_name_to_list]
        logging.info(f"file name list after sorted by y coordinate is <{file_name_list}>")
        return file_name_list

    def check_file_names_in_folder_list_view(self, expected_file_list):
        """
        Check expect files shows in folder list view screen.
        @param:expected_file_list:
        @return:
        """
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view)
        for file_name in expected_file_list:
            self.spice.wait_for(f"#{file_name}",timeout = 20)
        logging.info(f"Check file name list {expected_file_list} success")

    def check_search_result_number_in_folder_list_view(self, expected_file_list):
        """
        Check Search Result numbers shows in folder list view screen.
        @param:expected_file_list:
        @return:
        """
        time.sleep(3)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view)
        result_message = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.search_result_message_locator)["text"]
        result_number = result_message.split("+")[0]
        assert len(expected_file_list) == int(result_number), "Search result numbers is error"

    def select_print_file_or_folder_by_property_text(self, file_name, timeout_val=300):
        """
        Select print file or folder by property text
        @param name:
        @return:
        """
        logging.info("Wait_For print_usb_folder_landing_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_landing_view)
        logging.info("Wait_For  print_usb_folder_grid_view")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_usb_folder_grid_view)
        logging.info("goto_item print_usb_folder_grid_view")
        # This is a workaround for only test_printfromusb_ui_filename_special_characters (hello@#$%^&world)
        time.sleep(5)
        count = self.get_index_from_file_name(file_name)
        current_button = self.spice.query_item("#printUsbFolderLandingView SpiceText[visible=true]", count)
        current_button.mouse_click()

    def check_spec_on_usb_print_options(self, net, two_sided=None,color=None, quality=None, paper_selection=None, collate=None):
        """
        Check spec on USBPrint_Options
        @param net:
        @param two_sided:str -> on/off
        @param color:str
        @param quality:str
        @param paper_seleection:dict
        @param collate:str -> on/off
        @return:
        """
        # paper_selection optional parameters
        paper_selection_key_list = ["paper_size", "paper_type", "paper_tray"]
        logging.info("check static spec(Options, 2-Sided, Color, Quality, Paper Selection) on usb print options page")

        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view + " MouseArea")

        if(two_sided):
            logging.info("check 2sided options spec")
            assert ("on" if self.get_copy_2sided_options_status() else "off") == two_sided
        if(collate):
            logging.info("check collate status spec")
            assert ("on" if self.get_collate_options_status() else "off") == collate
        if(color):
            logging.info("check color options spec")
            assert self.get_color_options() == color
        if(quality):
            logging.info("check quality otpions spec")
            assert self.get_quality_options() == quality
        if(paper_selection):
            paper_selection_options_list = self.get_paper_selection_options().split(", ")
            actual_paper_selection_dict = dict(zip(paper_selection_key_list,paper_selection_options_list))

            for key, val in paper_selection.items():
                logging.info(f"check paper selection option: {key}")
                assert actual_paper_selection_dict[key.lower()] == val

    def set_collate_options(self, collate_options="off"):
        """
        Set collate option
        @param collate_options:str -> on/off
        @return:
        """
        logging.info(f"Set Collate_options to {collate_options}")
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.options_view)

        menu_item_id = [PrintFromUsbAppWorkflowObjectIds.options_collate_setting_switch, PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch ]
        self.workflow_common_operations.goto_item(menu_item_id, PrintFromUsbAppWorkflowObjectIds.view_optionView, scrollbar_objectname = PrintFromUsbAppWorkflowObjectIds.options_view_scrollbar )
        collate_options_checked = self.get_collate_options_status()

        active_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.options_collate_menu_switch)

        if collate_options == "off" and collate_options_checked:
            logging.info("need to turn off collate option")
            self.spice.common_operations.click_button_on_middle(active_item)
            time.sleep(1)

        if collate_options == "on" and not collate_options_checked:
            logging.info("need to turn on collate option")
            self.spice.common_operations.click_button_on_middle(active_item)
            time.sleep(1)

        if collate_options == "off":
            assert not self.get_collate_options_status(), f"Failed to set collate to {collate_options}"
        else:
            assert self.get_collate_options_status(), f"Failed to set collate to {collate_options}"

    def select_print_file_by_name(self, file_name):
        """
        Select print file. UI should be in USBPrint_PrintFromUSBHome.
        @param file_name:
        @return:
        """
        print_app = self.spice.wait_for("#" + file_name)
        print_app.mouse_click()

    def start_print_from_usb(self):
        """
        UI should be in USBPrint_PrintFromUSB.
        UI Flow is click on print button
        @return:
        """
        print_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.print_button_locator)
        print_button.mouse_click()

    def set_color_options(self, net, color_options="color", locale: str = "en-US"):
        """
        Set the color option
        @param net:
        @param color_options: str -> color/auto/grayscale
        @param locale:
        @return:
        """
        option_view = PrintFromUsbAppWorkflowObjectIds.options_view
        select_item = PrintFromUsbAppWorkflowObjectIds.option_color_button_locator
        color_item = self.spice.query_item(option_view + " " + select_item)
        color_item.mouse_click()
        time.sleep(1)

        if color_options == "color":
            gray_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_color_set_color)
            gray_item.mouse_click()
            time.sleep(1)

        if color_options == "grayscale":
            gray_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_color_set_grayscale)
            gray_item.mouse_click()
            time.sleep(1)

        if color_options == "auto":
            comboBoxscrollBar = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.standard_sizes_scrollbar)
            scrollbarSize = comboBoxscrollBar["size"]
            comboBoxscrollBar["position"] = 1-scrollbarSize
            gray_item = self.spice.query_item(PrintFromUsbAppWorkflowObjectIds.option_color_set_auto)
            gray_item.mouse_click()
            time.sleep(1)

    def wait_for_preview_layout(self):
        """
        wait until preview layout displayed
        @param name:
        @return:
        """
        logging.info("Wait_For preview_layout")
        self.spice.wait_for("#SpiceView " + PrintFromUsbAppWorkflowObjectIds.preview_screen_progress, timeout = 20.0)
        time.sleep(5)
        self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.preview_screen_for_large, timeout = 40.0)
        logging.info("Wait_For preview_layout success")