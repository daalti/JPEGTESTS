import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 security vulnerability
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:pclpat.prn=9cfed0952cb371c6de7fc8a576d5f6c20899e48b13ba9ab235123916f21a54a7
    +name:test_pcl5_UseAfterFree
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_UseAfterFree
        +guid:6596a868-b257-481d-94bf-0b9e3060f3f5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_UseAfterFree(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('9cfed0952cb371c6de7fc8a576d5f6c20899e48b13ba9ab235123916f21a54a7')
    outputsaver.save_output() 