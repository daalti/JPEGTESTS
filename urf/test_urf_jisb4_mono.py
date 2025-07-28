import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **JISB4_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JISB4_Mono.urf=c11e8d325bb4e020402ab593f6a15119f332daa6a7c6155d0f6ec7f0b6102ba6
    +name:test_urf_jisb4_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_jisb4_mono
        +guid:9a10ba99-d229-4859-9b01-3f20f4de7ddf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_jisb4_mono(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()

    if tray.is_size_supported('jis_b4_257x364mm', default):
        tray.configure_tray(default, 'jis_b4_257x364mm', 'stationery')
    
    printjob.print_verify('c11e8d325bb4e020402ab593f6a15119f332daa6a7c6155d0f6ec7f0b6102ba6')
    outputsaver.save_output()
    tray.reset_trays()
