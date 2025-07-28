import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A6_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A6_Mono_600.urf=56fae7357ce1896130fc0f7f43782e57e70b8fa3ea1937396f969890d3339bb5
    +name:test_urf_a6_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a6_mono_600
        +guid:ac861c6c-e180-40a1-888a-0367d3091c8c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a6_105x148mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a6_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a6_105x148mm', default):
        tray.configure_tray(default, 'iso_a6_105x148mm', 'stationery')

    printjob.print_verify('56fae7357ce1896130fc0f7f43782e57e70b8fa3ea1937396f969890d3339bb5')
    outputsaver.save_output()
    tray.reset_trays()
