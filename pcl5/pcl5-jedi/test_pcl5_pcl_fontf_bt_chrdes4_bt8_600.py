import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt8_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt8_600.obj=15105a57aaa1a11cae6972543062a96bfb1494a0d996924f4ce45891fcb9f4b2
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt8_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt8_600
        +guid:1e92936d-dca6-4d00-867d-cc78779fceb6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt8_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('15105a57aaa1a11cae6972543062a96bfb1494a0d996924f4ce45891fcb9f4b2', timeout=600)
    outputsaver.save_output()
