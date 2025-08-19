
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.OOBEAppWorkflowUICommonOperations import OOBEAppWorkflowUICommonOperations
class OOBEAppWorkflowUIXSOperations(OOBEAppWorkflowUICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        super().__init__(self.spice)

    def goto_network_settings_screen(
        self, spice, udw=None,
        country="#OobeCountryRegionView #OobeCountryRegionViewverticalLayout #GenericStructureView #panelsStack #nativeStackView #SpiceView #SpiceListViewView"
        ) -> None:
        """goto network screen

        Args:
            spice: spice instance  
            oobe: oobe instance
            udw: underware instance
            country: objectName of country list
        Returns:
            None 
        """
        self.goto_country_screen(spice, udw)
        countryList = spice.wait_for(country)

        # Set the index position based on the country to be set
        countryList.__setitem__("_indexPosition", "0")
        countryList.mouse_click()

        # Network Settings Screen
        assert spice.wait_for("#oobeNetworkSummary")
        logging.info("At Network Setting Screen")

    def goto_thank_you_screen(self, oobe):
        """ Navigate from begining of oobe to the thank you screen"""

        self.goto_network_settings_screen(self.spice, oobe)
        optionButton = self.spice.wait_for("#continueButton")
        optionButton.mouse_click()

        try:
            self.spice.wait_for("#IccErrorView", 40)
            skipInternetButton = self.spice.wait_for("#SkipButton")
            skipInternetButton.mouse_click()
        except:
            pass

        self.firmware_update_config_page(self.spice)
        self.select_firmware_update_option(self.spice)
        self.goto_set_date_time_screen()
        
        # Thank You Screen
        assert self.spice.wait_for("#oobeThankYouMessageView")
        logging.info("At thank you screen")

    def enter_admin_pin(self, spice, password, confirmPassword):
        """Enters Admin Pin
        Args:
            spice: spice instance 
            password: new admin pin
            confirmPassword: confirming admin pin         
        Returns:
            None 
        """
        logging.info("Entering new passwords for admin")
        spice.wait_for("#oobeAdminPasswordEdit")

        spice.wait_for("#adminPasswordTextField").mouse_click()
        spice.keyBoard.keyboard_set_text_with_out_dial_action(password, '#adminPasswordTextField')

        scrollbar = self.spice.wait_for("#adminPasswordMainViewScrollBar")
        scrollbar.__setitem__("position", ".4")

        spice.wait_for("#adminPasswordConfirmTextField").mouse_click()
        spice.keyBoard.keyboard_set_text_with_out_dial_action(confirmPassword, '#adminPasswordConfirmTextField')

        applyButton = spice.wait_for("#oobeAdminPasswordEditFooter #applyButton")
        applyButton.mouse_click()