import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcp.obj=5b051f8e6bfefe6e6cc825b0774c888798f345423701f0c01d32d23da431e393
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcp
        +guid:dbbb82d4-17c9-426a-901e-327f4803ede7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b051f8e6bfefe6e6cc825b0774c888798f345423701f0c01d32d23da431e393', timeout=600)
    outputsaver.save_output()
