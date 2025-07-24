import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using driver.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:driver.pcl=b8bc13909c9e88ea4a648f5f866d2f2d7400b26c06ddcb4840e1d797a1a1b678
    +test_classification:System
    +name: test_pcl5_allocidcoverage_driver
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_allocidcoverage_driver
        +guid:4a42cc12-0d94-4931-bf28-f1a353ef4225
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_driver(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b8bc13909c9e88ea4a648f5f866d2f2d7400b26c06ddcb4840e1d797a1a1b678', timeout=600)
    outputsaver.save_output()
