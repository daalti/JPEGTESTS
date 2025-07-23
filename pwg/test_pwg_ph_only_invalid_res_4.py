import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidRes-4.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidRes-4.pwg=38a6e4e6d09137f2eaa592b5c5b71ba2db4102c67469b2c483f5afe7c45a0fdd
    +name:test_pwg_negative_ph_only_invalid_resolution_4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_resolution_4
        +guid:f50a685e-5ea3-48b2-a1b1-6b6be89651aa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_resolution_4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('38a6e4e6d09137f2eaa592b5c5b71ba2db4102c67469b2c483f5afe7c45a0fdd', 'FAILED')
    outputsaver.save_output()
