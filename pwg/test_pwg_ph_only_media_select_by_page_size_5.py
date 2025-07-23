import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MediaSelectByPageSize-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-5.pwg=cb965b3d16e9fd9bed3aa4c1723a25411d2e240d210f21a05d9e6f15fb009df9
    +name:test_pwg_ph_only_media_select_by_page_size_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_5
        +guid:b0987bf4-3081-44e0-b6cc-418064dae319
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_5(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')
    
    printjob.print_verify('cb965b3d16e9fd9bed3aa4c1723a25411d2e240d210f21a05d9e6f15fb009df9', 'FAILED')
    outputsaver.save_output()
    tray.reset_trays()
