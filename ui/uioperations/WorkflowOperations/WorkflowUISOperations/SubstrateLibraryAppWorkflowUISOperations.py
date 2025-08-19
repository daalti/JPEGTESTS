from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryAppWorkflowUICommonOperations import SubstrateLibraryAppWorkflowUICommonOperations
import time

from dunetuf.ui.uioperations.WorkflowOperations.SubstrateLibraryWorkflowObjectIds import SubstrateLibraryWorkflowObjectIds

class SubstrateLibraryAppWorkflowUISOperations(SubstrateLibraryAppWorkflowUICommonOperations):

    def __init__(self, spice):
        super().__init__(spice)
        self.maxtimeout = 120

    def delete_substrate_per_id(self, spice, cdm, substrate_id):
        """
        Deletes a substrate by its ID.

        Args:
            spice (object): The spice object to interact with the substrate library UI.
            cdm (object): The cdm object required for navigation within the substrate library.
            substrate_id (str): The ID of the substrate to be deleted.

        Returns:
            None
        """
        spice.substrateLibraryUI().goto_substrate_category(spice, SubstrateLibraryWorkflowObjectIds.button_category_textile_paper, SubstrateLibraryWorkflowObjectIds.category_textile, cdm)
        spice.substrateLibraryUI().goto_substrate(spice, "#"+substrate_id)
        # Delete the substrate. Set valid new name.
        spice.substrateLibraryUI().delete_substrate(spice)

        # Check if progress window displayed
        assert(spice.wait_for(SubstrateLibraryWorkflowObjectIds.view_delete_progress)), "VERIFY error: PROGRESS window for delete MEDIA not displayed."
        
        