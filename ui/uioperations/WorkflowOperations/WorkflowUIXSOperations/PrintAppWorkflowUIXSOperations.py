import logging
from dunetuf.ui.uioperations.WorkflowOperations.PrintAppWorkflowUICommonOperations import PrintAppWorkflowUICommonOperations

class PrintAppWorkflowUIXSOperations(PrintAppWorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice

        self.PRINT_QUALITY_VIEW = "#printQualityMenuList"
        self.TONER_DENSITY = "#tonerDensityMenuSlider"
        self.LESS_PAPER_CURL = "#lessPaperCurlWFMenuSwitch"
        self.workflow_common_operations = spice.basic_common_operations

    def get_toner_density_slider_value(self):
        '''
        Ui Should be in print quality panel
        Get toner density slider value
        '''
        self._spice.wait_for(self.PRINT_QUALITY_VIEW)
        self._spice.wait_for(self.TONER_DENSITY)
        current_element = self._spice.query_item(self.TONER_DENSITY)
        print(current_element.__getitem__('value'))
        return current_element.__getitem__('value')

    def set_toner_density_slider_value(self, value):
        '''
        Ui Should be in print quality panel
        Set toner density slider value
        '''
        self._spice.wait_for(self.PRINT_QUALITY_VIEW)
        slider = self._spice.wait_for(self.TONER_DENSITY)
        slider.__setitem__('value', value)
    
    def get_less_paper_curl_toggle_state(self):
        """Get 'Less Paper Curl' toggle state"""
        self._spice.wait_for(self.LESS_PAPER_CURL, timeout = 10)
        less_paper_curl_toggled_state = self._spice.query_item(self.LESS_PAPER_CURL)["checked"]
        logging.info("'Less Paper Curl' toggle state : %s", less_paper_curl_toggled_state)
        return 'true' if less_paper_curl_toggled_state else 'false'
    
    def click_less_paper_curl_toggle(self):
        """Click 'Less Paper Curl' toggle"""
        self._spice.wait_for(self.LESS_PAPER_CURL, timeout = 10)
        self._spice.query_item(self.LESS_PAPER_CURL).mouse_click()
