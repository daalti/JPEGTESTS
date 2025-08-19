import sys
from dunetuf.ews.pom.quick_sets.quicksets_enum import QuickSetStartOption

class IMenuAppUIOperations(object):

    is_menu_enabled = False

    # Menu

    def goto_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Help
    
    def goto_help(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Status

    def goto_status(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu

    def goto_menu_info(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_status(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_copy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_idCopy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_scan(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_print(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_fax(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_status(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_contacts(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_supplies(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_trays(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_quickSets(self, spice, quickset_type=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_cloudScanToEmail(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_scanToCloud(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_jobs(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Status
    def goto_joblog(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Settings

    def goto_menu_settings_rolls(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_scan(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_copy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_supplies(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_supplies_verylowbehavior(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_supplies_lowwarningthreshold(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)  

    def goto_menu_settings_supplies_storesupplyusagedata(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_supplies_authorizedhpcartridgepolicy(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_supplies_cartridgeprotection(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_supplies_resetsupplies(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_eventsandnotifications(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_security(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_webservices(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_network(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_replaceableparts(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_print(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_jobs_settings(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_finisher(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_developeroptions(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_fax(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_tray(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_printerUpdate(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_printerUpdate_allowUpgrades(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
     
    def goto_menu_settings_printerUpdate_allowUpgrades_iris_options(self, spice, enterNav=True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_printerUpdate_allowAutoUpdate(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_printerUpdate_notifyWhenAvailable(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_printerUpdate_allowAutoUpdate_goto_iris_message_screen(self, spice, net):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_printerUpdate_notifyWhenAvailable_goto_iris_message_screen(self, spice, net, enterNav=True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Settings General

    def goto_menu_settings_general_inactivitytimeout(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_energy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_energy_disableshutdown(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_settings_general_energy_shutdown(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_energy_sleep(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_units(self, spice, units):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Settings General Energy Sleep

    def set_energysleep_fiveminutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_energysleep_tenminutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_energysleep_fifteenminutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_energysleep_thirtyminutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_energysleep_onehour(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    

    # Menu Settings General Energy Shutdown

    def set_energyshutdown_never(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_energyshutdown_onehour(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_energyshutdown_twohours(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_energyshutdown_threehours(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_energyshutdown_fourhours(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Settings General Energy Disable Shutdown

    def set_energydisableshutdown_donotdisable(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_energydisableshutdown_whenportsareactive(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    

    # Menu Settings General Volume

    def set_volume_slider_validation(self, spice ):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Settings General Inactivity Timeout

    def set_inactivitytimeout_never(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_inactivitytimeout_thirtyseconds(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_inactivitytimeout_oneminute(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_inactivitytimeout_twominutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_inactivitytimeout_fiveminutes(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_inactivity_timeout_options_visible(self, spice):
        """
        Check timeout options shows in inactivity timeout screen.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_selected_inactivity_timeout_value(self, spice, inactivity_value,isEnterPriseProduct=False):
        '''
        This is helper method to verify selected inactivity timeout value
        UI flow Menu > Settings > General > Inactivity Timeout
        Args: inactivity_value: 30/60/120/300
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu settings job settings

    def is_visible_jobs_settings_menu_option(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_hide_deleted_jobs(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_hide_deleted_jobs(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_hide_deleted_jobs(self, spice, value:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_cancel_jobs_on_hold_delay(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_cancel_jobs_on_hold_delay(self, spice) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_cancel_jobs_on_hold_delay(self, spice, value:int) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_job_queue_recovery_mode(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_job_queue_recovery_mode(self, spice) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_job_queue_recovery_mode(self, spice, value:str) -> int:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_job_on_hold_for_manual_release(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_job_on_hold_for_manual_release(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_job_on_hold_for_manual_release(self, spice, enable:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)


    def is_visible_reprint_resend_jobs_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_reprint_resend_jobs_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_reprint_resend_jobs_enabled(self, spice, enable:bool, confirm_disabled:bool = False) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_visible_promote_to_interrupt_print_job_enabled(self, spice) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_visible_promote_to_interrupt_print_job_enabled(self, spice, enable:bool) -> bool:
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Tools

    def goto_menu_tools_reports(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_maintenance(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)  

    def goto_menu_tools_servicemenu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_reportnewproblem(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    # Menu Tools Troubleshooting
    def goto_menu_tools_troubleshooting_printquality(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_printquality_printqualitytroubleshootingpage(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_printquality_colorcalibration(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_print_quality_tray_alignment(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax_FaxT30ReportMode(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax_RunFaxTest(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax_ClearFaxLogMemory(self, spice, pressClearButton2 = True):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax_PBXRingDetect(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_troubleshooting_Fax_JBIG_Compression(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_troubleshooting_Fax_JBIG_Compression(self, spice, enableOption = False):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

	# Menu Tools Maintenace
	
    def goto_menu_tools_maintenance_restoresettingsmenu(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_tools_maintenance_restoresettingsmenu_resetusersettings(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_maintenance_restoresettingsmenu_resetuserdata(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_mfp(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_maintenance_restoresettingsmenu_restoreallfactorydefaults_sfp(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

	# Menu Tools Reports
    
    def goto_menu_tools_reports_statusreports(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   # Menu Tools Service Menu

    def goto_menu_tools_servicemenu_information(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_serviceresets(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_systemconfiguration(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_connectivitydiagnostics(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    # Menu Tools Service Menu Information Menu

    def goto_menu_tools_servicemenu_information_productnumber(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_serialnumber(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_regionlanguage(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_servicecounts(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_firmwarerevision(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_eventlog(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_assertlog(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_information_wirelessregion(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Tools Service Menu Service Resets

    def goto_menu_tools_servicemenu_serviceresets_usersettingsreset(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_serviceresets_userdatareset(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_tools_servicemenu_serviceresets_factorydatareset(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_serviceresets_transferkitreset(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_serviceresets_repairmode(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

     # Menu Tools Service Menu System Configuration

    def goto_menu_tools_servicemenu_systemconfiguration_serialnumber(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_systemconfiguration_serviceid(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_systemconfiguration_ethernetmac(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_systemconfiguration_switchbootmode(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_systemconfiguration_coldresetpaper(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Tools Service Menu Fax Diagnostics

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_hookoperations(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_showallfaxlocations(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnosticsmenu_transmitsignalloss(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_generateDialNumber(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_ringSettings(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_faxV29SpeedSelection(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_generaterandomdata(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_generatesinglemodemtonemenu(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_faxdiagnostics_faxparameters(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_supportmenu_faxdiagnosticsmenu_generatedialingtonespulses(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)    

    # Menu Tools Service Menu Connectivity Menu

    def goto_menu_tools_servicemenu_connectivity_report(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_connectivity_wirelessdiagnostic(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_connectivity_capturenwtrace(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_connectivity_wirelessmetrics(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Tools  Service Menu Service Tests

    def goto_menu_tools_servicemenu_servicetests_scanmotortest(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_frontusbporttest(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_servicekeys(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_displaytest(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_contadfpick(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_flatbed(self, spice, udw):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_tools_servicemenu_servicetests_serviceinfinitehs(self, spice, udw, kvp):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    # Menu Help

    def goto_menu_help_howtovideos(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_digitalofficetips(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_printerinformation(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_help_product_tour(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Help Working Smart Tips

    def goto_menu_help_workingsmarttips_twosideddocumentswithfax(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips_twosideddocumentswithoutfax(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips_usingthekeyboard(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips_controlpanelnavigation(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips_wifidirect(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_workingsmarttips_idcardcopy(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Help Digital Office Tips

    def goto_menu_help_digitalofficetips_documentscanning(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_digitalofficetips_mobileprinting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_digitalofficetips_usbprinting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_digitalofficetips_printapps(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    # Menu Help Environmental Tips

    def goto_menu_help_hpenvironmentaltips_shutdown(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips_sleep(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips_recycle(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips_twosidedcopying(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips_twosidedprinting(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_hpenvironmentaltips_scheduleonoff(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

# Menu Help How To Videos

    def goto_menu_help_howtovideos_loadpaperintray2legal(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_help_howtovideos_clearajaminthedocumentfeeder(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadpaperintray3legal(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadpaperintray3(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_clearajamintray2(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_insertausbdevicejobstorage(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_manualduplexfromtray1(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_clearajamintheoutputbin(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_clearajamintray1(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_connectanextensionphone(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_cleanthescannerglass(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_insertausbdevicewalkup(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadoriginalsonthescannerglass(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadpaperintray2(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_replacethecyancartridge(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_connectafaxcable(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadpaperintray1(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_manualduplexfromtray2(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_replacetheyellowcartridge(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_replacethemagentacartridge(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_loadoriginalsinthedocumentfeeder(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_replacetheblackcartridge(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_clearajamintray3(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_howtovideos_clearajaminsidetheprinter(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_product_tour_play_demo_once(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_help_product_tour_play_demo_repeat(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_system_alert_and_close(self,spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_system_alert(self,spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_menu_quickSets_and_check_loading_screen(self, spice, net, quickset_type=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_copy_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_network_folder_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_scan_to_email_quickset_from_menu_quickset(self, spice, cdm, udw, quickset_name, start_option=QuickSetStartOption.user_presses_start, profile_name=None):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_spec_on_quicksets_home_screen(self, spice, net, quickset_name):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_scan_scan_to_email(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_sharepoint_quickset_from_menu_quickset(self, spice, quickset_name, start_option=QuickSetStartOption.user_presses_start):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_fax_t30_report_mode_from_troubleshooting_fax(self, spice, fax_t30_report_mode):
        '''
        This is helper method to select fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_save_button_fax_t30_report_mode_view(self, spice):
        '''
        This is helper method to save fax T30 report mode from troubleshooting
        UI should be Menu->Tools->Troubleshooting->Fax->Fax T.30 Trace Report
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_set_fax_t30_report_mode_successfully(self, spice, fax_t30_report_mode):
        '''
        This is helper method to verify set fax T30 report mode successfully
        UI should be Menu->Tools->Troubleshooting->Fax
        Args: fax_t30_report_mode: fax T30 report mode
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_display(self, spice):
        """
        Navigates to Menu App --> Settings --> General -->Display
        @param spice:  
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_energy_inactivity_shutdown_value(self,spice,inactivity_shutdown_value):
        '''
        Select an inactivity shutdown value in inactivity shutdown screen.
        Args: inactivity_shutdown_value: inactivity shutdown value
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_inactivity_shutdown_options_list_display_in_ui(self, net, spice, inactivity_shutdown_options):
        """
        UI Workflow should be: Inactivity Shutdown screen
        Verify inactivity shutdown options list display correctly.
        Args: inactivity_shutdown_options: inactivity shutdown options
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_set_inactivity_shutdown_option_display_in_ui(self, spice, inactivity_shutdown_value):
        """
        UI Workflow should be: Energy  Settings screen
        Verify set inactivity shutdown option display correctly.
        Args: inactivity_shutdown_value: inactivity shutdown value
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_energy_shutdown_already_signin(self, spice):
        '''
        UI flow: Menu > Settings > General > Energy > Inactivity Shutdown(Already sign in from sign app)
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_reset_button(self, spice):
        """
        click reset button under reset user settings and reset user data
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def select_status_reports_mode_from_menu_tools_reports_status_reports(self, spice, status_reports_mode, check_expected=True):
        '''
        This is helper method to select status reports mode from tools -> reports -> status reports
        UI should be Menu->Tools-> Reports -> Status Reports
        Args: status_reports_mode: status reports mode, such as Network Security Report/Usage RePORT /Web Access Test Report/ Job Log and so on...
                                   add different status reports mode implementation if necessary
              check_expected: True/False, if permission is applied we would be expected the login screen instead of report getting selected
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def print_status_reports_with_click_print_button(self, spice):
        '''
        This is helper method to click print button to printing status reports.
        UI should be Menu->Tools-> Reports -> Status Reports
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def print_eventlog_with_click_print_button(self, spice):
        '''
        This is helper method to click print button to print the eventlog.
        UI should be Menu -> Tools -> Reports -> Event Log
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def print_prt_log_list(self, spice):
        '''
        This is helper method to select a number of reports and click print.
        UI should be Menu-> Tools -> Reports -> Status Reports
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_print_defaultprintoptions(self, spice):
        '''
        UI flow: Menu > Settings > Print > Default Print Options
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def modify_sides_default_print_options(self, spice, select_side):
        '''
        UI flow: Menu > Settings > Print > Default Print Options > Sides
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_traysettings(self, spice):
        '''
        UI flow: Menu > Settings > Tray Settings
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_settings_tray_manual_feed(self, spice, enableOption = True):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable Manual feed
        @param spice: 
        @param enableOption: True to enable manual feed False to Disable
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_settings_tray_alternative_letterhead_mode(self, spice, enableOption = True):
        """
        Helper method to enable/disable Alternative Letterhead Mode
        UI Should be in Menu App --> Settings --> tray and enable/disable Alternative Letterhead Mode
        @param spice:
        @param enableOption: True to enable Alternative Letterhead Mode, False to disable
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
      
    def change_settings_tray_override_size_errors(self, spice, enableOption = True):
        """
        Helper method to enable/disable override size errors
        UI should be in Menu --> Settings --> Tray
        @param spice:
        @param enableOption: True to enable override size errors, False to disable
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def change_settings_size_type_prompt(self, spice, select_prompt):
        """
        Helper method to enable/disable manual feed
        UI Should be in Menu App --> Settings --> tray and enable/disable size/type Prompt
        @param spice: 
        @param enableOption: True to enable size/type Prompt False to Disable
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_traysettings_paperoutaction(self, spice):
        '''
        UI flow: Menu > Settings > Tray Settings > Paper Out Action
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_autocontinue_timeout_combobox(self, spice):
        '''
        UI flow: Menu > Settings > Tray Settings > Paper Out Action > Auto Continue Timeout
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_autocontinue_action_combobox(self, spice):
        '''
        UI flow: Menu > Settings > Tray Settings > Paper Out Action > Auto Continue Action
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_date_from_menu_settings_general_date_time(self, spice):
        """
        goto set Data screen from menu -> settings->general -> date and time screen
        UI should be in Menu -> Settings-> General -> Date and Time screen
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def goto_settings_general_quietmode_from_to(self, spice):
        """
        Goto quite mode From-To
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> enable Quiet mode
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_from_to_start_time(self, spice, from_hour=None, from_minutes=None):
        """
        Set from to start time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_from_to_end_time(self, spice, to_hour=None, to_minutes=None):
        """
        Set from to end time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To -> Next
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_hour_value_on_settings_general_quietmode_from_to(self, spice, value:str):
        """
        Set from to time hour value
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_minutes_value_on_settings_general_quietmode_from_to(self, spice, value:str):
        """
        Set from to time minutes value
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def click_next_btn_on_from_to_screen(self, spice):
        """
        Click next button on from to set time screen
        UI Should be in Menu App --> Settings --> General --> Quiet Mode --> From-To 
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_quitemode_from_to_time(self, spice):
        """
        Get current From-To time
        UI Should be in Menu App --> Settings --> General --> Quiet Mode
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def verify_settings_general_quickmode_schedule(self, spice, enable_status):
        """
        Helper method to verify the enabled/disabled state of Quiet Mode Schedule
        UI Should be in Menu App --> Settings --> General --> Quiet Mode (schedule must be support)
        @param spice:
        @param enabledOption: True to verify enabled state and False to verify Disabled state
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_date_value_on_menu_settings_general_datetime(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_time_value_on_menu_settings_general_date_time(self, spice):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_menu_settings_general_date_time_date_day(self, spice, day_value:int, data_format="DD-MM-YYYY"):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def set_menu_settings_general_date_time_date_month(self, spice, month_value:int):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_menu_settings_general_date_time_date_year(self, spice, year_value:int, data_format="DD-MM-YYYY"):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def set_menu_settings_general_date_time_date(self, spice, date, month, year, data_format="DD-MM-YYYY"):
        """
        set menu settings general date time date
        UI should be in Menu -> Settings-> General -> Date and Time -> Date screen
        data_format: must be in "DD-MM-YYYY"/"MM-DD-YYYY"/"YYYY-MM-DD"
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_apply_btn_at_date_screen(self, spice):
        '''
        Click Apply button at date screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def get_max_brightness_slider_value(self, spice):
        '''
        UI should be in Menu -> Setting -> General -> Display screen.
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_menu_settings_general_date_time_option_time_zone(self, spice, net):
        '''
        Check Time Zone option
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_menu_settings_general_date_time_option_date(self, spice, net):
        '''
        Check Date option
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def check_menu_settings_general_date_time_option_time(self, spice, net):
        '''
        Check Time option
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_options_menu_settings_general_date_time(self, spice, net):
        '''
        Get all options from date and time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_datetime_date_dateformat(self,spice):
        '''
        Negative to Menu->General->Date and Time ->Date ->Date Format screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_date_format_option_on_dateformat_screen(self, spice, option):
        '''
        select date format option on date format screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_date_format_reflect_on_date_time_screen(self, spice, date_format):
        '''
        Verify date format reflect successfully on date time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_yyyymmdd_date_format_on_datetime_screen(self, date):
        '''
        Check date format if yyyymmdd
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_mmddyyyy_date_format_on_datetime_screen(self, date):
        '''
        Check date format if mmddyyyy
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_ddmmyyyy_date_format_on_datetime_screen(self, date):
        '''
        Check date format if ddmmyyyy
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_date_format_on_datetime_screen(self, date):
        '''
        get the date format for the current date
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_menu_settings_general_datetime_time_timeformat(self,spice):
        '''
        Negative to Menu->General->Date and Time ->Time ->Time Format screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def select_time_format_option_on_timeformat_screen(self, spice, option):
        '''
        select time format option on time format screen
        option: string ->hr12 or hr24
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def click_apply_btn_at_time_screen(self, spice):
        '''
        Click Apply button at time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_time_value_on_menu_settings_general_dateTime(self, spice):
        '''
        Get time value on date and time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def is_ampm_time_format_on_datetime_screen(self, time):
        '''
        Check time format if 12 hr
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_time_format_on_datetime_screen(self, time):
        '''
        get the time format for the current time
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_time_format_reflect_on_date_time_screen(self, spice, time_format):
        '''
        Verify time format reflect successfully on date time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def get_time_zone_value_on_menu_settings_general_dateTime(self, spice):
        '''
        Get time zone value on date and time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_time_zone_reflect_on_date_time_screen(self, spice, net, time_zone):
        '''
        Verify time zone reflect successfully on date time screen
        '''
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
