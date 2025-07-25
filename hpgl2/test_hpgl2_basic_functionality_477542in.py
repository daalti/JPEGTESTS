import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **477542in.plt
    +test_tier:1
    +is_manual:False    
    +reqid:Dune-45716
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:477542in.plt=2ee7a44078cecd09a1532d70b14139e30a01a12656646a1b16f09a215baa9d14
    +test_classification:System
    +name:test_hpgl2_basic_functionality_477542in
    +test:
        +title:test_hpgl2_basic_functionality_477542in
        +guid:bea4fd4f-443e-4c19-8361-a11d965073ad
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_477542in(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2ee7a44078cecd09a1532d70b14139e30a01a12656646a1b16f09a215baa9d14')
    outputsaver.save_output()

    logging.info("477542in Page - Print job completed successfully")