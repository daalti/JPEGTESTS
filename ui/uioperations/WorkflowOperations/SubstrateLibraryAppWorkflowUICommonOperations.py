import logging
import time

from dunetuf.ui.uioperations.BaseOperations.ISubstrateLibraryAppUIOperations import ISubstrateLibraryAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryWorkflowObjectIds import SubstrateLibraryWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.cdm.CdmEndpoints import CdmEndpoints

class SubstrateLibraryAppWorkflowUICommonOperations(ISubstrateLibraryAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
        self.MenuAppWorkflowObjectIds = MenuAppWorkflowObjectIds()
        self.workflow_common_operations = spice.basic_common_operations

    def goto_substrate_library_app(self, spice):
        '''
        Expected view: Home Screen
        '''

        try:
            # Wait for HomeScreen to appear and dismiss SystemError if exists
            spice.cleanSystemEventAndWaitHomeScreen()
        except:
            #do nothing
            pass

        if self._spice.uisize in ["XS", "S"]:
            # go to menu
            self.click_button(SubstrateLibraryWorkflowObjectIds.button_menu_on_homescreen)
            time.sleep(1)

            # move the scrollbar firstly.
            self.workflow_common_operations.scroll_to_position_vertical(.2, SubstrateLibraryWorkflowObjectIds.scrollbar_main_menu)
            time.sleep(1)

            # enter the substrate library app
            logging.info("Entering Substrate Library")
            self.click_button(SubstrateLibraryWorkflowObjectIds.button_substratelibrary_app)

            assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrateLibrary)
            time.sleep(1)
            logging.info("At Substrate Library Screen")

        else:            
            # Go to menu
            self._spice.main_app.goto_menu_app()
            time.sleep(1)
    
            # Scroll to substrate library app
            self._spice.homeMenuUI().scroll_position_utilities(SubstrateLibraryWorkflowObjectIds.button_substratelibrary_app)
            time.sleep(1)
            substratelibrary_button = self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.button_substratelibrary_app + " MouseArea")
    
            # enter the substrate library app
            logging.info("Entering Substrate Library")
            substratelibrary_button.mouse_click()
    
            assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrateLibrary)
            time.sleep(1)
            logging.info("At Substrate Library Screen")


    def goto_installed_substrates(self, spice):
        """Navigate to Installed Substrates tab inside Substrate Library"""

        # expected view: SubstrateLibrary view
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrateLibrary)

        # click on installed substrates tab to navigate into it
        tab = spice.wait_for(SubstrateLibraryWorkflowObjectIds.tab_installed_substrates)
        tab.mouse_click()
        time.sleep(1)

        # check we are inside installed substrates view
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates)
        logging.info("At Substrate Library->Installed Substrates screen")

    def goto_packages_printos(self):
        """Navigate to Packages from PrintOS tab inside Substrate Library"""

        # check we are inside substrate library app
        assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrateLibrary)

        # click on gaia packages tab to navigate into it
        tab = self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.tab_gaia_packages)
        tab.mouse_click()
        time.sleep(1)

        # check we are inside gaia packages view
        assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_gaia_packages)
        logging.info("At Substrate Library->Packages from PrintOS screen")

    def goto_add_substrate (self, spice):

        # Click on "Add Substrate"
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_add)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_choose_substrate_name)
        logging.info("At Substrate Library->Create substrate screen")

    def goto_substrate_category(self, spice, categoryButton, category, cdm):
        """
        Clicks on a raw and in result goes to given category view.
        Args:
            spice: ui fixture
            category: category ID, must be of a type STRING
        """

        # expected view: SubstrateLibrary->Installed substrates
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates)

        # Get the amount of categories
        response = cdm.get(CdmEndpoints.CDM_MEDIAPROFILES_CAPABILITIES)
        categories_list = response.get("mediaFamiliesSupported")
        amount_of_categories = len(categories_list)
        scroll_step = 0.5/int(amount_of_categories)

        time.sleep(2)

        categoryPosition = categories_list.index(category)
        scroll_position = scroll_step * categoryPosition
        self.workflow_common_operations.scroll_to_position_vertical(scroll_position, SubstrateLibraryWorkflowObjectIds.scrollbar_installed_substrates_layout_categories)

        self.click_button(categoryButton)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category)
        time.sleep(2)
        logging.info("At Substrate Library->Installed Substrates->Category: " + category)

    def goto_first_category(self, spice):
        """
        Clicks on a row and in result goes to given category view.
        Args:
            spice: ui fixture
        """

        # expected view: SubstrateLibrary->Installed substrates
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates)

        installed_papers_layout = spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates)
        middle_width = installed_papers_layout["width"] / 2
        height = int(installed_papers_layout["height"] / 4)
        installed_papers_layout.mouse_click(middle_width, height)
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category)
        logging.info("At Substrate Library->Installed Substrates->Category->First Category")

    def goto_substrate(self, spice, substrate_id):
        # expected view: SubstrateLibrary->Installed substrates view->Category

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category)

        self.click_button(substrate_id)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrate)
        logging.info("At Substrate screen, substrate ID: " + substrate_id)

    def goto_first_substrate(self, spice):
        """
        Clicks on a first row and in a result goes to given substrate view
        Args:
            spice: ui fixture
        """

        # expected view: SubstrateLibrary->Installed substrates view->Category

        category_layout = spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category)
        middle_width = category_layout["width"] / 2
        height = int(category_layout["height"] / 4)
        category_layout.mouse_click(middle_width, height)
        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrate)
        time.sleep(2)
        logging.info("At Substrate Library->Installed Substrates->Selected Category->First Substrate")

    def navigate_to_installed_substrates(self):
        """Navigate to installed substrates tab inside the substrate library
        Expects to be at home screen before starting the navigation.
        """

        self.goto_substrate_library_app(self._spice)
        self.goto_installed_substrates(self._spice)

    def navigate_to_packages_printos(self):
        """Navigate to packages from PrintOS tab inside the substrate library
        Expects to be at home screen before starting the navigation.
        """

        self.goto_substrate_library_app(self._spice)
        self.goto_packages_printos()

    def add_substrate(self, spice, substrate_name, categoryName, categoryScrollAdvance, substrate_id):

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_choose_substrate_name)
        time.sleep(2)

        # Change name
        text_substrate_name = spice.wait_for(SubstrateLibraryWorkflowObjectIds.add_substrate_text_field)
        text_substrate_name.__setitem__('displayText', substrate_name)
        text_substrate_name.__setitem__('inputText', substrate_name)

        # Click on "next"
        self.click_button(SubstrateLibraryWorkflowObjectIds.add_choose_substrate_name_next_button)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_choose_category)
        time.sleep(2)

        self.workflow_common_operations.scroll_to_position_vertical(categoryScrollAdvance, SubstrateLibraryWorkflowObjectIds.choose_category_sroll_bar)
        categoryBtn = spice.wait_for(categoryName)

        spice.wait_until(lambda: categoryBtn["enabled"] == True)
        spice.wait_until(lambda: categoryBtn["visible"] == True)
        categoryBtn.mouse_click()

        # Click on "next"
        self.click_button(SubstrateLibraryWorkflowObjectIds.add_choose_substrate_category_next_button)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_choose_base_substrate)
        time.sleep(2)

        self.click_button("#"+substrate_id)

        # Click on "next"
        self.click_button(SubstrateLibraryWorkflowObjectIds.add_choose_base_substrate_next_button)

    def clone_substrate(self, spice, new_name):

        # expected view: SubstrateLibrary->Installed substrates view->Category->Substrate

        # Click on "Clone Substrate"
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_clone)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_clone_substrate)
        time.sleep(2)
        logging.info("At Substrate Clone screen")

        # Change name
        text_substrate_name = spice.wait_for(SubstrateLibraryWorkflowObjectIds.txt_clone_insert_name)
        text_substrate_name.__setitem__('displayText', new_name)

        # Click on "OK"
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_clone_ok)

    def clone_substrate_and_navigate_back(self, cdm, category_btn: str, category: str, new_name: str, back_level: int = 0, timeout: int = 120) -> None:
        """Clone the first substrate inside the specified category
        Expects to be at installed substrate tab inside the substrate library
        Args:
            cdm (CDM): CDM object for CDM endpoints rest operations
            category_btn (str): Object name of the category to navigate to
            category (str): Category name to clone its first substrate
            new_name (str): New name for the cloned substrate
            back_level (int, optional): how many levels to navigate back. Defaults to 0.
            timeout (int, optional): time to wait for the clone to finish before returning an error. Defaults to 120.
        """

        # click on category
        self.goto_substrate_category(self._spice, category_btn, category, cdm)

        # click on first substrate
        self.goto_first_substrate(self._spice)

        # clone selected substrate
        self.clone_substrate(self._spice, new_name)

        # wait for substrate to be cloned
        assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_clone_success, timeout)

        # click ok on success button
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_ok)

        # navigate back to substrate library
        if back_level >= 1:
            back_button = self._spice.wait_for(f"{SubstrateLibraryWorkflowObjectIds.view_substrate} {SubstrateLibraryWorkflowObjectIds.button_back}")
            back_button.mouse_click()

            # make sure in category list view
            assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category)

        if back_level >= 2:
            back_button = self._spice.wait_for(f"{SubstrateLibraryWorkflowObjectIds.view_category} {SubstrateLibraryWorkflowObjectIds.button_back}")
            back_button.mouse_click()

            # make sure in installed substrates view
            assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates)

        if back_level >= 3:
            back_button = self._spice.wait_for(f"{SubstrateLibraryWorkflowObjectIds.view_installedSubstrates} {SubstrateLibraryWorkflowObjectIds.button_back}")
            back_button.mouse_click()

            # make sure in substrate library view
            assert self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_substrateLibrary)

    def add_new_media_mode(self, spice, media_mode_name):

        # Change name
        text_substrate_name = spice.wait_for(SubstrateLibraryWorkflowObjectIds.media_mode_text_field)
        text_substrate_name.__setitem__('displayText', media_mode_name )

        # Change ColorMode
        self.click_button(SubstrateLibraryWorkflowObjectIds.color_mode_box)

        self.click_button(SubstrateLibraryWorkflowObjectIds.color_mode_cmyk)

        self.click_button(SubstrateLibraryWorkflowObjectIds.done_media_mode_button)

    def edit_substrate(self, spice, substrate_name):
        """
        Edit substrate from the substrate view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate
        Args:
            spice: ui fixture
            substrate_name: new substrate name
        """

        # Click on "..."
        self.open_more_options(spice)

        # Edit substrate
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_rename)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_rename_substrate)
        logging.info("At Substrate Rename screen")

        # Rename the substrate
        text_bar = spice.wait_for(SubstrateLibraryWorkflowObjectIds.rename_text_bar)
        text_bar["inputText"] = substrate_name

        # Click on "OK"
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_clone_ok)

        time.sleep(3)

    def rename_substrate(self, spice, mode, substrate_name = ""):
        """
        Clicks on a raw and in result goes to given category view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate
        Args:
            spice: ui fixture
            mode: defines how the new name should be created, possible values:
                0 - new name will be set as empty string
                1 - the new name will be set the same as current name
                2 - new name will be set as: current name + "_1"
                3 - new name = substrate_name
            substrate_name: new value for the name if mode=3
        """

        # Click on "..."
        self.open_more_options(spice)

        # Edit substrate
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_rename)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_rename_substrate)
        logging.info("At Substrate Rename screen")
        time.sleep(2)

        # # Click on OPTIONS
        # self.click_button(SubstrateLibraryWorkflowObjectIds.button_substrate_options)

        # # Goes to options screen

        # # Click on RENAME
        # self.click_button(SubstrateLibraryWorkflowObjectIds.button_options_rename)

        # assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_delete_substrate)
        # time.sleep(2)

        # Get current name
        display_name_textbox = spice.query_item(SubstrateLibraryWorkflowObjectIds.rename_text_bar)
        current_name = display_name_textbox.__getitem__('displayText')
        print("TEST RENAME: current name = " + current_name)

        # Set new name
        if mode == 0:
            new_name = ""
        elif mode == 1:
            name_length = len(current_name) - 2
            new_name = current_name[:name_length]   # will remove "_1" from the end of the string
        elif mode == 2:
            new_name = current_name
        elif mode == 3:
            new_name = substrate_name
        display_name_textbox.__setitem__('displayText', new_name)

        # Confirm rename
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_clone_ok)

    def delete_substrate(self, spice):
        """
        Delete substrate from the substrate view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate
        Args:
            spice: ui fixture
        """

        # Click on "..."
        self.open_more_options(spice)
        time.sleep(2)

        # Delete substrate
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_delete)

        assert spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_delete_substrate)
        time.sleep(2)
        logging.info("At Substrate Delete screen")

        # Click on "Delete"
        self.click_button(SubstrateLibraryWorkflowObjectIds.button_delete_ok)

    def open_more_options(self, spice):
        """
        Open the more options view inside the substrate details view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate
        Args:
            spice: ui fixture
        """
        otherDetailsBtn = spice.wait_for(SubstrateLibraryWorkflowObjectIds.button_more_options, 20)
        otherDetailsBtn.mouse_click()

    def open_mediaMode_more_options(self, spice):
        """
        Open the more options view inside the substrate details view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate->mediaMode
        Args:
            spice: ui fixture
        """
        otherDetailsBtn = spice.wait_for(SubstrateLibraryWorkflowObjectIds.button_mediaMode_options, 20)
        otherDetailsBtn.mouse_click()

    def recover_substrate_name(self, spice):
        """
        Recover substrate name from the substrate view.
        expected view: SubstrateLibrary->Installed substrates view->Category->Substrate
        Args:
            spice: ui fixture
        """
        time.sleep(5)
        return spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_category + " SpiceText")["text"]

    def click_on_mismatch_options_print_anyway(self):
        options_button = self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.mismatch_options_button)
        options_button.mouse_click()
        print_anyway_button = self._spice.wait_for(SubstrateLibraryWorkflowObjectIds.print_anyway_button)
        print_anyway_button.mouse_click()

    def click_backup_button(self):
        if self._spice.uisize in ["XS", "S"]:
            self._spice.substrateLibraryUI().click_button("{} {}".format(SubstrateLibraryWorkflowObjectIds.view_installedSubstrates, SubstrateLibraryWorkflowObjectIds.button_backup))
        else:
            self._spice.substrateLibraryUI().click_button("{} {}".format(SubstrateLibraryWorkflowObjectIds.view_mediaLibraryLayoutFooter, SubstrateLibraryWorkflowObjectIds.button_backup))

    def click_button(self, button_name: str):
        """Search and click the given button.
        Args:
            button_name (str): Object name of the button to click.
        """

        button =  self.check_button_enabled_visible(button_name)
        button.mouse_click()

    def check_button_enabled_visible(self, button_name: str):
        """Search and check the given button is enabled and visible.
        Args:
            button_name (str): Object name of the button to check.
        Returns:
            Button object to operate with it.
        """

        button =  self._spice.wait_for(button_name)
        self._spice.wait_until(lambda: button["enabled"] is True)
        self._spice.wait_until(lambda: button["visible"] is True)

        return button
