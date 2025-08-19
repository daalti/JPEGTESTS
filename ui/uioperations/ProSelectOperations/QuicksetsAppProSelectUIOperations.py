from dunetuf.ui.uioperations.BaseOperations.IQuicksetsAppUIOperations import IQuicksetsAppUIOperations


class QuicksetsAppProSelectUIOperations(IQuicksetsAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self._spice = spice
