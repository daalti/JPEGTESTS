import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **harley_a4.hpg
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:harley_a4.hpg=2ab8b39b7b4cad6ff07a0fb94d6ef8d00ff3d6ff17ba13b1d99e2062d984e83c
    +test_classification:System
    +name:test_hpgl2_basic_functionality_harley_a4
    +test:
        +title:test_hpgl2_basic_functionality_harley_a4
        +guid:2d92caf0-32f2-422b-9ec4-b11e28e5d975
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_harley_a4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2ab8b39b7b4cad6ff07a0fb94d6ef8d00ff3d6ff17ba13b1d99e2062d984e83c')
    outputsaver.save_output()

    logging.info("harley_a4 Page - Print job completed successfully")