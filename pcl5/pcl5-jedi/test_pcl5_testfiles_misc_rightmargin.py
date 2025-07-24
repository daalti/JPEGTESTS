import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using rightmargin.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rightmargin.pcl=0925ac1251e8c9cfc48247907277ea3b15a5309e832988a8b67f73765d422b5d
    +test_classification:System
    +name: test_pcl5_testfiles_misc_rightmargin
    +test:
        +title: test_pcl5_testfiles_misc_rightmargin
        +guid:102b9876-7bf5-481e-9c90-4f82aa5be8a4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_rightmargin(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0925ac1251e8c9cfc48247907277ea3b15a5309e832988a8b67f73765d422b5d', timeout=600)
    outputsaver.save_output()
