import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mcroesce.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:mcroesce.obj=3588d96518d8922c1405fd4c8e87c6ab5b70a7b9337dc2e0a94e515b2dd8242b
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_mcroesce
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_mcroesce
        +guid:9d0ead49-b05e-4367-bf05-e583f68b9ac6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_mcroesce(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3588d96518d8922c1405fd4c8e87c6ab5b70a7b9337dc2e0a94e515b2dd8242b', timeout=600)
    outputsaver.save_output()
