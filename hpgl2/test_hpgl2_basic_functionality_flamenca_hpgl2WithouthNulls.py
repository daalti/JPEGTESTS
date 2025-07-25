import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **flamenca_hpgl2WithouthNulls.prn 
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:240
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:flamenca_hpgl2WithouthNulls.prn=3749b8704eec618a3189e6150277b2b0a490a8bf5f1085010ebcce186b261aa0
    +test_classification:System
    +name:test_hpgl2_basic_functionality_flamenca_hpgl2WithouthNulls
    +test:
        +title:test_hpgl2_basic_functionality_flamenca_hpgl2WithouthNulls
        +guid:3b5868f5-8f26-4c4f-8ffa-aaabde1fb167
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_flamenca_hpgl2WithouthNulls(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3749b8704eec618a3189e6150277b2b0a490a8bf5f1085010ebcce186b261aa0')
    outputsaver.save_output()

    logging.info("flamenca_hpgl2WithouthNulls Page - Print job completed successfully")
