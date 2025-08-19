import logging
from dunetuf.ui.uioperations.WorkflowOperations.StorageJobAppWorkflowUICommonOperations import StorageJobAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.PrintFromUsbAppWorkflowObjectIds import PrintFromUsbAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds

class StorageJobAppWorkflowUIXLOperations(StorageJobAppWorkflowUICommonOperations):
    """StorageJobAppWorkflowUIXLOperations class to initialize StorageJob workflow operations."""

    def __init__(self, spice):
        super().__init__(spice)
    
    def goto_job_storage(self):
        '''
        Go to Print from Job Storage app
        '''
        print_app = self.spice.wait_for(HomeAppWorkflowObjectIds.print_app_button)
        print_app.mouse_click()
        
        job_storage_button = self.spice.wait_for(PrintFromUsbAppWorkflowObjectIds.job_storage)
        job_storage_button.mouse_click()
        
        try:
            # Click in comboBoxList
            sign_in_combobox = self.spice.wait_for(MenuAppWorkflowObjectIds.sign_in_combobox)
            sign_in_combobox.mouse_click()

            # Click in the Administrator option
            admin_option = self.spice.wait_for(MenuAppWorkflowObjectIds.list_item_admin)
            middle_width  = admin_option["width"]/2
            middle_height = admin_option["height"]/2
            admin_option.mouse_click(middle_width, middle_height)

            password_textfield = self.spice.wait_for(SignInAppWorkflowObjectIds.adminPasswordInputField)
            password_textfield.__setitem__('displayText', "12345678")

            signin_button = self.spice.wait_for(SignInAppWorkflowObjectIds.adminSignInButtonControl)
            signin_button.mouse_click()
        except TimeoutError:
            logging.info("Job Storage view is load without login")
        
        self.spice.wait_for(MenuAppWorkflowObjectIds.menu_job_storage)
    
    def stored_job_click_ok(self):
        '''
        click Ok button in storageDisabledView screen
        '''
        assert self.spice.wait_for("#storageDisabledView")
        logging.info("Click ok button to cancel the alert")
        ok_button = self.spice.query_item("#okButton")
        ok_button.mouse_click()        
