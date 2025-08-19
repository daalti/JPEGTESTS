from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowUICommonOperations import NetworkFolderAppWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.ScanAppWorkflowUISOperations import ScanAppWorkflowUISOperations
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUISOperations.WorkflowUICommonSOperations import WorkflowUICommonSOperations
from dunetuf.ui.uioperations.WorkflowOperations.NetworkFolderAppWorkflowObjectIds import NetworkFolderAppWorkflowObjectIds

class NetworkFolderAppWorkflowUISOperations(NetworkFolderAppWorkflowUICommonOperations):
    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice
        self.scan_operations = ScanAppWorkflowUISOperations(self.spice)
        self.workflow_common_operations = WorkflowUICommonSOperations(self.spice)

    def validate_screen_buttons(self, net, isButtonConstrained, buttonObjectId, isEjectButtonVisible):
        button_ids = [
            NetworkFolderAppWorkflowObjectIds.button_network_folder_send,
            NetworkFolderAppWorkflowObjectIds.button_network_folder_start,
        ]

        button = None
        for button_id in button_ids:
            if buttonObjectId == button_id:
                try:
                    button = self.spice.wait_for(button_id, 60)
                    self.wait_and_validate_property_value(button, "visible", True, 30)
                    self.wait_and_validate_property_value(button, "enabled", True, 30)
                    self.wait_and_validate_property_value(button, "constrained", isButtonConstrained, 30)
                    break
                except:
                    continue

        if button is None:
            raise ValueError(f"Button with ID {buttonObjectId} not found")

        #Get Eject
        ejectButton = self.spice.wait_for( NetworkFolderAppWorkflowObjectIds.eject_button_for_beam_power_mfp, 5 )

        #Validate eject
        assert ejectButton["visible"] == isEjectButtonVisible

    @staticmethod
    def check_eject_button_operation(spice):
        eject_button =spice.wait_for(NetworkFolderAppWorkflowObjectIds.eject_button_for_beam_power_mfp)
        eject_button.mouse_click()
        WorkflowUICommonSOperations.wait_until_object_not_visible(spice, eject_button)

