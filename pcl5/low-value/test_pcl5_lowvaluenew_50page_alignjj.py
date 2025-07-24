import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 50Page_alignjj.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:50Page-alignjj.obj=78c4d8ed3a4bb3d086413aa9b75c01935ff84c2545a796e58e2bed570537a51a
    +test_classification:System
    +name: test_pcl5_lowvaluenew_50page_alignjj
    +test:
        +title: test_pcl5_lowvaluenew_50page_alignjj
        +guid:74fee6a7-cd83-42a1-919a-aa8e2ba61a6b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_50page_alignjj(setup_teardown, printjob, outputsaver):
    printjob.print_verify('78c4d8ed3a4bb3d086413aa9b75c01935ff84c2545a796e58e2bed570537a51a', timeout=600)
    outputsaver.save_output()
