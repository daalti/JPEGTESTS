import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **InvalidURFTest.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:InvalidURFTest.urf=ccef8ab504cd6c7b190ab6f187834a764a76b21617639a0ebb567d3ddcd534e1
    +name:test_urf_invalid_urf
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_invalid_urf
        +guid:f4355bdb-ae31-486b-b3b8-7e3facf36f73
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_invalid_urf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ccef8ab504cd6c7b190ab6f187834a764a76b21617639a0ebb567d3ddcd534e1', 'FAILED')
    outputsaver.save_output()
