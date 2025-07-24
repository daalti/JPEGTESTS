import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 9Page_bt5_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:9Page-bt5_600.obj=31e3ab17036ae365378f2f0c294dbcca969288fc8a1094134e50447478c62f0a
    +test_classification:System
    +name: test_pcl5_lowvaluenew_9page_bt5_600
    +test:
        +title: test_pcl5_lowvaluenew_9page_bt5_600
        +guid:3de74059-c5fd-4a27-8596-58032777b1c4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_9page_bt5_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('31e3ab17036ae365378f2f0c294dbcca969288fc8a1094134e50447478c62f0a', timeout=600)
    outputsaver.save_output()
