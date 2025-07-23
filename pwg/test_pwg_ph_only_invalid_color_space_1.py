import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidColorspace-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:150
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidColorspace-1.pwg=295caed41e8e1e7487463c6867a70e3318d29f7f46639decfdb1893e06a18ad7
    +name:test_pwg_negative_ph_only_invalid_color_space_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_color_space_1
        +guid:b1dce84a-810a-4b03-b2bd-14ed11d62a26
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_color_space_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('295caed41e8e1e7487463c6867a70e3318d29f7f46639decfdb1893e06a18ad7', 'SUCCESS', timeout=150)
    outputsaver.save_output()
