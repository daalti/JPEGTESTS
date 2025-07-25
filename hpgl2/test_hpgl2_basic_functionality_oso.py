import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:HPGL2 basic functionality test using **oso.prn
    +test_tier:1
    +is_manual:False
    +reqid:Dune-45716
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:oso.prn=d28e46ac4b04c6235b2902bf8594b6565c68d6f8137cbc80115be6a9cc542c49
    +test_classification:System
    +name:test_hpgl2_basic_functionality_oso
    +test:
        +title:test_hpgl2_basic_functionality_oso
        +guid:9bb20a08-1fa0-4ca0-9c27-853315c4ab94
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_basic_functionality_oso(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d28e46ac4b04c6235b2902bf8594b6565c68d6f8137cbc80115be6a9cc542c49')
    outputsaver.save_output()

    logging.info("oso Page - Print job completed successfully")