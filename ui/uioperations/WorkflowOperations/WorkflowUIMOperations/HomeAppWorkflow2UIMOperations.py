from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflow2UICommonOperations import HomeAppWorkflow2UICommonOperations

class HomeAppWorkflow2UIMOperations(HomeAppWorkflow2UICommonOperations):

    def __init__(self, spice):
        self.spice = spice
        super().__init__(spice)
