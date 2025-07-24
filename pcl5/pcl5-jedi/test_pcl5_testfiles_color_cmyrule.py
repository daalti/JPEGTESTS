import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cmyRule.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cmyRule.pcl=67dbdf6a5f2349939360ab5c4aec7804667e33fa2a42d0751482d69113fc1034
    +test_classification:System
    +name: test_pcl5_testfiles_color_cmyrule
    +test:
        +title: test_pcl5_testfiles_color_cmyrule
        +guid:4b55ddb1-e51a-4017-8e80-6e1ed5fb8ba2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_color_cmyrule(setup_teardown, printjob, outputsaver):
    printjob.print_verify('67dbdf6a5f2349939360ab5c4aec7804667e33fa2a42d0751482d69113fc1034',timeout=600)
    outputsaver.save_output()
