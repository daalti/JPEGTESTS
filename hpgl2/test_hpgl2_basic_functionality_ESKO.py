import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **ESKO.plt
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:ESKO.plt=1ef9cc2593dfa8451ef87c7796e2affae87d8d40ace307f48dfddf7c8a1d6245
    +test_classification:System
    +name:test_hpgl2_basic_functionality_ESKO
    +test:
        +title:test_hpgl2_basic_functionality_ESKO
        +guid:f2fc7e9b-3644-44ff-99f5-a2016da6be5f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_ESKO(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1ef9cc2593dfa8451ef87c7796e2affae87d8d40ace307f48dfddf7c8a1d6245')
    outputsaver.save_output()

    logging.info("ESKOPage - Print job completed successfully")