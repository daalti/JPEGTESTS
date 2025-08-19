import sys

class ISubstrateLibraryAppUIOperations(object):

    def goto_substrate_library(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_installed_substrates(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_packages_printos(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_substrate_category(self, spice, categoryButton, category, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_first_category(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_substrate(self, spice, substrate_id):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_first_substrate(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_add_substrate (self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
