import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **CancelOperationTestFile.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CancelOperationTestFile.urf=2eb242c470c8d2b3a21b46b58fce083bdbf26b6428b12b9d4a3862296e64f4b3
    +name:test_urf_cancel_operation
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_cancel_operation
        +guid:9755572a-9454-46b4-938e-e16689a6e64e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_cancel_operation(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2eb242c470c8d2b3a21b46b58fce083bdbf26b6428b12b9d4a3862296e64f4b3')
    outputsaver.save_output()
