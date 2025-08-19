from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryAppWorkflowUICommonOperations import SubstrateLibraryAppWorkflowUICommonOperations
import time

from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryWorkflowObjectIds import SubstrateLibraryWorkflowObjectIds

class SubstrateLibraryAppWorkflowUIXLOperations(SubstrateLibraryAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def delete_substrate_per_id(self, spice, cdm, substrate_id):
        """
        Deletes a substrate from the substrate library by its ID.

        Args:
            spice (object): The main application object used to interact with the UI.
            cdm (object): The context data model object.
            substrate_id (str): The unique identifier of the substrate to be deleted.

        Returns:
            None
        """
        spice.substrateLibraryUI().goto_substrate_category(spice, SubstrateLibraryWorkflowObjectIds.button_category_custom_paper, SubstrateLibraryWorkflowObjectIds.category_custom, cdm)
        delete_button = spice.wait_for("#"+substrate_id+"_secondaryButton")
        delete_button.mouse_click()

        # Confirm delete
        delete_ok_button = spice.wait_for(SubstrateLibraryWorkflowObjectIds.button_delete_ok)
        delete_ok_button.mouse_click()

         # Check if progress window displayed
        assert(spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_delete_progress)), "VERIFY error: PROGRESS window for delete MEDIA not displayed."           
            