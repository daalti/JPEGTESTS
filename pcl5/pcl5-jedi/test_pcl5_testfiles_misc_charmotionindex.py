import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using charMotionIndex.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:charMotionIndex.pcl=96a3a457e03d9d2c9be866305dc5fd2f30e2e95b3191b0c88a54be94e9d528b3
    +test_classification:System
    +name: test_pcl5_testfiles_misc_charmotionindex
    +test:
        +title: test_pcl5_testfiles_misc_charmotionindex
        +guid:1baa8c2d-f900-446d-a901-88b60d73ca2d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_charmotionindex(setup_teardown, printjob, outputsaver):
    printjob.print_verify('96a3a457e03d9d2c9be866305dc5fd2f30e2e95b3191b0c88a54be94e9d528b3', timeout=600)
    outputsaver.save_output()
