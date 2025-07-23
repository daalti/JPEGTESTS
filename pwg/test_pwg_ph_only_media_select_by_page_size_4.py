import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MediaSelectByPageSize-4.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-4.pwg=1aa27c4404bd271df7132c13335ae93c01da629642f178e182874b7390a820c7
    +name:test_pwg_ph_only_media_select_by_page_size_4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_4
        +guid:e4105b71-efff-46cb-a005-71dd1aad072b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_4(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('1aa27c4404bd271df7132c13335ae93c01da629642f178e182874b7390a820c7')
    outputsaver.save_output()
    tray.reset_trays()
