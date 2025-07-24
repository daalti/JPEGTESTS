import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt6_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt6_300.obj=a04750aa578af9b4837e9262b2f38758230c85bd59ea5aa4671c52658b0ababc
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt6_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt6_300
        +guid:614da1bb-f030-42b5-bd2c-9ce762840054
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt6_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a04750aa578af9b4837e9262b2f38758230c85bd59ea5aa4671c52658b0ababc', timeout=600)
    outputsaver.save_output()
