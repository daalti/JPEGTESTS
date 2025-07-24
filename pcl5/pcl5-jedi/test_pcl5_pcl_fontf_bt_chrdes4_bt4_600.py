import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt4_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt4_600.obj=3da0bfd93537543786b0be5f87dd856a028b869149c547ee82b5d604b5730821
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt4_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt4_600
        +guid:8384373e-f492-4400-85a1-ebea582a8394
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt4_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3da0bfd93537543786b0be5f87dd856a028b869149c547ee82b5d604b5730821', timeout=600)
    outputsaver.save_output()
