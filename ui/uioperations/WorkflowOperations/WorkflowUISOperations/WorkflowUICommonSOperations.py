
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations


class WorkflowUICommonSOperations(WorkflowUICommonOperations):

    def __init__(self, spice):

        self.maxtimeout = 120
        self._spice = spice
        
    def click_button_on_middle(self, button):
        """
        Click in the middle of the received button 
        """
        try:
            # Validate object Button and click it on middle
            self._spice.wait_until(lambda: button["enabled"] == True) 
            middle_width = button["width"] / 2
            middle_height = button["height"] / 2
            button.mouse_click(middle_width, middle_height)
            time.sleep(3)
        except:
            logging.info("FAILED: Button is not enabled")
