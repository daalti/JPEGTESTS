import pytest
import logging
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **columbia.hpg
    +test_tier:1
    +is_manual:False
    +reqid:Dune-63249
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:columbia.hpg=2dcdb1efce3e7e3bb0b8545393760e5716b0f596054c714a249b5ef7d1bb1739
    +test_classification:System
    +name:test_hpgl2_basic_functionality_columbia
    +test:
        +title:test_hpgl2_basic_functionality_columbia
        +guid:26e3331e-8898-4f8f-b7a8-156a8dfd77b7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_columbia(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2dcdb1efce3e7e3bb0b8545393760e5716b0f596054c714a249b5ef7d1bb1739')
    outputsaver.save_output()

logging.info("columbia Page - Print job completed successfully")