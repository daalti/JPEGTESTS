import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ctxtshad.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctxtshad.pcl=374cbb8e08a27fc67d5ef41c866273c0f483236257dc31401ce32d87fccab0b0
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_ctxtshad
    +test:
        +title: test_pcl5_testfiles_pattern_ctxtshad
        +guid:2da8c29e-b943-4b67-b9de-5663eaee7cb5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_ctxtshad(setup_teardown, printjob, outputsaver):
    printjob.print_verify('374cbb8e08a27fc67d5ef41c866273c0f483236257dc31401ce32d87fccab0b0', timeout=600)
    outputsaver.save_output()
