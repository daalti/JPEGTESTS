#########################################################################################
# @file      IFaxDiagnosticUIOperations.py
# @author    Praveen
# @date      28-11-2021
# @brief     Interface for all the Fax Diagnostics methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
import sys


class IFaxDiagnosticUIOperations(object):

    def single_modem_tone(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def showallfaxlocations(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_faxdiagnosticsmenu_hookoperations(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def generate_dial_phone_no(self, cdm):  
         raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_faxdiagnostics_faxParameters(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_faxdiagnostics_generaterandomdata(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
