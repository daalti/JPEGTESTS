import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-InvalidRes-1.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidRes-1.pwg=e40cf2498e0c93693c3925a72806922082019946cb59c402cb4a10b305324d5c
    +name:test_pwg_negative_ph_only_invalid_resolution_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_resolution_1
        +guid:70f103b6-552f-4f0f-8de0-91b27db44829
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_resolution_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e40cf2498e0c93693c3925a72806922082019946cb59c402cb4a10b305324d5c')
    outputsaver.save_output()
