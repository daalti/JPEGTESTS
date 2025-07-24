import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt14_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt14_300.obj=4473e1fcc4db97a3199aa7f11cf4f2b9cc1e57e12bc01943ad91f097c785386c
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt14_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt14_300
        +guid:c5f934bc-8e0a-4dcd-a4ea-6f255b2d0c31
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt14_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4473e1fcc4db97a3199aa7f11cf4f2b9cc1e57e12bc01943ad91f097c785386c', timeout=600)
    outputsaver.save_output()
