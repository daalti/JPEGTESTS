import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt3_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt3_600.obj=ba64499a8e1c4f358f57ba98c4a3330b8219a13e0bc3a075e71cef1e972b205e
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt3_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt3_600
        +guid:6b484f28-8328-422c-a4d2-725da77f9753
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt3_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ba64499a8e1c4f358f57ba98c4a3330b8219a13e0bc3a075e71cef1e972b205e', timeout=600)
    outputsaver.save_output()
