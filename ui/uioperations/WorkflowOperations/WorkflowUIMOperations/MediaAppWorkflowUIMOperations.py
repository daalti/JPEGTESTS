
import logging
import time

from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowUICommonOperations import MediaAppWorkflowUICommonOperations
from dunetuf.configuration import Configuration
from dunetuf.cdm import CDM

class MediaAppWorkflowUIMOperations(MediaAppWorkflowUICommonOperations):
    
    ALERT_DETAIL_DESCRIPTION = "#contentItem"
    ALERT_TITLE_TEXT = "#textContainerObject #titleObject"	

    
    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120
        
        configuration = Configuration(CDM(spice.ipaddress))
        is_enterprise = configuration.familyname == 'enterprise'

        self.MEDIA_ALERT_TITLE_CSTRINGS =  { 
            "standard_bin_full"               : "cStandardBinParam" if is_enterprise else "cOutputBinFullHeader",
            "bin_full"                      : "cVariableBinFull" if is_enterprise else None} # Note: homePro doesn't report binfull string alone.
            
        self.MEDIA_ALERT_CONTENT_CSTRINGS = {
            "standard_bin_full"               : "cRemoveAllPaperFromBin" if is_enterprise else "cOutputBinRemovePaper"
            }
    
    def get_alert_message(self):
        alertMessage = self._spice.wait_for(self.ALERT_TITLE_TEXT)
        return str(alertMessage["text"])
    
    def get_alert_message_details(self):
        alertMessageDetails = self._spice.wait_for(self.ALERT_DETAIL_DESCRIPTION)
        return str(alertMessageDetails["text"])