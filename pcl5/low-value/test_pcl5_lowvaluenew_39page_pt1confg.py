import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 39Page_pt1confg.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:39Page-pt1confg.obj=622d0a90edbf9680239ab9b0de9d5369e89076dd246293c8b2e24f0a568e760e
    +test_classification:System
    +name: test_pcl5_lowvaluenew_39page_pt1confg
    +test:
        +title: test_pcl5_lowvaluenew_39page_pt1confg
        +guid:98fb20e7-324f-4de8-893f-aa69ed9f510c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_39page_pt1confg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('622d0a90edbf9680239ab9b0de9d5369e89076dd246293c8b2e24f0a568e760e', timeout=600)
    outputsaver.save_output()
