import sys

class IStorageJobAppUIOperations(object):

    def goto_mainmenu(self):
        """
        Purpose: Navigates to Home screen Menu App from any other screen
        Ui Flow: Any screen -> Main menu
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_job_storage(self):
        """
        Purpose: Navigates to Job Storage app screen from any other screen
        Ui Flow: Any screen -> Main menu -> Job Storage app
        :param spice: Takes 0 arguments
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def job_storage_click_button(self, buttonName):
        """
        Purpose: Click to the button 'buttonName' inside job storage app screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_jobStorageFormatUsbSuccessful_okButton(self, dunestorejob):
        """
        Purpose: Click to the ok button after the jobStorageFormatUsbSuccessful
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_jobStorageFormatUsb_continueButton(self):
        """
        Purpose: Click to the continue button after the jobStorageFormatUsb
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_storageJob(self, userName, fileName):
        """
        Purpose: Select the store Job
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def print_storeJob_selected(self):
        """
        Purpose: Print the selected Store Job
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def delete_storeJob_selected(self):
        """
        Purpose: Delete the selected Store Job
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def detailed_storeJob_selected(self):
        """
        Purpose: Go to detailed view of the selected Store Job
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_job_from_storage(self, jobName, query_index=0):
        """
        Purpose: Select the job from job storage
        :param jobName: Name of the job to be selected
        :param query_index: Index of the job in the list (default is 0)
        :return: None
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_list_object_visibility_by_id(self, list_view_id, target_item_id, timeout=5):
        """
        Validates if a target item is visible within a list view by querying the elements using their object IDs.
        
        :param list_view_id: Object ID of the list view container
        :param target_item_id: Object ID of the target item to check visibility for
        :param timeout: Timeout for waiting for elements (default: 5 seconds)
        :return: True if the target item is visible, False otherwise
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def close_detail_panel(self):
        """
        Hide detail panel if it is open.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_more_options_visible(self, timeout=10):
        """
        Checks if the More Options button is visible in the Job Storage app.
        
        :param timeout: Timeout for waiting for the More Options button (default: 10 seconds)
        :return: True if the More Options button is visible, False otherwise
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_number_of_copies_in_settings_view(self, value: int):
        """
        Set the number of copies in the settings view spin box
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_number_of_copies_in_settings_view(self):
        """
        Get the number of copies from the settings view spin box
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
