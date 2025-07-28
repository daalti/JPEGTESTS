import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A3_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3_Mono_600.urf=faf1231ecb1058fc5b3f96e589450bb21c40690349c0176a64b40a3f0bd84447
    +name:test_urf_a3_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a3_mono_600
        +guid:80bd66e8-172b-4c52-a575-d3123d89adbc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a3_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
    
    printjob.print_verify('faf1231ecb1058fc5b3f96e589450bb21c40690349c0176a64b40a3f0bd84447')
    outputsaver.save_output()
    tray.reset_trays()
