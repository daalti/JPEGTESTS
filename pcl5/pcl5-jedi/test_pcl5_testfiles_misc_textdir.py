import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using textDir.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:textDir.pcl=7f53eaaf3a5f1faf77b780a1cd4a175dbb04c5689256cec8e658cacb40fa902f
    +test_classification:System
    +name: test_pcl5_testfiles_misc_textdir
    +test:
        +title: test_pcl5_testfiles_misc_textdir
        +guid:2e23473f-a817-4e88-9d97-f44352d812b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_textdir(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7f53eaaf3a5f1faf77b780a1cd4a175dbb04c5689256cec8e658cacb40fa902f', timeout=600)
    outputsaver.save_output()
