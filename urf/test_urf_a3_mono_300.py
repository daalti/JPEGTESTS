import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A3_Mono_300.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3_Mono_300.urf=d8dd81c376e6dfced1cafe9845e6f210ef2c8dc298e7af94c8ff94d37c0df427
    +name:test_urf_a3_mono_300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a3_mono_300
        +guid:c14aa27c-be28-4d80-8020-cfb76cda64ca
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a3_mono_300(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
    
    printjob.print_verify('d8dd81c376e6dfced1cafe9845e6f210ef2c8dc298e7af94c8ff94d37c0df427')
    outputsaver.save_output()
    tray.reset_trays()
