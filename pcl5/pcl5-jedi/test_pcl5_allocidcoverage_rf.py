import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using rf.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rf.pcl=dee626b17fdf9fc4c60ac50c5f19a42f57449c88439aaeaa38e82e88a36d4b7d
    +test_classification:System
    +name: test_pcl5_allocidcoverage_rf
    +test:
        +title: test_pcl5_allocidcoverage_rf
        +guid:95ca646a-d635-4bb9-8cfa-a0c3c9fa7cca
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_rf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dee626b17fdf9fc4c60ac50c5f19a42f57449c88439aaeaa38e82e88a36d4b7d', timeout=600)
    outputsaver.save_output()
