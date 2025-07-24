import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt10_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt10_300.obj=d3a1005a29dd7c98f24b64013e5cd19a34c3b0d4d484b1f76008e34432d0edbc
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt10_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt10_300
        +guid:20572b33-ab5d-48fb-8b49-159251e0a904
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt10_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d3a1005a29dd7c98f24b64013e5cd19a34c3b0d4d484b1f76008e34432d0edbc', timeout=600)
    outputsaver.save_output()
