import logging

from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowUICommonOperations import SignInAppWorkflowUIOperations
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.security.SecurityTypes import AuthenticationMethod

class SignInAppWorkflowUIXSOperations(SignInAppWorkflowUIOperations):

    def click_password_input_reveal_icon(self) -> bool:
        """
            XS workflow UI specific implementation to click the password reveal icon in the sign-in screen.
            The Workflow1 version
        """
        currentAgent = self.get_authentication_method_from_current_sign_in_page()
        scroll_bar_locator = self.get_sign_in_scroll_bar_locator(currentAgent)
        scroll_bar = self.workflow_common_operations.get_element(scroll_bar_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not scroll_bar:
            logging.error(f"Failed to get scroll_bar: {scroll_bar_locator}")
            return False

        signInScreenLocator = self.get_current_sign_in_view_locator(currentAgent)
        signInScreen = self.workflow_common_operations.get_element(signInScreenLocator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        signInScreenHeight = self.workflow_common_operations.get_element_property(signInScreen, "height")
        if not signInScreenHeight:
            logging.error(f"Failed to get height of: {scroll_bar_locator}")
            return False

        password_field_locator = self.get_password_input_field_locator(currentAgent)
        password_field = self.workflow_common_operations.get_element(password_field_locator, timeout=self.TIMEOUT_IMMEDIATE_CHECK_WITH_RETRY)
        if not password_field:
            logging.error(f"Failed to get password_field: {password_field_locator}")
            return False

        if not self.workflow_common_operations.scroll_vertical(scroll_bar, password_field, signInScreenHeight):
            logging.error(f"Failed to scroll to password field: {password_field_locator}")
            return False

        button_locator = self.get_password_reveal_icon_locator(currentAgent)
        reveal_icon_button = self.workflow_common_operations.get_element(button_locator)
        if not reveal_icon_button:
            logging.error(f"Failed to get reveal_icon_button: {button_locator}")
            return False

        logging.info(f"Clicking reveal icon button: {button_locator}")
        outcome = self.workflow_common_operations.click(reveal_icon_button)
        if not outcome:
            logging.error(f"Failed to click reveal icon button: {button_locator}")
        return outcome
