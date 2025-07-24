import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 13Page_bt3_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-bt3_300.obj=cd14b2b9b1c388fe49d90c2b4e0300450fff5ad2cdbda438aa34cda35e135528
    +test_classification:System
    +name: test_pcl5_lowvaluenew_13page_bt3_300
    +test:
        +title: test_pcl5_lowvaluenew_13page_bt3_300
        +guid:eafeadb7-a2cc-44d9-8776-cdcb263277b8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_13page_bt3_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cd14b2b9b1c388fe49d90c2b4e0300450fff5ad2cdbda438aa34cda35e135528', timeout=600)
    outputsaver.save_output()
