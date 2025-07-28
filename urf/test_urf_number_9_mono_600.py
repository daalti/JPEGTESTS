import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Number_9_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number_9_Mono_600.urf=3e091270125d982ed891f73d6f3705cb1d2a664e0a7dc11cfe6ab9cde1c78d2b
    +name:test_urf_number_9_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_9_mono_600
        +guid:0338178d-25f7-45ad-afda-caf403766439
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-9_3.875x8.875in &  MediaInputInstalled=Tray3

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_9_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-9_3.875x8.875in', default):
        tray.configure_tray(default, 'na_number-9_3.875x8.875in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('3e091270125d982ed891f73d6f3705cb1d2a664e0a7dc11cfe6ab9cde1c78d2b')
    outputsaver.save_output()
    tray.reset_trays()
