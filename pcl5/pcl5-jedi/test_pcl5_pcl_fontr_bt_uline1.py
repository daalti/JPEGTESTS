import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using uline1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:uline1.obj=7d3098405369b61418370d315a0244b641c7b81438344074965f3858e93d7e1b
    +test_classification:System
    +name: test_pcl5_pcl_fontr_bt_uline1
    +test:
        +title: test_pcl5_pcl_fontr_bt_uline1
        +guid:2182b2f6-7079-48bc-9e44-fafa279fc749
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_bt_uline1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7d3098405369b61418370d315a0244b641c7b81438344074965f3858e93d7e1b', timeout=600)
    outputsaver.save_output()
