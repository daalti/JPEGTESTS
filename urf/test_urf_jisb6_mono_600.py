import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **JISB6_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JISB6_Mono_600.urf=6db41effce512af1f274179bfb5f42d2157ca2100574247846db65c15c3ad2e9
    +name:test_urf_jisb6_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_jisb6_mono_600
        +guid:72d97971-0854-4608-9e1c-8a4d4c2e58ae
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jis_b6_128x182mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_jisb6_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jis_b6_128x182mm', default):
        tray.configure_tray(default, 'jis_b6_128x182mm', 'stationery')
    
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('6db41effce512af1f274179bfb5f42d2157ca2100574247846db65c15c3ad2e9')
    outputsaver.save_output()
    tray.reset_trays()
