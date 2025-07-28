import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Index_4x6_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_4x6_Mono_600.urf=36044297b3448dad4d9efcf682a6b2e984852dbcc69e0543b50623d9f642aeca
    +name:test_urf_index_4x6_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_4x6_mono_600
        +guid:4292fdc4-fc30-46cb-981d-887e858bdb86
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_4x6_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')

    printjob.print_verify('36044297b3448dad4d9efcf682a6b2e984852dbcc69e0543b50623d9f642aeca')
    outputsaver.save_output()
    tray.reset_trays()
