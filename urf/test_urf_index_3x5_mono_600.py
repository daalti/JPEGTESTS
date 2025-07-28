import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Index_3x5_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_3x5_Mono_600.urf=0cad346c19911adc54169a036ef777999fc35bc024159e140c6c170ff282f05e
    +name:test_urf_index_3x5_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_3x5_mono_600
        +guid:1d82c04c-1549-4564-a19b-007b7d60d87c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-3x5_3x5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_3x5_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-3x5_3x5in', default):
        tray.configure_tray(default, 'na_index-3x5_3x5in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('0cad346c19911adc54169a036ef777999fc35bc024159e140c6c170ff282f05e')
    outputsaver.save_output()
    tray.reset_trays()
