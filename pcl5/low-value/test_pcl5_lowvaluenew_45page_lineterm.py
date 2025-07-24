import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 45Page_lineterm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:45Page-lineterm.obj=2015dd02b31ae61c02b0ff2013400c6417e8e53cb44d7cdb1e66bab6bd267db9
    +test_classification:System
    +name: test_pcl5_lowvaluenew_45page_lineterm
    +test:
        +title: test_pcl5_lowvaluenew_45page_lineterm
        +guid:e12b9b8a-54d8-465c-a450-2e44a5b93dbd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_45page_lineterm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2015dd02b31ae61c02b0ff2013400c6417e8e53cb44d7cdb1e66bab6bd267db9', timeout=600)
    outputsaver.save_output()
