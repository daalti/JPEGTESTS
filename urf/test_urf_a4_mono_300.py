import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A4_Mono_300.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Mono_300.urf=2871f1e2137609ba01c88b99a5a0a938721aa7e0b5d5d8b85d86ce414c00a55c
    +name:test_urf_a4_mono_300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a4_mono_300
        +guid:09799137-d9c2-49d3-b5f7-7dda311e1c2b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a4_mono_300(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('2871f1e2137609ba01c88b99a5a0a938721aa7e0b5d5d8b85d86ce414c00a55c')
    outputsaver.save_output()
    tray.reset_trays()
