import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidRes-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidRes-3.pwg=3ba04371c66419d45f0c75d8793b6273eb7ca7911cc33cb5d693a929c864992a
    +name:test_pwg_negative_ph_only_invalid_resolution_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_resolution_3
        +guid:e8468be6-6b2e-4fc7-a836-63a73683e0c4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_resolution_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3ba04371c66419d45f0c75d8793b6273eb7ca7911cc33cb5d693a929c864992a', 'FAILED')
    outputsaver.save_output()
