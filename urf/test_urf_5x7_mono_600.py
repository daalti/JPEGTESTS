import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **5x7_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5x7_Mono_600.urf=0a667bc8fd74a20edc53d3d6953b16d3022582551266254c210229ac2c3fb713
    +name:test_urf_5x7_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_5x7_mono_600
        +guid:376c7733-b023-44f5-a56b-b831e801bf50
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_5x7_5x7in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_5x7_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index_5x7_5x7in', default):
        tray.configure_tray(default, 'na_index_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('na_5x7_5x7in', default):
        tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('0a667bc8fd74a20edc53d3d6953b16d3022582551266254c210229ac2c3fb713')
    outputsaver.save_output()
    tray.reset_trays()
