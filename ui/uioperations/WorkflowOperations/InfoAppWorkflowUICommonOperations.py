
from dunetuf.ui.uioperations.BaseOperations.IInfoAppUIOperations import IInfoAppUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowUICommonOperations import MenuAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from time import sleep
from dunetuf.localization.LocalizationHelper import LocalizationHelper




class InfoAppWorkflowUICommonOperations(IInfoAppUIOperations):

    hostname_name = "#ethernet_hostName #ValueText"
    Ip_adress = "#ethernet_ipAddress #ValueText"
    Ipv6_adress_state = "#ethernet_ipv6Status #ValueText"
    MAC_adress_eth0 = "#ethernet_macAddress #ValueText"


    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        self.maxtimeout = 120
        self.home_menu_dial_operations = spice.menu_operations
        self.workflow_common_operations = spice.basic_common_operations

    
    def goto_info(self):
        self.home_menu_dial_operations.goto_menu_info(self._spice)

    def click_on_card(self,object_name):
        card = self._spice.wait_for(object_name)
        middle_width = int(card["width"] / 2)
        middle_height = int(card["height"] / 2)
        card.mouse_click(middle_width, middle_height)
    
