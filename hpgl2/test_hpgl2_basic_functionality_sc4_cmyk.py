import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **sc4-cmyk.plt
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:sc4-cmyk.plt=4018acd649646fb0f86395f7b24be029f8e68edb5ea569026744e99158449248
    +test_classification:System
    +name:test_hpgl2_basic_functionality_sc4_cmyk
    +test:
        +title:test_hpgl2_basic_functionality_sc4_cmyk
        +guid:eb60da37-9a85-46b0-b35d-fd7dea35395d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_sc4_cmyk(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4018acd649646fb0f86395f7b24be029f8e68edb5ea569026744e99158449248')
    outputsaver.save_output()

    logging.info("sc4-cmyk Page - Print job completed successfully")