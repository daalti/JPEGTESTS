import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt6_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt6_600.obj=2bc190207dc231fc688eafb68e503d8c5f7aa48fb70d7926495f6446d8a6420e
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt6_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt6_600
        +guid:b6e78938-f1d8-4f0b-a770-ff4b11d6a79a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt6_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2bc190207dc231fc688eafb68e503d8c5f7aa48fb70d7926495f6446d8a6420e', timeout=600)
    outputsaver.save_output()
