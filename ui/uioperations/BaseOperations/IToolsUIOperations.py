#########################################################################################
# @file      IToolsUIOperations.py
# @author    Srinivas
# @date      27-01-2022
# @brief     Interface for all the Fax Diagnostics methods
#            Interface for service pin methods
# (c) Copyright HP Inc. 2022. All rights reserved.
###########################################################################################
import sys


class IToolsUIOperations(object):

    def servicePinTest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def troubleshoot_fax_runFaxTest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def troubleshoot_fax_PBXRingDetect(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def troubleshoot_fax_clearFaxMemoryLog(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def troubleshoot_fax_faxT30RepMode(self, cdm):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def troubleshooting_print_quality_image_registration(self,cdm, tray):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def validate_image_registration_limits(self, tray, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_servicetests_continuousflatbedtest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_servicetests_displaytest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_servicetests_continuousadfpicktest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_servicetests_scanmotortest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def servicemenu_servicetests_frontusbporttest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_serviceresets_transferkitreset(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def servicemenu_servicetests_serviceinfinitehs(self, kvp, cdm, job, net, locale):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def maintenancemenu_restoresettings_check_visibility_of_restore_button_under_restoreallfactorydefaults(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def maintenancemenu_restoresettings_check_visibility_of_cancel_button_under_restoreallfactorydefaults(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def maintenancemenu_restoresettings_click_cancel_button_under_restoreallfactorydefaults(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
