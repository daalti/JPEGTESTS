
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.OOBEAppWorkflowUICommonOperations import OOBEAppWorkflowUICommonOperations


class OOBEAppWorkflowUILOperations(OOBEAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        super().__init__(self.spice)

    def goto_language_confirmation_screen(self, spice, language="#DeviceLanguageView #DeviceLanguageViewverticalLayout #GenericStructureView #SpiceView #SpiceListViewView") -> None:
        """Selects the language in oobe flow and go to language confirmation screen

        Args:
            spice: spice instance  
            language: objectName of the language list
        Returns:
            None 
        """
        self.goto_language_screen(spice)

        # TBD: need to enable scrolling
        # spice.homeMenuUI().menu_navigation(spice, "#RadioButtonListLayout", language)

        languageList = spice.wait_for(language)

        # Set the index position based on the language to be set
        languageList.__setitem__("_indexPosition", "0")
        languageList.mouse_click()

        # Language Confirmation Screen
        logging.info("Entering Language Confirmation Screen")
        assert spice.wait_for("#langConfirmPopup")
        logging.info("At Language Confirmation Screen")

    def goto_network_settings_screen(
        self, spice, udw=None,
        altitude="#oobeAltitudeView #oobeAltitudeViewverticalLayout #GenericStructureView #SpiceView #SpiceListViewView",
        country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #SpiceView #SpiceListViewView"
        ) -> None:
        """Select the altitude on oobe flow and goto network screen

        Args:
            spice: spice instance 
            altitude: objectName of altitude list     
        Returns:
            None 
        """
        response = self.cdm.get("cdm/deviceSetup/v1/status")
        if "actionAltitudeConfiguration" in response:
            self.goto_altitude_screen(spice, udw)
            altitudeList = spice.wait_for(altitude)

            # Set the index position based on the altitude to be set
            altitudeList.__setitem__("_indexPosition", "0")
            altitudeFirstPosition = spice.wait_for("#altitudeTextImageBranch0")
            altitudeFirstPosition.mouse_click()
        else:
            self.goto_country_screen(spice, udw)
            countryList = spice.wait_for(country)

            # Set the index position based on the country to be set
            countryList.__setitem__("_indexPosition", "0")
            countryList.mouse_click()

        self.goto_set_date_time_screen()
        # Network Settings Screen
        logging.info("Entering Network Setting Screen")
        assert spice.wait_for("#oobeNetworkSummary")
        logging.info("At Network Setting Screen")
    
    def click_country(self) -> bool:
        list = self.workflow_common_operations.get_element("#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #mainPanelArea #SpiceView #SpiceListViewView")
        list.__setitem__("_indexPosition", 0)
        us_button = self.workflow_common_operations.get_element("#OobeCountryRegionView #232 #SpiceRadioButton")
        if not us_button: return False
        return self.workflow_common_operations.click(us_button, check_enabled=False)
