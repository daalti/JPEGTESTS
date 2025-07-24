import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt14_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt14_600.obj=376c9598f31df00ff3b2c8560f1beb4f2e46a6c6cb2dc893c57dc613cec98a13
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt14_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt14_600
        +guid:da590490-90bc-471f-82c5-97fc3ec682ac
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt14_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('376c9598f31df00ff3b2c8560f1beb4f2e46a6c6cb2dc893c57dc613cec98a13', timeout=600)
    outputsaver.save_output()
