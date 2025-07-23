import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-Orientation-3.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-Orientation-3.pwg=fbbc9e80fe2924e339ed56d176ff404d5b3a81a7cd0b52c84dc8b8f78001c4ab
    +name:test_pwg_ph_only_orientation_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_orientation_3
        +guid:6af51e76-9669-492d-b7dd-8bc08041d585
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_orientation_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fbbc9e80fe2924e339ed56d176ff404d5b3a81a7cd0b52c84dc8b8f78001c4ab')
    outputsaver.save_output()
