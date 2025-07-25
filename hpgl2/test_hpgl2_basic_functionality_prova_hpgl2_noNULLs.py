import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **prova_hpgl2_noNULLs.plt
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:prova_hpgl2_noNULLs.plt=a6f2a50129e13409fab27a4bb4b07aaff4f77e4be8c7d395bd7ca877270102be
    +test_classification:System
    +name:test_hpgl2_basic_functionality_prova_hpgl2_noNULLs
    +test:
        +title:test_hpgl2_basic_functionality_prova_hpgl2_noNULLs
        +guid:cdabaa3f-9295-4beb-8fe7-baa2a8b3dfe9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_prova_hpgl2_noNULLs(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a6f2a50129e13409fab27a4bb4b07aaff4f77e4be8c7d395bd7ca877270102be')
    outputsaver.save_output()

    logging.info("prova_hpgl2_noNULLs Page - Print job completed successfully")