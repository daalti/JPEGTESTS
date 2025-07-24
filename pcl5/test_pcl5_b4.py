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
    +external_files:b4.pcl=d1dd3f083ba21baddfd979700b56e3a3f9eab67d1c9d4fa1385cdf445c080116
    +name:test_pcl5_b4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_b4
        +guid:900c7972-1a3d-40d4-9c30-357faa032c87
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_b4(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('d1dd3f083ba21baddfd979700b56e3a3f9eab67d1c9d4fa1385cdf445c080116')
    outputsaver.save_output()