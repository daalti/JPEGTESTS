from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowUICommonOperations import StatusCenterWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.StatusCenterWorkflowObjectIds import StatusCenterWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds

class StatusCenterWorkflowUISOperations(StatusCenterWorkflowUICommonOperations):

    def compare_homescreen_and_status_center_sign_in_buttons(self, spice):
        """
            Compares two sign in buttons to see if they both are "Sign In" buttons or "Sign Out" buttons
            Returns True if they are the same and False otherwise
        """
        homescreen_sign_in_button_text = spice.query_item(SignInAppWorkflowObjectIds.menu_item_signinid + " SpiceText")["text"]
        spice.status_center.expand()
        status_center_sign_in_button_text = self.get_sign_in_button_text()
        spice.status_center.collapse()
        return homescreen_sign_in_button_text == status_center_sign_in_button_text
