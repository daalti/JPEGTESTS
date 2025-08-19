
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflow2UICommonOperations import MenuAppWorkflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.Workflow2UICommonOperations import Workflow2UICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXSOperations.MenuAppWorkflowXSObjectIds import MenuAppWorkflowXSObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations

class MenuAppWorkflow2UIXSOperations(MenuAppWorkflow2UICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.workflow_common_operations = Workflow2UICommonOperations(spice)
        self.MenuAppWorkflowUIXSObjectIds = MenuAppWorkflowObjectIds()
    
    def goto_menu(self, spice):
        self.homeApp_workflow2_common_operations.goto_home_menu()
        print("At Menu App")

    def goto_menu_settings_printerUpdate_autoUpdateOptions_iris_radio(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.9, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        assert spice.wait_for(MenuAppWorkflowObjectIds.view_printerUpdate_iris_radioButtonsView)
        logging.info("At Printer Update RadioButtons Screen")

    def goto_menu_settings_printerUpdate_autoupdateoptions_iris_options(self, spice):
        self.goto_menu_settings_printerUpdate_autoUpdateOptions(spice)
        self.workflow_common_operations.scroll_to_position_vertical(0.9, MenuAppWorkflowObjectIds.scrollbar_printer_update_iris)
        nextButton = spice.wait_for(MenuAppWorkflowObjectIds.menu_button_settings_printerUpdate_autoupdateoptions_next)
        nextButton.mouse_click()
        logging.info("At Printer Allow Upgrade Screen")

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(self, spice, udw):
        self.goto_menu_tools_servicemenu_systemconfiguration(spice, udw)
        coldResetPaperComboboxList = "#SettingsSpiceComboBoxpopupList"
        coldResetPaperComboboxOption = "#SettingsSpiceComboBox"
        self.workflow_common_operations.scroll_to_position_vertical(0.9,scrollbar_objectname = MenuAppWorkflowObjectIds.scrollbar_tools_system_configuration)
        selectOption = spice.wait_for(coldResetPaperComboboxOption)
        selectOption.mouse_click()
        spice.wait_for(coldResetPaperComboboxList)
        logging.info("option end")

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaper(self, spice, udw):
        coldResetMediaSize_option_A4 = "#coldResetMediaComboA4"
        coldResetMediaSize_option_Letter = "#coldResetMediaComboLetter"   

        self.goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(spice, udw)
        logging.info("At Cold Reset Paper Screen")

        #select opposite media size
        if spice.query_item(coldResetMediaSize_option_Letter)["selected"] is True:
            coldResetMediaSize_original_option = coldResetMediaSize_option_Letter
            current_button = spice.query_item(coldResetMediaSize_option_A4)
            logging.info("Original is Letter and A4 selected and reboot now")
        else:
            coldResetMediaSize_original_option = coldResetMediaSize_option_A4
            current_button = spice.query_item(coldResetMediaSize_option_Letter)
            logging.info("Original is A4 and Letter selected and reboot now")
        assert current_button
        current_button.mouse_click()

        #Wait for homescreen view after 1st reboot
        time.sleep(120)
        self.goto_menu_tools_servicemenu_systemconfiguration_coldresetpaperr_option(spice, udw)

        #Check the cold reset paper is changed.
        if spice.query_item(coldResetMediaSize_option_A4)["selected"] is True:
            if(coldResetMediaSize_original_option == coldResetMediaSize_option_A4):
                logging.info("Check: A4 selected : Fail revert original")
            current_button = spice.query_item(coldResetMediaSize_option_Letter)
        else:
            if(coldResetMediaSize_original_option == coldResetMediaSize_option_Letter):
                logging.info("Check: Letter selected : Fail revert original")
            current_button = spice.query_item(coldResetMediaSize_option_A4)
        assert current_button
        current_button.mouse_click()

        #Wait for homescreen view after 2nd reboot for next test
        time.sleep(120)

        logging.info("Cold Reset Paper test ends.")

    def goto_menu_tools_servicemenu_servicetests_displaytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        selectOption = spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_displaytest)
        selectOption.mouse_click()

    def goto_menu_tools_servicemenu_servicetests_keytest(self, spice, udw):
        self.goto_menu_tools_servicemenu_servicetests(spice, udw)
        selectOption = spice.wait_for(MenuAppWorkflowXSObjectIds.menu_button_service_servicetests_keytest)
        selectOption.mouse_click()

    def goto_menu_settings_print(self, spice):
        self.goto_menu_settings(spice)
        self.workflow_common_operations.goto_item("#printSettingsSettingsTextImage", "#settingsMenuListListViewlist1", 0, True, 0.1, "#settingsMenuListListViewlist1ScrollBar")

    def goto_menu_settings_print_printquality(self, spice):
        self.goto_menu_settings_print(spice)
        self.workflow_common_operations.goto_item("#printQualitySettingsTextImage", "#printSettingsMenuList", 0, True, 0.1, "#printSettingsMenuListScrollBar")
        logging.info("At Print Quality Screen")

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        self.goto_menu_tools_servicemenu_faxdiagnosticsmenu(spice, udw)
        assert spice.wait_for("#faxDiagnosticMenuMenuList")
        time.sleep(1)
        # currentElement = spice.wait_for("#generateRandomDataTextImage")
        currentElement = spice.wait_for("#randomDataSettingsTextImage")
        time.sleep(1)
        currentElement.mouse_click()
        time.sleep(2)
        assert spice.wait_for("#generateRandomDataView")
        time.sleep(1)
        logging.info("At Fax Diagnostic Generate Randaom Data Screen")

    def reduce_scrollbar_position_event_filter(self, spice, scrollbar_id, size):
            """
            Reduces the scrollbar position by a given size
            """
            scroll_bar = spice.wait_for(scrollbar_id)
            scrollbar_size = scroll_bar["visualSize"]
            scroll_bar.__setitem__("position", scrollbar_size - size)
            return True