import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt8_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt8_300.obj=67aa648e5d82d6c415aada81bca62093fd2bbd9a18435480329e11644ee0abff
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt8_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt8_300
        +guid:02fa5a42-b90a-4a14-8236-53c74ae555bc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt8_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('67aa648e5d82d6c415aada81bca62093fd2bbd9a18435480329e11644ee0abff', timeout=300)
    outputsaver.save_output()
