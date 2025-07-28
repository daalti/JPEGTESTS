import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **om_small_photo_100x150mm_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:om_small_photo_100x150mm_Mono.urf=02e9a7f9c9d6481ef8b88580dcb4ebb2dc458f4ec9e12ba172a9da648fb10c90
    +name:test_urf_om_small_photo_100x150mm_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_om_small_photo_100x150mm_mono
        +guid:0739430d-a664-4646-ba9e-82c1d61463ae
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_small-photo_100x150mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_om_small_photo_100x150mm_mono(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_small-photo_100x150mm', default):
        tray.configure_tray(default, 'om_small-photo_100x150mm', 'stationery')

    printjob.print_verify('02e9a7f9c9d6481ef8b88580dcb4ebb2dc458f4ec9e12ba172a9da648fb10c90')
    outputsaver.save_output()
    tray.reset_trays()
