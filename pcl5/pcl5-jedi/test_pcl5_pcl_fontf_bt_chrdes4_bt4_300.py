import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt4_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt4_300.obj=9862bb7fc12388ba0e49cce46e0fc2c2a66a404e8a1884ed2f09ade7a8874511
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt4_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt4_300
        +guid:fd24ae00-bd26-4a98-8460-bab73a915270
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt4_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9862bb7fc12388ba0e49cce46e0fc2c2a66a404e8a1884ed2f09ade7a8874511', timeout=600)
    outputsaver.save_output()
