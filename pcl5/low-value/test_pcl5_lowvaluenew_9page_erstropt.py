import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 9Page_erstropt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:9Page-erstropt.obj=07444dd6a4f09e73cc212dd47a7f34f5377bec8baf5d84b9b5c0bf0f366a5aac
    +test_classification:System
    +name: test_pcl5_lowvaluenew_9page_erstropt
    +test:
        +title: test_pcl5_lowvaluenew_9page_erstropt
        +guid:a5d12db4-a6d5-4a5c-bca9-e11a41ac5d90
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_9page_erstropt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('07444dd6a4f09e73cc212dd47a7f34f5377bec8baf5d84b9b5c0bf0f366a5aac', timeout=600)
    outputsaver.save_output()
