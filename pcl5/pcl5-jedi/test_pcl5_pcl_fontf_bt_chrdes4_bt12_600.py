import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt12_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt12_600.obj=0935c177c18d9800e25fb895287666dab63161db073df358f5b3dec817ab77bf
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt12_600
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt12_600
        +guid:4b919047-3853-4428-92d8-c4f7be35fe06
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt12_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0935c177c18d9800e25fb895287666dab63161db073df358f5b3dec817ab77bf', timeout=600)
    outputsaver.save_output()
