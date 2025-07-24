import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scskai.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scskai.obj=5e6b3d95968dfda324998c092947c4c1ea5b904262b311c95f95dcb3a6be0c28
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scskai
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scskai
        +guid:622b85bf-0ef5-4c49-a076-357cdb7a21fb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scskai(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5e6b3d95968dfda324998c092947c4c1ea5b904262b311c95f95dcb3a6be0c28', timeout=600)
    outputsaver.save_output()
