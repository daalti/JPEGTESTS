import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using locpr_nc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:locpr_nc.obj=4ba732a1f9f2da92f558bc4d7180d8ae274ede71386311732bcbbccb9851e9ac
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_locpr_nc
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_locpr_nc
        +guid:c96f616f-11c9-47c0-92e3-2d9f4f01ad94
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_locpr_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4ba732a1f9f2da92f558bc4d7180d8ae274ede71386311732bcbbccb9851e9ac', timeout=600)
    outputsaver.save_output()
