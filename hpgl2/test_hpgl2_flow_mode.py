import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job through flow mode (A1N)
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191697
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:catala1.rtl=ee6d69bc8de9934b366039898bab17ed71cb8d27bd79ee39a7f01ac05d53ae18
    +test_classification:System
    +name:test_hpgl2_flow_mode
    +test:
        +title:test_hpgl2_flow_mode
        +guid:ec658d46-93ba-46fb-8336-e48defcc5e5d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_hpgl2_flow_mode(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ee6d69bc8de9934b366039898bab17ed71cb8d27bd79ee39a7f01ac05d53ae18')
    outputsaver.save_output()

    logging.info("catala1.rtl - Print job completed successfully")