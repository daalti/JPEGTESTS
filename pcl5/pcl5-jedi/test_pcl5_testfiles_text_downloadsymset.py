import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using downloadSymSet.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:downloadSymSet.pcl=c3076d2d8a97af2f1ba647d788f558575afb051313f19013a4a17be7cfc4049b
    +test_classification:System
    +name: test_pcl5_testfiles_text_downloadsymset
    +test:
        +title: test_pcl5_testfiles_text_downloadsymset
        +guid:149e6a52-23a6-421a-a244-9e26eca22763
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_downloadsymset(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c3076d2d8a97af2f1ba647d788f558575afb051313f19013a4a17be7cfc4049b', timeout=600)
    outputsaver.save_output()
