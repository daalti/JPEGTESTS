import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **10_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number-10_Mono_600.urf=c360d1c5ef0079781d4a5037ab3bf35a66df365cbb4e3edd610e3576fb3b3df1
    +name:test_urf_number_10_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_10_mono_600
        +guid:0f1713bd-0a2f-4c79-b96d-37b8a36070f5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_10_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')

    printjob.print_verify('c360d1c5ef0079781d4a5037ab3bf35a66df365cbb4e3edd610e3576fb3b3df1')
    outputsaver.save_output()
    tray.reset_trays()
