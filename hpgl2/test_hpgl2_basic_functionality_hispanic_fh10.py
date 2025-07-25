import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **hispanic_fh10.hpg
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716   
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:hispanic_fh10.hpg=f43706cd4d4c6cee399c0830f348a06d806ea378b22028321c4384dd0166ad96
    +test_classification:System
    +name:test_hpgl2_basic_functionality_hispanic_fh10
    +test:
        +title:test_hpgl2_basic_functionality_hispanic_fh10
        +guid:3bc6b228-6931-424e-b8f3-58c3b64fd34b
        +dut:
            +type:Simulator,Emulator,Engine
            +configuration: DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_hispanic_fh10(setup_teardown, counters, printjob, outputsaver):
    printjob.print_verify('f43706cd4d4c6cee399c0830f348a06d806ea378b22028321c4384dd0166ad96')
    outputsaver.save_output()

    logging.info("hispanic_fh10 Page - Print job completed successfully")