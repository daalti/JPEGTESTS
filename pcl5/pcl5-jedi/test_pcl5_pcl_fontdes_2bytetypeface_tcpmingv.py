import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpmingv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpmingv.obj=d8812203309c41075bf6303e9141cc1006d07ba49758b59b02a376c70d9d8a2f
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingv
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingv
        +guid:b9fa32f4-af67-4233-9427-220b5738d013
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpmingv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d8812203309c41075bf6303e9141cc1006d07ba49758b59b02a376c70d9d8a2f', timeout=600)
    outputsaver.save_output()
