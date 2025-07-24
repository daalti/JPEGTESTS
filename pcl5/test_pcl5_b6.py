import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:b6.pcl=650c187424b33c3636b91877f09d20f158e5d9d307a37161af192d199bc4d790
    +name:test_pcl5_b6
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_b6
        +guid:3d64d11c-d757-4614-a50c-1dc0b6cf73e5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_b6(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('650c187424b33c3636b91877f09d20f158e5d9d307a37161af192d199bc4d790')
    outputsaver.save_output()