import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using prspace.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:prspace.obj=20d6d57a80945fbedbf1acd270a0fb00324fe08ea33f7f477eae20bbee919388
    +test_classification:System
    +name: test_pcl5_pcl_fontr_bt_prspace
    +test:
        +title: test_pcl5_pcl_fontr_bt_prspace
        +guid:b338c4a6-9ee3-47f9-ac5f-36ad4637d5c8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_bt_prspace(setup_teardown, printjob, outputsaver):
    printjob.print_verify('20d6d57a80945fbedbf1acd270a0fb00324fe08ea33f7f477eae20bbee919388', timeout=600)
    outputsaver.save_output()
